<div class="problem-anchor" id="problem-lc-6"></div>

??? problem "LeetCode 6 · Z 字形变换"
    [打开原题 ↗](https://leetcode.cn/problems/zigzag-conversion/){ .problem-source }

    **难度与分值**：LeetCode 官方「中等」。

    **题意**：把字符串按指定行数写成 Z 字形，再逐行读出。

    **思路**：周期为 $2r-2$；逐行枚举竖列字符，并在中间行补上周期内对称的斜线字符。

    **复杂度**：时间 $O(n)$，除结果外额外空间 $O(1)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      string convert(string s, int numRows) {
        if (numRows == 1 || numRows >= static_cast<int>(s.size())) {
          return s;
        }
        int period = 2 * numRows - 2;
        string answer;
        answer.reserve(s.size());
        for (int row = 0; row < numRows; ++row) {
          for (int base = row; base < static_cast<int>(s.size()); base += period) {
            answer.push_back(s[base]);
            int diagonal = base + period - 2 * row;
            if (row != 0 && row != numRows - 1 && diagonal < static_cast<int>(s.size())) {
              answer.push_back(s[diagonal]);
            }
          }
        }
        return answer;
      }
    };
    int main() {
    }
    ```
