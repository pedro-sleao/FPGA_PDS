# Implementação da NTT e INTT pela definição

import sage.all as sage

n = 256
q = 3329
Zq = sage.Integers(q)
primitive_root = min(Zq.zeta(n, all=True))

def ntt_256_3329(a: list[int]) -> list[int]:
    if len(a) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()
    
    A = [0 for i in range(n)]
        
    for j in range(n):
        for i in range(n):
            A[j] += Zq(primitive_root**(i*j)*a[i])
        
    return A

def intt_256_3329(A: list[int]) -> list[int]:
    if len(A) != n:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in A):
        raise ValueError()
    
    a = [0 for i in range(n)]
        
    for j in range(n):
        for i in range(n):
            a[j] += Zq(primitive_root**(-i*j)*A[i])
        a[j] = a[j]*sage.inverse_mod(n, q)
        
    return a
                   
a = [i for i in range(n)]
b = [i for i in range(n)]

A = ntt_256_3329(a)
B = ntt_256_3329(b)

C = [(x*y)%q for x, y in zip(A, B)]

result = intt_256_3329(C)

print(result)

