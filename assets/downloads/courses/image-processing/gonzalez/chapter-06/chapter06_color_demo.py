"""Chapter 06: RGB, HSI and HSV in a beginner-friendly example.

Requirements: Pillow.  The colorsys module belongs to Python's standard library.
Running this script prints sample colors and creates an HSV mask for red objects.
"""
import colorsys
import math
from pathlib import Path
from PIL import Image


def rgb_to_hsi(rgb):
    """Return (H degrees or None for gray, S from 0 to 1, I from 0 to 255)."""
    r, g, b = (v / 255.0 for v in rgb)
    intensity = (sum(rgb) / 3.0)
    total = r + g + b
    saturation = 0.0 if total == 0 else 1 - 3 * min(r, g, b) / total
    if max(rgb) == min(rgb):
        return None, 0.0, intensity
    numerator = 0.5 * ((r - g) + (r - b))
    denominator = math.sqrt((r - g)**2 + (r - b) * (g - b))
    angle = math.degrees(math.acos(max(-1.0, min(1.0, numerator / denominator))))
    hue = angle if b <= g else 360 - angle
    return hue, saturation, intensity


def rgb_to_hsv(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    if max(rgb) == min(rgb):
        return None, 0.0, v * 255
    return h * 360, s, v * 255


def select_red_pixels(image):
    mask = Image.new('L', image.size, 0)
    for y in range(image.height):
        for x in range(image.width):
            h, s, v = rgb_to_hsv(image.getpixel((x, y)))
            if h is not None and (h < 17 or h > 343) and s > 0.45 and v > 0.25 * 255:
                mask.putpixel((x, y), 255)
    return mask


def main():
    for name, rgb in [('red', (255, 0, 0)), ('yellow', (255, 255, 0)),
                      ('gray', (120, 120, 120)), ('pink', (255, 128, 128))]:
        print(f'{name:7} RGB={rgb}  HSI={rgb_to_hsi(rgb)}  HSV={rgb_to_hsv(rgb)}')
    base = Path(__file__).resolve().parent
    source = base / 'sample_color_shapes.png'
    if not source.exists():
        raise SystemExit(f'Missing sample image: {source}')
    image = Image.open(source).convert('RGB')
    destination = base / 'red_mask_generated.png'
    select_red_pixels(image).save(destination)
    print('Mask saved to:', destination)


if __name__ == '__main__':
    main()
