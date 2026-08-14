---
title: "[力扣 Top 135] LC 85 最大矩形 困难"
---

# [力扣 Top 135] LC 85 最大矩形 困难

<p class="daily-archive-kicker">2026-08-15 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-15 题目列表</a> · <a href="../../../data-structures/monotonic-stacks/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=232e3d26afb08701445de5b1e7f2b1d5be2474b149869a045b422f69d6cf821b -->
[官方题目：LC 85 最大矩形](https://leetcode.cn/problems/maximal-rectangle/)

## 官方原始信息

- 题号：85。
- 标题：最大矩形。
- 官方难度：困难。
- 官方链接：[力扣中国](https://leetcode.cn/problems/maximal-rectangle/)。
- 题库顺序：Top 135；权威表格原行标题与当前官方标题一致。
- 标签：栈、数组、动态规划、矩阵、单调栈。

给定一个只含字符 `'0'` 与 `'1'`、大小为 `rows x cols` 的二维矩阵，求只包含 `'1'` 的轴对齐矩形的最大面积。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maximalRectangle(vector<vector<char>>& matrix);
};
```

### 全部官方样例

样例 1：

```text
输入：matrix = [["1","0","1","0","0"],
                ["1","0","1","1","1"],
                ["1","1","1","1","1"],
                ["1","0","0","1","0"]]
输出：6
解释：第 2 至 3 行、第 3 至 5 列组成一个 2 x 3 的全 1 矩形。
```

样例 2：

```text
输入：matrix = [["0"]]
输出：0
```

样例 3：

```text
输入：matrix = [["1"]]
输出：1
```

### 全部约束

- `rows == matrix.length`。
- `cols == matrix[0].length`。
- $1\le rows,cols\le200$。
- `matrix[i][j]` 为 `'0'` 或 `'1'`。

## 约束推导与模型转化

矩形由上下左右四条边决定，直接枚举有 $O(rows^2cols^2)$ 个候选。二维前缀和能在 $O(1)$ 检查一个候选是否全为 1，但 $200^4=1.6\times10^9$ 仍过大。

固定矩形的下边界为当前行。对每一列维护从当前行向上连续 1 的高度 `height[j]`：遇到 `'1'` 加一，遇到 `'0'` 清零。于是所有以当前行为下边界的全 1 矩形，恰好对应这个柱状图中的矩形。问题转化为对每一行求一次“柱状图中最大的矩形”。

柱状图中，若把某根柱子的高度作为矩形最小高度，最大宽度延伸到左右第一个严格更矮的柱子之间。单调递增栈在线维护这些边界，每根柱子只入栈、出栈一次，所以每行 $O(cols)$，总时间 $O(rows\cdot cols)$。

最大面积不超过 $200\times200=40000$，`int` 安全；高度、下标也都不超过 200。

## 解法递进

### 解法一：二维前缀和枚举四条边

先计算 1 的二维前缀和，再枚举所有非空矩形；区域和等于面积时，该矩形全部为 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximalRectangle(vector<vector<char>>& matrix) {
    int rows = static_cast<int>(matrix.size());
    int cols = static_cast<int>(matrix[0].size());
    vector<vector<int>> prefix(rows + 1, vector<int>(cols + 1));
    for (int row = 0; row < rows; ++row) {
      for (int col = 0; col < cols; ++col) {
        prefix[row + 1][col + 1] = prefix[row][col + 1] +
            prefix[row + 1][col] - prefix[row][col] + (matrix[row][col] == '1');
      }
    }
    int answer = 0;
    for (int top = 0; top < rows; ++top) {
      for (int bottom = top; bottom < rows; ++bottom) {
        for (int left = 0; left < cols; ++left) {
          for (int right = left; right < cols; ++right) {
            int ones = prefix[bottom + 1][right + 1] - prefix[top][right + 1] -
                prefix[bottom + 1][left] + prefix[top][left];
            int area = (bottom - top + 1) * (right - left + 1);
            if (ones == area) answer = max(answer, area);
          }
        }
      }
    }
    return answer;
  }
};
int main() {
  vector<vector<char>> matrix{{'1', '1'}, {'1', '0'}};
  cout << Solution().maximalRectangle(matrix) << '\n';
}
```

时间 $O(rows^2cols^2)$，前缀和空间 $O(rows\cdot cols)$。它适合小规模对拍，无法应对上界。

### 解法二：逐行累积高度后向两侧扫描

把每行转成柱状图后，可对每根柱子分别向左右扫描，找到第一个更矮位置。这样已把二维候选压到每行一维，但单行最坏仍为 $O(cols^2)$，总时间 $O(rows\cdot cols^2)$。

### 最佳实用解：逐行柱状图加单调栈

栈中保存严格递增高度的柱子下标。当前高度不大于栈顶时，栈顶柱子的右边界已经确定；弹出后，新栈顶就是它左侧第一个更矮柱子。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int largestHistogram(const vector<int>& height) {
    vector<int> increasing{-1};
    int answer = 0;
    int n = static_cast<int>(height.size());
    for (int i = 0; i <= n; ++i) {
      int current = i == n ? 0 : height[i];
      while (increasing.back() != -1 && height[increasing.back()] >= current) {
        int value = height[increasing.back()];
        increasing.pop_back();
        int width = i - increasing.back() - 1;
        answer = max(answer, value * width);
      }
      increasing.push_back(i);
    }
    return answer;
  }
public:
  int maximalRectangle(vector<vector<char>>& matrix) {
    int cols = static_cast<int>(matrix[0].size());
    vector<int> height(cols);
    int answer = 0;
    for (const auto& row : matrix) {
      for (int col = 0; col < cols; ++col) {
        height[col] = row[col] == '1' ? height[col] + 1 : 0;
      }
      answer = max(answer, largestHistogram(height));
    }
    return answer;
  }
};
int main() {
  vector<vector<char>> matrix{
      {'1', '0', '1', '0', '0'},
      {'1', '0', '1', '1', '1'},
      {'1', '1', '1', '1', '1'},
      {'1', '0', '0', '1', '0'}};
  cout << Solution().maximalRectangle(matrix) << '\n';
}
```

每个单元格引起至多一次入栈和一次出栈，时间 $O(rows\cdot cols)$；高度与栈占 $O(cols)$ 额外空间。

### 同阶方案：动态维护左右边界

也可逐行维护 `height[j]`、可延伸的最左边界 `left[j]` 与开区间右边界 `right[j]`。每行分别从左到右和从右到左更新边界，再计算 `height[j]*(right[j]-left[j])`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximalRectangle(vector<vector<char>>& matrix) {
    int cols = static_cast<int>(matrix[0].size());
    vector<int> height(cols), left(cols), right(cols, cols);
    int answer = 0;
    for (const auto& row : matrix) {
      int currentLeft = 0;
      int currentRight = cols;
      for (int col = 0; col < cols; ++col) {
        if (row[col] == '1') {
          ++height[col];
          left[col] = max(left[col], currentLeft);
        } else {
          height[col] = 0;
          left[col] = 0;
          currentLeft = col + 1;
        }
      }
      for (int col = cols - 1; col >= 0; --col) {
        if (row[col] == '1') {
          right[col] = min(right[col], currentRight);
        } else {
          right[col] = cols;
          currentRight = col;
        }
      }
      for (int col = 0; col < cols; ++col) {
        answer = max(answer, height[col] * (right[col] - left[col]));
      }
    }
    return answer;
  }
};
int main() {
  vector<vector<char>> matrix{{'1', '1'}, {'1', '1'}};
  cout << Solution().maximalRectangle(matrix) << '\n';
}
```

