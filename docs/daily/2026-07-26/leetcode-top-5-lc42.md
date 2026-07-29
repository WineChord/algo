---
title: "[力扣 Top 5] LC 42 接雨水 困难"
---

# [力扣 Top 5] LC 42 接雨水 困难

<p class="daily-archive-kicker">2026-07-26 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../basics/sequence-invariants.md">进入知识专题</a></p>

## 官方原始信息

- 难度：困难
- 官方链接：https://leetcode.cn/problems/trapping-rain-water/
- 函数签名：`int trap(vector<int>& height)`

### 原始题意

给定 $n$ 个非负整数，表示宽度均为 $1$ 的柱子高度。求下雨后柱子之间能够存下的雨水总量。

### 全部官方样例

1. `height = [0,1,0,2,1,0,1,3,2,1,2,1]`，输出 `6`。
2. `height = [4,2,0,3,2,5]`，输出 `9`。

### 全部约束

- `n == height.length`
- $1\le n\le 2\times 10^4$
- $0\le height[i]\le 10^5$

## 最优结论

位置 $i$ 上方的水位由左右最高挡板的较小值决定：

$$
water_i=\max\bigl(0,\min(leftMax_i,rightMax_i)-height_i\bigr).
$$

双指针维护两侧已知最大值。若 `leftMax <= rightMax`，左端水量已经由 `leftMax` 确定，可以结算并右移；反之结算右端。时间 $O(n)$，额外空间 $O(1)$。面试优先记忆双指针，同时理解前后缀公式；单调栈适合进一步处理“每个凹槽何时闭合”的题。

## 约束、边界与关键观察

- 最外侧柱子没有左右两堵墙，不能存水。
- 每个位置只关心左右最高值，不关心最高值之间的具体形状。
- 单个位置最多存 $10^5$ 量级，总量上界约 $2\times 10^9$，官方返回 `int`；累加时使用 `long long` 更稳健。
- 全递增、全递减、全相等或长度不足 $3$ 时答案为 $0$。
- 高度相等的挡板同样可以闭合凹槽。

## 样例手推

对 `[4,2,0,3,2,5]`，每个内部位置的左侧最高值都是 $4$，右侧最高值都是 $5$。对应水量为 $2,4,1,2$，总计 $9$。这也说明中间柱子并非必须低于相邻柱子，只需低于两侧全局挡板。

## 解法一：逐位置向两侧扫描

对每个位置重新寻找左侧和右侧最高柱。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trap(vector<int>& height) {
    int n = height.size();
    long long ans = 0;
    for (int i = 1; i + 1 < n; ++i) {
      int leftMax = 0, rightMax = 0;
      for (int j = 0; j <= i; ++j) leftMax = max(leftMax, height[j]);
      for (int j = i; j < n; ++j) rightMax = max(rightMax, height[j]);
      ans += min(leftMax, rightMax) - height[i];
    }
    return (int)ans;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。重复计算左右最大值是唯一瓶颈。

## 解法二：前后缀最大值

预处理每个位置左侧最高和右侧最高，再按公式求和。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trap(vector<int>& height) {
    int n = height.size();
    vector<int> leftMax(n), rightMax(n);
    leftMax[0] = height[0];
    for (int i = 1; i < n; ++i) leftMax[i] = max(leftMax[i - 1], height[i]);
    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; --i) rightMax[i] = max(rightMax[i + 1], height[i]);
    long long ans = 0;
    for (int i = 0; i < n; ++i) ans += min(leftMax[i], rightMax[i]) - height[i];
    return (int)ans;
  }
};
```

时间 $O(n)$，额外空间 $O(n)$。

## 解法三：单调栈

维护高度单调不增的下标栈。新柱更高时，栈顶是凹槽底；弹出后，新栈顶与当前柱成为左右边界，按宽度乘有效高度结算一层。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trap(vector<int>& height) {
    stack<int> st;
    long long ans = 0;
    for (int i = 0; i < (int)height.size(); ++i) {
      while (!st.empty() && height[i] > height[st.top()]) {
        int bottom = st.top();
        st.pop();
        if (st.empty()) break;
        int left = st.top();
        int width = i - left - 1;
        int level = min(height[left], height[i]) - height[bottom];
        ans += 1LL * width * level;
      }
      st.push(i);
    }
    return (int)ans;
  }
};
```

每个下标至多进栈、出栈一次，时间 $O(n)$，空间 $O(n)$。

