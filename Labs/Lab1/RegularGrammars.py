import random


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


a = Grammar()
a.generateStrings()
