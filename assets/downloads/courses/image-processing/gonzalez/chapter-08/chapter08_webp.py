"""Simple WebP experiment. Requires Pillow with WebP enabled.
Usage: python chapter08_webp.py [optional_photo.png]
"""
from PIL import Image, ImageDraw, features
from pathlib import Path
import sys, math

def make_demo_image():
    im = Image.new("RGB", (480, 320), (199, 220, 239))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 215, 480, 320), fill=(83, 134, 74))
    d.polygon(((0, 215), (115, 95), (240, 215)), fill=(87, 110, 118))
    d.rectangle((255, 145, 392, 240), fill=(210, 150, 100))
    d.polygon(((240, 151), (325, 105), (410, 151)), fill=(120, 80, 60))
    for x in range(265, 375, 45):
        d.rectangle((x, 174, x + 23, 199), fill=(57, 126, 175))
    return im

def psnr(original, reconstructed):
    a = original.convert("RGB").tobytes()
    b = reconstructed.convert("RGB").tobytes()
    mse = sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)
    return float("inf") if mse == 0 else 10 * math.log10(255**2/mse)

def main():
    if not features.check("webp"):
        print("Your Pillow build does not support WebP. Try another Pillow build.")
        return
    im = Image.open(sys.argv[1]).convert("RGB") if len(sys.argv) > 1 else make_demo_image()
    out = Path("chapter08_webp_results")
    out.mkdir(exist_ok=True)
    configs = [("png", "PNG", {"optimize": True}),
               ("webp_lossless", "WEBP", {"lossless": True}),
               ("webp_q35", "WEBP", {"quality": 35}),
               ("webp_q65", "WEBP", {"quality": 65}),
               ("webp_q90", "WEBP", {"quality": 90})]
    for name, fmt, opts in configs:
        path = out / (name + (".png" if fmt == "PNG" else ".webp"))
        im.save(path, format=fmt, **opts)
        restored = Image.open(path).convert("RGB")
        exact = (restored.tobytes() == im.tobytes())
        print(f"{path.name:20s} {path.stat().st_size:8d} bytes"
              f"   PSNR={psnr(im,restored):6.2f} dB  exact={exact}")
    print("Compare both size and visual quality; results depend on the input image.")
if __name__ == "__main__":
    main()