## 解法四：双指针（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trap(vector<int>& height) {
    int l = 0, r = (int)height.size() - 1;
    int leftMax = 0, rightMax = 0;
    long long ans = 0;
    while (l <= r) {
      leftMax = max(leftMax, height[l]);
      rightMax = max(rightMax, height[r]);
      if (leftMax <= rightMax) {
        ans += leftMax - height[l];
        ++l;
      } else {
        ans += rightMax - height[r];
        --r;
      }
    }
    return (int)ans;
  }
};
```

### 正确性证明

始终有 `leftMax` 是当前左端及其左侧最高值，`rightMax` 是当前右端及其右侧最高值。若 `leftMax <= rightMax`，右侧至少存在高度为 `rightMax` 的挡板，所以左端位置的较矮挡板必为 `leftMax`，其水量已经确定为 `leftMax - height[l]`，未知的中间形状无法改变它；因此可安全结算左端。另一种情况对称。每一步删除一个已正确结算的位置，最终所有位置均被处理。

### 复杂度与方案比较

- 前后缀：证明最直接，适合还要输出每个位置水量。
- 单调栈：按凹槽分层结算，适合与“下一个更大元素”类问题迁移。
- 双指针：同为 $O(n)$，但只用 $O(1)$ 空间，主问题首选。

## 常见错误

- 用相邻两柱的较小值代替左右全局最大值。
- 双指针比较 `height[l]` 与 `height[r]` 时却错误维护水位；应保证所用不变量一致。
- 栈弹出凹槽底后忘记检查栈是否为空。
- 栈解法宽度写成 `i - left`，漏减 $1$。
- 把负水量直接累加；正确水位公式在包含当前位置的前后缀最大值下天然非负。

## Follow-up 1：返回每个位置的存水量

需要逐位置答案时，前后缀数组比双指针更直接。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> waterAtEachPosition(vector<int>& height) {
    int n = height.size();
    vector<int> leftMax(n), rightMax(n), water(n);
    leftMax[0] = height[0];
    for (int i = 1; i < n; ++i) leftMax[i] = max(leftMax[i - 1], height[i]);
    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; --i) rightMax[i] = max(rightMax[i + 1], height[i]);
    for (int i = 0; i < n; ++i) {
      water[i] = min(leftMax[i], rightMax[i]) - height[i];
    }
    return water;
  }
};
```

时间 $O(n)$，空间 $O(n)$。

## Follow-up 2：二维高度图

对应 [LeetCode 407 · 接雨水 II](https://leetcode.cn/problems/trapping-rain-water-ii/)。从边界最矮格开始向内扩张；优先队列维护当前最低围墙，内部格可存的水由该围墙决定。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int trapRainWater(vector<vector<int>>& heightMap) {
    int m = heightMap.size(), n = heightMap[0].size();
    if (m < 3 || n < 3) return 0;
    using State = tuple<int, int, int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    vector<vector<int>> vis(m, vector<int>(n));
    for (int i = 0; i < m; ++i) {
      for (int j : {0, n - 1}) {
        if (!vis[i][j]) {
          vis[i][j] = 1;
          pq.emplace(heightMap[i][j], i, j);
        }
      }
    }
    for (int j = 0; j < n; ++j) {
      for (int i : {0, m - 1}) {
        if (!vis[i][j]) {
          vis[i][j] = 1;
          pq.emplace(heightMap[i][j], i, j);
        }
      }
    }
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    long long ans = 0;
    while (!pq.empty()) {
      auto [level, x, y] = pq.top();
      pq.pop();
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n || vis[nx][ny]) continue;
        vis[nx][ny] = 1;
        ans += max(0, level - heightMap[nx][ny]);
        pq.emplace(max(level, heightMap[nx][ny]), nx, ny);
      }
    }
    return (int)ans;
  }
};
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## Follow-up 3：柱子宽度不再都是 $1$

水位仍只由高度决定，但每个位置的体积要乘自己的宽度。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long trapWithWidths(vector<int>& height, vector<int>& width) {
    int n = height.size();
    vector<int> leftMax(n), rightMax(n);
    leftMax[0] = height[0];
    for (int i = 1; i < n; ++i) leftMax[i] = max(leftMax[i - 1], height[i]);
    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; --i) rightMax[i] = max(rightMax[i + 1], height[i]);
    long long ans = 0;
    for (int i = 0; i < n; ++i) {
      ans += 1LL * (min(leftMax[i], rightMax[i]) - height[i]) * width[i];
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(n)$。

## Follow-up 4：高度流逐个追加，随时返回当前总水量

未来柱子会关闭此前尚未闭合的凹槽。单调栈只在新柱到来时结算新形成的层，因此适合在线追加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class RainWaterStream {
  vector<int> height;
  stack<int> st;
  long long total = 0;
public:
  long long append(int h) {
    int i = height.size();
    height.push_back(h);
    while (!st.empty() && height[i] > height[st.top()]) {
      int bottom = st.top();
      st.pop();
      if (st.empty()) break;
      int left = st.top();
      int width = i - left - 1;
      int level = min(height[left], height[i]) - height[bottom];
      total += 1LL * width * level;
    }
    st.push(i);
    return total;
  }
};
```

每个柱子均摊 $O(1)$，保存全部未决下标和高度，空间 $O(n)$。

## Reference

- 官方题面与接口：https://leetcode.cn/problems/trapping-rain-water/

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/trapping-rain-water/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-4-lc146.md">← [力扣 Top 4] LC 146 LRU 缓存 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-6-lc49.md">[力扣 Top 6] LC 49 字母异位词分组 中等 →</a>
</nav>
