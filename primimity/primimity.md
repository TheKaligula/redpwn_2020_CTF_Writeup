# primimity

This, like [4k-rsa](../4k-rsa/4k-rsa.md), is another RSA cipher challenge. The challenge statements reads as follows:

```
People claim that RSA with two 1024-bit primes is secure. But I trust no one. That's why I use three 1024-bit primes.

I even created my own prime generator to be extra cautious!
```

We are provided with `primimity-public-key.txt` which contains the public key numbers *N* and *e* of the RSA cipher and the encrypted message *C*. We are also given `primimity.py` which contains the code used to generate the *N* from three prime numbers. As the challenge statement states *N* is composed of three prime numbers which are each 1024 bits long. Factoring such a large *N* is impractical so there must be some weakness in the way it is composed.

Looking at the code, the function that generates the prime factors of *N* (*p,q and r*) is:

```python
def prime_gen():
    i = getRandomNBitInteger(1024)
    d = getRandomNBitInteger(8)
    for _ in range(d):
        i = find_next_prime(i)
    p = find_next_prime(i)
    d = getRandomNBitInteger(8)
    for _ in range(d):
        i = find_next_prime(i)
    q = find_next_prime(i)
    d = getRandomNBitInteger(8)
    for _ in range(d):
        i = find_next_prime(i)
    r = find_next_prime(i)
    return (p,q,r)
```

The function starts off my generating a 1024 bit number `i` and an 8 bit number `d`. In base 10 `d` can be between 128 and 255. The function then loops through the next `d` prime numbers and sets *p* equal to the prime number after that. The process is then repeated using the same `i` and `d` to generate *q* and again to generate *r*.

This is where the weakness in this RSA implementation is. One 1024 bit number is used to derive *p,q and r*. The next prime number is searched for starting from the previous and only skips the next `d` prime numbers. This means that *p,q and r* will, at most, only be 255 prime numbers apart. This means that these three number are going to be very close to the cube root of *N*. 

For RSA to be effective the selection of the primes used to compute *N* need to be carefully selected. It is not enough for them to just be large numbers. They also need to be significantly far away from eachother to make factoring difficult.

We can therefore break this RSA implementation as follows:
1. Find the cube root of *N*
2. Starting at the cube root, find the next prime number and see if it is a factor of *N*. 
3. Repeat step 2 until a number *p* has been found and divide *N* by it to get *M*
4. Starting at *p*, find the next prime number and see if it is a factor of *M*. 
5. Repeat step 4 until a number *q* has been found and divide *M* by it to to get *r*

The `factor_n.py` python program factors *N* in this manner.

Once we have *p,q and r*, we can use the same process as outlined in the [4k-rsa](../4k-rsa/4k-rsa.md) challenge to decrypt the ciphertext *C* and recover the flag.

The flag is: `flag{pr1m3_pr0x1m1ty_c4n_b3_v3ry_d4ng3r0u5}`