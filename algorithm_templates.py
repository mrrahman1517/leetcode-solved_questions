from collections import defaultdict, Counter, deque
from heapq import heappush, heappop
from typing import List, Tuple, Optional

# Sliding window template (at most k distinct)
def longest_substr_k_distinct(s: str, k: int) -> int:
    freq, left, best = defaultdict(int), 0, 0
    for right, ch in enumerate(s):
        freq[ch] += 1
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0: del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best

# Binary search on answer with predicate
def bs_answer(lo, hi, ok):
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid): hi = mid
        else: lo = mid + 1
    return lo

# Dijkstra (adj list: u -> list[(v, w)])
def dijkstra(n: int, adj: List[List[Tuple[int,int]]], src: int) -> List[int]:
    INF = 10**18
    dist = [INF]*n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d,u = heappop(pq)
        if d != dist[u]: 
            continue
        for v,w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heappush(pq, (nd, v))
    return dist

# Topological sort (Kahn)
def topo_order(n: int, edges: List[Tuple[int,int]]) -> Optional[List[int]]:
    g = [[] for _ in range(n)]
    indeg = [0]*n
    for u,v in edges:
        g[u].append(v); indeg[v]+=1
    q = deque([i for i in range(n) if indeg[i]==0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return order if len(order)==n else None

# Union-Find
class DSU:
    def __init__(self, n): 
        self.p=list(range(n)); self.r=[0]*n
    def find(self,x):
        while x!=self.p[x]:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb: return False
        if self.r[ra]<self.r[rb]: ra,rb=rb,ra
        self.p[rb]=ra
        if self.r[ra]==self.r[rb]: self.r[ra]+=1
        return True
