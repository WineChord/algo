---
title: "[codeforces] CF Round 1116 Div.2 B Domino Tiles"
---

# [codeforces] CF Round 1116 Div.2 B Domino Tiles

<p class="daily-archive-kicker">2026-08-13 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-13 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c7060887a1495fc50b4a4b050920f20d31a7094629211a2958c1c9fc442aaf7d -->
[Official problem: Codeforces 2256B - Domino Tiles](https://codeforces.com/contest/2256/problem/B)

## 官方来源与元数据

- 比赛：Codeforces Round 1116 (Div. 2)，contestId 2256。
- 题目：Div.2 B - Domino Tiles；这是 Div.2 独有题，不存在 Div.1 别名。
- 官方分值：1000；官方 API 当前没有 `rating` 字段，故 rating 未知。
- 官方标签：implementation、math。
- 时间限制：1 秒；内存限制：256 MB。
- 官方链接：[Codeforces 2256B](https://codeforces.com/contest/2256/problem/B)。
- Codeforces 来源与公开使用条件见 [Materials usage license v0.1](https://codeforces.com/blog/entry/967)；下方英文层按官方可见题面自包含呈现，不包含测试生成器、校验器或隐藏数据。

## Complete English statement

### Task

Nygglatho brought home a box of old square tiles whose markings were fading. Chtholly and the fairies arranged them in one row for a puzzle.

The row contains $n$ tiles. Every tile should contain either `0` or `1`; a faded tile is written as `?`. The current row is described by a string $s$ of length $n$. Replace every `?` independently with `0` or `1`.

After completion, for every $1\le i<n$, tiles $s_i$ and $s_{i+1}$ form a domino of weight $s_i+s_{i+1}$. Two consecutive dominoes share exactly one tile. The completed row is valid if and only if every two consecutive dominoes have different weights.

Count the distinct valid replacements modulo $998244353$. Two replacements are different exactly when their completed binary strings differ.

### Input

The first line contains $t$, the number of test cases. Each test case contains:

```text
n
s
```

### Output

For every test case, print the number of valid completions modulo $998244353$.

### Constraints

- $1\le t\le10^4$.
- $2\le n\le2\times10^5$.
- $|s|=n$ and every character is `0`, `1`, or `?`.
- The sum of $n$ over all test cases is at most $2\times10^5$.

### Sample

```text
4
2
??
5
0?1??
5
0?0??
8
00110011
```

```text
4
2
0
1
```

For the first test case, there is only one domino, so all four completions `00`, `01`, `10`, and `11` are valid. For the second test case, the valid strings are exactly `00110` and `01100`. The third test case has no valid completion. The fourth test case has the unique valid completion `00110011`.

The official statement contains no task-essential image and no additional note beyond these four explanations.

## 中文题意

把每个问号补成 0 或 1。相邻两个字符形成骨牌，权重等于两字符之和。要求任意两块连续骨牌权重不同，统计不同完整二进制串的数量，模 $998244353$。

## 约束推导与核心等价

设完整串为 $x_1,x_2,\ldots,x_n$，第 $i$ 块骨牌权重 $w_i=x_i+x_{i+1}$。连续骨牌条件等价于：

$$
w_i\ne w_{i+1}
\iff x_i+x_{i+1}\ne x_{i+1}+x_{i+2}
\iff x_i\ne x_{i+2}.
$$

字符只有 0、1，所以进一步强制 $x_{i+2}=1-x_i$。前两位一旦确定，整串唯一；四个候选分别以 `00`、`01`、`10`、`11` 开头，并以 4 为周期。逐个检查与固定字符是否冲突即可。答案实际上至多 4，不会触及模数。

## 解法递进

### 解法一：枚举全部问号

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string s;
  cin >> s;
  vector<int> unknown;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '?') unknown.push_back(i);
  }
  int answer = 0;
  for (int mask = 0; mask < (1 << unknown.size()); ++mask) {
    string current = s;
    for (int i = 0; i < static_cast<int>(unknown.size()); ++i) {
      current[unknown[i]] = '0' + ((mask >> i) & 1);
    }
    bool valid = true;
    for (int i = 0; i + 2 < static_cast<int>(current.size()); ++i) {
      if (current[i] == current[i + 2]) valid = false;
    }
    answer += valid;
  }
  cout << answer << '\n';
}
```

若有 $q$ 个问号，时间 $O(n2^q)$，空间 $O(n)$，只能作为小规模 oracle。

### 解法二：最后两位四状态 DP

记录最后两位，追加新位时只允许它不同于前前位。时间 $O(n)$、空间 $O(1)$，而且容易扩展；但原题可进一步发现每个初始二位状态只有唯一后继。

### 最佳实用解：检查四个周期候选

对位置 $i$，令开头两位由 `mask` 表示；每跨过两个位置就翻转，因此目标位为 `((mask >> (i & 1)) & 1) ^ ((i >> 1) & 1)`。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    string s;
    cin >> n >> s;
    int answer = 0;
    for (int mask = 0; mask < 4; ++mask) {
      bool valid = true;
      for (int i = 0; i < n; ++i) {
        int bit = ((mask >> (i & 1)) & 1) ^ ((i >> 1) & 1);
        if (s[i] != '?' && s[i] - '0' != bit) {
          valid = false;
          break;
        }
      }
      answer += valid;
    }
    cout << answer << '\n';
  }
}
```

