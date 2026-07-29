---
title: "[atcoder] ABC468 A Maximal Value"
---

# [atcoder] ABC468 A Maximal Value

<p class="daily-archive-kicker">2026-07-26 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../basics/sequence-invariants.md">进入知识专题</a></p>

## Official source information

- Series and contest: AtCoder Beginner Contest 468 (ABC468)
- Division / task alias: ABC468 A
- Official title: Maximal Value
- Official difficulty: AtCoder does not publish a difficulty label on the task page
- Score: 100
- Time limit: 2 seconds
- Memory limit: 1024 MiB
- Official task: https://atcoder.jp/contests/abc468/tasks/abc468_a
- Official contest task list: https://atcoder.jp/contests/abc468/tasks
- Program interface: GNU++23 full program using standard input and output.
- Official image: the statement has no problem-specific diagram; the page's “Image” links are editorial-language controls rather than statement figures

### Original English statement

Open the [complete original English statement](https://atcoder.jp/contests/abc468/tasks/abc468_a?lang=en) on AtCoder.

> “You are given an integer sequence of length N.”

The official metadata, limits, input/output structure, and sample data are preserved below. The remaining prose is a faithful, complete teaching restatement.

### Faithful complete statement restatement

You are given an integer sequence $A=(A_1,A_2,\ldots,A_N)$ of length $N$. Count the indices $i$ with $1\le i\le N-2$ for which the middle of three consecutive elements is strictly greater than both neighbors:

$$
A_i<A_{i+1}>A_{i+2}.
$$

Print that count.

### Input

```text
N
A_1 A_2 ... A_N
```

### Output

Print one integer: the number of valid indices.

### All official constraints

- $3\le N\le100$
- $1\le A_i\le100$
- All input values are integers

### All official samples

Sample 1:

```text
Input
6
3 1 4 1 5 2
Output
2
```

The valid one-based indices are $i=2$ and $i=4$: the peaks are the values `4` and `5`.

Sample 2:

```text
Input
5
1 1 1 2 1
Output
1
```

Sample 3:

```text
Input
10
7 3 9 8 10 3 1 5 5 4
Output
2
```

## 中文题意

枚举每个长度为 3 的连续窗口，统计中间元素严格大于左右两侧元素的窗口数量。相等不算峰值。

## 最优结论

每个候选中心都由三个相邻值独立决定，只需扫描 `i = 1..N-2` 并检查 `A[i-1] < A[i] && A[i] > A[i+1]`。时间 $O(N)$、额外空间 $O(1)$；任何正确算法都必须在最坏情况下读取全部输入，因此达到 $\Omega(N)$ 下界。

## 约束与边界

- 候选中心只有数组下标 `1..N-2`；两端永远不能同时拥有左右邻居。
- 不等号严格，相邻相等时不是峰值。
- 每个中心至多贡献 1，答案不超过 $N-2\le98$，`int` 足够。
- 输入规模虽小，仍应直接体现局部判定，不需要排序或额外数据结构。

## 样例手推

样例 1 的三个连续窗口中心依次为 `1,4,1,5`。只有 `4` 满足 `1 < 4 > 1`，`5` 满足 `1 < 5 > 2`，答案为 2。

## 暴力基准：枚举所有三元位置再筛连续

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  int ans = 0;
  for (int l = 0; l < n; ++l) {
    for (int m = l + 1; m < n; ++m) {
      for (int r = m + 1; r < n; ++r) {
        if (m == l + 1 && r == m + 1 && a[l] < a[m] && a[m] > a[r]) ++ans;
      }
    }
  }
  cout << ans << '\n';
}
```

时间 $O(N^3)$，空间 $O(N)$（输入数组）。它枚举了大量不连续位置，未利用题目只关心长度为 3 的窗口。

## 最佳实用解：单次局部扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  int ans = 0;
  for (int i = 1; i + 1 < n; ++i) {
    if (a[i - 1] < a[i] && a[i] > a[i + 1]) ++ans;
  }
  cout << ans << '\n';
}
```

### 正确性证明

题目中的每个合法一基索引 $i$ 唯一对应零基中心 `i`，以及窗口 `(a[i-1],a[i],a[i+1])`。循环恰好访问全部内部中心一次；条件与官方不等式逐项相同，因此合法中心恰好被计数一次，非法中心不被计数。输出即为所求。

