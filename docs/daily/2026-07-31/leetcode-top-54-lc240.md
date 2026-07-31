---
title: "[力扣 Top 54] LC 240 搜索二维矩阵 II 中等"
---

# [力扣 Top 54] LC 240 搜索二维矩阵 II 中等

<p class="daily-archive-kicker">2026-07-31 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=19d7ea849c30f04ab485b855f77cdb19b10cf165bd2c879bfea099f5c3768f17 -->
## 官方原始信息

- Top 排名：54
- 题号：LC 240
- 官方中文标题：搜索二维矩阵 II
- 官方难度：中等
- 官方链接：[搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)

### 原始题意

在 $m\times n$ 矩阵中查找 `target`。每行从左到右非降，每列从上到下非降。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target);
};
```

### 全部官方样例

```text
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true
```

```text
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
输出：false
```

### 全部约束

- `m == matrix.length`，`n == matrix[i].length`。
- $1\le m,n\le300$。
- $-10^9\le matrix_{i,j},target\le10^9$。
- 每行从左到右非降，每列从上到下非降。

## 约束推导与边界

总元素最多 $9\times10^4$，逐行二分已足够，但没有同时利用列有序性。从右上角看，向左严格不增、向下严格不减：一次比较就能排除整列或整行。重复值不影响方向判断。矩阵按约束非空，不需要额外处理空行，但通用实现仍可防御。

## 解法递进

### 解法一：每行二分

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    for (const auto& row : matrix) {
      if (binary_search(row.begin(), row.end(), target)) {
        return true;
      }
    }
    return false;
  }
};
```

时间 $O(m\log n)$，空间 $O(1)$。

### 最佳实用解：右上角阶梯搜索

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    int row = 0;
    int column = static_cast<int>(matrix[0].size()) - 1;
    while (row < static_cast<int>(matrix.size()) && column >= 0) {
      if (matrix[row][column] == target) {
        return true;
      }
      if (matrix[row][column] > target) {
        --column;
      } else {
        ++row;
      }
    }
    return false;
  }
};
```

时间 $O(m+n)$，空间 $O(1)$。

## 正确性证明

当前候选区域是行 `[row,m)` 与列 `[0,column]` 的矩形。若右上角值大于目标，同列下方值只会更大，因此该列不可能含目标，可以删列；若小于目标，同一行左侧值只会更小，因此该行不可能含目标，可以删行。相等时显然找到。每步只删除不可能区域且候选至少缩小一行或一列，退出矩形时若未找到，目标不存在。

## 样例手推

查找 5 时从 15 开始，连续左移到 4；4 小于 5，向下到 5 并命中。查找 20 时也会沿一条至多 $m+n-1$ 个格子的阶梯路径离开矩阵。

## 易错点与方案比较

- 不能从左上角开始，因为右移和下移都会增大，比较后无法唯一排除一维。
- “升序”允许重复值；算法不依赖严格递增。
- 从左下角也可对称实现，复杂度相同。
- 当 $m\ll n$ 时逐行二分可能常数更好；默认推荐阶梯搜索，证明与实现最简洁。

## 变种一：返回任意一个目标坐标

沿相同阶梯路径，命中时输出行列；不存在输出 `-1 -1`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, target;
  cin >> m >> n >> target;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  int row = 0;
  int column = n - 1;
  while (row < m && column >= 0 && matrix[row][column] != target) {
    if (matrix[row][column] > target) {
      --column;
    } else {
      ++row;
    }
  }
  if (row < m && column >= 0) {
    cout << row << ' ' << column << '\n';
  } else {
    cout << "-1 -1\n";
  }
}
```

时间 $O(m+n)$，空间 $O(1)$。

## 变种二：统计不大于目标的元素数

从左下角出发；若当前值不大于目标，则该列上方共 `row + 1` 个值都合格，并右移。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countAtMost(const vector<vector<int>>& matrix, int target) {
  int row = static_cast<int>(matrix.size()) - 1;
  int column = 0;
  long long count = 0;
  while (row >= 0 && column < static_cast<int>(matrix[0].size())) {
    if (matrix[row][column] <= target) {
      count += row + 1;
      ++column;
    } else {
      --row;
    }
  }
  return count;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, target;
  cin >> m >> n >> target;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  cout << countAtMost(matrix, target) << '\n';
}
```

时间 $O(m+n)$，空间 $O(1)$。

## 变种三：求矩阵中的第 k 小值

在值域上二分，用上一个变种统计不大于中值的元素数。重复值按出现次数计。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countAtMost(const vector<vector<int>>& matrix, long long target) {
  int row = static_cast<int>(matrix.size()) - 1;
  int column = 0;
  long long count = 0;
  while (row >= 0 && column < static_cast<int>(matrix[0].size())) {
    if (matrix[row][column] <= target) {
      count += row + 1;
      ++column;
    } else {
      --row;
    }
  }
  return count;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n;
  long long k;
  cin >> m >> n >> k;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  long long low = matrix[0][0];
  long long high = matrix[m - 1][n - 1];
  while (low < high) {
    long long middle = low + (high - low) / 2;
    if (countAtMost(matrix, middle) >= k) {
      high = middle;
    } else {
      low = middle + 1;
    }
  }
  cout << low << '\n';
}
```

时间 $O((m+n)\log W)$，其中 $W$ 是值域宽度；空间 $O(1)$。

## 变种四：同一矩阵有大量目标查询

逐行保存有序数组，每次查询在所有行二分；相比逐次阶梯搜索，瘦高矩阵或缓存友好场景可能更合适。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, q;
  cin >> m >> n >> q;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  while (q--) {
    int target;
    cin >> target;
    bool found = false;
    for (const auto& row : matrix) {
      found = found || binary_search(row.begin(), row.end(), target);
    }
    cout << (found ? "YES\n" : "NO\n");
  }
}
```

每次查询 $O(m\log n)$，额外空间 $O(1)$。

## 可复现验证

随机生成非负增量矩阵以保证行列有序，把阶梯搜索与全矩阵扫描逐例比较；对计数与第 k 小变种再与展平排序结果比较。覆盖单行、单列、重复值和目标越界。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/search-a-2d-matrix-ii/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/search-a-2d-matrix-ii/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-53-lc207/">← [力扣 Top 53] LC 207 课程表 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-55-lc131/">[力扣 Top 55] LC 131 分割回文串 中等 →</a>
</nav>
