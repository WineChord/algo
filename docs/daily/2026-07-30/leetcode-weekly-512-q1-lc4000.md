---
title: "[力扣竞赛] 第 512 场周赛 Q1 LC 4000 给定数位和的最大整数 简单"
---

# [力扣竞赛] 第 512 场周赛 Q1 LC 4000 给定数位和的最大整数 简单

<p class="daily-archive-kicker">2026-07-30 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=de8890f4e0e7dafa31c8df8fd16bad3290ad00d92de2c67edb62a96790d8258f -->
## 官方原始信息

- 来源：力扣中国
- 比赛：第 512 场周赛
- 题目序号：Q1
- 题号：LC 4000
- 官方中文标题：给定数位和的最大整数
- 官方难度：简单
- 官方比赛分值：3 分
- ZeroTracer 社区估算竞赛分：未知（抓取于 2026-07-30）
- 官方链接：[给定数位和的最大整数](https://leetcode.cn/problems/largest-integer-with-given-digit-sum/)

### 原始题意

给定非负整数 `n` 与 `s`，返回十进制表示最多含 `n` 位、各位数字和恰为 `s` 的最大非负整数；不存在则返回 -1。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int largestInteger(int n, int s);
};
```

### 全部官方样例

```text
输入：n = 2, s = 9
输出：90
解释：最多两位且数位和为 9 的最大整数是 90。
```

```text
输入：n = 2, s = 19
输出：-1
解释：两位十进制数的数位和最多为 18。
```

```text
输入：n = 5, s = 0
输出：0
解释：数位和为 0 的唯一非负整数是 0。
```

### 全部约束

- $1\le n\le5$。
- $0\le s\le100$。
- 每个十进制位在 $[0,9]$ 内，因此可行必要且充分条件为 $s\le9n$。
- 最多五位，结果在 `int` 范围内。

## 约束推导与贪心选择

比较两个等长十进制数时，第一处不同的高位决定大小。为了让结果最大，应从最高位开始放入尽可能大的数字；当前位最多取 9，也不能超过剩余数位和。若 $s=0$，规范十进制表示应返回 0，而不是若干前导零。

## 解法递进

### 解法一：枚举所有候选整数

从 0 扫描到 $10^n-1$，检查数位和并保留最大值。当前 $n\le5$ 时至多枚举十万个数，能通过但没有利用结构。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int digitSum(int value) {
    int sum = 0;
    do {
      sum += value % 10;
      value /= 10;
    } while (value > 0);
    return sum;
  }
public:
  int largestInteger(int n, int s) {
    int limit = 1;
    for (int i = 0; i < n; ++i) {
      limit *= 10;
    }
    int answer = -1;
    for (int value = 0; value < limit; ++value) {
      if (digitSum(value) == s) {
        answer = value;
      }
    }
    return answer;
  }
};
```

时间 $O(n10^n)$，空间 $O(1)$。

### 最佳实用解：高位优先填 9

