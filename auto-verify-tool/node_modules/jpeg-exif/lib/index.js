'use strict';

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var tags = require('./tags.json');

/*
 unsignedByte,
 asciiStrings,
 unsignedShort,
 unsignedLong,
 unsignedRational,
 signedByte,
 undefined,
 signedShort,
 signedLong,
 signedRational,
 singleFloat,
 doubleFloat
 */
var bytes = [0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8];
var SOIMarkerLength = 2;
var JPEGSOIMarker = 0xffd8;
var TIFFINTEL = 0x4949;
var TIFFMOTOROLA = 0x4d4d;
var APPMarkerLength = 2;
var APPMarkerBegin = 0xffe0;
var APPMarkerEnd = 0xffef;
var data = void 0;
/**
 * @param buffer {Buffer}
 * @returns {Boolean}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var isImage = isValid(content);
 * console.log(isImage);
 */
var isValid = function isValid(buffer) {
  try {
    var SOIMarker = buffer.readUInt16BE(0);
    return SOIMarker === JPEGSOIMarker;
  } catch (e) {
    throw new Error('Unsupport file format.');
  }
};
/**
 * @param buffer {Buffer}
 * @returns {Boolean}
 * @example
 */
var isTiff = function isTiff(buffer) {
  try {
    var SOIMarker = buffer.readUInt16BE(0);
    return SOIMarker === TIFFINTEL || SOIMarker === TIFFMOTOROLA;
  } catch (e) {
    throw new Error('Unsupport file format.');
  }
};
/**
 * @param buffer {Buffer}
 * @returns {Number}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var APPNumber = checkAPPn(content);
 * console.log(APPNumber);
 */
var checkAPPn = function checkAPPn(buffer) {
  try {
    var APPMarkerTag = buffer.readUInt16BE(0);
    var isInRange = APPMarkerTag >= APPMarkerBegin && APPMarkerTag <= APPMarkerEnd;
    return isInRange ? APPMarkerTag - APPMarkerBegin : false;
  } catch (e) {
    throw new Error('Invalid APP Tag.');
  }
};
/**
 * @param buffer {Buffer}
 * @param tagCollection {Object}
 * @param order {Boolean}
 * @param offset {Number}
 * @returns {Object}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var exifFragments = IFDHandler(content, 0, true, 8);
 * console.log(exifFragments.value);
 */
var IFDHandler = function IFDHandler(buffer, tagCollection, order, offset) {
  var entriesNumber = order ? buffer.readUInt16BE(0) : buffer.readUInt16LE(0);

  if (entriesNumber === 0) {
    return {};
  }

  var entriesNumberLength = 2;
  var entries = buffer.slice(entriesNumberLength);
  var entryLength = 12;
  // let nextIFDPointerBegin = entriesNumberLength + entryLength * entriesNumber;
  // let bigNextIFDPointer= buffer.readUInt32BE(nextIFDPointerBegin) ;
  // let littleNextIFDPointer= buffer.readUInt32LE(nextIFDPointerBegin);
  // let nextIFDPointer = order ?bigNextIFDPointer:littleNextIFDPointer;
  var exif = {};
  var entryCount = 0;

  for (entryCount; entryCount < entriesNumber; entryCount += 1) {
    var entryBegin = entryCount * entryLength;
    var entry = entries.slice(entryBegin, entryBegin + entryLength);
    var tagBegin = 0;
    var tagLength = 2;
    var dataFormatBegin = tagBegin + tagLength;
    var dataFormatLength = 2;
    var componentsBegin = dataFormatBegin + dataFormatLength;
    var componentsNumberLength = 4;
    var dataValueBegin = componentsBegin + componentsNumberLength;
    var dataValueLength = 4;
    var tagAddress = entry.slice(tagBegin, dataFormatBegin);
    var tagNumber = order ? tagAddress.toString('hex') : tagAddress.reverse().toString('hex');
    var tagName = tagCollection[tagNumber];
    var bigDataFormat = entry.readUInt16BE(dataFormatBegin);
    var littleDataFormat = entry.readUInt16LE(dataFormatBegin);
    var dataFormat = order ? bigDataFormat : littleDataFormat;
    var componentsByte = bytes[dataFormat];
    var bigComponentsNumber = entry.readUInt32BE(componentsBegin);
    var littleComponentNumber = entry.readUInt32LE(componentsBegin);
    var componentsNumber = order ? bigComponentsNumber : littleComponentNumber;
    var dataLength = componentsNumber * componentsByte;
    var dataValue = entry.slice(dataValueBegin, dataValueBegin + dataValueLength);

    if (dataLength > 4) {
      var dataOffset = (order ? dataValue.readUInt32BE(0) : dataValue.readUInt32LE(0)) - offset;
      dataValue = buffer.slice(dataOffset, dataOffset + dataLength);
    }

    var tagValue = void 0;

    if (tagName) {
      switch (dataFormat) {
        case 1:
          tagValue = dataValue.readUInt8(0);
          break;
        case 2:
          tagValue = dataValue.toString('ascii').replace(/\0+$/, '');
          break;
        case 3:
          tagValue = order ? dataValue.readUInt16BE(0) : dataValue.readUInt16LE(0);
          break;
        case 4:
          tagValue = order ? dataValue.readUInt32BE(0) : dataValue.readUInt32LE(0);
          break;
        case 5:
          tagValue = [];

          for (var i = 0; i < dataValue.length; i += 8) {
            var bigTagValue = dataValue.readUInt32BE(i) / dataValue.readUInt32BE(i + 4);
            var littleTagValue = dataValue.readUInt32LE(i) / dataValue.readUInt32LE(i + 4);
            tagValue.push(order ? bigTagValue : littleTagValue);
          }

          break;
        case 7:
          switch (tagName) {
            case 'ExifVersion':
              tagValue = dataValue.toString();
              break;
            case 'FlashPixVersion':
              tagValue = dataValue.toString();
              break;
            case 'SceneType':
              tagValue = dataValue.readUInt8(0);
              break;
            default:
              tagValue = '0x' + dataValue.toString('hex', 0, 15);
              break;
          }
          break;
        case 10:
          {
            var bigOrder = dataValue.readInt32BE(0) / dataValue.readInt32BE(4);
            var littleOrder = dataValue.readInt32LE(0) / dataValue.readInt32LE(4);
            tagValue = order ? bigOrder : littleOrder;
            break;
          }
        default:
          tagValue = '0x' + dataValue.toString('hex');
          break;
      }
      exif[tagName] = tagValue;
    }
    /*
     else {
     console.log(`Unkown Tag [0x${tagNumber}].`);
     }
     */
  }
  return exif;
};

