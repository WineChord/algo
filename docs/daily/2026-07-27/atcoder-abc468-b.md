---
title: "[atcoder] ABC468 B Corridor Watch"
---

# [atcoder] ABC468 B Corridor Watch

<p class="daily-archive-kicker">2026-07-27 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

Official problem: [Open the official problem](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)

Copyright terms: [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en)

## Official source record

- Platform and contest: AtCoder, AtCoder Beginner Contest 468.
- Official task identity: `abc468_b`, index B, title “Corridor Watch”.
- Contest window: 2026-07-25 21:00–22:40 JST; duration 100 minutes.
- Official contest rated range: 0–1999.
- Official task score: 200 points.
- Official per-task difficulty label: not provided by AtCoder.
- AtCoder Problems community model: raw estimated difficulty `-388`, `is_experimental=false`, retrieved 2026-07-27. This is a community estimate, not an AtCoder rating.
- Limits: 2 seconds, 1024 MiB.
- Program interface: GNU++23 full program.
- Official statement images: none inside the task statement.

!!! info "Official source and copyright"
    AtCoder is the authoritative source. Ordinary AtCoder contest statements do not carry a confirmed blanket republication licence, so the complete English statement below is independently written from the official task while preserving its full semantics, data contract, constraints, and examples.

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

## Constraint-driven observations

For a fixed cell $x$, only the clipped interval

$$
[\max(0,x-D),\min(M-1,x+D)]
$$

matters in zero-based indexing. The official bound $M\le100$ makes the direct $O(M^2)$ scan fully acceptable: at most $10^4$ position checks. Nevertheless, the problem exposes a reusable interval-union/sliding-window pattern that scales to $M$ in the millions.

No arithmetic can overflow a 32-bit `int`: indices and the answer are at most 100. The important boundary cases are $D=0$, no guards, all guards, a guard at an endpoint, and overlapping watch intervals.

## Sample 1 state evolution

With $D=1$, the guards at zero-based positions $1,5,6$ watch intervals $[0,2]$, $[4,6]$, and $[5,6]$. Their union is $[0,2]\cup[4,6]$, leaving only position 3, which is cell 4.

## Solution 1: direct cell–guard enumeration

For each cell $x$, scan every possible guard position $i$. The cell is unwatched if no pair satisfies `S[i] == 'G' && abs(x - i) <= D`.

Coverage is immediate: every possible witnessing guard is tested. The bottleneck is repeating essentially the same neighborhood work for adjacent cells.

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

- Time: $O(M^2)$.
- Extra space: $O(1)$.

## Solution 2: interval difference array

Each guard contributes $+1$ to an interval $[i-D,i+D]$, clipped to the corridor. Apply these interval additions to a difference array, take prefix sums, and count positions whose coverage is zero.

This removes repeated per-cell guard checks and naturally generalizes to guard-specific radii.

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

- Time: $O(M)$.
- Extra space: $O(M)$.

## Solution 3: sliding guard count — recommended

For cell $x$, maintain the number of guards in its watch window $[x-D,x+D]$. When moving from $x$ to $x+1$, remove $x-D$ and add $x+D+1$, if those indices exist.

### Invariant and proof

Before testing cell $x$, `guards` equals the number of `G` characters in the clipped interval $[x-D,x+D]$. This is true for $x=0$ after initialization over $[0,D]$. The remove/add update transforms exactly that interval into the next cell’s interval, so induction preserves the invariant. A cell is watched exactly when this count is positive; therefore every increment of `ans` and only such increments corresponds to an unwatched cell.

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

- Time: $O(M)$.
- Extra space: $O(1)$.
- Recommendation: remember this version when every interval has the same radius and only the zero/nonzero coverage status is needed. Remember the difference-array version when intervals have varying endpoints or richer output is required.

## Common mistakes

- Counting guards rather than watched cells.
- Forgetting that a guard’s own cell is watched.
- Using an unclipped negative or out-of-range endpoint.
- Summing interval lengths without merging overlaps.
- Treating $D$ as an exclusive radius.
- Returning zero when there are no guards; the correct answer is $M$.

## Follow-up 1: output maximal unwatched ranges

**New definition.** Output all maximal one-based intervals consisting entirely of unwatched cells.

The difference-array coverage remains valid. After prefix summation, group consecutive zero-coverage positions.

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

- Time: $O(M)$.
- Extra space: $O(M+R)$, where $R$ is the number of output ranges.

## Follow-up 2: every guard has its own radius

**New definition.** Input includes a radius $d_i$ for every position; it matters only where `S[i] == 'G'`.

The fixed-window solution fails because adjacent cells no longer share one uniform window. Interval difference additions still work unchanged after computing each guard’s own endpoints.

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

- Time: $O(M)$.
- Extra space: $O(M)$.

## Follow-up 3: circular corridor

**New definition.** Cells form a cycle, and distance is the shorter circular distance. Assume $0\le D<M$.

Duplicate the string three times. For the middle copy, every circular radius-$D$ neighborhood becomes one ordinary interval in the tripled string.

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

- Time: $O(M)$.
- Extra space: $O(M)$.

## Follow-up 4: online guard toggles and count queries

**New definition.** `T p` toggles a guard at one-based position $p$; `Q` asks for the current number of unwatched cells. $D$ stays fixed.

A toggle performs a range add of $+1$ or $-1$. A lazy segment tree stores the minimum coverage and how many positions attain it. Coverage is never negative, so positions are unwatched exactly when the global minimum is zero.

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

- Update: $O(\log M)$.
- Query: $O(1)$.
- Space: $O(M)$.

## Follow-up 5: two-dimensional grid with Manhattan distance

**New definition.** Guards occupy cells of an $H\times W$ grid. A cell is watched if its Manhattan distance from a guard is at most $D$.

Intervals are no longer one-dimensional. Multi-source BFS from all guards computes the nearest-guard distance to every cell in $O(HW)$.

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

- Time: $O(HW)$.
- Extra space: $O(HW)$.

## Follow-up 6: place the minimum number of guards

**New definition.** The corridor starts empty. Place guards of common radius $D$ so every cell is watched, and output a minimum placement.

Take the leftmost uncovered cell and put a guard as far right as possible while still covering it. That greedily maximizes the newly covered suffix. Any valid solution needs a guard that covers this leftmost cell, and moving that guard right to the greedy position cannot reduce coverage of any still-uncovered cell.

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

- Time: $O(M/(2D+1)+1)$.
- Extra space: proportional to the output.

## Reproducible verification plan

- Compile every C++ block with Clang in C++23 mode.
- Exhaustively/randomly compare the direct scan, difference array, and sliding-window counts on small corridors, including $D=0$, $D=M-1$, no guards, and all guards.
- For the circular variant, compare against direct circular-distance enumeration.
- For the toggle segment tree, compare every query against recomputation on a mutable string.

## Sources

- Official task: [Open the official problem](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)
- Official contest information and scoring: [Open the official contest](https://atcoder.jp/contests/abc468?lang=en)
- Official editorial: [Open the official editorial](https://atcoder.jp/contests/abc468/editorial/23735)
- AtCoder Problems model data: [打开来源页面](https://kenkoooo.com/atcoder/resources/problem-models.json)

## Reference

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_b?lang=en)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-11-lc2/">[力扣 Top 11] LC 2 两数相加 中等 →</a>
</nav>
