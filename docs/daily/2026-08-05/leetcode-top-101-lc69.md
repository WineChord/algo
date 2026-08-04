---
title: "[力扣 Top 101] LC 69 x 的平方根 简单"
---

# [力扣 Top 101] LC 69 x 的平方根 简单

<p class="daily-archive-kicker">2026-08-05 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=9c8cbb93c29225e3696d30fbea6d61f4228031af96263fb88af7f9f00a8924b0 -->
## 官方原始信息

- Top 排名：101
- 题号：LC 69
- 官方中文标题：x 的平方根
- 官方难度：简单
- 官方链接：[x 的平方根](https://leetcode.cn/problems/sqrtx/)

### 原始题意

给定非负整数 `x`，返回其算术平方根向下取整后的整数。不得调用 `pow`、指数运算符等内置幂函数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int mySqrt(int x);
};
```

### 全部官方样例

```text
输入：x = 4
输出：2
```

```text
输入：x = 8
输出：2
解释：sqrt(8) 约为 2.82842，舍去小数部分后为 2。
```

### 全部约束

- $0\le x\le2^{31}-1$。

## 约束推导与观察

答案是满足 $r^2\le x$ 的最大非负整数。布尔条件“$m^2\le x$”随 $m$ 增大只会从真变假，因此可以二分最后一个可行值。若直接使用 32 位 `int` 计算 `m * m`，接近上界时会溢出；可以提升到 64 位，或使用等价且更通用的判定 $m\le\lfloor x/m\rfloor$。

答案最大为 46340，返回 `int` 安全。任何方法都不应对 `x = 0` 执行除零。

## 解法递进

### 解法一：从 0 线性枚举

依次尝试下一个整数，直到其平方超过 `x`。用 64 位乘法保证判定安全。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int mySqrt(int x) {
    long long root = 0;
    while ((root + 1) * (root + 1) <= x) {
      ++root;
    }
    return static_cast<int>(root);
  }
};
```

时间 $O(\sqrt{x})$，额外空间 $O(1)$。瓶颈是逐个排除候选值。

### 最佳实用解：二分最后一个平方不超过 `x` 的整数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int mySqrt(int x) {
    long long left = 0;
    long long right = x;
    long long answer = 0;
    while (left <= right) {
      long long middle = left + (right - left) / 2;
      bool feasible = middle == 0 || middle <= x / middle;
      if (feasible) {
        answer = middle;
        left = middle + 1;
      } else {
        right = middle - 1;
      }
    }
    return static_cast<int>(answer);
  }
};
```

时间 $O(\log x)$，额外空间 $O(1)$。它直接对应单调边界，证明和实现都稳定，是面试优先记忆的方案。

### 同阶方案：整数牛顿迭代

由 $r=(r+x/r)/2$ 反复改进高估值，直到 $r^2\le x$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int mySqrt(int x) {
    if (x < 2) {
      return x;
    }
    long long root = x;
    while (root > x / root) {
      root = (root + x / root) / 2;
    }
    return static_cast<int>(root);
  }
};
```

迭代次数为 $O(\log x)$，空间 $O(1)$，通常常数更小；但单调收敛与取整细节比二分更难证明，竞赛中已熟练时再使用。

## 正确性证明

记 $P(m)$ 为 $m^2\le x$。对非负整数，若 $P(m)$ 为假，则所有更大的整数也为假，因此可行集合必为前缀。二分过程中，`answer` 始终是已验证可行的最大候选；若 `middle` 可行，答案不小于它，故丢弃左半段并向右找；否则答案小于它，故丢弃右半段。循环结束时所有大于 `answer` 的候选均已判为不可行，而 `answer` 自身可行，所以它恰是 $\lfloor\sqrt{x}\rfloor$。

## 样例手推

对 `x = 8`，可行整数为 0、1、2，3 已满足 $3^2>8$。二分最终保留 2。边界 `x = 0` 直接把 0 记为可行；`x = 2^{31}-1` 的答案为 46340，使用除法判定不会发生乘法溢出。

## 易错点与方案比较

