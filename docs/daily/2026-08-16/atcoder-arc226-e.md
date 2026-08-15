---
title: "[atcoder] ARC226 E Cellular Messenger"
---

# [atcoder] ARC226 E Cellular Messenger

<p class="daily-archive-kicker">2026-08-16 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-16 题目列表</a> · <a href="../../../math/modular-constructions/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=27a9b30d792599e4db465c9baf6916c8a503d0215da49cfc0f0010262d6e1481 -->
[Official problem: ARC226 E - Cellular Messenger](https://atcoder.jp/contests/arc226/tasks/arc226_e?lang=en)

## 官方来源与元数据

- 比赛：UNIQUE VISION Programming Contest 2026 Summer（AtCoder Regular Contest 226）。
- 题目：E - Cellular Messenger。
- 比赛时间：2026-08-09 21:00–23:00（JST）。
- 官方分值：1000 分；比赛 rated 范围：1200–2799。
- 官方难度：AtCoder 未标注。
- 时间限制：2 秒；内存限制：1024 MiB。
- AtCoder Problems 社区估算难度：3505，核对于 2026-08-16；这不是 AtCoder 官方难度。
- [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)；[官方题解](https://atcoder.jp/contests/arc226/editorial/23908?lang=en)。

下方英文层是模型逐项阅读官方页面后独立组织的自包含呈现。任务页没有给出题目专属开放
转载许可；官方页面与服务条款仍是权威来源。坐标示意图只解释下方为行号增大方向、右方为
列号增大方向，本文已用文字完整给出该语义。

## Complete English statement

Snuke wants to build a cellular automaton that transmits an arbitrary binary sequence. The automaton
operates on an infinite grid. Every cell has state 0 or 1. Rows increase downward, columns increase to
the right, and a cell is denoted by $(r,c)$. Its eight neighbors are the cells that share an edge or a
corner with it.

You choose a rectangle with top-left cell $(0,0)$, height $H$, and width $W$, where
$1\le H,W\le150$. You set every initial state $A_{r,c}$ inside this rectangle; every cell outside it
starts at 0.

You also choose an update rule $F_{i,j}\in\{0,1\}$ for $i\in\{0,1\}$ and
$j\in\{0,1,\ldots,8\}$. The mandatory condition is $F_{0,0}=0$. During one update, all cells change
simultaneously. If a cell currently has state $i$ and exactly $j$ of its eight neighbors have state 1,
its next state is $F_{i,j}$.

Finally, choose a sending cell $(R_s,C_s)$, a receiving cell $(R_t,C_t)$, and a delay $D$. Both cells
must lie in the rectangle, $50\le |C_s-C_t|\le100$, and $50\le D\le100$.

For each test, the judge fixes a positive integer $N$ and a binary sequence
$S=(S_1,S_2,\ldots,S_N)$. Starting from your initial configuration, it performs $N+D-1$ turns. On
turn $k$ it does the following in order:

1. If $k\le N$, overwrite the sending cell with $S_k$.
2. Apply one simultaneous update to the whole grid.
3. If $D\le k<D+N$, append the receiving cell's new state to a sequence $T$.

Your fixed design is correct if $T=S$ for every judge test. A universally correct design exists. The
implementation uses only tests with $1\le N\le300$, but the intended construction works for every
positive $N$ and every binary sequence.

### Input

This is an output-only construction problem and provides no input.

### Output

Print exactly this structure:

```text
F_0,0 F_0,1 ... F_0,8 as one 9-bit string
F_1,0 F_1,1 ... F_1,8 as one 9-bit string
H W
A_0,0 A_0,1 ... A_0,W-1
...
A_H-1,0 A_H-1,1 ... A_H-1,W-1
R_s C_s R_t C_t D
```

The spaces shown inside the symbolic bit-string descriptions are explanatory only: each rule and each
grid row must be printed as a contiguous binary string. All chosen values must satisfy the ranges above.

### Constraints

- $F_{0,0}=0$ and every $F_{i,j}$ is either 0 or 1.
- $1\le H,W\le150$.
- The sending and receiving cells both lie inside the printed rectangle.
- $50\le |C_s-C_t|\le100$ and $50\le D\le100$.
- Every judge sequence is nonempty; the implementation uses $1\le N\le300$.

### Complete official sample output

```text
000100000
001100000
4 54
100000000000000000000000000000000000000000000000000000
000010000000000000000000000000000000000000000000000000
100010000000000000000000000000000000000000000000000000
011110000000000000000000000000000000000000000000000000
0 3 0 53 100
```

The official note says this output only illustrates the format. It is correct for every sequence when
$N=1$, but some sequences fail when $N\ge2$. The official page also provides a visualizer for testing
an output design.

## 中文题意解释

我们要一次性打印一个有限初态和一个只看“自身旧状态、八邻居中 1 的个数”的全局规则。
Judge 随后每轮强制把一个输入位写进发送格，再让整个无限网格同步演化。目标是让接收格恰好
延迟固定的 $D$ 轮重现每一位，且连续输入之间不能互相污染。

这不是读取输入再计算答案，而是设计一根由生命类自动机实现的数字电缆。关键难点有两个：

1. 总计数规则如何在某一行模拟“左右两格异或”；
2. 有限长电缆如何既延迟 63 轮，又在旧脉冲离开时彻底清零。

## 约束推导与构造目标

$D$ 与水平距离都必须在 50 到 100 之间。取

$$
H=3,\qquad W=65,\qquad (R_s,C_s)=(1,0),\qquad
(R_t,C_t)=(1,63),\qquad D=63
$$

即可同时满足范围。令第 0、2 行全为 1，夹住中间全 0 的一行。对中间行的内部格，来自
上下两条“轨道”的邻居恰有 6 个固定的 1；若左右中间格之和为 0、1、2，则八邻居中的 1
总数分别为 6、7、8。因此只要在 $j=6,7,8$ 时令下一状态为 $0,1,0$，中间格就实现

$$
x_c' = x_{c-1}\oplus x_{c+1},
$$

即一维元胞自动机 Rule 90。规则还要让上下轨道在自身为 1、邻居数为 1 到 5 时保持 1。
这正好对应两行规则 `000000010` 与 `011111010`。

## 解法一：直接搜索小型自动机作为暴力

最朴素的验证方式是枚举规则、矩形初态、端点与延迟，再穷举所有短输入串并模拟足够多的
网格。枚举空间至少有 $2^{18+HW}$，不能作为正式算法；但固定候选设计后，穷举短串是很好
的独立 oracle。下面程序验证本构造对所有长度不超过 10 的输入都逐位正确。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  const string rule[2] = {"000000010", "011111010"};
  const int delay = 63;
  for (int length = 1; length <= 10; ++length) {
    for (int mask = 0; mask < (1 << length); ++mask) {
      vector<vector<int>> grid(9, vector<int>(141));
      for (int column = 38; column < 103; ++column) {
        grid[3][column] = 1;
        grid[5][column] = 1;
      }
      vector<int> received;
      for (int turn = 1; turn <= length + delay - 1; ++turn) {
        if (turn <= length) grid[4][38] = mask >> (turn - 1) & 1;
        vector<vector<int>> next(9, vector<int>(141));
        for (int row = 1; row + 1 < 9; ++row) {
          for (int column = 1; column + 1 < 141; ++column) {
            int neighbors = 0;
            for (int dr = -1; dr <= 1; ++dr) {
              for (int dc = -1; dc <= 1; ++dc) {
                if (dr != 0 || dc != 0) {
                  neighbors += grid[row + dr][column + dc];
                }
              }
            }
            next[row][column] = rule[grid[row][column]][neighbors] - '0';
          }
        }
        grid.swap(next);
        if (delay <= turn) received.push_back(grid[4][101]);
      }
      for (int i = 0; i < length; ++i) {
        if (received[i] != (mask >> i & 1)) return 1;
      }
    }
  }
  cout << "verified\n";
}
```

固定一个设计时，模拟时间与“输入长度 × 模拟网格面积”成正比；若再枚举全部设计则指数
爆炸。它的价值是找反例，而不是产生最终答案。

## 从局部规则到有限电缆

把中间行第 1 到 63 格写成列向量 $v$，其一次自然更新是

$$
v'=Av+e_1s,
$$

其中运算位于 $\mathbb F_2$，$A$ 是 63 个顶点路径图的邻接矩阵，$s$ 是当前发送位。
路径邻接矩阵的特征多项式满足

$$
p_0(x)=1,\quad p_1(x)=x,\quad p_m(x)=xp_{m-1}(x)+p_{m-2}(x).
$$

在特征 2 中，$m=2^6-1=63$ 时递推得到 $p_{63}(x)=x^{63}$。由 Cayley–Hamilton
定理，$A^{63}=0$。另一方面，从第 1 格走到第 63 格至少要 62 条边；发送格在本轮更新时
先进入第 1 格，所以一个脉冲恰在第 63 次更新到达接收格。唯一最短路径使该系数为 1。

于是每个输入脉冲经过 63 轮在接收格出现，之后其整段内部状态归零。Rule 90 是线性规则，
多个不同轮次的脉冲可在 $\mathbb F_2$ 上叠加而不干扰，连续任意长输入也成立。

## 最佳实用解：打印 3 × 65 的 Rule 90 电缆

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  cout << "000000010\n";
  cout << "011111010\n";
  cout << "3 65\n";
  cout << string(65, '1') << '\n';
  cout << string(65, '0') << '\n';
  cout << string(65, '1') << '\n';
  cout << "1 0 1 63 63\n";
}
```

程序没有输入，运行时间和额外空间都是 $O(W)=O(65)$。输出满足 $H,W\le150$、水平距离
63、延迟 63，以及 $F_{0,0}=0$。相比盲搜，这一构造的局部规则、传播时间与脉冲清除都能
分别证明，是应优先记忆的方案。

## 正确性证明

**引理 1：边界稳定，中间内部格执行 Rule 90。**

上下轨道中状态为 1 的格只会遇到 1 到
5 个活邻居，规则 `011111010` 使其保持 1。矩形外的 0 格至多看到 3 个活邻居，不会触发
`F_{0,7}=1`；中间第 64 列的固定 0 至多看到 5 个活邻居，也不会变成 1。发送格第 0 列
在每轮更新前被覆盖为本轮输入位，它有 4 或 5 个活邻居；规则在这些邻居数下让 0 保持 0、
让 1 保持 1，因此本次更新后仍等于该输入位。
中间第 1 到 63 格有 6 个固定轨道邻居，邻居总数是
$6+x_{c-1}+x_{c+1}$；两条规则在 6、7、8 上都给出 0、1、0，故下一状态是
$x_{c-1}\oplus x_{c+1}$，与自身旧状态无关。

**引理 2：单个输入位恰延迟 63 轮到达，随后不留残影。**

第一次更新把发送位送入第 1
格。每轮信息最多移动一列，因此在第 63 次更新以前不能到达第 63 格；第 63 次更新对应
唯一的全向右路径，系数为 1。上节证明 $A^{63}=0$，所以再推进一轮时该脉冲在电缆内部的
状态已经归零。

**定理：Judge 读出的 $T$ 等于任意输入 $S$。**

Rule 90 对异或线性，每个 $S_k$ 的响应
可独立叠加。引理 2 表明它只在应读取的第 $k+62$ 轮为接收格贡献 $S_k$，其他输入的贡献
按各自延迟对齐。故每个输出位置都等于对应输入位，$T=S$。

## 样例手推与边界

对单脉冲 `1`，第 1 次更新后列 1 为 1；其后 Rule 90 产生熟悉的 Sierpiński 三角形。
第 63 次更新时列 63 为 1，第 64 次更新后内部 63 格全部为 0。若下一轮又写入 1，两幅图形
会异或叠加，但线性保证各自在接收端仍只贡献自己的时间槽。

- 输入全 0：中间行保持全 0，接收端持续为 0。
- 连续全 1：波形大量重叠，线性叠加仍逐位恢复。
- $N=1$ 与 $N=300$：证明不依赖长度；后者只是 Judge 的实现上限。
- 发送格被每轮强制覆盖：构造正是把这次覆盖作为新的边界输入，不依赖它的自然旧状态。
- 无限网格：规则满足 $F_{0,0}=0$，远离有限结构的 0 不会凭空产生无限活动。

## 方案比较与易错点

- 只证明“信号能传到”不够；还必须证明延迟精确、旧信号清除且连续输入可叠加。
- `D=63` 对应本轮写入后立即做第一次更新，不能误写成 62 或 64。
- 中间向量长度是 63，右侧第 64 列充当固定 0 边界；接收格是列 63。
- `F` 的字符串下标就是邻居数 0 到 8，`000000010` 的 1 位于下标 7。
- 官方样例只是格式示例，并非通用正确构造，不能直接提交样例输出。

## 验证说明

最终生成器以 GNU++23 编译并逐字符核对 5 行输出。独立模拟器在比构造更大的有限窗口内穷举
了所有长度 1 到 10 的二进制串，共 2046 个输入，全部恢复正确；另以矩阵递推验证
$A^{63}=0$、单脉冲第 63 轮到达且下一轮内部清零。

## 变种一：距离为 $2^q-1$ 的通用电缆

新定义允许自行选择更大的尺寸与延迟，要求传输距离 $L=2^q-1$。同一特征多项式归纳给出
$p_L(x)=x^L$，所以只需把上下轨道宽度改为 $L+2$，接收列改为 $L$，延迟设为 $L$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int q;
  cin >> q;
  int length = (1 << q) - 1;
  cout << "000000010\n" << "011111010\n";
  cout << 3 << ' ' << length + 2 << '\n';
  cout << string(length + 2, '1') << '\n';
  cout << string(length + 2, '0') << '\n';
  cout << string(length + 2, '1') << '\n';
  cout << 1 << ' ' << 0 << ' ' << 1 << ' ' << length << ' ' << length << '\n';
}
```

生成时间和输出空间为 $O(2^q)$。原题的 50 到 100 范围只容纳 $q=6$ 的 63；变种放宽了
尺寸约束，算法与证明不变。

## 变种二：反向传输

新定义要求从右向左传输。Rule 90 关于左右镜像对称，只需交换发送与接收列，其他规则与
初态完全不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  cout << "000000010\n" << "011111010\n";
  cout << "3 65\n";
  cout << string(65, '1') << '\n';
  cout << string(65, '0') << '\n';
  cout << string(65, '1') << '\n';
  cout << "1 63 1 0 63\n";
}
```

