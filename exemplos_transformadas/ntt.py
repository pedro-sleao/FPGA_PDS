#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 09:36:17 2025

@author: pedro
"""

import sage.all as sage

def ntt(a: list[int], q: int) -> list[int]:
    if len(a) >= q:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()
    if (q-1) % len(a) != 0:
        raise ValueError()
        
    n = len(a)
    
    Zq = sage.Integers(q)
    
    primitive_root = min(Zq.zeta(n, all=True))
    
    A = [0 for i in range(n)]
        
    for j in range(n):
        for i in range(n):
            A[j] += Zq(primitive_root**(i*j)*a[i])
        
    return A

def intt(A: list[int], q: int) -> list[int]:
    if len(A) >= q:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in A):
        raise ValueError()
    if (q-1) % len(A) != 0:
        raise ValueError()

    n = len(A)
    
    Zq = sage.Integers(q)
    
    primitive_root = min(Zq.zeta(n, all=True))
    
    a = [0 for i in range(n)]
        
    for j in range(n):
        for i in range(n):
            a[j] += Zq(primitive_root**(-i*j)*A[i])
        a[j] = a[j]*sage.inverse_mod(n, q)
        
    return a
                        
B = ntt([1, 2, 3, 4], 7681)

print(B)

b = intt(B, 7681)

print(b)
