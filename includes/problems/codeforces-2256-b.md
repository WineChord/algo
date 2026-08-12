<div class="problem-anchor" id="problem-codeforces-2256-b"></div>

??? problem "CF Round 1116 · Div.2 B · Domino Tiles (2256B)"
    [打开原题 ↗](https://codeforces.com/contest/2256/problem/B){ .problem-source }

    **难度与分值**：Codeforces 官方 1000 分，rating 字段缺失，官方 tags 为 implementation、math（核对于 2026-08-13）。

    **题意**：把 0/1/? 串补成二进制串，使任意两块连续骨牌的相邻位之和不同，统计有效补全数。

    **思路**：相邻骨牌权重不同等价于 x_i≠x_(i+2)。二进制下这强制 x_(i+2)=1-x_i，因此前两位决定唯一的四周期串；检查四个候选与固定字符是否冲突即可。

    **复杂度**：每组时间 O(n)，空间 O(1)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
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
        string s;
        cin >> n >> s;
        int answer = 0;
        for (int mask = 0; mask < 4; ++mask) {
          bool valid = true;
          for (int i = 0; i < n; ++i) {
            int bit = ((mask >> (i & 1)) & 1) ^ ((i >> 1) & 1);
            if (s[i] != '?' && s[i] - '0' != bit) {
              valid = false;
              break;
            }
          }
          answer += valid;
        }
        cout << answer << '\n';
      }
    }
    ```
