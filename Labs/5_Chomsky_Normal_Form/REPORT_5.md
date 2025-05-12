# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Daniela Cojocari

----
## Objectives:

* Learn about Chomsky Normal Form (CNF).
* Get familiar with the approaches of normalizing a grammar.
* Implement a method for normalizing an input grammar by the rules of CNF.
  * The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
  * The implemented functionality needs executed and tested.
  * Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

* In order to normalize an input grammar by the rules of CNF there are needed 5 steps:
  * Elimination of empty strings
  * Elimination of unit productions
  * Elimination of non-productive symbols
  * Elimination of non-accessible symbols
  * Transforming to Chomsky Normal Form
  
    
* The emptyStringElimination function is designed to eliminate ε-productions from a context-free grammar. The function 
first builds a set called nullable that contains all non-terminal symbols that can derive ε. It starts with an empty 
set and iteratively adds non-terminals that have a direct production → ε, or have a production composed entirely of 
symbols already known to be nullable. This step continues until no new nullable symbols can be found. Then, a new 
dictionary new_P is created to store the updated grammar without ε-productions. For each non-terminal and its set of 
productions if a production is ε, it is skipped. Otherwise, the function examines which symbols in the production are 
nullable. It then generates all possible combinations of that production by optionally omitting any subset of the 
nullable symbols. Each new combination (that is not an empty string) is added to the set of new productions. After 
processing all productions, the original production set self.P is updated with new_P.

```
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

        self.P = new_P
```

* The unitProdElimination function eliminates unit productions from a context-free grammar. A dictionary unit_graph is 
created, where each non-terminal maps to a set of non-terminals it directly leads to via unit productions. The 
function iterates over each non-terminal A in self.VN, and for each of its productions if a production consists of 
exactly one symbol and that symbol is a non-terminal, it is identified as a unit production A → B. This relationship 
is recorded in the unit_graph. For each non-terminal A, the function computes all non-terminals B that A can reach 
through a sequence of unit productions. It uses a stack-based DFS (depth-first search) to find the transitive closure: 
it starts with the direct unit productions of A (from unit_graph[A]). It repeatedly pops elements from the stack and 
adds them to the set of reachable non-terminals for A, continuing the search through unit_graph[B]. A new dictionary 
new_P is created to store the updated productions. For each non-terminal A, two things are done: all of A's original 
productions that are not unit productions are copied to new_productions and for every non-terminal B that is reachable
from A via unit productions, all of B's non-unit productions are also added to A’s productions.

```
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

        self.P = new_P
```

* The nonprodSymbolsElimination function removes non-productive symbols from a context-free grammar. An empty set called
productive is created to store all non-terminals that are known to be productive. A flag changed is set to True to 
enter the iterative discovery loop. The loop continues as long as new productive symbols are being found. For each 
non-terminal A in self.VN if A is already in the productive set, it is skipped, otherwise each production A → α is 
checked: if all symbols in α are either terminals (self.VT) or already known to be productive non-terminals, then A 
is marked as productive. The loop is marked as “changed = True” to indicate progress. A new dictionary new_P is created 
to store updated productions rules. For each productive non-terminal A, its productions are filtered: only those in 
which all symbols are terminals or productive non-terminals are retained. These valid productions are stored in new_P.


```
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
```

* The inaccesibileSymbolsElimination function removes inaccessible symbols from a context-free grammar. A set 
accessibleSymbols is created to store non-terminals that are considered accessible. The function loops through all 
production rules: for each non-terminal A and each of its productions it examines each character char in the production
string. If the character is a non-terminal and not already in accessibleSymbols, it is added. A new dictionary new_P is
constructed to store production rules only for accessible non-terminals. For each accessible non-terminal A it keeps 
productions where all symbols are terminals or accessible non-terminals.


```
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

        self.VN = accessibleSymbols
        self.P = new_P
```

* The computeCNF function transforms a context-free grammar into Chomsky Normal Form (CNF), where each production must 
either consist of a single terminal or two non-terminal symbols. The function starts by initializing dictionaries to 
track replacements of terminals and combinations of non-terminals with new variables, as well as a counter for generating 
these new variable names. It iterates through each production rule of the grammar and checks whether the right-hand 
side of a rule contains terminals in longer productions. If a terminal appears in a rule with more than one symbol, 
it is replaced with a new non-terminal that maps to the original terminal. These replacement mappings are stored to 
avoid duplication. Next, the function ensures that all right-hand sides of productions have at most two non-terminal 
symbols. If a rule has more than two symbols, the function iteratively replaces the last two symbols with a new 
non-terminal and updates the production accordingly, continuing this process until the rule consists of only two 
symbols. Each newly introduced pair is also added to the production set, mapping it to the original pair of symbols. 
Finally, after processing all production rules in this way, the grammar’s production set is updated to reflect the new 
CNF-compliant structure, where every rule now conforms to the CNF format.

```
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
```


## Conclusions 
In this laboratory, the main focus was on understanding and implementing the transformation of context-free grammars 
into Chomsky Normal Form (CNF), an essential concept in formal language theory. The implementation systematically 
addressed each required step: eliminating empty strings, unit productions, non-productive and inaccessible symbols, 
and finally restructuring productions to comply with CNF standards. The process was handled through modular functions 
that iteratively updated the grammar's production rules while preserving its language. The functionality was encapsulated 
efficiently, allowing flexibility and potential reuse for any input grammar. Through this work, I gained deep theoretical 
understanding of CNF by practical implementing all the required rules.