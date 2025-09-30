"""
Demonstration of when the stale entry optimization in Dijkstra's algorithm matters.
This creates a scenario that will definitely show the difference.
"""

from heapq import heappush, heappop
from typing import List

def dijkstra_with_stale_check(grid: List[List[int]]) -> tuple[int, int, int]:
    """Dijkstra with stale entry optimization"""
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    
    processed = 0
    total_popped = 0
    
    while pq:
        d, r, c = heappop(pq)
        total_popped += 1
        
        # THE OPTIMIZATION: Skip stale entries
        if d != dist[r][c]:
            continue
            
        processed += 1
        
        if (r, c) == (m-1, n-1):
            return d, processed, total_popped
            
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1, processed, total_popped


def dijkstra_without_stale_check(grid: List[List[int]]) -> tuple[int, int, int]:
    """Dijkstra without stale entry optimization"""
    m, n = len(grid), len(grid[0])
    INF = 10**18
    dist = [[INF]*n for _ in range(m)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    
    processed = 0
    total_popped = 0
    
    while pq:
        d, r, c = heappop(pq)
        total_popped += 1
        processed += 1
        
        # NO OPTIMIZATION: Process all entries, even stale ones
        
        if (r, c) == (m-1, n-1):
            return d, processed, total_popped
            
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heappush(pq, (nd, nr, nc))
    return -1, processed, total_popped


def create_stale_entry_grid():
    """Create a grid designed to generate many stale entries"""
    # This grid has a specific pattern:
    # - Initial paths go through expensive cells
    # - Later, much cheaper paths are discovered
    # - This causes many entries in the queue to become stale
    
    size = 15
    grid = []
    
    for i in range(size):
        row = []
        for j in range(size):
            if i == 0 and j == 0:
                cost = 1  # Start
            elif i == size-1 and j == size-1:
                cost = 1  # End
            elif i == size // 2:  # Middle row - very cheap path
                cost = 1
            elif j == size // 2:  # Middle column - very cheap path
                cost = 1
            elif i < size // 2 and j < size // 2:  # Top-left quadrant - expensive
                cost = 100
            elif i < size // 2 and j > size // 2:  # Top-right quadrant - expensive
                cost = 100
            elif i > size // 2 and j < size // 2:  # Bottom-left quadrant - expensive
                cost = 100
            elif i > size // 2 and j > size // 2:  # Bottom-right quadrant - expensive
                cost = 100
            else:
                cost = 50  # Border areas
            
            row.append(cost)
        grid.append(row)
    
    return grid


def create_worse_grid():
    """Create an even worse grid for stale entries"""
    # This creates a "spider web" pattern where:
    # 1. There are many expensive paths initially explored
    # 2. Cheap "shortcut" paths are discovered later
    # 3. This invalidates many queue entries
    
    size = 20
    grid = [[1000 for _ in range(size)] for _ in range(size)]  # Start with all expensive
    
    # Add cheap paths that create shortcuts
    center = size // 2
    
    # Horizontal cheap path through middle
    for j in range(size):
        grid[center][j] = 1
    
    # Vertical cheap path through middle  
    for i in range(size):
        grid[i][center] = 1
    
    # Diagonal cheap paths
    for i in range(size):
        if i < size:
            grid[i][i] = 1  # Main diagonal
            if size - 1 - i >= 0:
                grid[i][size - 1 - i] = 1  # Anti-diagonal
    
    # Start and end
    grid[0][0] = 1
    grid[size-1][size-1] = 1
    
    # Add some random cheap cells to create more alternatives
    import random
    random.seed(42)
    for _ in range(size * 2):
        i, j = random.randint(0, size-1), random.randint(0, size-1)
        grid[i][j] = random.randint(1, 5)
    
    return grid


def main():
    print("=== Demonstrating Stale Entry Optimization ===\n")
    
    # Test 1: Basic grid designed for stale entries
    print("Test 1: Basic grid with cheap middle paths")
    grid1 = create_stale_entry_grid()
    
    result1_opt, processed1_opt, total1_opt = dijkstra_with_stale_check(grid1)
    result1_no_opt, processed1_no_opt, total1_no_opt = dijkstra_without_stale_check(grid1)
    
    print(f"With optimization:    Result={result1_opt}, Processed={processed1_opt}, Total popped={total1_opt}")
    print(f"Without optimization: Result={result1_no_opt}, Processed={processed1_no_opt}, Total popped={total1_no_opt}")
    print(f"Stale entries saved: {processed1_no_opt - processed1_opt}")
    print()
    
    # Test 2: Worse grid
    print("Test 2: Spider web grid with many shortcuts")
    grid2 = create_worse_grid()
    
    result2_opt, processed2_opt, total2_opt = dijkstra_with_stale_check(grid2)
    result2_no_opt, processed2_no_opt, total2_no_opt = dijkstra_without_stale_check(grid2)
    
    print(f"With optimization:    Result={result2_opt}, Processed={processed2_opt}, Total popped={total2_opt}")
    print(f"Without optimization: Result={result2_no_opt}, Processed={processed2_no_opt}, Total popped={total2_no_opt}")
    print(f"Stale entries saved: {processed2_no_opt - processed2_opt}")
    print()
    
    if processed1_no_opt > processed1_opt or processed2_no_opt > processed2_opt:
        print("SUCCESS: The optimization makes a difference!")
    else:
        print("Interesting: Even these grids don't generate many stale entries in this implementation")


if __name__ == "__main__":
    main()