from argparse import ArgumentParser
from pathlib import Path

import regex

HASH_LINE_RE = regex.compile(r'SHA256\((?<filename>.+)\)=\s(?<sha256_digest>[0-9a-f]{64})')


def read_all_lines(filename):
    with open(filename) as fp:
        return [line.rstrip() for line in fp]

def parse_line(line):
    m = HASH_LINE_RE.search(line)
    if m:
        return (m['filename'], m['sha256_digest'])

def main():
    parser = ArgumentParser()
    parser.add_argument('hash_digest_file')
    args = parser.parse_args()
    hash_digest_file = args.hash_digest_file
    lines = read_all_lines(args.hash_digest_file)
    parsed_lines = [parse_line(line) for line in lines]

    output_file = Path(hash_digest_file).with_name('hash_info.txt')
    with output_file.open(mode='w') as fp:
        for filename, hexdigest in parsed_lines:
            print(f'{hexdigest} {filename}', file=fp)

if __name__ == '__main__':
    main()
