<div class="problem-anchor" id="problem-codeforces-2247-f"></div>

??? problem "CF Round 1111 · Div.2 F · Paths on a Grid (2247F)"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/F){ .problem-source }

    **难度与分值**：Codeforces 官方 3500 分；官方 API 暂未给出 problem rating，标签为 `data structures`、`dp`、`hashing`。

    **题意**：在向右或向下的自由格路径中，把具有完全相同完整路径集合的格子归为一类，统计各等价类的非空子集总数。

    **思路**：先把无完整路径经过的格子合并为空签名类；对活跃 DAG 分别构造起点支配树与终点后支配树，用互为直接父子的边识别相同路径签名，再以并查集合并。

    **复杂度**：设 $V=nm$，时间 $O(V\log V)$，峰值额外空间 $O(V\log V)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    const int mod = 998244353;
    const int levels = 21;
    struct DisjointSet {
      vector<int> parent;
      vector<int> size;
      explicit DisjointSet(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
      }
      int find(int value) {
        while (value != parent[value]) {
          parent[value] = parent[parent[value]];
          value = parent[value];
        }
        return value;
      }
      void unite(int first, int second) {
        first = find(first);
        second = find(second);
        if (first == second) {
          return;
        }
        if (size[first] < size[second]) {
          swap(first, second);
        }
        parent[second] = first;
        size[first] += size[second];
      }
    };
    struct DominatorTree {
      int rows;
      int columns;
      const vector<char>& active;
      vector<array<int, levels>> ancestor;
      vector<int> depth;
      vector<int> parent;
      DominatorTree(int rows, int columns, const vector<char>& active)
          : rows(rows),
            columns(columns),
            active(active),
            ancestor(rows * columns),
            depth(rows * columns),
            parent(rows * columns, -1) {
      }
      int lca(int first, int second) {
        if (depth[first] < depth[second]) {
          swap(first, second);
        }
        int difference = depth[first] - depth[second];
        for (int bit = 0; bit < levels; ++bit) {
          if (difference >> bit & 1) {
            first = ancestor[first][bit];
          }
        }
        if (first == second) {
          return first;
        }
        for (int bit = levels - 1; bit >= 0; --bit) {
          if (ancestor[first][bit] != ancestor[second][bit]) {
            first = ancestor[first][bit];
            second = ancestor[second][bit];
          }
        }
        return ancestor[first][0];
      }
      void add(int node, int directParent) {
        parent[node] = directParent;
        depth[node] = node == directParent ? 0 : depth[directParent] + 1;
        ancestor[node][0] = directParent;
        for (int bit = 1; bit < levels; ++bit) {
          ancestor[node][bit] = ancestor[ancestor[node][bit - 1]][bit - 1];
        }
      }
      vector<int> buildFromStart() {
        add(0, 0);
        for (int row = 0; row < rows; ++row) {
          for (int column = 0; column < columns; ++column) {
            int node = row * columns + column;
            if (!active[node] || node == 0) {
              continue;
            }
            int up = row > 0 && active[node - columns] ? node - columns : -1;
            int left = column > 0 && active[node - 1] ? node - 1 : -1;
            int directParent = up == -1 ? left : left == -1 ? up : lca(up, left);
            add(node, directParent);
          }
        }
        return std::move(parent);
      }
      vector<int> buildFromFinish() {
        int finish = rows * columns - 1;
        add(finish, finish);
        for (int row = rows - 1; row >= 0; --row) {
          for (int column = columns - 1; column >= 0; --column) {
            int node = row * columns + column;
            if (!active[node] || node == finish) {
              continue;
            }
            int down = row + 1 < rows && active[node + columns] ? node + columns : -1;
            int right = column + 1 < columns && active[node + 1] ? node + 1 : -1;
            int directParent = down == -1 ? right : right == -1 ? down : lca(down, right);
            add(node, directParent);
          }
        }
        return std::move(parent);
      }
    };
    void solve() {
      int rows, columns;
      cin >> rows >> columns;
      vector<string> grid(rows);
      for (string& row : grid) {
        cin >> row;
      }
      int cells = rows * columns;
      vector<char> fromStart(cells), toFinish(cells), active(cells);
      for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
          int node = row * columns + column;
          fromStart[node] = grid[row][column] == '1' &&
              (node == 0 || (row > 0 && fromStart[node - columns]) ||
                  (column > 0 && fromStart[node - 1]));
        }
      }
      for (int row = rows - 1; row >= 0; --row) {
        for (int column = columns - 1; column >= 0; --column) {
          int node = row * columns + column;
          toFinish[node] = grid[row][column] == '1' &&
              (node == cells - 1 || (row + 1 < rows && toFinish[node + columns]) ||
                  (column + 1 < columns && toFinish[node + 1]));
          active[node] = fromStart[node] && toFinish[node];
        }
      }
      int activeCount = count(active.begin(), active.end(), 1);
      vector<long long> powerOfTwo(cells + 1, 1);
      for (int i = 1; i <= cells; ++i) {
        powerOfTwo[i] = powerOfTwo[i - 1] * 2 % mod;
      }
      if (activeCount == 0) {
        cout << (powerOfTwo[cells] - 1 + mod) % mod << '\n';
        return;
      }
      vector<int> startParent = DominatorTree(rows, columns, active).buildFromStart();
      vector<int> finishParent = DominatorTree(rows, columns, active).buildFromFinish();
      DisjointSet dsu(cells);
      for (int node = 0; node < cells; ++node) {
        if (!active[node]) {
          continue;
        }
        int before = startParent[node];
        if (before != node && finishParent[before] == node) {
          dsu.unite(before, node);
        }
      }
      vector<int> componentSize(cells);
      for (int node = 0; node < cells; ++node) {
        if (active[node]) {
          ++componentSize[dsu.find(node)];
        }
      }
      long long answer = 0;
      int inactive = cells - activeCount;
      if (inactive > 0) {
        answer = powerOfTwo[inactive] - 1;
      }
      for (int size : componentSize) {
        if (size > 0) {
          answer += powerOfTwo[size] - 1;
          answer %= mod;
        }
      }
      cout << answer << '\n';
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCases;
      cin >> testCases;
      while (testCases--) {
        solve();
      }
    }
    ```
