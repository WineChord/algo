??? problem "LeetCode 5 · 最长回文子串"
    [打开原题 ↗](https://leetcode.cn/problems/longest-palindromic-substring/){ .problem-source }

    **题意**：求字符串中的最长回文连续子串。

    **思路**：每个回文串都有一个中心。依次把每个字符和每对相邻字符作为中心，向两侧扩展到失配为止，并维护最长区间；分别覆盖奇数长度和偶数长度回文。

    **复杂度**：时间 $O(n^2)$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      string longestPalindrome(string s) {
        int n = s.size();
        int bestStart = 0, bestLength = 1;
        auto expand = [&](int left, int right) {
          while (left >= 0 && right < n && s[left] == s[right]) {
            --left;
            ++right;
          }
          int length = right - left - 1;
          if (length > bestLength) {
            bestStart = left + 1;
            bestLength = length;
          }
        };
        for (int center = 0; center < n; ++center) {
          expand(center, center);
          expand(center, center + 1);
        }
        return s.substr(bestStart, bestLength);
      }
    };
    ```
