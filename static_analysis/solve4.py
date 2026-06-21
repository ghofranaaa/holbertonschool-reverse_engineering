#!/usr/bin/env python3

obfuscated = [
    0x8a, 0x101, 0x11e, 0x178, 0x163, 0x108, 0x136, 0x101,
    0x104, 0x12d, 0x178, 0x17f, 0x165, 0x11d, 0x171, 0x136,
    0x101, 0x171, 0x17f, 0x135, 0x135, 0x163, 0x11b, 0x178,
    0x11e, 0x127, 0x3f, 0x12b
]

flag = ""
for val in obfuscated:
    ebx = val
    ebx ^= 0x55        # XOR with 0x55
    ebx -= 7           # subtract 7
    quotient = ebx // 3    # idiv quotient in eax
    remainder = ebx % 3    # idiv remainder in edx
    # cmp al, dl -> comparing input byte to remainder (dl = edx low byte)
    # but let's try quotient
    print(f"val={hex(val)} ebx={hex(ebx)} quot={quotient}={chr(quotient) if 32<=quotient<=126 else '?'} rem={remainder}")
    flag += chr(quotient & 0xff)

print("\nFlag (quotient):", flag)