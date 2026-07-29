---
title: "[力扣 Top 9] LC 15 三数之和 中等"
---

# [力扣 Top 9] LC 15 三数之和 中等

<p class="daily-archive-kicker">2026-07-26 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/3sum/)
- 函数签名：`vector<vector<int>> threeSum(vector<int>& nums)`

### 原始题意

给定整数数组 `nums`，返回所有由三个不同下标构成、元素和为 0 的不重复数值三元组。三元组内部与结果顺序均不重要。

### 全部官方样例

1. `nums = [-1,0,1,2,-1,-4]`，输出 `[[-1,-1,2],[-1,0,1]]`。
2. `nums = [0,1,1]`，输出 `[]`。
3. `nums = [0,0,0]`，输出 `[[0,0,0]]`。

### 全部约束

- $3\le n\le 3000$
- $-10^5\le nums[i]\le 10^5$

## 最优结论

排序后枚举最小元素 `nums[i]`，在其右侧用相向双指针寻找和为 `-nums[i]` 的数对，并在三个层次跳过重复值。时间 $O(n^2)$，除排序栈和输出外空间 $O(1)$。在需要输出所有三元组时，最坏答案规模本身可达 $\Theta(n^2)$，因此该时间界已经输出最优。

## 约束、边界与观察

- 去重针对数值三元组，不是下标三元组；相同数值可来自不同位置。
- 排序把去重与二数之和的单调移动统一起来。
- 当 `nums[i] > 0` 时，右侧都不小于它，和不可能为 0，可提前结束。
- 三数和范围约为 $[-3\times10^5,3\times10^5]$，`int` 足够；推广到更大值域时用 `long long`。
- $n=3000$ 允许约 $9\times10^6$ 的二次扫描，三重枚举约 $2.7\times10^{10}$，不可行。

## 样例手推

排序后为 `[-4,-1,-1,0,1,2]`。`i=0` 时双指针找不到和 4；`i=1` 时先找到 `(-1,-1,2)`，跳过重复边界，再找到 `(-1,0,1)`；`i=2` 与前一个 `-1` 相同，整轮跳过，避免重复答案。

## 解法一：三重枚举加集合去重

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> threeSum(vector<int>& nums) {
    set<array<int, 3>> uniqueTriples;
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        for (int k = j + 1; k < n; ++k) {
          if (nums[i] + nums[j] + nums[k] != 0) continue;
          array<int, 3> triple{nums[i], nums[j], nums[k]};
          sort(triple.begin(), triple.end());
          uniqueTriples.insert(triple);
        }
      }
    }
    vector<vector<int>> ans;
    for (auto t : uniqueTriples) ans.push_back({t[0], t[1], t[2]});
    return ans;
  }
};
```

时间 $O(n^3\log K)$，空间 $O(K)$，其中 $K$ 为答案数。它可作为小规模 oracle。

## 解法二：固定一个数后使用哈希表

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> threeSum(vector<int>& nums) {
    set<array<int, 3>> uniqueTriples;
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
      unordered_set<int> seen;
      for (int j = i + 1; j < n; ++j) {
        int need = -nums[i] - nums[j];
        if (seen.contains(need)) {
          array<int, 3> triple{nums[i], nums[j], need};
          sort(triple.begin(), triple.end());
          uniqueTriples.insert(triple);
        }
        seen.insert(nums[j]);
      }
    }
    vector<vector<int>> ans;
    for (auto t : uniqueTriples) ans.push_back({t[0], t[1], t[2]});
    return ans;
  }
};
```

平均时间 $O(n^2\log K)$，空间 $O(n+K)$。它消除了第三层枚举，但仍需全局集合去重。

