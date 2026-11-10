"""Reproducible Chapter 3 data-mining proximity experiments; synthetic examples only."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt, log2, exp
from collections import Counter
from itertools import combinations
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent


def minkowski(a, b, p=2):
    if len(a) != len(b) or not a:
        raise ValueError("Vectors must be equally sized and nonempty")
    if p == float('inf'):
        return max(abs(x-y) for x, y in zip(a, b))
    if p < 1:
        raise ValueError("A metric Minkowski exponent must be p>=1")
    return sum(abs(x-y)**p for x,y in zip(a,b))**(1/p)


def binary_counts(a, b):
    if len(a)!=len(b): raise ValueError("Binary vector length mismatch")
    if not set(a).issubset({0,1}) or not set(b).issubset({0,1}):
        raise ValueError("Binary values must be 0 or 1")
    q=sum(x==1 and y==1 for x,y in zip(a,b))
    r=sum(x==1 and y==0 for x,y in zip(a,b))
    s=sum(x==0 and y==1 for x,y in zip(a,b))
    t=sum(x==0 and y==0 for x,y in zip(a,b))
    return q,r,s,t


def jaccard(a,b):
    q,r,s,t=binary_counts(a,b)
    return q/(q+r+s) if q+r+s else 1.0  # explicit both-empty convention


def smc(a,b):
    q,r,s,t=binary_counts(a,b)
    return (q+t)/(q+r+s+t) if a else float('nan')


def cosine(a,b):
    dot=sum(x*y for x,y in zip(a,b))
    aa=sum(x*x for x in a)
    bb=sum(x*x for x in b)
    if aa==0 or bb==0: raise ValueError("Cosine undefined for zero vector")
    return dot/sqrt(aa*bb)


def pearson(a,b):
    if len(a)!=len(b) or len(a)<2: raise ValueError("Pearson needs >=2 paired values")
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    return cosine([x-ma for x in a],[y-mb for y in b])


def gower_pair(row1, row2, specs):
    """Mixed-type Gower dissimilarity; specs dict of {kind, range, nlevels, weight}."""
    numerator=denominator=0.0
    details=[]
    for attr, spec in specs.items():
        a,b=row1.get(attr),row2.get(attr)
        if a is None or b is None: continue
        kind=spec['kind']; w=spec.get('weight',1.)
        if w<0: raise ValueError('Nonnegative weights only')
        if kind=='binary_asym' and a==0 and b==0: continue
        if kind in ('nominal','binary_sym','binary_asym'):
            dist=float(a!=b)
        elif kind=='ordinal':
            levels=spec['nlevels']
            if levels<2:raise ValueError('Ordinal levels must be >=2')
            dist=abs(a-b)/(levels-1)
        elif kind=='numeric':
            rng=spec['range']
            if rng<=0: raise ValueError('Range must be positive')
            dist=abs(a-b)/rng
        else: raise ValueError('Unknown attribute kind '+kind)
        numerator+=w*dist;denominator+=w; details.append((attr,dist,w))
    return (numerator/denominator if denominator else float('nan'),details)


def kl(p,q):
    if abs(sum(p)-1)>1e-9 or abs(sum(q)-1)>1e-9:
        raise ValueError('Distributions must sum to 1')
    if any(x<0 for x in p+q): raise ValueError('probabilities nonnegative')
    return sum(pi*log2(pi/qi) if pi>0 and qi>0 else (float('inf') if pi>0 else 0.) for pi,qi in zip(p,q))


def js(p,q):
    m=[(x+y)/2 for x,y in zip(p,q)]
    return (kl(p,m)+kl(q,m))/2


def mutual_information(pxy):
    """Discrete MI in bits from a joint matrix; no smoothing."""
    r=[sum(a) for a in pxy]
    c=[sum(row[j] for row in pxy) for j in range(len(pxy[0]))]
    return sum(p*log2(p/(r[i]*c[j])) for i,row in enumerate(pxy) for j,p in enumerate(row) if p>0)


def mahalanobis_diag(a,b,variances):
    if any(v<=0 for v in variances): raise ValueError('Positive variances required')
    return sqrt(sum((x-y)**2/v for x,y,v in zip(a,b,variances)))


def demonstrator():
    A=(0,0);B=(3,4);C=(0,6)
    pair={f'L{p}':{'B':minkowski(A,B,p),'C':minkowski(A,C,p)} for p in (1,2,float('inf'))}
    a=[1,1]+[0]*997+[0]
    b=[1,0]+[1]+[0]*997
    q,r,s,t=binary_counts(a,b)
    mixed_specs={
        'region':{'kind':'nominal'},
        'tier':{'kind':'ordinal','nlevels':4},
        'spend':{'kind':'numeric','range':200},
        'app':{'kind':'binary_sym'},
        'rare':{'kind':'binary_asym'}}
    m1=dict(region='north',tier=2,spend=100,app=1,rare=0)
    m2=dict(region='north',tier=4,spend=140,app=0,rare=0)
    gd,gparts=gower_pair(m1,m2,mixed_specs)
    P=[.75,.25];Q=[.5,.5]
    return {
      'minkowski':pair,
      'binary_counts':{'q':q,'r':r,'s':s,'t':t,'smc':smc(a,b),'jaccard':jaccard(a,b)},
      'cosine_scaled':cosine([1,2],[2,4]),
      'pearson_shifted':pearson([1,2,3],[11,12,13]),
      'gower':{'value':gd,'included':gparts},
      'kl_pq':kl(P,Q),'kl_qp':kl(Q,P),'js':js(P,Q),'sqrt_js':sqrt(js(P,Q)),
      'mi_perfect_binary':mutual_information([[.5,0],[0,.5]]),
      'mahalanobis':mahalanobis_diag([0,0],[3,1],[9,1]),
      'triangle_cosine':{'xz':1-cosine([1,0],[0,1]),'xy_plus_yz':2*(1-cosine([1,0],[1,1]))},
    }


if __name__=='__main__':
    print(json.dumps(demonstrator(),ensure_ascii=False,indent=2,sort_keys=True))
