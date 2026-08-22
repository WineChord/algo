---
title: "[codeforces] CF Round 1117 Div.2 F1 Beaver's Jumping Track (Easy Version)"
---

# [codeforces] CF Round 1117 Div.2 F1 Beaver's Jumping Track (Easy Version)

<p class="daily-archive-kicker">2026-08-23 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-23 题目列表</a> · <a href="../../../data-structures/min-plus-segment-tree/#problem-codeforces-2257-f1">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=88ac3da99ddf05cb70491a573102818a4e2bc128289e1d4c23739dbb4a22a850 -->
[Official problem: Codeforces 2257F1 — Beaver's Jumping Track (Easy Version)](https://codeforces.com/contest/2257/problem/F1)

## 官方来源与元数据

- 比赛：Codeforces Round 1117 (Div. 2)；Contest ID 2257。
- 题目：Div.2 F1 — Beaver's Jumping Track (Easy Version)。
- 官方 points：2750；截至 2026-08-23，官方 rating 未提供，官方标签为 data structures、dp、
  matrices。
- 时间限制：2 秒；内存限制：1024 MB。
- 题面没有理解所必需的图片。
- 下方英文层是模型逐项核对官方页面后独立组织的自包含忠实呈现；官方来源依
  [Codeforces Problems’ Materials Publishing License v0.1](https://codeforces.com/blog/entry/967)
  呈现；未包含隐藏测试、生成器、校验器或独立图片资产。

## Complete English statement

The Beaver is training for long-distance jumps. Since always jumping as far as possible would be easy
and uninteresting, it built a special training track. It can determine an optimal route without
computational limitations and always minimizes the total penalty, even as platform lengths and
penalties change over time.

This is the easy version of the problem: here $1\le x\le5$ and the time limit is 2 seconds. In the
hard version, $1\le x\le10$ and the time limit is 3 seconds; all other limits, operations, and sample
data are the same. Codeforces allows hacks only after both versions have been solved.

A beaver moves only forward along a track. In one jump, it can move by any integer distance from
$1$ through $x$ cells, inclusive.

The track consists of $n$ consecutive platforms. Platform $i$ contains $d_i$ cells. If both the
starting cell and the landing cell of a jump belong to platform $i$, that jump incurs a penalty of
$s_i$. A jump whose endpoints belong to different platforms incurs no penalty. A jump may pass over
one or more whole platforms.

The track changes over time. Process three types of operations:

- `1 i v`: set the length of platform $i$ to $v$, that is, assign $d_i=v$;
- `2 i y`: set the penalty of platform $i$ to $y$, that is, assign $s_i=y$;
- `? l r`: starting from the first cell of platform $l$, find the minimum total penalty needed to
  reach the last cell of platform $r$.

All jumps must move forward and have an integer length between $1$ and $x$.

### Input

The first line contains three integers $n$, $q$, and $x$: the number of platforms, the number of
operations, and the maximum jump length.

The second line contains $n$ integers $d_1,d_2,\ldots,d_n$, the platform lengths.

The third line contains $n$ integers $s_1,s_2,\ldots,s_n$, the within-platform penalties.

Each of the next $q$ lines is one operation in one of the three formats shown above.

### Output

For every operation of type `?`, print one integer: the minimum possible total penalty for that
query.

### Constraints

- $1\le n\le10^6$.
- $1\le q\le10^4$.
- $1\le x\le5$.
- $1\le d_i\le10^7$.
- $1\le s_i\le10^5$.
- In type 1, $1\le i\le n$ and $1\le v\le10^7$.
- In type 2, $1\le i\le n$ and $1\le y\le10^5$.
- In type `?`, $1\le l\le r\le n$.
- Every input value is an integer.

### Official sample

Sample input:

```text
5 8 3
4 2 5 1 3
4 2 7 1 5
? 1 3
2 2 10
? 1 3
1 1 2
? 1 3
? 2 5
1 3 2
? 2 5
```

Sample output:

```text
11
11
7
7
0
```

In the official sample note, for the first query, one optimal sequence of global cell positions is
$1\rightarrow4\rightarrow6\rightarrow8\rightarrow11$. The first jump stays on platform 1 and
costs 4; the two cross-platform jumps cost 0; the last jump stays on platform 3 and costs 7, for a
total of 11. Raising $s_2$ does not change this route. For the third query, one optimal route is
$1\rightarrow4\rightarrow6\rightarrow9$; only the jump $6\rightarrow9$ has both endpoints on one
platform, so its total penalty is 7.

As an additional check of the remaining sample operations, after the final length update the last
query can be completed with penalty 0.

Source: [Codeforces problem 2257F1](https://codeforces.com/contest/2257/problem/F1), published under
the [Codeforces materials license](https://codeforces.com/blog/entry/967).

## 中文解释与最优结论

把全局最短代价 DP 写到每个格子：到达一个格子的最优值只依赖它前面至多 $x$ 个格子。
因此，一个平台不需要知道更早历史，只需把“平台前的最后 $x$ 个 DP 值”变换为“平台后的
最后 $x$ 个 DP 值”。这个变换是一个 $x\times x$ 的 min-plus 矩阵。

平台更新就是替换一个矩阵，区间询问就是按从左到右的顺序复合一段矩阵。用线段树维护矩阵
乘积后，建树 $O(nx^3)$，单次更新与询问 $O(x^3\log n)$，内存 $O(nx^2)$。由于 $x\le5$，
矩阵维数是常数。

## 约束推导、溢出与边界

- $n$ 可达 $10^6$，每次从头扫描平台不可行；$q$ 只有 $10^4$，适合线段树点更新与区间复合。
- $d_i$ 可达 $10^7$，不能展开平台格子；必须直接算出一个平台的转移。
- $x\le5$ 是核心小参数，使 $x^2$ 状态和 $x^3$ 复合可行。
- 代价可能接近 $10^{18}$：总长度可达 $10^{13}$，每次同平台跳跃罚值可达 $10^5$。必须用
  `long long`，并在无穷大参与加法前跳过，避免溢出。
- 平台长度可能小于 $x$。此时“平台后的最后 $x$ 个格子”中有一部分仍位于平台之前，转移矩阵
  必须原样传递这些输入状态，不能把它们当作当前平台格子。
- $l=r$ 时无需区间矩阵，只计算从该平台首格到末格的同平台跳跃数。
- 跳跃可以越过整个短平台，所以不能强迫每个平台至少落地一次。

## 官方样例手推

样例第一问中 $x=3$。从平台 1 首格出发，先在同平台跳 3 格，付 $s_1=4$；再跨平台落到
平台 2，跨边界免费；下一跳跨到平台 3 仍免费；最后在平台 3 内跳到终点，付 $s_3=7$，总计
11。第二次操作只改平台 2 的罚值，而这条最优路线没有在平台 2 内起落，所以答案不变。

## 解法一：展开查询区间做格子 DP

在小数据中，把 $l$ 到 $r$ 的每个格子展开。令 `dp[p]` 为到达第 `p` 个展开格子的最小罚值，
枚举前面 1 到 $x$ 个格子作为上一落点；两格属于同一平台时加对应 $s_i$，否则加 0。它枚举
了最后一次跳跃的全部合法来源，因此覆盖所有路径。一次询问时间
$O(x\sum_{i=l}^{r}d_i)$，空间 $O(\sum d_i)$，只适合作为小规模 oracle。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  int x;
  cin >> n >> q >> x;
  vector<int> length(n);
  vector<int64> penalty(n);
  for (int& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  while (q--) {
    char type;
    cin >> type;
    if (type == '1') {
      int index;
      int value;
      cin >> index >> value;
      length[index - 1] = value;
    } else if (type == '2') {
      int index;
      int64 value;
      cin >> index >> value;
      penalty[index - 1] = value;
    } else {
      int left;
      int right;
      cin >> left >> right;
      --left;
      --right;
      vector<int> platform;
      for (int i = left; i <= right; ++i) {
        platform.insert(platform.end(), length[i], i);
      }
      constexpr int64 INF = 4000000000000000000LL;
      vector<int64> dp(platform.size(), INF);
      dp[0] = 0;
      for (int position = 1; position < static_cast<int>(platform.size()); ++position) {
        for (int jump = 1; jump <= x && jump <= position; ++jump) {
          int previous = position - jump;
          int64 cost = platform[previous] == platform[position]
              ? penalty[platform[position]] : 0;
          dp[position] = min(dp[position], dp[previous] + cost);
        }
      }
      cout << dp.back() << '\n';
    }
  }
  return 0;
}
```

## 从格子 DP 到平台边界状态

一个格子的转移只看前 $x$ 格，所以切开平台边界后，更早的 DP 值不会再被使用。把平台起点
前的相对位置编号为 $-x+1,-x+2,\ldots,0$，把平台末端的最后 $x$ 个相对位置编号为
$d-x+1,\ldots,d$。输入向量不是任意起点代价，而是已经对左侧前缀完成递推、满足 DP 闭包的
最后 $x$ 个值；输出向量也保持同一不变量。

固定输入位置 $p\le0$ 与正的输出位置 $t\ge1$。第一次从平台外跳入平台免费，并应落在
$\min(t,p+x)$；只有 $t>p+x$ 时才尽量前跳 $x$ 格。之后仍需在平台内完成的每一跳都付 $s$。
最少付费跳跃数为

$$
\max\left(0,\left\lceil\frac{t-p-x}{x}\right\rceil\right).
$$

若输出位置 $t\le0$，它其实还是输入窗口中的旧格子。其 DP 值已经吸收了更早格子的所有跳转，
当前平台不能回头改写它；因此只从同坐标输入复制代价 0，其余设为无穷大。这里表达的是闭合
DP 向量的传递，并不是宣称旧格之间不存在物理跳跃。这样才能正确处理 $d<x$ 的短平台。

## 最佳实用解：min-plus 矩阵线段树

设平台矩阵 $M_i$ 是一个作用在“已闭合边界 DP 向量”上的转移：对正的输出坐标，元素记录经
输入边界进入当前平台的最小新增罚值；对仍位于旧窗口的输出坐标，元素只负责同坐标复制。
连续两个平台的复合满足

$$
(A\otimes B)[i][j]=\min_k\{A[i][k]+B[k][j]\},
$$

这就是 min-plus 矩阵乘法。它满足结合律但不满足交换律，因此线段树查询必须保持从左到右的
顺序。

查询从平台 $l$ 的第一格开始。直接构造处理完平台 $l$ 后的边界向量：对输出相对位置
$t\ge1$，同平台付费跳跃数为 $\lceil(t-1)/x\rceil$；$t<1$ 不可达。随后乘上
$l+1$ 到 $r$ 的矩阵乘积，最终向量的最后一项对应平台 $r$ 的最后一格。

### 正确性证明

**引理一**：对任意已经完成左侧前缀递推的边界向量 $v$，$v\otimes M_i$ 精确给出处理平台
$i$ 后的新边界 DP 向量。

任一输出位置 $t\le0$ 尚未进入当前平台，其最优值已经包含在输入向量同坐标分量中，直接复制
即可。对 $t>0$，任一到达路径最后一次从输入窗口进入平台时使用某个 $p\le0$：这次跨边界
跳跃免费，此后所有端点都在平台内，每跳付 $s_i$。首次落在 $\min(t,p+x)$ 不会增加付费
次数；若 $t>p+x$，把落点前推到 $p+x$ 最优。剩余距离每次最多前进 $x$，故闭式给出可达
下界；按最大步长跳跃能达到该下界。
对全部输入分量取 min-plus 最小值，恰好覆盖最后一次入边界的所有选择，所以新向量正确。

**引理二**：min-plus 乘积精确表示相邻平台的串联。

任何穿过两个区间的路径在公共边界窗口有某个中间状态 $k$，代价是左右两段代价之和；对所有
$k$ 取最小即覆盖全部路径。反之，每个有限的左右状态组合都能拼成一条合法路径。

查询起始向量枚举了从平台 $l$ 首格到其每个末端边界状态的最少同平台跳跃。根据引理二，按序
乘上后续平台矩阵后，向量包含到达平台 $r$ 末端各状态的全局最优代价；最后一项就是指定终点。
线段树只利用结合律重加括号，不改变矩阵次序，因此返回值正确。点更新重建对应叶子和祖先，
故更新后仍保持同一不变量。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int MAX_X = 5;
constexpr int64 INF = 4000000000000000000LL;
int jumpLimit;
struct Matrix {
  array<int64, MAX_X * MAX_X> value;
  Matrix() {
    value.fill(INF);
  }
  int64& at(int row, int column) {
    return value[row * MAX_X + column];
  }
  int64 at(int row, int column) const {
    return value[row * MAX_X + column];
  }
};
Matrix identityMatrix() {
  Matrix answer;
  for (int i = 0; i < jumpLimit; ++i) answer.at(i, i) = 0;
  return answer;
}
Matrix multiply(const Matrix& left, const Matrix& right) {
  Matrix answer;
  for (int i = 0; i < jumpLimit; ++i) {
    for (int k = 0; k < jumpLimit; ++k) {
      int64 first = left.at(i, k);
      if (first == INF) continue;
      for (int j = 0; j < jumpLimit; ++j) {
        int64 second = right.at(k, j);
        if (second == INF) continue;
        answer.at(i, j) = min(answer.at(i, j), first + second);
      }
    }
  }
  return answer;
}
Matrix platformMatrix(int length, int64 penalty) {
  Matrix answer;
  for (int input = 0; input < jumpLimit; ++input) {
    int start = input - jumpLimit + 1;
    for (int output = 0; output < jumpLimit; ++output) {
      int target = length - jumpLimit + 1 + output;
      if (target <= 0) {
        if (target == start) answer.at(input, output) = 0;
      } else {
        int remaining = target - start - jumpLimit;
        int paidJumps = remaining <= 0 ? 0 : (remaining + jumpLimit - 1) / jumpLimit;
        answer.at(input, output) = 1LL * paidJumps * penalty;
      }
    }
  }
  return answer;
}
class SegmentTree {
public:
  SegmentTree(const vector<int>& length, const vector<int64>& penalty) {
    size = 1;
    while (size < static_cast<int>(length.size())) size *= 2;
    tree.assign(size * 2, identityMatrix());
    for (int i = 0; i < static_cast<int>(length.size()); ++i) {
      tree[size + i] = platformMatrix(length[i], penalty[i]);
    }
    for (int node = size - 1; node > 0; --node) {
      tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
    }
  }
  void update(int index, int length, int64 penalty) {
    int node = size + index;
    tree[node] = platformMatrix(length, penalty);
    for (node /= 2; node > 0; node /= 2) {
      tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
    }
  }
  Matrix query(int left, int right) const {
    Matrix leftProduct = identityMatrix();
    Matrix rightProduct = identityMatrix();
    for (left += size, right += size; left < right; left /= 2, right /= 2) {
      if (left % 2 == 1) leftProduct = multiply(leftProduct, tree[left++]);
      if (right % 2 == 1) rightProduct = multiply(tree[--right], rightProduct);
    }
    return multiply(leftProduct, rightProduct);
  }
private:
  int size;
  vector<Matrix> tree;
};
int64 answerQuery(
    int left, int right, const vector<int>& length, const vector<int64>& penalty,
    const SegmentTree& tree) {
  array<int64, MAX_X> state;
  state.fill(INF);
  for (int output = 0; output < jumpLimit; ++output) {
    int target = length[left] - jumpLimit + 1 + output;
    if (target < 1) continue;
    int paidJumps = (target - 1 + jumpLimit - 1) / jumpLimit;
    state[output] = 1LL * paidJumps * penalty[left];
  }
  Matrix product = tree.query(left + 1, right + 1);
  array<int64, MAX_X> result;
  result.fill(INF);
  for (int input = 0; input < jumpLimit; ++input) {
    if (state[input] == INF) continue;
    for (int output = 0; output < jumpLimit; ++output) {
      if (product.at(input, output) == INF) continue;
      result[output] = min(result[output], state[input] + product.at(input, output));
    }
  }
  return result[jumpLimit - 1];
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  cin >> n >> q >> jumpLimit;
  vector<int> length(n);
  vector<int64> penalty(n);
  for (int& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  SegmentTree tree(length, penalty);
  while (q--) {
    char type;
    cin >> type;
    if (type == '1') {
      int index;
      int value;
      cin >> index >> value;
      --index;
      length[index] = value;
      tree.update(index, length[index], penalty[index]);
    } else if (type == '2') {
      int index;
      int64 value;
      cin >> index >> value;
      --index;
      penalty[index] = value;
      tree.update(index, length[index], penalty[index]);
    } else {
      int left;
      int right;
      cin >> left >> right;
      cout << answerQuery(left - 1, right - 1, length, penalty, tree) << '\n';
    }
  }
  return 0;
}
```

建树时间 $O(nx^3)$；每次更新或询问时间 $O(x^3\log n)$；线段树空间 $O(nx^2)$。固定
25 个 `long long` 的矩阵在最大 $n$ 下约占 400 MiB 量级，处于 1024 MB 限制内。

## 同阶方案比较与易错点

可以用递归线段树或迭代线段树；二者复杂度相同。迭代版本避免百万叶子下的大量递归调用，
并能显式维护左积与右积的次序，实战更稳。矩阵不能交换，不能把普通稀疏表的重叠区间技巧
直接套过来。

- 把跨平台跳跃也加罚值；只有起点与终点在同一平台才罚。
- 强制在每个平台落地，会漏掉一次跳过短平台的合法路径。
- 平台长度小于 $x$ 时忘记传递仍在左边界窗口内的旧状态。
- 线段树右侧累积写成 `rightProduct * node` 的反序，破坏非交换乘积。
- 查询起点是平台 $l$ 的第一格，不是平台前的虚拟边界；必须单独构造起始向量。
- 使用 `int` 保存总罚值，或直接计算 `INF + value` 导致溢出。

## 可复现验证

两份原题程序均以 Apple Clang 的 C++23 模式编译。最优程序通过官方样例，逐项得到
`11, 11, 7, 7, 0`；还覆盖 $n=1$、$x=1$、$d_i<x$、一步跨过整个平台、连续更新同一平台
等边界。随机生成 12,000 组 $n\le7,d_i\le8,x\le5$ 的平台与更新/询问序列，以展开格子 DP
为 oracle，所有查询结果完全一致。

## Follow-up 与约束变种

### 变种一：最大跳长固定为 1

新定义：$x$ 固定为 1，因此输入首行改为 `n q`，不再读入 `x`；其余仍支持两种点更新和
区间询问。跨平台的唯一一步免费；平台 $i$ 内必须走
$d_i-1$ 步，贡献 $(d_i-1)s_i$。用树状数组维护每个平台贡献，更新和区间查询均为
$O(\log n)$，空间 $O(n)$，不再需要矩阵。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
class Fenwick {
public:
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index, int64 delta) {
    for (; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  int64 sum(int index) const {
    int64 answer = 0;
    for (; index > 0; index -= index & -index) answer += tree[index];
    return answer;
  }
private:
  vector<int64> tree;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  cin >> n >> q;
  vector<int64> length(n);
  vector<int64> penalty(n);
  for (int64& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  auto contribution = [&](int index) {
    return (length[index] - 1) * penalty[index];
  };
  Fenwick fenwick(n);
  for (int i = 0; i < n; ++i) fenwick.add(i + 1, contribution(i));
  while (q--) {
    char type;
    cin >> type;
    if (type == '?') {
      int left;
      int right;
      cin >> left >> right;
      cout << fenwick.sum(right) - fenwick.sum(left - 1) << '\n';
    } else {
      int index;
      int64 value;
      cin >> index >> value;
      --index;
      int64 old = contribution(index);
      if (type == '1') {
        length[index] = value;
      } else {
        penalty[index] = value;
      }
      fenwick.add(index + 1, contribution(index) - old);
    }
  }
  return 0;
}
```

### 变种二：查询可从任意格出发并在任意格结束

新定义：平台静态，总格子数为 $D\le2\times10^5$；输入首行仍为 `n q x`，每次询问只给两个
全局格子编号，并保证 $1\le start\le finish\le D$。原题固定“首格到末格”的起始向量不再
适用。对询问区间直接做前向 DP，第一格代价为 0，每格枚举前 $x$ 格。单次时间
$O(x(finish-start+1))$，额外 DP 空间为 $O(finish-start+1)$；加上展开并保存整条赛道所需
$O(D)$，程序总空间为 $O(D)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  int x;
  cin >> n >> q >> x;
  vector<int> length(n);
  vector<int64> penalty(n);
  for (int& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  vector<int> platform;
  for (int i = 0; i < n; ++i) platform.insert(platform.end(), length[i], i);
  constexpr int64 INF = 4000000000000000000LL;
  while (q--) {
    int start;
    int finish;
    cin >> start >> finish;
    --start;
    --finish;
    vector<int64> dp(finish - start + 1, INF);
    dp[0] = 0;
    for (int position = start + 1; position <= finish; ++position) {
      for (int jump = 1; jump <= x && position - jump >= start; ++jump) {
        int previous = position - jump;
        int64 cost = platform[previous] == platform[position]
            ? penalty[platform[position]] : 0;
        dp[position - start] = min(dp[position - start], dp[previous - start] + cost);
      }
    }
    cout << dp.back() << '\n';
  }
  return 0;
}
```

### 变种三：统计最优跳跃序列数量

新定义：平台静态、总格子数至多 $2\times10^5$，只询问从整条赛道第一格到最后一格；除最小
罚值外，还要统计达到最小值的跳跃序列数，模 $10^9+7$。输入首行为 `n x`，不再包含更新和
查询。min-plus 矩阵元素需扩展为“代价 + 方案数”半环；在这一规模下更直接的是格子 DP：
更小代价覆盖，等价代价累加。时间 $O(xD)$，空间 $O(D)$，其中 $D$ 是总格子数。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int MOD = 1000000007;
constexpr int64 INF = 4000000000000000000LL;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int x;
  cin >> n >> x;
  vector<int> length(n);
  vector<int64> penalty(n);
  for (int& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  vector<int> platform;
  for (int i = 0; i < n; ++i) platform.insert(platform.end(), length[i], i);
  vector<int64> best(platform.size(), INF);
  vector<int> ways(platform.size());
  best[0] = 0;
  ways[0] = 1;
  for (int position = 1; position < static_cast<int>(platform.size()); ++position) {
    for (int jump = 1; jump <= x && jump <= position; ++jump) {
      int previous = position - jump;
      int64 cost = platform[previous] == platform[position]
          ? penalty[platform[position]] : 0;
      int64 candidate = best[previous] + cost;
      if (candidate < best[position]) {
        best[position] = candidate;
        ways[position] = ways[previous];
      } else if (candidate == best[position]) {
        ways[position] += ways[previous];
        if (ways[position] >= MOD) ways[position] -= MOD;
      }
    }
  }
  cout << best.back() << ' ' << ways.back() << '\n';
  return 0;
}
```

### 变种四：允许向前或向后跳

新定义：平台静态、总格子数 $D\le2\times10^5$，仅有一组满足
$1\le start,finish\le D$ 的起终点；每跳可向任一方向移动 1 到 $x$ 格，同平台罚值规则不变。
输入先给 `n x`、两组平台数组，再给 `start finish`，不支持更新或多次询问。原来的前向 DAG
与边界矩阵失效，因为出现环。所有边权非负，可以把每个格子视为顶点，连接距离不超过 $x$
的格子并运行 Dijkstra。时间 $O(Dx\log D)$，空间 $O(D)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 INF = 4000000000000000000LL;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int x;
  cin >> n >> x;
  vector<int> length(n);
  vector<int64> penalty(n);
  for (int& value : length) cin >> value;
  for (int64& value : penalty) cin >> value;
  vector<int> platform;
  for (int i = 0; i < n; ++i) platform.insert(platform.end(), length[i], i);
  int start;
  int finish;
  cin >> start >> finish;
  --start;
  --finish;
  vector<int64> distance(platform.size(), INF);
  priority_queue<pair<int64, int>, vector<pair<int64, int>>, greater<>> queue;
  distance[start] = 0;
  queue.push({0, start});
  while (!queue.empty()) {
    auto [currentDistance, position] = queue.top();
    queue.pop();
    if (currentDistance != distance[position]) continue;
    for (int delta = -x; delta <= x; ++delta) {
      if (delta == 0) continue;
      int next = position + delta;
      if (next < 0 || next >= static_cast<int>(platform.size())) continue;
      int64 cost = platform[position] == platform[next] ? penalty[platform[next]] : 0;
      if (distance[next] > currentDistance + cost) {
        distance[next] = currentDistance + cost;
        queue.push({distance[next], next});
      }
    }
  }
  cout << distance[finish] << '\n';
  return 0;
}
```

## 推荐记忆

这题的核心不是“线段树套 DP”，而是先找到可复合的边界：局部递推只依赖前 $x$ 格，就把
平台压成 $x\times x$ 的 min-plus 转移。随后点更新与有序区间复合才自然落到非交换线段树。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/F1)
- [对应知识专题](../../data-structures/min-plus-segment-tree.md#problem-codeforces-2257-f1)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-189-q2-lc4021/">← [力扣竞赛] 第 189 场双周赛 Q2 LC 4021 得到旋转回文字符串的最少操作次数 I 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-23-lc1927/">[力扣每日一题] 2026-08-23｜LC 1927 求和游戏 →</a>
</nav>
