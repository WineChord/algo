---
title: "[codeforces] CF Educational Round 193 Div.2 A The Best Card"
---

# [codeforces] CF Educational Round 193 Div.2 A The Best Card

<p class="daily-archive-kicker">2026-08-25 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-25 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=48303beec8286a92d876773b92324039620a59da4956d7b68d8d6502455b617d -->
[Official problem: Codeforces 2253A — The Best Card](https://codeforces.com/contest/2253/problem/A)

## 官方来源与元数据

- 比赛：Educational Codeforces Round 193 (Rated for Div. 2)；Contest ID 2253。
- 题目：Div.2 A — The Best Card。
- 官方 problem/API 未给出 points，故官方分值记为未知；官方 rating 为 800，官方标签为
  greedy、math、number theory。
- 时间限制：2 秒；内存限制：512 MB。
- 题面没有理解所必需的图片。
- 下方英文层逐项核对当前官方页面，并依
  [Codeforces Problems’ Materials Publishing License v0.1](https://codeforces.com/blog/entry/967)
  呈现；来源链接紧邻题面，未包含隐藏测试、生成器、校验器或独立图片资产。

## Complete English statement

A card game contains exactly $n$ cards whose values are $2,3,4,\ldots,n+1$.

When cards with values $x$ and $y$ play against each other, determine the winner by these rules:

- if one of $x$ and $y$ is divisible by the other, the card with the smaller value wins;
- otherwise, the card with the larger value wins.

For example, card 2 beats card 6 because 6 is divisible by 2. Card 6 beats card 4 because neither
4 nor 6 divides the other.

Determine whether there is a card that wins against every other card in the game.

### Input

The first line contains an integer $t$, the number of test cases. Each test case consists of one
integer $n$.

### Output

For every test case, print `YES` if a card beating every other card exists, and print `NO`
otherwise. Letters may be printed in any case.

### Constraints

- $1\le t\le10^4$.
- $2\le n\le2\times10^5$.
- The sum of $n$ over all test cases does not exceed $3\times10^6$.
- Every input value is an integer.

### Official sample

```text
Input
5
2
3
4
5
8
Output
YES
NO
YES
NO
NO
```

For $n=2$, cards 2 and 3 are incomparable by divisibility, so the larger card 3 wins. For $n=3$,
card 2 beats 4, card 3 beats 2, and card 4 beats 3; therefore no card beats all others. These are
the two cases explained in the official Note.

Source: [Codeforces 2253A](https://codeforces.com/contest/2253/problem/A), published under the
[Codeforces materials license](https://codeforces.com/blog/entry/967).

## 中文解释与最优结论

任意 $x\in[2,n]$ 都会输给 $x+1$：两个连续且都大于 1 的整数互不整除，所以按规则较大的
$x+1$ 获胜。因此唯一可能全胜的是最大牌 $n+1$。

最大牌遇到较小的 $y$ 时，若 $y\mid(n+1)$，较小的 $y$ 获胜；否则最大牌获胜。于是存在
全胜牌当且仅当 $n+1$ 没有 2 到 $n$ 的因子，也就是 $n+1$ 为素数。

逐例试除到平方根即可，时间复杂度 $O(\sqrt n)$、空间 $O(1)$。批量查询也可先筛素数。

## 约束推导、溢出与边界

- 直接枚举所有牌与全部对手是 $O(n^2)$，总规模下无法通过。
- 证明唯一候选后，线性检查 $2,3,\ldots,n$ 已可利用 $\sum n\le3\times10^6$ 通过。
- 合数必有不超过平方根的因子，试除可进一步降到 $O(\sqrt n)$。
- $n=2$ 时检查 3，为素数，输出 `YES`；这是最小边界。
- $n=8$ 时 $n+1=9$，因子 3 必须被平方根循环检查到，输出 `NO`。
- 当前值域内 `int` 足够，但循环条件使用 `1LL * d * d <= value`，避免扩展范围后乘法溢出。
- 筛法上界必须包含 $n+1$，最大需要下标 200001。

## 官方样例手推

五个测试对应检查 $3,4,5,6,9$ 是否为素数，结果依次为真、假、真、假、假，所以输出
`YES NO YES NO NO`。其中 4 被 2 整除，6 被 2 和 3 整除，9 被 3 整除；这些较小因子都会
在对局中击败最大牌。

## 解法一：枚举候选牌与全部对手

对每个候选 $x$，逐个按规则判断它是否击败 $y$。若可整除，较小值获胜；否则较大值获胜。
它直接检查定义中的全部有序候选，因此覆盖正确。时间 $O(n^2)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool wins(int x, int y) {
  if (x % y == 0 || y % x == 0)
    return x < y;
  return x > y;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    bool exists = false;
    for (int x = 2; x <= n + 1; ++x) {
      bool good = true;
      for (int y = 2; y <= n + 1; ++y) {
        if (x != y && !wins(x, y))
          good = false;
      }
      exists = exists || good;
    }
    cout << (exists ? "YES\n" : "NO\n");
  }
  return 0;
}
```

## 从所有候选到唯一候选

若 $x\le n$，集合中一定有 $x+1$。假设 $x\mid(x+1)$，则 $x$ 也整除两者之差 1，与
$x\ge2$ 矛盾；而 $x+1>x$ 不可能整除 $x$。因此两者互不整除，较大的 $x+1$ 击败 $x$。
所有非最大牌都被排除，只需检查 $n+1$ 有没有较小因子。

## 解法二：线性扫描最大牌的因子

扫描 $d=2$ 到 $n$。若某个 $d$ 整除 $n+1$，它就是会击败最大牌的较小卡；否则最大牌全胜。
时间 $O(n)$，并且所有测试的总扫描量受 $3\times10^6$ 限制。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    int value = n + 1;
    bool prime = true;
    for (int divisor = 2; divisor < value; ++divisor) {
      if (value % divisor == 0)
        prime = false;
    }
    cout << (prime ? "YES\n" : "NO\n");
  }
  return 0;
}
```

## 最佳实用解：试除到平方根

### 正确性证明

前述连续整数论证说明只有 $n+1$ 可能全胜。若 $n+1$ 为合数，存在分解
$n+1=ab$，其中 $2\le a\le b\le n$；较小因子 $a$ 在牌组中并击败最大牌，所以答案为
`NO`。反之，若 $n+1$ 为素数，没有任何 $y\in[2,n]$ 整除它；它与每张较小牌都不满足
整除关系，于是按较大值规则逐一获胜，答案为 `YES`。

合数的两个因子中至少一个不超过平方根，所以试除到平方根不会漏掉合数；没有找到因子时
恰为素数。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool isPrime(int value) {
  if (value < 2)
    return false;
  for (int divisor = 2; 1LL * divisor * divisor <= value; ++divisor) {
    if (value % divisor == 0)
      return false;
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    cout << (isPrime(n + 1) ? "YES\n" : "NO\n");
  }
  return 0;
}
```

时间复杂度为每例 $O(\sqrt n)$，额外空间 $O(1)$。

## 同阶方案比较与易错点

若先读入全部 $n$，可筛到最大 $n+1$，预处理 $O(U\log\log U)$、每例 $O(1)$、空间
$O(U)$。当前上界很小，筛法批量常数稳定；试除写法更短且为 $O(1)$ 空间。面试和普通竞赛
优先记忆“证明唯一候选 + 试除”，多次区间统计再切换筛法。

- 错把最大牌必胜当作无需条件；任一较小因子都会击败它。
- 只检查 $n$ 是否为素数，而正确对象是 $n+1$。
- 平方根循环写成 `<`，漏掉 9、25 等完全平方数。
- 认为任意较小牌都可能成为候选，忽略它必输给下一张连续牌。
- 把 API 的 rating 800 或 standings 中一次解题计数误写成官方 points。

## 可复现验证

三份原题程序均以 C++23 编译并通过官方样例。额外覆盖 $n=2$、$n+1$ 为完全平方数、
$n+1$ 为大素数、$n=200000$ 及多测试总规模边界。直接对局暴力对 $n=2$ 到 200 与
“$n+1$ 为素数”等价式逐项比较，无差异。

## Follow-up 与约束变种

### 变种一：牌值改为连续区间 [L,R]

新定义：牌值是 $L,L+1,\ldots,R$，其中 $2\le L\le R\le10^{12}$。仍只有最大牌 $R$ 可能全胜；它全胜当且
仅当区间内没有 $R$ 的真因子。$R$ 的最大真因子为 $R/\operatorname{spf}(R)$，其中
$\operatorname{spf}$ 是最小质因子；该值小于 $L$ 时输出 `YES`。试除求最小质因子，时间
$O(\sqrt R)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long smallestFactor(long long value) {
  for (long long divisor = 2; divisor <= value / divisor; ++divisor) {
    if (value % divisor == 0)
      return divisor;
  }
  return value;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    long long left;
    long long right;
    cin >> left >> right;
    long long largestProper = right / smallestFactor(right);
    cout << (largestProper < left ? "YES\n" : "NO\n");
  }
  return 0;
}
```

### 变种二：牌值是任意互异集合

新定义：输入任意互异正整数集合。连续整数证明失效，例如集合 $\{2,4\}$ 中 2 击败 4。
候选 $x$ 全胜当且仅当没有更小的集合元素整除 $x$，并且每个更大的集合元素都是 $x$ 的
倍数。直接枚举候选与对手，时间 $O(m^2)$，总空间 $O(m)$；若不计输入数组，额外空间
$O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool wins(long long x, long long y) {
  if (x % y == 0 || y % x == 0)
    return x < y;
  return x > y;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m;
  cin >> m;
  vector<long long> card(m);
  for (long long& value : card)
    cin >> value;
  long long answer = -1;
  for (long long candidate : card) {
    bool good = true;
    for (long long opponent : card) {
      if (candidate != opponent && !wins(candidate, opponent))
        good = false;
    }
    if (good)
      answer = candidate;
  }
  cout << answer << '\n';
  return 0;
}
```

### 变种三：统计一段 n 中有多少个 YES

新定义：给定 $1\le q\le2\times10^5$ 个询问，且
$2\le L\le R\le10^7$，统计区间 $[L,R]$ 中多少个 $n$ 会输出 `YES`。原结论把问题变成统计
$[L+1,R+1]$ 中的素数个数。令 $U=\max R+1$，筛到 $U$ 并建素数前缀和，预处理
$O(U\log\log U)$，每问 $O(1)$，总空间 $O(U+q)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<pair<int, int>> query(q);
  int limit = 2;
  for (auto& [left, right] : query) {
    cin >> left >> right;
    limit = max(limit, right + 1);
  }
  vector<char> prime(limit + 1, true);
  prime[0] = prime[1] = false;
  for (int value = 2; 1LL * value * value <= limit; ++value) {
    if (!prime[value])
      continue;
    for (int multiple = value * value; multiple <= limit; multiple += value) {
      prime[multiple] = false;
    }
  }
  vector<int> prefix(limit + 1, 0);
  for (int value = 1; value <= limit; ++value) {
    prefix[value] = prefix[value - 1] + prime[value];
  }
  for (auto [left, right] : query) {
    cout << prefix[right + 1] - prefix[left] << '\n';
  }
  return 0;
}
```

### 变种四：n 扩大到 64 位

新定义：$n$ 可达 $10^{18}-1$。结论仍是判断 $n+1$ 是否为素数，但平方根试除太慢。使用
`unsigned __int128` 做模乘，并采用覆盖 64 位整数的确定性 Miller–Rabin 基组，单次约
$O(7\log n)$ 次模幂层级运算。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using u64 = uint64_t;
using u128 = __uint128_t;
u64 powerMod(u64 base, u64 exponent, u64 mod) {
  u64 result = 1;
  while (exponent) {
    if (exponent & 1)
      result = static_cast<u128>(result) * base % mod;
    base = static_cast<u128>(base) * base % mod;
    exponent >>= 1;
  }
  return result;
}
bool isPrime64(u64 value) {
  if (value < 2)
    return false;
  for (u64 prime :
      {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 19ULL, 23ULL, 29ULL, 31ULL, 37ULL}) {
    if (value % prime == 0)
      return value == prime;
  }
  u64 odd = value - 1;
  int shift = 0;
  while ((odd & 1) == 0) {
    odd >>= 1;
    ++shift;
  }
  for (u64 base : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
    if (base % value == 0)
      continue;
    u64 current = powerMod(base % value, odd, value);
    if (current == 1 || current == value - 1)
      continue;
    bool witness = true;
    for (int round = 1; round < shift; ++round) {
      current = static_cast<u128>(current) * current % value;
      if (current == value - 1) {
        witness = false;
        break;
      }
    }
    if (witness)
      return false;
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    u64 n;
    cin >> n;
    cout << (isPrime64(n + 1) ? "YES\n" : "NO\n");
  }
  return 0;
}
```

## 推荐记忆

本题真正的第一步不是写素数模板，而是用相邻牌 $x+1$ 排除所有非最大候选。随后“最大牌
全胜”等价于“最大值没有真因子”，素数判定才自然出现。这个证明顺序比直接猜答案更可迁移。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2253/problem/A)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-189-q4-lc4023/">← [力扣竞赛] 第 189 场双周赛 Q4 LC 4023 电梯请求 II 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-25-lc3718/">[力扣每日一题] 2026-08-25｜LC 3718 缺失的最小倍数 →</a>
</nav>
