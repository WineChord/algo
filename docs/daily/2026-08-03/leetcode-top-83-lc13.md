---
title: "[力扣 Top 83] LC 13 罗马数字转整数 简单"
---

# [力扣 Top 83] LC 13 罗马数字转整数 简单

<p class="daily-archive-kicker">2026-08-03 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b79d23143a2c3464f4ac375ac494e26e59b038b2e391700028078b034dbcd4d1 -->
## 官方原始信息

- Top 排名：83
- 题号：LC 13
- 官方中文标题：罗马数字转整数
- 官方难度：简单
- 官方链接：[罗马数字转整数](https://leetcode.cn/problems/roman-to-integer/)

### 原始题意

罗马数字使用 `I,V,X,L,C,D,M` 表示 1、5、10、50、100、500、1000，通常从大到小相加；六种减法组合 `IV,IX,XL,XC,CD,CM` 表示 4、9、40、90、400、900。给定一个有效罗马数字，返回对应整数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int romanToInt(string s);
};
```

### 全部官方样例

```text
输入：s = "III"
输出：3
```

```text
输入：s = "IV"
输出：4
```

```text
输入：s = "IX"
输出：9
```

```text
输入：s = "LVIII"
输出：58
解释：L=50，V=5，III=3。
```

```text
输入：s = "MCMXCIV"
输出：1994
解释：M=1000，CM=900，XC=90，IV=4。
```

### 全部约束

- $1\le s.length\le15$。
- `s` 只含 `I,V,X,L,C,D,M`。
- `s` 保证是 $[1,3999]$ 内整数的有效罗马数字表示。

## 约束推导与观察

长度很小，但核心是避免把六个减法组合写成容易遗漏的特判。有效罗马数字中，一个字符若小于右邻，便是减法项；否则是加法项。因此可统一写成

$$
value(s)=\sum_i sign_i\cdot value(s_i),\qquad sign_i=\begin{cases}-1,&v_i<v_{i+1},\\1,&\text{其他。}\end{cases}
$$

最后一个字符没有右邻，必为加法。答案至多 3999，`int` 足够。题目已保证输入规范，不需要在主解中检查 `IL`、`IIII` 等非法写法。

## 解法递进

### 解法一：显式识别六种双字符减法

从左到右优先读取合法二字符组合，否则读取单字符。它忠实复现规则，但需要维护组合表。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int romanToInt(string s) {
    unordered_map<string, int> pairValue{
        {"IV", 4}, {"IX", 9}, {"XL", 40}, {"XC", 90}, {"CD", 400}, {"CM", 900}};
    unordered_map<char, int> value{
        {'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}};
    int answer = 0;
    for (int i = 0; i < static_cast<int>(s.size());) {
      if (i + 1 < static_cast<int>(s.size()) && pairValue.count(s.substr(i, 2))) {
        answer += pairValue[s.substr(i, 2)];
        i += 2;
      } else {
        answer += value[s[i]];
        ++i;
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$（表大小固定）。

### 最佳实用解：与右邻比较决定正负号

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int value(char symbol) {
    if (symbol == 'I')
      return 1;
    if (symbol == 'V')
      return 5;
    if (symbol == 'X')
      return 10;
    if (symbol == 'L')
      return 50;
    if (symbol == 'C')
      return 100;
    if (symbol == 'D')
      return 500;
    return 1000;
  }
public:
  int romanToInt(string s) {
    int answer = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      int current = value(s[i]);
      int next = i + 1 < static_cast<int>(s.size()) ? value(s[i + 1]) : 0;
      answer += current < next ? -current : current;
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。它用一个局部不变量覆盖全部减法组合，是推荐记忆的方案。

## 正确性证明

有效罗马数字由普通加法符号与六种合法减法对构成。普通符号不小于右邻，算法将其值相加；减法对的左符号严格小于右符号，算法先减左值、后加右值，净贡献恰为右值减左值。每个字符属于且仅属于上述一种贡献，最后一个字符按加法处理。因此总和等于罗马数字表示的整数。

## 样例手推

`MCMXCIV` 的符号贡献依次为 $1000,-100,1000,-10,100,-1,5$，和为 1994。`LVIII` 中没有左小右大位置，贡献全部相加得到 $50+5+1+1+1=58$。单字符 `I` 的右邻值视为 0，答案为 1。

## 易错点与方案比较

- 比较的是相邻符号对应的数值，不是字符 ASCII 大小。
- 只有严格小于右邻才减，相等符号仍相加。
- 主问题保证输入有效；若接口不保证，局部正负规则会接受 `IL` 等非规范串，需额外校验。
- 显式组合表更贴近题面，右邻符号法更简洁、无漏组合风险；竞赛中优先使用后者。

## 变种一：整数转规范罗马数字

新定义：输入 $1..3999$ 的整数，输出唯一规范表示。按数值从大到小贪心取包括六个减法组合在内的符号块。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int number;
  cin >> number;
  vector<pair<int, string>> symbols{{1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"},
      {90, "XC"}, {50, "L"}, {40, "XL"}, {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};
  string answer;
  for (const auto& [value, symbol] : symbols) {
    while (number >= value) {
      number -= value;
      answer += symbol;
    }
  }
  cout << answer << '\n';
}
```

