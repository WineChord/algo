---
title: "[力扣 Top 141] LC 62 不同路径 中等"
---

# [力扣 Top 141] LC 62 不同路径 中等

<p class="daily-archive-kicker">2026-08-26 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-26 题目列表</a> · <a href="../../../dp/grid-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=6a32abc07943cb4127e453cc756c25a92e3e6309a14fd01dd10ab03497dc66f4 -->
[力扣官方题目：62. 不同路径](https://leetcode.cn/problems/unique-paths/)

## 官方原始信息

- 高频队列排名：Top 141；题号：LC 62。
- 官方中文标题：不同路径；官方难度：中等。
- 官方链接：[https://leetcode.cn/problems/unique-paths/](https://leetcode.cn/problems/unique-paths/)
- 函数签名：`int uniquePaths(int m, int n)`。
- 官方标签：数学、动态规划、组合数学。
- 该题官方页面没有竞赛分值；本次读取的 ZeroTracer 数据中没有可可靠映射的社区竞赛分，
  因而记为未知，不按题号或主观感受补数。

### 原始题意

一个机器人位于 $m\times n$ 网格左上角。每一步只能向右或向下移动一格，目标是到达右下角。
返回不同移动路径的总数。

### 全部官方样例

```text
示例 1
输入：m = 3, n = 7
输出：28

示例 2
输入：m = 3, n = 2
输出：3
解释：三条路径分别是 RDD、DDR、DRD。

示例 3
输入：m = 7, n = 3
输出：28

示例 4
输入：m = 3, n = 3
输出：6
```

### 全部约束

- $1\le m,n\le100$。
- 测试数据保证答案不超过 $2\times10^9$。

## 最优结论摘要

每条路径都恰含 $m-1$ 次向下和 $n-1$ 次向右，只需从总共 $m+n-2$ 个位置里选择较少的
那一类移动：

$$
\text{answer}=\binom{m+n-2}{m-1}=\binom{m+n-2}{n-1}.
$$

推荐面试先讲二维 DP，再把状态转移识别成杨辉三角并推出组合数。最佳实用解时间
$O(\min(m,n))$、额外空间 $O(1)$。

## 约束与观察

- 机器人不能向左或向上，因此路径不会形成环；每条合法路径的总步数固定为 $m+n-2$。
- $m,n\le100$，二维 DP 已经绰绰有余；组合数学进一步消除了整张网格状态。
- 最终答案虽然适合 `int`，乘除组合数的中间过程仍应使用 `long long`。
- 当 $m=1$ 或 $n=1$ 时没有选择，唯一方案是沿直线走到底，答案为 1。
- 网格没有障碍，所有 R/D 排列都合法；一旦加入障碍，组合数公式一般会失效。

## 样例手推与边界

对 $m=3,n=3$，路径长度为 4，其中恰有 2 个 `D`。选择 `D` 所在的两个位置即可：
`DDRR`、`DRDR`、`DRRD`、`RDDR`、`RDRD`、`RRDD`，共
$\binom{4}{2}=6$ 条。

对 $m=1,n=100$，必须连续向右 99 次；组合式为 $\binom{99}{0}=1$。对称交换 $m,n$ 不会
改变答案，这也是实现自测的重要不变量。

## 解法一：完整递归枚举

从当前位置分别尝试向下和向右；到达终点计 1，越界计 0。它覆盖每个 R/D 序列且不重不漏，
但同一格会被不同前缀反复计算。时间复杂度为
$O\!\left(\binom{m+n-2}{m-1}\right)$，递归栈 $O(m+n)$，只适合作为小网格暴力 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(int row, int column, int m, int n) {
    if (row == m - 1 && column == n - 1) return 1;
    if (row >= m || column >= n) return 0;
    return search(row + 1, column, m, n) + search(row, column + 1, m, n);
  }
public:
  int uniquePaths(int m, int n) {
    return search(0, 0, m, n);
  }
};
```

## 解法二：二维动态规划

令 $dp[i][j]$ 为到达格子 $(i,j)$ 的路径数。第一行和第一列只有一种走法；其余格子的最后
一步只能来自上方或左方，因此

$$
dp[i][j]=dp[i-1][j]+dp[i][j-1].
$$

这个转移把指数级重复子问题压缩为 $mn$ 个状态，时间 $O(mn)$、空间 $O(mn)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePaths(int m, int n) {
    vector<vector<int>> dp(m, vector<int>(n, 1));
    for (int row = 1; row < m; ++row) {
      for (int column = 1; column < n; ++column) {
        dp[row][column] = dp[row - 1][column] + dp[row][column - 1];
      }
    }
    return dp[m - 1][n - 1];
  }
};
```

## 解法三：滚动数组 DP

逐行扫描时，更新前的 `dp[column]` 是上方路径数，更新后的 `dp[column - 1]` 是左方路径数，
所以可把二维表压成一维。时间仍为 $O(mn)$，空间降为 $O(n)$；让较短维作为列还可写成
$O(\min(m,n))$ 空间。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePaths(int m, int n) {
    if (m < n) swap(m, n);
    vector<int> dp(n, 1);
    for (int row = 1; row < m; ++row) {
      for (int column = 1; column < n; ++column) {
        dp[column] += dp[column - 1];
      }
    }
    return dp[n - 1];
  }
};
```

## 从 DP 到组合数

二维转移与杨辉三角完全相同，但路径还有更直接的编码：把一条路径写成长度 $m+n-2$ 的
R/D 字符串。只要选出 $m-1$ 个 `D` 的位置，其余位置就自动是 `R`。这是路径与组合选择
之间的双射。

为降低中间数值，取 $k=\min(m-1,n-1)$，按

$$
\binom{T}{k}=\prod_{i=1}^{k}\frac{T-k+i}{i}
$$

逐步计算。每一步的结果都是整数；在题目保证的有效测试中，结果单调增长且最终不超过
$2\times10^9$，`long long` 的乘法中间值安全。

## 最佳实用解：乘法计算组合数

### 正确性证明

每条合法路径恰有 $m-1$ 个 `D` 和 $n-1$ 个 `R`，所以映射到 `D` 的位置集合，集合大小为
$m-1$。反过来，任取这样的集合，在这些位置向下、其余位置向右，最终必从左上角走到右下角，
且过程中不会越界。两个不同集合产生的移动串不同，因此这是双射，路径数就是组合数。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePaths(int m, int n) {
    int total = m + n - 2;
    int choose = min(m - 1, n - 1);
    long long answer = 1;
    for (int i = 1; i <= choose; ++i) {
      answer = answer * (total - choose + i) / i;
    }
    return static_cast<int>(answer);
  }
};
```

