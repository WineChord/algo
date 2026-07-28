<div class="problem-anchor" id="problem-codeforces-2247-d1"></div>

??? problem "CF Round 1111 · Div.2 D1 · XOR Sorting (Easy Version) (2247D1)"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/D1){ .problem-source }

    **难度与分值**：Codeforces 官方 1500 分；官方 API 暂未给出 problem rating，标签为 `bitmasks`、`greedy`。

    **题意**：允许交换满足 $(i\mathbin{\mathrm{XOR}}j)\le k$ 的下标元素，求能把数组排成非降序的最小非负整数 $k$；Easy Version 没有修改询问。

    **思路**：答案只会是零或二的幂。按下标二进制前缀递归切分区间；若左半最大值大于右半最小值，就必须把两半合并到同一可交换块。

    **复杂度**：每组时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Node {
      int minimum = INT_MAX;
      int maximum = INT_MIN;
      int answer = 0;
      bool empty = true;
    };
    Node solve(const vector<int>& a, int left, int right) {
      if (right - left == 1) {
        if (left >= static_cast<int>(a.size())) {
          return {};
        }
        return Node{a[left], a[left], 0, false};
      }
      int middle = (left + right) / 2;
      Node first = solve(a, left, middle);
      Node second = solve(a, middle, right);
      if (first.empty) {
        return second;
      }
      if (second.empty) {
        return first;
      }
      Node result;
      result.empty = false;
      result.minimum = min(first.minimum, second.minimum);
      result.maximum = max(first.maximum, second.maximum);
      result.answer = max(first.answer, second.answer);
      if (first.maximum > second.minimum) {
        result.answer = max(result.answer, (right - left) / 2);
      }
      return result;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n, q;
        cin >> n >> q;
        vector<int> a(n);
        for (int& value : a) {
          cin >> value;
        }
        int size = 1;
        while (size < n) {
          size <<= 1;
        }
        cout << solve(a, 0, size).answer << '\n';
      }
      return 0;
    }
    ```
