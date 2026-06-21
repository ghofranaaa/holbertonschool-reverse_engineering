#!/usr/bin/env python3

# Expected values array from the binary (60 values, indices 0-59 = 0x3b)
expected = [
    0x80, 0xe4, 0x08, 0x18, 0x4a, 0x58, 0xb8, 0xe4,
    0xac, 0x34, 0x58, 0xe4, 0x7e, 0xbc, 0x9e, 0x8c,
    0x7e, 0xd0, 0xc0, 0x7c, 0xac, 0xf4, 0x7e, 0x28,
    0x9e, 0x04, 0x7e, 0xbc, 0x9e, 0x8c, 0x7e, 0x5c,
    0x14, 0x4c, 0x7e, 0x5c, 0x7e, 0x6c, 0x02, 0x14,
    0xb8, 0x4c, 0x14, 0xa4, 0x9e, 0x08, 0x7e, 0xe4,
    0xf4, 0x08, 0x6a, 0x14, 0xa6, 0x5c, 0xb8, 0x7c,
    0x9e, 0x28, 0x3e, 0xac
]

# Algorithm:
# if i is even: val = (char * 0xffffffd2) ^ 0xfffffe90, masked & 0xff
# if i is odd:  val = (char * 0x13c) ^ 0x9e0, masked & 0xff

# Flag format: Holberton{XXXXX?}
# Known prefix: "Holberton{"  = 10 chars
# Known suffix: "}"
# Length = 60 chars (loop goes 0 to 0x3b = 59)

import string

# Brute force each character
charset = string.ascii_lowercase + '_!@#$%^&*?}'

def transform(char, i):
    c = ord(char)
    if i % 2 == 0:
        val = (c * 0xffffffd2) ^ 0xfffffe90
    else:
        val = (c * 0x13c) ^ 0x9e0
    return val & 0xff

# Known prefix
known = "Holberton{"
flag = list(known) + ['?'] * (60 - len(known))
flag[59] = '}'

# Verify known prefix
for i, c in enumerate(known):
    result = transform(c, i)
    print(f"[{i}] '{c}' -> {hex(result)} == {hex(expected[i])} : {result == expected[i]}")

# Brute force unknown positions
print("\nBrute forcing unknown chars...")
all_chars = string.ascii_lowercase + string.digits + '_!@#$%^&*?!}'

for i in range(len(known), 59):
    for c in all_chars:
        if transform(c, i) == expected[i]:
            flag[i] = c
            break

print("\nFlag:", "".join(flag))