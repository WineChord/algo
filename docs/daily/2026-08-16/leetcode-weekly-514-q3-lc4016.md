---
title: "[力扣竞赛] 第 514 场周赛 Q3 LC 4016 两个不重叠子正方形的最大面积 中等"
---

# [力扣竞赛] 第 514 场周赛 Q3 LC 4016 两个不重叠子正方形的最大面积 中等

<p class="daily-archive-kicker">2026-08-16 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-16 题目列表</a> · <a href="../../../dp/grid-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=88a41186c00d899847f5cecada59ee1a49b1eadc0d17d21741e7ed2c6d2e11f4 -->
[力扣 4016：两个不重叠子正方形的最大面积](https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/)

## 官方原始信息

- 来源：第 514 场周赛 Q3。
- 题号：4016。
- 官方中文标题：两个不重叠子正方形的最大面积。
- 官方难度：中等。
- 官方竞赛分值：5 分。
- ZeroTracer 社区估算竞赛分：截至 2026-08-16 的公开数据中暂无该题数值。
- 函数签名：`int maxArea(vector<vector<int>>& mat)`。

给定一个 `m × n` 的 0/1 矩阵。要选择两个边长相同的正方形子矩阵；二者不能共享单元格，
并且覆盖的每个单元格都必须为 1。返回每个正方形能达到的最大面积；若连两个边长为 1
的正方形都无法选择，返回 0。

### 全部官方样例

样例 1：

```text
输入：mat = [[1,1,1,0],[1,1,1,1],[0,0,1,1]]
输出：4
```

可以选择左上角为 `(0,0)` 与 `(1,2)` 的两个 `2 × 2` 全 1 正方形，二者不重叠。

样例 2：

```text
输入：mat = [[0,1],[1,0]]
输出：1
```

两个值为 1 的单元格各自构成边长为 1 的正方形。

样例 3：

```text
输入：mat = [[0,0],[0,1]]
输出：0
```

矩阵只有一个可用单元格，无法选出两个正方形。

### 全部官方约束

- `mat.length == m`。
- `mat[i].length == n`。
- `1 <= m, n <= 500`。
- `mat[i][j]` 只可能是 0 或 1。

## 约束与关键几何观察

若逐对枚举正方形，候选左上角有 $O(mn)$ 个，候选对有 $O(m^2n^2)$ 个，远超
`500 × 500` 的规模。需要同时利用两个结构：

1. 全 1 正方形可以用二维前缀和或最大正方形动态规划快速判定；
2. 两个轴对齐正方形不相交，当且仅当它们的行区间不相交，或列区间不相交。

第二点意味着任意合法答案都能被一条水平分割线或垂直分割线隔开。这会把“四维枚举两个
正方形”降为“枚举一条分割线并比较两侧的最大正方形”。

面积最多为 $500^2=250000$，`int` 安全。动态规划的边长也不超过 500。

## 样例手推与边界

样例 1 中，最大正方形动态规划会在 `(1,1)` 得到边长 2，在 `(2,3)` 也得到边长 2。
第一块的列区间是 `[0,1]`，第二块是 `[2,3]`，可由列 1 与列 2 之间的垂直线隔开，
所以答案边长至少为 2。矩阵只有 3 行，不可能容纳两个不重叠的 `3 × 3` 正方形，答案为 4。

- `1 × 1` 矩阵：最多只有一个正方形，答案为 0。
- 只有一行：仍可由垂直分割线隔开两个边长为 1 的正方形。
- 全 0：所有动态规划值为 0。
- 全 1：答案由能否在行或列方向并排放下两个同边长正方形决定。
- 两个正方形可以接触边界或彼此贴边；只禁止共享单元格。

## 解法一：完整枚举作为暴力 oracle

枚举边长、两个左上角，再逐格检查两个正方形是否全 1，最后检查行区间或列区间是否分离。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool allOnes(const vector<vector<int>>& mat, int row, int column, int side) {
    for (int i = row; i < row + side; ++i) {
      for (int j = column; j < column + side; ++j) {
        if (mat[i][j] == 0) return false;
      }
    }
    return true;
  }
