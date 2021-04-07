# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 23:41:09 2021

@author: Michael Lin
"""

# Use Kosaraju's Algorithm
# Faster than DFS method
import itertools

class Solution:
    # The following implementation uses Kosaraju's Algorithm
    # If there is a scc with size > 1, then it means that there is a cycle dependency
    def canFinish(self, numCourses, prerequisites):    
        if not prerequisites: return True
        result, seq = self.find_scc(numCourses, prerequisites)
        for v in result:
            if len(v) > 1:
                return False
        return len(seq) == numCourses

    #　This transforms the giving information into a dictionary of adjacent sets format
    def graph_transformation(self, numCourses, prerequisites):
        graph = {_: set() for _ in range(numCourses)}
        for course, prereq in prerequisites:
            # Due to not gaving the built-in mechanism of deselecting self-contained loops
            # Like the other implementation
            # The following logic needs to be added in order for this to work
            if course == prereq: 
                graph.pop(prereq)
            else:
                graph[prereq].add(course)
        
        return graph

    # This function reverts the edges
    def tr(self, G):
        GT = {}
        for u in G:
            GT[u] = set()
        for u in G:
            for v in G[u]:
                GT[v].add(u)
        return GT

    # This function traverses through the whole graph barring forbidden/seen regions
    def walk(self, G, s, S=set()):
        P, Q = dict(), set()
        P[s] = None
        Q.add(s)
        while Q:
            u = Q.pop()
            for v in G[u].difference(P,S):
                Q.add(v)
                P[v] = u
        return P

    # Topological sort using DFS
    def dfs_topsort(self, G):
        S, seq = set(), []
        def recurse(u):
            if u in S: return
            S.add(u)
            for v in G[u]:
                recurse(v)
            seq.append(u)
        for u in G:
            recurse(u)
        seq.reverse()
        return seq
    
    # Kosaraju's Algorithm
    # Step 1: Run dfs topsort to find a sequence
    # Step 2: Reverse all edges
    # Step 3: Run full traversal using sequence
    def find_scc(self, numCourses, prerequisites):
        G = self.graph_transformation(numCourses, prerequisites)
        GT = self.tr(G)
        sccs, seen = [], set()
        # print(self.dfs_topsort(G))
        for u in self.dfs_topsort(G):
            if u in seen: continue
            C = self.walk(GT, u, seen)
            seen.update(C)
            sccs.append(C)
        return sccs, self.dfs_topsort(G)