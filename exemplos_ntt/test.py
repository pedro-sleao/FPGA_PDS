# Implementação dos algoritmos de NTT descritos no seguinte artigo:
# Speeding up the Number Theoretic Transform
# for Faster Ideal Lattice-Based Cryptography
# Patrick Longa and Michael Naehrig
# ================================================
# Alguns passos/funções foram retirados da biblioteca LatticeCrypto, disponível no artigo.

from LUT import *

q = 3329
n = 256
k_red = 13
k_red_inv = pow(k_red, -1, q)
m = 8
primitive_root = 17

def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

twiddle_factors = [pow(primitive_root, reverse_Bits(i, 7), q) for i in range(256)]

twiddle_factors_kred = [(i * k_red_inv) % q for i in twiddle_factors]
twiddle_factors_kred_inv = [(pow(i, -1, q) * k_red_inv) % q for i in twiddle_factors]

# twiddle_factors_kred = psi_12289_rev_kinv_512
# twiddle_factors_kred_inv = psi_12289_inv_rev_kinv_512

def kred(a):
    c0 = a % (2**m)
    c1 = a//(2**m)
    return k_red*c0 - c1

def kred_2x(a):
    c0 = a % (2**m)
    c1 = a//(2**m) % (2**m)
    c2 = a//(2**(2*m))
    return k_red**2 * c0 - k_red*c1 + c2

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

def pmul(a, b):
    c = [0]*n
    for i in range(n):
        c[i] = kred(a[i]*b[i])
        c[i] = kred(c[i])
    return c

def correction(a, p, N):
    for i in range(N):
        mask = a[i] >> 31
        a[i] += (p & mask) - p
        mask = a[i] >> 31
        a[i] += (p & mask)
    return a

def two_reduce(a):
    for i in range(n):
        a[i] = kred(a[i])
        a[i] = kred(a[i])
    return a


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

def intt_gs_kred(a: list[int]) -> list[int]:
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
    k_inv_7 = pow(k_red, -7, q)
    k_inv_8 = pow(k_red, -8, q)
    k_inv_11 = pow(k_red, -11, q)
    k_inv_10 = pow(k_red, -10, q)
    nK_inv = (n_inv * k_inv_8) % q
    psiK_inv = (n_inv * k_inv_7 * twiddle_factors_kred_inv[1]) % q

    for j in range(t):
        U = a[j]
        V = a[j+t]
        a[j] = kred((U + V) * nK_inv)
        a[j+t] = kred((U - V) * psiK_inv)

    return a

a = [i for i in range(n)]
b = [i for i in range(n)]

C = mul_test(a, b)

A = ntt_ct_kred(a)
B = ntt_ct_kred(b)

D = pmul(A, B)
D = correction(D, q, n)

C_ = intt_gs_kred(D)
C_ = two_reduce(C_)
C_ = correction(C_, q, n)

print(C_)

