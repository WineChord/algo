---
title: "[codeforces] CF Educational Round 193 Div.2 B Hypercarp and the Control Panel"
---

# [codeforces] CF Educational Round 193 Div.2 B Hypercarp and the Control Panel

<p class="daily-archive-kicker">2026-08-26 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-26 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=559d7afb3f849a726c732a2ddfe6304e03f814df82510fd1d065a162daa8c972 -->
[Codeforces 2253B — Hypercarp and the Control Panel（官方英文题面）](https://codeforces.com/contest/2253/problem/B)

## 官方来源与元数据

- 来源：Educational Codeforces Round 193 (Rated for Div. 2)，Div.2 B
- Contest ID：2253
- 官方 rating：1100
- 官方 points：未知（官方 API 未提供）
- 官方 tags：`brute force`、`data structures`、`two pointers`
- 时间限制：2 秒
- 内存限制：512 MB
- 题面入口：[Codeforces 官方题面](https://codeforces.com/contest/2253/problem/B)
- 许可说明：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)

下列英文题面层根据 Codeforces 官方页面整理，完整保留任务定义、输入输出、约束和全部样例。题面中与输入、输出及判题契约无关的实现指令不属于题意，未纳入呈现。

## Complete English statement

Hypercarp is building a spaceship control panel containing $n$ signal modules in one row. Module $i$ has color $a_i$.

He first chooses which modules to retain. Removing modules preserves the relative order of every retained module. Once all removals are complete, he may perform at most one operation that exchanges two neighboring modules in the retained sequence. He cannot remove any further module after that exchange.

The final retained sequence must have different colors at every pair of neighboring positions. Find the greatest possible number of retained modules.

### Input

The input contains several test cases.

- The first line contains $t$ ($1\le t\le 10^4$).
- For each test case, the first line contains $n$ ($1\le n\le 2\times 10^5$).
- The second line contains $a_1,a_2,\ldots,a_n$ ($1\le a_i\le n$).
- The sum of $n$ over all test cases does not exceed $2\times 10^5$.

### Output

For every test case, print the maximum possible number of retained modules.

### Constraints

- $1\le t\le 10^4$.
- $1\le n\le 2\times 10^5$ for every test case.
- $1\le a_i\le n$ for every module.
- The sum of $n$ over all test cases does not exceed $2\times 10^5$.

### Official sample

```text
Input
12
1
1
6
1 2 1 3 1 2
5
4 4 4 4 4
3
1 1 2
4
1 2 2 1
5
1 1 2 1 1
6
1 2 2 3 3 1
8
1 1 2 3 3 2 2 1
4
1 1 2 3
4
1 2 1 1
4
3 2 1 1
6
1 1 2 1 1 3

Output
1
6
1
3
4
3
6
7
4
3
4
5
```

For example, in the fourth test case, swapping the second and third retained modules turns $[1,1,2]$ into $[1,2,1]$. In the seventh test case, swapping positions $3$ and $4$ turns the whole sequence into $[1,2,3,2,3,1]$. In the eighth test case, one leading $1$ can be removed first; the retained sequence $[1,2,3,3,2,2,1]$ then becomes $[1,2,3,2,3,2,1]$ after one adjacent swap.

## 中文解释与最优结论

先删除任意元素，得到原数组的一个子序列；删除结束后，至多交换一次这个子序列中相邻的两个元素。最终相邻颜色必须不同，目标是最大化保留长度。允许交换的是“删除后相邻”的元素，它们在原数组里不一定相邻。

把数组压成极大等值游程。每个游程先取一个，基础答案是游程数 $m$。一次交换最多再保留两个元素：

- 若有两个相邻游程的长度都至少为 $2$，局部 $x,x,y,y$ 交换中间两项后变成 $x,y,x,y$，答案是 $m+2$；
- 否则，若某个长游程能把一个副本越过相邻游程，且不会撞上距离为 $2$ 的同色游程，答案是 $m+1$；
- 其余情况答案是 $m$。

推荐记住：**先压缩成游程，再研究一次局部操作最多能修复多少条相等邻边。**

## 约束推导、溢出与边界

所有测试的总长度不超过 $2\times10^5$，因此目标是总 $O(n)$ 或 $O(n\log n)$。

- 枚举子序列有 $2^n$ 种，只适合作为小规模正确性基准。
- 同一游程若保留至少三个相同元素，一次相邻交换仍至少留下一个相等邻边，所以每个游程最多贡献两个元素。
- 交换只改变至多三条相邻关系，是否能增加长度只依赖相邻和距离为 $2$ 的游程。
- 答案不超过 $n$，`int` 足够；实现没有大整数乘法。

关键边界：一个游程时答案永远为 $1$；两个游程中一个长游程可增加 $1$，两个都长可增加 $2$；形如 $x,y,x$ 时，不能把 $x$ 越过 $y$ 后与另一个 $x$ 相邻；已经相邻全异时答案就是 $n$。

## 解法一：枚举子序列与交换位置

枚举所有非空子序列，再枚举“不交换”或交换其中任意一对相邻元素，检查最终序列是否相邻全异。它覆盖了所有合法操作顺序，因此正确，但时间复杂度为 $O(2^n n^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  int ans = 0;
  for (int mask = 1; mask < (1 << n); ++mask) {
    vector<int> b;
    for (int i = 0; i < n; ++i) {
      if (mask >> i & 1) b.push_back(a[i]);
    }
    for (int p = -1; p + 1 < static_cast<int>(b.size()); ++p) {
      if (p >= 0) swap(b[p], b[p + 1]);
      bool ok = true;
      for (int i = 1; i < static_cast<int>(b.size()); ++i) {
        if (b[i] == b[i - 1]) ok = false;
      }
      if (ok) ans = max(ans, static_cast<int>(b.size()));
      if (p >= 0) swap(b[p], b[p + 1]);
    }
  }
  cout << ans << '\n';
}
```

## 从暴力到游程公式

不交换时，每个极大等值游程最多取一个，而且每个游程取一个一定相邻全异，所以基础答案恰为游程数 $m$。

若要从某个游程多取一个，就会产生一条相等邻边。一次相邻交换最多同时修复交换位置两侧的两条相等邻边，因此总增量最多为 $2$。这把指数级子序列枚举压缩成三种候选：$m$、$m+1$、$m+2$。

记游程为 $(c_i,\ell_i)$，其中相邻 $c_i$ 不同。若相邻两个游程都长，局部 $x,x,y,y$ 可达到增量 $2$。否则，长游程 $i$ 向右增加一个副本的条件为

$$
i+1<m\quad\text{且}\quad(i+2\ge m\ \text{或}\ c_i\ne c_{i+2}),
$$

向左条件对称：

$$
i>0\quad\text{且}\quad(i<2\ \text{或}\ c_i\ne c_{i-2}).
$$

## 最佳实用解：RLE 加局部见证

### 正确性证明

**引理 1**：每个原游程最多贡献两个元素。若同一游程保留三个相同元素，它们在删除后的序列中仍按原顺序形成连续同色块；一次相邻交换至多插入一个外部颜色，仍会留下相等邻边。

**引理 2**：最优长度不超过 $m+2$。基础上每多取一个元素就产生一条需要修复的相等邻边，而一次交换只可能修复交换位置两侧的两条邻边。

**引理 3**：能达到 $m+2$ 当且仅当存在相邻的两个长游程。要多取两个元素，两条相等邻边必须同时位于被交换元素的两侧，交换前局部只能是 $x,x,y,y$；反过来该局部交换中间两项立即得到 $x,y,x,y$。

**引理 4**：在不存在增量 $2$ 时，能达到 $m+1$ 当且仅当某个长游程满足上述向左或向右条件。以向右为例，$x,x,y,z$ 交换中间的 $x,y$ 后成为 $x,y,x,z$，只有当 $z$ 不存在或 $x\ne z$ 才合法。任何只增加一个元素的方案也必须用相邻颜色插入唯一重复对，故不会遗漏其他结构。

由四个引理，算法按 $m+2$、$m+1$、$m$ 的顺序判定，得到最优答案。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Run {
  int color;
  int length;
};
void solve() {
  int n;
  cin >> n;
  vector<Run> runs;
  for (int i = 0; i < n; ++i) {
    int x;
    cin >> x;
    if (runs.empty() || runs.back().color != x) {
      runs.push_back({x, 1});
    } else {
      ++runs.back().length;
    }
  }
  int m = static_cast<int>(runs.size());
  int bonus = 0;
  for (int i = 0; i + 1 < m; ++i) {
    if (runs[i].length >= 2 && runs[i + 1].length >= 2) bonus = 2;
  }
  if (bonus < 2) {
    for (int i = 0; i < m; ++i) {
      if (runs[i].length < 2) continue;
      bool right = i + 1 < m &&
          (i + 2 >= m || runs[i].color != runs[i + 2].color);
      bool left = i > 0 &&
          (i < 2 || runs[i].color != runs[i - 2].color);
      if (right || left) bonus = 1;
    }
  }
  cout << m + bonus << '\n';
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) solve();
}
```

时间复杂度为每组 $O(n)$，空间复杂度为 $O(n)$。

## 可复现验证

官方 12 组样例均得到指定输出；另以“枚举全部子序列与全部相邻交换”为 oracle，对三种颜色、$1\le n\le8$ 的 9840 个数组穷举对拍，结果全部一致。在线追加版本又对 1392 个前缀序列逐步核对，结果全部一致。

## 易错点

- 操作顺序是先删再交换；删除后相邻不等于原数组相邻。
- `points` 缺失应写未知，不能把 `rating=1100` 当作比赛分值。
- 增量 $2$ 要求两个长游程相邻，不能只检查是否存在两个长游程。
- 增量 $1$ 必须检查距离为 $2$ 的颜色；$x,x,y,x$ 交换后仍会出现相邻的 $x$。
- 一旦发现增量 $2$ 就应优先返回，增量 $1$ 不能覆盖它。

## Follow-up 1：恢复一组最优操作

新要求是输出保留的原下标，以及删除后要交换的相邻位置；若无需交换，输出 $0$。RLE 时保存每个游程的下标。对增量 $2$ 的相邻长游程各取两个；对增量 $1$ 的见证游程取两个；其余游程各取一个。构造与证明中的局部结构完全一致。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Run {
  int color;
  vector<int> pos;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Run> r;
  for (int i = 1; i <= n; ++i) {
    int x;
    cin >> x;
    if (r.empty() || r.back().color != x) r.push_back({x, {}});
    r.back().pos.push_back(i);
  }
  int m = static_cast<int>(r.size()), kind = 0, at = -1;
  for (int i = 0; i + 1 < m; ++i) {
    if (r[i].pos.size() >= 2 && r[i + 1].pos.size() >= 2) {
      kind = 2;
      at = i;
      break;
    }
  }
  if (!kind) {
    for (int i = 0; i < m; ++i) {
      if (r[i].pos.size() < 2) continue;
      bool right = i + 1 < m &&
          (i + 2 >= m || r[i].color != r[i + 2].color);
      bool left = i > 0 &&
          (i < 2 || r[i].color != r[i - 2].color);
      if (right) {
        kind = 1;
        at = i;
        break;
      }
      if (left) {
        kind = -1;
        at = i;
        break;
      }
    }
  }
  vector<int> take(m, 1);
  if (kind == 2) take[at] = take[at + 1] = 2;
  if (kind == 1 || kind == -1) take[at] = 2;
  vector<int> kept;
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < take[i]; ++j) kept.push_back(r[i].pos[j]);
  }
  int swap_left = 0;
  int before = 0;
  if (at >= 0) before = accumulate(take.begin(), take.begin() + at, 0);
  if (kind == 2 || kind == 1) swap_left = before + 2;
  if (kind == -1) swap_left = before;
  cout << kept.size() << '\n';
  for (int i = 0; i < static_cast<int>(kept.size()); ++i) {
    cout << kept[i] << " \n"[i + 1 == static_cast<int>(kept.size())];
  }
  cout << swap_left << '\n';
}
```

时间、空间均为 $O(n)$；输出下标数也是 $O(n)$。

## Follow-up 2：交换必须发生在删除之前

新规则是先至多交换一次原数组中的相邻元素，再删除。此时交换后的最大可保留长度就是新数组的游程数。枚举交换边，只有它附近至多三条“是否相等”边会变化，可在 $O(1)$ 求增量。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  auto diff = [&](int i) {
    return i >= 0 && i + 1 < n && a[i] != a[i + 1];
  };
  int changes = 0;
  for (int i = 0; i + 1 < n; ++i) changes += diff(i);
  int ans = changes + 1;
  for (int p = 0; p + 1 < n; ++p) {
    vector<int> edges;
    for (int e = p - 1; e <= p + 1; ++e) {
      if (e >= 0 && e + 1 < n) edges.push_back(e);
    }
    int old = 0;
    for (int e : edges) old += diff(e);
    swap(a[p], a[p + 1]);
    int now = 0;
    for (int e : edges) now += diff(e);
    swap(a[p], a[p + 1]);
    ans = max(ans, changes - old + now + 1);
  }
  cout << ans << '\n';
}
```

