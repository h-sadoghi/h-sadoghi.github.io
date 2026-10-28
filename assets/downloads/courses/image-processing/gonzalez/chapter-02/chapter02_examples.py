"""Chapter 2 examples: Digital Image Fundamentals.
Runs with Python 3.12+, NumPy, Matplotlib and Pillow.
All images are synthetic; no copyrighted textbook figures are used.
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

N=256
y,x=np.mgrid[-1:1:complex(N),-1:1:complex(N)]
f=np.exp(-4*(x*x+y*y)) + 0.55*np.exp(-45*((x-.35)**2+(y+.22)**2)) + 0.25*(np.sin(10*x+4*y)+1)
f=(f-f.min())/(f.max()-f.min())

def quantize(img,bits):
    L=2**bits
    return np.round(img*(L-1))/(L-1)

def sample(img,step):
    return img[::step,::step]

fig,ax=plt.subplots(2,3,figsize=(9,6))
for j,step in enumerate([1,4,8]):
    for i,bits in enumerate([8,3]):
        g=quantize(sample(f,step),bits)
        ax[i,j].imshow(g,cmap='gray',vmin=0,vmax=1,interpolation='nearest')
        ax[i,j].set_title(f'step={step}, bits={bits}')
        ax[i,j].axis('off')
plt.tight_layout(); plt.show()
