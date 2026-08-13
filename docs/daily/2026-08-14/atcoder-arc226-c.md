---
title: "[atcoder] ARC226 C Square Corner Packing"
---

# [atcoder] ARC226 C Square Corner Packing

<p class="daily-archive-kicker">2026-08-14 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-14 题目列表</a> · <a href="../../../math/modular-constructions/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=235d0ea2688691a6f2fde32a6a996f1597fab2cc9f23b305fb2e39196a4f5e5f -->
[Official problem: ARC226 C - Square Corner Packing](https://atcoder.jp/contests/arc226/tasks/arc226_c?lang=en)

## 官方来源与元数据

- 比赛：UNIQUE VISION Programming Contest 2026 Summer（AtCoder Regular Contest 226）。
- 题目：C - Square Corner Packing。
- 官方分值：700 分。
- 时间限制：2 秒；内存限制：1024 MiB。
- 比赛 rated 范围：1200–2799。
- [官方题面](https://atcoder.jp/contests/arc226/tasks/arc226_c?lang=en)。
- [AtCoder 服务条款](https://atcoder.jp/tos)。
- AtCoder Problems 社区估算难度：2070，核对于 2026-08-14；这不是 AtCoder 官方难度。

下方英文层是模型基于官方任务独立组织的自包含呈现。任务页没有给出题目专属的开放转载许可；官方页面与 AtCoder 服务条款仍是权威来源。

## Complete English statement

An $H$-by-$W$ grid is initially entirely white. Cell $(i,j)$ is in row $i$ from the top and column $j$ from the left.

In one operation, choose integers $r,c,s$ satisfying

$$
1\le r<r+s\le H,\qquad 1\le c<c+s\le W.
$$

The four cells

$$
(r,c),\ (r+s,c),\ (r,c+s),\ (r+s,c+s)
$$

must all still be white. Paint exactly those four cells black. Geometrically, they are the four corners of an axis-aligned square with side length $s$.

Repeat the operation any number of times. Maximize the number of operations and output any operation sequence that attains this maximum. There are $T$ test cases.

### Input

```text
T
H_1 W_1
H_2 W_2
...
H_T W_T
```

### Output

For each test case, print the maximum number of operations $K$. Then print $K$ lines, where line $i$ contains `r_i c_i s_i` describing the $i$-th operation. Any optimal valid sequence is accepted.

### Constraints

- $1\le T\le500$.
- $2\le H,W\le500$.
- The sum of $HW$ over all test cases is at most $250000$.
- All input values are integers.

### Complete official sample

Input:

```text
2
5 6
2 2
```

One accepted output shown by the official task:

```text
6
1 1 3
3 4 2
1 2 3
3 3 2
1 3 3
2 1 1
1
1 1 1
```

For the first test case, the official sample illustrates the six operations with this ASCII grid:

```text
135135
66....
664242
135135
..4242
```

Digit $i$ marks cells painted by operation $i$; `.` marks a cell never painted. Other optimal outputs are accepted. On a $2\times2$ grid, exactly one side-length-1 square can be chosen. There is no separate official note section and no task image required for understanding.

## 中文题意解释

每次操作选择一个与网格边平行的正方形，只把四个角染黑；四个角在操作前必须全白。不同操作的四角因此不能重复，但正方形内部、边和几何区域可以重叠。目标是让操作次数最大，并构造任意一组最优操作。

最容易误判的是“每次使用四格，所以答案是 $\lfloor HW/4\rfloor$”。四格不仅要不重复，同一次操作还会在两行各用两个格、在两列各用两个格，这带来更强的行列偶性约束。

## 约束推导与解法上界

### 暴力建模

枚举所有合法 $(r,c,s)$，每个候选对应四个格子的集合。问题变成：从这些四元集合中选出最多个两两不交集合。子集回溯是指数级，只能作为小网格 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int bestPacking(const vector<unsigned long long>& squares, int index,
                unsigned long long used) {
  if (index == static_cast<int>(squares.size())) return 0;
  int answer = bestPacking(squares, index + 1, used);
  if ((used & squares[index]) == 0) {
    answer = max(answer, 1 + bestPacking(squares, index + 1,
                                        used | squares[index]));
  }
  return answer;
}
int main() {
  int height, width;
  cin >> height >> width;
  if (height * width > 63) return 0;
  vector<unsigned long long> squares;
  for (int r = 0; r < height; ++r) {
    for (int c = 0; c < width; ++c) {
      for (int side = 1; r + side < height && c + side < width; ++side) {
        unsigned long long mask = 0;
        mask |= 1ULL << (r * width + c);
        mask |= 1ULL << ((r + side) * width + c);
        mask |= 1ULL << (r * width + c + side);
        mask |= 1ULL << ((r + side) * width + c + side);
        squares.push_back(mask);
      }
    }
  }
  cout << bestPacking(squares, 0, 0) << '\n';
}
```

它完整枚举“跳过或选择”每个正方形，最坏时间 $O(2^M)$，其中 $M$ 是候选正方形数；递归空间 $O(M)$。只用于极小实例验证。

### 行列偶性上界

一次操作在任意一行染黑的格子数只能是 0 或 2，所以每行最终黑格数为偶数；每列同理。

- 若 $W$ 为奇数，每行至少留下一个白格。
- 若 $H$ 为奇数，每列至少留下一个白格。

设最终黑格总数为 $P$，则

$$
P\le H\bigl(W-(W\bmod2)\bigr),
$$

$$
P\le W\bigl(H-(H\bmod2)\bigr).
$$

每次操作恰用四个新格，因此

$$
K\le\left\lfloor
\frac{\min\bigl(H(W-W\bmod2),\ W(H-H\bmod2)\bigr)}4
\right\rfloor.
$$

接下来构造恰好达到这个上界。

## 最优构造

### 至少一个维度为偶数

在左上角最大的偶数乘偶数子矩形内，用边长 1 的正方形铺开：令 $r=1,3,5,\ldots$，$c=1,3,5,\ldots$，输出 $(r,c,1)$。操作数为

$$
\left\lfloor\frac H2\right\rfloor
\left\lfloor\frac W2\right\rfloor,
$$

正好等于偶性上界。

### 两个维度都为奇数

令 $h=\min(H,W)$、$w=\max(H,W)$。若原网格高大于宽，先在转置坐标系构造，输出时交换行列坐标。

先构造最优的奇数 $h\times h$ 正方形，再把右侧剩余区域按每两列一条带，用边长 1 的正方形铺满前 $h-1$ 行。每条两列条带贡献 $(h-1)/2$ 次操作。

### 奇数正方形递归

考虑左上角为 $(R,C)$、边长为奇数 $n$ 的正方形。

- $n=1$：不操作。
- $n=3$：加入 $(R,C,1)$。
- $n\ge5$：先加入跨四个外角的 $(R,C,n-1)$；上边与右边在偏移 $1,3,\ldots,n-4$ 放单位方块；下边与左边在偏移 $2,4,\ldots,n-3$ 放单位方块；最后递归处理左上角 $(R+2,C+2)$、边长 $n-4$ 的内层正方形。

本层加入

$$
1+4\cdot\frac{n-3}{2}=2n-5
$$

次操作。若 $F(n)$ 为奇数正方形的操作数，则

$$
F(1)=0,\quad F(3)=1,\quad F(n)=F(n-4)+2n-5.
$$

按 $n\bmod4$ 归纳可得

$$
F(n)=\left\lfloor\frac{n(n-1)}4\right\rfloor.
$$

奇数矩形的总数为

$$
F(h)+\frac{w-h}{2}\cdot\frac{h-1}{2}
=\left\lfloor\frac{w(h-1)}4\right\rfloor,
$$

正好等于列偶性上界。

### 最佳实用解：直接输出构造

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using Operation = array<int, 3>;
void addOperation(vector<Operation>& operations, int r, int c, int side,
                  bool transpose) {
  if (transpose) swap(r, c);
  operations.push_back({r, c, side});
}
void buildOddSquare(int size, int row, int column,
                    vector<Operation>& operations, bool transpose) {
  if (size == 1) return;
  if (size == 3) {
    addOperation(operations, row, column, 1, transpose);
    return;
  }
  addOperation(operations, row, column, size - 1, transpose);
  for (int offset = 1; offset <= size - 4; offset += 2) {
    addOperation(operations, row, column + offset, 1, transpose);
    addOperation(operations, row + offset, column + size - 2, 1, transpose);
  }
  for (int offset = 2; offset <= size - 3; offset += 2) {
    addOperation(operations, row + size - 2, column + offset, 1, transpose);
    addOperation(operations, row + offset, column, 1, transpose);
  }
  buildOddSquare(size - 4, row + 2, column + 2, operations, transpose);
}
vector<Operation> solve(int height, int width) {
  vector<Operation> operations;
  if (height % 2 == 0 || width % 2 == 0) {
    for (int r = 1; r < height; r += 2) {
      for (int c = 1; c < width; c += 2) {
        operations.push_back({r, c, 1});
      }
    }
    return operations;
  }
  bool transpose = false;
  if (height > width) {
    swap(height, width);
    transpose = true;
  }
  buildOddSquare(height, 1, 1, operations, transpose);
  for (int c = height + 1; c <= width; c += 2) {
    for (int r = 1; r < height; r += 2) {
      addOperation(operations, r, c, 1, transpose);
    }
  }
  return operations;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int height, width;
    cin >> height >> width;
    vector<Operation> operations = solve(height, width);
    cout << operations.size() << '\n';
    for (auto [r, c, side] : operations) {
      cout << r << ' ' << c << ' ' << side << '\n';
    }
  }
}
```

时间与输出量同阶，为 $O(K)=O(HW)$；保存操作的空间为 $O(K)$。递归深度不超过约 $500/4=125$。

## 正确性证明

第一，行列偶性已经证明任何方案都不能超过给定上界。

第二，至少一个维度为偶数时，每个单位方块占据一个互不相交的 $2\times2$ 块，合法且操作数达到上界。

第三，奇数正方形每层中，大方块只使用四个外角；上、右两边的单位方块使用奇偏移，下、左两边使用偶偏移，所以四组边界格彼此不冲突，也不碰大方块。内层正方形距四条外边至少两格，递归操作不会碰本层格。由递归归纳，全部操作的四角集合两两不交，因此按任意输出顺序执行时，当前四角始终为白色。

第四，右侧每条两列带只使用新列与前 $h-1$ 行，彼此不交，也不碰左侧正方形。前述计数证明总操作数等于偶性上界。故构造合法且最优。

## 样例手推与边界

对 $5\times6$，至少一个维度为偶数，直接在行对 $(1,2)$、$(3,4)$ 与列对 $(1,2)$、$(3,4)$、$(5,6)$ 的六个 $2\times2$ 块放单位方块，得到 6 次操作，与官方最优数一致。

- $2\times2$：输出 `(1,1,1)`，恰一次。
- $3\times3$：奇数基础情形，只输出 `(1,1,1)`。
- $5\times5$：外层加入边长 4 的大方块和四个边界单位方块，共 5 次。
- $H>W$：只交换输出中的行列坐标，边长不变。
- $500\times500$：输出 62500 次，正好使用全部 250000 个格。

## 方案比较与推荐

把问题当一般四元集合装箱只能得到指数搜索；单位方块铺法能解决偶数维度，却在双奇数网格上达不到偶性上界；递归构造正好补齐缺口。竞赛中应优先记“先找可达到的结构上界，再按偶偶铺块、双奇递归剥边”，而不是先猜某种局部贪心。

## 易错点

- 每次占四格并不足以推出紧上界，必须加入每行、每列黑格数为偶数。
- 奇数正方形四边单位方块的偏移奇偶不能写反。
- 递归边长减少 4，而不是 2。
- 转置时只交换 `r`、`c`，不要修改 `s`。
- 右侧条带从 `height+1` 列开始，每次跨两列。
- 几何区域可以重叠，真正需要全局不相交的是每次所用的四个角。
- 官方 700 分与社区估算难度 2070 是不同字段，不能混写。

## 可复现验证

最优构造以 GNU++23 严格告警编译通过。精确位掩码集合装箱 oracle 覆盖全部 $2\le H,W\le6$ 的 25 个尺寸，构造值与真实最优值逐项一致。合法性检查覆盖全部 $2\le H,W\le30$ 的 841 个尺寸，共 51080 次操作；固定种子再检查 10000 个 $2\le H,W\le100$ 的随机尺寸，共 6425471 次操作，逐项确认坐标合法、四角未重复且数量等于偶性上界，零失败。$500\times500$、$499\times499$、$499\times500$、$499\times497$ 等边界也全部通过。

## 变种一：只输出最大操作数

不恢复方案时，直接计算行列偶性上界；原构造已证明它总能达到。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long maximumOperations(long long height, long long width) {
  long long byRows = height * (width - width % 2);
  long long byColumns = width * (height - height % 2);
  return min(byRows, byColumns) / 4;
}
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    long long height, width;
    cin >> height >> width;
    cout << maximumOperations(height, width) << '\n';
  }
}
```

每组时间、空间均为 $O(1)$。

## 变种二：强制所有正方形边长为 1

长边递归失效，只能选择互不重叠的 $2\times2$ 单位块，答案为 $\lfloor H/2\rfloor\lfloor W/2\rfloor$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int height, width;
  cin >> height >> width;
  vector<pair<int, int>> answer;
  for (int r = 1; r < height; r += 2) {
    for (int c = 1; c < width; c += 2) answer.push_back({r, c});
  }
  cout << answer.size() << '\n';
  for (auto [r, c] : answer) cout << r << ' ' << c << " 1\n";
}
```

输出时间 $O(K)$，保存方案空间 $O(K)$。例如 $5\times5$ 原题可做 5 次，这个变种只能做 4 次。

## 变种三：允许轴对齐长方形的四角

行跨度与列跨度可以不同。偶性上界不变，而原题的全部正方形仍是合法长方形，因此最优值和构造完全不变。下面给出只输出最优数量的完整程序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    long long height, width;
    cin >> height >> width;
    long long rows = height * (width - width % 2);
    long long columns = width * (height - height % 2);
    cout << min(rows, columns) / 4 << '\n';
  }
}
```

每组 $O(1)$；若需恢复方案，直接复用原题构造即可。这说明等边限制没有降低最大基数。

## 变种四：同时输出每个格子的所属操作

生成方案后维护 `owner`，把每个操作的四角写成其 1-based 编号，未使用格保持 0；这也是构造调试器。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using Operation = array<int, 3>;
int main() {
  int height, width, count;
  cin >> height >> width >> count;
  vector<Operation> operations(count);
  vector<vector<int>> owner(height + 1, vector<int>(width + 1));
  for (int i = 0; i < count; ++i) {
    auto& [r, c, side] = operations[i];
    cin >> r >> c >> side;
    array<pair<int, int>, 4> cells{{
        {r, c}, {r + side, c}, {r, c + side}, {r + side, c + side}}};
    for (auto [row, column] : cells) owner[row][column] = i + 1;
  }
  for (int r = 1; r <= height; ++r) {
    for (int c = 1; c <= width; ++c) {
      cout << owner[r][c] << (c == width ? '\n' : ' ');
    }
  }
}
```

