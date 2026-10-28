# -*- coding: utf-8 -*-
"""Chapter 11 — Texture and SIFT examples.

Python 3.12+.
Required: numpy, matplotlib, Pillow
Optional for SIFT matching: opencv-python

Install:
    py -3.12 -m pip install numpy matplotlib pillow opencv-python
Run:
    py -3.12 chapter11_examples.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def histogram_descriptors(image, levels=256):
    a=np.clip(np.asarray(image),0,levels-1).astype(np.uint8)
    n=np.bincount(a.ravel(),minlength=levels).astype(float)
    p=n/n.sum(); z=np.arange(levels,dtype=float)
    m=float(np.sum(z*p)); centered=z-m
    mu2=float(np.sum(centered**2*p)); sigma=np.sqrt(mu2)
    mu3=float(np.sum(centered**3*p)); mu4=float(np.sum(centered**4*p))
    smoothness=(mu2/(levels-1)**2)/(1+mu2/(levels-1)**2)
    uniformity=float(np.sum(p*p))
    nz=p>0; entropy=float(-np.sum(p[nz]*np.log2(p[nz])))
    skewness=mu3/sigma**3 if sigma>0 else np.nan
    excess_kurtosis=mu4/sigma**4-3 if sigma>0 else np.nan
    return dict(mean=m,variance=mu2,std=sigma,smoothness=smoothness,
                uniformity=uniformity,entropy=entropy,skewness=skewness,
                excess_kurtosis=excess_kurtosis)


def glcm(image, dx=1, dy=0, levels=None):
    a=np.asarray(image,dtype=int)
    if levels is None: levels=int(a.max())+1
    h,w=a.shape
    G=np.zeros((levels,levels),dtype=float)
    y0=max(0,-dy); y1=min(h,h-dy); x0=max(0,-dx); x1=min(w,w-dx)
    for y in range(y0,y1):
        for x in range(x0,x1):
            i=a[y,x]; j=a[y+dy,x+dx]
            G[i,j]+=1
    P=G/G.sum() if G.sum() else G
    return G,P


def glcm_descriptors(P):
    P=np.asarray(P,dtype=float); K=P.shape[0]
    i=np.arange(K)[:,None]; j=np.arange(K)[None,:]
    contrast=float(np.sum((i-j)**2*P))
    uniformity=float(np.sum(P**2))
    homogeneity=float(np.sum(P/(1+np.abs(i-j))))
    nz=P>0; entropy=float(-np.sum(P[nz]*np.log2(P[nz])))
    pr=P.sum(axis=1); pc=P.sum(axis=0)
    mur=float(np.sum(np.arange(K)*pr)); muc=float(np.sum(np.arange(K)*pc))
    sr=np.sqrt(np.sum((np.arange(K)-mur)**2*pr)); sc=np.sqrt(np.sum((np.arange(K)-muc)**2*pc))
    corr=float(np.sum((i-mur)*(j-muc)*P)/(sr*sc)) if sr*sc>0 else np.nan
    return dict(contrast=contrast,uniformity=uniformity,homogeneity=homogeneity,
                entropy=entropy,correlation=corr,max_probability=float(P.max()))


def synthetic_textures(n=192):
    y,x=np.mgrid[:n,:n]
    vertical=(np.sin(2*np.pi*x/20)>0).astype(float)
    horizontal=(np.sin(2*np.pi*y/20)>0).astype(float)
    checker=((x//12+y//12)%2).astype(float)
    return vertical,horizontal,checker


def dft_power(image):
    F=np.fft.fftshift(np.fft.fft2(np.asarray(image,dtype=float)))
    return np.log1p(np.abs(F)**2)


def sift_match_demo(output_path):
    try:
        import cv2
    except Exception as exc:
        print('OpenCV unavailable; SIFT demo skipped:',exc); return None
    canvas=np.zeros((340,420),np.uint8)+22
    rng=np.random.default_rng(447)
    for i in range(42):
        x,y=int(rng.integers(20,400)),int(rng.integers(20,320)); r=int(rng.integers(4,15)); col=int(rng.integers(85,250))
        if i%3==0: cv2.circle(canvas,(x,y),r,col,2)
        elif i%3==1: cv2.rectangle(canvas,(x-r,y-r),(x+r,y+r),col,2)
        else: cv2.line(canvas,(x-r,y),(x+r,y+r),col,2)
    cv2.putText(canvas,'FEATURES',(65,205),cv2.FONT_HERSHEY_SIMPLEX,1.05,255,2,cv2.LINE_AA)
    M=cv2.getRotationMatrix2D((210,170),26,.82)
    warped=cv2.warpAffine(canvas,M,(420,340),borderValue=22)
    sift=cv2.SIFT_create(nfeatures=900)
    k1,d1=sift.detectAndCompute(canvas,None); k2,d2=sift.detectAndCompute(warped,None)
    matcher=cv2.BFMatcher(); pairs=matcher.knnMatch(d1,d2,k=2)
    good=[a for a,b in pairs if a.distance<.75*b.distance]
    vis=cv2.drawMatches(canvas,k1,warped,k2,good[:28],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite(str(output_path),vis)
    return len(good)


def main():
    out=Path('chapter11_demo_output'); out.mkdir(exist_ok=True)
    A=np.tile([0,1,0,1],(4,1)); B=np.tile(np.array([0,0,1,1])[:,None],(1,4))
    print('Histogram A:',histogram_descriptors(A,levels=2))
    print('Histogram B:',histogram_descriptors(B,levels=2))
    for name,img in [('A',A),('B',B)]:
        G,P=glcm(img,dx=1,dy=0,levels=2)
        print(name,'G=\n',G,'\nP=\n',P,'\nDescriptors:',glcm_descriptors(P))
    v,h,c=synthetic_textures()
    fig,axs=plt.subplots(2,3,figsize=(10,6))
    for col,(im,title) in enumerate([(v,'vertical'),(h,'horizontal'),(c,'checker')]):
        axs[0,col].imshow(im,cmap='gray'); axs[0,col].set_title(title); axs[0,col].axis('off')
        axs[1,col].imshow(dft_power(im),cmap='magma'); axs[1,col].set_title('log power spectrum'); axs[1,col].axis('off')
    fig.tight_layout(); fig.savefig(out/'texture_spectra.png',dpi=150); plt.close(fig)
    n=sift_match_demo(out/'sift_matches.png')
    if n is not None: print('SIFT ratio-test matches:',n)
    print('Outputs:',out.resolve())

if __name__=='__main__': main()
