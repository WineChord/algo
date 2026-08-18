---
title: "[codeforces] CF Round 1117 Div.2 B Gigantomachy"
---

# [codeforces] CF Round 1117 Div.2 B Gigantomachy

<p class="daily-archive-kicker">2026-08-19 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-19 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=866a3478c7e9e6ac74e829093e7a12bc9f2933a85df0c1f4ee2c3158e34ffd60 -->
[Official problem: Codeforces Round 1117 (Div. 2), B — Gigantomachy](https://codeforces.com/contest/2257/problem/B?locale=en)

## 官方来源与元数据

- 比赛 ID：2257；正式比赛名：Codeforces Round 1117 (Div. 2)，比赛已经结束。
- 题目：Div.2 B — Gigantomachy；没有经官方关系确认的跨组别别名。
- 官方分值：750；官方当前未给出 problem rating；官方标签：`math`。
- 时间限制：1 秒；内存限制：256 MB。
- 题面含一幅初始山脉示意图，但图中没有正文之外的新规则；下方文字已自包含地定义方向、
  编号和操作，因此该图不是理解或作答所必需的资产。

下方保留完整官方英文题意层。Codeforces 来源、官方直达链接和材料许可就近列出。

## Complete English statement

Two giants, Bea and Ver, play on two mountain ranges. Bea's range has heights
$a_1,a_2,\ldots,a_n$, numbered from left to right. Ver's range has heights
$b_1,b_2,\ldots,b_m$, numbered from right to left, so the two giants face each other. Initially each
giant stands on mountain 1 of the corresponding range.

Both height sequences are non-increasing:

$$
a_i\ge a_{i+1}\quad(1\le i<n),\qquad
b_i\ge b_{i+1}\quad(1\le i<m).
$$

Bea moves first, after which the giants alternate turns. On a giant's turn, all of the following happen:

1. The giant throws a boulder at the mountain currently occupied by the opponent, reducing that
   mountain's height by 1.
2. If the next mountain in the active giant's own range exists and is now higher than the mountain the
   giant occupies, the active giant jumps to that next mountain.
3. Otherwise, if the active giant is on the last mountain and its current height is 0, that giant admits
   defeat.

The numbers and heights can make direct simulation extremely long. Determine which giant wins. Print
`1` for Bea and `2` for Ver.

### Input

The first line contains the number of test cases $t$ ($1\le t\le500$). Each test case contains:

```text
n m
a_1 a_2 ... a_n
b_1 b_2 ... b_m
```

Here $1\le n,m\le100$, $1\le a_i,b_i\le10^9$, and both sequences are non-increasing.

### Constraints

- $1\le t\le500$.
- $1\le n,m\le100$ for every test case.
- $1\le a_i,b_i\le10^9$.
- $a_i\ge a_{i+1}$ for $1\le i<n$.
- $b_i\ge b_{i+1}$ for $1\le i<m$.

### Output

For each test case, output one integer: `1` if Bea wins, or `2` if Ver wins.

### Official sample

```text
Input
6
1 1
1
1
1 1
1
2
1 2
4
4 1
4 2
4 3 2 1
10 1
4 2
4 3 2 1
6 5
4 2
4 3 2 1
7 5

Output
1
2
2
2
1
2
```

In the first case Bea's first throw reduces Ver's only mountain to 0, and Ver loses on his turn. In the
second case Bea first changes Ver's height from 2 to 1; Ver then reduces Bea's only mountain to 0, and
Bea loses on her next turn. In the third case the first three rounds reduce both currently occupied
mountains to height 1; Bea then reduces Ver's current mountain to 0, but Ver still advances to his
second mountain and ultimately wins.

Statement source: [Codeforces problem 2257B](https://codeforces.com/contest/2257/problem/B?locale=en).
This public, non-judge presentation follows the
[Codeforces materials usage license v0.1](https://codeforces.com/page/254); see also the
[official materials notice](https://codeforces.com/blog/entry/967?locale=en).

## 中文解释与题解

两名巨人轮流攻击对方脚下的山，每次把高度减 1。自己的回合攻击完成后，如果前方下一座山
已经比脚下山高，就向前跳一座；若脚下最后一座山降到 0，则认输。山高可达 $10^9$，不能
按回合硬模拟。

## 约束推导与“可承受攻击次数”

考虑一条非递增山脉 $h_1\ge h_2\ge\cdots\ge h_k$。巨人在第 $i$ 座山上受到若干次攻击。
要让下一座山严格高于当前山，需要

$$
h_i-x<h_{i+1},
$$

所以从第 $i$ 座移动到第 $i+1$ 座恰需 $h_i-h_{i+1}+1$ 次攻击。最后一座山从 $h_k$
降到 0 恰需 $h_k$ 次攻击。总和望远镜消去：

$$
H(h)=\sum_{i=1}^{k-1}(h_i-h_{i+1}+1)+h_k=h_1+k-1.
$$

因此山脉内部的具体高度都不影响胜负，只需首座山高和山数。记
$H_A=a_1+n-1$、$H_B=b_1+m-1$。Bea 先攻击：若 $H_B\le H_A$，她会先让 Ver 耗尽；
相等时 Ver 在自己的回合认输，仍是 Bea 获胜。否则 Bea 先认输。最大值约为
$10^9+99$，`long long` 或 `int` 均安全；用 `long long` 更便于变种扩展。

## 样例手推与边界

第五组中 Bea 的耐久为 $4+4-1=7$，Ver 的耐久为 $6+2-1=7$。两者相等，但 Bea 先手，
第 7 次攻击使 Ver 在自己的回合认输，所以输出 `1`。第六组只把 Ver 的首山改为 7，其耐久
变为 8，大于 Bea 的 7，故输出 `2`。

- 单座山：耐久就是该山高度。
- 相邻山等高：只受一次攻击，当前山就比下一山低并发生跳跃。
- 相邻差很大：需要“差值加一”次攻击，不能漏掉严格大于条件。
- 耐久相等：先手 Bea 获胜。
- 内部高度改变但仍保持非递增：不改变望远镜结果。
- 玩家在自己的回合先扔石头，再检查自己的移动或失败；比较式已经正确处理这个时序。

## 解法一：逐回合模拟

复制两条高度数组，按题意逐回合减高度、移动并判断失败。它忠实执行状态转移，适合小高度
输入和作为 oracle；但回合数可能达到 $10^9$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int& height : a) cin >> height;
    for (int& height : b) cin >> height;
    int bea = 0;
    int ver = 0;
    while (true) {
      --b[ver];
      if (bea + 1 < n && a[bea + 1] > a[bea]) ++bea;
      else if (bea + 1 == n && a[bea] == 0) {
        cout << 2 << '\n';
        break;
      }
      --a[bea];
      if (ver + 1 < m && b[ver + 1] > b[ver]) ++ver;
      else if (ver + 1 == m && b[ver] == 0) {
        cout << 1 << '\n';
        break;
      }
    }
  }
  return 0;
}
```

若最大山高为 $V$，时间复杂度可达 $O(V+n+m)$，额外空间 $O(n+m)$。瓶颈是把相邻高度差
逐次减完，而这些次数可以直接求和。

## 从状态模拟到望远镜和

对每条山脉分别统计“离开每座山所需的受击次数”。非递增保证每段恰为差值加一，末段为末
山高度；求和后所有内部高度一正一负抵消，只剩首山高度和 $k-1$ 次跨山额外攻击。于是整局
游戏压缩成两个整数的先手竞速。

## 最佳实用解：比较两条山脉的耐久

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    long long firstA = 0;
    long long firstB = 0;
    for (int i = 0; i < n; ++i) {
      long long height;
      cin >> height;
      if (i == 0) firstA = height;
    }
    for (int i = 0; i < m; ++i) {
      long long height;
      cin >> height;
      if (i == 0) firstB = height;
    }
    long long enduranceA = firstA + n - 1;
    long long enduranceB = firstB + m - 1;
    cout << (enduranceB <= enduranceA ? 1 : 2) << '\n';
  }
  return 0;
}
```

时间复杂度为 $O(n+m)$，用于读取输入；额外空间 $O(1)$。若输入流允许只提供首项和长度，
判定本身是 $O(1)$。算法没有乘法，`long long` 不会溢出。

### 正确性证明

先证明耐久公式。对每个非末山 $i$，受到 $h_i-h_{i+1}$ 次攻击后当前高度仍等于
$h_{i+1}$，下一山并未严格更高；再受一次才跳走，所以需要 $h_i-h_{i+1}+1$ 次。末山受
$h_k$ 次后为 0。相加得到 $H(h)=h_1+k-1$，这正是该巨人认输前能承受的攻击数。

Bea 的第 $q$ 个回合先给 Ver 第 $q$ 次攻击。若 $H_B\le H_A$，在第 $H_B$ 轮开始时 Bea
至多受到 $H_B-1<H_A$ 次攻击，仍能行动；她攻击后 Ver 已承受 $H_B$ 次并在自己的回合认输，
故 Bea 获胜。若 $H_B>H_A$，Ver 完成第 $H_A$ 次攻击后 Bea 已耗尽耐久；Bea 下一回合虽先
扔石头，但随后自己认输，而 Ver 尚未耗尽，故 Ver 获胜。算法的比较与这两个充要情形一致。

## 同阶方案与推荐

可以在线扫描数组并显式求各段 `(h[i] - h[i+1] + 1)`，同样为 $O(n+m)$；它更贴近推导，
也自然推广到非单位伤害。原题中望远镜化成 `first + length - 1` 更短、状态更少。优先记忆
“先求单方可承受攻击次数，再做先手竞速”，不要死记最终不等式而忽略回合顺序。

## 易错点

- 把跨山代价写成 `h[i] - h[i+1]`，漏掉“严格更高”的最后一次攻击。
- 相等耐久时判 Ver 胜；Bea 先攻击，所以平局归 Bea。
- 使用总高度之和；未站上的山不会被攻击，总和不是生命值。
- 在自己的回合开始前就判脚下为 0 而跳过攻击，导致先手时序错误。
- 只读首元素后忘记消费剩余输入，使下一测试错位。
- 把官方分值 750 或标签 `math` 当作 problem rating；官方 rating 当前未知。

## 验证说明

六组官方样例均通过。额外覆盖单山、全部等高、严格下降、首山高 $10^9$、耐久相等和只改
内部高度的成对用例。对 $n,m\le5$、高度不超过 8 的全部非递增数组，可将公式解与逐回合
模拟比较，验证胜者完全一致。

## 变种一：同时输出结束的回合数

新定义：输出胜者和发生认输时已经执行的个人回合数。若 Bea 获胜，Ver 在第 $H_B$ 轮的
第二个个人回合认输，总数为 $2H_B$；否则 Bea 在受到 $H_A$ 次攻击后的下一轮第一个个人
回合认输，总数为 $2H_A+1$。判定为 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  long long firstA, firstB, value;
  cin >> firstA;
  for (int i = 1; i < n; ++i) cin >> value;
  cin >> firstB;
  for (int i = 1; i < m; ++i) cin >> value;
  long long enduranceA = firstA + n - 1;
  long long enduranceB = firstB + m - 1;
  if (enduranceB <= enduranceA) cout << 1 << ' ' << 2 * enduranceB << '\n';
  else cout << 2 << ' ' << 2 * enduranceA + 1 << '\n';
  return 0;
}
```

## 变种二：起手玩家由输入指定

新定义：`starter=1` 表示 Bea 先手，`starter=2` 表示 Ver 先手。先手方在耐久平局时获胜；
更一般地，先手获胜当且仅当对手耐久不大于自己耐久。时间和空间均为 $O(1)$（读入除外）。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, starter;
  cin >> n >> m >> starter;
  long long firstA, firstB, value;
  cin >> firstA;
  for (int i = 1; i < n; ++i) cin >> value;
  cin >> firstB;
  for (int i = 1; i < m; ++i) cin >> value;
  long long endurance[3] = {0, firstA + n - 1, firstB + m - 1};
  int other = 3 - starter;
  cout << (endurance[other] <= endurance[starter] ? starter : other) << '\n';
  return 0;
}
```

