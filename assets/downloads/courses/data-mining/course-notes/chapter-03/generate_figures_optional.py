from pathlib import Path
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch
from scipy.spatial.distance import cdist
out=Path(__file__).resolve().parent.parent/'images';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':11,'figure.dpi':145,'savefig.dpi':165,'axes.spines.top':False,'axes.spines.right':False})

def save(n):
 plt.tight_layout(pad=1.4);plt.savefig(out/f'fig03_{n:02d}.png',bbox_inches='tight');plt.close()

# 1 conceptual story
fig,ax=plt.subplots(figsize=(9.3,4.1));P={'A':(0,0),'B':(3,4),'C':(0,6)}
for p,(x,y) in P.items():ax.scatter(x,y,s=125);ax.annotate(f'{p} ({x},{y})',(x,y),xytext=(12,9),textcoords='offset points',weight='bold')
ax.plot([0,3],[0,4],ls='--',label='A to B: L2=5, L1=7');ax.plot([0,0],[0,6],ls=':',linewidth=2,label='A to C: L2=6, L1=6');ax.set(xlim=(-1,5),ylim=(-1,7),xlabel='Feature 1',ylabel='Feature 2',title='The nearest neighbor can change with the definition of distance');ax.grid(alpha=.23);ax.legend(loc='lower right');save(1)
# 2 matrix
fig,axes=plt.subplots(1,2,figsize=(10,4.3));X=np.array([[0,0],[3,4],[0,6]],float);D=cdist(X,X)
for ax,data,title,labels in zip(axes,[X,D],['Data matrix (objects x attributes)','Distance matrix (objects x objects)'],[['f1','f2'],['A','B','C']]):
 im=ax.imshow(data,cmap='Blues');ax.set_xticks(range(len(labels)),labels);ax.set_yticks(range(3),['A','B','C']);ax.set_title(title)
 for i in range(data.shape[0]):
  for j in range(data.shape[1]):ax.text(j,i,format(data[i,j],'.1f'),ha='center',va='center',fontsize=10,color='black')
fig.colorbar(im,ax=axes[-1],fraction=.045);save(2)
# 3 norm unit balls
fig,axes=plt.subplots(1,3,figsize=(11,3.8));t=np.linspace(-np.pi,np.pi,700)
for ax,p,name in zip(axes,[1,2,np.inf],['L1: diamond','L2: circle','L-infinity: square']):
 if p==np.inf:x=np.cos(t)/np.maximum(abs(np.cos(t)),abs(np.sin(t)));y=np.sin(t)/np.maximum(abs(np.cos(t)),abs(np.sin(t)))
 else:r=(abs(np.cos(t))**p+abs(np.sin(t))**p)**(-1/p);x=r*np.cos(t);y=r*np.sin(t)
 ax.plot(x,y,linewidth=2.5);ax.axhline(0,lw=.5);ax.axvline(0,lw=.5);ax.set(xlim=(-1.2,1.2),ylim=(-1.2,1.2),title=name,xlabel='x1',ylabel='x2');ax.set_aspect('equal');ax.grid(alpha=.15)
save(3)
# 4 scale ranking flip
fig,axes=plt.subplots(1,2,figsize=(9,4));A=(0,0);B=(3,0);C=(0,5)
for ax,mul in zip(axes,[1,2]):
 for name,v in [('A',A),('B',B),('C',C)]:
  x,y=v[0]*mul,v[1];ax.scatter(x,y,s=100);ax.annotate(name,(x,y),xytext=(7,8),textcoords='offset points')
 ax.set(xlim=(-1,8),ylim=(-1,7),xlabel=f'feature 1 x {mul}',ylabel='feature 2',title=f'Scale x{mul}: nearest to A is '+('B' if mul==1 else 'C'))
 ax.grid(alpha=.2)
save(4)
# 5 contingency with annotation
fig,ax=plt.subplots(figsize=(7,4.6));mat=np.array([[1,1],[1,997]]);ax.imshow(np.log1p(mat),cmap='Blues');ax.set_xticks([0,1],['B=1','B=0']);ax.set_yticks([0,1],['A=1','A=0']);ax.set(xlabel='Object B',ylabel='Object A',title='Sparse presence/absence: q=1, r=1, s=1, t=997');
for i in range(2):
 for j in range(2):ax.text(j,i,['q','r','s','t'][i*2+j]+f' = {mat[i,j]}',ha='center',va='center',weight='bold')
