<div class="problem-anchor" id="problem-codeforces-2247-b"></div>

??? problem "CF Round 1111 · Div.2 B · Yet Another Constructive（2247B）"
    [打开原题 ↗](https://codeforces.com/problemset/problem/2247/B){ .problem-source }

    **分值与难度**：Codeforces 官方 750 分；官方 API 暂未给出 problem rating，未按题号推断。

    **题意**：构造正整数数组，使和能被 $m$ 整除的最短非空连续子数组长度恰为 $k$；无解时输出 `NO`。

    **思路**：前缀余数在任意连续 $k$ 个位置内必须互异，故必要条件为 $k\le m$。可行时把 $m$ 拆成 $k$ 个正整数并周期重复；任意长度 $k$ 的窗口和为 $m$，更短窗口和严格介于 0 与 $m$ 之间。

    **复杂度**：每组时间 $O(n)$，额外空间 $O(k)$。

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
        int n, k;
        long long m;
        cin >> n >> k >> m;
        if (k > m) {
          cout << "NO\n";
          continue;
        }
        long long quotient = m / k;
        int remainder = m % k;
        vector<long long> block(k, quotient);
        for (int i = k - remainder; i < k; ++i) ++block[i];
        cout << "YES\n";
        for (int i = 0; i < n; ++i) cout << block[i % k] << " \n"[i + 1 == n];
      }
    }
    ```
