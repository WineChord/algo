---
title: "[atcoder] ARC226 A Meeting Division"
---

# [atcoder] ARC226 A Meeting Division

<p class="daily-archive-kicker">2026-08-12 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-12 题目列表</a> · <a href="../../../graph/weighted-parity-states/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=86995098e59773ba5f81fdae7fdbf55a04d5872657e64cfc989f7c37b4d3aa0a -->
[Official problem: ARC226 A - Meeting Division](https://atcoder.jp/contests/arc226/tasks/arc226_a?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 226。
- 题目：A - Meeting Division；官方分值 400。
- 时间限制：2 秒；内存限制：1024 MiB。
- 官方链接：[ARC226 A](https://atcoder.jp/contests/arc226/tasks/arc226_a?lang=en)。
- 下方英文层是模型独立组织的自包含呈现，官方页面与 [AtCoder 服务条款](https://atcoder.jp/tos)仍是权威来源；本页不主张题目存在专属开放转载许可。

## Complete English statement

### Task

There are $N$ meetings, numbered from $1$ through $N$. Meeting $i$ starts at time $S_i$ and ends at time $T_i$.

Every meeting must be assigned to exactly one of Takahashi and Aoki. One person must not be responsible for two meetings whose time intervals overlap for a positive amount of time. Equivalently, one person may handle both meetings $i$ and $j$ only when $T_i\le S_j$ or $T_j\le S_i$.

Count the valid assignments and print the count modulo $998244353$.

### Input

```text
N
S_1 T_1
S_2 T_2
...
S_N T_N
```

### Output

Print the number of valid assignments modulo $998244353$.

### Constraints

- $1\le N\le3\times10^5$.
- $1\le S_i<T_i\le2N$.
- The $2N$ values $S_1,T_1,S_2,T_2,\ldots,S_N,T_N$ are pairwise distinct.
- Every input value is an integer.

### Sample 1

```text
3
1 3
2 4
5 6
```

```text
4
```

The four assignments are obtained by giving meetings $1$ and $3$ to either person and meeting $2$ to the other, or by giving meetings $2$ and $3$ to either person and meeting $1$ to the other.

### Sample 2

```text
3
1 4
2 5
3 6
```

```text
0
```

All three meetings overlap during a positive-length interval, so two people cannot cover them.

The official statement contains no task-essential image and no additional note. The official score is 400 points; the limits are 2 seconds and 1024 MiB. AtCoder does not attach an official difficulty rating to the task.

## 中文题意

把每场会议交给高桥或青木中的恰好一人。同一个人负责的任意两场会议不能有正长度重叠；端点相接本来允许，但本题所有端点互异。求合法二着色方案数，模 $998244353$。

## 约束推导与关键观察

共有 $2N$ 个互异端点，且每个端点都在恰有 $2N$ 个整数的集合 $[1,2N]$ 中，所以端点实际恰好是 $1,2,\ldots,2N$ 的一个排列。我们可以直接建立事件数组，无需排序。

区间图中，两个会议重叠就连边，负责人就是两种颜色。若某时刻同时存在三场会议，它们两两重叠，形成三角形，必定无解。反过来，若扫描深度始终不超过 2，新会议开始时至多只有一场旧会议仍在进行：没有旧会议时任选负责人，恰有一场时选另一人，就能满足全部约束。

每当开始事件到来前活动会议数为 0，就开启一个新的连通分量。每个连通二分图分量有两种整体翻色方案，因此答案为 $2^C$，其中 $C$ 是这样的开始次数。

## 解法递进

### 解法一：枚举全部负责人分配

枚举 $2^N$ 个二进制分配，再逐对检查同色区间是否重叠。它直接覆盖定义，是小规模验证 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> s(n), t(n);
  for (int i = 0; i < n; ++i) cin >> s[i] >> t[i];
  long long answer = 0;
  for (int mask = 0; mask < (1 << n); ++mask) {
    bool valid = true;
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        bool same = ((mask >> i) & 1) == ((mask >> j) & 1);
        bool overlap = max(s[i], s[j]) < min(t[i], t[j]);
        if (same && overlap) valid = false;
      }
    }
    answer += valid;
  }
  cout << answer << '\n';
}
```

时间 $O(2^N N^2)$，空间 $O(N)$。

### 解法二：显式建立区间图并二着色

为每对重叠会议连边，BFS 检查二分图并统计连通分量。若出现同色边输出 0，否则输出 $2^C$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  int n;
  cin >> n;
  vector<int> s(n), t(n);
  for (int i = 0; i < n; ++i) cin >> s[i] >> t[i];
  vector<vector<int>> graph(n);
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if (max(s[i], s[j]) < min(t[i], t[j])) {
        graph[i].push_back(j);
        graph[j].push_back(i);
      }
    }
  }
  vector<int> color(n, -1);
  long long answer = 1;
  for (int start = 0; start < n; ++start) {
    if (color[start] != -1) continue;
    answer = answer * 2 % MOD;
    queue<int> queue;
    queue.push(start);
    color[start] = 0;
    while (!queue.empty()) {
      int node = queue.front();
      queue.pop();
      for (int next : graph[node]) {
        if (color[next] == -1) {
          color[next] = color[node] ^ 1;
          queue.push(next);
        } else if (color[next] == color[node]) {
          cout << 0 << '\n';
          return 0;
        }
      }
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N^2)$，空间 $O(N^2)$；它说明了计数本质，但仍浪费了区间结构。

### 最佳实用解：扫描同时进行的会议数

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
long long modPow(long long base, int exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * base % MOD;
    base = base * base % MOD;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> event(2 * n + 1);
  for (int i = 0; i < n; ++i) {
    int start, finish;
    cin >> start >> finish;
    event[start] = 1;
    event[finish] = -1;
  }
  int active = 0;
  int components = 0;
  for (int time = 1; time <= 2 * n; ++time) {
    if (event[time] == 1) {
      if (active == 0) ++components;
      ++active;
      if (active >= 3) {
        cout << 0 << '\n';
        return 0;
      }
    } else {
      --active;
    }
  }
  cout << modPow(2, components) << '\n';
}
```

