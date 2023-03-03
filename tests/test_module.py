import unittest
from src.FastaUtils import Nx0, FastaIO, say
# First party modules #
import os

this_dir = os.path.dirname(__file__)


class MyTestCase(unittest.TestCase):

    def test_Nx0(self):
        data = [10, 20, 30, 40, 50]
        self.assertEqual(Nx0(data, 50), (40, 2))

    def test_FastaIO(self):
        seqs = FastaIO(os.path.join(this_dir, 'sample.fasta'))
        self.assertEqual(len(seqs), 4)

    def test_say(self):
        strings = say('a','b',1, 1.0, indent=5, decimal=2)
        self.assertIn(strings.strip(), 'a    b    1    1.00')


if __name__ == '__main__':
    unittest.main()
