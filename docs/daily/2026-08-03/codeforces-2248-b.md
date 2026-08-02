---
title: "[codeforces] CF Round 1113 Div.2 B Merge to Match"
---

# [codeforces] CF Round 1113 Div.2 B Merge to Match

<p class="daily-archive-kicker">2026-08-03 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=e0f4fedcddec1f37c720982bd3ac70f90b6b450001f52f763b1717cdc9b5ca9f -->
## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1113 (Div. 2)。
- Contest ID：2248。
- 题号与标题：Div.2 B - Merge to Match。
- 官方 points：1250。
- 官方 rating：未知（2026-08-03 核对时官方 API 未提供）。
- 官方 tags：`greedy`、`sortings`。
- 时间限制：1.5 秒。
- 内存限制：256 MB。
- 官方题面：[Codeforces 2248B - Merge to Match](https://codeforces.com/contest/2248/problem/B)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)。

下方英文题面层按 Codeforces 材料许可在公开、非判题用途下呈现，并保留来源、官方直达链接与许可说明。这里不复制隐藏测试、生成器、checker、validator 或其他未公开判题材料。

## Complete English statement

### B. Merge to Match

- **Time limit per test:** 1.5 seconds
- **Memory limit per test:** 256 megabytes
- **Input:** standard input
- **Output:** standard output
- **Official task:** [Codeforces 2248B](https://codeforces.com/contest/2248/problem/B)

You are given two arrays $a$ and $b$ whose lengths are $n$ and $m$, respectively. All $n+m$ integers occurring in the two arrays are distinct.

You may apply the following operation to $a$ any number of times, including zero times:

1. Choose two elements of $a$ whose values are $x$ and $y$, with $x\le y$.
2. Delete both chosen elements from $a$.
3. Insert one integer $z$ satisfying $x\le z\le y$ into $a$.

After all operations, you may reorder the elements of $a$ arbitrarily. Determine whether $a$ can be made equal to $b$.

### Input

The first line contains the number of test cases $t$:

$$
1\le t\le10^4.
$$

For each test case:

- The first line contains $n$ and $m$, the lengths of $a$ and $b$.
- The second line contains $a_1,a_2,\ldots,a_n$.
- The third line contains $b_1,b_2,\ldots,b_m$.

### Complete Constraints

$$
1\le n,m\le2\cdot10^5,
$$

$$
1\le a_i,b_i\le10^9.
$$

All $n+m$ values in $a$ and $b$ are distinct. Across all test cases, the sum of $n$ does not exceed $2\cdot10^5$, and the sum of $m$ does not exceed $2\cdot10^5$.

### Output

For each test case, print `YES` if the transformation is possible and `NO` otherwise. Letter case is ignored; for example, `yEs`, `yes`, `Yes`, and `YES` are all accepted as positive answers.

### Official Sample

```text
Input
11
2 1
1 3
2
3 2
1 3 5
2 4
4 2
1 3 5 7
4 6
4 2
2 5 8 11
1 10
4 2
1 4 7 9
3 10
5 2
10 1 100 6 4
90 5
6 3
1 4 10 20 30 40
3 15 35
4 2
1 2 3 100
4 5
7 3
1 8 3 30 18 12 25
2 15 28
4 1
1 2 3 5
4
4 2
1 3 5 6
2 4
```

```text
Output
YES
NO
YES
NO
NO
YES
YES
NO
YES
YES
YES
```

### Official Notes

- In test case 1, merge $1$ and $3$ and insert $2$.
- Test case 2 has no valid sequence of operations.
- In test case 3, merge $1$ with $5$ into $4$, then merge $3$ with $7$ into $6$.
- In test case 6, merge $1$ and $10$ into $5$, merge $6$ and $100$ into $90$, then merge $4$ and the inserted $5$ into $5$.
- In test case 7, merge the pairs $(1,4)$, $(10,20)$, and $(30,40)$ into $3$, $15$, and $35$.
- In test case 9, merge $(1,3)$, $(8,18)$, and $(25,30)$ into $2$, $15$, and $28$; then merge $12$ with the inserted $15$ and keep $15$.
- In test case 10, successively merge $(1,2)$ into $2$, $(2,3)$ into $3$, and $(3,5)$ into $4$.

The official statement contains no required image.

## 中文题意

数组 $a$ 是一个可反复合并的多重集合：选两个值 $x\le y$，删掉它们，再插入任意 $z\in[x,y]$。每次操作让长度减 1，最后允许任意重排。两数组中的初始值全部互不相同，问能否把 $a$ 变成 $b$。

## 约束推导与结构化建模

一次完整变换会把若干初始 $a$ 值合并成一个最终 $b_j$。把这些初始值看作一组，合并过程始终不能让结果越出该组初始最小值与最大值形成的闭区间；反过来，只要组内存在

$$
\min(group)<b_j<\max(group),
$$

先把最小值与最大值合并成 $b_j$，再逐个把其余元素与当前 $b_j$ 合并并仍插入 $b_j$，就能得到目标。严格不等号来自题目保证 $a$ 与 $b$ 的所有值互异。

因此，每个 $b_j$ 必须获得一个不同的较小见证与一个不同的较大见证，故首先需要 $n\ge2m$。剩余元素可随意并入任一组，不再施加约束。问题化为两个不相交的阈值匹配。

关键交换是：若存在可行方案，总能把排序后最小的 $m$ 个 $a$ 作为全部较小见证。假设某个全局较小元素 $x$ 原先充当较大见证，而某个更大的元素 $y$ 充当较小见证；交换二者后，$x<y<b$ 仍让 $x$ 可作较小见证，而 $y\ge x>b'$ 仍可替代 $x$ 的较大见证。反复交换即可得到规范形。

于是排序 $a,b$ 后：

1. 检查 $a_i<b_i$，$0\le i<m$；
2. 在剩余 $a_m,\ldots,a_{n-1}$ 中用双指针依次为升序 $b_i$ 取第一个严格大于它的值。

排序比较只使用 $10^9$ 内整数，不做加乘，无溢出风险。

## 解法递进

### 解法一：回溯枚举每个目标的两名见证

对每个 $b_j$ 枚举未使用的 $a_p<b_j<a_q$。若所有目标都能拿到不相交的见证，则剩余元素可任意吸收。该方法覆盖全部分组，但最坏接近 $O(n^{2m})$，仅适合作为小规模 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool searchWitnesses(
    const vector<long long>& a, const vector<long long>& b, int target, vector<int>& used) {
  if (target == static_cast<int>(b.size())) {
    return true;
  }
  for (int low = 0; low < static_cast<int>(a.size()); ++low) {
    if (used[low] || a[low] >= b[target]) {
      continue;
    }
    used[low] = true;
    for (int high = 0; high < static_cast<int>(a.size()); ++high) {
      if (used[high] || a[high] <= b[target]) {
        continue;
      }
      used[high] = true;
      if (searchWitnesses(a, b, target + 1, used)) {
        return true;
      }
      used[high] = false;
    }
    used[low] = false;
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(m);
    for (long long& value : a) {
      cin >> value;
    }
    for (long long& value : b) {
      cin >> value;
    }
    vector<int> used(n);
    bool possible = n >= 2 * m && searchWitnesses(a, b, 0, used);
    cout << (possible ? "YES" : "NO") << '\n';
  }
}
```

时间指数级，空间 $O(n+m)$；它直接验证“两名见证”模型。

### 最佳实用解：排序、交换规范形与阈值贪心

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool possible(vector<long long> a, vector<long long> b) {
  int n = a.size();
  int m = b.size();
  if (n < 2 * m) {
    return false;
  }
  sort(a.begin(), a.end());
  sort(b.begin(), b.end());
  for (int i = 0; i < m; ++i) {
    if (a[i] >= b[i]) {
      return false;
    }
  }
  int next = m;
  for (long long target : b) {
    while (next < n && a[next] <= target) {
      ++next;
    }
    if (next == n) {
      return false;
    }
    ++next;
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(m);
    for (long long& value : a) {
      cin >> value;
    }
    for (long long& value : b) {
      cin >> value;
    }
    cout << (possible(a, b) ? "YES" : "NO") << '\n';
  }
}
```

每组时间 $O(n\log n+m\log m)$，排序外额外空间 $O(1)$（忽略递归栈和按值传参副本）。总规模 $2\cdot10^5$，可以稳定通过。

## 正确性证明

**引理 1**：一组初始元素能合并成 $b$，当且仅当组内存在一个值小于 $b$ 和一个值大于 $b$。必要性来自每次新值都留在参与元素区间内，因此最终值位于整组初始极值之间；因所有初始值与 $b$ 不同，必须严格夹住。充分性由“先合并两名见证得到 $b$，再让 $b$ 逐个吸收其余元素并仍插入 $b$”构造。

**引理 2**：若存在可行见证分配，则存在一个使用全局最小 $m$ 个 $a$ 作为较小见证的可行分配。把一个尚未作为较小见证的全局小元素 $x$ 与当前某个更大的较小见证 $y$ 交换。若 $x$ 未使用，直接替换；若 $x$ 是某目标的较大见证，则 $y\ge x$ 仍大于该目标，可接替其角色。交换不破坏任何严格不等式，有限次后得到规范形。

对规范形，排序后的 $a_i<b_i$ 正是较小见证阈值匹配的充要条件。剩余元素与升序目标之间的“大于”关系是嵌套阈值图；给当前最小目标选择最小可用较大元素不会伤害后续更大目标。若贪心找不到，所有剩余值都不大于当前目标，更不可能存在其他匹配；若找到，交换任一可行匹配中的对应见证即可让它采用贪心选择。归纳得双指针成功当且仅当较大见证完美匹配存在。

两类见证不相交，依引理 1 分别构造各组，再把所有剩余元素并入任一组，即得到完整操作序列。因此算法输出 `YES` 当且仅当变换可行。

## 样例手推

样例 3 中 $a=[1,3,5,7]$、$b=[4,6]$。最小两个 $a$ 为 1、3，分别小于 4、6；剩余 5、7 分别严格大于 4、6。两组可取 $(1,5)\to4$、$(3,7)\to6$。

样例 2 中 $n=3<2m=4$，每个目标至少需要两个不同初始元素，立即判 `NO`。样例 10 中 $m=1$，1 可作较小见证、5 可作较大见证，2、3 再逐个被结果吸收，得到 4。

## 易错点与方案比较

- 每个 $b$ 不能由单个 $a$ 原样保留，因为题目保证两数组所有值互异。
- 阈值必须严格：`a < b < a`，不能写成 `<=`。
- 先固定最小 $m$ 个作较小见证后，较大见证只能从下标 $m$ 开始扫描。
- 双指针遇到 `a[next] <= target` 要跳过；这些元素可作为最终的额外吸收项，但不能作较大见证。
- 最大流能表达匹配，却忽略阈值图的嵌套结构；排序贪心证明更短、常数更小，是竞赛中应优先记忆的方案。

## 变种一：恢复分组与一条操作序列

新定义：若可行，输出每个目标的较小、较大见证，并把所有剩余元素分配给第一组。按“见证先合并，额外元素再被目标吸收”即可恢复操作。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> a(n), b(m);
  for (long long& value : a) {
    cin >> value;
  }
  for (long long& value : b) {
    cin >> value;
  }
  sort(a.begin(), a.end());
  sort(b.begin(), b.end());
  if (n < 2 * m) {
    cout << "NO\n";
    return 0;
  }
  vector<vector<long long>> groups(m);
  vector<int> used(n);
  for (int i = 0; i < m; ++i) {
    if (a[i] >= b[i]) {
      cout << "NO\n";
      return 0;
    }
    groups[i].push_back(a[i]);
    used[i] = true;
  }
  int next = m;
  for (int i = 0; i < m; ++i) {
    while (next < n && (used[next] || a[next] <= b[i])) {
      ++next;
    }
    if (next == n) {
      cout << "NO\n";
      return 0;
    }
    groups[i].push_back(a[next]);
    used[next++] = true;
  }
  for (int i = 0; i < n; ++i) {
    if (!used[i]) {
      groups[0].push_back(a[i]);
    }
  }
  cout << "YES\n";
  for (int i = 0; i < m; ++i) {
    cout << b[i] << ':';
    for (long long value : groups[i]) {
      cout << ' ' << value;
    }
    cout << '\n';
  }
}
```

时间 $O(n\log n+m\log m)$，恢复结果占 $O(n)$ 空间。每行的前两个值夹住冒号前目标，其余值可依次吸收。

## 变种二：每个目标必须恰由 $K$ 个初始元素形成

新定义：每组大小固定为 $K\ge2$。见证条件不变，但总数必须满足 $n=Km$；匹配两名见证后，任意把剩余元素按每组 $K-2$ 个分配即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, k;
  cin >> n >> m >> k;
  vector<long long> a(n), b(m);
  for (long long& value : a) {
    cin >> value;
  }
  for (long long& value : b) {
    cin >> value;
  }
  if (k < 2 || n != k * m) {
    cout << "NO\n";
    return 0;
  }
  sort(a.begin(), a.end());
  sort(b.begin(), b.end());
  for (int i = 0; i < m; ++i) {
    if (a[i] >= b[i]) {
      cout << "NO\n";
      return 0;
    }
  }
  int next = m;
  for (long long target : b) {
    while (next < n && a[next] <= target) {
      ++next;
    }
    if (next == n) {
      cout << "NO\n";
      return 0;
    }
    ++next;
  }
  cout << "YES\n";
}
```

时间 $O(n\log n+m\log m)$，空间由排序决定。固定组大小只增加计数条件，不改变区间可达性。

## 变种三：目标值允许重复

新定义：$a$ 内部仍互异，且任何 $a_i$ 都不等于任何 $b_j$，但不同目标可以相等。每个目标仍需要独立两名见证，排序阈值匹配允许相等的 $b$ 连续出现，原算法无需改变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> a(n), b(m);
  for (long long& value : a) {
    cin >> value;
  }
  for (long long& value : b) {
    cin >> value;
  }
  sort(a.begin(), a.end());
  sort(b.begin(), b.end());
  bool ok = n >= 2 * m;
  for (int i = 0; ok && i < m; ++i) {
    ok = a[i] < b[i];
  }
  int next = m;
  for (int i = 0; ok && i < m; ++i) {
    while (next < n && a[next] <= b[i]) {
      ++next;
    }
    ok = next < n;
    ++next;
  }
  cout << (ok ? "YES" : "NO") << '\n';
}
```

时间 $O(n\log n+m\log m)$。若允许 $a_i=b_j$，单元素组也可能合法，必须先剥离相等值，不能直接套用本代码。

## 变种四：只能合并相邻元素且不能重排

新定义：数组顺序固定，每次只能合并当前相邻元素，最终顺序必须等于 $b$。每个目标对应原数组的一个连续非空段；在仍假设所有 $a_i$ 与 $b_j$ 不同的前提下，段长至少 2 且段最小值小于目标、最大值大于目标。用前缀分段 DP 枚举最后一段。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> a(n), b(m);
  for (long long& value : a) {
    cin >> value;
  }
  for (long long& value : b) {
    cin >> value;
  }
  vector<vector<char>> dp(m + 1, vector<char>(n + 1));
  dp[0][0] = true;
  for (int target = 0; target < m; ++target) {
    for (int left = 0; left < n; ++left) {
      if (!dp[target][left]) {
        continue;
      }
      long long minimum = a[left];
      long long maximum = a[left];
      for (int right = left; right < n; ++right) {
        minimum = min(minimum, a[right]);
        maximum = max(maximum, a[right]);
        if (right > left && minimum < b[target] && b[target] < maximum) {
          dp[target + 1][right + 1] = true;
        }
      }
    }
  }
  cout << (dp[m][n] ? "YES" : "NO") << '\n';
}
```

时间 $O(mn^2)$，空间 $O(mn)$，适合小规模版本。全局见证贪心失效，因为一个元素只能服务于所在的连续段。

## 验证说明

本轮将所有代码按 GNU++23 编译；最佳贪心会与指数回溯在所有总长度不超过 13、目标数不超过 4 的小型相对次序模式上穷举对拍，并用官方 11 组样例复核输出。对拍只比较严格大小关系，因此同时覆盖大整数而无溢出假设。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/B)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-513-q1-lc4010/">← [力扣竞赛] 第 513 场周赛 Q1 LC 4010 数对的最大强度 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-03-lc1406/">[力扣每日一题] 2026-08-03｜LC 1406 石子游戏 III →</a>
</nav>
