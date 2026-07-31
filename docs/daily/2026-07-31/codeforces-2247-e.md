---
title: "[codeforces] CF Round 1111 Div.2 E Build a Tree"
---

# [codeforces] CF Round 1111 Div.2 E Build a Tree

<p class="daily-archive-kicker">2026-07-31 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=7e7f1eb1b9f1dc41cc831ba4cbd1e2a1bd34020012a75e814e0554eb2dddad1c -->
## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1111 (Div. 2)。
- Contest ID：2247。
- 题号与标题：Div.2 E - Build a Tree。
- 官方 points：3000。
- 官方 rating：未知（官方 API 未提供）。
- 官方 tags：`constructive algorithms`、`trees`、`two pointers`。
- 时间限制：2 秒。
- 内存限制：256 MB。
- 官方题面：[Codeforces 2247E - Build a Tree](https://codeforces.com/contest/2247/problem/E)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)。

下方英文题面层按 Codeforces 材料许可在公开、非判题用途下呈现，并保留来源与官方直达链接。这里不复制隐藏测试、生成器、checker、validator 或其他未公开判题材料。官方页面提示题面近期有过修改，本页依据 2026-07-31 核对到的当前版本。

## Complete English statement

### E. Build a Tree

**Time limit per test:** 2 seconds

**Memory limit per test:** 256 megabytes

**Input:** standard input

**Output:** standard output

You are given two integers $n$ and $k$.

Construct a tree with $n$ vertices such that

$$
\sum_{i=1}^{n}\operatorname{dist}\bigl(i,(i\bmod n)+1\bigr)=k,
$$

or determine that no such tree exists.

A tree is a connected graph without cycles. $\operatorname{dist}(i,j)$ is the number of edges on the shortest path from vertex $i$ to vertex $j$ in the tree.

### Input and Complete Constraints

Each test contains multiple test cases. The first line contains the number of test cases $t$:

$$
1\le t\le10^4.
$$

The only line of each test case contains two integers $n$ and $k$:

$$
2\le n\le2\times10^5,\qquad0\le k\le n^2.
$$

The sum of $n$ over all test cases does not exceed $2\times10^5$.

### Output

For each test case, if no solution exists, output `-1`.

Otherwise, output $n-1$ lines. Each line contains two integers $u$ and $v$ $(1\le u,v\le n)$, denoting an edge of the tree. The edges may be output in any order. If multiple trees are suitable, output any of them.

### Official Sample

```text
Input
5
2 2
4 6
5 10
5 14
100 8347
```

```text
Output
1 2
1 4
1 3
1 2
3 2
3 4
4 1
5 3
-1
-1
```

For the first test case, the tree consists of the single edge $(1,2)$, so

$$
\operatorname{dist}(1,2)+\operatorname{dist}(2,1)=1+1=2.
$$

For the second test case, the shown tree is a star centered at vertex 1 with leaves 2, 3, and 4. The four cyclic distances are $1,2,2,1$, whose sum is 6.

For the fourth test case, no suitable tree exists. The official statement gives no additional explanation for the third and fifth test cases.

## 中文题意

构造一棵标号为 $1,\ldots,n$ 的树，使按循环顺序

$$
1\to2\to\cdots\to n\to1
$$

访问相邻标号时的树上距离总和恰为 $k$。若无法做到，输出 `-1`。

## 约束推导与可行区间

这个访问序列是一条回到起点的闭合巡游。删除任意树边后会形成两个非空连通块；巡游进入另一侧后必须再次跨边返回，所以每条树边被跨越正偶数次。树有 $n-1$ 条边，因此

$$
k\equiv0\pmod2,\qquad k\ge2(n-1).
$$

取树的一个重心为根。每棵根子树大小不超过 $\lfloor n/2\rfloor$。任意两点距离不超过二者深度之和，而循环中每个顶点恰出现在两个距离项中，所以

$$
k\le2\sum_v depth(v).
$$

大小为 $s$ 的根子树，其深度和最多为 $1+\cdots+s$，由一条链取等。凸性要求把 $n-1$ 个非根顶点尽量集中到两个受限子树中，得到

$$
k\le\left\lfloor\frac{n^2}{2}\right\rfloor.
$$

最终可行的充要条件是

$$
k\text{ 为偶数},\qquad
2(n-1)\le k\le\left\lfloor\frac{n^2}{2}\right\rfloor.
$$

## 解法递进

### 解法一：枚举 Prüfer 序列

当 $n$ 很小时，可枚举长度 $n-2$ 的所有 Prüfer 序列，解码每棵标号树，再用 BFS 计算循环距离和。它覆盖全部 $n^{n-2}$ 棵树，可作构造的穷举 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long evaluate(const vector<pair<int, int>>& edges, int n) {
  vector<vector<int>> graph(n + 1);
  for (auto [u, v] : edges) {
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  long long answer = 0;
  for (int source = 1; source <= n; ++source) {
    int target = source == n ? 1 : source + 1;
    vector<int> distance(n + 1, -1);
    queue<int> q;
    q.push(source);
    distance[source] = 0;
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      for (int v : graph[u]) {
        if (distance[v] == -1) {
          distance[v] = distance[u] + 1;
          q.push(v);
        }
      }
    }
    answer += distance[target];
  }
  return answer;
}
vector<pair<int, int>> decode(const vector<int>& code, int n) {
  vector<int> degree(n + 1, 1);
  for (int value : code) {
    ++degree[value];
  }
  priority_queue<int, vector<int>, greater<int>> leaves;
  for (int i = 1; i <= n; ++i) {
    if (degree[i] == 1) {
      leaves.push(i);
    }
  }
  vector<pair<int, int>> edges;
  for (int value : code) {
    int leaf = leaves.top();
    leaves.pop();
    edges.push_back({leaf, value});
    if (--degree[value] == 1) {
      leaves.push(value);
    }
  }
  int u = leaves.top();
  leaves.pop();
  edges.push_back({u, leaves.top()});
  return edges;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long target;
  cin >> n >> target;
  if (n > 8) {
    cout << -1 << '\n';
    return 0;
  }
  vector<int> code(max(0, n - 2), 1);
  bool found = false;
  function<void(int)> search = [&](int index) {
    if (found) {
      return;
    }
    if (index == n - 2) {
      auto edges = decode(code, n);
      if (evaluate(edges, n) == target) {
        found = true;
        for (auto [u, v] : edges) {
          cout << u << ' ' << v << '\n';
        }
      }
      return;
    }
    for (int value = 1; value <= n; ++value) {
      code[index] = value;
      search(index + 1);
    }
  };
  search(0);
  if (!found) {
    cout << -1 << '\n';
  }
}
```

时间 $O(n^{n-2}\cdot n^2)$，只适合 $n\le8$。

### 最佳实用解：奇偶分组与可控深度

把顶点 1 作为根，偶数标号放入一棵根子树，奇数标号 $3,5,\ldots$ 放入另一棵。自然标号中的连续非根顶点总在不同子树，故它们的路径经过根：

$$
\operatorname{dist}(i,i+1)=depth(i)+depth(i+1).
$$

首尾两项涉及根也满足同一式子，所以总和等于所有非根深度和的两倍。令目标深度和为 $S=k/2$，相对星形树还需增加

$$
extra=S-(n-1).
$$

对一组顶点维护当前最深路径。加入新顶点时，让它连接深度为 $d$ 的节点，便比直接连根多贡献 $d$；贪心取 $d=\min(extra,\text{当前路径长度})$，即可逐个消耗从 0 到该组最大增量的每个整数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
void buildGroup(const vector<int>& vertices, int64& extra, vector<pair<int, int>>& edges) {
  vector<int> path;
  for (int vertex : vertices) {
    int depth = min<int64>(extra, path.size());
    edges.push_back({depth == 0 ? 1 : path[depth - 1], vertex});
    extra -= depth;
    if (depth == static_cast<int>(path.size())) {
      path.push_back(vertex);
    }
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    int64 k;
    cin >> n >> k;
    int64 minimum = 2LL * (n - 1);
    int64 maximum = 1LL * n * n / 2;
    if (k % 2 || k < minimum || k > maximum) {
      cout << -1 << '\n';
      continue;
    }
    vector<int> even;
    vector<int> odd;
    for (int vertex = 2; vertex <= n; ++vertex) {
      (vertex % 2 == 0 ? even : odd).push_back(vertex);
    }
    int64 extra = k / 2 - (n - 1);
    vector<pair<int, int>> edges;
    buildGroup(even, extra, edges);
    buildGroup(odd, extra, edges);
    for (auto [u, v] : edges) {
      cout << u << ' ' << v << '\n';
    }
  }
}
```

总时间 $O(\sum n)$，额外空间 $O(n)$。`k` 与 $n^2$ 必须使用 `long long`。

## 正确性证明

两组大小分别为 $\lceil(n-1)/2\rceil$ 与 $\lfloor(n-1)/2\rfloor$，均不超过 $\lfloor n/2\rfloor$。一组含 $s$ 个顶点时，贪心依次可消费额外深度 $0,1,\ldots,s-1$；若剩余 `extra` 小于当前路径长度，就一次恰好消费剩余值。故该组能实现从 0 到 $s(s-1)/2$ 的每个整数增量，两组串联覆盖整个可行区间。

每条输出边都把新顶点接到已存在的根或路径节点，因此始终连通且无环，共输出 $n-1$ 条边，结果是树。连续非根标号奇偶交替，必属不同根子树，距离等于深度和；根到 2 与 $n$ 到根也成立。每个非根顶点深度恰被计算两次，最终距离和为 $2S=k$。

## 样例与边界

- $n=2$ 时唯一可行值为 2。
- $k=2(n-1)$ 时 `extra=0`，输出以 1 为中心的星形树。
- $k=\lfloor n^2/2\rfloor$ 时，两组都尽量延成长链。
- $n=5,k=14$ 超过上界 12；$n=100,k=8347$ 既为奇数又超过上界 5000。
- 只检查偶性不够，两个边界同样是必要条件。

## 易错点与方案比较

- 目标包含 $n\to1$，是闭合循环，不是普通路径。
- 官方样例输出最后有两个 `-1`，分别对应第 4、5 组。
- 上界应写成 `1LL*n*n/2`，避免 `int` 乘法溢出。
- 构造时两组内部可形成链，但连续标号必须落在不同组。
- Prüfer 枚举只用于小规模验证；线性构造证明短、常数小，推荐记忆“距离和变深度和 + 奇偶交替标签”。

## 变种一：只判断可行性并统计可行值个数

新定义：不输出树，只判断给定 $k$，并输出固定 $n$ 下可行的不同 $k$ 数量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long n;
  int queries;
  cin >> n >> queries;
  long long low = 2 * (n - 1);
  long long high = n * n / 2;
  cout << (high - low) / 2 + 1 << '\n';
  while (queries--) {
    long long k;
    cin >> k;
    cout << (k % 2 == 0 && low <= k && k <= high ? "YES\n" : "NO\n");
  }
}
```

预处理 $O(1)$，每次询问 $O(1)$。

## 变种二：访问顺序改为任意给定排列

新定义：给定循环访问排列 $p_1,\ldots,p_n$。以 $p_1$ 为根，按排列位置奇偶把其余顶点分组，构造完全相同。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
void build(const vector<int>& vertices, int root, int64& extra, vector<pair<int, int>>& edges) {
  vector<int> path;
  for (int vertex : vertices) {
    int depth = min<int64>(extra, path.size());
    edges.push_back({depth == 0 ? root : path[depth - 1], vertex});
    extra -= depth;
    if (depth == static_cast<int>(path.size())) {
      path.push_back(vertex);
    }
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int64 k;
  cin >> n >> k;
  vector<int> order(n);
  for (int& vertex : order) {
    cin >> vertex;
  }
  if (k % 2 || k < 2LL * (n - 1) || k > 1LL * n * n / 2) {
    cout << -1 << '\n';
    return 0;
  }
  vector<int> first;
  vector<int> second;
  for (int i = 1; i < n; ++i) {
    (i % 2 ? first : second).push_back(order[i]);
  }
  int64 extra = k / 2 - (n - 1);
  vector<pair<int, int>> edges;
  build(first, order[0], extra, edges);
  build(second, order[0], extra, edges);
  for (auto [u, v] : edges) {
    cout << u << ' ' << v << '\n';
  }
}
```

