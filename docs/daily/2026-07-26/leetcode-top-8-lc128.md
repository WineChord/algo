---
title: "[力扣 Top 8] LC 128 最长连续序列 中等"
---

# [力扣 Top 8] LC 128 最长连续序列 中等

<p class="daily-archive-kicker">2026-07-26 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/longest-consecutive-sequence/)
- 函数签名：`int longestConsecutive(vector<int>& nums)`

### 原始题意

给定未排序整数数组 `nums`，找出由数值连续的整数构成的最长序列长度。序列元素不要求在原数组中相邻，重复值只代表同一个整数。要求设计 $O(n)$ 时间算法。

### 全部官方样例

1. `nums = [100,4,200,1,3,2]`，输出 `4`，最长序列为 `[1,2,3,4]`。
2. `nums = [0,3,7,2,5,8,4,6,0,1]`，输出 `9`。
3. `nums = [1,0,1,2]`，输出 `3`。

### 全部约束

- $0\le n\le 10^5$
- $-10^9\le nums[i]\le 10^9$

## 最优结论

把所有值放入哈希集合。只有当 `x - 1` 不存在时，`x` 才是某条连续序列的起点；从这些起点向右枚举。每个不同值最多作为一次起点检查，并且只会在所属序列的唯一扩张中被访问一次，平均时间 $O(n)$，空间 $O(n)$。

## 约束、边界与观察

- 空数组答案为 0。
- 重复值必须先去重，否则排序扫描或计数会把重复项误算进长度。
- 值域跨度可达 $2\times10^9$，不能开值域数组。
- 对 `INT_MIN` 计算 `x - 1`、对 `INT_MAX` 计算 `x + 1` 会溢出；使用 `long long` 集合或显式边界判断。
- 若从每个值都向右扩张，长连续段会被重复扫描成 $O(n^2)$；“只从起点扩张”是线性的关键。

## 样例手推

集合 `{100,4,200,1,3,2}` 中，`100`、`200`、`1` 的前驱不存在，都是起点。前两条长度为 1；从 `1` 依次找到 `2,3,4`，长度为 4，因此答案为 4。

## 解法一：从每个元素线性查找后继

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestConsecutive(vector<int>& nums) {
    int ans = 0;
    for (int x : nums) {
      long long y = x;
      int len = 0;
      while (find(nums.begin(), nums.end(), y) != nums.end()) {
        ++len;
        ++y;
      }
      ans = max(ans, len);
    }
    return ans;
  }
};
```

最坏时间 $O(n^2)$，空间 $O(1)$。它既重复做成员查询，也从序列内部重复扩张。

## 解法二：排序后扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestConsecutive(vector<int>& nums) {
    if (nums.empty()) return 0;
    sort(nums.begin(), nums.end());
    int ans = 1, current = 1;
    for (int i = 1; i < (int)nums.size(); ++i) {
      if (nums[i] == nums[i - 1]) continue;
      if ((long long)nums[i] == (long long)nums[i - 1] + 1) {
        ++current;
      } else {
        current = 1;
      }
      ans = max(ans, current);
    }
    return ans;
  }
};
```

时间 $O(n\log n)$，额外空间依排序实现而定；它稳定易写，但不满足题目明确要求的 $O(n)$。

## 解法三：哈希集合只从起点扩张（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestConsecutive(vector<int>& nums) {
    unordered_set<long long> values(nums.begin(), nums.end());
    int ans = 0;
    for (long long x : values) {
      if (values.contains(x - 1)) continue;
      long long y = x;
      while (values.contains(y)) ++y;
      ans = max(ans, (int)(y - x));
    }
    return ans;
  }
};
```

### 正确性证明

任意最大连续段可唯一写成 $[a,a+1,\ldots,b]$，其中 $a-1$ 不在集合。算法遍历到 $a$ 时不会跳过，并从 $a$ 连续扩张到第一个缺失值 $b+1$，得到准确长度 $b-a+1$。段内其他值都有前驱，因此不会重复启动扩张。每条连续段都被处理且只被处理一次，取最大长度即为答案。

### 复杂度与选择

建集合平均 $O(n)$；起点检查与全部扩张合计平均 $O(n)$，空间 $O(n)$。哈希退化时理论最坏可达 $O(n^2)$；若必须保证最坏界，排序法提供确定的 $O(n\log n)$。

## 常见错误

- 从每个值都扩张，误以为集合查询 $O(1)$ 就能保证总复杂度 $O(n)$。
- 重复值使排序扫描的当前长度多加 1。
- 空数组仍把答案初始化为 1。
- 在 `INT_MIN`/`INT_MAX` 附近做有符号整数溢出。
- 遍历集合时插入或删除元素，导致迭代器失效。

## Follow-up 1：返回一条最长连续序列

记录最佳起点和长度，最后按数值恢复。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> longestConsecutiveValues(vector<int>& nums) {
    unordered_set<long long> values(nums.begin(), nums.end());
    long long bestStart = 0;
    int bestLen = 0;
    for (long long x : values) {
      if (values.contains(x - 1)) continue;
      long long y = x;
      while (values.contains(y)) ++y;
      int len = y - x;
      if (len > bestLen || (len == bestLen && x < bestStart)) {
        bestStart = x;
        bestLen = len;
      }
    }
    vector<int> ans;
    for (int i = 0; i < bestLen; ++i) ans.push_back((int)(bestStart + i));
    return ans;
  }
};
```

