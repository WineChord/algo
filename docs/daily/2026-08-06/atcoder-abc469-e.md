---
title: "[atcoder] ABC469 E Pro Exam Eligibility"
---

# [atcoder] ABC469 E Pro Exam Eligibility

<p class="daily-archive-kicker">2026-08-06 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=774370faabd1e81be8430015cf73ed4a73fdf25953d34d7ff45db63ec9de50e5 -->
[Official problem: ABC469 E - Pro Exam Eligibility](https://atcoder.jp/contests/abc469/tasks/abc469_e?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 469。
- 题号与标题：E - Pro Exam Eligibility。
- 官方分值：475 分；官方未标注难度。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒；内存限制：1024 MiB。
- AtCoder Problems 社区估算难度：1566，检索于 2026-08-06。

## Complete English statement

### E. Pro Exam Eligibility

Takahashi played a game $N$ times. A string $S$ of length $N$ records the results: he won game $i$ exactly when $S_i$ is `o`, and lost it when $S_i$ is `x`. The string contains at least $K$ occurrences of `o`.

Choose a contiguous, nonempty interval of games $[l,r]$ such that

$$
1\le l\le r\le N
$$

and Takahashi won at least $K$ games in that interval. The win rate of the interval is the number of `o` characters in $S_l,S_{l+1},\ldots,S_r$ divided by its length $r-l+1$. Find the maximum possible win rate.

### Input

```text
N K
S
```

### Output

Print the maximum win rate. An answer is accepted when its absolute or relative error from the true answer is at most $10^{-6}$.

### Constraints

- $1\le K\le N\le10^6$.
- $N$ and $K$ are integers.
- $S$ has length $N$ and consists only of `o` and `x`.
- $S$ contains at least $K$ occurrences of `o`.

### Sample 1

```text
Input
10 4
oxooxoxxox

Output
0.6666666666
```

Choosing $(l,r)=(1,6)$ gives four wins in six games, hence a win rate of $2/3$. No eligible interval has a larger win rate.

### Sample 2

```text
Input
5 1
xxoxx

Output
1
```

### Sample 3

```text
Input
16 10
xxxoxooooxoxoooo

Output
0.769230769230769
```

There is no additional official note or required image. The English layer above is independently organized from the official statement while preserving the complete task semantics, input, output, constraints, samples, and official explanation. See the [AtCoder statement](https://atcoder.jp/contests/abc469/tasks/abc469_e?lang=en) and [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en).

## 中文题意

在只含胜 `o` 与负 `x` 的比赛记录中选一个连续区间。区间内至少有 $K$ 次胜利，目标最大化“胜利数 / 区间长度”。注意条件是至少 $K$ 次；最优区间可能包含更多胜利，不能只枚举恰好 $K$ 个 `o` 的窗口。

## 约束推导与观察

暴力枚举 $O(N^2)$ 个区间并用前缀和求胜率，仍无法承受 $N=10^6$。答案在 $(0,1]$，可二分候选胜率 $p$。把 `o` 赋值 $1-p$、`x` 赋值 $-p$，则区间和为

$$
\#o-p\cdot\text{length},
$$

其非负当且仅当区间胜率至少为 $p$。

对固定右端点 `r`，合法左端前缀下标 `t=l-1` 必须满足 `wins[r]-wins[t]>=K`。前缀胜数单调，因此合法 `t` 形成前缀 `[0,limit[r]]`；只需比较变换前缀和 `prefix[r]` 与该范围内的最小前缀和。`limit` 与 $p$ 无关，可预先用双指针求出。

## 解法递进

### 解法一：枚举全部区间

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  string s;
  cin >> n >> k >> s;
  vector<int> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    prefix[i + 1] = prefix[i] + (s[i] == 'o');
  }
  double answer = 0;
  for (int left = 0; left < n; ++left) {
    for (int right = left; right < n; ++right) {
      int wins = prefix[right + 1] - prefix[left];
      if (wins >= k) {
        answer = max(answer, static_cast<double>(wins) / (right - left + 1));
      }
    }
  }
  cout << fixed << setprecision(12) << answer << '\n';
}
```

时间 $O(N^2)$，空间 $O(N)$，仅用于小规模 oracle。

### 最佳实用解：答案二分 + 前缀最小值

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  string s;
  cin >> n >> k >> s;
  vector<int> wins(n + 1);
  for (int i = 0; i < n; ++i) {
    wins[i + 1] = wins[i] + (s[i] == 'o');
  }
  vector<int> limit(n + 1, -1);
  int pointer = 0;
  for (int right = 1; right <= n; ++right) {
    if (wins[right] < k) {
      continue;
    }
    int maximumWins = wins[right] - k;
    while (pointer + 1 < right && wins[pointer + 1] <= maximumWins) {
      ++pointer;
    }
    limit[right] = pointer;
  }
  vector<double> prefix(n + 1), minimum(n + 1);
  auto feasible = [&](double rate) {
    prefix[0] = minimum[0] = 0;
    for (int i = 1; i <= n; ++i) {
      prefix[i] = prefix[i - 1] + (s[i - 1] == 'o' ? 1.0 - rate : -rate);
      minimum[i] = min(minimum[i - 1], prefix[i]);
      if (limit[i] >= 0 && prefix[i] >= minimum[limit[i]]) {
        return true;
      }
    }
    return false;
  };
  double low = 0;
  double high = 1;
  for (int iteration = 0; iteration < 70; ++iteration) {
    double middle = (low + high) / 2;
    if (feasible(middle)) {
      low = middle;
    } else {
      high = middle;
    }
  }
  cout << fixed << setprecision(12) << low << '\n';
}
```

