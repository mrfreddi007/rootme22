#!/usr/bin/env python3
import websocket
import mendeleev
import math
import binascii

def strtobin(str):
    str = "".join(f"{ord(i):08b}" for i in str)
    return str

def bin2str(binstr):
    chal = int(binstr,2)

    byte_number = chal.bit_length() + 7 // 8
    binary_array = chal.to_bytes(byte_number, "big")
    ascii_chal = binary_array.decode()
    return ascii_chal

stoffer = mendeleev.elements.get_all_elements()

ws = websocket.WebSocket()
ws.connect("ws://ctf10k.root-me.org:8000")


while True:

    chal = ws.recv()

    ascii_chal = bin2str(chal)
    if "RM{" in ascii_chal:
        svar = ascii_chal
        break
    print(ascii_chal)

    if "Yo, please tell me what is the value of the number of electrons" in ascii_chal:
        stoff = ascii_chal.split("for the ")[1]
        a = mendeleev.element(stoff)
        b = str(a.atomic_number)
    elif "Yo, please tell me what is the value of the cas number for the" in ascii_chal:
        stoff = ascii_chal.split("for the ")[1]
        a = mendeleev.element(stoff)
        b = a.cas
    elif "Yo" in ascii_chal:
        stoff = ascii_chal.split("for the ")[1]
        a = mendeleev.element(stoff)
        b = str(round(a.atomic_weight,1))
    elif "Can you tell me what is the cas number" in ascii_chal:
        stoff = ascii_chal.split("number of ")[1].split(" please")[0]
        a = mendeleev.element(stoff)
        b = a.cas
    elif "Can you tell me what is the number of electrons of" in ascii_chal:
        stoff = ascii_chal.split("electrons of ")[1].split(" please")[0]
        a = mendeleev.element(stoff)
        b = str(a.atomic_number)
    else:
        stoff = ascii_chal.split(" weight of ")[1].split(" please")[0]
        a = mendeleev.element(stoff)
        b = str(round(a.atomic_weight,1))

    print(b)
    b = strtobin(b)
    ws.send(b)
    svar = bin2str(ws.recv())
    if "RM{" in svar:
        break
    
print(svar)

ws.close()
    


