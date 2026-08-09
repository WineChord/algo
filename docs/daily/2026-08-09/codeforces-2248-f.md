---
title: "[codeforces] CF Round 1113 Div.2 F Matrix Elimination"
---

# [codeforces] CF Round 1113 Div.2 F Matrix Elimination

<p class="daily-archive-kicker">2026-08-09 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0a14ac164a2cc3b738afbf13cc76568883cb6564eb1f1de806a20be2bf99a28f -->
[Official problem: Codeforces 2248F - Matrix Elimination](https://codeforces.com/contest/2248/problem/F)

## 官方来源与元数据

- 比赛：Codeforces Round 1113 (Div. 2)，比赛 ID 2248。
- 题号与标题：Div.2 F - Matrix Elimination。
- 官方分值：2500；官方 rating：2500。
- 官方标签：binary search、greedy、math。
- 时间限制：2 秒；内存限制：256 MB。

## Complete English statement

### F. Matrix Elimination

You are given an integer $k$ and an integer matrix $v$ with $n$ rows and $m$ columns. The element in row $i$ and column $j$ is denoted by $v_{i,j}$.

A cell $(x,y)$ is a peak when its value is at least the sum of every other value in row $x$ and column $y$:

$$
v_{x,y}\ge
\sum_{\substack{1\le i\le n\\i\ne x}}v_{i,y}
+
\sum_{\substack{1\le j\le m\\j\ne y}}v_{x,j}.
$$

You may perform the following operation any number of times, possibly zero:

1. Choose integers $x_l,x_r,y_l,y_r$ satisfying $1\le x_l\le x_r\le n$ and $1\le y_l\le y_r\le m$.
2. Subtract $1$ from every $v_{i,j}$ with $x_l\le i\le x_r$ and $y_l\le j\le y_r$.

Find the minimum number of operations needed to obtain at least $k$ peaks. If no solution exists, print $-1$.

### Input

The first line contains the number of test cases $t$ ($1\le t\le10^4$). For each test case:

```text
n m k
v_1,1 v_1,2 ... v_1,m
...
v_n,1 v_n,2 ... v_n,m
```

The constraints are:

- $1\le n,m\le10^5$.
- $1\le k\le nm$.
- $nm\le10^5$ for each test case.
- $-10^9\le v_{i,j}\le10^9$.
- The sum of $nm$ over all test cases does not exceed $10^5$.

### Output

For each test case, print the minimum number of operations, or $-1$ if it is impossible.

### Complete official sample

```text
Input
16
3 3 7
-1 -30 7
6 -3 22
1 -18 16
3 1 2
100000000
300000000
200000000
1 3 1
2 3 4
1 3 1
1 2 3
1 2 2
5 7
5 2 8
531959596 -61416172
425363565 672913308
981527099 451180253
-161687136 898803495
-388356105 897723313
1 1 1
0
1 1 1
-5
1 4 3
-8 -4 4 -11
1 9 5
-12 -4 -13 9 -1 -15 6 -15 -4
1 3 3
-12 -15 8
1 5 5
10 8 -4 0 -4
1 3 3
12 9 -1
1 3 3
-14 11 -6
1 6 6
-1 0 15 3 1 -14
1 2 2
1000000000 -1000000000

Output
2
100000000
1
0
2
734592698
0
-1
0
0
11
6
12
11
7
2000000000
```

### Complete official note

For the first test case, two valid operations are $(1,3,2,3)$ and $(2,3,1,3)$. They produce

| $-1$ | $-31$ | $6$ |
|---:|---:|---:|
| $5$ | $-5$ | $20$ |
| $0$ | $-20$ | $14$ |

The seven peaks are $(1,1),(1,3),(2,2),(2,3),(3,1),(3,2),(3,3)$. In particular, $-1\ge5+0-31+6=-20$ for $(1,1)$, and $0\ge-20+14-1+5=-2$ for $(3,1)$. Cell $(2,1)$ is not a peak because $5<-5+20-1+0=14$. Fewer than two operations cannot create seven peaks.

In the eighth test case the only cell is $-5$. A $1\times1$ cell is a peak exactly when it is nonnegative, and operations can only decrease it, so no solution exists. In the last test case both cells are peaks exactly when their values are equal; reducing $10^9$ to $-10^9$ needs $2\times10^9$ operations.

Codeforces is the source of the statement. The official problem is linked above; publication follows the [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967). No hidden tests, validators, generators, or separate image assets are reproduced.

## 中文题意

一次操作把任意连续子矩形整体减 1。某格若不小于同一行、同一列其余所有格之和，就叫峰值。目标用最少操作制造至少 $k$ 个峰值。矩阵可能退化成一行、一列，甚至单格，这些情形的最优操作与真正二维矩阵不同。

## 约束推导与观察

记行和、列和为 $R_x,C_y$。峰值条件等价于

$$
3v_{x,y}\ge R_x+C_y.
$$

定义缺口 $g_{x,y}=R_x+C_y-3v_{x,y}$，峰值当且仅当 $g_{x,y}\le0$。行列和、缺口与答案都可能超过 32 位，统一用 `long long`。

当 $n,m\ge2$ 时，一次整矩阵操作把每格缺口都减少 $n+m-3$，并逐格支配任何局部子矩形操作。因此只需给每格计算成为峰值所需的整矩阵操作数，取第 $k$ 小。

一维长度 $L$ 时，设总和为 $S$、元素为 $a_i$，缺口为 $h_i=S-2a_i$。长度不超过 $L-2$ 的区间操作被整段操作支配；只需考虑整段、遗漏首元素的长度 $L-1$ 区间、遗漏尾元素的长度 $L-1$ 区间。

## 解法递进

### 解法一：小矩阵上按操作层数 BFS

下面的定义级搜索枚举所有子矩形操作；除单格负数外，其余情形最终会找到答案，但状态爆炸，只能作极小 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int peakCount(const vector<long long>& state, int n, int m) {
  vector<long long> row(n), column(m);
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      row[i] += state[i * m + j];
      column[j] += state[i * m + j];
    }
  }
  int count = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      count += 3 * state[i * m + j] >= row[i] + column[j];
    }
  }
  return count;
}
int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<long long> initial(n * m);
  for (long long& x : initial) {
    cin >> x;
  }
  if (n * m == 1 && initial[0] < 0) {
    cout << -1 << '\n';
    return 0;
  }
  queue<pair<vector<long long>, int>> queue;
  set<vector<long long>> visited{initial};
  queue.push({initial, 0});
  while (!queue.empty()) {
    auto [state, distance] = queue.front();
    queue.pop();
    if (peakCount(state, n, m) >= k) {
      cout << distance << '\n';
      return 0;
    }
    for (int top = 0; top < n; ++top) {
      for (int bottom = top; bottom < n; ++bottom) {
        for (int left = 0; left < m; ++left) {
          for (int right = left; right < m; ++right) {
            vector<long long> next = state;
            for (int i = top; i <= bottom; ++i) {
              for (int j = left; j <= right; ++j) {
                --next[i * m + j];
              }
            }
            if (visited.insert(next).second) {
              queue.push({move(next), distance + 1});
            }
          }
        }
      }
    }
  }
}
```

分支数 $O(n^2m^2)$，状态数随答案指数增长，仅用于验证小值域、小答案实例。

### 解法二：非退化二维矩阵的第 `k` 小缺口

这个版本完整解决 $n,m\ge2$ 的子问题，先展示核心支配结构。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long ceilDivide(long long value, long long positiveDivisor) {
  if (value >= 0) {
    return (value + positiveDivisor - 1) / positiveDivisor;
  }
  return value / positiveDivisor;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, m, k;
    cin >> n >> m >> k;
    vector<vector<long long>> value(n, vector<long long>(m));
    vector<long long> row(n), column(m);
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < m; ++j) {
        cin >> value[i][j];
        row[i] += value[i][j];
        column[j] += value[i][j];
      }
    }
    vector<long long> need;
    long long gain = n + m - 3;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < m; ++j) {
        long long deficit = row[i] + column[j] - 3 * value[i][j];
        need.push_back(max(0LL, ceilDivide(deficit, gain)));
      }
    }
    nth_element(need.begin(), need.begin() + k - 1, need.end());
    cout << need[k - 1] << '\n';
  }
}
```

