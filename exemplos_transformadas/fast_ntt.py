from red_mod import kred_3329, barret_red_3329, montgomery_red_3329, k_red

n = 256
q = 3329
primitive_root = 17

def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

def bit_reverse_copy(a, n):
    result = [0]*n
    bits = n.bit_length()-1
    for k in range(n):
        rev = 0
        x = k
        for _ in range(bits):
            rev = (rev << 1) | (x & 1)
            x >>= 1
        result[rev] = a[k]
    return result

twiddle_factors = [pow(primitive_root, reverse_Bits(i, 7), q) for i in range(128)]

def ct_ntt_256_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()

    f = a.copy()
    i = 1
    length = 128

    while length >= 2:
        for start in range(0, 256, 2 * length):
            zeta = twiddle_factors[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f[j + length]) % q
                f[j + length] = (f[j] - t) % q
                f[j] = (f[j] + t) % q
        length //= 2

    return f

def ct_intt_256_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()

    f = a.copy()

    i = 127
    length = 2
    while length <= 128:
        for start in range(0, 256, 2 * length):
            zeta = twiddle_factors[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (f[j+length] + t) % q
                f[j + length] = (zeta*(f[j+length] - t)) % q
        length *= 2

    for i, x in enumerate(f):
        f[i] = (x*3303) % q

    return f


a = [i for i in range(n)]
A = ct_ntt_256_3329(a)

print(A)
