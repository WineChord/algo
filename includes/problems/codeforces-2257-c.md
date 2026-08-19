<div class="problem-anchor" id="problem-codeforces-2257-c"></div>

??? problem "Codeforces 2257C: Spying on the Beaver"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/C?locale=en){ .problem-source }

    **难度与分值**：官方分值 1250；官方 rating 未给出；官方标签 `dfs and similar`、`dsu`、`graphs`、`trees`（2026-08-20）

    **题意**：在一棵以 1 为根的树上选若干父边安装摄像头。坝点沿根路径看到的摄像头序列必须两两不同；求最少摄像头数及任一最优方案。

    **思路**：删去 $k$ 条摄像头边只会得到 $k+1$ 个连通块，所以区分 $m$ 个坝点至少需要 $m-1$ 条边。保留一个深度最小的坝点，对其余每个坝点切父边；每个被切坝点独占一块，根块只剩保留点，恰好达到下界。

    **复杂度**：时间 $O(n+m)$，额外空间 $O(n+m)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        int n;
        cin >> n;
        vector<int> depth(n + 1);
        for (int vertex = 2; vertex <= n; ++vertex) {
          int parent;
          cin >> parent;
          depth[vertex] = depth[parent] + 1;
        }
        int m;
        cin >> m;
        vector<int> dams(m);
        for (int& vertex : dams) cin >> vertex;
        int keep = *min_element(dams.begin(), dams.end(), [&](int a, int b) {
          return depth[a] < depth[b];
        });
        cout << m - 1;
        for (int vertex : dams) {
          if (vertex != keep) cout << ' ' << vertex;
        }
        cout << '\n';
      }
      return 0;
    }
    ```