## 解法三：排序加双指针（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> ans;
    int n = nums.size();
    for (int i = 0; i + 2 < n; ++i) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      if (nums[i] > 0) break;
      int l = i + 1, r = n - 1;
      while (l < r) {
        long long sum = (long long)nums[i] + nums[l] + nums[r];
        if (sum < 0) {
          ++l;
        } else if (sum > 0) {
          --r;
        } else {
          ans.push_back({nums[i], nums[l], nums[r]});
          int leftValue = nums[l], rightValue = nums[r];
          while (l < r && nums[l] == leftValue) ++l;
          while (l < r && nums[r] == rightValue) --r;
        }
      }
    }
    return ans;
  }
};
```

### 正确性证明

固定排序后位置 `i`。双指针状态 `(l,r)` 若和小于 0，则在固定 `l` 时任何更小的右端只会使和更小，所以 `l` 不可能参与解，右移 `l` 安全；和大于 0 时对称地左移 `r`；和等于 0 时记录唯一数值三元组，并跳过相同边界值。该过程覆盖固定 `i` 的全部可行数对。外层跳过相同首值，所以同一数值三元组既不遗漏也不重复。

### 复杂度与选择

排序 $O(n\log n)$，每个 `i` 的双指针线性，总时间 $O(n^2)$；除输出和排序栈外空间 $O(1)$。哈希方案也可达平均 $O(n^2)$，但去重状态更复杂；面试优先排序双指针。

## 常见错误

- 找到答案后只移动一个指针，导致重复或死循环。
- 只跳过外层重复值，却不跳过左右边界重复值。
- 在未排序数组上使用“和小就右移左指针”的单调规则。
- 用下标去重而不是数值三元组去重。
- 把 `nums[i] >= 0` 作为提前结束，漏掉 `[0,0,0]`。

## Follow-up 1：目标和改为任意 `target`

双指针结构不变，只需比较三数和与 `target`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> threeSumTarget(vector<int> nums, long long target) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> ans;
    for (int i = 0; i + 2 < (int)nums.size(); ++i) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      int l = i + 1, r = nums.size() - 1;
      while (l < r) {
        long long sum = (long long)nums[i] + nums[l] + nums[r];
        if (sum < target) {
          ++l;
        } else if (sum > target) {
          --r;
        } else {
          ans.push_back({nums[i], nums[l], nums[r]});
          int a = nums[l], b = nums[r];
          while (l < r && nums[l] == a) ++l;
          while (l < r && nums[r] == b) --r;
        }
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间取决于排序。

## Follow-up 2：统计和为 0 的下标三元组数量

此时重复位置必须分别计数。排序后，找到左右值相加满足目标时按频次一次性累加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countThreeSumIndices(vector<int> nums) {
    sort(nums.begin(), nums.end());
    long long ans = 0;
    int n = nums.size();
    for (int i = 0; i + 2 < n; ++i) {
      int l = i + 1, r = n - 1;
      while (l < r) {
        long long sum = (long long)nums[i] + nums[l] + nums[r];
        if (sum < 0) {
          ++l;
        } else if (sum > 0) {
          --r;
        } else if (nums[l] == nums[r]) {
          long long count = r - l + 1;
          ans += count * (count - 1) / 2;
          break;
        } else {
          long long leftCount = 1, rightCount = 1;
          while (l + 1 < r && nums[l + 1] == nums[l]) {
            ++leftCount;
            ++l;
          }
          while (r - 1 > l && nums[r - 1] == nums[r]) {
            ++rightCount;
            --r;
          }
          ans += leftCount * rightCount;
          ++l;
          --r;
        }
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间取决于排序；答案使用 `long long`。

## Follow-up 3：最接近目标的三数和

对应 [LeetCode 16 · 最接近的三数之和](https://leetcode.cn/problems/3sum-closest/)。不再去重输出，而是在双指针过程中维护误差最小值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int threeSumClosest(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    long long best = (long long)nums[0] + nums[1] + nums[2];
    for (int i = 0; i + 2 < (int)nums.size(); ++i) {
      int l = i + 1, r = nums.size() - 1;
      while (l < r) {
        long long sum = (long long)nums[i] + nums[l] + nums[r];
        if (llabs(sum - target) < llabs(best - target)) best = sum;
        if (sum < target) {
          ++l;
        } else if (sum > target) {
          --r;
        } else {
          return target;
        }
      }
    }
    return (int)best;
  }
};
```

时间 $O(n^2)$，额外空间取决于排序。

## Follow-up 4：推广为四数之和

对应 [LeetCode 18 · 四数之和](https://leetcode.cn/problems/4sum/)。再固定一层，内层仍用双指针，并在两层与双指针处分别去重。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> fourSum(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> ans;
    int n = nums.size();
    for (int i = 0; i + 3 < n; ++i) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      for (int j = i + 1; j + 2 < n; ++j) {
        if (j > i + 1 && nums[j] == nums[j - 1]) continue;
        int l = j + 1, r = n - 1;
        while (l < r) {
          long long sum = (long long)nums[i] + nums[j] + nums[l] + nums[r];
          if (sum < target) {
            ++l;
          } else if (sum > target) {
            --r;
          } else {
            ans.push_back({nums[i], nums[j], nums[l], nums[r]});
            int a = nums[l], b = nums[r];
            while (l < r && nums[l] == a) ++l;
            while (l < r && nums[r] == b) --r;
          }
        }
      }
    }
    return ans;
  }
};
```

时间 $O(n^3)$，除输出和排序栈外空间 $O(1)$。

## 验证

随机生成长度 $3\ldots11$、值域 $[-6,6]$ 的数组，以三重枚举加集合为 oracle；把双指针输出的每个三元组排序，再将答案集合比较。覆盖全零、无解、大量重复、全正、全负和多组并列答案。

## Reference

- [官方题目](https://leetcode.cn/problems/3sum/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-8-lc128/">← [力扣 Top 8] LC 128 最长连续序列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-10-lc70/">[力扣 Top 10] LC 70 爬楼梯 简单 →</a>
</nav>
