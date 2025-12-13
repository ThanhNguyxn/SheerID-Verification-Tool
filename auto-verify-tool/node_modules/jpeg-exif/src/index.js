import fs from 'fs';

const tags = require('./tags.json');

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
const bytes = [0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8];
const SOIMarkerLength = 2;
const JPEGSOIMarker = 0xffd8;
const TIFFINTEL = 0x4949;
const TIFFMOTOROLA = 0x4d4d;
const APPMarkerLength = 2;
const APPMarkerBegin = 0xffe0;
const APPMarkerEnd = 0xffef;
let data;
/**
 * @param buffer {Buffer}
 * @returns {Boolean}
 * @example
 * var content = fs.readFileSync("~/Picture/IMG_0911.JPG");
 * var isImage = isValid(content);
 * console.log(isImage);
 */
const isValid = (buffer) => {
  try {
    const SOIMarker = buffer.readUInt16BE(0);
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
const isTiff = (buffer) => {
  try {
    const SOIMarker = buffer.readUInt16BE(0);
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
const checkAPPn = (buffer) => {
  try {
    const APPMarkerTag = buffer.readUInt16BE(0);
    const isInRange = APPMarkerTag >= APPMarkerBegin && APPMarkerTag <= APPMarkerEnd;
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
const IFDHandler = (buffer, tagCollection, order, offset) => {
  const entriesNumber = order ? buffer.readUInt16BE(0) : buffer.readUInt16LE(0);

  if (entriesNumber === 0) {
    return {};
  }

  const entriesNumberLength = 2;
  const entries = buffer.slice(entriesNumberLength);
  const entryLength = 12;
  // let nextIFDPointerBegin = entriesNumberLength + entryLength * entriesNumber;
  // let bigNextIFDPointer= buffer.readUInt32BE(nextIFDPointerBegin) ;
  // let littleNextIFDPointer= buffer.readUInt32LE(nextIFDPointerBegin);
  // let nextIFDPointer = order ?bigNextIFDPointer:littleNextIFDPointer;
  const exif = {};
  let entryCount = 0;

  for (entryCount; entryCount < entriesNumber; entryCount += 1) {
    const entryBegin = entryCount * entryLength;
    const entry = entries.slice(entryBegin, entryBegin + entryLength);
    const tagBegin = 0;
    const tagLength = 2;
    const dataFormatBegin = tagBegin + tagLength;
    const dataFormatLength = 2;
    const componentsBegin = dataFormatBegin + dataFormatLength;
    const componentsNumberLength = 4;
    const dataValueBegin = componentsBegin + componentsNumberLength;
    const dataValueLength = 4;
    const tagAddress = entry.slice(tagBegin, dataFormatBegin);
    const tagNumber = order ? tagAddress.toString('hex') : tagAddress.reverse().toString('hex');
    const tagName = tagCollection[tagNumber];
    const bigDataFormat = entry.readUInt16BE(dataFormatBegin);
    const littleDataFormat = entry.readUInt16LE(dataFormatBegin);
    const dataFormat = order ? bigDataFormat : littleDataFormat;
    const componentsByte = bytes[dataFormat];
    const bigComponentsNumber = entry.readUInt32BE(componentsBegin);
    const littleComponentNumber = entry.readUInt32LE(componentsBegin);
    const componentsNumber = order ? bigComponentsNumber : littleComponentNumber;
    const dataLength = componentsNumber * componentsByte;
    let dataValue = entry.slice(dataValueBegin, dataValueBegin + dataValueLength);

    if (dataLength > 4) {
      const dataOffset = (order ? dataValue.readUInt32BE(0) : dataValue.readUInt32LE(0)) - offset;
      dataValue = buffer.slice(dataOffset, dataOffset + dataLength);
    }

    let tagValue;

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

          for (let i = 0; i < dataValue.length; i += 8) {
            const bigTagValue = dataValue.readUInt32BE(i) / dataValue.readUInt32BE(i + 4);
            const littleTagValue = dataValue.readUInt32LE(i) / dataValue.readUInt32LE(i + 4);
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
              tagValue = `0x${dataValue.toString('hex', 0, 15)}`;
              break;
          }
          break;
        case 10: {
          const bigOrder = dataValue.readInt32BE(0) / dataValue.readInt32BE(4);
          const littleOrder = dataValue.readInt32LE(0) / dataValue.readInt32LE(4);
          tagValue = order ? bigOrder : littleOrder;
          break;
        }
        default:
          tagValue = `0x${dataValue.toString('hex')}`;
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
const EXIFHandler = (buf, pad = true) => {
  let buffer = buf;

  if (pad) {
    buffer = buf.slice(APPMarkerLength);
    const length = buffer.readUInt16BE(0);
    buffer = buffer.slice(0, length);
    const lengthLength = 2;
    buffer = buffer.slice(lengthLength);
    const identifierLength = 5;
    buffer = buffer.slice(identifierLength);
    const padLength = 1;
    buffer = buffer.slice(padLength);
  }

  const byteOrderLength = 2;
  const byteOrder = buffer.toString('ascii', 0, byteOrderLength) === 'MM';
  const fortyTwoLength = 2;
  const fortyTwoEnd = byteOrderLength + fortyTwoLength;
  const big42 = buffer.readUInt32BE(fortyTwoEnd);
  const little42 = buffer.readUInt32LE(fortyTwoEnd);
  const offsetOfIFD = byteOrder ? big42 : little42;

  buffer = buffer.slice(offsetOfIFD);

  if (buffer.length > 0) {
    data = IFDHandler(buffer, tags.ifd, byteOrder, offsetOfIFD);

    if (data.ExifIFDPointer) {
      buffer = buffer.slice(data.ExifIFDPointer - offsetOfIFD);
      data.SubExif = IFDHandler(buffer, tags.ifd, byteOrder, data.ExifIFDPointer);
    }

    if (data.GPSInfoIFDPointer) {
      const gps = data.GPSInfoIFDPointer;
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
const APPnHandler = (buffer) => {
  const APPMarkerTag = checkAPPn(buffer);

  if (APPMarkerTag !== false) { // APP0 is 0, and 0==false
    const length = buffer.readUInt16BE(APPMarkerLength);

    switch (APPMarkerTag) {
      case 1: // EXIF
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
const fromBuffer = (buffer) => {
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
const sync = (file) => {
  if (!file) {
    throw new Error('File not found');
  }

  const buffer = fs.readFileSync(file);

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
const async = (file, callback) => {
  data = undefined;

  new Promise((resolve, reject) => {
    if (!file) {
      reject(new Error('❓File not found.'));
    }

    fs.readFile(file, (err, buffer) => {
      if (err) {
        reject(err);
      } else {
        try {
          if (isValid(buffer)) {
            const buf = buffer.slice(SOIMarkerLength);

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
  }, (error) => {
    callback(error, undefined);
  }).then((d) => {
    callback(undefined, d);
  }).catch((error) => {
    callback(error, undefined);
  });
};

exports.fromBuffer = fromBuffer;
exports.parse = async;
exports.parseSync = sync;