平均时间 $O(n+\text{答案长度})$，空间 $O(n)$。

## Follow-up 2：只插入的新值流，随时查询最长长度

只在区间边界保存长度。插入新值 `x` 时读取相邻区间长度并合并，更新新大区间两端。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class ConsecutiveStream {
  unordered_map<long long, int> boundaryLength;
  unordered_set<long long> present;
  int best = 0;
public:
  int add(long long x) {
    if (present.contains(x)) return best;
    present.insert(x);
    int left = boundaryLength.contains(x - 1) ? boundaryLength[x - 1] : 0;
    int right = boundaryLength.contains(x + 1) ? boundaryLength[x + 1] : 0;
    int len = left + 1 + right;
    boundaryLength[x] = len;
    boundaryLength[x - left] = len;
    boundaryLength[x + right] = len;
    best = max(best, len);
    return best;
  }
};
```

每次插入平均 $O(1)$，空间 $O(q)$。若允许删除，区间可能被劈开，此结构不能直接维护。

## Follow-up 3：允许任意插入和删除

用有序不交区间映射保存每个连续段，并用多重集合维护段长。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicConsecutive {
  map<long long, long long> intervals;
  multiset<long long> lengths;
  void addLength(long long l, long long r) {
    lengths.insert(r - l + 1);
  }
  void eraseLength(long long l, long long r) {
    lengths.erase(lengths.find(r - l + 1));
  }
public:
  void insert(long long x) {
    auto right = intervals.upper_bound(x);
    auto left = right == intervals.begin() ? intervals.end() : prev(right);
    if (left != intervals.end() && left->second >= x) return;
    bool joinLeft = left != intervals.end() && left->second + 1 == x;
    bool joinRight = right != intervals.end() && right->first - 1 == x;
    if (joinLeft && joinRight) {
      long long l = left->first, r = right->second;
      eraseLength(left->first, left->second);
      eraseLength(right->first, right->second);
      intervals.erase(right);
      left->second = r;
      addLength(l, r);
    } else if (joinLeft) {
      long long l = left->first;
      eraseLength(left->first, left->second);
      left->second = x;
      addLength(l, x);
    } else if (joinRight) {
      long long r = right->second;
      eraseLength(right->first, right->second);
      intervals.erase(right);
      intervals[x] = r;
      addLength(x, r);
    } else {
      intervals[x] = x;
      addLength(x, x);
    }
  }
  void erase(long long x) {
    auto it = intervals.upper_bound(x);
    if (it == intervals.begin()) return;
    --it;
    long long l = it->first, r = it->second;
    if (x < l || x > r) return;
    eraseLength(l, r);
    intervals.erase(it);
    if (l <= x - 1) {
      intervals[l] = x - 1;
      addLength(l, x - 1);
    }
    if (x + 1 <= r) {
      intervals[x + 1] = r;
      addLength(x + 1, r);
    }
  }
  long long query() const {
    return lengths.empty() ? 0 : *lengths.rbegin();
  }
};
```

每次插入、删除为 $O(\log q)$，查询最大长度 $O(1)$，空间 $O(q)$。

## Follow-up 4：区间内部最多允许缺一个数

排序去重后用滑动窗口维护 `跨度 - 已有数量 <= 1`；窗口两端均为已存在值，答案是覆盖跨度。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestWithAtMostOneHole(vector<int> nums) {
    if (nums.empty()) return 0;
    sort(nums.begin(), nums.end());
    nums.erase(unique(nums.begin(), nums.end()), nums.end());
    int ans = 1, l = 0;
    for (int r = 0; r < (int)nums.size(); ++r) {
      while ((long long)nums[r] - nums[l] + 1 - (r - l + 1) > 1) ++l;
      ans = max(ans, nums[r] - nums[l] + 1);
    }
    return ans;
  }
};
```

时间 $O(n\log n)$，空间取决于排序。允许一个缺口后，“只从前驱不存在处扩张”不再足以描述窗口，模型变为排序后的双指针。

## 验证

对长度 $0\ldots12$、值域 $[-8,8]$ 的随机数组，以排序去重扫描为 oracle，与哈希起点法比较。专门覆盖全重复、单条长序列、多条并列序列、空数组以及 `INT_MIN`、`INT_MAX`。

## Reference

- [官方题目](https://leetcode.cn/problems/longest-consecutive-sequence/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-7-lc5/">← [力扣 Top 7] LC 5 最长回文子串 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-9-lc15/">[力扣 Top 9] LC 15 三数之和 中等 →</a>
</nav>
