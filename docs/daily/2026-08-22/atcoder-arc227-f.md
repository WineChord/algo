---
title: "[atcoder] ARC227 F Erase and Raise"
---

# [atcoder] ARC227 F Erase and Raise

<p class="daily-archive-kicker">2026-08-22 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-22 题目列表</a> · <a href="../../../math/combinatorial-counting/#active-gap-budget-dp">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=1070e56a59d3ce284c546a3a391f2dab2b6fa4ca8d8162d0a4d865cba04e0d26 -->
[Official problem: ARC227 F — Erase and Raise](https://atcoder.jp/contests/arc227/tasks/arc227_f?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227），比赛时长 120 分钟，rated 范围为 1200–2799。
- 题目：F — Erase and Raise；任务 slug 为 `arc227_f`。
- 官方分值：800 分；AtCoder 未发布单题官方难度。
- AtCoder Problems 社区估算难度：3159，抓取于 2026-08-22；这不是 AtCoder 官方难度。
- 时间限制：5 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en) 仍是权威来源。

## Complete English statement

There is an integer sequence $A=(0,0,\ldots,0)$ of length $N$. Repeatedly perform the following
operation for as long as some valid pair exists:

1. Choose indices $i,j$ with $1\le i<j\le |A|$ and $A_i=A_j$.
2. Remove $A_i$ and $A_j$ from the sequence.
3. Add $1$ to every element that lay strictly between those two elements immediately before their
   removal.

Here, $|A|$ is the current length of the sequence. The choices of pairs may lead to different
terminal sequences. Count the distinct sequences that can remain when no valid operation is possible,
modulo $998244353$. Two equal final sequences are counted once even if obtained by different operation
histories. The empty sequence is also one valid terminal sequence.

### Input

```text
N
```

### Output

Print the number of distinct possible terminal sequences modulo $998244353$.

### Constraints

- $1\le N\le2\times10^5$.
- Every input value is an integer.

### Official samples

Sample 1 input:

```text
1
```

Sample 1 output:

```text
1
```

No operation is possible, so the only terminal sequence is $(0)$.

Sample 2 input:

```text
5
```

Sample 2 output:

```text
3
```

The three terminal sequences are $(0)$, $(1)$, and $(2)$.

Sample 3 input:

```text
7
```

Sample 3 output:

```text
8
```

Eight different terminal sequences can be obtained.

Sample 4 input:

```text
200000
```

Sample 4 output:

```text
159211719
```

The answer is taken modulo $998244353$.

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/arc227/tasks/arc227_f?lang=en) remains normative;
reuse is subject to the [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en).

## 中文解释与结论摘要

设终态为非负整数序列 $B=(B_1,\ldots,B_M)$，并补 $B_0=B_{M+1}=0$。终态可达当且仅当：

1. $M\equiv N\pmod2$；
2. 所有 $B_i$ 两两不同；
3. $C(B)=M+\sum_{i=0}^{M}|B_i-B_{i+1}|\le N$。

第三个量可理解为“留下每个元素花 1 个长度预算，再为相邻值之间跨过的每一层付费”。按
数值从小到大插入终态元素，并维护仍会放入更大值的活跃间隙数 `gaps`，就能逐层累计这个
预算。跳过一个值增加 `2 * gaps`；把当前值插入某个活跃间隙后，新活跃间隙可以有 0、1、2
个。预算至多 $N$ 又迫使 `gaps` 只有 $O(\sqrt N)$，得到 $O(N\sqrt N)$ 时间和
$O(N\sqrt N)$ 空间的计数 DP。

## 约束推导、溢出与边界

- 一次操作删去两个元素，故终态长度与 $N$ 同奇偶；空序列只在 $N$ 为偶数时可达。
- 终态不能有相等元素，否则仍能操作；这也是按值每次至多插入一个元素的原因。
- $N=2\times10^5$，不能枚举操作序列、终态排列或所有不同值集合。
- 若活跃间隙从 1 增至 $g$，最省预算也至少为
  $5+7+\cdots+(2g+1)=g^2+2g-3$，所以 $g=O(\sqrt N)$。
