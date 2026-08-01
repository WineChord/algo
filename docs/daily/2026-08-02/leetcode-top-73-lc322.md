---
title: "[力扣 Top 73] LC 322 零钱兑换 中等"
---

# [力扣 Top 73] LC 322 零钱兑换 中等

<p class="daily-archive-kicker">2026-08-02 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=82c76d47ad9e24e62667526fe66b0d3e53e7f053d61d18839ff3bad5332646e9 -->
## 官方原始信息

- Top 排名：73
- 题号：LC 322
- 官方中文标题：零钱兑换
- 官方难度：中等
- 官方链接：[零钱兑换](https://leetcode.cn/problems/coin-change/)

### 原始题意

给定不同面额数组 `coins` 和目标金额 `amount`。每种硬币可使用无限次，返回凑出目标金额所需的最少硬币数；无法凑出时返回 `-1`。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int coinChange(vector<int>& coins, int amount);
};
```

### 全部官方样例

```text
输入：coins = [1,2,5], amount = 11
输出：3
解释：11 = 5 + 5 + 1。
```

```text
输入：coins = [2], amount = 3
输出：-1
```

```text
输入：coins = [1], amount = 0
输出：0
```

### 全部约束

- $1\le |coins|\le12$。
- $1\le coins_i\le2^{31}-1$。
- $0\le amount\le10^4$。
- 每种硬币数量无限。

## 约束推导与状态选择

硬币种数很少，但目标金额达到 $10^4$，按每枚硬币选多少枚做组合枚举仍可能指数爆炸。金额非负且每次加入硬币都会让剩余金额严格下降，因此“凑出金额 $x$ 的最少硬币数”只依赖更小金额，形成一维完全背包。

定义 $dp[x]$ 为凑出 $x$ 的最少硬币数。边界 $dp[0]=0$；对每个 $x>0$，最后一枚硬币若为 $c$，则前缀必须最优地凑出 $x-c$：

$$
dp[x]=1+\min_{c\le x}dp[x-c].
$$

不可达状态使用 `amount+1` 作无穷大，因为任何可行解最多使用 `amount` 枚面额 1 的硬币；没有面额 1 时这个上界仍安全。先判断 `coin <= amount`，避免大面额参与无意义下标或加法。

## 解法递进

### 解法一：枚举每一步选择

从剩余金额出发尝试所有不超过它的硬币，递归取最小值。它完整枚举所有有序取币序列。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const vector<int>& coins, int remaining) {
    if (remaining == 0) {
      return 0;
    }
    int best = remaining + 1;
    for (int coin : coins) {
      if (coin <= remaining) {
        int suffix = search(coins, remaining - coin);
        if (suffix != -1) {
          best = min(best, suffix + 1);
        }
      }
    }
    return best == remaining + 1 ? -1 : best;
  }
public:
  int coinChange(vector<int>& coins, int amount) {
    return search(coins, amount);
  }
};
```

最坏时间指数级，递归深度 $O(amount)$；只适合很小金额的 oracle。

### 解法二：自顶向下记忆化

相同剩余金额会被不同取币顺序反复访问。缓存每个金额的答案，把状态数降为 `amount+1`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> memo;
  int solve(const vector<int>& coins, int remaining) {
    if (remaining == 0) {
      return 0;
    }
    if (memo[remaining] != -2) {
      return memo[remaining];
    }
    int best = remaining + 1;
    for (int coin : coins) {
      if (coin <= remaining) {
        int previous = solve(coins, remaining - coin);
        if (previous != -1) {
          best = min(best, previous + 1);
        }
      }
    }
    return memo[remaining] = best == remaining + 1 ? -1 : best;
  }
public:
  int coinChange(vector<int>& coins, int amount) {
    memo.assign(amount + 1, -2);
    memo[0] = 0;
    return solve(coins, amount);
  }
};
```

时间 $O(amount\cdot|coins|)$，空间 $O(amount)$，另有同阶最坏递归栈。

### 最佳实用解：自底向上一维完全背包

按金额递增，转移所需的 `dp[value-coin]` 已经确定。迭代写法消除深递归风险。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int value = 1; value <= amount; ++value) {
      for (int coin : coins) {
        if (coin <= value) {
          dp[value] = min(dp[value], dp[value - coin] + 1);
        }
      }
    }
    return dp[amount] > amount ? -1 : dp[amount];
  }
};
```

时间 $O(amount\cdot|coins|)$，空间 $O(amount)$。这是约束下最稳定、最易扩展的实用解。

## 正确性证明

对金额 $x$ 归纳。$x=0$ 时不用硬币，`dp[0]=0` 正确。假设所有小于 $x$ 的状态正确。任意凑出 $x$ 的方案都有最后一枚硬币 $c$，删去它后是凑出 $x-c$ 的方案；由归纳假设，其硬币数不少于 `dp[x-c]`，所以任意方案不少于转移所得最小值。反过来，若某个 `dp[x-c]` 可达，在其最优方案后加一枚 $c$ 就构成 `dp[x-c]+1` 的合法方案。因此转移既不低估也不高估，`dp[x]` 正确。归纳至 `amount` 即得结论。

