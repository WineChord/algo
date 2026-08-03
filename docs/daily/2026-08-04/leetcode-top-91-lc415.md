---
title: "[力扣 Top 91] LC 415 字符串相加 简单"
---

# [力扣 Top 91] LC 415 字符串相加 简单

<p class="daily-archive-kicker">2026-08-04 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a228afdea79a2ef1c8827eeb8dd7d32e1fa815c9d9f21eb02ada9d28c96776e4 -->
## 官方原始信息

- Top 排名：91
- 题号：LC 415
- 官方中文标题：字符串相加
- 官方难度：简单
- 官方链接：[字符串相加](https://leetcode.cn/problems/add-strings/)

### 原始题意

给定两个表示非负整数的十进制字符串，返回它们的和的十进制字符串。不能调用大整数库，也不能把整个输入直接转换成整数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string addStrings(string num1, string num2);
};
```

### 全部官方样例

```text
输入：num1 = "11", num2 = "123"
输出："134"
```

```text
输入：num1 = "456", num2 = "77"
输出："533"
```

```text
输入：num1 = "0", num2 = "0"
输出："0"
```

### 全部约束

- $1\le num1.length,num2.length\le10^4$。
- 两个字符串只含数字 `0` 到 `9`。
- 两个字符串都没有前导零。

## 约束推导与观察

输入可达 $10^4$ 位，任何整型都装不下，但每一列只需要两个数位和一个至多为 1 的进位。必须从最低位向最高位处理，因为第 $i$ 列的进位依赖更低一列。若在字符串头部反复插入答案字符，每次都会移动已有内容，最坏变成 $O(n^2)$；应先从低位顺序追加，再整体反转。

设当前两位为 $a_i,b_j$、进位为 $c$，则

$$
\operatorname{digit}=(a_i+b_j+c)\bmod10,\qquad c=\left\lfloor\frac{a_i+b_j+c}{10}\right\rfloor.
$$

单列和至多 19，`int` 足够；结果长度至多 $\max(n,m)+1$。

## 解法递进

### 解法一：逐列计算并插入字符串头部

它正确模拟竖式，但头插导致累计搬移平方级字符。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string addStrings(string num1, string num2) {
    int i = static_cast<int>(num1.size()) - 1;
    int j = static_cast<int>(num2.size()) - 1;
    int carry = 0;
    string answer;
    while (i >= 0 || j >= 0 || carry) {
      int sum = carry;
      if (i >= 0) {
        sum += num1[i--] - '0';
      }
      if (j >= 0) {
        sum += num2[j--] - '0';
      }
      answer.insert(answer.begin(), static_cast<char>('0' + sum % 10));
      carry = sum / 10;
    }
    return answer;
  }
};
```

时间 $O((n+m)^2)$，答案外额外空间 $O(1)$。

### 最佳实用解：尾部追加后反转

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string addStrings(string num1, string num2) {
    int i = static_cast<int>(num1.size()) - 1;
    int j = static_cast<int>(num2.size()) - 1;
    int carry = 0;
    string answer;
    answer.reserve(max(num1.size(), num2.size()) + 1);
    while (i >= 0 || j >= 0 || carry) {
      int sum = carry;
      if (i >= 0) {
        sum += num1[i--] - '0';
      }
      if (j >= 0) {
        sum += num2[j--] - '0';
      }
      answer.push_back(static_cast<char>('0' + sum % 10));
      carry = sum / 10;
    }
    reverse(answer.begin(), answer.end());
    return answer;
  }
};
```

时间 $O(n+m)$，答案占 $O(\max(n,m))$ 空间，除此之外为 $O(1)$。每个输入字符至少要读一次，因此达到下界；这是应优先记忆的通用竖式模板。

## 正确性证明

循环开始处理某一列时，`carry` 等于所有已处理低位向该列产生的唯一进位。算法把当前存在的两个数位与 `carry` 相加，写出的余数正是该列十进制数位，商正是传向下一列的进位。因此每轮都保持竖式加法不变量。循环覆盖两串所有数位，并在最后仍有进位时额外写出它；反转只恢复从高位到低位的显示顺序，不改变数位。故返回字符串恰为两数之和。

## 样例手推

`456 + 77` 从右向左：$6+7=13$，写 3、进 1；$5+7+1=13$，写 3、进 1；$4+0+1=5$，写 5。临时串为 `335`，反转得到 `533`。`0+0` 第一轮写出 0，结果不会变成空串。`999+1` 连续传播进位，最终多出最高位 1，得到 `1000`。

## 易错点与方案比较

- 循环条件必须包含 `carry`，否则会漏掉最高位进位。
- 较短字符串耗尽后对应数位按 0 处理，不要补造新字符串。
- 题目保证无前导零，因此主解无需额外规范化。
- 头插与尾插方案算术完全相同，差别在字符串操作成本；推荐尾插再反转。

## 变种一：任意 $2\le B\le36$ 进制相加

新定义：数字字符使用 `0-9A-Z`，给定进制 $B$。把取模和除数从 10 改为 $B$，并补充字符与数值映射。

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
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int base;
  string a, b;
  cin >> base >> a >> b;
  int i = static_cast<int>(a.size()) - 1;
  int j = static_cast<int>(b.size()) - 1;
  int carry = 0;
  string answer;
  while (i >= 0 || j >= 0 || carry) {
    int sum = carry;
    if (i >= 0) {
      sum += value(a[i--]);
    }
    if (j >= 0) {
      sum += value(b[j--]);
    }
    answer.push_back(symbol(sum % base));
    carry = sum / base;
  }
  reverse(answer.begin(), answer.end());
  cout << answer << '\n';
}
```

