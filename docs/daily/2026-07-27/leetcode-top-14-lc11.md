---
title: "[力扣 Top 14] LC 11 盛最多水的容器 中等"
---

# [力扣 Top 14] LC 11 盛最多水的容器 中等

<p class="daily-archive-kicker">2026-07-27 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-27 题目列表</a> · <a href="../../basics/sequence-invariants.md">进入知识专题</a></p>

官方题目：https://leetcode.cn/problems/container-with-most-water/

## 官方原始信息

- 题号：11
- 官方中文标题：盛最多水的容器
- 官方英文标题：Container With Most Water
- slug：`container-with-most-water`
- 官方难度：中等
- 函数签名：`int maxArea(vector<int>& height)`
- 官方竞赛归属与分值：未发现官方竞赛归属，官方分值未知
- ZeroTracer 社区估算竞赛分：无。2026-07-27 检索公开 `data.json`，该 slug 不在数据集中

### 原始题意

数组 `height` 的第 $i$ 项表示位于横坐标 $i$ 的竖线高度。选择两条线作为容器左右边界，水面高度由较短的边限制，底宽是两下标之差。容器不可倾斜，返回最大容量：

$$
\max_{0\le i<j<n}(j-i)\min(height[i],height[j]).
$$

### 全部官方样例

1. `height = [1,8,6,2,5,4,8,3,7]`，输出 `49`。选择下标 1 与 8，宽 7、短边 7，面积 $7\times7=49$。
2. `height = [1,1]`，输出 `1`。

### 全部官方约束

- `n == height.length`
- $2\le n\le10^5$
- $0\le height[i]\le10^4$

官方题面含一张解释样例 1 的示意图；完整原图以官方页面为准。

## 约束推导、样例与边界

下标对有 $\binom n2$ 个，$n=10^5$ 时完全枚举约 $5\times10^9$ 对，不可接受。面积同时受“宽度”和“短边”约束：从最宽的一对开始，若左边不高于右边，那么保留左边、缩小右端只会让宽度变小且短边仍不超过左边，因此不可能更优；唯一有希望的是丢弃左边去寻找更高的短边。这就是双指针的支配性删除。

样例 1 的状态可概括为：

- `(0,8)`：面积 8，左边更短，删除下标 0。
- `(1,8)`：面积 49，右边更短，删除下标 8。
- 后续宽度持续减小，虽遇到高度 8，也无法超过 49。

边界：

- 只有两条线时只能选这一对。
- 某端高度为 0 时，该对面积为 0，应移动零高端。
- 高度全相等时，最外侧两条线最优。
- 单调递增或递减数组仍不能贪心只取最高两条线，距离可能更重要。
- 最大面积至多 $(10^5-1)\times10^4<10^9$，32 位有符号 `int` 足够。

## 解法一：枚举所有下标对

