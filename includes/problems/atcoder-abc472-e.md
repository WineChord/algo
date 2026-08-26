<div class="problem-anchor" id="problem-atcoder-abc472-e"></div>

??? problem "AtCoder ABC472 E: Odd Cycle"
    [打开原题 ↗](https://atcoder.jp/contests/abc472/tasks/abc472_e?lang=en){ .problem-source }

    **难度与分值**：官方分值 450；AtCoder 未给出单题官方难度；AtCoder Problems 社区估算难度 1029（2026-08-27）

    **题意**：给定简单连通无向图，输出任意一个顶点数为奇数的简单环；不存在时输出 `-1`。

    **思路**：在 BFS 生成树上按深度奇偶二染色。若所有边都跨颜色，图是二分图而无奇环；若找到同色边 $(u,v)$，树上 $u$ 到 $v$ 的路径有偶数条边，与该边合成奇环。用父指针和深度把两端同步提升到 LCA，即可安全恢复路径。

    **复杂度**：时间 $O(N+M)$，额外空间 $O(N+M)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    vector<int> buildCycle(int u, int v, const vector<int>& parent, const vector<int>& depth) {
      vector<int> left, right;
      int x = u, y = v;
      while (depth[x] > depth[y]) {
        left.push_back(x);
        x = parent[x];
      }
      while (depth[y] > depth[x]) {
        right.push_back(y);
        y = parent[y];
      }
      while (x != y) {
        left.push_back(x);
        right.push_back(y);
        x = parent[x];
        y = parent[y];
      }
      left.push_back(x);
      reverse(right.begin(), right.end());
      left.insert(left.end(), right.begin(), right.end());
      return left;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n, m;
        cin >> n >> m;
        vector<vector<int>> graph(n);
        for (int i = 0; i < m; ++i) {
          int u, v;
          cin >> u >> v;
          --u;
          --v;
          graph[u].push_back(v);
          graph[v].push_back(u);
        }
        vector<int> color(n, -1), parent(n, -1), depth(n);
        queue<int> pending;
        color[0] = 0;
        pending.push(0);
        vector<int> cycle;
        while (!pending.empty() && cycle.empty()) {
          int u = pending.front();
          pending.pop();
          for (int v : graph[u]) {
            if (color[v] == -1) {
              color[v] = color[u] ^ 1;
              parent[v] = u;
              depth[v] = depth[u] + 1;
              pending.push(v);
            } else if (color[v] == color[u]) {
              cycle = buildCycle(u, v, parent, depth);
              break;
            }
          }
        }
        if (cycle.empty()) {
          cout << -1 << '\n';
        } else {
          cout << cycle.size() << '\n';
          for (int v : cycle)
            cout << v + 1 << ' ';
          cout << '\n';
        }
      }
      return 0;
    }
    ```
