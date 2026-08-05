---
title: "[力扣 Top 119] LC 73 矩阵置零 中等"
---

# [力扣 Top 119] LC 73 矩阵置零 中等

<p class="daily-archive-kicker">2026-08-06 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=86a6e35f2e333a268a738e9ea382b0aa10b3287c09f2a2a43b39aed02de3cbff -->
## 官方原始信息

- Top 排名：119
- 题号：LC 73
- 官方中文标题：矩阵置零
- 官方难度：中等
- 官方链接：[矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/)

### 原始题意、签名、样例与约束

若原矩阵某元素为 0，把其整行和整列设为 0，要求原地修改。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  void setZeroes(vector<vector<int>>& matrix);
};
```

```text
[[1,1,1],[1,0,1],[1,1,1]] -> [[1,0,1],[0,0,0],[1,0,1]]
[[0,1,2,0],[3,4,5,2],[1,3,1,5]] -> [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

- $1\le m,n\le200$。
- $-2^{31}\le matrix_{ij}\le2^{31}-1$。
- 进阶依次要求从 $O(mn)$、$O(m+n)$ 额外空间降到常数空间。

## 约束推导与观察

不能边扫描边扩散零，否则新写入的零会被误认为原始零。先收集“哪些行、列应归零”，再统一写入。为省空间，可借用第一行和第一列作标记，但 `matrix[0][0]` 同时属于二者，因此必须另存第一行、第一列原本是否含零。

## 解法递进

### 解法一：复制原矩阵

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void setZeroes(vector<vector<int>>& matrix) {
    vector<vector<int>> original = matrix;
    int m = matrix.size();
    int n = matrix[0].size();
    for (int i = 0; i < m; ++i) {
      for (int j = 0; j < n; ++j) {
        if (original[i][j] == 0) {
          for (int c = 0; c < n; ++c) {
            matrix[i][c] = 0;
          }
          for (int r = 0; r < m; ++r) {
            matrix[r][j] = 0;
          }
        }
      }
    }
  }
};
```

时间最坏 $O(mn(m+n))$，空间 $O(mn)$，语义最直接。

### 解法二：行列布尔标记

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void setZeroes(vector<vector<int>>& matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<char> row(m), column(n);
    for (int i = 0; i < m; ++i) {
      for (int j = 0; j < n; ++j) {
        if (matrix[i][j] == 0) {
          row[i] = true;
          column[j] = true;
        }
      }
    }
    for (int i = 0; i < m; ++i) {
      for (int j = 0; j < n; ++j) {
        if (row[i] || column[j]) {
          matrix[i][j] = 0;
        }
      }
    }
  }
};
```

时间 $O(mn)$，空间 $O(m+n)$。

### 最佳实用解：首行首列作为标记

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void setZeroes(vector<vector<int>>& matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    bool firstRowZero = false;
    bool firstColumnZero = false;
    for (int j = 0; j < n; ++j) {
      firstRowZero |= matrix[0][j] == 0;
    }
    for (int i = 0; i < m; ++i) {
      firstColumnZero |= matrix[i][0] == 0;
    }
    for (int i = 1; i < m; ++i) {
      for (int j = 1; j < n; ++j) {
        if (matrix[i][j] == 0) {
          matrix[i][0] = 0;
          matrix[0][j] = 0;
        }
      }
    }
    for (int i = 1; i < m; ++i) {
      for (int j = 1; j < n; ++j) {
        if (matrix[i][0] == 0 || matrix[0][j] == 0) {
          matrix[i][j] = 0;
        }
      }
    }
    if (firstRowZero) {
      fill(matrix[0].begin(), matrix[0].end(), 0);
    }
    if (firstColumnZero) {
      for (int i = 0; i < m; ++i) {
        matrix[i][0] = 0;
      }
    }
  }
};
```

时间 $O(mn)$，空间 $O(1)$，是推荐记忆方案。

## 正确性证明

第一轮先保存首行、首列的原始零状态。对内部每个原始零 `(i,j)`，把对应行标记写在 `(i,0)`，列标记写在 `(0,j)`；尚未据此改内部值，所以标记只来源于原始零。第二轮把且仅把行标记或列标记存在的内部格设零。最后依据独立布尔量处理首行、首列，既不会丢失它们自己的原始信息，也不会误扩散新零。因此每个格最终为零当且仅当其原始行或列含零。

## 样例手推

第一例内部零 `(1,1)` 把 `matrix[1][0]`、`matrix[0][1]` 置零；第二轮清空第 1 行和第 1 列。第二例首行本身含零，`firstRowZero=true`；内部行通过首列标记，最后再整体清空首行。

## 易错点与方案比较

- 必须分“记录标记”和“按标记写零”两阶段。
- `matrix[0][0]` 无法同时编码两件事，至少保留一个独立布尔量。
- 处理首行首列要放最后，避免提前破坏内部标记。
- 行列数组更易写；常数空间方案满足进阶且同为线性时间。

## 变种一：矩阵只读，返回新矩阵

直接记录原始零行列并生成结果，输入不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> transformed(const vector<vector<int>>& matrix) {
  int m = matrix.size();
  int n = matrix[0].size();
  vector<char> row(m), column(n);
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
      if (matrix[i][j] == 0) {
        row[i] = column[j] = true;
      }
    }
  }
  vector<vector<int>> answer = matrix;
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
      if (row[i] || column[j]) {
        answer[i][j] = 0;
      }
    }
  }
  return answer;
}
int main() {
  vector<vector<int>> a{{1}};
  cout << transformed(a)[0][0] << '\n';
}
```

