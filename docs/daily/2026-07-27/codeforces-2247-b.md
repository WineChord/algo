---
title: "[codeforces] CF Round 1111 Div.2 B Yet Another Constructive"
---

# [codeforces] CF Round 1111 Div.2 B Yet Another Constructive

<p class="daily-archive-kicker">2026-07-27 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../math/modular-constructions/">进入知识专题</a></p>

Official problem: [Open the official problem](https://codeforces.com/problemset/problem/2247/B)

## Official source record

- Platform and contest: Codeforces, Codeforces Round 1111 (Div. 2).
- Contest ID: 2247.
- Official task identity: Div.2 B, title “Yet Another Constructive”.
- Cross-division aliases: none found in the official problemset API; the title maps only to contest 2247, index B.
- Official task points: 750.
- Official problem rating: unavailable in the current official API; it must not be inferred from index B.
- Official tags: `constructive algorithms`.
- Limits: 1.5 seconds, 256 MB.
- Program interface: GNU++23 full program.
- Official statement images: none.

## Complete statement semantics

For each test case, given $n,k,m$, construct a positive integer array $a_1,\ldots,a_n$ such that the minimum length of a nonempty contiguous subarray whose sum is divisible by $m$ is exactly $k$.

Equivalently:

1. at least one length-$k$ subarray has sum divisible by $m$; and
2. no nonempty subarray of length less than $k$ has sum divisible by $m$.

Print any valid array with $1\le a_i\le10^{18}$, or print `NO` if none exists.

### Input

```text
t
n k m
...
```

### Output

For every test case:

- print `NO` if construction is impossible; or
- print `YES`, then a valid array of $n$ integers.

Letter case is ignored.

### All official constraints

- $1\le t\le10^4$.
- $1\le k\le n\le2\cdot10^5$.
- $1\le m\le10^9$.
- The sum of $n$ over all test cases is at most $2\cdot10^5$.
- Every output value must lie in $[1,10^{18}]$.

### Official sample

```text
Input
4
1 1 1
5 3 5
2 2 1000000000
6 4 3
Output
YES
1
YES
9 17 14 23 11
YES
500000000 500000000
NO
```

The output is non-unique. In test 2, `[9,17,14]` sums to 40, divisible by 5, while no shorter subarray is divisible by 5. Test 4 is impossible.

## 中文题意与样例说明

每组给定 $n,k,m$，需要构造一个长度为 $n$ 的正整数数组，使“和能被 $m$ 整除”的最短非空连续子数组长度恰好为 $k$。这同时要求至少存在一个长度为 $k$ 的合法区间，并且所有更短的非空区间都不合法。每个输出元素必须在 $[1,10^{18}]$ 内；无解输出 `NO`，否则输出 `YES` 与任意一个合法数组。

样例输出不是唯一答案。第二组中 `[9,17,14]` 的和为 40，可被 5 整除，同时不存在更短的可整除区间；第四组无解。输入输出结构、全部约束和逐字符样例数据以上方官方英文信息为准。

## Prefix-residue model

Let

$$
p_0=0,\qquad p_i=\sum_{j=1}^{i}a_j\bmod m.
$$

Subarray $[l,r]$ has sum divisible by $m$ exactly when $p_{l-1}=p_r$. Therefore the shortest divisible-subarray length is exactly the minimum index distance between equal prefix residues.

This translation removes the distracting magnitude bound: every residue increment can be represented by a positive value in $[1,m]$, already far below $10^{18}$.

## Necessary condition

No divisible subarray may have length below $k$, so the first $k$ prefix residues

$$
p_0,p_1,\ldots,p_{k-1}
$$

must be pairwise distinct. Only $m$ residues exist. By the pigeonhole principle,

$$
k\le m
$$

is necessary.

## Solution 1: exhaustive residue-array search

For a conceptual brute force, enumerate every array whose values are in $[1,m]$, then test all subarrays. Restricting to $[1,m]$ is complete because these values realize every possible increment modulo $m$.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
bool good(const vector<long long>& a, int k, long long m) {
  int n = a.size();
  int best = n + 1;
  for (int l = 0; l < n; ++l) {
    long long sum = 0;
    for (int r = l; r < n; ++r) {
      sum = (sum + a[r]) % m;
      if (sum == 0) best = min(best, r - l + 1);
    }
  }
  return best == k;
}
bool searchArray(int i, vector<long long>& a, int k, long long m) {
  if (i == (int)a.size()) return good(a, k, m);
  for (long long value = 1; value <= m; ++value) {
    a[i] = value;
    if (searchArray(i + 1, a, k, m)) return true;
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, k;
    long long m;
    cin >> n >> k >> m;
    vector<long long> a(n);
    if (!searchArray(0, a, k, m)) {
      cout << "NO\n";
      continue;
    }
    cout << "YES\n";
    for (int i = 0; i < n; ++i) cout << a[i] << " \n"[i + 1 == n];
  }
}
```

- Time: $O(m^n n^2)$.
- Extra space: $O(n)$ excluding recursion overhead.
- Bottleneck: the brute force searches sequences instead of exploiting the equal-prefix-residue structure.

## Solution 2: repeat a positive block of sum $m$ — recommended

When $k\le m$, split $m$ into $k$ positive integers and repeat that block. A balanced split uses

$$
q=\left\lfloor\frac{m}{k}\right\rfloor,\qquad r=m\bmod k,
$$

with $k-r$ copies of $q$ and $r$ copies of $q+1$.

Every $k$ consecutive values form one rotation of the block, so their sum is exactly $m$. Every shorter consecutive segment in the infinite periodic sequence omits at least one positive block element, so its sum lies strictly between 0 and $m$ and cannot be divisible by $m$.

### Correctness proof

- If $k>m$, the pigeonhole argument proves impossibility, so `NO` is correct.
- If $k\le m$, $q\ge1$, hence every constructed element is positive.
- Period $k$ makes each length-$k$ window contain every block element exactly once, with sum $m$, so a divisible window of length $k$ exists.
- Any window of length $d<k$ is a proper cyclic segment of the positive block. Its sum is positive and strictly less than the full block sum $m$, so it is not divisible by $m$.

Thus the minimum divisible length is exactly $k$.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, k;
    long long m;
    cin >> n >> k >> m;
    if (k > m) {
      cout << "NO\n";
      continue;
    }
    long long q = m / k;
    int r = m % k;
    vector<long long> block(k, q);
    for (int i = k - r; i < k; ++i) ++block[i];
    cout << "YES\n";
    for (int i = 0; i < n; ++i) cout << block[i % k] << " \n"[i + 1 == n];
  }
}
```

- Time: $O(n)$ per test case; $O(\sum n)$ overall.
- Extra space: $O(k)$, reducible to $O(1)$ by generating values from the index.
- Output bound: $\max a_i=\lceil m/k\rceil\le10^9$.
- Recommendation: remember “equal prefix residues encode divisible subarrays” for the necessity proof, and “repeat a positive composition of $m$” for the construction. The balanced composition minimizes the largest generated element.

## Same-order alternative: sparse jump block

The block

$$
[1,1,\ldots,1,m-k+1]
$$

also consists of $k$ positive values summing to $m$. It gives a particularly short implementation but can use a much larger maximum value than the balanced block.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, k;
    long long m;
    cin >> n >> k >> m;
    if (k > m) {
      cout << "NO\n";
      continue;
    }
    cout << "YES\n";
    for (int i = 0; i < n; ++i) {
      long long value = i % k == k - 1 ? m - k + 1 : 1;
      cout << value << " \n"[i + 1 == n];
    }
  }
}
```

- Time: $O(n)$.
- Extra space: $O(1)$.
- Trade-off: simplest generator, but maximum value $m-k+1$ instead of $\lceil m/k\rceil$.

## Common mistakes

- Testing only whether one length-$k$ subarray is divisible and ignoring shorter windows.
- Looking at array values modulo $k$ instead of prefix sums modulo $m$.
- Claiming impossibility from $n>m$; repeats are allowed once their distance reaches $k$.
- Constructing a block with zero entries; all output values must be positive.
- Forgetting $k=1$: outputting $m$ works because each one-element window is divisible.
- Printing values outside $10^{18}$; the construction never exceeds $m$.
- Inferring an official Codeforces rating when the API field is absent.

## Follow-up 1: impose an element cap $B$

**New definition.** Require $1\le a_i\le B$.

Necessity:

- Prefix residues still require $k\le m$.
- A length-$k$ divisible subarray has positive sum at least $m$, but its sum is at most $kB$, so $m\le kB$.

These conditions are sufficient: a balanced positive composition of $m$ has maximum $\lceil m/k\rceil\le B$.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, k;
    long long m, b;
    cin >> n >> k >> m >> b;
    if (k > m || (__int128)k * b < m) {
      cout << "NO\n";
      continue;
    }
    long long q = m / k;
    int r = m % k;
    cout << "YES\n";
    for (int i = 0; i < n; ++i) {
      int j = i % k;
      long long value = q + (j >= k - r);
      cout << value << " \n"[i + 1 == n];
    }
  }
}
```

