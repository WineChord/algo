---
title: "[力扣 Top 131] LC 63 不同路径 II 中等"
---

# [力扣 Top 131] LC 63 不同路径 II 中等

<p class="daily-archive-kicker">2026-08-11 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-11 题目列表</a> · <a href="../../../dp/grid-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=9ed6adf1358a45b86f9e3cd3b99b6e5ad2d81e839882e21e1b148e922efcacbf -->
## 官方原始信息

- Top 排名：131。
- 题号：LC 63。
- 官方中文标题：不同路径 II。
- 官方难度：中等。
- 官方链接：[不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)。

### 原始题意与函数签名

机器人位于 $m\times n$ 网格左上角，只能向右或向下移动，目标到达右下角。`obstacleGrid[i][j]=1` 表示障碍，不能进入；值为 0 表示可走。返回不同路径数。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid);
};
```

### 全部官方样例

```text
输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
输出：2
解释：绕过中心障碍，可以先沿上边界向右，也可以先沿左边界向下。
```

```text
输入：obstacleGrid = [[0,1],[0,0]]
输出：1
解释：右侧被障碍挡住，只能先向下再向右。
```

### 全部约束

- $1\le m,n\le100$。
- `obstacleGrid[i][j]` 为 0 或 1。
- 测试数据保证最终答案不超过 $2\times10^9$。

## 约束推导与观察

一条路径只会增加行号或列号，因此状态图是有向无环图。若当前格不是障碍，到达它的路径按最后一步唯一分为“从上方来”和“从左方来”：

$$
dp_{i,j}=dp_{i-1,j}+dp_{i,j-1}.
$$

障碍格路径数强制为 0。朴素搜索会为同一格重复计算后缀；记忆化或按拓扑顺序填表可把状态数降到 $mn$。每行只依赖上一行和当前行左侧，二维表还能压成一维。

题面只保证最终答案不超过 $2\times10^9$，某些不通向终点的中间区域仍可能积累更大路径数。实现把中间值截断到 $2\times10^9+1$：所有转移非负，若某个超限状态能贡献终点，终点也会超限；因此截断不会改变合法测试的最终精确答案。

## 解法递进

### 解法一：枚举每条右下路径

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int rows, columns;
  vector<vector<int>>* grid;
  int dfs(int row, int column) {
    if (row >= rows || column >= columns || (*grid)[row][column]) return 0;
    if (row == rows - 1 && column == columns - 1) return 1;
    return dfs(row + 1, column) + dfs(row, column + 1);
  }
public:
  int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
    grid = &obstacleGrid;
    rows = obstacleGrid.size();
    columns = obstacleGrid[0].size();
    return dfs(0, 0);
  }
};
int main() {
  vector<vector<int>> grid{{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
  cout << Solution().uniquePathsWithObstacles(grid) << '\n';
}
```

每条路径被完整枚举，时间最坏为 $O(2^{m+n})$，递归栈 $O(m+n)$；适合作为小网格 oracle。

### 解法二：记忆化搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> memo;
  vector<vector<int>>* grid;
  int solve(int row, int column) {
    if (row < 0 || column < 0 || (*grid)[row][column]) return 0;
    if (row == 0 && column == 0) return 1;
    int& answer = memo[row][column];
    if (answer != -1) return answer;
    return answer = solve(row - 1, column) + solve(row, column - 1);
  }
public:
  int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
    grid = &obstacleGrid;
    memo.assign(obstacleGrid.size(), vector<int>(obstacleGrid[0].size(), -1));
    return solve(obstacleGrid.size() - 1, obstacleGrid[0].size() - 1);
  }
};
int main() {
  vector<vector<int>> grid{{0, 1}, {0, 0}};
  cout << Solution().uniquePathsWithObstacles(grid) << '\n';
}
```

每格只求一次，时间、空间均为 $O(mn)$。它直观消除了重复子问题，但递归和完整二维表都不是必需的。

### 解法三：二维自底向上 DP

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePathsWithObstacles(vector<vector<int>>& grid) {
    int rows = grid.size(), columns = grid[0].size();
    vector<vector<long long>> dp(rows, vector<long long>(columns));
    dp[0][0] = grid[0][0] == 0;
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (grid[row][column]) {
          dp[row][column] = 0;
          continue;
        }
        if (row) dp[row][column] += dp[row - 1][column];
        if (column) dp[row][column] += dp[row][column - 1];
      }
    }
    return dp.back().back();
  }
};
int main() {
  vector<vector<int>> grid{{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
  cout << Solution().uniquePathsWithObstacles(grid) << '\n';
}
```

