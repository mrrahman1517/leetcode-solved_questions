from collections import defaultdict, deque
from typing import List

def possibleBipartition(n: int, dislikes: List[List[int]]) -> bool:
    if n == 1:
        return True
    graph = defaultdict(list)
    for (u, v) in dislikes:
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * (n + 1)
    for person in range(1, n + 1):
        if color[person] == -1:
            queue = deque([person])
            color[person] = 0

            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if color[v] == color[u]:
                        return False
                    if color[v] == -1:
                        queue.append(v)
                        color[v] = 1 - color[u]
    return True


if __name__ == "__main__":
    # Test cases
    tests = [
        # (n, dislikes, expected)
        (4, [[1,2],[1,3],[2,4]], True),
        (3, [[1,2],[1,3],[2,3]], False),
        (5, [[1,2],[2,3],[3,4],[4,5],[1,5]], False),
        (1, [], True),
        (2, [[1,2]], True),
        (3, [], True),
    ]
    for i, (n, dislikes, expected) in enumerate(tests, 1):
        result = possibleBipartition(n, dislikes)
        print(f"Test case {i}: possibleBipartition({n}, {dislikes}) = {result} (expected: {expected}) -> {'PASS' if result == expected else 'FAIL'}")
