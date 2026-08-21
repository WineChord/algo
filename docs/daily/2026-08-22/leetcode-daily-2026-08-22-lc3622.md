---
title: "[力扣每日一题] 2026-08-22｜LC 3622 判断整除性"
---

# [力扣每日一题] 2026-08-22｜LC 3622 判断整除性

<p class="daily-archive-kicker">2026-08-22 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-22 题目列表</a> · <a href="../../../math/#digit-sum-product-divisibility">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c55e58e831d28a7fabe3cb88bb386dc92f0278058548c5e70142d5287275378a -->
[力扣官方题目：3622. 判断整除性](https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/)

## 官方原始信息

- 北京时间每日一题日期：2026-08-22；题号：LC 3622。
- 官方中文标题：判断整除性；官方难度：简单。
- 官方链接：[https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/](https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/)
- 函数签名：`bool checkDivisibility(int n)`。
- 原竞赛：第 459 场周赛 Q1。
- ZeroTracer 社区估算竞赛分：1148.94，抓取于 2026-08-22；这不是力扣官方难度或分值。
- 官方标签：数学。

### 原始题意

给定正整数 `n`。计算它的十进制各位数字之和 `sum` 与各位数字之积 `product`；若 `n` 能被
`sum + product` 整除，返回 `true`，否则返回 `false`。

### 全部官方样例

```text
示例 1
输入：n = 99
输出：true
解释：数字和为 9 + 9 = 18，数字积为 9 * 9 = 81，18 + 81 = 99，99 可以整除 99。

示例 2
输入：n = 23
输出：false
解释：数字和为 2 + 3 = 5，数字积为 2 * 3 = 6，5 + 6 = 11，23 不能整除 11。
```

### 全部约束

- $1\le n\le10^6$。

## 最优结论摘要

逐位取 `digit = value % 10`，同时累加数字和 $s$ 并累乘数字积 $p$，再令

$$
d=s+p.
$$

答案是 `n % d == 0`。十进制位数为 $L$ 时，时间复杂度 $O(L)=O(\log n)$，额外空间
$O(1)$。

## 约束推导、溢出与边界

- 只需扫描数字，枚举因数或倍数都没有必要。
- $n\le10^6$ 最多 7 位；数字积最大不超过 $9^7=4\,782\,969$，`int` 足够。
- `n` 为正数，所以至少有一位。数字和至少为 1，即使数字积因 0 变成 0，除数也不会为 0。
- 数字 0 会把整个数字积变成 0，不能把它当乘法单位跳过。
- 必须保留原始 `n`；若直接把它除到 0，最后会错误地检查 `0 % d`。

## 样例手推

对 `n = 99`，两次迭代依次得到 `(sum, product) = (9, 9)`、`(18, 81)`，除数为 99，余数
为 0。对 `n = 23`，得到除数 11，而 $23\bmod11=1$，故返回 `false`。

边界 `n = 10` 中数字和为 1、数字积为 0，除数为 1，所以返回 `true`；这也验证了零数字处理。

## 解法一：字符串扫描

把数字转为十进制字符串，按字符计算和与积。它直观、便于调试，时间与空间均为 $O(L)$；
额外字符串不是必要的，但可作为独立实现和测试 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool checkDivisibility(int n) {
    string digits = to_string(n);
    int sum = 0;
    int product = 1;
    for (char character : digits) {
      int digit = character - '0';
      sum += digit;
      product *= digit;
    }
    return n % (sum + product) == 0;
  }
};
```

## 从字符串到原地取位

十进制末位是 `value % 10`，删去末位是 `value /= 10`。因此可用一个副本从低位到高位扫描，
无需分配字符串。和与积都满足交换律，扫描方向不影响结果。

## 最佳实用解：除十取余

### 正确性证明

设 `value` 在一次循环前包含尚未处理的十进制前缀。`value % 10` 恰是其中最低位，加入 `sum`
并乘入 `product` 后，`value /= 10` 恰好删除这一位。这个循环不变量保证每一位被处理一次且仅
一次。循环结束后，`sum`、`product` 分别等于原数全部十进制位之和与之积，因此最终取模判断
与题目定义完全一致。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool checkDivisibility(int n) {
    int value = n;
    int sum = 0;
    int product = 1;
    while (value > 0) {
      int digit = value % 10;
      sum += digit;
      product *= digit;
      value /= 10;
    }
    return n % (sum + product) == 0;
  }
};
```

时间复杂度 $O(\log n)$，额外空间 $O(1)$。

## 同阶方案比较与易错点

字符串方案的意图最直观；算术方案无分配、常数更小，也自然迁移到任意进制。面试与竞赛中
优先记忆算术方案。

- 把数字积初始为 0，会让所有输入的积都错误地保持 0。
- 遇到数字 0 时跳过乘法；标准数字积必须变为 0。
- 修改 `n` 本身后再取模，导致被除数变成 0。
- 把条件写反：题目问的是 `n` 能否被两者之和整除，即 `n % divisor == 0`。

## 可复现验证

两种原题实现均以 C++23 编译，通过全部官方样例及 `1`、`10`、`1000000`、全为 9、含多个 0
等边界。对 $1\le n\le10^6$ 穷举比较字符串与算术实现，1,000,000 个输入全部一致。

