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

twiddle_factors = [pow(primitive_root, reverse_Bits(i, 7), q) for i in range(256)]
twiddle_factors_kred = [(i*pow(k_red, -1, q)) % q for i in twiddle_factors]

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

def gs_intt_256_3329(a: list[int]) -> list[int]:
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

def ntt_ct_kred(a: list[int]) -> list[int]:
    t = n
    m = 1
    while m < n:
        t = t//2
        for i in range(m):
            j1 = 2*i*t
            j2 = j1 + t - 1
            S = twiddle_factors_kred[m+i]
            for j in range(j1, j2+1):
                U = a[j]
                V = kred_3329(a[j+t]*S)
                a[j] = (U + V) % q
                a[j+t] = (U - V) % q
        m = 2*m
    return a

def intt_gs_kred(a: list[int]) -> list[int]:
    t = 1
    m = n
    while m > 1:
        j1 = 0
        h = m//2
        for i in range(h):
            j2 = j1 + t - 1
            S = pow(twiddle_factors[h+i], -1, q)*pow(k_red, -1, q) % q
            for j in range(j1, j2+1):
                U = a[j]
                V = a[j+t]
                temp = (U - V) % q
                a[j] = (U + V) % q
                a[j+t] = kred_3329(temp*S)
            j1 = j1 + 2*t
        m = m//2
        t = 2*t
    
    for j in range(n):
        nk_inv = (pow(n, -1, q)*pow(k_red, -1, q)) % q
        a[j] = kred_3329(a[j]*nk_inv)

    return a


a = [i for i in range(n)]
A = ntt_ct_kred(a)

print(intt_gs_kred(A))
