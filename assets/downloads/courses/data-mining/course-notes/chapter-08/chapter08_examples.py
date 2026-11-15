#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chapter 08: clustering foundations. Deterministic synthetic data only.

Usage: python chapter08_examples.py [--output example_results.json]
Reproduction needs numpy, pandas, scipy and scikit-learn, offline.
Ground-truth synthetic_group is reserved for post-hoc audit, NEVER for fitting.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score, silhouette_score, davies_bouldin_score
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

SEED = 824
FEATURES = ("x1", "x2")


def manual_example():
    names = ["A", "B", "C", "D", "E", "F"]
    x = np.array([[1., 1.], [1., 2.], [2., 1.], [8., 8.], [8., 9.], [9., 8.]])
    centers = np.array([[1., 1.], [8., 8.]])
    d2 = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    labels = d2.argmin(axis=1)
    next_centers = np.array([x[labels == k].mean(axis=0) for k in range(2)])
    sse = sum(float(((x[labels == k] - next_centers[k]) ** 2).sum()) for k in range(2))
    return dict(names=names, points=x, initial_centers=centers, labels=labels,
                new_centers=next_centers, sse=sse)


def manual_1d_dbscan(eps=1.1, min_samples=3):
    """Explicit counting includes the point itself, sklearn's convention."""
    x = np.array([0., 1., 2., 5., 8.])
    neighborhoods = [np.flatnonzero(np.abs(x - v) <= eps).tolist() for v in x]
    core = [i for i, neighbors in enumerate(neighborhoods) if len(neighbors) >= min_samples]
    border = [i for i, neighbors in enumerate(neighborhoods)
              if i not in core and any(j in core for j in neighbors)]
    noise = [i for i in range(len(x)) if i not in core and i not in border]
    return dict(x=x.tolist(), neighborhoods=neighborhoods, core=core, border=border, noise=noise)


def k_medoids_exhaustive(x, k=2):
    """Small-data teaching algorithm: exhaustively choose representatives minimizing L1 cost."""
    import itertools
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or not 1 <= k <= len(x):
        raise ValueError("Expected a nonempty (n,d) matrix and 1<=k<=n")
    d = pairwise_distances(x, metric='manhattan')
    best = None
    for candidate in itertools.combinations(range(len(x)), k):
        cost = float(np.min(d[:, list(candidate)], axis=1).sum())
        if best is None or cost < best[0] - 1e-10:
            best = (cost, candidate)
    return dict(cost=best[0], medoid_indices=list(best[1]), points=x[list(best[1])].tolist())


def produce_datasets(seed=SEED):
    rng = np.random.default_rng(seed)
    compact = []
    centers = np.array([[2.0, 2.0], [7.1, 2.1], [4.5, 7.1]])
    for g, mu in enumerate(centers):
        z = rng.normal(0, [0.52, 0.61], size=(65, 2)) + mu
        for row in z:
            compact.append(('compact', row[0], row[1], f'G{g+1}'))
    for row in rng.uniform([0., 0.], [9., 9.], size=(9, 2)):
        compact.append(('compact', row[0], row[1], 'injected_noise'))
    moons, labels = make_moons(n_samples=200, noise=0.065, random_state=seed)
    moons = (moons * np.array([2.15, 2.20]) + [4., 4.])
    rows = list(compact)
    rows.extend([('moons', r[0], r[1], f'arc{v+1}') for r, v in zip(moons, labels)])
    for row in rng.uniform([1.2, 1.8], [8.5, 7.7], size=(14, 2)):
        rows.append(('moons', row[0], row[1], 'injected_noise'))
    for row in rng.uniform([0., 0.], [9., 9.], size=(155, 2)):
        rows.append(('uniform', row[0], row[1], 'no_true_groups'))
    frame = pd.DataFrame(rows, columns=['dataset', 'x1', 'x2', 'synthetic_group'])
    frame.insert(0, 'observation_id', [f'R{i:04d}' for i in range(len(frame))])
    return frame


def feature_matrix(frame, subset):
    """No label or record identifier is ever included in fit features."""
    sub = frame.loc[frame.dataset == subset].copy()
    x = sub.loc[:, list(FEATURES)].to_numpy(dtype=float)
    if not np.isfinite(x).all():
        raise ValueError('Nonfinite features')
    return sub, x


