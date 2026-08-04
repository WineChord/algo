---
title: "[codeforces] CF Round 1113 Div.2 D Good Pair Queries"
---

# [codeforces] CF Round 1113 Div.2 D Good Pair Queries

<p class="daily-archive-kicker">2026-08-05 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=7c266fe2236f83fb85f3ece855d0c0ab1a29176647230955a8a87d1692107093 -->
[Official problem: Codeforces Round 1113 Div.2 D - Good Pair Queries](https://codeforces.com/contest/2248/problem/D)

## 官方来源信息

- 比赛：Codeforces Round 1113 (Div. 2)。
- 竞赛 ID：2248。
- 组别别名：Div.2 D。
- 官方标题：Good Pair Queries。
- 官方分值：1750。
- 官方 rating：1400。
- 官方 tags：`constructive algorithms`、`greedy`。
- 时间限制：2 秒。
- 内存限制：256 MB。

## Complete English statement

You are given two binary strings $s$ and $t$, both of length $n$.

For two binary strings $a$ and $b$ of the same length, the pair $(a,b)$ is called good if both strings can be made empty by performing the following operation zero or more times:

1. Choose a non-empty set of positions $1\le i_1<i_2<\cdots<i_k\le|a|$ and a character $c\in\{\mathtt{0},\mathtt{1}\}$.
2. Let $x=a_{i_1}a_{i_2}\cdots a_{i_k}$ and $y=b_{i_1}b_{i_2}\cdots b_{i_k}$.
3. The chosen character $c$ must be a mode of both $x$ and $y$.
4. Delete the chosen positions from both strings. Concatenate the remaining characters without changing their relative order.

A character is a mode of a binary string $z$ if it appears at least $\lceil|z|/2\rceil$ times. Therefore an even-length binary string with equal numbers of zeros and ones has both characters as modes.

Answer $q$ independent queries. Query $(l,r)$ asks whether the aligned substring pair

$$
(s_ls_{l+1}\cdots s_r,\ t_lt_{l+1}\cdots t_r)
$$

is good.

### Input

The first line contains the number of test cases $T$. For each test case:

```text
n q
s
t
l_1 r_1
⋮
l_q r_q
```

### Output

For every query, print `YES` if the substring pair is good and `NO` otherwise. Letter case is ignored.

### Constraints

- $1\le T\le10^4$.
- $1\le n,q\le2\times10^5$.
- `s` and `t` are binary strings of length $n$.
- $1\le l\le r\le n$.
- The sum of $n$ over all test cases is at most $2\times10^5$.
- The sum of $q$ over all test cases is at most $2\times10^5$.

### Official sample

```text
Input
3
2 2
01
10
1 1
1 2
5 1
11111
11111
1 3
5 1
00011
01111
1 5

Output
NO
YES
YES
YES
```

For the first query, the pair is `(0,1)`, which has no common mode. For the second query, choosing both positions and `c = 0` deletes `(01,10)` in one operation because both subsequences have zero as a mode. In the third test case the whole pair cannot be deleted in one operation, but it can be emptied as follows:

1. Choose positions 2 and 4 with `c = 1`; `(01,11)` is deleted and the pair becomes `(001,011)`.
2. Choose positions 1 and 2 with `c = 0`; `(00,01)` is deleted and the pair becomes `(1,1)`.
3. Choose the remaining position with `c = 1`.

There are no official images. Source and reuse terms: [official problem](https://codeforces.com/contest/2248/problem/D), [Codeforces Materials Usage License v0.1](https://codeforces.com/blog/entry/967?mobile=false).

## 中文题意

每个位置可按二元组分成 `00`、`01`、`10`、`11`。一次操作选同一批位置；只要选出字符 0 或 1，使它在两条被选子序列中都至少占一半，就能同时删除这些位置。每个询问独立判断对应区间最终能否删空。

## 约束推导与观察

记四类位置数为 $c_{00},c_{01},c_{10},c_{11}$。充要条件是

$$
|c_{01}-c_{10}|\le c_{00}+c_{11}.
$$

直观构造：先把一个 `01` 与一个 `10` 成对删除；两条子序列都是一零一一的平局。剩余错配只会朝一个方向，每个 `00` 或 `11` 都能吸收一个错配。右侧的相同位置数足够时即可删空。静态多询问只需前缀统计 `01`、`10`，每问 $O(1)$。

## 解法递进

### 解法一：对子集删除做状态搜索

仅适合区间长度不超过 18。状态 `mask` 表示仍存在的位置，枚举非空删除子集并检查是否有共同众数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool goodSubset(int subset, const string& s, const string& t) {
  int length = popcount(static_cast<unsigned>(subset));
  int zeroS = 0;
  int zeroT = 0;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (subset >> i & 1) {
      zeroS += s[i] == '0';
      zeroT += t[i] == '0';
    }
  }
  bool commonZero = 2 * zeroS >= length && 2 * zeroT >= length;
  bool commonOne = 2 * (length - zeroS) >= length && 2 * (length - zeroT) >= length;
  return commonZero || commonOne;
}
bool solve(int mask, const string& s, const string& t, vector<int>& memo) {
  if (mask == 0) {
    return true;
  }
  if (memo[mask] != -1) {
    return memo[mask];
  }
  for (int subset = mask; subset; subset = (subset - 1) & mask) {
    if (goodSubset(subset, s, t) && solve(mask ^ subset, s, t, memo)) {
      return memo[mask] = true;
    }
  }
  return memo[mask] = false;
}
int main() {
  string s, t;
  cin >> s >> t;
  int states = 1 << s.size();
  vector<int> memo(states, -1);
  cout << (solve(states - 1, s, t, memo) ? "YES" : "NO") << '\n';
}
```

时间 $O(3^L\cdot L)$，空间 $O(2^L)$。它忠实覆盖所有操作序列，但无法应对 $2\times10^5$。

### 最佳实用解：四类计数的充要条件

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n, q;
    string s, t;
    cin >> n >> q >> s >> t;
    vector<int> count01(n + 1), count10(n + 1);
    for (int i = 0; i < n; ++i) {
      count01[i + 1] = count01[i] + (s[i] == '0' && t[i] == '1');
      count10[i + 1] = count10[i] + (s[i] == '1' && t[i] == '0');
    }
    while (q--) {
      int left, right;
      cin >> left >> right;
      int opposite01 = count01[right] - count01[left - 1];
      int opposite10 = count10[right] - count10[left - 1];
      int length = right - left + 1;
      int same = length - opposite01 - opposite10;
      cout << (abs(opposite01 - opposite10) <= same ? "YES" : "NO") << '\n';
    }
  }
}
```

每个测试预处理 $O(n)$，每问 $O(1)$，总时间 $O(\sum n+\sum q)$，空间 $O(n)$。

## 正确性证明

先证必要性。对某次操作，若共同众数是 0，则两串中的零都不少于一，化为计数不等式可得 $|c_{01}-c_{10}|\le c_{00}-c_{11}\le c_{00}+c_{11}$；共同众数为 1 时对称得到同一结论。对所有删除组的差值求和并使用三角不等式，整段仍满足该不等式。

再证充分性。先配对删除 `min(c01,c10)` 组 `01+10`；每组在两串中都是平局，任取 0 为共同众数。剩余错配数量为 $|c_{01}-c_{10}|$，条件保证至少有这么多相同位置。每个剩余错配与一个 `00` 配对时共同众数为 0，与一个 `11` 配对时共同众数为 1，均可删除。最后剩余的 `00`、`11` 可单点删除。因此条件充分。

## 样例手推

第一组 `[1,1]` 有一个 `01`、没有 `10` 与相同位置，`1>0`，故 `NO`。区间 `[1,2]` 有一个 `01` 与一个 `10`，差为 0，故 `YES`。第三组整段有两个 `01`、零个 `10`、三个相同位置，`2<=3`，虽不能一步删空却能按官方三步构造。

## 易错点与方案比较

- 偶数长度平局时 0、1 都是 mode。
- 不能只检查整段是否能一次删除；允许多次操作。
- `01`、`10` 的定义方向可互换，但最后必须取绝对值。
- 询问独立，不能把前一问的删除状态带入后一问。

## 变种一：恢复一组实际删除操作

新定义：对一个已知合法区间输出每次删除的原下标。先配对两类错配，再用相同位置吸收剩余错配，最后单删相同位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string s, t;
  cin >> s >> t;
  vector<int> a, b, same;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == t[i]) {
      same.push_back(i + 1);
    } else if (s[i] == '0') {
      a.push_back(i + 1);
    } else {
      b.push_back(i + 1);
    }
  }
  if (abs(static_cast<int>(a.size()) - static_cast<int>(b.size())) >
      static_cast<int>(same.size())) {
    cout << "NO\n";
    return 0;
  }
  vector<vector<int>> operations;
  while (!a.empty() && !b.empty()) {
    operations.push_back({a.back(), b.back()});
    a.pop_back();
    b.pop_back();
  }
  vector<int>& left = a.empty() ? b : a;
  while (!left.empty()) {
    operations.push_back({left.back(), same.back()});
    left.pop_back();
    same.pop_back();
  }
  for (int position : same) {
    operations.push_back({position});
  }
  cout << operations.size() << '\n';
  for (const auto& operation : operations) {
    cout << operation.size();
    for (int position : operation) {
      cout << ' ' << position;
    }
    cout << '\n';
  }
}
```

时间 $O(L)$，空间 $O(L)$ 加输出。原判定只需计数，恢复方案必须保存位置。

## 变种二：要求一次操作就删空

新定义：不能分组。只需检查整个区间是否存在共同众数，即两串的零都至少一半，或一都至少一半。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, q;
  string s, t;
  cin >> n >> q >> s >> t;
  vector<int> zeroS(n + 1), zeroT(n + 1);
  for (int i = 0; i < n; ++i) {
    zeroS[i + 1] = zeroS[i] + (s[i] == '0');
    zeroT[i + 1] = zeroT[i] + (t[i] == '0');
  }
  while (q--) {
    int left, right;
    cin >> left >> right;
    int length = right - left + 1;
    int a = zeroS[right] - zeroS[left - 1];
    int b = zeroT[right] - zeroT[left - 1];
    bool zero = 2 * a >= length && 2 * b >= length;
    bool one = 2 * (length - a) >= length && 2 * (length - b) >= length;
    cout << (zero || one ? "YES" : "NO") << '\n';
  }
}
```