时间 $O(n)$，额外空间 $O(1)$；所有测试合计 $O(\sum n)$。

## 正确性证明

任何有效串都必须对每个 $i$ 满足 $x_i\ne x_{i+2}$，二进制下即递推 $x_{i+2}=1-x_i$，所以必属于四个候选之一。反之，四个候选按构造满足该递推，代回可知任意连续骨牌权重不同；若候选又兼容原串全部固定字符，它就是合法补全。不同候选前两位不同，因此补全结果互异。算法检查四个候选，不重不漏。

## 样例手推与边界

对 `0?1??`，四候选中 `00110` 与 `01100` 兼容，另外两个首位为 1，故答案 2。对 `0?0??`，固定的第 1、3 位相同，直接违反 $x_1\ne x_3$，答案 0。

- $n=2$ 时没有两块连续骨牌，所有兼容补全都有效；四候选恰覆盖四种二进制串。
- 全问号时无论长度均有 4 个候选。
- 全固定串答案只能是 0 或 1。

## 方案比较与推荐

四状态 DP 与候选法同为 $O(n)$、$O(1)$。候选法状态更少、证明直达 4 周期，竞赛中应优先记；DP 更适合加权骨牌、扩大字符集或允许若干违例。

## 易错点

- 不能只禁止 `000`、`111`；`010`、`101` 的两块骨牌权重也都为 1，同样非法。
- 模式是 `a,b,!a,!b`，不是简单的 `01` 交替。
- 问号不独立贡献 2 倍；前两位确定后，其余全部被强制。
- 官方 API 缺少 rating，不能按 B 题或 1000 分猜测。

## 可复现验证

最佳代码以 GNU++23 与 Clang C++23 严格编译，官方样例输出 `4,2,0,1`。本轮统一测试完全枚举长度 2 至 10 的 88,569 个 `0/1/?` 源串并枚举各自补全，零不一致。独立复核进一步覆盖长度 2 至 11 的 265,716 个源串、5,592,400 个完成串，以及 20,000 组随机和 4 个 $n=200000$ 边界，均与四状态 DP 一致。

## 变种一：在线单点更新