save(5)
# 6 Sets Jaccard
fig,ax=plt.subplots(figsize=(7,4.1));ax.add_patch(Circle((0,0),1,fill=False,lw=2));ax.add_patch(Circle((1.1,0),1,fill=False,lw=2));ax.text(-.6,0,'b',ha='center',fontsize=18);ax.text(.55,0,'a',ha='center',fontsize=18);ax.text(1.7,0,'c',ha='center',fontsize=18);ax.text(-.8,1.1,'Set A',ha='center');ax.text(1.7,1.1,'Set B',ha='center');ax.set(xlim=(-1.5,2.6),ylim=(-1.25,1.35),title='Jaccard: intersection / union = 1/3');ax.set_aspect('equal');ax.axis('off');save(6)
# 7 ordinal
fig,ax=plt.subplots(figsize=(9,2.2));names=['very low','low','medium','high','very high'];ax.scatter(np.arange(1,6),[0]*5,s=140);ax.plot(np.arange(1,6),[0]*5);ax.set_xticks(range(1,6),names);ax.set_ylim(-.5,.5);ax.set_yticks([]);ax.annotate('',xy=(4,.14),xytext=(2,.14),arrowprops={'arrowstyle':'<->'});ax.text(3,.24,'2 / (5 - 1) = 0.5',ha='center');ax.set_title('Ordinal codes are ranks, not physical intervals');save(7)
# 8 cosine vectors
fig,ax=plt.subplots(figsize=(6.2,5));ax.quiver([0,0,0],[0,0,0],[1,2,-1],[2,4,-2],angles='xy',scale_units='xy',scale=1);ax.text(1.1,2,'x=(1,2)');ax.text(2.2,4,'2x=(2,4)');ax.text(-1.2,-2.2,'-x');ax.set(xlim=(-2,3),ylim=(-3,5),title='Direction vs magnitude: cosine(x, 2x) = 1');ax.axhline(0,lw=.7);ax.axvline(0,lw=.7);ax.grid(alpha=.2);ax.set_aspect('equal');save(8)
# 9 cosine vs corr
fig,axes=plt.subplots(1,2,figsize=(9.2,3.7));x=np.array([1.,2.,3.]);y=x+10
axes[0].plot(range(3),x,marker='o',label='x');axes[0].plot(range(3),y,marker='s',label='y=x+10');axes[0].legend();axes[0].set_title('Raw observations: offset differs')
axes[1].plot(range(3),x-x.mean(),marker='o',label='x centered');axes[1].plot(range(3),y-y.mean(),marker='s',ls='--',label='y centered');axes[1].set_title('After centering: identical profiles');axes[1].legend();save(9)
#10 Mahalanobis axes
fig,ax=plt.subplots(figsize=(7,5));for_v=[(1,1),(4,2),(9,3)]
for v,r in for_v:ax.add_patch(Ellipse((0,0),2*3*r/3,2*r/3,angle=0,fill=False,lw=2))
ax.scatter([0,3],[0,1],s=90);ax.annotate('origin',(0,0),xytext=(-50,-20),textcoords='offset points');ax.annotate('point (3,1)',(3,1),xytext=(10,10),textcoords='offset points');ax.set(xlim=(-5,5),ylim=(-3.5,3.5),title='Covariance geometry: variance along x is 9, along y is 1');ax.grid(alpha=.2);ax.set_aspect('equal');save(10)
#11 mixed weighted distances
fig,ax=plt.subplots(figsize=(9,3.8));labs=['region','tier','spend','app','rare 0-0'];vals=[0,2/3,.2,1,0];bars=ax.barh(labs,vals);ax.invert_yaxis();ax.set(xlim=(0,1.1),xlabel='Per-attribute dissimilarity',title='Gower: omit asymmetric 0-0 in the denominator');
for i,v in enumerate(vals):ax.text(v+.025,i,'omitted' if i==4 else f'{v:.2f}',va='center');bars[-1].set_hatch('//');save(11)
#12 KL direction as bars
from math import log2
P=np.array([.75,.25]);Q=np.array([.5,.5]);fig,axes=plt.subplots(1,2,figsize=(9,3.4))
xx=np.arange(2);axes[0].bar(xx-.18,P,width=.35,label='P');axes[0].bar(xx+.18,Q,width=.35,label='Q');axes[0].set_xticks(xx,['Event 1','Event 2']);axes[0].set_ylim(0,1);axes[0].legend();axes[0].set_title('Distributions')
axes[1].bar(['KL(P||Q)','KL(Q||P)','JS(P,Q)'],[.1887218755,.2075187496,.0487949407]);axes[1].set_title('Direction matters (bits)');save(12)
#13 MI same correlation nonlinear sample
rng=np.random.default_rng(7);x=rng.uniform(-1,1,800);y=x*x+rng.normal(0,.065,len(x));z=rng.uniform(-1,1,800)
fig,axes=plt.subplots(1,2,figsize=(9,3.9));axes[0].scatter(x,y,s=5,alpha=.3);axes[0].set(xlabel='X',ylabel='Y',title=f'Nonlinear dependence, Pearson={np.corrcoef(x,y)[0,1]:.2f}')
axes[1].scatter(x,z,s=5,alpha=.3);axes[1].set(xlabel='X',ylabel='Z',title=f'Independent simulation, Pearson={np.corrcoef(x,z)[0,1]:.2f}');save(13)
#14 kernel PSD
X=np.array([[0],[1],[2],[3]],float);K=np.exp(-(cdist(X,X))**2);fig,axes=plt.subplots(1,2,figsize=(8.8,3.8));im=axes[0].imshow(K,vmin=0,vmax=1,cmap='Blues');axes[0].set_title('RBF Gram matrix');axes[0].set_xticks(range(4));axes[0].set_yticks(range(4));
for i in range(4):
 for j in range(4):axes[0].text(j,i,f'{K[i,j]:.2f}',ha='center',va='center',fontsize=9)
