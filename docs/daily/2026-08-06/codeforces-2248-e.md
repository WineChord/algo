---
title: "[codeforces] CF Round 1113 Div.2 E Excuse for Breaks"
---

# [codeforces] CF Round 1113 Div.2 E Excuse for Breaks

<p class="daily-archive-kicker">2026-08-06 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=53ff20519054949fec06cdf05d9525d09833cc003bc5cc945c8458891557a376 -->
[Official problem: Codeforces 2248E - Excuse for Breaks](https://codeforces.com/contest/2248/problem/E)

## 官方来源与元数据

- 比赛：Codeforces Round 1113 (Div. 2)，Contest ID 2248。
- 题号与别名：Div.2 E。
- 官方标题：Excuse for Breaks。
- 官方分值：2500；官方 rating：1900。
- 官方标签：binary search、brute force、greedy、math、two pointers。
- 时间限制：2 秒；内存限制：256 MB。

## Complete English statement

### E. Excuse for Breaks

For each test case, three integers $n,m,d$ and two arrays $p_1<p_2<\cdots<p_m$ and $r_1,r_2,\ldots,r_m$ are given. For any positive finite binary array $a$—its length does not have to equal $n$—define $f(a)$ by the following procedure.

```text
function f(a):
  v := 0
  c := 0
  for i from 1 to length(a):
    if a[i] is equal to 1:
      v := v + d
      c := c + 1
    else:
      c := 0
    for j from 1 to m:
      if c is equal to p[j]:
        v := v + r[j]
    if c is equal to n:
      c := 0
  return v
```

Here `:=` denotes assignment. In particular, a reward at $p_j=n$ is added before the counter is reset.

Let $I(a)$ be the all-one array of length $|a|$. Determine whether there exists a binary array $a$ such that

$$
f(a)>f(I(a)).
$$

### Input

The first line contains the number of test cases $t$. Each test case starts with `n m d`, followed by $m$ lines `p_i r_i`.

### Output

For each test case print `YES` if such an array exists, otherwise print `NO`. Letter case is ignored.

### Constraints

- $1\le t\le2000$.
- $1\le n\le10^9$.
- $0\le m\le2000$.
- $0\le d\le10^9$.
- $1\le p_i\le n$ and $1\le r_i\le10^9$.
- $p$ is strictly increasing.
- The sum of $m$ over all test cases is at most 2000.

### Sample

```text
Input
3
6 4 3
2 5
3 9
4 1
5 3
7 3 5
2 5
4 5
7 10
684492057 3 386217943
367971233 991739271
612599954 429216213
684492056 402931836

Output
YES
NO
YES
```

For the first test case, one witness is

```text
[1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1].
```

It has 16 ones, contributing $16\cdot3=48$. Its one-runs have lengths 9, 4, and 3 and contribute rewards 32, 15, and 14, so its total value is 109. The all-one array of length 18 consists of three complete counter cycles; each contributes $6\cdot3+5+9+1+3=36$, so its value is 108. No winning array exists in the second test case; the official note gives no additional explanation for the third.

There is no required image. The statement is presented under the [Codeforces source](https://codeforces.com/contest/2248/problem/E) and [Codeforces Materials Usage License](https://codeforces.com/blog/entry/967).

## 中文题意

连续读 1 会累加基础分 `d` 与命中奖励点 `p_i` 的奖励；读到 0 或连续 1 计数达到 `n` 后，计数器归零。要判断能否插入某些 0，让某个二进制串的得分严格超过同长度全 1 串。数组长度任意，不固定为 `n`。

## 约束推导与观察

记 $S_x=f(I(x))$，$S_0=0$。计数器每 $n$ 个 1 自动归零，因此

$$
S_{x+n}=S_x+S_n.
$$

零会把前后两段 1 的得分完全分开。若某个串能获胜，按第一个零拆成 $I(x),0,t$；归纳可证明全部收益都由某一次拆分控制。定义

$$
M=\max_{x,y\ge1}(S_x+S_y-S_{x+y+1}),
$$

则存在答案当且仅当 $M>0$，且一个零的串 $I(x),0,I(y)$ 已足够作见证。

函数对每个变量以 $n$ 为周期变化。固定 `y` 时，差值只有当 `x+1` 经过奖励点才可能向上跳，所以某个最大值可在 `x=p_i` 取得；对 `y` 同理。于是只需枚举奖励点对：

$$
M=\max_{i,j}(S_{p_i}+S_{p_j}-S_{p_i+p_j+1}).
$$

若 $m=0$，则 $M=-d\le0$。

## 解法递进

### 解法一：小 `n` 枚举所有余数对

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  long long d;
  cin >> n >> m >> d;
  vector<long long> reward(n + 1);
  for (int i = 0, p; i < m; ++i) {
    long long r;
    cin >> p >> r;
    reward[p] += r;
  }
  vector<long long> prefix(n + 1);
  for (int i = 1; i <= n; ++i) {
    prefix[i] = prefix[i - 1] + d + reward[i];
  }
  auto value = [&](long long length) { return length / n * prefix[n] + prefix[length % n]; };
  bool possible = false;
  for (int x = 1; x <= n; ++x) {
    for (int y = 1; y <= n; ++y) {
      possible |= value(x) + value(y) > value(x + y + 1);
    }
  }
  cout << (possible ? "YES\n" : "NO\n");
}
```

时间 $O(n^2)$、空间 $O(n)$，只适用于小 `n` 的 oracle。

### 最佳实用解：只枚举奖励点对

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    long long n, d;
    int m;
    cin >> n >> m >> d;
    vector<long long> p(m), r(m), rewardPrefix(m + 1), score(m);
    for (int i = 0; i < m; ++i) {
      cin >> p[i] >> r[i];
      rewardPrefix[i + 1] = rewardPrefix[i] + r[i];
      score[i] = p[i] * d + rewardPrefix[i + 1];
    }
    long long cycleScore = n * d + rewardPrefix[m];
    bool possible = false;
    for (int i = 0; i < m && !possible; ++i) {
      long long currentCycle = -1;
      int pointer = 0;
      for (int j = 0; j < m; ++j) {
        long long length = p[i] + p[j] + 1;
        long long cycles = length / n;
        long long remainder = length % n;
        if (cycles != currentCycle) {
          currentCycle = cycles;
          pointer = 0;
        }
        while (pointer < m && p[pointer] <= remainder) {
          ++pointer;
        }
        long long wholeScore = cycles * cycleScore + remainder * d;
        wholeScore += rewardPrefix[pointer];
        if (score[i] + score[j] > wholeScore) {
          possible = true;
          break;
        }
      }
    }
    cout << (possible ? "YES\n" : "NO\n");
  }
}
```

对固定 `i`，`p_i+p_j+1` 单调，跨越周期时重置奖励指针，故每行总指针移动 $O(m)$。总时间 $O(m^2)$，空间 $O(m)$；结合 $\sum m\le2000$ 可通过。直接对每对 `upper_bound` 为 $O(m^2\log m)$，更短但不是最优。

## 正确性证明

对任意含零串，按第一个零写成 $I(x),0,t$。零使两侧计数器独立，故 $f= S_x+f(t)$。若所有两段差都不超过 0，则归纳得到任意串得分不超过同长度全 1 串；若某对差大于 0，$I(x),0,I(y)$ 立即构成见证。因此判定等价于 $M>0$。周期性与奖励点跳变保证某个最优 `x,y` 分别等于奖励点，算法枚举全部这样的点对并精确计算三个 $S$ 值，所以不会漏掉见证，也不会接受不存在的见证。

## 样例手推

样例 1 选择 `x=9,y=4` 后再接另一段可形成官方见证；核心局部差来自“在奖励点前主动归零，使早期奖励再次触发”。样例 2 对三个奖励点的全部 9 对计算都不产生正差，故答案 `NO`。`m=0` 时插入一个零只损失同长度全 1 串的一次基础分，必为 `NO`。

## 易错点与方案比较

- 目标是严格 `>`，差等于 0 仍输出 `NO`。
- 奖励检查发生在 `c==n` 重置之前，`p_i=n` 的奖励必须计入。
- `a` 的长度任意；不能只比较长度 `n`。
- `n*d` 和奖励和使用 64 位；本题上界仍在有符号 64 位内。
- `m=0` 无奖励行，应直接自然得到 `NO`。

## 变种一：输出一个最短见证

新定义：存在时输出长度最短的 `I(p_i),0,I(p_j)`；枚举所有盈利点对并最小化长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n, d;
  int m;
  cin >> n >> m >> d;
  vector<long long> p(m), prefix(m + 1), score(m);
  for (int i = 0; i < m; ++i) {
    long long reward;
    cin >> p[i] >> reward;
    prefix[i + 1] = prefix[i] + reward;
    score[i] = p[i] * d + prefix[i + 1];
  }
  long long cycle = n * d + prefix[m];
  pair<long long, pair<int, int>> best{LLONG_MAX, {-1, -1}};
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < m; ++j) {
      long long length = p[i] + p[j] + 1;
      long long remainder = length % n;
      int count = upper_bound(p.begin(), p.end(), remainder) - p.begin();
      long long whole = length / n * cycle + remainder * d + prefix[count];
      if (score[i] + score[j] > whole) {
        best = min(best, {length, {i, j}});
      }
    }
  }
  if (best.second.first == -1) {
    cout << "NO\n";
  } else {
    cout << "YES\n" << best.first << '\n';
    cout << p[best.second.first] << ' ' << p[best.second.second] << '\n';
  }
}
```

时间 $O(m^2\log m)$，空间 $O(m)$；只输出段长，避免构造可能长达 $10^9$ 的数组。

## 变种二：求最大可获得的严格优势值

新定义：输出 $\max(0,M)$，不仅判断存在性。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n, d;
  int m;
  cin >> n >> m >> d;
  vector<long long> p(m), prefix(m + 1), score(m);
  for (int i = 0; i < m; ++i) {
    long long reward;
    cin >> p[i] >> reward;
    prefix[i + 1] = prefix[i] + reward;
    score[i] = p[i] * d + prefix[i + 1];
  }
  long long cycle = n * d + prefix[m];
  long long answer = 0;
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < m; ++j) {
      long long length = p[i] + p[j] + 1;
      long long remainder = length % n;
      int count = upper_bound(p.begin(), p.end(), remainder) - p.begin();
      long long whole = length / n * cycle + remainder * d + prefix[count];
      answer = max(answer, score[i] + score[j] - whole);
    }
  }
  cout << answer << '\n';
}
```

