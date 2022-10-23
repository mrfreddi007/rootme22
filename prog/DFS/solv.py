#!/usr/bin/env python3
from pwn import *

r = remote("ctf10k.root-me.org",8001)

def dfs(visited, graph, node):
    global reaches
    if node not in visited:
        reaches.append(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    return reaches

for j in range(60):
    chal = r.recv().decode()
    if "Hum, are you" in chal:
        print(chal)
        r.sendline("yes")
        chal = r.recv()
    chal = chal.split("\n")
    print(chal)
    
    visited = set()
    graph = dict()

    for i,nodes in enumerate(chal[2:]):
        if ">" in nodes:
            continue
        try:
            graph[str(i)] = nodes.split(" : ")[1].split(", ")
        except:
            graph[str(i)] = []
        
    reachable = chal[1].split("reach node ")[1].split(" from")[0] #Node to reach
    fra = chal[1].split(" from ")[1].split(" please")[0] #From which node
    
    reaches = []
    
    dfs(visited,graph,fra)
    print(reaches)
    
    if reachable in reaches:
        r.sendline("yes")
    else:
        r.sendline("no")
    
    
    
    
print(r.recv())