## 样例手推

`coins=[1,2,5]` 时，`dp[1]=1`、`dp[2]=1`、`dp[5]=1`，继续递推得到 `dp[10]=2`、`dp[11]=3`。`coins=[2],amount=3` 中只有偶数状态可达，`dp[3]` 保持无穷大，返回 `-1`。`amount=0` 直接读取 `dp[0]=0`。

## 易错点与方案比较

- 这是求最少数量，不是组合数；不可达状态不能默认 0。
- `amount=0` 的答案是 0，不需要任何硬币。
- 硬币面额可远大于金额，转移前必须检查 `coin <= value`。
- 贪心取最大面额对 `[1,3,4],6` 会得到 `4+1+1`，不如 `3+3`，一般币制不能贪心。
- 记忆化与迭代同阶；面试中先写递推含义，再推荐无栈风险的自底向上版本。

## 变种一：恢复一组最少硬币方案

新定义：除数量外输出实际硬币。更新 `dp[x]` 时记录最后使用的面额，从目标金额逆推。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, amount;
  cin >> n >> amount;
  vector<int> coins(n), dp(amount + 1, amount + 1), last(amount + 1, -1);
  for (int& coin : coins) {
    cin >> coin;
  }
  dp[0] = 0;
  for (int value = 1; value <= amount; ++value) {
    for (int coin : coins) {
      if (coin <= value && dp[value - coin] + 1 < dp[value]) {
        dp[value] = dp[value - coin] + 1;
        last[value] = coin;
      }
    }
  }
  if (last[amount] == -1 && amount != 0) {
    cout << -1 << '\n';
    return 0;
  }
  cout << dp[amount] << '\n';
  for (int value = amount; value > 0; value -= last[value]) {
    cout << last[value] << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\cdot amount)$，空间 $O(amount)$。

## 变种二：统计无序组合数量

新定义：求凑出金额的组合数，硬币顺序不区分。把硬币放在外层，保证每个组合按非降面额只生成一次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, amount;
  cin >> n >> amount;
  vector<int> coins(n);
  for (int& coin : coins) {
    cin >> coin;
  }
  vector<unsigned long long> ways(amount + 1);
  ways[0] = 1;
  for (int coin : coins) {
    for (int value = coin; value <= amount; ++value) {
      ways[value] += ways[value - coin];
    }
  }
  cout << ways[amount] << '\n';
}
```

时间 $O(n\cdot amount)$，空间 $O(amount)$；若答案可能更大，应按题意取模或使用大整数。

## 变种三：每种硬币数量有限

新定义：第 $i$ 种面额只有 `count[i]` 枚。无限使用转移失效；把数量按二进制拆成若干 0-1 物品，每组带金额与硬币数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, amount;
  cin >> n >> amount;
  vector<int> dp(amount + 1, amount + 1);
  dp[0] = 0;
  for (int i = 0; i < n; ++i) {
    int coin, count;
    cin >> coin >> count;
    for (int group = 1; count > 0; group <<= 1) {
      int take = min(group, count);
      count -= take;
      long long weight = 1LL * coin * take;
      if (weight > amount) {
        continue;
      }
      for (int value = amount; value >= weight; --value) {
        dp[value] = min(dp[value], dp[value - weight] + take);
      }
    }
  }
  cout << (dp[amount] > amount ? -1 : dp[amount]) << '\n';
}
```

时间 $O(amount\sum_i\log(count_i+1))$，空间 $O(amount)$。

## 变种四：同一币制回答多个金额

新定义：币制固定，有 $Q$ 个金额询问。先读出最大金额并一次预处理，随后 $O(1)$ 回答。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> coins(n), queries(q);
  for (int& coin : coins) {
    cin >> coin;
  }
  int maximum = 0;
  for (int& value : queries) {
    cin >> value;
    maximum = max(maximum, value);
  }
  vector<int> dp(maximum + 1, maximum + 1);
  dp[0] = 0;
  for (int value = 1; value <= maximum; ++value) {
    for (int coin : coins) {
      if (coin <= value) {
        dp[value] = min(dp[value], dp[value - coin] + 1);
      }
    }
  }
  for (int value : queries) {
    cout << (dp[value] > maximum ? -1 : dp[value]) << '\n';
  }
}
```

预处理 $O(n\cdot A_{max})$，每次查询 $O(1)$，空间 $O(A_{max})$。

## 验证说明

自底向上解与指数枚举在 7000 个小金额、随机币制上对拍；另覆盖最大面额、金额 0、最大公因数不整除金额和大量重复路径。七段代码均通过 C++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/coin-change/)
- [对应知识专题](../../dp/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-72-lc34/">← [力扣 Top 72] LC 34 在排序数组中查找元素的第一个和最后一个位置 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-74-lc64/">[力扣 Top 74] LC 64 最小路径和 中等 →</a>
</nav>
