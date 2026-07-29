---
title: "[力扣 Top 39] LC 59 螺旋矩阵 II 中等"
---

# [力扣 Top 39] LC 59 螺旋矩阵 II 中等

<p class="daily-archive-kicker">2026-07-29 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-29 题目列表</a> · <a href="../../../basics/">进入知识专题</a></p>

## 官方原始信息

- Top 排名：39
- 题号：LC 59
- 官方中文标题：螺旋矩阵 II
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/spiral-matrix-ii/)

### 原始题意

给定正整数 `n`，生成一个 `n × n` 矩阵，使整数 $1$ 到 $n^2$ 从左上角开始按顺时针螺旋顺序填入。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> generateMatrix(int n);
};
```

### 全部官方样例

```text
输入：n = 3
输出：[[1,2,3],[8,9,4],[7,6,5]]
```

```text
输入：n = 1
输出：[[1]]
```

### 全部约束

- $1\le n\le20$。
- 最大写入值为 $n^2\le400$，`int` 安全。
- 输出矩阵本身有 $n^2$ 个元素，所以任何显式构造算法都需要 $\Omega(n^2)$ 时间和输出空间。

## 最优结论

维护尚未填充矩形的四条边界 `top`、`bottom`、`left`、`right`。每轮依次填顶边、右边、底边、左边，然后四条边界向内收缩。每个单元恰好写一次，时间 $O(n^2)$；除返回矩阵外只用 $O(1)$ 空间，达到输出下界。

## 约束与观察

- 方向只在下一步越界或遇到已填位置时改变，因此“方向模拟”和“四边界收缩”是同一个几何过程的两种表达。
- 显式 `visited` 矩阵能降低首次实现难度，但输出矩阵本身的 0 值已经可以充当未访问标记。
- 四边界法把转向条件提升到整条边，分支更少，也更容易证明每格只写一次。
- 奇数阶矩阵最后剩一个中心格，循环条件必须允许单行或单列剩余区域。

## 解法递进

### 解法一：逐步模拟方向

沿右、下、左、上四个方向前进；下一格越界或已填时转向。时间 $O(n^2)$、除输出外空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> generateMatrix(int n) {
    vector<vector<int>> matrix(n, vector<int>(n, 0));
    const array<int, 4> rowChange{0, 1, 0, -1};
    const array<int, 4> columnChange{1, 0, -1, 0};
    int row = 0;
    int column = 0;
    int direction = 0;
    for (int value = 1; value <= n * n; ++value) {
      matrix[row][column] = value;
      int nextRow = row + rowChange[direction];
      int nextColumn = column + columnChange[direction];
      bool blocked = nextRow < 0 || nextRow >= n || nextColumn < 0 || nextColumn >= n ||
          matrix[nextRow][nextColumn] != 0;
      if (blocked) {
        direction = (direction + 1) % 4;
        nextRow = row + rowChange[direction];
        nextColumn = column + columnChange[direction];
      }
      row = nextRow;
      column = nextColumn;
    }
    return matrix;
  }
};
```

### 解法二：四边界逐层收缩

每条边只写当前尚未处理部分，边界收缩后不会再次访问。时间 $O(n^2)$，额外空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> generateMatrix(int n) {
    vector<vector<int>> matrix(n, vector<int>(n));
    int top = 0;
    int bottom = n - 1;
    int left = 0;
    int right = n - 1;
    int value = 1;
    while (top <= bottom && left <= right) {
      for (int column = left; column <= right; ++column) {
        matrix[top][column] = value++;
      }
      ++top;
      for (int row = top; row <= bottom; ++row) {
        matrix[row][right] = value++;
      }
      --right;
      if (top <= bottom) {
        for (int column = right; column >= left; --column) {
          matrix[bottom][column] = value++;
        }
        --bottom;
      }
      if (left <= right) {
        for (int row = bottom; row >= top; --row) {
          matrix[row][left] = value++;
        }
        ++left;
      }
    }
    return matrix;
  }
};
```

## 正确性证明

循环开始时，边界围成的矩形恰好是全部尚未填充单元。算法按顺时针顺序写其顶边、右边、底边和左边；底边、左边只有在对应维度仍存在时才写，因此角点不会重复。随后四边界各向内移动一格，新的矩形正好删去了本轮写完的外环，不变量保持。边界交错时不存在未填单元，循环结束。每次写入值递增一，所以最终矩阵恰按要求包含 $1$ 到 $n^2$。

## 样例手推

`n=3` 时，第一轮依次填：

- 顶边：1、2、3；
- 右边：4、5；
- 底边反向：6、7；
- 左边向上：8。

四边界收缩后只剩中心 `(1,1)`，填入 9，得到 `[[1,2,3],[8,9,4],[7,6,5]]`。

## 易错点

- 顶边和右边写完后，剩余区域可能已经为空；底边和左边必须带边界判断。
- 模拟法最后一次写入后计算出的“下一位置”不会再访问，虽可越界但不能拿它继续索引。
- 矩形版本中单行、单列更容易发生重复写角点。
- 本题要求顺时针且从左上向右开始，改变起点或方向必须重新定义边的顺序。

## 验证说明

对 $n=1\ldots20$ 比较方向模拟与四边界结果；同时验证每个值 $1\ldots n^2$ 恰好出现一次，并按螺旋读取矩阵时得到严格递增序列。

## Follow-up 与变种

### 变种一：生成 `m × n` 的顺时针螺旋矩阵

四边界本来就适用于矩形，只需把行列上界分开。时间 $O(mn)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> generateRectangle(int rows, int columns) {
    vector<vector<int>> matrix(rows, vector<int>(columns));
    int top = 0;
    int bottom = rows - 1;
    int left = 0;
    int right = columns - 1;
    int value = 1;
    while (top <= bottom && left <= right) {
      for (int column = left; column <= right; ++column) {
        matrix[top][column] = value++;
      }
      ++top;
      for (int row = top; row <= bottom; ++row) {
        matrix[row][right] = value++;
      }
      --right;
      if (top <= bottom) {
        for (int column = right; column >= left; --column) {
          matrix[bottom][column] = value++;
        }
        --bottom;
      }
      if (left <= right) {
        for (int row = bottom; row >= top; --row) {
          matrix[row][left] = value++;
        }
        ++left;
      }
    }
    return matrix;
  }
};
```

