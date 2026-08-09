<div class="problem-anchor" id="problem-atcoder-abc469-f"></div>

??? problem "AtCoder ABC469 F · GCD Maximum Spanning Tree"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_f?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 500 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1567（非官方，检索于 2026-08-09）。

    **题意**：给定严格递增正整数，把每个数视为顶点、两点边权为它们的最大公约数，求完全图的最大生成树权值和。

    **思路**：按公约数从大到小枚举其倍数；同一倍数桶中用一个锚点合并尚未连通的 DSU 分量，每次成功合并贡献当前公约数，等价于降序 Kruskal。

    **复杂度**：设最大值为 $M$，时间 $O(M\log M\,\alpha(N))$，空间 $O(M+N)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct DSU {
      vector<int> parent, size;
      explicit DSU(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
      }
      int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
      }
      bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) {
          return false;
        }
        if (size[a] < size[b]) {
          swap(a, b);
        }
        parent[b] = a;
        size[a] += size[b];
        return true;
      }
    };
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<int> a(n);
      int maximum = 0;
      for (int& x : a) {
        cin >> x;
        maximum = max(maximum, x);
      }
      vector<int> vertexAt(maximum + 1, -1);
      for (int i = 0; i < n; ++i) {
        vertexAt[a[i]] = i;
      }
      DSU dsu(n);
      long long answer = 0;
      int chosenEdges = 0;
      for (int divisor = maximum; divisor >= 1; --divisor) {
        int anchor = -1;
        for (int multiple = divisor; multiple <= maximum; multiple += divisor) {
          int vertex = vertexAt[multiple];
          if (vertex == -1) {
            continue;
          }
          if (anchor == -1) {
            anchor = vertex;
          } else if (dsu.unite(anchor, vertex)) {
            answer += divisor;
            ++chosenEdges;
          }
        }
      }
      assert(chosenEdges == n - 1);
      cout << answer << '\n';
    }
    ```