时间复杂度 $O(\min(m,n))$，额外空间 $O(1)$。

## 同阶与实用方案比较

- 二维 DP 最直观，最容易迁移到障碍、权值等变种，但保存了不必要的整张表。
- 一维 DP 仍保留局部转移语义，是面试中最稳健的通用答案。
- 组合数代码最短、空间最小，但依赖“无障碍且只允许右/下”的强结构。
- 本题推荐最终提交组合数；若题意稍有扩展，优先回到一维 DP，而不是勉强修补公式。

## 易错点

- 总步数是 $m+n-2$，不是 $m+n$。
- 选择次数应为 $m-1$ 或 $n-1$，取较小者只是为了少循环，不改变结果。
- 组合数乘法要先转成 `long long`，不能让 `int` 先溢出。
- 不能使用浮点阶乘再四舍五入；组合数的精确整数性很容易被浮点误差破坏。
- 单行或单列必须返回 1，递推初始化不能写成 0。

## 验证说明

所有代码块均通过 C++23 语法编译。对 $1\le m,n\le10$，递归枚举、二维 DP、一维 DP 与
组合数四种实现逐项比对一致；另检查了交换 $m,n$ 的对称性、单行单列和全部官方样例。

## 变种一：网格中加入障碍（LC 63）

新定义：`obstacleGrid[i][j] == 1` 的格子不可进入。组合数双射失效，因为同一种 R/D 排列
可能撞上障碍。将障碍格的路径数清零，其余格仍累加上方与左方，时间 $O(mn)$、空间 $O(n)$。

