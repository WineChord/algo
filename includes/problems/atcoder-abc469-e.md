<div class="problem-anchor" id="problem-atcoder-abc469-e"></div>

??? problem "AtCoder ABC469 E · Pro Exam Eligibility"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_e?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 475 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1566（非官方，检索于 2026-08-06）。

    **题意**：在只含胜负标记的序列中选择至少包含 $K$ 次胜利的非空连续区间，使区间胜率最大。

    **思路**：二分候选胜率 $p$，把胜记为 $1-p$、负记为 $-p$；双指针求每个右端点允许的最晚左边界，再用前缀最小值判断是否存在非负区间和。

    **复杂度**：每次判定 $O(N)$，总时间 $O(N\log(1/\varepsilon))$，额外空间 $O(N)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, k;
      string s;
      cin >> n >> k >> s;
      vector<int> wins(n + 1);
      for (int i = 0; i < n; ++i) {
        wins[i + 1] = wins[i] + (s[i] == 'o');
      }
      vector<int> limit(n + 1, -1);
      int pointer = 0;
      for (int right = 1; right <= n; ++right) {
        if (wins[right] < k) {
          continue;
        }
        int maximumWins = wins[right] - k;
        while (pointer + 1 < right && wins[pointer + 1] <= maximumWins) {
          ++pointer;
        }
        limit[right] = pointer;
      }
      vector<double> prefix(n + 1), minimum(n + 1);
      auto feasible = [&](double rate) {
        prefix[0] = minimum[0] = 0;
        for (int i = 1; i <= n; ++i) {
          prefix[i] = prefix[i - 1] + (s[i - 1] == 'o' ? 1.0 - rate : -rate);
          minimum[i] = min(minimum[i - 1], prefix[i]);
          if (limit[i] >= 0 && prefix[i] >= minimum[limit[i]]) {
            return true;
          }
        }
        return false;
      };
      double low = 0;
      double high = 1;
      for (int iteration = 0; iteration < 70; ++iteration) {
        double middle = (low + high) / 2;
        if (feasible(middle)) {
          low = middle;
        } else {
          high = middle;
        }
      }
      cout << fixed << setprecision(12) << low << '\n';
    }
    ```
