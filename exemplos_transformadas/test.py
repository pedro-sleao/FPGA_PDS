import sage.all as sage

q = 12289
n = 512
k_red = 3
m = 12
primitive_root = 3

def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

twiddle_factors = [pow(primitive_root, reverse_Bits(i, 8), q) for i in range(512)]
twiddle_factors = [(i * pow(k_red, -1, q)) % q for i in twiddle_factors]

twiddle_factors_inv = [(pow(i, -1, q) * pow(k_red, -1, q)) % q for i in twiddle_factors]

def kred_3329(a):
    c0 = a % (2**m)
    c1 = a//(2**m)
    return k_red*c0 - c1

def kred_2x_3329(a):
    c0 = a % (2**m)
    c1 = a//(2**m) % (2**m)
    c2 = a//(2**(2*m))
    return k_red**2 * c0 - k_red*c1 + c2

def ntt_ct_kred(a: list[int]) -> list[int]:
    t = n
    m = 1
    while m < n:
        t = t//2
        for i in range(m):
            j1 = 2*i*t
            j2 = j1 + t - 1
            S = twiddle_factors[m+i]
            for j in range(j1, j2+1):
                U = a[j]
                V = a[j+t]*S
                if m == 128:
                    U = kred_3329(U)
                    V = kred_2x_3329(V)
                else:
                    V = kred_3329(V)
                a[j] = (U + V)
                a[j+t] = (U - V)
        m = 2*m
    return a

def intt_ct_kred(a: list[int]) -> list[int]:
    t = 1
    m = n
    while m > 2:
        j1 = 0
        h = m//2
        for i in range(h):
            j2 = j1 + t - 1
            S = twiddle_factors_inv[h+i]
            for j in range(j1, j2+1):
                U = a[j]
                V = a[j+t]
                a[j] = (U + V)
                a[j+t] = ((U - V)*S)
                if m == 32:
                    a[j] = kred_3329(a[j])
                    a[j+t] = kred_2x_3329(a[j+t])
                else:
                    a[j+t] = kred_3329(a[j+t])
            j1 = j1 + 2*t
        m = m//2
        t = 2*t
    
    for j in range(t):
        U = a[j]
        V = a[j+t]
        a[j] = kred_3329((U + V) * pow(n, -1, q) * pow(k_red, -11, q))
        a[j+t] = kred_3329((U - V) * pow(n, -1, q) * pow(k_red, -10, q) * twiddle_factors_inv[1])

    return a


a = [i for i in range(n)]
A = ntt_ct_kred(a)

print(A)