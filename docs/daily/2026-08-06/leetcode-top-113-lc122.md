---
title: "[力扣 Top 113] LC 122 买卖股票的最佳时机 II 中等"
---

# [力扣 Top 113] LC 122 买卖股票的最佳时机 II 中等

<p class="daily-archive-kicker">2026-08-06 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0eaf3dffd28afaa1d43d04d22ecace5715ef47155fce561e89502d97d147bf2a -->
## 官方原始信息

- Top 排名：113
- 题号：LC 122
- 官方中文标题：买卖股票的最佳时机 II
- 官方难度：中等
- 官方链接：[买卖股票的最佳时机 II](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/)

### 原始题意与函数签名

第 `i` 天股价为 `prices[i]`。任意时刻最多持有一股，可以同日卖出后再买入，求不限交易次数时的最大利润。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maxProfit(vector<int>& prices);
};
```

### 全部官方样例

```text
输入：prices = [7,1,5,3,6,4]
输出：7
解释：1 买 5 卖得 4，3 买 6 卖得 3。
```

```text
输入：prices = [1,2,3,4,5]
输出：4
```

```text
输入：prices = [7,6,4,3,1]
输出：0
```

### 全部约束

- $1\le n\le3\times10^4$。
- $0\le prices_i\le10^4$。

## 约束推导与观察

每天只有“收盘后不持股”和“收盘后持股”两个状态。不限交易次数且无手续费时，一段上涨 `a<b<c` 的利润满足 $(c-a)=(b-a)+(c-b)$，所以可以把每段上涨拆成所有正相邻差之和，不会丢失最优性。最大利润不超过 $(n-1)10^4<3\times10^8$，`int` 安全。

## 解法递进

### 解法一：枚举每天买、卖或等待

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int dfs(const vector<int>& prices, int day, bool holding) {
    if (day == static_cast<int>(prices.size())) {
      return holding ? INT_MIN / 2 : 0;
    }
    int answer = dfs(prices, day + 1, holding);
    if (holding) {
      answer = max(answer, prices[day] + dfs(prices, day + 1, false));
    } else {
      answer = max(answer, -prices[day] + dfs(prices, day + 1, true));
    }
    return answer;
  }
public:
  int maxProfit(vector<int>& prices) {
    return dfs(prices, 0, false);
  }
};
```

时间 $O(2^n)$、递归空间 $O(n)$，能完整覆盖所有合法动作，是小规模 oracle。

### 解法二：两状态动态规划

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int cash = 0;
    int hold = -prices[0];
    for (int i = 1; i < static_cast<int>(prices.size()); ++i) {
      int oldCash = cash;
      cash = max(cash, hold + prices[i]);
      hold = max(hold, oldCash - prices[i]);
    }
    return cash;
  }
};
```

时间 $O(n)$，空间 $O(1)$。它保留了可扩展到手续费、冷冻期等变种的统一状态模型。

### 最佳实用解：累加所有正相邻差

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int answer = 0;
    for (int i = 1; i < static_cast<int>(prices.size()); ++i) {
      answer += max(0, prices[i] - prices[i - 1]);
    }
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(1)$，常数最小。对本题优先记忆贪心；同时记住它依赖“不限次数、无手续费、无冷冻期”。

## 正确性证明

任何交易 `[buy,sell]` 的利润可望远镜展开为区间内相邻差之和，其中负差只会降低利润，故所有交易总利润不超过全部正相邻差之和。反过来，对每个正差 `prices[i]-prices[i-1]`，在第 `i-1` 天买入、第 `i` 天卖出；相邻交易允许同日卖出再买入，动作合法，恰取得这部分利润。因此上界可达，贪心最优。

## 样例手推

样例 1 的相邻差为 `-6,+4,-2,+3,-2`，正差和为 `4+3=7`。全下降样例没有正差，最优是从不交易，利润为 0。单日数组循环不执行，也返回 0。

## 易错点与方案比较

- 不能同时持有多股；正差拆分仍只需一股。
- 本题允许同日卖出再买入，因此连续上涨每天结算与一次持有等价。
- 若加入手续费或冷冻期，直接累加正差立即失效，应回到状态 DP。
- 更新 `hold` 时使用旧 `cash` 最清晰，避免变种中同日状态串用。

## 变种一：每次交易收取手续费

对应 [LC 714 买卖股票的最佳时机含手续费](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)。卖出时扣费，正差不再能独立结算。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices, int fee) {
    int cash = 0;
    int hold = -prices[0];
    for (int i = 1; i < static_cast<int>(prices.size()); ++i) {
      int oldCash = cash;
      cash = max(cash, hold + prices[i] - fee);
      hold = max(hold, oldCash - prices[i]);
    }
    return cash;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：卖出后有一天冷冻期

对应 [LC 309 买卖股票的最佳时机含冷冻期](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/)。维护持股、当天卖出、空闲三个状态。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(vector<int>& prices) {
    int hold = -prices[0];
    int sold = INT_MIN / 2;
    int rest = 0;
    for (int i = 1; i < static_cast<int>(prices.size()); ++i) {
      int nextHold = max(hold, rest - prices[i]);
      int nextSold = hold + prices[i];
      int nextRest = max(rest, sold);
      hold = nextHold;
      sold = nextSold;
      rest = nextRest;
    }
    return max(rest, sold);
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：至多完成 `k` 笔交易

对应 [LC 188 买卖股票的最佳时机 IV](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/)。第 `j` 笔交易维护买入与卖出最优值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProfit(int k, vector<int>& prices) {
    if (prices.empty()) {
      return 0;
    }
    if (k >= static_cast<int>(prices.size()) / 2) {
      int answer = 0;
      for (int i = 1; i < static_cast<int>(prices.size()); ++i) {
        answer += max(0, prices[i] - prices[i - 1]);
      }
      return answer;
    }
    vector<int> buy(k + 1, INT_MIN / 2);
    vector<int> sell(k + 1);
    for (int price : prices) {
      for (int j = 1; j <= k; ++j) {
        buy[j] = max(buy[j], sell[j - 1] - price);
        sell[j] = max(sell[j], buy[j] + price);
      }
    }
    return sell[k];
  }
};
```

时间 $O(nk)$，空间 $O(k)$。

## 变种四：恢复一组最优交易区间

新定义：输出任一组取得最大利润的买卖日。把每个严格上升段压成一次谷底买入、峰顶卖出，利润仍等于正差和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> prices(n);
  for (int& x : prices) {
    cin >> x;
  }
  vector<pair<int, int>> trades;
  int i = 0;
  while (i + 1 < n) {
    while (i + 1 < n && prices[i + 1] <= prices[i]) {
      ++i;
    }
    int buy = i;
    while (i + 1 < n && prices[i + 1] > prices[i]) {
      ++i;
    }
    if (i > buy) {
      trades.push_back({buy, i});
    }
  }
  cout << trades.size() << '\n';
  for (auto [buy, sell] : trades) {
    cout << buy << ' ' << sell << '\n';
  }
}
```

时间 $O(n)$，输出外空间 $O(1)$。

## 可复现验证

枚举长度不超过 10、价格值域 `0..6` 的数组，以三动作 DFS 为 oracle，对比 DP 与正差贪心；固定覆盖单日、全等、全升、全降、锯齿和零价格。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-112-lc155/">← [力扣 Top 112] LC 155 最小栈 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-114-lc142/">[力扣 Top 114] LC 142 环形链表 II 中等 →</a>
</nav>
