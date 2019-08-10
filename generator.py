import argparse

from config import RunOpts, load_config
from image_processor import ImageProcessor
from image_scanner import ImageLibrary
from font_scanner import FontLibrary

parser = argparse.ArgumentParser(description='Generate images')

parser.add_argument('--input', metavar='PATH', type=str, help='Image input path', required=True)
parser.add_argument('--output', metavar='PATH', type=str, help='Image output path', required=True)
parser.add_argument('--output-depth', metavar='N', type=int, help='Output subdirectory depth', default=5)
parser.add_argument('--config', metavar='FILE', type=str, help='Generator config YAML', required=True)
parser.add_argument('--samples', metavar='N', type=int, help='How many samples to generate', default=10)
parser.add_argument('--show', type=bool, help='Show generated images', default=False)

args = parser.parse_args()

(run_opts, err) = RunOpts.Schema().load(vars(args)) # type: (RunOpts, dict)

if bool(err) is True:
    print(err)
    raise Exception('Invalid arguments')

config = load_config(run_opts.config)

im_library = ImageLibrary(config, run_opts.input)
font_library = FontLibrary(config, run_opts.input)

im_library.scan()
font_library.scan()

for i in range(run_opts.samples):
    ip = ImageProcessor(config, run_opts, im_library, font_library, str(i))
    ip.generate()
    ip.save()


