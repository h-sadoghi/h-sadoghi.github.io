# -*- coding: utf-8 -*-
"""
Chapter 10 reproducible examples — Digital Image Processing
Compatible with Python 3.12+ on Windows/Linux/macOS.

Dependencies:
    numpy
    matplotlib
    Pillow

Install:
    py -3.12 -m pip install numpy matplotlib pillow

Run synthetic examples:
    py -3.12 chapter10_examples.py

Run also on an arbitrary image:
    py -3.12 chapter10_examples.py --input path/to/image.png
"""

from __future__ import annotations

from pathlib import Path
from collections import deque
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def conv2(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    image = np.asarray(image, dtype=float)
    kernel = np.asarray(kernel, dtype=float)
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(image, ((ph, ph), (pw, pw)), mode="reflect")
    out = np.zeros_like(image, dtype=float)
    for r in range(kh):
        for c in range(kw):
            out += kernel[r, c] * padded[r:r + image.shape[0], c:c + image.shape[1]]
    return out


def minmax_scale(z: np.ndarray, L: int = 256) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    zmin, zmax = float(z.min()), float(z.max())
    if zmax == zmin:
        return np.zeros(z.shape, dtype=np.uint8)
    g = (z - zmin) / (zmax - zmin) * (L - 1)
    return np.clip(g, 0, L - 1).astype(np.uint8)


def sobel_xy(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    ky = kx.T
    gx = conv2(image, kx)
    gy = conv2(image, ky)
    mag = np.hypot(gx, gy)
    return gx, gy, mag


def otsu_threshold(image: np.ndarray) -> tuple[int, np.ndarray]:
    u8 = np.clip(image, 0, 255).astype(np.uint8)
    hist = np.bincount(u8.ravel(), minlength=256).astype(float)
    p = hist / hist.sum()
    P1 = np.cumsum(p)
    m = np.cumsum(np.arange(256) * p)
    mG = m[-1]
    sigma_b = np.zeros(256, dtype=float)
    valid = (P1 > 0) & (P1 < 1)
    sigma_b[valid] = (mG * P1[valid] - m[valid]) ** 2 / (P1[valid] * (1 - P1[valid]))
    k_star = int(np.argmax(sigma_b))
    return k_star, sigma_b


def region_grow(image: np.ndarray, seed: tuple[int, int], T: float) -> np.ndarray:
    """4-connected region growing using similarity to the seed intensity."""
    image = np.asarray(image, dtype=float)
    h, w = image.shape
    sr, sc = seed
    seed_value = image[sr, sc]
    accepted = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    q = deque([(sr, sc)])

    while q:
        r, c = q.popleft()
        if visited[r, c]:
            continue
        visited[r, c] = True

        if abs(image[r, c] - seed_value) <= T:
            accepted[r, c] = True
            for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= rr < h and 0 <= cc < w and not visited[rr, cc]:
                    q.append((rr, cc))
    return accepted


def synthetic_image(size: int = 160) -> np.ndarray:
    rng = np.random.default_rng(10)
    f = np.full((size, size), 35.0)
    f[35:125, 45:115] = 175.0
    y, x = np.ogrid[:size, :size]
    f[(x - 112) ** 2 + (y - 42) ** 2 < 18 ** 2] = 225.0
    f += rng.normal(0, 8, f.shape)
    return np.clip(f, 0, 255)


def save_image(a: np.ndarray, path: Path) -> None:
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)


def run_all(output_dir: Path, input_path: Path | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    f = synthetic_image()
    gx, gy, mag = sobel_xy(f)
    k_star, sigma_b = otsu_threshold(f)
    binary = (f > k_star).astype(np.uint8) * 255

    save_image(f, output_dir / "synthetic_input.png")
    save_image(minmax_scale(np.abs(gx)), output_dir / "sobel_gx.png")
    save_image(minmax_scale(np.abs(gy)), output_dir / "sobel_gy.png")
    save_image(minmax_scale(mag), output_dir / "gradient_magnitude.png")
    save_image(binary, output_dir / "otsu_binary.png")

    # Region growing toy example used in the chapter
    toy = np.array([
        [11, 10, 12, 80, 81],
        [10, 12, 11, 79, 82],
        [ 9, 11, 12, 78, 80],
        [10, 13, 11, 77, 81],
        [12, 10,  9, 76, 83],
    ], dtype=float)
    mask = region_grow(toy, seed=(2, 1), T=3)
    np.savetxt(output_dir / "region_growing_toy_mask.txt", mask.astype(int), fmt="%d")

    # Log transform and the display-scaling equation
    z = np.log1p(f)
    save_image(z.astype(np.uint8), output_dir / "log_direct_bad.png")
    save_image(minmax_scale(z), output_dir / "log_minmax_scaled.png")

    # Otsu diagnostic plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(np.arange(256), sigma_b)
    ax.axvline(k_star, linestyle="--", label=f"Otsu threshold = {k_star}")
    ax.set_xlabel("threshold k")
    ax.set_ylabel("between-class variance")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "otsu_between_class_variance.png", dpi=150)
    plt.close(fig)

    if input_path is not None:
        with Image.open(input_path) as im:
            real = np.asarray(im.convert("L"), dtype=float)
        rx, ry, rmag = sobel_xy(real)
        rk, _ = otsu_threshold(real)
        save_image(real, output_dir / "input_gray.png")
        save_image(minmax_scale(np.abs(rx)), output_dir / "input_gx.png")
        save_image(minmax_scale(np.abs(ry)), output_dir / "input_gy.png")
        save_image(minmax_scale(rmag), output_dir / "input_gradient_magnitude.png")
        save_image((real > rk).astype(np.uint8) * 255, output_dir / "input_otsu_binary.png")
        save_image(minmax_scale(np.log1p(real)), output_dir / "input_log_scaled.png")

    print(f"Outputs saved in: {output_dir.resolve()}")
    print(f"Synthetic Otsu threshold: {k_star}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chapter 10 image segmentation examples")
    parser.add_argument("--input", type=Path, default=None, help="Optional input image")
    parser.add_argument("--output", type=Path, default=Path("chapter10_demo_output"))
    args = parser.parse_args()
    run_all(args.output, args.input)


if __name__ == "__main__":
    main()
