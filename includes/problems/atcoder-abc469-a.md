<div class="problem-anchor" id="problem-atcoder-abc469-a"></div>

??? problem "AtCoder ABC469 A · Train Car"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_a?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 100 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 -1026（非官方，检索于 2026-08-02）。

    **题意**：一列火车有 $N$ 节车厢，求从前数第 $K$ 节车厢从后数是第几节。

    **思路**：同一位置的两端一基编号之和恒为 $N+1$，答案直接是 $N-K+1$。

    **复杂度**：时间 $O(1)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, k;
      cin >> n >> k;
      cout << n - k + 1 << '\n';
    }
    ```
