<div class="problem-anchor" id="problem-codeforces-2248-b"></div>

??? problem "CF Round 1113 · Div.2 B · Merge to Match (2248B)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/B){ .problem-source }

    **难度与分值**：Codeforces 官方 1250 分；官方 API 暂未给出 problem rating，官方 tags 为 greedy、sortings（核对于 2026-08-03）。

    **题意**：从数组 $a$ 选择不相交、各至少含两个元素的组，使每组最小值与最大值之和等于给定且互异的目标值，判断能否完成全部目标。

    **思路**：每个目标需要一个严格更小与严格更大的见证；交换论证把小见证规范为全局最小的 $m$ 个数，逐位检查后再从剩余数中贪心匹配严格更大的最小可用值。

    **复杂度**：每组测试时间 $O((n+m)\log(n+m))$，额外空间 $O(n+m)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    bool possible(vector<long long> a, vector<long long> b) {
      int n = a.size();
      int m = b.size();
      if (n < 2 * m) {
        return false;
      }
      sort(a.begin(), a.end());
      sort(b.begin(), b.end());
      for (int i = 0; i < m; ++i) {
        if (a[i] >= b[i]) {
          return false;
        }
      }
      int next = m;
      for (long long target : b) {
        while (next < n && a[next] <= target) {
          ++next;
        }
        if (next == n) {
          return false;
        }
        ++next;
      }
      return true;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        int n, m;
        cin >> n >> m;
        vector<long long> a(n), b(m);
        for (long long& value : a) {
          cin >> value;
        }
        for (long long& value : b) {
          cin >> value;
        }
        cout << (possible(a, b) ? "YES" : "NO") << '\n';
      }
    }
    ```
