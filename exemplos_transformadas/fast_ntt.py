import sage.all as sage

def ct_ntt(a: list[int], q: int) -> list[int]:
    if len(a) >= q:
        raise ValueError()
    if not all((0 <= int(val) < q) for val in a):
        raise ValueError()
    if (q-1) % len(a) != 0:
        raise ValueError()
    
    n = len(a)

    if n == 1:
        return [a[0]]

    Zq = sage.Integers(q)
    
    primitive_root = Zq.zeta(2*n)
    
    A = [0 for i in range(n)]

    evens = ct_ntt(a[::2], q)
    odds = ct_ntt(a[1::2], q)

    for i in range(n//2):
        A[i] = Zq(evens[i] + primitive_root**(2*i+1)*odds[i])
        A[i + n//2] = Zq(evens[i] - primitive_root**(2*i+1)*odds[i])

    return A

a = [1, 2, 3, 4, 5, 6, 7, 8]
A = ct_ntt(a, 7681)

print(A)