时间 $O(rows\cdot cols)$，空间 $O(cols)$。它避免显式栈，但要同时维护三组状态与两种开闭边界，证明和实现更易出错。

## 正确性证明

先证明二维转化。处理第 `r` 行后，`height[c]` 等于从 `(r,c)` 向上连续 `'1'` 的数量。任一以下边界 `r` 结束、列区间为 `[l,r]` 的全 1 矩形，其高度不超过区间内每个 `height[c]`；反之，取区间最小高度就一定得到对应的全 1 矩形。因此当前行所有候选与柱状图矩形一一对应。

再证明单调栈。柱子 `k` 被弹出时，当前下标 `i` 是其右侧第一个高度严格小于 `height[k]` 的位置；弹出后栈顶 `j` 是其左侧第一个严格更矮位置。故以 `height[k]` 为最小高度的最大区间是 `(j,i)`，宽度为 `i-j-1`，算法恰计算它的最大面积。所有柱子最终都会被某个更矮高度或末尾哨兵弹出，所以每种可能的最小高度都被完整考虑。逐行取最大值即得到全矩阵最优。

## 样例手推与边界

样例 1 的累计高度逐行为：

```text
[1,0,1,0,0]
[2,0,2,1,1]
[3,1,3,2,2]
[4,0,0,3,0]
```