时间 $O(N\log(1/\varepsilon))$，70 轮约为 $7\times10^7$ 次线性操作；空间 $O(N)$。误差门槛下稳定可过，是推荐方案。整数精确分数或凸包方案证明负担更高，没有必要。

## 正确性证明

对任意区间，变换和非负等价于其胜率至少为二分值 $p$。固定右端 `r` 时，至少 $K$ 胜等价于 `wins[t]<=wins[r]-K`；单调前缀胜数保证所有可选 `t` 恰为 `[0,limit[r]]`。其中存在变换和非负区间，当且仅当 `prefix[r]` 不小于这段前缀中的最小值。因此 `feasible(p)` 准确判断答案是否至少为 $p$。可行性随 $p$ 增大单调不增，二分始终维护 `low` 可行、答案不大于 `high`，区间收敛后 `low` 与最优值误差远小于 $10^{-6}$。

## 样例手推

样例 1 在 $p=2/3$ 时，`o` 权重 $1/3$、`x` 权重 $-2/3$；区间 `[1,6]` 有 4 个 `o`、2 个 `x`，变换和为 0，故可行。若提高 $p$，所有至少 4 胜区间的变换和都为负。样例 3 的 `[4,16]` 有 10 胜、长度 13，得到 $10/13$。

## 易错点与方案比较

- “至少 $K$”不能改成“恰好 $K$”；`ooxoo`、$K=3$ 时全段 $4/5$ 优于任一三胜窗口。
- `limit` 是前缀下标 `l-1`，注意与一基区间转换。
- 行为值接近 0 时用 `double` 与充分迭代次数，不做相等判断。
- 前缀数组大小为 $N+1$；$N=10^6$ 时避免每轮重新分配。

## 变种一：同时恢复一个最优区间

二分后再运行一次检查，并为每个前缀最小值保存其下标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  string s;
  cin >> n >> k >> s;
  vector<int> wins(n + 1), limit(n + 1, -1);
  for (int i = 0; i < n; ++i) {
    wins[i + 1] = wins[i] + (s[i] == 'o');
  }
  int pointer = 0;
  for (int r = 1; r <= n; ++r) {
    if (wins[r] >= k) {
      while (pointer + 1 < r && wins[pointer + 1] <= wins[r] - k) {
        ++pointer;
      }
      limit[r] = pointer;
    }
  }
  vector<double> prefix(n + 1), minimum(n + 1);
  auto check = [&](double rate, pair<int, int>* interval) {
    vector<int> index(n + 1);
    prefix[0] = minimum[0] = 0;
    for (int i = 1; i <= n; ++i) {
      prefix[i] = prefix[i - 1] + (s[i - 1] == 'o' ? 1 - rate : -rate);
      if (prefix[i] < minimum[i - 1]) {
        minimum[i] = prefix[i];
        index[i] = i;
      } else {
        minimum[i] = minimum[i - 1];
        index[i] = index[i - 1];
      }
      if (limit[i] >= 0 && prefix[i] + 1e-12 >= minimum[limit[i]]) {
        if (interval) {
          *interval = {index[limit[i]] + 1, i};
        }
        return true;
      }
    }
    return false;
  };
  double low = 0, high = 1;
  for (int it = 0; it < 70; ++it) {
    double mid = (low + high) / 2;
    if (check(mid, nullptr))
      low = mid;
    else
      high = mid;
  }
  pair<int, int> interval;
  check(low - 1e-10, &interval);
  cout << fixed << setprecision(12) << low << '\n';
  cout << interval.first << ' ' << interval.second << '\n';
}
```

复杂度不变。

## 变种二：要求恰好 `K` 次胜利

此时两端都可收缩到 `o`，只需找覆盖连续 `K` 个 `o` 的最短跨度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  string s;
  cin >> n >> k >> s;
  vector<int> positions;
  for (int i = 0; i < n; ++i) {
    if (s[i] == 'o') {
      positions.push_back(i);
    }
  }
  int bestLength = n + 1;
  for (int i = 0; i + k <= static_cast<int>(positions.size()); ++i) {
    bestLength = min(bestLength, positions[i + k - 1] - positions[i] + 1);
  }
  cout << fixed << setprecision(12) << static_cast<double>(k) / bestLength << '\n';
}
```

