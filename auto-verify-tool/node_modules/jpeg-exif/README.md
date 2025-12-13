# jpeg-exif
Get exif information from jpeg format file. Works with TIFF too!

[![npm](https://img.shields.io/npm/dm/jpeg-exif.svg)][npm-url] [![Inline docs](http://inch-ci.org/github/zhso/jpeg-exif.svg?branch=master&style=shields)](http://inch-ci.org/github/zhso/jpeg-exif) [![Build Status](https://travis-ci.org/zhso/jpeg-exif.svg?branch=master)](https://travis-ci.org/zhso/jpeg-exif) [![Coverage Status](https://coveralls.io/repos/github/zhso/jpeg-exif/badge.svg?branch=master)](https://coveralls.io/github/zhso/jpeg-exif?branch=master)

[npm-url]: https://npmjs.org/package/jpeg-exif
### Async

```js
import exif from "jpeg-exif";

const filePath = "~/Photo/IMG_0001.JPG";

exif.parse(filePath, (err, data) => {
    if (err) {
        console.log(err);
    } else {
        console.log(data);
    }
});
```

### Sync

```js
import exif from "jpeg-exif";

const filePath = "~/Photo/IMG_0001.JPG";
const data = exif.parseSync(filePath);

console.log(data);
```

## From Buffer

```js
import fs from "fs";
import exif from "jpeg-exif";

const filePath = "~/Documents/DOC_0001.TIFF";
const buffer = fs.readFileSync(filePath);
const data = exif.fromBuffer(buffer);

console.log(data);
```

## Features

* Support All CP3451 Standard Tags (Include GPS & SubExif Tags)
* Support Sync, Async
* Support pass Buffer Type

## Installation

```bash
$ npm i jpeg-exif
```

## Callback Data Format

```js
{
    "Make": "Apple",
    "Model": "Apple",
    //...
    "SubExif": [
        "DateTimeOriginal": "2015:10:06 17:19:36",
        "CreateDate": "2015:10:06 17:19:36",
        //...
    ],
    "GPSInfo":[
        "GPSLatitudeRef": "N",
        "GPSLatitude": [ 35, 39, 40.08 ],
	    //...
    ]
}
```
