"""
Reproduce the numerical experiments for
"On the Geometry of Capability-Aware Imbalance in Composite Decision Systems."

Run from the Tex directory:
    python run_experiments.py

Outputs:
    results.json
    experiments_figure.pdf
    experiments_tables.tex
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, linprog, linear_sum_assignment, minimize


SEED = 20260624
rng = np.random.default_rng(SEED)


def e1_fundamental_theorem() -> list[dict[str, float]]:
    """Discrete Kantorovich problem for increasingly skewed task measures."""
    m = 8
    capabilities = np.linspace(1, m, m)
    difficulties = capabilities.copy()
    nu = np.ones(m) / m
    cost = (difficulties[:, None] - capabilities[None, :]) ** 2

    a_eq: list[np.ndarray] = []
    for k in range(m):
        row = np.zeros(m * m)
        row[k * m : (k + 1) * m] = 1.0
        a_eq.append(row)
    for i in range(m):
        row = np.zeros(m * m)
        row[i::m] = 1.0
        a_eq.append(row)
    a_eq_arr = np.vstack(a_eq)

    rows = []
    for s in [0.0, 0.5, 1.0, 1.5, 2.0]:
        ranks = np.arange(1, m + 1, dtype=float)
        weights = ranks ** (-s)
        mu = weights / weights.sum()
        b_eq = np.concatenate([mu, nu])
        res = linprog(cost.ravel(), A_eq=a_eq_arr, b_eq=b_eq, bounds=(0, None), method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        gamma_unif = mu[:, None] * nu[None, :]
        j_star = float(res.fun)
        j_unif = float(np.sum(gamma_unif * cost))
        rows.append(
            {
                "s": s,
                "J_star": j_star,
                "J_unif": j_unif,
                "gap": j_unif - j_star,
                "relative_gap": (j_unif - j_star) / j_unif,
            }
        )
    return rows


def e2_harmonic_bound() -> dict[str, object]:
    m = 6
    complexities = np.sort(rng.uniform(1.0, 20.0, size=m))
    p_opt = (1.0 / complexities) / np.sum(1.0 / complexities)
    c_eff_opt = float(np.sum(p_opt * complexities))
    c_eff_unif = float(np.mean(complexities))
    return {
        "C": complexities.tolist(),
        "p_opt": p_opt.tolist(),
        "min_C": float(np.min(complexities)),
        "Ceff_opt": c_eff_opt,
        "Ceff_unif": c_eff_unif,
        "max_C": float(np.max(complexities)),
        "bound_holds": bool(np.min(complexities) <= c_eff_opt <= c_eff_unif <= np.max(complexities)),
    }


def e3_attenuation() -> dict[str, object]:
    cr, ce = 1.0, 1000.0
    p_e = np.array([0.5, 0.2, 0.1, 0.05, 0.01, 0.001, 0.0001])
    c_eff = (1.0 - p_e) * cr + p_e * ce
    return {"Cr": cr, "Ce": ce, "p_e": p_e.tolist(), "Ceff": c_eff.tolist()}


def solve_distributed(mu_rates: np.ndarray, total_load: float) -> tuple[float, np.ndarray]:
    """Solve min sum_i L_i/(mu_i-L_i) subject to sum_i L_i=Lambda."""

    def excess(lam: float) -> float:
        loads = np.maximum(mu_rates - np.sqrt(mu_rates / lam), 0.0)
        return float(np.sum(loads) - total_load)

    lo, hi = 1.0e-12, 1.0
    while excess(hi) < 0.0:
        hi *= 4.0
    lam_star = brentq(excess, lo, hi, xtol=1.0e-13, rtol=1.0e-13, maxiter=500)
    loads = np.maximum(mu_rates - np.sqrt(mu_rates / lam_star), 0.0)
    return float(lam_star), loads


def e4_distributed_load() -> dict[str, object]:
    n = 5
    mu_rates = np.array([2.0, 3.0, 5.0, 7.0, 10.0])

    def aggregate_cost(loads: np.ndarray) -> float:
        return float(np.sum(loads / (mu_rates - loads)))

    trials = []
    for total_load in [1.0, 3.0, 5.0, 7.0, 9.0]:
        lam_star, loads = solve_distributed(mu_rates, total_load)
        uniform_loads = np.full(n, total_load / n)
        service_prop_loads = total_load * mu_rates / np.sum(mu_rates)
        j_star = aggregate_cost(loads)
        j_unif = aggregate_cost(uniform_loads)
        j_service_prop = aggregate_cost(service_prop_loads)
        mean_star = j_star / total_load
        mean_unif = j_unif / total_load
        mean_service_prop = j_service_prop / total_load

        def objective(x: np.ndarray) -> float:
            return aggregate_cost(x)

        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - total_load}
        bounds = [(0.0, rate - 1.0e-9) for rate in mu_rates]
        best = None
        for scale in np.linspace(0.85, 1.15, 8):
            x0 = np.clip(loads * scale + 1.0e-6, 1.0e-9, mu_rates - 1.0e-9)
            x0 *= total_load / np.sum(x0)
            res = minimize(
                objective,
                x0=x0,
                method="SLSQP",
                bounds=bounds,
                constraints=[constraints],
                options={"ftol": 1.0e-14, "maxiter": 20000},
            )
            if best is None or res.fun < best.fun:
                best = res
        assert best is not None
        active = loads > 1.0e-8
        marginal = mu_rates / (mu_rates - loads) ** 2
        trials.append(
            {
                "Lambda": total_load,
                "lambda_star": lam_star,
                "loads": loads.tolist(),
                "numeric_loads": best.x.tolist(),
                "formula_matches_numeric": bool(np.allclose(loads, best.x, atol=2.5e-4)),
                "sojourn_terms": (loads / (mu_rates - loads)).tolist(),
                "marginal_costs": marginal.tolist(),
                "active_marginal_mean": float(np.mean(marginal[active])),
                "J_unif": j_unif,
                "J_service_prop": j_service_prop,
                "J_star": j_star,
                "mean_unif": mean_unif,
                "mean_service_prop": mean_service_prop,
                "mean_star": mean_star,
            }
        )

    light = []
    for total_load in [0.05, 0.10, 0.20, 0.40]:
        _, loads = solve_distributed(mu_rates, total_load)
        uniform_loads = np.full(n, total_load / n)
        gap = aggregate_cost(uniform_loads) - aggregate_cost(loads)
        leading = total_load * (np.mean(1.0 / mu_rates) - 1.0 / np.max(mu_rates))
        light.append(
            {
                "Lambda": total_load,
                "gap_numeric": gap,
                "gap_leading_order": float(leading),
                "ratio": gap / leading,
            }
        )
    return {"mu_rates": mu_rates.tolist(), "trials": trials, "light_traffic_check": light}


def _best_stump(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> dict[str, float]:
    n, d = x.shape
    best: dict[str, float] = {"err": np.inf, "feature": 0, "threshold": 0.0, "polarity": 1}
    for feature in range(d):
        order = np.argsort(x[:, feature])
        xs = x[order, feature]
        thresholds = (xs[:-1] + xs[1:]) / 2.0
        stride = max(1, len(thresholds) // 80)
        for threshold in thresholds[::stride]:
            for polarity in (1, -1):
                pred = np.where(x[:, feature] >= threshold, polarity, -polarity)
                err = float(np.sum(weights[pred != y]))
                if err < best["err"]:
                    best = {
                        "err": err,
                        "feature": float(feature),
                        "threshold": float(threshold),
                        "polarity": float(polarity),
                    }
    return best


def e5_dynamic_imbalance() -> dict[str, object]:
    n_samples, n_stages, n_features = 600, 10, 4
    x = rng.normal(size=(n_samples, n_features))
    true_w = rng.normal(size=n_features)
    margin = x @ true_w + 0.55 * rng.normal(size=n_samples)
    y = np.where(margin >= 0.0, 1, -1)
    difficulty = -np.abs(x @ true_w)
    hard_idx = np.argsort(difficulty)[-int(0.1 * n_samples) :]

    weights = np.ones(n_samples) / n_samples
    uniform = np.ones(n_samples) / n_samples
    components = np.linspace(0.5, 6.0, 6)
    bins = np.quantile(difficulty, np.linspace(0.0, 1.0, len(components) + 1))
    bin_idx = np.clip(np.digitize(difficulty, bins[1:-1]), 0, len(components) - 1)

    imbalance, hard_mass, effective_complexity, edges = [], [], [], []
    for _ in range(n_stages):
        stump = _best_stump(x, y, weights)
        pred = np.where(
            x[:, int(stump["feature"])] >= stump["threshold"],
            int(stump["polarity"]),
            -int(stump["polarity"]),
        )
        err_indicator = (pred != y).astype(float)
        err = float(np.clip(np.sum(weights * err_indicator), 1.0e-6, 0.5 - 1.0e-6))
        alpha = 0.5 * np.log((1.0 - err) / err)
        weights *= np.exp(alpha * (2.0 * err_indicator - 1.0))
        weights /= np.sum(weights)
        p_t = np.array([np.sum(weights[bin_idx == i]) for i in range(len(components))])
        p_t /= np.sum(p_t)
        edges.append(0.5 - err)
        imbalance.append(float(np.sum(weights * np.log((weights + 1.0e-300) / uniform))))
        hard_mass.append(float(np.sum(weights[hard_idx])))
        effective_complexity.append(float(np.sum(p_t * components)))

    stages = np.arange(1, n_stages + 1, dtype=float)
    slopes = {
        "imbalance": float(np.polyfit(stages, imbalance, 1)[0]),
        "hard_mass": float(np.polyfit(stages, hard_mass, 1)[0]),
        "effective_complexity": float(np.polyfit(stages, effective_complexity, 1)[0]),
    }
    return {
        "edges": edges,
        "imbalance_index": imbalance,
        "residual_concentration": hard_mass,
        "effective_complexity": effective_complexity,
        "slopes": slopes,
    }


def e6_hierarchical_screening() -> dict[str, object]:
    """Check when a cheap screening stage beats a flat rare-specialist plan."""
    c_r, c_e, c_screen = 1.0, 50.0, 0.2
    p_e_values = np.array([0.50, 0.20, 0.10, 0.05, 0.01])
    rows = []
    for p_e in p_e_values:
        flat = (1.0 - p_e) * c_r + p_e * c_e
        hierarchical = c_screen + p_e * c_e
        rows.append(
            {
                "p_e": float(p_e),
                "flat_cost": float(flat),
                "hierarchical_cost": float(hierarchical),
                "improvement": float(flat - hierarchical),
            }
        )
    return {"C_r": c_r, "C_e": c_e, "C_screen": c_screen, "rows": rows}


def e7_empirical_transport_convergence() -> dict[str, object]:
    """Monte Carlo check of convergence of empirical capability-proportional plans."""
    true_c = np.array([2.0, 4.0, 8.0, 16.0])
    p_star = (1.0 / true_c) / np.sum(1.0 / true_c)
    sample_sizes = np.array([50, 100, 200, 500, 1000, 2000])
    repetitions = 300
    rows = []
    for n in sample_sizes:
        errors = []
        costs = []
        for _ in range(repetitions):
            c_hat = np.maximum(true_c + rng.normal(scale=1.2 / np.sqrt(n), size=true_c.size), 1.0e-6)
            p_hat = (1.0 / c_hat) / np.sum(1.0 / c_hat)
            errors.append(np.sum(np.abs(p_hat - p_star)))
            costs.append(np.sum(p_hat * true_c))
        rows.append(
            {
                "n": int(n),
                "mean_l1_error": float(np.mean(errors)),
                "sd_l1_error": float(np.std(errors, ddof=1)),
                "mean_cost": float(np.mean(costs)),
            }
        )
    return {
        "true_complexities": true_c.tolist(),
        "p_star": p_star.tolist(),
        "Ceff_star": float(np.sum(p_star * true_c)),
        "rows": rows,
    }


def _squared_distances(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    diff = x[:, None, :] - y[None, :, :]
    return np.sum(diff * diff, axis=2)


def _uniform_ot_cost(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    n, m = x.shape[0], y.shape[0]
    cost = _squared_distances(x, y)
    a_eq = []
    for i in range(n):
        row = np.zeros(n * m)
        row[i * m : (i + 1) * m] = 1.0
        a_eq.append(row)
    for j in range(m):
        row = np.zeros(n * m)
        row[j::m] = 1.0
        a_eq.append(row)
    b_eq = np.concatenate([np.ones(n) / n, np.ones(m) / m])
    res = linprog(cost.ravel(), A_eq=np.vstack(a_eq), b_eq=b_eq, bounds=(0, None), method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    gamma = res.x.reshape(n, m)
    product = np.ones((n, m)) / (n * m)
    j_star = float(np.sum(gamma * cost))
    j_ind = float(np.sum(product * cost))
    concentration = float((n * m) * np.sum(gamma * gamma))
    return {
        "W2_squared": j_star,
        "independent_cost": j_ind,
        "gap": j_ind - j_star,
        "relative_gap": (j_ind - j_star) / j_ind,
        "plan_concentration": concentration,
    }


def _sinkhorn_cost_uniform(cost: np.ndarray, epsilon: float = 0.08, n_iter: int = 800) -> float:
    n, m = cost.shape
    a = np.ones(n) / n
    b = np.ones(m) / m
    scale = max(float(np.median(cost)), 1.0e-12)
    kernel = np.exp(-cost / (epsilon * scale)) + 1.0e-300
    u = np.ones(n)
    v = np.ones(m)
    for _ in range(n_iter):
        u = a / (kernel @ v + 1.0e-300)
        v = b / (kernel.T @ u + 1.0e-300)
    gamma = (u[:, None] * kernel) * v[None, :]
    return float(np.sum(gamma * cost))


def _nearest_independent_cost(cost: np.ndarray) -> float:
    return float(np.mean(np.min(cost, axis=1)))


def _assignment_cost_uniform(cost: np.ndarray) -> float:
    rows, cols = linear_sum_assignment(cost)
    return float(np.mean(cost[rows, cols]))


def _two_moons(n: int, noise: float) -> np.ndarray:
    half = n // 2
    theta = np.linspace(0.0, np.pi, half, endpoint=False)
    moon_a = np.column_stack([np.cos(theta), np.sin(theta)])
    moon_b = np.column_stack([1.0 - np.cos(theta), 0.45 - np.sin(theta)])
    points = np.vstack([moon_a, moon_b])
    points += noise * rng.normal(size=points.shape)
    return points


def _gaussian_mixture(n: int) -> np.ndarray:
    centers = np.array([[-1.7, -1.0], [1.5, -0.8], [0.1, 1.6]])
    counts = np.array([n // 3, n // 3, n - 2 * (n // 3)])
    parts = [center + 0.22 * rng.normal(size=(count, 2)) for center, count in zip(centers, counts)]
    return np.vstack(parts)


def _checkerboard(n: int) -> np.ndarray:
    side = int(np.sqrt(n))
    grid = np.linspace(-1.0, 1.0, side)
    cells = []
    for i, gx in enumerate(grid):
        for j, gy in enumerate(grid):
            if (i + j) % 2 == 0:
                cells.append([gx, gy])
    points = np.array(cells[:n], dtype=float)
    if len(points) < n:
        repeats = n - len(points)
        points = np.vstack([points, points[:repeats]])
    points += 0.035 * rng.normal(size=points.shape)
    return points[:n]


def e8_geometry_benchmarks() -> dict[str, object]:
    """Toy OT geometry benchmarks common in theoretical ML papers."""
    n = 48
    datasets = {}
    source = _two_moons(n, noise=0.035)
    target = _two_moons(n, noise=0.035) @ np.array([[0.97, -0.18], [0.18, 0.97]]).T + np.array([0.25, -0.10])
    datasets["two_moons"] = (source, target)

    source = _gaussian_mixture(n)
    target = source @ np.array([[0.86, -0.32], [0.32, 0.86]]).T + np.array([0.35, 0.20])
    target += 0.12 * rng.normal(size=target.shape)
    datasets["gaussian_mixture"] = (source, target)

    source = _checkerboard(n)
    target = source + np.array([0.18, -0.12])
    target[:, 0] += 0.10 * np.sin(3.0 * source[:, 1])
    target[:, 1] += 0.10 * np.cos(3.0 * source[:, 0])
    datasets["checkerboard"] = (source, target)

    rows = []
    for name, (source_points, target_points) in datasets.items():
        cost = _squared_distances(source_points, target_points)
        metrics = _uniform_ot_cost(source_points, target_points)
        metrics["nearest_cost"] = _nearest_independent_cost(cost)
        metrics["sinkhorn_cost"] = _sinkhorn_cost_uniform(cost)
        metrics["hungarian_cost"] = _assignment_cost_uniform(cost)
        rows.append({"dataset": name, **metrics})
    return {"n_per_measure": n, "rows": rows}


def _downsample_average(image: np.ndarray, target_side: int) -> np.ndarray:
    h, w = image.shape
    if h == target_side and w == target_side:
        return image.astype(float)
    block_h = h // target_side
    block_w = w // target_side
    trimmed = image[: target_side * block_h, : target_side * block_w]
    return trimmed.reshape(target_side, block_h, target_side, block_w).mean(axis=(1, 3))


def _normalize_histogram(image: np.ndarray) -> np.ndarray:
    hist = np.maximum(image.astype(float), 0.0).ravel()
    hist += 1.0e-9
    return hist / hist.sum()


def _histogram_ot_cost(p: np.ndarray, q: np.ndarray, cost: np.ndarray) -> dict[str, float]:
    n = len(p)
    a_eq = []
    for i in range(n):
        row = np.zeros(n * n)
        row[i * n : (i + 1) * n] = 1.0
        a_eq.append(row)
    for j in range(n):
        row = np.zeros(n * n)
        row[j::n] = 1.0
        a_eq.append(row)
    res = linprog(cost.ravel(), A_eq=np.vstack(a_eq), b_eq=np.concatenate([p, q]), bounds=(0, None), method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    independent = np.outer(p, q)
    sinkhorn = _sinkhorn_cost_histogram(p, q, cost)
    return {
        "W2_squared": float(res.fun),
        "independent_cost": float(np.sum(independent * cost)),
        "sinkhorn_cost": sinkhorn,
    }


def _sinkhorn_cost_histogram(p: np.ndarray, q: np.ndarray, cost: np.ndarray, epsilon: float = 0.06, n_iter: int = 1200) -> float:
    scale = max(float(np.median(cost)), 1.0e-12)
    kernel = np.exp(-cost / (epsilon * scale)) + 1.0e-300
    u = np.ones_like(p)
    v = np.ones_like(q)
    for _ in range(n_iter):
        u = p / (kernel @ v + 1.0e-300)
        v = q / (kernel.T @ u + 1.0e-300)
    gamma = (u[:, None] * kernel) * v[None, :]
    return float(np.sum(gamma * cost))


def _load_mnist_digit_means(target_side: int = 7) -> tuple[str, dict[int, np.ndarray]]:
    try:
        from torchvision.datasets import MNIST

        data = MNIST(root=str(Path(__file__).resolve().parent / "data"), train=True, download=True)
        images_by_digit: dict[int, list[np.ndarray]] = {digit: [] for digit in range(10)}
        for image, label in data:
            digit = int(label)
            if len(images_by_digit[digit]) < 40:
                images_by_digit[digit].append(_downsample_average(np.asarray(image), target_side))
            if all(len(v) >= 40 for v in images_by_digit.values()):
                break
        return "MNIST", {digit: np.mean(images, axis=0) for digit, images in images_by_digit.items()}
    except Exception:
        from sklearn.datasets import load_digits

        digits = load_digits()
        images_by_digit = {digit: [] for digit in range(10)}
        for image, label in zip(digits.images, digits.target):
            digit = int(label)
            if len(images_by_digit[digit]) < 40:
                images_by_digit[digit].append(_downsample_average(image, 8))
        return "sklearn digits fallback", {digit: np.mean(images, axis=0) for digit, images in images_by_digit.items()}


def e9_mnist_as_distributions() -> dict[str, object]:
    """Treat average digit images as probability measures over pixel locations."""
    dataset_name, digit_means = _load_mnist_digit_means()
    side = next(iter(digit_means.values())).shape[0]
    grid = np.array([(i / (side - 1), j / (side - 1)) for i in range(side) for j in range(side)], dtype=float)
    cost = _squared_distances(grid, grid)
    pairs = [(0, 1), (3, 8), (4, 9), (1, 7)]
    rows = []
    for a, b in pairs:
        p = _normalize_histogram(digit_means[a])
        q = _normalize_histogram(digit_means[b])
        metrics = _histogram_ot_cost(p, q, cost)
        metrics["gap_vs_independent"] = metrics["independent_cost"] - metrics["W2_squared"]
        rows.append({"pair": f"{a}-{b}", **metrics})
    return {"dataset": dataset_name, "grid_side": side, "rows": rows}


def e10_baseline_comparison(e2: dict[str, object], e4: dict[str, object], e8: dict[str, object]) -> dict[str, object]:
    """Compact comparison against natural non-OT baselines."""
    geometry_rows = []
    for row in e8["rows"]:
        geometry_rows.append(
            {
                "dataset": row["dataset"],
                "independent": row["independent_cost"],
                "nearest": row["nearest_cost"],
                "sinkhorn": row["sinkhorn_cost"],
                "optimal": row["W2_squared"],
            }
        )

    load_row = next(row for row in e4["trials"] if row["Lambda"] == 7.0)
    return {
        "geometry": geometry_rows,
        "distributed_lambda7": {
            "equal_load": load_row["mean_unif"],
            "service_proportional": load_row["mean_service_prop"],
            "optimal": load_row["mean_star"],
        },
        "composite": {
            "uniform": e2["Ceff_unif"],
            "capability_proportional": e2["Ceff_opt"],
            "best_single_component": e2["min_C"],
        },
    }


def make_figure(results: dict[str, object], path: Path) -> None:
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(2, 2, figsize=(9.2, 6.8))

    e1 = results["E1_fundamental_theorem"]
    s = [row["s"] for row in e1]
    axs[0, 0].plot(s, [row["J_star"] for row in e1], marker="o", label=r"$J^\star$")
    axs[0, 0].plot(s, [row["J_unif"] for row in e1], marker="s", label=r"$J_{\rm unif}$")
    axs[0, 0].set_xlabel("skew s")
    axs[0, 0].set_ylabel("transport cost")
    axs[0, 0].set_title("E1: optimal vs. uniform")
    axs[0, 0].legend(frameon=False)

    e3 = results["E3_attenuation"]
    axs[0, 1].semilogx(e3["p_e"], e3["Ceff"], marker="o")
    axs[0, 1].invert_xaxis()
    axs[0, 1].set_xlabel(r"rare probability $p_e$")
    axs[0, 1].set_ylabel(r"$C_{\rm eff}$")
    axs[0, 1].set_title("E3: attenuation")

    e4 = results["E4_distributed_load"]["trials"]
    axs[1, 0].plot([row["Lambda"] for row in e4], [row["mean_star"] for row in e4], marker="o", label="optimal")
    axs[1, 0].plot([row["Lambda"] for row in e4], [row["mean_unif"] for row in e4], marker="s", label="uniform")
    axs[1, 0].set_xlabel(r"arrival rate $\Lambda$")
    axs[1, 0].set_ylabel("mean sojourn cost")
    axs[1, 0].set_title("E4: distributed load")
    axs[1, 0].legend(frameon=False)

    e5 = results["E5_dynamic_imbalance"]
    stages = np.arange(1, len(e5["imbalance_index"]) + 1)
    axs[1, 1].plot(stages, e5["imbalance_index"], marker="o", label="KL imbalance")
    axs[1, 1].plot(stages, e5["effective_complexity"], marker="s", label=r"$C_{\rm eff}$")
    axs[1, 1].set_xlabel("boosting stage")
    axs[1, 1].set_title("E5: dynamic imbalance")
    axs[1, 1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def format_tables(results: dict[str, object]) -> str:
    lines = []
    lines.append("% Auto-generated by run_experiments.py")
    lines.append("% E1 rows")
    for row in results["E1_fundamental_theorem"]:
        lines.append(
            f"{row['s']:.1f} & {row['J_star']:.3f} & {row['J_unif']:.3f} & "
            f"{row['gap']:.3f} & {100.0 * row['relative_gap']:.1f}\\% \\\\"
        )
    e2 = results["E2_harmonic_bound"]
    lines.append("% E2 values")
    for label, key in [
        (r"$\\min_i C_i$", "min_C"),
        (r"$C_\\eff^\\star$ (harmonic mean)", "Ceff_opt"),
        (r"$C_\\eff^{\\unif}$ (arithmetic mean)", "Ceff_unif"),
        (r"$\\max_i C_i$", "max_C"),
    ]:
        lines.append(f"{label} & {e2[key]:.3f} \\\\")
    e4 = results["E4_distributed_load"]
    lines.append("% E4 rows")
    for row in e4["trials"]:
        active_marg = [m for load, m in zip(row["loads"], row["marginal_costs"]) if load > 1.0e-8]
        lines.append(
            f"{row['Lambda']:.0f} & {'yes' if row['formula_matches_numeric'] else 'no'} & "
            f"{row['mean_unif']:.3f} & {row['mean_star']:.3f} & "
            f"{np.mean(active_marg):.3f} \\\\"
        )
    lines.append("% E4 light-traffic rows")
    for row in e4["light_traffic_check"]:
        lines.append(
            f"{row['Lambda']:.2f} & {row['gap_numeric']:.6f} & "
            f"{row['gap_leading_order']:.6f} & {row['ratio']:.3f} \\\\"
        )
    e5 = results["E5_dynamic_imbalance"]
    lines.append("% E5 rows")
    lines.append(
        f"Imbalance index $\\mathcal I^{{(t)}}$ & {e5['imbalance_index'][0]:.3f} & "
        f"{e5['imbalance_index'][-1]:.3f} & {e5['slopes']['imbalance']:+.3f} \\\\"
    )
    lines.append(
        f"Residual mass on hardest 10\\% & {e5['residual_concentration'][0]:.3f} & "
        f"{e5['residual_concentration'][-1]:.3f} & {e5['slopes']['hard_mass']:+.3f} \\\\"
    )
    lines.append(
        f"Hierarchical $C_\\eff^{{(t)}}$ & {e5['effective_complexity'][0]:.3f} & "
        f"{e5['effective_complexity'][-1]:.3f} & {e5['slopes']['effective_complexity']:+.3f} \\\\"
    )
    e6 = results["E6_hierarchical_screening"]
    lines.append("% E6 rows")
    for row in e6["rows"]:
        lines.append(
            f"{row['p_e']:.2f} & {row['flat_cost']:.3f} & "
            f"{row['hierarchical_cost']:.3f} & {row['improvement']:.3f} \\\\"
        )
    e7 = results["E7_empirical_transport_convergence"]
    lines.append("% E7 rows")
    for row in e7["rows"]:
        lines.append(
            f"{row['n']} & {row['mean_l1_error']:.4f} & "
            f"{row['sd_l1_error']:.4f} & {row['mean_cost']:.4f} \\\\"
        )
    e8 = results["E8_geometry_benchmarks"]
    lines.append("% E8 rows")
    for row in e8["rows"]:
        label = row["dataset"].replace("_", " ")
        lines.append(
            f"{label} & {row['W2_squared']:.4f} & {row['sinkhorn_cost']:.4f} & "
            f"{row['independent_cost']:.4f} & {row['relative_gap'] * 100.0:.1f}\\% & "
            f"{row['plan_concentration']:.1f} \\\\"
        )
    e9 = results["E9_mnist_as_distributions"]
    lines.append("% E9 rows")
    for row in e9["rows"]:
        lines.append(
            f"{row['pair']} & {row['W2_squared']:.5f} & {row['sinkhorn_cost']:.5f} & "
            f"{row['independent_cost']:.5f} & {row['gap_vs_independent']:.5f} \\\\"
        )
    e10 = results["E10_baseline_comparison"]
    lines.append("% E10 geometry baseline rows")
    for row in e10["geometry"]:
        label = row["dataset"].replace("_", " ")
        lines.append(
            f"{label} & {row['independent']:.4f} & {row['nearest']:.4f} & "
            f"{row['sinkhorn']:.4f} & {row['optimal']:.4f} \\\\"
        )
    lines.append("% E10 distributed baseline row")
    row = e10["distributed_lambda7"]
    lines.append(
        f"distributed load ($\\Lambda=7$) & {row['equal_load']:.4f} & "
        f"{row['service_proportional']:.4f} & {row['optimal']:.4f} \\\\"
    )
    lines.append("% E10 composite baseline row")
    row = e10["composite"]
    lines.append(
        f"composite complexity & {row['uniform']:.4f} & "
        f"{row['capability_proportional']:.4f} & {row['best_single_component']:.4f} \\\\"
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    e1 = e1_fundamental_theorem()
    e2 = e2_harmonic_bound()
    e3 = e3_attenuation()
    e4 = e4_distributed_load()
    e5 = e5_dynamic_imbalance()
    e6 = e6_hierarchical_screening()
    e7 = e7_empirical_transport_convergence()
    e8 = e8_geometry_benchmarks()
    e9 = e9_mnist_as_distributions()
    results = {
        "seed": SEED,
        "E1_fundamental_theorem": e1,
        "E2_harmonic_bound": e2,
        "E3_attenuation": e3,
        "E4_distributed_load": e4,
        "E5_dynamic_imbalance": e5,
        "E6_hierarchical_screening": e6,
        "E7_empirical_transport_convergence": e7,
        "E8_geometry_benchmarks": e8,
        "E9_mnist_as_distributions": e9,
        "E10_baseline_comparison": e10_baseline_comparison(e2, e4, e8),
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (out_dir / "experiments_tables.tex").write_text(format_tables(results), encoding="utf-8")
    make_figure(results, out_dir / "experiments_figure.pdf")


if __name__ == "__main__":
    main()
