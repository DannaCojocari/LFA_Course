import unittest
from RegularGrammars import *


class MyTestCase(unittest.TestCase):
    def test_chomsky(self):
        grammar = Grammar()
        self.assertEqual(grammar.chomskyHierarchy(), 3)


if __name__ == '__main__':
    unittest.main()
