---
title: "[atcoder] ARC227 C Follow the Letters"
---

# [atcoder] ARC227 C Follow the Letters

<p class="daily-archive-kicker">2026-08-19 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-19 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=f5e2be04b2766aac536aef460a5c5fb3e9f85641b5091c13a6db31041d6f111d -->
[Official problem: ARC227 C — Follow the Letters](https://atcoder.jp/contests/arc227/tasks/arc227_c?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227）。
- 题目：C — Follow the Letters；任务 slug 为 `arc227_c`。
- 官方分值：700 分；AtCoder 未发布单题官方难度。
- 比赛 rated 范围：1200–2799。
- AtCoder Problems 社区估算难度：2121，核对于 2026-08-19；这不是 AtCoder 官方难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是模型逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)仍是权威来源。

## Complete English statement

You are given a lowercase English string $S=S_1S_2\ldots S_N$.

There are $N$ islands arranged in a circle and numbered $1,2,\ldots,N$ clockwise. Island $N$ is
followed clockwise by island $1$, and character $S_i$ is written on island $i$. Initially, exactly one
person stands on every island.

You may perform the following operation any number of times:

- Choose a character $c$ that occurs in $S$.
- Every person leaves their current island, moves clockwise one island at a time, and stops at the first
  island reached after departure whose written character is $c$. A person must leave even when their
  current island itself is labeled $c$.

Let $K$ be the minimum possible number of occupied islands after all operations. Find $K$ and one
operation sequence that leaves exactly $K$ occupied islands. Under the constraints, a valid sequence of
length at most $10^6$ always exists.

### Input

```text
N
S
```

### Output

Let $L$ be the number of operations and let $X$ be the string of chosen characters in chronological
order. Print:

```text
K
L
X
```

If $L=0$, the third line must be empty. The output must satisfy $0\le L\le10^6$; every character of
$X$ must occur in $S$; and following $X$ must leave exactly $K$ occupied islands. Any valid answer is
accepted.

### Constraints

- $1\le N\le1000$.
- $S$ has length $N$ and consists only of lowercase English letters.
- $N$ is an integer.

### Official samples

Sample 1:

```text
Input
4
abca

Output
1
1
b
```

Choosing `b` moves everyone to the unique island labeled `b`, so one occupied island is achievable.

Sample 2:

```text
Input
4
aabb

Output
1
2
ab
```

Choosing `a` and then `b` gathers everyone on one island.

Sample 3:

```text
Input
4
aaaa

Output
4
0

```

Every operation simply moves each person to the next island, so the four people never merge. The sample
therefore uses no operation and has $K=4$.

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/arc227/tasks/arc227_c?lang=en) remains the normative
source; reuse is subject to the [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en).

## 中文解释与题解

每次操作对所有人使用同一个字符，但每个人从不同起点寻找顺时针方向的下一个该字符。
我们既要证明不可能少于多少个占用岛，又要在 $10^6$ 次以内真的达到这个下界。

## 约束推导与结构观察

设 $p$ 是 $S$ 的最小正周期，即 $S_i=S_{i+p}$（下标按模 $N$ 理解），且 $p\mid N$。
字符串由长度为 $p$ 的基本块重复

$$
K=\frac{N}{p}
$$

次。相隔 $p$ 个岛的起点看到完全相同的无限循环字符序列，所以任意一次操作中，这些人移动
的距离都相同。它们的相对距离始终为 $p$，永远不能合并。因此最终至少有 $K$ 个占用岛。

另一方面，把整个 $S$ 作为一轮操作，再重复 $N$ 轮，即令 $X=S^N$。长度为
$L=N^2\le10^6$，刚好满足输出限制。下面会证明该构造最终恰有 $K$ 个占用岛。

最小周期可由 KMP 前缀函数在线性时间求出。若 $b=\pi_{N-1}$，候选周期为 $N-b$；只有
它整除 $N$ 时才是真正的重复块长度，否则 $p=N$。`int` 足以保存前缀函数和 $K$，但
$N^2$ 的表达式仍用 `long long` 书写以保持类型习惯稳定。

## 样例手推与边界

- `abca` 的最小周期是 4，故 $K=1$；官方样例用一次 `b` 就达到下界，而通用构造也会
  输出一个合法但更长的序列。
- `aabb` 的最小周期仍是 4，所以 $K=1$；操作 `ab` 已足够。
- `aaaa` 的最小周期是 1，故 $K=4$。所有人每次都等距移动，不能发生合并。
- $N=1$ 时 $p=1,K=1$；输出一次该字符也合法。
- 若 $S$ 没有非平凡周期，则 $p=N,K=1$；构造会把所有人聚到一个岛。
- 若 $S=T^K$，相隔 $|T|$ 的 $K$ 个人给出不可突破的下界，但不同周期轨道之间可以合并。