逐一计算每个合法容器，覆盖性直接来自目标定义。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxArea(vector<int>& height) {
    int n = height.size(), ans = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        ans = max(ans, (j - i) * min(height[i], height[j]));
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。瓶颈是每个端点会与大量已经被支配的另一端重复配对。

## 解法二：双指针消去被支配端点（最佳实用解）

指针 `l`、`r` 从两端开始。记录当前面积后移动较短的一边；两边相等时移动任意一边都正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxArea(vector<int>& height) {
    int l = 0, r = static_cast<int>(height.size()) - 1;
    int ans = 0;
    while (l < r) {
      ans = max(ans, (r - l) * min(height[l], height[r]));
      if (height[l] <= height[r]) {
        ++l;
      } else {
        --r;
      }
    }
    return ans;
  }
};
```

### 正确性证明

考虑当前区间 $[l,r]$ 且 $height[l]\le height[r]$。对任意 $j$ 满足 $l<j<r$，有

$$
(j-l)\min(height[l],height[j])
\le (j-l)height[l]
< (r-l)height[l],
$$

而右侧正是当前对 `(l,r)` 的面积。因此所有以 `l` 为左端、另一端仍在当前区间内的未考察容器都严格不优于当前容器，删除 `l` 不会丢失尚未记录的更优答案。若右端较短则论证对称。每轮删除一个可安全排除的端点，直到所有可能包含最优解的候选都被考察或保留，所以最终最大值正确。

时间复杂度 $O(n)$，额外空间 $O(1)$，达到读取输入的 $\Omega(n)$ 下界。面试优先记忆“双指针 + 删除较短端的支配证明”，而不是死记移动方向。

## 同阶方案比较与常见错误

没有比 $O(n)$ 更好的渐进复杂度。可以用单调结构按高度处理端点，但代码、常数和证明都更重，且没有扩展收益；双指针是唯一值得优先记忆的实用方案。

常见错误：

- 移动较高的一边；这样既缩小宽度，又保留原短板，无法制造更优候选。
- 面积写成两边高度之和或较高边乘宽度。
- 把 LC 42“接雨水”的逐列蓄水模型套到本题；本题只选择两条边，中间线不会排水或占体积。
- 忘记宽度是 `r - l`，不是元素个数。
- 对相等高度同时移动两端虽然仍可求最大值，但会跳过一些同面积下标对；若要恢复特定字典序答案需另行定义。

## Follow-up 1：返回任意一组最优下标

### 新定义与变化

除了最大面积，还返回产生该面积的 `(left,right)`。原双指针路径一定访问至少一个最优对，只需在更新最大值时保存下标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  array<int, 3> maxAreaWithIndices(vector<int>& height) {
    int l = 0, r = static_cast<int>(height.size()) - 1;
    array<int, 3> ans = {0, 0, 1};
    while (l < r) {
      int area = (r - l) * min(height[l], height[r]);
      if (area > ans[0]) ans = {area, l, r};
      if (height[l] <= height[r]) {
        ++l;
      } else {
        --r;
      }
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(1)$。若要求“字典序最小的最优对”，不能只在等面积时随意覆盖；最稳妥的基线是先求最优面积，再枚举全部对筛选，代价 $O(n^2)$，除非进一步利用值域或离线结构。

## Follow-up 2：竖线横坐标不等距

### 新定义与变化

给定严格递增坐标 `x[i]` 与高度 `h[i]`，面积为 $(x[j]-x[i])\min(h[i],h[j])$。删除短边的证明只需要内部点带来更小的宽度，因此双指针仍成立。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long maxArea(vector<long long>& x, vector<long long>& h) {
    int l = 0, r = static_cast<int>(x.size()) - 1;
    long long ans = 0;
    while (l < r) {
      ans = max(ans, (x[r] - x[l]) * min(h[l], h[r]));
      if (h[l] <= h[r]) {
        ++l;
      } else {
        --r;
      }
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(1)$。坐标和高度的新值域未给出时用 `long long`，并仍需由实际上界判断 64 位乘法是否安全。

## Follow-up 3：大量“固定宽度”查询

### 新定义与变化

每次询问宽度恰为 $d$ 的最大容量。原双指针优化的是所有宽度混合后的最大值，无法直接给出每个 $d$ 的答案；预处理每个间距的最佳短边即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class FixedWidthContainers {
  vector<long long> best;
public:
  explicit FixedWidthContainers(const vector<int>& h) {
    int n = h.size();
    best.assign(n, 0);
    for (int d = 1; d < n; ++d) {
      for (int i = 0; i + d < n; ++i) {
        best[d] = max(best[d], 1LL * d * min(h[i], h[i + d]));
      }
    }
  }
  long long query(int width) const {
    if (width <= 0 || width >= static_cast<int>(best.size())) return 0;
    return best[width];
  }
};
```

预处理 $O(n^2)$，空间 $O(n)$，每次查询 $O(1)$。这是用更重预处理换取大量查询吞吐；单次查询直接扫描 $O(n)$ 更合适。

## Follow-up 4：改为所有柱子共同蓄水（LC 42）

### 新定义与变化

不再只选择两条边；每个位置的水深由其左侧最高柱和右侧最高柱共同决定。原面积目标失效，但“两端较低侧的水位已经确定”仍导出双指针。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trap(vector<int>& height) {
    int l = 0, r = static_cast<int>(height.size()) - 1;
    int leftMax = 0, rightMax = 0, ans = 0;
    while (l <= r) {
      if (leftMax <= rightMax) {
        leftMax = max(leftMax, height[l]);
        ans += leftMax - height[l];
        ++l;
      } else {
        rightMax = max(rightMax, height[r]);
        ans += rightMax - height[r];
        --r;
      }
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(1)$。区别要牢记：LC 11 的状态是一对端点，移动短边是删除不可能更优的容器；LC 42 的状态是两侧最高水位，处理的是每个位置的确定水深。

## 可复现验证

- 官方元数据、题面、两组样例与全部约束通过力扣中国 GraphQL `question(titleSlug: "container-with-most-water")` 于 2026-07-27 核对。
- ZeroTracer `data.json` 于同日检索无此 slug。
- 最优双指针以 $2\le n\le 10$、小值域随机数组和 $O(n^2)$ 枚举作 oracle 对拍。
- 所有代码块应以 C++23 独立编译。

## Reference

- [力扣中国 LC 11 官方题面](https://leetcode.cn/problems/container-with-most-water/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/container-with-most-water/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-13-lc200.md">← [力扣 Top 13] LC 200 岛屿数量 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-15-lc4.md">[力扣 Top 15] LC 4 寻找两个正序数组的中位数 困难 →</a>
</nav>
