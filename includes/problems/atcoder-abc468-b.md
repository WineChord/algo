??? problem "AtCoder ABC468 B · Corridor Watch"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en){ .problem-source }

    **分值与难度**：AtCoder 官方 200 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 -388（非官方，检索于 2026-07-27）。

    **题意**：长为 $M$ 的走廊中，守卫能监视与其距离不超过 $D$ 的格子，统计没有被任何守卫监视的格子数。

    **思路**：维护当前格子监视窗口 $[x-D,x+D]$ 内的守卫数。右移一格时删除离开窗口的位置并加入新进入的位置；计数为零即未被监视。

    **复杂度**：时间 $O(M)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int m, d;
      string s;
      cin >> m >> d >> s;
      int guards = 0;
      for (int i = 0; i <= d && i < m; ++i) guards += s[i] == 'G';
      int answer = 0;
      for (int x = 0; x < m; ++x) {
        answer += guards == 0;
        int outgoing = x - d;
        int incoming = x + d + 1;
        if (outgoing >= 0 && s[outgoing] == 'G') --guards;
        if (incoming < m && s[incoming] == 'G') ++guards;
      }
      cout << answer << '\n';
    }
    ```