- Time: $O(n)$.
- Extra space: $O(1)$.
- Existence criterion: $k\le m\le kB$.

## Follow-up 2: lexicographically smallest period block of sum $m$

**New definition.** Among positive length-$k$ blocks whose sum is exactly $m$, output the lexicographically smallest block and repeat it.

Make every early position as small as possible: the first $k-1$ values are 1, and the last receives the remainder $m-k+1$.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  long long m;
  cin >> n >> k >> m;
  if (k > m) {
    cout << "NO\n";
    return 0;
  }
  cout << "YES\n";
  for (int i = 0; i < n; ++i) {
    int j = i % k;
    long long value = j + 1 == k ? m - k + 1 : 1;
    cout << value << " \n"[i + 1 == n];
  }
}
```

- Time: $O(n)$.
- Extra space: $O(1)$.

## Follow-up 3: count periodic sum-$m$ constructions

**New definition.** Count positive ordered length-$k$ blocks whose sum is exactly $m$, modulo $10^9+7$. Assume $m\le2\cdot10^5$.

By stars and bars, the count is

$$
\binom{m-1}{k-1}
$$

when $k\le m$, and zero otherwise. Repeating any such block yields a valid original construction.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
long long power(long long a, long long e) {
  long long result = 1;
  while (e) {
    if (e & 1) result = result * a % mod;
    a = a * a % mod;
    e >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, k;
  cin >> m >> k;
  if (k > m) {
    cout << 0 << '\n';
    return 0;
  }
  vector<long long> fact(m + 1, 1), invFact(m + 1, 1);
  for (int i = 1; i <= m; ++i) fact[i] = fact[i - 1] * i % mod;
  invFact[m] = power(fact[m], mod - 2);
  for (int i = m; i >= 1; --i) invFact[i - 1] = invFact[i] * i % mod;
  long long answer = fact[m - 1] * invFact[k - 1] % mod * invFact[m - k] % mod;
  cout << answer << '\n';
}
```