public:
  int maxArea(vector<vector<int>>& mat) {
    int rows = static_cast<int>(mat.size());
    int columns = static_cast<int>(mat[0].size());
    int best = 0;
    for (int side = 1; side <= min(rows, columns); ++side) {
      for (int r1 = 0; r1 + side <= rows; ++r1) {
        for (int c1 = 0; c1 + side <= columns; ++c1) {
          if (!allOnes(mat, r1, c1, side)) continue;
          for (int r2 = r1; r2 + side <= rows; ++r2) {
            for (int c2 = 0; c2 + side <= columns; ++c2) {
              if (r1 == r2 && c2 <= c1) continue;
              bool separated = abs(r1 - r2) >= side ||
                  abs(c1 - c2) >= side;
              if (separated && allOnes(mat, r2, c2, side)) {
                best = side * side;
              }
            }
          }
        }
      }
    }
    return best;
  }
};
```

该写法的候选对和逐格检查都很昂贵，最坏远高于 $O(m^2n^2)$，只适合很小矩阵做 oracle。

## 解法二：二维前缀和、单调性与二分答案

二维前缀和让一个 `k × k` 正方形是否全 1 可在 $O(1)$ 判定。对固定 `k`，记录所有合法
左上角的最小/最大行与列。存在两个不重叠正方形，当且仅当

$$
\max row-\min row\ge k
\quad\text{或}\quad
\max column-\min column\ge k.
$$

若边长 `k` 可行，把两个正方形各自裁成更小的同边长正方形仍不重叠，因此可行性对 `k`
单调，可以二分最大边长。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxArea(vector<vector<int>>& mat) {
    int rows = static_cast<int>(mat.size());
    int columns = static_cast<int>(mat[0].size());
    vector<vector<int>> prefix(rows + 1, vector<int>(columns + 1));
    for (int i = 0; i < rows; ++i) {
      for (int j = 0; j < columns; ++j) {
        prefix[i + 1][j + 1] = mat[i][j] + prefix[i][j + 1] +
            prefix[i + 1][j] - prefix[i][j];
      }
    }
    auto squareSum = [&](int row, int column, int side) {
      return prefix[row + side][column + side] -
          prefix[row][column + side] - prefix[row + side][column] +
          prefix[row][column];
    };
    auto feasible = [&](int side) {
      int minimumRow = rows;
      int maximumRow = -1;
      int minimumColumn = columns;
      int maximumColumn = -1;
      for (int i = 0; i + side <= rows; ++i) {
        for (int j = 0; j + side <= columns; ++j) {
          if (squareSum(i, j, side) != side * side) continue;
          minimumRow = min(minimumRow, i);
          maximumRow = max(maximumRow, i);
          minimumColumn = min(minimumColumn, j);
          maximumColumn = max(maximumColumn, j);
        }
      }
      return maximumRow - minimumRow >= side ||
          maximumColumn - minimumColumn >= side;
    };
    int low = 0;
    int high = min(rows, columns) + 1;
    while (low + 1 < high) {
      int middle = (low + high) / 2;
      if (feasible(middle)) low = middle;
      else high = middle;
    }
    return low * low;
  }
};
```

时间 $O(mn\log\min(m,n))$，空间 $O(mn)$。它已经能通过约束，且与官方提示的思路一致。

## 从二分到线性：分割线两侧的最大正方形

标准最大正方形动态规划令 `end[i][j]` 为以 `(i,j)` 为右下角的最大全 1 正方形边长：

$$
end_{i,j}=1+\min(end_{i-1,j},end_{i,j-1},end_{i-1,j-1}).
$$

再反向计算 `start[i][j]`，表示以 `(i,j)` 为左上角的最大边长。由 `end` 得到每个行前缀、
列前缀内的最大正方形；由 `start` 得到每个行后缀、列后缀内的最大正方形。

枚举水平分割线时，若上侧最大边长为 `a`、下侧为 `b`，两边都能裁出边长
`min(a,b)` 的正方形。垂直分割线同理。这样一次扫描就覆盖全部可能答案。

