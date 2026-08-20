---
title: "[atcoder] ARC227 E Shift and XOR Switches"
---

# [atcoder] ARC227 E Shift and XOR Switches

<p class="daily-archive-kicker">2026-08-21 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-21 题目列表</a> · <a href="../../../math/#binary-polynomial-carry">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3d7f29bb340a44ac8ea47edf4e904210de1a543ccb50de78d061b7b644f2f2b3 -->
[Official problem: ARC227 E — Shift and XOR Switches](https://atcoder.jp/contests/arc227/tasks/arc227_e?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227），比赛时长 120 分钟，rated 范围为 1200–2799。
- 题目：E — Shift and XOR Switches；任务 slug 为 `arc227_e`。
- 官方分值：700 分；AtCoder 未发布单题官方难度。
- AtCoder Problems 社区估算难度：2710，抓取于 2026-08-21；这不是 AtCoder 官方难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en) 仍是权威来源。

## Complete English statement

There is a binary sequence $B=(B_1,B_2,\ldots,B_N)$ of length $N$. Initially, $B_1=1$, and every
other element is $0$.

There are $M$ numbered switches. Switch $i$ has the integer $A_i$ written on it. When this switch is
pressed, all positions are updated simultaneously from the state immediately before the operation:

$$
B_j\leftarrow
\begin{cases}
B_j\oplus B_{j-A_i},&A_i<j,\\
B_j,&j\le A_i.
\end{cases}
$$

Each switch may be pressed zero or one time, and the chosen switches may be pressed in any order.
Find the number of distinct final sequences $B$, modulo $998244353$.

Here, XOR is the bitwise operation whose bit is $1$ exactly when the two input bits differ. For
example, $3\oplus5=6$, or $011\oplus101=110$ in binary. XOR of several values is independent of
the order in which the XOR operations are evaluated.

### Input

```text
N M
A_1 A_2 ... A_M
```

### Output

Print the number of distinct possible final sequences modulo $998244353$.

### Constraints

- $2\le N\le2\times10^5$.
- $1\le M\le2\times10^5$.
- $1\le A_i<N$ for every $1\le i\le M$.
- All input values are integers. Equal values among different switches are allowed.

### Official samples

Sample 1:

```text
Input
4 2
2 3

Output
4
```

The four possible final sequences are $(1,0,0,0)$, $(1,0,1,0)$, $(1,0,0,1)$, and
$(1,0,1,1)$.

Sample 2:

```text
Input
2 1
1

Output
2
```

The two possible final sequences are $(1,0)$ and $(1,1)$.

Sample 3:

```text
Input
96 30
56 6 46 18 9 38 20 25 18 44 46 71 44 65 42 20 38 25 9 95 18 65 71 9 95 65 9 42 65 6

Output
384912
```

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/arc227/tasks/arc227_e?lang=en) remains normative;
reuse is subject to the [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en).

## 中文解释与结论摘要

把 $B_j$ 看成多项式中 $x^{j-1}$ 的系数。初始多项式为 $1$，按下数值为 $a$ 的开关，
就是在 $\mathbb F_2$ 上乘以 $1+x^a$，并舍去次数不小于 $N$ 的项。因此，选择了哪些开关
决定最终结果，按下顺序不影响结果。

关键恒等式是

$$
(1+x^a)^2=1+x^{2a}\pmod 2.
$$

两个相同值 $a$ 可以“进位”为一个 $2a$；若 $2a\ge N$，这个进位在截断后直接消失。
按奇数部分给所有 $A_i$ 分组后，各组形成 $d,2d,4d,\ldots$ 的独立二进制进位链。
每条链只需维护至多两个进位状态，总复杂度为 $O(N+M)$，额外空间为 $O(N)$。

## 约束推导、溢出与边界

- $N,M$ 都达到 $2\times10^5$，不能枚举 $2^M$ 个开关子集，也不能显式枚举最终序列。
- 重复 $A_i$ 是题目的核心，而不是可删除的冗余；两个相同开关恰好产生一次二进制进位。
- 每个 $A_i<N$，所以单个开关一定能改变初始多项式；多次进位可能越过 $N-1$，越界部分
  在模 $x^N$ 后无影响。
- 状态中的“剩余开关数”至多 $M$，使用 `long long` 足够；方案数全程模 $998244353$。
- $M=1$ 时答案恒为 2。某条奇数链没有开关时只贡献一种全零规范位串。
- 顺序无关来自线性移位算子的可交换性，不能只用“XOR 本身可交换”代替完整论证。

## 样例手推

样例 1 的开关值为 2 和 3，属于不同的奇数部分链。两者都不重复，四个子集分别给出
$1$、$1+x^2$、$1+x^3$、$(1+x^2)(1+x^3)\equiv1+x^2+x^3\pmod{x^4}$，对应官方列出的
四个序列。

