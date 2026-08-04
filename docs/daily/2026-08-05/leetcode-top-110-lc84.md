---
title: "[力扣 Top 110] LC 84 柱状图中最大的矩形 困难"
---

# [力扣 Top 110] LC 84 柱状图中最大的矩形 困难

<p class="daily-archive-kicker">2026-08-05 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../data-structures/monotonic-stacks/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=753f23249edd82f62888518af6815910486dcebab8405d62e8b9547bc583d75f -->
## 官方原始信息

- Top 排名：110
- 题号：LC 84
- 官方中文标题：柱状图中最大的矩形
- 官方难度：困难
- 官方链接：[柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/)

### 原始题意

给定相邻、宽度均为 1 的柱子高度数组，求完全位于柱状图内部的最大轴对齐矩形面积。

### 官方示意图

样例图由官方题面提供：[样例 1 柱状图](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)、[样例 2 柱状图](https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg)。图只用于说明矩形覆盖范围，不增加额外输入条件。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int largestRectangleArea(vector<int>& heights);
};
```

### 全部官方样例

```text
输入：heights = [2,1,5,6,2,3]
输出：10
解释：高度 5 和 6 的两根柱子形成高 5、宽 2 的最大矩形。
```

```text
输入：heights = [2,4]
输出：4
```

### 全部约束

- $1\le n=heights.length\le10^5$。
- $0\le heights[i]\le10^4$。
- 每根柱宽为 1。

## 约束推导与观察

任意最优矩形的高度一定等于其覆盖柱子中的最小高度，也就等于某根柱高。固定柱 `i` 作为矩形最低高度后，最大宽度由其左右第一个严格更矮的柱子确定。逐柱向两侧扫描是 $O(n^2)$；单调递增栈能在柱子第一次遇到右侧更矮边界时一次结算。

最大面积为 $10^5\times10^4=10^9$，仍在 32 位有符号范围内；中间乘法使用 64 位更便于迁移到更大约束。

## 解法递进

### 解法一：枚举左端点并维护区间最小值

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestRectangleArea(vector<int>& heights) {
    int n = heights.size();
    long long answer = 0;
    for (int left = 0; left < n; ++left) {
      int minimum = heights[left];
      for (int right = left; right < n; ++right) {
        minimum = min(minimum, heights[right]);
        answer = max(answer, 1LL * minimum * (right - left + 1));
      }
    }
    return static_cast<int>(answer);
  }
};
```

时间 $O(n^2)$，空间 $O(1)$。虽已把三次暴力的区间最小值扫描压掉，但仍重复扩展相同高度边界。

### 解法二：预计算左右第一个更矮位置

两次单调栈分别求边界，再逐柱计算贡献。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestRectangleArea(vector<int>& heights) {
    int n = heights.size();
    vector<int> left(n, -1), right(n, n), stack;
    for (int i = 0; i < n; ++i) {
      while (!stack.empty() && heights[stack.back()] >= heights[i]) {
        stack.pop_back();
      }
      left[i] = stack.empty() ? -1 : stack.back();
      stack.push_back(i);
    }
    stack.clear();
    for (int i = n - 1; i >= 0; --i) {
      while (!stack.empty() && heights[stack.back()] >= heights[i]) {
        stack.pop_back();
      }
      right[i] = stack.empty() ? n : stack.back();
      stack.push_back(i);
    }
    long long answer = 0;
    for (int i = 0; i < n; ++i) {
      answer = max(answer, 1LL * heights[i] * (right[i] - left[i] - 1));
    }
    return static_cast<int>(answer);
  }
};
```

时间 $O(n)$，空间 $O(n)$。它最便于观察每根柱子的完整左右边界。

### 最佳实用解：单次单调栈在线结算

在末尾追加逻辑高度 0，强制弹出全部未结算柱。栈内高度严格递增；弹出 `middle` 时，当前下标是右侧首个更矮位置，弹出后的栈顶是左侧首个更矮位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestRectangleArea(vector<int>& heights) {
    vector<int> stack;
    stack.push_back(-1);
    long long answer = 0;
    for (int i = 0; i <= static_cast<int>(heights.size()); ++i) {
      int current = i == static_cast<int>(heights.size()) ? 0 : heights[i];
      while (stack.back() != -1 && heights[stack.back()] >= current) {
        int height = heights[stack.back()];
        stack.pop_back();
        int width = i - stack.back() - 1;
        answer = max(answer, 1LL * height * width);
      }
      stack.push_back(i);
    }
    return static_cast<int>(answer);
  }
};
```

时间 $O(n)$，空间 $O(n)$。每个下标至多入栈、出栈各一次，达到线性下界；这是推荐竞赛模板。

## 正确性证明

当柱 `j` 被当前更矮柱 `i` 弹出时，`i` 是 `j` 右侧第一个高度严格小于 `heights[j]` 的位置；弹出后栈顶 `p` 是左侧第一个严格更矮位置。区间 `(p,i)` 中每根柱高都至少为 `heights[j]`，而向任一侧再扩一格都会遇到更矮柱，所以以该高度为最低高度的最大矩形面积恰为 `heights[j] * (i-p-1)`。每根柱都被哨兵最终结算，所有可能的最优最低柱均被考虑，取最大值即为全局答案。

## 样例手推

