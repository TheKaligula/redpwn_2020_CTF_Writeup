# alien-transmissions-v2

This challenge is a variation on a repeating-key XOR cipher. It was likely seen as a more difficult challenge given the lower number of solves compared to the others. What likely makes this challenge seem difficult is the that the plaintext is encrypted with two repeating keys each of differing lenghts. However this does not make the cryptanalysis any more difficult then a repeating key XOR with only one key and in fact adds no additional security.

The challenge statement reads as follows:

```
The aliens are at it again! We've discovered that their communications are in base 512 and have transcribed them in base 10. However, it seems like they used XOR encryption twice with two different keys! We do have some information:

- This alien language consists of words delimitated by the character represented as 481
- The two keys appear to be of length 21 and 19
- The value of each character in these keys does not exceed 255

Find these two keys for me; concatenate their ASCII encodings and wrap it in the flag format.
```

From this we can derive that the alien alphabet contains 512 characters with character 481 representing a delimiter between words. At this point we can assume that the message is just numeric and will not translate to English. 
We are also given the key lenghts of the two keys, 21 and 19 characters respectively, used in this cipher.

Before we attempt to solve this challenge lets first look at the methodolgy used to recover the key for a repeating-key XOR cipher with a key length on *N*. Under such a cipher the first letter of the plaintext is XOR'ed with the first letter of the key, the second letter of the plaintext with the second letter of the key and so on, until the *N+1* letter of the plaintext which gets XOR'ed with the first letter of the key again. Therefore we the *1st, (N+1)th, (2N+1)th ...* letter of the plaintext all get XOR'ed with the same letter of the key. Hence, given a ciphertext, we can take an extract of the *1st, (N+1)th, (2N+1)th ...* letters and perform a frequency analysis to recover the first letter of the key. We can then repeat this for the *2nd, (N+2)th, (2N+2)th ...* letter to recover the second letter of the key and so on until we have recover all N letters.

Now if we apply the same logic to this challenge then which characters in the plaintext would have been XOR with the same character in both keys? Given that the first key has a length of 21 and the second a length of 19, both keys will repeat at the lowest common multiple of 21 and 19 which is 399. That is, the first character of the plaintext gets XOR'ed with the first character of the key of length 21 (key 1) and the first character of the key of length 19 (key 2). The next character that gets XOR'ed by the same two character in key 1 and key 2 is character 400. This is equivalent to a repeating-key XOR cipher with a key length of 399.

Therefore we will follow the following process to recover the two key:
1. First we will recover the composite key of length 399 using the ciphertext provide.
2. Second we treat this composite key a ciphertext a attempt to recover the key of length 19 using the methodology descibed above.
3. Once we have this we can recover the key of length 21.

To begin we load the *encrypted.txt* file and start by analysing the distibution of the character of the subset of every slice of step 399 (i.e the length of the composite key). What becomes immediately evident is that for every slice there is one character that is a lot more frequent than all other. This is very likely the delimiter character which we know to be character 481 in the alien alphabet. Therefore we will loop through all slices of size 399 of ciphertext taking the most frequent character and XOR'ing it with 481 to get the composite key. The following Python code does this:

```python
import pandas as pd 

df = pd.read_csv('encrypted.txt', header=None, usecols=[1], names=['ciphertext'])

composite_key = []

for i in range(399):
    freq = df['ciphertext'].iloc[i::399].value_counts()
    composite_key.append(freq.index[0]^481)
```

Now that we have the composite key we treat this as our new ciphertext and we attempt to recover the key of length 19. This is now a repeating-key XOR of length 19 and so we take slices of length 19, loop though all character from 0 to 255 XOR'ing the ciphertext, score the resultant plaintext relative to the ASCII letter frequency and pick the character that gave the lowest score as the character of the key.

The method I use to score the plaintext is the *Squared Error* and I using a the character frequencies of the uppercase, lowercase and numbers. I replace the *space*  with _ since the flag format uses _ for spaces.

The scoring function is as followings:

```python
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
```

The code used to recover the key of length 19 is as follows:

```python
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
```

Finally, once we have the key of length 19 we can use it to XOR the first 21 characters of the composite key to recover the key of length 21.

```python
key_21 = composite_key[:21]
key = key_19 + key_19[:2]
for i in range(21): key_21[i] = key_21[i] ^ key[i]

print(''.join(list(map(chr,key_19))))
print(''.join(list(map(chr,key_21))))
```
The output that is given from running this code (`decrypt.py`) is:
```
_th3_53c0nd_15_th15
h3r3'5_th3_f1r5t_h4lf
```

Placing this in the flag format the flag becomes `flag{h3r3'5_th3_f1r5t_h4lf_th3_53c0nd_15_th15}`