再看一个进位例子：若 $N=5$，有两个值为 1 的开关，那么同时选择它们得到
$(1+x)^2=1+x^2$，与选择一个值为 2 的开关完全相同；若再有两个值为 2 的开关，它们会
继续进位到 4。这个过程正是二进制加法。

## 解法一：枚举开关子集，作为小规模暴力

当 $N\le63$ 且 $M$ 很小时，用一个无符号整数保存多项式。选择值 $a$ 后执行
`state ^= state << a`，再截断到 $N$ 位。枚举全部子集并去重，时间 $O(2^M M)$，空间
$O(2^M)$。它不适合正式约束，但非常适合作为随机对拍的 oracle。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> a(m);
  for (int& value : a) cin >> value;
  if (n > 63 || m > 24) return 0;
  unsigned long long mask = (1ULL << n) - 1;
  unordered_set<unsigned long long> results;
  for (int subset = 0; subset < (1 << m); ++subset) {
    unsigned long long state = 1;
    for (int i = 0; i < m; ++i) {
      if ((subset >> i) & 1) state ^= state << a[i];
    }
    results.insert(state & mask);
  }
  cout << results.size() << '\n';
  return 0;
}
```

## 解法二：每条奇数链做循环可达集合 DP

对固定奇数 $d$，设 $d2^0,d2^1,\ldots,d2^{L-1}<N$。选择一个处于第 $i$ 层的开关，
等价于给一个模 $2^L$ 的和增加 $2^i$。因此可以用布尔数组维护所有可达余数；每加入一个
开关就做一次循环平移并取并集。

这已经消除了最终多项式本身，但最坏仍需 $O(MN)$ 时间。它适合中等规模，也清楚展示了
“规范开关集合”等价于二进制和的原因。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> frequency(n);
  for (int i = 0; i < m; ++i) {
    int value;
    cin >> value;
    ++frequency[value];
  }
  long long answer = 1;
  for (int odd = 1; odd < n; odd += 2) {
    vector<int> values;
    for (int value = odd; value < n; value *= 2) values.push_back(value);
    int modulus = 1 << values.size();
    vector<unsigned char> reachable(modulus);
    reachable[0] = 1;
    for (int level = 0; level < static_cast<int>(values.size()); ++level) {
      int shift = 1 << level;
      for (int copy = 0; copy < frequency[values[level]]; ++copy) {
        vector<unsigned char> next = reachable;
        for (int residue = 0; residue < modulus; ++residue) {
          if (!reachable[residue]) continue;
          next[(residue + shift) & (modulus - 1)] = 1;
        }
        reachable.swap(next);
      }
    }
    int ways = accumulate(reachable.begin(), reachable.end(), 0);
    answer = answer * ways % MOD;
  }
  cout << answer << '\n';
  return 0;
}
```

## 从可达余数到两状态数位 DP

对一条链从低位向高位处理。进入当前层时有 `carry` 个由低层成对进位而来的开关，再加上
本层原有的 `frequency[value]` 个，合计为 $c$。

- 若规范位选择 0，尽量把剩余开关两两进位，下一层得到 $\lfloor c/2\rfloor$。
- 若 $c>0$，规范位也可选择 1，使用一个开关后下一层得到 $\lfloor(c-1)/2\rfloor$。

为什么可以把“剩余开关全部进位”？对一个固定目标位串，保留尽可能多的高层资源只会扩大
后续可行性，不会改变已经确定的低位。于是这个贪心进位给出目标是否可达的充要判定。

若当前可能的进位值至多是两个相邻整数，上述两个取整映射的并集仍至多是两个相邻整数。
初始只有进位 0，因此每层永远只有至多两个状态。不同低位串即使汇合到同一进位，也必须把
计数相加，因为它们代表不同最终规范集合。

## 最佳实用解：按奇数部分拆链的线性 DP

每个 $1\le a<N$ 唯一写成 $a=d2^k$，其中 $d$ 为奇数，所以所有位置恰好落入一条链。
不同链的规范因子互不进位，最终多项式又能唯一恢复规范因子集合，故各链答案相乘。

### 正确性证明

**引理 1**：按下值为 $a$ 的开关等价于将当前多项式乘以 $1+x^a$，模 $x^N$。

这是更新式逐项展开的直接结果。乘法可交换，所以同一开关子集的按下顺序不影响结果。

**引理 2**：两个值为 $a$ 的规范因子等价于一个值为 $2a$ 的规范因子。

在特征 2 的域上，$(1+x^a)^2=1+x^{2a}$。不断应用后，每个小于 $N$ 的指数最多保留一次，
越过截断边界的因子消失。

**引理 3**：规范因子集合唯一决定且能由最终多项式恢复。

若最低的非零非常数项次数为 $a$，它只能来自最低规范因子 $1+x^a$。除去该因子后重复此
过程即可恢复全部指数。因此两个不同规范集合不会产生同一最终序列。

