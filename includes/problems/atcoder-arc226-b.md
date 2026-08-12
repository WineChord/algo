<div class="problem-anchor" id="problem-atcoder-arc226-b"></div>

??? problem "AtCoder ARC226 B · Bin-ary Packing"
    [打开原题 ↗](https://atcoder.jp/contests/arc226/tasks/arc226_b?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 500 分，官方未标注难度；AtCoder Problems 社区估算难度为 1207（核对于 2026-08-13）。

    **题意**：有 N 个袋子，重量 2^i 的包裹有 A_i 个；把全部包裹分配到袋子中，最小化最重袋子的重量。

    **思路**：对每个二进制尺度 2^k，统计所有不小于该尺度的包裹折算出的单位数 U_k。任何袋容量都至少是 2^k·ceil(U_k/N)；二进制整除链又保证全部尺度下界同时充分，故取最大值。

    **复杂度**：每组时间 O(M)，空间 O(M)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        long long n;
        int m;
        cin >> n >> m;
        vector<long long> count(m);
        for (long long& x : count) cin >> x;
        long long units = 0;
        long long answer = 0;
        for (int i = m - 1; i >= 0; --i) {
          units = units * 2 + count[i];
          long long bags = (units + n - 1) / n;
          answer = max(answer, bags * (1LL << i));
        }
        cout << answer << '\n';
      }
    }
    ```
