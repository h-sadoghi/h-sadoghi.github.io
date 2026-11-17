"""Reproducible chapter 12 demonstrations. Python >=3.9, standard library only."""
from __future__ import annotations
from collections import Counter
import hashlib, math, random, json, time, tracemalloc

def events(n=30000,seed=12026):
    rng=random.Random(seed)
    for t in range(n):
        q = (0.08 if t < n//2 else 0.19) # deliberate distribution shift
        item = 'rare' if rng.random() < q else rng.choice(['bread','milk','coffee','rice'])
        yield (t,item)

def reservoir(items,k,seed=24):
    rng=random.Random(seed);sample=[]
    for t,item in enumerate(items,1):
        if t<=k:sample.append(item)
        else:
            j=rng.randrange(t)
            if j<k:sample[j]=item
    return sample

def h(key,seed,mod):
    return int.from_bytes(hashlib.blake2b((str(seed)+':'+str(key)).encode(),digest_size=8).digest(),'little')%mod

class CountMin:
    def __init__(self,width=512,depth=5):
        self.width,self.depth=width,depth
        self.a=[[0]*width for _ in range(depth)]
    def add(self,key,n=1):
        for i in range(self.depth):self.a[i][h(key,i,self.width)]+=n
    def estimate(self,key):return min(self.a[i][h(key,i,self.width)] for i in range(self.depth))

class Bloom:
    def __init__(self,m=8192,k=5):self.m,self.k=m,k;self.bits=bytearray((m+7)//8)
    def add(self,x):
        for j in range(self.k):
            v=h(x,j,self.m);self.bits[v//8]|=1<<(v%8)
    def contains(self,x):
        return all(self.bits[(v:=h(x,j,self.m))//8]&(1<<(v%8)) for j in range(self.k))

def drift_by_window(rows,window=1000):
    result=[];buf=[]
    for _,name in rows:
        buf.append(name)
        if len(buf)==window:
            result.append(buf.count('rare')/window);buf=[]
    return result

def benchmark(n=30000):
    rows=list(events(n));true=Counter(x for _,x in rows)
    cms=CountMin(width=256,depth=5)
    for _,x in rows:cms.add(x)
    sample=reservoir((x for _,x in rows),2000)
    bloom=Bloom()
    for x in true:bloom.add(x)
    return {'n':n,'exact':dict(true),'cms':{x:cms.estimate(x) for x in true},
       'reservoir_rare_share':round(sample.count('rare')/len(sample),5),
       'true_rare_share':round(true['rare']/n,5),
       'drift_window_rates':drift_by_window(rows),
       'bloom_known':all(bloom.contains(x) for x in true),
       'bloom_absent_test':bloom.contains('not-in-data')}

def self_test():
    assert reservoir(range(6),10)==list(range(6))
    assert len(reservoir(range(100),11))==11
    b=Bloom(1200,4)
    for i in range(50):b.add(str(i))
    assert all(b.contains(str(i)) for i in range(50))
    c=CountMin(64,4);d=Counter()
    for i in range(500):
        key=str(i%17);c.add(key);d[key]+=1
    assert all(c.estimate(k)>=v for k,v in d.items())
    result=benchmark(4000)
    assert sum(result['exact'].values())==4000
    assert all(result['cms'][k]>=v for k,v in result['exact'].items())
    return result

if __name__=='__main__':
    print('SELF_TEST_OK')
    print(json.dumps(self_test(),ensure_ascii=False,indent=2))
    print(json.dumps(benchmark(),ensure_ascii=False,indent=2))
