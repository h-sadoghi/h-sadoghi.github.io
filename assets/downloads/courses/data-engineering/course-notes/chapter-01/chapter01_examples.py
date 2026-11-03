"""Chapter 01: CSV -> validation -> SQLite -> a small revenue report.

All records in orders_sample.csv are SYNTHETIC. Requires Python >=3.9 only.
"""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = ('order_id', 'order_date', 'city', 'status', 'amount_toman')
VALID_STATUSES = {'paid', 'pending', 'canceled'}


def clean_record(row: dict[str, str]) -> tuple[int, str, str, str, int]:
    """Return a validated row or raise ValueError with an explicit reason."""
    try:
        if None in row:
            raise ValueError('too many CSV fields in a row')
        for field in REQUIRED_COLUMNS:
            if row.get(field) is None:
                raise ValueError(f'missing CSV value for {field}')
        raw_id = row['order_id'].strip()
        if not raw_id.isascii() or not raw_id.isdecimal() or int(raw_id) <= 0:
            raise ValueError('order_id must be a positive integer')
        order_id = int(raw_id)
        date_text = row['order_date'].strip()
        date_value = None
        for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
            try:
                date_value = datetime.strptime(date_text, fmt).date().isoformat()
                break
            except ValueError:
                continue
        if date_value is None:
            raise ValueError('invalid order_date (use YYYY-MM-DD or DD/MM/YYYY)')
        city = row['city'].strip()
        if not city:
            raise ValueError('city is empty')
        status = row['status'].strip().lower()
        if status not in VALID_STATUSES:
            raise ValueError('unknown status')
        amount_text = row['amount_toman'].strip()
        if not amount_text or not amount_text.isascii() or not amount_text.isdecimal():
            raise ValueError('amount_toman must be a nonnegative integer')
        amount_toman = int(amount_text)
        return order_id, date_value, city, status, amount_toman
    except KeyError as exc:
        raise ValueError(f'missing field: {exc.args[0]}') from exc


def run_pipeline(input_csv: str | Path, output_dir: str | Path) -> dict:
    """Process a synthetic file and return reproducible quality/report metrics.

    A matching duplicate business key is discarded. A conflicting duplicate is
    quarantined (never silently overwritten). Repeated runs preserve totals.
    """
    input_csv = Path(input_csv)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = output_dir / 'orders.db'
    quarantine_path = output_dir / 'quarantine.csv'
    invalid_rows: list[dict[str, str]] = []
    seen: dict[int, tuple[int, str, str, str, int]] = {}
    duplicates = 0
    accepted = 0
    total_rows = 0

    with input_csv.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or tuple(reader.fieldnames) != REQUIRED_COLUMNS:
            raise ValueError(f'CSV header must be {REQUIRED_COLUMNS}')
        with sqlite3.connect(db_path) as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                order_date TEXT NOT NULL,
                city TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('paid','pending','canceled')),
                amount_toman INTEGER NOT NULL CHECK(amount_toman >= 0)
            )''')
            for line_no, row in enumerate(reader, start=2):
                total_rows += 1
                try:
                    record = clean_record(row)
                    if record[0] in seen:
                        if seen[record[0]] == record:
                            duplicates += 1
                            continue
                        raise ValueError('conflicting duplicate order_id in the input')
                    seen[record[0]] = record
                    old = connection.execute(
                        'SELECT order_id,order_date,city,status,amount_toman FROM orders WHERE order_id=?',
                        (record[0],)
                    ).fetchone()
                    if old is not None:
                        if tuple(old) == record:
                            accepted += 1  # valid source record; no DB mutation
                            continue
                        raise ValueError('order_id conflicts with previously stored data')
                    connection.execute('''INSERT INTO orders
                        (order_id,order_date,city,status,amount_toman)
                        VALUES (?,?,?,?,?)''', record)
                    accepted += 1
                except ValueError as exc:
                    invalid_rows.append({'line_no': str(line_no), **{name: row.get(name) or '' for name in REQUIRED_COLUMNS}, 'reason': str(exc)})
            report_rows = connection.execute('''SELECT city, COUNT(*) AS paid_orders,
                        SUM(amount_toman) AS revenue_toman
                FROM orders WHERE status='paid'
                GROUP BY city ORDER BY city''').fetchall()
            stored_rows = connection.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    # Quarantine is replaced, not appended, on each execution.
    with quarantine_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['line_no', *REQUIRED_COLUMNS, 'reason'])
        writer.writeheader()
        writer.writerows(invalid_rows)

    report = [{'city': city, 'paid_orders': n, 'revenue_toman': value}
              for city, n, value in report_rows]
    result = {'source_records': total_rows, 'accepted_records': accepted,
              'exact_duplicates': duplicates, 'rejected_records': len(invalid_rows),
              'stored_records': stored_rows, 'report': report,
              'total_paid_revenue_toman': sum(item['revenue_toman'] for item in report)}
    with (output_dir / 'report.json').open('w', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--input', type=Path, default=here / 'orders_sample.csv')
    parser.add_argument('--output-dir', type=Path, default=here / 'example_output')
    args = parser.parse_args()
    result = run_pipeline(args.input, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
