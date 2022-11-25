from hashlib import sha256
import logging
from pathlib import Path

import regex

_HASH_LINE_RE = regex.compile(r'SHA256\((?<filename>.+)\)=\s(?<sha256_digest>[0-9a-f]{64})')


def read_all_lines(filename):
    with open(filename) as fp:
        return [line[:-1] for line in fp]

def get_sha256_digest(p: Path):
    with p.open(mode='rb') as fp:
        m = sha256()
        m.update(fp.read())
        return m.hexdigest()

def parse_line(line):
    m = _HASH_LINE_RE.search(line)
    if m:
        return (m['filename'], m['sha256_digest'])

def get_sha256_dict():
    parsed_lines = (parse_line(line) for line in read_file())
    return {filename:sha256_digest for filename, sha256_digest in parsed_lines}