- Time: $O(m+\log\text{MOD})$.
- Extra space: $O(m)$.

## Follow-up 4: verify an arbitrary array and recover a witness

**New definition.** Given a positive integer array, return the shortest divisible-subarray length and one one-based witness interval.

For each prefix residue, the closest previous equal residue gives the shortest divisible subarray ending at the current position. Tracking only the latest occurrence is therefore sufficient.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long m;
  cin >> n >> m;
  unordered_map<long long, int> last;
  last.reserve(2 * n + 1);
  last[0] = 0;
  long long prefix = 0;
  int best = n + 1;
  int answerL = -1;
  int answerR = -1;
  for (int i = 1; i <= n; ++i) {
    long long value;
    cin >> value;
    prefix = (prefix + value % m) % m;
    auto it = last.find(prefix);
    if (it != last.end() && i - it->second < best) {
      best = i - it->second;
      answerL = it->second + 1;
      answerR = i;
    }
    last[prefix] = i;
  }
  if (answerL == -1) {
    cout << -1 << '\n';
  } else {
    cout << best << ' ' << answerL << ' ' << answerR << '\n';
  }
}
```

- Expected time: $O(n)$.
- Extra space: $O(\min(n,m))$.

## Follow-up 5: streaming shortest length after every append

**New definition.** Positive values arrive online. After each append, output the shortest divisible-subarray length seen so far, or `-1`.

Update one prefix residue and its latest occurrence; the global minimum can only decrease.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long m;
  cin >> n >> m;
  unordered_map<long long, int> last;
  last.reserve(2 * n + 1);
  last[0] = 0;
  long long prefix = 0;
  int best = n + 1;
  for (int i = 1; i <= n; ++i) {
    long long value;
    cin >> value;
    prefix = (prefix + value % m) % m;
    auto it = last.find(prefix);
    if (it != last.end()) best = min(best, i - it->second);
    last[prefix] = i;
    cout << (best == n + 1 ? -1 : best) << " \n"[i == n];
  }
}
```