/**
 * @param buf {Buffer}
 * @returns {Undefined}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var exifFragments = EXIFHandler(content);
 */
var EXIFHandler = function EXIFHandler(buf) {
  var pad = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;

  var buffer = buf;

  if (pad) {
    buffer = buf.slice(APPMarkerLength);
    var length = buffer.readUInt16BE(0);
    buffer = buffer.slice(0, length);
    var lengthLength = 2;
    buffer = buffer.slice(lengthLength);
    var identifierLength = 5;
    buffer = buffer.slice(identifierLength);
    var padLength = 1;
    buffer = buffer.slice(padLength);
  }

  var byteOrderLength = 2;
  var byteOrder = buffer.toString('ascii', 0, byteOrderLength) === 'MM';
  var fortyTwoLength = 2;
  var fortyTwoEnd = byteOrderLength + fortyTwoLength;
  var big42 = buffer.readUInt32BE(fortyTwoEnd);
  var little42 = buffer.readUInt32LE(fortyTwoEnd);
  var offsetOfIFD = byteOrder ? big42 : little42;

  buffer = buffer.slice(offsetOfIFD);

  if (buffer.length > 0) {
    data = IFDHandler(buffer, tags.ifd, byteOrder, offsetOfIFD);

    if (data.ExifIFDPointer) {
      buffer = buffer.slice(data.ExifIFDPointer - offsetOfIFD);
      data.SubExif = IFDHandler(buffer, tags.ifd, byteOrder, data.ExifIFDPointer);
    }

    if (data.GPSInfoIFDPointer) {
      var gps = data.GPSInfoIFDPointer;
      buffer = buffer.slice(data.ExifIFDPointer ? gps - data.ExifIFDPointer : gps - offsetOfIFD);
      data.GPSInfo = IFDHandler(buffer, tags.gps, byteOrder, gps);
    }
  }
};

/**
 * @param buffer {Buffer}
 * @returns {Undefined}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var exifFragments = APPnHandler(content);
 */
var APPnHandler = function APPnHandler(buffer) {
  var APPMarkerTag = checkAPPn(buffer);

  if (APPMarkerTag !== false) {
    // APP0 is 0, and 0==false
    var length = buffer.readUInt16BE(APPMarkerLength);

    switch (APPMarkerTag) {
      case 1:
        // EXIF
        EXIFHandler(buffer);
        break;
      default:
        APPnHandler(buffer.slice(APPMarkerLength + length));
        break;
    }
  }
};

/**
 * @param buffer {Buffer}
 * @returns {Object}
 * @example
 */
var fromBuffer = function fromBuffer(buffer) {
  if (!buffer) {
    throw new Error('buffer not found');
  }

  data = undefined;

  if (isValid(buffer)) {
    buffer = buffer.slice(SOIMarkerLength);
    data = {};
    APPnHandler(buffer);
  } else if (isTiff(buffer)) {
    data = {};
    EXIFHandler(buffer, false);
  }

  return data;
};

/**
 * @param file {String}
 * @returns {Object}
 * @example
 * var exif = sync("~/Picture/IMG_1981.JPG");
 * console.log(exif.createTime);
 */
var sync = function sync(file) {
  if (!file) {
    throw new Error('File not found');
  }

  var buffer = _fs2.default.readFileSync(file);

  return fromBuffer(buffer);
};

/**
 * @param file {String}
 * @param callback {Function}
 * @example
 * async("~/Picture/IMG_0707.JPG", (err, data) => {
 *     if(err) {
 *         console.log(err);
 *     }
 *     if(data) {
 *         console.log(data.ExifOffset.createTime);
 *     }
 * }
 */
var async = function async(file, callback) {
  data = undefined;

  new Promise(function (resolve, reject) {
    if (!file) {
      reject(new Error('❓File not found.'));
    }

    _fs2.default.readFile(file, function (err, buffer) {
      if (err) {
        reject(err);
      } else {
        try {
          if (isValid(buffer)) {
            var buf = buffer.slice(SOIMarkerLength);

            data = {};

            APPnHandler(buf);
            resolve(data);
          } else if (isTiff(buffer)) {
            data = {};

            EXIFHandler(buffer, false);
            resolve(data);
          } else {
            reject(new Error('😱Unsupport file type.'));
          }
        } catch (e) {
          reject(e);
        }
      }
    });
  }, function (error) {
    callback(error, undefined);
  }).then(function (d) {
    callback(undefined, d);
  }).catch(function (error) {
    callback(error, undefined);
  });
};

exports.fromBuffer = fromBuffer;
exports.parse = async;
exports.parseSync = sync;
//# sourceMappingURL=index.js.map