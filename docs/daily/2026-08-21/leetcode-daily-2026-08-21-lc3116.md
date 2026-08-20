---
title: "[力扣每日一题] 2026-08-21｜LC 3116 单面值组合的第 K 小金额"
---

# [力扣每日一题] 2026-08-21｜LC 3116 单面值组合的第 K 小金额

<p class="daily-archive-kicker">2026-08-21 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-21 题目列表</a> · <a href="../../../basics/binary-search/#inclusion-exclusion-count">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0c6b86afcc40175c7581a2608437da452eb9ecb527f434ff15cfa9a05c5f31dd -->
[力扣官方题目：3116. 单面值组合的第 K 小金额](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/)

## 官方原始信息

- 北京时间每日一题日期：2026-08-21；题号：LC 3116。
- 官方中文标题：单面值组合的第 K 小金额；官方难度：困难。
- 官方链接：[https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/)
- 函数签名：`long long findKthSmallest(vector<int>& coins, int k)`。
- 原竞赛：第 393 场周赛 Q3；官方竞赛分值：6 分。
- ZeroTracer 社区估算竞赛分：2387.93，抓取于 2026-08-21；这不是力扣官方难度或分值。
- 官方标签：位运算、数组、数学、二分查找、组合数学、数论。

### 原始题意

给定两两不同的硬币面额数组 `coins` 和整数 `k`。每种面额有无限枚，但一次金额只能使用同一
种面额，不能混用不同面额。把所有能得到的正金额去重并升序排列，返回第 `k` 小金额。

### 全部官方样例

```text
示例 1
输入：coins = [3,6,9], k = 3
输出：9
解释：去重后的金额依次为 3, 6, 9, 12, 15, ...。

示例 2
输入：coins = [5,2], k = 7
输出：12
解释：去重后的金额依次为 2, 4, 5, 6, 8, 10, 12, 14, 15, ...。
```

### 全部约束

- $1\le coins.length\le15$。
- $1\le coins[i]\le25$。
- $1\le k\le2\times10^9$。
- `coins` 中的整数两两不同。

## 最优结论摘要

答案 $x$ 具有单调判定：不超过 $x$ 的合法金额数至少为 $k$。合法集合是各面额倍数集合的
并集，用最小公倍数上的容斥计算其大小：

$$
count(x)=\sum_{\varnothing\ne T\subseteq coins}
(-1)^{|T|+1}\left\lfloor\frac{x}{\operatorname{lcm}(T)}\right\rfloor.
$$

先删去被更小面额整除的冗余面额，再预聚合同一 LCM 的系数，最后在
$[1,\min(coins)\cdot k]$ 二分。复杂度约为
$O(2^m m+U\log(\min(coins)k))$，其中 $m\le15$，$U$ 是不同有效 LCM 数。

## 约束与观察

- `k` 可达 $2\times10^9$，不能逐个生成金额；但面额数最多 15，允许枚举面额子集。
- “不能混用面额”意味着合法金额是“至少被一个面额整除”，不是零钱兑换的可达和。
- 若 $a\mid b$，所有 $b$ 的倍数已经是 $a$ 的倍数，面额 $b$ 对并集没有贡献，可删除。
- 最小面额的前 $k$ 个倍数保证区间上界 `minCoin * k` 内至少有 $k$ 个合法金额。
- 上界最大为 $25\times2\times10^9=5\times10^{10}$，返回值和 LCM 都必须用 `long long`。
- 计算 LCM 前先判断 `lcm > limit / factor`，避免先乘后溢出。

## 样例手推与边界

样例 1 中 6 和 9 都是 3 的倍数，因此删去后只剩面额 3，第 3 个倍数就是 9。

样例 2 对 $x=12$：2 的倍数有 6 个，5 的倍数有 2 个，同时为两者倍数的 10 的倍数有 1 个，
所以 $count(12)=6+2-1=7$；而 $count(11)=5+2-1=6$，故第 7 小金额恰为 12。