- 方案数用 `int` 存模值，乘以间隙选择数时先提升为 `long long`。
- $N=1$ 时只有 `(0)`；$N=2$ 时只有空序列；这两个边界同时检查长度奇偶与空序列。

## 样例与状态手推

以 $N=5$ 为例。非空构造从一个活跃间隙开始。若插入值 0 后不保留活跃子间隙，预算为 1，
得到 `(0)`；先跳过 0 要花 2，再插入值 1 花 1，预算为 3，得到 `(1)`；再跳过 1 多花 2，
插入值 2 后预算为 5，得到 `(2)`。更大单元素值预算超过 5；多元素终态要满足奇数长度，最小
三元素预算也超过 5。因此正好有三个终态。

## 解法一：完整枚举可达状态

当 $N\le12$ 时，从全零序列出发，枚举每一对相等元素，生成下一状态并递归；没有后继的状态
加入集合去重。这是定义级别的正确暴力，状态数与分支数均呈指数增长，只适合作为 oracle。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
map<vector<int>, set<vector<int>>> memo;
const set<vector<int>>& terminals(const vector<int>& sequence) {
  auto found = memo.find(sequence);
  if (found != memo.end()) return found->second;
  set<vector<int>> answer;
  bool moved = false;
  for (int left = 0; left < static_cast<int>(sequence.size()); ++left) {
    for (int right = left + 1; right < static_cast<int>(sequence.size()); ++right) {
      if (sequence[left] != sequence[right]) continue;
      moved = true;
      vector<int> next;
      for (int i = 0; i < left; ++i) next.push_back(sequence[i]);
      for (int i = left + 1; i < right; ++i) next.push_back(sequence[i] + 1);
      for (int i = right + 1; i < static_cast<int>(sequence.size()); ++i) {
        next.push_back(sequence[i]);
      }
      const auto& child = terminals(next);
      answer.insert(child.begin(), child.end());
    }
  }
  if (!moved) answer.insert(sequence);
  return memo.emplace(sequence, move(answer)).first->second;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  if (n > 12) return 0;
  cout << terminals(vector<int>(n)).size() << '\n';
  return 0;
}
```

## 可达性刻画

一次操作不会增大

$$
|A|+\sum_{i=0}^{|A|}|A_i-A_{i+1}|,
$$

其中两端补 0；初态该值为 $N$。终态还必须两两不同且长度同奇偶，所以三项条件必要。

反过来，从满足条件的非负序列 $B$ 出发，对每一层依次处理当前所有极大的正值连续块：在块的
两端各插入一个 0，并把整块元素减 1。每个块正好是原折线跨过这一高度层的一段正区域；处理完
全部高度层后，所有元素都变成 0，插入的元素数恰为
$\sum|B_i-B_{i+1}|$。于是得到长度恰为 $C(B)$ 的全零序列。若 $C(B)<N$，因总变差为偶数且
$|B|\equiv N\pmod2$，差值也是偶数，可继续插入相邻零对补到长度 $N$。逆转这些步骤即可从
初态得到 $B$，故条件也充分。

## 解法二：不利用间隙上界的预算 DP

把终态的值按 $0,1,2,\ldots$ 依次考虑。当前已有较小值时，`gaps` 表示最终还会放入至少一个
更大值的间隙数。

- 不选当前值：跨过这一数值层，每个活跃间隙产生两条跨层边，预算增加 `2 * gaps`。
- 选当前值：先从 `gaps` 个活跃间隙中选一个插入。该间隙被拆成左右两个，新活跃子间隙数可
  为 0、1、2，对应新状态 `gaps - 1`、`gaps`、`gaps + 1`；选择数分别为 `gaps`、
  `2 * gaps`、`gaps`。元素自身花 1，再为新活跃间隙跨到下一层花 `2 * nextGaps`。

直接让 `gaps` 扫到 $N$ 是 $O(N^2)$ 状态。下面版本只适合 `N <= 3000`，但已经消除了终态
和值域枚举。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MOD = 998244353;
void addMod(int& target, long long value) {
  target = (target + value) % MOD;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  if (n > 3000) return 0;
  vector<vector<int>> dp(n + 1, vector<int>(n + 2));
  dp[0][1] = 1;
  for (int cost = 0; cost <= n; ++cost) {
    for (int gaps = 1; gaps <= n; ++gaps) {
      int ways = dp[cost][gaps];
      if (ways == 0) continue;
      if (cost + 2 * gaps <= n) addMod(dp[cost + 2 * gaps][gaps], ways);
      for (int children = 0; children <= 2; ++children) {
        int nextGaps = gaps - 1 + children;
        int nextCost = cost + 1 + 2 * nextGaps;
        if (nextCost > n) continue;
        long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
        addMod(dp[nextCost][nextGaps], choices * ways);
      }
    }
  }
  int answer = n % 2 == 0;
  for (int cost = n % 2; cost <= n; cost += 2) addMod(answer, dp[cost][0]);
  cout << answer << '\n';
  return 0;
}
```

