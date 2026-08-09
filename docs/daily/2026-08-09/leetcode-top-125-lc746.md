---
title: "[力扣 Top 125] LC 746 使用最小花费爬楼梯 简单"
---

# [力扣 Top 125] LC 746 使用最小花费爬楼梯 简单

<p class="daily-archive-kicker">2026-08-09 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../dp/linear-recurrences/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4f1d5d4c54d0690bf571847c7b8f109691559d971c6b8e873e3712b4634ff054 -->
## 官方原始信息

- Top 排名：125
- 题号：LC 746
- 官方中文标题：使用最小花费爬楼梯
- 官方难度：简单
- 官方链接：[使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)

### 原始题意与函数签名

`cost[i]` 是从第 `i` 级向上爬时支付的费用；付费后可上 1 或 2 级。可以从第 0 或第 1 级开始，求到达下标 `n` 所代表楼顶的最低花费。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minCostClimbingStairs(vector<int>& cost);
};
```

### 全部官方样例

```text
输入：cost = [10,15,20]
输出：15
解释：从下标 1 开始，支付 15 后跨两级到楼顶。
```

```text
输入：cost = [1,100,1,1,1,100,1,1,100,1]
输出：6
解释：依次支付下标 0、2、4、6、7、9 的费用到达楼顶。
```

### 全部约束

- $2\le n\le1000$。
- $0\le cost_i\le999$。

## 约束推导与观察

把楼顶视为下标 `n` 且费用为 0。到达位置 `i` 的最后一步只能来自 `i-1` 或 `i-2`，因此最优子结构是

$$
dp_i=\min(dp_{i-1}+cost_{i-1},\ dp_{i-2}+cost_{i-2}),\qquad dp_0=dp_1=0.
$$

答案上界小于 $1000\times999$，`int` 足够。

## 解法递进

### 解法一：递归枚举每次走一步或两步

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int solve(const vector<int>& cost, int position) {
    if (position <= 1) {
      return 0;
    }
    return min(solve(cost, position - 1) + cost[position - 1],
        solve(cost, position - 2) + cost[position - 2]);
  }
public:
  int minCostClimbingStairs(vector<int>& cost) {
    return solve(cost, cost.size());
  }
};
```

覆盖全部路径，时间 $O(2^n)$、递归空间 $O(n)$，可作为小规模 oracle。

### 解法二：自底向上的动态规划表

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minCostClimbingStairs(vector<int>& cost) {
    int n = cost.size();
    vector<int> dp(n + 1);
    for (int i = 2; i <= n; ++i) {
      dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
    }
    return dp[n];
  }
};
```

时间 $O(n)$、空间 $O(n)$，显式保存了每个位置的最优值。

### 最佳实用解：滚动两个状态

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minCostClimbingStairs(vector<int>& cost) {
    int twoBack = 0;
    int oneBack = 0;
    for (int i = 2; i <= static_cast<int>(cost.size()); ++i) {
      int current = min(oneBack + cost[i - 1], twoBack + cost[i - 2]);
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
};
```

时间 $O(n)$、空间 $O(1)$。转移只依赖前两项，滚动变量是最简实用版本。

## 正确性证明

对位置 `i` 归纳。`dp[0]=dp[1]=0` 正确表示可免费从这两个位置开始。任何到达 `i>=2` 的路径，最后一步必从 `i-1` 或 `i-2` 出发，并分别支付对应台阶费用；归纳假设保证到这两个前驱的代价已最小，因此二者较小值就是到 `i` 的最小代价。滚动实现逐项计算相同递推，故返回 `dp[n]` 正确。

## 样例手推

`[10,15,20]`：`dp[2]=min(15,10)=10`，`dp[3]=min(10+20,0+15)=15`。第二个样例在高费用 100 前倾向跨两级，最终滚动状态到楼顶为 6。

## 易错点与方案比较

- 支付的是“离开台阶”的费用，不是“落到台阶”的费用。
- 楼顶下标是 `n`，没有额外费用。
- 起点 0 和 1 都免费，因此两个初值都是 0。
- 返回 `dp[n]`，不是 `min(dp[n-1],dp[n-2])`，除非使用了另一种状态定义。

## 变种一：恢复一条最低花费路径

