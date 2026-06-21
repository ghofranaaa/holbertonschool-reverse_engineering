#!/usr/bin/env python3
encrypted_hex = "9E89846A786585866A977D797C8463807C7F6B67848BAB907B698370896B997C797C8D6C6F7E81AE866AB36D7B7F669D7E6A7F96678F9382898263B474"
encrypted = bytes.fromhex(encrypted_hex)
key = [ord(c) for c in "mysecretkey"]
flag = []
for i in range(len(encrypted)):
    step1 = (encrypted[i] - key[(i + 1) % 11]) & 0xFF
    step2 = step1 ^ key[i % 11]
    flag.append(chr(step2))
print("Flag:", "".join(flag))
