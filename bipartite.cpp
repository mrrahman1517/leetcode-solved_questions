#include <iostream>
#include <vector>
#include <queue>
#include <cassert>

using namespace std;


bool possibleBipartition(int n, vector<vector<int>>& dislikes) {
    if (n == 1) {
        return true;
    }
    // create graph
    vector<vector<int>> graph(n+1);
    for (int u = 1; u <= n; u++) {
        graph[u] = vector<int>();
    }
    for (auto& edge: dislikes) {
        graph[edge[0]].push_back(edge[1]);
        graph[edge[1]].push_back(edge[0]);
    }
    // 2 coloring bfs
    // keep a vector to track node colors (even and odd)
    vector<int> color(n+1,-1);  // 0 = even, 1 = odd
    queue<int> q;
    for (int u = 1; u <= n; u++) {
        if (color[u] == -1) {
            q.push(u);
            color[u] = 0;
        }    
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto& v: graph[u]) {
                if (color[v] == -1) {
                    q.push(v);
                    color[v] = 1 - color[u];
                }
                else if (color[v] == color[u]) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main() {
    // Test case 1: Simple bipartite
    int n1 = 4;
    vector<vector<int>> dislikes1 = {{1,2},{1,3},{2,4}};
    assert(possibleBipartition(n1, dislikes1) == true);

    // Test case 2: Not bipartite (odd cycle)
    int n2 = 3;
    vector<vector<int>> dislikes2 = {{1,2},{1,3},{2,3}};
    assert(possibleBipartition(n2, dislikes2) == false);

    // Test case 3: No dislikes
    int n3 = 5;
    vector<vector<int>> dislikes3 = {};
    assert(possibleBipartition(n3, dislikes3) == true);

    // Test case 4: Single node
    int n4 = 1;
    vector<vector<int>> dislikes4 = {};
    assert(possibleBipartition(n4, dislikes4) == true);

    // Test case 5: Disconnected graph, all bipartite
    int n5 = 5;
    vector<vector<int>> dislikes5 = {{1,2},{3,4}};
    assert(possibleBipartition(n5, dislikes5) == true);

    // Test case 6: Disconnected, one component not bipartite
    int n6 = 6;
    vector<vector<int>> dislikes6 = {{1,2},{2,3},{3,1},{4,5}};
    assert(possibleBipartition(n6, dislikes6) == false);

    cout << "All test cases passed!\n";
    return 0;
}