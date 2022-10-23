#!/usr/bin/env python3

enc = ['þ', 'Ã', 'E', '\x97', '\x9f', 'ü', 'G', '\x9e', 'ÿ', '½', ']', '´', 'Þ', '½', 'a', '\x87', 'à', 'º', 'Y', '\x9e', '\x9f', 'à', ']', '³', 'Õ', 'þ', 'J', 'ñ', 'Þ', '¯', '\x1f', '¼']
key = [0xac,0x8e,0x3e,0xc1]
flag = ""
a = 0
for i in enc:
    flag += chr(ord(i) ^ key[a])
    a = (a+1)%4
    
print(flag)