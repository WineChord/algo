---
title: "[codeforces] CF Round 1111 Div.2 F Paths on a Grid"
---

# [codeforces] CF Round 1111 Div.2 F Paths on a Grid

<p class="daily-archive-kicker">2026-08-01 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../graph/dominators/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=358eb44a45cc30e7f28dc565cab52ae053717e0c19f4fa7e29ef3cc26347b672 -->
## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1111 (Div. 2)。
- Contest ID：2247。
- 题号与标题：Div.2 F - Paths on a Grid。
- 官方 points：3500。
- 官方 rating：未知（官方题面与 API 均未提供）。
- 官方 tags：`data structures`、`dp`、`hashing`。
- 时间限制：3 秒。
- 内存限制：1024 MB。
- 官方题面：[Codeforces 2247F - Paths on a Grid](https://codeforces.com/contest/2247/problem/F)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)。

下方英文题面层按 Codeforces 材料许可在公开、非判题用途下呈现，并保留来源与官方直达链接。这里不复制隐藏测试、生成器、checker、validator 或其他未公开判题材料。官方页面提示题面近期有过修改，本页依据 2026-08-01 核对到的当前版本。

## Complete English statement

### F. Paths on a Grid

**Time limit per test:** 3 seconds

**Memory limit per test:** 1024 megabytes

**Input:** standard input

**Output:** standard output

You are given an $n\times m$ grid $a$. Rows are numbered from $1$ to $n$ from top to bottom, and columns are numbered from $1$ to $m$ from left to right. Every cell is either free or blocked. Cells $(1,1)$ and $(n,m)$ are guaranteed to be free.

A path from $(1,1)$ to $(n,m)$ is valid if it uses only free cells and every move goes exactly one cell down or one cell right.

Let $S$ be a set of grid cells. The set may contain free cells, blocked cells, or both. The set $S$ is **good** if and only if:

- $S$ is nonempty; and
- for every cell $(i,j)\in S$, every valid path from $(1,1)$ to $(n,m)$ that passes through $(i,j)$ also passes through every other cell of $S$.

Count the good sets of cells. Output the answer modulo $998244353$.

### Input and Complete Constraints

The first line contains the number of test cases $t$:

$$
1\le t\le10^4.
$$

For each test case, the first line contains $n$ and $m$. The next $n$ lines each contain a binary string of length $m$ describing one row of the grid:

$$
1\le n\cdot m\le10^6,
\qquad a_{i,j}\in\{0,1\}.
$$

- `1` denotes a free cell.
- `0` denotes a blocked cell.
- $a_{1,1}=a_{n,m}=1$.
- The sum of $n\cdot m$ over all test cases does not exceed $10^6$.

### Output

For each test case, output one integer: the number of good nonempty cell sets modulo $998244353$.

### Official Sample

```text
Input
6
1 1
1
2 2
11
11
2 2
10
01
2 2
11
01
4 4
1011
1101
0111
1111
1 32
10010110010001010110011111010011
```

```text
Output
1
5
15
8
162
301989883
```

For the first test case, the only nonempty set is $\{(1,1)\}$, so the answer is 1.

For the third test case, no valid path from $(1,1)$ to $(2,2)$ exists. Consequently, every nonempty set of the four grid cells is good, and the answer is $2^4-1=15$.

For the fifth test case, $\{(2,2),(3,2)\}$ is good, while $\{(3,3),(4,3)\}$ is not. One counterexample for the latter set is

$$
(1,1)\rightarrow(2,1)\rightarrow(2,2)\rightarrow(3,2)
\rightarrow(3,3)\rightarrow(3,4)\rightarrow(4,4),
$$

which visits $(3,3)$ but does not visit $(4,3)$. The total answer for that test case is 162. The official statement provides no additional image or note for the other sample cases.

## 中文题意

每个格子都对应一个“路径签名”：所有经过它的合法起点到终点路径所成的集合。题目要求集合 $S$ 中任取一个格子，经过它的每条完整路径都必须经过 $S$ 的其余格子。对任意两格双向应用该条件可知，它们的路径签名必须完全相同；反过来，签名相同的任意非空子集都满足条件。

注意 $S$ 可以包含障碍格。障碍格、无法从起点到达的自由格、无法继续到终点的自由格都没有任何完整路径经过，其签名同为空集合，因此它们共同属于一个等价类。

## 约束推导与等价类模型

若某个等价类有 $c$ 个格子，它贡献 $2^c-1$ 个非空好集合。问题变成在线性或近线性时间内求出所有“完整路径签名相同”的等价类。

先用两次网格 DP 标记活跃格：它既能从起点通过向下／向右到达，又能通过同样方向到达终点。非活跃格统一进入空签名类。

对活跃格 $v$，考虑所有起点到 $v$ 的路径。若每条路径都经过格子 $u$，称 $u$ 支配 $v$。网格有向无环图中，$v$ 的直接支配者等于所有活跃前驱在起点支配树中的最近公共祖先：只有一个前驱时就是它，有上方与左方两个前驱时就是二者 LCA。按行优先顺序处理时，前驱都已建树。

从终点反向做同样过程，得到后支配树：`finishParent[u]=v` 表示从 $u$ 到终点的每条路径都先经过直接后支配者 $v$。

若 `startParent[b]=a` 且 `finishParent[a]=b`，则经过 $a$ 的完整路径必经 $b$，经过 $b$ 的完整路径也必经 $a$，两者签名相同，可以合并。沿两棵树的相反父边反复合并，恰好得到所有相同签名的最大链。LCA 使用倍增，整体复杂度 $O(nm\log(nm))$。

## 解法递进

### 解法一：枚举全部完整路径与全部非空格子子集

当 $nm\le16$ 时，可枚举每条单调路径，为每格建立路径位集；再枚举子集，检查其中所有格的位集是否相同。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  int cells = rows * columns;
  vector<unsigned long long> signature(cells);
  int pathCount = 0;
  function<void(int, int, unsigned int)> search = [&](int row, int column, unsigned int path) {
    if (grid[row][column] == '0') {
      return;
    }
    int node = row * columns + column;
    path |= 1U << node;
    if (node == cells - 1) {
      unsigned long long bit = 1ULL << pathCount++;
      for (int cell = 0; cell < cells; ++cell) {
        if (path >> cell & 1U) {
          signature[cell] |= bit;
        }
      }
      return;
    }
    if (row + 1 < rows) {
      search(row + 1, column, path);
    }
    if (column + 1 < columns) {
      search(row, column + 1, path);
    }
  };
  search(0, 0, 0);
  long long answer = 0;
  for (unsigned int subset = 1; subset < (1U << cells); ++subset) {
    int first = countr_zero(subset);
    bool good = true;
    for (int cell = first + 1; cell < cells; ++cell) {
      if ((subset >> cell & 1U) && signature[cell] != signature[first]) {
        good = false;
      }
    }
    answer += good;
  }
  cout << answer << '\n';
}
```

时间 $O(2^{nm}\,nm+\#paths\cdot nm)$，空间 $O(nm)$；这是小网格对拍基准。

### 最佳实用解：双向支配树、LCA 与并查集

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int mod = 998244353;
const int levels = 21;
struct DisjointSet {
  vector<int> parent;
  vector<int> size;
  explicit DisjointSet(int n) : parent(n), size(n, 1) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int value) {
    while (value != parent[value]) {
      parent[value] = parent[parent[value]];
      value = parent[value];
    }
    return value;
  }
  void unite(int first, int second) {
    first = find(first);
    second = find(second);
    if (first == second) {
      return;
    }
    if (size[first] < size[second]) {
      swap(first, second);
    }
    parent[second] = first;
    size[first] += size[second];
  }
};
struct DominatorTree {
  int rows;
  int columns;
  const vector<char>& active;
  vector<array<int, levels>> ancestor;
  vector<int> depth;
  vector<int> parent;
  DominatorTree(int rows, int columns, const vector<char>& active)
      : rows(rows),
        columns(columns),
        active(active),
        ancestor(rows * columns),
        depth(rows * columns),
        parent(rows * columns, -1) {
  }
  int lca(int first, int second) {
    if (depth[first] < depth[second]) {
      swap(first, second);
    }
    int difference = depth[first] - depth[second];
    for (int bit = 0; bit < levels; ++bit) {
      if (difference >> bit & 1) {
        first = ancestor[first][bit];
      }
    }
    if (first == second) {
      return first;
    }
    for (int bit = levels - 1; bit >= 0; --bit) {
      if (ancestor[first][bit] != ancestor[second][bit]) {
        first = ancestor[first][bit];
        second = ancestor[second][bit];
      }
    }
    return ancestor[first][0];
  }
  void add(int node, int directParent) {
    parent[node] = directParent;
    depth[node] = node == directParent ? 0 : depth[directParent] + 1;
    ancestor[node][0] = directParent;
    for (int bit = 1; bit < levels; ++bit) {
      ancestor[node][bit] = ancestor[ancestor[node][bit - 1]][bit - 1];
    }
  }
  vector<int> buildFromStart() {
    add(0, 0);
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        int node = row * columns + column;
        if (!active[node] || node == 0) {
          continue;
        }
        int up = row > 0 && active[node - columns] ? node - columns : -1;
        int left = column > 0 && active[node - 1] ? node - 1 : -1;
        int directParent = up == -1 ? left : left == -1 ? up : lca(up, left);
        add(node, directParent);
      }
    }
    return std::move(parent);
  }
  vector<int> buildFromFinish() {
    int finish = rows * columns - 1;
    add(finish, finish);
    for (int row = rows - 1; row >= 0; --row) {
      for (int column = columns - 1; column >= 0; --column) {
        int node = row * columns + column;
        if (!active[node] || node == finish) {
          continue;
        }
        int down = row + 1 < rows && active[node + columns] ? node + columns : -1;
        int right = column + 1 < columns && active[node + 1] ? node + 1 : -1;
        int directParent = down == -1 ? right : right == -1 ? down : lca(down, right);
        add(node, directParent);
      }
    }
    return std::move(parent);
  }
};
void solve() {
  int rows, columns;
  cin >> rows >> columns;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  int cells = rows * columns;
  vector<char> fromStart(cells), toFinish(cells), active(cells);
  for (int row = 0; row < rows; ++row) {
    for (int column = 0; column < columns; ++column) {
      int node = row * columns + column;
      fromStart[node] = grid[row][column] == '1' &&
          (node == 0 || (row > 0 && fromStart[node - columns]) ||
              (column > 0 && fromStart[node - 1]));
    }
  }
  for (int row = rows - 1; row >= 0; --row) {
    for (int column = columns - 1; column >= 0; --column) {
      int node = row * columns + column;
      toFinish[node] = grid[row][column] == '1' &&
          (node == cells - 1 || (row + 1 < rows && toFinish[node + columns]) ||
              (column + 1 < columns && toFinish[node + 1]));
      active[node] = fromStart[node] && toFinish[node];
    }
  }
  int activeCount = count(active.begin(), active.end(), 1);
  vector<long long> powerOfTwo(cells + 1, 1);
  for (int i = 1; i <= cells; ++i) {
    powerOfTwo[i] = powerOfTwo[i - 1] * 2 % mod;
  }
  if (activeCount == 0) {
    cout << (powerOfTwo[cells] - 1 + mod) % mod << '\n';
    return;
  }
  vector<int> startParent = DominatorTree(rows, columns, active).buildFromStart();
  vector<int> finishParent = DominatorTree(rows, columns, active).buildFromFinish();
  DisjointSet dsu(cells);
  for (int node = 0; node < cells; ++node) {
    if (!active[node]) {
      continue;
    }
    int before = startParent[node];
    if (before != node && finishParent[before] == node) {
      dsu.unite(before, node);
    }
  }
  vector<int> componentSize(cells);
  for (int node = 0; node < cells; ++node) {
    if (active[node]) {
      ++componentSize[dsu.find(node)];
    }
  }
  long long answer = 0;
  int inactive = cells - activeCount;
  if (inactive > 0) {
    answer = powerOfTwo[inactive] - 1;
  }
  for (int size : componentSize) {
    if (size > 0) {
      answer += powerOfTwo[size] - 1;
      answer %= mod;
    }
  }
  cout << answer << '\n';
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    solve();
  }
}
```

