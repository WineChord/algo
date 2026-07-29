---
title: "[codeforces] CF Round 1111 Div.2 D2 XOR Sorting (Hard Version)"
---

# [codeforces] CF Round 1111 Div.2 D2 XOR Sorting (Hard Version)

<p class="daily-archive-kicker">2026-07-30 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3661c68c2e9f012cc2a2e56fc423ad1d4ba1a7324318397cff5289d7263db7e7 -->
## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1111 (Div. 2)。
- 比赛 ID：2247。
- 题号与标题：Div.2 D2 - XOR Sorting (Hard Version)。
- 官方分值：1250 分。
- 官方 rating：未知；当前官方 API 对象没有 `rating` 字段。
- 官方标签：`bitmasks`、`data structures`、`greedy`。
- 时间限制：2 秒。
- 内存限制：256 MB。
- 官方题面：[CF 2247 D2](https://codeforces.com/contest/2247/problem/D2)。
- 材料许可：[Codeforces materials usage licence v0.1](https://codeforces.com/blog/entry/967)。

下方英文题面层按上述材料许可保留官方来源与直达链接，用于公开、非判题的教学阅读；不包含隐藏测试、生成器、校验器或许可未覆盖的独立资产。

## Complete English statement

- Contest: Codeforces Round 1111 (Div. 2)
- Contest ID: 2247
- Problem alias: Div.2 D2
- Official title: D2. XOR Sorting (Hard Version)
- Official points: 1250
- Official rating: unknown; the current official API object has no `rating` field
- Official tags: bitmasks, data structures, greedy
- Time limit: 2 seconds
- Memory limit: 256 megabytes
- Official problem: [CF 2247 D2](https://codeforces.com/contest/2247/problem/D2)

The following English task text is presented under the [Codeforces materials usage licence v0.1](https://codeforces.com/blog/entry/967), with attribution and a direct link to the current official statement. It is used here on a public, non-judge educational page. Hidden tests, generators, validators, and unrelated assets are not reproduced.

### Problem Statement

This is the hard version. Its only constraint difference from D1 is that here

$$
0\le q\le10^6.
$$

Zero-based indexing is used.

For an array $b$ of $m$ positive integers, define $f(b)$ as follows. For a non-negative integer $k$, call $b$ **$k$-sortable** if it can be sorted in non-decreasing order by applying this operation any number of times:

1. Choose indices $i,j$ satisfying $0\le i<j\le m-1$ and $i\oplus j\le k$.
   The XOR condition concerns the indices, not the values $b_i,b_j$.

2. Swap $b_i$ and $b_j$.

The value $f(b)$ is the smallest non-negative $k$ for which $b$ is $k$-sortable.

You are given an array $a$ of length $n$ and $q$ cumulative point updates. Each update

$$
i\ x
$$

assigns $a_i=x$. Every update affects all subsequent states.

For the initial array and after every update, output $f(a)$.

The symbol $\oplus$ denotes bitwise XOR.

### Input

The first line contains the number of test cases $t$.

For each test case:

```text
n q
a_0 a_1 ... a_(n-1)
i_1 x_1
...
i_q x_q
```

Each update line means `a_i = x`.

### Output

For each test case, output $q+1$ integers in chronological order: the answer for the initial array, then the answer after each update. Whitespace-separated output is accepted.

### Complete constraints

$$
1\le t\le10^4
$$

$$
1\le n\le10^6,\qquad0\le q\le10^6
$$

$$
1\le a_i\le10^9
$$

$$
0\le i_j<n,\qquad1\le x_j\le10^9
$$

Across all test cases:

$$
\sum n\le10^6,\qquad\sum q\le10^6.
$$

### Official sample

```text
Input
3
2 0
1 2
2 1
1000000000 999999999
1 1000000000
6 2
2 5 3 4 1 6
1 2
4 5

Output
0
1
0
4
4
0
```

### Sample explanation

- `[1,2]` is already sorted, so its answer is 0.
- `[10^9,10^9-1]` needs the swap of indices 0 and 1. Their XOR is 1, so the answer is 1.
- After setting `a_1=10^9`, the second array is constant and its answer becomes 0.
- For `[2,5,3,4,1,6]`, swaps using index pairs `(0,1)` and `(0,4)` suffice; their XOR values are 1 and 4, and no smaller $k$ is sufficient.
- After `a_1=2`, the value 1 at index 4 must still cross the same major index boundary, so the answer remains 4.
- After `a_4=5`, the array becomes `[2,2,3,4,5,6]`, so the answer becomes 0.

## 中文题意与元数据说明

允许交换的不是某一固定距离内的值，而是满足“两个 **下标** 的异或不超过 $k$”的任意位置。求能把数组排成非递减顺序所需的最小 $k$，并在最多 $10^6$ 次点赋值后持续输出答案。

官方 points 为 1250；这不是 rating。官方 API 当前没有提供本题 rating，因此保持未知，不按题号推断。官方页面标注题面近期修改过，本页按 2026-07-30 读取到的当前版本核对。

## 从逆序对到二进制块

若

$$
2^h\le k<2^{h+1},
$$

任何满足 $i\oplus j\le k$ 的边都不能改变第 $h+1$ 位及更高位。因此允许交换图的连通分量不能跨出长度 $2^{h+1}$ 的对齐区间。

反过来，同一对齐区间内可以逐位翻转低 $h+1$ 位；每次翻转的 XOR 是某个不超过 $2^h$ 的二次幂，因此区间内所有有效位置连通。最后一个不完整区间也是二进制立方体的前缀，逐个清除偏移量中的置位仍留在该前缀内。

所以答案只可能是 0 或二的幂。给定某一级块划分后，块内可任意排列；全局能排好当且仅当相邻块之间没有逆序。等价公式为

$$
f(a)=
\begin{cases}
0,&a\text{ 已经非递减},\\
\displaystyle
\max_{\substack{i<j\\a_i>a_j}}
2^{\lfloor\log_2(i\oplus j)\rfloor},&\text{否则}.
\end{cases}
$$

## 解法递进

### 解法一：枚举全部逆序对

直接用上式计算；可作小规模 oracle，时间 $O(n^2)$、空间 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int answer = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if (a[i] > a[j]) {
        int difference = i ^ j;
        answer = max(answer, 1 << (31 - __builtin_clz(difference)));
      }
    }
  }
  cout << answer << '\n';
}
```

这里不会对 0 调用 `__builtin_clz`，因为 $i<j$ 保证 $i\oplus j>0$。

### 最佳实用解：维护所有二进制块的线段树

把长度补到最小二次幂 $N$，补位放置严格大于所有合法值的 `INF`。每个线段树节点对应一个对齐二进制区间，维护：

- `mn`：区间最小值；
- `mx`：区间最大值；
- `need`：解决区间内所有逆序所需的最小答案。

当前节点长度为 $L$，左右孩子各长 $L/2$，合并式为

$$
mn=\min(mn_L,mn_R),
$$

$$
mx=\max(mx_L,mx_R),
$$

$$
need=\max\left(
need_L,\ need_R,\
\begin{cases}
L/2,&mx_L>mn_R,\\
0,&mx_L\le mn_R.
\end{cases}
\right).
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int minimum;
  int maximum;
  int need;
};
Node mergeNode(const Node& left, const Node& right, int half) {
  return {min(left.minimum, right.minimum), max(left.maximum, right.maximum),
      max({left.need, right.need, left.maximum > right.minimum ? half : 0})};
}
void solve() {
  int n, q;
  cin >> n >> q;
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  const int INF = 1'000'000'001;
  vector<Node> tree(2 * size, {INF, INF, 0});
  for (int i = 0; i < n; ++i) {
    cin >> tree[size + i].minimum;
    tree[size + i].maximum = tree[size + i].minimum;
  }
  int half = 1;
  for (int first = size; first > 1; first >>= 1, half <<= 1) {
    for (int node = first >> 1; node < first; ++node) {
      tree[node] = mergeNode(tree[node << 1], tree[node << 1 | 1], half);
    }
  }
  cout << tree[1].need << '\n';
  while (q--) {
    int index, value;
    cin >> index >> value;
    int node = size + index;
    tree[node] = {value, value, 0};
    half = 1;
    for (node >>= 1; node > 0; node >>= 1, half <<= 1) {
      tree[node] = mergeNode(tree[node << 1], tree[node << 1 | 1], half);
    }
    cout << tree[1].need << '\n';
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    solve();
  }
}
```

建树 $O(N)=O(n)$，每次更新 $O(\log n)$，总空间 $O(N)=O(n)$。

## 正确性证明

存在跨左右孩子的逆序对，当且仅当

$$
mx_L>mn_R.
$$

任意跨越该中点的两个下标，其最高不同二进制位恰对应 $L/2$，所以任何跨孩子逆序都会且只会把当前区间要求提升到 $L/2$。孩子内部逆序分别由 `need_L`、`need_R` 精确描述。

归纳假设两个孩子的三项信息均正确。合并后最小值、最大值显然正确；区间内任意逆序要么完全位于左孩子、完全位于右孩子，要么跨越二者，三种互斥情况的最大需求正是合并式。由叶到根归纳，根的 `need` 等于所有逆序对所需二次幂的最大值，也就是 $f(a)$。

点赋值只影响对应叶子及其到根路径；重新合并这些节点后所有不变量恢复，因此每个状态的答案都正确。

## 样例手推

数组 `[2,5,3,4,1,6]` 的根划分把下标 `[0,4)` 与 `[4,8)` 分开。左侧最大值 5 大于右侧有效最小值 1，存在跨根孩子逆序，因此根贡献 $L/2=4$。孩子内部需求不超过 2，根答案为 4。

更新 `a_1=2` 后，左侧仍有值大于下标 4 的 1，答案保持 4；再更新 `a_4=5` 后数组非递减，所有节点跨孩子条件均为假，答案降为 0。

## 易错点与方案比较

- XOR 的对象是下标，不是数组值。
- 下标已经是 zero-based，更新位置不能减一。
- 答案是 $i\oplus j$ 的最高位对应二次幂，不是完整 XOR 值。
- 排序目标为非递减，只有 `mx_L>mn_R` 才构成逆序；相等合法。
- 无逆序时答案为 0，不能输出 1。
- `q=0` 仍要输出初始状态答案。
- 补位值必须严格大于合法值并位于末尾，`1'000'000'001` 满足要求。
- 原题中 “updates are persistent” 只表示更新累计生效，不是可分叉持久化数据结构。
- D1 可逐尺度扫描，D2 的百万次更新要求把所有尺度汇总进同一棵树。

## 变种一：静态数组要求线性时间

新定义与 D1 相同，$q=0$。直接在补齐后的完整二叉划分上分治，每个节点只合并一次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Info {
  int minimum;
  int maximum;
  int need;
};
Info mergeInfo(const Info& left, const Info& right, int half) {
  return {min(left.minimum, right.minimum), max(left.maximum, right.maximum),
      max({left.need, right.need, left.maximum > right.minimum ? half : 0})};
}
Info build(const vector<int>& a, int left, int right) {
  if (right - left == 1) {
    int value = left < static_cast<int>(a.size()) ? a[left] : 1'000'000'001;
    return {value, value, 0};
  }
  int middle = (left + right) >> 1;
  return mergeInfo(build(a, left, middle), build(a, middle, right), (right - left) >> 1);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  cout << build(a, 0, size).need << '\n';
}
```

时间 $O(n)$，递归空间 $O(\log n)$。

## 变种二：恢复决定答案的逆序对

新定义：除 $k$ 外，输出一对 $i<j$，满足 $a_i>a_j$ 且其最高 XOR 位对应 $k$。节点额外保存最小值、最大值的位置与当前需求的见证对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int minimum;
  int maximum;
  int need;
  int minimumPosition;
  int maximumPosition;
  int witnessLeft;
  int witnessRight;
};
Node mergeNode(const Node& left, const Node& right, int half) {
  Node result;
  if (left.minimum <= right.minimum) {
    result.minimum = left.minimum;
    result.minimumPosition = left.minimumPosition;
  } else {
    result.minimum = right.minimum;
    result.minimumPosition = right.minimumPosition;
  }
  if (left.maximum >= right.maximum) {
    result.maximum = left.maximum;
    result.maximumPosition = left.maximumPosition;
  } else {
    result.maximum = right.maximum;
    result.maximumPosition = right.maximumPosition;
  }
  if (left.need >= right.need) {
    result.need = left.need;
    result.witnessLeft = left.witnessLeft;
    result.witnessRight = left.witnessRight;
  } else {
    result.need = right.need;
    result.witnessLeft = right.witnessLeft;
    result.witnessRight = right.witnessRight;
  }
  if (left.maximum > right.minimum) {
    result.need = half;
    result.witnessLeft = left.maximumPosition;
    result.witnessRight = right.minimumPosition;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  const int INF = 1'000'000'001;
  vector<Node> tree(2 * size, {INF, INF, 0, -1, -1, -1, -1});
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    tree[size + i] = {value, value, 0, i, i, -1, -1};
  }
  int half = 1;
  for (int first = size; first > 1; first >>= 1, half <<= 1) {
    for (int node = first >> 1; node < first; ++node) {
      tree[node] = mergeNode(tree[node << 1], tree[node << 1 | 1], half);
    }
  }
  cout << tree[1].need << ' ' << tree[1].witnessLeft << ' ' << tree[1].witnessRight << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。点更新版本只需沿路径用同一合并式重算，复杂度仍为 $O(\log n)$。

## 变种三：更新可从任意历史版本分叉

新定义：操作 `v i x` 从历史版本 `v` 创建新版本并赋值。使用可持久化线段树，每次只复制根到叶的路径。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int left;
  int right;
  int minimum;
  int maximum;
  int need;
};
vector<Node> tree;
int makeNode(const Node& node) {
  tree.push_back(node);
  return tree.size() - 1;
}
void pull(int node, int half) {
  const Node& left = tree[tree[node].left];
  const Node& right = tree[tree[node].right];
  tree[node].minimum = min(left.minimum, right.minimum);
  tree[node].maximum = max(left.maximum, right.maximum);
  tree[node].need = max({left.need, right.need, left.maximum > right.minimum ? half : 0});
}
int build(const vector<int>& a, int left, int right) {
  if (right - left == 1) {
    int value = left < static_cast<int>(a.size()) ? a[left] : 1'000'000'001;
    return makeNode({-1, -1, value, value, 0});
  }
  int middle = (left + right) >> 1;
  int leftChild = build(a, left, middle);
  int rightChild = build(a, middle, right);
  int node = makeNode({leftChild, rightChild, 0, 0, 0});
  pull(node, (right - left) >> 1);
  return node;
}
int update(int node, int left, int right, int position, int value) {
  int copy = makeNode(tree[node]);
  if (right - left == 1) {
    tree[copy].minimum = value;
    tree[copy].maximum = value;
    return copy;
  }
  int middle = (left + right) >> 1;
  if (position < middle) {
    tree[copy].left = update(tree[copy].left, left, middle, position, value);
  } else {
    tree[copy].right = update(tree[copy].right, middle, right, position, value);
  }
  pull(copy, (right - left) >> 1);
  return copy;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  vector<int> roots = {build(a, 0, size)};
  cout << tree[roots[0]].need << '\n';
  while (q--) {
    int version, index, value;
    cin >> version >> index >> value;
    roots.push_back(update(roots[version], 0, size, index, value));
    cout << tree[roots.back()].need << '\n';
  }
}
```

建树 $O(n)$，每个版本 $O(\log n)$ 时间与新增空间，总空间 $O(n+q\log n)$。

## 变种四：点赋值改为区间加

新定义：每次给区间 `[l,r]` 的所有值加上 `x`。完整覆盖某节点时，内部相对大小与 `need` 不变，只需给 `mn`、`mx` 和懒标记加 `x`；部分覆盖后重新合并跨孩子条件。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long minimum;
  long long maximum;
  long long lazy;
  int need;
};
struct SegmentTree {
  int n;
  int size = 1;
  vector<Node> tree;
  explicit SegmentTree(const vector<long long>& a) : n(a.size()) {
    while (size < n) {
      size <<= 1;
    }
    tree.resize(4 * size);
    build(1, 0, size, a);
  }
  void pull(int node, int half) {
    tree[node].minimum = min(tree[node << 1].minimum, tree[node << 1 | 1].minimum);
    tree[node].maximum = max(tree[node << 1].maximum, tree[node << 1 | 1].maximum);
    tree[node].need = max({tree[node << 1].need, tree[node << 1 | 1].need,
        tree[node << 1].maximum > tree[node << 1 | 1].minimum ? half : 0});
  }
  void build(int node, int left, int right, const vector<long long>& a) {
    if (right - left == 1) {
      long long value = left < n ? a[left] : (1LL << 60);
      tree[node] = {value, value, 0, 0};
      return;
    }
    int middle = (left + right) >> 1;
    build(node << 1, left, middle, a);
    build(node << 1 | 1, middle, right, a);
    pull(node, (right - left) >> 1);
  }
  void apply(int node, long long delta) {
    tree[node].minimum += delta;
    tree[node].maximum += delta;
    tree[node].lazy += delta;
  }
  void push(int node) {
    if (tree[node].lazy == 0) {
      return;
    }
    apply(node << 1, tree[node].lazy);
    apply(node << 1 | 1, tree[node].lazy);
    tree[node].lazy = 0;
  }
  void add(int node, int left, int right, int queryLeft, int queryRight, long long delta) {
    if (queryRight <= left || right <= queryLeft) {
      return;
    }
    if (queryLeft <= left && right <= queryRight) {
      apply(node, delta);
      return;
    }
    push(node);
    int middle = (left + right) >> 1;
    add(node << 1, left, middle, queryLeft, queryRight, delta);
    add(node << 1 | 1, middle, right, queryLeft, queryRight, delta);
    pull(node, (right - left) >> 1);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> a(n);
  for (long long& value : a) {
    cin >> value;
  }
  SegmentTree tree(a);
  cout << tree.tree[1].need << '\n';
  while (q--) {
    int left, right;
    long long delta;
    cin >> left >> right >> delta;
    tree.add(1, 0, tree.size, left, right + 1, delta);
    cout << tree.tree[1].need << '\n';
  }
}
```

建树 $O(n)$，每次区间加 $O(\log n)$，空间 $O(n)$。

## 可复现验证

- 推荐解必须输出官方样例中的六个值：`0,1,0,4,4,0`。
- 小规模随机数组可用逆序对公式作 oracle，并在随机点更新后逐状态对拍。
- 区间加、见证对与可持久化版本应分别与同一静态 oracle 对拍。
- 所有完整代码按 GNU++23 编译。

## Reference

- [CF 2247 D2 官方题面](https://codeforces.com/contest/2247/problem/D2)
- [CF Round 1111 官方比赛页](https://codeforces.com/contest/2247)
- [Codeforces 官方题解](https://codeforces.com/blog/entry/155337?locale=en)
- [Codeforces materials usage licence v0.1](https://codeforces.com/blog/entry/967)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://codeforces.com/contest/2247/problem/D2)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-512-q1-lc4000/">← [力扣竞赛] 第 512 场周赛 Q1 LC 4000 给定数位和的最大整数 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-30-lc3014/">[力扣每日一题] 2026-07-30｜LC 3014 输入单词需要的最少按键次数 I →</a>
</nav>
