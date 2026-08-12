<div class="problem-anchor" id="problem-atcoder-arc226-a"></div>

??? problem "AtCoder ARC226 A · Meeting Division"
    [打开原题 ↗](https://atcoder.jp/contests/arc226/tasks/arc226_a?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 400 分，比赛 Rated Range 为 1200–2400；AtCoder Problems 社区估算难度未知（核对于 2026-08-12）。

    **题意**：给定端点恰为 1 到 2N 的 N 个会议区间，把会议分给两位负责人，使同一负责人负责的会议互不重叠，统计合法分配数。

    **思路**：按端点扫描活跃会议数；若某个开始端点出现时没有活跃会议，就开启区间图的一个新连通分量。题目保证同时活跃数不超过 2，每个分量恰有两种二染色。

    **复杂度**：时间 O(N)，空间 O(N)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    constexpr long long MOD = 998244353;
    long long modPow(long long base, int exponent) {
      long long result = 1;
      while (exponent > 0) {
        if (exponent & 1) result = result * base % MOD;
        base = base * base % MOD;
        exponent >>= 1;
      }
      return result;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<int> event(2 * n + 1);
      for (int i = 0; i < n; ++i) {
        int start, finish;
        cin >> start >> finish;
        event[start] = 1;
        event[finish] = -1;
      }
      int active = 0;
      int components = 0;
      for (int time = 1; time <= 2 * n; ++time) {
        if (event[time] == 1) {
          if (active == 0) ++components;
          ++active;
          if (active >= 3) {
            cout << 0 << '\n';
            return 0;
          }
        } else {
          --active;
        }
      }
      cout << modPow(2, components) << '\n';
    }
    ```
