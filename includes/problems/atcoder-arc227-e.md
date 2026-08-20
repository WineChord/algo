<div class="problem-anchor" id="problem-atcoder-arc227-e"></div>

??? problem "AtCoder ARC227 E: Shift and XOR Switches"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_e?lang=en){ .problem-source }

    **难度与分值**：官方分值 700；AtCoder 未标注单题难度；AtCoder Problems 社区估算难度 2710（2026-08-21）

    **题意**：从初始序列 $(1,0,\ldots,0)$ 出发，每个给定开关至多按一次。按下值为 $a$ 的开关时，从右向左执行 $B_i\leftarrow B_i\oplus B_{i-a}$；求所有开关子集能产生多少种不同终态。

    **思路**：把序列视为 $\mathbb F_2[x]/(x^N)$ 上的多项式。一个开关乘上 $1+x^a$，而 $(1+x^a)^2=1+x^{2a}$，所以相同因子像二进制位一样向指数 $2a$ 进位。按指数的奇数部分拆成互不影响的倍增链；每层只需记录进位数量，分别选择当前规范位为 0 或 1，链答案相乘。

    **复杂度**：时间 $O(N+M)$，空间 $O(N)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    constexpr long long MOD = 998244353;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, m;
      cin >> n >> m;
      vector<int> frequency(n);
      for (int i = 0; i < m; ++i) {
        int value;
        cin >> value;
        ++frequency[value];
      }
      long long answer = 1;
      for (int odd = 1; odd < n; odd += 2) {
        map<int, long long> dp;
        dp[0] = 1;
        for (int value = odd; value < n; value *= 2) {
          map<int, long long> next;
          for (auto [carry, ways] : dp) {
            int available = carry + frequency[value];
            int without = available / 2;
            next[without] = (next[without] + ways) % MOD;
            if (available > 0) {
              int with = (available - 1) / 2;
              next[with] = (next[with] + ways) % MOD;
            }
          }
          dp.swap(next);
        }
        long long chainWays = 0;
        for (auto [carry, ways] : dp) {
          static_cast<void>(carry);
          chainWays = (chainWays + ways) % MOD;
        }
        answer = answer * chainWays % MOD;
      }
      cout << answer << '\n';
      return 0;
    }
    ```
