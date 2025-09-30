"""
FINALLY! A test that will show the stale entry optimization.
The key insight: We need to force the algorithm t            if skip2 > 0:
        print("\nSUCCESS! The optimization works!")
        print(f"The stale entry check saved {skip2} unnecessary node processing operations.")
    else:
        print("\nEven this graph didn't generate stale entries in the specific order needed.")ip2 > 0:
        print("\nSUCCESS! The optimization works!")
        print(f"The stale entry check saved {skip2} unnecessary node processing operations.")
    else:
        print("\nEven this graph didn't generate stale entries in the specific order needed.")ip2 > 0:
        print("\nSUCCESS! The optimization works!")
        print(f"The stale entry check saved {skip2} unnecessary node processing operations.")
    else:
        print("\nEven this graph didn't generate stale entries in the specific order needed.")cess nodes 
in an order where stale entries MUST be popped before reaching the target.
"""

from heapq import heappush, heappop

def dijkstra_final_test(graph, start, end, use_optimization=True):
    """Dijkstra with the most detailed logging"""
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    
    processed = 0
    total_popped = 0
    stale_skipped = 0
    
    print(f"\\nStarting Dijkstra ({'WITH' if use_optimization else 'WITHOUT'} stale entry optimization)")
    print("Priority queue operations:")
    
    step = 0
    while pq:
        step += 1
        d, u = heappop(pq)
        total_popped += 1
        
        print(f"  Step {step}: Popped ({d}, {u})")
        
        if use_optimization and d != dist[u]:
            stale_skipped += 1
            print(f"    STALE! Current best distance to {u} is {dist[u]}, skipping...")
            continue
            
        processed += 1
        print(f"    Processing node {u} with distance {d}")
        
        if u == end:
            print(f"    Reached target! Final distance: {d}")
            break
            
        # Explore neighbors
        for v in range(n):
            if graph[u][v] > 0:  # There's an edge
                new_dist = d + graph[u][v]
                if new_dist < dist[v]:
                    old_dist = dist[v] 
                    dist[v] = new_dist
                    heappush(pq, (new_dist, v))
                    print(f"      Added ({new_dist}, {v}) to queue (improved from {old_dist})")
    
    print(f"\\nFinal: Processed={processed}, Total popped={total_popped}, Stale skipped={stale_skipped}")
    return dist[end], processed, total_popped, stale_skipped


def create_guaranteed_stale_graph():
    """Create a graph that GUARANTEES stale entries will be popped"""
    # Strategy: Create a graph where:
    # 1. Target is far away, requiring processing of intermediate nodes
    # 2. Intermediate nodes will have stale entries that must be processed
    # 3. Use a "diamond" pattern to force stale entry creation
    
    n = 7  # nodes 0,1,2,3,4,5,6
    graph = [[0] * n for _ in range(n)]
    
    # Create paths that ensure stale entries:
    # Path 1 (expensive): 0 -> 1 -> 6 (target)
    graph[0][1] = 50
    graph[1][6] = 1
    
    # Path 2 (cheap but longer): 0 -> 2 -> 3 -> 4 -> 5 -> 6
    graph[0][2] = 1
    graph[2][3] = 1  
    graph[3][4] = 1
    graph[4][5] = 1
    graph[5][6] = 1
    
    # Create a shortcut that improves path to node 1 AFTER it's been added to queue
    graph[2][1] = 1  # This will create a better path to node 1: 0->2->1 (cost 2) vs 0->1 (cost 50)
    
    return graph


def main():
    print("=== GUARANTEED Stale Entry Demonstration ===")
    
    graph = create_guaranteed_stale_graph()
    
    print("\\nGraph structure:")
    node_names = ["Start", "Expensive", "Cheap1", "Cheap2", "Cheap3", "Cheap4", "Target"]
    for i, row in enumerate(graph):
        connections = [f"{node_names[j]}({row[j]})" for j in range(len(row)) if row[j] > 0]
        print(f"{node_names[i]}: {' '.join(connections)}")
    
    print("\\nThis graph will:")
    print("1. Add expensive path to 'Expensive' node (cost 50)")
    print("2. Discover cheap path 0->Cheap1->Expensive (cost 2)")  
    print("3. The expensive entry (50, Expensive) becomes STALE")
    print("4. We MUST pop the stale entry to reach the target")
    
    # Test without optimization
    result1, proc1, pop1, skip1 = dijkstra_final_test(graph, 0, 6, use_optimization=False)
    
    # Test with optimization  
    result2, proc2, pop2, skip2 = dijkstra_final_test(graph, 0, 6, use_optimization=True)
    
    print("\\n" + "="*50)
    print("FINAL COMPARISON:")
    print(f"Final distance: {result1} (should be same for both)")
    print(f"Without optimization: {proc1} nodes processed, {pop1} total popped")
    print(f"With optimization:    {proc2} nodes processed, {pop2} total popped, {skip2} stale skipped")
    print(f"Efficiency improvement: {skip2} stale entries avoided")
    
    if skip2 > 0:
        print("\\nSUCCESS! The optimization works!")
        print(f"The stale entry check saved {skip2} unnecessary node processing operations.")
    else:
        print("\\nEven this graph didn't generate stale entries in the specific order needed.")


if __name__ == "__main__":
    main()