import argparse
import os

from src.config import RunOpts, load_config
from src.image_processor import ImageProcessor
from src.image_scanner import ImageLibrary
from src.font_scanner import FontLibrary


parser = argparse.ArgumentParser(description='Generate images')

parser.add_argument('--input', metavar='PATH', type=str, help='Image input path', required=True)
parser.add_argument('--output', metavar='PATH', type=str, help='Image output path', required=True)
parser.add_argument('--output-depth', metavar='N', type=int, help='Output subdirectory depth', default=5)
parser.add_argument('--config', metavar='FILE', type=str, help='Generator config YAML', required=True)
parser.add_argument('--samples', metavar='N', type=int, help='How many samples to generate', default=10)
parser.add_argument('--show', help='Show generated images', action='store_true', default=False)
parser.add_argument('--skip-cache', help='Re-scan image and font cache', action='store_true', default=False)


args = parser.parse_args()

(run_opts, err) = RunOpts.Schema().load(vars(args)) # type: (RunOpts, dict)

if bool(err) is True:
    print(err)
    raise Exception('Invalid arguments')

if run_opts.output == run_opts.input:
    raise Exception('Input and output paths must not match')

config = load_config(run_opts.config)


# Image library
im_library = ImageLibrary(config, run_opts.input)
im_library_cache_file = os.path.join(run_opts.input, '.tartarus.image.cache.json')
im_should_scan = True

if (os.path.exists(im_library_cache_file) is True) or (run_opts.skip_cache is True):
    try:
        im_library.load(im_library_cache_file)
        im_should_scan = False
    except FileNotFoundError:
        pass

if im_should_scan is True:
    im_library.scan()
    im_library.save(im_library_cache_file)


# Font library
font_library = FontLibrary(config, run_opts.input)
font_library_cache_file = os.path.join(run_opts.input, '.tartarus.font.cache.json')
font_should_scan = True

if (os.path.exists(font_library_cache_file) is True) or (run_opts.skip_cache is True):
    try:
        font_library.load(font_library_cache_file)
        font_should_scan = False
    except FileNotFoundError:
        pass

if font_should_scan is True:
    font_library.scan()
    font_library.save(font_library_cache_file)


for i in range(run_opts.samples):
    if i % 100 == 0:
        print(f"Generating images {i}...")

    ip = ImageProcessor(config, run_opts, im_library, font_library, str(i))
    ip.generate()
    ip.save()

    if run_opts.show is True:
        ip.im.show()