单面额时答案直接是 `coins[0] * k`。若面额含 1，所有正整数都合法，答案就是 $k$。

## 解法一：最小堆归并所有倍数序列

每个面额产生一条递增序列 $c,2c,3c,\ldots$。把每条序列首项放入最小堆，每次取最小值并
推进对应序列；相同值只增加一次排名。时间 $O(R\log m)$，其中 $R$ 至少为 $k$ 且可能因
重复更大，正式约束不可行，但它是可靠的小规模 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long findKthSmallest(vector<int>& coins, int k) {
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> heap;
    for (int i = 0; i < static_cast<int>(coins.size()); ++i) {
      heap.push({coins[i], i});
    }
    long long previous = -1;
    int rank = 0;
    while (!heap.empty()) {
      auto [value, index] = heap.top();
      heap.pop();
      if (value != previous) {
        previous = value;
        if (++rank == k) return value;
      }
      heap.push({value + coins[index], index});
    }
    return -1;
  }
};
```

## 解法二：二分答案 + 每次枚举全部子集容斥

对固定 `limit`，每个非空面额子集的交集是其 LCM 的倍数集合。按子集大小奇加偶减，就能
准确消除重复。判定函数随 `limit` 单调不减，因此二分第一个 `count(limit) >= k` 的位置。

每次判定重新计算全部子集 LCM，时间
$O(2^m m\log(min(coins)k))$，空间 $O(1)$。这已能通过约束，但还可预计算 LCM 系数。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long findKthSmallest(vector<int>& coins, int k) {
    long long low = 1;
    long long high = 1LL * *min_element(coins.begin(), coins.end()) * k;
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      int m = coins.size();
      for (int mask = 1; mask < (1 << m); ++mask) {
        long long multiple = 1;
        bool tooLarge = false;
        for (int i = 0; i < m; ++i) {
          if (((mask >> i) & 1) == 0) continue;
          long long factor = coins[i] / gcd(multiple, 1LL * coins[i]);
          if (multiple > limit / factor) {
            tooLarge = true;
            break;
          }
          multiple *= factor;
        }
        if (tooLarge) continue;
        if (__builtin_popcount(mask) & 1) {
          total += limit / multiple;
        } else {
          total -= limit / multiple;
        }
      }
      return total;
    };
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) {
        high = middle;
      } else {
        low = middle + 1;
      }
    }
    return low;
  }
};
```

## 从重复容斥到系数预聚合

先排序面额。若当前面额能被某个已保留的更小面额整除，它对倍数并集没有新增元素，直接跳过。
然后只枚举一次子集，把相同 LCM 的容斥符号累加到映射 `coefficient[lcm]`。某些不同子集可能
得到同一 LCM；预聚合既减少每次判定的工作，也避免反复求 gcd。

只保留不超过二分上界的 LCM：更大的 LCM 在整个搜索区间内贡献始终为 0。

## 最佳实用解：冗余消除、LCM 系数与二分

### 正确性证明

**引理 1**：删除被较小面额整除的面额不改变合法金额集合。

若 $a\mid b$，每个 $b$ 的倍数也是 $a$ 的倍数；删除 $b$ 不会删除并集中的任何元素。

**引理 2**：`countAtMost(x)` 等于不超过 $x$ 的不同合法金额数。

每个面额定义一个倍数集合。任意非空子集的交集恰是其 LCM 的倍数，大小为
$\lfloor x/\operatorname{lcm}\rfloor$。有限集合的容斥原理给出公式；合并相同 LCM 只是在
重排同一总和。

**引理 3**：二分区间包含答案，判定单调。

集合计数随 $x$ 增大不减。最小面额的 $k$ 个倍数均不超过 `minCoin * k`，所以上界判定为真；
下界从 1 开始。标准“第一个为真”二分返回最小满足计数至少 $k$ 的金额，也就是第 $k$ 小值。

