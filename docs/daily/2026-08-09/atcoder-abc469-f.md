---
title: "[atcoder] ABC469 F GCD Maximum Spanning Tree"
---

# [atcoder] ABC469 F GCD Maximum Spanning Tree

<p class="daily-archive-kicker">2026-08-09 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d698a2b2ff2de2eb17f6ecdf06481dee0e781ad37237e25b49bac3d33c3b1976 -->
[Official problem: ABC469 F - GCD Maximum Spanning Tree](https://atcoder.jp/contests/abc469/tasks/abc469_f?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 469。
- 题号与标题：F - GCD Maximum Spanning Tree。
- 官方分值：500 分；官方未标注难度。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒；内存限制：1024 MiB。
- AtCoder Problems 社区估算难度：1567，检索于 2026-08-09。

## Complete English statement

### F. GCD Maximum Spanning Tree

You are given a sequence of $N$ positive integers $A_1,A_2,\ldots,A_N$.

Consider the complete undirected graph whose vertices are numbered $1,2,\ldots,N$. For every pair $1\le i<j\le N$, the edge joining vertices $i$ and $j$ has weight

$$
\gcd(A_i,A_j).
$$

Among all spanning trees of this graph, find the maximum possible sum of edge weights.

### Input

```text
N
A_1 A_2 ... A_N
```

### Output

Print the maximum total edge weight of a spanning tree.

### Constraints

- $2\le N\le2\times10^5$.
- $1\le A_1<A_2<\cdots<A_N\le10^6$.
- Every input value is an integer.

### Sample 1

```text
Input
3
4 6 12

Output
10
```

The complete graph has edges of weights $2$ between vertices 1 and 2, $4$ between vertices 1 and 3, and $6$ between vertices 2 and 3. Choosing the latter two edges gives the maximum sum $10$.

### Sample 2

```text
Input
5
5 14 15 21 42

Output
43
```

### Sample 3

```text
Input
2
1 1000000

Output
1
```

There is no additional official note or required image. The English layer above is independently organized from the official statement while preserving the complete task semantics, input, output, constraints, samples, and official explanation. See the [AtCoder statement](https://atcoder.jp/contests/abc469/tasks/abc469_f?lang=en) and [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en).

## 中文题意

把每个数看成一个顶点，任意两点间边权为两数的最大公约数。这个图有 $\Theta(N^2)$ 条隐式边；要求最大生成树的总权值，不能显式建图。

## 约束推导与观察

最大生成树 Kruskal 需要按边权从大到小处理。边权只可能是 $1..M$ 中的整数，其中 $M=\max A_i\le10^6$。对固定 $d$，所有能被 $d$ 整除的输入值形成集合 $S_d$；任意两点的 gcd 至少含因子 $d$。从 $M$ 降序枚举 $d$，把 $S_d$ 当前不同 DSU 分量连起来，就等价于处理 gcd 恰为 $d$ 的边权层。

答案上界小于 $(N-1)10^6<2\times10^{11}$，必须使用 64 位整数。倍数枚举次数为

$$
\sum_{d=1}^{M}\left\lfloor\frac Md\right\rfloor=O(M\log M).
$$

## 解法递进

### 解法一：显式构造完全图再跑 Kruskal

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent, size;
  explicit DSU(int n) : parent(n), size(n, 1) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return false;
    }
    if (size[a] < size[b]) {
      swap(a, b);
    }
    parent[b] = a;
    size[a] += size[b];
    return true;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  vector<tuple<int, int, int>> edges;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      edges.push_back({gcd(a[i], a[j]), i, j});
    }
  }
  sort(edges.rbegin(), edges.rend());
  DSU dsu(n);
  long long answer = 0;
  for (auto [weight, u, v] : edges) {
    if (dsu.unite(u, v)) {
      answer += weight;
    }
  }
  cout << answer << '\n';
}
```

边数 $O(N^2)$，时间 $O(N^2\log N)$、空间 $O(N^2)$，只能用于小规模 oracle。

### 解法二：为实际约数建立顶点桶

先用最小质因子分解每个输入值并枚举其全部约数，把顶点放入对应约数桶；再按约数从大到小连接桶内顶点。这避免遍历没有任何输入倍数的位置，但需要保存所有“顶点—约数”关系。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent, size;
  explicit DSU(int n) : parent(n), size(n, 1) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return false;
    }
    if (size[a] < size[b]) {
      swap(a, b);
    }
    parent[b] = a;
    size[a] += size[b];
    return true;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  int maximum = a.back();
  vector<int> smallest(maximum + 1);
  for (int i = 2; i <= maximum; ++i) {
    if (smallest[i] == 0) {
      for (int multiple = i; multiple <= maximum; multiple += i) {
        if (smallest[multiple] == 0) {
          smallest[multiple] = i;
        }
      }
    }
  }
  vector<vector<int>> bucket(maximum + 1);
  for (int vertex = 0; vertex < n; ++vertex) {
    int value = a[vertex];
    vector<pair<int, int>> factors;
    while (value > 1) {
      int prime = smallest[value];
      int exponent = 0;
      while (value % prime == 0) {
        value /= prime;
        ++exponent;
      }
      factors.push_back({prime, exponent});
    }
    vector<int> divisors{1};
    for (auto [prime, exponent] : factors) {
      int oldSize = divisors.size();
      int power = 1;
      for (int e = 1; e <= exponent; ++e) {
        power *= prime;
        for (int i = 0; i < oldSize; ++i) {
          divisors.push_back(divisors[i] * power);
        }
      }
    }
    for (int divisor : divisors) {
      bucket[divisor].push_back(vertex);
    }
  }
  DSU dsu(n);
  long long answer = 0;
  for (int divisor = maximum; divisor >= 1; --divisor) {
    if (bucket[divisor].empty()) {
      continue;
    }
    int anchor = bucket[divisor][0];
    for (int vertex : bucket[divisor]) {
      if (dsu.unite(anchor, vertex)) {
        answer += divisor;
      }
    }
  }
  cout << answer << '\n';
}
```

