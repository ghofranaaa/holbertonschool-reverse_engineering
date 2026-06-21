#!/usr/bin/env python3
import struct

# Encrypted flag - 7 chunks of 8 bytes from 0x4020
data = bytes.fromhex(
    "8e82d972b66c836f"
    "a896da60a7779a69"
    "bc84db77a0729877"
    "a582d1758c778461"
    "a883da69ba70905f"
    "a498c14fba6da861"
    "9980c063a763f700"
)

# Read as little-endian 64-bit from exact bytes
exponent = struct.unpack('<Q', bytes.fromhex('ffffffffffff0000'))[0]
modulus  = struct.unpack('<Q', bytes.fromhex('fbffffffffffffff'))[0]

# But modulus is 8 bytes at 0x4060: fbffffff ffffff0f
modulus = struct.unpack('<Q', bytes.fromhex('fbffffffffffffff0f'[:16]))[0]

print(f"exponent: {hex(exponent)}")
print(f"modulus:  {hex(modulus)}")

key = pow(2, exponent, modulus)
print(f"key: {hex(key)}")

flag = ""
for i in range(7):
    chunk = struct.unpack('<Q', data[i*8:(i+1)*8])[0]
    decrypted = chunk ^ key
    for j in range(8):
        byte = (decrypted >> (j*8)) & 0xFF
        if byte != 0:
            flag += chr(byte)

print(f"Flag: {flag}")