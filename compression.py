from fractions import Fraction as f

class Arithmetic:
    """
    Assumes iid symbols.
    """

    def __init__(self, ensamble):
        self.e = ensamble
    
    def _qr(self, symbol):
        q = f(0)
        for a, p in self.e.tuples():
            if a == symbol:
                r = q + p
                break
            q += p
        return q, r

    def encode(self, message):
        u = f(0)
        v = f(1)
        p = v - u

        for symbol in message:
            q, r = self._qr(symbol)
            v = u + p * r
            u = u + p * q
            p = v - u
        
        encoded = ""
        a = f(0)
        b = f(1)
        while a < u or v < b:
            if u - a >= b - v:
                encoded += '1'
                a += (b - a) / 2
            else:
                encoded += '0'
                b -= (b - a) / 2
        
        return encoded

    def _bin2interval(self, enc):
        a = f(0)
        b = f(1)
        for bit in enc:
            if bit == '0':
                b = (a + b) / 2
            else:
                a = (a + b) / 2
        return a, b

    def _interval2char(self, u, v, a, b):
        base = u
        height = v - u
        for s, p in self.e.tuples():
            p_ = p * height
            if base <= a and base + p_ >= b:
                return base, base + p_, s
            else:
                base = base + p_
        assert False
   
    def _decode_eof(self, enc):
        a, b = self._bin2interval(enc)
        
        decoded = ""
        u = f(0)
        v = f(1)
        c = None
        while c != '.':
            u, v, c = self._interval2char(u, v, a, b)
            decoded += c
        
        return decoded
    
    def _decode_len(self, enc, length):
        a, b = self._bin2interval(enc)
        
        decoded = ""
        u = f(0)
        v = f(1)
        for _ in range(length):
            u, v, c = self._interval2char(u, v, a, b)
            decoded += c
        
        return decoded

    def decode(self, enc, length=0):
        if length == 0:
            return self._decode_eof(enc)
        else:
            return self._decode_len(enc, length)

class BossArithmetic:
    """
    Assumes iid symbols.
    """

    def __init__(self, ensamble):
        self.e = ensamble
    
    def _qr(self, symbol):
        q = f(0)
        for a, p in self.e.tuples():
            if a == symbol:
                r = q + p
                break
            q += p
        return q, r

    def encode(self, message):
        u = f(0)
        v = f(1)
        p = v - u

        for symbol in message:
            q, r = self._qr(symbol)
            v = u + p * r
            u = u + p * q
            p = v - u
        
        encoded = ""
        a = f(0)
        b = f(1)
        while u > (a + b) / 2  or (a + b) / 2 > v:
            if u > (a + b) / 2:
                encoded += '1'
                a = (a + b) / 2
            else:
                encoded += '0'
                b = (a + b) / 2
        
        return encoded

    def _bin2interval(self, enc):
        a = f(0)
        b = f(1)
        for bit in enc:
            if bit == '0':
                b = (a + b) / 2
            else:
                a = (a + b) / 2
        return a, b

    def _interval2char(self, u, v, center):
        base = u
        height = v - u
        for s, p in self.e.tuples():
            p_ = p * height
            if base <= center < base + p_:
                return base, base + p_, s
            else:
                base = base + p_
        assert False

        
    def decode(self, enc):
        a, b = self._bin2interval(enc)
        center = (a + b) / 2
        
        decoded = ""
        u = f(0)
        v = f(1)
        c = None
        while c != '.':
            u, v, c = self._interval2char(u, v, center)
            decoded += c
        
        return decoded

        

if __name__ == "__main__":
    from statistics import Ensamble
    test_message = '222221111100000.'
    e = Ensamble.from_strings([test_message])

    ar = Arithmetic(e)
    enc = ar.encode(test_message)
    print("=========: Standard Arithmetic")
    print("Entropy  : {}".format(e.entropy()))
    print("Encoded  : {}".format(enc))
    print("Length   : {}".format(len(enc)))
    print("Minimal  : {}".format(e.min_encoding_length(test_message)))
    print("Original : {}".format(test_message))
    print("Decoded  : {}".format(ar.decode(enc)))
    print("Decoded_l: {}".format(ar.decode(enc, len(test_message))))

    ar = BossArithmetic(e)
    enc = ar.encode(test_message)
    print("=========: Boss Arithmetic")
    print("Entropy  : {}".format(e.entropy()))
    print("Encoded  : {}".format(enc))
    print("Length   : {}".format(len(enc)))
    print("Minimal  : {}".format(e.min_encoding_length(test_message)))
    print("Original : {}".format(test_message))
    print("Decoded  : {}".format(ar.decode(enc)))