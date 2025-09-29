#include <queue>
using namespace std;

class Solution {
public:
    // use top sort
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        if (numCourses == 1) {
            return true;
        }
        // create adj list rep of graph
        vector<vector<int>> graph(numCourses);
        for (int u = 0; u < numCourses; u++) {
            graph[u] = vector<int>();
        }
        // count the node in degrees
        vector<int> in_degree(numCourses);
        for (auto& edge: prerequisites) {
            in_degree[edge[0]]++;
            graph[edge[1]].push_back(edge[0]);
        }
        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (in_degree[i] == 0) {
                q.push(i);
            }
        }   
        // if no indegree 0 node to start with, then fail
        if (q.empty()) {
            return false;
        }
        // otherwise atleast one 0 indegree node, start peeling
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto& v: graph[u]) {
                in_degree[v]--;  // guarantee in degree of v > 0 since the edge uv exists
                if (in_degree[v] == 0) {
                    q.push(v);
                }
            }
        }
        // if some nodes still have positive indegree, fail
        for (int n = 0; n < numCourses; n++) {
            if (in_degree[n] > 0) {
                return false;
            }
        }
        return true;
    }
};