## 最佳实用解

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxArea(vector<vector<int>>& mat) {
    int rows = static_cast<int>(mat.size());
    int columns = static_cast<int>(mat[0].size());
    vector<vector<int>> ending(rows, vector<int>(columns));
    vector<vector<int>> starting(rows, vector<int>(columns));
    vector<int> top(rows), bottom(rows), left(columns), right(columns);
    for (int i = 0; i < rows; ++i) {
      for (int j = 0; j < columns; ++j) {
        if (mat[i][j] == 0) continue;
        ending[i][j] = 1;
        if (i > 0 && j > 0) {
          ending[i][j] += min({ending[i - 1][j], ending[i][j - 1],
              ending[i - 1][j - 1]});
        }
        top[i] = max(top[i], ending[i][j]);
        left[j] = max(left[j], ending[i][j]);
      }
    }
    for (int i = rows - 1; i >= 0; --i) {
      for (int j = columns - 1; j >= 0; --j) {
        if (mat[i][j] == 0) continue;
        starting[i][j] = 1;
        if (i + 1 < rows && j + 1 < columns) {
          starting[i][j] += min({starting[i + 1][j], starting[i][j + 1],
              starting[i + 1][j + 1]});
        }
        bottom[i] = max(bottom[i], starting[i][j]);
        right[j] = max(right[j], starting[i][j]);
      }
    }
    for (int i = 1; i < rows; ++i) top[i] = max(top[i], top[i - 1]);
    for (int i = rows - 2; i >= 0; --i) {
      bottom[i] = max(bottom[i], bottom[i + 1]);
    }
    for (int j = 1; j < columns; ++j) left[j] = max(left[j], left[j - 1]);
    for (int j = columns - 2; j >= 0; --j) {
      right[j] = max(right[j], right[j + 1]);
    }
    int side = 0;
    for (int i = 0; i + 1 < rows; ++i) {
      side = max(side, min(top[i], bottom[i + 1]));
    }
    for (int j = 0; j + 1 < columns; ++j) {
      side = max(side, min(left[j], right[j + 1]));
    }
    return side * side;
  }
};
```

时间复杂度 $O(mn)$，空间复杂度 $O(mn)$。它消除了二分的对数因子，同时保留清晰证明，
是应优先记忆的方案。二分方案更贴近官方提示，适合作为从前缀和过渡到最优解的中间层。

## 正确性证明

最大正方形递推正确：若 `(i,j)` 为 0，任何以它为右下角的全 1 正方形边长为 0；若为 1，
向左上扩一层所能达到的边长由上、左、左上三个相邻状态的最小值限制。反向递推同理。

对任意两个不重叠的轴对齐正方形，它们的行区间或列区间至少有一个不相交。前一种情况
存在一条水平分割线把二者分在两侧，算法枚举该线时，两侧最大边长分别不小于这两个正方形
的边长；取两者最小值不会小于该合法答案。后一种情况由某条垂直分割线覆盖。

反过来，算法在某条分割线两侧各选一个最大正方形，并把较大的裁成共同较小边长。
两块完全位于分割线两侧，所以必不共享单元格，且裁剪仍保持全 1。因此算法产生的每个候选
都合法。上下界一致，返回面积最优。

## 同阶方案比较

- 线性分割 DP：$O(mn)$，证明利用“任意两个不相交矩形可被横线或竖线分开”，常数最小。
- 前缀和加二分：$O(mn\log\min(m,n))$，代码中的可行性检查更独立，容易推广到额外间距。
- 两者空间都是 $O(mn)$；若极限压缩空间，可以分多遍滚动计算边界摘要，但实现更易错。

面试中先讲前缀和、极值与二分，再主动指出分割线 DP 可去掉对数因子，层次最清楚。

## 易错点

- 不重叠条件是“行分离或列分离”，不能误写成同时分离。
- 两个正方形必须边长相同；分割线两侧大小不同时要取 `min`，而不是取 `max`。
- 反向 DP 表示左上角，不可继续使用右下角状态，否则后缀摘要会包含跨过分割线的方块。
- 返回面积 `side * side`，不是边长。
- 单行或单列仍要检查垂直或水平分割；不要预先要求 `m,n >= 2`。

## 验证说明

以完整枚举为 oracle，对所有 `1..5 × 1..5` 尺寸的随机 0/1 矩阵比较二分方案和线性方案；
另覆盖全 0、全 1、棋盘格、单个 1、仅两角为 1 以及两个方块贴边等构造。所有发布代码使用
C++23 编译，并核对三个官方样例。

## 变种一：恢复两个最优正方形的位置

新定义要求返回两个左上角与边长。给每个前缀/后缀摘要同时保存产生最大值的方块；若一侧
更大，只取其左上角处的共同边长子方块即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Square {
  int side = 0;
  int row = -1;
  int column = -1;
};
struct Answer {
  Square first;
  Square second;
};
Answer recoverSquares(const vector<vector<int>>& mat) {
  int m = static_cast<int>(mat.size());
  int n = static_cast<int>(mat[0].size());
  vector<vector<int>> end(m, vector<int>(n)), start(m, vector<int>(n));
  vector<Square> top(m), bottom(m), left(n), right(n);
  auto keep = [](Square& best, Square candidate) {
    if (candidate.side > best.side) best = candidate;
  };
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
      if (!mat[i][j]) continue;
      end[i][j] = 1;
      if (i && j) end[i][j] += min({end[i - 1][j], end[i][j - 1],
          end[i - 1][j - 1]});
      Square square{end[i][j], i - end[i][j] + 1, j - end[i][j] + 1};
      keep(top[i], square);
      keep(left[j], square);
    }
  }
  for (int i = m - 1; i >= 0; --i) {
    for (int j = n - 1; j >= 0; --j) {
      if (!mat[i][j]) continue;
      start[i][j] = 1;
      if (i + 1 < m && j + 1 < n) {
        start[i][j] += min({start[i + 1][j], start[i][j + 1],
            start[i + 1][j + 1]});
      }
      Square square{start[i][j], i, j};
      keep(bottom[i], square);
      keep(right[j], square);
    }
  }
  for (int i = 1; i < m; ++i) keep(top[i], top[i - 1]);
  for (int i = m - 2; i >= 0; --i) keep(bottom[i], bottom[i + 1]);
  for (int j = 1; j < n; ++j) keep(left[j], left[j - 1]);
  for (int j = n - 2; j >= 0; --j) keep(right[j], right[j + 1]);
  Answer answer;
  auto consider = [&](Square a, Square b) {
    int side = min(a.side, b.side);
    if (side > answer.first.side) {
      a.side = b.side = side;
      answer = {a, b};
    }
  };
  for (int i = 0; i + 1 < m; ++i) consider(top[i], bottom[i + 1]);
  for (int j = 0; j + 1 < n; ++j) consider(left[j], right[j + 1]);
  return answer;
}
int main() {
  int m, n;
  cin >> m >> n;
  vector<vector<int>> mat(m, vector<int>(n));
  for (auto& row : mat) for (int& value : row) cin >> value;
  Answer answer = recoverSquares(mat);
  cout << answer.first.side << '\n';
  if (answer.first.side) {
    cout << answer.first.row << ' ' << answer.first.column << '\n';
    cout << answer.second.row << ' ' << answer.second.column << '\n';
  }
}
```

