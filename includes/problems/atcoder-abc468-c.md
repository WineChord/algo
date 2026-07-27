<div class="problem-anchor" id="problem-atcoder-abc468-c"></div>

??? problem "AtCoder ABC468 C · Between P and Q"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en){ .problem-source }

    **分值与难度**：AtCoder 官方 300 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 282（非官方，检索于 2026-07-28）。

    **题意**：给定 $1,\ldots,N$ 的两个排列 $P,Q$，统计字典序严格满足 $P<R<Q$ 的排列 $R$ 数量。

    **思路**：用 Lehmer 码求排列的零基字典序排名。位置 $i$ 若还有 $c_i$ 个未使用值小于当前值，就贡献 $c_i(N-i-1)!$；答案为 $\max(0,\operatorname{rank}(Q)-\operatorname{rank}(P)-1)$。

    **复杂度**：时间 $O(N^2)$，额外空间 $O(N)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    long long permutationRank(const vector<int>& permutation, const vector<long long>& factorial) {
      int n = permutation.size();
      vector<char> used(n + 1);
      long long rank = 0;
      for (int i = 0; i < n; ++i) {
        int smaller = 0;
        for (int value = 1; value < permutation[i]; ++value) {
          if (!used[value]) ++smaller;
        }
        rank += smaller * factorial[n - i - 1];
        used[permutation[i]] = 1;
      }
      return rank;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<int> p(n), q(n);
      for (int& x : p) cin >> x;
      for (int& x : q) cin >> x;
      vector<long long> factorial(n + 1, 1);
      for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i;
      long long left = permutationRank(p, factorial);
      long long right = permutationRank(q, factorial);
      cout << max(0LL, right - left - 1) << '\n';
    }
    ```
