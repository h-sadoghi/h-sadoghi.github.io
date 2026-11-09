"""داده‌کاوی، فصل ۱: بازتولید مثال قواعد انجمنی روی ۱۰ تراکنش ساختگی."""
from __future__ import annotations
from pathlib import Path
import csv

DATA = Path(__file__).with_name("transactions.csv")

def load_baskets(path: Path = DATA) -> list[set[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [set(row["items"].split("|")) for row in csv.DictReader(handle)]

def count(baskets: list[set[str]], *items: str) -> int:
    subset = set(items)
    return sum(subset <= basket for basket in baskets)

def rule(baskets: list[set[str]], antecedent: str, consequent: str) -> dict:
    n = len(baskets)
    a, b, ab = count(baskets, antecedent), count(baskets, consequent), count(baskets, antecedent, consequent)
    if a == 0 or b == 0:
        raise ValueError("برای محاسبهٔ معیارها فراوانی مقدم و تالی باید مثبت باشد.")
    support = ab / n
    confidence = ab / a
    lift = confidence / (b / n)
    leverage = support - (a / n) * (b / n)
    return dict(n=n, A=a, B=b, AB=ab, support=support,
                confidence=confidence, lift=lift, leverage=leverage)

if __name__ == "__main__":
    baskets = load_baskets()
    for ant, cons in [("پوشک", "شیر"), ("آبمیوه", "پوشک"), ("نان", "شیر")]:
        r = rule(baskets, ant, cons)
        print(f"{ant} => {cons}: A={r['A']} B={r['B']} AB={r['AB']} "
              f"support={r['support']:.4f} confidence={r['confidence']:.4f} "
              f"lift={r['lift']:.4f} leverage={r['leverage']:.4f}")
    assert rule(baskets, "پوشک", "شیر")["AB"] == 6
    assert abs(rule(baskets, "پوشک", "شیر")["lift"] - 60/49) < 1e-12
