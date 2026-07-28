<div class="problem-anchor" id="problem-atcoder-abc468-d"></div>

??? problem "AtCoder ABC468 D · Pre-Palindrome"
    [打开原题 ↗](https://atcoder.jp/contests/abc468/tasks/abc468_d?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 400 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 683（非官方，检索于 2026-07-29）。

    **题意**：统计字符串的非空连续子串中，至多改写一个字符后便能成为回文串的数量。

    **思路**：分别枚举奇、偶回文中心并向两侧扩展，累计镜像失配对数。失配至多一对时当前子串可行；出现第二对后，同一中心的更大子串也不再可行。

    **复杂度**：时间 $O(n^2)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      string s;
      cin >> s;
      int n = static_cast<int>(s.size());
      long long answer = 0;
      for (int center = 0; center < n; ++center) {
        int mismatches = 0;
        for (int left = center, right = center; left >= 0 && right < n; --left, ++right) {
          mismatches += s[left] != s[right];
          if (mismatches > 1) {
            break;
          }
          ++answer;
        }
      }
      for (int center = 0; center + 1 < n; ++center) {
        int mismatches = 0;
        for (int left = center, right = center + 1; left >= 0 && right < n; --left, ++right) {
          mismatches += s[left] != s[right];
          if (mismatches > 1) {
            break;
          }
          ++answer;
        }
      }
      cout << answer << '\n';
      return 0;
    }
    ```
