<div class="problem-anchor" id="problem-codeforces-2247-c"></div>

??? problem "CF Round 1111 · Div.2 C · Inversion of a Subsequence（2247C）"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/C){ .problem-source }

    **分值与难度**：Codeforces 官方 1250 分；官方 API 暂未给出 problem rating，标签为 `greedy`、`math`。

    **题意**：每次选择当前元素和为奇数的非空子序列并翻转其全部二进制位，求把数组 $a$ 变成 $b$ 的最少操作数，无解输出 `-1`。

    **思路**：令 $x$ 为失配位置中当前值为 1 的数量。一轮完成必须恰好翻转全部失配位，因此 $x$ 为奇数时答案为 1；$x$ 为偶数时通常可拆成两轮。非平凡的全零起点没有合法操作，非平凡的全一目标也不可能由最后一次合法操作得到，二者为仅有的无解边界。

    **复杂度**：每组时间 $O(n)$，额外空间 $O(n)$。

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
        int n;
        cin >> n;
        vector<int> a(n), b(n);
        for (int& x : a) cin >> x;
        for (int& x : b) cin >> x;
        if (a == b) {
          cout << 0 << '\n';
          continue;
        }
        int onesA = accumulate(a.begin(), a.end(), 0);
        int onesB = accumulate(b.begin(), b.end(), 0);
        if (onesA == 0 || onesB == n) {
          cout << -1 << '\n';
          continue;
        }
        int mismatchOnes = 0;
        for (int i = 0; i < n; ++i) {
          if (a[i] != b[i] && a[i] == 1) ++mismatchOnes;
        }
        cout << (mismatchOnes % 2 == 1 ? 1 : 2) << '\n';
      }
    }
    ```
