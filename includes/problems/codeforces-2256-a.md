<div class="problem-anchor" id="problem-codeforces-2256-a"></div>

??? problem "CF Round 1116 · Div.2 A · Three Numbers on the Blackboard (2256A)"
    [打开原题 ↗](https://codeforces.com/contest/2256/problem/A){ .problem-source }

    **难度与分值**：Codeforces 官方 500 分，rating 字段缺失，官方 tags 为 math、sortings（核对于 2026-08-12）。

    **题意**：黑板上有三个非负整数；每步可把一个数替换为另外两个数之和，求最终最大值与最小值之差的最小可能值。

    **思路**：排序为 x≤y≤z。零步的值差是 z-x；执行第一步后只有替换最大值可能更优，得到值差 y，而进入加和状态后值差不再下降。

    **复杂度**：每组时间 O(1)，空间 O(1)。

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
        array<long long, 3> a;
        for (long long& x : a) cin >> x;
        sort(a.begin(), a.end());
        cout << min(a[2] - a[0], a[1]) << '\n';
      }
    }
    ```
