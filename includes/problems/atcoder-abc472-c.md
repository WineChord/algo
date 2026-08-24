<div class="problem-anchor" id="problem-atcoder-abc472-c"></div>

??? problem "AtCoder ABC472 C: On a Diet"
    [打开原题 ↗](https://atcoder.jp/contests/abc472/tasks/abc472_c?lang=en){ .problem-source }

    **难度与分值**：官方分值 300；AtCoder 未给出单题官方难度；AtCoder Problems 社区估算难度 87（2026-08-25）

    **题意**：依次处理每天的零食；若把当天热量加入最近 $M$ 天内已经吃下的热量后不超过 $K$，当天必须吃，否则跳过。输出每天的决定。

    **思路**：用 `eaten[i]` 保存第 $i$ 天真正吃下的热量，拒绝时为 0。处理新一天前减去刚离开最近 $M$ 天窗口的贡献，再用当前窗口和作唯一判定；每个贡献至多加入、删除一次。

    **复杂度**：时间 $O(N)$，额外空间 $O(N)$；改用带日期队列可降为 $O(M)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      int m;
      long long k;
      cin >> n >> m >> k;
      vector<long long> calories(n);
      vector<long long> eaten(n, 0);
      for (long long& value : calories)
        cin >> value;
      long long window = 0;
      for (int i = 0; i < n; ++i) {
        if (i >= m)
          window -= eaten[i - m];
        if (window + calories[i] <= k) {
          eaten[i] = calories[i];
          window += calories[i];
          cout << "Yes\n";
        } else {
          cout << "No\n";
        }
      }
      return 0;
    }
    ```
