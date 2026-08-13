---
title: "[力扣竞赛] 第 514 场周赛 Q1 LC 4014 应用折扣后的最低总价 中等"
---

# [力扣竞赛] 第 514 场周赛 Q1 LC 4014 应用折扣后的最低总价 中等

<p class="daily-archive-kicker">2026-08-14 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-14 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ccac6bfbdcb026477af13d4b588d4173389db9e3dae0de8fc266f79ae3a8f368 -->
[官方题目：LC 4014 应用折扣后的最低总价](https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/)

## 官方原始信息

- 比赛：第 514 场周赛。
- 题目：Q1，公开题号 LC 4014。
- 标题：应用折扣后的最低总价。
- 官方难度：中等。
- 官方比赛分值：4 分。
- 官方链接：[力扣中国](https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/)。
- ZeroTracer 社区估算竞赛分：截至 2026-08-14 未收录，记为未知。

给定商品原价数组 `prices` 与折扣百分比数组 `discounts`。每个折扣至多用于一件商品，每件商品至多使用一个折扣，也允许不使用折扣。把折扣 `d` 用在价格 `p` 上，支付价格为 $p(100-d)/100$，不做舍入。返回购买全部商品的最低总价；与正确答案的误差不超过 $10^{-5}$ 即可。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  double minPrice(vector<int>& prices, vector<int>& discounts);
};
```

### 全部官方样例

样例 1：

```text
输入：prices = [10,30,21], discounts = [50,60]
输出：32.50000
解释：把 60% 用于 30，把 50% 用于 21，未折扣商品为 10。
```

支付总价为 $30\times0.4+21\times0.5+10=32.5$。

样例 2：

```text
输入：prices = [100,70], discounts = [10,40,50]
输出：92.00000
解释：把 50% 用于 100，把 40% 用于 70，10% 折扣不使用。
```

样例 3：

```text
输入：prices = [7,3,9], discounts = [100,100]
输出：3.00000
解释：两张 100% 折扣用于价格 9 与 7 的商品，只需支付剩余商品的 3。
```

### 全部约束

- $1\le prices.length,discounts.length\le10^5$。
- $1\le prices[i]\le10^5$。
- $1\le discounts[i]\le100$。

## 约束推导与目标改写

若折扣 `d` 用在价格 `p` 上，相对原价节省 $pd/100$。所有商品原价总和固定，因此“最小支付总价”等价于“最大化折扣带来的总节省”。

所有价格与折扣都为正数，所以只要还有未匹配的商品和折扣，多使用一张折扣就会严格增加节省。最优方案一定使用

$$
k=\min(|prices|,|discounts|)
$$

张折扣，并选择最大的 $k$ 个价格与最大的 $k$ 个折扣。

真正需要证明的是配对顺序。若 $p\ge q$ 且 $d\ge e$，同序配对相对交叉配对多出的节省为

$$
(pd+qe)-(pe+qd)=(p-q)(d-e)\ge0.
$$

因此消除所有逆序配对后，最大价格与最大折扣同序匹配最优。这是重排不等式的交换论证。

原价总和最大为 $10^{10}$。把全部金额先乘 100，最坏分子不超过 $10^{12}$，64 位整数安全；最后只除一次 100，可避免反复浮点乘加造成的误差。

## 解法递进

### 解法一：枚举折扣分配

对每张折扣选择“不用”或分配给一个尚未使用的商品，完整覆盖所有可行匹配。它只适合很小规模，是可靠 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> price;
  vector<int> discount;
  vector<int> used;
  long long best = 0;
  void search(int index, long long saving) {
    if (index == static_cast<int>(discount.size())) {
      best = max(best, saving);
      return;
    }
    search(index + 1, saving);
    for (int item = 0; item < static_cast<int>(price.size()); ++item) {
      if (used[item]) continue;
      used[item] = 1;
      search(index + 1, saving + 1LL * price[item] * discount[index]);
      used[item] = 0;
    }
  }
public:
  double minPrice(vector<int>& prices, vector<int>& discounts) {
    price = prices;
    discount = discounts;
    used.assign(prices.size(), 0);
    search(0, 0);
    long long numerator = 100LL * accumulate(prices.begin(), prices.end(), 0LL);
    return static_cast<double>(numerator - best) / 100.0;
  }
};
int main() {
  vector<int> prices{10, 30, 21};
  vector<int> discounts{50, 60};
  cout << fixed << setprecision(5) << Solution().minPrice(prices, discounts) << '\n';
}
```

