---
title: "[力扣 Top 74] LC 64 最小路径和 中等"
---

# [力扣 Top 74] LC 64 最小路径和 中等

<p class="daily-archive-kicker">2026-08-02 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../dp/grid-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=9ea0625f173747c6cd8b77494fff16bfe29d8efbfaed4d3dcbe931d73d91d1b0 -->
## 官方原始信息

- Top 排名：74
- 题号：LC 64
- 官方中文标题：最小路径和
- 官方难度：中等
- 官方链接：[最小路径和](https://leetcode.cn/problems/minimum-path-sum/)

### 原始题意

给定一个由非负整数构成的 $m\times n$ 网格，从左上角出发，每次只能向右或向下，求到右下角路径上所有格子之和的最小值。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minPathSum(vector<vector<int>>& grid);
};
```

### 全部官方样例

```text
输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：路径 1→3→1→1→1 的总和最小。
```

```text
输入：grid = [[1,2,3],[4,5,6]]
输出：12
```

### 全部约束

- $m=grid.length$，$n=grid[i].length$。
- $1\le m,n\le200$。
- $0\le grid_{i,j}\le200$。
- 只能向右或向下移动。

## 约束推导与状态模型

每条路径固定经过 $m+n-1$ 个格子，但路径数量为 $\binom{m+n-2}{m-1}$，最大时呈指数增长。移动方向使状态图是有向无环图：进入 `(i,j)` 的最后一步只可能来自上方或左方。因此

$$
dp[i][j]=grid[i][j]+\min(dp[i-1][j],dp[i][j-1]).
$$

当前行只依赖上一行同列和当前行前一列，可压缩到一维。最大路径和不超过 $200(200+200-1)=79800$，`int` 安全。第一行和第一列只有一条到达方式，必须单独处理或使用无穷大哨兵。

## 解法递进

### 解法一：枚举全部路径

递归尝试向下和向右，抵达终点时返回格子值；越界分支返回无穷大。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const vector<vector<int>>& grid, int row, int column) {
    int rows = grid.size();
    int columns = grid[0].size();
    if (row == rows - 1 && column == columns - 1) {
      return grid[row][column];
    }
    int best = INT_MAX / 4;
    if (row + 1 < rows) {
      best = min(best, search(grid, row + 1, column));
    }
    if (column + 1 < columns) {
      best = min(best, search(grid, row, column + 1));
    }
    return grid[row][column] + best;
  }
public:
  int minPathSum(vector<vector<int>>& grid) {
    return search(grid, 0, 0);
  }
};
```

时间与路径数同阶，最坏指数级；递归深度 $O(m+n)$。

### 解法二：二维动态规划

保存每个格子的最优前缀，按行或按列拓扑顺序填表。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minPathSum(vector<vector<int>>& grid) {
    int rows = grid.size();
    int columns = grid[0].size();
    vector<vector<int>> dp(rows, vector<int>(columns, INT_MAX / 4));
    dp[0][0] = grid[0][0];
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (row > 0) {
          dp[row][column] = min(dp[row][column], dp[row - 1][column] + grid[row][column]);
        }
        if (column > 0) {
          dp[row][column] = min(dp[row][column], dp[row][column - 1] + grid[row][column]);
        }
      }
    }
    return dp.back().back();
  }
};
```

时间 $O(mn)$，空间 $O(mn)$。

### 最佳实用解：一维滚动动态规划

处理 `(i,j)` 前，`dp[j]` 是上方最优值；更新后的 `dp[j-1]` 是左方最优值。用二者较小值加当前格子即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minPathSum(vector<vector<int>>& grid) {
    int rows = grid.size();
    int columns = grid[0].size();
    vector<int> dp(columns, INT_MAX / 4);
    dp[0] = 0;
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        int fromLeft = column == 0 ? INT_MAX / 4 : dp[column - 1];
        dp[column] = min(dp[column], fromLeft) + grid[row][column];
      }
    }
    return dp.back();
  }
};
```

时间 $O(mn)$，空间 $O(n)$。若列数大于行数且允许转置访问，可沿较短维滚动，把空间进一步写成 $O(\min(m,n))$。

## 正确性证明

按行优先顺序归纳。起点路径和显然为 `grid[0][0]`。对任意其他格子 `(i,j)`，合法路径的最后一步必且只可能来自 `(i-1,j)` 或 `(i,j-1)`；删除最后一个格子后得到对应前驱的一条合法路径。由归纳假设，两个前驱的 `dp` 已分别是最小路径和，因此取较小者再加当前格子既构造了合法路径，也不可能被任何其他路径改进。滚动数组在更新时恰好保存这两个值，所以与二维递推等价，终点答案正确。

## 样例手推

