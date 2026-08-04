<div class="problem-anchor" id="problem-codeforces-2248-d"></div>

??? problem "CF Round 1113 · Div.2 D · Good Pair Queries (2248D)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/D){ .problem-source }

    **难度与分值**：Codeforces 官方 1750 分，官方 rating 1400，官方 tags 为 constructive algorithms、greedy（核对于 2026-08-05）。

    **题意**：对两个等长二进制子串，允许同步删除同一位置集合，且所选字符在两串中共享一个众数；回答每个区间能否最终删空。

    **思路**：把位置分为 00、01、10、11 四类。共同字符类提供消化不匹配的容量；可删空当且仅当 $|c_{01}-c_{10}|\le c_{00}+c_{11}$，由前缀计数常数回答。

    **复杂度**：预处理 $O(n)$，每次询问 $O(1)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCases;
      cin >> testCases;
      while (testCases--) {
        int n, q;
        string s, t;
        cin >> n >> q >> s >> t;
        vector<int> count01(n + 1), count10(n + 1);
        for (int i = 0; i < n; ++i) {
          count01[i + 1] = count01[i] + (s[i] == '0' && t[i] == '1');
          count10[i + 1] = count10[i] + (s[i] == '1' && t[i] == '0');
        }
        while (q--) {
          int left, right;
          cin >> left >> right;
          int opposite01 = count01[right] - count01[left - 1];
          int opposite10 = count10[right] - count10[left - 1];
          int length = right - left + 1;
          int same = length - opposite01 - opposite10;
          cout << (abs(opposite01 - opposite10) <= same ? "YES" : "NO") << '\n';
        }
      }
    }
    ```
