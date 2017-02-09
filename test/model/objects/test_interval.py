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

def main():
	unittest.main()

if __name__ == '__main__':
	main()