**引理 4**：单链 DP 恰好计数该链的所有规范位串。

对任意固定低位前缀，DP 保存可用于更高层的最大进位数。输出位为 0 时可将全部 $c$ 个开关
两两进位；输出位为 1 时先使用一个，再把其余开关进位。若相应资源不存在，该位选择不可行；
若存在，最大化剩余资源不会破坏前缀且包含所有未来可行延伸。归纳可得转移充要。汇合只合并
未来资源状态，方案计数仍相加，所以每个可达规范位串恰计一次。

由四个引理和链间独立性，算法输出的乘积正是不同最终序列数。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> frequency(n);
  for (int i = 0; i < m; ++i) {
    int value;
    cin >> value;
    ++frequency[value];
  }
  long long answer = 1;
  for (int odd = 1; odd < n; odd += 2) {
    map<int, long long> dp;
    dp[0] = 1;
    for (int value = odd; value < n; value *= 2) {
      map<int, long long> next;
      for (auto [carry, ways] : dp) {
        int available = carry + frequency[value];
        int without = available / 2;
        next[without] = (next[without] + ways) % MOD;
        if (available > 0) {
          int with = (available - 1) / 2;
          next[with] = (next[with] + ways) % MOD;
        }
      }
      dp.swap(next);
    }
    long long chainWays = 0;
    for (auto [carry, ways] : dp) {
      static_cast<void>(carry);
      chainWays = (chainWays + ways) % MOD;
    }
    answer = answer * chainWays % MOD;
  }
  cout << answer << '\n';
  return 0;
}
```

时间复杂度 $O(N+M)$，空间复杂度 $O(N)$。`map` 中每轮最多两个键；也可手写两元素数组
进一步减小常数，但当前实现更易审查，仍满足正式约束。

## 易错点

- 原地模拟单次开关时若从左到右更新，会错误读取本次已经改变的新状态；必须使用旧状态。
- 把相同 $A_i$ 去重会丢失进位信息。
- 统计的是不同最终序列，不是开关子集数量；样例之外很容易出现多个子集汇合。
- 链必须按“除尽 2 后的奇数部分”分类，而不是只按最低二进制位分类。
- 输出位为 1 时要先确认 `available > 0`，再计算 `(available - 1) / 2`。
- 处理完最高可见层后，剩余进位越过 $N-1$，不应再区分。

## 验证说明

所有代码块均以 GNU++23 语法编译。最佳解已对 $2\le N\le10$、小规模随机重复开关数组与
解法一的完整子集枚举逐一对拍；同时覆盖全相同值、连续进位、不同奇数链、进位刚好越界和
三个官方样例。

## 变种一：给定最终序列，恢复一组按下的开关

新定义：除原输入外再给一个长度为 $N$ 的目标 01 串，保证它可达，输出任意一组开关编号。
先按最低非零次数连续做形式幂级数除法，恢复目标的规范因子位；再对每条链做带前驱的循环
背包，找出实际选择数量。用二进制分组压缩重复开关，复杂度约为各链模数乘分组数，适合
需要构造而 $N$ 中等的场景。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Group {
  int level;
  int amount;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> a(m);
  vector<vector<int>> indices(n);
  for (int i = 0; i < m; ++i) {
    cin >> a[i];
    indices[a[i]].push_back(i + 1);
  }
  string target;
  cin >> target;
  vector<int> polynomial(n);
  for (int i = 0; i < n; ++i) polynomial[i] = target[i] - '0';
  vector<int> canonical(n);
  for (int degree = 1; degree < n; ++degree) {
    if (polynomial[degree] == 0) continue;
    canonical[degree] = 1;
    vector<int> quotient = polynomial;
    for (int j = degree; j < n; ++j) {
      quotient[j] = polynomial[j] ^ quotient[j - degree];
    }
    polynomial.swap(quotient);
  }
  vector<int> answer;
  for (int odd = 1; odd < n; odd += 2) {
    vector<int> values;
    for (int value = odd; value < n; value *= 2) values.push_back(value);
    int modulus = 1 << values.size();
    int wanted = 0;
    for (int level = 0; level < static_cast<int>(values.size()); ++level) {
      wanted |= canonical[values[level]] << level;
    }
    vector<Group> groups;
    for (int level = 0; level < static_cast<int>(values.size()); ++level) {
      int period = modulus >> level;
      int count = min(static_cast<int>(indices[values[level]].size()), period - 1);
      for (int take = 1; count > 0; take *= 2) {
        int amount = min(take, count);
        groups.push_back({level, amount});
        count -= amount;
      }
    }
    vector<unsigned char> reachable(modulus);
    vector<int> parent(modulus, -1), usedGroup(modulus, -1);
    reachable[0] = 1;
    for (int group = 0; group < static_cast<int>(groups.size()); ++group) {
      vector<unsigned char> before = reachable;
      int shift = (groups[group].amount << groups[group].level) & (modulus - 1);
      for (int residue = 0; residue < modulus; ++residue) {
        if (!before[residue]) continue;
        int next = (residue + shift) & (modulus - 1);
        if (reachable[next]) continue;
        reachable[next] = 1;
        parent[next] = residue;
        usedGroup[next] = group;
      }
    }
    if (!reachable[wanted]) return 0;
    vector<int> chosen(values.size());
    while (wanted != 0) {
      int group = usedGroup[wanted];
      chosen[groups[group].level] += groups[group].amount;
      wanted = parent[wanted];
    }
    for (int level = 0; level < static_cast<int>(values.size()); ++level) {
      for (int i = 0; i < chosen[level]; ++i) {
        answer.push_back(indices[values[level]][i]);
      }
    }
  }
  sort(answer.begin(), answer.end());
  cout << answer.size() << '\n';
  for (int index : answer) cout << index << ' ';
  cout << '\n';
  return 0;
}
```

