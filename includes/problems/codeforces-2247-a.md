<div class="problem-anchor" id="problem-codeforces-2247-a"></div>

??? problem "CF Round 1111 · Div.2 A · Zero Sum（2247A）"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/A){ .problem-source }

    **题意**：数组只含 $\pm1$；每次把一对相邻元素同时取反，判断能否把总和变成 0。

    **思路**：操作保持所有元素乘积。零和目标必须有 $n/2$ 个负数，因此可行当且仅当 $n$ 为偶数，且初始负数个数与 $n/2$ 奇偶相同；路径上的相邻翻转能生成任意偶数大小的差异集合。

    **复杂度**：每个测试时间 $O(n)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n, negative = 0;
        cin >> n;
        for (int i = 0; i < n; ++i) {
          int x;
          cin >> x;
          negative += x == -1;
        }
        bool possible = n % 2 == 0 && negative % 2 == (n / 2) % 2;
        cout << (possible ? "YES\n" : "NO\n");
      }
    }
    ```