预处理 $O(n)$，每问 $O(1)$。原题第三个测试说明“一步条件”严格强于“最终可删空”。

## 变种三：支持单点翻转与区间询问

新定义：可翻转 `s[i]` 或 `t[i]`。用两个 Fenwick 树动态维护 `01`、`10` 指示值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  vector<int> tree;
public:
  explicit Fenwick(int n) : tree(n + 1) {
  }
  void add(int index, int delta) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  int prefix(int length) const {
    int sum = 0;
    for (int index = length; index; index -= index & -index) {
      sum += tree[index];
    }
    return sum;
  }
  int range(int left, int right) const {
    return prefix(right) - prefix(left);
  }
};
int main() {
  int n, operations;
  string s, t;
  cin >> n >> operations >> s >> t;
  Fenwick count01(n), count10(n);
  auto type = [&](int i) {
    return pair<int, int>{s[i] == '0' && t[i] == '1', s[i] == '1' && t[i] == '0'};
  };
  for (int i = 0; i < n; ++i) {
    auto [a, b] = type(i);
    count01.add(i, a);
    count10.add(i, b);
  }
  while (operations--) {
    char command, which;
    int left, right;
    cin >> command;
    if (command == 'F') {
      cin >> which >> left;
      --left;
      auto [oldA, oldB] = type(left);
      (which == 's' ? s[left] : t[left]) ^= 1;
      auto [newA, newB] = type(left);
      count01.add(left, newA - oldA);
      count10.add(left, newB - oldB);
    } else {
      cin >> left >> right;
      --left;
      int a = count01.range(left, right);
      int b = count10.range(left, right);
      int same = right - left - a - b;
      cout << (abs(a - b) <= same ? "YES" : "NO") << '\n';
    }
  }
}
```

更新与查询均为 $O(\log n)$，空间 $O(n)$。静态前缀数组不能响应翻转。

## 变种四：统计一个区间最少需要多少个相同位置才能变好

新定义：允许向区间追加任意 `00` 或 `11` 位置，求最少追加数。缺口就是

$$
\max(0,|c_{01}-c_{10}|-(c_{00}+c_{11})).
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, q;
  string s, t;
  cin >> n >> q >> s >> t;
  vector<int> count01(n + 1), count10(n + 1);
  for (int i = 0; i < n; ++i) {
    count01[i + 1] = count01[i] + (s[i] == '0' && t[i] == '1');
    count10[i + 1] = count10[i] + (s[i] == '1' && t[i] == '0');
  }
  while (q--) {
    int left, right;
    cin >> left >> right;
    int a = count01[right] - count01[left - 1];
    int b = count10[right] - count10[left - 1];
    int same = right - left + 1 - a - b;
    cout << max(0, abs(a - b) - same) << '\n';
  }
}
```

预处理 $O(n)$，每问 $O(1)$。它把原布尔判定推广成离可行域的精确距离。

## 验证说明

本轮将六段完整程序按 GNU++23 编译并跑官方样例。主条件已独立穷举四类计数各不超过 6、总长度不超过 18 的 2275 个状态，与状态搜索零不一致；还会随机对拍动态翻转、一步删除、构造操作与缺口公式。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/D)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-513-q3-lc4012/">← [力扣竞赛] 第 513 场周赛 Q3 LC 4012 统计每个班次结束后的未完成任务数 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-05-lc3310/">[力扣每日一题] 2026-08-05｜LC 3310 移除可疑的方法 →</a>
</nav>
