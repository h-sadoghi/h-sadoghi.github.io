"""Data Mining Chapter 10: transparent anomaly scores and safe evaluation.
Synthetic data only. No network, private data, or optional package needed for core.
Anomaly scores are high = more unusual. Python 3.12 + NumPy.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent


def robust_z(x, reference=None):
    """Modified Z-score with MAD of the *reference* sample; refuse MAD=0."""
    x = np.asarray(x, dtype=float)
    ref = np.asarray(x if reference is None else reference, dtype=float)
    if x.ndim != 1 or ref.ndim != 1 or len(ref) < 3 or not np.isfinite(x).all() or not np.isfinite(ref).all():
        raise ValueError('finite 1-D observations, >=3 reference observations required')
    m = np.median(ref)
    mad = np.median(np.abs(ref-m))
    if mad == 0:
        raise ValueError('MAD=0; do not divide by zero: use domain threshold or another score')
    return 0.6744897501960817 * (x-m) / mad


def tukey_bounds(reference, factor=1.5):
    a=np.asarray(reference,float)
    if a.ndim!=1 or len(a)<4 or not np.isfinite(a).all() or factor<0: raise ValueError('invalid reference')
    q1,q3=np.quantile(a,[.25,.75]);iqr=q3-q1
    return float(q1-factor*iqr),float(q3+factor*iqr)


def k_neighbor_scores(query, reference=None, k=3, exclude_self=False):
    """Euclidean distance to exactly k-th nearest neighbor. Stable sort, no tie expansion.
    Set exclude_self=True only when query IS the SAME ordered array as reference.
    """
    q=np.atleast_2d(np.asarray(query,float))
    r=np.atleast_2d(np.asarray(query if reference is None else reference,float))
    if q.shape[1]!=r.shape[1] or not np.isfinite(q).all() or not np.isfinite(r).all():raise ValueError('bad coordinates')
    if exclude_self and (len(q)!=len(r) or not np.array_equal(q,r)):raise ValueError('exclude_self requires identical ordered arrays')
    if k<1 or k>len(r)-int(exclude_self):raise ValueError('invalid k')
    d=np.linalg.norm(q[:,None,:]-r[None,:,:],axis=-1)
    if exclude_self: np.fill_diagonal(d,np.inf)
    return np.sort(d,axis=1,kind='stable')[:,k-1]


def lof_fixed_k(points,k=2):
    """Educational LOF: exactly k neighbors; excludes self; ties by input order.
    Standard LOF uses all k-distance ties. Here k is fixed for manual arithmetic.
    """
    x=np.atleast_2d(np.asarray(points,float));n=len(x)
    if n<3 or k<1 or k>=n or not np.isfinite(x).all():raise ValueError('invalid x or k')
    dist=np.linalg.norm(x[:,None]-x[None,:],axis=2)
    np.fill_diagonal(dist,np.inf)
    neighbors=np.argsort(dist,axis=1,kind='stable')[:,:k]
    kdist=np.take_along_axis(dist,neighbors[:,-1:],axis=1)[:,0]
    reach=np.maximum(kdist[neighbors],np.take_along_axis(dist,neighbors,axis=1))
    density=1/np.maximum(np.mean(reach,axis=1),1e-12)
    return np.mean(density[neighbors],axis=1)/density


def mahalanobis_scores(query,reference,regularization=1e-5):
    q=np.atleast_2d(np.asarray(query,float));r=np.atleast_2d(np.asarray(reference,float))
    if len(r)<3 or q.shape[1]!=r.shape[1] or regularization<=0:raise ValueError('invalid input')
    mu=r.mean(axis=0);cov=np.atleast_2d(np.cov(r,rowvar=False))+regularization*np.eye(r.shape[1]);delta=q-mu
    return np.sqrt(np.einsum('ij,jk,ik->i',delta,np.linalg.inv(cov),delta).clip(min=0))


def contextual_score(amount,group,reference_amount,reference_group):
    """Absolute residual from robust group median. Requires every group represented."""
    groups=np.asarray(group);rg=np.asarray(reference_group);a=np.asarray(amount,float);ra=np.asarray(reference_amount,float)
    if len(a)!=len(groups) or len(ra)!=len(rg):raise ValueError('inconsistent lengths')
    lookup={g:float(np.median(ra[rg==g])) for g in np.unique(rg)}
    if any(g not in lookup for g in groups):raise ValueError('unseen context group')
    return np.array([abs(v-lookup[g]) for v,g in zip(a,groups)])


def scan_window_mean(series,window=4,baseline=0.0):
    """Causal trailing window score; output first window-1 NaN (not zero)."""
    a=np.asarray(series,float)
    if a.ndim!=1 or window<1 or window>len(a) or not np.isfinite(a).all():raise ValueError('invalid series/window')
    out=np.full(len(a),np.nan)
    for t in range(window-1,len(a)):out[t]=abs(np.mean(a[t-window+1:t+1])-baseline)
    return out


def positive_cusum(series,baseline=0.0,drift=0.25):
    """One-sided CUSUM S_t=max(0,S_{t-1}+x_t-baseline-drift)."""
    if drift<0:raise ValueError('drift must be nonnegative')
    result=[];s=0.
    for val in series:
        s=max(0.,s+float(val)-baseline-drift);result.append(s)
    return np.asarray(result)


def precision_recall_at_k(labels,scores,k):
    y=np.asarray(labels,int);s=np.asarray(scores,float)
    if len(y)!=len(s) or len(y)==0 or not np.isin(y,[0,1]).all() or not np.isfinite(s).all() or k<1 or k>len(y):raise ValueError('invalid input')
    sel=np.argsort(-s,kind='stable')[:k]
    hits=int(y[sel].sum()); positives=int(y.sum())
    return {'hits':hits,'precision_at_k':hits/k,'recall_at_k':hits/positives if positives else None}


def confusion_at_threshold(labels,scores,threshold):
    y=np.asarray(labels,int);s=np.asarray(scores,float)
    if len(y)!=len(s) or not np.isin(y,[0,1]).all() or not np.isfinite(s).all():raise ValueError('invalid input')
    pred=s>=threshold
    return {'TP':int(((y==1)&pred).sum()),'FP':int(((y==0)&pred).sum()),'FN':int(((y==1)&~pred).sum()),'TN':int(((y==0)&~pred).sum())}


def make_synthetic(seed=1042):
    """Returns a deliberately synthetic event log with saved ground-truth flags for evaluation only."""
    rng=np.random.default_rng(seed)
    n=300;account=np.repeat(np.arange(30),10);group=np.where(account%2==0,'retail','business')
    base=np.where(group=='retail',3.3,5.0);amount=np.exp(base+rng.normal(0,.28,n))
    hour=(np.tile(np.arange(10,20),30)+rng.integers(-2,3,n))%24
    flag=np.zeros(n,int)
    # Inject isolated high amounts and lower magnitude contextual surprises.
    isolated=[35,117,164,222,276];contextual=[58,143,205,291]
    for i in isolated:amount[i]*=8;flag[i]=1
    for i in contextual:amount[i]*=(3.0 if group[i]=='retail' else .24);flag[i]=1
    # A sustained group of unusual events, which should be inspected collectively.
    for i in range(253,259):amount[i]*=1.8;flag[i]=1
    return [{'event_id':i,'account_id':int(account[i]),'peer_group':group[i],'hour':int(hour[i]),'amount':round(float(amount[i]),2),'synthetic_truth_for_evaluation_only':int(flag[i])} for i in range(n)]


def write_example_files(folder=HERE):
    folder=Path(folder);rows=make_synthetic();p=folder/'events_synthetic.csv'
    with p.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    signals={'baseline':[0.1,-.3,0.4,-.1,0.0,.2,.1,.1], 'isolated_spike':[0.1,-.3,0.4,7.0,0.0,.2,.1,.1],
             'collective_shift':[0.1,-.3,0.4,-.1,1.5,1.6,1.7,1.4], 'units':'standardized sensor residuals', 'data_kind':'synthetic'}
    (folder/'signals_synthetic.json').write_text(json.dumps(signals,indent=2),encoding='utf8')
    return p


def demonstration():
    manual=[10,11,11,12,12,13,13,14,15,48]
    points=np.array([[0.],[.1],[.2],[.3],[.4],[1.8]])
    rows=make_synthetic();amount=np.array([r['amount'] for r in rows]);group=np.array([r['peer_group'] for r in rows]);truth=np.array([r['synthetic_truth_for_evaluation_only'] for r in rows]);train=np.array([r['event_id']<200 for r in rows]);
    ctx=contextual_score(amount,group,amount[train],group[train]);rank=precision_recall_at_k(truth,ctx,k=15)
    result={'median':float(np.median(manual)),'mad':float(np.median(abs(np.array(manual)-np.median(manual)))),'robust_z_48':float(robust_z([48],manual)[0]),'iqr_bounds':tukey_bounds(manual), 'fixed_k_lof':lof_fixed_k(points,2).round(6).tolist(), 'contextual_precision_at_15':rank,'anomaly_count':int(truth.sum()),'count':len(rows)}
    (HERE/'example_results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    return result

if __name__=='__main__':
    write_example_files();print(json.dumps(demonstration(),indent=2,ensure_ascii=False))
