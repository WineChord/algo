---
title: "[codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence"
---

# [codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence

<p class="daily-archive-kicker">2026-07-28 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

## Official source and metadata

- Complete official English statement: [打开 Codeforces 页面](https://codeforces.com/contest/2247/problem/C)
- Contest: Codeforces Round 1111 (Div. 2)
- Contest ID: 2247
- Task alias: Div.2 C
- Official title: Inversion of a Subsequence
- Official points: 1250
- Official problem rating: unknown; the current Codeforces API problem object omits `rating`
- Official tags: `greedy`, `math`
- Contest status: finished
- Contest time in Asia/Shanghai: 2026-07-18 22:35 to 2026-07-19 00:35
- Time limit: 2 seconds
- Memory limit: 256 megabytes
- Official statement images: none
- Program interface: GNU++23 full program, multiple test cases.

## Faithful complete statement semantics

Two binary arrays $a$ and $b$ of length $n$ are given. One operation on the current array $a$ is:

1. choose a nonempty subsequence, equivalently a nonempty set of indices
   $1\le i_1<i_2<\cdots<i_k\le n$;
2. require the selected current values to have odd sum;
3. invert every selected bit: $a_{i_j}\gets1-a_{i_j}$.

The operation may be used any number of times. Find the minimum number of operations needed to turn $a$ into $b$, or print `-1` if the transformation is impossible.

### Input

The first line contains the number of test cases $t$. Each test case contains:

```text
n
a_1 a_2 ... a_n
b_1 b_2 ... b_n
```

### Output

For each test case, print the minimum number of operations, or `-1`.

### Constraints

- $1\le t\le10^4$
- $1\le n\le2\cdot10^5$
- $a_i,b_i\in\{0,1\}$
- the sum of $n$ over all test cases does not exceed $2\cdot10^5$

### Official sample

```text
Input
5
1
0
0
2
1 0
0 1
3
1 1 1
0 0 0
4
1 0 1 0
0 1 0 1
5
1 0 1 0 1
1 1 1 1 1
Output
0
1
1
2
-1
```

- Case 1 already satisfies $a=b$.
- In case 2, selecting both positions has current sum $1$ and swaps `1 0` into `0 1`.
- In case 3, selecting all three ones has odd sum and solves the case once.
- In case 4, the mismatch set contains two current ones, so one operation is invalid but two suffice.
- In case 5, the nontrivial target is all ones, which no valid final operation can produce.

## Constraint-driven model

Let

$$
D=\{i:a_i\ne b_i\},\qquad
x=\#\{i\in D:a_i=1\}.
$$

If one operation solves the task, it must select exactly $D$: selecting a matching position would make it wrong, and omitting a mismatch would leave it wrong. Such an operation is legal exactly when $x$ is odd.

Two absorbing-boundary observations determine impossibility:

1. If $a$ is all zero and $a\ne b$, no operation is available because every selected sum is zero.
2. If $b$ is all one and $a\ne b$, consider the final operation. It must select exactly the zero positions of the previous state; those selected values sum to zero, so the final operation cannot be legal.

Outside these cases, every transformation needs at most two operations:

- if positive even $x\ge2$, split $D$ into two disjoint sets containing odd numbers of current ones;
- if $x=0$, all mismatches are `0 -> 1`. Since $a$ is not all zero, there is a matched `1`; since $b$ is not all one, there is a matched `0`. Use those two positions as temporary auxiliaries and restore them in the second operation.

Therefore the complete answer is

$$
\begin{cases}
0,&a=b,\\
-1,&a\ne b\text{ and }(\sum a_i=0\text{ or }\sum b_i=n),\\
1,&x\text{ is odd},\\
2,&x\text{ is even}.
\end{cases}
$$

## Brute-force oracle: BFS over all binary states

For a reduced constraint such as $n\le20$, encode the current array as a bitmask. From state `s`, a flip mask `m` is legal exactly when `popcount(s & m)` is odd; the next state is `s ^ m`.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int encode(const vector<int>& bits) {
  int mask = 0;
  for (int i = 0; i < static_cast<int>(bits.size()); ++i) mask |= bits[i] << i;
  return mask;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int start = encode(a), target = encode(b), states = 1 << n;
    vector<int> distance(states, -1);
    queue<int> q;
    distance[start] = 0;
    q.push(start);
    while (!q.empty()) {
      int state = q.front();
      q.pop();
      for (int flip = 1; flip < states; ++flip) {
        if (__builtin_popcount(static_cast<unsigned>(state & flip)) % 2 == 0) continue;
        int next = state ^ flip;
        if (distance[next] != -1) continue;
        distance[next] = distance[state] + 1;
        q.push(next);
      }
    }
    cout << distance[target] << '\n';
  }
}
```

There are $2^n$ states and up to $2^n-1$ masks per state, so time is $O(4^n)$ and space is $O(2^n)$. It is far beyond the official bound but is an excellent exhaustive oracle.

## Optimal O(n) solution

Scan once to determine equality, the number of ones in each array, and $x$, the number of mismatches currently equal to one.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    if (a == b) {
      cout << 0 << '\n';
      continue;
    }
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
      continue;
    }
    int mismatchOnes = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i] && a[i] == 1) ++mismatchOnes;
    }
    cout << (mismatchOnes % 2 == 1 ? 1 : 2) << '\n';
  }
}
```

