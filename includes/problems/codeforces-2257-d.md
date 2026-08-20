<div class="problem-anchor" id="problem-codeforces-2257-d"></div>

??? problem "Codeforces 2257D: Bermuda Rectangle"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/D?locale=en){ .problem-source }

    **难度与分值**：官方分值 1750；官方 rating 未给出；官方标签 `binary search`、`implementation`、`math`、`number theory`、`two pointers`（2026-08-21）

    **题意**：所有左下角在原点、整数边长且面积为 $S$ 的矩形共同覆盖若干单位格。每次给出 $x\times y$ 查询矩形，求其中被至少一个候选矩形覆盖的单位格数量。

    **思路**：枚举并排序 $S$ 的所有因数。第 $i$ 列的最大覆盖高度由不小于 $i$ 的最小因数决定，形成单调阶梯；预处理阶梯面积前缀。对查询按阈值 $S/y$ 二分最后一个高度至少为 $y$ 的阶梯端点，前段按 $y$ 截断，后段用前缀面积求和。

    **复杂度**：每组预处理 $O(\sqrt S+\tau(S)\log\tau(S))$，每次询问 $O(\log\tau(S))$，空间 $O(\tau(S))$。

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
        long long s;
        int q;
        cin >> s >> q;
        vector<long long> divisors;
        for (long long value = 1; value * value <= s; ++value) {
          if (s % value != 0) continue;
          divisors.push_back(value);
          if (value != s / value) divisors.push_back(s / value);
        }
        sort(divisors.begin(), divisors.end());
        vector<long long> prefix(divisors.size());
        for (int i = 0; i < static_cast<int>(divisors.size()); ++i) {
          long long previous = i == 0 ? 0 : divisors[i - 1];
          long long added = (divisors[i] - previous) * (s / divisors[i]);
          prefix[i] = added + (i == 0 ? 0 : prefix[i - 1]);
        }
        auto fullHeightPrefix = [&](long long x) {
          if (x == 0) return 0LL;
          int index = lower_bound(divisors.begin(), divisors.end(), x) - divisors.begin();
          long long previous = index == 0 ? 0 : divisors[index - 1];
          long long before = index == 0 ? 0 : prefix[index - 1];
          return before + (x - previous) * (s / divisors[index]);
        };
        while (q--) {
          long long x, y;
          cin >> x >> y;
          long long limit = s / y;
          int index = upper_bound(divisors.begin(), divisors.end(), limit) -
              divisors.begin() - 1;
          long long cappedUntil = min(x, divisors[index]);
          long long answer = cappedUntil * y;
          if (x > cappedUntil) {
            answer += fullHeightPrefix(x) - fullHeightPrefix(cappedUntil);
          }
          cout << answer << '\n';
        }
      }
      return 0;
    }
    ```