最坏分支数为所有部分匹配的数量，呈指数增长；递归与占用标记空间 $O(n+m)$。$10^5$ 规模无法使用。

### 最佳实用解：降序排序并同序配对

将两个数组都降序排序，前 $k$ 项一一配对。用“原价的百分之一单位”计算精确分子。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double minPrice(vector<int>& prices, vector<int>& discounts) {
    sort(prices.begin(), prices.end(), greater<int>());
    sort(discounts.begin(), discounts.end(), greater<int>());
    long long numerator = 0;
    for (int price : prices) numerator += 100LL * price;
    int used = min(prices.size(), discounts.size());
    for (int i = 0; i < used; ++i) {
      numerator -= 1LL * prices[i] * discounts[i];
    }
    return static_cast<double>(numerator) / 100.0;
  }
};
int main() {
  vector<int> prices{10, 30, 21};
  vector<int> discounts{50, 60};
  cout << fixed << setprecision(5) << Solution().minPrice(prices, discounts) << '\n';
}
```

时间 $O(n\log n+m\log m)$；原地排序外，额外空间由排序实现决定，通常为 $O(\log n+\log m)$。

### 同阶之外的替代：利用值域计数

价格值域只有 $1\ldots10^5$，折扣值域只有 $1\ldots100$。分别统计频次，再用两个降序指针批量配对，可去掉比较排序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  double minPrice(vector<int>& prices, vector<int>& discounts) {
    array<int, 100001> priceCount{};
    array<int, 101> discountCount{};
    long long numerator = 0;
    for (int price : prices) {
      ++priceCount[price];
      numerator += 100LL * price;
    }
    for (int discount : discounts) ++discountCount[discount];
    int price = 100000;
    int discount = 100;
    while (price > 0 && discount > 0) {
      while (price > 0 && priceCount[price] == 0) --price;
      while (discount > 0 && discountCount[discount] == 0) --discount;
      if (price == 0 || discount == 0) break;
      int take = min(priceCount[price], discountCount[discount]);
      numerator -= 1LL * take * price * discount;
      priceCount[price] -= take;
      discountCount[discount] -= take;
    }
    return static_cast<double>(numerator) / 100.0;
  }
};
int main() {
  vector<int> prices{100, 70};
  vector<int> discounts{10, 40, 50};
  cout << fixed << setprecision(5) << Solution().minPrice(prices, discounts) << '\n';
}
```

时间 $O(n+m+10^5)$，频次数组空间 $O(10^5)$。它渐近更快，但排序解更短、更通用，面试中通常更稳。

## 正确性证明

先证明选择集合。若一个已选价格 $q$ 小于未选价格 $p$，把同一正折扣从 $q$ 换到 $p$ 会增加节省；故必须选择最大的 $k$ 个价格。折扣同理，必须选择最大的 $k$ 个折扣。由于每个折扣都为正，少用一张时把任一剩余折扣给任一剩余商品会严格降低总价，故恰使用 $k$ 张。

再证明配对。若当前存在逆序：$p\ge q$ 却给 $p$ 较小折扣 $e$、给 $q$ 较大折扣 $d$，交换后节省不减，因为差值为 $(p-q)(d-e)\ge0$。不断交换可消除全部逆序，得到两个降序序列逐项配对。因此算法取得最大节省，也就取得最低总价。

## 样例手推与边界

样例 1 降序后价格为 `[30,21,10]`，折扣为 `[60,50]`。原价分子为 6100，节省分子为 $30\times60+21\times50=2850$，剩余 3250，除以 100 得 32.5。

- 折扣多于商品：只使用最大的 $n$ 张折扣。
- 商品多于折扣：只有最大的 $m$ 个价格享受折扣。
- 100% 折扣：对应商品支付 0，整数分子仍正确。
- 相同价格或相同折扣：交换差为 0，任意同值顺序均最优。
- 所有输入均为正，所以原题不存在“某张折扣最好不用”的反例。

## 方案比较与推荐

枚举分配直接对应定义，适合作为小规模对拍；排序贪心的交换证明短、实现稳定、对值域变化不敏感；计数值域解更快，却依赖两个明确上界。竞赛与面试优先记“最小总价改写为最大节省，再用同序配对的交换论证”，只有性能实测要求时才切换计数数组。

## 易错点

