#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Mining Ch07 reproducible classification lessons.
All data are synthetic. Do not use model scores for operational decision making.
Python 3.10+, numpy, pandas and scikit-learn.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score,balanced_accuracy_score,confusion_matrix,precision_score,
                             recall_score,f1_score,average_precision_score,roc_auc_score,brier_score_loss)

SEED=207
FEATURES=['amount_toman_thousands','failed_attempts','new_device','night','prior_alerts']

def toy_rows() -> pd.DataFrame:
    # fixed, hand-checkable ten transactions (not the modeling benchmark)
    return pd.DataFrame([
        ['T01',980,1,3,1],['T02',870,1,2,1],['T03',770,1,2,1],
        ['T04',450,1,0,1],['T05',820,1,0,0],['T06',760,0,2,1],
        ['T07',250,0,1,0],['T08',410,0,0,0],['T09',120,0,0,0],
        ['T10',230,0,0,0]],
        columns=['order_id','amount','new_device','failed_attempts','label'])

def gini(labels) -> float:
    y=np.asarray(list(labels))
    if y.size == 0: raise ValueError('empty leaf')
    p=np.unique(y,return_counts=True)[1]/len(y)
    return float(1-np.sum(p*p))

def entropy(labels) -> float:
    y=np.asarray(list(labels))
    if y.size == 0: raise ValueError('empty leaf')
    p=np.unique(y,return_counts=True)[1]/len(y)
    return float(-sum(q*np.log2(q) for q in p))

def split_gain(values,labels,criterion='gini') -> dict:
    y=np.asarray(labels); x=np.asarray(values)
    if len(y)!=len(x) or not len(y): raise ValueError('invalid feature/target length')
    fn={'gini':gini,'entropy':entropy}[criterion]
    parent=fn(y)
    weighted=sum((x==z).mean()*fn(y[x==z]) for z in np.unique(x))
    return {'parent':float(parent),'children_weighted':float(weighted),'gain':float(parent-weighted)}

def laplace_nb_demo() -> dict:
    d=toy_rows()
    # predicting a new order: new_device=1, failed_attempts>=2
    p1=float((d.label==1).mean()); p0=1-p1
    a1=int(((d.label==1)&(d.new_device==1)).sum());a0=int(((d.label==0)&(d.new_device==1)).sum())
    b1=int(((d.label==1)&(d.failed_attempts>=2)).sum());b0=int(((d.label==0)&(d.failed_attempts>=2)).sum())
    n1=int((d.label==1).sum());n0=len(d)-n1
    # add one to each binary outcome (Laplace smoothing)
    score1=p1*(a1+1)/(n1+2)*(b1+1)/(n1+2)
    score0=p0*(a0+1)/(n0+2)*(b0+1)/(n0+2)
    return {'class1':score1,'class0':score0,'posterior':score1/(score1+score0)}

def make_synthetic(path: Path, *, customers=120, per_customer=6, seed=SEED) -> pd.DataFrame:
    """Event-level synthetic flags with within-customer correlation; reproducible."""
    rng=np.random.default_rng(seed)
    rows=[]
    for group_id in range(customers):
        latent=rng.normal()
        prior_alerts=int(rng.random()<1/(1+np.exp(-(-2.0+0.65*latent))))
        for event in range(per_customer):
            new=int(rng.random() < 1/(1+np.exp(-(-1.1+0.4*latent))))
            fail=int(rng.poisson(np.exp(-1.10+.25*latent+.4*new)))
            night=int(rng.random()<.20)
            amount=float(np.clip(rng.lognormal(np.log(325)+.18*latent,.60),35,3500))
            logit=-4.0 + .0075*(amount-350)+1.25*new + .62*fail + .5*night + .85*prior_alerts + .4*latent
            prob=1/(1+np.exp(-np.clip(logit,-20,20)))
            label=int(rng.random()<prob)
            rows.append([f'E{group_id:03d}-{event:02d}',f'C{group_id:03d}',round(amount,2),fail,new,night,prior_alerts,label])
    data=pd.DataFrame(rows,columns=['event_id','customer_id']+FEATURES+['fraud_flag'])
    path.parent.mkdir(parents=True,exist_ok=True)
    data.to_csv(path,index=False)
    return data

def split_by_customer(df: pd.DataFrame, *, seed=SEED):
    assert {'customer_id','fraud_flag'}.issubset(df)
    split=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed)
    development_idx,test_idx=next(split.split(df,df.fraud_flag,groups=df.customer_id))
    development=df.iloc[development_idx].copy(); test=df.iloc[test_idx].copy()
    split2=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed+1)
    train_idx,val_idx=next(split2.split(development,development.fraud_flag,groups=development.customer_id))
    train=development.iloc[train_idx].copy(); val=development.iloc[val_idx].copy()
    assert len(set(train.customer_id)&set(test.customer_id))==0
    assert len(set(val.customer_id)&set(test.customer_id))==0
    assert len(set(val.customer_id)&set(train.customer_id))==0
    return train,val,test

