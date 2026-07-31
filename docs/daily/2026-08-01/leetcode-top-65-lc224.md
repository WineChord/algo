---
title: "[力扣 Top 65] LC 224 基本计算器 困难"
---

# [力扣 Top 65] LC 224 基本计算器 困难

<p class="daily-archive-kicker">2026-08-01 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../strings/expression-parsing/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=535b37196b2947797147bfed603ce75c79512a75305fba449a397fe1f47f2763 -->
## 官方原始信息

- Top 排名：65
- 题号：LC 224
- 官方中文标题：基本计算器
- 官方难度：困难
- 官方链接：[基本计算器](https://leetcode.cn/problems/basic-calculator/)

### 原始题意

计算只含整数、空格、加号、减号和括号的合法表达式 `s`，不得调用把字符串直接当表达式求值的内置函数。加号不能作一元运算，一元减号合法。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int calculate(string s);
};
```

### 全部官方样例

```text
输入：s = "1 + 1"
输出：2
```

```text
输入：s = " 2-1 + 2 "
输出：3
```

```text
输入：s = "(1+(4+5+2)-3)+(6+8)"
输出：23
```

### 全部约束

- $1\le |s|\le3\times10^5$。
- `s` 只含数字、`+`、`-`、`(`、`)` 与空格，并保证表达式合法。
- `+` 不能作为一元运算，`-` 可以作为一元运算。
- 不存在两个连续运算符。
- 每个数字及所有中间计算结果都在有符号 32 位整数范围内。

## 约束推导与边界

$|s|$ 达到 $3\times10^5$，反复寻找匹配括号或生成子串会退化到 $O(n^2)$。运算只有同一优先级的加减，扫描时只需维护“当前括号层累计值、下一个数前的符号”。遇到左括号时保存外层累计值和括号前符号，右括号时把内层结果整体乘符号再接回外层。

一元减号出现在开头或左括号后时，前一个待结算数字自然为 0，因此同一状态机仍成立。虽然最终返回 `int`，实现可用 `long long` 累计，避免解析多位数时发生不必要的中间溢出。

## 解法递进

### 解法一：递归扫描并反复寻找匹配括号

每层从左到右解释区间；遇到左括号时向后扫描深度找到匹配右括号，再递归求值。嵌套括号会重复扫描相同字符，最坏为 $O(n^2)$，但逻辑可作为小规模基准。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long evaluate(const string& s, int left, int right) {
    long long result = 0;
    int sign = 1;
    for (int i = left; i < right;) {
      if (s[i] == ' ') {
        ++i;
      } else if (s[i] == '+') {
        sign = 1;
        ++i;
      } else if (s[i] == '-') {
        sign = -1;
        ++i;
      } else if (s[i] == '(') {
        int depth = 1;
        int close = i + 1;
        while (depth > 0) {
          depth += s[close] == '(';
          depth -= s[close] == ')';
          ++close;
        }
        result += sign * evaluate(s, i + 1, close - 1);
        sign = 1;
        i = close;
      } else {
        long long number = 0;
        while (i < right && isdigit(static_cast<unsigned char>(s[i]))) {
          number = number * 10 + s[i++] - '0';
        }
        result += sign * number;
        sign = 1;
      }
    }
    return result;
  }
public:
  int calculate(string s) {
    return evaluate(s, 0, s.size());
  }
};
```

最坏时间 $O(n^2)$，递归空间 $O(n)$。

### 最佳实用解：一次扫描的上下文栈

