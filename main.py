plain_text = "HELLO"
cipher_text = "BYFFI"

for k in range(1, 26):
    s = "".join([(chr((ord(c) - 97 + k)%26 + 97)) for c in plain_text.lower()])
    if s == cipher_text.lower():
        print(f"Key: {k}")
        break

plain_text = "GOODLUCK"
cipher_text = ""
k = 7

for i in plain_text.lower():
    cipher_text += chr((ord(i) - 96 + k) % 26 + 96)
    #print(ord(i))

print(cipher_text.upper())
