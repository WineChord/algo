---
title: "[力扣 Top 25] LC 2235 两整数相加 简单"
---

# [力扣 Top 25] LC 2235 两整数相加 简单

<p class="daily-archive-kicker">2026-07-28 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../basics/">进入知识专题</a></p>

## 官方原始信息

- 难度：LeetCode 官方「简单」；非竞赛题，无官方分值与 ZeroTracer 竞赛分。
- 官方链接：[打开官方页面](https://leetcode.cn/problems/add-two-integers/)
- slug：`add-two-integers`
- 函数签名：`int sum(int num1, int num2)`
- 题意：返回两个整数之和。
- 示例：`12 + 5 -> 17`；`-10 + 4 -> -6`。
- 约束：$-100\le num1,num2\le100$，故答案位于 $[-200,200]$。

## 约束、样例与边界

题目没有禁止 `+`，因此直接加法才是符合契约的最优实用解。负数、零、异号和端点都不会溢出 `int`。不要把常见面试追问“禁止使用加减法”擅自加回原题。

## 暴力：重复加一或减一

把 `num2` 的单位量逐个转移给 `num1`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int sum(int num1, int num2) {
    while (num2 > 0) {
      ++num1;
      --num2;
    }
    while (num2 < 0) {
      --num1;
      ++num2;
    }
    return num1;
  }
};
```

时间 $O(|num2|)$，空间 $O(1)$。在本题小范围内能通过，但人为展开了硬件已提供的加法。

## 最优：直接使用整数加法

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int sum(int num1, int num2) {
    return num1 + num2;
  }
};
```

由约束可知数学和一定在 `int` 范围内，因此 C++ 表达式与目标完全一致。时间 $O(1)$，空间 $O(1)$。样例 `-10+4` 可看作相反符号抵消六个单位，结果 `-6`。竞赛中优先记忆“先遵守真实契约”：不要为不存在的限制复杂化实现。

## Follow-up 1：禁止使用 `+` 和 `-`

异或给出不计进位的和，按位与后左移给出进位；迭代到进位为零。使用无符号数避免左移负数的未定义行为。对应 LC 371。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int getSum(int a, int b) {
    uint32_t x = static_cast<uint32_t>(a);
    uint32_t y = static_cast<uint32_t>(b);
    while (y) {
      uint32_t carry = (x & y) << 1;
      x ^= y;
      y = carry;
    }
    return bit_cast<int32_t>(x);
  }
};
```

时间 $O(w)$、空间 $O(1)$，其中 $w=32$。

## Follow-up 2：检测 32 位有符号溢出

先提升到 64 位计算，再与 `int` 边界比较。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
optional<int> checkedAdd(int a, int b) {
  long long value = 1LL * a + b;
  if (value < INT_MIN || value > INT_MAX) return nullopt;
  return static_cast<int>(value);
}
```

时间与空间均为 $O(1)$。原题约束保证不会走到空结果。

## Follow-up 3：任意长度非负十进制整数

机器整数不再容纳输入；从低位到高位维护进位，并在末尾反转结果。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string addDecimalStrings(const string& a, const string& b) {
  int i = (int)a.size() - 1;
  int j = (int)b.size() - 1;
  int carry = 0;
  string ans;
  while (i >= 0 || j >= 0 || carry) {
    int x = i >= 0 ? a[i--] - '0' : 0;
    int y = j >= 0 ? b[j--] - '0' : 0;
    int value = x + y + carry;
    ans.push_back(char('0' + value % 10));
    carry = value / 10;
  }
  reverse(ans.begin(), ans.end());
  return ans;
}
```

时间 $O(|a|+|b|)$，结果空间 $O(\max(|a|,|b|))$。

## Follow-up 4：无溢出地计算模加法

给定 $0\le a,b<mod<2^{64}$，直接 `a+b` 可能先溢出。比较 `a` 与 `mod-b`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
uint64_t addModulo(uint64_t a, uint64_t b, uint64_t mod) {
  if (mod == 0 || a >= mod || b >= mod) throw invalid_argument("invalid residue");
  return a >= mod - b ? a - (mod - b) : a + b;
}
```

时间与空间均为 $O(1)$。

## Follow-up 5：数字以逆序链表存储

每个节点是一位十进制数字；逐位相加并传递进位。对应 LC 2。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* addTwoNumbers(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    int carry = 0;
    while (a || b || carry) {
      int value = carry;
      if (a) {
        value += a->val;
        a = a->next;
      }
      if (b) {
        value += b->val;
        b = b->next;
      }
      tail->next = new ListNode(value % 10);
      tail = tail->next;
      carry = value / 10;
    }
    return dummy.next;
  }
};
```

时间 $O(m+n)$，新链表空间 $O(\max(m,n))$。

## 易错点与验证

- 原题允许 `+`；位运算只是约束变种。
- 检测溢出必须在提升类型后计算，不能先让 `int` 溢出。
- 位运算加法使用无符号中间量。
- 随机验证：穷举 `num1,num2∈[-100,100]`，比较重复单位转移、直接加法与位运算结果；额外测试 `INT_MIN/INT_MAX` 的 checked 版本。

## Reference

- [官方题目](https://leetcode.cn/problems/add-two-integers/)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-24-lc283/">← [力扣 Top 24] LC 283 移动零 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-26-lc239/">[力扣 Top 26] LC 239 滑动窗口最大值 困难 →</a>
</nav>
