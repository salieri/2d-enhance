# Tartarus Image Generation Tools

Command line tools for generating large sets of variations from existing image sets. 


## Installation

1. MacOS only: `xcode-select install`
1. MacOS only: `brew install libjpeg`
1. MacOS Mojave only: `export CFLAGS="-I $(xcrun --show-sdk-path)/usr/include"`
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`


## Generating a Sample Library

```bash
python3 generator.py
    --input /path/to/input/images/and/fonts
    --output /path/to/output/images
    --output-depth 5
    --config /path/to/config.yaml
    --samples 10000
    [--show]
    [--skip-cache]
```

The input directory should contain sprites, background images, and TTF and/or OTF fonts. The generator script scans the
directory recursively. JPG and PNG images only.

An image is considered a sprite, if: 

1. it has alpha channel with alpha of any pixel set to anything expect 'opaque'; or
2. its size is smaller than the configured 'native' size of an image
(`processor.native.size.width` and `processor.native.size.height`). 


## Generator Configuration File

Image generation is controlled by the generator configuration file. See an example in [`etc/example/test.yaml`](etc/example/test.yaml).

