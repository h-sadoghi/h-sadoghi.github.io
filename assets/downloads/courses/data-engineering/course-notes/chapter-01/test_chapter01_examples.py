"""Run with: python -m unittest -v test_chapter01_examples.py (in downloads/)."""
import csv
import tempfile
import unittest
from pathlib import Path
from chapter01_examples import clean_record, run_pipeline


class Chapter01PipelineTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent
        self.fixture = self.root / 'orders_sample.csv'

    def test_expected_revenue_and_quality(self):
        with tempfile.TemporaryDirectory() as temp:
            r = run_pipeline(self.fixture, temp)
            self.assertEqual((r['source_records'], r['accepted_records'],
                              r['exact_duplicates'], r['rejected_records'],
                              r['stored_records']), (10, 7, 1, 2, 7))
            self.assertEqual(r['total_paid_revenue_toman'], 340000)
            self.assertEqual(r['report'], [
                {'city':'Isfahan','paid_orders':2,'revenue_toman':150000},
                {'city':'Tehran','paid_orders':3,'revenue_toman':190000}])
            with (Path(temp) / 'quarantine.csv').open(encoding='utf-8',newline='') as f:
                quarantined = list(csv.DictReader(f))
            self.assertEqual(len(quarantined), 2)

    def test_idempotence(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run_pipeline(self.fixture,temp), run_pipeline(self.fixture,temp))

    def test_date_normalization(self):
        r = {'order_id':'1009','order_date':'15/10/2026','city':'Tehran',
             'status':'paid','amount_toman':'40000'}
        self.assertEqual(clean_record(r)[1], '2026-10-15')

    def test_bad_values(self):
        r = {'order_id':'1','order_date':'2026-10-15','city':'Tehran',
             'status':'paid','amount_toman':'-1'}
        with self.assertRaises(ValueError): clean_record(r)

    def test_conflicting_duplicate_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'input.csv'
            p.write_text('order_id,order_date,city,status,amount_toman\n1,2026-10-15,Tehran,paid,10\n1,2026-10-15,Tehran,paid,20\n',encoding='utf-8')
            r = run_pipeline(p,Path(temp)/'out')
            self.assertEqual((r['accepted_records'],r['rejected_records'],r['stored_records']),(1,1,1))

    def test_incomplete_csv_row_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'short.csv'
            p.write_text('order_id,order_date,city,status,amount_toman\n1,2026-10-15,Tehran,paid\n', encoding='utf-8')
            r = run_pipeline(p,Path(temp)/'out')
            self.assertEqual((r['rejected_records'],r['stored_records']), (1,0))

    def test_extra_csv_field_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'long.csv'
            p.write_text('order_id,order_date,city,status,amount_toman\n1,2026-10-15,Tehran,paid,10,extra\n',encoding='utf-8')
            r = run_pipeline(p,Path(temp)/'out')
            self.assertEqual((r['rejected_records'],r['stored_records']), (1,0))

    def test_schema_error(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'bad.csv';p.write_text('id,wrong\n1,x\n',encoding='utf-8')
            with self.assertRaises(ValueError):run_pipeline(p,Path(temp)/'out')

if __name__ == '__main__': unittest.main()
