<div class="problem-anchor" id="problem-codeforces-2247-e"></div>

??? problem "CF Round 1111 · Div.2 E · Build a Tree (2247E)"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/E){ .problem-source }

    **难度与分值**：Codeforces 官方 3000 分；官方 API 暂未给出 problem rating，标签为 `constructive algorithms`、`trees`、`two pointers`。

    **题意**：构造一棵树，使从根出发按固定访问顺序累加的路径距离恰为给定值。

    **思路**：可行值必须为偶数且落在 $[2(n-1),\lfloor n^2/2\rfloor]$。把奇偶编号分组并逐步调节一侧深度，可以每次把总和增加 2，连续覆盖完整可行区间。

    **复杂度**：每组测试时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using int64 = long long;
    void buildGroup(const vector<int>& vertices, int64& extra, vector<pair<int, int>>& edges) {
      vector<int> path;
      for (int vertex : vertices) {
        int depth = min<int64>(extra, path.size());
        edges.push_back({depth == 0 ? 1 : path[depth - 1], vertex});
        extra -= depth;
        if (depth == static_cast<int>(path.size())) {
          path.push_back(vertex);
        }
      }
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        int64 k;
        cin >> n >> k;
        int64 minimum = 2LL * (n - 1);
        int64 maximum = 1LL * n * n / 2;
        if (k % 2 || k < minimum || k > maximum) {
          cout << -1 << '\n';
          continue;
        }
        vector<int> even;
        vector<int> odd;
        for (int vertex = 2; vertex <= n; ++vertex) {
          (vertex % 2 == 0 ? even : odd).push_back(vertex);
        }
        int64 extra = k / 2 - (n - 1);
        vector<pair<int, int>> edges;
        buildGroup(even, extra, edges);
        buildGroup(odd, extra, edges);
        for (auto [u, v] : edges) {
          cout << u << ' ' << v << '\n';
        }
      }
    }
    ```
