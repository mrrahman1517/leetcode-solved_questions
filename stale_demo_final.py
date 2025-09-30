"""
Finally! A test that shows when the stale entry optimization matters.
The key insight: we need a graph where           if skip2 > 0:
        print("\nSUCCESS! The optimization prevents processing of stale entries!")
    else:
        print("\nStill no stale entries... The graph might need more complexity")skip2 > 0:
        print("\nSUCCESS! The optimization prevents processing of stale entries!")
    else:
        print("\nStill no stale entries... The graph might need more complexity")skip2 > 0:
        print("\nSUCCESS! The optimization prevents processing of stale entries!")
    else:
        print("\nStill no stale entries... The graph might need more complexity")s are visited multiple times
with different distances before the optimal distance is found.
"""

from heapq import heappush, heappop

def dijkstra_verbose(graph, start, end, use_optimization=True):
    """Dijkstra with detailed logging to show stale entries"""
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    
    processed = 0
    total_popped = 0
    stale_skipped = 0
    
    print(f"Starting Dijkstra ({'with' if use_optimization else 'without'} optimization)")
    
    while pq:
        d, u = heappop(pq)
        total_popped += 1
        
        if use_optimization and d != dist[u]:
            stale_skipped += 1
            print(f"  SKIPPED: Node {u} with distance {d} (current best: {dist[u]})")
            continue
            
        processed += 1
        print(f"  Processing: Node {u} with distance {d}")
        
        if u == end:
            print(f"  Found target! Distance: {d}")
            break
            
        # Explore neighbors
        for v in range(n):
            if graph[u][v] > 0:  # There's an edge
                new_dist = d + graph[u][v]
                if new_dist < dist[v]:
                    old_dist = dist[v]
                    dist[v] = new_dist
                    heappush(pq, (new_dist, v))
                    print(f"    Update: Node {v} from {old_dist} to {new_dist}")
    
    print(f"Final stats: Processed={processed}, Total popped={total_popped}, Stale skipped={stale_skipped}")
    return dist[end], processed, total_popped, stale_skipped


def create_stale_heavy_graph():
    """Create a graph that will definitely generate stale entries"""
    # This graph is designed so that:
    # 1. Node 0 initially finds expensive paths to nodes 1,2,3
    # 2. Later it discovers much cheaper paths through indirect routes
    # 3. This creates many stale entries in the priority queue
    
    n = 6
    graph = [[0] * n for _ in range(n)]
    
    # Initial expensive direct paths from 0
    graph[0][1] = 100  # 0 -> 1 (expensive)
    graph[0][2] = 100  # 0 -> 2 (expensive) 
    graph[0][3] = 100  # 0 -> 3 (expensive)
    
    # Cheap path through node 4
    graph[0][4] = 1    # 0 -> 4 (cheap)
    graph[4][1] = 1    # 4 -> 1 (cheap)
    graph[4][2] = 1    # 4 -> 2 (cheap)
    graph[4][3] = 1    # 4 -> 3 (cheap)
    
    # Even cheaper path through node 5 (discovered later)
    graph[0][5] = 5    # 0 -> 5 (medium)
    graph[5][1] = 1    # 5 -> 1 (cheap)
    graph[5][2] = 1    # 5 -> 2 (cheap)
    graph[5][3] = 1    # 5 -> 3 (cheap)
    
    # Path to target
    graph[1][3] = 1    # 1 -> 3
    graph[2][3] = 1    # 2 -> 3
    
    return graph


def main():
    print("=== Demonstrating Stale Entries in Dijkstra's Algorithm ===\\n")
    
    graph = create_stale_heavy_graph()
    
    print("Graph adjacency matrix:")
    for i, row in enumerate(graph):
        print(f"Node {i}: {row}")
    print()
    
    print("This graph will cause the algorithm to:")
    print("1. Initially find expensive paths 0->1 (cost 100), 0->2 (cost 100), 0->3 (cost 100)")
    print("2. Later discover cheaper paths 0->4->1 (cost 2), 0->4->2 (cost 2), 0->4->3 (cost 2)")
    print("3. The expensive entries remain in the queue as 'stale entries'")
    print()
    
    print("--- WITHOUT optimization (processes stale entries) ---")
    result1, proc1, pop1, skip1 = dijkstra_verbose(graph, 0, 3, use_optimization=False)
    
    print("\\n--- WITH optimization (skips stale entries) ---")
    result2, proc2, pop2, skip2 = dijkstra_verbose(graph, 0, 3, use_optimization=True)
    
    print(f"\\n=== RESULTS ===")
    print(f"Final distance to target: {result1} (both should be same)")
    print(f"Without optimization: Processed {proc1} entries")
    print(f"With optimization:    Processed {proc2} entries, Skipped {skip2} stale entries")
    print(f"Efficiency gain: {proc1 - proc2} fewer entries processed")
    
    if skip2 > 0:
        print("\\nSUCCESS! The optimization prevents processing of stale entries!")
    else:
        print("\\nStill no stale entries... The graph might need more complexity")


if __name__ == "__main__":
    main()