## 变种二：每个开关可以按任意多次

新定义：一个已有开关不再限按一次。对某条长度为 $L$ 的链，只要最低存在层为 $r$，反复
选择该开关就能生成模 $2^L$ 下所有 $2^r$ 的倍数，共 $2^{L-r}$ 个规范位串。不同链相乘，
时间 $O(N+M)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
long long powerTwo(int exponent) {
  long long result = 1;
  while (exponent--) result = result * 2 % MOD;
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> present(n);
  while (m--) {
    int value;
    cin >> value;
    present[value] = 1;
  }
  long long answer = 1;
  for (int odd = 1; odd < n; odd += 2) {
    vector<int> values;
    for (int value = odd; value < n; value *= 2) values.push_back(value);
    int first = values.size();
    for (int level = 0; level < static_cast<int>(values.size()); ++level) {
      if (present[values[level]]) first = min(first, level);
    }
    if (first < static_cast<int>(values.size())) {
      answer = answer * powerTwo(values.size() - first) % MOD;
    }
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种三：保证所有开关值两两不同

新定义：$A_i$ 两两不同。任意子集中每个指数起初至多出现一次，因此没有二进制进位；而
规范因子集合又能由最终多项式唯一恢复。于是所有 $2^M$ 个子集产生不同结果，复杂度
$O(M+\log M)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  for (int i = 0, value; i < m; ++i) cin >> value;
  static_cast<void>(n);
  long long answer = 1;
  long long base = 2;
  for (int exponent = m; exponent > 0; exponent >>= 1) {
    if (exponent & 1) answer = answer * base % MOD;
    base = base * base % MOD;
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种四：初始序列改为任意非零 01 序列

新定义：额外输入初始串 $P$。设最低的 1 位于零基次数 $r$，则
$P=x^rQ$，其中 $Q$ 的常数项为 1，在截断幂级数环中可逆。乘以 $Q$ 不会合并两个不同的
开关乘积；真正可见的长度缩短为 $N-r$。若初始串全零，任何操作后仍全零，答案为 1。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
long long countWays(int length, const vector<int>& switches) {
  vector<int> frequency(length);
  for (int value : switches) {
    if (value < length) ++frequency[value];
  }
  long long answer = 1;
  for (int odd = 1; odd < length; odd += 2) {
    map<int, long long> dp{{0, 1}};
    for (int value = odd; value < length; value *= 2) {
      map<int, long long> next;
      for (auto [carry, ways] : dp) {
        int available = carry + frequency[value];
        next[available / 2] = (next[available / 2] + ways) % MOD;
        if (available > 0) {
          int after = (available - 1) / 2;
          next[after] = (next[after] + ways) % MOD;
        }
      }
      dp.swap(next);
    }
    long long chainWays = 0;
    for (auto [carry, ways] : dp) {
      static_cast<void>(carry);
      chainWays = (chainWays + ways) % MOD;
    }
    answer = answer * chainWays % MOD;
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  string initial;
  cin >> initial;
  vector<int> switches(m);
  for (int& value : switches) cin >> value;
  int first = initial.find('1');
  if (first == static_cast<int>(string::npos)) {
    cout << 1 << '\n';
  } else {
    cout << countWays(n - first, switches) << '\n';
  }
  return 0;
}
```

## 推荐记忆

优先记住“移位 XOR 等价于乘 $1+x^a$、两个同因子在特征 2 下向 $2a$ 进位、按奇数部分
拆链”这条建模链。真正让复杂度降到线性的最后一步，是固定目标低位时把剩余资源全部进位，
从而让每层的未来状态始终不超过两个相邻整数。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_e?lang=en)
- [对应知识专题](../../math/index.md#binary-polynomial-carry)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
