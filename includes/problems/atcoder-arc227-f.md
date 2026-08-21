<div class="problem-anchor" id="problem-atcoder-arc227-f"></div>

??? problem "AtCoder ARC227 F: Erase and Raise"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_f?lang=en){ .problem-source }

    **难度与分值**：官方分值 800；AtCoder 未标注单题难度；AtCoder Problems 社区估算难度 3159（2026-08-22）

    **题意**：从长度为 $N$ 的全零序列出发，反复删除两个相等元素，并把两者之间的元素全部加 1；统计无法继续操作时可能出现的不同终态，空序列也计入。

    **思路**：非负整数终态 $B$ 可达当且仅当长度与 $N$ 同奇偶、元素互异，且 $|B|+\sum|B_i-B_{i+1}|\le N$（两端补 0）。按值递增插入终态元素，维护未来仍会插入更大值的活跃间隙数；跳过值和插入值都只改变“预算、间隙数”。预算下界把间隙数限制为 $O(\sqrt N)$。

    **复杂度**：时间 $O(N\sqrt N)$，空间 $O(N\sqrt N)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    constexpr int MOD = 998244353;
    void addMod(int& target, long long value) {
      target = (target + value) % MOD;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      int gapLimit = 1;
      while (1LL * (gapLimit + 1) * (gapLimit + 1) +
          2LL * (gapLimit + 1) - 3 <= n) {
        ++gapLimit;
      }
      vector<vector<int>> dp(n + 1, vector<int>(gapLimit + 2));
      dp[0][1] = 1;
      for (int cost = 0; cost <= n; ++cost) {
        for (int gaps = 1; gaps <= gapLimit; ++gaps) {
          int ways = dp[cost][gaps];
          if (ways == 0) continue;
          if (cost + 2 * gaps <= n) addMod(dp[cost + 2 * gaps][gaps], ways);
          for (int children = 0; children <= 2; ++children) {
            int nextGaps = gaps - 1 + children;
            int nextCost = cost + 1 + 2 * nextGaps;
            if (nextCost > n) continue;
            long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
            if (nextGaps <= gapLimit) {
              addMod(dp[nextCost][nextGaps], choices * ways);
            }
          }
        }
      }
      int answer = n % 2 == 0;
      for (int cost = n % 2; cost <= n; cost += 2) {
        addMod(answer, dp[cost][0]);
      }
      cout << answer << '\n';
      return 0;
    }
    ```
