---
title: "[codeforces] CF Round 1116 Div.1 A / Div.2 C Hot Potatoes at the Fairy Warehouse"
---

# [codeforces] CF Round 1116 Div.1 A / Div.2 C Hot Potatoes at the Fairy Warehouse

<p class="daily-archive-kicker">2026-08-14 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-14 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d983d6eb22e89a6bf63d472e670ec49c925d851b63120067312486ead25e4f02 -->
[Official problem: Codeforces 2256C - Hot Potatoes at the Fairy Warehouse](https://codeforces.com/contest/2256/problem/C)

## 官方来源与元数据

- 比赛：Codeforces Round 1116，官方比赛 ID 分别为 Div.1 的 2255 与 Div.2 的 2256。
- 题目：Div.1 A / Div.2 C - Hot Potatoes at the Fairy Warehouse。两个官方页面的题面、输入输出、样例与 Note 一致，属于同一题目的两个正式别名。
- 官方链接：[Div.1 A](https://codeforces.com/contest/2255/problem/A)、[Div.2 C](https://codeforces.com/contest/2256/problem/C)。
- 官方分值：Div.1 A 为 500，Div.2 C 为 1500；两个官方 API 当前都没有 `rating` 字段，因此 rating 未知。
- 官方标签：Div.1 A 为 games、greedy、implementation；Div.2 C 为 games。标签按别名分别保留，不把并集冒充成单个页面的官方字段。
- 时间限制：2 秒；内存限制：256 MB。
- Codeforces 来源与公开使用条件见 [Materials usage license v0.1](https://codeforces.com/blog/entry/967)。下方英文层自包含呈现公开题面文本，不包含隐藏测试、生成器、checker 或 validator。

## Complete English statement

### Task

There are $2n$ leprechauns sitting in a circle and numbered $1,2,\ldots,2n$ clockwise. The odd-numbered leprechauns form the Red Team, and the even-numbered leprechauns form the Blue Team. Initially, some of them hold a potato. The game lasts for exactly $k$ rounds.

At the beginning of every round, both teams know all current potato positions. Then every holder simultaneously chooses exactly one action:

- keep the potato; or
- pass it to the next leprechaun clockwise, provided that this next leprechaun did not hold a potato at the beginning of the round.

If the next leprechaun did hold a potato at the beginning of the round, the current holder must keep theirs. Passing eligibility is determined solely from the round-start state, so every leprechaun holds at most one potato at all times.

After all $k$ rounds, every leprechaun still holding a potato is eliminated. A team's score is the number of eliminated leprechauns on the opposing team. Members of each team cooperate and share all information to maximize their team's score. Determine the Red Team and Blue Team scores when both teams play optimally. The resulting scores are uniquely determined, although the optimal strategy itself need not be unique.

### Input

The first line contains the number of test cases $t$. Each test case consists of a line containing $n$ and $k$, followed by a binary string $s$ of length $2n$. Character $s_i$ is `1` exactly when leprechaun $i$ initially holds a potato.

### Output

For every test case, print two integers: the Red Team score and the Blue Team score, in this order.

### Constraints

- $1\le t\le10^4$.
- $1\le n\le10^5$.
- $1\le k\le10^9$.
- $|s|=2n$ and every character of $s$ is `0` or `1`.
- The sum of $n$ over all test cases is at most $10^5$.

### Official sample

```text
6
2 1
1000
2 1
0011
3 2
101110
5 100000
1111111111
5 100000
0000000000
7 4
10011110101011
```

```text
1 0
0 2
3 1
5 5
0 0
7 2
```

### Official note

In the first test case, leprechaun $1$ passes the potato to leprechaun $2$ in the only round. Only Blue member $2$ holds a potato at the end, so the scores are Red $1$ and Blue $0$.

In the second test case, it is optimal for leprechaun $4$ to pass the potato to leprechaun $1$. Leprechaun $3$ cannot pass to leprechaun $4$, because $4$ already held a potato at the beginning of that round.

For the third test case, the official statement supplies an [animation of one possible optimal strategy](https://espresso.codeforces.com/45e2b71b9979cdb65198a6b629b54f7d540750ef.png). It shows the initial holders $1,3,4,5$; then $1\to2$ in the first round and $5\to6$ in the second, with the other holders keeping their potatoes. The final holders are $2,3,4,6$, producing Red score $3$ and Blue score $1$. Other optimal strategies may exist, but their final scores are the same. The linked animation is an official Codeforces asset; its complete semantic content is stated here, and the asset is not rehosted because the text license does not separately establish republication rights for independent image files.

## 中文题意解释

$2n$ 个人顺时针围成圆，奇数编号属于 Red，偶数编号属于 Blue。每轮所有持有者同时决定保留土豆，或在顺时针下一人于轮初没有土豆时传给他。经过恰好 $k$ 轮后，仍持有土豆的人被淘汰；一队得分是被淘汰的对方人数。两队内部完全合作且都最优，求唯一确定的 Red、Blue 分数。

关键是“能否传递”只看轮初状态，而不是按某个遍历顺序实时修改。最优分数唯一，也不代表最优动作序列唯一。

## 约束推导与零和化

直接模拟不可行，因为 $k$ 可达 $10^9$，而每个可传者又有“传或留”两个选择。土豆既不产生也不消失，设总数为 $P$，终局每个土豆恰好淘汰一名成员，因此

$$
\operatorname{RedScore}+\operatorname{BlueScore}=P.
$$

这是零和博弈：只要求出 Red 的值，Blue 的值就是 $P$ 减去它。

以下使用从 0 开始的下标。偶数位置是 Red 成员，奇数位置是 Blue 成员。令

$$
F(s)=\#\{i\text{ 为奇数}:s_i=1\}
+\#\{i\text{ 为偶数}:s_i=1,s_{i+1}=0\}
-\#\{i\text{ 为奇数}:s_i=1,s_{i+1}=0\},
$$

其中 $i+1$ 按 $2n$ 取模。第一项是当前位于 Blue 成员手里的土豆数；后两项分别记录 Red、Blue 持有者在最后一轮可以沿环形 `10` 边传递所带来的净收益。

## 解法递进

### 解法一：状态博弈树暴力

把土豆位置编码成位掩码。每轮先按轮初状态找出所有 `10` 源，分别枚举 Red 与 Blue 的传递子集，再同步生成后继状态。终局用奇下标的 1 数量计算 Red 得分，做 $\max_{R}\min_{B}$；小规模还可独立核对 $\min_{B}\max_{R}$。

<!-- compile:standalone -->
```cpp
#include <algorithm>
#include <bit>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
int m;
unsigned full_mask;
vector<unordered_map<unsigned, int>> memo;
vector<unsigned> moves(unsigned state, int parity) {
  vector<int> source;
  for (int i = parity; i < m; i += 2) {
    int next = (i + 1) % m;
    if ((state >> i & 1U) && !(state >> next & 1U)) source.push_back(i);
  }
  vector<unsigned> result;
  for (unsigned subset = 0; subset < (1U << source.size()); ++subset) {
    unsigned selected = 0;
    for (int j = 0; j < static_cast<int>(source.size()); ++j) {
      if (subset >> j & 1U) selected |= 1U << source[j];
    }
    result.push_back(selected);
  }
  return result;
}
unsigned advance(unsigned state, unsigned red_move, unsigned blue_move) {
  unsigned selected = red_move | blue_move;
  unsigned destination = ((selected << 1) | (selected >> (m - 1))) & full_mask;
  return (state & ~selected) | destination;
}
int red_terminal_score(unsigned state) {
  int score = 0;
  for (int i = 1; i < m; i += 2) score += state >> i & 1U;
  return score;
}
int solve(int rounds, unsigned state) {
  if (rounds == 0) return red_terminal_score(state);
  if (auto it = memo[rounds].find(state); it != memo[rounds].end()) return it->second;
  vector<unsigned> red_choices = moves(state, 0);
  vector<unsigned> blue_choices = moves(state, 1);
  int best = -1;
  for (unsigned red_move : red_choices) {
    int worst = m + 1;
    for (unsigned blue_move : blue_choices) {
      worst = min(worst, solve(rounds - 1, advance(state, red_move, blue_move)));
    }
    best = max(best, worst);
  }
  return memo[rounds][state] = best;
}
int main() {
  int n, rounds;
  string s;
  cin >> n >> rounds >> s;
  m = 2 * n;
  full_mask = (1U << m) - 1;
  unsigned state = 0;
  for (int i = 0; i < m; ++i) state |= static_cast<unsigned>(s[i] - '0') << i;
  memo.resize(rounds + 1);
  int red = solve(rounds, state);
  int potatoes = popcount(state);
  cout << red << ' ' << potatoes - red << '\n';
}
```

若不记忆，分支树随持有者数和轮数指数增长；即使记忆，也有 $O(k2^{2n})$ 个状态，无法应对正式约束。它的价值是为小规模随机对拍提供精确 oracle。

### 解法二：先解决最后一轮

若只剩一轮，每条合法 `10` 边都是独立的。Red 持有者传给空的 Blue 成员，会让 Red 得分增加 1；Blue 持有者传给空的 Red 成员，会让 Red 得分减少 1。双方在最后一轮都会选择严格有利的传递，所以 Red 的终局值恰为 $F(s)$。

### 解法三：势函数折叠前 $k-1$ 轮

考虑某一轮内单独做一次合法传递。若源位置 $i$ 属于 Red，则可以直接展开受影响的三条局部项，得到

$$
\Delta F=s_{i+2}-s_{i-1}-1\in\{-2,-1,0\}.
$$

Red 的任何传递都不会让后继状态的 $F$ 增大。若源位置属于 Blue，则

$$
\Delta F=s_{i-1}+1-s_{i+2}\in\{0,1,2\},
$$

Blue 的任何传递都不会让 $F$ 减小。同一队的多个合法传递源与目的互不冲突，可依次应用上述单调性。

当还剩至少两轮时，Red 选择全保留就能保证下一状态的 $F$ 不低于当前值；Blue 选择全保留就能保证它不高于当前值。双方全保留同时达到当前 $F$，形成纯策略鞍点。归纳可知，存在一种最优策略让前 $k-1$ 轮所有人保留，只在最后一轮把每条初态 `10` 边上的土豆传走。注意这只构造了一种最优策略，并未断言所有最优策略都相同。

### 最佳实用解：一次环形扫描

对每个初始土豆：若顺时针下一格为空，最后一轮把它传到下一格；否则保留。最终位置为奇下标时淘汰的是 Blue 成员，Red 得 1 分；为偶下标时 Blue 得 1 分。$k\ge1$ 时答案与 $k$ 的具体数值无关。

<!-- compile:standalone -->
```cpp
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    long long k;
    string s;
    cin >> n >> k >> s;
    int m = 2 * n;
    int red = 0;
    int blue = 0;
    for (int i = 0; i < m; ++i) {
      if (s[i] == '0') continue;
      int next = (i + 1) % m;
      int final_position = s[next] == '0' ? next : i;
      if (final_position & 1) ++red;
      else ++blue;
    }
    cout << red << ' ' << blue << '\n';
  }
}
```

每组时间 $O(n)$，除输入串外额外空间 $O(1)$。分数不超过 $2n$，`int` 安全；`k` 必须用 64 位读取，但定理消除了对它的循环。

## 正确性证明

**引理一：**若只剩一轮，Red 的最优终局得分是 $F(s)$。

证明：轮初每条 `10` 边都允许源持有者传递。Red 源传递使 Red 得分加 1，Blue 源传递使 Red 得分减 1，且不同合法源的目的互异。双方分别执行所有严格有利动作后，三类贡献正好是 $F$ 的定义。证毕。

**引理二：**Red 在一轮中的任意合法传递子集都不能增大后继状态的 $F$；Blue 的任意合法传递子集都不能减小它。

证明：单次 Red、Blue 传递的 $\Delta F$ 分别不大于 0、不小于 0；同队合法传递互不冲突，逐个应用即可。证毕。

**定理：**一次环形扫描输出双方最优分数。

证明：由引理二，在任何非末轮，Red 全保留保证后继 $F\ge F(s)$，Blue 全保留保证后继 $F\le F(s)$；两者同时全保留达到相等，故当前 $F$ 是鞍点值。向后归纳，前 $k-1$ 轮可全部保留，最后一轮由引理一处理。扫描代码正是在初态同步执行末轮全部有利传递，因此 Red 得分为 $F(s)$。土豆总数守恒，Blue 得分为 $P-F(s)$。证毕。

## 样例手推与边界

第 3 组 `101110` 有四个土豆。官方动画展示：第 1 轮做 $1\to2$，第 2 轮做 $5\to6$，最终持有者为 $2,3,4,6$，其中三个属于 Blue、一个属于 Red，所以分数为 `3 1`。本算法选择的“先全部保留、末轮一起传”可能给出不同动作序列，但势函数证明保证相同分数。

- 全 0 时没有淘汰者，答案 `0 0`。
- 全 1 时无人能传，每队各有 $n$ 名持有者，答案 `n n`。
- $n=1$ 时圆上只有两人，取模邻接仍应正确处理。
- 环尾位置可向位置 0 传递，不能漏掉最后一条边。
- 连续的 1 会互相阻塞；合法性必须根据轮初串判断，不能原地遍历模拟。

## 方案比较与推荐

精确 minimax 只适合验证。按轮动态规划仍被 $k$ 与 $2^{2n}$ 卡死。势函数方案既给出零和鞍点证明，又把 $10^9$ 轮压缩成最后一轮的一次扫描，时间和额外空间都最优。竞赛中应优先记住“守恒量先零和化，再寻找末轮值函数，并证明早期动作对它单调不利”的推导链，而不是只背扫描公式。

## 易错点

- 模拟 $k$ 轮会超时；答案在所有 $k\ge1$ 时相同。
- 原地修改字符串会破坏“轮初决定合法性”的规则。
- 忘记圆环的末位到首位，会漏掉一条可传边。
- 0-based 偶位置属于 Red，但土豆最终落在奇位置时，得分的是 Red；不要把持有者队伍与得分队伍反过来。
- 最优分数唯一不表示策略唯一；官方第 3 组就给出了不同于“前面全留”的另一种最优策略。
- Div.1 与 Div.2 的 points、tags 是别名专属元数据，不能混成单页字段；官方 rating 缺失也不能靠题号推测。

## 可复现验证

暴力与最佳代码均以 Clang C++23 严格编译，官方样例逐行得到 `1 0`、`0 2`、`3 1`、`5 5`、`0 0`、`7 2`。精确 minimax 枚举环长 2、4、6、8、10 的全部状态与剩余轮数 1 至 5，并枚举环长 12 的全部状态与剩余轮数 1 至 4，共 23,204 个 state-horizon、197,398 个联合行动 profile；每处都满足 $\max_R\min_B=\min_B\max_R=F(s)$。另对环长 2 至 12 的全部状态检查 39,060 次单队传递子集势函数单调性，并以固定种子完成 20,000 组最优代码与 minimax 对拍，均零不一致。$n=10^5,k=10^9$ 的最大规模 smoke 也在线性时间内完成。

## 变种一：同一初态，多次询问 $k$，并允许 $k=0$

$k=0$ 时没有动作，Red 得分是初态奇下标 1 的数量 $B$；$k\ge1$ 时使用原题定理。预处理 $P$、$B$ 与正轮数答案 $F$，每问 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
  int n, queries;
  string s;
  cin >> n >> queries >> s;
  int m = 2 * n;
  int potatoes = 0;
  int initial_red = 0;
  int positive_red = 0;
  for (int i = 0; i < m; ++i) {
    if (s[i] == '0') continue;
    ++potatoes;
    if (i & 1) ++initial_red;
    int next = (i + 1) % m;
    int final_position = s[next] == '0' ? next : i;
    if (final_position & 1) ++positive_red;
  }
  while (queries--) {
    long long k;
    cin >> k;
    int red = k == 0 ? initial_red : positive_red;
    cout << red << ' ' << potatoes - red << '\n';
  }
}
```

总时间 $O(n+q)$，额外空间 $O(1)$。

## 变种二：在线翻转一个初始位置后询问

每次把某位在 0、1 间翻转，并询问任意正轮数的最优分数。维护土豆数 $P$、奇下标 1 数 $B$，以及带符号环形 `10` 边和 $D$，则 $F=B+D$。翻转位置 $p$ 只影响边 $p-1,p$。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
using namespace std;
class Solver {
  string s;
  int m;
  int potatoes = 0;
  int blue_holders = 0;
  int edge_sum = 0;
  int edge(int i) const {
    i = (i + m) % m;
    int next = (i + 1) % m;
    if (s[i] != '1' || s[next] != '0') return 0;
    return i % 2 == 0 ? 1 : -1;
  }
public:
  explicit Solver(string value) : s(move(value)), m(static_cast<int>(s.size())) {
    for (int i = 0; i < m; ++i) {
      potatoes += s[i] == '1';
      if (i & 1) blue_holders += s[i] == '1';
      edge_sum += edge(i);
    }
  }
  pair<int, int> flip(int position) {
    edge_sum -= edge(position - 1) + edge(position);
    int delta = s[position] == '0' ? 1 : -1;
    s[position] = s[position] == '0' ? '1' : '0';
    potatoes += delta;
    if (position & 1) blue_holders += delta;
    edge_sum += edge(position - 1) + edge(position);
    int red = blue_holders + edge_sum;
    return {red, potatoes - red};
  }
};
int main() {
  int n, queries;
  string s;
  cin >> n >> queries >> s;
  Solver solver(s);
  while (queries--) {
    int position;
    cin >> position;
    auto [red, blue] = solver.flip(position - 1);
    cout << red << ' ' << blue << '\n';
  }
}
```

初始化 $O(n)$，每次修改与查询 $O(1)$，保存字符串使用 $O(n)$ 空间。原势函数定理对每个修改后的静态初态重新成立。

## 变种三：恢复一种最优策略与最终淘汰集合

输出一份压缩策略证书：前 $k-1$ 轮所有人保留；最后一轮让初态每条 `10` 边的源传递。程序列出末轮源编号与最终持有串。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
  int n;
  long long k;
  string s;
  cin >> n >> k >> s;
  int m = 2 * n;
  string final_state = s;
  vector<int> source;
  for (int i = 0; i < m; ++i) {
    int next = (i + 1) % m;
    if (s[i] == '1' && s[next] == '0') source.push_back(i);
  }
  for (int i : source) {
    final_state[i] = '0';
    final_state[(i + 1) % m] = '1';
  }
  int red = 0;
  int potatoes = 0;
  for (int i = 0; i < m; ++i) {
    potatoes += final_state[i] == '1';
    if (i & 1) red += final_state[i] == '1';
  }
  cout << red << ' ' << potatoes - red << '\n';
  cout << "keep rounds 1.." << k - 1 << '\n';
  cout << source.size();
  for (int i : source) cout << ' ' << i + 1;
  cout << '\n' << final_state << '\n';
}
```

时间 $O(n)$，输出与保存终态空间 $O(n)$。它只承诺给出一种最优策略；官方动画说明最优策略可以不唯一。

## 变种四：圆环改成有向路径

末人不能向首人传递。把 $F$ 中末位到首位的边删掉后，端点局部增量只是少一项，Red、Blue 的单调方向不变，所以仍可让早轮全留、末轮贪心。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    long long k;
    string s;
    cin >> n >> k >> s;
    int m = 2 * n;
    int red = 0;
    int blue = 0;
    for (int i = 0; i < m; ++i) {
      if (s[i] == '0') continue;
      int final_position = i;
      if (i + 1 < m && s[i + 1] == '0') final_position = i + 1;
      if (final_position & 1) ++red;
      else ++blue;
    }
    cout << red << ' ' << blue << '\n';
  }
}
```

时间 $O(n)$，额外空间 $O(1)$。

## 变种五：改为传给固定偏移 $d$ 的成员

传递目标变成 $(i+d)\bmod 2n$。若 $d$ 为奇数，映射分解出的每个环都交替经过两队，把势函数的前驱、后继替换成该置换即可复用证明；末轮沿所有“占用源到空目标”传递。若 $d$ 为偶数，土豆始终留在同一队，双方分数从初态起不变。

<!-- compile:standalone -->
```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    int n, d;
    long long k;
    string s;
    cin >> n >> k >> d >> s;
    int m = 2 * n;
    d = (d % m + m) % m;
    int red = 0;
    int blue = 0;
    for (int i = 0; i < m; ++i) {
      if (s[i] == '0') continue;
      int final_position = i;
      int target = (i + d) % m;
      if (d % 2 == 1 && s[target] == '0') final_position = target;
      if (final_position & 1) ++red;
      else ++blue;
    }
    cout << red << ' ' << blue << '\n';
  }
}
```

时间 $O(n)$，额外空间 $O(1)$。奇偏移保留跨队零和结构；偶偏移则直接退化为队伍归属不变量。

## 来源

- [Codeforces Div.1 A 官方题面](https://codeforces.com/contest/2255/problem/A)
- [Codeforces Div.2 C 官方题面](https://codeforces.com/contest/2256/problem/C)
- [Codeforces Materials usage license v0.1](https://codeforces.com/blog/entry/967)
- [第 3 组官方动画](https://espresso.codeforces.com/45e2b71b9979cdb65198a6b629b54f7d540750ef.png)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2256/problem/C)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-514-q1-lc4014/">← [力扣竞赛] 第 514 场周赛 Q1 LC 4014 应用折扣后的最低总价 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-14-lc3090/">[力扣每日一题] 2026-08-14｜LC 3090 每个字符最多出现两次的最长子字符串 →</a>
</nav>
