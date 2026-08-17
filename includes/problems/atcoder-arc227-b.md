<div class="problem-anchor" id="problem-atcoder-arc227-b"></div>

??? problem "AtCoder ARC227 B: Know Your Place"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_b?lang=en){ .problem-source }

    **难度与分值**：官方分值 500；AtCoder 未标注单题难度；AtCoder Problems 社区估算难度 1043（2026-08-18）

    **题意**：重排给定多重集，使每个值恰好等于它左侧严格更小元素的数量；判断可行性并构造一个答案。

    **思路**：值 x 必须在答案长度首次到达 x 时引入，多余副本后进先出暂存。新压栈的值都更大，故旧副本等待期间不会增加更小前驱数；没有同长度新值且栈空时即无解。

    **复杂度**：时间 O(N)，额外空间 O(N)。

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
      vector<int> count(n);
      for (int i = 0; i < n; ++i) {
        int value;
        cin >> value;
        ++count[value];
      }
      vector<int> pending;
      vector<int> answer;
      pending.reserve(n);
      answer.reserve(n);
      for (int length = 0; length < n; ++length) {
        if (count[length] > 0) {
          answer.push_back(length);
          for (int copy = 1; copy < count[length]; ++copy) {
            pending.push_back(length);
          }
          count[length] = 0;
        } else if (!pending.empty()) {
          answer.push_back(pending.back());
          pending.pop_back();
        } else {
          cout << "No\n";
          return 0;
        }
      }
      cout << "Yes\n";
      for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << answer[i];
      }
      cout << '\n';
      return 0;
    }
    ```
