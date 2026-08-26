<div class="problem-anchor" id="problem-codeforces-2253-c"></div>

??? problem "Codeforces 2253C: Sum of Distinct Values in a Matrix"
    [打开原题 ↗](https://codeforces.com/contest/2253/problem/C){ .problem-source }

    **难度与分值**：Educational Codeforces Round 193 Div.2 C；官方 rating 1500；官方 points 未提供；标签 `greedy`、`sortings`、`two pointers`（2026-08-27）

    **题意**：可反复用数组 $A$ 中的值覆盖整行、用数组 $B$ 中的值覆盖整列；最大化最终矩阵中所有不同值之和。

    **思路**：一个值集合可实现，当且仅当其中的 $A$ 独占值不超过 $n$ 个、$B$ 独占值不超过 $m$ 个，且总数不超过 $n+m-1$。从大到小合并两个有序数组，公共值只占全局容量，独占值还占对应方向容量；每次纳入不违反配额的最大剩余值。

    **复杂度**：时间 $O(x+y)$，除输入外额外空间 $O(1)$。

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
        int n, m, x, y;
        cin >> n >> m >> x >> y;
        vector<int> a(x), b(y);
        for (int& value : a)
          cin >> value;
        for (int& value : b)
          cin >> value;
        int i = x - 1, j = y - 1;
        int used = 0, onlyA = 0, onlyB = 0;
        int limit = n + m - 1;
        long long answer = 0;
        while (i >= 0 || j >= 0) {
          int value, type;
          if (j < 0 || (i >= 0 && a[i] > b[j])) {
            value = a[i--];
            type = 1;
          } else if (i < 0 || b[j] > a[i]) {
            value = b[j--];
            type = 2;
          } else {
            value = a[i];
            type = 3;
            --i;
            --j;
          }
          bool take = used < limit;
          if (type == 1)
            take = take && onlyA < n;
          if (type == 2)
            take = take && onlyB < m;
          if (!take)
            continue;
          answer += value;
          ++used;
          onlyA += type == 1;
          onlyB += type == 2;
        }
        cout << answer << '\n';
      }
      return 0;
    }
    ```
