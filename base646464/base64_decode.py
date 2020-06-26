#!/usr/bin/python3

import base64

f = open('cipher.txt', 'r')

ciphertext = f.readline()

for i in range(25):
    ciphertext = base64.b64decode(ciphertext)

print(ciphertext)

f.close()
