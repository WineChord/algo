---
title: "[力扣 Top 120] LC 74 搜索二维矩阵 中等"
---

# [力扣 Top 120] LC 74 搜索二维矩阵 中等

<p class="daily-archive-kicker">2026-08-06 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ba6c9aa1b76f391b2874c6fd28d623993fdcd05bf318d8f7c619541c41f2cedc -->
## 官方原始信息

- Top 排名：120
- 题号：LC 74
- 官方中文标题：搜索二维矩阵
- 官方难度：中等
- 官方链接：[搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/)

### 原始题意、签名、样例与约束

矩阵每行非严格递增，且每行首元素严格大于上一行末元素；判断 `target` 是否出现，要求 $O(\log(mn))$。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target);
};
```

```text
[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3 -> true
同一矩阵，target=13 -> false
```

- $1\le m,n\le100$。
- $-10^4\le matrix_{ij},target\le10^4$。

## 约束推导与观察

行内有序加上跨行严格边界，使按行拼接后的长度 $mn$ 序列整体非递减。虚拟下标 `index` 对应行 `index/n`、列 `index%n`，无需复制即可对整个序列二分。

## 解法递进

### 解法一：逐格扫描

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    for (const auto& row : matrix) {
      for (int value : row) {
        if (value == target) {
          return true;
        }
      }
    }
    return false;
  }
};
```

时间 $O(mn)$，空间 $O(1)$。

### 解法二：先定位行，再在行内二分

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    int top = 0;
    int bottom = matrix.size() - 1;
    while (top <= bottom) {
      int row = top + (bottom - top) / 2;
      if (target < matrix[row][0]) {
        bottom = row - 1;
      } else if (target > matrix[row].back()) {
        top = row + 1;
      } else {
        return binary_search(matrix[row].begin(), matrix[row].end(), target);
      }
    }
    return false;
  }
};
```

时间 $O(\log m+\log n)$，空间 $O(1)$。

### 最佳实用解：展平下标一次二分

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    int m = matrix.size();
    int n = matrix[0].size();
    int left = 0;
    int right = m * n - 1;
    while (left <= right) {
      int middle = left + (right - left) / 2;
      int value = matrix[middle / n][middle % n];
      if (value == target) {
        return true;
      }
      if (value < target) {
        left = middle + 1;
      } else {
        right = middle - 1;
      }
    }
    return false;
  }
};
```

时间 $O(\log(mn))$，空间 $O(1)$，直接命中题目目标，优先记忆。两级二分同阶，若矩阵行长度不一致则更易扩展。

## 正确性证明

对任意相邻虚拟下标：若仍在同一行，矩阵行有序；若跨行，下一行首元素严格大于上一行尾元素。因此虚拟序列整体有序。标准二分始终保留所有可能等于目标的下标：中值小于目标时左侧均不可能，反之右侧均不可能。命中即返回真；区间为空说明所有位置已排除，返回假正确。

## 样例手推

`3×4` 矩阵虚拟为 `[1,3,5,7,10,11,16,20,23,30,34,60]`。目标 3 时二分最终访问下标 1；目标 13 时被夹在 11 与 16 之间，搜索区间变空。单格矩阵与重复行内值也满足同一单调性。

## 易错点与方案比较

- 行列换算的除数、模数都应是列数 `n`。
- 本题保证矩阵非空；通用接口需额外判断。
- `m*n` 在本题不溢出，大规模应使用 64 位下标。
- 不要把本题与“仅行列各自有序”的 LC 240 混淆，后者不能展平二分。

## 变种一：每行、每列分别有序但跨行不连续

对应 [LC 240 搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)。从右上角开始，每步排除一行或一列。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool searchMatrix(vector<vector<int>>& matrix, int target) {
    int row = 0;
    int column = matrix[0].size() - 1;
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

## 变种二：返回目标的第一个坐标

新定义：矩阵可能含重复值，返回展平顺序中第一个目标坐标。二分 `lower_bound`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n, target;
  cin >> m >> n >> target;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& x : row) {
      cin >> x;
    }
  }
  int left = 0;
  int right = m * n;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (matrix[middle / n][middle % n] < target) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  if (left < m * n && matrix[left / n][left % n] == target) {
    cout << left / n << ' ' << left % n << '\n';
  } else {
    cout << "-1 -1\n";
  }
}
```

时间 $O(\log(mn))$，空间 $O(1)$。

## 变种三：统计不超过目标的元素个数

新定义：仍满足整体有序，答案就是虚拟序列的 `upper_bound` 位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n, target;
  cin >> m >> n >> target;
  vector<vector<int>> matrix(m, vector<int>(n));
  for (auto& row : matrix) {
    for (int& x : row) {
      cin >> x;
    }
  }
  int left = 0;
  int right = m * n;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (matrix[middle / n][middle % n] <= target) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  cout << left << '\n';
}
```

时间 $O(\log(mn))$，空间 $O(1)$。

## 变种四：大量查询同一个矩阵

新定义：有 `q` 个目标。矩阵不变时无需额外预处理，每次独立二分；若要返回频次，用两次边界二分。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n, q;
  cin >> m >> n >> q;
  vector<int> values(m * n);
  for (int& x : values) {
    cin >> x;
  }
  while (q--) {
    int target;
    cin >> target;
    auto first = lower_bound(values.begin(), values.end(), target);
    auto after = upper_bound(values.begin(), values.end(), target);
    cout << after - first << '\n';
  }
}
```

预处理读取 $O(mn)$，每次查询 $O(\log(mn))$，空间 $O(mn)$；若保留二维存储，也可手写虚拟边界二分做到 $O(1)$ 额外空间。

## 可复现验证

随机生成整体非递减数组后按随机行列切成矩阵，以逐格扫描为 oracle，枚举目标覆盖范围外、重复值和所有现有值，对比展平二分；固定覆盖 `1×1`、单行、单列。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/search-a-2d-matrix/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-119-lc73/">← [力扣 Top 119] LC 73 矩阵置零 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-513-q4-lc4013/">[力扣竞赛] 第 513 场周赛 Q4 LC 4013 按奇偶比统计子数组 II 困难 →</a>
</nav>