时间和空间仍为 $O(mn)$。

## 变种二：两个正方形边长可以不同，最大化面积和

原题取两侧边长的最小值；允许不同大小后，同一分割线两侧的最大方块可以全部保留，候选值
改为 $a^2+b^2$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximumTotalArea(const vector<vector<int>>& mat) {
  int m = static_cast<int>(mat.size());
  int n = static_cast<int>(mat[0].size());
  vector<vector<int>> end(m, vector<int>(n)), start(m, vector<int>(n));
  vector<int> top(m), bottom(m), left(n), right(n);
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) if (mat[i][j]) {
      end[i][j] = 1;
      if (i && j) end[i][j] += min({end[i - 1][j], end[i][j - 1],
          end[i - 1][j - 1]});
      top[i] = max(top[i], end[i][j]);
      left[j] = max(left[j], end[i][j]);
    }
  }
  for (int i = m - 1; i >= 0; --i) {
    for (int j = n - 1; j >= 0; --j) if (mat[i][j]) {
      start[i][j] = 1;
      if (i + 1 < m && j + 1 < n) {
        start[i][j] += min({start[i + 1][j], start[i][j + 1],
            start[i + 1][j + 1]});
      }
      bottom[i] = max(bottom[i], start[i][j]);
      right[j] = max(right[j], start[i][j]);
    }
  }
  for (int i = 1; i < m; ++i) top[i] = max(top[i], top[i - 1]);
  for (int i = m - 2; i >= 0; --i) bottom[i] = max(bottom[i], bottom[i + 1]);
  for (int j = 1; j < n; ++j) left[j] = max(left[j], left[j - 1]);
  for (int j = n - 2; j >= 0; --j) right[j] = max(right[j], right[j + 1]);
  int answer = 0;
  for (int i = 0; i + 1 < m; ++i) {
    answer = max(answer, top[i] * top[i] + bottom[i + 1] * bottom[i + 1]);
  }
  for (int j = 0; j + 1 < n; ++j) {
    answer = max(answer, left[j] * left[j] + right[j + 1] * right[j + 1]);
  }
  return answer;
}
int main() {
  int m, n;
  cin >> m >> n;
  vector<vector<int>> mat(m, vector<int>(n));
  for (auto& row : mat) for (int& value : row) cin >> value;
  cout << maximumTotalArea(mat) << '\n';
}
```

时间、空间均为 $O(mn)$；原来的共同边长约束失效，但分割线结构仍成立。

## 变种三：两个正方形之间至少留 `gap` 行或列

固定边长 `k` 时，左上角行差或列差必须至少为 `k + gap`。前缀和可行性检查只需修改
阈值，单调性仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximumAreaWithGap(const vector<vector<int>>& mat, int gap) {
  int m = static_cast<int>(mat.size());
  int n = static_cast<int>(mat[0].size());
  vector<vector<int>> sum(m + 1, vector<int>(n + 1));
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
      sum[i + 1][j + 1] = mat[i][j] + sum[i][j + 1] +
          sum[i + 1][j] - sum[i][j];
    }
  }
  auto feasible = [&](int side) {
    int minRow = m, maxRow = -1, minColumn = n, maxColumn = -1;
    for (int i = 0; i + side <= m; ++i) {
      for (int j = 0; j + side <= n; ++j) {
        int value = sum[i + side][j + side] - sum[i][j + side] -
            sum[i + side][j] + sum[i][j];
        if (value != side * side) continue;
        minRow = min(minRow, i);
        maxRow = max(maxRow, i);
        minColumn = min(minColumn, j);
        maxColumn = max(maxColumn, j);
      }
    }
    return maxRow - minRow >= side + gap ||
        maxColumn - minColumn >= side + gap;
  };
  int low = 0, high = min(m, n) + 1;
  while (low + 1 < high) {
    int middle = (low + high) / 2;
    if (feasible(middle)) low = middle;
    else high = middle;
  }
  return low * low;
}
int main() {
  int m, n, gap;
  cin >> m >> n >> gap;
  vector<vector<int>> mat(m, vector<int>(n));
  for (auto& row : mat) for (int& value : row) cin >> value;
  cout << maximumAreaWithGap(mat, gap) << '\n';
}
```

