---
title: "[atcoder] ABC472 D Bomber Mad"
---

# [atcoder] ABC472 D Bomber Mad

<p class="daily-archive-kicker">2026-08-26 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-26 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=173f2a9a29e8b41a2911c951869fcc8d51dc323f211b35bf0b38babf8e33c8b8 -->
[AtCoder ABC472 D — Bomber Mad（官方英文题面）](https://atcoder.jp/contests/abc472/tasks/abc472_d?lang=en)

## 官方来源与元数据

- 来源：AtCoder Beginner Contest 472，D 题「Bomber Mad」
- 题目分值：400 分（AtCoder 官方）
- 比赛 Rated Range：0–1999（AtCoder 官方）
- 时间限制：2 秒
- 内存限制：1024 MiB
- AtCoder Problems 社区估算难度：605（抓取于 2026-08-26；不是 AtCoder 官方难度）
- 题面入口：[AtCoder 官方英文题面](https://atcoder.jp/contests/abc472/tasks/abc472_d?lang=en)
- 使用条款：[AtCoder Terms of Service](https://atcoder.jp/tos)

下列英文题面层由模型根据官方页面独立组织，完整保留任务语义、输入输出、约束、样例与解释，不冒充逐字官方原文。

## Complete English statement

You are given a grid with $H$ rows and $W$ columns. Cell $(i,j)$ is the cell in row $i$ from the top and column $j$ from the left. The grid is described by $H$ strings $S_1,S_2,\ldots,S_H$, each of length $W$. A dot `.` denotes an empty cell, and `#` denotes a bomb cell.

An empty cell $(i,j)$ is called a **safe empty cell** precisely when row $i$ contains no bomb and column $j$ contains no bomb.

In one move, you may go from the current cell to an orthogonally adjacent empty cell. You cannot enter a bomb cell. Count the empty cells $(i,j)$ from which at least one safe empty cell is reachable in at most $K$ moves.

### Input

The input is given from Standard Input in the following form:

```text
H W K
S_1
S_2
\vdots
S_H
```

### Output

Print the number of empty cells satisfying the condition.

### Constraints

- $1 \le H,W \le 5\times 10^5$
- $H\times W \le 5\times 10^5$
- $0 \le K \le H\times W-1$
- Every $S_i$ is a length-$W$ string consisting only of `.` and `#`.
- $H$, $W$, and $K$ are integers.

### Official samples

Sample 1

```text
Input
3 3 1
#..
...
..#

Output
5
```

The only safe empty cell is $(2,2)$. The five cells $(1,2),(2,1),(2,2),(2,3),(3,2)$ can reach it in at most one move.

Sample 2

```text
Input
2 3 0
...
...

Output
6
```

There is no bomb anywhere, so every empty cell is safe and already satisfies the requirement with zero moves.

Sample 3

```text
Input
5 7 2
..#....
..#....
.......
...#...
...#...

Output
29
```

## 中文解释与最优结论

先找出所有“所在行没有炸弹，并且所在列也没有炸弹”的空格。它们是距离为 $0$ 的目标集合。随后从这些格子同时开始 BFS，第一次访问某个空格时得到的就是它到最近安全空格的最短路长度。最终统计距离不超过 $K$ 的空格即可。

推荐记住：**多目标最短路等价于把所有目标一起作为多源 BFS 的初始队列**。这样每个空格只入队一次，时间与网格大小成正比。

## 约束推导、溢出与边界

令 $N=H\times W$，官方保证 $N\le 5\times 10^5$。

- 若对每个空格单独搜索最近安全格，最坏要做 $O(N)$ 次、每次扫描 $O(N)$ 个格子，总时间可达 $O(N^2)$，不能通过。
- 网格中每个空格至多有四条边，所以整张可行图有 $O(N)$ 个顶点和 $O(N)$ 条边。
- 所有移动代价都是 $1$，多源 BFS 可在 $O(N)$ 时间内求出每个空格到安全集合的最短距离。
- 距离最大不超过 $N-1$，`int` 足够；答案最大为 $N$，`int` 也足够。实现仍可用 `long long` 保存计数，便于以后扩展。

真正需要检查的边界包括：

- $K=0$：只统计安全空格本身。
- 没有炸弹：每个格子的行、列都无炸弹，答案是 $H\times W$。
- 没有安全空格：初始队列为空，答案为 $0$。
- 全是炸弹：没有可统计的空格，答案为 $0$。
- $H=1$ 或 $W=1$：安全定义仍同时要求所在行和所在列无炸弹，不能只检查一个方向。
- 炸弹可能把空格分成多个连通块；只有含安全格的连通块才可能被 BFS 到达。

## 官方样例手推

样例 1 中，第 1 行和第 3 行含炸弹，第 1 列和第 3 列含炸弹；只有第 2 行与第 2 列同时无炸弹，所以唯一安全格是 $(2,2)$。

把它以距离 $0$ 入队：

- 第 $0$ 层：$(2,2)$；
- 第 $1$ 层：$(1,2),(2,1),(2,3),(3,2)$；
- $K=1$，不再统计更远的格子。

总数为 $1+4=5$。

## 解法一：为每个空格独立寻找安全格

先用行、列炸弹标记判断哪些格子安全。随后从每个空格各做一次 BFS，遇到安全格即停止；若最短距离不超过 $K$，答案加一。

该方法枚举了每个起点，因此覆盖所有候选空格，逻辑正确；但同一连通区域会被反复扫描。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w, k;
  cin >> h >> w >> k;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') {
        row_bomb[i] = 1;
        col_bomb[j] = 1;
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  long long ans = 0;
  for (int si = 0; si < h; ++si) {
    for (int sj = 0; sj < w; ++sj) {
      if (s[si][sj] == '#') continue;
      vector<int> dist(h * w, -1);
      queue<pair<int, int>> q;
      dist[si * w + sj] = 0;
      q.push({si, sj});
      bool ok = false;
      while (!q.empty()) {
        auto [i, j] = q.front();
        q.pop();
        int d = dist[i * w + j];
        if (!row_bomb[i] && !col_bomb[j]) {
          ok = true;
          break;
        }
        if (d == k) continue;
        for (int z = 0; z < 4; ++z) {
          int ni = i + di[z], nj = j + dj[z];
          if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
          int id = ni * w + nj;
          if (s[ni][nj] == '#' || dist[id] != -1) continue;
          dist[id] = d + 1;
          q.push({ni, nj});
        }
      }
      ans += ok;
    }
  }
  cout << ans << '\n';
}
```

时间复杂度最坏为 $O(N^2)$，空间复杂度为 $O(N)$。瓶颈是不同起点重复探索同一批空格。

## 从重复搜索到多源 BFS

问题只关心“到任意安全格的最短距离”，不关心具体选择哪个安全格。把所有安全格同时设为距离 $0$，等价于增加一个虚拟超级源，并用零代价边连接到每个安全格。由于真实移动边权全部为 $1$，从这一组源同时 BFS 就能一次性得到所有最短距离。

每个空格第一次出队时已经拿到最小距离，后续不需要从其他安全格重新搜索。这正好消除了暴力中的重复计算。

## 最佳实用解：行列标记加多源 BFS

### 算法

1. 扫描网格，记录每一行、每一列是否含炸弹。
2. 再扫描所有格子；若某格为空，且对应行、列均无炸弹，就把它以距离 $0$ 加入队列。
3. 从整个初始队列做普通 BFS，只沿空格的上下左右边扩展。
4. 统计距离不超过 $K$ 的空格。实现可在发现新格时立刻计数，并在距离达到 $K$ 后停止继续扩展。

### 正确性证明

记安全空格集合为 $A$，网格中所有空格及其相邻移动边组成无权图 $G$。

**引理 1**：初始队列恰好包含 $A$。

根据定义，空格 $(i,j)$ 安全当且仅当第 $i$ 行无炸弹且第 $j$ 列无炸弹。行列标记直接检查这两个条件，因此不会漏掉或误加入安全格。

**引理 2**：多源 BFS 给每个可达空格 $v$ 的距离等于 $\min_{a\in A}\operatorname{dist}_G(a,v)$。

把所有源同时置为第 $0$ 层后，BFS 依次处理距离 $0,1,2,\ldots$ 的层。若 $v$ 第一次在第 $d$ 层被发现，则存在一条从某个 $a\in A$ 到 $v$ 的长度 $d$ 路径；若存在更短路径，BFS 必会在更早层发现 $v$，矛盾。因此第一次记录的 $d$ 就是到集合 $A$ 的最短距离。

**定理**：算法统计的格子恰好是题目要求的格子。

由引理 2，一个空格被算法在第 $d\le K$ 层访问，当且仅当它能在至多 $K$ 次移动内到达某个安全空格。算法只统计这些格子，故答案正确。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w, k;
  cin >> h >> w >> k;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') {
        row_bomb[i] = 1;
        col_bomb[j] = 1;
      }
    }
  }
  vector<int> dist(h * w, -1);
  queue<int> q;
  long long ans = 0;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      int id = i * w + j;
      if (s[i][j] == '.' && !row_bomb[i] && !col_bomb[j]) {
        dist[id] = 0;
        q.push(id);
        ++ans;
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  while (!q.empty()) {
    int id = q.front();
    q.pop();
    int i = id / w, j = id % w;
    if (dist[id] == k) continue;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      int nid = ni * w + nj;
      if (s[ni][nj] == '#' || dist[nid] != -1) continue;
      dist[nid] = dist[id] + 1;
      q.push(nid);
      ++ans;
    }
  }
  cout << ans << '\n';
}
```

时间复杂度为 $O(HW)$，空间复杂度为 $O(HW)$。

## 同阶方案比较与易错点

也可以先把所有安全格连到一个虚拟超级源，再写一次单源 BFS；它与直接多源初始化完全等价，但会多一个无实际意义的节点。竞赛中优先记忆“多源初始化”，代码更短，也更直接表达目标集合。

常见错误：

- 把“行无炸弹且列无炸弹”错写成“或”。
- 只从一个安全格 BFS；不同连通块中的安全格会被漏掉。
- 允许 BFS 穿过 `#`，从而制造不存在的路径。
- 先把所有空格都加入队列；初始源只能是安全空格。
- 当没有安全格时仍把未访问距离 `-1` 当成合法距离。
- 用曼哈顿距离替代最短路；炸弹可能迫使路径绕行，甚至令两格不连通。

## 可复现验证

本轮对所有发布代码执行 GNU++23 编译。最优解会另外用小网格穷举：随机生成炸弹布局，分别用“每个起点独立 BFS”的暴力程序和多源 BFS 比较答案，覆盖 $K=0$、无炸弹、全炸弹、无安全格和多个连通块。

## Follow-up 与约束变种

### 变种一：同一网格回答多组 $K$

**新定义**：网格固定，给出 $Q$ 个询问，每次问距离安全集合不超过 $K_q$ 的空格数。

原算法若每次重新 BFS 会重复计算。只需做一次完整多源 BFS，把每个有限距离的格子计入直方图，再做前缀和。每个询问以 $O(1)$ 回答；总复杂度为 $O(HW+Q)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w, qn;
  cin >> h >> w >> qn;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') row_bomb[i] = col_bomb[j] = 1;
    }
  }
  int n = h * w;
  vector<int> dist(n, -1), cnt(n + 1);
  queue<int> q;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      int id = i * w + j;
      if (s[i][j] == '.' && !row_bomb[i] && !col_bomb[j]) {
        dist[id] = 0;
        q.push(id);
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  while (!q.empty()) {
    int id = q.front();
    q.pop();
    ++cnt[dist[id]];
    int i = id / w, j = id % w;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      int nid = ni * w + nj;
      if (s[ni][nj] == '#' || dist[nid] != -1) continue;
      dist[nid] = dist[id] + 1;
      q.push(nid);
    }
  }
  for (int d = 1; d <= n; ++d) cnt[d] += cnt[d - 1];
  while (qn--) {
    int k;
    cin >> k;
    cout << cnt[min(k, n)] << '\n';
  }
}
```

### 变种二：恢复一条到安全格的最短路径

**新定义**：预处理后回答若干起点；对每个起点输出一条到安全格的最短路径，若不可达则输出 `-1`。

多源 BFS 仍成立。发现新格时记录把它带入队列的前驱；由于搜索方向是从安全格向外，起点沿前驱反复走就会令距离每次减 $1$，最终到达安全格。预处理 $O(HW)$，每次输出耗时与路径长度成正比。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w;
  cin >> h >> w;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') row_bomb[i] = col_bomb[j] = 1;
    }
  }
  vector<int> dist(h * w, -1), parent(h * w, -1);
  queue<int> q;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      int id = i * w + j;
      if (s[i][j] == '.' && !row_bomb[i] && !col_bomb[j]) {
        dist[id] = 0;
        q.push(id);
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  while (!q.empty()) {
    int id = q.front();
    q.pop();
    int i = id / w, j = id % w;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      int nid = ni * w + nj;
      if (s[ni][nj] == '#' || dist[nid] != -1) continue;
      dist[nid] = dist[id] + 1;
      parent[nid] = id;
      q.push(nid);
    }
  }
  int qn;
  cin >> qn;
  while (qn--) {
    int x, y;
    cin >> x >> y;
    --x;
    --y;
    int id = x * w + y;
    if (s[x][y] == '#' || dist[id] == -1) {
      cout << -1 << '\n';
      continue;
    }
    vector<int> path;
    while (id != -1) {
      path.push_back(id);
      id = parent[id];
    }
    cout << path.size() << '\n';
    for (int v : path) cout << v / w + 1 << ' ' << v % w + 1 << '\n';
  }
}
```

