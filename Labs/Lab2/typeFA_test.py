import unittest
from FiniteAutomata import *


class MyTestCase(unittest.TestCase):
    def test_type(self):
        Q = {"q0", "q1", "q2", "q3"}
        Sigma = {"a", "b", "c"}
        delta = {
            ('q0', 'a'): ['q1'],
            ('q1', 'b'): ['q2', 'q1'],
            ('q2', 'c'): ['q3'],
            ('q3', 'a'): ['q1'],
            ('q0', 'b'): ['q2']
        }
        q0 = "q0"
        F = {"q3"}

        fA = FiniteAutomata(Q, Sigma, delta, q0, F)
        self.assertEqual(fA.typeFA(), False)


        delta2 = {
            ('q0', 'a'): ['q1'],
            ('q1', 'b'): ['q1'],
            ('q2', 'c'): ['q3'],
            ('q3', 'a'): ['q1'],
            ('q0', 'b'): ['q2']
        }
        fA2 = FiniteAutomata(Q, Sigma, delta2, q0, F)
        self.assertEqual(fA2.typeFA(), True)

        delta3 = {
            ('q0', 'a'): ['q1'],
            ('q1', 'b'): ['q1'],
            ('q2', 'c'): ['q3'],
            ('q3', 'a'): ['q1', 'q0,', 'q3'],
            ('q0', 'b'): ['q2']
        }
        fA3 = FiniteAutomata(Q, Sigma, delta3, q0, F)
        self.assertEqual(fA3.typeFA(), False)


if __name__ == '__main__':
    unittest.main()