axes[1].bar(range(1,5),np.linalg.eigvalsh(K));axes[1].set(xlabel='Eigenvalue index',ylabel='Eigenvalue',title='All eigenvalues are nonnegative');save(14)
#15 high dimension
fig,ax=plt.subplots(figsize=(7.8,4));dims=[2,5,10,25,50,100,200];coef=[]
for p in dims:
 pairs=rng.normal(size=(4000,p));pairs2=rng.normal(size=(4000,p));dd=np.linalg.norm(pairs-pairs2,axis=1);coef.append(dd.std()/dd.mean())
ax.plot(dims,coef,marker='o');ax.set(xlabel='Dimension',ylabel='CV(pairwise Euclidean distance)',title='Distance concentration in an isotropic Gaussian simulation');ax.grid(alpha=.25);save(15)
#16 decision flow
fig,ax=plt.subplots(figsize=(11,4));boxes=[('Feature types','Numeric / binary / mixed'),('Meaning','Magnitude / direction / presence'),('Proximity','L2 / cosine / Jaccard / Gower'),('Validation','Scale, weights, neighbors, task')]
for i,(ttl,sub) in enumerate(boxes):
 x=i*3;ax.add_patch(Rectangle((x,1),2.55,1.4,fill=False,lw=2));ax.text(x+1.275,2,ttl,ha='center',weight='bold');ax.text(x+1.275,1.5,sub,ha='center',fontsize=9)
 if i<3:ax.annotate('',xy=(x+2.94,1.7),xytext=(x+2.58,1.7),arrowprops={'arrowstyle':'->','lw':1.8})
ax.set(xlim=(-.15,11.7),ylim=(.75,2.65));ax.axis('off');ax.set_title('Metric selection is a modeling decision, not just a formula');save(16)
#17 shortest path vs euclid
fig,ax=plt.subplots(figsize=(7,4.3));nd={'A':(0,0),'B':(2,0),'C':(2,2),'D':(0,2)};ed=[('A','B',2),('B','C',2),('C','D',2)]
for u,v,w in ed:
 a,b=nd[u],nd[v];ax.plot([a[0],b[0]],[a[1],b[1]],lw=3);ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.16,f'{w}',ha='center')
for n,(x,y) in nd.items():ax.scatter(x,y,s=170);ax.annotate(n,(x,y),xytext=(5,9),textcoords='offset points',weight='bold')
ax.plot([0,0],[0,2],ls=':',lw=2,label='Euclidean A-D = 2 (no direct edge)');ax.set(xlim=(-.4,2.5),ylim=(-.4,2.5),title='Graph distance A-D = 6, Euclidean distance = 2');ax.legend(loc='lower center');ax.set_aspect('equal');ax.grid(alpha=.2);save(17)
#18 missing comparison caveat
fig,ax=plt.subplots(figsize=(8,3.5));arr=np.array([[0,np.nan],[0,0],[1,0]])
for i in range(3):
 for j in range(2):
  ax.add_patch(Rectangle((j,i),.95,.9,fill=False));ax.text(j+.475,i+.45,'?' if np.isnan(arr[i,j]) else str(int(arr[i,j])),ha='center',va='center',fontsize=17)
ax.set(xlim=(0,2),ylim=(0,3));ax.invert_yaxis();ax.set_xticks([.475,1.475],['feature 1','feature 2']);ax.set_yticks([.45,1.45,2.45],['X','Y','Z']);ax.set_title('Pairwise deletion: d(X,Z)=1 but d(X,Y)+d(Y,Z)=0.5');save(18)
print('saved',len(list(out.glob('fig03_*.png'))),'figures')
