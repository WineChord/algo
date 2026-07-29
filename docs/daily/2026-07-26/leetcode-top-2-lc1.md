---
title: "[力扣 Top 2] LC 1 两数之和 简单"
---

# [力扣 Top 2] LC 1 两数之和 简单

<p class="daily-archive-kicker">2026-07-26 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../data-structures/hash-and-cache.md">进入知识专题</a></p>

## 官方原始信息

- 难度：简单
- 官方链接：https://leetcode.cn/problems/two-sum/
- 函数签名：`vector<int> twoSum(vector<int>& nums, int target)`

### 原始题意

给定整数数组 `nums` 和目标值 `target`，找出两个不同下标，使对应元素之和等于目标值，并返回这两个下标。每组输入恰有一个有效答案，答案下标顺序不限。

### 全部官方样例

1. `nums = [2,7,11,15], target = 9`，输出 `[0,1]`。
2. `nums = [3,2,4], target = 6`，输出 `[1,2]`。
3. `nums = [3,3], target = 6`，输出 `[0,1]`；两个相等的值来自不同下标。

### 全部约束

- $2\le nums.length\le 10^4$
- $-10^9\le nums[i]\le 10^9$
- $-10^9\le target\le 10^9$
- 恰有一个有效答案
- 不能重复使用同一个元素

## 最优结论

从左到右扫描。处理下标 $i$ 时，只在哈希表中保存更早下标对应的值；先查 `target - nums[i]`，命中即得到两个不同下标，再插入当前值。期望时间 $O(n)$，额外空间 $O(n)$。这是面试中优先记忆的方案；若输入已排序，则双指针能把额外空间降为 $O(1)$。

## 约束、边界与关键观察

- 暴力枚举的是下标对 $(i,j)$，共有 $O(n^2)$ 个。
- 对固定的 `nums[i]`，另一个值被唯一确定为 `target - nums[i]`；瓶颈从“枚举另一个下标”转为“快速查补数”。
- 必须先查询后插入，否则 `target == 2 * nums[i]` 时可能错误地使用同一下标两次。
- 重复值合法，样例 `[3,3]` 说明哈希表应保存出现过的下标，而不是去重后丢失位置信息。
- 官方数值范围下两数和仍在 32 位有符号整数内；实现中使用 `long long` 计算补数可让边界意图更清楚。

## 样例手推

对 `[3,2,4]`、目标 $6$：扫描到 $3$ 时补数也是 $3$，表为空，插入 `3 -> 0`；扫描到 $2$ 时查 $4$ 未命中，插入 `2 -> 1`；扫描到 $4$ 时查 $2$，得到早先下标 $1$，返回 `[1,2]`。

## 解法一：双重枚举

枚举所有 $i<j$，因此不会重复使用元素，也一定覆盖唯一答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> twoSum(vector<int>& nums, int target) {
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        if (nums[i] + nums[j] == target) return {i, j};
      }
    }
    return {};
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。当 $n=10^4$ 时约需检查五千万个下标对，已经没有必要。

## 解法二：排序后双指针

