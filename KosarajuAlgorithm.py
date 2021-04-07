# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:57:05 2021

@author: Michael Lin
"""

# DFS topological sort
def dfs_topsort(G):
    S, seq = set(), []
    def recurse(u):
        if u in S: return
        S.add(u)
        for v in G[u]:
            recurse(v)
        seq.append(u)
    for u in G:
        recurse(u)
    # Without the reverse, it will show that we start from the farthest leaf 
    # node
    seq.reverse()
    return seq

# Reverse all edges
def tr(G):
    GT = {}
    for u in G:
        GT[u] = set()
    for u in G:
        for v in G[u]:
            GT[v].add(u)
    return GT

# Full traversal
def walk(G, s, S=set()):
    P, Q = dict(), set()
    P[s] = None
    Q.add(s)
    while Q:
        u = Q.pop()
        for v in G[u].difference(P,S):
            Q.add(v)
            P[v] = u
    return P

# Run a full traversal using dfs topological sort
def scc(G):
    GT = tr(G)
    sccs, seen = [], set()
    for u in dfs_topsort(G):
        if u in seen: continue
        C = walk(GT, u, seen)
        seen.update(C)
        sccs.append(C)
    return sccs

def graph_transformation(numCourses, prerequisites):
    graph = {_: set() for _ in range(numCourses)}
    for course, prereq in prerequisites:
        graph[prereq].add(course)
    return graph

def scc_canFinish(numCourses, prerequisites):
    G = graph_transformation(numCourses, prerequisites)
    GT = tr(G)
    sccs, seen = [], set()
    print("\nSEQ: ")
    print(dfs_topsort(G))
    for u in dfs_topsort(G):
        if u in seen: continue
        C = walk(GT, u, seen)
        seen.update(C)
        sccs.append(C)
    return sccs

def iter_topsort(numCourses, prerequisites):
    if not prerequisites: return True
    
		# Initialize indegrees and graph with all nodes
    indegrees = {n: 0 for n in range(0, numCourses)}
    graph = {n: [] for n in range(0, numCourses)}
    
		# build graph and indegrees dictionaries
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegrees[course] += 1
    
		# initalize queue with all nodes that have indegree = 0
    q = [course for course in indegrees if indegrees[course] == 0]
    if not q: return False
    visited = []
		
		# while q exists:
		# 1. pop a course, and mark it visited
		# 2. decrement indegrees of all neighbors of course
		# 3. add neighbor if updated indegree of neighbor == 0
    while q:
        course = q.pop(0)
        visited.append(course)
        for neighbor in graph[course]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                q.append(neighbor)
		# check to see if we've visited all nodes
    return visited

def main():
    G = {
        'a': set('bc'),
        'b': set('dei'),
        'c': set('d'),
        'd': set('ah'),
        'e': set('f'),
        'f': set('g'),
        'g': set('eh'),
        'h': set('i'),
        'i': set('h'),
        }
    
    test = {
        '0': set(),
        '1': set('0')
        }
    print("SCC: ")
    print(scc(G))
    print("\nDFS sort")
    print(dfs_topsort(test))
    # print(graph_transformation(2, [[0,1]]))
    print("\nLEETCODE canFinish Kosaraju Algorithm Test 1: ")
    print(scc_canFinish(2, [[0,1]]))
    print("\nLEETCODE canFinish Kosaraju Algorithm Test 2: ")
    print(scc_canFinish(2, [[0,1],[1,0]]))
    print("\nLEETCODE canFinish Kosaraju Algorithm Test 3: ")
    print(scc_canFinish(20, [[0,10],[3,18],[5,5],[6,11],[11,14],[13,1],[15,1],[17,4]]))
    
    
if __name__ == '__main__':
    main()

