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
def modMultInv(a, n) -> int:
    t = 0
    new_t = 1
    r = n
    new_r = a

    while new_r != 0:
        quotient = r // new_r
        
        temp = new_t
        new_t = t - quotient * new_t
        t = temp

        temp = new_r
        new_r = r - quotient * new_r
        r = temp

    if r > 1:
        return -1
    if t < 0:
        t += n
    return t

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

# p = 8443387835004101215851905054157724839443611784354943714867080447137227467125482283225661870188902481927291031623803848076838202005588776194736300663373289
# q = 12935144558132066666843525205115027645252508541376505355633204595670013888637205815127469543002003431382545047032763316310455959324586373400414535853870683

# calculate
n = p*q
phi = phi(p,q)
d = modMultInv(e, phi)

# print out all the numbers
print("p:", p)
print("q:", q)
print("n:", n)
print("phi:", phi)
print("e:", e)
print("d:", d)
print("e * d (mod phi):", (e * d) % phi)

# # encrypt - based on hard-coded p and q
# plaintext = 6759569506963574401869537758242835501766815189981273397955337795936567019014429127803797090682423142647973832860178613125969856093009480540013884861624
# plaintext_enc = modexp(plaintext, e, n)
# print("encrypted plaintext:", plaintext_enc)

# # decrypt - based on hard-coded p and q
# encryption = 87025328326623360381041427425456285738931607587831313249216326937149885497044701313846481619839243754389672471991414203455090267587922699687554543601897300689302144088372379355090453288183676918624767430833597665322749956654985310614944521053334038276506877719174634580476151457865672542858599814076665862301
# encryption_dec = modexp(encryption, d, n)
# print("decrypted encryption:", encryption_dec)