Time complexity is $O(n)$ per case and $O(\sum n)$ overall. Extra space is $O(n)$ for the input arrays.

### Correctness proof

If $a=b$, zero is clearly optimal. The all-zero source and nontrivial all-one target cases are impossible by the final-operation arguments above.

Assume neither impossible condition holds and $a\ne b$.

- If $x$ is odd, selecting exactly $D$ is legal and solves the task in one operation. Zero operations cannot suffice, so the optimum is one.
- If $x$ is positive and even, choose one mismatch whose current value is one as the first operation. Put every other mismatch in the second operation. The first selected sum is one; the second set is disjoint and contains $x-1$, an odd number, of unchanged current ones. Every mismatch is flipped exactly once, so two operations solve the task. One operation is impossible because $x$ is even.
- If $x=0$, choose a matched zero position $i$ and a matched one position $k$. The first operation selects $D\cup\{i,k\}$ and has selected sum one. After it, position $i$ is one and $k$ is zero, so selecting $\{i,k\}$ is also legal and restores both auxiliaries. Every mismatch remains flipped exactly once. Again, one operation is impossible because $x$ is even.

All cases return the minimum possible value.

## Sample state evolution

For `a = [1,0,1,0]`, `b = [0,1,0,1]`, every position is a mismatch and $x=2$.

- First select position 1: `[1,0,1,0] -> [0,0,1,0]`.
- Then select positions 2, 3, 4. Their current sum is 1:
  `[0,0,1,0] -> [0,1,0,1]`.

The even value $x=2$ rules out one operation, so the optimum is exactly two.

## Boundary cases and common mistakes

- Check `a == b` before the all-zero/all-one impossibility tests; equal all-zero and equal all-one arrays require zero operations.
- Count ones only on mismatch positions when testing the one-operation case.
- The selected values are evaluated in the current state, not always in the original array.
- A subsequence need not be contiguous; any ordered set of indices is allowed.
- For a nontrivial all-one target, inspect the final operation rather than assuming that an existing one can serve as an auxiliary.
- `x = 0` is not automatically impossible; matched zero and one positions make the two-operation construction work.
- Do not simulate arbitrary operations at $n=2\cdot10^5$; the answer depends on four sufficient statistics.

## Follow-up 1: output an optimal sequence of operations

### New definition

When possible, output the actual index sets for a minimum-operation transformation.

### Construction