时间、空间均为 $O(N)$；它不能解决原题的“至少”。

## 变种三：区间长度至少 `L`，不限制胜场数

候选率变换后，对每个右端只需查询 `prefix[0..r-L]` 的最小值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, minimumLength;
  string s;
  cin >> n >> minimumLength >> s;
  vector<double> prefix(n + 1);
  auto feasible = [&](double rate) {
    prefix[0] = 0;
    for (int i = 1; i <= n; ++i) {
      prefix[i] = prefix[i - 1] + (s[i - 1] == 'o' ? 1 - rate : -rate);
    }
    double minimum = 0;
    for (int right = minimumLength; right <= n; ++right) {
      minimum = min(minimum, prefix[right - minimumLength]);
      if (prefix[right] >= minimum) {
        return true;
      }
    }
    return false;
  };
  double low = 0, high = 1;
  for (int it = 0; it < 70; ++it) {
    double mid = (low + high) / 2;
    if (feasible(mid))
      low = mid;
    else
      high = mid;
  }
  cout << fixed << setprecision(12) << low << '\n';
}
```

时间 $O(N\log(1/\varepsilon))$，空间 $O(N)$。

## 变种四：每场有实数得分，且区间至少含 `K` 个合格标记

新定义：`score[i]` 替代 0/1 胜负，`qualified[i]` 决定计数条件；最大化平均得分。只需把变换权重改成 `score[i]-p`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  vector<double> score(n);
  vector<int> qualified(n), count(n + 1), limit(n + 1, -1);
  for (double& x : score)
    cin >> x;
  for (int& x : qualified)
    cin >> x;
  for (int i = 0; i < n; ++i)
    count[i + 1] = count[i] + qualified[i];
  int pointer = 0;
  for (int r = 1; r <= n; ++r) {
    if (count[r] >= k) {
      while (pointer + 1 < r && count[pointer + 1] <= count[r] - k)
        ++pointer;
      limit[r] = pointer;
    }
  }
  vector<double> prefix(n + 1), minimum(n + 1);
  auto feasible = [&](double average) {
    prefix[0] = minimum[0] = 0;
    for (int i = 1; i <= n; ++i) {
      prefix[i] = prefix[i - 1] + score[i - 1] - average;
      minimum[i] = min(minimum[i - 1], prefix[i]);
      if (limit[i] >= 0 && prefix[i] >= minimum[limit[i]])
        return true;
    }
    return false;
  };
  double low = *min_element(score.begin(), score.end());
  double high = *max_element(score.begin(), score.end());
  for (int it = 0; it < 70; ++it) {
    double mid = (low + high) / 2;
    if (feasible(mid))
      low = mid;
    else
      high = mid;
  }
  cout << fixed << setprecision(12) << low << '\n';
}
```

时间 $O(N\log(1/\varepsilon))$，空间 $O(N)$。

## 可复现验证

对 $N\le18$ 的随机 `o/x` 字符串和全部合法 $K$，用二次区间枚举作 oracle，对比二分答案误差不超过 $10^{-9}$；固定加入 `ooxoo,K=3` 反例、全 `o`、单个 `o`、长前后缀 `x`。发布程序通过 GNU++23 编译与三组官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_e?lang=en)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-111-lc189/">[力扣 Top 111] LC 189 轮转数组 中等 →</a>
</nav>
