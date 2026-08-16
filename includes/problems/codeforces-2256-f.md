<div class="problem-anchor" id="problem-codeforces-2256-f"></div>

??? problem "Codeforces 2256F / 2255D: How Long Until Nothing Remains?"
    [打开原题 ↗](https://codeforces.com/problemset/problem/2256/F?locale=en){ .problem-source }

    **难度与分值**：官方 rating 2300；Div.1 D / Div.2 F 官方分值 1750 / 3000

    **题意**：每秒选一个元素向下取整除以 2，其余元素向上取整除以 2，求全数组变为 0 的最少秒数。

    **思路**：固定 T 秒后，每个时间位 2^s 只能分给一个元素，元素收到的权值和至少覆盖初值。降序权值始终给最大剩余需求是充要贪心；答案位于 [n,n+30]，用最大堆判定并二分。

    **复杂度**：每个测试时间 O(n log n)，空间 O(n)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    bool feasible(const vector<int>& values, int seconds) {
      priority_queue<long long> remaining;
      for (int value : values) remaining.push(value);
      int largeWeights = max(0, seconds - 30);
      while (largeWeights-- > 0 && !remaining.empty()) remaining.pop();
      for (int bit = min(29, seconds - 1); bit >= 0 && !remaining.empty(); --bit) {
        long long need = remaining.top();
        remaining.pop();
        need -= 1LL << bit;
        if (need > 0) remaining.push(need);
      }
      return remaining.empty();
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        cin >> n;
        vector<int> values(n);
        for (int& value : values) cin >> value;
        int low = n - 1;
        int high = n + 30;
        while (high - low > 1) {
          int middle = low + (high - low) / 2;
          if (feasible(values, middle)) high = middle;
          else low = middle;
        }
        cout << high << '\n';
      }
    }
    ```