Use the same proof: the mismatch set for one operation, an odd/odd partition when $x\ge2$ is even, or two matched auxiliaries when $x=0$.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    vector<int> mismatch;
    int mismatchOnes = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i]) {
        mismatch.push_back(i);
        mismatchOnes += a[i];
      }
    }
    if (mismatch.empty()) {
      cout << 0 << '\n';
      continue;
    }
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
      continue;
    }
    vector<vector<int>> operations;
    if (mismatchOnes % 2 == 1) {
      operations.push_back(mismatch);
    } else if (mismatchOnes > 0) {
      vector<int> first, second;
      bool chosenOne = false;
      for (int index : mismatch) {
        if (!chosenOne && a[index] == 1) {
          first.push_back(index);
          chosenOne = true;
        } else {
          second.push_back(index);
        }
      }
      operations = {first, second};
    } else {
      int matchedZero = -1, matchedOne = -1;
      for (int i = 0; i < n; ++i) {
        if (a[i] == b[i] && a[i] == 0) matchedZero = i;
        if (a[i] == b[i] && a[i] == 1) matchedOne = i;
      }
      vector<int> first = mismatch;
      first.push_back(matchedZero);
      first.push_back(matchedOne);
      operations = {first, {matchedZero, matchedOne}};
    }
    cout << operations.size() << '\n';
    for (const vector<int>& operation : operations) {
      cout << operation.size();
      for (int index : operation) cout << ' ' << index + 1;
      cout << '\n';
    }
  }
}
```

Time is $O(n)$ and the output itself uses $O(n)$ space. Each emitted operation is nonempty and has odd current selected sum.

## Follow-up 2: the target changes by point flips

### New definition

Array $a$ is fixed. After each query, one bit of $b$ flips; report the new minimum immediately.

### Method

Maintain four statistics: mismatch count, mismatch positions whose fixed `a` value is one, total ones in $a$, and total ones in $b$.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int answer(int n, int difference, int mismatchOnes, int onesA, int onesB) {
  if (difference == 0) return 0;
  if (onesA == 0 || onesB == n) return -1;
  return mismatchOnes % 2 == 1 ? 1 : 2;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  cin >> n >> queries;
  vector<int> a(n), b(n);
  for (int& x : a) cin >> x;
  for (int& x : b) cin >> x;
  int onesA = accumulate(a.begin(), a.end(), 0);
  int onesB = accumulate(b.begin(), b.end(), 0);
  int difference = 0, mismatchOnes = 0;
  for (int i = 0; i < n; ++i) {
    if (a[i] != b[i]) {
      ++difference;
      mismatchOnes += a[i];
    }
  }
  while (queries--) {
    int position;
    cin >> position;
    --position;
    if (a[position] != b[position]) {
      --difference;
      mismatchOnes -= a[position];
    } else {
      ++difference;
      mismatchOnes += a[position];
    }
    onesB += b[position] == 0 ? 1 : -1;
    b[position] ^= 1;
    cout << answer(n, difference, mismatchOnes, onesA, onesB) << '\n';
  }
}
```

Initialization is $O(n)$; each update and answer is $O(1)$ with $O(n)$ storage for the arrays.

## Follow-up 3: each operation must select exactly two indices

### New definition

Each operation selects exactly two positions, and their current sum must be odd.

### New invariant

The selected bits are one zero and one one. Flipping both simply swaps them, so the total number of ones is invariant. When the totals agree, pair each `1 -> 0` mismatch with one `0 -> 1` mismatch.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA != onesB) {
      cout << -1 << '\n';
      continue;
    }
    int oneToZero = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] == 1 && b[i] == 0) ++oneToZero;
    }
    cout << oneToZero << '\n';
  }
}
```

Time is $O(n)$ and extra space beyond input is $O(1)$. Every operation fixes one mismatch of each direction, proving both feasibility and optimality.

## Follow-up 4: minimum operations first, then minimum weighted flip cost

### New definition

Each index has a positive weight $w_i$. The primary objective remains the minimum number of operations; among all such solutions, minimize the sum of weights of every index occurrence in every operation.

### Method

Every mismatch must be flipped at least once. A one-operation solution and the positive-even-$x$ partition flip every mismatch exactly once. When $x=0$, every two-operation solution must use an odd number of matched ones and an odd number of matched zeros as twice-flipped auxiliaries; choose the cheapest one of each type.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    vector<long long> weight(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    for (long long& x : weight) cin >> x;
    int difference = 0, mismatchOnes = 0;
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    long long mismatchCost = 0;
    long long cheapestMatchedZero = LLONG_MAX;
    long long cheapestMatchedOne = LLONG_MAX;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i]) {
        ++difference;
        mismatchOnes += a[i];
        mismatchCost += weight[i];
      } else if (a[i] == 0) {
        cheapestMatchedZero = min(cheapestMatchedZero, weight[i]);
      } else {
        cheapestMatchedOne = min(cheapestMatchedOne, weight[i]);
      }
    }
    if (difference == 0) {
      cout << "0 0\n";
    } else if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
    } else if (mismatchOnes % 2 == 1) {
      cout << "1 " << mismatchCost << '\n';
    } else if (mismatchOnes > 0) {
      cout << "2 " << mismatchCost << '\n';
    } else {
      long long cost = mismatchCost + 2 * (cheapestMatchedZero + cheapestMatchedOne);
      cout << "2 " << cost << '\n';
    }
  }
}
```