时间 $O(N)$，空间 $O(N)$。这是比赛中应优先记忆的实现：证明负担小、无排序常数、直接利用了端点排列这一最强约束。

## 正确性证明

若某次开始事件使活动会议数达到 3，这三场会议从该开始时刻到三者最早结束时刻共同存在。端点互异保证共同区间长度为正，于是三者形成三角形，无法用两色合法着色，输出 0 必然正确。

若活动会议数从未超过 2，新会议开始前只可能有 0 或 1 场活动会议。前者与所有旧分量都不相连，可以任取颜色；后者只需取唯一活动会议的相反颜色。任何更早开始且与新会议重叠的会议在此刻必然仍活动，所以算法没有遗漏约束，得到合法分配。

开始前 `active == 0` 当且仅当新会议与所有旧会议都不连通，因此恰好开启新区间图分量。每个连通分量第一场有两种选择，此后颜色被唯一强制；各分量独立，方案总数恰为 $2^C$。

## 样例手推、边界与易错点

样例一中，会议 1 开始前活动数为 0，建立第一个分量；会议 2 开始时活动数为 1，只能取相反颜色。会议 1、2 结束后，会议 3 开始前活动数重新为 0，建立第二个分量，所以答案为 $2^2=4$。

- $N=1$ 时有一个分量，答案为 2。
- 全部区间互不相交时答案为 $2^N$。
- 一个长区间依次覆盖多个互不重叠的短区间仍合法，整个星形分量只有两种整体翻色。
- 新分量必须在加入开始事件前判断。
- 若推广到相同端点，结束事件必须先于同坐标的开始事件处理。
- `active == 3` 已经形成奇环，不能继续按链式交替着色。

## 变种一：任意坐标且允许端点相同

