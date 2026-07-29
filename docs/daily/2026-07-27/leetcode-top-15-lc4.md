---
title: "[力扣 Top 15] LC 4 寻找两个正序数组的中位数 困难"
---

# [力扣 Top 15] LC 4 寻找两个正序数组的中位数 困难

<p class="daily-archive-kicker">2026-07-27 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-27 题目列表</a> · <a href="../../basics/binary-search.md">进入知识专题</a></p>

官方题目：https://leetcode.cn/problems/median-of-two-sorted-arrays/

## 官方原始信息

- 题号：4
- 官方中文标题：寻找两个正序数组的中位数
- 官方英文标题：Median of Two Sorted Arrays
- slug：`median-of-two-sorted-arrays`
- 官方难度：困难
- 函数签名：`double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2)`
- 官方要求：算法时间复杂度应为 $O(\log(m+n))$
- 官方竞赛归属与分值：未发现官方竞赛归属，官方分值未知
- ZeroTracer 社区估算竞赛分：无。2026-07-27 检索公开 `data.json`，该 slug 不在数据集中

### 原始题意

给定两个分别长为 $m,n$ 的非递减数组，返回二者合并后的中位数。总长度为奇数时，中位数是正中元素；总长度为偶数时，是中间两个元素的平均值。

### 全部官方样例

1. `nums1 = [1,3], nums2 = [2]`，输出 `2.00000`；合并序列为 `[1,2,3]`。
2. `nums1 = [1,2], nums2 = [3,4]`，输出 `2.50000`；中间两数为 2 与 3。

### 全部官方约束

- `nums1.length == m`
- `nums2.length == n`
- $0\le m,n\le1000$
- $1\le m+n\le2000$
- $-10^6\le nums1[i],nums2[i]\le10^6$

## 约束推导、样例与边界

$m+n\le2000$ 使线性合并足以通过，但官方显式要求对数时间，因此目标不是“能过”，而是利用两个数组均已排序，只定位中位线两侧的边界。若在较短数组中选择左半部分取 $i$ 个元素，则另一数组必须取 $j=\lfloor(m+n+1)/2\rfloor-i$ 个；只需寻找使两边有序的唯一分割区间。

样例 2 中总长度 4，左半应有 2 个元素。若从 `[1,2]` 左侧取 2 个、从 `[3,4]` 取 0 个，则左侧最大 2 不大于右侧最小 3，分割合法，中位数为 $(2+3)/2=2.5$。

边界：

- 一个数组为空：答案就是另一个数组的中位数。
- 两数组长度差异巨大：必须在较短数组上二分，才能保证另一侧分割下标合法。
- 重复值：合法分割条件必须用 `<=`，不能用 `<`。
- 极端负值与正值：哨兵只表示越界，不参与实际数组存储。
- 偶数长度求平均时先转 `long long` 或 `double` 再相加，避免通用值域下整数溢出。

## 解法一：完整归并

按归并排序的合并步骤生成整个有序数组，再读取中间位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> merged;
    merged.reserve(nums1.size() + nums2.size());
    int i = 0, j = 0;
    while (i < static_cast<int>(nums1.size()) || j < static_cast<int>(nums2.size())) {
      if (j == static_cast<int>(nums2.size()) || (i < static_cast<int>(nums1.size()) && nums1[i] <= nums2[j])) {
        merged.push_back(nums1[i++]);
      } else {
        merged.push_back(nums2[j++]);
      }
    }
    int n = merged.size();
    if (n % 2 == 1) return merged[n / 2];
    return (static_cast<long long>(merged[n / 2 - 1]) + merged[n / 2]) / 2.0;
  }
};
```

时间 $O(m+n)$，空间 $O(m+n)$。它清晰可靠，却生成了中位数之后永远不会使用的后半段。

## 解法二：归并到中间位置

只维护最近取出的两个数，归并到下标 $\lfloor(m+n)/2\rfloor$ 即停止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    int total = nums1.size() + nums2.size();
    int i = 0, j = 0, prev = 0, cur = 0;
    for (int step = 0; step <= total / 2; ++step) {
      prev = cur;
      if (j == static_cast<int>(nums2.size()) || (i < static_cast<int>(nums1.size()) && nums1[i] <= nums2[j])) {
        cur = nums1[i++];
      } else {
        cur = nums2[j++];
      }
    }
    if (total % 2 == 1) return cur;
    return (static_cast<long long>(prev) + cur) / 2.0;
  }
};
```

时间仍是 $O(m+n)$，额外空间降为 $O(1)$。瓶颈变成逐个跳过左半元素；排序性质还能一次排除一批。

## 解法三：第 $k$ 小元素的批量淘汰

