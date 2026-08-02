---
title: "[atcoder] ABC469 B Isolated Seats"
---

# [atcoder] ABC469 B Isolated Seats

<p class="daily-archive-kicker">2026-08-03 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=fbd484fa5d493d50404b6b04a65df7f4024e59d5ff240e48addad93327006e68 -->
## 官方来源与元数据

- 来源：AtCoder。
- 比赛：AtCoder Beginner Contest 469。
- 题号与标题：B - Isolated Seats。
- 官方分值：200 分。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- 官方题面：[ABC469 B - Isolated Seats](https://atcoder.jp/contests/abc469/tasks/abc469_b?lang=en)。
- 版权条款：[AtCoder Terms of Service](https://atcoder.jp/tos)。

普通 AtCoder 比赛题面没有已确认的统一开放转载许可。下方英文层依据官方题面独立组织，完整保留任务定义、输入输出、全部约束、样例与解释；它不是逐字官方原文，官方页面仍是事实核验的权威入口。

## Complete English statement

### B. Isolated Seats

- **Score:** 200 points
- **Time limit:** 2 seconds
- **Memory limit:** 1024 MiB
- **Official task:** [ABC469 B - Isolated Seats](https://atcoder.jp/contests/abc469/tasks/abc469_b?lang=en)

This self-contained English presentation was independently organized from the official task and preserves its complete meaning, input, output, constraints, samples, and explanations. It is not represented as a verbatim reproduction. See the official task and the [AtCoder Terms of Service](https://atcoder.jp/tos).

### Problem Statement

There are $N$ seats arranged in one row. Number them $1,2,\ldots,N$ from left to right. Their state is represented by a string $S$ of length $N$.

- For each $1\le i\le N$, if the $i$-th character $S_i$ is `o`, seat $i$ is occupied.
- For each $1\le i\le N$, if the $i$-th character $S_i$ is `x`, seat $i$ is empty.

An empty seat is called **isolated** when every adjacent seat that exists is also empty. More precisely, an empty seat $i$ is isolated if the seat immediately to its left is either nonexistent or empty, and the seat immediately to its right is either nonexistent or empty.

Find the number of isolated seats.

### Input

The input is given from Standard Input in the following format:

```text
N
S
```

### Output

Print the number of isolated seats on one line.

### Complete Constraints

$$
1\le N\le100.
$$

$S$ is a string of length $N$ consisting only of `o` and `x`. $N$ is an integer.

### Official Sample 1

```text
8
xxoxxxox
```

```text
2
```

The first and fifth seats are isolated. No other seat satisfies all three conditions.

### Official Sample 2

```text
5
ooooo
```

```text
0
```

Every seat is occupied, so there is no isolated empty seat.

### Official Sample 3

```text
1
x
```

```text
1
```

The only seat is empty and has no adjacent seat on either side, so it is isolated.

The official statement contains no additional note or required image.

## 中文题意与元数据说明

一排有 $N$ 个座位，`o` 表示有人，`x` 表示空位。一个空位只有在“存在的左邻座位为空”且“存在的右邻座位为空”时才算孤立；边界外没有座位，因此不会让条件失败。求孤立空位数量。

AtCoder 官方未标注独立题目难度。[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型在 2026-08-03 的估算难度为 $-576$；这是社区估算，不是 AtCoder 官方难度，也不与其他平台评分直接比较。

## 约束推导与边界

$N\le100$ 允许逐座位检查。每个位置只依赖自己与至多两个相邻位置，因此无需搜索或动态规划，线性扫描已经达到输入读取的下界 $\Omega(N)$。

判断式可以写成：

$$
\qquad S_i=\texttt{x}\quad\land\quad(i=0\lor S_{i-1}=\texttt{x})\quad\land\quad(i=N-1\lor S_{i+1}=\texttt{x}).
$$

最容易错的是把“没有邻居”当成失败。样例 3 明确说明单个 `x` 同时满足左右条件。答案介于 0 与 $N$，`int` 足够，不涉及溢出。

## 解法递进

### 解法一：为每个空位显式收集存在的邻居

枚举空位，再逐个检查合法下标的相邻座位。它直接翻译定义，适合作为小规模验证基准。

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
  int answer = 0;
  for (int i = 0; i < n; ++i) {
    if (s[i] != 'x') {
      continue;
    }
    bool isolated = true;
    for (int next : {i - 1, i + 1}) {
      if (0 <= next && next < n && s[next] == 'o') {
        isolated = false;
      }
    }
    answer += isolated;
  }
  cout << answer << '\n';
}
```

时间 $O(N)$，额外空间 $O(1)$。虽然内层只有两个方向，但分支较多。

### 最佳实用解：哨兵统一边界

在原串两侧各补一个 `x`。原位置 $i$ 在新串中对应 $i+1$，孤立条件恰好变成连续三字符均为 `x`，边界与内部位置无需分开处理。

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
  string padded = "x" + s + "x";
  int answer = 0;
  for (int i = 1; i <= n; ++i) {
    if (padded[i - 1] == 'x' && padded[i] == 'x' && padded[i + 1] == 'x') {
      ++answer;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N)$，额外空间 $O(N)$（也可用三个条件做到 $O(1)$）。竞赛中推荐记忆原始三条件写法；教学时哨兵能最清楚地说明边界为何等价于空位。

## 正确性证明

补入的两个哨兵都是 `x`，恰好代表左右边界外“不存在座位，因此条件自动成立”。对任一原座位 $i$：新串中心字符为 `x` 当且仅当该座位为空；左字符为 `x` 当且仅当左邻不存在或为空；右字符同理。因此代码计数的每个三连 `x` 中心与一个且仅一个孤立座位对应。扫描所有原位置后既不会漏计，也不会把非孤立座位计入，答案正确。

## 样例手推

样例 1 补哨兵后为 `xxxoxxxoxx`。原位置 1 的窗口为 `xxx`，原位置 5 的窗口也为 `xxx`；其余 `x` 至少一侧紧邻 `o`，窗口不是全 `x`，所以答案为 2。

样例 3 中 `x` 变为 `xxx`，唯一中心满足条件，答案为 1。全 `o` 时每个中心字符都先失败，答案为 0。

## 易错点与方案比较

- 只统计 `xxx` 子串数量会混淆“窗口”与“中心”：长度为 4 的空段有 2 个 `xxx` 窗口，却有 4 个孤立座位，因为边界外也视为通过。
- 条件必须先确认中心是 `x`，已占座位永远不计。
- 左右边界使用逻辑或，而不是要求两个邻居真实存在。
- 显式条件额外空间更小；哨兵实现分支更少。两者同为最优 $O(N)$，面试中优先写三条件，竞赛中任选更不易错的一种。

## 变种一：输出所有孤立座位编号

新定义：输出孤立座位数量及其一基编号。原判定仍成立，只需保存命中的位置。

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
  vector<int> positions;
  for (int i = 0; i < n; ++i) {
    bool leftEmpty = i == 0 || s[i - 1] == 'x';
    bool rightEmpty = i + 1 == n || s[i + 1] == 'x';
    if (s[i] == 'x' && leftEmpty && rightEmpty) {
      positions.push_back(i + 1);
    }
  }
  cout << positions.size() << '\n';
  for (int position : positions) {
    cout << position << ' ';
  }
  cout << '\n';
}
```

时间 $O(N)$，输出外额外空间 $O(N)$。

## 变种二：在线翻转座位并查询当前答案

新定义：每次把一个位置在 `o` 与 `x` 间翻转，并输出孤立座位数。一次更新只可能改变中心在 $p-1,p,p+1$ 的三个判定；更新前减去旧贡献，更新后加回新贡献。

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
  auto contribution = [&](int i) {
    if (i < 0 || i >= n || s[i] != 'x') {
      return 0;
    }
    bool leftEmpty = i == 0 || s[i - 1] == 'x';
    bool rightEmpty = i + 1 == n || s[i + 1] == 'x';
    return leftEmpty && rightEmpty ? 1 : 0;
  };
  int answer = 0;
  for (int i = 0; i < n; ++i) {
    answer += contribution(i);
  }
  while (q--) {
    int position;
    cin >> position;
    --position;
    for (int i = position - 1; i <= position + 1; ++i) {
      answer -= contribution(i);
    }
    s[position] = s[position] == 'x' ? 'o' : 'x';
    for (int i = position - 1; i <= position + 1; ++i) {
      answer += contribution(i);
    }
    cout << answer << '\n';
  }
}
```

预处理 $O(N)$，每次更新 $O(1)$，空间 $O(1)$（不计字符串）。原算法若每次全扫会退化为 $O(NQ)$。

## 变种三：座位围成一个圆环

新定义：$N\ge2$，位置 0 的左邻是 $N-1$，位置 $N-1$ 的右邻是 0。边界自动成立不再正确，必须用模运算取得真实邻居。

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
  int answer = 0;
  for (int i = 0; i < n; ++i) {
    int left = (i - 1 + n) % n;
    int right = (i + 1) % n;
    if (s[i] == 'x' && s[left] == 'x' && s[right] == 'x') {
      ++answer;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N)$，空间 $O(1)$。若允许 $N=1$，需先明确同一座位能否作为自己的邻居；这里用 $N\ge2$ 消除定义歧义。

## 变种四：半径 $D$ 内都不能有人

新定义：空位 $i$ 只有在距离不超过 $D$ 的所有存在座位也为空时才计入。逐点扫描半径会变成 $O(ND)$；对 occupied seat 建前缀和即可 $O(1)$ 查询窗口人数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, distance;
  string s;
  cin >> n >> distance >> s;
  vector<int> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    prefix[i + 1] = prefix[i] + (s[i] == 'o');
  }
  int answer = 0;
  for (int i = 0; i < n; ++i) {
    int left = max(0, i - distance);
    int right = min(n, i + distance + 1);
    if (s[i] == 'x' && prefix[right] - prefix[left] == 0) {
      ++answer;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N)$，空间 $O(N)$。前缀和消除了不同中心之间重复统计同一窗口的工作。

## 验证说明

本轮将所有代码按 GNU++23 编译；最佳解会与显式邻居枚举在全部长度不超过 12 的 `o/x` 字符串上逐一对拍，并覆盖 `x`、`o`、全空、全满、交替和长空段等边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_b?lang=en)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-81-lc31/">[力扣 Top 81] LC 31 下一个排列 中等 →</a>
</nav>
