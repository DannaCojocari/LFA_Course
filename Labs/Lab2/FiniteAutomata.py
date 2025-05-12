from tabulate import tabulate


class FiniteAutomata:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def convertToGrammar(self):
        grammar = Grammar(self.Q, self.Sigma, self.delta, self.q0, self.F)
        return grammar

    def typeFA(self):
        for operation, states in self.delta.items():
            if (len(states)) > 1:
                return False  # non-deterministic
        return True  # deterministic

    def NFA_to_DFA(self):
        dfa = {}
        queue = []
        start_state = [self.q0]
        queue.append(start_state)
        dfa[tuple(start_state)] = {}

        while queue:
            current = queue.pop(0)
            for terminal in self.Sigma:
                new_state = []
                for state in current:
                    if (state, terminal) in self.delta:
                        for s in self.delta[(state, terminal)]:
                            if s not in new_state:
                                new_state.append(s)

                if new_state and tuple(new_state) not in dfa:
                    queue.append(new_state)
                    dfa[tuple(new_state)] = {}

                if new_state:
                    dfa[tuple(current)][terminal] = tuple(new_state)

        return dfa

    def faTable(self):
        table = []
        headers = ["State"] + list(self.Sigma)

        for state in self.Q:
            row = []

            if state == self.q0:
                row.append(f"→{state}")
            elif state in self.F:
                row.append(f"*{state}")
            else:
                row.append(state)

            for symbol in self.Sigma:
                transition = self.delta.get((state, symbol), [])
                row.append(f"{{{', '.join(transition)}}}" if transition else "∅")

            table.append(row)
        print(tabulate(table, headers, tablefmt="grid"))



class Grammar:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Vn = Q
        self.Vt = Sigma
        self.S = q0
        self.P = self.computeProductions(delta, F)

    def computeProductions(self, delta, F):
        prod = {}

        for (nonTerminal, terminal), state in delta.items():
            if nonTerminal not in prod:
                prod[nonTerminal] = []
            rule = [terminal + s for s in state]
            prod[nonTerminal].append(rule)

        for finalState in F:
            if finalState not in prod:
                prod[finalState] = []
            prod[finalState].append("")

        return prod

    def showGrammar(self):
        print("Vn = ", self.Vn)
        print("Vt = ", self.Vt)
        print("S = ", self.S)
        print("P = ", self.P)


if __name__ == '__main__':
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
    g = fA.convertToGrammar()
    g.showGrammar()
    print(fA.NFA_to_DFA())
    fA.faTable()