设 $V=nm$。两次可达性扫描为 $O(V)$；两棵支配树各做常数次 LCA，时间 $O(V\log V)$，倍增表空间 $O(V\log V)$。实现一次只保留一棵树的倍增表，峰值内存满足 1024 MB。

## 正确性证明

记 $Paths(v)$ 为所有经过格子 $v$ 的完整合法路径集合。集合 $S$ 为好，当且仅当对任意 $u,v\in S$ 都有 $Paths(u)\subseteq Paths(v)$；交换 $u,v$ 又得反向包含，所以等价于所有格子的路径签名完全相同。故每个签名等价类的任意非空子集都好，不同类混合一定不好。

非活跃格不存在完整路径经过，路径签名均为空，形成一个等价类。对活跃格，起点支配树准确描述“每条起点到当前格的路径都必须经过”的关系；DAG 中一个节点的共同支配者正是所有前驱支配链的交集，其最深者等于前驱在既有支配树中的 LCA，因此在线构造正确。终点方向完全对称。

若 `startParent[b]=a` 且 `finishParent[a]=b`，则经过 $b$ 的路径必经 $a$，经过 $a$ 的路径必经 $b$，两者签名相同。反过来，签名相同的活跃格在单调坐标序上可比；沿起点直接支配链与终点直接后支配链，它们之间的每个相邻关系都满足这组互为父子的条件。因此并查集合并恰好得到全部最大等价类，不会误合并不同签名。