为四个候选维护固定字符冲突数。一次修改只更新四个计数，答案是冲突数为 0 的候选数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solver {
  string s;
  array<int, 4> conflict{};
  int expected(int mask, int index) {
    return ((mask >> (index & 1)) & 1) ^ ((index >> 1) & 1);
  }
  int bad(int mask, int index, char ch) {
    return ch != '?' && ch - '0' != expected(mask, index);
  }
public:
  explicit Solver(string value) : s(move(value)) {
    for (int mask = 0; mask < 4; ++mask) {
      for (int i = 0; i < static_cast<int>(s.size()); ++i) conflict[mask] += bad(mask, i, s[i]);
    }
  }
  int update(int index, char ch) {
    for (int mask = 0; mask < 4; ++mask) {
      conflict[mask] -= bad(mask, index, s[index]);
      conflict[mask] += bad(mask, index, ch);
    }
    s[index] = ch;
    return count(conflict.begin(), conflict.end(), 0);
  }
};
int main() {
  Solver solver("0?1??");
  cout << solver.update(1, '0') << '\n';
}
```

预处理 $O(n)$，每次修改 $O(1)$，空间 $O(n)$ 保存字符串。

## 变种二：方块首尾成环

环上条件仍为 $x_i\ne x_{i+2}$。步长 2 的循环可二染当且仅当 $n$ 是 4 的倍数；可行时仍检查同四个候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string s;
  cin >> s;
  int n = static_cast<int>(s.size());
  if (n % 4 != 0) {
    cout << 0 << '\n';
    return 0;
  }
  int answer = 0;
  for (int mask = 0; mask < 4; ++mask) {
    bool valid = true;
    for (int i = 0; i < n; ++i) {
      int bit = ((mask >> (i & 1)) & 1) ^ ((i >> 1) & 1);
      if (s[i] != '?' && s[i] - '0' != bit) valid = false;
    }
    answer += valid;
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：字符值扩展为 $0\ldots k-1$

消项后仍要求 $x_i\ne x_{i+2}$；奇、偶下标分别是相邻颜色不同的路径。对每条链做颜色 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  constexpr long long mod = 998244353;
  int n, colors;
  cin >> n >> colors;
  vector<int> fixed(n);
  for (int& x : fixed) cin >> x;
  long long answer = 1;
  for (int parity = 0; parity < 2; ++parity) {
    vector<long long> dp(colors, 1), next(colors);
    bool first = true;
    for (int i = parity; i < n; i += 2) {
      long long total = accumulate(dp.begin(), dp.end(), 0LL) % mod;
      for (int color = 0; color < colors; ++color) {
        long long ways = first ? 1 : (total - dp[color] + mod) % mod;
        next[color] = fixed[i] == -1 || fixed[i] == color ? ways : 0;
      }
      dp.swap(next);
      first = false;
    }
    answer = answer * (accumulate(dp.begin(), dp.end(), 0LL) % mod) % mod;
  }
  cout << answer << '\n';
}
```

时间 $O(nk)$，空间 $O(k)$。

## 变种四：加权骨牌

权重改为 $\alpha x_i+\beta x_{i+1}$ 时，中项不能一般消去；用最后两位的四状态 DP 尝试下一位。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, alpha, beta;
  string s;
  cin >> n >> alpha >> beta >> s;
  array<long long, 4> dp{};
  for (int a = 0; a < 2; ++a) for (int b = 0; b < 2; ++b) {
    if ((s[0] == '?' || s[0] - '0' == a) && (s[1] == '?' || s[1] - '0' == b)) dp[a * 2 + b] = 1;
  }
  for (int i = 2; i < n; ++i) {
    array<long long, 4> next{};
    for (int state = 0; state < 4; ++state) for (int z = 0; z < 2; ++z) {
      int x = state / 2;
      int y = state % 2;
      if (s[i] != '?' && s[i] - '0' != z) continue;
      if (alpha * x + beta * y != alpha * y + beta * z) next[y * 2 + z] += dp[state];
    }
    dp = next;
  }
  cout << accumulate(dp.begin(), dp.end(), 0LL) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种五：允许至多 $K$ 次相邻骨牌等权

一次违例等价于 $x_i=x_{i+2}$。状态记录最后两位与已用违例数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, limit;
  string s;
  cin >> n >> limit >> s;
  vector<array<long long, 4>> dp(limit + 1), next(limit + 1);
  for (int a = 0; a < 2; ++a) for (int b = 0; b < 2; ++b) {
    if ((s[0] == '?' || s[0] - '0' == a) && (s[1] == '?' || s[1] - '0' == b)) dp[0][a * 2 + b] = 1;
  }
  for (int i = 2; i < n; ++i) {
    fill(next.begin(), next.end(), array<long long, 4>{});
    for (int used = 0; used <= limit; ++used) for (int state = 0; state < 4; ++state) {
      for (int z = 0; z < 2; ++z) {
        if (s[i] != '?' && s[i] - '0' != z) continue;
        int extra = state / 2 == z;
        if (used + extra <= limit) next[used + extra][(state % 2) * 2 + z] += dp[used][state];
      }
    }
    dp.swap(next);
  }
  long long answer = 0;
  for (const auto& layer : dp) answer += accumulate(layer.begin(), layer.end(), 0LL);
  cout << answer << '\n';
}
```

时间 $O(nK)$，空间 $O(K)$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2256/problem/B)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-188-q4-lc4009/">← [力扣竞赛] 第 188 场双周赛 Q4 LC 4009 最小化最大可能等待时间 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-13-lc2213/">[力扣每日一题] 2026-08-13｜LC 2213 由单个字符重复的最长子字符串 →</a>
</nav>
