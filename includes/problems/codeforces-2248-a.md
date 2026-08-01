<div class="problem-anchor" id="problem-codeforces-2248-a"></div>

??? problem "CF Round 1113 · Div.2 A · You Delete, I Delete (2248A)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/A){ .problem-source }

    **难度与分值**：Codeforces 官方 500 分；官方 API 暂未给出 problem rating 与 tags（核对于 2026-08-02）。

    **题意**：Alice 先删一个 `0` 以最大化终局，Bob 再删一个 `1` 以最小化终局，求双方最优后的二进制串。

    **思路**：删除固定字符时，最大化应消去首个上升断点，最小化应消去首个下降断点；不存在断点则删该字符最后一次出现。

    **复杂度**：每组时间 $O(n)$，额外空间 $O(1)$（不计字符串原地移动）。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    void eraseForMaximum(string& s, char wanted) {
      for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
        if (s[i] == wanted && s[i] < s[i + 1]) {
          s.erase(s.begin() + i);
          return;
        }
      }
      s.erase(s.begin() + s.rfind(wanted));
    }
    void eraseForMinimum(string& s, char wanted) {
      for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
        if (s[i] == wanted && s[i] > s[i + 1]) {
          s.erase(s.begin() + i);
          return;
        }
      }
      s.erase(s.begin() + s.rfind(wanted));
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        string s;
        cin >> s;
        eraseForMaximum(s, '0');
        eraseForMinimum(s, '1');
        cout << s << '\n';
      }
    }
    ```
