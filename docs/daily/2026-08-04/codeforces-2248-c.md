---
title: "[codeforces] CF Round 1113 Div.2 C Maximize the Score"
---

# [codeforces] CF Round 1113 Div.2 C Maximize the Score

<p class="daily-archive-kicker">2026-08-04 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../dp/sequence-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=20359fd64e94d0e4d1971a6609ab50876fd556b3ad92c088128835c98f2ad82b -->
## 官方来源信息

- 来源：Codeforces。
- 比赛：Codeforces Round 1113 (Div. 2)。
- 题号与官方英文标题：C - Maximize the Score。
- 竞赛 ID：2248。
- 组别别名：Div.2 C。
- 官方分值：1500。
- 官方 rating：1300。
- 官方 tags：`dp`、`greedy`。
- 时间限制：2 秒。
- 内存限制：256 MB。
- 官方题面：[Codeforces 2248C - Maximize the Score](https://codeforces.com/contest/2248/problem/C)。
- 许可说明：英文题面层按 [Codeforces Materials Usage License v0.1](https://codeforces.com/blog/entry/967?mobile=false) 呈现；不包含隐藏测试、生成器、校验器或其他未覆盖材料。

## Complete English statement

### Problem Statement

You are given an array $a$ of length $2n$. Every integer from $1$ through $n$ occurs exactly twice in the array. Your score starts at zero.

While the array is non-empty, you may repeatedly do the following:

1. Choose a value $x$ that is currently present.
2. Let $l$ and $r$ be the positions of the leftmost and rightmost current occurrences of $x$. If only one copy remains, then $l=r$.
3. Add $(r-l+1)^2$ to your score.
4. Delete the entire current subarray $a_l,a_{l+1},\ldots,a_r$. Concatenate the remaining elements without changing their relative order, and index the new array from $1$ again.

Determine the maximum score obtainable when the array has been completely deleted.

### Input

The first line contains the number of test cases $t$.

For each test case:

- The first line contains $n$.
- The second line contains $2n$ integers $a_1,a_2,\ldots,a_{2n}$.

Every value from $1$ to $n$ appears exactly twice.

### Output

For every test case, print one integer: the maximum possible score.

### Constraints

- $1\le t\le10^4$.
- $1\le n\le2\cdot10^5$.
- $1\le a_i\le n$.
- Every integer from $1$ through $n$ occurs exactly twice.
- The sum of $n$ over all test cases does not exceed $2\cdot10^5$.

### Official Samples

```text
Input
6
1
1 1
2
1 2 1 2
2
1 2 2 1
3
1 1 2 3 3 2
3
1 2 3 3 2 1
4
1 2 3 4 1 2 3 4
```

```text
Output
4
10
16
20
36
28
```

### Official Sample Notes

- In test case 2, choosing value $1$ first removes `[1,2,1]` and scores $3^2=9$. The remaining `[2]` scores one more point, for 10 total.
- In test case 3, choosing value $1$ removes all four elements and scores $4^2=16$.
- In test case 4, choosing value $1$ and then value $2$ scores $2^2+4^2=20$.
- In test case 6, choosing value $2$ first removes `[2,3,4,1,2]` and scores $5^2=25$. The remaining `[1,3,4]` contributes three singleton points, for 28 total.

## 中文题意与来源说明

数组长度为 $2n$，每个编号恰出现两次。一次操作选择仍存在的编号，删除它在当前数组中最左与最右出现位置之间的整段，得分为当前段长的平方。删除会让左右剩余部分拼接。目标是删空数组时得分最大。

本页英文题面层依据 [Codeforces 官方题目](https://codeforces.com/contest/2248/problem/C) 自包含呈现；来源与使用条件见 [Codeforces Materials Usage License v0.1](https://codeforces.com/blog/entry/967?mobile=false)。题解、证明、变种与代码为独立推导和实现。

## 约束推导：把动态删除规整成原数组分块

直接模拟操作顺序会遇到“删除后距离改变”。关键交换论证是：若较晚的一次操作跨过了先前已删除的若干内部块，把这次外层操作提前，它会连同这些内部块一次删掉。设外层当时可见长度为 $L$，内部块长度为 $c_1,c_2,\ldots$，提前后的得分为 $(L+\sum c_i)^2$，而原来相关得分总和为 $L^2+\sum c_i^2$。由于长度非负，前者不小于后者。

不断做这种交换，可得到不劣方案：原数组被划分为若干连续块，每块直接一次删除。长度 1 的块总能得 1 分；长度大于 1 的块必须让首尾值相同，才能选择该值一次删除整块。反过来，任何这样的分块都能从左到右执行。因此问题精确化为“把原数组分块，单点块收益 1，同值首尾块收益长度平方”。

设 `dp[i]` 是前 `i` 个原数组元素的最大收益。最后一块只有两种：

- 单点 `[i,i]`：`dp[i-1]+1`；
- 若位置 `j<i` 与 `i` 值相同：`dp[j-1]+(i-j+1)^2`。

每个值恰出现两次，所以第二种候选只有一个。答案最大为 $(2n)^2\le1.6\cdot10^{11}$，必须使用 `long long`。

## 解法递进

### 解法一：枚举所有合法分块

从左端递归选择单点，或选择以当前位置为左端、同值第二次出现位置为右端的整块，覆盖全部规整方案。分支数可达指数级，只适合作为很小规模 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long solve(const vector<int>& values, int left) {
  int length = values.size();
  if (left == length) {
    return 0;
  }
  long long answer = 1 + solve(values, left + 1);
  for (int right = left + 1; right < length; ++right) {
    if (values[left] == values[right]) {
      long long block = right - left + 1;
      answer = max(answer, block * block + solve(values, right + 1));
    }
  }
  return answer;
}
int main() {
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n;
    cin >> n;
    vector<int> values(2 * n);
    for (int& value : values) {
      cin >> value;
    }
    cout << solve(values, 0) << '\n';
  }
}
```

最坏时间指数级，递归空间 $O(n)$。它的覆盖性直接对应分块定义。

### 最佳实用解：记录首次位置的一维动态规划

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n;
    cin >> n;
    int length = 2 * n;
    vector<int> first(n + 1, -1);
    vector<long long> dp(length + 1, 0);
    for (int index = 1; index <= length; ++index) {
      int value;
      cin >> value;
      dp[index] = dp[index - 1] + 1;
      if (first[value] == -1) {
        first[value] = index;
      } else {
        int left = first[value];
        long long blockLength = index - left + 1;
        dp[index] = max(dp[index], dp[left - 1] + blockLength * blockLength);
      }
    }
    cout << dp[length] << '\n';
  }
}
```

每个位置只处理一次，单测时间 $O(n)$，空间 $O(n)$；全体输入也是 $O(\sum n)$。它比显式模拟删除更简单、证明更稳定，是推荐方案。

## 正确性证明

先由交换论证可知，存在最优方案对应合法连续分块；任一合法分块也确实可执行，所以只需在分块集合中优化。

对前 `i` 个元素的最优分块考察最后一块。若它长度为 1，删去该块后留下前 `i-1` 个元素的某个分块，收益不超过 `dp[i-1]+1`。若长度大于 1，其左右端值相同；该值在全数组只出现两次，所以左端必为记录的 `first[value]`，收益不超过 `dp[left-1]+(i-left+1)^2`。递推恰取这两类的最大值，并且每个候选都能接在对应最优前缀分块之后执行。由归纳，`dp[i]` 精确等于前缀最优收益，`dp[2n]` 即答案。

## 样例手推、边界与易错点

对 `[1,2,1,2]`，`dp` 先为 1、2；到第三位可取 `[1,2,1]`，得到 9；第四位既可单点接在 9 后得到 10，也可用 `[2,1,2]` 接在首位后得到 10。单个编号 `[1,1]` 直接得到 4。完全嵌套的 `[1,2,2,1]` 会在末位用整段得到 16。

- 得分基于删除当时的长度；交换论证是把它转回原数组长度的必要桥梁。
- `dp[left-1]` 不能写成 `dp[left]`，否则重复使用块左端。
- 首次出现的位置本身仍可作为单点结束，不要跳过 `dp[index-1]+1`。
- 平方必须先转 `long long`。

## 方案比较

指数枚举适合证明覆盖和随机 oracle；记忆化递归可以降到与状态数相关的多项式，但仍需查找配对端点。一维 DP 利用“每值恰两次”把转移压成常数，时间、空间和实现风险都最低。竞赛中优先记住“凸收益允许吸收内部操作 → 原数组分块 → 前缀 DP”的推导链，而不是只背递推式。

## 变种一：恢复一个最优删除分块方案

新定义：除最大得分外，输出每个原数组块的左右端点。记录每个 `dp[i]` 来自单点还是配对块，再回溯。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  int length = 2 * n;
  vector<int> first(n + 1, -1), parent(length + 1), blockLeft(length + 1);
  vector<long long> dp(length + 1);
  for (int index = 1; index <= length; ++index) {
    int value;
    cin >> value;
    dp[index] = dp[index - 1] + 1;
    parent[index] = index - 1;
    blockLeft[index] = index;
    if (first[value] == -1) {
      first[value] = index;
    } else {
      int left = first[value];
      long long block = index - left + 1;
      long long candidate = dp[left - 1] + block * block;
      if (candidate > dp[index]) {
        dp[index] = candidate;
        parent[index] = left - 1;
        blockLeft[index] = left;
      }
    }
  }
  vector<pair<int, int>> blocks;
  for (int end = length; end > 0; end = parent[end]) {
    blocks.push_back({blockLeft[end], end});
  }
  reverse(blocks.begin(), blocks.end());
  cout << dp[length] << '\n';
  for (auto [left, right] : blocks) {
    cout << left << ' ' << right << '\n';
  }
}
```

时间 $O(n)$，空间 $O(n)$。按输出块从左到右操作即可实现同一得分。

## 变种二：每个值可以出现多次

新定义：值的出现次数不再限定为 2。最后块可由任意一对同值端点界定，需要枚举此前所有同值位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int length;
  cin >> length;
  vector<int> values(length + 1);
  for (int i = 1; i <= length; ++i) {
    cin >> values[i];
  }
  unordered_map<int, vector<int>> positions;
  vector<long long> dp(length + 1);
  for (int index = 1; index <= length; ++index) {
    dp[index] = dp[index - 1] + 1;
    for (int left : positions[values[index]]) {
      long long block = index - left + 1;
      dp[index] = max(dp[index], dp[left - 1] + block * block);
    }
    positions[values[index]].push_back(index);
  }
  cout << dp[length] << '\n';
}
```

最坏时间 $O(L^2)$，空间 $O(L)$。次数限制正是原题线性转移的来源。

## 变种三：得分改为长度的 $p$ 次方

新定义：得分为 $length^p$，其中整数 $p\ge1$，并保证结果不超过 64 位。函数仍超可加：$(u+v)^p\ge u^p+v^p$，交换与分块证明保持。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long power(long long base, int exponent) {
  long long answer = 1;
  while (exponent-- > 0) {
    answer *= base;
  }
  return answer;
}
int main() {
  int n, exponent;
  cin >> n >> exponent;
  vector<int> first(n + 1, -1);
  vector<long long> dp(2 * n + 1);
  for (int index = 1; index <= 2 * n; ++index) {
    int value;
    cin >> value;
    dp[index] = dp[index - 1] + 1;
    if (first[value] == -1) {
      first[value] = index;
    } else {
      int left = first[value];
      dp[index] = max(dp[index], dp[left - 1] + power(index - left + 1, exponent));
    }
  }
  cout << dp[2 * n] << '\n';
}
```

时间 $O(np)$，空间 $O(n)$。若 $0<p<1$，超可加性失效，原交换论证不能沿用。

## 变种四：元素带正权，得分为块权重和的平方

新定义：每个位置有正权 $w_i$，一次删除块得分为 $(\sum w_i)^2$。正权保证吸收内部块仍不劣，用权重前缀和替换长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  int length = 2 * n;
  vector<int> values(length + 1), first(n + 1, -1);
  vector<long long> prefix(length + 1), dp(length + 1);
  for (int i = 1; i <= length; ++i) {
    cin >> values[i];
  }
  for (int i = 1; i <= length; ++i) {
    long long weight;
    cin >> weight;
    prefix[i] = prefix[i - 1] + weight;
    dp[i] = dp[i - 1] + weight * weight;
    int value = values[i];
    if (first[value] == -1) {
      first[value] = i;
    } else {
      int left = first[value];
      long long total = prefix[i] - prefix[left - 1];
      dp[i] = max(dp[i], dp[left - 1] + total * total);
    }
  }
  cout << dp[length] << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。允许负权后，吸收内部元素可能降低平方前的绝对值，需重新建模。

## 可复现验证

所有程序按 GNU++23 编译。线性 DP 与合法分块指数枚举在随机小规模配对数组上对拍，并逐项复现六组官方样例；另覆盖相邻配对、完全嵌套、完全交叉与 $n=1$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/C)
- [对应知识专题](../../dp/sequence-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-513-q2-lc4011/">← [力扣竞赛] 第 513 场周赛 Q2 LC 4011 按奇偶比统计子数组 I 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-04-lc3731/">[力扣每日一题] 2026-08-04｜LC 3731 找出缺失的元素 →</a>
</nav>
