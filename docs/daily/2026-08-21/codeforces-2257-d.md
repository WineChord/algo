---
title: "[codeforces] CF Round 1117 Div.2 D Bermuda Rectangle"
---

# [codeforces] CF Round 1117 Div.2 D Bermuda Rectangle

<p class="daily-archive-kicker">2026-08-21 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-21 题目列表</a> · <a href="../../../math/combinatorial-counting/#divisor-staircase">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4e3824cc33e69f8b029a5925300c6b30fa61e1bfb1f0604f5c0ec8dcd5c01ddd -->
[Official problem: Codeforces 2257D — Bermuda Rectangle](https://codeforces.com/contest/2257/problem/D)

## 官方来源与元数据

- 比赛：Codeforces Round 1117 (Div. 2)；Contest ID 2257。
- 题目：Div.2 D — Bermuda Rectangle；没有已确认的跨 division 别名。
- 官方 points：1750；官方 API 没有提供本题 rating，故记为未知。
- 官方 tags：binary search、implementation、math、number theory、two pointers。
- 时间限制：2 秒；内存限制：256 MB；非交互题。
- 官方题目直达链接见首行；题面文字依照
  [Codeforces Problems’ Materials Publishing License v0.1](https://codeforces.com/blog/entry/967)
  标注来源。未使用隐藏测试、生成器、checker 或 validator。
- 原题配有示意图，但当前无法确认独立图片资产的原始 URL 与转载权；下方用自包含文字和样例
  手推完整表达语义，不使用第三方镜像图片。

## Complete English statement

The Beaver wants to explore an unknown **Bermuda Rectangle**. He knows only the following facts:

- its bottom-left corner is $(0,0)$;
- both side lengths are positive integers;
- its area is exactly $S$.

Thus, every possible Bermuda Rectangle has the form $[0,a]\times[0,b]$, where $a,b$ are positive
integers and $ab=S$.

The Beaver asks $q$ queries. A query gives positive integers $x$ and $y$ and considers the
$x\times y$ grid rectangle whose bottom-left corner is also $(0,0)$. Count the unit cells inside this
query rectangle that belong to at least one possible Bermuda Rectangle.

Equivalently, a unit cell with indices $(i,j)$, where $1\le i\le x$ and $1\le j\le y$, is counted if
there exists a positive divisor $a$ of $S$ such that

$$
i\le a\qquad\text{and}\qquad j\le \frac Sa.
$$

Answer every query independently.

### Input

The first line contains the number of test cases $t$. For each test case:

- the first line contains $S$ and $q$;
- each of the next $q$ lines contains one query $x,y$.

```text
t
S q
x_1 y_1
...
x_q y_q
```

### Output

For every query, print the number of unit cells in the required union-intersection.

### Constraints

- $1\le t\le10^4$.
- $1\le S\le10^{14}$.
- $1\le q\le3\times10^5$ for each test case.
- $1\le x,y\le S$.
- The sum of $q$ over all test cases does not exceed $3\times10^5$.
- The sum of $\sqrt S$ over all test cases does not exceed $10^7$.

### Official sample

```text
Input
3
6 4
2 3
4 5
6 6
1 1
5 2
2 2
3 4
8 2
3 1
5 6

Output
6
11
14
1
3
6
3
15
```

For $S=6$, the possible side pairs are $(1,6),(2,3),(3,2),(6,1)$. Query $(2,3)$ is itself one
candidate and all six cells are covered. Query $(4,5)$ intersects the union in 11 cells; query
$(6,6)$ contains the whole union of 14 cells; query $(1,1)$ contains its single covered cell.

Source: [Codeforces problem 2257D](https://codeforces.com/contest/2257/problem/D), published under the
[Codeforces materials license](https://codeforces.com/blog/entry/967).

## 中文解释与结论摘要

面积固定为 $S$，整数边长矩形与因数 $a\mid S$ 一一对应，宽为 $a$、高为 $S/a$。对第 $i$
列，能覆盖它的候选宽度必须满足 $a\ge i$；为了得到最高覆盖高度，应选“不小于 $i$ 的最小
因数”。因此并集的列高是一个随列号单调不增的阶梯函数。

把所有因数升序为 $d_1<d_2<\cdots<d_k$，则列
$d_{r-1}+1,\ldots,d_r$ 的最大高度都是 $S/d_r$。预处理阶梯面积前缀后，每次询问只需两次
二分，复杂度 $O(\sqrt S+q\log\tau(S))$，空间 $O(\tau(S))$。

## 约束推导、溢出与边界

- $S\le10^{14}$，单组可在 $O(\sqrt S)$ 枚举因数；全局
  $\sum\sqrt S\le10^7$ 正是这一做法的预算。
- $\sum q\le3\times10^5$，每次扫描全部因数仍可能超时，必须预处理并二分。
- $x,y\le S$，所以因数 1 总能成为高度阈值的候选，因数 $S$ 总能覆盖到第 $S$ 列。
- 单个候选矩形有 $S$ 个格子，但多个候选的并集更大；实现使用 `long long`，中间乘法先保持
  64 位。扩展到未保证范围的补集问题时应用 `__int128`。
- $S=1$ 时因数表只有 1，任何合法询问也只能是 $(1,1)$，答案为 1。
- 完全平方数的平方根因数只能加入一次，否则阶梯会出现重复断点。

## 样例手推

对 $S=6$，因数为 $1,2,3,6$。各列最大高度依次是

$$
h(1)=6,\quad h(2)=3,\quad h(3)=2,\quad h(4)=h(5)=h(6)=1.
$$

询问 $(4,5)$ 逐列截到高度 5，得到 $5+3+2+1=11$。对 $S=8$，因数为
$1,2,4,8$，询问 $(5,6)$ 的列高为 $6,4,2,2,1$，总和 15。

## 解法一：逐格检查所有候选矩形

小规模时枚举询问内每个格子 $(i,j)$，再枚举因数 $a$ 检查
$i\le a,j\le S/a$。它直接对应定义，时间
$O(qxy\tau(S))$，空间 $O(\tau(S))$，只适合作为 oracle。

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
    long long s;
    int q;
    cin >> s >> q;
    vector<long long> divisors;
    for (long long value = 1; value * value <= s; ++value) {
      if (s % value != 0) continue;
      divisors.push_back(value);
      if (value != s / value) divisors.push_back(s / value);
    }
    while (q--) {
      long long x, y;
      cin >> x >> y;
      long long answer = 0;
      for (long long column = 1; column <= x; ++column) {
        for (long long row = 1; row <= y; ++row) {
          bool covered = false;
          for (long long width : divisors) {
            if (column <= width && row <= s / width) covered = true;
          }
          answer += covered;
        }
      }
      cout << answer << '\n';
    }
  }
  return 0;
}
```

## 解法二：按因数阶梯逐段求和

升序因数中，宽度断点 $d_r$ 前的新列都由候选矩形
$d_r\times(S/d_r)$ 提供最高覆盖。对每个询问遍历这些阶梯段，把段宽截到 $x$，段高截到
$y$。时间降为 $O(q\tau(S))$，仍不足以承受最大询问数。

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
    long long s;
    int q;
    cin >> s >> q;
    vector<long long> divisors;
    for (long long value = 1; value * value <= s; ++value) {
      if (s % value != 0) continue;
      divisors.push_back(value);
      if (value != s / value) divisors.push_back(s / value);
    }
    sort(divisors.begin(), divisors.end());
    while (q--) {
      long long x, y;
      cin >> x >> y;
      long long answer = 0;
      long long previous = 0;
      for (long long width : divisors) {
        long long right = min(x, width);
        if (right > previous) {
          answer += (right - previous) * min(y, s / width);
          previous = right;
        }
        if (previous == x) break;
      }
      cout << answer << '\n';
    }
  }
  return 0;
}
```

## 从阶梯扫描到前缀面积

预处理

$$
F(z)=\sum_{i=1}^{z}h(i),
$$

其中 $h(i)$ 是第 $i$ 列在完整并集中的高度。对断点 $d_r$，新增面积为
$(d_r-d_{r-1})(S/d_r)$；任意 $z$ 落在某个阶梯段内，可用一次 `lower_bound` 补出部分段。

查询还要把每列高度截到 $y$。满足 $h(i)\ge y$ 的列恰是前 $p$ 列，其中 $p$ 是不超过
$S/y$ 的最大因数。于是：

$$
\operatorname{area}(x,y)
=y\min(x,p)+\max\bigl(0,F(x)-F(p)\bigr),
$$

第二项只在 $x>p$ 时加入。

## 最佳实用解：因数阶梯前缀 + 二分

### 正确性证明

**引理 1**：第 $i$ 列的最大覆盖高度为 $S/d$，其中 $d$ 是最小的满足 $d\mid S,d\ge i$
的因数。

任何覆盖第 $i$ 列的候选宽度必须至少为 $i$；其高度 $S/d$ 随宽度增大而减小，因此最小合法
宽度给出最大高度，且该候选确实覆盖这一整段列。

**引理 2**：满足列高至少为 $y$ 的列恰是 $1$ 到 $p$，其中
$p=\max\{d:d\mid S,d\le S/y\}$。

由引理 1，列高至少为 $y$ 等价于对应最小因数不超过 $S/y$。阶梯单调不增，所以这些列构成
连续前缀，其末端正是 $p$。

前 $\min(x,p)$ 列在询问中各贡献 $y$；若 $x>p$，后续列的完整高度已经小于 $y$，贡献就是
$F(x)-F(p)$。两部分无重叠且覆盖全部询问列，公式与算法正确。

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
    long long s;
    int q;
    cin >> s >> q;
    vector<long long> divisors;
    for (long long value = 1; value * value <= s; ++value) {
      if (s % value != 0) continue;
      divisors.push_back(value);
      if (value != s / value) divisors.push_back(s / value);
    }
    sort(divisors.begin(), divisors.end());
    vector<long long> prefix(divisors.size());
    for (int i = 0; i < static_cast<int>(divisors.size()); ++i) {
      long long previous = i == 0 ? 0 : divisors[i - 1];
      long long added = (divisors[i] - previous) * (s / divisors[i]);
      prefix[i] = added + (i == 0 ? 0 : prefix[i - 1]);
    }
    auto fullHeightPrefix = [&](long long x) {
      if (x == 0) return 0LL;
      int index = lower_bound(divisors.begin(), divisors.end(), x) - divisors.begin();
      long long previous = index == 0 ? 0 : divisors[index - 1];
      long long before = index == 0 ? 0 : prefix[index - 1];
      return before + (x - previous) * (s / divisors[index]);
    };
    while (q--) {
      long long x, y;
      cin >> x >> y;
      long long limit = s / y;
      int index = upper_bound(divisors.begin(), divisors.end(), limit) -
          divisors.begin() - 1;
      long long cappedUntil = min(x, divisors[index]);
      long long answer = cappedUntil * y;
      if (x > cappedUntil) {
        answer += fullHeightPrefix(x) - fullHeightPrefix(cappedUntil);
      }
      cout << answer << '\n';
    }
  }
  return 0;
}
```

枚举因数总时间 $O(\sqrt S)$，预处理 $O(\tau(S)\log\tau(S))$，每次询问
$O(\log\tau(S))$，空间 $O(\tau(S))$。

## 同阶方案比较

可以把询问离线按 $y$ 排序并用双指针移动高度阈值，从而去掉一次二分，但仍要处理每个 $x$
所在的阶梯段，代码和证明更复杂。当前每组因数数量远小于 $S$，二分版本常数稳定、在线回答、
更易复用，竞赛中优先记忆它。

## 易错点

- 题目求所有候选矩形的并集，不是选择一个候选使交面积最大。
- 阶梯段是 $(d_{r-1},d_r]$，宽度为 `d[r] - d[r-1]`，边界差一会直接破坏样例。
- 高度阈值使用“不超过 $S/y$ 的最大因数”，不是整数 $S/y$ 本身。
- 完全平方根因数不能重复加入。
- `lower_bound` 查询 $F(x)$ 时用的是首个 `d >= x`；题目保证 $x\le S$，索引一定存在。
- 不要把缺失的官方 rating 根据题目字母、points 或通过人数自行估算。

## 验证说明

所有代码块均通过 GNU++23 编译。最佳解已对小 $S$ 的所有 $1\le x,y\le S$ 与逐格暴力
比较，并对随机 $S$、质数、完全平方数、$S=1$、阈值恰落在因数和唯一样例做了复现测试。

## 变种一：询问任意轴对齐子矩形

新定义：查询单位格范围为列 $l\ldots r$、行 $b\ldots t$，不再从原点开始。原并集是向左下
闭合的阶梯形，令 `area(x,y)` 为原题前缀答案，则用二维容斥：

$$
A(r,t)-A(l-1,t)-A(r,b-1)+A(l-1,b-1).
$$

预处理不变，每次仍为 $O(\log\tau(S))$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Staircase {
  long long s;
  vector<long long> divisors;
  vector<long long> prefix;
  long long fullPrefix(long long x) const {
    if (x <= 0) return 0;
    x = min(x, s);
    int index = lower_bound(divisors.begin(), divisors.end(), x) - divisors.begin();
    long long previous = index == 0 ? 0 : divisors[index - 1];
    long long before = index == 0 ? 0 : prefix[index - 1];
    return before + (x - previous) * (s / divisors[index]);
  }
public:
  explicit Staircase(long long area) : s(area) {
    for (long long value = 1; value * value <= s; ++value) {
      if (s % value != 0) continue;
      divisors.push_back(value);
      if (value != s / value) divisors.push_back(s / value);
    }
    sort(divisors.begin(), divisors.end());
    prefix.resize(divisors.size());
    for (int i = 0; i < static_cast<int>(divisors.size()); ++i) {
      long long previous = i == 0 ? 0 : divisors[i - 1];
      prefix[i] = (divisors[i] - previous) * (s / divisors[i]);
      if (i > 0) prefix[i] += prefix[i - 1];
    }
  }
  long long area(long long x, long long y) const {
    if (x <= 0 || y <= 0) return 0;
    x = min(x, s);
    long long limit = s / min(y, s + 1);
    auto it = upper_bound(divisors.begin(), divisors.end(), limit);
    long long capped = it == divisors.begin() ? 0 : *prev(it);
    capped = min(capped, x);
    return capped * y + fullPrefix(x) - fullPrefix(capped);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long s;
  int q;
  cin >> s >> q;
  Staircase shape(s);
  while (q--) {
    long long l, b, r, t;
    cin >> l >> b >> r >> t;
    long long answer = shape.area(r, t) - shape.area(l - 1, t) -
        shape.area(r, b - 1) + shape.area(l - 1, b - 1);
    cout << answer << '\n';
  }
  return 0;
}
```