## 从平方状态到根号间隙

从 1 个活跃间隙增长到 $g$ 个，必须依次做 $1\to2\to\cdots\to g$。增长到新间隙数 $q$
的最小增量是 $1+2q$，故到达 $g$ 前至少花费

$$
\sum_{q=2}^{g}(1+2q)=g^2+2g-3.
$$

只要这个下界超过 $N$，该间隙数就绝不可能出现。把第二维截到满足下界的最大 $g$，即把
状态从 $O(N^2)$ 压到 $O(N\sqrt N)$，转移完全不变。

## 最佳实用解：预算与活跃间隙 DP

### 正确性证明

**引理 1**：可达性三条件充要。

必要性来自长度奇偶、终态两两不同和势函数不增；充分性由上述逆操作构造得到。

**引理 2**：DP 的每条终止路径唯一对应一个两两不同的终态序列。

按值递增时，每个值只可能插入一次。给定最终序列，当前值落在哪个活跃间隙、其左右哪一侧
仍含更大值都被最终相对顺序唯一确定；反之，所有插入选择唯一确定最终排列，因此没有遗漏或
重复。

**引理 3**：DP 的 `cost` 恰为 $C(B)$。

每次插入为长度项贡献 1。对任意整数层 $x$，活跃间隙恰对应最终序列中从不大于 $x$ 的元素
跨到大于 $x$ 的相邻边；每个活跃间隙贡献左右两次跨层，因此增加 `2 * gaps`。跨所有层累加
正是总变差。

