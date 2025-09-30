#Course/Task scheduling with durations.

#Given n tasks 0..n-1, directed edges u->v (u must precede v), and time[i] for each task, compute the minimum total time to finish all tasks if you can run multiple tasks in parallel when prerequisites are done. If there’s a cycle, return -1.

#Idea: Kahn’s toposort; DP the earliest finish ef[i] = time[i] + max(ef[p] for p in preds(i)).

#Solution (O(n+e))

from collections import deque

def min_total_time(n, edges, time):
    g = [[] for _ in range(n)]
    indeg = [0]*n
    preds = [[] for _ in range(n)]
    for u,v in edges:
        g[u].append(v)
        preds[v].append(u)
        indeg[v]+=1

    q = deque([i for i in range(n) if indeg[i]==0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0:
                q.append(v)

    if len(order) != n:
        return -1

    ef = [0]*n
    for u in order:
        if preds[u]:
            ef[u] = time[u] + max(ef[p] for p in preds[u])
        else:
            ef[u] = time[u]
    return max(ef) if ef else 0


def test_min_total_time():
    """Comprehensive test cases for min_total_time function"""
    
    # Test 1: Simple linear dependency chain
    # Task 0 -> Task 1 -> Task 2
    n1 = 3
    edges1 = [(0, 1), (1, 2)]
    time1 = [1, 2, 3]
    result1 = min_total_time(n1, edges1, time1)
    expected1 = 6  # 1 + 2 + 3 = 6 (sequential)
    assert result1 == expected1, f"Test 1 failed: expected {expected1}, got {result1}"
    print(f"Test 1 passed: {result1}")
    
    # Test 2: Parallel tasks (no dependencies)
    # All tasks can run in parallel
    n2 = 3
    edges2 = []
    time2 = [5, 3, 7]
    result2 = min_total_time(n2, edges2, time2)
    expected2 = 7  # max(5, 3, 7) = 7 (all parallel)
    assert result2 == expected2, f"Test 2 failed: expected {expected2}, got {result2}"
    print(f"Test 2 passed: {result2}")
    
    # Test 3: Diamond dependency pattern
    # Task 0 -> Task 1, Task 0 -> Task 2, Task 1 -> Task 3, Task 2 -> Task 3
    n3 = 4
    edges3 = [(0, 1), (0, 2), (1, 3), (2, 3)]
    time3 = [1, 2, 3, 1]
    result3 = min_total_time(n3, edges3, time3)
    expected3 = 5  # Path: 0(1) -> 2(3) -> 3(1) = 1 + 3 + 1 = 5
    assert result3 == expected3, f"Test 3 failed: expected {expected3}, got {result3}"
    print(f"Test 3 passed: {result3}")
    
    # Test 4: Cycle detection
    # Task 0 -> Task 1 -> Task 2 -> Task 0 (cycle)
    n4 = 3
    edges4 = [(0, 1), (1, 2), (2, 0)]
    time4 = [1, 1, 1]
    result4 = min_total_time(n4, edges4, time4)
    expected4 = -1  # Cycle detected
    assert result4 == expected4, f"Test 4 failed: expected {expected4}, got {result4}"
    print(f"Test 4 passed: {result4}")
    
    # Test 5: Single task
    n5 = 1
    edges5 = []
    time5 = [10]
    result5 = min_total_time(n5, edges5, time5)
    expected5 = 10
    assert result5 == expected5, f"Test 5 failed: expected {expected5}, got {result5}"
    print(f"Test 5 passed: {result5}")
    
    # Test 6: Complex dependency tree
    # Multiple branches with different critical paths
    n6 = 6
    edges6 = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)]
    time6 = [1, 3, 2, 4, 1, 2]
    result6 = min_total_time(n6, edges6, time6)
    # Critical path: 0(1) -> 1(3) -> 3(4) -> 5(2) = 1 + 3 + 4 + 2 = 10
    expected6 = 10
    assert result6 == expected6, f"Test 6 failed: expected {expected6}, got {result6}"
    print(f"Test 6 passed: {result6}")
    
    # Test 7: Self-cycle (task depends on itself)
    n7 = 3
    edges7 = [(0, 1), (1, 1), (1, 2)]  # Task 1 depends on itself
    time7 = [1, 2, 3]
    result7 = min_total_time(n7, edges7, time7)
    expected7 = -1  # Cycle detected
    assert result7 == expected7, f"Test 7 failed: expected {expected7}, got {result7}"
    print(f"Test 7 passed: {result7}")
    
    # Test 8: Star pattern (one task depends on many)
    # Tasks 0, 1, 2 -> Task 3
    n8 = 4
    edges8 = [(0, 3), (1, 3), (2, 3)]
    time8 = [5, 3, 7, 2]
    result8 = min_total_time(n8, edges8, time8)
    expected8 = 9  # max(5, 3, 7) + 2 = 7 + 2 = 9
    assert result8 == expected8, f"Test 8 failed: expected {expected8}, got {result8}"
    print(f"Test 8 passed: {result8}")
    
    # Test 9: Empty graph (no tasks)
    n9 = 0
    edges9 = []
    time9 = []
    result9 = min_total_time(n9, edges9, time9)
    expected9 = 0
    assert result9 == expected9, f"Test 9 failed: expected {expected9}, got {result9}"
    print(f"Test 9 passed: {result9}")
    
    # Test 10: Long chain with varying times
    n10 = 5
    edges10 = [(0, 1), (1, 2), (2, 3), (3, 4)]
    time10 = [1, 10, 1, 10, 1]
    result10 = min_total_time(n10, edges10, time10)
    expected10 = 23  # 1 + 10 + 1 + 10 + 1 = 23
    assert result10 == expected10, f"Test 10 failed: expected {expected10}, got {result10}"
    print(f"Test 10 passed: {result10}")
    
    print("All tests passed!")


if __name__ == "__main__":
    test_min_total_time()
