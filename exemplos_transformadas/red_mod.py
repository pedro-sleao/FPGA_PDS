import math

q = 3329
k = math.ceil(math.log2(q))
r = 2**k

# K-RED reduction parameters
k_red = 13 # 3329 = 13*2**8 + 1
m = 8

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

def kred_3329(a):
    c0 = a % (2**m)
    c1 = a//(2**m)
    return k_red*c0 - c1


print(kred_3329(3330))
