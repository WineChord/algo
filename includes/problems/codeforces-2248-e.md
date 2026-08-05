<div class="problem-anchor" id="problem-codeforces-2248-e"></div>

??? problem "CF Round 1113 · Div.2 E · Excuse for Breaks (2248E)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/E){ .problem-source }

    **难度与分值**：Codeforces 官方 2500 分，官方 rating 1900，官方 tags 为 binary search、brute force、greedy、math、two pointers（核对于 2026-08-06）。

    **题意**：判断是否存在两个正长二进制输入，使分别运行后的得分和严格大于在两输入之间插入一个零后运行的得分。

    **思路**：利用长度为 $n$ 的周期增量，把任意候选规约到奖励时刻；只需枚举奖励点对 $(p_i,p_j)$，检查 $S_{p_i}+S_{p_j}>S_{p_i+p_j+1}$。

    **复杂度**：每个测试时间 $O(m^2)$，额外空间 $O(m)$。

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
        long long n, d;
        int m;
        cin >> n >> m >> d;
        vector<long long> p(m), r(m), rewardPrefix(m + 1), score(m);
        for (int i = 0; i < m; ++i) {
          cin >> p[i] >> r[i];
          rewardPrefix[i + 1] = rewardPrefix[i] + r[i];
          score[i] = p[i] * d + rewardPrefix[i + 1];
        }
        long long cycleScore = n * d + rewardPrefix[m];
        bool possible = false;
        for (int i = 0; i < m && !possible; ++i) {
          long long currentCycle = -1;
          int pointer = 0;
          for (int j = 0; j < m; ++j) {
            long long length = p[i] + p[j] + 1;
            long long cycles = length / n;
            long long remainder = length % n;
            if (cycles != currentCycle) {
              currentCycle = cycles;
              pointer = 0;
            }
            while (pointer < m && p[pointer] <= remainder) {
              ++pointer;
            }
            long long wholeScore = cycles * cycleScore + remainder * d;
            wholeScore += rewardPrefix[pointer];
            if (score[i] + score[j] > wholeScore) {
              possible = true;
              break;
            }
          }
        }
        cout << (possible ? "YES\n" : "NO\n");
      }
    }
    ```
