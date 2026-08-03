---
title: "[力扣 Top 96] LC 7 整数反转 中等"
---

# [力扣 Top 96] LC 7 整数反转 中等

<p class="daily-archive-kicker">2026-08-04 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8c6f10baece161935343f9739f626983f2805d8de466dbe72e9ad1fc886dd7f3 -->
## 官方原始信息

- Top 排名：96
- 题号：LC 7
- 官方中文标题：整数反转
- 官方难度：中等
- 官方链接：[整数反转](https://leetcode.cn/problems/reverse-integer/)

### 原始题意

给定一个 32 位有符号整数，反转其十进制数字部分；若结果超出 32 位有符号整数范围，则返回 0。运行环境不允许借助 64 位整数暂存结果。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int reverse(int x);
};
```

### 全部官方样例

```text
输入：x = 123
输出：321
```

```text
输入：x = -123
输出：-321
```

```text
输入：x = 120
输出：21
```

```text
输入：x = 0
输出：0
```

### 全部约束

- $-2^{31}\le x\le2^{31}-1$。
- 不允许使用 64 位有符号或无符号整数保存中间结果。

## 约束推导与溢出门禁

每轮可用 `digit = x % 10` 取出末位，再用 `answer = answer * 10 + digit` 追加。危险恰好发生在乘 10 和加末位之前。对正上界，只有 `answer > INT_MAX / 10`，或二者相等且 `digit > 7` 时会溢出；负下界同理，边界末位是 `-8`。C++ 的整数除法向零截断、余数与被除数同号，因此负数无需先取绝对值，也避开 `abs(INT_MIN)` 的未表示问题。

最多处理 10 位，时间和额外空间都是 $O(1)$。

## 解法递进

### 解法一：字符串反转并按边界字符串比较

把符号与数字分离、反转并去前导零，再与 `2147483647` 或 `2147483648` 按长度和字典序比较。它覆盖所有情况，但需要额外字符串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int reverse(int x) {
    string text = to_string(x);
    bool negative = text[0] == '-';
    string digits = negative ? text.substr(1) : text;
    std::reverse(digits.begin(), digits.end());
    size_t first = digits.find_first_not_of('0');
    digits = first == string::npos ? "0" : digits.substr(first);
    string limit = negative ? "2147483648" : "2147483647";
    if (digits.size() > limit.size() || (digits.size() == limit.size() && digits > limit)) {
      return 0;
    }
    int answer = 0;
    for (char digit : digits) {
      answer = answer * 10 - (digit - '0');
    }
    return negative ? answer : -answer;
  }
};
```

时间 $O(d)$，空间 $O(d)$，其中 $d\le10$。

### 最佳实用解：弹出末位，追加前先判界

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int reverse(int x) {
    int answer = 0;
    while (x != 0) {
      int digit = x % 10;
      x /= 10;
      if (answer > INT_MAX / 10 || (answer == INT_MAX / 10 && digit > 7)) {
        return 0;
      }
      if (answer < INT_MIN / 10 || (answer == INT_MIN / 10 && digit < -8)) {
        return 0;
      }
      answer = answer * 10 + digit;
    }
    return answer;
  }
};
```

时间 $O(d)$，额外空间 $O(1)$。它直接落实题目“不用 64 位整数”的契约，推荐优先记忆。

## 正确性证明

设进入一轮时，`answer` 是已经弹出的后缀数字按反序组成的整数，`x` 是尚未处理的前缀。`x % 10` 正好取得下一位，追加后不变量继续成立。判界条件完整刻画 `answer * 10 + digit` 是否越过 `INT_MAX` 或 `INT_MIN`；若越界，题目要求返回 0。否则运算安全。循环结束时所有数字恰好处理一次，`answer` 就是所求反转值。

## 样例手推、边界与易错点

`x=-123` 时依次取出 `-3,-2,-1`，答案演化为 `-3,-32,-321`。`120` 先取 0，数值前导零自然消失，最终为 21。`1534236469` 在追加最后几位前命中上界检查并返回 0。

- 不能先做 `abs(x)`，因为 `INT_MIN` 的绝对值无法由 `int` 表示。
- 必须在乘 10 之前判界，已经发生的有符号溢出不能事后修复。
- 正边界末位是 7，负边界末位是 -8，不能写成对称的 7。

## 变种一：任意进制下反转整数

新定义：给定 `int` 与 $2\le base\le36$，反转其 base 进制数字，越界返回 0。原不变量仍成立，只需把 10 改为 `base`，并用除法形式判界。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int value, base;
  cin >> value >> base;
  int answer = 0;
  while (value != 0) {
    int digit = value % base;
    value /= base;
    if (answer > 0 && answer > (INT_MAX - digit) / base) {
      cout << 0 << '\n';
      return 0;
    }
    if (answer < 0 && answer < (INT_MIN - digit) / base) {
      cout << 0 << '\n';
      return 0;
    }
    answer = answer * base + digit;
  }
  cout << answer << '\n';
}
```

时间 $O(\log_{base}|x|)$，空间 $O(1)$。

## 变种二：判断十进制整数是否回文

新定义：负数不是回文，只反转数字的一半。完整反转会带来不必要的溢出；比较前半与后半更稳健。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int value;
  cin >> value;
  if (value < 0 || (value % 10 == 0 && value != 0)) {
    cout << "false\n";
    return 0;
  }
  int reversedHalf = 0;
  while (value > reversedHalf) {
    reversedHalf = reversedHalf * 10 + value % 10;
    value /= 10;
  }
  cout << (value == reversedHalf || value == reversedHalf / 10 ? "true" : "false") << '\n';
}
```

时间 $O(d)$，空间 $O(1)$，且最多反转一半数字。

## 变种三：越界时饱和到边界

新定义：不返回 0，正溢出返回 `INT_MAX`，负溢出返回 `INT_MIN`。判界不变量保留，只改变终态。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int value;
  cin >> value;
  int answer = 0;
  while (value != 0) {
    int digit = value % 10;
    value /= 10;
    if (answer > INT_MAX / 10 || (answer == INT_MAX / 10 && digit > 7)) {
      cout << INT_MAX << '\n';
      return 0;
    }
    if (answer < INT_MIN / 10 || (answer == INT_MIN / 10 && digit < -8)) {
      cout << INT_MIN << '\n';
      return 0;
    }
    answer = answer * 10 + digit;
  }
  cout << answer << '\n';
}
```

时间 $O(d)$，空间 $O(1)$。

## 变种四：反转字符串中的每个十进制数字块

新定义：输入一行混合文本，把每个连续数字块原地反转，其他字符不动。整数算术不再适用，双指针扫描字符串即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string text;
  getline(cin, text);
  for (int left = 0; left < static_cast<int>(text.size());) {
    if (!isdigit(static_cast<unsigned char>(text[left]))) {
      ++left;
      continue;
    }
    int right = left;
    while (
        right < static_cast<int>(text.size()) && isdigit(static_cast<unsigned char>(text[right]))) {
      ++right;
    }
    reverse(text.begin() + left, text.begin() + right);
    left = right;
  }
  cout << text << '\n';
}
```

时间 $O(n)$，原地额外空间 $O(1)$。

## 可复现验证

所有代码块按 GNU++23 编译。最佳解覆盖 0、尾零、`INT_MAX`、`INT_MIN`、合法边界反转与正负溢出，并与基于字符串和任意精度整数的测试 oracle 做随机对拍。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/reverse-integer/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-95-lc977/">← [力扣 Top 95] LC 977 有序数组的平方 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-97-lc16/">[力扣 Top 97] LC 16 最接近的三数之和 中等 →</a>
</nav>
