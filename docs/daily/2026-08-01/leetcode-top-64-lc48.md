---
title: "[力扣 Top 64] LC 48 旋转图像 中等"
---

# [力扣 Top 64] LC 48 旋转图像 中等

<p class="daily-archive-kicker">2026-08-01 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=efd68552a737803e1893907ad4294539052cf390f8ed1ad20b9ded32d4d653c4 -->
## 官方原始信息

- Top 排名：64
- 题号：LC 48
- 官方中文标题：旋转图像
- 官方难度：中等
- 官方链接：[旋转图像](https://leetcode.cn/problems/rotate-image/)

### 原始题意

给定 $n\times n$ 整数矩阵 `matrix`，把它表示的图像原地顺时针旋转 $90^\circ$；不能另建同规模矩阵。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  void rotate(vector<vector<int>>& matrix);
};
```

### 全部官方样例

```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]
```

```text
输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

### 全部约束

- `matrix` 有 $n$ 行且每行恰有 $n$ 项。
- $1\le n\le20$。
- $-1000\le matrix_{i,j}\le1000$。

## 约束推导与边界

顺时针旋转的坐标映射为

$$
(i,j)\longmapsto(j,n-1-i).
$$

直接按此式覆盖会破坏尚未读取的原值，因此要么使用副本，要么把映射分解为若干可原地完成的对称操作。先沿主对角线转置得到 $(j,i)$，再水平翻转每一行得到 $(j,n-1-i)$，恰好与目标映射一致。

$n=1$ 时两步都不改变矩阵；奇数阶中心元素保持不动。只交换整数，不存在溢出。

## 解法递进

### 解法一：复制到新矩阵

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    vector<vector<int>> rotated(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        rotated[j][n - 1 - i] = matrix[i][j];
      }
    }
    matrix = move(rotated);
  }
};
```

时间 $O(n^2)$，额外空间 $O(n^2)$。它最直接地验证坐标式，但违反原地要求。

### 最佳实用解：主对角线转置后逐行翻转

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        swap(matrix[i][j], matrix[j][i]);
      }
    }
    for (vector<int>& row : matrix) {
      reverse(row.begin(), row.end());
    }
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。

### 同阶方案：按层进行四元环交换

对每层的上边元素，一次保存并轮换上、左、下、右四个位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int layer = 0; layer < n / 2; ++layer) {
      int last = n - 1 - layer;
      for (int column = layer; column < last; ++column) {
        int offset = column - layer;
        int saved = matrix[layer][column];
        matrix[layer][column] = matrix[last - offset][layer];
        matrix[last - offset][layer] = matrix[last][last - offset];
        matrix[last][last - offset] = matrix[column][last];
        matrix[column][last] = saved;
      }
    }
  }
};
```

时间 $O(n^2)$，空间 $O(1)$。四元环少一次完整遍历，但下标证明与实现风险更高；推荐优先记忆“转置 + 翻转”，需要直接推广任意坐标置换时再使用环分解。

## 正确性证明

转置把原位置 $(i,j)$ 的元素送到 $(j,i)$。随后对第 $j$ 行水平翻转，把列 $i$ 变为 $n-1-i$，所以该元素最终位于 $(j,n-1-i)$。这正是顺时针 $90^\circ$ 的唯一坐标映射。两步都由互不冲突的成对交换完成，既不会丢失元素，也不会额外复制矩阵，因此结果正确且原地。

## 样例手推

对

```text
1 2 3
4 5 6
7 8 9
```

主对角线转置后是

```text
1 4 7
2 5 8
3 6 9
```

逐行翻转得到

```text
7 4 1
8 5 2
9 6 3
```

与官方输出一致。

## 易错点与方案比较

- 转置内层从 `i+1` 开始，不能把同一对位置交换两次。
- 顺时针是转置后翻转每一行；翻转行顺序得到的是另一种变换。
- 四元环的四个坐标方向很容易反写，应先固定一个保存值再顺着来源赋值。
- 只有方阵能在不改变容器形状的前提下原地旋转 $90^\circ$。

## 变种一：逆时针旋转 $90^\circ$

坐标变为 $(i,j)\mapsto(n-1-j,i)$。先转置，再把整行的顺序上下翻转。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<int>> matrix(n, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      swap(matrix[i][j], matrix[j][i]);
    }
  }
  reverse(matrix.begin(), matrix.end());
  for (const auto& row : matrix) {
    for (int j = 0; j < n; ++j) {
      cout << row[j] << (j + 1 == n ? '\n' : ' ');
    }
  }
}
```

时间 $O(n^2)$，空间 $O(1)$。

## 变种二：原地旋转 $180^\circ$

坐标为 $(i,j)\mapsto(n-1-i,n-1-j)$。先颠倒行顺序，再翻转每一行即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<int>> matrix(n, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  reverse(matrix.begin(), matrix.end());
  for (auto& row : matrix) {
    reverse(row.begin(), row.end());
  }
  for (const auto& row : matrix) {
    for (int j = 0; j < n; ++j) {
      cout << row[j] << (j + 1 == n ? '\n' : ' ');
    }
  }
}
```

时间 $O(n^2)$，空间 $O(1)$。

## 变种三：旋转一般的 $r\times c$ 矩阵

旋转后形状变为 $c\times r$，原容器维度改变，方阵的常数空间方案不再适用；按坐标式写入新矩阵。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<vector<int>> matrix(rows, vector<int>(columns));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  vector<vector<int>> rotated(columns, vector<int>(rows));
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      rotated[j][rows - 1 - i] = matrix[i][j];
    }
  }
  cout << columns << ' ' << rows << '\n';
  for (const auto& row : rotated) {
    for (int j = 0; j < rows; ++j) {
      cout << row[j] << (j + 1 == rows ? '\n' : ' ');
    }
  }
}
```

时间与空间均为 $O(rc)$。

## 变种四：顺时针旋转任意整数个四分之一圈

把次数规范化到 $[0,3]$；0 次不动，1 次执行主算法，2 次用 $180^\circ$，3 次等价于逆时针 $90^\circ$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void clockwise(vector<vector<int>>& matrix) {
  int n = matrix.size();
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      swap(matrix[i][j], matrix[j][i]);
    }
  }
  for (auto& row : matrix) {
    reverse(row.begin(), row.end());
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long turns;
  cin >> n >> turns;
  vector<vector<int>> matrix(n, vector<int>(n));
  for (auto& row : matrix) {
    for (int& value : row) {
      cin >> value;
    }
  }
  int count = static_cast<int>((turns % 4 + 4) % 4);
  while (count--) {
    clockwise(matrix);
  }
  for (const auto& row : matrix) {
    for (int j = 0; j < n; ++j) {
      cout << row[j] << (j + 1 == n ? '\n' : ' ');
    }
  }
}
```

时间 $O(n^2)$，空间 $O(1)$；规范化后最多执行三次旋转。

## 可复现验证

对 $1\le n\le8$ 的随机方阵，把两种原地算法与副本坐标映射逐项比较；再检查连续旋转四次恢复原矩阵、顺时针一次与逆时针三次一致。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/rotate-image/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/rotate-image/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-63-lc26/">← [力扣 Top 63] LC 26 删除有序数组中的重复项 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-65-lc224/">[力扣 Top 65] LC 224 基本计算器 困难 →</a>
</nav>
