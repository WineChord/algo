<div class="problem-anchor" id="problem-atcoder-abc468-e"></div>

??? problem "AtCoder ABC468 E · Sum of Average"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_e?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 450 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1038（非官方，检索于 2026-07-30）。

    **题意**：求所有非空连续子数组算术平均数之和，并对 $998244353$ 取模。

    **思路**：交换求和次序，统计每个 $A_i$ 在所有包含它的子数组平均数中的总系数。预处理模逆元与调和前缀后，相邻位置的系数只差两个调和数，可在线性扫描中递推。

    **复杂度**：时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using int64 = long long;
    constexpr int64 MOD = 998244353;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<int64> a(n + 1), inverse(n + 1), harmonic(n + 1);
      for (int i = 1; i <= n; ++i) {
        cin >> a[i];
      }
      inverse[1] = 1;
      for (int i = 2; i <= n; ++i) {
        inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
      }
      for (int i = 1; i <= n; ++i) {
        harmonic[i] = (harmonic[i - 1] + inverse[i]) % MOD;
      }
      int64 coefficient = 0;
      int64 answer = 0;
      for (int i = 1; i <= n; ++i) {
        coefficient = (coefficient + harmonic[n - i + 1] - harmonic[i - 1] + MOD) % MOD;
        answer = (answer + a[i] * coefficient) % MOD;
      }
      cout << answer << '\n';
    }
    ```
