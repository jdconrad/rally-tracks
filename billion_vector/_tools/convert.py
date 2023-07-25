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

def to_json(f, dims, total, query):
    for i in iterate(total):
        f.read(4) # number of dimensions per vector
        vector = struct.unpack("f" * dims, f.read(dims * 4))
        if query:
            print(str(vector).replace('(', '[').replace(')', ']'))
        else:
            print(json.dumps({"vector": vector}, ensure_ascii=False))

if len(sys.argv) != 5:
    print(f"Error: No vectors file. Rerun using [{sys.argv[0]} [dims] [total] [query?True:False] [/path/to/vectors.(f|b)vecs]].")
    sys.exit(1)

with open(sys.argv[4], "rb") as f:
    to_json(f, int(sys.argv[1]), int(sys.argv[2]), bool(sys.argv[3]))

