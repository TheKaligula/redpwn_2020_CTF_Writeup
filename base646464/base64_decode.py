#!/usr/bin/python3

import base64

with open('cipher.txt', 'r') as f:
    ciphertext = f.readline()

for i in range(25):
    ciphertext = base64.b64decode(ciphertext)

print(ciphertext)