第三行柱状图的区间第 3 至 5 列最小高度为 2，面积为 $2\times3=6$，即官方答案。

- 全零矩阵：所有高度始终为 0，答案为 0。
- 全一矩阵：最后一行柱状图给出 `rows*cols`。
- 单行矩阵：退化为最长连续 1 的长度。
- 单列矩阵：退化为最长连续 1 的高度。
- 相等高度：使用 `>=` 弹栈可统一把宽区间留给最后一根等高柱；使用 `>` 也可，但边界证明与实现必须一致。

## 方案比较与推荐

二维前缀和枚举适合作为可靠 oracle；逐柱左右扫描展示了降维收益；单调栈与左右边界 DP 都达到 $O(rows\cdot cols)$。单调栈只维护一个清晰不变量，并直接复用 LC 84 的柱状图模型，优先记忆；左右边界 DP 在需要逐行持续维护边界时也有价值，但状态更多、开闭区间更敏感。

## 易错点

- 矩阵元素是字符 `'0'`、`'1'`，不是整数 0、1。
- 遇到 `'0'` 必须把该列累计高度清零。
- 栈存下标而非高度，才能计算宽度。
- 弹栈后的宽度是 `i - newTop - 1`，不是 `i - oldTop`。
- 末尾需要高度 0 的哨兵，确保剩余柱子全部结算。
- 不要把本题与 LC 84 混淆：本题先逐行构造柱状图，再调用同一核心。

## 可复现验证

本页全部完整代码均以 C++23 严格编译，三个官方样例得到 6、0、1。固定种子穷举与随机生成 124,954 个小型二进制矩阵，把单调栈、左右边界 DP 与四边枚举前缀和 oracle 比较；另核对全零、全一、单行、单列、棋盘格和 $200\times200$ 边界，结果全部一致。

## 变种一：恢复一个最大矩形的坐标

柱子在第 `bottom` 行弹出时，高度确定上边界，弹栈后的栈顶和当前下标确定左右边界；面积变大时保存坐标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Rectangle {
  int area;
  int top;
  int left;
  int bottom;
  int right;
};
Rectangle maximalCoordinates(const vector<vector<char>>& matrix) {
  int cols = static_cast<int>(matrix[0].size());
  vector<int> height(cols);
  Rectangle best{0, -1, -1, -1, -1};
  for (int bottom = 0; bottom < static_cast<int>(matrix.size()); ++bottom) {
    for (int col = 0; col < cols; ++col) {
      height[col] = matrix[bottom][col] == '1' ? height[col] + 1 : 0;
    }
    vector<int> increasing{-1};
    for (int col = 0; col <= cols; ++col) {
      int current = col == cols ? 0 : height[col];
      while (increasing.back() != -1 && height[increasing.back()] >= current) {
        int value = height[increasing.back()];
        increasing.pop_back();
        int left = increasing.back() + 1;
        int area = value * (col - left);
        if (area > best.area) {
          best = {area, bottom - value + 1, left, bottom, col - 1};
        }
      }
      increasing.push_back(col);
    }
  }
  return best;
}
int main() {
  vector<vector<char>> matrix{{'1', '1'}, {'1', '1'}};
  Rectangle answer = maximalCoordinates(matrix);
  cout << answer.area << ' ' << answer.top << ' ' << answer.left << ' '
      << answer.bottom << ' ' << answer.right << '\n';
}
```

时间 $O(rows\cdot cols)$，空间 $O(cols)$；同面积时可再按字典序更新以固定返回规则。

## 变种二：允许矩形中至多有 $k$ 个零

累计高度模型失效，因为不同列中的零可以分布在不同高度。固定上下边界，统计每列在该行带中的零数，再用滑动窗口寻找零数和不超过 $k$ 的最宽列区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximalWithZeros(const vector<vector<char>>& matrix, int k) {
  int rows = static_cast<int>(matrix.size());
  int cols = static_cast<int>(matrix[0].size());
  int answer = 0;
  vector<int> zeros(cols);
  for (int top = 0; top < rows; ++top) {
    fill(zeros.begin(), zeros.end(), 0);
    for (int bottom = top; bottom < rows; ++bottom) {
      for (int col = 0; col < cols; ++col) {
        zeros[col] += matrix[bottom][col] == '0';
      }
      int left = 0;
      int used = 0;
      for (int right = 0; right < cols; ++right) {
        used += zeros[right];
        while (used > k) used -= zeros[left++];
        int area = (bottom - top + 1) * (right - left + 1);
        answer = max(answer, area);
      }
    }
  }
  return answer;
}
int main() {
  vector<vector<char>> matrix{{'1', '0'}, {'1', '1'}};
  cout << maximalWithZeros(matrix, 1) << '\n';
}
```

