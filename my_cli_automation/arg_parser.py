import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process file and directory paths.")
    parser.add_argument('-f', '--files', nargs='+', help='List of file paths')
    parser.add_argument('-d', '--dir', help='Directory path')

    return parser.parse_args()