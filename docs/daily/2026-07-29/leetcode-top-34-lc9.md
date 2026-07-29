---
title: "[力扣 Top 34] LC 9 回文数 简单"
---

# [力扣 Top 34] LC 9 回文数 简单

<p class="daily-archive-kicker">2026-07-29 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../basics/index.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：34
- 题号：LC 9
- 官方中文标题：回文数
- 官方难度：简单
- 官方链接：<https://leetcode.cn/problems/palindrome-number/>

### 原始题意

给定 32 位有符号整数 `x`，判断其十进制表示是否从左向右与从右向左完全相同。负号属于表示的一部分，因此负数不是回文数。进阶要求不把整数转成字符串。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool isPalindrome(int x);
};
```

### 全部官方样例

```text
输入：x = 121
输出：true
```

```text
输入：x = -121
输出：false
```

```text
输入：x = 10
输出：false
```

### 全部约束

- $-2^{31}\le x\le2^{31}-1$。

## 最优结论

只反转数字的后半部分，直到反转值不小于剩余前半部分：

- 偶数位回文满足 `front == reversedHalf`；
- 奇数位回文满足 `front == reversedHalf / 10`，中间位被除掉。

时间 $O(\log_{10}x)$，空间 $O(1)$，且不会发生完整反转的 32 位溢出。

## 约束与观察

- 负数直接为假。
- 除 0 外，以 0 结尾的数字不可能回文，因为其十进制首位不能为 0。
- 完整反转 `x` 可能溢出；反转一半时数值至多约为原数平方根数量级。

## 解法递进

### 解法一：字符串双指针

清晰但使用 $O(\log x)$ 额外空间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindrome(int x) {
    string value = to_string(x);
    int left = 0;
    int right = static_cast<int>(value.size()) - 1;
    while (left < right) {
      if (value[left++] != value[right--]) {
        return false;
      }
    }
    return true;
  }
};
```

### 解法二：完整数值反转

用 64 位承接反转结果可规避 32 位溢出，空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindrome(int x) {
    if (x < 0) {
      return false;
    }
    int original = x;
    long long reversed = 0;
    while (x > 0) {
      reversed = reversed * 10 + x % 10;
      x /= 10;
    }
    return reversed == original;
  }
};
```

### 解法三：只反转后半

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindrome(int x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) {
      return false;
    }
    int reversedHalf = 0;
    while (x > reversedHalf) {
      reversedHalf = reversedHalf * 10 + x % 10;
      x /= 10;
    }
    return x == reversedHalf || x == reversedHalf / 10;
  }
};
```

## 正确性证明

循环每次把 `x` 的最低位移到 `reversedHalf` 的末尾，因此执行 `t` 次后，`reversedHalf` 是原数最后 `t` 位的逆序，`x` 是删去这 `t` 位的前缀。

循环在后半位数不少于前半时停止。偶数总位数时两部分长度相同，回文当且仅当二者相等；奇数总位数时 `reversedHalf` 多含中间位，除以 10 后应与前半相等。前置条件排除了负数与非零尾随 0 的不可能情形，因此判断充要。

## 样例手推

`x=121`：

- 取出 1：`x=12`，`reversedHalf=1`；
- 取出 2：`x=1`，`reversedHalf=12`，停止；
- `1 == 12/10`，所以为回文。

## 易错点

- `0` 必须判真，不能被“末位为 0”规则误杀。
- 奇数位数要比较 `reversedHalf/10`。
- 不要对 `INT_MIN` 取绝对值；它在 32 位中溢出。
- 题意中的负号不能忽略。

## 验证说明

遍历大量 32 位边界值与随机整数，把半反转结果同 `to_string` 双指针 oracle 比较；覆盖 0、单位数、尾随 0、奇偶位数和负数。

## Follow-up 与变种

### 变种一：判断任意进制下是否回文

把十进制的 `%10`、`/10` 改为 `%base`、`/base`。要求 $2\le base\le36$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindromeInBase(long long x, int base) {
    if (x < 0 || base < 2) {
      return false;
    }
    vector<int> digits;
    do {
      digits.push_back(static_cast<int>(x % base));
      x /= base;
    } while (x > 0);
    return equal(digits.begin(), digits.begin() + digits.size() / 2, digits.rbegin());
  }
};
```

### 变种二：业务规则要求忽略负号

先转成 64 位再取绝对值，避免 `INT_MIN` 溢出；随后使用完整反转。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindromeIgnoringSign(int x) {
    long long value = llabs(static_cast<long long>(x));
    long long original = value;
    long long reversed = 0;
    do {
      reversed = reversed * 10 + value % 10;
      value /= 10;
    } while (value > 0);
    return reversed == original;
  }
};
```

### 变种三：删除至多一个十进制数字后能否回文

第一次不相等时，只需尝试跳过左端或右端一个字符。时间 $O(\log x)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool palindrome(const string& s, int left, int right) {
    while (left < right) {
      if (s[left++] != s[right--]) {
        return false;
      }
    }
    return true;
  }
public:
  bool validAfterDeletingOne(long long x) {
    if (x < 0) {
      return false;
    }
    string s = to_string(x);
    int left = 0;
    int right = static_cast<int>(s.size()) - 1;
    while (left < right && s[left] == s[right]) {
      ++left;
      --right;
    }
    return left >= right || palindrome(s, left + 1, right) || palindrome(s, left, right - 1);
  }
};
```

### 变种四：求严格大于给定非负整数的最小回文

先把左半镜像到右半；若结果不够大，就给中间向左的前缀加一后再次镜像。输入用字符串可支持超大整数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string mirror(string value) {
    for (int left = 0, right = static_cast<int>(value.size()) - 1; left < right; ++left, --right) {
      value[right] = value[left];
    }
    return value;
  }
public:
  string nextPalindrome(string value) {
    string candidate = mirror(value);
    if (candidate > value) {
      return candidate;
    }
    int index = (static_cast<int>(value.size()) - 1) / 2;
    while (index >= 0 && value[index] == '9') {
      value[index] = '0';
      --index;
    }
    if (index < 0) {
      return "1" + string(value.size() - 1, '0') + "1";
    }
    ++value[index];
    return mirror(value);
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/palindrome-number/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/palindrome-number/)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-33-lc27.md">← [力扣 Top 33] LC 27 移除元素 简单</a>
<a class="daily-archive-pager__next" href="leetcode-top-35-lc53.md">[力扣 Top 35] LC 53 最大子数组和 中等 →</a>
</nav>