## 解法一：小规模占用集合 BFS

当 $N\le20$ 时，用一个二进制掩码表示当前哪些岛有人。对每个出现在 $S$ 中的字符，精确
模拟一次同步移动，得到下一个掩码。对至多 $2^N$ 个状态做 BFS，遍历完后取置位数最少的
状态，并还原操作串。这覆盖所有有限操作序列，是构造和随机对拍的可靠 oracle。

时间复杂度 $O(2^N\cdot |\Sigma|\cdot N^2)$，空间复杂度 $O(2^N)$；指数级状态数是瓶颈。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  vector<char> alphabet = vector<char>(s.begin(), s.end());
  sort(alphabet.begin(), alphabet.end());
  alphabet.erase(unique(alphabet.begin(), alphabet.end()), alphabet.end());
  int start = (1 << n) - 1;
  vector<int> parent(1 << n, -2);
  vector<char> chosen(1 << n);
  queue<int> states;
  parent[start] = -1;
  states.push(start);
  int best = start;
  while (!states.empty()) {
    int mask = states.front();
    states.pop();
    if (popcount(static_cast<unsigned>(mask)) <
        popcount(static_cast<unsigned>(best))) best = mask;
    for (char letter : alphabet) {
      int next_mask = 0;
      for (int island = 0; island < n; ++island) {
        if ((mask & (1 << island)) == 0) continue;
        for (int step = 1; step <= n; ++step) {
          int next = (island + step) % n;
          if (s[next] != letter) continue;
          next_mask |= 1 << next;
          break;
        }
      }
      if (parent[next_mask] != -2) continue;
      parent[next_mask] = mask;
      chosen[next_mask] = letter;
      states.push(next_mask);
    }
  }
  string operations;
  for (int mask = best; parent[mask] != -1; mask = parent[mask]) {
    operations.push_back(chosen[mask]);
  }
  reverse(operations.begin(), operations.end());
  cout << popcount(static_cast<unsigned>(best)) << '\n';
  cout << operations.size() << '\n' << operations << '\n';
  return 0;
}
```

## 从暴力到最优：从状态搜索转向周期不变量

BFS 在反复询问“这一串操作把所有起点送到哪里”，却没有利用圆环本身的平移对称性。周期
相同的起点永不合并，直接给出严格下界；剩下的问题只需一个统一构造达到下界，不必搜索
操作空间。`S` 的最小周期同时编码了这个对称群，因此把指数级状态搜索降为线性求周期，
输出本身则需要 $N^2$ 个字符。

## 最佳实用解：KMP 最小周期加 $S^N$ 构造

先用前缀函数求最小周期 $p$，输出 $K=N/p$。操作串直接输出 $S$ 共 $N$ 次。

### 正确性证明

**引理 1**：初始位置相差 $p$ 的两个人永远不会合并。

因为 $S$ 以 $p$ 为周期，两人的顺时针字符序列完全相同。对任何选定字符，两人到下一个该
字符的距离相同，操作后仍相差 $p$。归纳可知相对位置永远不变。因此至少保留 $K=N/p$
个占用岛。

**引理 2**：执行一轮操作串 $S$ 时，位于每个基本周期末端的代表恰好绕行一周回到原岛；
其他人至少经过 $N+1$ 条边。

从周期末端出发，依次寻找 $S_1,S_2,\ldots,S_N$，正好按圆环上的字符顺序走完一周。若
起点不是周期末端，第一次匹配会错过这一轮顺序的起点；又因为人在每次操作中至少走一条
边，所以完成全部 $N$ 次匹配时必已越过下一整周的对应边界，即经过至少 $N+1$ 条边。

**引理 3**：人与人不会相互超越。

沿顺时针展开圆环。对同一个目标字符，从更靠前起点找到的“下一个目标位置”不会落在更靠
后起点所得位置之后；允许多个起点映到同一位置，但循环次序不会反转。

**定理**：操作串 $X=S^N$ 后恰有 $K$ 个占用岛。

把每个长度为 $p$ 的周期末端作为一个永不合并的代表。每执行一轮 $S$，代表走一周，而
同一周期区间内尚在它后方的其他人会多走至少一条边。由不超越性，这个“多走”只能让人与
前方人合并，不能越过代表保持独立。每个区间初始至多有 $N$ 个不同位置，重复 $N$ 轮后
都已并入对应代表，故至多剩 $K$ 个岛。结合引理 1 的下界，最终恰为 $K$。

### 完整 C++

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  vector<int> prefix(n);
  for (int i = 1; i < n; ++i) {
    int matched = prefix[i - 1];
    while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
    if (s[i] == s[matched]) ++matched;
    prefix[i] = matched;
  }
  int period = n - prefix[n - 1];
  if (n % period != 0) period = n;
  cout << n / period << '\n';
  cout << 1LL * n * n << '\n';
  for (int repeat = 0; repeat < n; ++repeat) cout << s;
  cout << '\n';
  return 0;
}
```