栈中成对保存进入括号前的外层结果与括号整体符号。数字结束、运算符、右括号和字符串末尾都是结算点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int calculate(string s) {
    long long result = 0;
    long long number = 0;
    int sign = 1;
    vector<long long> stack;
    for (char character : s) {
      if (isdigit(static_cast<unsigned char>(character))) {
        number = number * 10 + character - '0';
      } else if (character == '+' || character == '-') {
        result += sign * number;
        number = 0;
        sign = character == '+' ? 1 : -1;
      } else if (character == '(') {
        stack.push_back(result);
        stack.push_back(sign);
        result = 0;
        sign = 1;
      } else if (character == ')') {
        result += sign * number;
        number = 0;
        result *= stack.back();
        stack.pop_back();
        result += stack.back();
        stack.pop_back();
      }
    }
    return result + sign * number;
  }
};
```

时间 $O(n)$，空间 $O(d)$，其中 $d$ 为最大括号深度。

## 正确性证明

在任意括号层内，`result` 等于已经完整读完的项之和，`number` 是当前尚未结算的整数，`sign` 是它或下一个括号整体的符号。遇到加减号时结算当前数；遇到左括号时保存外层线性表达式状态并从零开始内层；遇到右括号时先完成内层最后一项，再按保存的符号与外层结果合并。

加减满足结合到有符号项之和的形式，括号合并又严格遵守嵌套顺序。因此该不变量逐字符保持。字符串结束时结算最后一个数，得到完整表达式值。

## 样例手推

对 `(1+(4+5+2)-3)+(6+8)`，首个左括号保存外层 `(0,+1)`；内层在第二个左括号前累计 1，第二层得到 11 后合并为 12，再减 3 得 9。退出首层后读第二个括号并得到 14，最终为 $9+14=23$。

表达式 `-1` 从 `result=0,sign=-1` 开始；`-(2+3)` 把符号 `-1` 与外层 0 入栈，内层 5 在右括号处乘为 -5，均无需特殊分支。

## 易错点与方案比较

- 右括号前要先结算括号内最后一个数字。
- 入栈顺序与出栈顺序必须配对；这里先存外层结果，再存符号。
- 空格应完全忽略，不能触发数字丢失。
- 题目没有乘除，因此不需要运算符优先级栈；加入乘除后必须换模型。
- 递归扫描更贴近语法，但朴素找括号会平方退化；一次扫描栈能稳定处理最长输入，推荐记忆。

## 变种一：无括号但加入乘除

乘除优先于加减。保留已经完成的低优先级总和 `result`，用 `term` 累积当前乘除链。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  getline(cin, s);
  long long result = 0;
  long long term = 0;
  long long number = 0;
  char operation = '+';
  for (int i = 0; i <= static_cast<int>(s.size()); ++i) {
    char character = i == static_cast<int>(s.size()) ? '+' : s[i];
    if (isdigit(static_cast<unsigned char>(character))) {
      number = number * 10 + character - '0';
    }
    if ((!isdigit(static_cast<unsigned char>(character)) && character != ' ') ||
        i == static_cast<int>(s.size())) {
      if (operation == '+') {
        result += term;
        term = number;
      } else if (operation == '-') {
        result += term;
        term = -number;
      } else if (operation == '*') {
        term *= number;
      } else {
        term /= number;
      }
      operation = character;
      number = 0;
    }
  }
  cout << result + term << '\n';
}
```

时间 $O(n)$，空间 $O(1)$；整数除法按 C++ 向零截断。

## 变种二：括号与四则运算同时存在