设 $S=\sum_i\tau(A_i)$，时间 $O(M\log\log M+S\alpha(N)+M)$、空间 $O(M+S)$。它适合实际约数很少的稀疏情况，但存储成本高于最终方案。

### 最佳实用解：筛倍数 + DSU

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent, size;
  explicit DSU(int n) : parent(n), size(n, 1) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return false;
    }
    if (size[a] < size[b]) {
      swap(a, b);
    }
    parent[b] = a;
    size[a] += size[b];
    return true;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  int maximum = 0;
  for (int& x : a) {
    cin >> x;
    maximum = max(maximum, x);
  }
  vector<int> vertexAt(maximum + 1, -1);
  for (int i = 0; i < n; ++i) {
    vertexAt[a[i]] = i;
  }
  DSU dsu(n);
  long long answer = 0;
  int chosenEdges = 0;
  for (int divisor = maximum; divisor >= 1; --divisor) {
    int anchor = -1;
    for (int multiple = divisor; multiple <= maximum; multiple += divisor) {
      int vertex = vertexAt[multiple];
      if (vertex == -1) {
        continue;
      }
      if (anchor == -1) {
        anchor = vertex;
      } else if (dsu.unite(anchor, vertex)) {
        answer += divisor;
        ++chosenEdges;
      }
    }
  }
  assert(chosenEdges == n - 1);
  cout << answer << '\n';
}
```

时间 $O(M\log M\,\alpha(N))$，空间 $O(M+N)$。连续数组、倍数筛和 DSU 常数稳定，适合 2 秒限制，是推荐方案。

## 正确性证明

按 `divisor` 降序处理前，所有权重大于当前值的边层已经完成。考虑 $S_d$ 中两个当前不同 DSU 分量。它们任取顶点的 gcd 是 $d$ 的倍数；若某对顶点 gcd 严格大于 $d$，那么它们在此前对应的更大 gcd 层已经同属一个集合，矛盾。因此当前不同分量之间实际存在权重恰为 $d$ 的边，而且这些分量在权重 $d$ 的商图上构成完全图。

用一个锚点依次连接 $S_d$ 中不同 DSU 分量，恰选取把这些分量连成树所需的安全边，与降序 Kruskal 在该权值层的效果一致。到 $d=1$ 时所有正整数都在 $S_1$，最终一定有 $N-1$ 次成功合并。由 Kruskal 定理，所得权值和为最大生成树权值。

## 样例手推

`[4,6,12]`：处理 $d=6$ 时连接 6 与 12，加入 6；处理 $d=4$ 时连接 4 与 12，加入 4；此时已有两条边，总和 10。到 $d=2$ 虽三数都是 2 的倍数，但已在同一分量，不再加边。

## 易错点与方案比较

- 不能写成“gcd 不小于 $d$ 当且仅当两数都是 $d$ 的倍数”；正确关系是“共同被 $d$ 整除”。
- `vertexAt` 单值映射依赖严格递增约束；重复值版本必须分组。
- 成功合并时加入当前 `divisor`，证明保证跨分量实际边权恰为它。
- 答案使用 `long long`；成功边数应恰为 $N-1$。

## 变种一：恢复一棵具体最大生成树

每次 DSU 合并成功时记录锚点与当前顶点，最终得到 $N-1$ 条真实边。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> p, size;
  explicit DSU(int n) : p(n), size(n, 1) {
    iota(p.begin(), p.end(), 0);
  }
  int find(int x) {
    return p[x] == x ? x : p[x] = find(p[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return false;
    }
    if (size[a] < size[b]) {
      swap(a, b);
    }
    p[b] = a;
    size[a] += size[b];
    return true;
  }
};
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  int maximum = 0;
  for (int& x : a) {
    cin >> x;
    maximum = max(maximum, x);
  }
  vector<int> at(maximum + 1, -1);
  for (int i = 0; i < n; ++i) {
    at[a[i]] = i;
  }
  DSU dsu(n);
  vector<tuple<int, int, int>> tree;
  for (int d = maximum; d >= 1; --d) {
    int anchor = -1;
    for (int x = d; x <= maximum; x += d) {
      if (at[x] == -1) {
        continue;
      }
      if (anchor == -1) {
        anchor = at[x];
      } else if (dsu.unite(anchor, at[x])) {
        tree.push_back({anchor + 1, at[x] + 1, d});
      }
    }
  }
  for (auto [u, v, weight] : tree) {
    cout << u << ' ' << v << ' ' << weight << '\n';
  }
}
```