时间复杂度是 $O(N+L)=O(N^2)$，空间复杂度是 $O(N)$；其中 $L=N^2$ 是必须实际写出的
输出长度。若只计算 $K$，则时间和空间分别可降为 $O(N)$ 与 $O(N)$。

## 方案比较与推荐

- BFS 能给小规模最短操作串，也最适合做 oracle，但 $2^N$ 不可能承受 $N=1000$。
- 周期构造的证明负担较高，却没有搜索、哈希或随机性；实现只需 KMP 和顺序输出，最稳定。
- 比赛中优先记住“平移对称给下界，单调不超越给构造”的思路，而不是死记 $S^N$。

## 易错点

- 操作时即使当前岛字符等于目标字符，人也必须先离开；模拟不能允许原地停留。
- `K` 是最小周期的重复次数 $N/p$，不是周期长度 $p$。
- `N-prefix[N-1]` 只有整除 $N$ 时才是重复周期。
- 输出的 $X$ 长度必须和 $L$ 完全一致，且 $L=0$ 时仍要输出空的第三行。
- 不能只输出 $K$；本题是构造题，操作串也属于判题契约。

## 可复现验证

最佳程序按 GNU++23 编译；三组官方样例均满足输出契约。另对小字母表上的全部短字符串，
把 KMP 得到的 $K$ 与占用集合 BFS 的最小置位数比较，并实际模拟 $S^N$，确认最终置位数
等于 $K$。同时检查了 $N=1$、全相同、无周期和多层周期字符串。

## 变种一：只询问最小占用岛数

新定义：不要求构造操作串，只返回 $K$。原来的周期下界与可达性证明完全保留，因此只需
求最小周期，时间 $O(N)$、空间 $O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = s.size();
  vector<int> prefix(n);
  for (int i = 1; i < n; ++i) {
    int matched = prefix[i - 1];
    while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
    if (s[i] == s[matched]) ++matched;
    prefix[i] = matched;
  }
  int period = n - prefix[n - 1];
  if (n % period != 0) period = n;
  cout << n / period << '\n';
  return 0;
}
```

## 变种二：$N\le20$ 时求达到 $K$ 的最短操作串

新定义：先最小化占用岛数，再最小化操作次数。$S^N$ 仍保证可达，却不保证最短；因此回到
掩码 BFS。先由最小周期算出目标 $K$，BFS 第一次遇到置位数为 $K$ 的状态就是最短答案。
复杂度为 $O(2^N\cdot |\Sigma|\cdot N^2)$，空间为 $O(2^N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  vector<int> prefix(n);
  for (int i = 1; i < n; ++i) {
    int matched = prefix[i - 1];
    while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
    if (s[i] == s[matched]) ++matched;
    prefix[i] = matched;
  }
  int period = n - prefix[n - 1];
  if (n % period != 0) period = n;
  int target = n / period;
  vector<char> alphabet(s.begin(), s.end());
  sort(alphabet.begin(), alphabet.end());
  alphabet.erase(unique(alphabet.begin(), alphabet.end()), alphabet.end());
  int start = (1 << n) - 1;
  vector<int> parent(1 << n, -2);
  vector<char> chosen(1 << n);
  queue<int> states;
  parent[start] = -1;
  states.push(start);
  int finish = -1;
  while (!states.empty()) {
    int mask = states.front();
    states.pop();
    if (popcount(static_cast<unsigned>(mask)) == target) {
      finish = mask;
      break;
    }
    for (char letter : alphabet) {
      int next_mask = 0;
      for (int island = 0; island < n; ++island) {
        if ((mask & (1 << island)) == 0) continue;
        for (int step = 1; step <= n; ++step) {
          int next = (island + step) % n;
          if (s[next] != letter) continue;
          next_mask |= 1 << next;
          break;
        }
      }
      if (parent[next_mask] != -2) continue;
      parent[next_mask] = mask;
      chosen[next_mask] = letter;
      states.push(next_mask);
    }
  }
  string operations;
  for (int mask = finish; parent[mask] != -1; mask = parent[mask]) {
    operations.push_back(chosen[mask]);
  }
  reverse(operations.begin(), operations.end());
  cout << target << '\n' << operations.size() << '\n' << operations << '\n';
  return 0;
}
```

## 变种三：初始只有指定岛有人

