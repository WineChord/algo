<div class="problem-anchor" id="problem-atcoder-abc472-b"></div>

??? problem "AtCoder ABC472 B: Break a Stick"
    [打开原题 ↗](https://atcoder.jp/contests/abc472/tasks/abc472_b?lang=en){ .problem-source }

    **难度与分值**：官方分值 200；AtCoder 未给出单题官方难度；AtCoder Problems 社区估算难度 -521（2026-08-24）

    **题意**：一根棒由 $N$ 段依次连接而成，只能在相邻两段之间切一刀。求切成的两根棒长度差的最小值。

    **思路**：设总长为 $S$，切口左侧前缀和为 $P$，两侧长度差就是 $|P-(S-P)|=|2P-S|$。先求总和，再在线性扫描中增量维护前缀和，枚举全部 $N-1$ 个合法切口。

    **复杂度**：时间 $O(N)$，额外空间 $O(1)$（不计输入数组）。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<long long> length(n);
      long long total = 0;
      for (long long& value : length) {
        cin >> value;
        total += value;
      }
      long long left = 0;
      long long answer = numeric_limits<long long>::max();
      for (int i = 0; i + 1 < n; ++i) {
        left += length[i];
        answer = min(answer, abs(2 * left - total));
      }
      cout << answer << '\n';
      return 0;
    }
    ```
