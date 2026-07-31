---
title: "[atcoder] ABC468 G Restricted Permutation"
---

# [atcoder] ABC468 G Restricted Permutation

<p class="daily-archive-kicker">2026-08-01 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../math/combinatorial-counting/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=095a742ff0a83d16ee8a60a223ef990733ad92847189cb90c4c1b18260533fb8 -->
## 官方来源与元数据

- 来源：AtCoder。
- 比赛：AtCoder Beginner Contest 468。
- 题号与标题：G - Restricted Permutation。
- 官方分值：550 分。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- 官方题面：[ABC468 G - Restricted Permutation](https://atcoder.jp/contests/abc468/tasks/abc468_g?lang=en)。
- 版权条款：[AtCoder Terms of Service](https://atcoder.jp/tos)。

普通 AtCoder 比赛题面没有已确认的统一开放转载许可。下方英文层依据官方题面独立组织，完整保留任务定义、输入输出、全部约束与样例；它不是逐字官方原文，官方页面仍是事实核验的权威入口。

## Complete English statement

- Contest: AtCoder Beginner Contest 468
- Task: G - Restricted Permutation
- Official score: 550 points
- Rated range: 0–1999
- Time limit: 2 seconds
- Memory limit: 1024 MiB
- Official task: [ABC468 G - Restricted Permutation](https://atcoder.jp/contests/abc468/tasks/abc468_g?lang=en)

This self-contained English presentation was independently organized from the official task and preserves its complete meaning, input, output, constraints, and samples. It is not represented as a verbatim reproduction. See the official task and the [AtCoder Terms of Service](https://atcoder.jp/tos).

### Problem Statement

You are given a positive integer $N$ and a string $S$ of length $N$. Every character of $S$ is either `o` or `x`.

Count the permutations

$$
P=(P_1,P_2,\ldots,P_N)
$$

of $(1,2,\ldots,N)$ that satisfy the following condition for every integer $k$ with $1\le k\le N$:

- $S_k$ is `o` if and only if $P$ contains, as a contiguous subsequence, some permutation of $(1,2,\ldots,k)$.

Equivalently, the positions occupied by the values $1,2,\ldots,k$ must form one contiguous interval exactly for those $k$ whose character in $S$ is `o`.

Output the count modulo $998244353$.

### Input

```text
N
S
```

### Output

Output the required number of permutations modulo $998244353$.

### Complete Constraints

$$
1\le N\le2000
$$

- $S$ has length $N$.
- Every character of $S$ is either `o` or `x`.
- All input values are integers where applicable.

### Official Sample 1

```text
3
oxo
```

```text
2
```

The two valid permutations are $(1,3,2)$ and $(2,3,1)$.

### Official Sample 2

```text
7
xxxxxxx
```

```text
0
```

### Official Sample 3

```text
15
oxxxoxxxxxooxxo
```

```text
1627648
```

The official statement provides no additional note or image for this task.

## 中文题意与元数据说明

对排列中的每个 $k$，观察数值集合 $\{1,2,\ldots,k\}$ 所占的位置是否恰好连成一段。`o` 要求连成一段，`x` 要求不连成一段，而且是“当且仅当”，两种方向都必须满足。求符合整串模式的排列数。

AtCoder 官方未标注独立题目难度。AtCoder Problems 社区模型在 2026-08-01 的估算难度为 1975；这是社区估算，不是 AtCoder 官方难度。

## 约束推导与结构分解

$N\le2000$ 允许 $O(N^2)$，但无法枚举 $N!$ 个排列。任何排列都必然满足：单元素集合 $\{1\}$ 连续，全集 $\{1,\ldots,N\}$ 也连续。因此若 `S[0]` 或 `S[N-1]` 为 `x`，答案立即为 0。

定义 $d_n$：长度为 $n$ 的排列中，只有 $k=1$ 与 $k=n$ 连续，而 $2\le k<n$ 全部不连续的排列数，也就是模式 `ox...xo` 的答案。

把任意 $n$ 阶排列按最小的 $k\ge2$ 分类，使 $\{1,\ldots,k\}$ 连续。这个最小块内部有 $d_k$ 种排列；把整个块收缩为一个元素后，它与 $k+1,\ldots,n$ 共 $n-k+1$ 个对象，可任意排列。因此

$$
n!=\sum_{k=2}^{n}d_k\,(n-k+1)!.
$$

由于 $d_n$ 的系数是 $1!$，可递推

$$
d_n=n!-\sum_{k=2}^{n-1}d_k\,(n-k+1)!.
$$

再设 `o` 的位置为

$$
1=A_1<A_2<\cdots<A_M=N.
$$

在两个相邻真位置之间，把已经连续的 $\{1,\ldots,A_i\}$ 收缩成一个对象，再加入 $A_i+1,\ldots,A_{i+1}$。这一段恰好要求“首尾连续、中间不连续”，独立贡献 $d_{A_{i+1}-A_i+1}$。故答案为

$$
\prod_{i=1}^{M-1}d_{A_{i+1}-A_i+1}.
$$

## 解法递进

### 解法一：枚举全部排列并逐个检查

对每个 $k$ 维护数值 $1..k$ 的最小与最大位置；它们连续当且仅当最大位置减最小位置加一等于 $k$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  vector<int> permutation(n);
  iota(permutation.begin(), permutation.end(), 1);
  long long answer = 0;
  do {
    vector<int> position(n + 1);
    for (int i = 0; i < n; ++i) {
      position[permutation[i]] = i;
    }
    int minimum = n;
    int maximum = -1;
    bool valid = true;
    for (int value = 1; value <= n; ++value) {
      minimum = min(minimum, position[value]);
      maximum = max(maximum, position[value]);
      bool contiguous = maximum - minimum + 1 == value;
      if (contiguous != (s[value - 1] == 'o')) {
        valid = false;
        break;
      }
    }
    answer += valid;
  } while (next_permutation(permutation.begin(), permutation.end()));
  cout << answer << '\n';
}
```

时间 $O(N!\,N)$，空间 $O(N)$，只适用于 $N\le10$ 的基准验证。

### 最佳实用解：不可再分块计数与相邻真位置乘法

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  if (s.front() != 'o' || s.back() != 'o') {
    cout << 0 << '\n';
    return 0;
  }
  vector<long long> factorial(n + 1, 1), primitive(n + 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  for (int length = 2; length <= n; ++length) {
    primitive[length] = factorial[length];
    for (int firstBlock = 2; firstBlock < length; ++firstBlock) {
      primitive[length] -= primitive[firstBlock] * factorial[length - firstBlock + 1] % mod;
      if (primitive[length] < 0) {
        primitive[length] += mod;
      }
    }
  }
  long long answer = 1;
  int previous = 0;
  for (int index = 1; index < n; ++index) {
    if (s[index] == 'o') {
      answer = answer * primitive[index - previous + 1] % mod;
      previous = index;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N^2)$，空间 $O(N)$。所有乘法先提升到 `long long`；取模后值小于 $998244353$，乘积在 64 位范围内。

## 正确性证明

先证明 $d_n$ 递推。每个 $n$ 阶排列至少在 $k=n$ 时形成连续块，所以存在唯一的最小 $k\ge2$。该块内部在更小的 $2..k-1$ 上都不能连续，恰有 $d_k$ 种；收缩后剩余对象完全不同且可任意排列，恰有 $(n-k+1)!$ 种。不同最小 $k$ 的类别互斥并覆盖全部 $n!$ 个排列，递推成立。

再证明乘法分解。相邻 `o` 位置 $A_i,A_{i+1}$ 都要求相应前缀值集合成块，而中间位置全部要求不成块。收缩已构成的较小块后，局部对象数为 $A_{i+1}-A_i+1$，其合法内部相对次序正是 $d$ 的定义。不同区间只决定逐层块内部的新相对次序，选择互不干扰；收缩与展开又构成双射，所以按乘法原理得到全部且无重复的合法排列。

## 样例手推

$d_2=2!=2$，而

$$
d_3=3!-d_2\cdot2!=6-4=2.
$$

样例 1 的 `o` 位于 1 与 3，唯一间隔贡献 $d_3=2$，对应 `(1,3,2)` 与 `(2,3,1)`。样例 2 首尾都是 `x`，与必然连续的单元素和全集矛盾，直接为 0。

$N=1,S=\texttt{o}$ 时没有相邻真位置，空乘积为 1，唯一排列合法。

## 易错点与方案比较

- 条件是“当且仅当”；`x` 位置必须不连续，不能只检查所有 `o`。
- 连续子序列只关心位置相邻，块内部可以是任意排列。
- 首尾字符都是必要条件；特别是 $k=1$ 永远成立。
- 递推中的压缩对象数是 $n-k+1$，阶乘不能写成 $(n-k)!$。
- 区间长度使用下标差加一：相邻真位置差为 $g$ 时贡献 $d_{g+1}$。
- 暴力用于对拍；$O(N^2)$ 递推恰好匹配约束、无需逆元，推荐记忆“按最早成块位置分类 + 连续真位置间独立收缩”。

## 变种一：同一个 $N$ 回答多条模式串

`d_2..d_N` 只依赖 $N$，预处理一次后每条字符串只扫描相邻 `o` 位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queryCount;
  cin >> n >> queryCount;
  vector<long long> factorial(n + 1, 1), primitive(n + 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  for (int length = 2; length <= n; ++length) {
    primitive[length] = factorial[length];
    for (int block = 2; block < length; ++block) {
      primitive[length] =
          (primitive[length] - primitive[block] * factorial[length - block + 1]) % mod;
    }
    primitive[length] = (primitive[length] + mod) % mod;
  }
  while (queryCount--) {
    string s;
    cin >> s;
    if (s.front() != 'o' || s.back() != 'o') {
      cout << 0 << '\n';
      continue;
    }
    long long answer = 1;
    int previous = 0;
    for (int i = 1; i < n; ++i) {
      if (s[i] == 'o') {
        answer = answer * primitive[i - previous + 1] % mod;
        previous = i;
      }
    }
    cout << answer << '\n';
  }
}
```

预处理 $O(N^2)$，每次查询 $O(N)$，空间 $O(N)$。

## 变种二：统计恰有 $M$ 个前缀值集合连续的排列

不指定具体 `o` 位置，只限定数量。令 `ways[position][count]` 表示最后一个真位置为 `position`、共出现 `count` 个真位置的方案数；枚举下一个真位置并乘相应 $d$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, required;
  cin >> n >> required;
  vector<long long> factorial(n + 1, 1), primitive(n + 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  for (int length = 2; length <= n; ++length) {
    primitive[length] = factorial[length];
    for (int block = 2; block < length; ++block) {
      primitive[length] =
          (primitive[length] - primitive[block] * factorial[length - block + 1]) % mod;
    }
    primitive[length] = (primitive[length] + mod) % mod;
  }
  vector<vector<long long>> ways(n + 1, vector<long long>(required + 1));
  ways[1][1] = 1;
  for (int position = 1; position < n; ++position) {
    for (int count = 1; count < required; ++count) {
      for (int next = position + 1; next <= n; ++next) {
        ways[next][count + 1] += ways[position][count] * primitive[next - position + 1] % mod;
        ways[next][count + 1] %= mod;
      }
    }
  }
  cout << ways[n][required] << '\n';
}
```

时间 $O(MN^2)$，空间 $O(MN)$。$N=1$ 时只有 $M=1$ 的答案为 1。

## 变种三：模式中允许通配符 `?`

`o` 必须连续，`x` 必须不连续，`?` 可任选。DP 枚举相邻真位置：端点字符不能为 `x`，而两端之间不能含强制 `o`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string pattern;
  cin >> n >> pattern;
  if (pattern.front() == 'x' || pattern.back() == 'x') {
    cout << 0 << '\n';
    return 0;
  }
  vector<long long> factorial(n + 1, 1), primitive(n + 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  for (int length = 2; length <= n; ++length) {
    primitive[length] = factorial[length];
    for (int block = 2; block < length; ++block) {
      primitive[length] =
          (primitive[length] - primitive[block] * factorial[length - block + 1]) % mod;
    }
    primitive[length] = (primitive[length] + mod) % mod;
  }
  vector<int> forcedPrefix(n + 1);
  for (int i = 0; i < n; ++i) {
    forcedPrefix[i + 1] = forcedPrefix[i] + (pattern[i] == 'o');
  }
  vector<long long> ways(n);
  ways[0] = 1;
  for (int next = 1; next < n; ++next) {
    if (pattern[next] == 'x') {
      continue;
    }
    for (int previous = 0; previous < next; ++previous) {
      if (forcedPrefix[next] - forcedPrefix[previous + 1] == 0) {
        ways[next] += ways[previous] * primitive[next - previous + 1] % mod;
        ways[next] %= mod;
      }
    }
  }
  cout << ways[n - 1] << '\n';
}
```

时间 $O(N^2)$，空间 $O(N)$。通配符取真时成为某段端点，取假时位于段内部。

## 变种四：模数由输入给出且可能为合数

核心递推只用加、减、乘与阶乘，不依赖除法或逆元，因此把模数参数化即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long modulus;
  string s;
  cin >> n >> modulus >> s;
  if (modulus == 1 || s.front() != 'o' || s.back() != 'o') {
    cout << 0 << '\n';
    return 0;
  }
  vector<long long> factorial(n + 1, 1), primitive(n + 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = static_cast<__int128>(factorial[i - 1]) * i % modulus;
  }
  for (int length = 2; length <= n; ++length) {
    primitive[length] = factorial[length];
    for (int block = 2; block < length; ++block) {
      long long subtract =
          static_cast<__int128>(primitive[block]) * factorial[length - block + 1] % modulus;
      primitive[length] = (primitive[length] - subtract + modulus) % modulus;
    }
  }
  long long answer = 1 % modulus;
  int previous = 0;
  for (int i = 1; i < n; ++i) {
    if (s[i] == 'o') {
      answer = static_cast<__int128>(answer) * primitive[i - previous + 1] % modulus;
      previous = i;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N^2)$，空间 $O(N)$；用 `__int128` 支持 64 位模数乘法。

## 可复现验证

- 三组官方样例分别得到 2、0、1627648。
- 对 $1\le N\le9$ 的全部排列，直接计算每个 $k$ 的位置跨度，按得到的完整 `o/x` 模式计数；与 $d_n$ 递推和相邻真位置乘积对每种模式逐项一致。
- 所有完整代码按 GNU++23 编译。

## 来源

- [AtCoder 官方题面](https://atcoder.jp/contests/abc468/tasks/abc468_g?lang=en)
- [AtCoder 官方题解](https://atcoder.jp/contests/abc468/editorial/23741)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
- [AtCoder Problems](https://kenkoooo.com/atcoder/#/table/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_g?lang=en)
- [对应知识专题](../../math/combinatorial-counting.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-61-lc41/">[力扣 Top 61] LC 41 缺失的第一个正数 困难 →</a>
</nav>