要找第 $k$ 小元素，每次比较两个数组各自第 $k/2$ 个尚未淘汰元素。较小者及其之前的元素不可能跨过第 $k$ 位，可整批删除。奇偶总长度分别查询一个或两个秩。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int kth(const vector<int>& a, const vector<int>& b, int k) {
    int i = 0, j = 0;
    while (true) {
      if (i == static_cast<int>(a.size())) return b[j + k - 1];
      if (j == static_cast<int>(b.size())) return a[i + k - 1];
      if (k == 1) return min(a[i], b[j]);
      int takeA = min(k / 2, static_cast<int>(a.size()) - i);
      int takeB = min(k / 2, static_cast<int>(b.size()) - j);
      if (a[i + takeA - 1] <= b[j + takeB - 1]) {
        i += takeA;
        k -= takeA;
      } else {
        j += takeB;
        k -= takeB;
      }
    }
  }
public:
  double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    int total = nums1.size() + nums2.size();
    int left = kth(nums1, nums2, (total + 1) / 2);
    int right = kth(nums1, nums2, (total + 2) / 2);
    return (static_cast<long long>(left) + right) / 2.0;
  }
};
```

每次至少淘汰当前 $k$ 的常数比例；时间 $O(\log(m+n))$，空间 $O(1)$。它直接推广到任意第 $k$ 小查询，但边界分支较多。

## 解法四：较短数组上的二分分割（最佳实用解）

令 `a` 为较短数组。左半总元素数固定为 `half = (m + n + 1) / 2`。二分 `i`，令 `j = half - i`，寻找

$$
a[i-1]\le b[j],\qquad b[j-1]\le a[i].
$$

越过数组边界时用正负无穷哨兵。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);
    int m = nums1.size(), n = nums2.size();
    int half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
      int i = lo + (hi - lo) / 2;
      int j = half - i;
      int aLeft = i == 0 ? INT_MIN : nums1[i - 1];
      int aRight = i == m ? INT_MAX : nums1[i];
      int bLeft = j == 0 ? INT_MIN : nums2[j - 1];
      int bRight = j == n ? INT_MAX : nums2[j];
      if (aLeft <= bRight && bLeft <= aRight) {
        int leftMax = max(aLeft, bLeft);
        if ((m + n) % 2 == 1) return leftMax;
        int rightMin = min(aRight, bRight);
        return (static_cast<long long>(leftMax) + rightMin) / 2.0;
      }
      if (aLeft > bRight) {
        hi = i - 1;
      } else {
        lo = i + 1;
      }
    }
    return 0.0;
  }
};
```

### 正确性证明

`i+j=half` 保证分割左边恰有中位数所需的元素个数。两个数组各自有序，所以只要左侧的两个最大候选均不超过右侧的两个最小候选，即上述交叉不等式成立，左侧所有元素都不大于右侧所有元素：奇数总长时左侧最大值就是中位数，偶数总长时再与右侧最小值取平均。

若 `aLeft > bRight`，从 `a` 取入左半的元素过多，增大 `i` 只会让 `aLeft` 不降、`bRight` 不升，因此必须向左二分；若 `bLeft > aRight` 则必须增大 `i`。可行分割必存在，二分不会排除它。

时间 $O(\log\min(m,n))$，额外空间 $O(1)$。它比第 $k$ 小淘汰法常数更小，只需一次二分；面试中优先记忆“固定左半大小 + 交叉边界”。

## 同阶方案比较与常见错误

- 二分分割：一次搜索，常数小；证明集中在分割条件，但下标边界最容易写错。
- 第 $k$ 小淘汰：抽象更通用，能直接回答任意秩；中位数偶数情形会调用两次，分支略多。
- 两者都是对数时间与常数空间。只针对中位数时推荐分割法；题目明确问任意 `k` 时推荐淘汰法。

常见错误：

- 没有保证在较短数组上二分，使 `j` 可能越界。
- `half` 忘记加一，奇数长度时左右定义混乱。
- 合法条件使用 `<`，错误拒绝重复值。
- 偶数长度整数除法丢失 `.5`。
- 用 `INT_MIN/INT_MAX` 做哨兵后直接把二者相加而不提升类型。
- 两数组都空；官方约束排除了这种情况，不应凭空设计返回值掩盖非法输入。

## Follow-up 1：求两个有序数组的第 $k$ 小

### 新定义与变化

