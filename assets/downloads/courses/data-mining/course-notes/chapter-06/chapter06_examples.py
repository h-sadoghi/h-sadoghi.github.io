"""Chapter 06: deterministic, standard-library sequence & graph mining demonstrations.

All inputs are synthetic. This is educational code, not a scalable gSpan implementation.
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent


def load_sequences(path: Path = HERE / "sequence_events_synthetic.csv") -> dict[str, tuple[tuple[int, frozenset[str]], ...]]:
    grouped: dict[str, list[tuple[int, int, frozenset[str]]]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            cid = row["customer_id"].strip()
            eid, day = int(row["event_id"]), int(row["day"])
            items = frozenset(x.strip() for x in row["items"].split("|") if x.strip())
            if not cid or not items or eid <= 0:
                raise ValueError("invalid event")
            grouped[cid].append((eid, day, items))
    result = {}
    for cid, rows in sorted(grouped.items()):
        ordered = sorted(rows)
        if len({x[0] for x in ordered}) != len(ordered):
            raise ValueError("duplicate event_id within one customer")
        if any(b[1] < a[1] for a, b in zip(ordered, ordered[1:])):
            raise ValueError("non-chronological day values")
        result[cid] = tuple((day, items) for _, day, items in ordered)
    return result


def _normal_pattern(pattern: Iterable[Iterable[str]]) -> tuple[frozenset[str], ...]:
    result = tuple(frozenset(x) for x in pattern)
    if not result or any(not x for x in result):
        raise ValueError("pattern must have nonempty ordered events")
    return result


def subsequence_match(
    events: tuple[tuple[int, frozenset[str]], ...],
    pattern: Iterable[Iterable[str]],
    *,
    max_gap: int | None = None,
    max_span_days: int | None = None,
) -> bool:
    """Events are strictly ordered; gap counts *intervening events*, not days.

    An event itemset must be contained in ONE event. A customer contributes once.
    Unlike naive greedy matching, backtracking handles constraints correctly.
    """
    p = _normal_pattern(pattern)
    if max_gap is not None and max_gap < 0:
        raise ValueError("max_gap must be nonnegative")
    if max_span_days is not None and max_span_days < 0:
        raise ValueError("max_span_days must be nonnegative")

    def search(k: int, prev: int, start_day: int | None) -> bool:
        if k == len(p):
            return True
        for j in range(prev + 1, len(events)):
            if prev >= 0 and max_gap is not None and j - prev - 1 > max_gap:
                break
            day, items = events[j]
            if start_day is not None and max_span_days is not None and day - start_day > max_span_days:
                break
            if p[k].issubset(items) and search(k + 1, j, day if start_day is None else start_day):
                return True
        return False

    return search(0, -1, None)


def seq_support(sequences, pattern, **kwargs) -> tuple[int, list[str]]:
    p = _normal_pattern(pattern)
    ids = [cid for cid, ev in sequences.items() if subsequence_match(ev, p, **kwargs)]
    return len(ids), ids


def basket_support(sequences, itemset: Iterable[str]) -> tuple[int, list[str]]:
    """Ignores time, but counts each customer once."""
    q = frozenset(itemset)
    ids = [cid for cid, ev in sequences.items() if q.issubset(frozenset().union(*(x[1] for x in ev)))]
    return len(ids), ids


def prefixspan_singletons(sequences, min_count: int = 3, max_len: int = 3):
    """Prefix projection for patterns of one item per ordered event.

    When event itemsets contain multiple items, it explores only S-extensions
    (later events), not I-extensions (same event). It is intentionally restricted.
    """
    if min_count < 1 or max_len < 1:
        raise ValueError("positive thresholds required")
    projected = [(cid, tuple(items for _, items in events)) for cid, events in sequences.items()]
    found: dict[tuple[str, ...], int] = {}

    def visit(prefix, suffixes):
        if len(prefix) >= max_len:
            return
        counts = Counter()
        for _, suffix in suffixes:
            seen = set().union(*suffix) if suffix else set()
            counts.update(seen)
        for symbol in sorted(x for x, n in counts.items() if n >= min_count):
            extended = prefix + (symbol,)
            found[extended] = counts[symbol]
            next_db = []
            for cid, suffix in suffixes:
                for index, event in enumerate(suffix):
                    if symbol in event:
                        next_db.append((cid, suffix[index+1:]))
                        break
            visit(extended, next_db)

    visit((), projected)
    return found


def exhaustive_singletons(sequences, min_count: int = 3, max_len: int = 3):
    symbols = sorted({item for ev in sequences.values() for _, items in ev for item in items})
    ans = {}
    for k in range(1, max_len + 1):
        for word in itertools.product(symbols, repeat=k):
            count, _ = seq_support(sequences, [{ch} for ch in word])
            if count >= min_count:
                ans[word] = count
    return ans


def taxonomy_projection(sequences, taxonomy):
    result = {}
    for cid, ev in sequences.items():
        result[cid] = tuple((day, frozenset(taxonomy.get(x,x) for x in items)) for day,items in ev)
    return result


def load_graphs(path: Path = HERE / "graphs_synthetic.json"):
    objects = json.loads(path.read_text(encoding="utf-8"))
    graphs = objects["graphs"]
    for graph in graphs:
        if len(set(graph["nodes"])) != len(graph["nodes"]):
            raise ValueError("duplicate vertices")
        if any(u not in graph["nodes"] or v not in graph["nodes"] or u == v for u,v in graph["edges"]):
            raise ValueError("invalid graph edge")
    return graphs


def graph_has_subgraph(host, pattern) -> bool:
    """Exact non-induced labeled subgraph matching for SMALL undirected graphs.

    Vertex IDs are local; labels must match. Extra host edges are permitted.
    Computationally exponential in general; never apply to large graphs.
    """
    hnodes, pnodes = host["nodes"], pattern["nodes"]
    if len(pnodes)>len(hnodes) or len(pattern["edges"])>len(host["edges"]):
        return False
    hedges = {frozenset(e) for e in host["edges"]}
    mapping = {}
    pids = sorted(pnodes, key=lambda u: (sum(u in e for e in pattern["edges"])*-1,u))

    def dfs(depth, occupied):
        if depth == len(pids):
            return True
        p = pids[depth]
        for h in hnodes:
            if h in occupied or hnodes[h] != pnodes[p]:
                continue
            if any(p in e and other in mapping and frozenset((h,mapping[other])) not in hedges
                   for e in pattern["edges"] for other in e if other != p):
                continue
            mapping[p] = h
            if dfs(depth+1, occupied | {h}):
                return True
            del mapping[p]
        return False
    return dfs(0, set())


def graph_support(graphs, pattern):
    ids = [g["id"] for g in graphs if graph_has_subgraph(g, pattern)]
    return len(ids), ids


def fisher_enrichment_upper(n, both, a, b):
    """Hypergeometric P(X >= both | fixed margins), not a multiple-test correction."""
    if not (0 <= both <= min(a,b) <= n) or both < max(0,a+b-n):
        raise ValueError("invalid 2x2 table margins")
    den = math.comb(n,b)
    return sum(math.comb(a,k)*math.comb(n-a,b-k)
               for k in range(both,min(a,b)+1)) / den


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-count",type=int,default=3)
    ap.add_argument("--max-len",type=int,default=3)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    sequences, graphs = load_sequences(), load_graphs()
    b,m = seq_support(sequences,[{"bread"},{"milk"}])
    b_adj,m_adj = seq_support(sequences,[{"bread"},{"milk"}],max_gap=0)
    patterns=prefixspan_singletons(sequences,args.min_count,args.max_len)
    edge_ab={"nodes":{"x":"A","y":"B"},"edges":[["x","y"]]}
    path_abc={"nodes":{"x":"A","y":"B","z":"C"},"edges":[["x","y"],["y","z"]]}
    triangle={"nodes":{"x":"A","y":"B","z":"C"},"edges":[["x","y"],["y","z"],["x","z"]]}
    result={
        "synthetic":True,"sequence_count":len(sequences),
        "bread_then_milk":{"count":b,"ids":m,"adjacent_count":b_adj,"adjacent_ids":m_adj},
        "basket_bread_milk":{"count":basket_support(sequences,{"bread","milk"})[0]},
        "milk_then_coffee":{"count":seq_support(sequences,[{"milk"},{"coffee"}])[0]},
        "bread_and_milk_same_event":{"count":seq_support(sequences,[{"bread","milk"}])[0]},
        "prefixspan_singletons":{" ".join(p):c for p,c in sorted(patterns.items())},
        "graph_support":{"AB":graph_support(graphs,edge_ab)[0],"ABC_path":graph_support(graphs,path_abc)[0],
                         "ABC_triangle":graph_support(graphs,triangle)[0]},
    }
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:
        args.output.write_text(text+"\n",encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
