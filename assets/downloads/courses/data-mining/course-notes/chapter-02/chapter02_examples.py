#!/usr/bin/env python3
"""Chapter 02 — reproducible synthetic data quality examples (Python stdlib only)."""
from __future__ import annotations
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median

HERE = Path(__file__).resolve().parent

def read_csv(name):
    with (HERE / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def quantile_tukey(values):
    """Tukey's median-of-halves hinges, for a small sorted sample."""
    v = sorted(values)
    n = len(v)
    return median(v[:n//2]), median(v), median(v[(n+1)//2:])

def measure_summary():
    xs = [float(r["reading"]) for r in read_csv("measurements_synthetic.csv")]
    q1, med, q3 = quantile_tukey(xs)
    iqr = q3 - q1
    return {"n": len(xs), "mean": mean(xs), "median": med, "q1": q1,
            "q3": q3, "iqr": iqr, "upper_fence": q3 + 1.5*iqr,
            "suspect": [x for x in xs if x > q3 + 1.5*iqr]}

def normalize_row(row):
    d = dict(row)
    d["customer_id"] = "" if d["customer_id"].strip() in ("?", "NA", "NULL") else d["customer_id"].strip()
    d["country"] = {"Iran": "IR", "IR": "IR"}.get(d["country"], d["country"])
    d["channel"] = d["channel"].strip().lower()
    return d

def quality_report(rows):
    normalized = [normalize_row(r) for r in rows]
    missing_customer = sum(not r["customer_id"] for r in normalized)
    keys = Counter((r["order_id"], r["line_no"]) for r in normalized)
    duplicated_key_groups = [k for k, count in keys.items() if count > 1]
    errors = []
    for row in normalized:
        qty, price = int(row["quantity"]), float(row["unit_price"])
        event = datetime.fromisoformat(row["event_time"])
        ingested = datetime.fromisoformat(row["ingest_time"])
        if price < 0: errors.append((row["order_id"], "negative_unit_price"))
        if qty == 0: errors.append((row["order_id"], "zero_quantity"))
        if qty < 0 and not row["order_id"].startswith("C"):
            errors.append((row["order_id"], "negative_qty_without_cancel"))
        if ingested < event: errors.append((row["order_id"], "ingest_before_event"))
        if row["channel"] not in {"web", "app"}: errors.append((row["order_id"], "invalid_channel"))
    return {"n_rows": len(rows), "missing_customer": missing_customer,
            "completeness_customer": (len(rows) - missing_customer)/len(rows),
            "distinct_orders": len({r["order_id"] for r in rows}),
            "duplicate_line_keys": duplicated_key_groups, "errors": errors,
            "normalized": normalized}

def baskets(rows):
    """Only clearly valid sales; key duplicates removed, returns excluded."""
    grouped = defaultdict(set)
    seen = set()
    for r in [normalize_row(q) for q in rows]:
        k = (r['order_id'], r['line_no'])
        if k in seen: continue
        seen.add(k)
        if r['order_id'].startswith('C'): continue
        if int(r['quantity']) <= 0 or float(r['unit_price']) < 0: continue
        grouped[r['order_id']].add(r['stock_code'])
    return dict(grouped)

def simpson():
    # success / total: A beats B in both strata, but loses in pooled data.
    strata = {'easy': {'A': (9,10), 'B': (72,90)},
              'hard': {'A': (18,90), 'B': (1,10)}}
    rates = {name: {g: good/total for g,(good,total) in groups.items()}
             for name,groups in strata.items()}
    pooled = {g: sum(s[g][0] for s in strata.values()) / sum(s[g][1] for s in strata.values())
              for g in ('A','B')}
    return rates, pooled

def missing_bias():
    full = [100,100,100,100,10,10,10,10]
    observed = [100,100,100,100,10]
    return mean(full), mean(observed)

def main():
    rows = read_csv('retail_lines_synthetic.csv')
    r = quality_report(rows)
    print('--- quality audit (synthetic records) ---')
    print('line count:', r['n_rows'])
    print('distinct order IDs:', r['distinct_orders'])
    print('customer ID missing:', r['missing_customer'])
    print('customer ID completeness:', f"{100*r['completeness_customer']:.2f}%")
    print('duplicate line keys:', r['duplicate_line_keys'])
    print('rule violations:', r['errors'])
    print('valid-sales baskets:', baskets(rows))
    print('--- robust measurement profile ---')
    print(measure_summary())
    rates, pooled = simpson()
    print('--- Simpson composition example ---')
    print('stratified rates:',rates,'pooled:',pooled)
    print('--- informative missingness bias ---')
    print('full mean / observed mean:',missing_bias())

if __name__ == '__main__':
    main()
