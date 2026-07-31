<div class="problem-anchor" id="problem-atcoder-abc468-g"></div>

??? problem "AtCoder ABC468 G · Restricted Permutation"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_g?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 550 分；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1975（非官方，检索于 2026-08-01）。

    **题意**：给定由 `o` 与 `x` 组成的长度为 $N$ 的模式，统计满足“值集 $\{1,\ldots,k\}$ 在排列中连续，当且仅当第 $k$ 位为 `o`”的排列数。

    **思路**：先递推只有首尾值集连续的不可再分块排列数 $d_n$。相邻两个 `o` 之间的选择在收缩既有块后互相独立，答案是对应 $d$ 值的乘积。

    **复杂度**：时间 $O(N^2)$，额外空间 $O(N)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    const long long mod = 998244353;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      string s;
      cin >> n >> s;
      if (s.front() != 'o' || s.back() != 'o') {
        cout << 0 << '\n';
        return 0;
      }
      vector<long long> factorial(n + 1, 1), primitive(n + 1);
      for (int i = 1; i <= n; ++i) {
        factorial[i] = factorial[i - 1] * i % mod;
      }
      for (int length = 2; length <= n; ++length) {
        primitive[length] = factorial[length];
        for (int firstBlock = 2; firstBlock < length; ++firstBlock) {
          primitive[length] -= primitive[firstBlock] * factorial[length - firstBlock + 1] % mod;
          if (primitive[length] < 0) {
            primitive[length] += mod;
          }
        }
      }
      long long answer = 1;
      int previous = 0;
      for (int index = 1; index < n; ++index) {
        if (s[index] == 'o') {
          answer = answer * primitive[index - previous + 1] % mod;
          previous = index;
        }
      }
      cout << answer << '\n';
    }
    ```