### 变种二：已有矩阵，按螺旋顺序读取

边界移动完全相同，只把写入改成读取。时间 $O(mn)$，除答案外空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> spiralOrder(vector<vector<int>>& matrix) {
    vector<int> answer;
    int top = 0;
    int bottom = static_cast<int>(matrix.size()) - 1;
    int left = 0;
    int right = static_cast<int>(matrix[0].size()) - 1;
    while (top <= bottom && left <= right) {
      for (int column = left; column <= right; ++column) {
        answer.push_back(matrix[top][column]);
      }
      ++top;
      for (int row = top; row <= bottom; ++row) {
        answer.push_back(matrix[row][right]);
      }
      --right;
      if (top <= bottom) {
        for (int column = right; column >= left; --column) {
          answer.push_back(matrix[bottom][column]);
        }
        --bottom;
      }
      if (left <= right) {
        for (int row = bottom; row >= top; --row) {
          answer.push_back(matrix[row][left]);
        }
        ++left;
      }
    }
    return answer;
  }
};
```

### 变种三：从左上角开始逆时针填充

每层依次写左边、底边、右边、顶边，并使用同样的防重复判断。时间 $O(mn)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> counterclockwise(int rows, int columns) {
    vector<vector<int>> matrix(rows, vector<int>(columns));
    int top = 0;
    int bottom = rows - 1;
    int left = 0;
    int right = columns - 1;
    int value = 1;
    while (top <= bottom && left <= right) {
      for (int row = top; row <= bottom; ++row) {
        matrix[row][left] = value++;
      }
      ++left;
      for (int column = left; column <= right; ++column) {
        matrix[bottom][column] = value++;
      }
      --bottom;
      if (left <= right) {
        for (int row = bottom; row >= top; --row) {
          matrix[row][right] = value++;
        }
        --right;
      }
      if (top <= bottom) {
        for (int column = right; column >= left; --column) {
          matrix[top][column] = value++;
        }
        ++top;
      }
    }
    return matrix;
  }
};
```

### 变种四：不构造矩阵，查询坐标 `(r,c)` 的值

坐标所在层为 $d=\min(r,c,n-1-r,n-1-c)$。该层边长 $s=n-2d$，起始值为 $n^2-s^2+1$；再按坐标位于哪条边求周长偏移。每次查询 $O(1)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long valueAt(int n, int row, int column) {
    int layer = min({row, column, n - 1 - row, n - 1 - column});
    int side = n - 2 * layer;
    long long start = 1LL * n * n - 1LL * side * side + 1;
    if (side == 1) {
      return start;
    }
    int last = n - 1 - layer;
    long long offset;
    if (row == layer) {
      offset = column - layer;
    } else if (column == last) {
      offset = side - 1 + row - layer;
    } else if (row == last) {
      offset = 2LL * (side - 1) + last - column;
    } else {
      offset = 3LL * (side - 1) + last - row;
    }
    return start + offset;
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/spiral-matrix-ii/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/spiral-matrix-ii/)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-38-lc46/">← [力扣 Top 38] LC 46 全排列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-40-lc236/">[力扣 Top 40] LC 236 二叉树的最近公共祖先 中等 →</a>
</nav>