## Follow-up 与约束变种

### 变种一：任意进制

新定义：给定 `2 <= base <= 36`，按 `base` 进制数字计算和与积。十进制写死的 `% 10`、`/ 10`
失效，改为 `% base`、`/ base` 即可。对 `n <= 10^18` 使用 `__int128` 保存乘积，时间
$O(\log_{base} n)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool checkInBase(long long n, int base) {
    long long value = n;
    __int128 sum = 0;
    __int128 product = 1;
    while (value > 0) {
      int digit = value % base;
      sum += digit;
      product *= digit;
      value /= base;
    }
    __int128 divisor = sum + product;
    return static_cast<__int128>(n) % divisor == 0;
  }
};
```

### 变种二：统计区间内满足条件的整数

新定义：返回 `[1, limit]` 中满足原条件的整数个数，`limit <= 10^6`。单个数的判定仍成立，
但必须对每个候选执行一次；时间 $O(limit\log limit)$，空间 $O(1)$。若范围扩大到数位级别，
由于“积 + 和”参与整除，常规只记录模数的数位 DP 不再有固定小状态，需要进一步限制位数或
枚举可能的和与积。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool valid(int n) {
    int value = n;
    int sum = 0;
    int product = 1;
    while (value > 0) {
      int digit = value % 10;
      sum += digit;
      product *= digit;
      value /= 10;
    }
    return n % (sum + product) == 0;
  }
public:
  int countDivisible(int limit) {
    int answer = 0;
    for (int value = 1; value <= limit; ++value) answer += valid(value);
    return answer;
  }
};
```

### 变种三：零数字不参与乘积

新定义：数字积只乘非零位；例如 105 的非零数字积为 5。原算法遇到 0 后永久归零，因而失效；
扫描时仅在 `digit != 0` 时乘入。复杂度仍为 $O(\log n)$ 与 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool checkIgnoringZeros(int n) {
    int value = n;
    int sum = 0;
    int product = 1;
    while (value > 0) {
      int digit = value % 10;
      sum += digit;
      if (digit != 0) product *= digit;
      value /= 10;
    }
    return n % (sum + product) == 0;
  }
};
```

### 变种四：输入是超长十进制字符串

新定义：`n` 最多 2,000 位，仍需做精确的“数字和 + 数字积”整除判断。内置整数会溢出，
必须把数字积提升为大整数，并用十进制长除法计算余数。下面实现以 $10^9$ 为基数的非负大
整数；每读一位，余数乘 10 加当前位，再至多减去除数 9 次。时间 $O(L^2)$，空间 $O(L)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct BigInteger {
  static constexpr unsigned int BASE = 1000000000;
  vector<unsigned int> digit{0};
  void normalize() {
    while (digit.size() > 1 && digit.back() == 0) digit.pop_back();
  }
  void multiply(unsigned int value) {
    unsigned long long carry = 0;
    for (unsigned int& current : digit) {
      unsigned long long product = 1ULL * current * value + carry;
      current = product % BASE;
      carry = product / BASE;
    }
    if (carry != 0) digit.push_back(carry);
    normalize();
  }
  void add(unsigned int value) {
    unsigned long long carry = value;
    for (unsigned int& current : digit) {
      unsigned long long sum = current + carry;
      current = sum % BASE;
      carry = sum / BASE;
      if (carry == 0) return;
    }
    digit.push_back(carry);
  }
  bool operator>=(const BigInteger& other) const {
    if (digit.size() != other.digit.size()) return digit.size() > other.digit.size();
    for (int i = static_cast<int>(digit.size()) - 1; i >= 0; --i) {
      if (digit[i] != other.digit[i]) return digit[i] > other.digit[i];
    }
    return true;
  }
  void subtract(const BigInteger& other) {
    long long borrow = 0;
    for (int i = 0; i < static_cast<int>(digit.size()); ++i) {
      long long value = 1LL * digit[i] - borrow;
      if (i < static_cast<int>(other.digit.size())) value -= other.digit[i];
      if (value < 0) {
        value += BASE;
        borrow = 1;
      } else {
        borrow = 0;
      }
      digit[i] = value;
    }
    normalize();
  }
  bool isZero() const {
    return digit.size() == 1 && digit[0] == 0;
  }
};
class Solution {
public:
  bool checkLargeDivisibility(const string& digits) {
    BigInteger divisor;
    divisor.digit[0] = 1;
    int sum = 0;
    for (char character : digits) {
      int digit = character - '0';
      sum += digit;
      divisor.multiply(digit);
    }
    divisor.add(sum);
    BigInteger remainder;
    for (char character : digits) {
      remainder.multiply(10);
      remainder.add(character - '0');
      while (remainder >= divisor) remainder.subtract(divisor);
    }
    return remainder.isZero();
  }
};
```

## 推荐记忆

数字属性题先保留原数，再用副本做“取末位、删末位”。本题的唯一特殊点是 0 会把数字积变为
0；把这一边界处理正确后，整除判断只是一次普通取模。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/)
- [对应知识专题](../../math/index.md#digit-sum-product-divisibility)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-e/">← [codeforces] CF Round 1117 Div.2 E Busy Beaver</a>
<span class="daily-archive-pager__empty"></span>
</nav>
