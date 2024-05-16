import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process file and directory paths.")
    parser.add_argument('-f', '--files', nargs='+', help='List of file paths')
    parser.add_argument('-d', '--dir', help='Directory path')
    parser.add_argument('-i', '--init', default='vegan recipe', help='Initial prompt key (default: programming)')

    return parser.parse_args()