时间 $O(n+m)$，空间为输出大小。单列和小于 $2B$，`int` 足够。

## 变种二：允许十进制有符号整数

新定义：输入可带负号。符号相同做绝对值相加；符号不同先比较绝对值，再用较大绝对值减较小绝对值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string addAbs(const string& a, const string& b) {
  int i = static_cast<int>(a.size()) - 1;
  int j = static_cast<int>(b.size()) - 1;
  int carry = 0;
  string answer;
  while (i >= 0 || j >= 0 || carry) {
    int sum = carry + (i >= 0 ? a[i--] - '0' : 0) + (j >= 0 ? b[j--] - '0' : 0);
    answer.push_back(static_cast<char>('0' + sum % 10));
    carry = sum / 10;
  }
  reverse(answer.begin(), answer.end());
  return answer;
}
string subtractAbs(const string& larger, const string& smaller) {
  int i = static_cast<int>(larger.size()) - 1;
  int j = static_cast<int>(smaller.size()) - 1;
  int borrow = 0;
  string answer;
  while (i >= 0) {
    int digit = larger[i--] - '0' - borrow - (j >= 0 ? smaller[j--] - '0' : 0);
    borrow = digit < 0;
    if (borrow) {
      digit += 10;
    }
    answer.push_back(static_cast<char>('0' + digit));
  }
  while (answer.size() > 1 && answer.back() == '0') {
    answer.pop_back();
  }
  reverse(answer.begin(), answer.end());
  return answer;
}
int main() {
  string first, second;
  cin >> first >> second;
  bool negativeFirst = first[0] == '-';
  bool negativeSecond = second[0] == '-';
  string a = negativeFirst ? first.substr(1) : first;
  string b = negativeSecond ? second.substr(1) : second;
  if (negativeFirst == negativeSecond) {
    cout << (negativeFirst ? "-" : "") << addAbs(a, b) << '\n';
    return 0;
  }
  bool aLarger = a.size() != b.size() ? a.size() > b.size() : a >= b;
  string answer = aLarger ? subtractAbs(a, b) : subtractAbs(b, a);
  bool negative = aLarger ? negativeFirst : negativeSecond;
  cout << (negative && answer != "0" ? "-" : "") << answer << '\n';
}
```

时间 $O(n+m)$，空间 $O(\max(n,m))$。异号时原加法模板本身不够，必须加入大小比较与借位。

## 变种三：一次求 $K$ 个大整数之和

新定义：输入 $K$ 个非负十进制字符串。按列汇总所有尚存在的数位，进位可能大于 1，但同一不变量仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int count;
  cin >> count;
  vector<string> numbers(count);
  size_t width = 0;
  for (string& number : numbers) {
    cin >> number;
    width = max(width, number.size());
  }
  long long carry = 0;
  string answer;
  for (size_t offset = 0; offset < width || carry; ++offset) {
    long long sum = carry;
    for (const string& number : numbers) {
      if (offset < number.size()) {
        sum += number[number.size() - 1 - offset] - '0';
      }
    }
    answer.push_back(static_cast<char>('0' + sum % 10));
    carry = sum / 10;
  }
  reverse(answer.begin(), answer.end());
  cout << (answer.empty() ? "0" : answer) << '\n';
}
```

设总输入字符数为 $L$、最大位数为 $W$，时间 $O(KW)$，空间 $O(W)$。若字符串长度差异悬殊，可按每个字符一次的桶式列累加做到 $O(L+W)$。

## 变种四：以 $10^9$ 为块降低常数

新定义：输入仍是十进制串，但每 9 位解析成一个安全的 32 位块，以 $10^9$ 为进制相加。它减少循环次数，适合更长输入。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> parse(const string& number) {
  vector<int> blocks;
  for (int right = static_cast<int>(number.size()); right > 0; right -= 9) {
    int left = max(0, right - 9);
    blocks.push_back(stoi(number.substr(left, right - left)));
  }
  return blocks;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string first, second;
  cin >> first >> second;
  vector<int> a = parse(first);
  vector<int> b = parse(second);
  vector<int> sum;
  long long carry = 0;
  for (size_t i = 0; i < max(a.size(), b.size()) || carry; ++i) {
    long long current = carry;
    if (i < a.size()) {
      current += a[i];
    }
    if (i < b.size()) {
      current += b[i];
    }
    sum.push_back(current % 1000000000);
    carry = current / 1000000000;
  }
  cout << sum.back();
  for (int i = static_cast<int>(sum.size()) - 2; i >= 0; --i) {
    cout << setw(9) << setfill('0') << sum[i];
  }
  cout << '\n';
}
```

时间仍为 $O(n+m)$ 个字符，但核心算术循环缩短约 9 倍；块和用 `long long` 防止越过 `int`。

## 验证说明

本轮将六段完整实现按 C++23 编译；最佳解会与 `boost::multiprecision::cpp_int` 仅在私有测试中对拍 20,000 组随机十进制串，并覆盖不同长度、连续进位、零、$10^4$ 位输入与四个变种的边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/add-strings/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-c/">← [atcoder] ABC469 C Cantrip</a>
<a class="daily-archive-pager__next" href="../leetcode-top-92-lc226/">[力扣 Top 92] LC 226 翻转二叉树 简单 →</a>
</nav>