终止状态 `gaps = 0` 枚举了所有两两不同序列的精确最小预算。只累加不超过 $N$ 且与 $N$
同奇偶的预算，并单独加入偶数 $N$ 的空序列，依据引理 1 得到全部且仅有可达终态。根号截断
只删除预算已超过 $N$ 的不可能状态，所以算法正确。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MOD = 998244353;
void addMod(int& target, long long value) {
  target = (target + value) % MOD;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  int gapLimit = 1;
  while (1LL * (gapLimit + 1) * (gapLimit + 1) +
      2LL * (gapLimit + 1) - 3 <= n) {
    ++gapLimit;
  }
  vector<vector<int>> dp(n + 1, vector<int>(gapLimit + 2));
  dp[0][1] = 1;
  for (int cost = 0; cost <= n; ++cost) {
    for (int gaps = 1; gaps <= gapLimit; ++gaps) {
      int ways = dp[cost][gaps];
      if (ways == 0) continue;
      if (cost + 2 * gaps <= n) addMod(dp[cost + 2 * gaps][gaps], ways);
      for (int children = 0; children <= 2; ++children) {
        int nextGaps = gaps - 1 + children;
        int nextCost = cost + 1 + 2 * nextGaps;
        if (nextCost > n) continue;
        long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
        if (nextGaps <= gapLimit) addMod(dp[nextCost][nextGaps], choices * ways);
      }
    }
  }
  int answer = n % 2 == 0;
  for (int cost = n % 2; cost <= n; cost += 2) addMod(answer, dp[cost][0]);
  cout << answer << '\n';
  return 0;
}
```

时间复杂度 $O(N\sqrt N)$，空间复杂度 $O(N\sqrt N)$。

## 同阶方案比较与易错点

可以把二维表改成按预算分块的稀疏映射以减少小数据内存，但哈希和节点常数更大；本题 1024 MiB
内存允许紧凑整数表，连续存储更稳定。竞赛中推荐记忆“按值插入排列 + 活跃间隙 + 势函数
预算”的建模，而不是死记转移系数。

- 活跃间隙跨一个数值层贡献 2，不是 1。
- 插入后恰有一个子间隙活跃时，左右两种选择不同，系数为 `2 * gaps`。
- `gaps = 0` 已经终止，不能再执行零成本“跳过”形成无限自环。
- 空序列未经过 `dp[0][1]`，要在偶数 $N$ 时单独加入。
- 只判断 `cost <= N` 不够，还要满足长度奇偶；而 `cost` 与长度同奇偶，可直接按预算奇偶筛。

## 可复现验证

最佳代码以 GNU++23 编译，四个官方样例依次输出 `1`、`3`、`8`、`159211719`。另对
$N=1\ldots11$ 枚举全部真实操作状态，得到
`1,1,2,3,3,7,8,13,23,29,52`，与 DP 逐项一致；`N=200000` 的优化实现实测完成。

## Follow-up 与约束变种

### 变种一：判定指定终态并求最小初始长度

新定义：给定候选序列 `B`，求能生成它的最小全零初始长度，并判断给定 `N` 是否可达。直接
检查元素非负且互异，再计算 $C(B)$；最小长度就是 $C(B)$，给定 `N` 还需同奇偶。时间
$O(M\log M)$，空间 $O(M)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> b(m);
  for (long long& value : b) cin >> value;
  set<long long> distinct;
  bool valid = true;
  for (long long value : b) {
    if (value < 0 || !distinct.insert(value).second) valid = false;
  }
  if (!valid) {
    cout << -1 << " No\n";
    return 0;
  }
  long long minimum = m;
  long long previous = 0;
  for (long long value : b) {
    minimum += abs(value - previous);
    previous = value;
  }
  minimum += abs(previous);
  bool reachable = minimum <= n && (m % 2 == n % 2);
  cout << minimum << ' ' << (reachable ? "Yes" : "No") << '\n';
  return 0;
}
```

### 变种二：终态长度恰为 K