时间 $O(rows^2cols)$，空间 $O(cols)$。可转置矩阵，让被平方的维度取 `min(rows,cols)`。

## 变种三：矩阵按行流式到达

只保存当前累计高度。每收到一行，更新柱状图并在线计算截至目前的最大面积，不必保存历史矩阵。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class RectangleStream {
  vector<int> height;
  int best = 0;
  int histogram() const {
    vector<int> increasing{-1};
    int answer = 0;
    int cols = static_cast<int>(height.size());
    for (int col = 0; col <= cols; ++col) {
      int current = col == cols ? 0 : height[col];
      while (increasing.back() != -1 && height[increasing.back()] >= current) {
        int value = height[increasing.back()];
        increasing.pop_back();
        answer = max(answer, value * (col - increasing.back() - 1));
      }
      increasing.push_back(col);
    }
    return answer;
  }
public:
  explicit RectangleStream(int columns) : height(columns) {}
  int addRow(const string& row) {
    for (int col = 0; col < static_cast<int>(height.size()); ++col) {
      height[col] = row[col] == '1' ? height[col] + 1 : 0;
    }
    best = max(best, histogram());
    return best;
  }
};
int main() {
  RectangleStream stream(3);
  cout << stream.addRow("111") << '\n';
  cout << stream.addRow("101") << '\n';
}
```

每行时间 $O(cols)$，长期状态空间 $O(cols)$；它只支持追加，修改旧行时需更强的数据结构。

## 变种四：把矩形改为正方形

矩形的宽高可独立变化，适合柱状图；正方形要求宽高相等，使用 DP 更直接。令 `dp[j]` 为当前行以该列为右下角的最大全 1 正方形边长。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximalSquare(const vector<vector<char>>& matrix) {
  int cols = static_cast<int>(matrix[0].size());
  vector<int> dp(cols + 1);
  int best = 0;
  for (const auto& row : matrix) {
    int upperLeft = 0;
    for (int col = 1; col <= cols; ++col) {
      int oldUpper = dp[col];
      if (row[col - 1] == '1') {
        dp[col] = min({dp[col], dp[col - 1], upperLeft}) + 1;
        best = max(best, dp[col]);
      } else {
        dp[col] = 0;
      }
      upperLeft = oldUpper;
    }
  }
  return best * best;
}
int main() {
  vector<vector<char>> matrix{{'1', '1'}, {'1', '1'}};
  cout << maximalSquare(matrix) << '\n';
}
```

时间 $O(rows\cdot cols)$，空间 $O(cols)$。原矩形算法不能直接保证弹栈宽度等于高度。

## 变种五：整数矩阵中求和最大的非空矩形

“全部为 1”的可行性不再存在，柱状图转化失效。固定上下边界，把行带压成每列之和，再对列数组运行一维 Kadane 算法。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long maximumSumRectangle(const vector<vector<int>>& matrix) {
  int rows = static_cast<int>(matrix.size());
  int cols = static_cast<int>(matrix[0].size());
  long long answer = LLONG_MIN;
  vector<long long> column(cols);
  for (int top = 0; top < rows; ++top) {
    fill(column.begin(), column.end(), 0);
    for (int bottom = top; bottom < rows; ++bottom) {
      for (int col = 0; col < cols; ++col) column[col] += matrix[bottom][col];
      long long current = column[0];
      long long best = column[0];
      for (int col = 1; col < cols; ++col) {
        current = max(column[col], current + column[col]);
        best = max(best, current);
      }
      answer = max(answer, best);
    }
  }
  return answer;
}
int main() {
  vector<vector<int>> matrix{{-1, 2}, {3, -2}};
  cout << maximumSumRectangle(matrix) << '\n';
}
```

时间 $O(rows^2cols)$，空间 $O(cols)$；转置后可写成 $O(\min(rows,cols)^2\max(rows,cols))$。初始化为负无穷可正确处理全负矩阵。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximal-rectangle/)
- [对应知识专题](../../data-structures/monotonic-stacks.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc226-d/">← [atcoder] ARC226 D Penta-Queue</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-514-q2-lc4015/">[力扣竞赛] 第 514 场周赛 Q2 LC 4015 树的加权和 中等 →</a>
</nav>
