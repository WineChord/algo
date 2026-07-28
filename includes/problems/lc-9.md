<div class="problem-anchor" id="problem-lc-9"></div>

??? problem "LeetCode 9 · 回文数"
    [打开原题 ↗](https://leetcode.cn/problems/palindrome-number/){ .problem-source }

    **难度与分值**：LeetCode 官方「简单」。

    **题意**：不转换为字符串，判断一个 32 位有符号整数的十进制表示是否回文。

    **思路**：排除负数与非零末尾零，只反转十进制后半部分；偶数位比较两半，奇数位丢弃反转部分的中间位后比较。

    **复杂度**：时间 $O(\log x)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      bool isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
          return false;
        }
        int reversedHalf = 0;
        while (x > reversedHalf) {
          reversedHalf = reversedHalf * 10 + x % 10;
          x /= 10;
        }
        return x == reversedHalf || x == reversedHalf / 10;
      }
    };
    ```
