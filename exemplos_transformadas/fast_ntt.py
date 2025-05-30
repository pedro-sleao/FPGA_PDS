from red_mod import kred_3329, barret_red_3329, montgomery_red_3329, k_red

def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

n = 256
q = 3329
primitive_root = 17
twiddle_factors = [pow(primitive_root, reverse_Bits(i, 7), q) for i in range(n)]
# print(twiddle_factors)

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

def ct_ntt_256_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()

    A = [0]*n

    t = n
    m = 1   
    while m < n:
        t = t//2
        for i in range(0, m):
            j1 = 2*i*t
            j2 = j1 + t - 1
            S = twiddle_factors[m + i]
            for j in range(j1, j2+1):
                u = a[j]
                v = (a[j+t]*S) % q
                A[j] = (u + v) % q
                A[j+t] = (u - v) % q
        m = 2*m

    return A

a = [i for i in range(n)]
A = ct_ntt_256_3329(a)

print(A)