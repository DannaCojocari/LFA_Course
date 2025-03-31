# Variant 2:  M? N^2 (O|P)^3 Q* R*
#             (X|Y|Z)^3 8+ (9|0)^2
#             (H|I) (J|K) L* N?

import random


def regex(input):
    expression = []
    elements = input.split()

    for element in elements:
        i = 0
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

    return "".join(expression)


def power(symbol_list, power, expression):
    if len(symbol_list) > 1:
        rand = random.randint(0, len(symbol_list) - 1)
        expression.extend(symbol_list[rand] * power)
    else:
        expression.extend(symbol_list[0] * power)
    return expression


print(regex("M? N^2 (O|P)^3 Q* R*"))
print(regex("(X|Y|Z)^3 8+ (9|0)^2"))
print(regex("(H|I) (J|K) L* N?"))
