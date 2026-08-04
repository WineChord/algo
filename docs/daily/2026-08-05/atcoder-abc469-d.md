---
title: "[atcoder] ABC469 D The Big Two"
---

# [atcoder] ABC469 D The Big Two

<p class="daily-archive-kicker">2026-08-05 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b99eca3e0d5b9a468e06f63c7e781b2a84286ded1cd221e035bc31152b5300cf -->
[Official problem: ABC469 D - The Big Two](https://atcoder.jp/contests/abc469/tasks/abc469_d?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 469。
- 题号与标题：D - The Big Two。
- 官方分值：400 分。
- 官方难度：AtCoder 未提供。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- AtCoder Problems 社区估算难度：1102，检索于 2026-08-05。

## Complete English statement

### D. The Big Two

There are $N$ players numbered $1,2,\ldots,N$. The game is played one-on-one. A tournament among these players was held $M$ times. In tournament $m$, players $A_m$ and $B_m$ reached the final.

Count the integer pairs $(x,y)$ satisfying both conditions:

1. $1\le x<y\le N$.
2. In every one of the $M$ tournaments, at least one of players $x$ and $y$ reached the final. Equivalently, for every $m$, at least one of $x,y$ belongs to $\{A_m,B_m\}$.

The input does not say that finalist pairs are distinct, so repeated pairs must be accepted.

### Input

```text
N M
A_1 B_1
A_2 B_2
⋮
A_M B_M
```

### Output

Print the number of valid pairs on one line.

### Constraints

- $2\le N\le2\times10^5$.
- $1\le M\le2\times10^5$.
- $1\le A_i<B_i\le N$.
- All input values are integers.

### Sample 1

```text
Input
5 5
1 2
3 4
1 3
2 3
2 5

Output
1
```

Only $(2,3)$ is valid. For example, $(1,4)$ fails on the fourth tournament because neither 1 nor 4 is one of its finalists 2 and 3.

### Sample 2

```text
Input
7 8
2 4
1 3
1 7
1 3
1 2
1 6
1 5
1 3

Output
2
```

The two valid pairs are $(1,2)$ and $(1,4)$.

### Sample 3

```text
Input
5 8
1 2
2 4
1 3
1 3
1 2
1 2
1 5
1 2

Output
2
```

There is no additional official explanation or required image for this sample.

来源说明：以上英文层由模型逐项阅读官方题面后独立组织，完整保留任务语义、输入输出、约束、样例与注释，不冒充逐字转载。核验入口为 [AtCoder 官方题面](https://atcoder.jp/contests/abc469/tasks/abc469_d?lang=en) 与 [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en)。

## 中文题意

把每名玩家看成顶点，把每场决赛的两名选手看成一条边。要统计多少个互异玩家对 `{x,y}` 能覆盖所有边：每条边至少有一个端点是 `x` 或 `y`。这正是统计大小恰为 2 的顶点覆盖，重边不会改变逻辑条件。

## 约束推导与观察

暴力枚举 $\binom N2$ 对玩家，再逐条检查 $M$ 场比赛，需要 $O(N^2M)$，远超 $2\times10^5$。

任取第一条边 `(a,b)`。任何合法二元覆盖都必须包含 `a` 或 `b`。固定必须包含某个玩家 `c` 后：

- 若所有边都与 `c` 相 incident，另一个玩家可以任取除 `c` 外的人。
- 否则，取第一条不含 `c` 的边 `(p,q)`。另一个玩家只能是 `p` 或 `q`，再分别扫描全部边验证。

因此只需两个分支和常数个候选。最大答案为 $\binom N2\approx2\times10^{10}$，必须使用 64 位。

## 解法递进

### 解法一：枚举所有玩家对

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  long long answer = 0;
  for (int x = 1; x <= n; ++x) {
    for (int y = x + 1; y <= n; ++y) {
      bool valid = true;
      for (auto [a, b] : edges) {
        valid &= a == x || b == x || a == y || b == y;
      }
      answer += valid;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N^2M)$，空间 $O(M)$，仅适合作为小规模 oracle。

### 最佳实用解：由第一条边分成两个固定端点分支

第二个分支排除 `a`，使两部分互斥，避免重复计算 `{a,b}`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool covers(int x, int y, const vector<pair<int, int>>& edges) {
  for (auto [a, b] : edges) {
    if (a != x && b != x && a != y && b != y) {
      return false;
    }
  }
  return true;
}
long long countContaining(int fixed, int excluded, int n, const vector<pair<int, int>>& edges) {
  pair<int, int> uncovered{-1, -1};
  for (auto edge : edges) {
    if (edge.first != fixed && edge.second != fixed) {
      uncovered = edge;
      break;
    }
  }
  if (uncovered.first == -1) {
    return n - 1 - (excluded != -1 && excluded != fixed);
  }
  long long answer = 0;
  for (int other : {uncovered.first, uncovered.second}) {
    if (other != fixed && other != excluded && covers(fixed, other, edges)) {
      ++answer;
    }
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  int a = edges[0].first;
  int b = edges[0].second;
  long long answer = countContaining(a, -1, n, edges) + countContaining(b, a, n, edges);
  cout << answer << '\n';
}
```

时间 $O(M)$，空间 $O(M)$。即使某分支允许任意第二人，也只用公式计数，不需要逐人扫描。

## 正确性证明

第一条边为 `{a,b}`，任意合法玩家对必须包含 `a` 或 `b`，所以两个分支覆盖全部答案。固定包含 `c` 后，若所有边都含 `c`，任意另一名不同玩家都能覆盖所有边；否则第一条不含 `c` 的边必须由另一名玩家覆盖，因此另一人只能是该边两个端点之一。逐边 `covers` 检查既不会接受非法候选，也不会漏掉合法候选。第二个分支显式排除 `a`，故两个分支互斥，和即为答案。

## 样例手推

样例 1 取第一条边 `{1,2}`。包含 1 的分支遇到不含 1 的边 `{3,4}`，只需尝试 3、4，均不能覆盖全部边；包含 2 且排除 1 的分支同样缩到第一条不含 2 的边端点，只有 3 通过，得到 `{2,3}`。样例 3 中重复边仍被逐条覆盖，不需去重。

## 易错点与方案比较

- 必须允许输入含重边。
- “所有边都含固定点”时贡献是 `N-1`，第二分支若排除另一端则是 `N-2`，不能只加 1。
- 答案使用 `long long`。
- 不要误建比赛淘汰树；题目只给决赛选手对。
- 常数次全边扫描比维护复杂度更高的度数与重边计数结构更稳，渐进复杂度已经最优。

## 变种一：输出全部合法玩家对

新定义：除数量外还要恢复每一对。候选生成完全相同；星形分支可能产生 $\Theta(N)$ 个答案，输出成本不可避免。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool valid(int x, int y, const vector<pair<int, int>>& edges) {
  for (auto [a, b] : edges) {
    if (a != x && b != x && a != y && b != y) {
      return false;
    }
  }
  return true;
}
void collect(int fixed, int n, const vector<pair<int, int>>& edges, set<pair<int, int>>& answer) {
  pair<int, int> uncovered{-1, -1};
  for (auto edge : edges) {
    if (edge.first != fixed && edge.second != fixed) {
      uncovered = edge;
      break;
    }
  }
  if (uncovered.first == -1) {
    for (int other = 1; other <= n; ++other) {
      if (other != fixed) {
        answer.insert(minmax(fixed, other));
      }
    }
    return;
  }
  for (int other : {uncovered.first, uncovered.second}) {
    if (valid(fixed, other, edges)) {
      answer.insert(minmax(fixed, other));
    }
  }
}
int main() {
  int n, m;
  cin >> n >> m;
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  set<pair<int, int>> answer;
  collect(edges[0].first, n, edges, answer);
  collect(edges[0].second, n, edges, answer);
  cout << answer.size() << '\n';
  for (auto [x, y] : answer) {
    cout << x << ' ' << y << '\n';
  }
}
```

时间 $O(M+N+答案数\log N)$，空间 $O(M+答案数)$。

## 变种二：每名玩家有代价，求最便宜的合法二元组

新定义：仍必须选恰好两名玩家，但目标改为最小总代价。生成所有可能候选，再按权重取最小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool valid(int x, int y, const vector<pair<int, int>>& edges) {
  return all_of(edges.begin(), edges.end(), [&](auto edge) {
    return edge.first == x || edge.second == x || edge.first == y || edge.second == y;
  });
}
void candidates(int fixed, int n, const vector<pair<int, int>>& edges, set<pair<int, int>>& out) {
  auto iterator = find_if(edges.begin(), edges.end(),
      [&](auto edge) { return edge.first != fixed && edge.second != fixed; });
  if (iterator == edges.end()) {
    for (int other = 1; other <= n; ++other) {
      if (other != fixed) {
        out.insert(minmax(fixed, other));
      }
    }
  } else {
    for (int other : {iterator->first, iterator->second}) {
      if (valid(fixed, other, edges)) {
        out.insert(minmax(fixed, other));
      }
    }
  }
}
int main() {
  int n, m;
  cin >> n >> m;
  vector<long long> cost(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> cost[i];
  }
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  set<pair<int, int>> possible;
  candidates(edges[0].first, n, edges, possible);
  candidates(edges[0].second, n, edges, possible);
  long long best = LLONG_MAX;
  pair<int, int> choice{-1, -1};
  for (auto pair : possible) {
    long long value = cost[pair.first] + cost[pair.second];
    if (value < best) {
      best = value;
      choice = pair;
    }
  }
  if (choice.first == -1) {
    cout << -1 << '\n';
  } else {
    cout << best << ' ' << choice.first << ' ' << choice.second << '\n';
  }
}
```

时间 $O(M+N)$ 加候选集合常数，空间 $O(M+N)$；不存在合法二人组时输出 `-1`。计数公式本身不再够用，因为必须比较每个可选搭档的代价。

## 变种三：判断是否存在大小至多为 `K` 的顶点覆盖

新定义：$K$ 很小。每次找一条尚未覆盖的边，任何解都必须选其一个端点，形成深度至多 `K` 的二叉搜索树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool searchCover(const vector<pair<int, int>>& edges, vector<char>& chosen, int remaining) {
  pair<int, int> uncovered{-1, -1};
  for (auto edge : edges) {
    if (!chosen[edge.first] && !chosen[edge.second]) {
      uncovered = edge;
      break;
    }
  }
  if (uncovered.first == -1) {
    return true;
  }
  if (remaining == 0) {
    return false;
  }
  for (int vertex : {uncovered.first, uncovered.second}) {
    chosen[vertex] = true;
    if (searchCover(edges, chosen, remaining - 1)) {
      return true;
    }
    chosen[vertex] = false;
  }
  return false;
}
int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  vector<char> chosen(n + 1);
  cout << (searchCover(edges, chosen, k) ? "YES" : "NO") << '\n';
}
```

时间 $O(2^K M)$，空间 $O(N+K)$。原题的 `K=2` 可进一步压成常数候选计数。

## 变种四：统计能单独覆盖全部比赛的玩家

新定义：只选一名玩家。第一条边仍给出唯二候选，逐边验证即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  cin >> n >> m;
  static_cast<void>(n);
  vector<pair<int, int>> edges(m);
  for (auto& [a, b] : edges) {
    cin >> a >> b;
  }
  int answer = 0;
  for (int candidate : {edges[0].first, edges[0].second}) {
    bool valid = all_of(edges.begin(), edges.end(),
        [&](auto edge) { return edge.first == candidate || edge.second == candidate; });
    answer += valid;
  }
  cout << answer << '\n';
}
```

时间 $O(M)$，空间 $O(M)$。大小为 1 时不再需要第二个端点分支。

## 验证说明

本轮将六段完整程序按 GNU++23 编译并跑全部官方样例。最佳解会与 $O(N^2M)$ oracle 对拍 50,000 个小规模随机多重图，覆盖 `N=2`、所有边相同、星形、两条不相交边、大量重边以及答案接近 $\binom N2$ 的情况。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_d?lang=en)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-101-lc69/">[力扣 Top 101] LC 69 x 的平方根 简单 →</a>
</nav>
