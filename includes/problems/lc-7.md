<div class="problem-anchor" id="problem-lc-7"></div>

??? problem "LeetCode 7 · 整数反转"
    [打开原题 ↗](https://leetcode.cn/problems/reverse-integer/){ .problem-source }

    **难度与分值**：LeetCode 官方「中等」。

    **题意**：反转 32 位有符号整数的十进制数字，越界返回 0，且不能用 64 位整数暂存结果。

    **思路**：反复弹出末位并执行 `answer = answer * 10 + digit`；每次乘加前用边界商与末位余数精确判定是否溢出。

    **复杂度**：时间 $O(d)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      int reverse(int x) {
        int answer = 0;
        while (x != 0) {
          int digit = x % 10;
          x /= 10;
          if (answer > INT_MAX / 10 || (answer == INT_MAX / 10 && digit > 7)) {
            return 0;
          }
          if (answer < INT_MIN / 10 || (answer == INT_MIN / 10 && digit < -8)) {
            return 0;
          }
          answer = answer * 10 + digit;
        }
        return answer;
      }
    };
    ```
