from itertools import combinations


class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def emptyStringElimination(self):
        nullable = set()
        changed = True
        while changed:
            changed = False
            for nonTerminal, productions in self.P.items():
                for production in productions:
                    if production == "ε" or all(symbol in nullable for symbol in production):
                        if nonTerminal not in nullable:
                            nullable.add(nonTerminal)
                            changed = True

        new_P = {}
        for nonTerminal, productions in self.P.items():
            new_productions = set()
            for prod in productions:
                if prod == "ε":
                    continue

                symbols = list(prod)
                positions = [i for i, symbol in enumerate(symbols) if symbol in nullable]

                for i in range(len(positions) + 1):
                    for indexes in combinations(positions, i):
                        new_prod = ''.join(
                            symbol for j, symbol in enumerate(symbols) if j not in indexes
                        )
                        if new_prod:
                            new_productions.add(new_prod)

                new_productions.add(prod)

            new_P[nonTerminal] = list(new_productions)

        print("Original productions:")
        print(self.P)
        self.P = new_P

        print("Nullable non-terminals:", nullable)

        print("Elimination of ε:")
        print(self.P)

    def unitProdElimination(self):
        print("Unit Productions:")

        unit_graph = {A: set() for A in self.VN}
        for A in self.VN:
            for prod in self.P.get(A, []):
                if len(prod) == 1 and prod in self.VN:
                    print(f"{A} -> {prod}")
                    unit_graph[A].add(prod)

        for A in self.VN:
            stack = list(unit_graph[A])
            while stack:
                B = stack.pop()
                if B not in unit_graph[A]:
                    unit_graph[A].add(B)
                    stack.extend(unit_graph[B])

        new_P = {}
        for A in self.VN:
            new_productions = set()
            for prod in self.P.get(A, []):
                if not (len(prod) == 1 and prod in self.VN):
                    new_productions.add(prod)
            for B in unit_graph[A]:
                for prod in self.P.get(B, []):
                    if not (len(prod) == 1 and prod in self.VN):
                        new_productions.add(prod)
            new_P[A] = list(new_productions)

        print("Elimination of unit productions:")
        self.P = new_P
        print(self.P)

    def nonprodSymbolsElimination(self):
        productive = set()

        changed = True
        while changed:
            changed = False
            for A in self.VN:
                if A in productive:
                    continue
                for prod in self.P.get(A, []):
                    if all(symbol in self.VT or symbol in productive for symbol in prod):
                        productive.add(A)
                        changed = True
                        break

        print("Productive symbols:", productive)

        new_P = {}
        for A in productive:
            new_productions = []
            for prod in self.P[A]:
                if all(symbol in self.VT or symbol in productive for symbol in prod):
                    new_productions.append(prod)
            new_P[A] = new_productions

        self.VN = productive
        self.P = new_P
        print("Elimination of non-productive symbols:")
        print(self.P)

    def inaccesibileSymbolsElimination(self):
        accessibleSymbols = set()

        for nonTerminal, productions in self.P.items():
            for production in productions:
                for char in production:
                    if char in self.VN and char not in accessibleSymbols:
                        accessibleSymbols.add(char)

        new_P = {}
        for A in accessibleSymbols:
            new_productions = []
            for prod in self.P[A]:
                if all(symbol in self.VT or symbol in accessibleSymbols for symbol in prod):
                    new_productions.append(prod)
            new_P[A] = new_productions

        print(f"Accessible symbols: {accessibleSymbols}")
        self.VN = accessibleSymbols
        self.P = new_P

        print("Elimination of non-accessible symbols:")
        print(self.P)

    def computeCNF(self):
        replacements = {}
        reverse_map = {}
        counter = 1
        new_productions = {}

        for symbol in self.P.keys():
            new_productions.setdefault(symbol, [])
            for production in self.P[symbol]:
                chars = list(production)

                for i in range(len(chars)):
                    if chars[i] in self.VT and len(chars) > 1:
                        terminal = chars[i]
                        if terminal not in replacements:
                            rep = f"X{counter}"
                            counter += 1
                            replacements[terminal] = rep
                            reverse_map[rep] = terminal
                            self.VN.add(rep)
                            new_productions[rep] = [terminal]
                        chars[i] = replacements[terminal]

                while len(chars) > 2:
                    last_two = chars[-2:]
                    pair = ''.join(last_two)
                    if pair not in replacements:
                        rep = f"X{counter}"
                        counter += 1
                        replacements[pair] = rep
                        reverse_map[rep] = pair
                        self.VN.add(rep)
                        new_productions[rep] = [''.join(last_two)]
                    chars = chars[:-2] + [replacements[pair]]

                new_productions[symbol].append(''.join(chars))

        self.P = new_productions

        print("Chomsky Normal Form:")
        print(self.P)

    def chomskyNormalForm(self):
        self.emptyStringElimination()
        print()
        self.unitProdElimination()
        print()
        self.nonprodSymbolsElimination()
        print()
        self.inaccesibileSymbolsElimination()
        print()
        self.computeCNF()


VN = {"S", "A", "B", "D"}
VT = {"a", "b", "d"}
P = {
    "S": ["dB", "AB", "B", "aA"],
    "A": ["ε", "d", "dS", "aAaAb"],
    "B": ["a", "aS", "A"],
    "D": ["Aba"]
}

g = Grammar(VN, VT, P)
g.chomskyNormalForm()