复杂度不变，输出空间 $O(N)$。

## 变种二：输入值允许重复

同值 $x$ 的顶点间边权为 $x$，先把每组用 $count[x]-1$ 条权重 $x$ 的边连接，再让一个代表参加倍数筛。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> p;
  explicit DSU(int n) : p(n, -1) {
  }
  int find(int x) {
    return p[x] < 0 ? x : p[x] = find(p[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return false;
    }
    if (p[a] > p[b]) {
      swap(a, b);
    }
    p[a] += p[b];
    p[b] = a;
    return true;
  }
};
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  int maximum = 0;
  vector<vector<int>> group(1000001);
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
    maximum = max(maximum, a[i]);
    group[a[i]].push_back(i);
  }
  DSU dsu(n);
  vector<int> representative(maximum + 1, -1);
  long long answer = 0;
  for (int value = 1; value <= maximum; ++value) {
    if (group[value].empty()) {
      continue;
    }
    representative[value] = group[value][0];
    for (int i = 1; i < static_cast<int>(group[value].size()); ++i) {
      dsu.unite(group[value][0], group[value][i]);
      answer += value;
    }
  }
  for (int d = maximum; d >= 1; --d) {
    int anchor = -1;
    for (int x = d; x <= maximum; x += d) {
      if (representative[x] == -1) {
        continue;
      }
      if (anchor == -1) {
        anchor = representative[x];
      } else if (dsu.unite(anchor, representative[x])) {
        answer += d;
      }
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N+M\log M\,\alpha(N))$，空间 $O(N+M)$。

## 变种三：数值上界极大，不能扫描到 `M`

对每个值分解质因数并枚举全部约数，建立只含实际出现约数的哈希桶，再按约数降序处理。这里用试除展示接口，适合 $N$ 较小或有快速分解器时。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> divisors(long long value) {
  vector<pair<long long, int>> factors;
  for (long long p = 2; p * p <= value; ++p) {
    if (value % p != 0) {
      continue;
    }
    int exponent = 0;
    while (value % p == 0) {
      value /= p;
      ++exponent;
    }
    factors.push_back({p, exponent});
  }
  if (value > 1) {
    factors.push_back({value, 1});
  }
  vector<long long> result{1};
  for (auto [p, exponent] : factors) {
    int oldSize = result.size();
    long long power = 1;
    for (int e = 1; e <= exponent; ++e) {
      power *= p;
      for (int i = 0; i < oldSize; ++i) {
        result.push_back(result[i] * power);
      }
    }
  }
  return result;
}
int main() {
  int n;
  cin >> n;
  vector<long long> a(n);
  map<long long, vector<int>, greater<long long>> bucket;
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
    for (long long d : divisors(a[i])) {
      bucket[d].push_back(i);
    }
  }
  vector<int> parent(n, -1);
  auto find = [&](auto&& self, int x) -> int {
    return parent[x] < 0 ? x : parent[x] = self(self, parent[x]);
  };
  long long answer = 0;
  for (auto& [d, vertices] : bucket) {
    int anchor = vertices[0];
    for (int vertex : vertices) {
      int x = find(find, anchor);
      int y = find(find, vertex);
      if (x != y) {
        if (parent[x] > parent[y]) {
          swap(x, y);
        }
        parent[x] += parent[y];
        parent[y] = x;
        answer += d;
      }
    }
  }
  cout << answer << '\n';
}
```

若 $S=\sum_i\tau(A_i)$，主体时间 $O(S\log S+S\alpha(N))$、空间 $O(S)$，另加因数分解成本。

## 变种四：边权改为 `f(gcd)`

若 `f` 单调不减，gcd 的降序仍与边权降序一致；成功合并时加入 `f(d)`。下面示例取 $f(d)=d^2$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  int maximum = 0;
  for (int& x : a) {
    cin >> x;
    maximum = max(maximum, x);
  }
  vector<int> at(maximum + 1, -1), parent(n, -1);
  for (int i = 0; i < n; ++i) {
    at[a[i]] = i;
  }
  auto find = [&](auto&& self, int x) -> int {
    return parent[x] < 0 ? x : parent[x] = self(self, parent[x]);
  };
  long long answer = 0;
  for (int d = maximum; d >= 1; --d) {
    int anchor = -1;
    for (int x = d; x <= maximum; x += d) {
      if (at[x] == -1) {
        continue;
      }
      if (anchor == -1) {
        anchor = at[x];
        continue;
      }
      int u = find(find, anchor);
      int v = find(find, at[x]);
      if (u != v) {
        if (parent[u] > parent[v]) {
          swap(u, v);
        }
        parent[u] += parent[v];
        parent[v] = u;
        answer += 1LL * d * d;
      }
    }
  }
  cout << answer << '\n';
}
```

复杂度不变。若 `f` 非单调，按 `d` 降序不再等于按真实边权降序，原证明失效。

## 可复现验证

官方三组样例全部通过。另对 $N=2..10$、数值范围 `1..60` 的 27,000 组随机互异序列，以完整图显式 Kruskal 为 oracle，与筛倍数算法逐组对拍，结果全部一致。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_f?lang=en)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-121-lc238/">[力扣 Top 121] LC 238 除了自身以外数组的乘积 中等 →</a>
</nav>
