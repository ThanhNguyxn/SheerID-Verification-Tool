/* global it, describe */
const fs = require('fs');
const { expect } = require('chai');
const exif = require('../lib/index.js');

describe('.parse()', () => {
  it('file {undefined}', () => {
    exif.parse(undefined, (err) => {
      expect(err).to.throw(Error);
    });
  });

  it('file {null}', () => {
    exif.parse('./test/null.jpg', (err) => {
      expect(err).to.throw(Error);
    });
  });

  it('APP1:#0xffe1', (done) => {
    exif.parse('./test/IMG_0001.JPG', (err, data) => {
      expect(data).to.be.an('object');
      done();
    });
  });

  it('APP0:#0xffe0', (done) => {
    exif.parse('./test/IMG_0003.JPG', (err, data) => {
      expect(data).to.be.an('undefined');
      done();
    });
  });

  it('!(APP1:#0xffe1||APP0:#0xffe0)', (done) => {
    exif.parse('./test/index.test.js', (err, data) => {
      expect(data).to.be.an('undefined');
      done();
    });
  });

  it('[SubExif]', (done) => {
    exif.parse('./test/IMG_0001.JPG', (err, data) => {
      expect(data.SubExif).to.be.an('object');
      done();
    });
  });

  it('[GPSInfo]', (done) => {
    exif.parse('./test/IMG_0001.JPG', (err, data) => {
      expect(data.GPSInfo).to.be.an('object');
      done();
    });
  });
});

describe('.parseSync()', () => {
  it('file {undefined}', () => {
    expect(exif.parseSync).to.throw(Error);
  });

  it('file {null}', () => {
    expect(exif.parseSync).to.throw(Error);
  });

  it('APP1:#0xffe1', () => {
    const data = exif.parseSync('./test/IMG_0001.JPG');
    expect(data).to.be.an('object');
  });

  it('!APP1:#0xffe1', () => {
    const data = exif.parseSync('./test/IMG_0003.JPG');
    expect(data).to.be.an('object');
  });

  it('[SubExif]', () => {
    const data = exif.parseSync('./test/IMG_0001.JPG');
    expect(data.SubExif).to.be.an('object');
  });

  it('[GPSInfo]', () => {
    const data = exif.parseSync('./test/IMG_0001.JPG');
    expect(data.GPSInfo).to.be.an('object');
  });

  it('TIFF', () => {
    const data = exif.parseSync('./test/Arbitro.tiff');

    expect(data).to.be.eql({
      ImageWidth: 174,
      ImageHeight: 38,
      BitsPerSample: 8,
      Compression: 5,
      PhotometricInterpretation: 2,
      StripOffsets: 8,
      Orientation: 1,
      SamplesPerPixel: 4,
      RowsPerStrip: 38,
      StripByteCounts: 6391,
      PlanarConfiguration: 1,
    });
  });
});

describe('.fromBuffer()', () => {
  it('file {undefined}', () => {
    expect(exif.fromBuffer).to.throw(Error);
  });

  it('APP1:#0xffe1', () => {
    const buffer = fs.readFileSync('./test/IMG_0001.JPG');
    const data = exif.fromBuffer(buffer);

    expect(data).to.be.an('object');
  });

  it('!APP1:#0xffe1', () => {
    const buffer = fs.readFileSync('./test/IMG_0003.JPG');
    const data = exif.fromBuffer(buffer);

    expect(data).to.be.an('object');
  });

  it('[SubExif]', () => {
    const buffer = fs.readFileSync('./test/IMG_0001.JPG');
    const data = exif.fromBuffer(buffer);

    expect(data.SubExif).to.be.an('object');
  });

  it('[GPSInfo]', () => {
    const buffer = fs.readFileSync('./test/IMG_0001.JPG');
    const data = exif.fromBuffer(buffer);

    expect(data.GPSInfo).to.be.an('object');
  });
});