新定义：除最小费用外，返回被付费的台阶下标。保留前驱并从楼顶反向恢复。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, vector<int>> minCostPath(const vector<int>& cost) {
  int n = cost.size();
  vector<int> dp(n + 1), parent(n + 1, -1);
  for (int i = 2; i <= n; ++i) {
    if (dp[i - 1] + cost[i - 1] <= dp[i - 2] + cost[i - 2]) {
      dp[i] = dp[i - 1] + cost[i - 1];
      parent[i] = i - 1;
    } else {
      dp[i] = dp[i - 2] + cost[i - 2];
      parent[i] = i - 2;
    }
  }
  vector<int> paid;
  for (int position = n; parent[position] != -1; position = parent[position]) {
    paid.push_back(parent[position]);
  }
  reverse(paid.begin(), paid.end());
  return {dp[n], paid};
}
int main() {
  auto [cost, path] = minCostPath({10, 15, 20});
  cout << cost << ' ' << path.size() << '\n';
}
```

时间 $O(n)$、空间 $O(n)$。

## 变种二：每次最多跨 `k` 级

新定义：可从前 `k` 个位置中的任意一个跳到当前楼层。转移是滑动窗口最小值，用单调队列把 $O(nk)$ 降为 $O(n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minCostKSteps(const vector<int>& cost, int k) {
  int n = cost.size();
  vector<long long> leave(n);
  deque<int> dq;
  for (int i = 0; i < n; ++i) {
    while (!dq.empty() && dq.front() < i - k) {
      dq.pop_front();
    }
    long long arrive = i < k ? 0 : leave[dq.front()];
    leave[i] = arrive + cost[i];
    while (!dq.empty() && leave[dq.back()] >= leave[i]) {
      dq.pop_back();
    }
    dq.push_back(i);
  }
  while (!dq.empty() && dq.front() < n - k) {
    dq.pop_front();
  }
  return dq.empty() ? 0 : leave[dq.front()];
}
int main() {
  cout << minCostKSteps({10, 15, 20}, 2) << '\n';
}
```

时间 $O(n)$、空间 $O(n)$；这里 `leave[i]` 表示付费离开 `i` 后的总代价。

## 变种三：费用允许为负数

新定义：某些台阶提供奖励。因为下标始终严格增加，状态图仍是 DAG，不会因负数形成循环；原 DP 仍成立，但用 64 位保存和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minCostWithRewards(const vector<long long>& cost) {
  long long twoBack = 0;
  long long oneBack = 0;
  for (int i = 2; i <= static_cast<int>(cost.size()); ++i) {
    long long current = min(oneBack + cost[i - 1], twoBack + cost[i - 2]);
    twoBack = oneBack;
    oneBack = current;
  }
  return oneBack;
}
int main() {
  cout << minCostWithRewards({-5, 10, -2}) << '\n';
}
```

时间 $O(n)$、空间 $O(1)$。

## 变种四：统计最低花费路径数量

新定义：返回最小费用及达到它的路径数，路径数对 `MOD` 取模。两种前驱代价相同时累加计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<long long, int> countOptimalPaths(const vector<int>& cost) {
  constexpr int MOD = 1000000007;
  int n = cost.size();
  vector<long long> dp(n + 1);
  vector<int> ways(n + 1, 1);
  for (int i = 2; i <= n; ++i) {
    long long fromOne = dp[i - 1] + cost[i - 1];
    long long fromTwo = dp[i - 2] + cost[i - 2];
    dp[i] = min(fromOne, fromTwo);
    ways[i] = 0;
    if (fromOne == dp[i]) {
      ways[i] = (ways[i] + ways[i - 1]) % MOD;
    }
    if (fromTwo == dp[i]) {
      ways[i] = (ways[i] + ways[i - 2]) % MOD;
    }
  }
  return {dp[n], ways[n]};
}
int main() {
  auto [cost, ways] = countOptimalPaths({0, 0, 0});
  cout << cost << ' ' << ways << '\n';
}
```

时间 $O(n)$、空间 $O(n)$。

## 可复现验证

枚举长度 $2..14$、费用值域 `0..9` 的随机数组，以递归枚举全部路径为 oracle，对比表 DP 与滚动 DP；固定覆盖全零、严格递增、高低交错和两起点同优。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/min-cost-climbing-stairs/)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-124-lc61/">← [力扣 Top 124] LC 61 旋转链表 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-126-lc295/">[力扣 Top 126] LC 295 数据流的中位数 困难 →</a>
</nav>
