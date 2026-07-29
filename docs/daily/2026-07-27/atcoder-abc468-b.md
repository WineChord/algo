---
title: "[atcoder] ABC468 B Corridor Watch"
---

# [atcoder] ABC468 B Corridor Watch

<p class="daily-archive-kicker">2026-07-27 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

官方题目：[打开 AtCoder 题目页](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)

版权条款：[AtCoder 使用条款](https://atcoder.jp/tos?lang=en)

## 官方原始信息

- 平台与比赛：AtCoder，AtCoder Beginner Contest 468。
- 官方题目标识：`abc468_b`，B 题，标题为 “Corridor Watch”。
- 比赛时间：2026-07-25 21:00–22:40 JST，共 100 分钟。
- 官方比赛 rated 范围：0–1999。
- 官方题目分值：200 分。
- 官方单题难度：AtCoder 未标注。
- AtCoder Problems 社区模型：原始估算难度 `-388`，`is_experimental=false`，抓取于 2026-07-27；这是社区估算，不是 AtCoder 官方 rating。
- 限制：2 秒，1024 MiB。
- 程序接口：GNU++23 完整程序。
- 官方题面图片：题面中没有图片。

!!! info "官方来源与版权边界"
    AtCoder 是本题的权威来源。普通 AtCoder 竞赛题面没有经过确认的统一开放转载许可，因此下方完整英文题面层依据官方题目独立组织，在不逐字镜像的前提下完整保留任务语义、输入输出契约、约束与样例。

## Complete English statement

There are $M$ cells in a straight row, numbered $1,\ldots,M$. The length-$M$ string $S$ contains only `G` and `.`. A `G` at position $i$ means a guard stands there. A cell $x$ is watched exactly when at least one guard position $i$ satisfies

$$
|x-i|\le D.
$$

Count the cells that are not watched. A watched cell may contain a guard; overlapping watch ranges still count that cell only once.

### Input

```text
M D
S
```

### Output

Print one integer: the number of unwatched cells.

### All official constraints

- $0\le D<M\le100$.
- $M$ and $D$ are integers.
- $S$ has length $M$ and consists only of `G` and `.`.

### All official samples

Sample 1:

```text
Input
7 1
.G...GG
Output
1
```

Only cell 4 is unwatched.

Sample 2:

```text
Input
6 5
......
Output
6
```

There is no guard, so every cell is unwatched even though $D$ is large.

Sample 3:

```text
Input
21 2
....G...GG.....G.....
Output
6
```

## 中文题意与样例说明

走廊由 $M$ 个格子组成，字符串 `S` 中的 `G` 表示守卫。若某格与至少一名守卫的位置距离不超过 $D$，该格就被监视；守卫所在格也按同一规则计算，多个监视区间重叠时仍只算一个格子。题目要求输出完全没有被任何守卫监视的格子数。

输入依次给出 $M,D$ 与长度为 $M$ 的字符串 `S`，输出一个整数。样例 1 中三名守卫覆盖除第 4 格外的所有位置，所以答案为 1；样例 2 没有守卫，因此六个格子都未被监视；样例 3 的答案为 6。全部边界与样例数据以上方官方英文信息为准。

## 约束驱动的观察

对固定格子 $x$，只有截断后的区间

$$
[\max(0,x-D),\min(M-1,x+D)]
$$

可能包含能监视它的守卫。官方约束 $M\le100$，因此直接进行 $O(M^2)$ 扫描最多检查 $10^4$ 对位置，已经完全足够。不过，这道题还暴露了可以迁移到百万规模数据的区间并集与滑动窗口模型。

下标与答案都不超过 100，使用 32 位 `int` 不会溢出。真正需要覆盖的边界包括 $D=0$、没有守卫、全是守卫、守卫位于端点，以及多个监视区间重叠。

## 样例 1 状态演化

当 $D=1$ 时，零基位置 $1,5,6$ 的守卫分别覆盖 $[0,2]$、$[4,6]$ 与 $[5,6]$。这些区间的并集是 $[0,2]\cup[4,6]$，只留下零基位置 3，也就是第 4 格未被监视。

## 解法一：枚举格子与守卫

对每个格子 $x$ 扫描所有可能的守卫位置 $i$。如果不存在满足 `S[i] == 'G' && abs(x - i) <= D` 的位置，这个格子就未被监视。

该做法的完备性很直接：所有可能监视 $x$ 的守卫都会被检查。瓶颈在于相邻格子的监视范围高度重叠，却被反复扫描。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  string s;
  cin >> m >> d >> s;
  int ans = 0;
  for (int x = 0; x < m; ++x) {
    bool watched = false;
    for (int i = 0; i < m; ++i) {
      if (s[i] == 'G' && abs(x - i) <= d) {
        watched = true;
        break;
      }
    }
    ans += !watched;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(M^2)$。
- 额外空间复杂度：$O(1)$。

## 解法二：区间差分

每名守卫会让截断到走廊范围内的区间 $[i-D,i+D]$ 覆盖次数增加 1。把所有区间加法记录到差分数组中，再求前缀和，统计覆盖次数为 0 的位置。

这样消除了逐格重复检查守卫的工作，也能自然推广到每名守卫半径不同的情形。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  string s;
  cin >> m >> d >> s;
  vector<int> diff(m + 1);
  for (int i = 0; i < m; ++i) {
    if (s[i] != 'G') continue;
    int l = max(0, i - d);
    int r = min(m - 1, i + d);
    ++diff[l];
    --diff[r + 1];
  }
  int ans = 0;
  int cover = 0;
  for (int x = 0; x < m; ++x) {
    cover += diff[x];
    ans += cover == 0;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(M)$。
- 额外空间复杂度：$O(M)$。

## 解法三：滑动维护守卫数量（推荐）

处理格子 $x$ 时，维护监视窗口 $[x-D,x+D]$ 内的守卫数量。窗口从 $x$ 移到 $x+1$ 时，如果对应下标存在，就删除 $x-D$，加入 $x+D+1$。

### 不变量与证明

检查格子 $x$ 之前，`guards` 恰好等于截断区间 $[x-D,x+D]$ 中 `G` 的数量。初始化扫描 $[0,D]$ 后，该结论对 $x=0$ 成立；删除离开窗口的位置并加入新进入窗口的位置，恰好把当前区间变成下一个格子的区间，因此归纳可知不变量始终成立。格子被监视当且仅当这个计数为正，所以 `ans` 增加的每一次且仅有这些次都对应一个未被监视的格子。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  string s;
  cin >> m >> d >> s;
  int guards = 0;
  for (int i = 0; i <= d && i < m; ++i) guards += s[i] == 'G';
  int ans = 0;
  for (int x = 0; x < m; ++x) {
    ans += guards == 0;
    int out = x - d;
    int in = x + d + 1;
    if (out >= 0 && s[out] == 'G') --guards;
    if (in < m && s[in] == 'G') ++guards;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(M)$。
- 额外空间复杂度：$O(1)$。
- 记忆建议：所有区间半径相同且只关心覆盖次数是否为零时，优先记滑动窗口；区间端点各不相同或需要更丰富的覆盖信息时，优先记差分数组。

## 常见错误

- 统计守卫数量，而不是被监视的格子数量。
- 忘记守卫所在格本身也被监视。
- 没有把负数或越界的区间端点截断。
- 未合并重叠区间就直接累加区间长度。
- 错把 $D$ 当作不包含端点的半径。
- 没有守卫时返回 0；正确答案应为 $M$。

## 追问一：输出极大未监视区间

<strong>新定义。</strong>输出所有完全由未监视格子构成的极大一基闭区间。

差分数组得到的覆盖次数仍然有效。求完前缀和后，把连续的零覆盖位置分组即可。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  string s;
  cin >> m >> d >> s;
  vector<int> diff(m + 1);
  for (int i = 0; i < m; ++i) {
    if (s[i] != 'G') continue;
    int l = max(0, i - d);
    int r = min(m - 1, i + d);
    ++diff[l];
    --diff[r + 1];
  }
  vector<pair<int, int>> ranges;
  int cover = 0;
  int start = -1;
  for (int i = 0; i < m; ++i) {
    cover += diff[i];
    if (cover == 0 && start == -1) start = i;
    if (cover > 0 && start != -1) {
      ranges.push_back({start + 1, i});
      start = -1;
    }
  }
  if (start != -1) ranges.push_back({start + 1, m});
  cout << ranges.size() << '\n';
  for (auto [l, r] : ranges) cout << l << ' ' << r << '\n';
}
```

- 时间复杂度：$O(M)$。
- 额外空间复杂度：$O(M+R)$，其中 $R$ 是输出区间数量。

## 追问二：每名守卫拥有独立半径

<strong>新定义。</strong>输入为每个位置提供半径 $d_i$，只有 `S[i] == 'G'` 时该半径才生效。

固定窗口方案失效，因为相邻格子不再共享统一半径的窗口。分别计算每名守卫的左右端点后，区间差分仍可原样使用。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m;
  string s;
  cin >> m >> s;
  vector<int> radius(m);
  for (int& x : radius) cin >> x;
  vector<int> diff(m + 1);
  for (int i = 0; i < m; ++i) {
    if (s[i] != 'G') continue;
    int l = max(0, i - radius[i]);
    int r = min(m - 1, i + radius[i]);
    ++diff[l];
    --diff[r + 1];
  }
  int ans = 0;
  int cover = 0;
  for (int i = 0; i < m; ++i) {
    cover += diff[i];
    ans += cover == 0;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(M)$。
- 额外空间复杂度：$O(M)$。

## 追问三：环形走廊

<strong>新定义。</strong>所有格子首尾相接成环，距离取环上两条路径中的较短者，且 $0\le D<M$。

把字符串连续复制三份。对中间副本中的格子而言，环形半径 $D$ 的邻域会变成三倍字符串中的普通连续区间。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  string s;
  cin >> m >> d >> s;
  if (2 * d + 1 >= m) {
    cout << (s.find('G') == string::npos ? m : 0) << '\n';
    return 0;
  }
  string t = s + s + s;
  vector<int> pref(3 * m + 1);
  for (int i = 0; i < 3 * m; ++i) pref[i + 1] = pref[i] + (t[i] == 'G');
  int ans = 0;
  for (int x = m; x < 2 * m; ++x) {
    int guards = pref[x + d + 1] - pref[x - d];
    ans += guards == 0;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(M)$。
- 额外空间复杂度：$O(M)$。

## 追问四：在线切换守卫并查询数量

<strong>新定义。</strong>`T p` 切换一基位置 $p$ 是否存在守卫，`Q` 查询当前未被监视的格子数，$D$ 保持不变。

一次切换对应区间整体加 $+1$ 或 $-1$。懒标记线段树维护全局最小覆盖次数及取得最小值的位置数量。覆盖次数不会为负，因此全局最小值为 0 时，取得最小值的位置恰好就是未被监视的格子。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
struct SegTree {
  int n;
  vector<int> mn, cnt, lazy;
  explicit SegTree(int size) : n(size), mn(4 * size), cnt(4 * size), lazy(4 * size) {
    build(1, 0, n - 1);
  }
  void build(int p, int l, int r) {
    cnt[p] = r - l + 1;
    if (l == r) return;
    int mid = (l + r) / 2;
    build(p * 2, l, mid);
    build(p * 2 + 1, mid + 1, r);
  }
  void apply(int p, int value) {
    mn[p] += value;
    lazy[p] += value;
  }
  void push(int p) {
    if (lazy[p] == 0) return;
    apply(p * 2, lazy[p]);
    apply(p * 2 + 1, lazy[p]);
    lazy[p] = 0;
  }
  void pull(int p) {
    mn[p] = min(mn[p * 2], mn[p * 2 + 1]);
    cnt[p] = 0;
    if (mn[p * 2] == mn[p]) cnt[p] += cnt[p * 2];
    if (mn[p * 2 + 1] == mn[p]) cnt[p] += cnt[p * 2 + 1];
  }
  void add(int p, int l, int r, int ql, int qr, int value) {
    if (ql <= l && r <= qr) {
      apply(p, value);
      return;
    }
    push(p);
    int mid = (l + r) / 2;
    if (ql <= mid) add(p * 2, l, mid, ql, qr, value);
    if (qr > mid) add(p * 2 + 1, mid + 1, r, ql, qr, value);
    pull(p);
  }
  void add(int l, int r, int value) {
    add(1, 0, n - 1, l, r, value);
  }
  int unwatched() const {
    return mn[1] == 0 ? cnt[1] : 0;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d, q;
  string s;
  cin >> m >> d >> q >> s;
  SegTree tree(m);
  auto update = [&](int i, int delta) {
    tree.add(max(0, i - d), min(m - 1, i + d), delta);
  };
  for (int i = 0; i < m; ++i) {
    if (s[i] == 'G') update(i, 1);
  }
  while (q--) {
    char type;
    cin >> type;
    if (type == 'Q') {
      cout << tree.unwatched() << '\n';
    } else {
      int p;
      cin >> p;
      --p;
      if (s[p] == 'G') {
        update(p, -1);
        s[p] = '.';
      } else {
        update(p, 1);
        s[p] = 'G';
      }
    }
  }
}
```

- 单次更新：$O(\log M)$。
- 单次查询：$O(1)$。
- 空间复杂度：$O(M)$。

## 追问五：二维网格与曼哈顿距离

<strong>新定义。</strong>守卫位于 $H\times W$ 网格中；若某格到至少一名守卫的曼哈顿距离不超过 $D$，该格就被监视。

监视范围不再是一维区间。从所有守卫同时出发进行多源 BFS，可以在 $O(HW)$ 时间内求出每个格子到最近守卫的距离。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w, d;
  cin >> h >> w >> d;
  vector<string> grid(h);
  for (string& row : grid) cin >> row;
  const int inf = 1e9;
  vector<vector<int>> dist(h, vector<int>(w, inf));
  queue<pair<int, int>> que;
  for (int i = 0; i < h; ++i) {
    for (int j = 0; j < w; ++j) {
      if (grid[i][j] != 'G') continue;
      dist[i][j] = 0;
      que.push({i, j});
    }
  }
  int di[4] = {1, -1, 0, 0};
  int dj[4] = {0, 0, 1, -1};
  while (!que.empty()) {
    auto [i, j] = que.front();
    que.pop();
    for (int z = 0; z < 4; ++z) {
      int ni = i + di[z];
      int nj = j + dj[z];
      if (ni < 0 || ni >= h || nj < 0 || nj >= w) continue;
      if (dist[ni][nj] <= dist[i][j] + 1) continue;
      dist[ni][nj] = dist[i][j] + 1;
      que.push({ni, nj});
    }
  }
  int ans = 0;
  for (const auto& row : dist) {
    for (int value : row) ans += value > d;
  }
  cout << ans << '\n';
}
```

- 时间复杂度：$O(HW)$。
- 额外空间复杂度：$O(HW)$。

## 追问六：放置最少数量的守卫

<strong>新定义。</strong>走廊初始为空，放置监视半径均为 $D$ 的守卫，使所有格子都被监视，并输出一种数量最少的放置方案。

每次找到最左侧未覆盖格子，并在仍能覆盖它的前提下把守卫放得尽量靠右，从而最大化新覆盖的后缀。任何合法方案都必须用某名守卫覆盖这个最左格；把该守卫向右移动到贪心位置，不会减少对任何尚未覆盖格子的覆盖，因此贪心保持最优。

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, d;
  cin >> m >> d;
  vector<int> guards;
  int left = 1;
  while (left <= m) {
    int position = min(m, left + d);
    guards.push_back(position);
    left = position + d + 1;
  }
  cout << guards.size() << '\n';
  for (int i = 0; i < (int)guards.size(); ++i) {
    if (i) cout << ' ';
    cout << guards[i];
  }
  cout << '\n';
}
```

- 时间复杂度：$O(M/(2D+1)+1)$。
- 额外空间复杂度：与输出方案长度成正比。

## 可复现验证

- 使用 C++23 编译每个 C++ 代码块。
- 在小规模走廊上穷举或随机生成数据，对拍直接扫描、差分数组与滑动窗口，覆盖 $D=0$、$D=M-1$、没有守卫和全是守卫。
- 环形变种与直接枚举环形距离的暴力实现对拍。
- 在线切换变种中，每次查询都与在可变字符串上重新计算的结果比较。

## 来源

- 官方题目：[打开 AtCoder 题目页](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)
- 官方比赛信息与分值：[打开 AtCoder 比赛页](https://atcoder.jp/contests/abc468?lang=en)
- 官方题解：[打开 AtCoder 官方题解](https://atcoder.jp/contests/abc468/editorial/23735)
- AtCoder Problems 模型数据：[打开数据源](https://kenkoooo.com/atcoder/resources/problem-models.json)

## 参考资料

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-11-lc2/">[力扣 Top 11] LC 2 两数相加 中等 →</a>
</nav>
