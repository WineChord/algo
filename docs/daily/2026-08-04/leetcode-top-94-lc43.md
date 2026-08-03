---
title: "[力扣 Top 94] LC 43 字符串相乘 中等"
---

# [力扣 Top 94] LC 43 字符串相乘 中等

<p class="daily-archive-kicker">2026-08-04 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=94b48633f09cc3d633d69232c814aeca14ed3034bfb077038dba40dab9fd11f2 -->
## 官方原始信息

- Top 排名：94
- 题号：LC 43
- 官方中文标题：字符串相乘
- 官方难度：中等
- 官方链接：[字符串相乘](https://leetcode.cn/problems/multiply-strings/)

### 原始题意

给定两个表示非负整数的十进制字符串，返回乘积的十进制字符串。不能调用大整数库，也不能把整个输入直接转换成整数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string multiply(string num1, string num2);
};
```

### 全部官方样例

```text
输入：num1 = "2", num2 = "3"
输出："6"
```

```text
输入：num1 = "123", num2 = "456"
输出："56088"
```

### 全部约束

- $1\le num1.length,num2.length\le200$。
- 两个字符串只含十进制数字。
- 除数字 `0` 本身外，输入没有前导零。

## 约束推导与位权结构

200 位已经远超内置整数。若长度分别为 $n,m$，乘积最多有 $n+m$ 位。十进制竖式中，`num1[i] * num2[j]` 的个位应累加到结果从右数第

$$
(n-1-i)+(m-1-j)
$$

列。直接保存长度 $n+m$ 的数位数组，就能让所有 $nm$ 个数位乘积只写入确定位置，再统一处理进位。单个格子累加最多约 $200\times81=16200$，`int` 足够；实现仍可边乘边向高位进位，避免最后一次大扫描。

若任一输入为 `0`，必须直接返回 `0`，否则去掉高位零后可能得到空串。

## 解法递进

### 解法一：生成每个部分积，再用字符串加法累加

对乘数每个数位生成一行部分积并补相应个数的尾零，再逐行相加。它忠实模拟纸笔竖式，但重复构造和相加使最坏时间增至 $O(m(n+m))$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string add(string first, string second) {
    int i = static_cast<int>(first.size()) - 1;
    int j = static_cast<int>(second.size()) - 1;
    int carry = 0;
    string answer;
    while (i >= 0 || j >= 0 || carry) {
      int sum = carry + (i >= 0 ? first[i--] - '0' : 0) + (j >= 0 ? second[j--] - '0' : 0);
      answer.push_back(static_cast<char>('0' + sum % 10));
      carry = sum / 10;
    }
    reverse(answer.begin(), answer.end());
    return answer;
  }
public:
  string multiply(string num1, string num2) {
    if (num1 == "0" || num2 == "0") {
      return "0";
    }
    string answer = "0";
    for (int j = static_cast<int>(num2.size()) - 1, zeros = 0; j >= 0; --j, ++zeros) {
      int carry = 0;
      string part(zeros, '0');
      for (int i = static_cast<int>(num1.size()) - 1; i >= 0; --i) {
        int product = (num1[i] - '0') * (num2[j] - '0') + carry;
        part.push_back(static_cast<char>('0' + product % 10));
        carry = product / 10;
      }
      if (carry) {
        part.push_back(static_cast<char>('0' + carry));
      }
      reverse(part.begin(), part.end());
      answer = add(answer, part);
    }
    return answer;
  }
};
```

时间 $O(m(n+m))$，空间 $O(n+m)$。

### 最佳实用解：固定结果槽位统一累加