时间 $O(mn\log\min(m,n))$，空间 $O(mn)$。

## 变种四：固定边长 `k`，统计不重叠正方形对数

先列出所有全 1 的 `k × k` 左上角。总对数减去重叠对数即可；按行扫描并用树状数组维护
最近 `k - 1` 行的列坐标，统计列差也小于 `k` 的先前候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Fenwick {
  vector<int> tree;
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index, int value) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += value;
    }
  }
  int sumPrefix(int index) const {
    int result = 0;
    for (++index; index > 0; index -= index & -index) result += tree[index];
    return result;
  }
  int range(int left, int right) const {
    if (left > right) return 0;
    return sumPrefix(right) - (left ? sumPrefix(left - 1) : 0);
  }
};
long long countPairs(const vector<vector<int>>& mat, int side) {
  int m = static_cast<int>(mat.size());
  int n = static_cast<int>(mat[0].size());
  vector<vector<int>> sum(m + 1, vector<int>(n + 1));
  for (int i = 0; i < m; ++i) for (int j = 0; j < n; ++j) {
    sum[i + 1][j + 1] = mat[i][j] + sum[i][j + 1] +
        sum[i + 1][j] - sum[i][j];
  }
  vector<pair<int, int>> squares;
  for (int i = 0; i + side <= m; ++i) for (int j = 0; j + side <= n; ++j) {
    int value = sum[i + side][j + side] - sum[i][j + side] -
        sum[i + side][j] + sum[i][j];
    if (value == side * side) squares.push_back({i, j});
  }
  Fenwick active(n);
  long long overlapping = 0;
  int first = 0;
  for (int index = 0; index < static_cast<int>(squares.size()); ++index) {
    auto [row, column] = squares[index];
    while (first < index && squares[first].first <= row - side) {
      active.add(squares[first].second, -1);
      ++first;
    }
    overlapping += active.range(max(0, column - side + 1),
        min(n - 1, column + side - 1));
    active.add(column, 1);
  }
  long long total = static_cast<long long>(squares.size()) *
      (static_cast<long long>(squares.size()) - 1) / 2;
  return total - overlapping;
}
int main() {
  int m, n, side;
  cin >> m >> n >> side;
  vector<vector<int>> mat(m, vector<int>(n));
  for (auto& row : mat) for (int& value : row) cin >> value;
  cout << countPairs(mat, side) << '\n';
}
```

设合法方块数为 `P`，时间 $O(mn+P\log n)$，空间 $O(mn+P)$。

## 变种五：小矩阵上的在线翻转与查询

若矩阵尺寸不超过 60，但有多次单点 0/1 翻转，每次更新后可直接重算线性 DP。原算法不支持
增量维护；在小规模约束下，重建比复杂二维动态结构更稳定。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int solve(const vector<vector<int>>& mat) {
  int m = static_cast<int>(mat.size());
  int n = static_cast<int>(mat[0].size());
  vector<vector<int>> end(m, vector<int>(n)), start(m, vector<int>(n));
  vector<int> top(m), bottom(m), left(n), right(n);
  for (int i = 0; i < m; ++i) for (int j = 0; j < n; ++j) if (mat[i][j]) {
    end[i][j] = 1;
    if (i && j) end[i][j] += min({end[i - 1][j], end[i][j - 1],
        end[i - 1][j - 1]});
    top[i] = max(top[i], end[i][j]);
    left[j] = max(left[j], end[i][j]);
  }
  for (int i = m - 1; i >= 0; --i) {
    for (int j = n - 1; j >= 0; --j) if (mat[i][j]) {
      start[i][j] = 1;
      if (i + 1 < m && j + 1 < n) {
        start[i][j] += min({start[i + 1][j], start[i][j + 1],
            start[i + 1][j + 1]});
      }
      bottom[i] = max(bottom[i], start[i][j]);
      right[j] = max(right[j], start[i][j]);
    }
  }
  for (int i = 1; i < m; ++i) top[i] = max(top[i], top[i - 1]);
  for (int i = m - 2; i >= 0; --i) bottom[i] = max(bottom[i], bottom[i + 1]);
  for (int j = 1; j < n; ++j) left[j] = max(left[j], left[j - 1]);
  for (int j = n - 2; j >= 0; --j) right[j] = max(right[j], right[j + 1]);
  int side = 0;
  for (int i = 0; i + 1 < m; ++i) side = max(side, min(top[i], bottom[i + 1]));
  for (int j = 0; j + 1 < n; ++j) side = max(side, min(left[j], right[j + 1]));
  return side * side;
}
int main() {
  int m, n, queries;
  cin >> m >> n >> queries;
  vector<vector<int>> mat(m, vector<int>(n));
  for (auto& row : mat) for (int& value : row) cin >> value;
  while (queries--) {
    int row, column;
    cin >> row >> column;
    mat[row][column] ^= 1;
    cout << solve(mat) << '\n';
  }
}
```

每次更新 $O(mn)$，空间 $O(mn)$；若尺寸和查询数同时很大，才需要新的分块或动态二维结构。

## 来源

- [力扣 4016 官方题面](https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/)
- [第 514 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-514/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/)
- [对应知识专题](../../dp/grid-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-136-lc118/">← [力扣 Top 136] LC 118 杨辉三角 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-e/">[codeforces] CF Round 1116 Div.1 C / Div.2 E Even If the World Turns →</a>
</nav>