## 变种二：只允许给定的一部分边长

新定义：输入若干合法宽度 `allowed`，候选只包含
`width × (S / width)`。阶梯仍按宽度升序、高度降序，但最右边只到最大允许宽度；复用同一
前缀与阈值二分即可。预处理 $O(k\log k)$，查询 $O(\log k)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long s;
  int k, q;
  cin >> s >> k >> q;
  vector<long long> widths(k);
  for (long long& width : widths) cin >> width;
  sort(widths.begin(), widths.end());
  widths.erase(unique(widths.begin(), widths.end()), widths.end());
  vector<long long> prefix(widths.size());
  for (int i = 0; i < static_cast<int>(widths.size()); ++i) {
    long long previous = i == 0 ? 0 : widths[i - 1];
    prefix[i] = (widths[i] - previous) * (s / widths[i]);
    if (i > 0) prefix[i] += prefix[i - 1];
  }
  auto fullPrefix = [&](long long x) {
    x = min(x, widths.back());
    if (x <= 0) return 0LL;
    int index = lower_bound(widths.begin(), widths.end(), x) - widths.begin();
    long long previous = index == 0 ? 0 : widths[index - 1];
    long long before = index == 0 ? 0 : prefix[index - 1];
    return before + (x - previous) * (s / widths[index]);
  };
  while (q--) {
    long long x, y;
    cin >> x >> y;
    x = min(x, widths.back());
    auto it = upper_bound(widths.begin(), widths.end(), s / y);
    long long capped = it == widths.begin() ? 0 : *prev(it);
    capped = min(capped, x);
    long long answer = capped * y + fullPrefix(x) - fullPrefix(capped);
    cout << answer << '\n';
  }
  return 0;
}
```

## 变种三：至少被 K 个候选矩形覆盖

新定义：一个格子必须落在至少 `need` 个不同因数矩形内。对第 $i$ 列，取所有不小于 $i$ 的
因数；第 `need` 小的可用宽度给出第 `need` 大的高度。阶梯断点从 `d_r` 平移到
`d_{r+need-1}`，仍可构造列高数组并做前缀。下面给出预处理后逐询问扫描版，复杂度
$O(\sqrt S+q\tau(S))$；同样可再套原题二分优化。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long s;
  int need, q;
  cin >> s >> need >> q;
  vector<long long> divisors;
  for (long long value = 1; value * value <= s; ++value) {
    if (s % value != 0) continue;
    divisors.push_back(value);
    if (value != s / value) divisors.push_back(s / value);
  }
  sort(divisors.begin(), divisors.end());
  while (q--) {
    long long x, y;
    cin >> x >> y;
    long long answer = 0;
    long long previous = 0;
    int count = divisors.size();
    for (int first = 0; first + need - 1 < count; ++first) {
      long long right = min(x, divisors[first]);
      long long height = s / divisors[first + need - 1];
      if (right > previous) answer += (right - previous) * min(y, height);
      previous = right;
      if (previous == x) break;
    }
    cout << answer << '\n';
  }
  return 0;
}
```

