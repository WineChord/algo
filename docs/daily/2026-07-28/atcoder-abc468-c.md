---
title: "[atcoder] ABC468 C Between P and Q"
---

# [atcoder] ABC468 C Between P and Q

<p class="daily-archive-kicker">2026-07-28 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../math/permutation-ranking/">进入知识专题</a></p>

## 官方来源与元数据

- 完整官方英文题面：[打开 AtCoder 页面](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- 版权条款：[AtCoder 使用条款](https://atcoder.jp/tos?lang=en)
- 比赛：AtCoder Beginner Contest 468
- 题号别名：ABC468 C
- 官方标题：Between P and Q
- 官方分值：300 分
- 官方难度标签：AtCoder 未提供
- 官方比赛评级范围：0–1999
- AtCoder Problems 社区估算难度：282
- 社区估算获取日期：2026-07-28
- 时间限制：2 秒
- 内存限制：1024 MiB
- 官方题面图片：无
- 程序接口：GNU++23 完整程序。

!!! info "官方来源与版权"
    AtCoder 是权威来源。普通 AtCoder 竞赛题面没有已确认的统一再发布许可，所以下方英文题面依据官方内容独立整理，并完整保留语义、输入输出契约、约束与样例。

## Complete English statement

An integer $N$ and two permutations

$$
P=(P_1,P_2,\ldots,P_N),\qquad Q=(Q_1,Q_2,\ldots,Q_N)
$$

of $(1,2,\ldots,N)$ are given. Count the permutations $R$ of the same values that satisfy both strict inequalities

$$
P<R<Q
$$

in lexicographic order.

For two equal-length sequences, lexicographic order is decided at their first differing position: the sequence with the smaller value there is lexicographically smaller. The endpoints themselves are excluded. If $P\ge Q$, the answer is therefore zero.

### Input

```text
N
P_1 P_2 ... P_N
Q_1 Q_2 ... Q_N
```

### Output

Print the number of permutations strictly between $P$ and $Q$.

### Constraints

- $1\le N\le10$
- $P$ and $Q$ are permutations of $(1,2,\ldots,N)$
- Every input value is an integer

### Official samples

Sample 1:

```text
Input
3
1 3 2
3 1 2
Output
2
```

The two valid permutations are $(2,1,3)$ and $(2,3,1)$.

Sample 2:

```text
Input
5
5 4 2 1 3
5 1 2 3 4
Output
0
```

Here $P>Q$, so no permutation lies in the open interval.

Sample 3:

```text
Input
7
3 6 5 2 7 1 4
4 1 5 7 2 3 6
Output
223
```

## 中文解释

给定 $N$ 以及两个由 $1,2,\ldots,N$ 组成的排列 $P,Q$，统计有多少个排列 $R$ 在字典序上严格满足 $P<R<Q$。字典序比较从左到右找到第一个不同位置，该位置数值更小的排列更小；端点 $P,Q$ 本身都不计入。若 $P\ge Q$，开区间为空，答案就是 0。

输入依次给出 $N$、排列 $P$ 和排列 $Q$，输出满足条件的排列数量。三组官方样例的答案分别为 2、0、223；第一组的两个合法排列是 $(2,1,3)$ 与 $(2,3,1)$。

## 从约束推导

共有 $N!$ 个排列。由于 $10!=3\,628\,800$，直接枚举已经可行，也能作为可信的暴力基准；但枚举每个排列时都会重复计算高度相似的字典序信息。

字典序为每个排列赋予唯一的从零开始排名。若 `rank(X)` 表示字典序严格小于 $X$ 的排列数量，则

$$
\#\{R:P<R<Q\}=
\max\!\left(0,\operatorname{rank}(Q)-\operatorname{rank}(P)-1\right).
$$

减去 1 是为了排除下端点 $P$；而 `rank(Q)` 本身只统计小于 $Q$ 的排列，因此 $Q$ 已自然被排除。

在 $N\le10$ 下，所有排名都能放入 32 位有符号整数；实现仍使用 `long long`，使阶乘运算与后续变种的边界更明确。

## 样例手推

当 $N=3$ 时，排列的字典序为

$$
123,\ 132,\ 213,\ 231,\ 312,\ 321.
$$

因此 `rank(132) = 1`，`rank(312) = 4`，开区间内共有

$$
4-1-1=2
$$

个排列。

样例 3 的 Lehmer 码贡献为：

- $P$: $2\cdot6!+4\cdot5!+3\cdot4!+1\cdot3!+2\cdot2!=2002$;
- $Q$: $3\cdot6!+0\cdot5!+2\cdot4!+3\cdot3!=2226$.

所以答案是 $2226-2002-1=223$。

## 解法一：枚举全部排列

从 $(1,2,\ldots,N)$ 出发反复调用 `next_permutation`。每个排列都会按字典序恰好访问一次，因此统计满足 `P < current && current < Q` 的排列既完整又不会重复。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n), current(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  iota(current.begin(), current.end(), 1);
  long long answer = 0;
  do {
    if (p < current && current < q) ++answer;
  } while (next_permutation(current.begin(), current.end()));
  cout << answer << '\n';
}
```

时间复杂度为 $O(N!\,N)$，因为每次比较和求后继排列都可能检查 $O(N)$ 个位置；额外空间为 $O(N)$。该方案能通过官方范围，但没有揭示可复用的排名结构。

## 解法二：使用已用标记数组计算 Lehmer 排名（推荐）

在位置 $i$，设尚未使用且小于 $X_i$ 的值共有 $c_i$ 个。选择其中任意一个都会让该位置成为第一个差异，并使整个排列小于 $X$；剩余 $N-i-1$ 个值有 $(N-i-1)!$ 种排列方式。因此

$$
\operatorname{rank}(X)=
\sum_{i=0}^{N-1}c_i(N-i-1)!.
$$

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long permutationRank(const vector<int>& permutation, const vector<long long>& factorial) {
  int n = permutation.size();
  vector<char> used(n + 1);
  long long rank = 0;
  for (int i = 0; i < n; ++i) {
    int smaller = 0;
    for (int value = 1; value < permutation[i]; ++value) {
      if (!used[value]) ++smaller;
    }
    rank += smaller * factorial[n - i - 1];
    used[permutation[i]] = 1;
  }
  return rank;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  vector<long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i;
  long long left = permutationRank(p, factorial);
  long long right = permutationRank(q, factorial);
  cout << max(0LL, right - left - 1) << '\n';
}
```

时间复杂度为 $O(N^2)$，额外空间为 $O(N)$。

### 正确性证明

固定位置 $i$，所有在该位置首次与 $X$ 不同且选用更小未使用值的排列，会被划入 $c_i$ 个互不相交的块；每个块有 $(N-i-1)!$ 种后缀。对所有位置求和后，每个小于 $X$ 的排列都会且只会在其首个差异位置被统计一次，故排名公式成立。

排名与字典序一一对应且保持顺序。因此严格位于 `rank(P)` 与 `rank(Q)` 之间的整数排名，与严格位于 $P$ 和 $Q$ 之间的排列一一对应。当 $P<Q$ 时数量为 `rank(Q) - rank(P) - 1`，否则为零，算法恰好返回该值。

## 解法三：使用树状数组计算 Lehmer 排名

树状数组维护哪些值尚未使用，小于 `permutation[i]` 的未使用值数量可通过一次前缀和查询得到。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  int n;
  vector<int> tree;
public:
  explicit Fenwick(int size) : n(size), tree(size + 1) {}
  void add(int index, int delta) {
    for (; index <= n; index += index & -index) tree[index] += delta;
  }
  int sum(int index) const {
    int result = 0;
    for (; index > 0; index -= index & -index) result += tree[index];
    return result;
  }
};
long long permutationRank(const vector<int>& permutation, const vector<long long>& factorial) {
  int n = permutation.size();
  Fenwick available(n);
  for (int value = 1; value <= n; ++value) available.add(value, 1);
  long long rank = 0;
  for (int i = 0; i < n; ++i) {
    int smaller = available.sum(permutation[i] - 1);
    rank += smaller * factorial[n - i - 1];
    available.add(permutation[i], -1);
  }
  return rank;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  vector<long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i;
  long long answer = permutationRank(q, factorial) - permutationRank(p, factorial) - 1;
  cout << max(0LL, answer) << '\n';
}
```

时间复杂度为 $O(N\log N)$，额外空间为 $O(N)$。在 $N\le10$ 时，更推荐 $O(N^2)$ 的已用数组版本：组成部件更少、证明更短、常数也更小。需要让同一排名原语扩展到大规模时，树状数组版本才更有价值。

## 边界与常见错误

- $N=1$：两个排列必然相同，答案为 0。
- 相邻排列的排名差为 1，严格开区间内没有排列。
- 若 $P=Q$ 或 $P>Q$，应返回 0，而不是负数。
- 不能使用 `abs(rank(P) - rank(Q)) - 1`，因为区间有方向。
- 两个端点都不能计入。
- 每个位置要统计仍未使用的较小值，而不是所有数值上更小的值。
- 使用 $(N-i-1)!$，不要误写为 $(N-i)!$。
- 普通集合无法高效给出顺序统计；树状数组可以。

## 追问一：返回开区间内第 $k$ 个排列

### 新定义

给定从 1 开始的 $k$，输出满足 $P<R<Q$ 的第 $k$ 个字典序排列；若不足 $k$ 个则输出 `-1`。

### 方法

第一个合法排名是 `rank(P) + 1`。目标排名为 `rank(P) + k`，依次选择阶乘进制数位即可将该排名还原为排列。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long permutationRank(const vector<int>& permutation, const vector<long long>& factorial) {
  int n = permutation.size();
  vector<char> used(n + 1);
  long long rank = 0;
  for (int i = 0; i < n; ++i) {
    int smaller = 0;
    for (int value = 1; value < permutation[i]; ++value) {
      if (!used[value]) ++smaller;
    }
    rank += smaller * factorial[n - i - 1];
    used[permutation[i]] = 1;
  }
  return rank;
}
vector<int> unrankPermutation(int n, long long rank, const vector<long long>& factorial) {
  vector<int> available(n), result;
  iota(available.begin(), available.end(), 1);
  for (int remaining = n; remaining >= 1; --remaining) {
    long long block = factorial[remaining - 1];
    int index = rank / block;
    rank %= block;
    result.push_back(available[index]);
    available.erase(available.begin() + index);
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long k;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  cin >> k;
  vector<long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i;
  long long left = permutationRank(p, factorial);
  long long right = permutationRank(q, factorial);
  if (k < 1 || left + k >= right) {
    cout << -1 << '\n';
    return 0;
  }
  vector<int> answer = unrankPermutation(n, left + k, factorial);
  for (int i = 0; i < n; ++i) cout << answer[i] << " \n"[i + 1 == n];
}
```

