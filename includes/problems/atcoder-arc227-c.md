<div class="problem-anchor" id="problem-atcoder-arc227-c"></div>

??? problem "AtCoder ARC227 C: Follow the Letters"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_c?lang=en){ .problem-source }

    **难度与分值**：官方分值 700；AtCoder 未标注单题难度；AtCoder Problems 社区估算难度 2121（2026-08-19）

    **题意**：圆环上每个岛有一个字符且初始各站一人。每次指定字符后，所有人顺时针移动到下一个该字符岛；同岛的人会合并。构造操作串，使最终占用岛数最少。

    **思路**：用 KMP 求字符串最小周期 $p$。相差 $p$ 的人永不合并，给出下界 $N/p$；执行 $X=S^N$ 时，每个周期区间内的人都会并入一个代表，恰好达到下界。

    **复杂度**：输出长度 $L=N^2$，时间 $O(N+L)=O(N^2)$，额外空间 $O(N)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      string s;
      cin >> n >> s;
      vector<int> prefix(n);
      for (int i = 1; i < n; ++i) {
        int matched = prefix[i - 1];
        while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
        if (s[i] == s[matched]) ++matched;
        prefix[i] = matched;
      }
      int period = n - prefix[n - 1];
      if (n % period != 0) period = n;
      cout << n / period << '\n';
      cout << 1LL * n * n << '\n';
      for (int repeat = 0; repeat < n; ++repeat) cout << s;
      cout << '\n';
      return 0;
    }
    ```