由三个引理，算法正确。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long findKthSmallest(vector<int>& coins, int k) {
    sort(coins.begin(), coins.end());
    vector<int> base;
    for (int coin : coins) {
      bool redundant = false;
      for (int smaller : base) {
        if (coin % smaller == 0) redundant = true;
      }
      if (!redundant) base.push_back(coin);
    }
    long long high = 1LL * base[0] * k;
    map<long long, int> coefficient;
    int m = base.size();
    for (int mask = 1; mask < (1 << m); ++mask) {
      long long multiple = 1;
      bool tooLarge = false;
      for (int i = 0; i < m; ++i) {
        if (((mask >> i) & 1) == 0) continue;
        long long factor = base[i] / gcd(multiple, 1LL * base[i]);
        if (multiple > high / factor) {
          tooLarge = true;
          break;
        }
        multiple *= factor;
      }
      if (tooLarge) continue;
      coefficient[multiple] += (__builtin_popcount(mask) & 1) ? 1 : -1;
    }
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      for (auto [multiple, sign] : coefficient) {
        total += sign * (limit / multiple);
      }
      return total;
    };
    long long low = 1;
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) {
        high = middle;
      } else {
        low = middle + 1;
      }
    }
    return low;
  }
};
```

最坏预处理 $O(2^m m)$，每次判定 $O(U)$，二分次数不超过 36；空间 $O(U)$。这里
$U\le2^m-1$，而冗余删除通常会显著减小 $m$。

## 同阶方案比较

可以在每次判定中 DFS 生成 LCM，并在超过 `limit` 时剪枝，代码更短；预聚合版本把与二分点
无关的 gcd/LCM 工作只做一次，性能更稳定，也自然合并相同交集。竞赛中推荐记忆“二分 +
LCM 容斥”，实现时根据面额数选择 DFS 或预聚合。

## 易错点

- 金额集合要去重；直接相加 `x / coin` 会把公倍数重复计算。
- 题意禁止混用不同面额，不能套完全背包或零钱兑换。
- 容斥符号是奇数大小子集加、偶数大小子集减。
- LCM 不能先乘再判断溢出；要先除以 gcd，并用除法比较上界。
- 二分上界要用 `long long`，`25 * 2e9` 已超过 32 位有符号整数。
- 删除冗余面额必须在排序后检查“是否被更小保留值整除”，方向不能写反。

## 验证说明

所有代码块均通过 C++23 语法编译。最佳解已对随机面额子集和小 `k` 与最小堆归并逐项对拍，
覆盖单面额、面额 1、整除链、两两互质、LCM 超上界、最大 `k` 的 64 位边界和全部官方样例。

## 变种一：重复金额按产生序列的重数计数

新定义：金额 10 若既是面额 2 的倍数又是面额 5 的倍数，就出现两次。此时不再求集合并集，
计数直接是 $\sum\lfloor x/c\rfloor$；二分复杂度 $O(m\log(min(coins)k))$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long kthWithMultiplicity(const vector<int>& coins, long long k) {
    long long low = 1;
    long long high = 1LL * *min_element(coins.begin(), coins.end()) * k;
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      for (int coin : coins) {
        total += limit / coin;
        if (total >= k) return k;
      }
      return total;
    };
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) high = middle;
      else low = middle + 1;
    }
    return low;
  }
};
```

## 变种二：只统计恰好能由一种面额产生的金额

