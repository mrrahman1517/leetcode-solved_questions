
#Minimum-cost path on a weighted grid.
#You have grid[m][n] non-negative costs. Move 4-directions. Return min cost from (0,0) to (m-1,n-1) including both cells’ costs.

#Solution (O(mn log mn))

from heapq import heappush, heappop
from typing import List
import math

def min_cost_path(grid: List[List[int]]) -> int:
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


def test_min_cost_path() -> None:
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


def min_cost_path_unoptimized(grid: List[List[int]]) -> int:
    """Version without the stale entry check for comparison"""
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    processed_count = 0  # Count how many entries we process
    
    while pq:
        d, r, c = heappop(pq)
        processed_count += 1
        # No stale entry check here!
        
        if (r, c) == (m-1, n-1):
            print(f"Unoptimized: Processed {processed_count} entries")
            return d
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1


def min_cost_path_optimized(grid: List[List[int]]) -> int:
    """Version with the stale entry check for comparison"""
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    processed_count = 0  # Count how many entries we process
    
    while pq:
        d, r, c = heappop(pq)
        if d != dist[r][c]:  # Skip stale entries
            continue
        processed_count += 1
        
        if (r, c) == (m-1, n-1):
            print(f"Optimized: Processed {processed_count} entries")
            return d
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1


def compare_performance():
    """Compare performance between optimized and unoptimized versions"""
    
    # Create a specific pattern that WILL cause many stale entries
    print("=== Complex Grid Designed to Trigger Stale Entries ===")
    
    # This pattern creates a scenario where the algorithm will:
    # 1. Initially find expensive paths
    # 2. Later discover much cheaper alternatives
    # 3. Generate many stale entries in the priority queue
    
    size = 20
    complex_grid = []
    
    for i in range(size):
        row = []
        for j in range(size):
            # Create a pattern with "valleys" of low cost surrounded by high cost
            # This forces the algorithm to initially explore expensive paths,
            # then later find cheaper alternatives, creating stale entries
            
            if i == 0 or j == 0:  # Top and left edges - moderate cost
                cost = 10
            elif i == size-1 or j == size-1:  # Bottom and right edges - moderate cost  
                cost = 10
            elif (i + j) % 7 == 0:  # Diagonal "valleys" of very low cost
                cost = 1
            elif abs(i - j) < 2:  # Near main diagonal - low cost
                cost = 2
            elif (i % 4 == 0) or (j % 4 == 0):  # Grid lines - medium cost
                cost = 15
            else:  # Everything else - high cost
                cost = 50 + (i * j) % 30
            
            row.append(cost)
        complex_grid.append(row)
    
    # Add some strategic low-cost paths that will be discovered late
    for i in range(1, size-1):
        if i % 5 == 0:
            complex_grid[i][size//2] = 1  # Vertical low-cost corridor
            complex_grid[size//2][i] = 1  # Horizontal low-cost corridor
    
    print(f"Grid size: {size}x{size}")
    print("This grid has expensive initial paths but cheaper alternatives discovered later...")
    print()
    
    result1 = min_cost_path_unoptimized(complex_grid)
    result2 = min_cost_path_optimized(complex_grid)
    print(f"Both results: {result1} == {result2}")
    print()
    
    # If we still don't see a difference, let's create an extreme case
    print("=== Extreme Case: Dense Graph with Many Path Updates ===")
    
    extreme_grid = []
    size = 30
    
    for i in range(size):
        row = []
        for j in range(size):
            # This creates a very complex cost landscape where:
            # - Many cells will be reached multiple times with different costs
            # - The algorithm will constantly find better paths
            base_cost = 1
            
            # Add complexity layers
            distance_factor = ((i - size//2)**2 + (j - size//2)**2) // 10
            wave_factor = int(10 * abs(math.sin(i * 0.5) * math.cos(j * 0.5)))
            grid_factor = 5 if (i % 3 == 0 and j % 3 == 0) else 0
            
            cost = base_cost + distance_factor + wave_factor + grid_factor
            cost = max(1, cost)  # Ensure positive cost
            row.append(cost)
        extreme_grid.append(row)
    
    print(f"Grid size: {size}x{size}")
    
    result3 = min_cost_path_unoptimized(extreme_grid)
    result4 = min_cost_path_optimized(extreme_grid)
    print(f"Both results: {result3} == {result4}")
    print()


def min_cost_path_unoptimized_with_tracking(grid: List[List[int]]) -> int:
    """Version without the stale entry check, with detailed tracking"""
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    processed_count = 0
    skipped_count = 0
    
    while pq:
        d, r, c = heappop(pq)
        processed_count += 1
        
        # Check if this would be skipped in optimized version
        if d != dist[r][c]:
            skipped_count += 1
            print(f"  Would skip: ({r},{c}) with distance {d}, current best: {dist[r][c]}")
        
        if (r, c) == (m-1, n-1):
            print(f"Unoptimized: Processed {processed_count} entries, {skipped_count} were stale")
            return d
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1


def demonstrate_stale_entries():
    """Create a specific example that will definitely show stale entries"""
    print("=== Demonstration of Stale Entry Optimization ===")
    
    # Create a small but strategic grid that will force path updates
    demo_grid = [
        [1,   100, 1,   1],
        [1,   100, 100, 1], 
        [1,   1,   1,   1],
        [100, 100, 100, 1]
    ]
    
    print("Grid layout:")
    for row in demo_grid:
        print(row)
    print()
    
    print("Unoptimized version (showing what would be skipped):")
    result1 = min_cost_path_unoptimized_with_tracking(demo_grid)
    print()
    
    print("Optimized version:")
    result2 = min_cost_path_optimized(demo_grid)
    print()
    
    print(f"Both results: {result1} == {result2}")
    print()
    
    # An even more extreme example
    print("=== More Extreme Example ===")
    extreme_demo = [
        [1,  50, 50, 50, 1],
        [1,  50, 50, 50, 1],
        [1,  1,  1,  1,  1],
        [50, 50, 50, 50, 1],
        [50, 50, 50, 50, 1]
    ]
    
    print("Grid layout:")
    for row in extreme_demo:
        print(row)
    print()
    
    print("Unoptimized version (showing what would be skipped):")
    result3 = min_cost_path_unoptimized_with_tracking(extreme_demo)
    print()
    
    print("Optimized version:")
    result4 = min_cost_path_optimized(extreme_demo)
    print()
    
    print(f"Both results: {result3} == {result4}")


if __name__ == "__main__":
    demonstrate_stale_entries()
    print("\n" + "="*50 + "\n")
    compare_performance()
    print("\n" + "="*50 + "\n")
    test_min_cost_path()