- `middle * middle` 若使用 `int` 会溢出。
- 求的是向下取整，不是四舍五入，也不是最接近的整数。
- 除法判定要单独容纳 `middle = 0`。
- 二分和牛顿迭代同为对数级；二分的循环不变量更透明，牛顿法常数更好但边界更敏感。

## 变种一：计算 64 位无符号整数平方根

新定义：输入扩展到 $0\le x\le2^{64}-1$。平方一定可能溢出 64 位，因此只用除法判定；答案不超过 $2^{32}-1$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  unsigned long long x;
  cin >> x;
  unsigned long long left = 0;
  unsigned long long right = 1ULL << 32;
  unsigned long long answer = 0;
  while (left <= right) {
    unsigned long long middle = left + (right - left) / 2;
    bool feasible = middle == 0 || middle <= x / middle;
    if (feasible) {
      answer = middle;
      left = middle + 1;
    } else {
      right = middle - 1;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(32)$，空间 $O(1)$。原二分结构仍成立，只有溢出判定必须升级。

## 变种二：判断一个整数是否为完全平方数

新定义：返回是否存在整数 $r$ 使 $r^2=x$。先求向下取整平方根，再用除法与余数核验，避免最终乘法。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long x;
  cin >> x;
  long long left = 0;
  long long right = min(x, 3037000499LL);
  long long root = 0;
  while (left <= right) {
    long long middle = left + (right - left) / 2;
    if (middle == 0 || middle <= x / middle) {
      root = middle;
      left = middle + 1;
    } else {
      right = middle - 1;
    }
  }
  bool square = root == 0 ? x == 0 : x / root == root && x % root == 0;
  cout << (square ? "true" : "false") << '\n';
}
```

时间 $O(\log x)$，空间 $O(1)$。

## 变种三：求非负整数的 $k$ 次方根向下取整

新定义：$0\le x\le10^{18}$、$1\le k\le60$。可行性检查逐次乘法，并在乘前判断是否会超过 `x`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool powerAtMost(unsigned long long base, int exponent, unsigned long long limit) {
  unsigned long long value = 1;
  for (int i = 0; i < exponent; ++i) {
    if (base != 0 && value > limit / base) {
      return false;
    }
    value *= base;
  }
  return value <= limit;
}
int main() {
  unsigned long long x;
  int k;
  cin >> x >> k;
  unsigned long long left = 0;
  unsigned long long right = x;
  unsigned long long answer = 0;
  while (left <= right) {
    unsigned long long middle = left + (right - left) / 2;
    if (powerAtMost(middle, k, x)) {
      answer = middle;
      left = middle + 1;
    } else {
      right = middle - 1;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(k\log x)$，空间 $O(1)$。原平方专用除法判定不再够用，需通用的受限幂检查。

## 变种四：大量小值域询问

新定义：有 $q$ 次询问且所有 $x\le10^7$。一次线性预处理每个整数的平方根，随后每问 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<int> query(q);
  int maximum = 0;
  for (int& x : query) {
    cin >> x;
    maximum = max(maximum, x);
  }
  vector<int> root(maximum + 1);
  int current = 0;
  for (int x = 0; x <= maximum; ++x) {
    while (1LL * (current + 1) * (current + 1) <= x) {
      ++current;
    }
    root[x] = current;
  }
  for (int x : query) {
    cout << root[x] << '\n';
  }
}
```

预处理 $O(U)$、查询总计 $O(q)$、空间 $O(U)$。当询问不多或值域很大时，逐问二分更节省内存。

## 验证说明

本轮将七段代码按 C++23 编译；主解与线性枚举会对拍全部 $0\le x\le10^6$，再覆盖 0、1、2、完全平方数两侧以及 $2^{31}-1$。64 位与 $k$ 次根变种另用 `__int128` 仅作为私有 oracle 随机核验。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/sqrtx/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-d/">← [atcoder] ABC469 D The Big Two</a>
<a class="daily-archive-pager__next" href="../leetcode-top-102-lc647/">[力扣 Top 102] LC 647 回文子串 中等 →</a>
</nav>