### 复杂度

时间 $O(N)$，保存输入时空间 $O(N)$；若流式维护最近三个数，可把额外空间降为 $O(1)$。

## 常见错误

- 把严格大于写成大于等于。
- 循环从 0 开始或走到 `n-1`，发生越界。
- 输出峰值本身的数量去重后结果，而不是峰值位置数量。
- 把任意局部最大值误解为需要大于数组所有其他元素。

## Follow-up 1：返回全部峰值位置

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  vector<int> positions;
  for (int i = 1; i + 1 < n; ++i) {
    if (a[i - 1] < a[i] && a[i] > a[i + 1]) positions.push_back(i + 1);
  }
  cout << positions.size() << '\n';
  for (int i = 0; i < (int)positions.size(); ++i) {
    if (i) cout << ' ';
    cout << positions[i];
  }
  cout << '\n';
}
```

时间 $O(N)$，除输出外空间 $O(1)$。

## Follow-up 2：平台型峰值

把一段相等的连续平台视作一个峰，当且仅当平台左右都存在且更低。扫描等值块而不是单个中心。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  int ans = 0;
  for (int l = 0; l < n;) {
    int r = l;
    while (r + 1 < n && a[r + 1] == a[l]) ++r;
    if (l > 0 && r + 1 < n && a[l - 1] < a[l] && a[r] > a[r + 1]) ++ans;
    l = r + 1;
  }
  cout << ans << '\n';
}
```

时间 $O(N)$，空间 $O(N)$（输入）。原算法逐中心判断会把平台全部判为非峰，因此必须改为分块。

## Follow-up 3：支持单点修改并随时查询峰值数

修改位置 `p` 只会影响中心 `p-1,p,p+1`，先删旧贡献、修改、再加新贡献。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class PeakCounter {
  vector<int> a;
  int peaks = 0;
  bool isPeak(int i) const {
    return 0 < i && i + 1 < (int)a.size() && a[i - 1] < a[i] && a[i] > a[i + 1];
  }
public:
  explicit PeakCounter(vector<int> values) : a(std::move(values)) {
    for (int i = 1; i + 1 < (int)a.size(); ++i) peaks += isPeak(i);
  }
  void update(int p, int value) {
    for (int i = p - 1; i <= p + 1; ++i) peaks -= isPeak(i);
    a[p] = value;
    for (int i = p - 1; i <= p + 1; ++i) peaks += isPeak(i);
  }
  int query() const {
    return peaks;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  PeakCounter counter(std::move(a));
  while (q--) {
    int p, x;
    cin >> p >> x;
    counter.update(p - 1, x);
    cout << counter.query() << '\n';
  }
}
```

预处理 $O(N)$，每次修改和查询 $O(1)$，空间 $O(N)$。

## Follow-up 4：二维网格中的严格峰值

定义一个格子严格大于存在的上、下、左、右邻居，枚举所有格子。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w;
  cin >> h >> w;
  vector<vector<int>> a(h, vector<int>(w));
  for (auto& row : a) {
    for (int& x : row) cin >> x;
  }
  const int dr[4] = {1, -1, 0, 0};
  const int dc[4] = {0, 0, 1, -1};
  int ans = 0;
  for (int r = 0; r < h; ++r) {
    for (int c = 0; c < w; ++c) {
      bool peak = true;
      for (int d = 0; d < 4; ++d) {
        int nr = r + dr[d], nc = c + dc[d];
        if (0 <= nr && nr < h && 0 <= nc && nc < w && a[r][c] <= a[nr][nc]) peak = false;
      }
      ans += peak;
    }
  }
  cout << ans << '\n';
}
```

时间 $O(HW)$，空间 $O(HW)$。

## 验证

主解逐条件对应官方定义，可用三重枚举基准对随机数组比较。测试应覆盖最小长度 3、严格单调、全相等、相邻双峰、峰在第一个或最后一个合法中心，以及数值边界 1 和 100。

## Reference

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_a)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="leetcode-top-1-lc3286.md">[力扣 Top 1] LC 3286 穿越网格图的安全路径 中等 →</a>
</nav>