处理 `[2,1,5,6,2,3]` 时，遇到高度 2 会依次弹出 6 与 5。柱 5 的左侧更矮位置是下标 1、右侧更矮位置是下标 4，宽度为 2，面积为 10。末尾逻辑 0 再结算剩余高度。`[2,4]` 的最大值可由高度 2、宽 2 或高度 4、宽 1 得到，均为 4。

## 易错点与方案比较

- 宽度是 `right - left - 1`，不是两边界之差。
- 相等高度使用 `>=` 弹出可合并边界；若用 `>`，仍可正确但必须保证重复柱最终获得完整宽度。
- 逻辑哨兵下标 `n` 不能再访问 `heights[n]`。
- 两遍边界法更易调试；单遍法代码短、常数小，熟练后优先。

## 变种一：二进制矩阵中的最大矩形

新定义：每行把连续 1 的高度累加成柱状图，逐行调用单调栈。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int histogram(const vector<int>& heights) {
    vector<int> stack{-1};
    int answer = 0;
    for (int i = 0; i <= static_cast<int>(heights.size()); ++i) {
      int current = i == static_cast<int>(heights.size()) ? 0 : heights[i];
      while (stack.back() != -1 && heights[stack.back()] >= current) {
        int height = heights[stack.back()];
        stack.pop_back();
        answer = max(answer, height * (i - stack.back() - 1));
      }
      stack.push_back(i);
    }
    return answer;
  }
public:
  int maximalRectangle(vector<vector<char>>& matrix) {
    if (matrix.empty()) {
      return 0;
    }
    vector<int> heights(matrix[0].size());
    int answer = 0;
    for (const auto& row : matrix) {
      for (int column = 0; column < static_cast<int>(row.size()); ++column) {
        heights[column] = row[column] == '1' ? heights[column] + 1 : 0;
      }
      answer = max(answer, histogram(heights));
    }
    return answer;
  }
};
```

时间 $O(rows\cdot columns)$，空间 $O(columns)$；对应 [LC 85](https://leetcode.cn/problems/maximal-rectangle/)。

## 变种二：柱宽不再全为 1

新定义：每柱有正宽度 `width[i]`。用宽度前缀和替代下标差，边界结构仍由高度决定。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<long long> height(n), width(n), prefix(n + 1);
  for (long long& value : height) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    cin >> width[i];
    prefix[i + 1] = prefix[i] + width[i];
  }
  vector<int> stack{-1};
  long long answer = 0;
  for (int i = 0; i <= n; ++i) {
    long long current = i == n ? 0 : height[i];
    while (stack.back() != -1 && height[stack.back()] >= current) {
      long long h = height[stack.back()];
      stack.pop_back();
      int leftIndex = stack.back() + 1;
      answer = max(answer, h * (prefix[i] - prefix[leftIndex]));
    }
    stack.push_back(i);
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；面积和宽度和必须使用 64 位。

## 变种三：圆形柱状图

新定义：首尾相邻，矩形最多覆盖每根柱一次。复制数组两遍，并把任何候选宽度截断为 `n`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> height(2 * n);
  for (int i = 0; i < n; ++i) {
    cin >> height[i];
    height[i + n] = height[i];
  }
  vector<int> stack{-1};
  long long answer = 0;
  for (int i = 0; i <= 2 * n; ++i) {
    int current = i == 2 * n ? 0 : height[i];
    while (stack.back() != -1 && height[stack.back()] >= current) {
      int h = height[stack.back()];
      stack.pop_back();
      int width = min(n, i - stack.back() - 1);
      answer = max(answer, 1LL * h * width);
    }
    stack.push_back(i);
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。不限制宽度会错误地让同一柱被覆盖两次。

## 变种四：恢复一个最大矩形的左右边界和高度

新定义：返回面积之外，还输出 `[left,right]` 与高度。弹栈结算时同步保存当前候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> height(n);
  for (int& value : height) {
    cin >> value;
  }
  vector<int> stack{-1};
  long long bestArea = -1;
  int bestLeft = 0;
  int bestRight = 0;
  int bestHeight = 0;
  for (int i = 0; i <= n; ++i) {
    int current = i == n ? 0 : height[i];
    while (stack.back() != -1 && height[stack.back()] >= current) {
      int h = height[stack.back()];
      stack.pop_back();
      int left = stack.back() + 1;
      int right = i - 1;
      long long area = 1LL * h * (right - left + 1);
      if (area > bestArea) {
        bestArea = area;
        bestLeft = left;
        bestRight = right;
        bestHeight = h;
      }
    }
    stack.push_back(i);
  }
  cout << bestArea << ' ' << bestLeft << ' ' << bestRight << ' ' << bestHeight << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。若要求字典序最小边界，可在面积相等时增加明确次级比较。

## 验证说明

本轮将八段代码按 C++23 编译；单栈与双边界方案会和 $O(n^2)$ oracle 对拍 50,000 组随机高度，并覆盖全零、严格递增、严格递减、全相等、单柱和面积接近 $10^9$。矩阵、变宽、圆形及恢复方案各用对应枚举 oracle 核验。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/largest-rectangle-in-histogram/)
- [对应知识专题](../../data-structures/monotonic-stacks.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-109-lc141/">← [力扣 Top 109] LC 141 环形链表 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-513-q3-lc4012/">[力扣竞赛] 第 513 场周赛 Q3 LC 4012 统计每个班次结束后的未完成任务数 中等 →</a>
</nav>
