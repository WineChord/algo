<div class="problem-anchor" id="problem-codeforces-2248-c"></div>

??? problem "CF Round 1113 · Div.2 C · Maximize the Score (2248C)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/C){ .problem-source }

    **难度与分值**：Codeforces 官方 1500 分，官方 rating 1300，官方 tags 为 dp、greedy（核对于 2026-08-04）。

    **题意**：数组中每个值恰出现两次；每次选一个值并删除其当前两次出现之间的整段，获得删除长度的平方，求清空数组的最大总分。

    **思路**：交换论证把任意动态删除方案规范为原数组上的连续分块；扫描到某值第二次出现时，用从其首次位置开始的整块平方更新前缀动态规划。

    **复杂度**：每组测试时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        int n;
        cin >> n;
        int length = 2 * n;
        vector<int> first(n + 1, -1);
        vector<long long> dp(length + 1, 0);
        for (int index = 1; index <= length; ++index) {
          int value;
          cin >> value;
          dp[index] = dp[index - 1] + 1;
          if (first[value] == -1) {
            first[value] = index;
          } else {
            int left = first[value];
            long long blockLength = index - left + 1;
            dp[index] = max(dp[index], dp[left - 1] + blockLength * blockLength);
          }
        }
        cout << dp[length] << '\n';
      }
    }
    ```