输出长度内时间 $O(1)$，空间 $O(1)$。

## 变种二：同时验证是否为规范罗马数字

新定义：输入不再保证有效。先按局部规则解析得到整数，再把整数重新编码；只有范围合法且重编码与原串逐字一致时才接受。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  unordered_map<char, int> value{
      {'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}};
  int number = 0;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (!value.count(s[i])) {
      cout << "INVALID\n";
      return 0;
    }
    number += i + 1 < static_cast<int>(s.size()) && value[s[i]] < value[s[i + 1]] ? -value[s[i]]
                                                                                  : value[s[i]];
  }
  vector<pair<int, string>> symbols{{1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"},
      {90, "XC"}, {50, "L"}, {40, "XL"}, {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};
  string canonical;
  int remaining = number;
  for (const auto& [amount, symbol] : symbols) {
    while (remaining >= amount) {
      remaining -= amount;
      canonical += symbol;
    }
  }
  cout << (1 <= number && number <= 3999 && canonical == s ? to_string(number) : "INVALID") << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。重编码把分散的语法限制统一为规范形比较。

## 变种三：批量解析大小写混合输入

新定义：有 $Q$ 个有效串，允许小写字母。逐字符转大写后应用同一右邻规则。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  unordered_map<char, int> value{
      {'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}};
  int queryCount;
  cin >> queryCount;
  while (queryCount--) {
    string s;
    cin >> s;
    for (char& symbol : s) {
      symbol = toupper(static_cast<unsigned char>(symbol));
    }
    int answer = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      int next = i + 1 < static_cast<int>(s.size()) ? value[s[i + 1]] : 0;
      answer += value[s[i]] < next ? -value[s[i]] : value[s[i]];
    }
    cout << answer << '\n';
  }
}
```

总时间与输入字符数线性，额外空间 $O(1)$。

## 变种四：自定义减法记数系统

新定义：输入 $K$ 个互异符号及其正权值，再给一个保证满足“较小符号位于较大符号之前即作减法”的有效串。映射从固定分支变为哈希表，局部符号法仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int symbolCount;
  cin >> symbolCount;
  unordered_map<char, long long> value;
  while (symbolCount--) {
    char symbol;
    long long weight;
    cin >> symbol >> weight;
    value[symbol] = weight;
  }
  string encoded;
  cin >> encoded;
  long long answer = 0;
  for (int i = 0; i < static_cast<int>(encoded.size()); ++i) {
    long long next = i + 1 < static_cast<int>(encoded.size()) ? value[encoded[i + 1]] : 0;
    answer += value[encoded[i]] < next ? -value[encoded[i]] : value[encoded[i]];
  }
  cout << answer << '\n';
}
```

时间 $O(K+n)$，空间 $O(K)$；若合法减法对不是由大小关系完全决定，就必须改回显式二字符语法表。

## 验证说明

本轮将六段代码按 C++23 编译；右邻法会与显式六组合解析在 1–3999 的全部规范罗马数字上对拍，并复核五个官方样例与所有减法边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/roman-to-integer/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-82-lc139/">← [力扣 Top 82] LC 139 单词拆分 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-84-lc135/">[力扣 Top 84] LC 135 分发糖果 困难 →</a>
</nav>