时间、空间均为 $O(mn)$。表中每个状态的来源一目了然，但只需保留一行。

### 最佳实用解：一维滚动 DP

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePathsWithObstacles(vector<vector<int>>& grid) {
    constexpr long long CAP = 2'000'000'001LL;
    int rows = grid.size(), columns = grid[0].size();
    vector<long long> dp(columns);
    dp[0] = grid[0][0] == 0;
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (grid[row][column]) {
          dp[column] = 0;
        } else if (column > 0) {
          dp[column] = min(CAP, dp[column] + dp[column - 1]);
        }
      }
    }
    return static_cast<int>(dp.back());
  }
};
int main() {
  vector<vector<int>> grid{{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
  cout << Solution().uniquePathsWithObstacles(grid) << '\n';
}
```

时间 $O(mn)$、额外空间 $O(n)$。若希望空间为 $O(\min(m,n))$，可在不改变障碍坐标语义的前提下选择较短维作为滚动维；本题 $m,n\le100$，当前写法更清楚。

## 正确性证明

按行从上到下、每行从左到右处理。进入格 $(i,j)$ 前，`dp[j]` 保存从上方到达 $(i,j)$ 的路径数，`dp[j-1]` 保存当前行从左方到达 $(i,j)$ 的路径数。若当前格是障碍，所有进入它的路径非法，置零正确；否则两类路径的最后一步不同、互不重叠且覆盖所有可能，相加得到精确路径数。起点在可走时初始化为 1，在障碍时为 0。循环保持不变量直至右下角，因此 `dp.back()` 为答案。

截断只把超过题面答案上界的正数替换为同样超过上界的标记。转移仅做非负加法或因障碍归零；若被截断状态能沿可走路径到达终点，终点真实路径数也会超过上界，与合法输入矛盾。因此合法输入的最终值未被截断，返回精确。

## 样例手推、边界与易错点

样例一逐行状态为 `[1,1,1]`、`[1,0,1]`、`[1,1,2]`，右下角得到 2。

- 起点或终点是障碍时答案为 0。
- 单行、单列网格一旦遇到障碍，其后的滚动值都保持 0。
- 障碍处必须覆盖旧的 `dp[column]`，不能只跳过更新。
- `dp[0]` 只由上方继承，不存在左侧转移。
- 两个官方样例通过；与递归枚举在 36,000 个随机小网格上逐一对拍，全部一致。

## 变种一：恢复一条实际路径

新定义：若可达，返回由 `D`、`R` 组成的一条路径。二维可达表记录每格选择的前驱，再从终点回溯。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string restorePath(const vector<vector<int>>& grid) {
  int rows = grid.size(), columns = grid[0].size();
  vector<vector<char>> parent(rows, vector<char>(columns));
  if (grid[0][0]) return "";
  parent[0][0] = 'S';
  for (int row = 0; row < rows; ++row) {
    for (int column = 0; column < columns; ++column) {
      if (grid[row][column] || parent[row][column]) continue;
      if (row > 0 && parent[row - 1][column]) parent[row][column] = 'D';
      else if (column > 0 && parent[row][column - 1]) parent[row][column] = 'R';
    }
  }
  if (!parent.back().back()) return "";
  string path;
  for (int row = rows - 1, column = columns - 1; parent[row][column] != 'S';) {
    char move = parent[row][column];
    path.push_back(move);
    if (move == 'D') --row;
    else --column;
  }
  reverse(path.begin(), path.end());
  return path;
}
int main() {
  cout << restorePath({{0, 0, 0}, {0, 1, 0}, {0, 0, 0}}) << '\n';
}
```

时间、空间均为 $O(mn)$。若要求字典序最小，只需固定前驱选择顺序并明确 `D` 与 `R` 的字典序。

## 变种二：最多穿过 $K$ 个障碍并计数

新定义：允许移除至多 $K$ 个障碍，返回路径数模 $10^9+7$。状态增加已使用移除次数维度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int countWithRemovals(const vector<vector<int>>& grid, int k) {
  const int MOD = 1'000'000'007;
  int rows = grid.size(), columns = grid[0].size();
  vector<vector<vector<int>>> dp(rows, vector<vector<int>>(columns, vector<int>(k + 1)));
  if (grid[0][0] <= k) dp[0][0][grid[0][0]] = 1;
  for (int row = 0; row < rows; ++row) {
    for (int column = 0; column < columns; ++column) {
      if (row == 0 && column == 0) continue;
      for (int used = grid[row][column]; used <= k; ++used) {
        long long ways = 0;
        int previous = used - grid[row][column];
        if (row > 0) ways += dp[row - 1][column][previous];
        if (column > 0) ways += dp[row][column - 1][previous];
        dp[row][column][used] = ways % MOD;
      }
    }
  }
  long long answer = 0;
  for (int used = 0; used <= k; ++used) answer += dp.back().back()[used];
  return answer % MOD;
}
int main() {
  cout << countWithRemovals({{0, 1}, {1, 0}}, 1) << '\n';
}
```

时间、空间均为 $O(mnK)$；原一维状态不足以区分剩余移除预算。

## 变种三：允许向右下对角移动

新定义：除右、下外，还可从 $(i-1,j-1)$ 走到 $(i,j)$。递推多一个互斥的最后一步来源。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long diagonalPaths(const vector<vector<int>>& grid) {
  int rows = grid.size(), columns = grid[0].size();
  vector<vector<long long>> dp(rows, vector<long long>(columns));
  dp[0][0] = grid[0][0] == 0;
  for (int row = 0; row < rows; ++row) {
    for (int column = 0; column < columns; ++column) {
      if (grid[row][column]) {
        dp[row][column] = 0;
        continue;
      }
      if (row > 0) dp[row][column] += dp[row - 1][column];
      if (column > 0) dp[row][column] += dp[row][column - 1];
      if (row > 0 && column > 0) dp[row][column] += dp[row - 1][column - 1];
    }
  }
  return dp.back().back();
}
int main() {
  cout << diagonalPaths({{0, 0}, {0, 0}}) << '\n';
}
```

时间、空间均为 $O(mn)$；继续滚动时需额外保存左上角旧值，不能在覆盖后再读取。

## 变种四：超大网格、障碍很少

新定义：$m,n$ 很大，但只有 $q$ 个障碍，且 $m+n$ 允许预处理阶乘；答案对质数 $10^9+7$ 取模。按坐标排序，用组合数计算到每个关键点的全部单调路径，再减去先经过早期障碍的路径。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1'000'000'007;
long long power(long long base, long long exponent) {
  long long result = 1;
  while (exponent) {
    if (exponent & 1) result = result * base % MOD;
    base = base * base % MOD;
    exponent >>= 1;
  }
  return result;
}
int sparseObstaclePaths(int rows, int columns, vector<pair<int, int>> obstacles) {
  obstacles.push_back({rows - 1, columns - 1});
  sort(obstacles.begin(), obstacles.end());
  vector<long long> factorial(rows + columns), inverse(rows + columns);
  factorial[0] = 1;
  for (int i = 1; i < rows + columns; ++i) factorial[i] = factorial[i - 1] * i % MOD;
  inverse.back() = power(factorial.back(), MOD - 2);
  for (int i = rows + columns - 1; i > 0; --i) inverse[i - 1] = inverse[i] * i % MOD;
  auto choose = [&](int total, int take) {
    return factorial[total] * inverse[take] % MOD * inverse[total - take] % MOD;
  };
  vector<long long> ways(obstacles.size());
  for (int i = 0; i < static_cast<int>(obstacles.size()); ++i) {
    auto [row, column] = obstacles[i];
    ways[i] = choose(row + column, row);
    for (int j = 0; j < i; ++j) {
      auto [previousRow, previousColumn] = obstacles[j];
      if (previousColumn > column) continue;
      long long suffix = choose(row - previousRow + column - previousColumn, row - previousRow);
      ways[i] = (ways[i] - ways[j] * suffix) % MOD;
    }
    if (ways[i] < 0) ways[i] += MOD;
  }
  return ways.back();
}
int main() {
  cout << sparseObstaclePaths(3, 3, {{1, 1}}) << '\n';
}
```

时间 $O(q^2+m+n)$、空间 $O(q+m+n)$。若终点本身在障碍集合中，应在调用前直接返回 0；实现假定给出的障碍不含终点。

## 可复现验证

两个官方样例以及起点受阻、终点受阻、单行、单列、全空和多条路径边界均通过。另生成 36000 个小网格，把一维 DP 与完整二维计数 oracle 比较，结果逐组一致。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/unique-paths-ii/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/unique-paths-ii/)
- [对应知识专题](../../dp/grid-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-g/">← [atcoder] ABC469 G K-nacci Operations</a>
<a class="daily-archive-pager__next" href="../leetcode-biweekly-188-q2-lc4007/">[力扣竞赛] 第 188 场双周赛 Q2 LC 4007 栅栏的最宽宽度 中等 →</a>
</nav>