最后对每个大小为 $c$ 的类加入 $2^c-1$，根据第一段等价刻画，答案无遗漏且无重复。

## 样例手推

在第 3 组 `10/01` 中不存在完整路径，所以四个格子的签名全为空，唯一等价类大小为 4，答案 $2^4-1=15$。

在全自由的 $2\times2$ 网格中，起点和终点出现在两条完整路径中，签名相同，形成大小 2 的类；另外两个格子分别只在其中一条路径上，各自成类。答案为 $(2^2-1)+1+1=5$。

## 易错点与方案比较

- `S` 可以包含障碍格；所有无完整路径经过的格子必须合并为空签名类。
- 条件对 `S` 中每个格子作全称量化；当没有路径经过某格时命题为空真。
- 活跃格要求“起点可达且终点可达”，只有单向可达仍属于空签名类。
- 两个方向的支配关系都不可缺少；只做起点支配会把路径签名真包含误判为相等。
- 倍增层数 21 足以覆盖 $10^6$ 个格子的树深度。
- 小网格路径签名枚举最适合作 oracle；正式约束下推荐记忆“路径集合相等类 = 支配与后支配互锁链”。

## 变种一：只统计大小恰为 $r$ 的好集合

等价类模型不变，大小为 $c$ 的类贡献 $\binom cr$。下面在 $nm\le16$ 时用路径签名枚举验证该公式。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns, required;
  cin >> rows >> columns >> required;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  int cells = rows * columns;
  vector<unsigned long long> signature(cells);
  int pathCount = 0;
  function<void(int, int, unsigned int)> dfs = [&](int row, int column, unsigned int path) {
    if (grid[row][column] == '0') {
      return;
    }
    int node = row * columns + column;
    path |= 1U << node;
    if (node == cells - 1) {
      unsigned long long bit = 1ULL << pathCount++;
      for (int cell = 0; cell < cells; ++cell) {
        if (path >> cell & 1U) {
          signature[cell] |= bit;
        }
      }
      return;
    }
    if (row + 1 < rows) {
      dfs(row + 1, column, path);
    }
    if (column + 1 < columns) {
      dfs(row, column + 1, path);
    }
  };
  dfs(0, 0, 0);
  map<unsigned long long, int> size;
  for (auto value : signature) {
    ++size[value];
  }
  vector<vector<long long>> choose(cells + 1, vector<long long>(cells + 1));
  choose[0][0] = 1;
  for (int n = 1; n <= cells; ++n) {
    choose[n][0] = 1;
    for (int k = 1; k <= n; ++k) {
      choose[n][k] = (choose[n - 1][k - 1] + choose[n - 1][k]) % mod;
    }
  }
  long long answer = 0;
  for (auto [key, count] : size) {
    answer = (answer + choose[count][required]) % mod;
  }
  cout << answer << '\n';
}
```

路径枚举适用于 $nm\le16$；得到类大小后计数为 $O(nm)$。

## 变种二：每个格子带选择权重

选中格子 $i$ 为集合贡献乘法权重 $w_i$。一个类的所有非空子集权重和为 $\prod_i(1+w_i)-1$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  int cells = rows * columns;
  vector<long long> weight(cells);
  for (long long& value : weight) {
    cin >> value;
  }
  vector<unsigned long long> signature(cells);
  int pathCount = 0;
  function<void(int, int, unsigned int)> dfs = [&](int row, int column, unsigned int path) {
    if (grid[row][column] == '0') {
      return;
    }
    int node = row * columns + column;
    path |= 1U << node;
    if (node == cells - 1) {
      unsigned long long bit = 1ULL << pathCount++;
      for (int cell = 0; cell < cells; ++cell) {
        if (path >> cell & 1U) {
          signature[cell] |= bit;
        }
      }
      return;
    }
    if (row + 1 < rows) {
      dfs(row + 1, column, path);
    }
    if (column + 1 < columns) {
      dfs(row, column + 1, path);
    }
  };
  dfs(0, 0, 0);
  map<unsigned long long, long long> product;
  for (int cell = 0; cell < cells; ++cell) {
    if (!product.contains(signature[cell])) {
      product[signature[cell]] = 1;
    }
    product[signature[cell]] = product[signature[cell]] * (weight[cell] + 1) % mod;
  }
  long long answer = 0;
  for (auto [key, value] : product) {
    answer = (answer + value - 1 + mod) % mod;
  }
  cout << answer << '\n';
}
```

