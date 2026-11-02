"""Chapter 8 classroom entry point: no network or scikit-image required."""
from collections import Counter
import math

def entropy(values):
    counts = Counter(values)
    total = sum(counts.values())
    return -sum((n/total) * math.log2(n/total) for n in counts.values())

if __name__ == '__main__':
    data = [0] * 32 + [85] * 16 + [170] * 8 + [255] * 8
    print('H =', entropy(data), 'bits/pixel')
    from chapter08_huffman import build_codes, encode, decode
    codes = build_codes(data)
    print('codes =', codes)
    blob = encode(data, width=8, height=8)
    result, w, h = decode(blob)
    assert result == bytes(data) and (w,h) == (8,8)
    print('lossless decode: OK')
    print('Huffman bits only =', sum(len(codes[v]) for v in data))
    print('container bytes =', len(blob), '(includes codebook / overhead)')
    try:
        from chapter08_webp import main as demo_webp
        demo_webp()
    except ImportError:
        print('Pillow is not installed; optional WebP demo skipped')
