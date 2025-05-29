from red_mod import kred_3329, barret_red_3329, montgomery_red_3329

n = 256
q = 3329
primitive_root = 17

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
        w_m = pow(primitive_root, (n // (2*m)), q)
        for i in range(0, n, 2*m):
            w = 1
            for j in range(m):
                u = A[i + j]
                v = montgomery_red_3329(w * A[i + j + m])
                A[i + j] = montgomery_red_3329(u + v)
                A[i + j + m] = montgomery_red_3329(u - v)
                w = montgomery_red_3329(w*w_m)
        m <<= 1

    return A

a = [i for i in range(n)]
A = ct_ntt_256_3329(a)

print(A)