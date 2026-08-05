---
title: "[力扣每日一题] 2026-08-06｜LC 3345 最小可整除数位乘积 I"
---

# [力扣每日一题] 2026-08-06｜LC 3345 最小可整除数位乘积 I

<p class="daily-archive-kicker">2026-08-06 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8741cb6cda20a0b211a0555f7e3191cac443507f13b7830be1533065e0440471 -->
## 官方原始信息

- 日期：2026-08-06（Asia/Shanghai）。
- 题号：LC 3345。
- 官方中文标题：最小可整除数位乘积 I。
- 官方难度：简单。
- 官方链接：[最小可整除数位乘积 I](https://leetcode.cn/problems/smallest-divisible-digit-product-i/)

### 原始题意与函数签名

给定正整数 `n,t`，返回不小于 `n` 的最小整数，使其十进制各数位之积能被 `t` 整除。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int smallestNumber(int n, int t);
};
```

### 全部官方样例

```text
输入：n = 10, t = 2
输出：10
解释：10 的数位积为 0，可被 2 整除。
```

```text
输入：n = 15, t = 3
输出：16
解释：16 的数位积为 6，可被 3 整除。
```

### 全部约束

- $1\le n\le100$。
- $1\le t\le10$。

## 约束推导与观察

候选整数最多三位，直接从 `n` 递增检验已经足够。更强的是：任意 10 个连续整数中都有一个十进制个位为 0，其数位积为 0，而 $0$ 能被任意正整数 `t` 整除。因此答案一定在 `[n,n+9]`，搜索次数是严格常数。数位积最大也很小，但通用实现仍用 `int` 即可。

## 解法递进

### 解法一：无界顺序枚举

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int digitProduct(int value) {
    int product = 1;
    while (value > 0) {
      product *= value % 10;
      value /= 10;
    }
    return product;
  }
public:
  int smallestNumber(int n, int t) {
    for (int value = n;; ++value) {
      if (digitProduct(value) % t == 0) {
        return value;
      }
    }
  }
};
```

每个候选检查 $O(\log n)$；借助下一个十的倍数，候选数实际上不超过 10。

### 最佳实用解：显式使用九步上界

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int digitProduct(int value) {
    int product = 1;
    while (value > 0) {
      product *= value % 10;
      value /= 10;
    }
    return product;
  }
public:
  int smallestNumber(int n, int t) {
    for (int value = n; value <= n + 9; ++value) {
      if (digitProduct(value) % t == 0) {
        return value;
      }
    }
    return -1;
  }
};
```

最多检查 10 个整数，时间 $O(\log n)$、空间 $O(1)$；末尾 `-1` 由证明知不可达。它最直接，优先记忆。

## 正确性证明

算法按严格递增顺序检查从 `n` 开始的每个候选，因此返回的第一个合格值必为最小值。令 $q=10\lceil n/10\rceil$，则 $n\le q\le n+9$，且 `q` 的个位为 0，数位积为 0。因为 `t>0` 且 $0\bmod t=0$，`q` 必合格，所以循环一定在上界内返回。两部分共同证明算法终止且答案正确。

## 样例手推

`n=15,t=3`：15 的数位积为 5，不整除 3；16 的数位积为 6，立即返回 16。`n=10` 自身含 0，任何 `t` 都直接返回 10。边界 `n=99,t=10` 时 99 不合格，100 的数位积为 0，返回 100。

## 易错点与方案比较

- 0 的数位积在本题语义下为 0；候选本身为正，不需定义整数 0 的空乘积。
- 判断是“数位积被 `t` 整除”，写作 `product % t == 0`。
- 不要误求“各数位分别被 `t` 整除”。
- 数位 DP 在本题范围完全多余；常数次枚举证明更短、更稳定。

## 变种一：改为 `B` 进制

新定义：$2\le B\le36$，求不小于 `n` 的最小数，使其 `B` 进制数位积被 `t` 整除。下一个 `B` 的倍数末位为 0，最多检查 `B` 个候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long digitProduct(long long value, int base) {
  long long product = 1;
  while (value > 0) {
    product *= value % base;
    value /= base;
  }
  return product;
}
int main() {
  long long n, t;
  int base;
  cin >> n >> t >> base;
  for (long long value = n; value < n + base; ++value) {
    if (digitProduct(value, base) % t == 0) {
      cout << value << '\n';
      return 0;
    }
  }
}
```

