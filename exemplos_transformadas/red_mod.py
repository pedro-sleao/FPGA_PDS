import math

q = 3329
k = math.ceil(math.log2(q))
r = 2**k

# Montgomery reduction parameters
qinv = -pow(q, -1, r) % r

# Barret reduction parameters
mu = math.floor(r**(2)/q)

def barret_red_3329(a):
    t = (a * mu) >> (2 * k)
    c = a - t * q
    if c >= q:
        c -= q
    elif c < 0:
        c += q
    return c

def montgomery_red_3329(a):
    am = (a * r) % q    
    t = (am * qinv) % r
    cm = (am + t * q) >> k
    return cm

print(montgomery_red_3329(3330))