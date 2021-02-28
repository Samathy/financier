from . import main

import argparse
import pathlib
import os

parser = argparse.ArgumentParser()
parser.add_argument("--format", required=True, nargs=1, action="store")
parser.add_argument("--filename", required=True, nargs=1, action="store")
parser.add_argument("--output", required=False, nargs=1, action="store", default="output.csv")


args = parser.parse_args()

format_filename = os.path.dirname(__file__) / pathlib.Path("formats") / f"{args.format[0]}.json"
filename = pathlib.Path(args.filename[0]).expanduser()
output_filename = pathlib.Path(args.output[0]).expanduser()

breakpoint()

main(format_filename, filename, output_filename)
