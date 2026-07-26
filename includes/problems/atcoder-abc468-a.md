??? problem "AtCoder ABC468 A · Maximal Value"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_a){ .problem-source }

    **题意**：统计整数序列中满足 $A_{i-1}<A_i>A_{i+1}$ 的严格局部峰值位置。

    **思路**：恰好枚举所有拥有左右邻居的内部位置，并逐项检查严格不等式。

    **复杂度**：时间 $O(N)$，保存输入时空间 $O(N)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      cin >> n;
      vector<int> a(n);
      for (int& x : a) cin >> x;
      int answer = 0;
      for (int i = 1; i + 1 < n; ++i) {
        if (a[i - 1] < a[i] && a[i] > a[i + 1]) ++answer;
      }
      cout << answer << '\n';
    }
    ```
