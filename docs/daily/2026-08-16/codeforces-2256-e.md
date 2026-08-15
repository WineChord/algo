---
title: "[codeforces] CF Round 1116 Div.1 C / Div.2 E Even If the World Turns"
---

# [codeforces] CF Round 1116 Div.1 C / Div.2 E Even If the World Turns

<p class="daily-archive-kicker">2026-08-16 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-16 题目列表</a> · <a href="../../../math/modular-constructions/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=856a8747e950a5d50b756776e7515cf0e4ca5be6309bc5d8624f01f6224ab198 -->
[Official problem: Codeforces 2256E - Even If the World Turns](https://codeforces.com/contest/2256/problem/E)

## 官方来源与元数据

- 比赛：Codeforces Round 1116。
- 官方别名：[Div.1 C（2255C）](https://codeforces.com/contest/2255/problem/C) / [Div.2 E（2256E）](https://codeforces.com/contest/2256/problem/E)。
- 官方英文标题：Even If the World Turns。
- Div.1 C 官方分值：1750；Div.2 E 官方分值：2750。
- 官方 rating：2100。
- Div.2 E 官方标签：`communication`、`greedy`、`interactive`、`math`、`number theory`。
- Div.1 C 在上述标签外另标注 `constructive algorithms`、`expression parsing`。
- 时间限制：2 秒；内存限制：256 MB。
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)。

两个页面来自同一 Round，题名、完整题面、输入输出、约束与样例一致，因而按同一道官方题
实体处理。题面没有理解所必需的独立图片。下方英文层是模型逐项阅读官方页面后独立组织的
完整语义呈现；样例数据逐字符保留，叙述与 Note 不冒充官方逐字原文。

## Complete English statement

This is a run-twice communication problem. The two players, Chtholly and Willem, may agree on a
strategy in advance, but they cannot communicate during a test. The jury first runs the program as
Chtholly and later runs it as Willem. Nothing persists between the runs except the modified picture,
and the test cases may be reordered.

For each test case, the jury prepares an $n\times n$ black-and-white picture and chooses a target cell
$x$. Rows and columns are numbered from 1 through $n$. If the picture contains $w$ black cells, the
guarantee is

$$
\gcd(n,w)=1.
$$

On the first run, Chtholly sees both the picture and $x$. She must choose two cells and swap their
colors. The two cells may be the same; swapping equal colors also leaves the picture unchanged. The
target cell itself does not move during this swap.

The jury then secretly applies any number of the following operations, in any order:

1. Choose $0\le d_r,d_c<n$ and cyclically shift every cell $(r,c)$ to
   $((r-1+d_r)\bmod n+1,(c-1+d_c)\bmod n+1)$.
2. Rotate clockwise by $90^\circ$, moving $(r,c)$ to $(c,n+1-r)$.
3. Reflect across the vertical axis, moving $(r,c)$ to $(r,n+1-c)$.
4. Invert every color.

The target undergoes every shift, rotation, and reflection, but color inversion does not move it.
On the second run, Willem sees only the final picture and must output the final target position.

The program is run exactly twice. The first input line is either `first` or `second` and determines the
contract below.

### First-run input and output

After `first`, read $t$. Each test case contains $n$, then $n$ strings of length $n$ using `#` for black
and `.` for white, then target coordinates $r_x,c_x$. Print four coordinates
$r_1,c_1,r_2,c_2$ for the cells to swap.

### Second-run input and output

After `second`, read the same number $t$ of transformed cases, possibly in another order. Each test
contains $n$ and the $n$ final picture rows. Print the recovered coordinates $r'_x,c'_x$.

### Constraints

- $1\le t\le10^4$.
- $2\le n\le800$.
- On the first run, $\gcd(n,w)=1$.
- The sum of $n^2$ over all test cases is at most $800^2$.
- Hacks are disabled.

### Complete official first-run sample

Input:

```text
first
2
5
#....
.#...
.....
.....
.....
3 4
5
.....
####.
.....
#####
.....
1 1
```

One valid output:

```text
1 1 4 1
1 1 1 1
```

### Complete official second-run sample

Input:

```text
second
2
5
.....
####.
.....
#####
.....
5
.....
.....
....#
..#..
.....
```

Output:

```text
1 1
1 4
```

### Complete official note semantics, independently restated

The first sample output is only one valid set of swaps. In its first case, swapping $(1,1)$ and
$(4,1)$ leaves black cells at $(2,2)$ and $(4,1)$. The jury shifts one row downward and two columns
right, rotates clockwise once, and reflects vertically. The target moves
$(3,4)\to(4,1)\to(1,2)\to(1,4)$, while the two black cells end at $(3,5)$ and $(4,3)$; Willem therefore
prints $(1,4)$. In the second case, Chtholly may choose one cell twice, and the jury may do nothing.

## 中文题意解释

第一次运行知道目标，却只能通过交换两个格子的颜色把目标“写进”图片；第二次运行既没有
原图，也不知道对方做过哪些平移、旋转、镜像与反色。我们要设计一个随这些几何变换一起
移动、却在全局反色下保持不变的图片特征。

把坐标改为 $\mathbb Z_n^2$ 中的 0 下标。若黑格集合为 $B$、数量为 $w$，定义模意义下的
黑格重心

$$
P(B)=w^{-1}\sum_{p\in B}p\pmod n.
$$

$\gcd(n,w)=1$ 保证逆元存在。第一次把这个重心调到目标；第二次从最终图重算重心即可。

## 约束推导与暴力 oracle

图片最多有 64 万格，允许线性扫描，但不能枚举两格形成的 $O(n^4)$ 个交换，更不能枚举所有
秘密变换。下面的小规模 oracle 枚举黑格集合和目标，检查编码交换后重心恰等于目标；正式
算法的随机验证还会枚举几何变换与反色。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int inverseModulo(int value, int mod) {
  for (int candidate = 1; candidate < mod; ++candidate) {
    if (value * candidate % mod == 1) return candidate;
  }
  return -1;
}
int main() {
  for (int n = 2; n <= 4; ++n) {
    int cells = n * n;
    for (int mask = 1; mask + 1 < (1 << cells); ++mask) {
      int weight = __builtin_popcount(static_cast<unsigned>(mask));
      if (gcd(n, weight) != 1) continue;
      int sumRow = 0;
      int sumColumn = 0;
      for (int id = 0; id < cells; ++id) {
        if (mask >> id & 1) {
          sumRow = (sumRow + id / n) % n;
          sumColumn = (sumColumn + id % n) % n;
        }
      }
      for (int target = 0; target < cells; ++target) {
        int deltaRow = (weight * (target / n) - sumRow) % n;
        int deltaColumn = (weight * (target % n) - sumColumn) % n;
        if (deltaRow < 0) deltaRow += n;
        if (deltaColumn < 0) deltaColumn += n;
        int changed = mask;
        if (deltaRow != 0 || deltaColumn != 0) {
          bool found = false;
          for (int id = 0; id < cells && !found; ++id) {
            if (!(mask >> id & 1)) continue;
            int nextRow = (id / n + deltaRow) % n;
            int nextColumn = (id % n + deltaColumn) % n;
            int next = nextRow * n + nextColumn;
            if (!(mask >> next & 1)) {
              changed ^= 1 << id;
              changed ^= 1 << next;
              found = true;
            }
          }
          if (!found) return 1;
        }
        int rowMoment = 0;
        int columnMoment = 0;
        for (int id = 0; id < cells; ++id) {
          if (changed >> id & 1) {
            rowMoment = (rowMoment + id / n) % n;
            columnMoment = (columnMoment + id % n) % n;
          }
        }
        int inverse = inverseModulo(weight % n, n);
        if (rowMoment * inverse % n != target / n) return 1;
        if (columnMoment * inverse % n != target % n) return 1;
      }
    }
  }
  cout << "verified\n";
}
```

穷举集合是 $O(2^{n^2}n^4)$ 量级，只能用于 $n\le4$。它验证了交换的存在性和代数目标，
但正式算法必须把找交换降到一次扫描。

## 解法递进：从目标重心到一对可交换格

设当前坐标和为 $S=\sum_{p\in B}p$，目标为 $x$。若把黑格 $a$ 与白格 $b$ 交换，新和为
$S-a+b$。需要

$$
S-a+b\equiv wx\pmod n,
$$

所以令

$$
\Delta=wx-S,\qquad b=a+\Delta.
$$

当 $\Delta=0$ 时交换同一格即可。否则只需扫描一个满足 $a\in B$ 且
$a+\Delta\notin B$ 的黑格。

这样的格必然存在。反设每个黑格平移 $\Delta$ 后仍是黑格，则 $B$ 是非零平移作用下若干
完整轨道的并。每条轨道长度 $q>1$ 且 $q\mid n$，于是 $q\mid w$，与
$\gcd(n,w)=1$ 矛盾。

## 变换不变量

任意允许的几何变换都可写成

$$
p\mapsto Mp+t,
$$

其中 $M$ 是由换轴和取负构成的可逆矩阵。它把重心变为

$$
P(MB+t)=MP(B)+t,
$$

恰与目标坐标以同样方式移动。

反色后黑格集合变为补集，数量 $w'=n^2-w\equiv-w\pmod n$。全网格每一维坐标和都是
$n(0+1+\cdots+n-1)\equiv0\pmod n$，故补集坐标和是 $-S$，于是

$$
P(\overline B)=(-w)^{-1}(-S)=w^{-1}S=P(B).
$$

所以反色不会改变解码坐标。

## 最佳实用解：模重心编码

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long extendedGcd(long long a, long long b, long long& x, long long& y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }
  long long nextX, nextY;
  long long divisor = extendedGcd(b, a % b, nextX, nextY);
  x = nextY;
  y = nextX - a / b * nextY;
  return divisor;
}
int normalize(long long value, int mod) {
  value %= mod;
  if (value < 0) value += mod;
  return static_cast<int>(value);
}
int inverseModulo(int value, int mod) {
  long long x, y;
  extendedGcd(value, mod, x, y);
  return normalize(x, mod);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string mode;
  cin >> mode;
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    vector<string> picture(n);
    for (string& row : picture) cin >> row;
    int blackCount = 0;
    int sumRow = 0;
    int sumColumn = 0;
    for (int row = 0; row < n; ++row) {
      for (int column = 0; column < n; ++column) {
        if (picture[row][column] == '#') {
          ++blackCount;
          sumRow = (sumRow + row) % n;
          sumColumn = (sumColumn + column) % n;
        }
      }
    }
    if (mode == "first") {
      int targetRow, targetColumn;
      cin >> targetRow >> targetColumn;
      --targetRow;
      --targetColumn;
      int deltaRow = normalize(1LL * blackCount * targetRow - sumRow, n);
      int deltaColumn = normalize(1LL * blackCount * targetColumn - sumColumn, n);
      if (deltaRow == 0 && deltaColumn == 0) {
        cout << "1 1 1 1\n";
        continue;
      }
      bool found = false;
      for (int row = 0; row < n && !found; ++row) {
        for (int column = 0; column < n && !found; ++column) {
          if (picture[row][column] != '#') continue;
          int nextRow = (row + deltaRow) % n;
          int nextColumn = (column + deltaColumn) % n;
          if (picture[nextRow][nextColumn] == '.') {
            cout << row + 1 << ' ' << column + 1 << ' ';
            cout << nextRow + 1 << ' ' << nextColumn + 1 << '\n';
            found = true;
          }
        }
      }
    } else {
      int inverse = inverseModulo(blackCount % n, n);
      int targetRow = normalize(1LL * sumRow * inverse, n);
      int targetColumn = normalize(1LL * sumColumn * inverse, n);
      cout << targetRow + 1 << ' ' << targetColumn + 1 << '\n';
    }
  }
}
```

每个测试只扫描常数遍图片，时间 $O(n^2)$、空间 $O(n^2)$；可把图片保留空间视为输入存储。
全批时间 $O(800^2)$。扩展欧几里得只在第二次运行每例执行一次，且逆元由题目保证存在。

## 正确性证明

**引理 1：第一次运行总能完成目标交换。**

若 $\Delta=0$，不改变图片即可使
$S=wx$。否则若没有黑格 $a$ 使 $a+\Delta$ 为白格，黑格集合便对非零平移 $\Delta$ 封闭；
其轨道长度 $q>1$ 同时整除 $n$ 与 $w$，违反互质条件。因此扫描必找到交换，交换后
$S'=S+\Delta=wx$，重心等于 $x$。

**引理 2：重心与所有几何变换等变。**

对 $p\mapsto Mp+t$，坐标和变为
$MS+wt$，乘以 $w^{-1}$ 后得到 $MP+t$，与目标的变换完全相同。

**引理 3：反色不改变重心。**

反色使数量和坐标和模 $n$ 同时取负，其商保持不变。

**定理：第二次运行输出最终目标。**

引理 1 让秘密变换前的重心等于目标；引理 2、3 保证
任意允许操作后，最终图片重心仍等于最终目标。第二次运行精确重算该重心，所以输出正确。

## 样例手推与边界

官方第一组初图有黑格 $(0,0),(1,1)$，故 $w=2$、坐标和 $(1,1)$，目标是 0 下标
$(2,3)$。在模 5 下

$$
\Delta=2(2,3)-(1,1)=(3,0).
$$

选择黑格 $(0,0)$，对应白格 $(3,0)$，正是样例交换 `(1,1)` 与 `(4,1)`。新坐标和
$(4,1)=2(2,3)$，重心已经等于目标。后续平移、旋转、镜像后，重心随目标到 `(1,4)`。

- 图片不能全黑或全白：此时 $w$ 分别为 $n^2$ 或 0，都不与 $n\ge2$ 互质。
- $\Delta=0$：必须输出合法的同一格两次，不能继续寻找黑白对。
- 反色后黑格数改变，但仍有 $n^2-w\equiv-w$，与 $n$ 互质。
- 第二次测试顺序可变：算法不存任何跨运行或跨测试状态，因此不受影响。
- 坐标必须先减 1 做模运算，最后再加 1 输出。

## 方案比较与易错点

枚举秘密变换无法解决通信问题；寻找几何中心或包围盒又会被环形平移、反色和对称图片破坏。
模重心只保留两个一阶矩，却正好具备“仿射等变 + 补集不变 + 一次交换可调”的三项结构，
证明短、实现线性，应优先记忆。

- 不可使用普通整数平均；需要的是模 $n$ 的乘法逆元。
- 交换改变量是 `white - black`，符号写反会编码到错误位置。
- 存在性证明依赖二维平移轨道长度整除 $n$，不是凭经验假设一定能找到。
- 旋转包含常量平移项，但仿射公式已经覆盖，不要只证明线性部分。
- 第二次运行可能看到补图，必须用它当前的黑格数求逆。

## 验证说明

最终程序以 GNU++23 编译，分别核对两份官方输入的解析契约；官方 `second` 样例来自官方
展示的另一组合法交换，不能直接拿来断言本策略的解码值。验证器把本程序对官方 `first`
输入实际输出的交换应用到图片，再送入同一程序的 `second` 模式，两个目标均正确恢复。
小规模 oracle 穷举 $n=2,3,4$ 的全部互质黑格集合和全部目标；随机对拍另对每个编码结果
组合平移、0 到 3 次旋转、可选镜像与可选反色，再由独立解码器核对最终目标，全部通过。

## 变种一：一维环上的目标编码

新定义把图片改为奇数长度 $n$ 的环，只允许循环平移与反色。奇数条件使全环位置和
$n(n-1)/2\equiv0\pmod n$，所以补集仍保持重心；一次交换只需寻找黑点 $a$ 与白点
$a+\Delta$。若 $n$ 为偶数，反色会额外平移重心，原证明失效。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int inverseModulo(int value, int mod) {
  for (int candidate = 1; candidate < mod; ++candidate) {
    if (value * candidate % mod == 1) return candidate;
  }
  return -1;
}
int main() {
  string mode, ring;
  int n;
  cin >> mode >> n >> ring;
  int count = 0;
  int sum = 0;
  for (int i = 0; i < n; ++i) {
    if (ring[i] == '#') {
      ++count;
      sum = (sum + i) % n;
    }
  }
  if (mode == "encode") {
    int target;
    cin >> target;
    --target;
    int delta = (1LL * count * target - sum) % n;
    if (delta < 0) delta += n;
    if (delta == 0) {
      cout << "1 1\n";
    } else {
      for (int i = 0; i < n; ++i) {
        int next = (i + delta) % n;
        if (ring[i] == '#' && ring[next] == '.') {
          cout << i + 1 << ' ' << next + 1 << '\n';
          break;
        }
      }
    }
  } else {
    cout << sum * inverseModulo(count % n, n) % n + 1 << '\n';
  }
}
```

时间 $O(n)$、空间 $O(n)$；条件是 $n$ 为奇数且 $\gcd(n,w)=1$。二维算法不是偶然技巧，而是一维
循环群重心编码的坐标乘积版本。

## 变种二：矩形环面与独立模数

新定义为 $h\times w$ 环面，只允许行列平移与水平/垂直镜像，不允许反色。若黑格数 $k$
同时与 $h,w$ 互质，就分别在模 $h$、模 $w$ 下编码两个坐标。矩形全网格的坐标和不总为
0，删去反色正是这一变种与原题的模型差异。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int inverseModulo(int value, int mod) {
  for (int candidate = 1; candidate < mod; ++candidate) {
    if (value * candidate % mod == 1) return candidate;
  }
  return -1;
}
int main() {
  string mode;
  int height, width;
  cin >> mode >> height >> width;
  vector<string> picture(height);
  for (string& row : picture) cin >> row;
  int count = 0;
  int sumRow = 0;
  int sumColumn = 0;
  for (int row = 0; row < height; ++row) {
    for (int column = 0; column < width; ++column) {
      if (picture[row][column] == '#') {
        ++count;
        sumRow = (sumRow + row) % height;
        sumColumn = (sumColumn + column) % width;
      }
    }
  }
  if (mode == "first") {
    int targetRow, targetColumn;
    cin >> targetRow >> targetColumn;
    --targetRow;
    --targetColumn;
    int deltaRow = (1LL * count * targetRow - sumRow) % height;
    int deltaColumn = (1LL * count * targetColumn - sumColumn) % width;
    if (deltaRow < 0) deltaRow += height;
    if (deltaColumn < 0) deltaColumn += width;
    if (deltaRow == 0 && deltaColumn == 0) {
      cout << "1 1 1 1\n";
      return 0;
    }
    for (int row = 0; row < height; ++row) {
      for (int column = 0; column < width; ++column) {
        int nextRow = (row + deltaRow) % height;
        int nextColumn = (column + deltaColumn) % width;
        if (picture[row][column] == '#' && picture[nextRow][nextColumn] == '.') {
          cout << row + 1 << ' ' << column + 1 << ' ';
          cout << nextRow + 1 << ' ' << nextColumn + 1 << '\n';
          return 0;
        }
      }
    }
  } else {
    int inverseRow = inverseModulo(count % height, height);
    int inverseColumn = inverseModulo(count % width, width);
    cout << sumRow * inverseRow % height + 1 << ' ';
    cout << sumColumn * inverseColumn % width + 1 << '\n';
  }
}
```

两次运行均为 $O(hw)$ 时间、$O(hw)$ 空间。平移轨道长度整除
$\operatorname{lcm}(h,w)$；$k$ 与两个模数分别互质便与该轨道长度互质。非正方形时不允许
90 度旋转，因为它会改变形状。

## 变种三：三维环面

新定义为 $n\times n\times n$ 二值体素，允许三维循环平移、坐标轴置换、取反与颜色反转。
三维坐标和乘 $w^{-1}$ 后仍是等变重心，一次交换沿三维 $\Delta$ 调整即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int inverseModulo(int value, int mod) {
  for (int candidate = 1; candidate < mod; ++candidate) {
    if (value * candidate % mod == 1) return candidate;
  }
  return -1;
}
int main() {
  string mode;
  int n;
  cin >> mode >> n;
  vector<vector<string>> cube(n, vector<string>(n));
  for (auto& layer : cube) {
    for (string& row : layer) cin >> row;
  }
  int count = 0;
  array<int, 3> sum{};
  for (int x = 0; x < n; ++x) {
    for (int y = 0; y < n; ++y) {
      for (int z = 0; z < n; ++z) {
        if (cube[x][y][z] == '#') {
          ++count;
          sum[0] = (sum[0] + x) % n;
          sum[1] = (sum[1] + y) % n;
          sum[2] = (sum[2] + z) % n;
        }
      }
    }
  }
  if (mode == "first") {
    array<int, 3> target{};
    cin >> target[0] >> target[1] >> target[2];
    for (int& coordinate : target) --coordinate;
    array<int, 3> delta{};
    for (int axis = 0; axis < 3; ++axis) {
      delta[axis] = (1LL * count * target[axis] - sum[axis]) % n;
      if (delta[axis] < 0) delta[axis] += n;
    }
    if (delta == array<int, 3>{0, 0, 0}) {
      cout << "1 1 1 1 1 1\n";
      return 0;
    }
    for (int x = 0; x < n; ++x) {
      for (int y = 0; y < n; ++y) {
        for (int z = 0; z < n; ++z) {
          int nextX = (x + delta[0]) % n;
          int nextY = (y + delta[1]) % n;
          int nextZ = (z + delta[2]) % n;
          if (cube[x][y][z] == '#' && cube[nextX][nextY][nextZ] == '.') {
            cout << x + 1 << ' ' << y + 1 << ' ' << z + 1 << ' ';
            cout << nextX + 1 << ' ' << nextY + 1 << ' ' << nextZ + 1 << '\n';
            return 0;
          }
        }
      }
    }
  } else {
    int inverse = inverseModulo(count % n, n);
    cout << sum[0] * inverse % n + 1 << ' ';
    cout << sum[1] * inverse % n + 1 << ' ';
    cout << sum[2] * inverse % n + 1 << '\n';
  }
}
```

两次运行的时间与存储均为 $O(n^3)$。三维全网格每一维坐标和包含 $n^2$ 份
$0+\cdots+(n-1)$，模 $n$ 恒为 0；存在性证明和补集证明按坐标逐维原样推广。

## 变种四：不再互质时列出全部候选重心

新定义不保证 $\gcd(n,w)=1$，只给最终图片，要求列出满足 $wx\equiv S\pmod n$ 的全部候选
坐标。设 $g=\gcd(n,w)$；一维同余有解当且仅当 $g\mid S$，有解时恰有 $g$ 个答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<string> picture(n);
  for (string& row : picture) cin >> row;
  int count = 0;
  int sumRow = 0;
  int sumColumn = 0;
  for (int row = 0; row < n; ++row) {
    for (int column = 0; column < n; ++column) {
      if (picture[row][column] == '#') {
        ++count;
        sumRow = (sumRow + row) % n;
        sumColumn = (sumColumn + column) % n;
      }
    }
  }
  vector<int> rows;
  vector<int> columns;
  for (int value = 0; value < n; ++value) {
    if (1LL * count * value % n == sumRow) rows.push_back(value);
    if (1LL * count * value % n == sumColumn) columns.push_back(value);
  }
  cout << 1LL * rows.size() * columns.size() << '\n';
  for (int row : rows) {
    for (int column : columns) cout << row + 1 << ' ' << column + 1 << '\n';
  }
}
```

时间 $O(n^2)$ 用于读图，额外枚举 $O(n)$；候选数可达 $g^2$。这说明互质条件不是实现细节，
而是让重心唯一可解的必要结构。

## 变种五：随机端到端协议验证器

新定义不求解 Judge 输入，而是对给定编码后图片与目标随机施加全部允许变换，再断言解码结果
同步变化。它适合作为通信题本地测试框架。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int inverseModulo(int value, int mod) {
  for (int candidate = 1; candidate < mod; ++candidate) {
    if (value * candidate % mod == 1) return candidate;
  }
  return -1;
}
pair<int, int> decode(const vector<string>& picture) {
  int n = static_cast<int>(picture.size());
  int count = 0;
  int sumRow = 0;
  int sumColumn = 0;
  for (int row = 0; row < n; ++row) {
    for (int column = 0; column < n; ++column) {
      if (picture[row][column] == '#') {
        ++count;
        sumRow = (sumRow + row) % n;
        sumColumn = (sumColumn + column) % n;
      }
    }
  }
  int inverse = inverseModulo(count % n, n);
  return {sumRow * inverse % n, sumColumn * inverse % n};
}
int main() {
  mt19937 random(20260816);
  int n;
  cin >> n;
  vector<string> picture(n);
  for (string& row : picture) cin >> row;
  auto target = decode(picture);
  for (int step = 0; step < 10000; ++step) {
    int operation = random() % 4;
    vector<string> next(n, string(n, '.'));
    if (operation == 0) {
      int dr = random() % n;
      int dc = random() % n;
      for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
          next[(row + dr) % n][(column + dc) % n] = picture[row][column];
        }
      }
      target = {(target.first + dr) % n, (target.second + dc) % n};
    } else if (operation == 1) {
      for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
          next[column][n - 1 - row] = picture[row][column];
        }
      }
      target = {target.second, n - 1 - target.first};
    } else if (operation == 2) {
      for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
          next[row][n - 1 - column] = picture[row][column];
        }
      }
      target.second = n - 1 - target.second;
    } else {
      next = picture;
      for (string& row : next) {
        for (char& cell : row) cell = cell == '#' ? '.' : '#';
      }
    }
    picture.swap(next);
    if (decode(picture) != target) return 1;
  }
  cout << "verified\n";
}
```

每次变换与解码都是 $O(n^2)$，10000 轮总计 $O(10000n^2)$，空间 $O(n^2)$。它直接覆盖
平移、旋转、镜像、反色及长组合，而不是只测试某个静态公式。

## 来源

- [Codeforces Div.2 官方题面](https://codeforces.com/contest/2256/problem/E)
- [Codeforces Div.1 官方题面](https://codeforces.com/contest/2255/problem/C)
- [Codeforces 官方 API](https://codeforces.com/apiHelp)
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2256/problem/E)
- [对应知识专题](../../math/modular-constructions.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-514-q3-lc4016/">← [力扣竞赛] 第 514 场周赛 Q3 LC 4016 两个不重叠子正方形的最大面积 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-16-lc2029/">[力扣每日一题] 2026-08-16｜LC 2029 石子游戏 IX →</a>
</nav>