- 最大折扣应匹配最大价格，而不是为了“平均”而交叉匹配。
- 不能只排序折扣而保持原价格顺序。
- 每张折扣和每件商品均至多使用一次。
- 题目明确不舍入；不要逐件转换成整数金额。
- 用 `int` 累加原价会溢出，应从第一步就使用 `long long`。
- 4014 是公开题号；竞赛接口中的其他内部标识不能写进邮件主题或题目索引。

## 可复现验证

三种完整实现均以 C++23 严格编译，官方样例得到 32.5、92、3。本轮固定种子生成 10,000 组 $1\le n,m\le8$、价格 1 至 50、折扣 1 至 100 的实例，排序贪心和计数值域解都与枚举全部部分匹配的精确 oracle 一致，零处不符；另用长度 $10^5$ 的极值数组核对 64 位分子安全。

## 变种一：恢复每张折扣分配给哪件商品

排序时保留原下标；前 $k$ 项同序配对即可恢复一组最优方案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Result {
  double total;
  vector<pair<int, int>> assignment;
};
Result minimumWithAssignment(const vector<int>& prices,
  const vector<int>& discounts) {
  vector<pair<int, int>> items;
  vector<pair<int, int>> coupons;
  for (int i = 0; i < static_cast<int>(prices.size()); ++i) {
    items.push_back({prices[i], i});
  }
  for (int i = 0; i < static_cast<int>(discounts.size()); ++i) {
    coupons.push_back({discounts[i], i});
  }
  sort(items.rbegin(), items.rend());
  sort(coupons.rbegin(), coupons.rend());
  long long numerator = 100LL * accumulate(prices.begin(), prices.end(), 0LL);
  vector<pair<int, int>> assignment;
  int used = min(items.size(), coupons.size());
  for (int i = 0; i < used; ++i) {
    numerator -= 1LL * items[i].first * coupons[i].first;
    assignment.push_back({coupons[i].second, items[i].second});
  }
  return {static_cast<double>(numerator) / 100.0, assignment};
}
int main() {
  vector<int> prices{10, 30, 21};
  vector<int> discounts{50, 60};
  Result result = minimumWithAssignment(prices, discounts);
  cout << result.total << ' ' << result.assignment.size() << '\n';
}
```

时间与排序解相同，额外空间 $O(n+m)$；同值时下标顺序只决定返回哪一组等价最优方案。

## 变种二：折扣可能为零或负数，且使用可选

零折扣无收益，负折扣会加价；只保留正折扣，再与最大价格同序配对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
double minimumPrice(vector<int> prices, vector<int> discounts) {
  discounts.erase(remove_if(discounts.begin(), discounts.end(),
                            [](int value) { return value <= 0; }),
                  discounts.end());
  sort(prices.rbegin(), prices.rend());
  sort(discounts.rbegin(), discounts.rend());
  long long numerator = 100LL * accumulate(prices.begin(), prices.end(), 0LL);
  int used = min(prices.size(), discounts.size());
  for (int i = 0; i < used; ++i) {
    numerator -= 1LL * prices[i] * discounts[i];
  }
  return static_cast<double>(numerator) / 100.0;
}
int main() {
  vector<int> prices{20, 10};
  vector<int> discounts{-30, 0, 50};
  cout << minimumPrice(prices, discounts) << '\n';
}
```

时间 $O(n\log n+m\log m)$，空间取决于排序；原题“全部折扣为正”的使用数量结论在此不再直接成立。

## 变种三：每种折扣有可使用次数