## 变种四：输出询问矩形中的未覆盖格数

新定义：返回 `x*y - covered(x,y)`。原并集算法完全保留，但 $x\cdot y$ 在扩展约束下可能
超过 64 位，所以用 `__int128` 完成补集运算和输出。查询复杂度仍为 $O(\log\tau(S))$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void printInt128(__int128 value) {
  if (value == 0) {
    cout << 0 << '\n';
    return;
  }
  string digits;
  while (value > 0) {
    digits.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  }
  reverse(digits.begin(), digits.end());
  cout << digits << '\n';
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long s;
  int q;
  cin >> s >> q;
  vector<long long> divisors;
  for (long long value = 1; value * value <= s; ++value) {
    if (s % value != 0) continue;
    divisors.push_back(value);
    if (value != s / value) divisors.push_back(s / value);
  }
  sort(divisors.begin(), divisors.end());
  vector<__int128> prefix(divisors.size());
  for (int i = 0; i < static_cast<int>(divisors.size()); ++i) {
    long long previous = i == 0 ? 0 : divisors[i - 1];
    prefix[i] = static_cast<__int128>(divisors[i] - previous) * (s / divisors[i]);
    if (i > 0) prefix[i] += prefix[i - 1];
  }
  auto fullPrefix = [&](long long x) {
    if (x == 0) return static_cast<__int128>(0);
    int index = lower_bound(divisors.begin(), divisors.end(), x) - divisors.begin();
    long long previous = index == 0 ? 0 : divisors[index - 1];
    __int128 before = index == 0 ? 0 : prefix[index - 1];
    return before + static_cast<__int128>(x - previous) * (s / divisors[index]);
  };
  while (q--) {
    long long x, y;
    cin >> x >> y;
    auto it = upper_bound(divisors.begin(), divisors.end(), s / y);
    long long capped = min(x, *prev(it));
    __int128 covered = static_cast<__int128>(capped) * y;
    if (x > capped) covered += fullPrefix(x) - fullPrefix(capped);
    printInt128(static_cast<__int128>(x) * y - covered);
  }
  return 0;
}
```

## 推荐记忆

先把因数矩形并集投影成“每列的最大高度”，再看出列高只会在因数位置下降。任何原点前缀
询问都可以拆成“被 $y$ 截平的前缀 + 原始阶梯面积”，这正是二分阈值与前缀和结合的核心。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/D)
- [对应知识专题](../../math/combinatorial-counting.md#divisor-staircase)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-515-q4-lc4027/">← [力扣竞赛] 第 515 场周赛 Q4 LC 4027 电梯请求 III 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-21-lc3116/">[力扣每日一题] 2026-08-21｜LC 3116 单面值组合的第 K 小金额 →</a>
</nav>