def assess(x, labels, ignore_noise=True):
    labels = np.asarray(labels)
    keep = labels != -1 if ignore_noise else np.ones(len(labels), dtype=bool)
    used = labels[keep]
    uniq = set(used)
    if len(uniq) < 2 or len(uniq) >= keep.sum():
        return None
    return {
        'silhouette': float(silhouette_score(x[keep], used)),
        'davies_bouldin': float(davies_bouldin_score(x[keep], used)),
        'used': int(keep.sum()),
        'excluded_noise': int((~keep).sum()),
    }


def experiment(frame):
    compact, xc = feature_matrix(frame, 'compact')
    moons, xm = feature_matrix(frame, 'moons')
    uniform, xu = feature_matrix(frame, 'uniform')
    km = KMeans(n_clusters=3, random_state=SEED, n_init=20).fit(xc)
    ward = AgglomerativeClustering(n_clusters=3, linkage='ward').fit_predict(xc)
    db = DBSCAN(eps=0.38, min_samples=5).fit_predict(xm)
    kmm = KMeans(n_clusters=2, random_state=SEED, n_init=20).fit(xm)
    kunif = KMeans(n_clusters=3, random_state=SEED, n_init=20).fit(xu)
    centers = km.cluster_centers_
    # These synthetic_group labels are used ONLY for audit after fitting.
    clean = compact.synthetic_group != 'injected_noise'
    ar = adjusted_rand_score(compact.loc[clean, 'synthetic_group'], km.labels_[clean.to_numpy()])
    _,x0=feature_matrix(frame,'compact')
    errs=[]
    for k in range(1,9):
        errs.append(float(KMeans(n_clusters=k, random_state=SEED, n_init=20).fit(x0).inertia_))
    scores=[]
    for k in range(2,9):
        lab=KMeans(n_clusters=k, random_state=SEED, n_init=20).fit_predict(x0)
        scores.append(float(silhouette_score(x0,lab)))
    results = {
      'seed': SEED, 'counts': frame.dataset.value_counts().to_dict(),
      'manual_sse': manual_example()['sse'],
      'compact_kmeans_inertia': float(km.inertia_),
      'compact_kmeans_silhouette': float(silhouette_score(xc, km.labels_)),
      'compact_ward_silhouette': float(silhouette_score(xc, ward)),
      'compact_ari_audit_only': float(ar),
      'moons_dbscan': assess(xm,db),
      'moons_dbscan_clusters': int(len(set(db))-(int(-1 in db))),
      'moons_dbscan_noise': int(np.sum(db==-1)),
      'moons_kmeans_silhouette': float(silhouette_score(xm,kmm.labels_)),
      'uniform_kmeans_silhouette': float(silhouette_score(xu,kunif.labels_)),
      'elbow_inertia': errs, 'k_silhouettes': scores,
      'centers': np.round(centers,4).tolist(),
      'profile_means': compact.assign(cluster=km.labels_).groupby('cluster')[list(FEATURES)].mean().round(4).to_dict(orient='index'),
      'stability_repeated_seeds': []
    }
    for seed in range(8):
        other = KMeans(n_clusters=3, random_state=seed,n_init=1).fit_predict(xc)
        results['stability_repeated_seeds'].append(float(adjusted_rand_score(km.labels_,other)))
    return results


def run(output='example_results.json'):
    frame=produce_datasets()
    folder=Path(__file__).resolve().parent
    frame.to_csv(folder/'clustering_synthetic.csv', index=False, float_format='%.6f')
    result=experiment(frame)
    (folder/output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Manual SSE:', result['manual_sse'])
    print('Compact kmeans silhouette:',round(result['compact_kmeans_silhouette'],4))
    print('Moons DBSCAN clusters/noise:',result['moons_dbscan_clusters'],result['moons_dbscan_noise'])
    print('Uniform baseline kmeans silhouette:',round(result['uniform_kmeans_silhouette'],4))
    print('Saved:',folder/output)
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='example_results.json')
    run(parser.parse_args().output)
