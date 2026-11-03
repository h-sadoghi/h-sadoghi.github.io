"""Creates original educational figures for Chapter 07 (wavelets).
Usage: python chapter07_generate_figures.py --output my_figures
Requires numpy + matplotlib; uses chapter07_wavelet_core.py only.
All figure annotations are in English to avoid font/RTL rendering issues.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from chapter07_wavelet_core import (SQRT2, synthetic_image, dwt_haar_1d, idwt_haar_1d,
    dwt_haar_2d, multilevel_haar_2d, inverse_multilevel_haar_2d, wavelet_denoise,
    cwt_mexican_hat, soft_threshold)

OUT = None

def save(n,slug):
    plt.tight_layout(pad=1.5)
    plt.savefig(OUT/f'fig07_{n:02d}_{slug}.png',dpi=165,facecolor='white',bbox_inches='tight')
    plt.close()

def base(figsize=(10.5,4.5)):
    return plt.subplots(figsize=figsize)

def style(ax):
    ax.grid(alpha=.20); ax.spines[['top','right']].set_visible(False)

def box(ax, xy, width, height, label, color='#e8f1fa', fs=11):
    r=FancyBboxPatch(xy,width,height,boxstyle='round,pad=0.02,rounding_size=.03',facecolor=color,edgecolor='#315a7c',linewidth=1.3)
    ax.add_patch(r);ax.text(xy[0]+width/2,xy[1]+height/2,label,ha='center',va='center',fontsize=fs,weight='semibold')

def arrow(ax, a,b):
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',lw=2,color='#345e8a'))

def flow(fig_id,slug,nodes,arrows_,title=None,width=12):
    fig,ax=plt.subplots(figsize=(width,4.3))
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    for x,y,w,h,lab,c in nodes: box(ax,(x,y),w,h,lab,c)
    for a,b in arrows_:arrow(ax,a,b)
    if title:ax.set_title(title,fontsize=14,pad=8)
    save(fig_id,slug)

def plot_matrix(ax,a, title,vmin=None,vmax=None,cmap='gray', signed=False):
    if signed:
        cap=np.percentile(np.abs(a),99)+1e-9
        ax.imshow(a,cmap='coolwarm',vmin=-cap,vmax=cap,interpolation='nearest')
    else:
        ax.imshow(a,cmap=cmap,vmin=vmin,vmax=vmax,interpolation='nearest')
    ax.set_title(title,fontsize=11)
    ax.axis('off')

def main(output):
    global OUT
    OUT=Path(output);OUT.mkdir(parents=True,exist_ok=True)
    # 00: learning spine
    flow(0,'learning_path',[(.015,.38,.18,.24,'Known: Fourier','#e6eef7'),(.225,.38,.18,.24,'Why localization?','#f2f4d8'),(.435,.38,.16,.24,'CWT: scale / shift','#e8f6ef'),(.625,.38,.15,.24,'DWT: filter bank','#e8f6ef'),(.81,.38,.17,.24,'2D / reconstruction','#e6eef7')],
         [((.195,.5),(.224,.5)),((.405,.5),(.434,.5)),((.595,.5),(.624,.5)),((.775,.5),(.809,.5))], 'Chapter 7: from Fourier to wavelets')
    # signal
    N=512;t=np.arange(N)
    x=0.25*np.sin(2*np.pi*.016*t)+.8*np.sin(2*np.pi*.12*t)*(t<205)+.6*np.sin(2*np.pi*.062*t)*(t>305)
    fig,axs=plt.subplots(2,1,figsize=(10.6,6.1));axs[0].plot(t,x,lw=1.4);axs[0].axvspan(0,205,color='#e7effe',alpha=.55);axs[0].axvspan(305,512,color='#fef1d7',alpha=.65)
    axs[0].set(title='One signal: high frequencies first, lower frequencies later',xlabel='Sample location',ylabel='Amplitude');style(axs[0])
    sp=np.fft.rfftfreq(N);axs[1].plot(sp,np.abs(np.fft.rfft(x))/N,color='#bd663b');axs[1].set(xlabel='Frequency (cycles / sample)',ylabel='Fourier magnitude',title='Global Fourier spectrum: where did each component occur?');style(axs[1]);save(1,'fourier_global')
    # same Fourier magnitude shifted
    pulse=np.zeros(256);pulse[22:44]=1; pulse[25:33]=2.1
    shifted=np.roll(pulse,120)
    fig,axs=plt.subplots(2,1,figsize=(10.5,5.6));axs[0].plot(pulse,label='Event A',lw=2);axs[0].plot(shifted,label='Event B (shifted)',lw=2);axs[0].legend();axs[0].set(title='Two events at different positions',xlabel='Sample',ylabel='Amplitude');style(axs[0])
    axs[1].plot(abs(np.fft.rfft(pulse)),label='|FFT(A)|');axs[1].plot(abs(np.fft.rfft(shifted)),'--',label='|FFT(B)|');axs[1].set(title='Identical Fourier magnitude; phase carries position',xlabel='Frequency bin',ylabel='Magnitude');axs[1].legend();style(axs[1]);save(2,'same_magnitude')
    # mother wavelet scales shifts
    fig,axs=plt.subplots(1,3,figsize=(12,3.6));u=np.linspace(-7,7,700)
    for ax,scale,shift in zip(axs,[.7,1.5,2.6],[-2,0,1.7]):
        z=(u-shift)/scale;psi=(1-z*z)*np.exp(-z*z/2)/np.sqrt(scale)
        ax.plot(u,psi,color='#2878aa',lw=2);ax.axhline(0,color='gray',lw=.6);ax.set(title=f'Scale a={scale}; shift b={shift}',xlabel='Position',ylabel='Wavelet value');style(ax)
    save(3,'scale_and_shift')
    # local match correlation sliding
    pos=np.arange(500);edge=np.tanh((pos-260)/3);w=(1-((pos-260)/22)**2)*np.exp(-.5*((pos-260)/22)**2)/np.sqrt(22)
    fig,axs=plt.subplots(2,1,figsize=(10.5,5.5));axs[0].plot(pos,edge,color='#454545');axs[0].set(title='Signal with local transition',xlabel='Position');style(axs[0]);axs[1].plot(pos,w,color='#ad582c');axs[1].set(title='One shifted and scaled analysis wavelet',xlabel='Position');style(axs[1]);save(4,'wavelet_matching')
    # scalogram
    scales=np.arange(3,49)
    co=cwt_mexican_hat(x,scales)
    fig,ax=base((11,5.5));im=ax.imshow(np.abs(co),aspect='auto',origin='lower',extent=[0,512,scales[0],scales[-1]],cmap='viridis');ax.set(title='Illustrative CWT magnitude: position versus scale',xlabel='Sample location b',ylabel='Scale a (large = coarse)');fig.colorbar(im,ax=ax,label='|Coefficient|');save(5,'scalogram')
    # time frequency tiles
    fig,axs=plt.subplots(1,2,figsize=(11.5,4.1))
    for ax in axs:ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set(xlabel='Position / time',ylabel='Frequency');style(ax)
    axs[0].set_title('Fixed time-frequency windows (STFT idea)')
    for i in range(6):
        for j in range(4):axs[0].add_patch(Rectangle((i/6,j/4),1/6,1/4,fill=False,edgecolor='#4677a0',linewidth=1.4))
    axs[1].set_title('Wavelet: narrow high-frequency / wide low-frequency')
    for y1,y2,n in [(0,.25,2),(.25,.5,4),(.5,.75,8),(.75,1,16)]:
        for k in range(n):axs[1].add_patch(Rectangle((k/n,y1),1/n,y2-y1,fill=False,edgecolor='#4677a0',linewidth=1.4))
    save(6,'time_frequency_tiles')
    # continuous vs dyadic
    fig,axs=plt.subplots(1,2,figsize=(11,4.4));rng=np.random.default_rng(7)
    bb=rng.uniform(0,100,350); aa=rng.uniform(1,16,350)
    axs[0].scatter(bb,aa,s=10,alpha=.35);axs[0].set(title='CWT: dense scale / shift samples',xlabel='Shift b',ylabel='Scale a');style(axs[0])
    for j in range(4):
        a=2**j
        k=np.arange(0,100,a)
        axs[1].scatter(k,np.full(len(k),a),s=17)
    axs[1].set(title='DWT concept: dyadic sampling',xlabel='Shift b',ylabel='Scale a = 2^j');axs[1].set_yscale('log',base=2);style(axs[1]);save(7,'cwt_dwt_sampling')
    # haar 1d actual numbers
    signal=np.array([4,6,8,10],float);a,d=dwt_haar_1d(signal);a2,d2=dwt_haar_1d(a)
    fig,axs=plt.subplots(3,1,figsize=(10,7));axs[0].bar(np.arange(4),signal,color='#6799c8');axs[0].set(title='Input x = [4, 6, 8, 10]',xticks=range(4),ylabel='Signal');style(axs[0])
    axs[1].bar([0,1],a,label='a1 (average)');axs[1].bar([2.5,3.5],d,label='d1 (difference)',color='#cd8463');axs[1].set(xticks=[0,1,2.5,3.5],xticklabels=['a1[0]','a1[1]','d1[0]','d1[1]'],title='Level 1: normalized pairwise sum and difference');style(axs[1])
    axs[2].bar([0,1],np.r_[a2,d2],color=['#477fb2','#c07b42']);axs[2].set(xticks=[0,1],xticklabels=['a2 = 14','d2 = -4'],title='Level 2: decompose approximation only');style(axs[2]);save(8,'haar_hand_calculation')
    # frequency response Haar
    f=np.linspace(0,.5,512);w=2*np.pi*f
    lo=np.abs(1+np.exp(-1j*w))/np.sqrt(2);hi=np.abs(1-np.exp(-1j*w))/np.sqrt(2)
    fig,ax=base();ax.plot(f,lo,label='Low-pass: [1, 1] / sqrt(2)',lw=2);ax.plot(f,hi,label='High-pass: [1, -1] / sqrt(2)',lw=2);ax.set(title='Haar analysis filter magnitudes',xlabel='Normalized frequency (cycles / sample)',ylabel='Magnitude');ax.legend();style(ax);save(9,'filter_frequency_responses')
    # filterbank
    flow(10,'analysis_filterbank',[(.025,.4,.17,.2,'Input x[n]','#e8effa'),(.26,.66,.21,.19,'Low-pass h0','#e4f5e9'),(.26,.19,.21,.19,'High-pass h1','#fdeadd'),(.56,.66,.16,.19,'Downsample / 2','#e8effa'),(.56,.19,.16,.19,'Downsample / 2','#e8effa'),(.8,.66,.17,.19,'Approx. a[k]','#e4f5e9'),(.8,.19,.17,.19,'Detail d[k]','#fdeadd')],
       [((.195,.50),(.24,.75)),((.195,.50),(.24,.28)),((.47,.755),(.55,.755)),((.47,.285),(.55,.285)),((.72,.755),(.79,.755)),((.72,.285),(.79,.285))],title='DWT analysis = filter + downsample')
    # intuitive bank multiple
    fig,ax=plt.subplots(figsize=(11,4.5));ax.set_xlim(0,10);ax.set_ylim(0,4.5);ax.axis('off')
    for i,(lab,y,w,c) in enumerate([('Input bandwidth',3.6,8,'#aac4e5'),('Level-1 detail: fine',2.65,4,'#e3a77f'),('Level-2 detail: medium',1.7,2,'#e3a77f'),('Level-2 approx.: coarse',.75,2,'#9ed1b8')]):
        ax.add_patch(Rectangle((1,y),w,.55,facecolor=c,edgecolor='#37546f'));ax.text(1.1+w+.15,y+.25,lab,va='center',fontsize=11)
    ax.set_title('Conceptual splitting into frequency bands (not to exact scale)',fontsize=14);save(11,'frequency_band_splitting')
    # 1d hierarchy flow
    flow(12,'pyramid_decomposition',[(.005,.39,.14,.23,'Signal x','#ddeafe'),(.205,.58,.14,.23,'a1','#d9f1e5'),(.205,.16,.14,.23,'d1','#f7e4d5'),(.425,.58,.14,.23,'a2','#d9f1e5'),(.425,.16,.14,.23,'d2','#f7e4d5'),(.65,.58,.14,.23,'a3','#d9f1e5'),(.65,.16,.14,.23,'d3','#f7e4d5')],
      [((.145,.50),(.204,.70)),((.145,.50),(.204,.27)),((.345,.70),(.424,.70)),((.345,.70),(.424,.27)),((.565,.70),(.649,.70)),((.565,.70),(.649,.27))],title='Multilevel DWT: repeat decomposition on approximation only')
    # 2d quadrants conceptual
    fig,ax=plt.subplots(figsize=(8.2,5.6));a=np.zeros((4,4));ax.set_xlim(0,2);ax.set_ylim(0,2);ax.axis('off')
    blocks=[(0,1,'LL\nSmooth / coarse','#a3d9c1'),(1,1,'V\nVertical edges','#efc89b'),(0,0,'H\nHorizontal edges','#efc89b'),(1,0,'D\nDiagonal detail','#c2c1ed')]
    for x0,y0,txt,col in blocks:
        r=Rectangle((x0,y0),1,1,facecolor=col,edgecolor='#344a5f',linewidth=2);ax.add_patch(r);ax.text(x0+.5,y0+.5,txt,ha='center',va='center',fontsize=13)
    ax.set_title('Separable Haar transform: four subbands',fontsize=14);save(13,'four_subbands')
    # image and components
    z=synthetic_image(256);LL,H,V,D=dwt_haar_2d(z)
    fig,ax=base((6,5.3));plot_matrix(ax,z,'Original synthetic image');save(14,'synthetic_image')
    fig,axs=plt.subplots(2,2,figsize=(9.6,8.2));plot_matrix(axs[0,0],LL,'LL: coarse image',cmap='gray');plot_matrix(axs[0,1],V,'V: vertical structures',signed=True);plot_matrix(axs[1,0],H,'H: horizontal structures',signed=True);plot_matrix(axs[1,1],D,'D: diagonal details',signed=True);save(15,'four_band_image')
    # mosaic signed normalize manually
    def visband(b):return .5 + .5 * np.clip(b/(np.percentile(abs(b),99)+1e-9),-1,1)
    lev1=np.block([[np.clip(LL/510.,0,1),visband(V)],[visband(H),visband(D)]])
    a2,bands=multilevel_haar_2d(z,levels=2)
    h2,v2,d2=bands[-1]
    small=np.block([[np.clip(a2/1020,0,1),visband(v2)],[visband(h2),visband(d2)]])
    mosaic=lev1.copy();mosaic[:128,:128]=small
    fig,axs=plt.subplots(1,2,figsize=(10.8,5));plot_matrix(axs[0],lev1,'Level 1 coefficient layout',vmin=0,vmax=1);plot_matrix(axs[1],mosaic,'Level 2: split LL again',vmin=0,vmax=1);save(16,'coefficient_pyramid')
    # exact recovery
    approx,bands=multilevel_haar_2d(z,3);rec=inverse_multilevel_haar_2d(approx,bands)
    fig,axs=plt.subplots(1,3,figsize=(12.5,4.3));plot_matrix(axs[0],z,'Input');plot_matrix(axs[1],rec,'Inverse DWT: reconstructed');plot_matrix(axs[2],abs(rec-z),'Absolute difference (scale: 0 to 1e-10)',vmin=0,vmax=1e-10,cmap='inferno');save(17,'perfect_reconstruction')
    # soft threshold denoise
    rng=np.random.default_rng(42);noisy=np.clip(z+rng.normal(0,20,z.shape),0,255)
    den=wavelet_denoise(noisy,3,22)
    fig,axs=plt.subplots(1,3,figsize=(12,4.4));plot_matrix(axs[0],z,'Clean (synthetic)',vmin=0,vmax=255);plot_matrix(axs[1],noisy,'Gaussian noise',vmin=0,vmax=255);plot_matrix(axs[2],den,'Soft threshold: t = 22',vmin=0,vmax=255);save(18,'denoising_gallery')
    # MSE vs t denoising experiment with fixed values
    ts=np.arange(0,63,3);mse=[]
    for threshold in ts:
        result=wavelet_denoise(noisy,3,float(threshold));mse.append(float(np.mean((result-z)**2)))
    fig,ax=base((10,4.4));ax.plot(ts,mse,'o-',ms=4);ax.axhline(np.mean((noisy-z)**2),color='tab:red',ls='--',label='Noisy MSE');ax.set(title='Threshold trade-off for one synthetic noisy image',xlabel='Soft threshold t',ylabel='Mean squared error (MSE)');ax.legend();style(ax);save(19,'denoise_threshold_tradeoff')
    # coefficient sparsity compression idea
    allvals=np.concatenate([approx.flatten()]+[band.flatten() for group in bands for band in group]);absvals=np.abs(allvals)
    fractions=[1,.7,.4,.2,.1,.05];errors=[]
    for fraction in fractions:
        keep=int(np.ceil(fraction*len(allvals)));ix=np.argpartition(absvals,-keep)[-keep:];masked=np.zeros_like(allvals);masked[ix]=allvals[ix]
        idx=0;c=masked[:approx.size].reshape(approx.shape);idx=approx.size;bb=[]
        for group in bands:
            new=[]
            for b in group:new.append(masked[idx:idx+b.size].reshape(b.shape));idx+=b.size
            bb.append(tuple(new))
        recon=inverse_multilevel_haar_2d(c,bb);errors.append(float(np.mean((z-recon)**2)))
    fig,ax=base((10,4.4));ax.plot(np.array(fractions)*100,errors,'o-',lw=2);ax.set(title='Retaining largest wavelet coefficients (NOT a file-size benchmark)',xlabel='Coefficients retained (%)',ylabel='Reconstruction MSE');ax.invert_xaxis();style(ax);save(20,'coefficient_sparsity')
    # boundary
    s=np.array([2,3,4,7,11],float)
    sym=np.r_[s,s[-1]];zero=np.r_[s,0]
    fig,axs=plt.subplots(2,1,figsize=(10,5.6))
    axs[0].stem(np.arange(6),sym,basefmt=' ');axs[0].set(title='Even-length extension by repeating the last sample',xticks=range(6));style(axs[0]);axs[1].stem(np.arange(6),zero,basefmt=' ');axs[1].set(title='Zero-padding makes an artificial last difference',xticks=range(6));style(axs[1]);save(21,'boundary_effect')
    # compression chain
    flow(22,'jpeg2000_concept',[(.015,.37,.15,.25,'Image','#e8effa'),(.207,.37,.17,.25,'DWT 2D','#dceee4'),(.42,.37,.17,.25,'Quantization*','#fdf0df'),(.64,.37,.17,.25,'Entropy coding','#fdf0df'),(.85,.37,.14,.25,'Bitstream','#e8effa')],
        [((.165,.49),(.206,.49)),((.377,.49),(.419,.49)),((.59,.49),(.639,.49)),((.81,.49),(.849,.49))],title='JPEG 2000 simplified concept (*lossy mode only)')
    # 23: reconstruction bank
    flow(23,'synthesis_filterbank',[(.03,.63,.17,.19,'Approx. a[k]','#e4f5e9'),(.03,.17,.17,.19,'Detail d[k]','#fdeadd'),(.3,.63,.17,.19,'Upsample x2','#e8effa'),(.3,.17,.17,.19,'Upsample x2','#e8effa'),(.57,.63,.17,.19,'Synthesis g0','#e4f5e9'),(.57,.17,.17,.19,'Synthesis g1','#fdeadd'),(.82,.41,.15,.19,'Sum = x[n]','#e8effa')],
        [((.2,.73),(.3,.73)),((.2,.26),(.3,.26)),((.47,.73),(.569,.73)),((.47,.26),(.569,.26)),((.74,.73),(.82,.5)),((.74,.26),(.82,.5))],title='Perfect reconstruction: synthesis bank')
    # 24 localization detector
    p=np.zeros(256);p[46:53]=2;p[186:193]=2
    scales=np.arange(3,36);co=cwt_mexican_hat(p,scales)
    fig,axs=plt.subplots(2,1,figsize=(10.7,6.2));axs[0].plot(p);axs[0].set(title='Two separated short events',xlabel='Sample',ylabel='Amplitude');style(axs[0]);im=axs[1].imshow(abs(co),origin='lower',aspect='auto',extent=[0,256,3,35]);axs[1].set(xlabel='Location b',ylabel='Scale a',title='CWT reveals both event locations');fig.colorbar(im,ax=axs[1]);save(24,'localized_events')
    # 25 Parseval numeric
    fig,ax=plt.subplots(figsize=(8,4));orig=float(np.sum(z*z));co_energy=float(np.sum(approx**2)+sum(np.sum(b**2) for g in bands for b in g));ax.bar(['Image samples','DWT coefficients'],[orig,co_energy]);ax.set_title('Energy conservation (orthonormal Haar DWT)');ax.set_ylabel('Sum of squared values');ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0));save(25,'energy_conservation')
    print(f'Generated {len(list(OUT.glob("fig07_*.png")))} chapter figures into {OUT}')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='chapter07_generated_figures');args=ap.parse_args();main(args.output)
