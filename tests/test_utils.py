import unittest

from api.utils import distance, check_distance


class UtilTests(unittest.TestCase):
    def test_distance_zero(self):
        test = (51.741753, -0.341337)
        self.assertEqual(0, distance(test, test))

    def test_distance_basic(self):
        marylebone_high_st = (51.524112, -0.148504)
        camden = (51.545113, -0.163054)
        self.assertEqual(2, int(distance(marylebone_high_st, camden)))

    def test_check_distance_basic(self):
        marylebone_high_st = (51.524112, -0.148504)
        camden = (51.545113, -0.163054)
        radius = 3
        self.assertTrue(check_distance(marylebone_high_st[0],
                                       marylebone_high_st[1],
                                       camden[0], camden[1], radius))

    def test_check_distance_too_small_radius(self):
        test = (51.741753, -0.341337)
        radius = -2
        self.assertFalse(check_distance(test[0], test[1], test[0], test[1], radius))

    def test_check_distance_too_big_radius(self):
        test = (51.741753, -0.341337)
        radius = 200000
        self.assertFalse(check_distance(test[0], test[1], test[0], test[1], radius))
        
    def test_check_distance_zero_radius(self):
        test = (51.741753, -0.341337)
        radius = 0
        self.assertTrue(check_distance(test[0], test[1], test[0], test[1], radius))