## 变种三：两人的攻击伤害不同

新定义：Bea 每次把 Ver 脚下高度减少 $d_A$，Ver 每次把 Bea 脚下高度减少 $d_B$；高度降到
非正数视为 0。差值不再直接望远镜。对非末山，离开所需攻击数为
$\lfloor(h_i-h_{i+1})/d\rfloor+1$；末山为 $\lceil h_k/d\rceil$。线性求双方受击次数后仍按
先手规则比较，时间 $O(n+m)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long hitsNeeded(const vector<long long>& heights, long long damage) {
  long long hits = 0;
  for (int i = 0; i + 1 < static_cast<int>(heights.size()); ++i) {
    hits += (heights[i] - heights[i + 1]) / damage + 1;
  }
  hits += (heights.back() + damage - 1) / damage;
  return hits;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  long long damageA, damageB;
  cin >> n >> m >> damageA >> damageB;
  vector<long long> a(n), b(m);
  for (long long& height : a) cin >> height;
  for (long long& height : b) cin >> height;
  long long enduranceA = hitsNeeded(a, damageB);
  long long enduranceB = hitsNeeded(b, damageA);
  cout << (enduranceB <= enduranceA ? 1 : 2) << '\n';
  return 0;
}
```

## 变种四：山高任意，受击后立即检查跳跃

新定义：输入山脉可以任意起伏；每次山受到单位伤害后，站在其上的巨人立即检查下一山，
若下一山严格更高就跳过去。这样双方都没有“先手尚未受击却先检查”的时序特例。若下一山
本来更高，也至少要先受到一次攻击才会触发检查；一般转移代价为
$\max(1,h_i-h_{i+1}+1)$。内部高度不再完全抵消，需要线性求和；最后一山仍需 $h_k$ 次。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long endurance(const vector<long long>& heights) {
  long long answer = heights.back();
  for (int i = 0; i + 1 < static_cast<int>(heights.size()); ++i) {
    answer += max(1LL, heights[i] - heights[i + 1] + 1);
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> a(n), b(m);
  for (long long& height : a) cin >> height;
  for (long long& height : b) cin >> height;
  cout << (endurance(b) <= endurance(a) ? 1 : 2) << '\n';
  return 0;
}
```

## 来源

- [Codeforces Round 1117 (Div. 2)](https://codeforces.com/contest/2257)
- [Codeforces 2257B — Gigantomachy](https://codeforces.com/contest/2257/problem/B?locale=en)
- [Codeforces 官方 API：contest.standings](https://codeforces.com/api/contest.standings?contestId=2257)
- [Codeforces materials usage license v0.1](https://codeforces.com/page/254)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/B?locale=en)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-515-q2-lc4025/">← [力扣竞赛] 第 515 场周赛 Q2 LC 4025 交通灯的最大等待时间 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-19-lc1386/">[力扣每日一题] 2026-08-19｜LC 1386 安排电影院座位 →</a>
</nav>
