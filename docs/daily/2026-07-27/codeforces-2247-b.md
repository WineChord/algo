---
title: "[codeforces] CF Round 1111 Div.2 B Yet Another Constructive"
---

# [codeforces] CF Round 1111 Div.2 B Yet Another Constructive

<p class="daily-archive-kicker">2026-07-27 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../math/modular-constructions/">进入知识专题</a></p>

官方题目：[打开 Codeforces 题目页](https://codeforces.com/problemset/problem/2247/B)

材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)

## 官方原始信息

- 平台与比赛：Codeforces，Codeforces Round 1111（Div. 2）。
- 竞赛 ID：2247。
- 官方题目标识：Div.2 B，标题为 “Yet Another Constructive”。
- 跨组别别名：官方 problemset API 中未发现其他映射；该标题只对应竞赛 2247 的 B 题。
- 官方题目分值：750。
- 官方题目 rating：当前官方 API 未提供，不能根据 B 题序号推断。
- 官方标签：`constructive algorithms`。
- 限制：1.5 秒，256 MB。
- 程序接口：GNU++23 完整程序。
- 官方题面图片：无。

!!! info "官方来源与材料许可"
    Codeforces 是本题来源。下方完整英文题面层遵循 Codeforces 材料使用许可，保留来源署名与官方直链；本站仅作教学展示，不提供自动判题，也不复制隐藏测试、生成器、checker 或 validator。

## Complete English statement

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

## 前缀余数模型

定义

$$
p_0=0,\qquad p_i=\sum_{j=1}^{i}a_j\bmod m.
$$

子数组 $[l,r]$ 的元素和能被 $m$ 整除，当且仅当 $p_{l-1}=p_r$。因此，最短可整除子数组的长度，就是两个相等前缀余数之间的最小下标距离。

这个转化消除了元素上界带来的干扰：模 $m$ 意义下的每种增量都能用 $[1,m]$ 内的正整数表示，远小于 $10^{18}$。

## 必要条件

不能存在长度小于 $k$ 的可整除子数组，所以前 $k$ 个前缀余数

$$
p_0,p_1,\ldots,p_{k-1}
$$

必须两两不同。余数总共只有 $m$ 种，根据抽屉原理，必须满足

$$
k\le m
$$

。

## 解法一：穷举数组

作为概念上的暴力解，可以枚举所有元素都位于 $[1,m]$ 的数组，再检查全部子数组。把值域限制在 $[1,m]$ 不会漏解，因为这些正整数已经能实现模 $m$ 下的全部增量。

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

- 时间复杂度：$O(m^n n^2)$。
- 额外空间复杂度：不计递归栈为 $O(n)$。
- 瓶颈：暴力在搜索完整数列，没有利用“相等前缀余数”这一核心结构。

## 解法二：重复一个和为 $m$ 的正数块（推荐）

当 $k\le m$ 时，把 $m$ 拆成 $k$ 个正整数，并周期性重复这个块。均衡拆分取

$$
q=\left\lfloor\frac{m}{k}\right\rfloor,\qquad r=m\bmod k,
$$

其中包含 $k-r$ 个 $q$ 和 $r$ 个 $q+1$。

任意连续 $k$ 个元素都恰好是该块的一次循环位移，元素和为 $m$。无限周期序列中任意更短的连续段都会漏掉至少一个正数，因此其和严格位于 0 与 $m$ 之间，不可能被 $m$ 整除。

### 正确性证明

- 若 $k>m$，抽屉原理已经证明无解，因此输出 `NO` 正确。
- 若 $k\le m$，则 $q\ge1$，构造出的每个元素都是正数。
- 周期为 $k$，所以每个长度为 $k$ 的窗口恰好包含块中每个元素一次，元素和为 $m$，一定存在合法窗口。
- 任意长度 $d<k$ 的窗口都是正数块的真循环子段，其和大于 0 且严格小于整个块的和 $m$，因此不能被 $m$ 整除。

所以最短可整除子数组长度恰好为 $k$。

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

- 时间复杂度：每组 $O(n)$，总计 $O(\sum n)$。
- 额外空间复杂度：$O(k)$；按下标直接生成时可降为 $O(1)$。
- 输出上界：$\max a_i=\lceil m/k\rceil\le10^9$。
- 记忆建议：用“相等前缀余数对应可整除子数组”证明必要性，用“周期重复 $m$ 的正整数拆分”完成构造。均衡拆分还能最小化构造中的最大元素。

## 同阶替代方案：稀疏跳跃块

也可以使用块

$$
[1,1,\ldots,1,m-k+1]
$$

它同样由 $k$ 个正数组成且总和为 $m$。这种实现特别短，但最大元素可能远大于均衡拆分。

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

- 时间复杂度：$O(n)$。
- 额外空间复杂度：$O(1)$。
- 权衡：生成器最简单，但最大值为 $m-k+1$，而不是 $\lceil m/k\rceil$。

