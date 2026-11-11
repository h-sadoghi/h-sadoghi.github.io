"""Chapter 4 data mining: reproducible, synthetic examples. Python 3.10+.

All data are educational synthetic data; functions avoid downloading anything.
Only numpy and pandas are needed for core examples; matplotlib/scikit-learn optional.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 1405


def generate_transactions(n: int = 320, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Synthetic store transactions; rare_event is diagnostic ground truth, not a model input."""
    rng = np.random.default_rng(seed)
    city = rng.choice(["A", "B", "C"], size=n, p=[.55, .33, .12])
    category = rng.choice(["grocery", "home", "electronics", "other"], n,
                          p=[.60, .25, .10, .05])
    day = rng.integers(0, 45, size=n)
    visits30 = rng.poisson(3, size=n) + 1
    units = rng.poisson(2, size=n) + 1
    discount_pct = rng.choice([0, 5, 10, 15], size=n, p=[.55, .20, .18, .07])
    city_effect = np.select([city == "B", city == "C"], [30, 80], default=0)
    spend = 35 + 18 * units + 3 * visits30 + city_effect + rng.normal(0, 8, n)
    rare_idx = rng.choice(n, size=max(1, n // 25), replace=False)
    rare_event = np.zeros(n, dtype=int)
    rare_event[rare_idx] = 1
    spend[rare_idx] += rng.uniform(140, 230, len(rare_idx))
    spend = np.round(np.maximum(spend, 0), 2)
    return pd.DataFrame({"transaction_id": [f"T{i:04d}" for i in range(n)],
                         "day": day, "city": city, "category": category,
                         "units": units, "visits30": visits30,
                         "discount_pct": discount_pct, "spend": spend,
                         "rare_event": rare_event})


def aggregate_day(df: pd.DataFrame) -> pd.DataFrame:
    """One record per day, retaining both total and transaction counts."""
    return df.groupby("day", as_index=False).agg(
        total_spend=("spend", "sum"), n_transactions=("spend", "size"),
        mean_spend=("spend", "mean"), rare_events=("rare_event", "sum"))


def srs_without_replacement(df: pd.DataFrame, n: int, seed: int = RANDOM_SEED) -> pd.DataFrame:
    if n > len(df) or n < 0:
        raise ValueError("Require 0 <= n <= len(df).")
    return df.sample(n=n, replace=False, random_state=seed).reset_index(drop=True)


def stratified_sample(df: pd.DataFrame, stratum: str, n_per_stratum: dict, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Fixed allocation per stratum; nonproportional allocation requires weights for population means."""
    pieces = []
    for offset, (key, num) in enumerate(n_per_stratum.items()):
        sub = df.loc[df[stratum] == key]
        if num < 0 or num > len(sub):
            raise ValueError(f"Invalid allocation for stratum {key!r}")
        pieces.append(sub.sample(n=num, replace=False, random_state=seed + offset))
    return pd.concat(pieces, ignore_index=True)


def weighted_stratum_mean(sample: pd.DataFrame, population: pd.DataFrame, stratum: str, value: str) -> float:
    """Estimator sum_h (N_h/N) * sample_mean_h; all population strata need sampled records."""
    p = population[stratum].value_counts(normalize=True)
    m = sample.groupby(stratum)[value].mean()
    if set(p.index) != set(m.index):
        raise ValueError("Each population stratum requires at least one sample.")
    return float(sum(p[h] * m[h] for h in p.index))


def reservoir_sample(stream, k: int, seed: int = RANDOM_SEED) -> list:
    """Uniform sample without replacement from an unknown-length stream."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    rng = np.random.default_rng(seed)
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        elif k:
            j = rng.integers(0, i + 1)
            if j < k:
                reservoir[j] = item
    return reservoir


@dataclass(frozen=True)
class ScaleParams:
    center: np.ndarray
    scale: np.ndarray


def zscore_fit(x: np.ndarray) -> ScaleParams:
    x = np.asarray(x, dtype=float)
    center = np.mean(x, axis=0)
    scale = np.std(x, axis=0, ddof=0)
    return ScaleParams(center, np.where(scale == 0, 1., scale))


def zscore_transform(x: np.ndarray, params: ScaleParams) -> np.ndarray:
    return (np.asarray(x, dtype=float) - params.center) / params.scale


def minmax_fit(x: np.ndarray) -> ScaleParams:
    x = np.asarray(x, dtype=float)
    lo = np.min(x, axis=0)
    delta = np.max(x, axis=0) - lo
    return ScaleParams(lo, np.where(delta == 0, 1., delta))


def robust_fit(x: np.ndarray) -> ScaleParams:
    x = np.asarray(x, dtype=float)
    med = np.median(x, axis=0)
    q25, q75 = np.quantile(x, [.25, .75], axis=0)
    iqr = q75 - q25
    return ScaleParams(med, np.where(iqr == 0, 1., iqr))


def equal_width_edges(x: np.ndarray, n_bins: int) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if n_bins <= 0 or len(x) == 0:
        raise ValueError("Nonempty data and positive n_bins required")
    lo, hi = float(np.min(x)), float(np.max(x))
    if lo == hi:
        return np.array([lo, np.nextafter(hi, np.inf)])
    return np.linspace(lo, hi, n_bins + 1)


def one_hot_categories(values: list[str] | np.ndarray, categories: list[str]) -> np.ndarray:
    """Stable schema: unknown categories map to all-zero, which must be documented."""
    return (np.asarray(values, dtype=object)[:, None] == np.asarray(categories)[None, :]).astype(int)


@dataclass(frozen=True)
class PCAParams:
    mean: np.ndarray
    components: np.ndarray  # components have shape (k,p)
    eigenvalues: np.ndarray


def pca_fit(x: np.ndarray, k: int) -> PCAParams:
    """PCA based on centered data and population covariance (1/n)."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or len(x) < 2 or not (1 <= k <= x.shape[1]):
        raise ValueError("X must have >= 2 rows and k within 1..p")
    mean = x.mean(axis=0)
    xc = x - mean
    cov = xc.T @ xc / len(x)
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals = np.maximum(vals[order], 0)
    vecs = vecs[:, order]
    return PCAParams(mean, vecs[:, :k].T, vals)


def pca_transform(x: np.ndarray, params: PCAParams) -> np.ndarray:
    return (np.asarray(x, dtype=float) - params.mean) @ params.components.T


def pca_inverse(z: np.ndarray, params: PCAParams) -> np.ndarray:
    return np.asarray(z, dtype=float) @ params.components + params.mean


def pca_variance_ratio(params: PCAParams) -> np.ndarray:
    total = params.eigenvalues.sum()
    return params.eigenvalues / total if total > 0 else np.zeros_like(params.eigenvalues)


def reconstruction_mse(x: np.ndarray, params: PCAParams) -> float:
    z = pca_transform(x, params)
    return float(np.mean((np.asarray(x, dtype=float) - pca_inverse(z, params)) ** 2))


def best_rank_k_svd(x: np.ndarray, k: int) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    if not 0 <= k <= min(x.shape):
        raise ValueError("k outside rank range")
    return (u[:, :k] * s[:k]) @ vt[:k, :]


def neighbor_overlap(x: np.ndarray, z: np.ndarray, neighbors: int = 5) -> float:
    """Average per-row Jaccard of k-NN sets, each computed excluding self."""
    x, z = np.asarray(x, float), np.asarray(z, float)
    if x.shape[0] != z.shape[0] or not (1 <= neighbors < len(x)):
        raise ValueError("invalid sample size or k")
    def sets(a):
        d = ((a[:, None, :] - a[None, :, :]) ** 2).sum(axis=2)
        np.fill_diagonal(d, np.inf)
        return [set(np.argsort(d[i])[:neighbors].tolist()) for i in range(len(a))]
    A, B = sets(x), sets(z)
    return float(np.mean([len(a & b) / len(a | b) for a, b in zip(A, B)]))


def build_demo(seed: int = RANDOM_SEED) -> dict:
    frame = generate_transactions(seed=seed)
    sample = srs_without_replacement(frame, 50, seed)
    features = frame[["spend", "units", "visits30", "discount_pct"]].to_numpy()
    split = 240
    train, test = features[:split], features[split:]
    scaler = zscore_fit(train)    # Fit only on training portion
    train_z = zscore_transform(train, scaler)
    test_z = zscore_transform(test, scaler)
    pca = pca_fit(train_z, 2)     # Fit only on training portion
    test_low = pca_transform(test_z, pca)
    return {"n_rows": len(frame), "n_days": len(aggregate_day(frame)),
            "sample_events": int(sample.rare_event.sum()),
            "population_events": int(frame.rare_event.sum()),
            "explained_variance": float(pca_variance_ratio(pca)[:2].sum()),
            "test_reconstruction_mse": reconstruction_mse(test_z, pca),
            "test_projection_shape": test_low.shape}


def main():
    import json
    print(json.dumps(build_demo(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