时间复杂度 $O(n)$，空间复杂度 $O(n)$。原题允许跨过已删除元素交换，因此原题的 RLE 公式不能直接用于此变种。

## Follow-up 3：禁止删除，判断能否一次交换修好

新规则不允许删除，只问原数组能否通过至多一次相邻交换变成相邻全异。一次交换只能影响它附近三条边；取第一条相等边，只需尝试它前后常数个交换位置，再线性检查。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  auto valid = [&]() {
    for (int i = 1; i < n; ++i) {
      if (a[i] == a[i - 1]) return false;
    }
    return true;
  };
  if (valid()) {
    cout << "YES\n";
    return 0;
  }
  int bad = 0;
  while (a[bad] != a[bad + 1]) ++bad;
  for (int p = max(0, bad - 2); p <= min(n - 2, bad + 1); ++p) {
    swap(a[p], a[p + 1]);
    bool ok = valid();
    swap(a[p], a[p + 1]);
    if (ok) {
      cout << "YES\n";
      return 0;
    }
  }
  cout << "NO\n";
}
```

候选交换位置为常数个，每次检查 $O(n)$，所以总时间 $O(n)$，空间 $O(n)$。

## Follow-up 4：在线追加颜色并立即询问

初始序列为空；每次在末尾追加一个颜色后，输出当前原题答案。维护游程、相邻长游程见证数和增量 $1$ 见证数。追加只会改变尾部常数个游程的长度或“是否处于边界”，因此删除旧尾部贡献、修改 RLE、再加入新尾部贡献即可。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Run {
  int color;
  int length;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<Run> r;
  int cnt2 = 0, cnt1 = 0;
  auto two = [&](int i) {
    return i >= 0 && i + 1 < static_cast<int>(r.size()) &&
        r[i].length >= 2 && r[i + 1].length >= 2;
  };
  auto one = [&](int i) {
    int m = static_cast<int>(r.size());
    if (i < 0 || i >= m || r[i].length < 2) return false;
    bool right = i + 1 < m && (i + 2 >= m || r[i].color != r[i + 2].color);
    bool left = i > 0 && (i < 2 || r[i].color != r[i - 2].color);
    return right || left;
  };
  while (q--) {
    int x;
    cin >> x;
    int old_m = static_cast<int>(r.size());
    vector<int> affected;
    for (int i = max(0, old_m - 2); i <= old_m; ++i) affected.push_back(i);
    for (int i : affected) {
      cnt2 -= two(i);
      cnt1 -= one(i);
    }
    if (!r.empty() && r.back().color == x) {
      ++r.back().length;
    } else {
      r.push_back({x, 1});
    }
    for (int i : affected) {
      cnt2 += two(i);
      cnt1 += one(i);
    }
    int m = static_cast<int>(r.size());
    cout << m + (cnt2 ? 2 : cnt1 ? 1 : 0) << '\n';
  }
}
```

每次追加的摊还时间为 $O(1)$，总空间为 $O(m)$。与静态算法相比，难点是尾部从“边界”变成“内部”时，原来的增量 $1$ 见证可能失效，不能只在新游程上加贡献而不撤销旧贡献。

## 来源

- [Codeforces 官方题面](https://codeforces.com/contest/2253/problem/B)
- [Educational Codeforces Round 193 官方比赛页](https://codeforces.com/contest/2253)
- [Codeforces 官方 API](https://codeforces.com/api/contest.standings?contestId=2253)
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2253/problem/B)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-516-q1-lc4030/">← [力扣竞赛] 第 516 场周赛 Q1 LC 4030 判断 ASCII 值回文 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-26-lc2904/">[力扣每日一题] 2026-08-26｜LC 2904 最短且字典序最小的美丽子字符串 →</a>
</nav>