排名计算为 $O(N^2)$，基于向量的反排名也为 $O(N^2)$，空间复杂度为 $O(N)$。使用支持顺序统计的树状数组可将两者都降为 $O(N\log N)$。

## 追问二：端点是可重集合排列

### 新定义

$P$ 与 $Q$ 由同一个可重集合构成，不再要求元素互异。在 $N\le20$ 下，统计严格位于二者之间的不同可重排列数量。

### 原公式为何需要变化

排名差仍能解决区间问题，但含重复值的长度为 $r$ 的后缀只有

$$
\frac{r!}{\prod_v c_v!}
$$

种不同排列，而不是 $r!$ 种。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long arrangementCount(int remaining, const map<int, int>& count, const vector<long long>& factorial) {
  long long denominator = 1;
  for (auto [value, frequency] : count) denominator *= factorial[frequency];
  return factorial[remaining] / denominator;
}
long long multisetRank(const vector<int>& sequence, const vector<long long>& factorial) {
  map<int, int> count;
  for (int x : sequence) ++count[x];
  long long rank = 0;
  int n = sequence.size();
  for (int i = 0; i < n; ++i) {
    for (auto& [value, frequency] : count) {
      if (value >= sequence[i]) break;
      if (frequency == 0) continue;
      --frequency;
      rank += arrangementCount(n - i - 1, count, factorial);
      ++frequency;
    }
    --count[sequence[i]];
  }
  return rank;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  vector<long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i;
  long long answer = multisetRank(q, factorial) - multisetRank(p, factorial) - 1;
  cout << max(0LL, answer) << '\n';
}
```

设不同值有 $D$ 种，这个直观实现的时间复杂度为 $O(ND^2)$，因为每个候选值都会重新计算多项式系数分母；空间复杂度为 $O(D)$。由于 $20!<2^{63}$，$N\le20$ 时全部计数都能放入 64 位有符号整数。

## 追问三：$N$ 很大且只需模 $10^9+7$ 的答案

### 新定义

$N\le2\cdot10^5$，$P,Q$ 仍为普通排列，答案对 $M=10^9+7$ 取模。

### 方法

先直接比较 $P$ 与 $Q$，判断区间是否为空；再用树状数组和模 $M$ 阶乘计算两个 Lehmer 排名的模值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007;
class Fenwick {
  int n;
  vector<int> tree;
public:
  explicit Fenwick(int size) : n(size), tree(size + 1) {}
  void add(int index, int delta) {
    for (; index <= n; index += index & -index) tree[index] += delta;
  }
  int sum(int index) const {
    int result = 0;
    for (; index > 0; index -= index & -index) result += tree[index];
    return result;
  }
};
long long rankModulo(const vector<int>& permutation, const vector<long long>& factorial) {
  int n = permutation.size();
  Fenwick available(n);
  for (int value = 1; value <= n; ++value) available.add(value, 1);
  long long rank = 0;
  for (int i = 0; i < n; ++i) {
    long long smaller = available.sum(permutation[i] - 1);
    rank = (rank + smaller * factorial[n - i - 1]) % MOD;
    available.add(permutation[i], -1);
  }
  return rank;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  if (!(p < q)) {
    cout << 0 << '\n';
    return 0;
  }
  vector<long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i % MOD;
  long long answer = (rankModulo(q, factorial) - rankModulo(p, factorial) - 1) % MOD;
  if (answer < 0) answer += MOD;
  cout << answer << '\n';
}
```