期望时间 $O(nm)$、空间 $O(nm)$。原题还含一维输入，不能直接提交这一受限版本。

### 最佳实用解：二维支配公式 + 一维端点特判

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
const int64 INF = 4'000'000'000'000'000'000LL;
int64 ceilDivide(int64 value, int64 positiveDivisor) {
  if (value >= 0) {
    return (value + positiveDivisor - 1) / positiveDivisor;
  }
  return value / positiveDivisor;
}
int64 endpointStrategy(vector<int64> others, int64 endpoint, int64 sum, int k) {
  int length = others.size() + 1;
  if (k == 1) {
    return max(0LL, ceilDivide(sum - 2 * endpoint, length - 1));
  }
  sort(others.rbegin(), others.rend());
  int64 thresholdValue = others[k - 2];
  int64 operations = max({0LL, ceilDivide(sum - endpoint - thresholdValue, length - 2),
      ceilDivide(sum - 2 * endpoint, length - 1)});
  int64 lower = max(0LL, sum - 2 * endpoint - (length - 2) * operations);
  int64 upper = min(operations, (length - 2) * operations - (sum - 2 * thresholdValue));
  return lower <= upper ? operations : INF;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, m, k;
    cin >> n >> m >> k;
    vector<vector<int64>> value(n, vector<int64>(m));
    vector<int64> row(n), column(m), flat;
    int64 total = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < m; ++j) {
        cin >> value[i][j];
        row[i] += value[i][j];
        column[j] += value[i][j];
        total += value[i][j];
        flat.push_back(value[i][j]);
      }
    }
    if (n + m <= 3) {
      sort(flat.begin(), flat.end());
      if (flat.size() == 1) {
        cout << (flat[0] >= 0 ? 0 : -1) << '\n';
      } else if (k == 1) {
        cout << 0 << '\n';
      } else {
        cout << flat[1] - flat[0] << '\n';
      }
      continue;
    }
    int64 gain = n + m - 3;
    vector<int64> need;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < m; ++j) {
        int64 deficit = row[i] + column[j] - 3 * value[i][j];
        need.push_back(max(0LL, ceilDivide(deficit, gain)));
      }
    }
    sort(need.begin(), need.end());
    int64 answer = need[k - 1];
    if (n == 1 || m == 1) {
      vector<int64> withoutLast(flat.begin(), flat.end() - 1);
      vector<int64> withoutFirst(flat.begin() + 1, flat.end());
      answer = min(answer, endpointStrategy(withoutLast, flat.back(), total, k));
      answer = min(answer, endpointStrategy(withoutFirst, flat.front(), total, k));
    }
    cout << answer << '\n';
  }
}
```

时间 $O(nm\log(nm))$、空间 $O(nm)$；总元素数不超过 $10^5$，可以稳定通过。二维部分可用 `nth_element` 降为期望线性，但统一排序便于一维选择其余最大值，证明和实现更一致。

## 正确性证明

### 二维情形

若操作矩形在某格的同行覆盖 $a$ 个单元、同列覆盖 $b$ 个单元：格在矩形内时，其缺口减少 $a+b-3$；不在矩形内时，最多只覆盖同行或同列，缺口减少至多 $\max(n-1,m-1)$。当 $n,m\ge2$，两者都不超过 $n+m-3$。整矩阵操作对每格都恰减少 $n+m-3$，所以逐格支配任意局部操作。

经过 $T$ 次操作，一格成为峰值必须满足 $g\le T(n+m-3)$；反过来 $T$ 次整矩阵操作同时让所有满足该式的格成为峰值。因此每格所需次数为

$$
need_{x,y}=\max\left(0,\left\lceil\frac{R_x+C_y-3v_{x,y}}{n+m-3}\right\rceil\right),
$$

至少 $k$ 格的最小次数就是第 $k$ 小 `need`。

### 一维情形

长度 $L\ge3$ 时，整段操作让每个缺口减少 $L-2$。长度 $\ell\le L-2$ 的区间，对区间内格减少 $\ell-2$、区间外格减少 $\ell$，均被整段操作支配。剩下的长度 $L-1$ 区间只有“漏首”“漏尾”两种。若两种都用了正次数，把相同数量的一对替换为两次整段操作，两个端点收益不变、中间格更优，所以最优解只需一种端点操作。

固定端点 $p$，总操作数为 $T$、其中 $y$ 次遗漏该端点。端点缺口减少 $(L-2)T+y$，其余格减少 $(L-2)T-y$。若端点成为峰值，另外 $k-1$ 格显然选值最大的那些；设其中最小值为 $v_k$。可行性等价于

$$
\begin{aligned}
(L-2)T+y&\ge S-2a_p,\\
(L-2)T-y&\ge S-2v_k,\\
0&\le y\le T.
\end{aligned}
$$

`endpointStrategy` 由这三个线性不等式求最小候选 $T$ 并检查整数区间是否非空。再与只用整段操作、左右两个端点策略取最小，覆盖所有未被支配的方案。$L=1,2$ 按定义直接求解，故统一算法正确。

## 样例手推

第一组 $n=m=3$，每次整矩阵操作的统一缺口收益为 3。计算九个初始缺口后，第七小所需次数为 2，因此两次足够；官方给出的两个局部操作也达到同一最优值。单格 `-5` 的峰值条件是 `-5>=0`，操作只会更小，故无解。两元素 `[10^9,-10^9]` 要让两者同时为峰值只能使它们相等，需要对较大者做 $2\times10^9$ 次单格操作。

## 易错点与方案比较

- 不能把二维公式直接用于 $n+m-3\le0$；单格、两元素必须先特判。
- 一维 $L\ge3$ 时只做整段操作并不总最优，长度 $L-1$ 的端点增强必须保留。
- 向上取整要正确处理负分子；本实现随后与 0 取最大。
- 所有和、乘积、阈值与答案使用 `long long`；官方样例已有 $2\times10^9$。

## 变种一：输出压缩的最优操作计划

新定义：一维数组除最少次数外，输出“区间 + 重复次数”，避免答案很大时逐次展开。闭式不等式还能恢复可行的 `y`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
const int64 INF = 4'000'000'000'000'000'000LL;
int64 ceilDiv(int64 x, int64 d) {
  return x >= 0 ? (x + d - 1) / d : x / d;
}
pair<int64, int64> endpointPlan(vector<int64> others, int64 endpoint, int64 sum, int k) {
  int length = others.size() + 1;
  if (k == 1) {
    int64 operations = max(0LL, ceilDiv(sum - 2 * endpoint, length - 1));
    return {operations, operations};
  }
  sort(others.rbegin(), others.rend());
  int64 value = others[k - 2];
  int64 operations = max(
      {0LL, ceilDiv(sum - endpoint - value, length - 2), ceilDiv(sum - 2 * endpoint, length - 1)});
  int64 lower = max(0LL, sum - 2 * endpoint - (length - 2) * operations);
  int64 upper = min(operations, (length - 2) * operations - sum + 2 * value);
  return lower <= upper ? pair{operations, lower} : pair{INF, 0LL};
}
int main() {
  int length, k;
  cin >> length >> k;
  vector<int64> a(length), need;
  int64 sum = 0;
  for (int64& x : a) {
    cin >> x;
    sum += x;
  }
  if (length <= 2) {
    if (length == 1) {
      cout << (a[0] >= 0 ? 0 : -1) << '\n';
    } else if (k == 1) {
      cout << 0 << '\n';
    } else {
      cout << llabs(a[0] - a[1]) << " operations on the larger singleton\n";
    }
    return 0;
  }
  for (int64 x : a) {
    need.push_back(max(0LL, ceilDiv(sum - 2 * x, length - 2)));
  }
  sort(need.begin(), need.end());
  tuple<int64, int, int64> best{need[k - 1], -1, 0};
  vector<int64> withoutFirst(a.begin() + 1, a.end());
  auto [leftTotal, leftSkip] = endpointPlan(withoutFirst, a.front(), sum, k);
  best = min(best, tuple{leftTotal, 0, leftSkip});
  vector<int64> withoutLast(a.begin(), a.end() - 1);
  auto [rightTotal, rightSkip] = endpointPlan(withoutLast, a.back(), sum, k);
  best = min(best, tuple{rightTotal, 1, rightSkip});
  auto [total, side, skip] = best;
  cout << total << '\n';
  if (total - skip > 0) {
    cout << "1 " << length << ' ' << total - skip << '\n';
  }
  if (skip > 0 && side == 0) {
    cout << "2 " << length << ' ' << skip << '\n';
  }
  if (skip > 0 && side == 1) {
    cout << "1 " << length - 1 << ' ' << skip << '\n';
  }
}
```

