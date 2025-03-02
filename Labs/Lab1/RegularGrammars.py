import random
import re


class Grammar:
    def __init__(self):
        self.VN = {"S", "B", "L"}
        self.VT = {"a", "b", "c"}
        self.P = {
            "S": ["aB"],
            "B": ["bB", "cL"],
            "L": ["cL", "aS", "b"]
        }

    def generateStrings(self, non_terminal="S"):
        string = [None]*5

        for i in range(5):
            string[i] = non_terminal

            print(f"\nProcess for string nr. {i+1}:")
            while any(char in self.VN for char in string[i]):
                final_string = ""
                for char in string[i]:
                    if char in self.VN:
                        final_string += random.choice(self.P[char])
                    else:
                        final_string += char
                print(final_string)
                string[i] = final_string

        print(f"\nFinal result:")
        for i in range(5):
            print(f"{i+1}: {string[i]}")

    def toFiniteAutomaton(self):
        finiteAutomaton = FiniteAutomaton(self.VN, self.VT, self.P)
        return finiteAutomaton


    def chomskyHierarchy(self):
        type1 = True
        type2 = True
        type3 = True

        for leftSide, rightSide in self.P.items():
            leftLinear = False
            rightLinear = False

            if len(leftSide) > 1 or leftSide in self.VT:
                type2 = False
                type3 = False
            elif len(leftSide) > len(rightSide):
                type1 = False

            for term in rightSide:
                if re.match(r'^[a-z][A-Z]?$', term):
                    leftLinear = True
                elif re.match(r'^[A-Z]?[a-z]$', term):
                    rightLinear = True
                else:
                    type3 = False

                if leftLinear and rightLinear:
                    type3 = False

        if type3:
            return 3
        if type2:
            return 2
        if type1:
            return 1
        else:
            return 0




class FiniteAutomaton:
    def __init__(self, VN, VT, P):
        self.Q = VN
        self.Sigma = VT
        self.delta = self.transitions(P)
        self.q0 = "S"
        self.F = self.finalStates(P)


    def transitions(self, P):
        transitionSet = {}
        for non_terminal, productions in P.items():
            for production in productions:
                terminal = production[0]
                if production[1:] in self.Q:
                    state = production[1:]
                else:
                    state = "final"

                transitionSet[(non_terminal, terminal)] = state
        return transitionSet


    def finalStates(self, P):
        finalSet = []
        for non_terminal, productions in P.items():
            for production in productions:
                if all(char in self.Sigma for char in production):
                    finalSet.append((non_terminal, production))
        return finalSet


    def stringBelongToLanguage(self, inputString):
        state = self.q0
        final = ""

        print(f"\nValidation of string: {inputString}")

        for char in inputString:
            if (state, char) in self.delta:
                state = self.delta[(state, char)]
                final = char
            else:
                print(f"No transition from δ({state}, {char})")
                return False

        if (state, final) in self.F or state == "final":
            return True
        else:
            print(f"Final state wrong")
            return False


if __name__ == '__main__':
    grammar = Grammar()
    grammar.generateStrings()