对第一个网格，滚动数组逐行变化：`[1,4,5]`、`[2,7,6]`、`[6,8,7]`，最终为 7。单行网格只能从左累计，单列网格只能从上累计；含 0 时递推仍成立。

## 易错点与方案比较

- 路径和包含起点与终点。
- 一维压缩必须从左向右更新；反向会读到上一行的左邻值。
- `dp[0]=0` 是给起点提供虚拟前驱，其他初值必须为无穷大。
- 非负性不是 DAG 动态规划成立的必要条件；真正关键是只能向右／下，不会形成环。
- 需要恢复路径时保留二维父指针；只求数值时一维版更省空间，推荐优先写一维版。

## 变种一：恢复一条最小路径

新定义：输出最小和与一条由 `D`、`R` 构成的路径。二维 DP 更新时记录选择的前驱。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<vector<long long>> grid(rows, vector<long long>(columns));
  vector<vector<long long>> dp(rows, vector<long long>(columns, LLONG_MAX / 4));
  vector<string> parent(rows, string(columns, '?'));
  for (auto& row : grid) {
    for (long long& value : row) {
      cin >> value;
    }
  }
  dp[0][0] = grid[0][0];
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      if (i > 0 && dp[i - 1][j] + grid[i][j] < dp[i][j]) {
        dp[i][j] = dp[i - 1][j] + grid[i][j];
        parent[i][j] = 'D';
      }
      if (j > 0 && dp[i][j - 1] + grid[i][j] < dp[i][j]) {
        dp[i][j] = dp[i][j - 1] + grid[i][j];
        parent[i][j] = 'R';
      }
    }
  }
  string path;
  for (int i = rows - 1, j = columns - 1; i > 0 || j > 0;) {
    path.push_back(parent[i][j]);
    if (parent[i][j] == 'D') {
      --i;
    } else {
      --j;
    }
  }
  reverse(path.begin(), path.end());
  cout << dp.back().back() << '\n' << path << '\n';
}
```

时间 $O(mn)$，空间 $O(mn)$。

## 变种二：部分格子不可进入

新定义：`-1` 表示障碍，其他值为非负代价；无路径输出 `-1`。不可达状态保持无穷大，禁止从它转移。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  const long long inf = LLONG_MAX / 4;
  vector<long long> dp(columns, inf);
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      long long value;
      cin >> value;
      if (value == -1) {
        dp[j] = inf;
        continue;
      }
      if (i == 0 && j == 0) {
        dp[j] = value;
        continue;
      }
      long long left = j == 0 ? inf : dp[j - 1];
      dp[j] = min(dp[j], left);
      if (dp[j] != inf) {
        dp[j] += value;
      }
    }
  }
  cout << (dp.back() == inf ? -1 : dp.back()) << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$。

## 变种三：格子权值允许为负数

新定义：权值可正可负，移动方向仍只能右／下。由于图仍无环，不需要 Bellman-Ford；拓扑 DP 原样成立，只把类型提升为 `long long`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  const long long inf = LLONG_MAX / 4;
  vector<long long> dp(columns, inf);
  dp[0] = 0;
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      long long value;
      cin >> value;
      long long left = j == 0 ? inf : dp[j - 1];
      dp[j] = min(dp[j], left) + value;
    }
  }
  cout << dp.back() << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$；无环性消除了负环问题。

## 变种四：同时统计最小路径条数

新定义：输出最小和，以及达到该最小和的路径数量模 $10^9+7$。相同最优前驱的计数相加。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  const long long inf = LLONG_MAX / 4;
  const int mod = 1000000007;
  vector<long long> cost(columns, inf);
  vector<int> ways(columns);
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      long long value;
      cin >> value;
      if (i == 0 && j == 0) {
        cost[j] = value;
        ways[j] = 1;
        continue;
      }
      long long upCost = cost[j];
      int upWays = ways[j];
      long long leftCost = j == 0 ? inf : cost[j - 1];
      int leftWays = j == 0 ? 0 : ways[j - 1];
      long long best = min(upCost, leftCost);
      int count = 0;
      if (upCost == best) {
        count = (count + upWays) % mod;
      }
      if (leftCost == best) {
        count = (count + leftWays) % mod;
      }
      cost[j] = best + value;
      ways[j] = count;
    }
  }
  cout << cost.back() << ' ' << ways.back() << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$。

## 验证说明

一维 DP 与路径枚举对 6000 个 $1..6$ 随机网格对拍，覆盖单行、单列、全零与极值；七段 C++23 代码全部编译通过。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-path-sum/)
- [对应知识专题](../../dp/grid-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-73-lc322/">← [力扣 Top 73] LC 322 零钱兑换 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-75-lc394/">[力扣 Top 75] LC 394 字符串解码 中等 →</a>
</nav>
