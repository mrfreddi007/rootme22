#!/usr/bin/env python3
import enum
from pwn import *
import operator

def RPN(eq):
    operatorer = ["+","-","*","/"]
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

    while len(eq)>2:
        for i, a in enumerate(eq):
            if a in operatorer:
                sum = ops[a](int(eq[i-2]),int(eq[i-1]))
                eq = eq[0:i-2] + [str(sum)] + eq[i+1:]
                break
    return eq[0]

r = remote("ctf10k.root-me.org",8002)
eq = r.recv().decode().split("\n")[1].replace("x","*").split(" ")
eq = RPN(eq)
r.sendline(eq)
eq = r.recv()

while True:
    eq = eq.decode().split("\n")[2].replace("x","*").split(" ")
    eq = RPN(eq)
    r.sendline(eq)
    eq = r.recv()
    if b"RM{" in eq:
        print(eq.decode())
        break
    
        
