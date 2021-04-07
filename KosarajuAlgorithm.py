# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 23:41:09 2021

@author: Michael Lin
"""

# Use Kosaraju's Algorithm
# Faster than DFS method


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
            # Due to not having the built-in mechanism of deselecting self-contained loops
            # Like the other implementation
            # The following logic needs to be added in order for this to work
            if course == prereq: 
                graph.pop(prereq)
            else:
                graph[prereq].add(course)
        
        return graph

    # This function reverts the edges
    def edge_reversal(self, graph):
        reverse_graph = {}
        for u in graph:
            reverse_graph[u] = set()
        for u in graph:
            for v in graph[u]:
                reverse_graph[v].add(u)
        return reverse_graph

    # This function traverses through the whole graph barring forbidden/seen regions
    def walk(self, graph, s, seen=set()):
        if seen is None:
            seen = set()
        prev_state, queue = dict(), set()
        prev_state[s] = None
        queue.add(s)
        while queue:
            u = queue.pop()
            for v in graph[u].difference(prev_state, seen):
                queue.add(v)
                prev_state[v] = u
        return prev_state

    # Topological sort using DFS
    def dfs_topsort(self, graph):
        seen, seq = set(), []
        
        def recurse(u):
            if u in seen:
                return
            seen.add(u)
            for v in graph[u]:
                recurse(v)
            seq.append(u)
            
        for u in graph:
            recurse(u)
        seq.reverse()
        return seq
    
    # Kosaraju's Algorithm
    # Step 1: Run dfs topsort to find a sequence
    # Step 2: Reverse all edges
    # Step 3: Run full traversal using sequence
    def find_scc(self, numCourses, prerequisites):
        graph = self.graph_transformation(numCourses, prerequisites)
        reverse_graph = self.edge_reversal(graph)
        sccs, seen = [], set()
        for u in self.dfs_topsort(graph):
            if u in seen: 
                continue
            C = self.walk(reverse_graph, u, seen)
            seen.update(C)
            sccs.append(C)
        return sccs, self.dfs_topsort(graph)
