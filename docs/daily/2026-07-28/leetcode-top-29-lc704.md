---
title: "[力扣 Top 29] LC 704 二分查找 简单"
---

# [力扣 Top 29] LC 704 二分查找 简单

<p class="daily-archive-kicker">2026-07-28 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

## 官方原始信息

- 官方链接：[打开官方页面](https://leetcode.cn/problems/binary-search/)
- slug：`binary-search`
- 官方难度：简单；官方竞赛分未提供；ZeroTracer 数据集无记录。
- 函数签名：`int search(vector<int>& nums, int target)`
- 题意：在严格升序整数数组中查找 `target`，存在则返回其下标，否则返回 `-1`；要求 $O(\log n)$。
- 样例 1：`nums=[-1,0,3,5,9,12], target=9`，输出 `4`。
- 样例 2：同数组、`target=2`，输出 `-1`。
- 约束：$1\le n\le10000$；元素互不相同且升序；$-9999\le nums[i]\le9999$。

要求显式排除了线性扫描作为最终解。中点必须用 `left+(right-left)/2`，以便迁移到更大下标范围时规避加法溢出。

## 解法一：线性扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int search(vector<int>& nums, int target) {
    for (int i = 0; i < (int)nums.size(); ++i) {
      if (nums[i] == target) return i;
    }
    return -1;
  }
};
```

时间 $O(n)$，空间 $O(1)$，正确但不满足题目复杂度。

## 解法二：闭区间二分

维护答案若存在则位于 `[left,right]`。比较后必须排除 `middle`，因此更新为 `middle+1` 或 `middle-1`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int search(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left <= right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] == target) return middle;
      if (nums[middle] < target) left = middle + 1;
      else right = middle - 1;
    }
    return -1;
  }
};
```

时间 $O(\log n)$，空间 $O(1)$。

## 推荐统一模板：半开区间找首个 `>= target`

维护 `[left,right)`，其中 `[0,left)` 全部 `<target`，`[right,n)` 全部 `>=target`。循环结束时 `left=right` 是第一个 `>=target` 的位置，再检查是否等于目标。它把精确查找、lower_bound、边界查找统一为一个不变量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int search(vector<int>& nums, int target) {
    int left = 0, right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] >= target) right = middle;
      else left = middle + 1;
    }
    return left < (int)nums.size() && nums[left] == target ? left : -1;
  }
};
```

每轮区间严格缩小；终止时分界唯一，因此正确。时间 $O(\log n)$，空间 $O(1)$。

边界：目标小于首元素时返回 `-1`；大于尾元素时 `left=n`；单元素数组仍成立。常见错误：闭区间却初始化 `right=n`；半开区间更新 `right=middle-1`；循环用 `left<=right` 与半开区间混搭；结束后未检查 `left<n`；数组无序仍套二分。

## Follow-up 1：重复元素的首尾位置

新定义：数组非递减，返回目标第一次和最后一次出现的位置。分别求 `lower_bound(target)` 与 `lower_bound(target+1)`；为避免 `target+1` 溢出，写独立 upper bound。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int lowerBound(vector<int>& nums, int target) {
    int left = 0, right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] >= target) right = middle;
      else left = middle + 1;
    }
    return left;
  }
  int upperBound(vector<int>& nums, int target) {
    int left = 0, right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] > target) right = middle;
      else left = middle + 1;
    }
    return left;
  }
public:
  vector<int> searchRange(vector<int>& nums, int target) {
    int first = lowerBound(nums, target);
    if (first == (int)nums.size() || nums[first] != target) return {-1, -1};
    return {first, upperBound(nums, target) - 1};
  }
};
```

时间 $O(\log n)$，空间 $O(1)$。

## Follow-up 2：旋转升序数组中查找

新定义：严格升序数组在未知位置旋转。全局不再有单一分界，但每轮至少一半仍有序；判断目标是否落在有序半段。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int searchRotated(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left <= right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] == target) return middle;
      if (nums[left] <= nums[middle]) {
        if (nums[left] <= target && target < nums[middle]) right = middle - 1;
        else left = middle + 1;
      } else {
        if (nums[middle] < target && target <= nums[right]) left = middle + 1;
        else right = middle - 1;
      }
    }
    return -1;
  }
};
```

时间 $O(\log n)$，空间 $O(1)$；若允许大量重复值，最坏可能退化为 $O(n)$。

## Follow-up 3：长度未知、只能通过越界返回无穷大的接口读取

新定义：不能直接取得 `n`。先指数扩张找到包含目标的上界，再在该范围二分。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class UnknownArray {
  vector<int> data;
public:
  explicit UnknownArray(vector<int> values) : data(std::move(values)) {}
  int get(int index) const {
    return index < (int)data.size() ? data[index] : INT_MAX;
  }
};
class Solution {
public:
  int searchUnknown(const UnknownArray& reader, int target) {
    int right = 1;
    while (reader.get(right) < target && right <= INT_MAX / 2) right *= 2;
    int left = right / 2;
    while (left <= right) {
      int middle = left + (right - left) / 2;
      int value = reader.get(middle);
      if (value == target) return middle;
      if (value < target) left = middle + 1;
      else right = middle - 1;
    }
    return -1;
  }
};
```

若答案位置为 `p`，时间 $O(\log(p+1))$，空间 $O(1)$。

## Follow-up 4：二分答案——最小可行容量

新定义：货物按顺序运输，要求 `days` 天内运完，求最小船容量。查找对象不再是数组元素，而是满足“容量可行”的单调谓词。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool feasible(vector<int>& weights, int days, long long capacity) {
    int used = 1;
    long long load = 0;
    for (int weight : weights) {
      if (load + weight > capacity) {
        ++used;
        load = 0;
      }
      load += weight;
    }
    return used <= days;
  }
public:
  int shipWithinDays(vector<int>& weights, int days) {
    long long left = *max_element(weights.begin(), weights.end());
    long long right = accumulate(weights.begin(), weights.end(), 0LL);
    while (left < right) {
      long long middle = left + (right - left) / 2;
      if (feasible(weights, days, middle)) right = middle;
      else left = middle + 1;
    }
    return (int)left;
  }
};
```

设总重量为 $S$，时间 $O(n\log S)$，空间 $O(1)$。

## Follow-up 5：降序数组查找

新定义：数组严格降序。只有比较方向改变，不变量改为左侧元素都大于目标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int searchDescending(vector<int>& nums, int target) {
    int left = 0, right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] <= target) right = middle;
      else left = middle + 1;
    }
    return left < (int)nums.size() && nums[left] == target ? left : -1;
  }
};
```

时间 $O(\log n)$，空间 $O(1)$。

## 可复现验证

随机生成互异升序数组，将推荐模板与 `std::find` 对拍；重复数组的范围查询与线性首尾扫描对拍；旋转数组与线性查找对拍。结果见 `validation-report.json`。

## Reference

- [官方题目](https://leetcode.cn/problems/binary-search/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-28-lc25/">← [力扣 Top 28] LC 25 K 个一组翻转链表 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-30-lc14/">[力扣 Top 30] LC 14 最长公共前缀 简单 →</a>
</nav>