Time is $O(n)$ and extra working space is $O(1)$. With $w_i\le10^9$ and total $n\le2\cdot10^5$, `long long` is sufficient.

## Follow-up 5: each selected subsequence has length at most L

### New definition

The original odd-sum rule remains, but an operation may flip at most $L$ positions. For $n\le18$, find the true minimum.

### Why the closed form fails

The one- and two-operation constructions may use more than $L$ positions. The exact arrangement of mismatches now matters, so retain the complete state and run BFS over legal bounded masks.

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int encode(const vector<int>& bits) {
  int mask = 0;
  for (int i = 0; i < static_cast<int>(bits.size()); ++i) mask |= bits[i] << i;
  return mask;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n, limit;
    cin >> n >> limit;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int states = 1 << n;
    vector<int> masks;
    for (int mask = 1; mask < states; ++mask) {
      if (__builtin_popcount(static_cast<unsigned>(mask)) <= limit) masks.push_back(mask);
    }
    int start = encode(a), target = encode(b);
    vector<int> distance(states, -1);
    queue<int> q;
    distance[start] = 0;
    q.push(start);
    while (!q.empty()) {
      int state = q.front();
      q.pop();
      for (int flip : masks) {
        if (__builtin_popcount(static_cast<unsigned>(state & flip)) % 2 == 0) continue;
        int next = state ^ flip;
        if (distance[next] != -1) continue;
        distance[next] = distance[state] + 1;
        q.push(next);
      }
    }
    cout << distance[target] << '\n';
  }
}
```

Time is

$$
O\!\left(2^n\sum_{k=1}^{L}\binom{n}{k}\right),
$$

and space is $O(2^n)$. This is deliberately a small-$n$ exact solver; the cap destroys the original sufficient-statistics collapse.

## Reproducible validation

- Every code block is compiled independently as GNU++23 with warnings enabled.
- The official five-case sample and explicit boundaries `a == b`, all-zero source, all-one target, $x=0$, $x=1$, and positive even $x$ are checked.
- For every ordered source/target pair through small binary state spaces, the $O(n)$ formula is compared with exhaustive directed BFS.
- Every constructive output is replayed: each selected set is nonempty, has odd current sum, and reaches the target in the claimed minimum.
- The online-update statistics are compared after random target flips with full recomputation.
- The exactly-two-indices formula is compared with its own exhaustive state graph.
- The weighted tie-break formula is compared with exhaustive one- and two-operation enumeration for small $n$ and random positive weights.

Validation result: all 7 GNU++23 blocks compiled independently with `-Wall -Wextra -pedantic`; no block contains a tab or blank source line, and every indentation depth is a multiple of two spaces. Exhaustive directed state graphs through $n=8$ checked 87380 ordered source/target pairs against the closed form, replayed 85874 constructive answers, and checked the exactly-two-indices variant on the same 87380 pairs. With fixed seed 20260728, 500000 online target flips matched full recomputation and 100000 weighted tie-break cases matched exhaustive one- and two-operation enumeration. All 5 official sample cases passed.

## Sources

- [Codeforces 2247C official statement](https://codeforces.com/contest/2247/problem/C)
- [Codeforces Round 1111 official contest page](https://codeforces.com/contest/2247)
- [Codeforces Round 1111 official editorial](https://codeforces.com/blog/entry/155337)
- [Codeforces official API problemset data](https://codeforces.com/api/problemset.problems)
- [Codeforces official API contest list](https://codeforces.com/api/contest.list?gym=false)

## Reference

- [官方题目](https://codeforces.com/contest/2247/problem/C)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-511-q3-lc3998/">← [力扣竞赛] 第 511 场周赛 Q3 LC 3998 使用子序列排序转换二进制字符串 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-28-lc3517/">[力扣每日一题] 2026-07-28｜LC 3517 最小回文排列 I →</a>
</nav>