若 `s > 9*n` 则无解。否则从高位到低位，每位取 `min(9,s)`，并从剩余和中扣除。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestInteger(int n, int s) {
    if (s > 9 * n) {
      return -1;
    }
    int answer = 0;
    for (int position = 0; position < n; ++position) {
      int digit = min(9, s);
      answer = answer * 10 + digit;
      s -= digit;
    }
    return answer;
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(1)$。

## 正确性证明

设贪心与任意最优答案第一次不同的位置为 `p`。在此前所有高位相同。贪心在 `p` 放置了当前可用的最大数字 $\min(9,remain)$。

若另一答案该位更大，则超过 9 或超过剩余数位和，不可行；若该位更小，即使把少放的数位和分配到更低位，也无法抵消第 `p` 位变小带来的十进制位权损失。因此任何可行答案在第一处不同位置都不可能大于贪心答案，贪心全局最大。

当 $s\le9n$ 时，每次最多取 9，剩余位置总容量始终足以容纳剩余和，最终恰好用完；所以可行性也得到保证。

## 样例手推

`n=2,s=9`：最高位取 9，剩余 0；下一位取 0，得到 90。若尝试 81、72 等，最高位都小于 9，因此必然更小。

## 易错点与方案比较

- “最多 `n` 位”允许前导零；实现固定循环 `n` 位后，整数运算会自然去掉前导零。
- $s=0$ 返回 0。
- 无解条件不是 `s>n`，而是 `s>9n`。
- 最大化必须从高位开始放大；从低位填 9 会得到最小一类结果。
- 枚举解可作小规模 oracle；贪心解更快、更能推广，推荐记忆交换论证。

## 变种一：求满足数位和的最小非负整数

新定义：仍限制最多 `n` 位，但求最小整数。`s=0` 返回 0；`s>0` 时最高位不能为 0。为了最小化，应把尽可能多的数位和放到低位，同时保证高位至少承担无法放入剩余位置的部分。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, sum;
  cin >> n >> sum;
  if (sum == 0) {
    cout << 0 << '\n';
    return 0;
  }
  if (sum > 9 * n) {
    cout << -1 << '\n';
    return 0;
  }
  string answer(n, '0');
  --sum;
  for (int i = n - 1; i >= 1; --i) {
    int digit = min(9, sum);
    answer[i] = static_cast<char>('0' + digit);
    sum -= digit;
  }
  answer[0] = static_cast<char>('1' + sum);
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。先为最高位预留 1，再从最低位填 9，可以避免前导零。

## 变种二：必须恰好有 $n$ 位

新定义：首位不能为 0。可行条件变为 $1\le s\le9n$。最大值仍高位优先填 9，但最后必须保证剩余位置至少能完成总和；对最大化而言直接填 9 仍安全，只需排除 $s=0$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, sum;
  cin >> n >> sum;
  if (sum < 1 || sum > 9 * n) {
    cout << -1 << '\n';
    return 0;
  }
  string answer;
  for (int i = 0; i < n; ++i) {
    int digit = min(9, sum);
    answer.push_back(static_cast<char>('0' + digit));
    sum -= digit;
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种三：改为任意进制

新定义：在 $B$ 进制下最多 `n` 位，数位和为 `s`，求最大数的数位序列。每位上限从 9 改为 $B-1$；为支持 $B>10$，输出整数数位数组。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int base, n, sum;
  cin >> base >> n >> sum;
  if (base < 2 || sum > (base - 1) * n) {
    cout << -1 << '\n';
    return 0;
  }
  vector<int> digits;
  for (int i = 0; i < n; ++i) {
    int digit = min(base - 1, sum);
    digits.push_back(digit);
    sum -= digit;
  }
  for (int digit : digits) {
    cout << digit << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；贪心证明只依赖位权从高到低严格递减。

## 变种四：`n` 很大，答案必须以字符串返回

新定义：`n` 可达 $10^5$，结果不再能放入内置整数。算法不变，直接构造字符串，前导零可按规范去除。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long sum;
  cin >> n >> sum;
  if (sum > 9LL * n) {
    cout << -1 << '\n';
    return 0;
  }
  string answer;
  answer.reserve(n);
  for (int i = 0; i < n; ++i) {
    int digit = min(9LL, sum);
    answer.push_back(static_cast<char>('0' + digit));
    sum -= digit;
  }
  if (answer.find_first_not_of('0') == string::npos) {
    cout << 0 << '\n';
  } else {
    cout << answer << '\n';
  }
}
```

时间与输出空间均为 $O(n)$。不能用数值乘 10 累加，否则会溢出。

## 可复现验证

- 三个官方样例、`s=0`、`s=9n`、`s=9n+1` 与 `n=1` 均应覆盖。
- 在官方 $n\le5$ 范围可把枚举解作为 oracle，与贪心结果穷举对拍。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/largest-integer-with-given-digit-sum/)
- [第 512 场周赛](https://leetcode.cn/contest/weekly-contest-512/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/largest-integer-with-given-digit-sum/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-50-lc32/">← [力扣 Top 50] LC 32 最长有效括号 困难</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-d2/">[codeforces] CF Round 1111 Div.2 D2 XOR Sorting (Hard Version) →</a>
</nav>
