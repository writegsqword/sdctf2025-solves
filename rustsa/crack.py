import math


expo = 65537
ciphertext = 187943791592623141370643984438525124469
pubmod = int(2**128)

# Python3 program to find modular
# inverse of A under modulo M

# A naive method to find modulor
# multiplicative inverse of A
# under modulo M

# Python3 program to find multiplicative modulo
# inverse using Extended Euclid algorithm.

# Global Variables
x, y = 0, 1

# Function for extended Euclidean Algorithm


def gcdExtended(a, b):
    global x, y

    # Base Case
    if (a == 0):
        x = 0
        y = 1
        return b

    # To store results of recursive call
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd


def modInverse(A, M):

    g = gcdExtended(A, M)
    if (g != 1):
        print("Inverse doesn't exist")

    else:

        # m is added to handle negative x
        res = (x % M + M) % M
        print("Modular multiplicative inverse is ", res)
        return res


def modular_exponentiation(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

# This code is contributed by phasing17
if __name__ == "__main__":
    A = 65537
    M = 2**128

    inv = modInverse(A, M)
    print(modular_exponentiation(ciphertext, inv, M).to_bytes(16, byteorder='little'))



k = 65537
c = 187943791592623141370643984438525124469
m = 2**128

# Try to find a solution mod 2^8 (for Hensel lifting)
mod_small = 2**8
roots = []
for a in range(mod_small):
    if pow(a, k, mod_small) == c % mod_small:
        roots.append(a)

print("Possible roots mod 2^8:", roots)

mod = 2**128
# Initial solution mod 2^8
a = 117
n = 8

while n < 128:
    m = 2**n
    f = pow(a, k, 2**(n+1)) - c % 2**(n+1)
    df = (k * pow(a, k - 1, 2**(n+1))) % 2**(n+1)
    # We solve df * t ≡ -f mod 2^n
    t = (-f * pow(df, -1, 2**n)) % 2**n
    a = (a + t * 2**n) % 2**(n+1)
    n += 1

print("Solution a =", a)
print("Check:", pow(a, k, mod) == c)
