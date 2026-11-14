#!/usr/bin/env python3
"""Chapter 05, Data Mining: reproducible basket-pattern mining.

All sample baskets are fictional. Python standard library only.
Run: python chapter05_examples.py --data baskets_synthetic.csv --min-count 3 --min-conf .70
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

BASE=Path(__file__).resolve().parent

def read_baskets(csv_path: str | Path) -> list[frozenset[str]]:
    baskets=[]
    ids=set()
    with Path(csv_path).open(encoding='utf-8-sig', newline='') as h:
        reader=csv.DictReader(h)
        if not {'tid','items'}.issubset(reader.fieldnames or []):
            raise ValueError('Required CSV columns: tid,items')
        for row in reader:
            tid=row['tid'].strip()
            if not tid or tid in ids:
                raise ValueError(f'Empty or duplicate transaction id: {tid!r}')
            ids.add(tid)
            items=[x.strip() for x in row['items'].split(';') if x.strip()]
            if not items: raise ValueError(f'Empty basket: {tid}')
            baskets.append(frozenset(items))
    return baskets

def support_count(baskets, itemset) -> int:
    q=frozenset(itemset)
    if not q: raise ValueError('An itemset must be non-empty')
    return sum(q<=b for b in baskets)

def apriori(baskets:list[frozenset[str]], min_count:int=2) -> dict[frozenset[str],int]:
    """All frequent nonempty itemsets, counted by Apriori levelwise pruning."""
    if not baskets or not 1<=min_count<=len(baskets): raise ValueError('Invalid sample size or support threshold')
    singles=Counter(item for b in baskets for item in b)
    prev={frozenset([x]) for x,c in singles.items() if c>=min_count}
    result={p:singles[next(iter(p))] for p in prev}
    k=2
    while prev:
        prior=sorted(prev, key=lambda s:tuple(sorted(s)))
        candidates=set()
        for a,b in itertools.combinations(prior,2):
            u=a|b
            if len(u)==k and all(frozenset(z) in prev for z in itertools.combinations(sorted(u),k-1)):
                candidates.add(u)
        next_level={}
        for itemset in sorted(candidates, key=lambda s:tuple(sorted(s))):
            count=support_count(baskets,itemset)
            if count>=min_count: next_level[itemset]=count
        result.update(next_level)
        prev=set(next_level)
        k+=1
    return result

def eclat(baskets:list[frozenset[str]], min_count:int=2) -> dict[frozenset[str],int]:
    """Vertical TID-set intersection search for every frequent itemset."""
    if not baskets or not 1<=min_count<=len(baskets): raise ValueError('Invalid support threshold')
    tidsets=defaultdict(set)
    for tid,b in enumerate(baskets):
        for x in b:tidsets[x].add(tid)
    items=sorted((x,t) for x,t in tidsets.items() if len(t)>=min_count)
    ans={}
    def dfs(prefix, suffix):
        for i,(item,tids) in enumerate(suffix):
            key=frozenset(prefix+(item,));ans[key]=len(tids)
            rest=[]
            for nxt,nxtids in suffix[i+1:]:
                overlap=tids & nxtids
                if len(overlap)>=min_count: rest.append((nxt,overlap))
            dfs(prefix+(item,),rest)
    dfs((),items)
    return ans

@dataclass
class FPNode:
    item:str | None
    count:int=0
    parent:'FPNode | None'=None
    children:dict[str,'FPNode']=field(default_factory=dict)


def fp_growth(baskets:list[frozenset[str]],min_count:int=2) -> dict[frozenset[str],int]:
    """FP-tree conditional pattern bases, recursive mining (no Apriori fallback)."""
    if not baskets or not 1<=min_count<=len(baskets):raise ValueError('Invalid support threshold')
    def build(weighted):
        freq=Counter()
        for items,w in weighted:
            for item in set(items): freq[item]+=w
        freq=Counter({x:c for x,c in freq.items() if c>=min_count})
        root=FPNode(None); header=defaultdict(list)
        for items,w in weighted:
            ordered=sorted((x for x in set(items) if x in freq),key=lambda x:(-freq[x],x))
            node=root
            for x in ordered:
                if x not in node.children:
                    node.children[x]=FPNode(x,0,node)
                    header[x].append(node.children[x])
                node=node.children[x]
                node.count+=w
        return freq,header
    def mine(weighted,suffix,found):
        freq,header=build(weighted)
        for item in sorted(freq,key=lambda x:(freq[x],x)):
            q=frozenset(suffix+(item,))
            if q in found: raise AssertionError('Duplicate FP itemset')
            found[q]=freq[item]
            conditional=[]
            for node in header[item]:
                path=[];parent=node.parent
                while parent is not None and parent.item is not None:
                    path.append(parent.item);parent=parent.parent
                if path: conditional.append((tuple(path),node.count))
            if conditional: mine(conditional,suffix+(item,),found)
    found={}
    mine([(tuple(b),1) for b in baskets],(),found)
    return found

def association_rules(frequent:dict[frozenset[str],int], n:int,min_conf:float=0.6)->list[dict]:
    if n<1 or not 0<=min_conf<=1:raise ValueError('Invalid n or confidence')
    out=[]
    for itemset,inter in frequent.items():
        if len(itemset)<2:continue
        seq=sorted(itemset)
        for size in range(1,len(seq)):
            for left in itertools.combinations(seq,size):
                A=frozenset(left); B=itemset-A
                cA=frequent[A];cB=frequent[B]
                conf=inter/cA
                if conf+1e-12<min_conf:continue
                sB=cB/n
                out.append({'antecedent':sorted(A),'consequent':sorted(B),
                            'count':inter,'support':inter/n,'confidence':conf,
                            'lift':conf/sB,
                            'leverage':inter/n-(cA/n)*(cB/n),
                            'conviction':(1-sB)/(1-conf) if conf<1 else None})
    return sorted(out,key=lambda x:(-x['lift'],-x['confidence'],tuple(x['antecedent']),tuple(x['consequent'])))

def closed_itemsets(frequent):
    """Frequent itemsets without an equally supported frequent proper superset."""
    return {x:c for x,c in frequent.items() if not any(x<y and c==c2 for y,c2 in frequent.items())}

def maximal_itemsets(frequent):
    """Frequent itemsets with no frequent proper superset."""
    return {x:c for x,c in frequent.items() if not any(x<y for y in frequent)}

def rule_metrics(baskets, antecedent, consequent):
    A=frozenset(antecedent);B=frozenset(consequent)
    if not A or not B or A&B:raise ValueError('Nonempty disjoint left/right required')
    n=len(baskets)
    a=support_count(baskets,A);b=support_count(baskets,B);ab=support_count(baskets,A|B)
    return {'n':n,'n_A':a,'n_B':b,'n_AB':ab,'support':ab/n,
            'confidence':ab/a if a else None,'lift':ab*n/(a*b) if a and b else None,
            'leverage':ab/n-(a/n)*(b/n)}

def simulate_rare_event(n:int=10000,rare_rate:float=.001,seed:int=17, sample:int=200):
    """Simple, seeded rare-event sampling example; no real-world claim."""
    import random
    rng=random.Random(seed)
    mask=[rng.random()<rare_rate for _ in range(n)]
    idx=rng.sample(range(n),sample)
    return {'population':n,'rare_in_population':sum(mask),'sample':sample,
            'rare_in_sample':sum(mask[i] for i in idx)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data',default=str(BASE/'baskets_synthetic.csv'))
    ap.add_argument('--min-count',type=int,default=3)
    ap.add_argument('--min-conf',type=float,default=.7)
    args=ap.parse_args()
    baskets=read_baskets(args.data)
    a=apriori(baskets,args.min_count)
    b=eclat(baskets,args.min_count)
    c=fp_growth(baskets,args.min_count)
    assert a==b==c,'Cross-algorithm mismatch'
    rules=association_rules(a,len(baskets),args.min_conf)
    output={'transactions':len(baskets),'min_count':args.min_count,
            'frequent_itemsets':[{'items':sorted(k),'count':v} for k,v in sorted(a.items(),key=lambda p:(len(p[0]),sorted(p[0])))],
            'closed_itemsets':[{'items':sorted(k),'count':v} for k,v in sorted(closed_itemsets(a).items(),key=lambda p:(len(p[0]),sorted(p[0])))],
            'maximal_itemsets':[{'items':sorted(k),'count':v} for k,v in sorted(maximal_itemsets(a).items(),key=lambda p:(len(p[0]),sorted(p[0])))],
            'rules':rules}
    print(json.dumps(output,ensure_ascii=False,indent=2,allow_nan=False,default=lambda o:'infinity' if o==math.inf else str(o)))
    return output
if __name__=='__main__':main()
