# -*- coding: utf-8 -*-
"""
Chapter 05 reproducible examples: image restoration and reconstruction.

Compatible with Python 3.12+.

Dependencies:
    numpy
    matplotlib
    Pillow
    scipy

Install:
    py -3.12 -m pip install numpy matplotlib pillow scipy

Run:
    py -3.12 chapter05_examples.py

Outputs are saved in:
    chapter05_demo_output/
"""

from __future__ import annotations

from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


def synthetic_image(n: int = 192) -> np.ndarray:
    y, x = np.ogrid[:n, :n]
    f = np.zeros((n, n), dtype=float)
    f[28:164, 35:155] = 0.35
    f[(x - 70) ** 2 + (y - 70) ** 2 <= 28 ** 2] = 0.95
    f[(x - 125) ** 2 + (y - 115) ** 2 <= 20 ** 2] = 0.7
    f[120:150, 55:95] = 0.12
    return f


def add_gaussian_noise(image: np.ndarray, sigma: float = 0.08, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.clip(image + rng.normal(0.0, sigma, image.shape), 0.0, 1.0)


def add_salt_pepper(image: np.ndarray, amount: float = 0.08, seed: int = 2) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = image.copy()
    r = rng.random(image.shape)
    out[r < amount / 2] = 0.0
    out[(r >= amount / 2) & (r < amount)] = 1.0
    return out


def arithmetic_mean_filter(image: np.ndarray, size: int = 3) -> np.ndarray:
    return ndimage.uniform_filter(image, size=size, mode="reflect")


def median_filter(image: np.ndarray, size: int = 3) -> np.ndarray:
    return ndimage.median_filter(image, size=size, mode="reflect")


def motion_psf(length: int = 17, angle_deg: float = 0.0, shape=(192, 192)) -> np.ndarray:
    psf = np.zeros(shape, dtype=float)
    cy, cx = shape[0] // 2, shape[1] // 2
    half = length // 2
    psf[cy, cx-half:cx+half+1] = 1.0
    if angle_deg:
        psf = ndimage.rotate(psf, angle_deg, reshape=False, order=1)
    psf /= psf.sum()
    return np.fft.ifftshift(psf)


def fft_blur(image: np.ndarray, psf: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    H = np.fft.fft2(psf)
    F = np.fft.fft2(image)
    g = np.real(np.fft.ifft2(H * F))
    return g, H


def inverse_filter(observed: np.ndarray, H: np.ndarray, eps: float = 0.08) -> np.ndarray:
    G = np.fft.fft2(observed)
    # Stabilized inverse: do not divide by extremely small |H|.
    denom = np.where(np.abs(H) < eps, eps * np.exp(1j * np.angle(H)), H)
    out = np.real(np.fft.ifft2(G / denom))
    return np.clip(out, 0.0, 1.0)


def wiener_filter(observed: np.ndarray, H: np.ndarray, K: float = 0.004) -> np.ndarray:
    G = np.fft.fft2(observed)
    W = np.conj(H) / (np.abs(H) ** 2 + K)
    out = np.real(np.fft.ifft2(W * G))
    return np.clip(out, 0.0, 1.0)


def phantom(n: int = 160) -> np.ndarray:
    y, x = np.ogrid[:n, :n]
    f = np.zeros((n, n), dtype=float)
    f[(x - n/2) ** 2 / (0.32*n) ** 2 + (y - n/2) ** 2 / (0.42*n) ** 2 <= 1] = 0.9
    f[(x - 0.38*n) ** 2 / (0.08*n) ** 2 + (y - 0.42*n) ** 2 / (0.16*n) ** 2 <= 1] = 0.25
    f[(x - 0.62*n) ** 2 / (0.07*n) ** 2 + (y - 0.58*n) ** 2 / (0.12*n) ** 2 <= 1] = 0.45
    return f


def radon_simple(image: np.ndarray, angles: np.ndarray) -> np.ndarray:
    projections = []
    for theta in angles:
        rotated = ndimage.rotate(image, -float(theta), reshape=False, order=1, mode="constant", cval=0.0)
        projections.append(rotated.sum(axis=0))
    return np.asarray(projections).T  # detector x angle


def ramp_filter_sinogram(sino: np.ndarray) -> np.ndarray:
    n = sino.shape[0]
    freq = np.fft.fftfreq(n)
    ramp = np.abs(freq)
    S = np.fft.fft(sino, axis=0)
    return np.real(np.fft.ifft(S * ramp[:, None], axis=0))


def backproject(filtered_sino: np.ndarray, angles: np.ndarray, out_shape: tuple[int, int]) -> np.ndarray:
    h, w = out_shape
    n = filtered_sino.shape[0]
    recon = np.zeros((h, w), dtype=float)
    for k, theta in enumerate(angles):
        strip = np.tile(filtered_sino[:, k], (h, 1))
        if strip.shape[1] != w:
            strip = ndimage.zoom(strip, (1, w / n), order=1)
        recon += ndimage.rotate(strip, float(theta), reshape=False, order=1, mode="constant", cval=0.0)
    recon *= np.pi / (2 * len(angles))
    recon -= recon.min()
    if recon.max() > 0:
        recon /= recon.max()
    return recon


def save_noise_demo(outdir: Path) -> None:
    f = synthetic_image()
    g_gauss = add_gaussian_noise(f)
    g_sp = add_salt_pepper(f)
    gauss_mean = arithmetic_mean_filter(g_gauss, 5)
    sp_mean = arithmetic_mean_filter(g_sp, 5)
    sp_med = median_filter(g_sp, 5)

    fig, ax = plt.subplots(2, 3, figsize=(11, 7))
    items = [
        (f, "Original"),
        (g_gauss, "Gaussian noise"),
        (gauss_mean, "Mean filter"),
        (g_sp, "Salt-and-pepper"),
        (sp_mean, "Mean filter"),
        (sp_med, "Median filter"),
    ]
    for a, (im, title) in zip(ax.ravel(), items):
        a.imshow(im, cmap="gray", vmin=0, vmax=1)
        a.set_title(title)
        a.axis("off")
    fig.tight_layout()
    fig.savefig(outdir / "fig05_demo_noise_filters.png", dpi=170)
    plt.close(fig)


def save_wiener_demo(outdir: Path) -> None:
    f = synthetic_image()
    psf = motion_psf(length=19, angle_deg=8, shape=f.shape)
    blurred, H = fft_blur(f, psf)
    observed = add_gaussian_noise(blurred, sigma=0.035, seed=4)
    inv = inverse_filter(observed, H, eps=0.09)
    wie = wiener_filter(observed, H, K=0.004)

    fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
    for a, im, title in zip(
        ax,
        [f, observed, inv, wie],
        ["Original", "Blur + noise", "Stabilized inverse", "Wiener"]
    ):
        a.imshow(im, cmap="gray", vmin=0, vmax=1)
        a.set_title(title)
        a.axis("off")
    fig.tight_layout()
    fig.savefig(outdir / "fig05_demo_wiener.png", dpi=170)
    plt.close(fig)


def save_fbp_demo(outdir: Path) -> None:
    f = phantom()
    angles = np.linspace(0, 180, 120, endpoint=False)
    sino = radon_simple(f, angles)
    filtered = ramp_filter_sinogram(sino)
    recon = backproject(filtered, angles, f.shape)

    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    ax[0].imshow(f, cmap="gray", vmin=0, vmax=1)
    ax[0].set_title("Synthetic phantom")
    ax[1].imshow(sino, cmap="gray", aspect="auto",
                 extent=[angles[0], angles[-1], sino.shape[0], 0])
    ax[1].set_title("Sinogram")
    ax[1].set_xlabel("Angle (degree)")
    ax[1].set_ylabel("Detector index")
    ax[2].imshow(recon, cmap="gray", vmin=0, vmax=1)
    ax[2].set_title("Filtered backprojection")
    for a in (ax[0], ax[2]):
        a.axis("off")
    fig.tight_layout()
    fig.savefig(outdir / "fig05_demo_fbp.png", dpi=170)
    plt.close(fig)


def run_all(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    save_noise_demo(outdir)
    save_wiener_demo(outdir)
    save_fbp_demo(outdir)
    print(f"Saved demonstration figures to: {outdir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("chapter05_demo_output"))
    args = parser.parse_args()
    run_all(args.output)


if __name__ == "__main__":
    main()
