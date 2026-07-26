??? problem "LeetCode 1 · 两数之和"
    [打开原题 ↗](https://leetcode.cn/problems/two-sum/){ .problem-source }

    **题意**：在整数数组中找出两个不同下标，使对应元素之和等于 `target`；题目保证恰有一个答案。

    **思路**：从左到右扫描。查询补数 `target - nums[i]` 是否已出现，命中时返回更早下标与当前下标；未命中才记录当前值，避免重复使用同一位置。

    **复杂度**：期望时间 $O(n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<long long, int> pos;
        for (int i = 0; i < (int)nums.size(); ++i) {
          long long need = 1LL * target - nums[i];
          auto it = pos.find(need);
          if (it != pos.end()) return {it->second, i};
          pos[nums[i]] = i;
        }
        return {};
      }
    };
    ```
