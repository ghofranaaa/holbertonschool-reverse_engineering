#!/usr/bin/env python3
import struct

# Raw .data bytes
data = bytes.fromhex(
    "8e82d972b66c836f"
    "a896da60a7779a69"
    "bc84db77a0729877"
    "a582d1758c778461"
    "a883da69ba70905f"
    "a498c14fba6da861"
    "9980c063a763f700"
)

# Exponent and modulus (little-endian 64-bit)
exponent = struct.unpack('<Q', bytes.fromhex('ffffffffffffff00'))[0]
modulus  = struct.unpack('<Q', bytes.fromhex('fbffffffffffff0f'))[0]

print(f"exponent: {hex(exponent)}")
print(f"modulus:  {hex(modulus)}")

# Fast modular exponentiation
key = pow(2, exponent, modulus)
print(f"key: {hex(key)}")

# Decrypt: XOR each 8-byte chunk with key
flag = ""
for i in range(7):
    chunk = struct.unpack('<Q', data[i*8:(i+1)*8])[0]
    decrypted = chunk ^ key
    # Extract bytes
    for j in range(8):
        byte = (decrypted >> (j*8)) & 0xFF
        if byte != 0:
            flag += chr(byte)

print(f"Flag: {flag}")