时间 $O(B\log_B n)$，空间 $O(1)$。

## 变种二：候选整数本身也必须被 `t` 整除

原来的十倍数保证不再充分；但 `lcm(10,t)` 的倍数同时满足自身整除 `t` 且数位积为 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int digitProduct(int value) {
  int product = 1;
  while (value > 0) {
    product *= value % 10;
    value /= 10;
  }
  return product;
}
int main() {
  int n, t;
  cin >> n >> t;
  int period = lcm(10, t);
  int upper = (n + period - 1) / period * period;
  for (int value = n; value <= upper; ++value) {
    if (value % t == 0 && digitProduct(value) % t == 0) {
      cout << value << '\n';
      return 0;
    }
  }
}
```

对原范围 `t<=10`，最多检查 90 个候选；空间 $O(1)$。

## 变种三：大量 `n` 查询、固定 `t`

新定义：所有 `n<=limit`。从右向左预计算 `next[i]` 为最小合格数，每问 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int digitProduct(int value) {
  int product = 1;
  while (value > 0) {
    product *= value % 10;
    value /= 10;
  }
  return product;
}
int main() {
  int limit, t, q;
  cin >> limit >> t >> q;
  vector<int> next(limit + 11);
  int nearest = -1;
  for (int value = limit + 10; value >= 1; --value) {
    if (digitProduct(value) % t == 0) {
      nearest = value;
    }
    next[value] = nearest;
  }
  while (q--) {
    int n;
    cin >> n;
    cout << next[n] << '\n';
  }
}
```

预处理 $O(limit\log limit)$，空间 $O(limit)$，每问 $O(1)$。

## 变种四：统计区间内数位积可整除 `t` 的整数

新定义：$1\le L\le R\le10^{18}$、`t<=100`，求计数。数位 DP 记录位置、当前积模 `t`、是否已开始和上界约束；数字内部出现 0 后余数自然变 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countUpTo(long long bound, int t) {
  if (bound <= 0) {
    return 0;
  }
  string digits = to_string(bound);
  long long memo[20][101][2];
  memset(memo, -1, sizeof(memo));
  function<long long(int, int, bool, bool)> dfs = [&](int position, int remainder, bool started,
                                                      bool tight) {
    if (position == static_cast<int>(digits.size())) {
      return static_cast<long long>(started && remainder == 0);
    }
    if (!tight && memo[position][remainder][started] != -1) {
      return memo[position][remainder][started];
    }
    int upper = tight ? digits[position] - '0' : 9;
    long long answer = 0;
    for (int digit = 0; digit <= upper; ++digit) {
      bool nextStarted = started || digit != 0;
      int nextRemainder = remainder;
      if (nextStarted) {
        nextRemainder = started ? remainder * digit % t : digit % t;
      }
      answer += dfs(position + 1, nextRemainder, nextStarted, tight && digit == upper);
    }
    if (!tight) {
      memo[position][remainder][started] = answer;
    }
    return answer;
  };
  return dfs(0, 1 % t, false, true);
}
int main() {
  long long left, right;
  int t;
  cin >> left >> right >> t;
  cout << countUpTo(right, t) - countUpTo(left - 1, t) << '\n';
}
```

时间 $O(20\cdot t\cdot10)$，空间 $O(20t)$。

## 可复现验证

枚举 `n=1..100`、`t=1..10`，与从 `n` 扫到首个十倍数的独立 oracle 比较；固定覆盖自身合格、含零、`n=99`、`t=1` 与 `t=10`。最佳源码通过 GNU++23 编译、两组官方样例及边界测试，并作为当天提交源码的唯一算法来源。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/smallest-divisible-digit-product-i/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-e/">← [codeforces] CF Round 1113 Div.2 E Excuse for Breaks</a>
<span class="daily-archive-pager__empty"></span>
</nav>
