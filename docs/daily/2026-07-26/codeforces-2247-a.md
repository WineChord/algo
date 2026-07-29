---
title: "[codeforces] CF Round 1111 Div.2 A Zero Sum"
---

# [codeforces] CF Round 1111 Div.2 A Zero Sum

<p class="daily-archive-kicker">2026-07-26 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

## Official source information

- Contest: Codeforces Round 1111 (Div. 2)
- Contest ID: 2247
- Division / task aliases: Div.2 A
- Official title: Zero Sum
- Official rating: not published in the official API at verification time
- Time limit: 1 second
- Memory limit: 256 MB
- Official problem: [Open the official problem](https://codeforces.com/contest/2247/problem/A)
- Canonical problemset link: [打开 Codeforces 页面](https://codeforces.com/problemset/problem/2247/A)
- Program interface: GNU++23 full program.
- Official statement image: none

### Original English statement

Open the [complete original English statement](https://codeforces.com/contest/2247/problem/A) on Codeforces.

> “You are given an array a of length n, consisting only of -1 and 1.”

The official metadata, limits, input/output structure, sample data, and note facts are preserved below. The remaining prose is a faithful, complete teaching restatement.

### Faithful complete statement restatement

For each test case, an array $a$ of length $n$ contains only `-1` and `1`. One operation chooses an adjacent pair $(i,i+1)$ and negates both values:

$$
a_i\leftarrow-a_i,\qquad a_{i+1}\leftarrow-a_{i+1}.
$$

The operation may be used any number of times. Determine whether the array can be transformed so that the sum of all elements is zero.

### Input

The first line contains the number of test cases $t$. Each test case contains:

```text
n
a_1 a_2 ... a_n
```

### Output

For each test case print `YES` if a zero sum is reachable, otherwise print `NO`. Letter case is ignored.

### All official constraints

- $1\le t\le200$
- $1\le n\le100$
- $a_i\in\{-1,1\}$

### Official sample

```text
Input
5
1
-1
2
1 -1
2
1 1
5
1 -1 1 -1 1
6
-1 1 -1 -1 -1 -1
Output
NO
YES
NO
NO
YES
```

The first case has odd length and cannot have equal numbers of `1` and `-1`. The second already sums to zero. In the fifth case, flipping positions 3 and 4 changes the array to `[-1,1,1,1,-1,-1]`, whose sum is zero.

## 中文题意

每次同时把一对相邻的 $\pm1$ 取反，问能否最终让正一和负一数量相同。

## 最优结论

一次操作同时改变两个数，数组所有元素的乘积保持不变。零和目标必须有 $n/2$ 个 `-1`，其乘积为 $(-1)^{n/2}$。因此可行当且仅当：

1. $n$ 为偶数；
2. 初始负数个数 `neg` 与 $n/2$ 奇偶性相同。

这个条件也充分：若初态与某个零和目标的乘积相同，两者不同的位置数为偶数；路径图上的相邻翻转可以生成任意偶数大小的位置集合。每个测试只需计数负数，时间 $O(n)$、空间 $O(1)$。

## 暴力：状态图 BFS

把每个 $\pm1$ 数组编码为位掩码，枚举全部相邻翻转；仅适合很小的 $n$，可作 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool brute(const vector<int>& a) {
  int n = a.size();
  if (n > 20) return false;
  int start = 0;
  for (int i = 0; i < n; ++i) {
    if (a[i] == 1) start |= 1 << i;
  }
  vector<char> seen(1 << n);
  queue<int> q;
  seen[start] = 1;
  q.push(start);
  while (!q.empty()) {
    int mask = q.front();
    q.pop();
    if (__builtin_popcount((unsigned)mask) * 2 == n) return true;
    for (int i = 0; i + 1 < n; ++i) {
      int next = mask ^ (3 << i);
      if (!seen[next]) {
        seen[next] = 1;
        q.push(next);
      }
    }
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    cout << (brute(a) ? "YES\n" : "NO\n");
  }
}
```

时间 $O(n2^n)$、空间 $O(2^n)$。它完全覆盖可达状态，但没有利用不变量。

## 最佳实用解：乘积奇偶不变量

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, negative = 0;
    cin >> n;
    for (int i = 0; i < n; ++i) {
      int x;
      cin >> x;
      negative += x == -1;
    }
    bool possible = n % 2 == 0 && negative % 2 == (n / 2) % 2;
    cout << (possible ? "YES\n" : "NO\n");
  }
}
```

### 正确性证明

必要性：零和要求正负数各 $n/2$ 个，所以 $n$ 必须为偶数。每次操作给总乘积乘以 $(-1)^2=1$，初始乘积 $(-1)^{negative}$ 必须等于目标乘积 $(-1)^{n/2}$，即两指数奇偶相同。

充分性：任选一个含 $n/2$ 个负数的目标数组。乘积相同意味着初态与目标不同的位置数为偶数。设差异位向量为 $d_1,\ldots,d_n$，令边操作选择 $x_i=d_1\oplus\cdots\oplus d_i$。位置 1 的翻转奇偶为 $x_1=d_1$，内部位置 $i$ 为 $x_{i-1}\oplus x_i=d_i$；由于全部 $d_i$ 异或为 0，最后位置也满足。执行所有 $x_i=1$ 的相邻操作即可到达目标。

### 复杂度

每个测试时间 $O(n)$，额外空间 $O(1)$；输入本身已给出 $\Omega(n)$ 读取下界。

## 常见错误

- 只判断 `n` 为偶数；`[1,1]` 仍不可行。
- 误以为总和的奇偶性足够。对偶数 $n$，总和总是偶数，但可达性还受乘积约束。
- 将“相邻”忽略后直接随意翻两个位置，却没有证明路径图能生成同一偶数子空间。
- 对 `negative - n/2` 直接取 `% 2` 并依赖负数取模符号；比较两个非负计数的奇偶更清楚。

## Follow-up 1：输出一组实际操作

选定“前 $n/2$ 个位置为 `-1`、其余为 `1`”的零和目标，再用前缀异或恢复需要执行的边。

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
  int negative = 0;
  for (int& x : a) {
    cin >> x;
    negative += x == -1;
  }
  if (n % 2 || negative % 2 != (n / 2) % 2) {
    cout << "NO\n";
    return 0;
  }
  vector<int> operations;
  int prefix = 0;
  for (int i = 0; i + 1 < n; ++i) {
    int target = i < n / 2 ? -1 : 1;
    int different = a[i] != target;
    prefix ^= different;
    if (prefix) operations.push_back(i + 1);
  }
  cout << "YES\n" << operations.size() << '\n';
  for (int edge : operations) cout << edge << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。输出的 `edge` 是一基左端点。

## Follow-up 2：可翻转任意两个位置

可达差异集合仍恰好是任意偶数大小集合，因此判定条件相同；构造时把所有差异位置两两配对。

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
  int negative = 0;
  for (int& x : a) {
    cin >> x;
    negative += x == -1;
  }
  if (n % 2 || negative % 2 != (n / 2) % 2) {
    cout << "NO\n";
    return 0;
  }
  vector<int> different;
  for (int i = 0; i < n; ++i) {
    int target = i < n / 2 ? -1 : 1;
    if (a[i] != target) different.push_back(i + 1);
  }
  cout << "YES\n" << different.size() / 2 << '\n';
  for (int i = 0; i < (int)different.size(); i += 2) {
    cout << different[i] << ' ' << different[i + 1] << '\n';
  }
}
```

判定与构造均为 $O(n)$。

## Follow-up 3：求达到任意零和目标的最少相邻操作数

目标中恰有 $n/2$ 个负数。动态规划从左到右选择每个目标符号，并把当前前缀差异异或作为下一条边是否必须操作；最后要求总差异异或为 0。

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
  if (n % 2) {
    cout << -1 << '\n';
    return 0;
  }
  const int inf = 1e9;
  vector<vector<int>> dp(n / 2 + 1, vector<int>(2, inf));
  dp[0][0] = 0;
  for (int i = 0; i < n; ++i) {
    vector<vector<int>> next(n / 2 + 1, vector<int>(2, inf));
    for (int used = 0; used <= n / 2; ++used) {
      for (int parity = 0; parity < 2; ++parity) {
        if (dp[used][parity] == inf) continue;
        for (int targetNegative = 0; targetNegative <= 1; ++targetNegative) {
          int newUsed = used + targetNegative;
          if (newUsed > n / 2) continue;
          int target = targetNegative ? -1 : 1;
          int newParity = parity ^ (a[i] != target);
          int cost = dp[used][parity] + (i + 1 < n ? newParity : 0);
          next[newUsed][newParity] = min(next[newUsed][newParity], cost);
        }
      }
    }
    dp.swap(next);
  }
  int answer = dp[n / 2][0];
  cout << (answer == inf ? -1 : answer) << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$。主问题只问存在性，因此不需要这个目标选择 DP。

## Follow-up 4：目标和改为指定值 `S`

目标正数个数必须为 $(n+S)/2$，负数个数为 $(n-S)/2$；范围、奇偶与乘积不变量同时满足才可行。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, targetSum, negative = 0;
    cin >> n >> targetSum;
    for (int i = 0; i < n; ++i) {
      int x;
      cin >> x;
      negative += x == -1;
    }
    bool shape = abs(targetSum) <= n && (n - targetSum) % 2 == 0;
    int targetNegative = shape ? (n - targetSum) / 2 : 0;
    bool possible = shape && negative % 2 == targetNegative % 2;
    cout << (possible ? "YES\n" : "NO\n");
  }
}
```

每个测试时间 $O(n)$，空间 $O(1)$。

## 验证

对 $n=1\ldots12$ 枚举全部 $2^n$ 个初态，以状态图 BFS 为 oracle，与奇偶判定逐一比较；同时把构造出的操作真实应用到数组，检查最终和为 0。官方五组样例输出依次为 `NO YES NO NO YES`。

## Reference

- [官方题目](https://codeforces.com/contest/2247/problem/A)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-511-q1-lc3996/">← [力扣竞赛] 第 511 场周赛 Q1 LC 3996 偶数次骑士移动 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-26-lc628/">[力扣每日一题] 2026-07-26｜LC 628 三个数的最大乘积 →</a>
</nav>