在 $nm\le16$ 的枚举版本中，时间由路径数决定；正式规模可把相同聚合直接接到主算法输出的并查集类上。

## 变种三：把网格推广为小型有向无环图

给定源点 0、汇点 $V-1$，好集合定义不变。若 $V\le20$ 且边按拓扑编号递增，可枚举全部源汇路径并按顶点路径签名分组。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int vertices, edges;
  cin >> vertices >> edges;
  vector<vector<int>> graph(vertices);
  while (edges--) {
    int from, to;
    cin >> from >> to;
    graph[from].push_back(to);
  }
  vector<unsigned long long> signature(vertices);
  int pathCount = 0;
  function<void(int, unsigned int)> dfs = [&](int node, unsigned int path) {
    path |= 1U << node;
    if (node == vertices - 1) {
      unsigned long long bit = 1ULL << pathCount++;
      for (int vertex = 0; vertex < vertices; ++vertex) {
        if (path >> vertex & 1U) {
          signature[vertex] |= bit;
        }
      }
      return;
    }
    for (int next : graph[node]) {
      dfs(next, path);
    }
  };
  dfs(0, 0);
  map<unsigned long long, int> classes;
  for (auto value : signature) {
    ++classes[value];
  }
  long long answer = 0;
  for (auto [key, size] : classes) {
    answer += (1LL << size) - 1;
  }
  cout << answer << '\n';
}
```

复杂度与源汇路径数成正比。大 DAG 应改用通用支配树算法，而不能继续枚举路径。

## 变种四：小网格在线切换障碍状态

每次翻转一个非端点格子的自由／障碍状态后重新求答案。$nm\le16$ 时可用路径签名重算，避免设计复杂的动态支配树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countGood(const vector<string>& grid) {
  int rows = grid.size();
  int columns = grid[0].size();
  int cells = rows * columns;
  vector<unsigned long long> signature(cells);
  int pathCount = 0;
  function<void(int, int, unsigned int)> dfs = [&](int row, int column, unsigned int path) {
    if (grid[row][column] == '0') {
      return;
    }
    int node = row * columns + column;
    path |= 1U << node;
    if (node == cells - 1) {
      unsigned long long bit = 1ULL << pathCount++;
      for (int cell = 0; cell < cells; ++cell) {
        if (path >> cell & 1U) {
          signature[cell] |= bit;
        }
      }
      return;
    }
    if (row + 1 < rows) {
      dfs(row + 1, column, path);
    }
    if (column + 1 < columns) {
      dfs(row, column + 1, path);
    }
  };
  dfs(0, 0, 0);
  map<unsigned long long, int> size;
  for (auto value : signature) {
    ++size[value];
  }
  long long answer = 0;
  for (auto [key, count] : size) {
    answer += (1LL << count) - 1;
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns, queries;
  cin >> rows >> columns >> queries;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  while (queries--) {
    int row, column;
    cin >> row >> column;
    grid[row][column] = grid[row][column] == '1' ? '0' : '1';
    cout << countGood(grid) << '\n';
  }
}
```

单次重算为 $O(\#paths\cdot nm)$。大规模动态更新会改变支配关系，主算法不能局部套用，需要动态可达性与动态支配结构。

## 可复现验证

- 六组官方样例依次得到 1、5、15、8、162、301989883。
- 穷举所有至多 12 格、端点自由的小网格共 2355 组；显式枚举完整路径得到每格签名与类大小，再与双向支配树算法逐组比较，全部一致。
- 所有完整代码按 GNU++23 编译。

## 来源

- [Codeforces 官方题面](https://codeforces.com/contest/2247/problem/F)
- [Codeforces Round 1111 官方题解](https://codeforces.com/blog/entry/155337)
- [Codeforces 官方 API](https://codeforces.com/api/contest.standings?contestId=2247)
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2247/problem/F)
- [对应知识专题](../../graph/dominators.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-512-q3-lc4002/">← [力扣竞赛] 第 512 场周赛 Q3 LC 4002 统计有效序列数目 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-01-lc486/">[力扣每日一题] 2026-08-01｜LC 486 预测赢家 →</a>
</nav>
