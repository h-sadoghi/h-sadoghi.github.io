"""Chapter 4 - independently runnable frequency-domain filtering teaching examples.
Requires numpy, matplotlib and Pillow. It uses only synthetic data created in memory.
Run: python chapter04_examples.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def original_image(n=256):
    y,x=np.ogrid[:n,:n]
    a=(0.15+0.25*(x/n)+0.1*(y/n))*np.ones((n,n))
    a[(x-n*.3)**2+(y-n*.38)**2<(n*.16)**2]=.85
    a[(x>n*.57)&(x<n*.84)&(y>n*.55)&(y<n*.78)]=.25
    return np.clip(a,0,1)

def distance_grid(shape):
    y=np.fft.fftshift(np.fft.fftfreq(shape[0]))*shape[0]
    x=np.fft.fftshift(np.fft.fftfreq(shape[1]))*shape[1]
    return np.hypot(*np.meshgrid(x,y))

def filter_fft(img,H):
    F=np.fft.fftshift(np.fft.fft2(img))
    return np.fft.ifft2(np.fft.ifftshift(F*H)).real

def run(out_dir='chapter04_results'):
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    image=original_image(); D=distance_grid(image.shape); D0=21
    lowpass={
       'Ideal':(D<=D0).astype(float),
       'Gaussian':np.exp(-(D**2)/(2*D0**2)),
       'Butterworth':1/(1+(D/D0)**6)
    }
    fig,ax=plt.subplots(2,4,figsize=(12,6))
    arrays=[('Original',image),('Log spectrum',np.log1p(abs(np.fft.fftshift(np.fft.fft2(image)))))]
    arrays.extend((k,filter_fft(image,H)) for k,H in lowpass.items())
    H=1-lowpass['Gaussian']
    arrays.extend([('Highpass detail',filter_fft(image,H)),('High-boost',image+1.7*filter_fft(image,H))])
    for aa,(name,data) in zip(ax.flat,arrays):aa.imshow(data,cmap='gray');aa.set_title(name);aa.axis('off')
    for aa in ax.flat[len(arrays):]:aa.axis('off')
    fig.tight_layout();fig.savefig(out/'filters.png',dpi=160);plt.close(fig)
    # Notch filtering of periodic sinusoidal interference
    n=image.shape[1]; y,x=np.indices(image.shape)
    noisy=image+0.22*np.cos(2*np.pi*18*x/n)
    F=np.fft.fftshift(np.fft.fft2(noisy));H=np.ones_like(image)
    for dx in (-18,18):
        r=np.hypot(x-(n//2+dx),y-(n//2))
        H*=1-np.exp(-(r*r)/(2*3.5**2))
    restored=np.fft.ifft2(np.fft.ifftshift(F*H)).real
    fig,ax=plt.subplots(1,3,figsize=(10,4))
    for aa,name,data in zip(ax,['Periodic noise','Notch function','Restored'],[noisy,H,restored]):aa.imshow(data,cmap='gray');aa.set_title(name);aa.axis('off')
    fig.tight_layout();fig.savefig(out/'notch.png',dpi=160);plt.close(fig)
    return out

if __name__=='__main__':
    print('Results saved in',run())