时间 $O(L\log L)$、空间 $O(L)$，计划最多含两种区间。

## 变种二：固定二维矩阵，多次询问不同的 `k`

新定义：保证 $n,m\ge2$，矩阵不变，回答多个峰值数量询问。排序一次 `need`，每次直接取下标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long ceilDiv(long long x, long long d) {
  return x >= 0 ? (x + d - 1) / d : x / d;
}
int main() {
  int n, m, queries;
  cin >> n >> m >> queries;
  vector<vector<long long>> a(n, vector<long long>(m));
  vector<long long> row(n), column(m), need;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> a[i][j];
      row[i] += a[i][j];
      column[j] += a[i][j];
    }
  }
  long long gain = n + m - 3;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      need.push_back(max(0LL, ceilDiv(row[i] + column[j] - 3 * a[i][j], gain)));
    }
  }
  sort(need.begin(), need.end());
  while (queries--) {
    int k;
    cin >> k;
    cout << need[k - 1] << '\n';
  }
}
```

预处理 $O(nm\log(nm))$，每次询问 $O(1)$，空间 $O(nm)$。

## 变种三：峰值必须额外领先 `margin`

新定义：保证 $n,m\ge2$，要求目标格至少比同行同列其余和大 `margin`。只需把每格缺口增加 `margin`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long ceilDiv(long long x, long long d) {
  return x >= 0 ? (x + d - 1) / d : x / d;
}
int main() {
  int n, m, k;
  long long margin;
  cin >> n >> m >> k >> margin;
  vector<vector<long long>> a(n, vector<long long>(m));
  vector<long long> row(n), column(m), need;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> a[i][j];
      row[i] += a[i][j];
      column[j] += a[i][j];
    }
  }
  long long gain = n + m - 3;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      long long deficit = row[i] + column[j] - 3 * a[i][j] + margin;
      need.push_back(max(0LL, ceilDiv(deficit, gain)));
    }
  }
  nth_element(need.begin(), need.begin() + k - 1, need.end());
  cout << need[k - 1] << '\n';
}
```

