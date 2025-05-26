import math

q = 3329

# Montgomery reduction parameters
R = 2**16
qinv = -pow(q, -1, R) % R

# Barret reduction parameters
k = math.ceil(math.log2(q))
mu = math.floor(2**(2*k)/q)

def barret_red_3329(a):
    t = (a * mu) >> (2 * k)
    r = a - t * q
    if r >= q:
        r -= q
    elif r < 0:
        r += q
    return r

print(qinv)