"""Chapter 3 executable examples: intensity transforms and spatial filtering.
Requirements: numpy, scipy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, gaussian_filter, median_filter


def synthetic_image(n=256):
    y, x = np.mgrid[0:n, 0:n]
    f = 0.12 + 0.55 * x / n
    f += 0.25 * (((x-70)**2 + (y-175)**2) < 38**2)
    f += 0.30 * ((x > 145) & (x < 220) & (y > 35) & (y < 115))
    f += 0.06 * np.sin(x/6) * np.sin(y/10)
    return np.clip(f, 0, 1)


def intensity_demo(f):
    eps = 1e-12
    neg = 1-f
    log = np.log1p(9*f)/np.log(10)
    gamma = f**0.45
    threshold = (f >= 0.5).astype(float)
    return neg, log, gamma, threshold


def histogram_equalize(f, levels=256):
    u = np.clip(np.round(f*(levels-1)), 0, levels-1).astype(np.uint8)
    hist = np.bincount(u.ravel(), minlength=levels)
    cdf = hist.cumsum().astype(float)
    cdf = (cdf-cdf.min())/(cdf.max()-cdf.min()+1e-12)
    return cdf[u]


def correlation_and_convolution(f):
    w = np.array([[0,1,2],[0,0,0],[-2,-1,0]], float)
    corr = convolve(f, np.flip(w), mode='reflect')  # scipy convolve flips internally
    conv = convolve(f, w, mode='reflect')
    return corr, conv, w


def smoothing_demo(f, seed=2):
    rng = np.random.default_rng(seed)
    noisy = f.copy()
    r = rng.random(f.shape)
    noisy[r < 0.025] = 0
    noisy[(r >= 0.025) & (r < 0.05)] = 1
    box = convolve(noisy, np.ones((5,5))/25, mode='reflect')
    gauss = gaussian_filter(noisy, 1.2)
    med = median_filter(noisy, 5, mode='reflect')
    return noisy, box, gauss, med


def sharpening_demo(f):
    lap_kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]], float)
    lap = convolve(f, lap_kernel, mode='reflect')
    lap_sharp = np.clip(f-lap, 0, 1)
    blur = gaussian_filter(f, 2)
    mask = f-blur
    highboost = np.clip(f+1.8*mask, 0, 1)
    sx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], float)
    sy = sx.T
    sobel = np.hypot(convolve(f, sx, mode='reflect'), convolve(f, sy, mode='reflect'))
    return lap, lap_sharp, mask, highboost, sobel


def zoneplate_demo(n=320):
    y, x = np.mgrid[-1:1:complex(n), -1:1:complex(n)]
    z = .5*(1+np.cos(120*np.pi*(x*x+y*y)))
    lp1 = gaussian_filter(z, 2)
    lp2 = gaussian_filter(z, 7)
    hp = z-lp1
    br = lp2 + (z-lp1)
    bp = z-br
    return z, lp1, hp, br, bp


def show_grid(images, titles, cols=3):
    rows = int(np.ceil(len(images)/cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 3.3*rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    for ax in axes[len(images):]: ax.axis('off')
    fig.tight_layout()
    return fig


if __name__ == '__main__':
    f = synthetic_image()
    neg, log, gamma, thr = intensity_demo(f)
    show_grid([f, neg, log, gamma, thr], ['input','negative','log','gamma .45','threshold'])

    eq = histogram_equalize(f)
    show_grid([f, eq], ['input','histogram equalized'], cols=2)

    noisy, box, gauss, med = smoothing_demo(f)
    show_grid([noisy, box, gauss, med], ['noisy','box','Gaussian','median'], cols=4)

    lap, lsharp, mask, hb, sobel = sharpening_demo(f)
    show_grid([f, lap, lsharp, mask, hb, sobel], ['input','Laplacian','Laplacian sharpened','unsharp mask','high-boost','Sobel'])

    z, lp, hp, br, bp = zoneplate_demo()
    show_grid([z, lp, hp, br, bp], ['zone plate','lowpass','highpass','bandreject','bandpass'])
    plt.show()