使用高位在前的长度 $n+m$ 数组。乘积写入 `i+j+1`，立即把十位进到 `i+j`；后续累加仍会沿相同规则传播。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string multiply(string num1, string num2) {
    if (num1 == "0" || num2 == "0") {
      return "0";
    }
    int n = num1.size();
    int m = num2.size();
    vector<int> digits(n + m);
    for (int i = n - 1; i >= 0; --i) {
      for (int j = m - 1; j >= 0; --j) {
        int sum = digits[i + j + 1] + (num1[i] - '0') * (num2[j] - '0');
        digits[i + j + 1] = sum % 10;
        digits[i + j] += sum / 10;
      }
    }
    string answer;
    int first = digits[0] == 0;
    for (int i = first; i < n + m; ++i) {
      answer.push_back(static_cast<char>('0' + digits[i]));
    }
    return answer;
  }
};
```

时间 $O(nm)$，空间 $O(n+m)$。在普通竖式模型下每对数位都可能影响答案，这一复杂度是最佳实用基线；更长输入才值得考虑 Karatsuba 或 FFT。

## 正确性证明

对任意下标 $i,j$，两数位的乘积乘以位权 $10^{(n-1-i)+(m-1-j)}$，代码把其个位写入结果下标 `i+j+1`，把十位传到更高一位 `i+j`，与该位权完全一致。内层循环结束后，每一对输入数位的乘积都被恰好累加一次；每次取模和整除只做等值的十进制进位，不改变总数值。长度 $n+m$ 足以容纳最大乘积，去掉唯一可能的最高前导零后得到规范十进制表示。因此算法返回的字符串恰为乘积。

## 样例手推

`123 * 456` 的部分积是 $123\times6=738$、$123\times50=6150$、$123\times400=49200$，和为 56088。槽位法把同一位权的贡献直接相加：例如 $3\times6$ 写入最低位，$2\times6$ 与 $3\times5$ 都影响下一位。`2*3` 只使用两个槽位，最高槽为 0，删除后得到 `6`。

## 易错点与方案比较

- 结果槽位是 `i+j+1`，其进位进入 `i+j`，容易出现一位偏移。
- 必须先特判零；其他输入无前导零，所以最多只跳过 `digits[0]`。
- 不要把 200 位字符串交给 `stoll`，即使只为“方便”。
- 部分积方案便于教学和作为 oracle；固定槽位方案少了重复字符串相加，是竞赛应提交的实现。

## 变种一：允许正负号

新定义：输入可带 `+` 或 `-`。先剥离符号并复用非负乘法，乘积非零且两符号不同时补负号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string multiplyAbs(const string& a, const string& b) {
  if (a == "0" || b == "0") {
    return "0";
  }
  vector<int> digits(a.size() + b.size());
  for (int i = static_cast<int>(a.size()) - 1; i >= 0; --i) {
    for (int j = static_cast<int>(b.size()) - 1; j >= 0; --j) {
      int sum = digits[i + j + 1] + (a[i] - '0') * (b[j] - '0');
      digits[i + j + 1] = sum % 10;
      digits[i + j] += sum / 10;
    }
  }
  string answer;
  for (int digit : digits) {
    if (!answer.empty() || digit != 0) {
      answer.push_back(static_cast<char>('0' + digit));
    }
  }
  return answer;
}
int main() {
  string first, second;
  cin >> first >> second;
  bool negativeFirst = first[0] == '-';
  bool negativeSecond = second[0] == '-';
  if (first[0] == '-' || first[0] == '+') {
    first.erase(first.begin());
  }
  if (second[0] == '-' || second[0] == '+') {
    second.erase(second.begin());
  }
  string answer = multiplyAbs(first, second);
  cout << ((negativeFirst != negativeSecond) && answer != "0" ? "-" : "") << answer << '\n';
}
```

时间 $O(nm)$，空间 $O(n+m)$。符号只影响最终表示，不进入数位卷积。

## 变种二：任意 $2\le B\le36$ 进制相乘

