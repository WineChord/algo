<div class="problem-anchor" id="problem-codeforces-2248-f"></div>

??? problem "CF Round 1113 · Div.2 F · Matrix Elimination (2248F)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/F){ .problem-source }

    **难度与分值**：Codeforces 官方 2500 分，官方 rating 2500，官方 tags 为 binary search、greedy、math（核对于 2026-08-09）。

    **题意**：每次选择一个子矩形并把其中所有数减一，求最少操作次数，使至少 $k$ 个格成为不小于同行和同列其余元素总和的峰值。

    **思路**：二维时整矩阵操作逐点支配任何局部操作，答案是每格缺口所需次数的第 $k$ 小值；一维额外枚举整段和两种漏端点策略。

    **复杂度**：时间 $O(nm\log(nm))$，空间 $O(nm)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using int64 = long long;
    const int64 INF = 4'000'000'000'000'000'000LL;
    int64 ceilDivide(int64 value, int64 positiveDivisor) {
      if (value >= 0) {
        return (value + positiveDivisor - 1) / positiveDivisor;
      }
      return value / positiveDivisor;
    }
    int64 endpointStrategy(vector<int64> others, int64 endpoint, int64 sum, int k) {
      int length = others.size() + 1;
      if (k == 1) {
        return max(0LL, ceilDivide(sum - 2 * endpoint, length - 1));
      }
      sort(others.rbegin(), others.rend());
      int64 thresholdValue = others[k - 2];
      int64 operations = max({0LL, ceilDivide(sum - endpoint - thresholdValue, length - 2),
          ceilDivide(sum - 2 * endpoint, length - 1)});
      int64 lower = max(0LL, sum - 2 * endpoint - (length - 2) * operations);
      int64 upper = min(operations, (length - 2) * operations - (sum - 2 * thresholdValue));
      return lower <= upper ? operations : INF;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n, m, k;
        cin >> n >> m >> k;
        vector<vector<int64>> value(n, vector<int64>(m));
        vector<int64> row(n), column(m), flat;
        int64 total = 0;
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < m; ++j) {
            cin >> value[i][j];
            row[i] += value[i][j];
            column[j] += value[i][j];
            total += value[i][j];
            flat.push_back(value[i][j]);
          }
        }
        if (n + m <= 3) {
          sort(flat.begin(), flat.end());
          if (flat.size() == 1) {
            cout << (flat[0] >= 0 ? 0 : -1) << '\n';
          } else if (k == 1) {
            cout << 0 << '\n';
          } else {
            cout << flat[1] - flat[0] << '\n';
          }
          continue;
        }
        int64 gain = n + m - 3;
        vector<int64> need;
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < m; ++j) {
            int64 deficit = row[i] + column[j] - 3 * value[i][j];
            need.push_back(max(0LL, ceilDivide(deficit, gain)));
          }
        }
        sort(need.begin(), need.end());
        int64 answer = need[k - 1];
        if (n == 1 || m == 1) {
          vector<int64> withoutLast(flat.begin(), flat.end() - 1);
          vector<int64> withoutFirst(flat.begin() + 1, flat.end());
          answer = min(answer, endpointStrategy(withoutLast, flat.back(), total, k));
          answer = min(answer, endpointStrategy(withoutFirst, flat.front(), total, k));
        }
        cout << answer << '\n';
      }
    }
    ```