新定义：给一个初始占用掩码，不再保证每座岛一人，求能达到的最少占用岛数和一条操作
序列。周期对应的人可能根本未出现，所以原来的 $K$ 下界失效；对 $N\le20$ 枚举所有可达
掩码并取最小值。复杂度仍为 $O(2^N\cdot |\Sigma|\cdot N^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, occupied;
  string s;
  cin >> n >> s >> occupied;
  int start = 0;
  for (int i = 0; i < occupied; ++i) {
    int island;
    cin >> island;
    start |= 1 << (island - 1);
  }
  vector<char> alphabet(s.begin(), s.end());
  sort(alphabet.begin(), alphabet.end());
  alphabet.erase(unique(alphabet.begin(), alphabet.end()), alphabet.end());
  vector<int> parent(1 << n, -2);
  vector<char> chosen(1 << n);
  queue<int> states;
  parent[start] = -1;
  states.push(start);
  int best = start;
  while (!states.empty()) {
    int mask = states.front();
    states.pop();
    if (popcount(static_cast<unsigned>(mask)) <
        popcount(static_cast<unsigned>(best))) best = mask;
    for (char letter : alphabet) {
      int next_mask = 0;
      for (int island = 0; island < n; ++island) {
        if ((mask & (1 << island)) == 0) continue;
        for (int step = 1; step <= n; ++step) {
          int next = (island + step) % n;
          if (s[next] != letter) continue;
          next_mask |= 1 << next;
          break;
        }
      }
      if (parent[next_mask] != -2) continue;
      parent[next_mask] = mask;
      chosen[next_mask] = letter;
      states.push(next_mask);
    }
  }
  string operations;
  for (int mask = best; parent[mask] != -1; mask = parent[mask]) {
    operations.push_back(chosen[mask]);
  }
  reverse(operations.begin(), operations.end());
  cout << popcount(static_cast<unsigned>(best)) << '\n';
  cout << operations.size() << '\n' << operations << '\n';
  return 0;
}
```

## 变种四：不同字符操作有不同代价

新定义：仍从所有岛有人开始，每个字符的操作代价为非负整数；优先达到最少占用岛数，再
最小化字符操作总代价。BFS 的
等权边不再成立；在 $N\le20$ 时改用 Dijkstra，并在首次弹出置位数为 $K$ 的状态时结束。
若字符代价最大为 $W$，时间复杂度为
$O(2^N\cdot |\Sigma|\cdot (N^2+\log 2^N))$，空间为 $O(2^N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string s;
  cin >> n >> s;
  vector<long long> cost(26);
  for (long long& value : cost) cin >> value;
  vector<int> prefix(n);
  for (int i = 1; i < n; ++i) {
    int matched = prefix[i - 1];
    while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
    if (s[i] == s[matched]) ++matched;
    prefix[i] = matched;
  }
  int period = n - prefix[n - 1];
  if (n % period != 0) period = n;
  int target = n / period;
  vector<char> alphabet(s.begin(), s.end());
  sort(alphabet.begin(), alphabet.end());
  alphabet.erase(unique(alphabet.begin(), alphabet.end()), alphabet.end());
  int start = (1 << n) - 1;
  const long long inf = numeric_limits<long long>::max() / 4;
  vector<long long> distance(1 << n, inf);
  using State = pair<long long, int>;
  priority_queue<State, vector<State>, greater<State>> queue;
  distance[start] = 0;
  queue.push({0, start});
  while (!queue.empty()) {
    auto [current, mask] = queue.top();
    queue.pop();
    if (current != distance[mask]) continue;
    if (popcount(static_cast<unsigned>(mask)) == target) {
      cout << current << '\n';
      return 0;
    }
    for (char letter : alphabet) {
      int next_mask = 0;
      for (int island = 0; island < n; ++island) {
        if ((mask & (1 << island)) == 0) continue;
        for (int step = 1; step <= n; ++step) {
          int next = (island + step) % n;
          if (s[next] != letter) continue;
          next_mask |= 1 << next;
          break;
        }
      }
      long long candidate = current + cost[letter - 'a'];
      if (candidate >= distance[next_mask]) continue;
      distance[next_mask] = candidate;
      queue.push({candidate, next_mask});
    }
  }
  return 0;
}
```

## 来源

- [AtCoder 官方题面](https://atcoder.jp/contests/arc227/tasks/arc227_c?lang=en)
- [AtCoder 官方题解](https://atcoder.jp/contests/arc227/editorial/24408?lang=en)
- [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)
- [AtCoder Problems 社区难度数据](https://kenkoooo.com/atcoder/#/table/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_c?lang=en)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-139-lc79/">[力扣 Top 139] LC 79 单词搜索 中等 →</a>
</nav>