新定义：在 `N <= 500`、`K <= 50` 下，只统计长度恰为 `K` 的可达终态。原状态不能区分长度，
增加 `used` 维；跳过值不变，插入值时 `used + 1`。时间 $O(NK\sqrt N)$，空间同阶。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MOD = 998244353;
void addMod(int& target, long long value) {
  target = (target + value) % MOD;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, wanted;
  cin >> n >> wanted;
  int limit = sqrt(n) + 3;
  vector dp(n + 1, vector(limit + 2, vector<int>(wanted + 1)));
  dp[0][1][0] = 1;
  for (int cost = 0; cost <= n; ++cost) {
    for (int gaps = 1; gaps <= limit; ++gaps) {
      for (int used = 0; used <= wanted; ++used) {
        int ways = dp[cost][gaps][used];
        if (ways == 0) continue;
        if (cost + 2 * gaps <= n) {
          addMod(dp[cost + 2 * gaps][gaps][used], ways);
        }
        if (used == wanted) continue;
        for (int children = 0; children <= 2; ++children) {
          int nextGaps = gaps - 1 + children;
          int nextCost = cost + 1 + 2 * nextGaps;
          if (nextCost > n || nextGaps > limit) continue;
          long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
          addMod(dp[nextCost][nextGaps][used + 1], choices * ways);
        }
      }
    }
  }
  int answer = wanted == 0 && n % 2 == 0;
  if (wanted % 2 == n % 2) {
    for (int cost = n % 2; cost <= n; cost += 2) {
      addMod(answer, dp[cost][0][wanted]);
    }
  }
  cout << answer << '\n';
  return 0;
}
```

### 变种三：终态最大值不超过 H

新定义：`N,H <= 300`，只统计所有元素均不超过 `H` 的终态。压掉“当前数值”的技巧不再适用，
必须显式处理 `0..H` 共 `H+1` 层；处理完后只接受 `gaps=0`。时间
$O(HN\sqrt N)$，空间 $O(N\sqrt N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MOD = 998244353;
void addMod(int& target, long long value) {
  target = (target + value) % MOD;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, maximum;
  cin >> n >> maximum;
  int limit = sqrt(n) + 3;
  vector<vector<int>> dp(n + 1, vector<int>(limit + 2));
  dp[0][1] = 1;
  for (int value = 0; value <= maximum; ++value) {
    vector<vector<int>> next(n + 1, vector<int>(limit + 2));
    for (int cost = 0; cost <= n; ++cost) {
      addMod(next[cost][0], dp[cost][0]);
      for (int gaps = 1; gaps <= limit; ++gaps) {
        int ways = dp[cost][gaps];
        if (ways == 0) continue;
        if (cost + 2 * gaps <= n) addMod(next[cost + 2 * gaps][gaps], ways);
        for (int children = 0; children <= 2; ++children) {
          int nextGaps = gaps - 1 + children;
          int nextCost = cost + 1 + 2 * nextGaps;
          if (nextCost > n || nextGaps > limit) continue;
          long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
          addMod(next[nextCost][nextGaps], choices * ways);
        }
      }
    }
    dp.swap(next);
  }
  int answer = n % 2 == 0;
  for (int cost = n % 2; cost <= n; cost += 2) addMod(answer, dp[cost][0]);
  cout << answer << '\n';
  return 0;
}
```

### 变种四：终态所有值至少为 L

新定义：给定 $0\le L\le N$，只统计非空元素均满足 `B_i >= L` 的终态。值 `0..L-1` 必须全部跳过；初始只有一个
活跃间隙，所以先固定消耗 `2L`，再运行原压缩 DP。若 `2L > N`，除可能的空序列外没有答案。
复杂度仍为 $O(N\sqrt N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int MOD = 998244353;
void addMod(int& target, long long value) {
  target = (target + value) % MOD;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, minimumValue;
  cin >> n >> minimumValue;
  int limit = sqrt(n) + 3;
  vector<vector<int>> dp(n + 1, vector<int>(limit + 2));
  if (2LL * minimumValue <= n) dp[2 * minimumValue][1] = 1;
  for (int cost = 0; cost <= n; ++cost) {
    for (int gaps = 1; gaps <= limit; ++gaps) {
      int ways = dp[cost][gaps];
      if (ways == 0) continue;
      if (cost + 2 * gaps <= n) addMod(dp[cost + 2 * gaps][gaps], ways);
      for (int children = 0; children <= 2; ++children) {
        int nextGaps = gaps - 1 + children;
        int nextCost = cost + 1 + 2 * nextGaps;
        if (nextCost > n || nextGaps > limit) continue;
        long long choices = 1LL * gaps * (children == 1 ? 2 : 1);
        addMod(dp[nextCost][nextGaps], choices * ways);
      }
    }
  }
  int answer = n % 2 == 0;
  for (int cost = n % 2; cost <= n; cost += 2) addMod(answer, dp[cost][0]);
  cout << answer << '\n';
  return 0;
}
```

## 推荐记忆

遇到“最终元素互异 + 相邻差绝对值和”的计数，优先考虑按值递增插入排列。未来还会插入元素的
间隙数正是跨越当前数值层的边数；再用预算下界把间隙维压到根号，这是本题最可迁移的结构。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_f?lang=en)
- [对应知识专题](../../math/combinatorial-counting.md#active-gap-budget-dp)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
