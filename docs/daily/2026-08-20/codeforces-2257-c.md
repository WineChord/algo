---
title: "[codeforces] CF Round 1117 Div.2 C Spying on the Beaver"
---

# [codeforces] CF Round 1117 Div.2 C Spying on the Beaver

<p class="daily-archive-kicker">2026-08-20 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-20 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=5ef7488941babb959dec1cc54eaa6b9253d1315833a9f5672543ded7eb1b8910 -->
[Official problem: Codeforces Round 1117 (Div. 2), C — Spying on the Beaver](https://codeforces.com/contest/2257/problem/C?locale=en)

## 官方来源与元数据

- 比赛 ID：2257；正式比赛名：Codeforces Round 1117 (Div. 2)，比赛已经结束。
- 题目：Div.2 C — Spying on the Beaver；没有经官方关系确认的跨组别别名。
- 官方分值：1250；官方当前未给出 problem rating。
- 官方标签：`dfs and similar`、`dsu`、`graphs`、`trees`。
- 时间限制：2 秒；内存限制：256 MB。
- 题面没有理解所必需的图片。

下方英文层依据官方页面完整、自包含地呈现任务；Codeforces 来源、直达链接和材料使用许可
就近列出。

## Complete English statement

You are given a tree rooted at vertex $1$. Its $n$ vertices are numbered from $1$ through $n$.
Starting at the root, a Beaver walks along the unique root-to-vertex path to exactly one dam. The possible
destinations are the $m$ distinct vertices $a_1,a_2,\ldots,a_m$.

Before the Beaver moves, you may install cameras on any tree edges. After the movement finishes, you
receive the ordered sequence of camera-equipped edges that the Beaver traversed. Choose as few cameras
as possible while guaranteeing that this observation uniquely identifies which of the $m$ dam vertices
was reached.

For every test case, output the minimum number $k$ and one valid placement. An edge is identified by its
non-root endpoint $u$: outputting $u$ means placing a camera on the edge joining $u$ to its parent $p_u$.

### Input

The input contains several test cases.

```text
t
For each test case:
n
p_2 p_3 ... p_n
m
a_1 a_2 ... a_m
```

The second line of each test case contains exactly $n-1$ integers; $p_i$ is the parent of vertex $i$
for every $2\le i\le n$.

### Constraints

- $1\le t\le2\cdot10^4$.
- $2\le n\le10^5$ in each test case.
- For every $2\le i\le n$, $1\le p_i<i$.
- $1\le m\le n$.
- $1\le a_i\le n$, and all dam vertices are distinct.
- The sum of $n$ over all test cases does not exceed $10^5$.

### Output

For each test case, print exactly one line. First print the minimum camera count $k$, followed by $k$
vertex numbers $u$ whose parent edges receive cameras. If several minimum placements exist, print any
one of them.

### Official samples

```text
Input
4
2
1
1
1
3
1 1
3
2 3 1
3
1 2
2
2 3
6
1 2 2 1 1
3
5 3 1

Output
0
2 2 3
1 3
2 2 5
```

In the first test case there is only one possible dam, so no camera is needed. In the second, every
vertex is a dam and both edges need cameras. In the third, the two dams are adjacent; a camera on their
connecting edge distinguishes them.

Additional observation: the fourth output is one of possibly several optimal placements.

Statement source: [Codeforces problem 2257C](https://codeforces.com/contest/2257/problem/C?locale=en).
This public, non-judge presentation follows the
[Codeforces materials usage license v0.1](https://codeforces.com/page/254); see also the
[official materials notice](https://codeforces.com/blog/entry/967?locale=en).

## 中文解释与题解

海狸从根走到某个候选坝点，路径唯一。摄像头只会报告它所在边是否出现在这条路径中。我们
要把所有候选坝点的观测序列两两区分，并输出最少摄像头所在边。

## 约束推导：摄像头就是树上的割边

移除所有装有摄像头的边，树被切成若干连通块。两个终点得到相同观测，当且仅当它们落在
同一个连通块：

- 若在同一块，两条根路径之间的差异路径不含摄像头，摄像头序列完全相同；
- 若在不同块，从根到这两个块经过的第一条不同摄像头边就能区分二者。

一棵树移除 $k$ 条边恰得到 $k+1$ 个连通块。要让 $m$ 个坝点各在不同块，必有

$$
k+1\ge m\quad\Longrightarrow\quad k\ge m-1.
$$

下界还需要构造达到。任选深度最小的坝点 $r$ 不切它的父边；对其余每个坝点 $v$，直接在
边 $(p_v,v)$ 上放摄像头，共 $m-1$ 个。任何被切出的坝点 $v$ 不会包含未切的 $r$：否则
$v$ 是 $r$ 的真祖先，深度会更小。它的坝点后代又各自在自己的父边处被继续切开，因此
$v$ 所在块只有它一个坝点。根所在剩余块也只含 $r$。

父节点满足 $p_i<i$，读入时即可算 `depth[i] = depth[p[i]] + 1`。$n$ 总和为 $10^5$，线性
处理足够；答案只输出已有顶点编号，不涉及整数溢出。

## 样例手推与边界

- 第一组只有坝点 1，选它为保留点，输出 0。
- 第二组的坝点是 2、3、1；根 1 深度最小，切边 1–2、1–3，输出 `2 2 3`。
- 第三组是一条链 1–2–3，坝点 2、3；保留较浅的 2，只切 2–3，输出 `1 3`。
- 若所有坝点在同一根到叶路径上，除最浅坝点外逐个切父边，得到嵌套但互异的观测序列。
- 若多个坝点深度并列，任取一个保留都合法；同深度节点不可能互为祖先。
- 根是否为坝点不需要特判：它自然是全树最浅点。

## 解法一：枚举摄像头边集

当 $n\le20$ 时，枚举 $n-1$ 条边的所有子集。未装摄像头的边用并查集合并；若任何连通块
含两个坝点，该子集无效。取摄像头数最少的有效子集。这完整覆盖所有放置方案，但时间为
$O(2^{n-1}n\alpha(n))$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent, size;
  explicit DSU(int n) : parent(n), size(n, 1) { iota(parent.begin(), parent.end(), 0); }
  int find(int node) { return parent[node] == node ? node : parent[node] = find(parent[node]); }
  void unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) return;
    if (size[a] < size[b]) swap(a, b);
    parent[b] = a;
    size[a] += size[b];
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n;
    cin >> n;
    vector<int> parent(n);
    for (int vertex = 1; vertex < n; ++vertex) {
      cin >> parent[vertex];
      --parent[vertex];
    }
    int m;
    cin >> m;
    vector<int> dams(m);
    for (int& vertex : dams) {
      cin >> vertex;
      --vertex;
    }
    int bestMask = 0;
    int bestCount = n;
    for (int mask = 0; mask < (1 << (n - 1)); ++mask) {
      int cameras = popcount(static_cast<unsigned>(mask));
      if (cameras >= bestCount) continue;
      DSU dsu(n);
      for (int vertex = 1; vertex < n; ++vertex) {
        if ((mask & (1 << (vertex - 1))) == 0) dsu.unite(vertex, parent[vertex]);
      }
      vector<int> count(n);
      bool valid = true;
      for (int vertex : dams) {
        if (++count[dsu.find(vertex)] > 1) valid = false;
      }
      if (valid) {
        bestCount = cameras;
        bestMask = mask;
      }
    }
    cout << bestCount;
    for (int vertex = 1; vertex < n; ++vertex) {
      if (bestMask & (1 << (vertex - 1))) cout << ' ' << vertex + 1;
    }
    cout << '\n';
  }
  return 0;
}
```

## 从子集搜索到紧下界

暴力在检查每种边集是否把坝点分开，却忽略了树删 $k$ 边必成 $k+1$ 块这一固定结构。
组件数立即给出 $m-1$ 下界；再把摄像头放到除一个最浅坝点外的各坝点父边，恰好达到
下界，搜索完全消失。

## 最佳实用解：保留一个最浅坝点

### 正确性证明

**引理 1**：任何可行方案至少需要 $m-1$ 个摄像头。

移除 $k$ 条摄像头边后只有 $k+1$ 个连通块。同块坝点观测相同，所以每块至多一个坝点；
至少需要 $m$ 块，故 $k\ge m-1$。

**引理 2**：选择最浅坝点 $r$，切断其余每个坝点的父边，会让每个连通块至多含一个坝点。

对任意被切坝点 $v$，其父边已把它与祖先分开；其他坝点若是 $v$ 的后代，也在自己的父边
处被切走。唯一未切坝点 $r$ 不可能是 $v$ 的后代，否则 $v$ 比最浅的 $r$ 更浅。因此
$v$ 所在块只含它。所有其他坝点都被切出，剩余根块只含 $r$。

**定理**：算法输出最少摄像头的合法方案。

引理 2 证明输出方案合法，摄像头数正好是 $m-1$；引理 1 证明任何方案都不能更少，因此
该构造最优。

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
    int n;
    cin >> n;
    vector<int> depth(n + 1);
    for (int vertex = 2; vertex <= n; ++vertex) {
      int parent;
      cin >> parent;
      depth[vertex] = depth[parent] + 1;
    }
    int m;
    cin >> m;
    vector<int> dams(m);
    for (int& vertex : dams) cin >> vertex;
    int keep = *min_element(dams.begin(), dams.end(), [&](int a, int b) {
      return depth[a] < depth[b];
    });
    cout << m - 1;
    for (int vertex : dams) {
      if (vertex != keep) cout << ' ' << vertex;
    }
    cout << '\n';
  }
  return 0;
}
```

时间复杂度 $O(n+m)$，额外空间 $O(n+m)$；若边读入后只保留深度，已经是最简稳定实现。
竞赛中建议优先记住“摄像头边的删除组件 = 观测等价类”，这比先写 DFS 或 DSU 更快触及
紧下界。

## 易错点

- 任意保留一个坝点后直接切其他坝点父边不一定合法；保留点必须不在某个已切坝点的子树
  中，选择全局最浅坝点即可保证。
- 输出的是子节点编号 `u`，代表边 `(p_u,u)`，不是输出两个端点。
- $m=1$ 时只输出 `0`，不能访问不存在的摄像头列表。
- 父节点输入从 `p_2` 开始；根 1 没有父边。
- 摄像头观测是路径上的边序列，但不能据此得到超过 $k+1$ 个等价类；每个删边组件恰对应
  一个序列。

## 可复现验证

程序按 GNU++23 编译并通过官方样例。对所有小规模父数组树与非空坝点子集，将线性构造
与边集枚举 oracle 比较：构造始终可区分全部坝点，摄像头数与暴力最优值相同。专项覆盖根
为坝、祖先—后代链、星形树、多层分叉、最浅深度并列和 $m=1$。

## 变种一：每条边有不同安装费用

新定义：边 $(p_v,v)$ 的费用为非负整数 $w_v$，并保证全部边费之和不超过 $10^{18}$；仍要
把坝点两两分开，最小化总费用。固定切坝点父边
不再最优。树形 DP 令 `dp[u][c]` 表示 `u` 子树内部已合法分隔，且仍与 `u` 连通的组件含
$c\in\{0,1\}$ 个坝点时的最小费用。对子边可切断并付费，也可保留但要求两侧坝点数之和
不超过 1。时间 $O(n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<pair<int, long long>>> children(n + 1);
  for (int vertex = 2; vertex <= n; ++vertex) {
    int parent;
    long long cost;
    cin >> parent >> cost;
    children[parent].push_back({vertex, cost});
  }
  int m;
  cin >> m;
  vector<char> marked(n + 1);
  while (m--) {
    int vertex;
    cin >> vertex;
    marked[vertex] = true;
  }
  const long long inf = numeric_limits<long long>::max() / 4;
  vector<array<long long, 2>> dp(n + 1);
  for (int node = n; node >= 1; --node) {
    dp[node] = {inf, inf};
    dp[node][marked[node]] = 0;
    for (auto [child, edgeCost] : children[node]) {
      array<long long, 2> next{inf, inf};
      long long cut = min(dp[child][0], dp[child][1]) + edgeCost;
      for (int here = 0; here <= 1; ++here) {
        next[here] = min(next[here], dp[node][here] + cut);
        for (int below = 0; below + here <= 1; ++below) {
          next[here + below] = min(
              next[here + below], dp[node][here] + dp[child][below]);
        }
      }
      dp[node] = next;
    }
  }
  cout << min(dp[1][0], dp[1][1]) << '\n';
  return 0;
}
```

## 变种二：只有部分边允许安装摄像头

新定义：每条父边给出 `allowed`，不允许的边不能切；问是否能区分全部坝点及最少数量。
沿用上一个 DP，把可切边费用设为 1，不可切边的切断转移设为无穷。若根状态仍为无穷则
无解。时间 $O(n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<pair<int, bool>>> children(n + 1);
  for (int vertex = 2; vertex <= n; ++vertex) {
    int parent, allowed;
    cin >> parent >> allowed;
    children[parent].push_back({vertex, allowed != 0});
  }
  int m;
  cin >> m;
  vector<char> marked(n + 1);
  while (m--) {
    int vertex;
    cin >> vertex;
    marked[vertex] = true;
  }
  const int inf = 1000000000;
  vector<array<int, 2>> dp(n + 1);
  for (int node = n; node >= 1; --node) {
    dp[node] = {inf, inf};
    dp[node][marked[node]] = 0;
    for (auto [child, allowed] : children[node]) {
      array<int, 2> next{inf, inf};
      int cut = allowed ? min(dp[child][0], dp[child][1]) + 1 : inf;
      for (int here = 0; here <= 1; ++here) {
        if (dp[node][here] < inf && cut < inf) next[here] = dp[node][here] + cut;
        for (int below = 0; below + here <= 1; ++below) {
          if (dp[node][here] < inf && dp[child][below] < inf) {
            next[here + below] = min(
                next[here + below], dp[node][here] + dp[child][below]);
          }
        }
      }
      dp[node] = next;
    }
  }
  int answer = min(dp[1][0], dp[1][1]);
  cout << (answer >= inf ? -1 : answer) << '\n';
  return 0;
}
```

## 变种三：统计最少摄像头方案数

新定义：返回最少摄像头数及达到最少值的边集数量，模 $10^9+7$。状态仍是根连通组件含
0 或 1 个坝点，但每个状态同时维护最小费用与方案数；同费用转移累加计数。时间 $O(n)$，
空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int mod = 1000000007;
struct State { int cost; int ways; };
void relax(State& target, int cost, long long ways) {
  if (cost < target.cost) target = {cost, static_cast<int>(ways % mod)};
  else if (cost == target.cost) target.ways = (target.ways + ways) % mod;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<int>> children(n + 1);
  for (int vertex = 2; vertex <= n; ++vertex) {
    int parent;
    cin >> parent;
    children[parent].push_back(vertex);
  }
  int m;
  cin >> m;
  vector<char> marked(n + 1);
  while (m--) {
    int vertex;
    cin >> vertex;
    marked[vertex] = true;
  }
  const int inf = 1000000000;
  vector<array<State, 2>> dp(n + 1);
  for (int node = n; node >= 1; --node) {
    dp[node] = {State{inf, 0}, State{inf, 0}};
    dp[node][marked[node]] = {0, 1};
    for (int child : children[node]) {
      array<State, 2> next{State{inf, 0}, State{inf, 0}};
      int childBest = min(dp[child][0].cost, dp[child][1].cost);
      int cutWays = 0;
      for (int state = 0; state <= 1; ++state) {
        if (dp[child][state].cost == childBest) {
          cutWays = (cutWays + dp[child][state].ways) % mod;
        }
      }
      for (int here = 0; here <= 1; ++here) {
        if (dp[node][here].cost == inf) continue;
        relax(next[here], dp[node][here].cost + childBest + 1,
              1LL * dp[node][here].ways * cutWays);
        for (int below = 0; below + here <= 1; ++below) {
          if (dp[child][below].cost == inf) continue;
          relax(next[here + below], dp[node][here].cost + dp[child][below].cost,
                1LL * dp[node][here].ways * dp[child][below].ways);
        }
      }
      dp[node] = next;
    }
  }
  int best = min(dp[1][0].cost, dp[1][1].cost);
  int ways = 0;
  for (int state = 0; state <= 1; ++state) {
    if (dp[1][state].cost == best) ways = (ways + dp[1][state].ways) % mod;
  }
  cout << best << ' ' << ways << '\n';
  return 0;
}
```

## 变种四：摄像头预算不足时最大化可区分组数

新定义：最多安装 $b$ 个摄像头，不要求区分所有坝点，最大化不同观测类别数并输出放置。
任意 $b$ 条边至多产生 $b+1$ 个组件，所以答案不超过 $\min(m,b+1)$。按深度从深到浅选择
至多 $m-1$ 个坝点的父边；每个被选坝点成为单坝组件，余下坝点留在一个组件，达到上界。
时间 $O(n+m\log m)$，空间 $O(n+m)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, budget;
  cin >> n >> budget;
  vector<int> depth(n + 1);
  for (int vertex = 2; vertex <= n; ++vertex) {
    int parent;
    cin >> parent;
    depth[vertex] = depth[parent] + 1;
  }
  int m;
  cin >> m;
  vector<int> dams(m);
  for (int& vertex : dams) cin >> vertex;
  sort(dams.begin(), dams.end(), [&](int a, int b) {
    if (depth[a] != depth[b]) return depth[a] > depth[b];
    return a < b;
  });
  int cameras = min(budget, m - 1);
  cout << cameras + 1 << '\n';
  cout << cameras;
  for (int i = 0; i < cameras; ++i) cout << ' ' << dams[i];
  cout << '\n';
  return 0;
}
```

## 来源

- [Codeforces 2257C 官方题面](https://codeforces.com/contest/2257/problem/C?locale=en)，核对于
  2026-08-20。
- [Codeforces 官方 API](https://codeforces.com/apiHelp)，用于比赛状态、分值、rating 缺失状态和
  标签核对，抓取于 2026-08-20。
- [Codeforces materials usage license v0.1](https://codeforces.com/page/254)。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/C?locale=en)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-515-q3-lc4026/">← [力扣竞赛] 第 515 场周赛 Q3 LC 4026 工位的最大间隔 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-20-lc3069/">[力扣每日一题] 2026-08-20｜LC 3069 将元素分配到两个数组中 I →</a>
</nav>