### 变种三：进入空格具有非负代价

**新定义**：仍有炸弹网格 $S$；另给每个空格一个非负进入代价，求到任意安全格的最小总代价不超过 $K$ 的空格数。沿反向搜索从安全格走向邻格时，应增加“原方向从邻格走向当前格”的进入代价，也就是当前格的代价。

普通 BFS 依赖所有边权相等，此时失效。使用多源 Dijkstra；状态仍只需每格一个最短距离。时间复杂度为 $O(HW\log(HW))$，空间复杂度为 $O(HW)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w;
  long long k;
  cin >> h >> w >> k;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<vector<int>> cost(h, vector<int>(w));
  for (auto &row : cost) {
    for (int &x : row) cin >> x;
  }
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') row_bomb[i] = col_bomb[j] = 1;
    }
  }
  const long long inf = (1LL << 62);
  vector<long long> dist(h * w, inf);
  using State = pair<long long, int>;
  priority_queue<State, vector<State>, greater<State>> pq;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      int id = i * w + j;
      if (s[i][j] == '.' && !row_bomb[i] && !col_bomb[j]) {
        dist[id] = 0;
        pq.push({0, id});
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  while (!pq.empty()) {
    auto [d, id] = pq.top();
    pq.pop();
    if (d != dist[id]) continue;
    int i = id / w, j = id % w;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      if (s[ni][nj] == '#') continue;
      int nid = ni * w + nj;
      long long nd = d + cost[i][j];
      if (nd < dist[nid]) {
        dist[nid] = nd;
        pq.push({nd, nid});
      }
    }
  }
  long long ans = 0;
  for (long long d : dist) ans += d <= k;
  cout << ans << '\n';
}
```

### 变种四：统计到安全集合的最短路径条数

**新定义**：对每个空格，求它到任意安全格的最短路径条数，答案对 $998244353$ 取模；炸弹格输出 `-1`，不可达空格输出 `0`。

先用多源 BFS 求 `dist`。所有安全格各有一条长度为 $0$ 的路径。随后按 BFS 出队顺序，把 `ways[u]` 只沿满足 `dist[v]=dist[u]+1` 的边传播。距离严格增加，形成分层 DAG，因此不会重复走回头边。时间、空间复杂度均为 $O(HW)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const int mod = 998244353;
  int h, w;
  cin >> h >> w;
  vector<string> s(h);
  for (string &row : s) cin >> row;
  vector<int> row_bomb(h), col_bomb(w);
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (s[i][j] == '#') row_bomb[i] = col_bomb[j] = 1;
    }
  }
  vector<int> dist(h * w, -1), order, ways(h * w);
  queue<int> q;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      int id = i * w + j;
      if (s[i][j] == '.' && !row_bomb[i] && !col_bomb[j]) {
        dist[id] = 0;
        ways[id] = 1;
        q.push(id);
      }
    }
  }
  const int di[4] = {-1, 1, 0, 0};
  const int dj[4] = {0, 0, -1, 1};
  while (!q.empty()) {
    int id = q.front();
    q.pop();
    order.push_back(id);
    int i = id / w, j = id % w;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      int nid = ni * w + nj;
      if (s[ni][nj] == '#' || dist[nid] != -1) continue;
      dist[nid] = dist[id] + 1;
      q.push(nid);
    }
  }
  for (int id : order) {
    int i = id / w, j = id % w;
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z], nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      int nid = ni * w + nj;
      if (dist[nid] == dist[id] + 1) {
        ways[nid] += ways[id];
        if (ways[nid] >= mod) ways[nid] -= mod;
      }
    }
  }
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (j) cout << ' ';
      int id = i * w + j;
      if (s[i][j] == '#') cout << -1;
      else cout << ways[id];
    }
    cout << '\n';
  }
}
```

## 推荐记忆

看到“到任意一个目标的最短距离”且所有边权相等时，优先把全部目标同时入队做多源 BFS。安全格的判定只是源集合构造；真正可迁移的核心是把重复单源搜索合并为一次分层扩张。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc472/tasks/abc472_d?lang=en)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
