??? problem "LeetCode 3 · 无重复字符的最长子串"
    [打开原题 ↗](https://leetcode.cn/problems/longest-substring-without-repeating-characters/){ .problem-source }

    **题意**：求不包含重复字符的最长连续子串长度。

    **思路**：右指针扫描字符串，记录每个字符最近出现的位置；左边界直接跳到重复位置之后，并保证只向右移动。

    **复杂度**：时间 $O(n)$，字符集固定时额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      int lengthOfLongestSubstring(string s) {
        array<int, 256> last;
        last.fill(-1);
        int answer = 0, left = 0;
        for (int right = 0; right < (int)s.size(); ++right) {
          unsigned char c = s[right];
          left = max(left, last[c] + 1);
          last[c] = right;
          answer = max(answer, right - left + 1);
        }
        return answer;
      }
    };
    ```
