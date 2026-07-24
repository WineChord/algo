??? problem "LeetCode 5 · 最长回文子串"
    [打开原题 ↗](https://leetcode.cn/problems/longest-palindromic-substring/){ .problem-source }

    **题意**：求字符串中的最长回文连续子串。

    **思路**：每个回文串都有一个中心。依次把每个字符和每对相邻字符作为中心，向两侧扩展到失配为止，并维护最长区间；分别覆盖奇数长度和偶数长度回文。

    **复杂度**：时间 \(O(n^2)\)，额外空间 \(O(1)\)。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
        string longestPalindrome(string s) {
            int n=s.size(),best=0,len=1;
            auto go=[&](int l,int r){
                while(l>=0&&r<n&&s[l]==s[r]) l--,r++;
                if(r-l-1>len) best=l+1,len=r-l-1;
            };
            for(int i=0;i<n;i++) go(i,i),go(i,i+1);
            return s.substr(best,len);
        }
    };
    ```