[力扣 63：不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
    int m = obstacleGrid.size();
    int n = obstacleGrid[0].size();
    vector<long long> dp(n);
    dp[0] = obstacleGrid[0][0] == 0;
    for (int row = 0; row < m; ++row) {
      for (int column = 0; column < n; ++column) {
        if (obstacleGrid[row][column] == 1) {
          dp[column] = 0;
        } else if (column > 0) {
          dp[column] += dp[column - 1];
        }
      }
    }
    return static_cast<int>(dp[n - 1]);
  }
};
```

## 变种二：每个格子有代价，求最小路径和（LC 64）

新定义：走到格子要支付该格权值，目标从“计数”改为“最小化”。状态结构不变，但加法合并
改成取最小值，转移为 `grid + min(up, left)`。时间 $O(mn)$、空间 $O(n)$。

[力扣 64：最小路径和](https://leetcode.cn/problems/minimum-path-sum/)

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size();
    int n = grid[0].size();
    vector<int> dp(n, numeric_limits<int>::max() / 4);
    dp[0] = 0;
    for (int row = 0; row < m; ++row) {
      for (int column = 0; column < n; ++column) {
        int fromLeft = numeric_limits<int>::max() / 4;
        if (column > 0) fromLeft = dp[column - 1];
        dp[column] = grid[row][column] + min(dp[column], fromLeft);
      }
    }
    return dp[n - 1];
  }
};
```

## 变种三：恢复字典序第 k 条路径

新定义：令 `D < R`，给定合法的 1-based `k`，返回第 `k` 个移动串。若当前先放 `D`，剩余
路径数是一个组合数；若 `k` 不超过它就选 `D`，否则减去这一整块并选 `R`。复杂度
$O(m+n)$，下面用饱和组合数避免超过查询范围。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long combinations(int total, int choose, long long cap) {
    choose = min(choose, total - choose);
    __int128 value = 1;
    for (int i = 1; i <= choose; ++i) {
      value = value * (total - choose + i) / i;
      if (value >= cap) return cap;
    }
    return static_cast<long long>(value);
  }
public:
  string kthPath(int m, int n, long long k) {
    int down = m - 1;
    int right = n - 1;
    string answer;
    while (down + right > 0) {
      if (down == 0) {
        answer.push_back('R');
        --right;
        continue;
      }
      long long firstBlock = combinations(down + right - 1, down - 1, k);
      if (k <= firstBlock) {
        answer.push_back('D');
        --down;
      } else {
        answer.push_back('R');
        --right;
        k -= firstBlock;
      }
    }
    return answer;
  }
};
```

## 变种四：超大网格，答案对质数取模

新定义：$m+n-2$ 可达 $10^6$，返回组合数模质数 `mod`，并保证总步数小于 `mod`。普通整数
乘除不能在模意义下直接除；预处理阶乘与逆阶乘，用费马小定理求逆，时间 $O(m+n+\log mod)$、
空间 $O(m+n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long power(long long base, long long exponent, long long mod) {
    long long result = 1;
    while (exponent > 0) {
      if (exponent & 1) result = result * base % mod;
      base = base * base % mod;
      exponent >>= 1;
    }
    return result;
  }
public:
  int uniquePathsModulo(int m, int n, int mod) {
    int total = m + n - 2;
    int choose = m - 1;
    vector<long long> factorial(total + 1, 1), inverse(total + 1, 1);
    for (int i = 1; i <= total; ++i) factorial[i] = factorial[i - 1] * i % mod;
    inverse[total] = power(factorial[total], mod - 2, mod);
    for (int i = total; i > 0; --i) inverse[i - 1] = inverse[i] * i % mod;
    long long answer = factorial[total] * inverse[choose] % mod;
    answer = answer * inverse[total - choose] % mod;
    return static_cast<int>(answer);
  }
};
```

## 推荐记忆

记住同一个模型的三层表达：网格状态递推、滚动数组、固定 R/D 多重集合的排列数。面试先用
DP 建立正确性，再根据“步数固定且无障碍”推出组合数；遇到任何结构变化，优先退回 DP。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/unique-paths/)
- [对应知识专题](../../dp/grid-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc472-d/">← [atcoder] ABC472 D Bomber Mad</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-516-q1-lc4030/">[力扣竞赛] 第 516 场周赛 Q1 LC 4030 判断 ASCII 值回文 简单 →</a>
</nav>