时间、空间均为 $O(mn)$。

## 变种二：稀疏矩阵仅输出需删除的行列

新定义：输入只有非零项与显式零坐标，输出受影响行列集合，不展开巨大矩阵。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n, z;
  cin >> m >> n >> z;
  set<int> rows;
  set<int> columns;
  while (z--) {
    int row, column;
    cin >> row >> column;
    rows.insert(row);
    columns.insert(column);
  }
  cout << rows.size();
  for (int row : rows) {
    cout << ' ' << row;
  }
  cout << '\n' << columns.size();
  for (int column : columns) {
    cout << ' ' << column;
  }
  cout << '\n';
}
```

时间 $O(z\log z)$，空间 $O(z)$，与矩阵面积无关。

## 变种三：三维张量置零

新定义：任一零使其所在的三个坐标平面归零。分别标记三个维度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int x, y, z;
  cin >> x >> y >> z;
  vector tensor(x, vector(y, vector<int>(z)));
  vector<char> axisX(x), axisY(y), axisZ(z);
  for (int i = 0; i < x; ++i) {
    for (int j = 0; j < y; ++j) {
      for (int k = 0; k < z; ++k) {
        cin >> tensor[i][j][k];
        if (tensor[i][j][k] == 0) {
          axisX[i] = axisY[j] = axisZ[k] = true;
        }
      }
    }
  }
  for (int i = 0; i < x; ++i) {
    for (int j = 0; j < y; ++j) {
      for (int k = 0; k < z; ++k) {
        if (axisX[i] || axisY[j] || axisZ[k]) {
          tensor[i][j][k] = 0;
        }
      }
    }
  }
  cout << tensor[0][0][0] << '\n';
}
```

时间 $O(xyz)$，额外空间 $O(x+y+z)$。

## 变种四：在线单点改零并查询单元格

新定义：更新只会把某格变成零，查询某格的当前值。维护零行、零列布尔量，无需重写整矩阵。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n, q;
  cin >> m >> n >> q;
  vector<vector<int>> matrix(m, vector<int>(n));
  vector<char> zeroRow(m), zeroColumn(n);
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
      cin >> matrix[i][j];
      if (matrix[i][j] == 0) {
        zeroRow[i] = zeroColumn[j] = true;
      }
    }
  }
  while (q--) {
    int type, i, j;
    cin >> type >> i >> j;
    if (type == 1) {
      matrix[i][j] = 0;
      zeroRow[i] = zeroColumn[j] = true;
    } else {
      cout << (zeroRow[i] || zeroColumn[j] ? 0 : matrix[i][j]) << '\n';
    }
  }
}
```

初始化 $O(mn)$，每次更新与查询 $O(1)$，空间 $O(mn)$ 存原值。

## 可复现验证

枚举不超过 `5×5` 的随机小矩阵，以保留副本的直接扩散为 oracle，对比行列标记与常数空间结果；覆盖单行、单列、首格为零、首行多零、无零和全零。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/set-matrix-zeroes/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-118-lc91/">← [力扣 Top 118] LC 91 解码方法 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-120-lc74/">[力扣 Top 120] LC 74 搜索二维矩阵 中等 →</a>
</nav>
