<div class="problem-anchor" id="problem-codeforces-2253-b"></div>

??? problem "Codeforces 2253B: Hypercarp and the Control Panel"
    [打开原题 ↗](https://codeforces.com/contest/2253/problem/B){ .problem-source }

    **难度与分值**：Educational Codeforces Round 193 Div.2 B；官方 rating 1100；官方 points 未提供；标签 `brute force`、`data structures`、`two pointers`（2026-08-26）

    **题意**：先删除任意元素得到子序列，再至多交换一次其中相邻两项；最大化最终相邻颜色均不同的保留长度。

    **思路**：压缩极大等值游程，基础答案是游程数 $m$。相邻两个长游程可用局部 $x,x,y,y\to x,y,x,y$ 增加 2；否则，单个长游程只有在跨过邻居后不会撞上距离为 2 的同色游程时才能增加 1。

    **复杂度**：时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Run {
      int color;
      int length;
    };
    void solve() {
      int n;
      cin >> n;
      vector<Run> runs;
      for (int i = 0; i < n; ++i) {
        int value;
        cin >> value;
        if (runs.empty() || runs.back().color != value)
          runs.push_back({value, 1});
        else
          ++runs.back().length;
      }
      int m = runs.size();
      int bonus = 0;
      for (int i = 0; i + 1 < m; ++i) {
        if (runs[i].length >= 2 && runs[i + 1].length >= 2)
          bonus = 2;
      }
      if (bonus < 2) {
        for (int i = 0; i < m; ++i) {
          if (runs[i].length < 2)
            continue;
          bool right = i + 1 < m &&
              (i + 2 >= m || runs[i].color != runs[i + 2].color);
          bool left = i > 0 &&
              (i < 2 || runs[i].color != runs[i - 2].color);
          if (right || left)
            bonus = 1;
        }
      }
      cout << m + bonus << '\n';
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--)
        solve();
      return 0;
    }
    ```
