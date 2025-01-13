import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    "-t",
    type=str,
    help="Specify captions directly as text to overlay on video"
)

group.add_argument(
    "-f",
    type=str,
    help="Provide .txt file with captions to overlay on video."
)

parser.add_argument(
    "-o",
    type=str,
    help="Output file name",
    default="output.mp4"
)