## 常见错误

- 只检查是否存在长度为 $k$ 的可整除区间，却忽略了更短区间。
- 对数组元素模 $k$，而不是对前缀和模 $m$。
- 因 $n>m$ 就判无解；只要相等余数之间的距离达到 $k$，余数可以重复。
- 构造中出现 0；题目要求所有输出元素都是正数。
- 忘记 $k=1$：直接输出 $m$ 即可，因为每个单元素窗口都能整除。
- 输出超过 $10^{18}$ 的值；本构造实际上从不超过 $m$。
- 官方 API 缺少 rating 时，根据题目序号自行推断。

## 追问一：增加元素上界 $B$

<strong>新定义。</strong>额外要求 $1\le a_i\le B$。

必要性：

- 前缀余数论证仍然要求 $k\le m$。
- 一个长度为 $k$、元素和能被 $m$ 整除的子数组，其正整数和至少为 $m$，同时至多为 $kB$，故还需 $m\le kB$。

这两个条件也充分：把 $m$ 尽量均匀地拆成 $k$ 个正整数，最大项为 $\lceil m/k\rceil\le B$。

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

- 时间复杂度：$O(n)$。
- 额外空间：$O(1)$。
- 存在性判据：$k\le m\le kB$。

## 追问二：和为 $m$ 的字典序最小周期块

<strong>新定义。</strong>在所有长度为 $k$、元素均为正整数且总和恰为 $m$ 的块中，输出字典序最小者，并将它周期性重复。

要让前面的元素尽可能小，令前 $k-1$ 项全为 1，最后一项承接剩余的 $m-k+1$。

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

- 时间复杂度：$O(n)$。
- 额外空间：$O(1)$。

## 追问三：统计和为 $m$ 的周期构造数量

<strong>新定义。</strong>统计长度为 $k$、元素均为正整数且总和恰为 $m$ 的有序块数量，对 $10^9+7$ 取模。设 $m\le2\cdot10^5$。

由隔板法，方案数为

$$
\binom{m-1}{k-1}
$$

其中 $k\le m$ 时公式成立，否则答案为零。任意这样的块周期性重复后，都是原题的合法构造。

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

- 时间复杂度：$O(m+\log\text{MOD})$。
- 额外空间：$O(m)$。

## 追问四：验证任意数组并恢复见证区间

<strong>新定义。</strong>给定一个正整数数组，返回元素和能被 $m$ 整除的最短子数组长度，以及一个下标从 1 开始的见证区间。

对每个前缀余数，与当前位置最近的同余前缀会给出以当前位置结尾的最短合法子数组。因此每个余数只需保存最近一次出现位置。

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

- 期望时间复杂度：$O(n)$。
- 额外空间：$O(\min(n,m))$。

## 追问五：流式追加后实时输出最短长度

<strong>新定义。</strong>正整数在线到达；每次追加后，输出目前出现过的最短合法子数组长度，若不存在则输出 `-1`。

每次只需更新一个前缀余数及其最近位置；全局最短长度只可能减小。

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

- 单次更新的期望时间复杂度：$O(1)$。
- 额外空间：$O(\min(n,m))$。

## 追问六：生成随机合法构造

<strong>新定义。</strong>根据给定随机种子生成可复现、形态多样的合法数据。

在 $[1,m-1]$ 中选择 $k-1$ 个互不相同的切分点，相邻切分点之差便构成 $m$ 的一个随机正整数拆分。Floyd 采样可在不遍历到 $m$ 的前提下，以期望 $O(k)$ 时间选出这些切分点。

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

- 期望时间复杂度：$O(k\log k+n)$。
- 额外空间：$O(k)$。

## 可复现验证

- 以 C++23 模式编译每份程序。
- 穷举 $1\le k\le n\le10$、$1\le m\le10$：核对恰在 $k\le m$ 时存在构造，再枚举全部子数组确认最短合法长度。
- 将均匀块、稀疏跳跃、带上界和随机拆分四类生成器，与同一个 $O(n^2)$ 检查器随机对拍。
- 将哈希表见证区间与流式算法，和完整子数组枚举随机对拍。

## 来源

- 官方题目：[打开官方题目](https://codeforces.com/problemset/problem/2247/B)
- 官方比赛：[打开官方比赛](https://codeforces.com/contest/2247)
- 官方比赛 API：[打开官方比赛 API](https://codeforces.com/api/contest.list?gym=false)
- 官方题库 API：[打开官方题库 API](https://codeforces.com/api/problemset.problems)

## 参考资料

- [官方题目](https://codeforces.com/problemset/problem/2247/B)
- [对应知识专题](../../math/modular-constructions.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-511-q2-lc3997/">← [力扣竞赛] 第 511 场周赛 Q2 LC 3997 统计二叉树中支配节点的数量 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-27-lc1464/">[力扣每日一题] 2026-07-27｜LC 1464 数组中两元素的最大乘积 →</a>
</nav>