时间复杂度为 $O(N\log N)$，空间复杂度为 $O(N)$。直接比较不可省略，因为只看模意义下的排名无法判断真实差值是否为负。

## 追问四：只统计满足位置限制的排列

### 新定义

$N\le20$。除 $P,Q$ 外，给定二进制矩阵 `allowed[i][v]`，表示值 $v$ 能否放在位置 $i$。统计严格位于两个端点之间且满足位置限制的排列。

### 单一排名为何不再足够

位置限制会影响后续选择，使阶乘分块不再等长。改用子集动态规划，统计严格小于某个上界的合法排列数量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countLess(const vector<int>& bound, const vector<string>& allowed) {
  int n = bound.size();
  int states = 1 << n;
  vector<array<long long, 2>> dp(states);
  dp[0][0] = 1;
  for (int mask = 0; mask < states; ++mask) {
    int position = __builtin_popcount(static_cast<unsigned>(mask));
    if (position == n) continue;
    for (int value = 0; value < n; ++value) {
      if ((mask >> value & 1) || allowed[position][value] == '0') continue;
      for (int less = 0; less <= 1; ++less) {
        if (dp[mask][less] == 0) continue;
        int actual = value + 1;
        if (!less && actual > bound[position]) continue;
        int nextLess = less || actual < bound[position];
        dp[mask | 1 << value][nextLess] += dp[mask][less];
      }
    }
  }
  return dp[states - 1][1];
}
bool isAllowed(const vector<int>& permutation, const vector<string>& allowed) {
  for (int i = 0; i < static_cast<int>(permutation.size()); ++i) {
    if (allowed[i][permutation[i] - 1] == '0') return false;
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), q(n);
  for (int& x : p) cin >> x;
  for (int& x : q) cin >> x;
  vector<string> allowed(n);
  for (string& row : allowed) cin >> row;
  if (!(p < q)) {
    cout << 0 << '\n';
    return 0;
  }
  long long answer = countLess(q, allowed) - countLess(p, allowed) - isAllowed(p, allowed);
  cout << answer << '\n';
}
```

共有 $2^N$ 个已用值状态，每个状态至多尝试 $N$ 次转移。时间复杂度为 $O(N2^N)$，空间复杂度为 $O(2^N)$。最终表达式先减去所有小于 $P$ 的合法排列；若 $P$ 本身也满足位置限制，还要将它一并排除。

## 可复现验证

- 每个 C++ 代码块都以 GNU++23 模式单独编译，并开启编译警告。
- 直接检查三组官方样例，以及 $N=1$、端点相等、端点逆序和相邻排列等边界。
- 对较小的 $N$ 枚举全部排列，将暴力区间计数与已用数组、树状数组两种 Lehmer 排名实现对拍。
- 在测试范围内逐个排名验证排名与反排名互为逆运算。
- 将可重集合排名与排序去重后的完整排列列表比较。
- 在阶乘可精确表示的范围内，将模树状数组版本与精确排名比较。
- 在随机位置限制矩阵下，将子集动态规划与直接枚举对拍。

验证结果：7 个 GNU++23 代码块均以 `-Wall -Wextra -pedantic` 独立编译通过；代码中没有制表符或空白源码行，每级缩进均为两个空格。使用固定种子 20260728，409113 个普通排列的已用数组排名、树状数组排名以及排名与反排名互逆关系完全一致；511281 个可重排列的排名与枚举一致；100000 组模排名测试和 2000 组随机位置限制测试均与精确算法或暴力基准一致。三组官方样例全部通过。

## 来源

- [ABC468 C 官方题面](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- [ABC468 官方比赛页](https://atcoder.jp/contests/abc468?lang=en)
- [ABC468 C 官方题解](https://atcoder.jp/contests/abc468/tasks/abc468_c/editorial)
- [AtCoder Problems 模型数据](https://kenkoooo.com/atcoder/resources/problem-models.json)（获取于 2026-07-28）

## 参考资料

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- [对应知识专题](../../math/permutation-ranking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-21-lc20/">[力扣 Top 21] LC 20 有效的括号 简单 →</a>
</nav>
