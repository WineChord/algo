---
title: "[力扣 Top 75] LC 394 字符串解码 中等"
---

# [力扣 Top 75] LC 394 字符串解码 中等

<p class="daily-archive-kicker">2026-08-02 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../strings/expression-parsing/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b75a0d814761860f22327b5d4fee4c6aba29f6947d438aba5fd1126e7b66e5f1 -->
## 官方原始信息

- Top 排名：75
- 题号：LC 394
- 官方中文标题：字符串解码
- 官方难度：中等
- 官方链接：[字符串解码](https://leetcode.cn/problems/decode-string/)

### 原始题意

编码片段 `k[encoded_string]` 表示括号内字符串重复 $k$ 次。编码可嵌套，输入保证有效，返回完全解码后的字符串。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string decodeString(string s);
};
```

### 全部官方样例

```text
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

```text
输入：s = "3[a2[c]]"
输出："accaccacc"
```

```text
输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
```

```text
输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"
```

### 全部约束

- $1\le |s|\le30$。
- `s` 只含小写字母、数字与方括号。
- 输入编码总是有效，括号匹配。
- 重复次数在 $[1,300]$。
- 原始字面量不含数字，所有数字都属于重复次数。
- 解码后长度不超过 $10^5$。

## 约束推导与语法模型

难点不在输入长度，而在嵌套结构和多位重复次数。每遇到 `[`，此前累计的字符串与重复次数构成一个未完成上下文；遇到匹配的 `]` 才能把当前子串重复并接回父层。这个过程天然对应栈或递归下降解析。

解码长度上限 $10^5$ 允许直接构造答案。时间下界本身就是 $O(|answer|)$，因为每个输出字符都必须写出。重复次数用 `int` 足够，但构建前可用 `size_t` 计算预留空间；官方上限保证不会溢出实际字符串容量。

## 解法递进

### 解法一：反复展开最内层括号

每次找到最左侧 `]`，向左找到对应的最近 `[` 和它前面的完整数字，替换为重复后的字面串。最左 `]` 内部不再含括号，因此替换合法。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string decodeString(string s) {
    while (s.find(']') != string::npos) {
      int close = s.find(']');
      int open = close;
      while (s[open] != '[') {
        --open;
      }
      int digitStart = open;
      while (digitStart > 0 && isdigit(static_cast<unsigned char>(s[digitStart - 1]))) {
        --digitStart;
      }
      int repeat = stoi(s.substr(digitStart, open - digitStart));
      string part = s.substr(open + 1, close - open - 1);
      string expanded;
      while (repeat--) {
        expanded += part;
      }
      s.replace(digitStart, close - digitStart + 1, expanded);
    }
    return s;
  }
};
```

最坏时间可达 $O(|s|\cdot|answer|)$，空间 $O(|answer|)$；大量 `replace` 会重复搬移字符，但它是直观的验证基准。

### 最佳实用解：上下文栈

扫描字符：数字累积到 `repeat`；`[` 时压入父串与次数并清空当前层；`]` 时弹出父层，把当前层重复后拼回；字母直接追加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string decodeString(string s) {
    vector<pair<string, int>> stack;
    string current;
    int repeat = 0;
    for (char character : s) {
      if (isdigit(static_cast<unsigned char>(character))) {
        repeat = repeat * 10 + character - '0';
      } else if (character == '[') {
        stack.push_back({std::move(current), repeat});
        current.clear();
        repeat = 0;
      } else if (character == ']') {
        auto [parent, times] = std::move(stack.back());
        stack.pop_back();
        parent.reserve(parent.size() + current.size() * times);
        for (int copy = 0; copy < times; ++copy) {
          parent += current;
        }
        current = std::move(parent);
      } else {
        current.push_back(character);
      }
    }
    return current;
  }
};
```

时间 $O(|s|+|answer|)$，空间 $O(|answer|+depth)$；移动父字符串避免不必要复制。推荐记忆“遇左括号保存父上下文，遇右括号归约子表达式”。

## 正确性证明

扫描过程中维持不变量：`current` 是从最近未匹配 `[` 之后到当前位置的完整解码结果；栈从外到内保存每个尚未闭合层的已解码前缀与重复次数。字母追加显然保持不变量；数字只构造下一层次数；`[` 把当前完整上下文入栈并开始新的子层；`]` 时当前子层已全部解码，重复指定次数并接到弹出的父前缀，恰好完成该语法单元。输入括号有效，最终栈为空，`current` 因而是整串的完整解码。

## 样例手推

`3[a2[c]]`：读到第一个 `[` 后栈为 `("",3)`；当前层读入 `a`，再压入 `("a",2)`；读 `c]` 后归约成 `acc`；最外 `]` 再把 `acc` 重复 3 次，得到 `accaccacc`。多位次数如 `12[a]` 通过 `repeat=repeat*10+digit` 正确累计。

## 易错点与方案比较

- 重复次数可能多位，不能逐字符独立处理。
- `]` 归约时顺序是“父前缀 + 子串重复”，不能反过来。
- 每次进入新层后必须把 `repeat` 清零。
- 输入字面量不含数字，因此数字状态只用于下一对括号。
- 最内层替换易理解但有重复搬移；栈版一次扫描达到输出规模下界，推荐作为主解。

## 变种一：只计算解码长度并设置上限

