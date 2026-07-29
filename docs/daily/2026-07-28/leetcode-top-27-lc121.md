---
title: "[力扣 Top 27] LC 121 买卖股票的最佳时机 简单"
---

# [力扣 Top 27] LC 121 买卖股票的最佳时机 简单

<p class="daily-archive-kicker">2026-07-28 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

## 官方原始信息

- 官方链接：[打开官方页面](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)
- slug：`best-time-to-buy-and-sell-stock`
- 官方难度：简单；官方竞赛分未提供；ZeroTracer 数据集无记录。
- 函数签名：`int maxProfit(vector<int>& prices)`
- 题意：第 `i` 天价格为 `prices[i]`，至多完成一次“先买后卖”，返回最大非负利润。
- 样例 1：`[7,1,5,3,6,4]` 输出 `5`，在价格 `1` 买入、`6` 卖出。
- 样例 2：`[7,6,4,3,1]` 输出 `0`。
- 约束：$1\le n\le10^5$，$0\le prices[i]\le10^4$。

最大差值不超过 $10^4$，`int` 足够。`n` 要求避免枚举全部买卖日。

## 解法一：枚举买卖日

枚举所有 $i<j$，覆盖全部合法交易。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int ans = 0;
    for (int buy = 0; buy < (int)prices.size(); ++buy) {
      for (int sell = buy + 1; sell < (int)prices.size(); ++sell) {
        ans = max(ans, prices[sell] - prices[buy]);
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间 $O(1)$；瓶颈是不同卖出日反复寻找此前最低价格。

## 解法二：后缀最大值

预处理每一天及之后的最高卖价，再枚举买入日。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int n = prices.size();
    vector<int> suffixMax(n);
    suffixMax[n - 1] = prices[n - 1];
    for (int i = n - 2; i >= 0; --i) suffixMax[i] = max(prices[i], suffixMax[i + 1]);
    int ans = 0;
    for (int i = 0; i < n; ++i) ans = max(ans, suffixMax[i] - prices[i]);
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(n)$。它消除了重复比较，但整张后缀表并非必要。

## 最佳实用解：扫描维护前缀最低价

把当前天视为卖出日。所有合法买入日都在此前，故只需此前最低价 `minimum`。处理价格 `p` 时先用 `p-minimum` 更新答案，再更新最低价；即便交换这两句，本题同日差值为 0，也不影响答案，但“先卖后纳入买入候选”更贴合不变量。

不变量：扫描到第 `i` 天后，`minimum=min(prices[0..i])`，`answer` 是卖出日不晚于 `i` 的最佳利润。新的一天只新增“第 `i` 天卖出”的交易，其最佳买价恰是此前最低价，因此转移完整且不遗漏。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int minimum = prices[0];
    int answer = 0;
    for (int price : prices) {
      answer = max(answer, price - minimum);
      minimum = min(minimum, price);
    }
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(1)$。优先记忆这一解法：它既是前缀最值，也是“最低持仓成本”的两状态 DP。

边界：单日返回 0；全下降返回 0；相同价格不会产生正利润；最低价可多次出现。常见错误包括允许卖出在买入之前、返回负数、把“至多一次”误解为必须交易、错误套用无限次交易的所有正差值。

## Follow-up 1：返回最佳买卖日

新定义：返回零基下标 `{buy,sell}`，无正利润时返回 `{-1,-1}`。除最低价外记录其最早下标；只在利润严格变大时更新，可稳定保留最早发现方案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> bestTransaction(vector<int>& prices) {
    int minIndex = 0;
    int bestBuy = -1, bestSell = -1, bestProfit = 0;
    for (int i = 1; i < (int)prices.size(); ++i) {
      int profit = prices[i] - prices[minIndex];
      if (profit > bestProfit) {
        bestProfit = profit;
        bestBuy = minIndex;
        bestSell = i;
      }
      if (prices[i] < prices[minIndex]) minIndex = i;
    }
    return {bestBuy, bestSell};
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 2：允许无限次交易

新定义：可完成任意次交易，但同一时刻最多持有一股。原“全局最低买价”失效，因为卖出后可以再次买入；每段正上涨都应收集。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfitUnlimited(vector<int>& prices) {
    int answer = 0;
    for (int i = 1; i < (int)prices.size(); ++i) {
      answer += max(0, prices[i] - prices[i - 1]);
    }
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(1)$。任意跨多天上涨等于相邻正差值之和。

## Follow-up 3：至多 `k` 次交易

新定义：最多完成 `k` 次买卖。需要记录交易次数；`buy[t]` 表示完成前 `t-1` 次交易后持股的最大收益，`sell[t]` 表示完成至多 `t` 次并空仓的最大收益。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfitK(int k, vector<int>& prices) {
    int n = prices.size();
    if (k >= n / 2) {
      int ans = 0;
      for (int i = 1; i < n; ++i) ans += max(0, prices[i] - prices[i - 1]);
      return ans;
    }
    vector<int> buy(k + 1, INT_MIN / 2), sell(k + 1);
    for (int price : prices) {
      for (int t = 1; t <= k; ++t) {
        buy[t] = max(buy[t], sell[t - 1] - price);
        sell[t] = max(sell[t], buy[t] + price);
      }
    }
    return sell[k];
  }
};
```

时间 $O(nk)$，空间 $O(k)$。

## Follow-up 4：无限次交易且每次收手续费

新定义：每次完成交易支付 `fee`。局部正差值不再能独立贪心，因为一次长交易可少付手续费；使用持股/空仓 DP。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfitWithFee(vector<int>& prices, int fee) {
    int cash = 0;
    int hold = -prices[0];
    for (int i = 1; i < (int)prices.size(); ++i) {
      int oldCash = cash;
      cash = max(cash, hold + prices[i] - fee);
      hold = max(hold, oldCash - prices[i]);
    }
    return cash;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 5：无限次交易且卖出后冷冻一天

新定义：卖出后的下一天不能买入。新增 `sold` 与 `rest` 状态，原两状态不足以表达冷冻约束。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfitCooldown(vector<int>& prices) {
    int hold = -prices[0];
    int sold = INT_MIN / 2;
    int rest = 0;
    for (int i = 1; i < (int)prices.size(); ++i) {
      int oldHold = hold, oldSold = sold, oldRest = rest;
      hold = max(oldHold, oldRest - prices[i]);
      sold = oldHold + prices[i];
      rest = max(oldRest, oldSold);
    }
    return max(sold, rest);
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

最优解与两重循环应在随机 `n<=30`、随机价格序列上对拍；无限次与手续费等变种分别用小规模状态搜索或二维 DP 交叉检查。结果见 `validation-report.json`。

## Reference

- [官方题目](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-26-lc239/">← [力扣 Top 26] LC 239 滑动窗口最大值 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-28-lc25/">[力扣 Top 28] LC 25 K 个一组翻转链表 困难 →</a>
</nav>