给定 $1\le k\le m+n$，返回第 $k$ 小元素。中位数只是一个或两个特定 `k` 的组合；批量淘汰法直接适用。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findKth(vector<int>& a, vector<int>& b, int k) {
    int i = 0, j = 0;
    while (true) {
      if (i == static_cast<int>(a.size())) return b[j + k - 1];
      if (j == static_cast<int>(b.size())) return a[i + k - 1];
      if (k == 1) return min(a[i], b[j]);
      int pa = min(k / 2, static_cast<int>(a.size()) - i);
      int pb = min(k / 2, static_cast<int>(b.size()) - j);
      if (a[i + pa - 1] <= b[j + pb - 1]) {
        i += pa;
        k -= pa;
      } else {
        j += pb;
        k -= pb;
      }
    }
  }
};
```

时间 $O(\log k)$，空间 $O(1)$。

## Follow-up 2：$r$ 个有序数组的中位数

### 新定义与变化

输入变为多个有序数组，并保证所有数组的总元素数至少为 1。二分分割不再只有一个自由变量；使用小根堆做 $r$ 路归并，弹出到中间位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double medianOfSortedArrays(vector<vector<int>>& arrays) {
    using Node = tuple<int, int, int>;
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    int total = 0;
    for (int i = 0; i < static_cast<int>(arrays.size()); ++i) {
      total += arrays[i].size();
      if (!arrays[i].empty()) pq.push({arrays[i][0], i, 0});
    }
    int leftPos = (total - 1) / 2, rightPos = total / 2;
    int left = 0, right = 0;
    for (int pos = 0; pos <= rightPos; ++pos) {
      auto [value, row, index] = pq.top();
      pq.pop();
      if (pos == leftPos) left = value;
      if (pos == rightPos) right = value;
      if (index + 1 < static_cast<int>(arrays[row].size())) {
        pq.push({arrays[row][index + 1], row, index + 1});
      }
    }
    return (static_cast<long long>(left) + right) / 2.0;
  }
};
```

设总元素数为 $N$，时间 $O(N\log r)$ 的最坏界（只弹到中位处时约一半），空间 $O(r)$。若值域较小或支持各数组二分计数，可再对值域二分。

## Follow-up 3：两个数组不再有序

### 新定义与变化

排序结构消失后，对数算法的核心前提失效。合并后用 `nth_element` 选择中间秩，避免完整排序。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double medianUnsorted(vector<int> a, vector<int> b) {
    a.insert(a.end(), b.begin(), b.end());
    int n = a.size(), mid = n / 2;
    nth_element(a.begin(), a.begin() + mid, a.end());
    int right = a[mid];
    if (n % 2 == 1) return right;
    int left = *max_element(a.begin(), a.begin() + mid);
    return (static_cast<long long>(left) + right) / 2.0;
  }
};
```

平均时间 $O(m+n)$，最坏复杂度由标准库实现保证决定，空间 $O(m+n)$（按值接收并合并）。若允许破坏性拼接，可减少复制。

## Follow-up 4：返回精确分数而非 `double`

### 新定义与变化

返回约分后的 `(分子,分母)`，分母只能是 1 或 2。分割搜索不变，只改变最终表示，可完全避免浮点格式问题。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<long long, long long> exactMedian(vector<int> a, vector<int> b) {
    if (a.size() > b.size()) swap(a, b);
    int m = a.size(), n = b.size(), half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
      int i = lo + (hi - lo) / 2, j = half - i;
      int aLeft = i == 0 ? INT_MIN : a[i - 1];
      int aRight = i == m ? INT_MAX : a[i];
      int bLeft = j == 0 ? INT_MIN : b[j - 1];
      int bRight = j == n ? INT_MAX : b[j];
      if (aLeft <= bRight && bLeft <= aRight) {
        long long x = max(aLeft, bLeft);
        if ((m + n) % 2 == 1) return {x, 1};
        long long y = min(aRight, bRight);
        long long numerator = x + y;
        long long denominator = 2;
        long long g = gcd(abs(numerator), denominator);
        return {numerator / g, denominator / g};
      }
      if (aLeft > bRight) {
        hi = i - 1;
      } else {
        lo = i + 1;
      }
    }
    return {0, 1};
  }
};
```

时间 $O(\log\min(m,n))$，空间 $O(1)$（题目接口若改为引用参数即可避免此示例的值复制）。

## 可复现验证

- 官方元数据、题面、样例与全部约束通过力扣中国 GraphQL `question(titleSlug: "median-of-two-sorted-arrays")` 于 2026-07-27 核对。
- ZeroTracer `data.json` 同日检索无此 slug。
- 二分分割与第 $k$ 小方案使用小规模随机非递减数组，与完整合并后的精确中位数对拍；覆盖一个数组为空、重复值、奇偶总长度和正负极值。
- 所有代码块应以 C++23 独立编译。

## Reference

- [力扣中国 LC 4 官方题面](https://leetcode.cn/problems/median-of-two-sorted-arrays/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/median-of-two-sorted-arrays/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-14-lc11.md">← [力扣 Top 14] LC 11 盛最多水的容器 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-16-lc56.md">[力扣 Top 16] LC 56 合并区间 中等 →</a>
</nav>
