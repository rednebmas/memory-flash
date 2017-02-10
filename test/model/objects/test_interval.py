import unittest
from model.objects.interval import Interval
from model.objects.note import Note

class TestInterval(unittest.TestCase):
    def test_subtract_interval(self):
        self.assertEqual(Interval.P5() - Interval.P4(), Interval.M2())

    def test_subtract_interval(self):
        self.assertEqual(Interval.M3() - Interval.M3(), Interval.P1())
    
    def test_equal(self):
        self.assertEqual(Interval.M2(), Interval.M2())
    
    def test_between(self):
        self.assertEqual(Interval.between(Note('C'), Note('D')), Interval.M2())
    
    def test_interval_number(self):
        self.assertEqual(Interval.P5().number, 5)
        self.assertEqual(Interval.m6().number, 6)
        self.assertEqual(Interval.M6().number, 6)

    def test_interval_quality(self):
        self.assertEqual(Interval.P5().quality_long, "perfect")
        self.assertEqual(Interval.P5().quality, "P")
        self.assertEqual(Interval.m6().quality_long, "minor")
        self.assertEqual(Interval.m6().quality, "m")
        self.assertEqual(Interval.M6().quality_long, "major")
        self.assertEqual(Interval.M6().quality, "M")

    def test_interval_half_steps(self):
        self.assertEqual(Interval.P5().half_steps, 7)
        self.assertEqual(Interval.m6().half_steps, 8)
        self.assertEqual(Interval.M6().half_steps, 9)

def main():
	unittest.main()

if __name__ == '__main__':
	main()