期望时间 $O(nm)$、空间 $O(nm)$；支配证明完全不变。

## 变种四：只有指定候选格可以计入 `k` 个峰值

新定义：保证 $n,m\ge2$，另给同形状 0/1 掩码；只有掩码为 1 的峰值计数。整矩阵仍同时支配所有候选格，只对候选格收集 `need`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long ceilDiv(long long x, long long d) {
  return x >= 0 ? (x + d - 1) / d : x / d;
}
int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<vector<long long>> a(n, vector<long long>(m));
  vector<long long> row(n), column(m), need;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> a[i][j];
      row[i] += a[i][j];
      column[j] += a[i][j];
    }
  }
  vector<vector<int>> allowed(n, vector<int>(m));
  long long gain = n + m - 3;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> allowed[i][j];
      if (allowed[i][j]) {
        long long deficit = row[i] + column[j] - 3 * a[i][j];
        need.push_back(max(0LL, ceilDiv(deficit, gain)));
      }
    }
  }
  if (static_cast<int>(need.size()) < k) {
    cout << -1 << '\n';
  } else {
    nth_element(need.begin(), need.begin() + k - 1, need.end());
    cout << need[k - 1] << '\n';
  }
}
```

期望时间 $O(nm)$、空间 $O(nm)$。

## 可复现验证

官方 16 组样例全部通过。另对一维长度 $1..5$、元素值域 `-2..2` 的 18,555 个“数组、$k$”组合，与最多六步 BFS 穷举完全一致；对 $2\times2$、$2\times3$、$3\times2$ 小矩阵共 9,072 个实例，与最多四步子矩形 BFS 完全一致。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/F)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-188-q1-lc4006/">← [力扣竞赛] 第 188 场双周赛 Q1 LC 4006 统计有效前缀数目 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-09-lc1140/">[力扣每日一题] 2026-08-09｜LC 1140 石子游戏 II →</a>
</nav>
