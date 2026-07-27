??? problem "LeetCode 4 · 寻找两个正序数组的中位数"
    [打开原题 ↗](https://leetcode.cn/problems/median-of-two-sorted-arrays/){ .problem-source }

    **难度**：LeetCode 官方「困难」。

    **题意**：给定两个非递减数组，在官方要求的对数时间内求合并序列的中位数。

    **思路**：只在较短数组上二分切分位置，使左右两半元素数固定且两条交叉边界均有序。合法切分处，左半最大值与右半最小值直接决定中位数。

    **复杂度**：时间 $O(\log\min(m,n))$，额外空间 $O(1)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.size(), n = nums2.size();
        int half = (m + n + 1) / 2;
        int low = 0, high = m;
        while (low <= high) {
          int i = low + (high - low) / 2;
          int j = half - i;
          int leftA = i == 0 ? INT_MIN : nums1[i - 1];
          int rightA = i == m ? INT_MAX : nums1[i];
          int leftB = j == 0 ? INT_MIN : nums2[j - 1];
          int rightB = j == n ? INT_MAX : nums2[j];
          if (leftA <= rightB && leftB <= rightA) {
            int leftMax = max(leftA, leftB);
            if ((m + n) % 2 == 1) return leftMax;
            int rightMin = min(rightA, rightB);
            return (static_cast<long long>(leftMax) + rightMin) / 2.0;
          }
          if (leftA > rightB) high = i - 1;
          else low = i + 1;
        }
        return 0.0;
      }
    };
    ```
