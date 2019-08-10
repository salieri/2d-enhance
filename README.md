> This project is an early stage draft. It does not work or compile.

## Installation

1. MacOS only: `xcode-select install`
1. MacOS only: `brew install libjpeg`
1. MacOS Mojave only: `export CFLAGS="-I $(xcrun --show-sdk-path)/usr/include"`
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`


## Building a Sample Library

```bash
python3 generator.py
    --input /path/to/input/images/and/fonts
    --output /path/to/output/images
    --output-depth 5
    --config /path/to/config.yaml
    --samples 10000
    [--show]
```

