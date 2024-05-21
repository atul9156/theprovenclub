from typing import List

def get_island_connectivity(grid: List[List[int]]):
    # do DFS and find the connected componenets
    # While doing DFS, find the size of the largest island that get's formed
    def should_visit(ro: int, col: int) -> bool:
        # are ro and col in correct bounds?
        # is this already visited?
        # is this even worth visiting?
        if ro < 0 or ro >= m or col < 0 or col >= n:
            return False
        if visited[ro][col] == True:
            return False
        if grid[ro][col] != "1":
            return False
        return True

    def dfs(ro: int, col) -> int:
        # Returns the size of island reachable from (ro, col)
        visited[ro][col] = True
        directions = [(ro, col - 1), (ro, col + 1), (ro - 1, col), (ro + 1, col)]
        island_size = 1
        for x, y in directions:
            if should_visit(x, y):
                island_size += dfs(x, y)
        return island_size

    if len(grid) == 0:
        return (0, 0)
    n_count = 0 # number of connected components
    max_size = -1 * float("inf")
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if should_visit(i, j):
                n_count += 1
                temp = dfs(i, j)
                max_size = max(temp, max_size)
    return n_count, max_size


grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]

islands, max_size = get_island_connectivity(grid=grid)
print("Number of Islands:", islands)
print("Size of largest island:", max_size)