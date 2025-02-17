# Topic: Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Daniela Cojocari

----
## Objectives:

* Implementing a type/class for your grammar;
* Adding one function that would generate 5 valid strings from the language expressed by my given grammar;
* Implementing some functionality that would convert an object of type Grammar to one of type Finite Automaton;
* Adding a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

* For the grammar I implemented a constructor that initializes the non-terminal and terminal variables and the productions. 

```
class Grammar:
    def __init__(self):
        self.VN = {"S", "B", "L"}
        self.VT = {"a", "b", "c"}
        self.P = {
            "S": ["aB"],
            "B": ["bB", "cL"],
            "L": ["cL", "aS", "b"]
        }
```

* In order to generate 5 strings, I initialize the string with "S" which is the first non-terminal, then I check if there are non-terminals in the word and I replace it randomly with the production. This loop continues until it reaches a string with only terminals.

```
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
```

* For converting a grammar to a finite automaton I pass to the constructor of FA the non-terminal, terminal and production variables.


```
    def toFiniteAutomaton(self):
        finiteAutomaton = FiniteAutomaton(self.VN, self.VT, self.P)
        return finiteAutomaton
        
    ##
    
    class FiniteAutomaton:
    def __init__(self, VN, VT, P):
        self.Q = VN
        self.Sigma = VT
        self.delta = self.transitions(P)
        self.q0 = "S"
        self.F = self.finalStates(P)

```


* To determine delta I implemented a function called "transitions" which takes as a parameter the productions. For the transition set, the first two values are the non-terminal and terminal, and the last one represents the state. If the state is not present, then the state is marked as final. 


```
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
```

* To get the final states I implemented a function "finalStates" which determines the production which has no non-terminals. And this represents the final state.


```
    def finalStates(self, P):
        finalSet = []
        for non_terminal, productions in P.items():
            for production in productions:
                if all(char in self.Sigma for char in production):
                    finalSet.append((non_terminal, production))
        return finalSet
```


* For checking if a string belongs to the language, I initialized the state with q0 and began to verify every character from the string. If the system identifies a state and char in delta then it changes the state to the next one. If the state and char is not identified then the string is not valid.

```
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
```

* To check the function "stringBelongToLanguage" I implemented a unit test which verifies it.

```
class MyTestCase(unittest.TestCase):
    def test_string(self):
        grammar = Grammar()
        fa = grammar.toFiniteAutomaton()

        self.assertEqual(fa.stringBelongToLanguage("abca"), False)
        self.assertEqual(fa.stringBelongToLanguage("bbca"), False)
        self.assertEqual(fa.stringBelongToLanguage("abbccaaabb"), False)
        self.assertEqual(fa.stringBelongToLanguage("accaabcc"), False)
        self.assertEqual(fa.stringBelongToLanguage("abcaacb"), True)


```


## Conclusions 
The laboratory implements a successful generation of 5 strings from a grammar. Moreover, it converts a regular grammar into a finite automaton, by passing its variables. 

The most challenging part for me was implementing the validation of the string that belongs to the language, because I needed to identify a good method of creating the operations.

In conclusion, I succeeded to implement several functions, that shows the relationship regular grammars and finite automata. 

