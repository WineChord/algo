---
title: "[atcoder] ABC472 E Odd Cycle"
---

# [atcoder] ABC472 E Odd Cycle

<p class="daily-archive-kicker">2026-08-27 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-27 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=5c8dd9f66c0f833a69d04843eb5e2e692cccdefc73f59f662fdce526528b6584 -->
[AtCoder ABC472 E — Odd Cycle（官方英文题面）](https://atcoder.jp/contests/abc472/tasks/abc472_e?lang=en)

## 官方来源与元数据

- 来源：AtCoder Beginner Contest 472，E 题「Odd Cycle」
- 题目分值：450 分（AtCoder 官方）
- 比赛 Rated Range：0–1999（AtCoder 官方）
- 时间限制：2 秒
- 内存限制：1024 MiB
- AtCoder Problems 社区估算难度：1029（抓取于 2026-08-27；不是 AtCoder 官方难度）
- 题面入口：[AtCoder 官方英文题面](https://atcoder.jp/contests/abc472/tasks/abc472_e?lang=en)
- 使用条款：[AtCoder Terms of Service](https://atcoder.jp/tos)

下列英文题面层由模型根据官方页面独立组织，完整保留任务语义、输入输出、约束、样例与解释，不冒充逐字官方原文。

## Complete English statement

For each test case, you are given a simple, connected, undirected graph with $N$ vertices and $M$ edges. The vertices are numbered from $1$ to $N$, and edge $i$ joins $a_i$ and $b_i$.

Determine whether the graph contains a cycle with an odd number of vertices. If it does, output any one such cycle.

More precisely, you must find a sequence of integers $(v_1,v_2,\ldots,v_K)$ satisfying all of the following conditions:

- $K$ is odd and $K\ge 3$;
- the vertices $v_1,v_2,\ldots,v_K$ are pairwise distinct;
- for every $1\le i\le K$, vertices $v_i$ and $v_{i+1}$ are adjacent, where $v_{K+1}=v_1$.

If no such sequence exists, report that fact. There are $T$ independent test cases.

### Input

The input is given in the following form:

```text
T
case_1
case_2
...
case_T
```

Each test case has the following form:

```text
N M
a_1 b_1
a_2 b_2
...
a_M b_M
```

### Output

For each test case, print `-1` if no odd cycle exists. Otherwise, print one valid cycle in the following form:

```text
K
v_1 v_2 ... v_K
```

Any valid odd cycle is accepted.

### Constraints

- $1\le T\le 2\times 10^5$
- $1\le N,M\le 2\times 10^5$
- the sum of $N$ over all test cases is at most $2\times 10^5$
- the sum of $M$ over all test cases is at most $2\times 10^5$
- $1\le a_i,b_i\le N$
- $a_i\ne b_i$
- every graph is simple, connected, and undirected
- all input values are integers

### Official sample

```text
Input
4
3 3
1 2
2 3
1 3
7 7
1 2
2 3
3 4
1 4
4 5
5 6
6 7
5 5
1 2
2 3
3 4
4 5
1 5
9 10
1 2
2 3
3 4
4 5
1 5
6 7
7 8
8 9
6 9
1 6

Output
3
2 1 3
-1
5
3 2 1 5 4
5
3 2 1 5 4
```

For the first graph, $(2,1,3)$ is valid because all three closing edges exist; another cyclic order such as $(2,3,1)$ would also be accepted. The second graph has no odd cycle. The last two outputs exhibit a valid cycle of length $5$; the fourth graph may contain additional vertices and edges outside the reported cycle.

## 中文题意解释

每个测试用例给出一张简单、连通、无向图。要么输出 `-1`，证明图中不存在奇环；要么输出一个顶点互不相同、首尾相接且顶点数为奇数的环。输出不要求最短，因此关键不是枚举所有环，而是利用“无奇环当且仅当图可二分”这一等价关系，并在二分染色失败时恢复冲突环。

## 最优结论与推荐记忆方案

对图做 BFS 二染色，同时保存 BFS 树中的父亲和深度。若检查边 $(u,v)$ 时发现 `color[u] == color[v]`，那么 BFS 树中 $u$ 到 $v$ 的唯一路径长度为偶数；再加上边 $(u,v)$，就得到奇环。

沿父指针把较深端提升到同一深度，再同时上跳到最近公共祖先，即可恢复树路径上的全部顶点。总时间复杂度为 $O(N+M)$，额外空间复杂度为 $O(N+M)$。

推荐记住：**二染色冲突不仅能判定奇环存在，还天然给出“同色边 + 生成树路径”的恢复证据**。这比并查集只判冲突更适合需要输出具体环的题目。

## 约束推导、奇偶性与边界

所有测试的点数和、边数和都不超过 $2\times 10^5$，因此允许线性扫描，但不允许从每个起点重新搜图或枚举简单环。

决定算法的结构是：

- 在任意 BFS/DFS 生成树中，顶点颜色可取 `depth % 2`。
- 若边两端异色，它与树路径组成偶环或不产生冲突。
- 若边两端同色，则两端深度同奇偶；树路径长度

$$
\operatorname{dist}_T(u,v)=\operatorname{depth}(u)+\operatorname{depth}(v)
-2\operatorname{depth}(\operatorname{lca}(u,v))
$$

为偶数，加上一条冲突边后，环长为奇数。
- 树路径本身不重复顶点，图又无自环，所以恢复出的环一定简单且长度至少为 $3$。

真正需要覆盖的边界包括：

- $N=1$ 或图是一棵树：必然输出 `-1`。
- 图中只有偶环：二染色始终一致，仍输出 `-1`。
- 冲突边两端深度不同：先提升较深端，不能直接同步上跳。
- 冲突边的一端是另一端的祖先：公共祖先可能就是其中一端。
- 测试用例很多但总规模受限：每轮必须重新初始化状态，整体仍是线性复杂度。

## 官方样例手推

第一个图从顶点 $1$ 开始染色：`color[1] = 0`，顶点 $2,3$ 都被染成 $1$。检查边 $(2,3)$ 时，两端同色。BFS 树路径是 $2\to1\to3$，含 $3$ 个顶点；再用原边 $(3,2)$ 闭合，得到奇环 $(2,1,3)$。

第二个图可以按两侧集合稳定染色，所有边都连接异色顶点，因此没有冲突边。根据二分图与奇环的等价定理，图中不存在奇环。

## 解法一：枚举所有简单环

最直接的暴力是固定环中编号最小的起点，DFS 枚举不重复顶点的路径；只要回到起点且路径顶点数为奇数，就输出该路径。它覆盖了所有简单环，但最坏会枚举阶乘数量的路径，只适用于极小图。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int n;
vector<vector<int>> g;
vector<int> path, answer;
vector<char> used;
void dfs(int u, int start) {
  if (!answer.empty())
    return;
  for (int v : g[u]) {
    if (v == start && path.size() >= 3 && path.size() % 2 == 1) {
      answer = path;
      return;
    }
    if (v < start || used[v])
      continue;
    used[v] = true;
    path.push_back(v);
    dfs(v, start);
    path.pop_back();
    used[v] = false;
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int T;
  cin >> T;
  while (T--) {
    int m;
    cin >> n >> m;
    g.assign(n, {});
    for (int i = 0; i < m; ++i) {
      int u, v;
      cin >> u >> v;
      --u;
      --v;
      g[u].push_back(v);
      g[v].push_back(u);
    }
    answer.clear();
    used.assign(n, false);
    for (int s = 0; s < n && answer.empty(); ++s) {
      path = {s};
      used[s] = true;
      dfs(s, s);
      used[s] = false;
    }
    if (answer.empty()) {
      cout << -1 << '\n';
    } else {
      cout << answer.size() << '\n';
      for (int v : answer)
        cout << v + 1 << ' ';
      cout << '\n';
    }
  }
}
```

时间复杂度最坏为 $O(N!)$，递归栈和路径空间为 $O(N)$。瓶颈是同一前缀被扩展到大量不同简单路径，而题目只需要知道奇偶冲突。

## 从暴力到线性解法

暴力把“找一个奇环”当成组合枚举。图论等价关系把它改写为局部一致性检查：

1. 偶环允许沿边交替染成两色，奇环不允许。
2. 若整张图能二染色，它就是二分图，因此不存在奇环。
3. 若二染色第一次失败，失败边的两端同色；生成树已经保存了连接两端的偶长路径。
4. 只需恢复这一条路径，不必继续搜索其他环。

这样消除了全部环枚举和重复路径搜索，把复杂度降到 $O(N+M)$。

## 最佳实用解：BFS 二染色并恢复冲突环

### 算法

1. 从顶点 $1$ 开始 BFS；记录 `color`、`parent`、`depth`。
2. 遇到未访问邻点时，把它染成相反颜色并加入 BFS 树。
3. 遇到已访问且同色的邻点时，记下冲突边 $(u,v)$。
4. 用两个指针沿父链上跳：先把深度对齐，再同步上跳到公共祖先。
5. 把 $u$ 到公共祖先的链与公共祖先到 $v$ 的链拼接，输出所得顶点序列；原冲突边负责闭环。
6. 若 BFS 结束没有冲突，输出 `-1`。

### 正确性证明

**引理 1**：若 BFS 检查到同色边 $(u,v)$，BFS 树中 $u$ 到 $v$ 的路径长度为偶数。

**证明**：BFS 染色等于深度奇偶性。同色意味着两端深度同奇偶。树路径长度为两端深度之和减去公共祖先深度的两倍，因此为偶数。证毕。

**引理 2**：恢复的树路径加上边 $(u,v)$ 构成简单奇环。

**证明**：树中两点之间的路径唯一且不重复顶点；冲突边连接路径的两个不同端点。由引理 1，树路径边数为偶数，再加一条边后环长为奇数。简单图无自环，故环长至少为 $3$。证毕。

**引理 3**：若 BFS 没有发现同色边，图中不存在奇环。

**证明**：此时每条边都连接异色顶点，`color` 给出合法二分划分。二分图中的任意闭合游走必须交替经过两侧，所有简单环长度均为偶数，因此不存在奇环。证毕。

**定理**：算法在存在奇环时输出一个合法奇环，在不存在奇环时输出 `-1`。

**证明**：若出现冲突，结论由引理 2 成立；若无冲突，结论由引理 3 成立。两种情况覆盖所有输入。证毕。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> buildCycle(int u, int v, const vector<int>& parent, const vector<int>& depth) {
  vector<int> left, right;
  int x = u, y = v;
  while (depth[x] > depth[y]) {
    left.push_back(x);
    x = parent[x];
  }
  while (depth[y] > depth[x]) {
    right.push_back(y);
    y = parent[y];
  }
  while (x != y) {
    left.push_back(x);
    right.push_back(y);
    x = parent[x];
    y = parent[y];
  }
  left.push_back(x);
  reverse(right.begin(), right.end());
  left.insert(left.end(), right.begin(), right.end());
  return left;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int T;
  cin >> T;
  while (T--) {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n);
    for (int i = 0; i < m; ++i) {
      int u, v;
      cin >> u >> v;
      --u;
      --v;
      g[u].push_back(v);
      g[v].push_back(u);
    }
    vector<int> color(n, -1), parent(n, -1), depth(n);
    queue<int> q;
    color[0] = 0;
    q.push(0);
    vector<int> cycle;
    while (!q.empty() && cycle.empty()) {
      int u = q.front();
      q.pop();
      for (int v : g[u]) {
        if (color[v] == -1) {
          color[v] = color[u] ^ 1;
          parent[v] = u;
          depth[v] = depth[u] + 1;
          q.push(v);
        } else if (color[v] == color[u]) {
          cycle = buildCycle(u, v, parent, depth);
          break;
        }
      }
    }
    if (cycle.empty()) {
      cout << -1 << '\n';
    } else {
      cout << cycle.size() << '\n';
      for (int v : cycle)
        cout << v + 1 << ' ';
      cout << '\n';
    }
  }
}
```

## 复杂度、溢出与实现边界

- 每个点入队一次，每条无向边被检查两次，时间复杂度为 $O(N+M)$。
- 邻接表、BFS 状态和恢复路径共占 $O(N+M)$ 空间。
- 深度和顶点编号不超过 $2\times 10^5$，`int` 足够；算法没有乘法累计，不存在整数溢出风险。
- 一旦找到冲突即可停止；题目不要求最短奇环。
- 官方保证连通，因此从顶点 $1$ 搜索即可覆盖整张图。若去掉连通保证，要对每个未访问点启动一次 BFS。

## 同阶方案比较

递归 DFS 二染色也能在 $O(N+M)$ 内找到冲突，并用父链恢复环；但最深递归可能达到 $2\times 10^5$，需要额外处理栈深。BFS 使用显式队列，深度含义直观，恢复公式也更容易核对。

带奇偶关系的并查集能在线检测新边是否制造奇环，单次近似常数；但普通并查集不会保留一条可直接输出的图路径。若本题只要求判定，并查集很合适；既要判定又要恢复具体环时，BFS/DFS 生成树更稳定。

## 常见错误

- 只写“发现同色边”却没有保存父亲，最终无法输出环。
- 把树路径的顶点数和边数混淆；同色端点之间是偶数条树边、奇数个路径顶点。
- 拼接两条父链时把公共祖先加入两次，导致重复顶点。
- 忘记反转从 $v$ 向公共祖先收集的链，输出顺序不相邻。
- 把父子树边误判为冲突；合法二染色下父子颜色必然相反。
- 用递归 DFS 却没有考虑 $2\times 10^5$ 的栈深。

## 可复现验证

验证应同时检查“判定”和“输出契约”：对小规模所有简单图枚举边集，暴力枚举简单奇环作为 oracle；若最优程序输出 `-1`，oracle 也必须无解；否则逐项检查 $K$ 为不小于 $3$ 的奇数、顶点互异、每对相邻顶点及首尾闭合边都存在。再对长链、纯偶环、三角形、奇环挂树和多测试总规模边界做定向测试。

## Follow-up 与约束变种

### 变种一：只判定非连通图是否为二分图

新定义：图不保证连通，只需输出整张图是否二分，不要求恢复奇环。原算法的染色不变量仍成立，但必须从每个未访问顶点启动 BFS；省去父亲和深度即可。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<int>> g(n);
  for (int i = 0; i < m; ++i) {
    int u, v;
    cin >> u >> v;
    --u;
    --v;
    g[u].push_back(v);
    g[v].push_back(u);
  }
  vector<int> color(n, -1);
  bool ok = true;
  for (int s = 0; s < n && ok; ++s) {
    if (color[s] != -1)
      continue;
    queue<int> q;
    color[s] = 0;
    q.push(s);
    while (!q.empty() && ok) {
      int u = q.front();
      q.pop();
      for (int v : g[u]) {
        if (color[v] == -1) {
          color[v] = color[u] ^ 1;
          q.push(v);
        } else if (color[v] == color[u]) {
          ok = false;
          break;
        }
      }
    }
  }
  cout << (ok ? "YES" : "NO") << '\n';
}
```

时间复杂度为 $O(N+M)$，空间复杂度为 $O(N+M)$。

### 变种二：输出最短奇环

新定义：若存在奇环，必须输出顶点数最少的一个。单次二染色只能给任意冲突环，因此原算法失效。对每个起点做一次 BFS，并检查 BFS 树中每条同奇偶边；该边与树路径组成一个实际奇环，保留最短者。对全局最短奇环上的任一起点，BFS 不会产生更长的必要路径，因此最小候选就是全局最短奇环。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> makeCycle(int u, int v, const vector<int>& par, const vector<int>& dep) {
  vector<int> a, b;
  while (dep[u] > dep[v]) {
    a.push_back(u);
    u = par[u];
  }
  while (dep[v] > dep[u]) {
    b.push_back(v);
    v = par[v];
  }
  while (u != v) {
    a.push_back(u);
    b.push_back(v);
    u = par[u];
    v = par[v];
  }
  a.push_back(u);
  reverse(b.begin(), b.end());
  a.insert(a.end(), b.begin(), b.end());
  return a;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<int>> g(n);
  vector<pair<int, int>> edges;
  for (int i = 0; i < m; ++i) {
    int u, v;
    cin >> u >> v;
    --u;
    --v;
    g[u].push_back(v);
    g[v].push_back(u);
    edges.push_back({u, v});
  }
  vector<int> best;
  for (int s = 0; s < n; ++s) {
    vector<int> dist(n, -1), par(n, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      for (int v : g[u]) {
        if (dist[v] != -1)
          continue;
        dist[v] = dist[u] + 1;
        par[v] = u;
        q.push(v);
      }
    }
    for (auto [u, v] : edges) {
      if ((dist[u] ^ dist[v]) & 1)
        continue;
      vector<int> cycle = makeCycle(u, v, par, dist);
      if (cycle.size() % 2 == 0)
        continue;
      if (best.empty() || cycle.size() < best.size())
        best = move(cycle);
    }
  }
  if (best.empty()) {
    cout << -1 << '\n';
  } else {
    cout << best.size() << '\n';
    for (int v : best)
      cout << v + 1 << ' ';
    cout << '\n';
  }
}
```

时间复杂度为 $O(N(N+M))$，空间复杂度为 $O(N+M)$；规模放大时需要更专门的最短奇环算法或图结构限制。

### 变种三：边在线加入，只需报告何时首次出现奇环

新定义：初始无边，每次加入一条无向边后回答当前图是否仍为二分图，不要求输出环。静态 BFS 反复重跑会达到 $O(Q(N+M))$。用带异或势能的并查集维护 `color[u] XOR color[v] = 1`；同一连通块内若新约束与已有奇偶关系冲突，就出现奇环。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> p, size, xr;
  explicit DSU(int n) : p(n), size(n, 1), xr(n) {
    iota(p.begin(), p.end(), 0);
  }
  pair<int, int> find(int x) {
    if (p[x] == x)
      return {x, 0};
    auto [r, w] = find(p[x]);
    xr[x] ^= w;
    p[x] = r;
    return {p[x], xr[x]};
  }
  bool addOpposite(int a, int b) {
    auto [ra, xa] = find(a);
    auto [rb, xb] = find(b);
    if (ra == rb)
      return (xa ^ xb) == 1;
    if (size[ra] < size[rb]) {
      swap(ra, rb);
      swap(xa, xb);
    }
    p[rb] = ra;
    xr[rb] = xa ^ xb ^ 1;
    size[ra] += size[rb];
    return true;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  DSU dsu(n);
  bool ok = true;
  while (q--) {
    int u, v;
    cin >> u >> v;
    --u;
    --v;
    if (ok && !dsu.addOpposite(u, v))
      ok = false;
    cout << (ok ? "BIPARTITE" : "ODD CYCLE") << '\n';
  }
}
```

每次操作的摊还时间复杂度为 $O(\alpha(N))$，空间复杂度为 $O(N)$。若还要输出具体奇环，必须额外维护可恢复的动态生成森林，普通并查集信息不足。

### 变种四：统计合法二染色方案数

新定义：图可以不连通，求所有合法二染色方案数，颜色 `0/1` 有区别，答案对 $998244353$ 取模。若任一连通分量含奇环，答案为 $0$；否则每个非空连通分量可独立翻转两种颜色，因此答案为 $2^C$，其中 $C$ 是连通分量数。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 998244353;
  int n, m;
  cin >> n >> m;
  vector<vector<int>> g(n);
  for (int i = 0; i < m; ++i) {
    int u, v;
    cin >> u >> v;
    --u;
    --v;
    g[u].push_back(v);
    g[v].push_back(u);
  }
  vector<int> color(n, -1);
  long long answer = 1;
  for (int s = 0; s < n; ++s) {
    if (color[s] != -1)
      continue;
    answer = answer * 2 % mod;
    queue<int> q;
    color[s] = 0;
    q.push(s);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      for (int v : g[u]) {
        if (color[v] == -1) {
          color[v] = color[u] ^ 1;
          q.push(v);
        } else if (color[v] == color[u]) {
          cout << 0 << '\n';
          return 0;
        }
      }
    }
  }
  cout << answer << '\n';
}
```

时间复杂度为 $O(N+M)$，空间复杂度为 $O(N+M)$。

## 来源

- [AtCoder ABC472 E 官方题面](https://atcoder.jp/contests/abc472/tasks/abc472_e?lang=en)
- [AtCoder ABC472 比赛页](https://atcoder.jp/contests/abc472)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
- [AtCoder Problems](https://kenkoooo.com/atcoder/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc472/tasks/abc472_e?lang=en)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
