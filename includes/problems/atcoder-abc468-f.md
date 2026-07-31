<div class="problem-anchor" id="problem-atcoder-abc468-f"></div>

??? problem "AtCoder ABC468 F · Chmax"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_f?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 500 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 1693（非官方，检索于 2026-07-31）。

    **题意**：给定排列，统计用前缀取最大操作得到它的操作序列数量。

    **思路**：每个前缀最大值出现时，其生成位置已被唯一确定；其余元素只能按一个严格递增子序列进入。答案等于可选择的非前缀最大值位置数减去对应 LIS 长度。

    **复杂度**：时间 $O(n\log n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      int maximum = 0;
      int records = 0;
      vector<int> tails;
      for (int i = 0; i < n; ++i) {
        int value;
        cin >> value;
        if (value > maximum) {
          maximum = value;
          ++records;
        } else {
          auto it = lower_bound(tails.begin(), tails.end(), value);
          if (it == tails.end()) {
            tails.push_back(value);
          } else {
            *it = value;
          }
        }
      }
      cout << records + static_cast<int>(tails.size()) << '\n';
    }
    ```
