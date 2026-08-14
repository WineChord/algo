<div class="problem-anchor" id="problem-codeforces-2256-d"></div>

??? problem "CF Round 1116 · Div.1 B / Div.2 D · A Ribbon for Tomorrow"
    [打开原题 ↗](https://codeforces.com/contest/2256/problem/D){ .problem-source }

    **难度与分值**：官方 rating 均为 1600；Div.1 B / Div.2 D 官方分值分别为 1000 / 2000，标签分别为 combinatorics、math / math（核对于 2026-08-15）。

    **题意**：二进制串中可反复反转当前首尾字符相同的任意子串，求从初始串能够到达的不同字符串数量，答案对 998244353 取模。

    **思路**：操作保持首尾字符、0/1 数量与相邻变化数，等价于保持两种颜色各自的 run 数；相邻同色 run 之间可以逐单位搬运长度，故两种颜色的正整数 run 长组成可独立任意重分配。

    **复杂度**：预处理阶乘 O(max n)，每组扫描 O(n)，空间 O(max n)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    const int MOD = 998244353;
    long long power(long long value, int exponent) {
      long long result = 1;
      while (exponent > 0) {
        if (exponent & 1) result = result * value % MOD;
        value = value * value % MOD;
        exponent >>= 1;
      }
      return result;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testsCount;
      cin >> testsCount;
      vector<pair<int, string>> tests(testsCount);
      int maximum = 0;
      for (auto& [n, s] : tests) {
        cin >> n >> s;
        maximum = max(maximum, n);
      }
      vector<long long> factorial(maximum + 1, 1);
      vector<long long> inverseFactorial(maximum + 1, 1);
      for (int i = 1; i <= maximum; ++i) {
        factorial[i] = factorial[i - 1] * i % MOD;
      }
      inverseFactorial[maximum] = power(factorial[maximum], MOD - 2);
      for (int i = maximum; i > 0; --i) {
        inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
      }
      auto combination = [&](int n, int k) -> long long {
        if (n < 0 || k < 0 || k > n) return 0;
        return factorial[n] * inverseFactorial[k] % MOD *
            inverseFactorial[n - k] % MOD;
      };
      auto compositions = [&](int count, int runs) -> long long {
        if (runs == 0) return count == 0;
        return combination(count - 1, runs - 1);
      };
      for (const auto& [n, s] : tests) {
        int zeros = 0;
        int zeroRuns = 0;
        int oneRuns = 0;
        for (int i = 0; i < n; ++i) {
          zeros += s[i] == '0';
          if (i == 0 || s[i] != s[i - 1]) {
            if (s[i] == '0') ++zeroRuns;
            else ++oneRuns;
          }
        }
        int ones = n - zeros;
        cout << compositions(zeros, zeroRuns) *
                compositions(ones, oneRuns) % MOD << '\n';
      }
    }
    ```
