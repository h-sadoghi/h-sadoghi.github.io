"""Pedagogical Haar wavelets: direct, separable, orthonormal transform.

Dependencies: NumPy. Boundary policy: arrays must have even dimensions
at each analyzed level; no implicit padding. Coefficients are signed floats.
Subband convention:
  H  = high-pass across rows / low-pass across columns (horizontal edges)
  V  = low-pass across rows / high-pass across columns (vertical edges)
  D  = high-pass across both directions.
"""
from __future__ import annotations
import numpy as np

SQRT2 = np.sqrt(2.0)

def dwt_haar_1d(signal):
    x = np.asarray(signal, dtype=np.float64)
    if x.ndim != 1 or len(x) % 2:
        raise ValueError('Expected a one-dimensional signal with even length')
    return (x[::2] + x[1::2]) / SQRT2, (x[::2] - x[1::2]) / SQRT2

def idwt_haar_1d(a, d):
    a = np.asarray(a, dtype=np.float64)
    d = np.asarray(d, dtype=np.float64)
    if a.ndim != 1 or a.shape != d.shape:
        raise ValueError('Approximation and detail must be equal-size 1D arrays')
    y = np.empty(a.size * 2, dtype=np.float64)
    y[::2] = (a + d) / SQRT2
    y[1::2] = (a - d) / SQRT2
    return y

def _fwd_axis(x, axis):
    z = np.moveaxis(np.asarray(x, dtype=np.float64), axis, -1)
    if z.shape[-1] % 2:
        raise ValueError('Transform axis length must be even')
    return (np.moveaxis((z[..., ::2] + z[..., 1::2]) / SQRT2, -1, axis),
            np.moveaxis((z[..., ::2] - z[..., 1::2]) / SQRT2, -1, axis))

def _inv_axis(a, d, axis):
    a = np.moveaxis(np.asarray(a, dtype=np.float64), axis, -1)
    d = np.moveaxis(np.asarray(d, dtype=np.float64), axis, -1)
    if a.shape != d.shape:
        raise ValueError('The subbands must have matching shapes')
    z = np.empty(a.shape[:-1] + (2 * a.shape[-1],), dtype=np.float64)
    z[..., ::2] = (a + d) / SQRT2
    z[..., 1::2] = (a - d) / SQRT2
    return np.moveaxis(z, -1, axis)

def dwt_haar_2d(image):
    x = np.asarray(image, dtype=np.float64)
    if x.ndim != 2 or x.shape[0] % 2 or x.shape[1] % 2:
        raise ValueError('Expected a 2D image with even height and width')
    ac, dc = _fwd_axis(x, axis=1)  # columns: average / change left-right
    LL, H = _fwd_axis(ac, axis=0)  # rows: average / change top-bottom
    V, D = _fwd_axis(dc, axis=0)
    return LL, H, V, D

def idwt_haar_2d(LL, H, V, D):
    ac = _inv_axis(LL, H, axis=0)
    dc = _inv_axis(V, D, axis=0)
    return _inv_axis(ac, dc, axis=1)

def multilevel_haar_2d(image, levels=3):
    a = np.asarray(image, dtype=np.float64)
    details = []
    for _ in range(levels):
        a, h, v, d = dwt_haar_2d(a)
        details.append((h, v, d))
    return a, details

def inverse_multilevel_haar_2d(approximation, details):
    a = np.asarray(approximation, dtype=np.float64)
    for h, v, d in reversed(details):
        a = idwt_haar_2d(a, h, v, d)
    return a

def synthetic_image(size=256):
    """Self-contained didactic image with edges, smooth gradients, fine texture."""
    if size % 16:
        raise ValueError('size must be a multiple of 16')
    yy, xx = np.mgrid[:size, :size]
    z = 45 + 0.42 * xx + 0.2 * yy
    z = z.astype(float)
    z[(xx > .11*size) & (xx < .49*size) & (yy > .12*size) & (yy < .48*size)] += 75
    z[((xx - .72*size)**2 + (yy - .34*size)**2) < (.16*size)**2] += 82
    z[(yy > .66*size) & (xx > .12*size) & (xx < .88*size)] += 23 * np.sin(.29 * (xx[(yy > .66*size) & (xx > .12*size) & (xx < .88*size)]))
    return np.clip(z, 0, 255)

def soft_threshold(x, t):
    return np.sign(x) * np.maximum(np.abs(x) - t, 0.0)

def wavelet_denoise(image, levels=3, threshold=20.0):
    a, details = multilevel_haar_2d(image, levels)
    return inverse_multilevel_haar_2d(a, [tuple(soft_threshold(b, threshold) for b in level) for level in details])

def cwt_mexican_hat(signal, scales):
    """Illustrative sampled CWT via direct correlation; sample period = 1.
    Uses finite-support Mexican-hat wavelet; not an exact analytic inverse CWT.
    """
    x = np.asarray(signal, dtype=np.float64)
    out = np.empty((len(scales), len(x)), dtype=np.float64)
    for k, a in enumerate(scales):
        if a < 2:
            raise ValueError('Use scales >= 2 for this sampled demonstration')
        t = np.arange(-int(4*a), int(4*a)+1) / float(a)
        psi = (1 - t**2) * np.exp(-t**2 / 2) / np.sqrt(float(a))
        out[k, :] = np.convolve(x, psi[::-1], mode='full')[len(psi)//2:len(psi)//2 + len(x)]
    return out

if __name__ == '__main__':
    x = np.array([8, 8, 4, 4, 10, 10, 6, 6], dtype=float)
    a, d = dwt_haar_1d(x)
    assert np.allclose(idwt_haar_1d(a,d),x)
    print('1D approximation:', np.round(a,3))
    print('1D detail:', np.round(d,3))
    z = synthetic_image()
    coarse, bands = multilevel_haar_2d(z, 3)
    restored = inverse_multilevel_haar_2d(coarse, bands)
    print('2D maximum reconstruction error:', float(np.max(abs(restored-z))))
    assert np.allclose(restored,z,atol=1e-10)
