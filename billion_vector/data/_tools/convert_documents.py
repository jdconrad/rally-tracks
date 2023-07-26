#!/usr/bin/env python3
import json
import struct
import sys

try:
    from tqdm import tqdm
    iterate = lambda i: tqdm(range(i))
except ModuleNotFoundError:
    print("Warning: [tqdm] package is not available and you won't be able to see progress.", file=sys.stderr)
    iterate = range

def to_json(f):
    dims = 128
    total = 1000000000
    for i in iterate(total):
        f.read(4) # number of dimensions per vector
        vector = struct.unpack("b" * dims, f.read(dims))
        print(json.dumps({"vector": vector}, ensure_ascii=False))

if len(sys.argv) != 2:
    print(f"Error: No vectors file.")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    to_json(f)