新定义：使用 `0-9A-Z`。槽位进位的模数从 10 改为 $B$，字符映射随之改变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int value(char symbol) {
  return isdigit(static_cast<unsigned char>(symbol)) ? symbol - '0' : symbol - 'A' + 10;
}
char symbol(int digit) {
  return digit < 10 ? static_cast<char>('0' + digit) : static_cast<char>('A' + digit - 10);
}
int main() {
  int base;
  string a, b;
  cin >> base >> a >> b;
  if (a == "0" || b == "0") {
    cout << "0\n";
    return 0;
  }
  vector<int> digits(a.size() + b.size());
  for (int i = static_cast<int>(a.size()) - 1; i >= 0; --i) {
    for (int j = static_cast<int>(b.size()) - 1; j >= 0; --j) {
      int sum = digits[i + j + 1] + value(a[i]) * value(b[j]);
      digits[i + j + 1] = sum % base;
      digits[i + j] += sum / base;
    }
  }
  bool started = false;
  for (int digit : digits) {
    if (digit || started) {
      cout << symbol(digit);
      started = true;
    }
  }
  cout << '\n';
}
```

时间 $O(nm)$，空间 $O(n+m)$。$B\le36$ 时单次乘积与槽位和仍安全落在 `int`。

## 变种三：只求乘积对 $M$ 的余数

新定义：不需要完整乘积，只返回 $(num1\times num2)\bmod M$。先逐字符求每个大整数的余数，再用 `__int128` 安全相乘。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long remainder(const string& number, long long modulus) {
  long long value = 0;
  for (char digit : number) {
    value = (static_cast<__int128>(value) * 10 + digit - '0') % modulus;
  }
  return value;
}
int main() {
  string first, second;
  long long modulus;
  cin >> first >> second >> modulus;
  long long a = remainder(first, modulus);
  long long b = remainder(second, modulus);
  cout << static_cast<long long>(static_cast<__int128>(a) * b % modulus) << '\n';
}
```

时间 $O(n+m)$，空间 $O(1)$。只求模时构造 $O(nm)$ 位乘积是无谓工作。

## 变种四：计算多个大整数的乘积

新定义：输入 $K$ 个非负十进制串。每次优先合并当前最短的两个结果，减少长中间串参与乘法的次数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string multiply(const string& a, const string& b) {
  if (a == "0" || b == "0") {
    return "0";
  }
  vector<int> digits(a.size() + b.size());
  for (int i = static_cast<int>(a.size()) - 1; i >= 0; --i) {
    for (int j = static_cast<int>(b.size()) - 1; j >= 0; --j) {
      int sum = digits[i + j + 1] + (a[i] - '0') * (b[j] - '0');
      digits[i + j + 1] = sum % 10;
      digits[i + j] += sum / 10;
    }
  }
  string answer;
  for (int digit : digits) {
    if (!answer.empty() || digit) {
      answer.push_back(static_cast<char>('0' + digit));
    }
  }
  return answer;
}
int main() {
  int count;
  cin >> count;
  auto compare = [](const string& first, const string& second) {
    return first.size() > second.size();
  };
  priority_queue<string, vector<string>, decltype(compare)> numbers(compare);
  while (count--) {
    string number;
    cin >> number;
    numbers.push(number);
  }
  while (numbers.size() > 1) {
    string first = numbers.top();
    numbers.pop();
    string second = numbers.top();
    numbers.pop();
    numbers.push(multiply(first, second));
  }
  cout << numbers.top() << '\n';
}
```

复杂度取决于中间结果长度；短串优先是竖式乘法下的实用启发式。若总位数极大，应改用分治乘法或 FFT，而不是继续堆叠 $O(nm)$。

## 验证说明

本轮将六段完整实现按 C++23 编译；槽位解会与 `boost::multiprecision::cpp_int` 在 15,000 组随机数字串上对拍，并覆盖零、单数位、连续进位、200 位极值及所有官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/multiply-strings/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-93-lc104/">← [力扣 Top 93] LC 104 二叉树的最大深度 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-95-lc977/">[力扣 Top 95] LC 977 有序数组的平方 简单 →</a>
</nav>
