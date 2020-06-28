#!/usr/bin/python3

from pwn import *

def BinToAscii(bit_str):
    string = ''
    for i in range(0,len(bit_str),7):
        code = int(bit_str[i:i+7], 2)
        string += chr(code)
    return string

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293]

plaintext_bits = ['_' for i in range(301)]

for i in primes:
    conn = remote('2020.redpwnc.tf', '31284')
    conn.recvuntil(': ')
    conn.send('{}\n'.format(i-1))
    conn.recvuntil(': ')
    conn.send('{}\n'.format(i))
    response = conn.readline()
    conn.close()

    ciphertext_bits = response[12:-1].decode('utf-8')
    
    for j in range(0,301,i):
        bit = ciphertext_bits[j]
        if bit == '0': plaintext_bits[j] = '1'
        else: plaintext_bits[j] = '0'

# The second bit is the only bit we can't deduce this way. Given that we know the first letter to be 'f' set the second bit to 1.
plaintext_bits[1] = '1'

plaintext_bits = ''.join(plaintext_bits)
print(BinToAscii(plaintext_bits))