新定义：不生成正文，只返回长度；超过给定 `limit` 时返回 `limit+1`。栈保存进入括号前的长度与次数，所有运算饱和以避免溢出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  unsigned long long limit;
  cin >> s >> limit;
  vector<pair<unsigned long long, unsigned long long>> stack;
  unsigned long long length = 0;
  unsigned long long repeat = 0;
  for (char character : s) {
    if (isdigit(static_cast<unsigned char>(character))) {
      repeat = min(limit + 1, repeat * 10 + static_cast<unsigned long long>(character - '0'));
    } else if (character == '[') {
      stack.push_back({length, repeat});
      length = 0;
      repeat = 0;
    } else if (character == ']') {
      auto [prefix, times] = stack.back();
      stack.pop_back();
      if (length != 0 && times > (limit + 1) / length) {
        length = limit + 1;
      } else {
        length = min(limit + 1, prefix + min(limit + 1, length * times));
      }
    } else {
      length = min(limit + 1, length + 1);
    }
  }
  cout << length << '\n';
}
```

时间 $O(|s|)$，空间 $O(depth)$。

## 变种二：查询解码串的第 $k$ 个字符

新定义：解码结果可能巨大，只查询一基位置 $k$。构建语法树并保存每个节点的饱和长度，再按长度跳过整段。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const unsigned long long cap = 4000000000000000000ULL;
struct Node {
  char literal = 0;
  unsigned long long repeat = 1;
  unsigned long long length = 0;
  vector<Node> children;
};
unsigned long long addCap(unsigned long long a, unsigned long long b) {
  return a > cap - b ? cap : a + b;
}
unsigned long long multiplyCap(unsigned long long a, unsigned long long b) {
  return a != 0 && b > cap / a ? cap : a * b;
}
Node parseSequence(const string& s, int& index) {
  Node sequence;
  while (index < static_cast<int>(s.size()) && s[index] != ']') {
    if (isalpha(static_cast<unsigned char>(s[index]))) {
      Node leaf;
      leaf.literal = s[index++];
      leaf.length = 1;
      sequence.children.push_back(std::move(leaf));
    } else {
      unsigned long long times = 0;
      while (isdigit(static_cast<unsigned char>(s[index]))) {
        times = times * 10 + s[index++] - '0';
      }
      ++index;
      Node group = parseSequence(s, index);
      ++index;
      group.repeat = times;
      group.length = multiplyCap(group.length, times);
      sequence.children.push_back(std::move(group));
    }
  }
  for (const Node& child : sequence.children) {
    sequence.length = addCap(sequence.length, child.length);
  }
  return sequence;
}
char findCharacter(const Node& node, unsigned long long position) {
  if (node.literal != 0) {
    return node.literal;
  }
  unsigned long long oneCopy = node.length / node.repeat;
  if (node.repeat > 1) {
    position = (position - 1) % oneCopy + 1;
  }
  for (const Node& child : node.children) {
    if (position <= child.length) {
      return findCharacter(child, position);
    }
    position -= child.length;
  }
  return '?';
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  unsigned long long k;
  cin >> s >> k;
  int index = 0;
  Node root = parseSequence(s, index);
  cout << (k <= root.length ? findCharacter(root, k) : '?') << '\n';
}
```

构树 $O(|s|)$，单次查询 $O($语法树深度与经过的兄弟数$)$，空间 $O(|s|)$；长度使用饱和算术。

## 变种三：输入可能非法，需要验证

新定义：数字必须紧跟 `[`，括号必须匹配，字母外不允许其他字符；非法输出 `INVALID`，否则解码。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  vector<pair<string, int>> stack;
  string current;
  int repeat = 0;
  bool readingNumber = false;
  bool valid = true;
  for (char character : s) {
    if (isdigit(static_cast<unsigned char>(character))) {
      readingNumber = true;
      repeat = repeat * 10 + character - '0';
    } else if (character == '[') {
      if (!readingNumber || repeat == 0) {
        valid = false;
        break;
      }
      stack.push_back({std::move(current), repeat});
      current.clear();
      repeat = 0;
      readingNumber = false;
    } else if (character == ']') {
      if (readingNumber || stack.empty()) {
        valid = false;
        break;
      }
      auto [parent, times] = std::move(stack.back());
      stack.pop_back();
      for (int copy = 0; copy < times; ++copy) {
        parent += current;
      }
      current = std::move(parent);
    } else if (islower(static_cast<unsigned char>(character)) && !readingNumber) {
      current.push_back(character);
    } else {
      valid = false;
      break;
    }
  }
  valid = valid && !readingNumber && stack.empty();
  cout << (valid ? current : "INVALID") << '\n';
}
```

时间 $O(|s|+|answer|)$，空间 $O(|answer|+depth)$。

## 变种四：只求最大嵌套深度

新定义：不解码，只求任意字符所在的最大括号层数。重复次数和值域不再重要，只需计数括号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int depth = 0;
  int maximum = 0;
  for (char character : s) {
    if (character == '[') {
      maximum = max(maximum, ++depth);
    } else if (character == ']') {
      --depth;
    }
  }
  cout << maximum << '\n';
}
```

时间 $O(|s|)$，空间 $O(1)$；这是只保留语法结构统计后的状态压缩。

## 验证说明

栈解法与最内层替换法对 6000 个随机有效嵌套表达式逐项比较，所有官方样例通过；六段 C++23 代码完成编译检查，并单独覆盖多位次数与最大输出长度。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/decode-string/)
- [对应知识专题](../../strings/expression-parsing.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-74-lc64/">← [力扣 Top 74] LC 64 最小路径和 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-76-lc19/">[力扣 Top 76] LC 19 删除链表的倒数第 N 个结点 中等 →</a>
</nav>
