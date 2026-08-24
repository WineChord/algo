<div class="problem-anchor" id="problem-codeforces-2253-a"></div>

??? problem "Codeforces 2253A: The Best Card"
    [打开原题 ↗](https://codeforces.com/contest/2253/problem/A){ .problem-source }

    **难度与分值**：Educational Codeforces Round 193 Div.2 A；官方 rating 800；官方 points 未给出；标签 `greedy`、`math`、`number theory`（2026-08-25）

    **题意**：牌值是 $2,3,\ldots,n+1$。两张牌可整除时较小者获胜，否则较大者获胜；判断是否存在一张能击败其余全部牌的牌。

    **思路**：任意非最大牌 $x$ 都会输给相邻牌 $x+1$，所以唯一候选是 $n+1$。它只会输给自己的较小因子，因此存在全胜牌当且仅当 $n+1$ 为素数。

    **复杂度**：每个测试时间 $O(\sqrt n)$，额外空间 $O(1)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    bool isPrime(int value) {
      if (value < 2)
        return false;
      for (int divisor = 2; 1LL * divisor * divisor <= value; ++divisor) {
        if (value % divisor == 0)
          return false;
      }
      return true;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        cin >> n;
        cout << (isPrime(n + 1) ? "YES\n" : "NO\n");
      }
      return 0;
    }
    ```
