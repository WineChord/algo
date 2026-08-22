<div class="problem-anchor" id="problem-atcoder-abc472-a"></div>

??? problem "AtCoder ABC472 A: A"
    [打开原题 ↗](https://atcoder.jp/contests/abc472/tasks/abc472_a?lang=en){ .problem-source }

    **难度与分值**：官方分值 100；AtCoder 未给出单题官方难度；AtCoder Problems 社区模型原始估算 -955，低分段界面校正后约 14（2026-08-23）

    **题意**：给定只含大写英文字母的字符串，保留其中的 `A`，把其他字符逐一替换为 `.`，输出等长结果。

    **思路**：每个输出位置只取决于同位置输入字符；原地扫描并按条件覆盖即可。

    **复杂度**：时间 $O(n)$，额外空间 $O(1)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      string s;
      cin >> s;
      for (char& character : s) {
        if (character != 'A') character = '.';
      }
      cout << s << '\n';
      return 0;
    }
    ```
