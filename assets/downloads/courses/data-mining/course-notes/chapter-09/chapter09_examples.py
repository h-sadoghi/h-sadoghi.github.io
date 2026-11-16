"""Chapter 09: advanced clustering. Synthetic examples; no downloads/network.

Required: NumPy >=1.24. Optional demonstrations: scipy/scikit-learn/matplotlib.
The implementation is deliberately transparent; not optimized for large data.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np


def _log_normal_1d(x, mu, var):
    if var <= 0:
        raise ValueError('variance must be positive')
    return -0.5 * (np.log(2 * np.pi * var) + (np.asarray(x) - mu) ** 2 / var)


def gmm_em_1d(x, centers=None, var=1.5, max_iter=100, tol=1e-9, min_var=1e-5):
    """Two normal components, learned means/variances/priors; stabilized E step."""
    x = np.asarray(x, float).reshape(-1)
    if len(x) < 3 or not np.isfinite(x).all() or min_var <= 0:
        raise ValueError('invalid x or variance floor')
    if centers is None:
        centers = [float(np.quantile(x, .25)), float(np.quantile(x, .75))]
    means = np.asarray(centers, float)
    if means.shape != (2,) or not np.isfinite(means).all():
        raise ValueError('centers must contain two finite values')
    if var <= 0: raise ValueError('positive initial variance required')
    variances = np.array([float(var), float(var)])
    weights = np.array([.5, .5])
    history = []
    for _ in range(max_iter):
        logp = np.stack([np.log(max(weights[k], 1e-15)) + _log_normal_1d(x, means[k], variances[k]) for k in range(2)], axis=1)
        row_max = logp.max(axis=1, keepdims=True)
        shifted = np.exp(logp-row_max)
        denom = shifted.sum(axis=1, keepdims=True)
        gamma = shifted / denom
        ll = float((row_max + np.log(denom)).sum())
        history.append(ll)
        if len(history) > 1 and abs(history[-1]-history[-2]) <= tol * (1 + abs(history[-2])):
            break
        nk = gamma.sum(axis=0)
        weights = nk / len(x)
        means = (gamma * x[:, None]).sum(axis=0) / np.maximum(nk, 1e-15)
        variances = np.maximum((gamma * (x[:, None]-means[None,:])**2).sum(axis=0) / np.maximum(nk, 1e-15), min_var)
    return {'means':means, 'variances':variances, 'weights':weights,
            'responsibilities':gamma, 'loglikelihood':history}


def gmm_bic(log_likelihood, n_samples, n_components=2, dim=1):
    """Full covariance Gaussian mix; k-1 weights + kd means + k*d*(d+1)/2 vars."""
    k,d = n_components,dim
    p = k - 1 + k*d + k*d*(d+1)//2
    return -2 * float(log_likelihood) + p*np.log(n_samples)


def fuzzy_membership_1d(x, centers, m=2.0):
    """Fuzzy c-means membership; zero-distance handled exactly."""
    if m <= 1: raise ValueError('fuzzifier m must be >1')
    ds = np.abs(np.asarray(centers, float) - float(x))
    if not np.isfinite(ds).all(): raise ValueError('finite values required')
    if (ds==0).any():
        out = np.zeros(len(ds),float)
        out[ds==0] = 1.0 / (ds==0).sum()
        return out
    p = 2/(m-1)
    inv = ds**(-p)
    return inv/inv.sum()


def fuzzy_cmeans_1d(x, centers, m=2, max_iter=80):
    x = np.asarray(x, float)
    c = np.asarray(centers, float).copy()
    if c.ndim != 1 or len(c)<2:raise ValueError('need >=2 centers')
    for _ in range(max_iter):
        u = np.stack([fuzzy_membership_1d(v,c,m) for v in x])
        um = u**m
        new = (um*x[:,None]).sum(axis=0)/np.maximum(um.sum(axis=0),1e-20)
        if np.max(np.abs(new-c))<1e-9: c=new;break
        c=new
    return c, np.stack([fuzzy_membership_1d(v,c,m) for v in x])


def graph_laplacian(w, normalized=True):
    w = np.asarray(w, float)
    if w.ndim!=2 or w.shape[0]!=w.shape[1] or np.any(w<0) or not np.allclose(w,w.T):
        raise ValueError('W must be square, symmetric, nonnegative')
    d = w.sum(axis=1)
    if normalized:
        if np.any(d<=0): raise ValueError('isolated nodes: normalized Laplacian undefined in this lesson')
        inv = 1/np.sqrt(d)
        return np.eye(len(w)) - inv[:,None]*w*inv[None,:]
    return np.diag(d)-w


def spectral_embedding(w, k=2):
    """Return smallest eigenvectors of symmetric normalized Laplacian, row normalized."""
    lap = graph_laplacian(w, normalized=True)
    values,vecs = np.linalg.eigh(lap)
    if k<1 or k>len(w):raise ValueError('invalid k')
    z = vecs[:,:k]
    norms = np.linalg.norm(z,axis=1,keepdims=True)
    z = z/np.maximum(norms,1e-15)
    return values,z


def shared_neighbor_similarity(neighbors_a,neighbors_b):
    return len(set(neighbors_a) & set(neighbors_b))


def bicluster_msr(a):
    """Mean squared residue of submatrix; 0 for ideal additive bicluster."""
    a=np.asarray(a,float)
    if a.ndim!=2 or min(a.shape)<2:raise ValueError('at least 2x2')
    residue=a-a.mean(axis=1,keepdims=True)-a.mean(axis=0,keepdims=True)+a.mean()
    return float(np.mean(residue**2))


def nmf_mu(v, rank=2, steps=300, seed=7, eps=1e-9):
    v=np.asarray(v,float)
    if v.ndim!=2 or np.min(v)<0 or rank<1:raise ValueError('NMF requires nonnegative matrix')
    rng=np.random.default_rng(seed)
    w=rng.uniform(.15,1.,size=(v.shape[0],rank))
    h=rng.uniform(.15,1.,size=(rank,v.shape[1]))
    errors=[]
    for _ in range(steps):
        h*= (w.T@v)/(w.T@w@h+eps)
        w*= (v@h.T)/(w@h@h.T+eps)
        errors.append(float(np.linalg.norm(v-w@h,ord='fro')))
    return w,h,errors


def cf_summary(points):
    """BIRCH CF triple (N, LS, SS) with SS=sum_i ||x_i||^2 scalar."""
    x=np.asarray(points,float)
    if x.ndim!=2 or len(x)==0:raise ValueError('nonempty rows x features')
    return {'N':len(x),'LS':x.sum(axis=0),'SS':float(np.sum(x*x))}


def merge_cf(a,b):
    return {'N':a['N']+b['N'],'LS':a['LS']+b['LS'],'SS':a['SS']+b['SS']}


def cf_sse(cf):
    return max(0.,float(cf['SS']-np.dot(cf['LS'],cf['LS'])/cf['N']))


def make_data(output_dir):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(2209)
    n=110
    x=np.r_[rng.normal(loc=(-1,0),scale=(.84,.34),size=(n,2)),
            rng.normal(loc=(1.1,.40),scale=(.70,.56),size=(n,2))]
    hidden=np.r_[np.zeros(n,dtype=int),np.ones(n,dtype=int)]
    with (out/'overlap_synthetic.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['id','x1','x2','synthetic_component_not_for_fit'])
        for i,(row,label) in enumerate(zip(x,hidden),1): w.writerow([f'S{i:03d}',round(float(row[0]),6),round(float(row[1]),6),int(label)])
    high=np.c_[x, rng.normal(0,1,size=(len(x),18))]
    with (out/'highdim_synthetic.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['id']+[f'f{i:02d}' for i in range(1,21)])
        for i,row in enumerate(high,1):writer.writerow([f'S{i:03d}']+[round(float(q),6) for q in row])
    # Additive bicluster submatrix with row and column offsets, independent rest is noisy.
    a=rng.uniform(.1,2.8,size=(10,9))
    rr=np.arange(4)[:,None]*.60
    cc=np.arange(5)[None,:]*.26
    a[2:6,3:8]=3.0+rr+cc
    with (out/'bicluster_synthetic.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['sample']+[f'feat_{j+1}' for j in range(9)])
        for i,row in enumerate(a):writer.writerow([f'R{i+1}']+[round(float(t),5) for t in row])
    w=np.zeros((8,8),float)
    for grp in ([0,1,2,3],[4,5,6,7]):
        for i in grp:
            for j in grp:
                if i!=j:w[i,j]=1.0
    w[3,4]=w[4,3]=.12
    (out/'network_synthetic.json').write_text(json.dumps({'nodes':[f'v{i+1}' for i in range(8)],'weights':w.tolist(),'note':'two 4-node dense communities with weak bridge'},indent=2),encoding='utf8')
    return x,high,a,w


def demo(output_dir=None):
    dest=Path(output_dir or Path(__file__).parent)
    x,high,a,w=make_data(dest)
    toy=np.array([-.7,-.2,.2,.6,2.5,3.2,4.1,4.8])
    gmm=gmm_em_1d(toy,centers=[0,4],var=1.6)
    eigenvalues, emb=spectral_embedding(w)
    cf=cf_summary(np.array([[1.,1.],[2.,1.],[5.,4.]]))
    mat=a[2:6,3:8]
    res={'gmm_means':[round(float(t),5) for t in gmm['means']],
         'gmm_weights':[round(float(t),5) for t in gmm['weights']],
         'gmm_ll_initial_final':[round(gmm['loglikelihood'][0],5),round(gmm['loglikelihood'][-1],5)],
         'posterior_x2': [round(float(q),6) for q in _posterior_example()],
         'fuzzy_x2_centers_0_5':[round(float(q),6) for q in fuzzy_membership_1d(2,[0,5])],
         'laplacian_eigenvalues':[round(float(t),6) for t in eigenvalues],
         'bicluster_msr':round(bicluster_msr(mat),10),
         'cf_n':cf['N'],'cf_sse':round(cf_sse(cf),6),
         'synthetic_rows':len(x),'synthetic_features':high.shape[1]}
    (dest/'example_results.json').write_text(json.dumps(res,indent=2,ensure_ascii=False),encoding='utf8')
    return res


def _posterior_example():
    z=np.exp(np.array([_log_normal_1d(2.,1.,1.),_log_normal_1d(2.,4.,1.)]))
    return z/z.sum()

if __name__=='__main__':
    print(json.dumps(demo(),ensure_ascii=False,indent=2))