def score_at_threshold(y_true, p, threshold=.5) -> dict:
    y=np.asarray(y_true);p=np.asarray(p)
    if len(y)!=len(p):raise ValueError('mismatched vectors')
    y_hat=(p>=threshold).astype(int)
    tn,fp,fn,tp=confusion_matrix(y,y_hat,labels=[0,1]).ravel()
    result={'tp':int(tp),'fp':int(fp),'fn':int(fn),'tn':int(tn),
            'accuracy':float(accuracy_score(y,y_hat)),
            'balanced_accuracy':float(balanced_accuracy_score(y,y_hat)),
            'precision':float(precision_score(y,y_hat,zero_division=0)),
            'recall':float(recall_score(y,y_hat,zero_division=0)),
            'f1':float(f1_score(y,y_hat,zero_division=0))}
    return result

def total_cost(y_true,p,threshold,fn_cost=8,fp_cost=1) -> int:
    scores=score_at_threshold(y_true,p,threshold)
    return int(fn_cost*scores['fn']+fp_cost*scores['fp'])

def choose_threshold(y_val,p_val,fn_cost=8,fp_cost=1) -> dict:
    # threshold selection *only* on validation, never test
    candidates=np.round(np.linspace(.025,.975,39),3)
    tab=[(total_cost(y_val,p_val,t,fn_cost,fp_cost),float(t)) for t in candidates]
    cost,threshold=min(tab,key=lambda pair:(pair[0],-pair[1]))
    return {'threshold':threshold,'validation_cost':int(cost),'costs':tab}

def evaluate_pipeline(path: Path) -> dict:
    df=pd.read_csv(path)
    train,val,test=split_by_customer(df)
    x_tr=train[FEATURES]; y_tr=train.fraud_flag
    x_val=val[FEATURES];y_val=val.fraud_flag
    x_test=test[FEATURES];y_test=test.fraud_flag
    models={
        'majority':DummyClassifier(strategy='prior'),
        'tree':DecisionTreeClassifier(max_depth=3,min_samples_leaf=18,random_state=SEED),
        'logistic':make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000,random_state=SEED))}
    validation={};fitted={}
    for name,model in models.items():
        fitted[name]=clone(model).fit(x_tr,y_tr)
        p=fitted[name].predict_proba(x_val)[:,1]
        validation[name]={
            'ap':float(average_precision_score(y_val,p)),
            'roc_auc':float(roc_auc_score(y_val,p)),
            'brier':float(brier_score_loss(y_val,p))}
    selected=max(validation,key=lambda name:validation[name]['ap'])
    choice=choose_threshold(y_val,fitted[selected].predict_proba(x_val)[:,1])
    probs_test=fitted[selected].predict_proba(x_test)[:,1]
    scores=score_at_threshold(y_test,probs_test,choice['threshold'])
    metrics={'roc_auc':float(roc_auc_score(y_test,probs_test)),
             'average_precision':float(average_precision_score(y_test,probs_test)),
             'brier':float(brier_score_loss(y_test,probs_test))}
    for key in ['train','validation','test']:
        pass
    metrics.update(scores)
    # out-of-group CV only in development data, not in test
    development=pd.concat([train,val],ignore_index=True)
    cv=StratifiedGroupKFold(n_splits=4,shuffle=True,random_state=SEED)
    folds=[]
    for itr,iva in cv.split(development[FEATURES],development.fraud_flag,groups=development.customer_id):
        left=development.iloc[itr];right=development.iloc[iva]
        assert not set(left.customer_id)&set(right.customer_id)
        model=clone(models['logistic']).fit(left[FEATURES],left.fraud_flag)
        folds.append(float(average_precision_score(right.fraud_flag,model.predict_proba(right[FEATURES])[:,1])))
    return {
        'n_total':len(df),'prevalence_all':float(df.fraud_flag.mean()),
        'sizes':{'train':len(train),'validation':len(val),'test':len(test)},
        'prevalence':{'train':float(y_tr.mean()),'validation':float(y_val.mean()),'test':float(y_test.mean())},
        'model_validation':validation,'selected_model':selected,
        'selected_threshold':choice['threshold'],'validation_cost':choice['validation_cost'],
        'test':metrics,'group_cv_logistic_AP':folds,
        'baseline_test_ap':float(y_test.mean())}

def main() -> None:
    folder=Path(__file__).resolve().parent
    data=folder/'fraud_events_synthetic.csv'
    if not data.exists():make_synthetic(data)
    result=evaluate_pipeline(data)
    manual={'gini':split_gain(toy_rows().new_device,toy_rows().label),
            'entropy':split_gain(toy_rows().new_device,toy_rows().label,'entropy'),
            'laplace_nb':laplace_nb_demo(),
            'confusion':score_at_threshold([1]*20+[0]*180,[.9]*12+[.1]*8+[.9]*18+[.1]*162)}
    print(json.dumps({'manual':manual,'benchmark':result},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
