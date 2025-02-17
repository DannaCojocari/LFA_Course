import unittest
from RegularGrammars import *

class MyTestCase(unittest.TestCase):
    def test_string(self):
        grammar = Grammar()
        fa = grammar.toFiniteAutomaton()

        self.assertEqual(fa.stringBelongToLanguage("abca"), False)
        self.assertEqual(fa.stringBelongToLanguage("bbca"), False)
        self.assertEqual(fa.stringBelongToLanguage("abbccaaabb"), False)
        self.assertEqual(fa.stringBelongToLanguage("accaabcc"), False)
        self.assertEqual(fa.stringBelongToLanguage("abcaacb"), True)


if __name__ == '__main__':
    unittest.main()
