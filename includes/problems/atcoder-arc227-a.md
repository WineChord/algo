<div class="problem-anchor" id="problem-atcoder-arc227-a"></div>

??? problem "AtCoder ARC227 A: Fermat Point of Binary Strings"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_a?lang=en){ .problem-source }

    **难度与分值**：官方分值 400；AtCoder 未标注难度；AtCoder Problems 社区估算难度 614（2026-08-17）

    **题意**：给定三个长度为 2N、各含 N 个 0 与 N 个 1 的串，构造同类串 X，使三个输入通过相邻交换变到 X 的总次数最少。

    **思路**：相邻交换距离等于同序号 1 的位置差绝对值之和。每一列取三个位置的中位数；三个位置序列严格递增，逐列中位数仍严格递增，因此各维最优能同时组成合法答案。

    **复杂度**：时间 O(N)，额外空间 O(N)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    vector<int> positions(const string& s) {
      vector<int> answer;
      for (int i = 0; i < static_cast<int>(s.size()); ++i) {
        if (s[i] == '1') answer.push_back(i);
      }
      return answer;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      string a, b, c;
      cin >> n >> a >> b >> c;
      vector<int> pa = positions(a);
      vector<int> pb = positions(b);
      vector<int> pc = positions(c);
      string answer(2 * n, '0');
      long long cost = 0;
      for (int k = 0; k < n; ++k) {
        array<int, 3> value{pa[k], pb[k], pc[k]};
        sort(value.begin(), value.end());
        int median = value[1];
        answer[median] = '1';
        cost += median - value[0] + value[2] - median;
      }
      cout << cost << '\n' << answer << '\n';
    }
    ```
