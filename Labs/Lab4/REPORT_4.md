# Topic: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Daniela Cojocari

----
## Objectives:

* Write and cover what regular expressions are, what they are used for;
* Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:
  * Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown). Be careful that idea is to interpret the given regular expressions dinamycally, not to hardcode the way it will generate valid strings. You give a set of regexes as input and get valid word as an output 
  * In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations); 
  * Bonus point: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)


## Implementation description

* The implementation involves parsing the input regex, processing modifiers, and dynamically generating valid strings.
Below is a breakdown of the approach:
* The input regex string is first split into separate elements based on spaces, which allows us to process each element
individually, ensuring accurate handling of modifiers and symbol groups.
```
def regex(input):
    expression = []
    elements = input.split()
```

* If an element contains parentheses, it indicates a group of symbols separated by | (e.g., (A|B|C)). These symbols are 
extracted and stored into a buffer. It ensures further processing.
```
    for element in elements:
        i = 0;
        while i < len(element):
            char = element[i]

            if char == "(":
                i += 1
                symbols = []
                buffer = ""

                while i < len(element) and element[i] != ")":
                    if element[i] == "|":
                        if buffer:
                            symbols.append(buffer)
                            buffer = ""
                    else:
                        buffer += element[i]
                    i += 1

                if buffer:
                    symbols.append(buffer)
```

* Once symbols are extracted, we check the modifier following ')' to determine the number of repetitions. This ensures 
that '^n' represents exactly n occurrences, '*' means 0 to 5 occurrences, '+' is 1 to 5 occurrences and '?' represents 0
or 1 occurrence. If there is no modifier, then the element occurs one time.
```
                if i+1 < len(element) and element[i] == ")":
                    i += 1
                    if i+1 < len(element) and element[i] == "^" and element[i+1].isdigit():
                        power(symbols, int(element[i+1]), expression)
                        i += 2
                    elif element[i] == "*":
                        rand = random.randint(0, 5)
                        power(symbols, rand, expression)
                        i += 1
                    elif element[i] == "+":
                        rand = random.randint(1, 5)
                        power(symbols, rand, expression)
                        i += 1
                    elif element[i] == "?":
                        rand = random.randint(0, 1)
                        power(symbols, rand, expression)
                        i += 1
                else:
                    power(symbols, 1, expression)
                    i += 1
```

* If an element does not contain parentheses, we check if it has a modifier and apply the corresponding repetition rule.
This ensures correct handling of individual characters with modifiers.
```
            elif i+1 < len(element) and element[i+1] in "^*+?":
                if element[i+1] == "^" and i + 2 <= len(element) and element[i + 2].isdigit():
                    power(element[i], int(element[i+2]), expression)
                    i += 2
                elif element[i+1] == "*":
                    rand = random.randint(0, 5)
                    power(element[i], rand, expression)
                    i += 1
                elif element[i + 1] == "+":
                    rand = random.randint(1, 5)
                    power(element[i], rand, expression)
                    i += 1
                elif element[i + 1] == "?":
                    rand = random.randint(0, 1)
                    power(element[i], rand, expression)
                    i += 1
            else:
                expression.append(char)
            i += 1
```

* Once processing is complete, the function returns the final string that is converted from the list of processed symbols.
```
    return "".join(expression)

```

* The power() function ensures symbols are repeated correctly. If multiple symbols are available, it randomly selects
one and repeats it the specified number of times.
```
def power(symbol_list, power, expression):
    if len(symbol_list) > 1:
        rand = random.randint(0, len(symbol_list) - 1)
        expression.extend(symbol_list[rand] * power)
    else:
        expression.extend(symbol_list[0] * power)
    return expression
```


## Conclusions 
This project successfully implemented a dynamic interpretation of regular expressions, generating valid symbol 
combinations based on given rules. The approach ensures correct parsing of regex expressions into individual components, 
accurate handling of grouped symbols and modifiers (*, +, ?, ^n), and randomized selection of symbols where applicable 
to ensure varied outputs. It also provides a clear structure for modifying or expanding the code for additional regex 
features in the future. This work provides a solid foundation for understanding regex processing, showcasing a practical
implementation that can be extended further.