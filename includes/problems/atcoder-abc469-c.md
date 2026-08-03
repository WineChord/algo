<div class="problem-anchor" id="problem-atcoder-abc469-c"></div>

??? problem "AtCoder ABC469 C · Cantrip"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_c?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 300 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 475（非官方，检索于 2026-08-04）。

    **题意**：字符串中的 `o` 表示行动前不消耗糖，`x` 表示行动前必须拿到一袋糖；对每个行动次数 $k$，求按顺序完成前 $k$ 次行动所需取到的最小袋子数。

    **思路**：第 $k$ 次行动若对应 `x`，至少要取到该位置；若对应 `o`，已有前缀资源足够。因此答案是第 $k$ 个 `x` 的位置，不存在时为总长度 $N$。

    **复杂度**：时间 $O(N)$，额外空间 $O(N)$；若流式输出可做到 $O(1)$ 额外空间。

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
      vector<int> misses;
      for (int i = 0; i < n; ++i) {
        if (s[i] == 'x') {
          misses.push_back(i + 1);
        }
      }
      for (int k = 1; k <= n; ++k) {
        cout << (k <= static_cast<int>(misses.size()) ? misses[k - 1] : n) << '\n';
      }
    }
    ```
