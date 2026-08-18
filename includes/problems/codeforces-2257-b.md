<div class="problem-anchor" id="problem-codeforces-2257-b"></div>

??? problem "Codeforces 2257B: Gigantomachy"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/B?locale=en){ .problem-source }

    **难度与分值**：官方分值 750；官方 rating 未给出；官方标签 `math`（2026-08-19）

    **题意**：Bea 与 Ver 轮流攻击对方所在山峰；攻击使高度减一，行动者再按规则向下一座更高山峰跳跃或在末山为零时认输。判断胜者。

    **思路**：一条非增山脉 $(h_1,\ldots,h_k)$ 在认输前可承受的攻击数望远镜化为 $H=h_1+k-1$。Bea 先手，因此 $H_A\ge H_B$ 时她先耗尽 Ver 的耐久，否则 Ver 获胜。

    **复杂度**：读取输入需 $O(n+m)$ 时间，额外空间 $O(1)$；判定本身为 $O(1)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        int n, m;
        cin >> n >> m;
        long long firstA = 0;
        long long firstB = 0;
        for (int i = 0; i < n; ++i) {
          long long height;
          cin >> height;
          if (i == 0) firstA = height;
        }
        for (int i = 0; i < m; ++i) {
          long long height;
          cin >> height;
          if (i == 0) firstB = height;
        }
        long long enduranceA = firstA + n - 1;
        long long enduranceB = firstB + m - 1;
        cout << (enduranceB <= enduranceA ? 1 : 2) << '\n';
      }
      return 0;
    }
    ```
