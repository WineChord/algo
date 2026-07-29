---
title: "[力扣 Top 10] LC 70 爬楼梯 简单"
---

# [力扣 Top 10] LC 70 爬楼梯 简单

<p class="daily-archive-kicker">2026-07-26 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../dp/linear-recurrences/">进入知识专题</a></p>

## 官方原始信息

- 难度：简单
- 官方链接：[打开官方页面](https://leetcode.cn/problems/climbing-stairs/)
- 函数签名：`int climbStairs(int n)`

### 原始题意

爬到第 `n` 阶楼顶，每次恰好走 1 阶或 2 阶，求不同移动序列的数量。

### 全部官方样例

1. `n = 2`，输出 `2`：`1+1`、`2`。
2. `n = 3`，输出 `3`：`1+1+1`、`1+2`、`2+1`。

### 全部约束

- $1\le n\le45$

## 最优结论

设 $f(i)$ 为到达第 $i$ 阶的方法数。最后一步只能来自 $i-1$ 或 $i-2$，两类方案互斥且覆盖全部情况，因此

$$
f(i)=f(i-1)+f(i-2),\qquad f(1)=1,\ f(2)=2.
$$

滚动保存前两项即可，时间 $O(n)$，额外空间 $O(1)$。这就是偏移后的 Fibonacci 数：$f(n)=F_{n+1}$。

## 约束、边界与观察

- “不同方法”区分步长顺序，`1+2` 与 `2+1` 不同。
- `n=1` 只有一种方法，不能从数组下标 2 起步后越界。
- $n\le45$ 保证答案 `1836311903` 仍在 32 位有符号整数范围内；若继续增大必须使用更宽整数或取模。
- 递归树会反复计算相同楼层，时间呈指数增长。

## 样例手推

$f(1)=1$、$f(2)=2$，所以 $f(3)=3$：最后走 1 阶的方案来自 `n=2` 的两种方法，最后走 2 阶的方案来自 `n=1` 的一种方法。

## 解法一：直接递归

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int climbStairs(int n) {
    if (n <= 2) return n;
    return climbStairs(n - 1) + climbStairs(n - 2);
  }
};
```

时间 $O(\varphi^n)$，递归栈 $O(n)$。它忠实表达状态转移，但重复计算严重。

## 解法二：记忆化搜索

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> memo;
  int solve(int n) {
    if (n <= 2) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = solve(n - 1) + solve(n - 2);
  }
public:
  int climbStairs(int n) {
    memo.assign(n + 1, -1);
    return solve(n);
  }
};
```

每个状态只计算一次，时间 $O(n)$，空间 $O(n)$。

## 解法三：自底向上动态规划

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int climbStairs(int n) {
    if (n <= 2) return n;
    vector<int> dp(n + 1);
    dp[1] = 1;
    dp[2] = 2;
    for (int i = 3; i <= n; ++i) dp[i] = dp[i - 1] + dp[i - 2];
    return dp[n];
  }
};
```

时间 $O(n)$，空间 $O(n)$。它消除了递归开销，但每个状态只依赖前两项，数组仍可压缩。

## 解法四：滚动变量（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; ++i) {
      int current = prev1 + prev2;
      prev2 = prev1;
      prev1 = current;
    }
    return prev1;
  }
};
```

### 正确性证明

按楼层归纳。基础状态 $f(1)=1,f(2)=2$ 正确。假设 `prev2`、`prev1` 分别等于 $f(i-2),f(i-1)$，所有到达 $i$ 的方案按最后一步长度分为：从 $i-1$ 走 1 阶，与从 $i-2$ 走 2 阶；两集合不交并覆盖全部方案，所以 `current = prev1 + prev2 = f(i)`。滚动后不变量对下一层继续成立，最终返回 $f(n)$。

时间 $O(n)$，空间 $O(1)$。若只计算单个 $n\le45$，它常数小、边界清楚，面试首选；若 $n$ 极大，再使用矩阵快速幂或快速倍增。

## 常见错误

- 把 $f(0)$ 未定义与组合意义下的 $f(0)=1$ 混用，导致基例偏移。
- 初始化为 Fibonacci 的 `0,1` 后返回了 $F_n$ 而不是 $F_{n+1}$。
- 更新两个滚动变量时先覆盖旧值。
- 误把方法当集合而忽略顺序。
- 扩大约束后仍用 `int`，发生溢出。

## Follow-up 1：允许任意步长集合

给定正步长集合 `steps`，转移为 $dp[i]=\sum_{d\in steps,i\ge d}dp[i-d]$，并令 $dp[0]=1$ 表示空序列。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countWays(int n, vector<int> steps) {
    sort(steps.begin(), steps.end());
    steps.erase(unique(steps.begin(), steps.end()), steps.end());
    vector<long long> dp(n + 1);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
      for (int step : steps) {
        if (step > i) break;
        dp[i] += dp[i - step];
      }
    }
    return dp[n];
  }
};
```

时间 $O(nk)$，空间 $O(n)$，其中 $k$ 是不同步长数。

## Follow-up 2：部分台阶禁止落脚

禁止状态的方法数直接设为 0，其他状态仍从可达前驱累加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long climbWithBlocked(int n, vector<int> blocked) {
    vector<char> forbidden(n + 1);
    for (int x : blocked) {
      if (1 <= x && x <= n) forbidden[x] = 1;
    }
    vector<long long> dp(n + 1);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
      if (forbidden[i]) continue;
      dp[i] = dp[i - 1];
      if (i >= 2) dp[i] += dp[i - 2];
    }
    return dp[n];
  }
};
```

时间 $O(n+b)$，空间 $O(n)$，其中 $b$ 是禁止台阶数。

## Follow-up 3：每阶有代价，求最小总代价

对应 [LeetCode 746 · 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)。计数加法改为最小值转移。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minCostClimbingStairs(vector<int>& cost) {
    int prev2 = 0, prev1 = 0;
    for (int i = 2; i <= (int)cost.size(); ++i) {
      int current = min(prev1 + cost[i - 1], prev2 + cost[i - 2]);
      prev2 = prev1;
      prev1 = current;
    }
    return prev1;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 4：`n` 极大并对模数取余

利用 $f(n)=F_{n+1}$，用 Fibonacci 快速倍增在 $O(\log n)$ 时间求值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long mod;
  pair<long long, long long> fib(unsigned long long n) {
    if (n == 0) return {0, 1};
    auto [a, b] = fib(n >> 1);
    long long c = a * ((2 * b % mod - a + mod) % mod) % mod;
    long long d = (a * a % mod + b * b % mod) % mod;
    if (n & 1) return {d, (c + d) % mod};
    return {c, d};
  }
public:
  long long climbStairsHuge(unsigned long long n, long long modulus) {
    mod = modulus;
    return fib(n + 1).first;
  }
};
```

时间 $O(\log n)$，递归栈 $O(\log n)$。乘法安全要求 `mod` 不超过约 $3\times10^9$；更大模数应使用 `__int128`。

## 验证

对 $n=1\ldots45$ 比较递归（小 $n$）、记忆化、数组 DP、滚动变量与快速倍增结果；边界覆盖 `n=1,2,45`。任意步长变种可对小 `n` 枚举所有步长序列作 oracle。

## Reference

- [官方题目](https://leetcode.cn/problems/climbing-stairs/)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-9-lc15/">← [力扣 Top 9] LC 15 三数之和 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-511-q1-lc3996/">[力扣竞赛] 第 511 场周赛 Q1 LC 3996 偶数次骑士移动 简单 →</a>
</nav>
