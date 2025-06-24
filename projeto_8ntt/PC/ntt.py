n = 8
q = 3329

# primitive_root = 40
# ZETA = [pow(primitive_root, reverse_Bits(i, 2), q) for i in range(4)]
# ZETA_MULT = [pow(primitive_root, 2*reverse_Bits(i, 2) + 1, q) for i in range(4)]

ZETA = [1, 1600, 40, 749]

ZETA_MULT = [40, 3289, 749, 2580]

def ct_ntt_8_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()

    f = a.copy()
    i = 1
    length = n//2

    while length >= 2:
        for start in range(0, n, 2 * length):
            zeta = ZETA[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f[j + length]) % q
                f[j + length] = (f[j] - t) % q
                f[j] = (f[j] + t) % q
        length //= 2

    return f

def gs_intt_8_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()

    f = a.copy()

    i = (n//2)-1
    length = 2
    while length <= n//2:
        for start in range(0, n, 2 * length):
            zeta = ZETA[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (f[j+length] + t) % q
                f[j + length] = (zeta*(f[j+length] - t)) % q
        length *= 2

    for i, x in enumerate(f):
        f[i] = (x*2497) % q

    return f

def base_case_multiply(a0, a1, b0, b1, gamma):
    c0 = (a0*b0 + a1*b1*gamma) % q
    c1 = (a0*b1 + a1*b0) % q
    return c0, c1

def multiply_ntt(f, g):
    h = [0] * n
    for i in range(n//2):
        h[2*i], h[2*i + 1] = base_case_multiply(f[2*i], f[2*i + 1], g[2*i], g[2*i + 1], ZETA_MULT[i])
    return h

def mul_test(a, b):
    c = [0] * n
    mask = n - 1

    for i in range(n):
        for j in range(n):
            index = (i + j) & mask
            prod = a[i] * b[j]
            if i + j >= n:
                c[index] = (c[index] - prod) % q
            else:
                c[index] = (c[index] + prod) % q

    return c

if __name__ == '__main__':
    a = [i for i in range(n)]
    b = [i for i in range(n)]
    A = ct_ntt_8_3329(a)
    B = ct_ntt_8_3329(b)
    
    C = multiply_ntt(A, B)

    D = gs_intt_8_3329(C)

    D_ = mul_test(a, b)

    print(D == D_)
