import sage.all as sage

n = 256
q = 3329
Zq = sage.Integers(q)
primitive_root = min(Zq.zeta(n, all=True))

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

    A = bit_reverse_copy(a, n)

    m = 1   
    while m < n:
        w_m = primitive_root ** (n // (2*m))
        for i in range(0, n, 2*m):
            w = Zq(1)
            for j in range(m):
                u = A[i + j]
                v = Zq(w * A[i + j + m])
                A[i + j] = Zq(u + v)
                A[i + j + m] = Zq(u - v)
                w *= Zq(w_m)
        m <<= 1

    return A

a = [i for i in range(n)]
A = ct_ntt_256_3329(a)

print(A)