新定义：坐标可达 $10^{18}$，不同会议可以首尾相接。排序事件；为体现半开区间 $[S,T)$，同坐标先处理结束再处理开始。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  int n;
  cin >> n;
  vector<pair<long long, int>> events;
  for (int i = 0; i < n; ++i) {
    long long start, finish;
    cin >> start >> finish;
    events.push_back({start, 1});
    events.push_back({finish, -1});
  }
  sort(events.begin(), events.end(), [](auto left, auto right) {
    if (left.first != right.first) return left.first < right.first;
    return left.second < right.second;
  });
  int active = 0;
  long long answer = 1;
  for (auto [time, type] : events) {
    (void)time;
    if (type == -1) {
      --active;
    } else {
      if (active == 0) answer = answer * 2 % MOD;
      if (++active >= 3) answer = 0;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。

## 变种二：有 $P$ 名负责人

新定义：每场会议从 $P$ 个有区分的人中选一人。活动区间形成团，新会议开始时不能使用已经被活动会议占据的 `active` 种颜色，所以贡献 $P-active$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  int n, people;
  cin >> n >> people;
  vector<int> event(2 * n + 1);
  for (int i = 0; i < n; ++i) {
    int start, finish;
    cin >> start >> finish;
    event[start] = 1;
    event[finish] = -1;
  }
  int active = 0;
  long long answer = 1;
  for (int time = 1; time <= 2 * n; ++time) {
    if (event[time] == -1) {
      --active;
    } else {
      if (active >= people) answer = 0;
      else answer = answer * (people - active) % MOD;
      ++active;
    }
  }
  cout << answer << '\n';
}
```

时间、空间均为 $O(N)$。

## 变种三：恢复一组具体负责人

新定义：若有解，输出每场会议的颜色。深度至多 2 时，活动集合最多只有一个旧会议；新区间根固定给高桥，其余取相反颜色。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<pair<int, int>> event(2 * n + 1, {-1, -1});
  for (int id = 0; id < n; ++id) {
    int start, finish;
    cin >> start >> finish;
    event[start] = {1, id};
    event[finish] = {-1, id};
  }
  set<int> active;
  vector<int> color(n);
  for (int time = 1; time <= 2 * n; ++time) {
    auto [type, id] = event[time];
    if (type == -1) {
      active.erase(id);
    } else {
      if (active.size() >= 2) {
        cout << "NO\n";
        return 0;
      }
      color[id] = active.empty() ? 0 : color[*active.begin()] ^ 1;
      active.insert(id);
    }
  }
  cout << "YES\n";
  for (int value : color) cout << (value ? "Aoki" : "Takahashi") << '\n';
}
```

时间 $O(N\log N)$（集合大小至多 2，实际为常数），空间 $O(N)$。

## 变种四：每场会议限制可选负责人

新定义：`mask[i]` 的最低两位表示该会议允许高桥、青木中的哪些人。先把深度不超过 2 的区间图压成森林，再对每个分量尝试两种根颜色，贡献可能为 0、1 或 2。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  int n;
  cin >> n;
  vector<int> allowed(n);
  for (int& mask : allowed) cin >> mask;
  vector<pair<int, int>> event(2 * n + 1, {-1, -1});
  for (int id = 0; id < n; ++id) {
    int start, finish;
    cin >> start >> finish;
    event[start] = {1, id};
    event[finish] = {-1, id};
  }
  set<int> active;
  vector<vector<int>> graph(n);
  for (int time = 1; time <= 2 * n; ++time) {
    auto [type, id] = event[time];
    if (type == -1) active.erase(id);
    else {
      if (active.size() >= 2) {
        cout << 0 << '\n';
        return 0;
      }
      if (!active.empty()) {
        int other = *active.begin();
        graph[id].push_back(other);
        graph[other].push_back(id);
      }
      active.insert(id);
    }
  }
  vector<int> side(n, -1);
  long long answer = 1;
  for (int root = 0; root < n; ++root) {
    if (side[root] != -1) continue;
    vector<int> component{root};
    side[root] = 0;
    for (int at = 0; at < static_cast<int>(component.size()); ++at) {
      int node = component[at];
      for (int next : graph[node]) if (side[next] == -1) {
        side[next] = side[node] ^ 1;
        component.push_back(next);
      }
    }
    int ways = 0;
    for (int flip = 0; flip < 2; ++flip) {
      bool valid = true;
      for (int node : component) valid &= allowed[node] >> (side[node] ^ flip) & 1;
      ways += valid;
    }
    answer = answer * ways % MOD;
  }
  cout << answer << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。

## 变种五：不同负责人带来不同收益

新定义：会议 $i$ 分给两人分别得到 `reward[i][0]`、`reward[i][1]`，求最大总收益及达到最大值的方案数。每个连通分量仍只有两种整体朝向，分别求和后取较大者；相等则方案数乘 2。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr long long MOD = 998244353;
int main() {
  int n;
  cin >> n;
  vector<array<long long, 2>> reward(n);
  for (auto& values : reward) cin >> values[0] >> values[1];
  vector<pair<int, int>> event(2 * n + 1, {-1, -1});
  for (int id = 0; id < n; ++id) {
    int start, finish;
    cin >> start >> finish;
    event[start] = {1, id};
    event[finish] = {-1, id};
  }
  set<int> active;
  vector<vector<int>> graph(n);
  for (int time = 1; time <= 2 * n; ++time) {
    auto [type, id] = event[time];
    if (type == -1) active.erase(id);
    else {
      if (active.size() >= 2) {
        cout << "IMPOSSIBLE\n";
        return 0;
      }
      if (!active.empty()) {
        int other = *active.begin();
        graph[id].push_back(other);
        graph[other].push_back(id);
      }
      active.insert(id);
    }
  }
  vector<int> side(n, -1);
  long long best = 0, ways = 1;
  for (int root = 0; root < n; ++root) {
    if (side[root] != -1) continue;
    vector<int> component{root};
    side[root] = 0;
    for (int at = 0; at < static_cast<int>(component.size()); ++at) {
      int node = component[at];
      for (int next : graph[node]) if (side[next] == -1) {
        side[next] = side[node] ^ 1;
        component.push_back(next);
      }
    }
    long long value[2]{};
    for (int flip = 0; flip < 2; ++flip) {
      for (int node : component) value[flip] += reward[node][side[node] ^ flip];
    }
    best += max(value[0], value[1]);
    if (value[0] == value[1]) ways = ways * 2 % MOD;
  }
  cout << best << ' ' << ways << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。

## 可复现验证

两个官方样例实际输出为 4 与 0。独立 oracle 枚举全部负责人分配：对 $N=1$ 到 6 的所有无标号端点完美配对共 11,464 组逐一比较；另以固定种子生成 $N\le12$ 的 50,000 组端点配对，全部与线性扫描一致。文中所有 C++ 块再以 GNU++23 编译。

## Reference

- [AtCoder official problem](https://atcoder.jp/contests/arc226/tasks/arc226_a?lang=en)
- [AtCoder Regular Contest 226](https://atcoder.jp/contests/arc226/tasks?lang=en)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/arc226/tasks/arc226_a?lang=en)
- [对应知识专题](../../graph/weighted-parity-states.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-132-lc18/">[力扣 Top 132] LC 18 四数之和 中等 →</a>
</nav>
