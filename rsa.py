from Crypto.Util import number


# GCD(a,b) using Euclids:
# a = q*b + r
def gcd(a, b) -> int:
    if a == 0 or b == 0:
        raise Exception()
    elif a < b:
        temp = a
        a = b
        b = temp
    elif a == b:
        return a

    # first pass
    r = a % b

    # repeat until the remainder is 0
    while r > 0:
        a = b
        b = r
        r = a % b
    
    # when r == 0, gcd() == b
    return b

# multiplicative inverse using extended euclid's: 
# 1 = (d * e) + (k * n)
# where 1 = d * e (mod n)
def modMultInv(a, b) -> int:
    s = 0
    old_s = 1
    r = b
    old_r = a

    while r != 0:
        quotient = old_r / r
        temp = r
        r = old_r - quotient * temp
        old_r = temp

# g^a (mod p) --- modular exponentiation
def modexp(g, a, p) -> int:
    if a < 1:
        raise Exception()

    # *** mod map
    mod_map = {}

    # base
    max_n = 1  # largest 2^n that fits in 
    temp = g % p
    mod_map.update({1:temp})

    # find largest 2^n exponent that fits in a exponent
    # compute mods as I go
    n = 2
    while n < a:
        max_n = n
        temp = (mod_map[n/2] ** 2) % p  # compute modexp
        mod_map.update({n:temp})  # add to map
        n *= 2

    # build list of exponents e in mod_map that add up to a and compute
    n = max_n
    result = mod_map[max_n]
    e = max_n

    # start from big e and work to small
    for exp, val in sorted(list(mod_map.items()), key=lambda x:x[0], reverse=True):
        if exp == max_n:
            continue # skip - already done
        if e + exp <= a:
            e += exp
            result *= val
    
    if e != a:
        raise Exception("\ne != a\nE:{} ; A:{}".format(e, a))

    # mod
    result %= p

    # print result
    return result

def phi(p,q) -> int:
    return (p-1)*(q-1)

def isHighBitSet(x, num_bits) -> bool:
    mask = 1 << (num_bits - 1)
    if x & mask > 0:
        return True
    else:
        return False

# ********** MAIN ********* #

# set vars
e = 65537

# get two primes p and q with:
# - high-bit (bit 2^511) set
# - gcd(e, PHI(n)) == 1
num_bits = 512  # number of bits in each prime

p = number.getPrime(num_bits)
q = number.getPrime(num_bits)
while not isHighBitSet(p, num_bits) or not isHighBitSet(q, num_bits) or gcd(e, phi(p,q)) > 1:
    p = number.getPrime(num_bits) # try a new p
    while not isHighBitSet(p, num_bits): # try until high-bit is set
        p = number.getPrime(num_bits)

    q = number.getPrime(num_bits) # try a new q
    while not isHighBitSet(q, num_bits): # try until high-bit is set
        q = number.getPrime(num_bits)

# calculate
n = p*q
phi = phi(p,q)
# d = modMultInv(e, phi)

# print out all the numbers
print("p:", p)
print("q:", q)
print("n:", n)
print("phi:", phi)
print("e:", e)
# print("d:", d)

# 
