<div class="problem-anchor" id="problem-codeforces-2257-a"></div>

??? problem "Codeforces 2257A: Creating Abbreviations"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/A?locale=en){ .problem-source }

    **难度与分值**：官方分值 500；官方 rating 未给出；官方标签 strings（2026-08-18）

    **题意**：初始单词可重复使用并按首字母组成新缩写；判断给定的全部目标缩写能否按某种顺序创建。

    **思路**：可生成缩写的首字符在生成前已经可用，因此加入缩写不会扩大首字母集合。顺序无关，只需检查每个目标字符是否属于初始首字母集合。

    **复杂度**：时间 O(T)，其中 T 为全部字符串总长度；额外空间 O(1)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int testCount;
      cin >> testCount;
      while (testCount--) {
        int n, m;
        cin >> n >> m;
        unsigned int available = 0;
        for (int i = 0; i < n; ++i) {
          string word;
          cin >> word;
          available |= 1U << (word.front() - 'a');
        }
        bool possible = true;
        for (int i = 0; i < m; ++i) {
          string abbreviation;
          cin >> abbreviation;
          for (char letter : abbreviation) {
            if ((available & (1U << (letter - 'A'))) == 0) possible = false;
          }
        }
        cout << (possible ? "YES\n" : "NO\n");
      }
      return 0;
    }
    ```
