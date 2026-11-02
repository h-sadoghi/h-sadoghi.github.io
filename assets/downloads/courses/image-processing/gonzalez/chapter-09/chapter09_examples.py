"""Chapter 9 — Four binary morphological operations, reproducible teaching labs.
Python >=3.10; requires numpy, scipy, matplotlib; optionally Pillow for loading masks.
No web data or copyrighted book illustrations. Generated source is synthetic.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi


def footprint(kind: str = 'disk', radius: int = 2):
    """Boolean structuring element centered at [radius, radius]."""
    y, x = np.mgrid[-radius:radius + 1, -radius:radius + 1]
    if kind == 'disk': return x*x + y*y <= radius*radius
    if kind == 'square': return np.ones((2*radius+1,)*2, bool)
    if kind == 'cross': return (x == 0) | (y == 0)
    if kind == 'diamond': return abs(x)+abs(y) <= radius
    if kind == 'horizontal': return y == 0
    raise ValueError(kind)


def erode(binary: np.ndarray, se: np.ndarray) -> np.ndarray:
    """Erosion: all active footprint positions must be foreground."""
    return ndi.binary_erosion(np.asarray(binary, bool), structure=se, border_value=0)


def dilate(binary: np.ndarray, se: np.ndarray) -> np.ndarray:
    """Dilation: foreground expands to footprint positions."""
    return ndi.binary_dilation(np.asarray(binary, bool), structure=se, border_value=0)


def open_mask(binary: np.ndarray, se: np.ndarray) -> np.ndarray:
    return dilate(erode(binary, se), se)


def close_mask(binary: np.ndarray, se: np.ndarray) -> np.ndarray:
    return erode(dilate(binary, se), se)


def synthetic_road(size=(260, 420), seed=42):
    """Illustration, NOT an actual UAV capture or a trained-model result.

    Returns synthetic road RGB, ground-truth defect mask and noisy predicted mask.
    Defects are broad regions, so a small disk SE is geometrically sensible.
    """
    rng = np.random.default_rng(seed)
    h, w = size
    yy, xx = np.mgrid[:h, :w]
    asphalt = np.clip(0.56 + rng.normal(0, 0.055, size), 0, 1)
    road = np.repeat(asphalt[..., None], 3, axis=2)
    # subtle painted road markings for context; synthetic only
    road[20:23, 50:145, :] = 0.85
    road[20:23, 200:295, :] = 0.85
    road[20:23, 345:415, :] = 0.85
    truth = np.zeros((h,w), bool)
    for cx, cy, rx, ry, angle in [(92, 94, 31, 19, .23), (238, 158, 40, 25, -.17), (345, 84, 25, 20, .21)]:
        px, py = xx-cx, yy-cy
        xr=px*np.cos(angle)+py*np.sin(angle)
        yr=-px*np.sin(angle)+py*np.cos(angle)
        irregular = 0.075*np.sin(np.arctan2(yr, xr)*5+1.5) + 0.055*np.cos(np.arctan2(yr,xr)*7)
        blob=(xr/rx)**2+(yr/ry)**2 <= 1+irregular
        truth |= blob
    road[truth] *= np.array([0.40,0.38,0.36])
    raw=truth.copy()
    # deliberately sparse false positives + internal holes in a thresholded mask
    salt=(rng.random(size)<0.008)
    pepper=(rng.random(size)<0.018)
    raw=(raw | salt) & ~pepper
    # deliberate short false-positive connecting tendril
    raw[153:157, 280:294] = True
    return np.clip(road,0,1), truth, raw


def process_road(raw:np.ndarray, r_open=2, r_close=3, r_edge=2):
    b1=footprint('disk', r_open); b2=footprint('disk',r_close); b3=footprint('disk',r_edge)
    after_erode=erode(raw,b1)
    after_open=dilate(after_erode,b1)
    after_dilate=dilate(after_open,b2)
    after_close=erode(after_dilate,b2)
    inner=erode(after_close,b3)
    outer=dilate(after_close,b3)
    border_band=outer & ~inner
    return dict(raw=raw, eroded=after_erode, opened=after_open, dilated=after_dilate,
                closed=after_close, inner=inner, outer=outer, boundary_band=border_band)


def iou(a,b):
    a=np.asarray(a,bool); b=np.asarray(b,bool)
    u=np.logical_or(a,b).sum()
    return float(np.logical_and(a,b).sum()/u) if u else 1.


def save_demo(output_dir: str | Path):
    folder=Path(output_dir);folder.mkdir(parents=True,exist_ok=True)
    road,truth,raw=synthetic_road()
    steps=process_road(raw)
    for name, data in [('synthetic_road_rgb', (road*255).astype('uint8')),
                       ('synthetic_truth',truth.astype('uint8')*255),
                       *[(k,v.astype('uint8')*255) for k,v in steps.items()]]:
        try:
            from PIL import Image
            Image.fromarray(data).save(folder/f'{name}.png')
        except ImportError:
            plt.imsave(folder/f'{name}.png',data,cmap='gray',vmin=0,vmax=255)
    fig, ax=plt.subplots(2,4,figsize=(14,7)); axs=ax.flat
    images=[road,truth,raw,steps['eroded'],steps['opened'],steps['dilated'],steps['closed'],steps['boundary_band']]
    names=['Synthetic road (RGB)','Reference mask','Noisy predicted mask','Erosion (open step)','Opening','Dilation (close step)','Closing','Inner/outer band']
    for a,image,label in zip(axs,images,names):
        if image.ndim==3: a.imshow(image)
        else:a.imshow(image,cmap='gray',vmin=0,vmax=1)
        a.set_title(label,fontsize=11); a.axis('off')
    fig.tight_layout();fig.savefig(folder/'road_pipeline.png',dpi=145);plt.close(fig)
    print('IoU raw:',round(iou(truth,raw),4),'IoU cleaned:',round(iou(truth,steps['closed']),4))
    print('Output:',folder.resolve())
    return steps


def verify():
    a=np.zeros((29,29),bool); a[8:21,7:22]=True
    se=footprint('disk',2)
    e=erode(a,se); d=dilate(a,se); o=open_mask(a,se); c=close_mask(a,se)
    assert np.all(e<=a) and np.all(a<=d)
    assert np.all(o<=a) and np.all(a<=c)
    assert np.array_equal(open_mask(o,se),o)
    assert np.array_equal(close_mask(c,se),c)
    assert np.array_equal(open_mask(a,se),dilate(erode(a,se),se))
    assert np.array_equal(close_mask(a,se),erode(dilate(a,se),se))
    assert np.array_equal(open_mask(a,se)[4:-4,4:-4],(~close_mask(~a,se))[4:-4,4:-4])  # duality away from finite-array borders
    print('All six binary-morphology checks passed.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='outputs_ch09')
    parser.add_argument('--verify-only', action='store_true')
    opt=parser.parse_args()
    verify()
    if not opt.verify_only: save_demo(opt.output)
