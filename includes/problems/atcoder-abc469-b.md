<div class="problem-anchor" id="problem-atcoder-abc469-b"></div>

??? problem "AtCoder ABC469 B · Isolated Seats"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_b?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 200 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 -576（非官方，检索于 2026-08-03）。

    **题意**：给定一排空座与已占座，统计左右相邻座位都为空且自身也为空的座位数；边界外视为已占座。

    **思路**：在原串两端补已占座哨兵，把首尾与内部统一为长度 3 的窗口；恰为 `...` 的窗口中心贡献 1。

    **复杂度**：时间 $O(N)$，额外空间 $O(N)$；也可直接分支扫描做到 $O(1)$ 额外空间。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      string s;
      cin >> n >> s;
      string padded = "x" + s + "x";
      int answer = 0;
      for (int i = 1; i <= n; ++i) {
        if (padded[i - 1] == 'x' && padded[i] == 'x' && padded[i + 1] == 'x') {
          ++answer;
        }
      }
      cout << answer << '\n';
    }
    ```
