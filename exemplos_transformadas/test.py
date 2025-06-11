import sage.all as sage
from LUT import *

q = 12289
n = 512
k_red = 3
k_red_inv = pow(k_red, -1, q)
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

#twiddle_factors_kred = [(i * k_red_inv) % q for i in twiddle_factors]
#twiddle_factors_kred_inv = [(pow(i, -1, q) * k_red_inv) % q for i in twiddle_factors]

twiddle_factors_kred = psi_12289_rev_kinv_512
twiddle_factors_kred_inv = psi_12289_inv_rev_kinv_512

def kred(a):
    c0 = a % (2**m)
    c1 = a//(2**m)
    return k_red*c0 - c1

def kred_2x(a):
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
            S = twiddle_factors_kred[m+i]
            for j in range(j1, j2+1):
                U = a[j]
                V = a[j+t]*S
                if m == 128:
                    U = kred(U)
                    V = kred_2x(V)
                else:
                    V = kred(V)
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
            S = twiddle_factors_kred_inv[h+i]
            for j in range(j1, j2+1):
                U = a[j]
                V = a[j+t]
                a[j] = (U + V)
                a[j+t] = ((U - V)*S)
                if m == 32:
                    a[j] = kred(a[j])
                    a[j+t] = kred_2x(a[j+t])
                else:
                    a[j+t] = kred(a[j+t])
            j1 = j1 + 2*t
        m = m//2
        t = 2*t

    n_inv = pow(n, -1, q)
    k_inv_11 = pow(k_red, -11, q)
    k_inv_10 = pow(k_red, -10, q)
    nK_inv = (n_inv * k_inv_11) % q
    psiK_inv = (n_inv * k_inv_10 * twiddle_factors_kred_inv[1]) % q

    for j in range(t):
        U = a[j]
        V = a[j+t]
        a[j] = kred((U + V) * nK_inv)
        a[j+t] = kred((U - V) * psiK_inv)

    return a

a = [i for i in range(n)]
A = ntt_ct_kred(a)

print(A)

