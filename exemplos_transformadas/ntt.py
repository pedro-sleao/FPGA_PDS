#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 09:36:17 2025

@author: pedro
"""

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
                   
B = ntt_256_3329([i for i in range(n)])
b = intt_256_3329(B)

print(B)
print(b)

