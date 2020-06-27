#!/usr/bin/python3

import pandas as pd 

df = pd.read_csv('encrypted.txt', header=None, usecols=[0], names=['ciphertext'])
ascii_df = pd.read_csv('CTFAsciiFrequency.txt')

def ScoreText(ciphertext, letter_frequency):

    # Calculate the frequency of the ciphertext
    ciphertext_frequency = [0.0 for i in range(256)]
    for c in ciphertext: 
        ciphertext_frequency[c] += 1.0/len(ciphertext)

    score = 0.0
    for i in range(256):
        score += (ciphertext_frequency[i] - letter_frequency[i])**2

    return score

composite_key = []

for i in range(399):
    freq = df['ciphertext'].iloc[i::399].value_counts()
    composite_key.append(freq.index[0]^481)

key_19 = [0 for c in range(19)]
for i in range(19):
    key_char = composite_key[i::19]
    best_score = 100
    for k in range(256):
        plaintext = [c^k for c in key_char]
        score = ScoreText(plaintext, ascii_df['frequency'].tolist())
        if score<best_score: 
            key_19[i]=k
            best_score = score

key_21 = composite_key[:21]
key = key_19 + key_19[:2]
for i in range(21): key_21[i] = key_21[i] ^ key[i]

print(''.join(list(map(chr,key_19))))
print(''.join(list(map(chr,key_21))))