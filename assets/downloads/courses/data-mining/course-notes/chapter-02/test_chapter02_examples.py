#!/usr/bin/env python3
import unittest
from chapter02_examples import read_csv, quality_report, measure_summary, baskets, simpson, missing_bias

class TestChapter02(unittest.TestCase):
    def test_quality_and_grain(self):
        r = quality_report(read_csv('retail_lines_synthetic.csv'))
        self.assertEqual((r['n_rows'],r['distinct_orders'],r['missing_customer']), (14,12,1))
        self.assertAlmostEqual(r['completeness_customer'], 13/14)
        self.assertEqual(r['duplicate_line_keys'], [('I008','1')])
        self.assertEqual(set(r['errors']),{('I005','zero_quantity'),('I006','negative_unit_price')})
    def test_baskets(self):
        b=baskets(read_csv('retail_lines_synthetic.csv'))
        self.assertEqual(len(b),9)
        self.assertEqual(b['I001'],{'P01','P02'})
        self.assertNotIn('C009',b)
    def test_robust_stats(self):
        r=measure_summary()
        self.assertEqual([r[k] for k in ('mean','median','q1','q3','iqr','upper_fence')], [25,12.5,11,14,3,18.5])
        self.assertEqual(r['suspect'],[90])
    def test_simpson_and_missing(self):
        strat, pooled=simpson()
        self.assertGreater(strat['easy']['A'],strat['easy']['B'])
        self.assertGreater(strat['hard']['A'],strat['hard']['B'])
        self.assertLess(pooled['A'],pooled['B'])
        self.assertEqual(missing_bias(),(55,82))

if __name__ == '__main__':unittest.main(verbosity=2)