输入不同折扣值及其容量。价格降序后，从最大正折扣起按容量批量消费，无须展开巨大的重复折扣数组。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
double minimumPrice(vector<int> prices, vector<pair<int, long long>> coupons) {
  sort(prices.rbegin(), prices.rend());
  sort(coupons.rbegin(), coupons.rend());
  long long numerator = 100LL * accumulate(prices.begin(), prices.end(), 0LL);
  int item = 0;
  for (auto [discount, capacity] : coupons) {
    if (discount <= 0) break;
    while (capacity > 0 && item < static_cast<int>(prices.size())) {
      numerator -= 1LL * prices[item] * discount;
      ++item;
      --capacity;
    }
    if (item == static_cast<int>(prices.size())) break;
  }
  return static_cast<double>(numerator) / 100.0;
}
int main() {
  vector<int> prices{100, 70, 20};
  vector<pair<int, long long>> coupons{{50, 2}, {10, 1000000}};
  cout << minimumPrice(prices, coupons) << '\n';
}
```

时间 $O(n\log n+q\log q+n)$，空间由排序决定；容量总和再大也只处理至多 $n$ 次实际分配。

## 变种四：每张折扣只允许用于指定商品

同序交换可能产生不合法配对，原贪心失效。若商品数不超过 20，可用位掩码记录已占用商品，逐张折扣做“跳过或分配”的动态规划。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
double minimumEligible(const vector<int>& prices, const vector<int>& discounts,
  const vector<vector<int>>& allowed) {
  int n = static_cast<int>(prices.size());
  const long long negative = -(1LL << 60);
  vector<long long> dp(1 << n, negative);
  dp[0] = 0;
  for (int coupon = 0; coupon < static_cast<int>(discounts.size()); ++coupon) {
    vector<long long> next = dp;
    for (int mask = 0; mask < (1 << n); ++mask) {
      if (dp[mask] == negative) continue;
      for (int item = 0; item < n; ++item) {
        if ((mask >> item & 1) || !allowed[coupon][item]) continue;
        int newMask = mask | (1 << item);
        long long saving = 1LL * prices[item] * discounts[coupon];
        next[newMask] = max(next[newMask], dp[mask] + saving);
      }
    }
    dp.swap(next);
  }
  long long best = *max_element(dp.begin(), dp.end());
  long long numerator = 100LL * accumulate(prices.begin(), prices.end(), 0LL);
  return static_cast<double>(numerator - best) / 100.0;
}
int main() {
  vector<int> prices{100, 70};
  vector<int> discounts{50, 40};
  vector<vector<int>> allowed{{0, 1}, {1, 1}};
  cout << minimumEligible(prices, discounts, allowed) << '\n';
}
```

时间 $O(mn2^n)$，空间 $O(2^n)$；大规模稀疏版本应改为最大权匹配或最小费用流。

## 变种五：任意“折扣—商品”节省矩阵

若节省不再可分解为 `price*discount`，交换论证彻底失效。把不分配建模为权重 0 的虚拟点，用 Hungarian 算法求最大权可选匹配。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long maximumOptionalSaving(const vector<vector<long long>>& saving) {
  int rows = static_cast<int>(saving.size());
  int columns = rows == 0 ? 0 : static_cast<int>(saving[0].size());
  int size = rows + columns;
  if (size == 0) return 0;
  vector<vector<long long>> cost(size, vector<long long>(size));
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) cost[i][j] = -max(0LL, saving[i][j]);
  }
  vector<long long> u(size + 1), v(size + 1);
  vector<int> matched(size + 1), way(size + 1);
  for (int row = 1; row <= size; ++row) {
    matched[0] = row;
    int column = 0;
    vector<long long> minimum(size + 1, (1LL << 60));
    vector<char> used(size + 1);
    do {
      used[column] = true;
      int currentRow = matched[column];
      long long delta = 1LL << 60;
      int nextColumn = 0;
      for (int candidate = 1; candidate <= size; ++candidate) {
        if (used[candidate]) continue;
        long long current = cost[currentRow - 1][candidate - 1] -
                            u[currentRow] - v[candidate];
        if (current < minimum[candidate]) {
          minimum[candidate] = current;
          way[candidate] = column;
        }
        if (minimum[candidate] < delta) {
          delta = minimum[candidate];
          nextColumn = candidate;
        }
      }
      for (int candidate = 0; candidate <= size; ++candidate) {
        if (used[candidate]) {
          u[matched[candidate]] += delta;
          v[candidate] -= delta;
        } else {
          minimum[candidate] -= delta;
        }
      }
      column = nextColumn;
    } while (matched[column] != 0);
    do {
      int previous = way[column];
      matched[column] = matched[previous];
      column = previous;
    } while (column != 0);
  }
  long long answer = 0;
  for (int column = 1; column <= size; ++column) {
    int row = matched[column] - 1;
    int item = column - 1;
    if (row < rows && item < columns) answer += max(0LL, saving[row][item]);
  }
  return answer;
}
int main() {
  vector<vector<long long>> saving{{8, 1}, {7, 6}};
  cout << maximumOptionalSaving(saving) << '\n';
}
```

令 $N=n+m$，时间 $O(N^3)$，空间 $O(N^2)$。虚拟行列使任何真实折扣或商品都可保持未匹配。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-134-lc509/">← [力扣 Top 134] LC 509 斐波那契数 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-c/">[codeforces] CF Round 1116 Div.1 A / Div.2 C Hot Potatoes at the Fairy Warehouse →</a>
</nav>
