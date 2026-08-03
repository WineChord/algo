---
title: "[力扣 Top 100] LC 67 二进制求和 简单"
---

# [力扣 Top 100] LC 67 二进制求和 简单

<p class="daily-archive-kicker">2026-08-04 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=bfa2c45e8c72b208e30a8d4ebe85eb3e82eee9dddaa07be6936720ef10986555 -->
## 官方原始信息

- Top 排名：100
- 题号：LC 67
- 官方中文标题：二进制求和
- 官方难度：简单
- 官方链接：[二进制求和](https://leetcode.cn/problems/add-binary/)

### 原始题意

给定两个只含 `0`、`1` 的二进制字符串，以二进制字符串返回它们的和。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string addBinary(string a, string b);
};
```

### 全部官方样例

```text
输入：a = "11", b = "1"
输出："100"
```

```text
输入：a = "1010", b = "1011"
输出："10101"
```

### 全部约束

- $1\le a.length,b.length\le10^4$。
- 字符串只包含 `0` 或 `1`。
- 除字符串 `"0"` 外没有前导零。

## 约束推导与逐位进位

长度达 $10^4$，不能转换为内置整数。二进制某一列只依赖两输入位和上一列进位；从末位向前处理，`sum` 最大为 3，结果位是 `sum % 2`，新进位是 `sum / 2`。输出长度至多为 $\max(n,m)+1$，线性时间达到读写下界。

## 解法递进

### 解法一：每次把新结果位插到字符串开头

逻辑正确，但头插需要搬移现有字符，最坏退化为 $O(L^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string addBinary(string a, string b) {
    int i = a.size() - 1;
    int j = b.size() - 1;
    int carry = 0;
    string answer;
    while (i >= 0 || j >= 0 || carry != 0) {
      int sum = carry;
      if (i >= 0) {
        sum += a[i--] - '0';
      }
      if (j >= 0) {
        sum += b[j--] - '0';
      }
      answer.insert(answer.begin(), static_cast<char>('0' + sum % 2));
      carry = sum / 2;
    }
    return answer;
  }
};
```

### 最佳实用解：尾部追加后整体反转

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string addBinary(string a, string b) {
    int i = static_cast<int>(a.size()) - 1;
    int j = static_cast<int>(b.size()) - 1;
    int carry = 0;
    string answer;
    answer.reserve(max(a.size(), b.size()) + 1);
    while (i >= 0 || j >= 0 || carry != 0) {
      int sum = carry;
      if (i >= 0) {
        sum += a[i--] - '0';
      }
      if (j >= 0) {
        sum += b[j--] - '0';
      }
      answer.push_back(static_cast<char>('0' + sum % 2));
      carry = sum / 2;
    }
    reverse(answer.begin(), answer.end());
    return answer;
  }
};
```

时间 $O(n+m)$，输出外额外空间 $O(1)$。它不依赖大整数库，边界清晰，推荐优先记忆。

## 正确性证明

进入每轮时，`answer` 按低位到高位保存了已处理列的正确结果，`carry` 是这些列向当前列产生的唯一进位。当前两位与 `carry` 的和由二进制除法唯一分解为结果位 `sum mod 2` 和下一进位 `floor(sum/2)`，故不变量延续。所有输入位和最终进位处理完后，反转低位优先序列，得到标准高位优先的精确和。

## 样例手推、边界与易错点

`1010 + 1011` 从右到左：`0+1=1`；`1+1=10` 写 0 进 1；`0+0+1=1`；`1+1=10`；最后写进位 1，反转得到 `10101`。`0+0` 返回 `0`，不同长度和连续进位也由循环条件覆盖。

- 循环条件必须包含最终 `carry`。
- 索引用有符号整数，避免空减一后的无符号下溢。
- 不能对长度 $10^4$ 的输入调用 `stoi`、`stoll` 或位集固定宽度。
- 头插版本正确但有隐藏的平方复杂度。

## 变种一：三个二进制字符串求和

新定义：同时加三个二进制串。每列最大和为 5，进位仍可用整数除 2 传递。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  array<string, 3> values;
  cin >> values[0] >> values[1] >> values[2];
  array<int, 3> index;
  for (int k = 0; k < 3; ++k) {
    index[k] = static_cast<int>(values[k].size()) - 1;
  }
  int carry = 0;
  string answer;
  while (index[0] >= 0 || index[1] >= 0 || index[2] >= 0 || carry != 0) {
    int sum = carry;
    for (int k = 0; k < 3; ++k) {
      if (index[k] >= 0) {
        sum += values[k][index[k]--] - '0';
      }
    }
    answer.push_back(static_cast<char>('0' + sum % 2));
    carry = sum / 2;
  }
  reverse(answer.begin(), answer.end());
  cout << answer << '\n';
}
```

时间与输出长度线性，空间 $O(L)$。

## 变种二：不使用加号计算定宽无符号整数和

新定义：输入两个 32 位无符号整数；异或给无进位和，按位与左移给进位，迭代至进位为零。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  uint32_t first, second;
  cin >> first >> second;
  while (second != 0) {
    uint32_t carry = (first & second) << 1;
    first ^= second;
    second = carry;
  }
  cout << first << '\n';
}
```

最多传播 32 轮，时间 $O(w)$，空间 $O(1)$。定宽语义是模 $2^{32}$。

## 变种三：固定宽度二进制补码加法并报告溢出

新定义：两个长度相同的补码字符串相加，保留固定宽度，并报告有符号溢出。结果符号与两个同号输入不同即溢出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string first, second;
  cin >> first >> second;
  int carry = 0;
  string result(first.size(), '0');
  for (int i = static_cast<int>(first.size()) - 1; i >= 0; --i) {
    int sum = first[i] - '0' + second[i] - '0' + carry;
    result[i] = static_cast<char>('0' + sum % 2);
    carry = sum / 2;
  }
  bool overflow = first[0] == second[0] && result[0] != first[0];
  cout << result << '\n' << (overflow ? "overflow" : "ok") << '\n';
}
```

时间 $O(w)$，空间 $O(w)$；丢弃最高位进位符合补码定宽规则。

## 变种四：许多超长二进制数求和

新定义：给出 $k$ 个二进制串。逐列累加所有当前位后传播可能大于 1 的进位，避免重复两两相加。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int count;
  cin >> count;
  vector<string> values(count);
  int length = 0;
  for (string& value : values) {
    cin >> value;
    length = max(length, static_cast<int>(value.size()));
  }
  long long carry = 0;
  string answer;
  for (int offset = 0; offset < length || carry != 0; ++offset) {
    long long sum = carry;
    for (const string& value : values) {
      int index = static_cast<int>(value.size()) - 1 - offset;
      if (index >= 0) {
        sum += value[index] - '0';
      }
    }
    answer.push_back(static_cast<char>('0' + sum % 2));
    carry = sum / 2;
  }
  reverse(answer.begin(), answer.end());
  cout << (answer.empty() ? "0" : answer) << '\n';
}
```

时间 $O(kL)$，空间 $O(L)$；`carry` 应能容纳 $k$ 的量级。

## 可复现验证

全部代码块按 GNU++23 编译。最佳解与逐字符任意精度 oracle 在随机长度、全零、长度不等和最长连续进位上对拍。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/add-binary/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-99-lc707/">← [力扣 Top 99] LC 707 设计链表 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-513-q2-lc4011/">[力扣竞赛] 第 513 场周赛 Q2 LC 4011 按奇偶比统计子数组 I 中等 →</a>
</nav>
