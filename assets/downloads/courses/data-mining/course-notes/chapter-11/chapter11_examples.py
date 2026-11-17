"""Chapter 11: reproducible significance analysis for DATA MINING.
Python >=3.10, standard library only for core scientific calculations.
Synthetic datasets, deterministic random number generators; no network access.
"""
from __future__ import annotations
import csv, math, random, statistics
from collections import Counter
from itertools import combinations
from pathlib import Path


def binomial_upper_tail(successes: int, trials: int, probability: float = 0.5) -> float:
    """Exact P[X>=successes], X~Binomial(n,p); valid for 0<=p<=1."""
    if not (0 <= successes <= trials and 0 <= probability <= 1):
        raise ValueError('binomial arguments out of range')
    return sum(math.comb(trials, k) * probability**k * (1-probability)**(trials-k)
               for k in range(successes, trials+1))


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float,float]:
    if not 0 <= successes <= trials or trials == 0 or z < 0:
        raise ValueError('Invalid Wilson interval arguments')
    p=successes/trials; z2=z*z; d=1+z2/trials
    c=(p+z2/(2*trials))/d
    w=z/d*math.sqrt(p*(1-p)/trials+z2/(4*trials*trials))
    return max(0,c-w),min(1,c+w)


def _check_p(pvalues):
    p=[float(x) for x in pvalues]
    if any((not math.isfinite(x) or x<0 or x>1) for x in p):
        raise ValueError('p-values must be finite in [0,1]')
    return p


def bonferroni(pvalues):
    p=_check_p(pvalues);n=len(p)
    return [min(1.0, n*x) for x in p]


def holm(pvalues):
    """Adjusted p-values, Holm step-down; FWER, arbitrary dependence."""
    p=_check_p(pvalues);n=len(p);idx=sorted(range(n),key=lambda i:p[i]);q=[0.0]*n
    lower=0.0
    for j,i in enumerate(idx):
        lower=max(lower,(n-j)*p[i]);q[i]=min(1.0,lower)
    return q


def benjamini_hochberg(pvalues):
    """BH adjusted p-values, FDR under independence/PRDS assumptions."""
    p=_check_p(pvalues);n=len(p);idx=sorted(range(n),key=lambda i:p[i]);q=[0.0]*n
    upper=1.0
    for j in range(n-1,-1,-1):
        i=idx[j];upper=min(upper,n*p[i]/(j+1));q[i]=upper
    return q


def discoveries(adjusted, alpha=0.05):
    return [i for i,p in enumerate(adjusted) if p<=alpha]


def mcnemar_exact(correct_a, correct_b):
    """Exact two-sided McNemar using discordant correctness; b/c counts."""
    a=list(correct_a);b=list(correct_b)
    if len(a)!=len(b) or not a:raise ValueError('Expected equal non-empty lists')
    bc=sum(bool(x) and not bool(y) for x,y in zip(a,b))
    cb=sum(not bool(x) and bool(y) for x,y in zip(a,b))
    n=bc+cb
    return (bc,cb,min(1.0,2*binomial_upper_tail(max(bc,cb),n,0.5))) if n else (0,0,1.0)


def permutation_difference(a,b,repetitions=4999,seed=202611):
    """Two-sided permutation p for independent groups. +1 Monte Carlo correction."""
    a=list(map(float,a));b=list(map(float,b))
    if not a or not b or repetitions<1:raise ValueError('Bad groups/repetitions')
    observed=sum(a)/len(a)-sum(b)/len(b);pool=a+b;rng=random.Random(seed)
    exceed=0
    for _ in range(repetitions):
        perm=pool.copy();rng.shuffle(perm)
        diff=sum(perm[:len(a)])/len(a)-sum(perm[len(a):])/len(b)
        exceed += abs(diff)>=abs(observed)-1e-12
    return observed,(1+exceed)/(1+repetitions)


def exact_permutation_difference(a,b):
    """Exhaustive two-sided permutation for a small, unpaired example."""
    a=list(map(float,a));b=list(map(float,b));p=a+b;n=len(a)
    if not a or not b or math.comb(len(p),n)>100_000:raise ValueError('example too large')
    target=abs(statistics.mean(a)-statistics.mean(b));success=0;total=0
    for ia in combinations(range(len(p)),n):
        total+=1;chosen=sum(p[i] for i in ia)
        d=abs(chosen/n-(sum(p)-chosen)/len(b))
        success+=d>=target-1e-12
    return success/total


def bootstrap_mean_difference(a,b,repetitions=3000,seed=42):
    """Percentile CI, independent-unit bootstrap, not a universal 95% guarantee."""
    a=list(map(float,a));b=list(map(float,b));rng=random.Random(seed)
    if not a or not b or repetitions<100:raise ValueError('Bad bootstrap input')
    dist=[]
    for _ in range(repetitions):
        aa=[rng.choice(a) for _ in a];bb=[rng.choice(b) for _ in b]
        dist.append(statistics.mean(aa)-statistics.mean(bb))
    dist.sort()
    return dist[int(0.025*(repetitions-1))],dist[int(0.975*(repetitions-1))]


def hypergeom_right_tail(overlap,population,positives,sample):
    """Fisher enrichment / hypergeometric right tail, fixed margins."""
    if not 0<=positives<=population or not 0<=sample<=population or not 0<=overlap<=min(positives,sample):
        raise ValueError('Invalid contingency table')
    denom=math.comb(population,sample)
    return sum(math.comb(positives,k)*math.comb(population-positives,sample-k)/denom
               for k in range(overlap,min(positives,sample)+1)
               if 0<=sample-k<=population-positives)


def fisher_association(a,b,c,d):
    """One-sided enrichment of co-occurrence in a 2x2 table."""
    if min(a,b,c,d)<0:raise ValueError('Negative count')
    return hypergeom_right_tail(a,a+b+c+d,a+b,a+c)


def random_split_overlap(size=200,train_fraction=0.7,seed=211):
    ids=list(range(size));random.Random(seed).shuffle(ids);k=int(size*train_fraction)
    return len(set(ids[:k])&set(ids[k:]))


def max_signal_null(repetitions=1000,number_of_features=100,seed=11):
    """Synthetic null: min p among independent uniform p-values per repetition."""
    rng=random.Random(seed)
    return [min(rng.random() for _ in range(number_of_features)) for _ in range(repetitions)]


def run_example(directory=None):
    p=[0.001,0.012,0.021,0.039,0.2,0.61]
    print('Exact one-sided binomial tail 8/10:',round(binomial_upper_tail(8,10),8))
    print('Wilson 8/10:',tuple(round(v,5) for v in wilson_interval(8,10)))
    for name,fun in [('Bonferroni',bonferroni),('Holm',holm),('Benjamini-Hochberg',benjamini_hochberg)]:
        q=fun(p);print(name,'adjusted', [round(x,5) for x in q], 'discoveries',discoveries(q))
    print('Exact permutation:',exact_permutation_difference([8,9,10],[1,2,3]))
    print('McNemar:',mcnemar_exact([1]*6+[0]*6,[0]*6+[0]*6))
    print('Fisher enrichment:',round(fisher_association(12,8,6,24),6))
    print('Train-test overlap:',random_split_overlap())
    if directory:
        with (Path(directory)/'pvalues_synthetic.csv').open(newline='',encoding='utf-8') as f:
            print('CSV rows:',len(list(csv.DictReader(f))))

if __name__=='__main__':
    run_example(Path(__file__).resolve().parent)
