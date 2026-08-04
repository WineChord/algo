<div class="problem-anchor" id="problem-atcoder-abc469-d"></div>

??? problem "AtCoder ABC469 D · The Big Two"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_d?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 400 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1102（非官方，检索于 2026-08-05）。

    **题意**：给定多重无向边，统计无序点对 $\{x,y\}$，使每条边至少有一个端点属于该点对。

    **思路**：任取第一条边 $(a,b)$，任何合法二元顶点覆盖必含 $a$ 或 $b$。分别固定一个端点，所有尚未覆盖边又迫使第二个端点唯一；验证两个分支并去重。

    **复杂度**：时间 $O(N+M)$，额外空间 $O(N)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    bool covers(int x, int y, const vector<pair<int, int>>& edges) {
      for (auto [a, b] : edges) {
        if (a != x && b != x && a != y && b != y) {
          return false;
        }
      }
      return true;
    }
    long long countContaining(int fixed, int excluded, int n, const vector<pair<int, int>>& edges) {
      pair<int, int> uncovered{-1, -1};
      for (auto edge : edges) {
        if (edge.first != fixed && edge.second != fixed) {
          uncovered = edge;
          break;
        }
      }
      if (uncovered.first == -1) {
        return n - 1 - (excluded != -1 && excluded != fixed);
      }
      long long answer = 0;
      for (int other : {uncovered.first, uncovered.second}) {
        if (other != fixed && other != excluded && covers(fixed, other, edges)) {
          ++answer;
        }
      }
      return answer;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, m;
      cin >> n >> m;
      vector<pair<int, int>> edges(m);
      for (auto& [a, b] : edges) {
        cin >> a >> b;
      }
      int a = edges[0].first;
      int b = edges[0].second;
      long long answer = countContaining(a, -1, n, edges) + countContaining(b, a, n, edges);
      cout << answer << '\n';
    }
    ```