- Expected update time: $O(1)$.
- Extra space: $O(\min(n,m))$.

## Follow-up 6: generate a randomized valid construction

**New definition.** Produce varied deterministic test data from a supplied seed.

Choose $k-1$ distinct cut positions in $[1,m-1]$; adjacent differences form a random positive composition of $m$. Floyd’s sampling algorithm selects the cuts in $O(k)$ expected time without iterating to $m$.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  long long m;
  unsigned long long seed;
  cin >> n >> k >> m >> seed;
  if (k > m) {
    cout << "NO\n";
    return 0;
  }
  mt19937_64 rng(seed);
  long long population = m - 1;
  long long sample = k - 1;
  unordered_set<long long> selected;
  selected.reserve(2 * k + 1);
  for (long long j = population - sample + 1; j <= population; ++j) {
    long long candidate = rng() % j + 1;
    if (selected.count(candidate)) {
      selected.insert(j);
    } else {
      selected.insert(candidate);
    }
  }
  vector<long long> cuts(selected.begin(), selected.end());
  sort(cuts.begin(), cuts.end());
  vector<long long> block;
  long long previous = 0;
  for (long long cut : cuts) {
    block.push_back(cut - previous);
    previous = cut;
  }
  block.push_back(m - previous);
  cout << "YES\n";
  for (int i = 0; i < n; ++i) cout << block[i % k] << " \n"[i + 1 == n];
}
```

- Expected time: $O(k\log k+n)$.
- Extra space: $O(k)$.

## Reproducible verification plan

- Compile every program in C++23 mode.
- Exhaustively test small $1\le k\le n\le10$, $1\le m\le10$: verify the construction exactly when $k\le m$, then enumerate all subarrays to confirm the shortest divisible length.
- Randomly test the balanced, sparse-jump, capped, and randomized-composition generators against the same $O(n^2)$ checker.
- Randomly compare the hash-map witness/stream algorithms against complete subarray enumeration.

## Sources

- Official problem: [Open the official problem](https://codeforces.com/problemset/problem/2247/B)
- Official contest: [Open the official contest](https://codeforces.com/contest/2247)
- Official contest API: [Open the official contest](https://codeforces.com/api/contest.list?gym=false)
- Official problemset API: [Open the official problem](https://codeforces.com/api/problemset.problems)

## Reference

- [官方题目](https://codeforces.com/problemset/problem/2247/B)
- [对应知识专题](../../math/modular-constructions.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-511-q2-lc3997/">← [力扣竞赛] 第 511 场周赛 Q2 LC 3997 统计二叉树中支配节点的数量 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-27-lc1464/">[力扣每日一题] 2026-07-27｜LC 1464 数组中两元素的最大乘积 →</a>
</nav>