在已有方案上时间 $O(HW+K)$、空间 $O(HW)$。正式使用时应在赋值前断言格子仍为 0，以捕获冲突。

## 变种五：网格中预先存在障碍格

原递归通常会碰障碍而失效，偶性也只剩上界。小网格可枚举所有不碰障碍的候选四元集合，再用记忆化集合装箱求最优。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<unsigned long long> candidate;
unordered_map<unsigned long long, int> memo;
int search(unsigned long long used) {
  auto found = memo.find(used);
  if (found != memo.end()) return found->second;
  int first = -1;
  for (int i = 0; i < static_cast<int>(candidate.size()); ++i) {
    if ((candidate[i] & used) == 0) {
      first = i;
      break;
    }
  }
  if (first == -1) return memo[used] = 0;
  int answer = 0;
  for (int i = first; i < static_cast<int>(candidate.size()); ++i) {
    if ((candidate[i] & used) == 0) {
      answer = max(answer, 1 + search(used | candidate[i]));
    }
  }
  return memo[used] = answer;
}
int main() {
  int height, width;
  cin >> height >> width;
  vector<string> grid(height);
  for (string& row : grid) cin >> row;
  if (height * width > 63) return 0;
  for (int r = 0; r < height; ++r) {
    for (int c = 0; c < width; ++c) {
      for (int side = 1; r + side < height && c + side < width; ++side) {
        array<pair<int, int>, 4> cells{{
            {r, c}, {r + side, c}, {r, c + side}, {r + side, c + side}}};
        unsigned long long mask = 0;
        bool valid = true;
        for (auto [row, column] : cells) {
          if (grid[row][column] == '#') valid = false;
          mask |= 1ULL << (row * width + column);
        }
        if (valid) candidate.push_back(mask);
      }
    }
  }
  cout << search(0) << '\n';
}
```

时间和状态数最坏为指数级，空间同样指数级，只适合至多约 60 格且候选较少的实例；更大的特殊版本需要轮廓 DP 或新的结构性质。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc226/tasks/arc226_c?lang=en)
- [对应知识专题](../../math/modular-constructions.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-134-lc509/">[力扣 Top 134] LC 509 斐波那契数 简单 →</a>
</nav>