复杂度仍为 $O(65)$；邻接矩阵在镜像置换下不变，所以延迟与清零证明原样成立。

## 变种三：两条互不干扰的并行信道

新定义允许两个发送端和两个接收端，并把矩形高度上限放宽。将两条 3 行电缆之间隔至少
两行 0，使任一格的八邻域不能跨越到另一条轨道；两路即可独立工作。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  const int height = 8;
  const int width = 65;
  vector<string> grid(height, string(width, '0'));
  for (int row : {0, 2, 5, 7}) grid[row] = string(width, '1');
  cout << "000000010\n" << "011111010\n";
  cout << height << ' ' << width << '\n';
  for (const string& row : grid) cout << row << '\n';
  cout << "1 0 1 63 63\n";
  cout << "6 0 6 63 63\n";
}
```

生成时间 $O(HW)$，两路各自的动态仍是 $O(NL)$。原题输出协议只有一对端点，因而不能直接
提交这段；它说明局部性如何扩展为多信道硬件。

## 变种四：为任意候选设计编写确定性验证器

新定义给定规则、有限初态、端点、延迟与一个输入串，输出实际接收串。对活动结构外再留
足够安全边界后逐轮同步更新，可复现排查延迟偏一和轨道泄漏。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string rule[2];
  int height, width;
  cin >> rule[0] >> rule[1] >> height >> width;
  vector<string> initial(height);
  for (string& row : initial) cin >> row;
  int senderRow, senderColumn, receiverRow, receiverColumn, delay;
  string bits;
  cin >> senderRow >> senderColumn >> receiverRow >> receiverColumn >> delay;
  cin >> bits;
  int margin = static_cast<int>(bits.size()) + delay + 2;
  int rows = height + 2 * margin;
  int columns = width + 2 * margin;
  vector<vector<int>> grid(rows, vector<int>(columns));
  for (int i = 0; i < height; ++i) {
    for (int j = 0; j < width; ++j) {
      grid[i + margin][j + margin] = initial[i][j] - '0';
    }
  }
  string received;
  int turns = static_cast<int>(bits.size()) + delay - 1;
  for (int turn = 1; turn <= turns; ++turn) {
    if (turn <= static_cast<int>(bits.size())) {
      grid[senderRow + margin][senderColumn + margin] = bits[turn - 1] - '0';
    }
    vector<vector<int>> next(rows, vector<int>(columns));
    for (int i = 1; i + 1 < rows; ++i) {
      for (int j = 1; j + 1 < columns; ++j) {
        int neighbors = 0;
        for (int di = -1; di <= 1; ++di) {
          for (int dj = -1; dj <= 1; ++dj) {
            if (di != 0 || dj != 0) neighbors += grid[i + di][j + dj];
          }
        }
        next[i][j] = rule[grid[i][j]][neighbors] - '0';
      }
    }
    grid.swap(next);
    if (turn >= delay) {
      received += char('0' + grid[receiverRow + margin][receiverColumn + margin]);
    }
  }
  cout << received << '\n';
}
```

若输入长为 $N$、安全窗口面积为 $G$，时间为 $O((N+D)G)$，空间为 $O(G)$。它不取代普适
证明，但能把候选规则与具体输入的状态演化完整复现。

## 来源

- [AtCoder 官方题面](https://atcoder.jp/contests/arc226/tasks/arc226_e?lang=en)
- [AtCoder 官方题解](https://atcoder.jp/contests/arc226/editorial/23908?lang=en)
- [AtCoder Problems](https://kenkoooo.com/atcoder/#/table/)
- [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc226/tasks/arc226_e?lang=en)
- [对应知识专题](../../math/modular-constructions.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-136-lc118/">[力扣 Top 136] LC 118 杨辉三角 简单 →</a>
</nav>
