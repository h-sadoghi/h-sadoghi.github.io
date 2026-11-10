import unittest, math
import chapter03_examples as e

class Chapter3Tests(unittest.TestCase):
    def test_minkowski_and_triangles(self):
        self.assertEqual(e.minkowski((0,0),(3,4),1),7)
        self.assertEqual(e.minkowski((0,0),(3,4),2),5)
        self.assertEqual(e.minkowski((0,0),(3,4),float('inf')),4)
        with self.assertRaises(ValueError):e.minkowski((0,),(1,),.5)
    def test_binary_sparse(self):
        a=[1,1,0,0,0];b=[1,0,1,0,0]
        self.assertEqual(e.binary_counts(a,b),(1,1,1,2))
        self.assertAlmostEqual(e.jaccard(a,b),1/3)
        self.assertAlmostEqual(e.smc(a,b),3/5)
        self.assertEqual(e.jaccard([0,0],[0,0]),1)
    def test_cosine_correlation(self):
        self.assertAlmostEqual(e.cosine([1,2],[2,4]),1)
        self.assertAlmostEqual(e.pearson([1,2,3],[11,12,13]),1)
        with self.assertRaises(ValueError):e.cosine([0,0],[1,2])
    def test_mixed(self):
        d,_=e.gower_pair({'a':'A','b':0},{'a':'A','b':0},{'a':{'kind':'nominal'},'b':{'kind':'binary_asym'}})
        self.assertEqual(d,0)
        d,_=e.gower_pair({'a':None},{'a':1},{'a':{'kind':'numeric','range':2}})
        self.assertTrue(math.isnan(d))
    def test_kl_js(self):
        self.assertAlmostEqual(e.kl([.75,.25],[.5,.5]),.18872187554,places=8)
        self.assertGreater(e.kl([.5,.5],[.75,.25]), e.kl([.75,.25],[.5,.5]))
        self.assertTrue(math.isinf(e.kl([1,0],[0,1])))
        self.assertAlmostEqual(e.js([1,0],[0,1]),1)
    def test_mi(self):
        self.assertAlmostEqual(e.mutual_information([[.5,0],[0,.5]]),1)
        self.assertAlmostEqual(e.mutual_information([[.25,.25],[.25,.25]]),0)
    def test_mahalanobis(self):
        self.assertAlmostEqual(e.mahalanobis_diag([0,0],[3,1],[9,1]),math.sqrt(2))
    def test_full_report(self):
        r=e.demonstrator()
        self.assertEqual((r['binary_counts']['q'],r['binary_counts']['r'],r['binary_counts']['s'],r['binary_counts']['t']),(1,1,1,997))
        self.assertAlmostEqual(r['gower']['value'],(2/3+.2+1)/4)
        self.assertGreater(r['triangle_cosine']['xz'],r['triangle_cosine']['xy_plus_yz'])

if __name__=='__main__':unittest.main(verbosity=2)
