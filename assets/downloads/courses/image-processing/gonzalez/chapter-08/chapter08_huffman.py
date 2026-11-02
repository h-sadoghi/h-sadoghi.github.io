"""Educational, reversible Huffman compressor for a small grayscale byte array.
Pure Python standard library; not a PNG/JPEG/WebP replacement.
File format: 4 bytes magic HF08, 4-byte big-endian header length,
UTF-8 JSON header with shape, codes, nbits, followed by packed bits.
"""
from collections import Counter
from heapq import heappush, heappop
from itertools import count
import json
from pathlib import Path
import struct


def build_codes(values):
    freqs = Counter(values)
    if not freqs:
        raise ValueError("Empty image")
    serial = count()
    heap = []
    for symbol in sorted(freqs):
        heappush(heap, (freqs[symbol], next(serial), symbol))
    if len(heap) == 1:
        return {heap[0][2]: "0"}
    while len(heap) > 1:
        fa, _, a = heappop(heap)
        fb, _, b = heappop(heap)
        heappush(heap, (fa + fb, next(serial), (a, b)))
    tree = heap[0][2]
    result = {}
    def walk(node, bits):
        if isinstance(node, int):
            result[node] = bits
        else:
            walk(node[0], bits + "0")
            walk(node[1], bits + "1")
    walk(tree, "")
    return result


def encode(values, width, height):
    values = bytes(values)
    if len(values) != width * height:
        raise ValueError("Input dimensions do not match the number of pixels")
    codes = build_codes(values)
    bits = "".join(codes[v] for v in values)
    padding = (-len(bits)) % 8
    bits_padded = bits + "0" * padding
    payload = bytes(int(bits_padded[i:i+8], 2)
                    for i in range(0, len(bits_padded), 8))
    header = json.dumps({"width": width, "height": height,
                         "nbits": len(bits),
                         "codes": {str(k): v for k, v in codes.items()}},
                        separators=(",", ":")).encode("utf-8")
    return b"HF08" + struct.pack(">I", len(header)) + header + payload


def decode(blob):
    if blob[:4] != b"HF08":
        raise ValueError("Not an HF08 educational file")
    nh = struct.unpack(">I", blob[4:8])[0]
    header = json.loads(blob[8:8+nh].decode("utf-8"))
    reverse = {v: int(k) for k, v in header["codes"].items()}
    nbits = header["nbits"]
    data = blob[8+nh:]
    output = bytearray()
    prefix = ""
    read = 0
    for byte in data:
        for b in range(7, -1, -1):
            if read >= nbits:
                break
            read += 1
            prefix += "1" if (byte >> b) & 1 else "0"
            if prefix in reverse:
                output.append(reverse[prefix])
                prefix = ""
    if prefix or len(output) != header["width"] * header["height"]:
        raise ValueError("Corrupted or incomplete bit stream")
    return bytes(output), header["width"], header["height"]


def demo():
    # 128 x 128: 4 synthetic intensity levels (not a photograph)
    width, height = 128, 128
    row = bytes([0]*64 + [85]*32 + [170]*16 + [255]*16)
    raw = row * height
    compressed = encode(raw, width, height)
    restored, w, h = decode(compressed)
    assert restored == raw and (w, h) == (width, height)
    Path("toy_huffman.hf8").write_bytes(compressed)
    print("LOSSLESS reconstruction: PASS")
    print("Raw grayscale pixel bytes:", len(raw))
    print("Huffman container bytes:", len(compressed))
    codes = build_codes(raw)
    print("Huffman codebook:", codes)
    print("Note: the container stores the codebook, unlike bare bit counts")

if __name__ == "__main__":
    demo()