时间 $O(m^2\log m)$，空间 $O(m)$。

## 变种三：同一奖励表回答很多 `d` 查询

基础分对差值的贡献恒为 $d(x+y-(x+y+1))=-d$。先令 `d=0` 求最大奖励优势 `bonus`，每问只判断 `bonus>d`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n;
  int m, q;
  cin >> n >> m >> q;
  vector<long long> p(m), prefix(m + 1);
  for (int i = 0; i < m; ++i) {
    long long reward;
    cin >> p[i] >> reward;
    prefix[i + 1] = prefix[i] + reward;
  }
  long long bonus = 0;
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < m; ++j) {
      long long length = p[i] + p[j] + 1;
      long long remainder = length % n;
      int count = upper_bound(p.begin(), p.end(), remainder) - p.begin();
      long long wholeReward = length / n * prefix[m] + prefix[count];
      bonus = max(bonus, prefix[i + 1] + prefix[j + 1] - wholeReward);
    }
  }
  while (q--) {
    long long d;
    cin >> d;
    cout << (bonus > d ? "YES\n" : "NO\n");
  }
}
```

预处理 $O(m^2\log m)$，每问 $O(1)$。

## 变种四：求杜绝任何插零获利所需的最小基础分

由 $M=bonus-d$，最小非负整数 `d` 使所有数组都无法严格获利，恰为 `bonus`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n;
  int m;
  cin >> n >> m;
  vector<long long> p(m), prefix(m + 1);
  for (int i = 0; i < m; ++i) {
    long long reward;
    cin >> p[i] >> reward;
    prefix[i + 1] = prefix[i] + reward;
  }
  long long required = 0;
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < m; ++j) {
      long long length = p[i] + p[j] + 1;
      long long remainder = length % n;
      int count = upper_bound(p.begin(), p.end(), remainder) - p.begin();
      long long whole = length / n * prefix[m] + prefix[count];
      required = max(required, prefix[i + 1] + prefix[j + 1] - whole);
    }
  }
  cout << required << '\n';
}
```

时间 $O(m^2\log m)$，空间 $O(m)$。

## 可复现验证

对 `n<=12`、随机奖励点和小分值，枚举 `x,y=1..n` 作周期余数 oracle，与奖励点枚举比较；再暴力枚举短二进制串验证“一个零见证”判定。固定覆盖 `m=0`、`p_m=n`、`d=0`、严格等号和三组官方样例。所有程序重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/E)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-513-q4-lc4013/">← [力扣竞赛] 第 513 场周赛 Q4 LC 4013 按奇偶比统计子数组 II 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-06-lc3345/">[力扣每日一题] 2026-08-06｜LC 3345 最小可整除数位乘积 I →</a>
</nav>