此时上下文栈不足以表达优先级。使用递归下降语法：表达式处理加减，项处理乘除，因子处理数字、括号和一元负号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Parser {
  string text;
  int index = 0;
  void skip() {
    while (index < static_cast<int>(text.size()) && text[index] == ' ') {
      ++index;
    }
  }
  long long factor() {
    skip();
    if (text[index] == '-') {
      ++index;
      return -factor();
    }
    if (text[index] == '(') {
      ++index;
      long long value = expression();
      skip();
      ++index;
      return value;
    }
    long long value = 0;
    while (index < static_cast<int>(text.size()) && isdigit(text[index])) {
      value = value * 10 + text[index++] - '0';
    }
    return value;
  }
  long long term() {
    long long value = factor();
    while (true) {
      skip();
      if (index == static_cast<int>(text.size()) || (text[index] != '*' && text[index] != '/')) {
        return value;
      }
      char operation = text[index++];
      long long right = factor();
      value = operation == '*' ? value * right : value / right;
    }
  }
  long long expression() {
    long long value = term();
    while (true) {
      skip();
      if (index == static_cast<int>(text.size()) || text[index] == ')') {
        return value;
      }
      char operation = text[index++];
      long long right = term();
      value = operation == '+' ? value + right : value - right;
    }
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  Parser parser;
  getline(cin, parser.text);
  cout << parser.expression() << '\n';
}
```

时间 $O(n)$，空间 $O(d)$。

## 变种三：超长整数且只需模意义结果

新定义：整数位数可以远超 64 位，另给 $1\le M\le 2\times 10^9$，输出表达式结果模 $M$ 的非负余数。原状态机仍成立；读数字时就逐位取模，所有合并也通过 `normalize` 归一化，因此不需要大整数库。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long modulus;
  cin >> modulus;
  cin.ignore(numeric_limits<streamsize>::max(), '\n');
  string s;
  getline(cin, s);
  auto normalize = [modulus](long long value) {
    value %= modulus;
    return value < 0 ? value + modulus : value;
  };
  long long result = 0;
  long long number = 0;
  int sign = 1;
  vector<pair<long long, int>> stack;
  for (char character : s) {
    if (isdigit(static_cast<unsigned char>(character))) {
      number = (number * 10 + character - '0') % modulus;
    } else if (character == '+' || character == '-') {
      result = normalize(result + sign * number);
      number = 0;
      sign = character == '+' ? 1 : -1;
    } else if (character == '(') {
      stack.push_back({result, sign});
      result = 0;
      sign = 1;
    } else if (character == ')') {
      result = normalize(result + sign * number);
      number = 0;
      auto [outside, outsideSign] = stack.back();
      stack.pop_back();
      result = normalize(outside + outsideSign * result);
    }
  }
  cout << normalize(result + sign * number) << '\n';
}
```

时间 $O(n)$，栈空间 $O(d)$；每个中间量始终位于 $[0,M)$，乘十也不会越过 64 位范围。

## 变种四：表达式可能非法并需报告首个错误位置

新定义：输入不再保证合法。递归下降在消费字符时检查缺少数字、括号不配对、非法一元加号和尾随字符，返回错误下标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Parser {
  string text;
  int index = 0;
  int error = -1;
  void skip() {
    while (index < static_cast<int>(text.size()) && text[index] == ' ') {
      ++index;
    }
  }
  optional<long long> expression(bool inside) {
    long long result = 0;
    int sign = 1;
    bool needValue = true;
    while (true) {
      skip();
      if (index == static_cast<int>(text.size()) || text[index] == ')') {
        if (needValue) {
          error = index;
          return nullopt;
        }
        if (inside && index == static_cast<int>(text.size())) {
          error = index;
          return nullopt;
        }
        return result;
      }
      if (!needValue) {
        if (text[index] != '+' && text[index] != '-') {
          error = index;
          return nullopt;
        }
        sign = text[index++] == '+' ? 1 : -1;
        needValue = true;
        continue;
      }
      if (text[index] == '+') {
        error = index;
        return nullopt;
      }
      if (text[index] == '-') {
        sign = -sign;
        ++index;
        skip();
      }
      long long value = 0;
      if (index < static_cast<int>(text.size()) && text[index] == '(') {
        ++index;
        auto nested = expression(true);
        if (!nested) {
          return nullopt;
        }
        value = *nested;
        ++index;
      } else if (index < static_cast<int>(text.size()) && isdigit(text[index])) {
        while (index < static_cast<int>(text.size()) && isdigit(text[index])) {
          value = value * 10 + text[index++] - '0';
        }
      } else {
        error = index;
        return nullopt;
      }
      result += sign * value;
      sign = 1;
      needValue = false;
    }
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  Parser parser;
  getline(cin, parser.text);
  auto value = parser.expression(false);
  parser.skip();
  if (!value || parser.index != static_cast<int>(parser.text.size())) {
    if (parser.error == -1) {
      parser.error = parser.index;
    }
    cout << "ERROR " << parser.error << '\n';
  } else {
    cout << *value << '\n';
  }
}
```

时间 $O(n)$，空间 $O(d)$。错误位置采用从 0 开始的字符下标。

## 可复现验证

随机生成深度不超过 8 的合法加减表达式，用独立递归语法树直接求值，与一次扫描栈比较；覆盖开头一元负号、括号前负号、多位数、全空格间隔和 300000 层级的非递归可承受模式。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/basic-calculator/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/basic-calculator/)
- [对应知识专题](../../strings/expression-parsing.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-64-lc48/">← [力扣 Top 64] LC 48 旋转图像 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-66-lc23/">[力扣 Top 66] LC 23 合并 K 个升序链表 困难 →</a>
</nav>
