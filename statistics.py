from fractions import Fraction as f
from functools import reduce
import math


class Ensamble:
    def __init__(self, A, P):
        assert(len(A) == len(P))
        assert(sum(P) == 1)

        self._pairs = dict(zip(A, P))

    def A(self):
        return list(zip(*self.tuples()))[0]

    def P(self):
        return list(zip(*self.tuples()))[1]
    
    def tuples(self):
        return sorted(self._pairs.items(), key=lambda t: t[0])

    def p(self, a):
        return self._pairs[a]
    
    def expand(self, a, p):
        self._pairs = dict(map(lambda t: (t[0], t[1] * (1-p)), self.tuples()))
        self._pairs[a] = p

    def entropy(self):
        return -sum([p * math.log(p, 2) for p in self.P()])

    def min_encoding_length(self, message):
        """
        Assuming iid symbols
        """
        return -math.log(reduce(lambda x,y: x*y, [self.p(a) for a in message]),2)
    
    def copy(self):
        return Ensamble(self.A(), self.P())

    def __str__(self):
        return "--- Ensamble\nA    B\n{}".format(
            "\n".join([
                ("{:<5}"*2).format(str(a),str(p)) for a,p in self.tuples()
            ])
        )
    
    @staticmethod
    def from_strings(strings):
        symbol_freqs = dict()

        for string in strings:
            for symbol in string:
                if symbol in symbol_freqs:
                    symbol_freqs[symbol] += 1
                else:
                    symbol_freqs[symbol] = 1
        
        symbol_count = sum([c for _, c in symbol_freqs.items()])
        A, P = tuple(zip(*[(s,f(c,symbol_count)) for s, c in symbol_freqs.items()]))

        return Ensamble(A,P)


if __name__ == "__main__":
    print("Demo of the available functionality in the statistics file:")

    e = Ensamble(['0','1'], [f(6,10), f(4,10)])
    print(e)
    print("Entropy: {}".format(e.entropy()))

    e.expand('2', f(1,10))
    print(e)
    print("Entropy: {}".format(e.entropy()))

    strings = ["10011","11100"]
    e2 = Ensamble.from_strings(strings)
    print(e2)
    print("Entropy: {}".format(e2.entropy()))