把值和原下标绑定后排序。当前和过小就增大左值，过大就减小右值；有序性让一次移动排除一整批不可能的组合。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> twoSum(vector<int>& nums, int target) {
    vector<pair<int, int>> a;
    for (int i = 0; i < (int)nums.size(); ++i) a.push_back({nums[i], i});
    sort(a.begin(), a.end());
    int l = 0, r = (int)a.size() - 1;
    while (l < r) {
      long long sum = 1LL * a[l].first + a[r].first;
      if (sum < target)
        ++l;
      else if (sum > target)
        --r;
      else
        return {a[l].second, a[r].second};
    }
    return {};
  }
};
```

时间 $O(n\log n)$，额外空间 $O(n)$。优点是最坏复杂度稳定；缺点是比哈希慢，并且要额外保存原下标。

## 解法三：单遍哈希（最佳实用解）

<!-- compile:leetcode -->
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

### 正确性证明

假设唯一答案下标为 $i<j$。扫描到 $j$ 前，算法已经把 `nums[i]` 及其下标放入表中；此时计算的补数恰为 `target - nums[j] = nums[i]`，查询必然命中并返回 $(i,j)$。算法只查询更早下标，所以两个下标一定不同；若提前返回其他下标对，该对同样满足目标和，与题意的唯一性并不冲突。

### 复杂度与方案比较

- 暴力：$O(n^2)$，空间最少，可做 oracle。
- 排序双指针：$O(n\log n)$，最坏复杂度稳定，适合不信任哈希或输入已排序。
- 单遍哈希：期望 $O(n)$、空间 $O(n)$，代码短且保留下标，最推荐。

## 常见错误

- 先插入当前值再查补数，导致同一下标被用两次。
- 只保存布尔“出现过”，却忘记题目要求返回下标。
- 用 `set` 去重，破坏 `[3,3]` 这类答案。
- 排序原数组后直接返回排序后下标。
- 把“恰有一个答案”误解为数组中没有重复值。

## Follow-up 1：返回所有下标对

不再保证答案唯一。扫描右端点 $j$，把补数此前出现的所有下标都与 $j$ 配对；输出规模本身可能达到 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<pair<int, int>> allPairs(vector<int>& nums, int target) {
    unordered_map<long long, vector<int>> pos;
    vector<pair<int, int>> ans;
    for (int j = 0; j < (int)nums.size(); ++j) {
      long long need = 1LL * target - nums[j];
      auto it = pos.find(need);
      if (it != pos.end()) {
        for (int i : it->second) ans.push_back({i, j});
      }
      pos[nums[j]].push_back(j);
    }
    return ans;
  }
};
```

期望时间 $O(n+\text{答案数})$，空间 $O(n)$。

## Follow-up 2：只统计下标对数量

不必保存每个下标，只维护此前每个值的出现次数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countPairs(vector<int>& nums, int target) {
    unordered_map<long long, long long> count;
    long long ans = 0;
    for (int x : nums) {
      ans += count[1LL * target - x];
      ++count[x];
    }
    return ans;
  }
};
```

期望时间 $O(n)$，空间 $O(n)$。

## Follow-up 3：输入已经非降序排列

对应 [LeetCode 167 · 两数之和 II](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/)。利用有序性使用相向双指针，并按题目要求返回一基下标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> twoSum(vector<int>& numbers, int target) {
    int l = 0, r = (int)numbers.size() - 1;
    while (l < r) {
      long long sum = 1LL * numbers[l] + numbers[r];
      if (sum < target)
        ++l;
      else if (sum > target)
        --r;
      else
        return {l + 1, r + 1};
    }
    return {};
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## Follow-up 4：在线支持 `add` 与 `find`

数据逐个到来，查询时判断当前集合中是否存在两数和。用频次表存数据；`add` 期望 $O(1)$，`find` 枚举不同值，期望 $O(u)$，其中 $u$ 是不同值数量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class TwoSum {
  unordered_map<long long, int> count;
public:
  void add(int number) {
    ++count[number];
  }
  bool find(int value) {
    for (auto [x, c] : count) {
      long long y = 1LL * value - x;
      auto it = count.find(y);
      if (it == count.end()) continue;
      if (x != y || c >= 2) return true;
    }
    return false;
  }
};
```

空间 $O(u)$。若查询远多于插入，也可以在 `add` 时预计算所有可达和，以增加插入成本换取 $O(1)$ 查询。

## Reference

- 官方题面与接口：https://leetcode.cn/problems/two-sum/

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/two-sum/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-1-lc3286.md">← [力扣 Top 1] LC 3286 穿越网格图的安全路径 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-3-lc3.md">[力扣 Top 3] LC 3 无重复字符的最长子串 中等 →</a>
</nav>
