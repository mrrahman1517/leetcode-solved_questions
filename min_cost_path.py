from heapq import heappush, heappop

def min_cost_path(grid):
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    while pq:
        d, r, c = heappop(pq)
        if d != dist[r][c]:
            continue
        if (r, c) == (m-1, n-1):
            return d
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1


def test_min_cost_path():
    """Basic tests for min_cost_path function"""
    
    # Test 1: Simple 2x2 grid
    grid1 = [
        [1, 3],
        [1, 5]
    ]
    result1 = min_cost_path(grid1)
    expected1 = 7  # 1 -> 1 -> 5 (path: (0,0) -> (1,0) -> (1,1))
    assert result1 == expected1, f"Test 1 failed: expected {expected1}, got {result1}"
    print(f"Test 1 passed: {result1}")
    
    # Test 2: 3x3 grid
    grid2 = [
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1]
    ]
    result2 = min_cost_path(grid2)
    expected2 = 5  # 1 -> 1 -> 1 -> 1 -> 1 (optimal path around the 2)
    assert result2 == expected2, f"Test 2 failed: expected {expected2}, got {result2}"
    print(f"Test 2 passed: {result2}")
    
    # Test 3: Single cell
    grid3 = [[5]]
    result3 = min_cost_path(grid3)
    expected3 = 5
    assert result3 == expected3, f"Test 3 failed: expected {expected3}, got {result3}"
    print(f"Test 3 passed: {result3}")
    
    # Test 4: Larger grid with varying costs
    grid4 = [
        [1, 4, 3],
        [1, 1, 1],
        [4, 2, 1]
    ]
    result4 = min_cost_path(grid4)
    expected4 = 5  # 1 -> 1 -> 1 -> 2 -> 1
    assert result4 == expected4, f"Test 4 failed: expected {expected4}, got {result4}"
    print(f"Test 4 passed: {result4}")
    
    # Test 5: Edge case with high costs
    grid5 = [
        [1, 100],
        [1, 1]
    ]
    result5 = min_cost_path(grid5)
    expected5 = 3  # 1 -> 1 -> 1
    assert result5 == expected5, f"Test 5 failed: expected {expected5}, got {result5}"
    print(f"Test 5 passed: {result5}")
    
    print("All tests passed!")


if __name__ == "__main__":
    test_min_cost_path()
