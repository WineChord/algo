---
title: "[atcoder] ABC469 C Cantrip"
---

# [atcoder] ABC469 C Cantrip

<p class="daily-archive-kicker">2026-08-04 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b89a76f0a261653c440ace765bc669370fac10999a3bda3a7806e35df3b6f85b -->
## 官方来源与元数据

- 来源：AtCoder。
- 比赛：AtCoder Beginner Contest 469。
- 题号与标题：C - Cantrip。
- 官方分值：300 分。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- 官方题面：[ABC469 C - Cantrip](https://atcoder.jp/contests/abc469/tasks/abc469_c?lang=en)。
- 版权条款：[AtCoder Terms of Service](https://atcoder.jp/tos)。

普通 AtCoder 比赛题面没有已确认的统一开放转载许可。下方英文层依据官方题面独立组织，完整保留任务定义、输入输出、全部约束、样例与解释；它不是逐字官方原文，官方页面仍是事实核验的权威入口。

## Complete English statement

### C. Cantrip

- **Score:** 300 points
- **Time limit:** 2 seconds
- **Memory limit:** 1024 MiB
- **Official task:** [ABC469 C - Cantrip](https://atcoder.jp/contests/abc469/tasks/abc469_c?lang=en)

This self-contained English presentation was independently organized from the official task and preserves its complete meaning, input, output, constraints, samples, and explanations. It is not represented as a verbatim reproduction. See the official task and the [AtCoder Terms of Service](https://atcoder.jp/tos).

### Problem Statement

You are given a string $S$ of length $N$ consisting of `o` and `x`.

There are $N$ bags in one row, with one sweet inside every bag. The $i$-th bag is marked **hit** when $S_i$ is `o`, and **miss** when $S_i$ is `x`.

For every $k=1,2,\ldots,N$, answer the following question independently.

Takahashi first takes the first $k$ bags from the front of the row, eats their sweets, and keeps the bags. He then repeats the action below as many times as possible:

1. Discard one hit-marked bag that he currently holds.
2. Take the bag currently at the front of the remaining row, eat its sweet, and keep that bag.

This action is available only while at least one bag remains in the row and Takahashi holds a hit-marked bag. Taking a bag removes it from the row. Determine the total number of sweets he eats for each $k$.

### Input

The input is given from Standard Input in the following format:

```text
N
S
```

### Output

Print $N$ lines. The $l$-th line must contain the answer for $k=l$.

### Complete Constraints

$$
1\le N\le8\times10^5.
$$

$N$ is an integer, and $S$ is a string of length $N$ consisting only of `o` and `x`.

### Official Sample 1

```text
5
oxoxo
```

```text
2
4
5
5
5
```

For $k=1$, Takahashi initially receives a hit bag. He discards it and receives the next bag, which is a miss bag. He then has no hit bag, so he stops after eating two sweets.

### Official Sample 2

```text
3
ooo
```

```text
3
3
3
```

### Official Sample 3

```text
1
x
```

```text
1
```

The official statement contains no additional note or required image.

## 中文题意与元数据说明

每次选择一个初始袋数 $k$。先直接吃掉前 $k$ 袋糖并保留袋子；此后每拿一个新袋子，都必须先消耗手里一个 `o` 袋。新拿到的袋子若也是 `o`，又能成为后续行动的凭证。对每个 $k$，求最终吃到的糖数。

AtCoder 官方未标注独立题目难度。[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型在 2026-08-04 的估算难度为 $475$；这是社区估算，不是 AtCoder 官方难度，也不与其他平台评分直接比较。

## 约束推导与核心不变量

$N$ 达到 $8\times10^5$，逐个 $k$ 模拟剩余过程的 $O(N^2)$ 做法不可行。关键是观察吃完前 $r$ 袋后的 `o` 袋数量。前 $r$ 袋中共有 $r-X_r$ 个 `o`，其中额外取得的 $r-k$ 袋各消耗过一个 `o`，所以手中仍可用的 `o` 袋数为

$$
(r-X_r)-(r-k)=k-X_r,
$$

其中 $X_r$ 是前 $r$ 个字符中 `x` 的数量。

因此，只要尚未到末尾且 $X_r<k$，就还能继续；第一次使 $X_r=k$ 的位置恰是字符串中第 $k$ 个 `x` 的位置，吃到该袋后资源归零。若全串不足 $k$ 个 `x`，则一直吃到第 $N$ 袋。于是答案只有一句话：

$$
ans_k=\begin{cases}
\text{第 }k\text{ 个 }x\text{ 的位置},&\#x\ge k,\\
N,&\#x<k.
\end{cases}
$$

答案不超过 $N$，`int` 足够。输入本身需要 $\Omega(N)$ 时间，线性解达到下界。

## 解法递进

### 解法一：对每个 $k$ 独立模拟

维护手中可用 `o` 袋数量，逐袋向右推进。它直接符合过程定义，可作为小规模 oracle，但全 `o` 时每个 $k$ 都走到末尾，最坏为 $O(N^2)$。

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
  for (int k = 1; k <= n; ++k) {
    int hits = count(s.begin(), s.begin() + k, 'o');
    int eaten = k;
    while (eaten < n && hits > 0) {
      --hits;
      hits += s[eaten] == 'o';
      ++eaten;
    }
    cout << eaten << '\n';
  }
}
```

时间 $O(N^2)$，额外空间 $O(1)$。

### 解法二：前缀 `x` 数与二分

先求 $X_r$。每个 $k$ 二分第一个满足 $X_r\ge k$ 的位置；若不存在则答案为 $N$。时间降为 $O(N\log N)$。

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
  vector<int> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    prefix[i + 1] = prefix[i] + (s[i] == 'x');
  }
  for (int k = 1; k <= n; ++k) {
    auto it = lower_bound(prefix.begin() + 1, prefix.end(), k);
    cout << (it == prefix.end() ? n : static_cast<int>(it - prefix.begin())) << '\n';
  }
}
```

时间 $O(N\log N)$，空间 $O(N)$。

### 最佳实用解：记录所有 `x` 的位置

第 $k$ 个答案只需要第 $k$ 个 `x`。按出现顺序保存一基位置后，前 $\#x$ 个答案直接读取，其余答案全为 $N$。

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
  vector<int> misses;
  for (int i = 0; i < n; ++i) {
    if (s[i] == 'x') {
      misses.push_back(i + 1);
    }
  }
  for (int k = 1; k <= n; ++k) {
    cout << (k <= static_cast<int>(misses.size()) ? misses[k - 1] : n) << '\n';
  }
}
```

时间 $O(N)$，空间 $O(N)$；若边扫描边输出不便，位置表是最清楚稳定的实现。竞赛中推荐记住“剩余资源 $=k-X_r$”这一不变量，而不是死记位置公式。

## 正确性证明

固定 $k$。吃完前 $r\ge k$ 袋后，已取得 $r-X_r$ 个 `o` 袋，额外取得的 $r-k$ 袋各消耗一个 `o` 袋，因此可用袋数严格等于 $k-X_r$。若 $X_r<k$ 且仍有袋子，资源为正，下一步一定能执行；若 $X_r=k$，资源为零，无法再执行。由于 $X_r$ 单调不减，第一次达到 $k$ 的位置正是第 $k$ 个 `x` 的位置。若不存在第 $k$ 个 `x`，资源在到达末尾前始终为正。算法在前一种情况下输出该位置，在后一种情况下输出 $N$，与过程终止位置完全一致，故对每个 $k$ 都正确。

## 样例手推

样例 1 的 `x` 位于 2、4。于是 $k=1$ 输出第一个 `x` 的位置 2，$k=2$ 输出第二个 `x` 的位置 4；$k=3,4,5$ 时全串不足 $k$ 个 `x`，均输出 5。以 $k=2$ 为例，初始 `ox` 中有一个 `o`；取得第 3 袋 `o` 后资源不变，再取得第 4 袋 `x` 后资源清零，确实吃 4 袋。

全 `o` 时位置表为空，所有答案为 $N$；全 `x` 时第 $k$ 个 `x` 就在位置 $k$，所有答案为 $k$。$N=1$ 的两个字符也分别落入这两类边界。

## 易错点与方案比较

- 停止位置是“吃掉第 $k$ 个 `x` 后”，不是它的前一位或后一位。
- 初始拿到的 `x` 不提供资源，却仍计入 $X_r$；公式已经统一处理这种情况。
- 新拿到 `o` 时先消耗一个、再获得一个，资源净变化为 0。
- 二分解便于从前缀不变量过渡到结论；位置表去掉了每次查询的对数因子，是应提交的方案。

## 变种一：只回答给定的若干个 $k$

新定义：给出 $Q$ 个任意询问，不必输出全部 $N$ 个答案。位置表仍成立，每次查询 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  vector<int> misses;
  for (int i = 0; i < n; ++i) {
    if (s[i] == 'x') {
      misses.push_back(i + 1);
    }
  }
  while (q--) {
    int k;
    cin >> k;
    cout << (k <= static_cast<int>(misses.size()) ? misses[k - 1] : n) << '\n';
  }
}
```

预处理 $O(N)$，每问 $O(1)$，空间 $O(N)$。

## 变种二：在线翻转字符并询问

新定义：支持把某位置在 `o/x` 间翻转，以及询问当前第 $k$ 个答案。Fenwick 树维护 `x` 的 0/1 计数，并用二进制提升寻找第 $k$ 个 `x`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  int n;
  vector<int> tree;
public:
  explicit Fenwick(int size) : n(size), tree(size + 1) {
  }
  void add(int index, int delta) {
    for (; index <= n; index += index & -index) {
      tree[index] += delta;
    }
  }
  int sum(int index) const {
    int answer = 0;
    for (; index > 0; index -= index & -index) {
      answer += tree[index];
    }
    return answer;
  }
  int kth(int order) const {
    int index = 0;
    int step = 1;
    while ((step << 1) <= n) {
      step <<= 1;
    }
    for (; step; step >>= 1) {
      int next = index + step;
      if (next <= n && tree[next] < order) {
        index = next;
        order -= tree[next];
      }
    }
    return index + 1;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  Fenwick fenwick(n);
  for (int i = 0; i < n; ++i) {
    if (s[i] == 'x') {
      fenwick.add(i + 1, 1);
    }
  }
  while (q--) {
    int type, value;
    cin >> type >> value;
    if (type == 1) {
      int index = value - 1;
      fenwick.add(value, s[index] == 'x' ? -1 : 1);
      s[index] = s[index] == 'x' ? 'o' : 'x';
    } else {
      cout << (fenwick.sum(n) < value ? n : fenwick.kth(value)) << '\n';
    }
  }
}
```

建树 $O(N\log N)$，每次更新或查询 $O(\log N)$，空间 $O(N)$。静态位置表在翻转后失效。

## 变种三：达到目标位置至少要先拿多少袋

新定义：给定目标 $T$，求最小初始 $k$，使 Takahashi 至少吃到第 $T$ 袋。到第 $T-1$ 袋后仍需有资源，即 $k>X_{T-1}$，所以最小值为 $X_{T-1}+1$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  vector<int> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    prefix[i + 1] = prefix[i] + (s[i] == 'x');
  }
  while (q--) {
    int target;
    cin >> target;
    cout << prefix[target - 1] + 1 << '\n';
  }
}
```

预处理 $O(N)$，每问 $O(1)$，空间 $O(N)$。这是把“给定资源求终点”反转为“给定终点求最小资源”。

## 变种四：每个 `o` 袋可提供 $C$ 次行动

新定义：一个 hit 袋有 $C$ 点能量，每取得一个 `o` 袋增加 $C$ 点，每拿一个额外袋消耗 1 点。此时经过 `o` 会净增 $C-1$，第 $k$ 个 `x` 公式不再成立；下面给出 $N\le3000$ 的逐 $k$ 模拟。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long capacity;
  string s;
  cin >> n >> capacity >> s;
  for (int k = 1; k <= n; ++k) {
    long long energy = capacity * count(s.begin(), s.begin() + k, 'o');
    int eaten = k;
    while (eaten < n && energy > 0) {
      --energy;
      if (s[eaten] == 'o') {
        energy += capacity;
      }
      ++eaten;
    }
    cout << eaten << '\n';
  }
}
```

时间 $O(N^2)$，空间 $O(1)$。$C=1$ 退化为原题；$C>1$ 时资源不再只由 `x` 数决定，必须重新建模。

## 验证说明

本轮将七段完整程序按 GNU++23 编译；线性位置解会与逐 $k$ 模拟在全部长度不超过 18 的 `o/x` 字符串上穷举对拍，并复核三组官方样例、全 `o`、全 `x`、交替串与 $N=1$ 边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_c?lang=en)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-91-lc415/">[力扣 Top 91] LC 415 字符串相加 简单 →</a>
</nav>
