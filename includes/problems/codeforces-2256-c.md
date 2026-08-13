<div class="problem-anchor" id="problem-codeforces-2256-c"></div>

??? problem "CF Round 1116 · Div.1 A / Div.2 C · Hot Potatoes at the Fairy Warehouse"
    [打开原题 ↗](https://codeforces.com/contest/2256/problem/C){ .problem-source }

    **难度与分值**：官方分值为 Div.1 A 500、Div.2 C 1500，两个 rating 字段均缺失；别名 tags 分别为 games/greedy/implementation 与 games（核对于 2026-08-14）。

    **题意**：两队成员交替坐成圆，持有者每轮可保留或在下一人轮初为空时顺时针传递；若干轮后按持有土豆的对方成员数计分，求双方最优分数。

    **思路**：土豆总数守恒使博弈零和。最后一轮的局部收益定义势函数 F；Red 的早期传递不增大 F，Blue 的早期传递不减小 F，所以全保留构成鞍点，只需对初态执行一次末轮环形贪心。

    **复杂度**：每组时间 O(n)，除输入串外空间 O(1)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <algorithm>
    #include <iostream>
    #include <string>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        long long k;
        string s;
        cin >> n >> k >> s;
        int m = 2 * n;
        int red = 0;
        int blue = 0;
        for (int i = 0; i < m; ++i) {
          if (s[i] == '0') continue;
          int next = (i + 1) % m;
          int final_position = s[next] == '0' ? next : i;
          if (final_position & 1) ++red;
          else ++blue;
        }
        cout << red << ' ' << blue << '\n';
      }
    }
    ```