新定义：金额必须被恰好一个面额整除。若一个数被 $r$ 个面额整除，则大小为 $s$ 的交集子集
共有 $\binom rs$ 个；权重改为 $s(-1)^{s-1}$ 后，所有 $r>1$ 的贡献抵消，$r=1$ 留下 1。
因此仍可二分，判定复杂度 $O(2^m m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long kthDivisibleByExactlyOne(vector<int> coins, long long k) {
    long long low = 1;
    long long high = 1LL * *min_element(coins.begin(), coins.end()) * k * coins.size();
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      int m = coins.size();
      for (int mask = 1; mask < (1 << m); ++mask) {
        long long multiple = 1;
        bool tooLarge = false;
        for (int i = 0; i < m; ++i) {
          if (((mask >> i) & 1) == 0) continue;
          long long factor = coins[i] / gcd(multiple, 1LL * coins[i]);
          if (multiple > limit / factor) {
            tooLarge = true;
            break;
          }
          multiple *= factor;
        }
        if (tooLarge) continue;
        int size = __builtin_popcount(mask);
        long long contribution = 1LL * size * (limit / multiple);
        total += (size & 1) ? contribution : -contribution;
      }
      return total;
    };
    while (countAtMost(high) < k) high *= 2;
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) high = middle;
      else low = middle + 1;
    }
    return low;
  }
};
```

## 变种三：允许混用不同面额

新定义：金额可由任意多枚、任意面额硬币相加。原来的“倍数集合并集”彻底失效。令最小面额
为 $b$，在模 $b$ 的余数图上用 Dijkstra 求每个余数的最小可达金额 `dist[r]`。此后同余且
不小于 `dist[r]` 的金额都可再加若干个 $b$ 得到。计数后仍可二分，复杂度
$O(bm\log b+b\log(bk))$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long kthAmountWithMixedCoins(vector<int> coins, long long k) {
    int base = *min_element(coins.begin(), coins.end());
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<long long> distance(base, infinity);
    using State = pair<long long, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    distance[0] = 0;
    heap.push({0, 0});
    while (!heap.empty()) {
      auto [value, residue] = heap.top();
      heap.pop();
      if (value != distance[residue]) continue;
      for (int coin : coins) {
        int next = (residue + coin) % base;
        if (value + coin >= distance[next]) continue;
        distance[next] = value + coin;
        heap.push({distance[next], next});
      }
    }
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      for (long long first : distance) {
        if (first > limit) continue;
        total += (limit - first) / base + 1;
      }
      return total - 1;
    };
    long long low = 1;
    long long high = 1LL * base * k;
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) high = middle;
      else low = middle + 1;
    }
    return low;
  }
};
```

## 变种四：同时返回能产生第 k 小金额的面额

新定义：返回答案和所有能单独产生该金额的原始面额。先用原算法找到金额 $x$，再筛选
`x % coin == 0`；这不会改变二分复杂度，额外只需 $O(m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<long long, vector<int>> kthAmountWithWitnesses(
      const vector<int>& coins, int k) {
    long long low = 1;
    long long high = 1LL * *min_element(coins.begin(), coins.end()) * k;
    auto countAtMost = [&](long long limit) {
      long long total = 0;
      int m = coins.size();
      for (int mask = 1; mask < (1 << m); ++mask) {
        long long multiple = 1;
        bool tooLarge = false;
        for (int i = 0; i < m; ++i) {
          if (((mask >> i) & 1) == 0) continue;
          long long factor = coins[i] / gcd(multiple, 1LL * coins[i]);
          if (multiple > limit / factor) {
            tooLarge = true;
            break;
          }
          multiple *= factor;
        }
        if (tooLarge) continue;
        if (__builtin_popcount(mask) & 1) total += limit / multiple;
        else total -= limit / multiple;
      }
      return total;
    };
    while (low < high) {
      long long middle = low + (high - low) / 2;
      if (countAtMost(middle) >= k) high = middle;
      else low = middle + 1;
    }
    vector<int> witnesses;
    for (int coin : coins) {
      if (low % coin == 0) witnesses.push_back(coin);
    }
    return {low, witnesses};
  }
};
```

## 推荐记忆

把问题拆成两层：外层是“第 k 小”常用的单调二分，内层是“至少被一个面额整除”的集合并集
计数。内层的交集由 LCM 描述，因此自然落到容斥；LCM 溢出保护和冗余面额删除是实现稳定性
的关键。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/)
- [对应知识专题](../../basics/binary-search.md#inclusion-exclusion-count)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-d/">← [codeforces] CF Round 1117 Div.2 D Bermuda Rectangle</a>
<span class="daily-archive-pager__empty"></span>
</nav>