时间与空间均为 $O(n)$。

## 变种三：限制树相对根的最大高度

新定义：所有顶点到根 1 的距离不得超过 $H$。一组大小为 $s$ 时最大深度和为

$$
F(s,H)=T_{\min(s,H)}+\max(0,s-H)H.
$$

构造时把可选父节点深度限制为 $H-1$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
int64 capacity(int size, int height) {
  int path = min(size, height);
  return 1LL * path * (path + 1) / 2 + 1LL * (size - path) * height;
}
void build(const vector<int>& vertices, int height, int64& extra, vector<pair<int, int>>& edges) {
  vector<int> path;
  for (int vertex : vertices) {
    int cap = min<int>(path.size(), max(0, height - 1));
    int depth = min<int64>(extra, cap);
    edges.push_back({depth == 0 ? 1 : path[depth - 1], vertex});
    extra -= depth;
    if (depth == static_cast<int>(path.size()) && static_cast<int>(path.size()) < height) {
      path.push_back(vertex);
    }
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, height;
  int64 k;
  cin >> n >> k >> height;
  vector<int> even;
  vector<int> odd;
  for (int vertex = 2; vertex <= n; ++vertex) {
    (vertex % 2 == 0 ? even : odd).push_back(vertex);
  }
  int64 low = 2LL * (n - 1);
  int64 high = 2 * (capacity(even.size(), height) + capacity(odd.size(), height));
  if (height < 1 || k % 2 || k < low || k > high) {
    cout << -1 << '\n';
    return 0;
  }
  int64 extra = k / 2 - (n - 1);
  vector<pair<int, int>> edges;
  build(even, height, extra, edges);
  build(odd, height, extra, edges);
  for (auto [u, v] : edges) {
    cout << u << ' ' << v << '\n';
  }
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种四：给定树，计算循环距离和

新定义：输入一棵树，直接求当前自然标号顺序对应的 $k$。倍增 LCA 后逐对计算距离。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<int>> graph(n + 1);
  for (int i = 1; i < n; ++i) {
    int u, v;
    cin >> u >> v;
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  int log = 1;
  while ((1 << log) <= n) {
    ++log;
  }
  vector<vector<int>> up(log, vector<int>(n + 1));
  vector<int> depth(n + 1);
  queue<int> q;
  q.push(1);
  up[0][1] = 1;
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (int v : graph[u]) {
      if (v != up[0][u]) {
        up[0][v] = u;
        depth[v] = depth[u] + 1;
        q.push(v);
      }
    }
  }
  for (int bit = 1; bit < log; ++bit) {
    for (int v = 1; v <= n; ++v) {
      up[bit][v] = up[bit - 1][up[bit - 1][v]];
    }
  }
  auto lca = [&](int u, int v) {
    if (depth[u] < depth[v]) {
      swap(u, v);
    }
    int difference = depth[u] - depth[v];
    for (int bit = 0; bit < log; ++bit) {
      if (difference >> bit & 1) {
        u = up[bit][u];
      }
    }
    if (u == v) {
      return u;
    }
    for (int bit = log - 1; bit >= 0; --bit) {
      if (up[bit][u] != up[bit][v]) {
        u = up[bit][u];
        v = up[bit][v];
      }
    }
    return up[0][u];
  };
  long long answer = 0;
  for (int u = 1; u <= n; ++u) {
    int v = u == n ? 1 : u + 1;
    int ancestor = lca(u, v);
    answer += depth[u] + depth[v] - 2 * depth[ancestor];
  }
  cout << answer << '\n';
}
```

预处理 $O(n\log n)$，计算 $O(n\log n)$，空间 $O(n\log n)$。

## 可复现验证

- 对 $2\le n\le40$ 的每个 $0\le k\le n^2$，构造结果恰在充要区间内存在；逐棵检查边数、连通性、无环性和实际距离和。
- 对 $2\le n\le7$ 穷举全部 Prüfer 序列，所得可行值与连续偶数区间完全一致。
- 所有完整代码按 GNU++23 编译。

## Reference

- [Codeforces 官方题面](https://codeforces.com/contest/2247/problem/E)
- [Codeforces Round 1111 官方题解](https://codeforces.com/blog/entry/155337)
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://codeforces.com/contest/2247/problem/E)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-512-q2-lc4001/">← [力扣竞赛] 第 512 场周赛 Q2 LC 4001 聚合两个时间序列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-31-lc3016/">[力扣每日一题] 2026-07-31｜LC 3016 输入单词需要的最少按键次数 II →</a>
</nav>
