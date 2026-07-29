---
title: "[atcoder] ABC468 C Between P and Q"
---

# [atcoder] ABC468 C Between P and Q

<p class="daily-archive-kicker">2026-07-28 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../math/permutation-ranking/">进入知识专题</a></p>

## Official source and metadata

- Complete official English statement: [打开 AtCoder 页面](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- Copyright terms: [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en)
- Contest: AtCoder Beginner Contest 468
- Task alias: ABC468 C
- Official title: Between P and Q
- Official task score: 300 points
- Official difficulty label: not provided by AtCoder
- Official contest rated range: 0–1999
- AtCoder Problems community-estimated difficulty: 282
- Community estimate retrieved: 2026-07-28
- Time limit: 2 seconds
- Memory limit: 1024 MiB
- Official statement images: none
- Program interface: GNU++23 full program.

!!! info "Official source and copyright"
    AtCoder is the authoritative source. Ordinary AtCoder contest statements do not carry a confirmed blanket republication licence, so the complete English statement below is independently written from the official task while preserving its full semantics, data contract, constraints, and examples.

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

## Constraint-driven observations

There are $N!$ permutations. Since $10!=3\,628\,800$, direct enumeration is already feasible and gives a trustworthy baseline. However, enumeration recomputes almost the same lexicographic information for every permutation.

Lexicographic order gives every permutation a unique zero-based rank. If `rank(X)` denotes the number of permutations lexicographically smaller than $X$, then

$$
\#\{R:P<R<Q\}=
\max\!\left(0,\operatorname{rank}(Q)-\operatorname{rank}(P)-1\right).
$$

The subtraction by one removes the lower endpoint $P$; $Q$ is already excluded because `rank(Q)` counts only permutations smaller than $Q$.

All ranks fit in 32-bit signed integers for $N\le10$, but `long long` keeps factorial arithmetic and follow-up extensions explicit.

## Sample walkthrough

For $N=3$, the lexicographic order is

$$
123,\ 132,\ 213,\ 231,\ 312,\ 321.
$$

Thus `rank(132) = 1` and `rank(312) = 4`. The open interval contains

$$
4-1-1=2
$$

permutations.

For sample 3, the Lehmer contributions are:

- $P$: $2\cdot6!+4\cdot5!+3\cdot4!+1\cdot3!+2\cdot2!=2002$;
- $Q$: $3\cdot6!+0\cdot5!+2\cdot4!+3\cdot3!=2226$.

Therefore the answer is $2226-2002-1=223$.

## Solution 1: enumerate all permutations

Start from $(1,2,\ldots,N)$ and use `next_permutation`. Every permutation is visited exactly once in lexicographic order, so counting those satisfying `P < current && current < Q` is complete and duplicate-free.

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

Time complexity is $O(N!\,N)$ because each comparison and permutation successor can inspect $O(N)$ positions. Extra space is $O(N)$. This passes the official bound, but it does not expose the reusable rank structure.

## Solution 2: Lehmer rank with a used array

At position $i$, suppose exactly $c_i$ unused values are smaller than $X_i$. Choosing any of them makes the first difference smaller than $X$, and the remaining $N-i-1$ values can be arranged in $(N-i-1)!$ ways. Therefore

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

Time complexity is $O(N^2)$ and extra space is $O(N)$.

### Correctness proof

For a fixed position $i$, every permutation first differing from $X$ at $i$ and using a smaller unused value belongs to exactly one of $c_i$ disjoint blocks. Each block has $(N-i-1)!$ suffix arrangements. Summing these blocks over all positions counts every permutation smaller than $X$ once, at its first differing position, proving the rank formula.

Ranks preserve lexicographic order bijectively. Hence ranks strictly between `rank(P)` and `rank(Q)` correspond one-to-one with permutations strictly between $P$ and $Q$. There are `rank(Q) - rank(P) - 1` such integers when $P<Q$, and none otherwise. The algorithm returns exactly that count.

## Solution 3: Lehmer rank with a Fenwick tree

A Fenwick tree stores which values remain unused. The number of unused values below `permutation[i]` becomes a prefix-sum query.

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

Time complexity is $O(N\log N)$ and extra space is $O(N)$. Under $N\le10$, the $O(N^2)$ used-array version is the recommended implementation: it has fewer moving parts, a shorter proof, and smaller constants. The Fenwick form is valuable when the same rank primitive must scale.

## Boundary cases and common mistakes

- $N=1$: the two permutations are identical, so the answer is 0.
- Adjacent permutations have rank difference 1, hence no strict interior point.
- If $P=Q$ or $P>Q$, return 0 rather than a negative value.
- Do not use `abs(rank(P) - rank(Q)) - 1`; the interval is directed.
- Do not include either endpoint.
- At each position, count smaller values that are still unused, not all numerically smaller values.
- Use $(N-i-1)!$, not $(N-i)!$.
- A set does not preserve the order-statistics count efficiently unless augmented; a Fenwick tree does.

## Follow-up 1: return the k-th permutation in the open interval

### New definition

Given one-based $k$, output the $k$-th lexicographic permutation $R$ satisfying $P<R<Q$, or `-1` if fewer than $k$ exist.

### Method

The first valid rank is `rank(P) + 1`. Convert target rank `rank(P) + k` back to a permutation by repeatedly selecting the factorial-number-system digit.

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

Ranking costs $O(N^2)$ and vector-based unranking costs $O(N^2)$; space is $O(N)$. A Fenwick order-statistics tree reduces both to $O(N\log N)$.

## Follow-up 2: endpoints are multiset permutations

### New definition

$P$ and $Q$ contain the same multiset rather than distinct values. For $N\le20$, count distinct multiset permutations strictly between them.

### Why the original formula changes

Rank differences still solve the interval problem, but a suffix with repeated values has

$$
\frac{r!}{\prod_v c_v!}
$$

distinct arrangements rather than $r!$.

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

With $D$ distinct values, time is $O(ND^2)$ in this transparent implementation because each candidate recomputes a multinomial denominator; space is $O(D)$. All counts fit in signed 64-bit integers for $N\le20$ because $20!<2^{63}$.

## Follow-up 3: N is large and only the answer modulo 1e9+7 is needed

### New definition

$N\le2\cdot10^5$, $P$ and $Q$ remain ordinary permutations, and the answer is requested modulo $M=10^9+7$.

### Method

Compare $P$ and $Q$ directly to decide whether the interval is empty. Compute each Lehmer rank modulo $M$ with a Fenwick tree and factorials modulo $M$.

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

Time is $O(N\log N)$ and space is $O(N)$. The direct comparison is essential: modular ranks alone cannot reveal whether the true difference is negative.

## Follow-up 4: only position-allowed permutations count

### New definition

$N\le20$. In addition to $P$ and $Q$, a binary matrix `allowed[i][v]` states whether value $v$ may occupy position $i$. Count valid permutations strictly between the endpoints.

### Why a single rank no longer suffices

Factorial blocks are no longer uniform because position constraints affect future choices. Use subset DP to count valid permutations strictly smaller than a bound.

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

There are $2^N$ used-value masks and at most $N$ transitions per state. Time is $O(N2^N)$ and space is $O(2^N)$. The expression subtracts all valid permutations smaller than $P$ and also removes $P$ itself when it satisfies the constraints.

## Reproducible validation

- Every C++ block is compiled independently as GNU++23 with warnings enabled.
- The three official samples and boundary cases $N=1$, equal endpoints, reversed endpoints, and adjacent permutations are checked directly.
- For small $N$, all permutations are enumerated to compare brute interval counts with used-array and Fenwick Lehmer ranks.
- Rank and unrank are checked as inverse functions over every rank in the tested domains.
- Multiset ranks are compared with sorted unique permutations.
- The modular Fenwick version is compared with exact ranks where factorials fit.
- The position-constraint subset DP is compared with direct enumeration under random allowed matrices.

Validation result: all 7 GNU++23 blocks compiled independently with `-Wall -Wextra -pedantic`; no block contains a tab or blank source line, and every indentation depth is a multiple of two spaces. With fixed seed 20260728, 409113 ordinary permutations had exact used-array rank, Fenwick rank, and rank/unrank inversion; 511281 multiset permutations matched enumerated ranks; 100000 modular-rank cases and 2000 random position-restriction cases matched their exact or brute-force oracles. All 3 official samples passed.

## Sources

- [ABC468 C official statement](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- [ABC468 official contest page](https://atcoder.jp/contests/abc468?lang=en)
- [ABC468 C official editorial](https://atcoder.jp/contests/abc468/tasks/abc468_c/editorial)
- [AtCoder Problems model data](https://kenkoooo.com/atcoder/resources/problem-models.json) (retrieved 2026-07-28)

## Reference

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_c?lang=en)
- [对应知识专题](../../math/permutation-ranking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-21-lc20/">[力扣 Top 21] LC 20 有效的括号 简单 →</a>
</nav>
