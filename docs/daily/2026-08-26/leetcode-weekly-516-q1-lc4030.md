---
title: "[力扣竞赛] 第 516 场周赛 Q1 LC 4030 判断 ASCII 值回文 简单"
---

# [力扣竞赛] 第 516 场周赛 Q1 LC 4030 判断 ASCII 值回文 简单

<p class="daily-archive-kicker">2026-08-26 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-26 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d9d18020838529933625e132b55443653be75d2eae95aec169dd62b8d596e487 -->
## 官方原始信息

- 来源：力扣第 516 场周赛 Q1
- 题号：LC 4030
- 官方中文标题：判断 ASCII 值回文
- 官方难度：简单
- 官方比赛分值：3 分
- ZeroTracer 社区估算竞赛分：未知（公开数据于 2026-08-26 未收录该题）
- 官方链接：[4030. 判断 ASCII 值回文](https://leetcode.cn/problems/check-ascii-palindromic/)
- 函数签名：`bool isPalindromic(string s)`

### 原始题意

给定只含小写英文字母的字符串 `s`。把每个字符替换为其 ASCII 值的 8 位二进制表示，前导零必须保留，并按原字符顺序拼接成一个二进制字符串。若这个二进制字符串是回文串，返回 `true`；否则返回 `false`。

### 全部官方样例

样例 1：

```text
输入：s = "ff"
输出：true
```

字符 `f` 的 ASCII 值为 102，8 位表示为 `01100110`。拼接结果是 `0110011001100110`，正反相同。

样例 2：

```text
输入：s = "leet"
输出：false
```

`l`、`e`、`e`、`t` 的 ASCII 值依次为 108、101、101、116，对应 `01101100`、`01100101`、`01100101`、`01110100`。拼接后的二进制串不是回文。

### 全部约束

- $1\le |s|\le 100$
- `s` 仅由小写英文字母组成。

## 最优结论摘要

不必真的构造长度为 $8|s|$ 的二进制串。整段字节串反转时，字符顺序会反转，每个字符内部的 8 个比特也会反转。因此答案为真当且仅当对所有 $i$ 都有：

$$
\operatorname{ASCII}(s_i)=\operatorname{rev}_8(\operatorname{ASCII}(s_{n-1-i})).
$$

逐对检查即可，时间复杂度为 $O(n)$，额外空间复杂度为 $O(1)$。推荐记忆这一“定长块整体反转 = 块顺序反转 + 每块内部反转”的结构等价。

## 约束推导、位序与边界

每个字符固定贡献 8 位，因此总位数只有 $8n\le 800$。直接构造已经足够快，但题目更值得提炼的是固定宽度分块的反转规律。

ASCII 的 8 位表示按最高位到最低位书写。若字符值为 $x$，它的 8 位反转为：

$$
\operatorname{rev}_8(x)=\sum_{b=0}^{7}\left((x\mathbin{\gg}b)\mathbin{\&}1\right)2^{7-b}.
$$

需要注意：

- 前导零属于二进制串的一部分，不能把字符值转成无前导零的普通二进制文本。
- 字符串长度可以为 1；此时该字符自身的 8 位表示也必须是回文。
- 使用位运算时把字符转成 `unsigned char`，可避免在更一般的字节输入中受 `char` 有符号性影响。
- 小写字符范围为 97–122，8 位无符号整数完全足够。

## 官方样例手推

对 `ff`，单个字节是：

$$
102=(01100110)_2,
$$

它自身反转后仍为 `01100110`。两个相同字节交换顺序也不改变结果，所以整体是回文。

对 `leet`，首字符 `l` 的字节是 `01101100`；末字符 `t` 的字节反转为 `00101110`，两者已经不同，立即返回 `false`。

## 解法一：显式构造二进制字符串

依次枚举每个字符的第 7 位到第 0 位，把对应的 `0` 或 `1` 追加到字符串；最后用双指针检查回文。这是最直接、最容易作为暴力基准的实现。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindromic(string s) {
    string bits;
    bits.reserve(s.size() * 8);
    for (unsigned char c : s) {
      for (int b = 7; b >= 0; --b) {
        bits.push_back('0' + ((c >> b) & 1));
      }
    }
    for (int l = 0, r = static_cast<int>(bits.size()) - 1; l < r; ++l, --r) {
      if (bits[l] != bits[r]) return false;
    }
    return true;
  }
};
```

时间复杂度为 $O(8n)=O(n)$，额外空间复杂度为 $O(8n)=O(n)$。它的不足不是速度，而是保存了其实可以随用随算的中间串。

## 解法二：直接比较两端比特

把虚拟二进制串的位置 $p$ 映射到字符下标 $p/8$ 和该字符中的位序 $7-p\bmod 8$，即可用双指针比较而不构造字符串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isPalindromic(string s) {
    int m = static_cast<int>(s.size()) * 8;
    auto bit = [&](int p) {
      unsigned char c = static_cast<unsigned char>(s[p / 8]);
      return (c >> (7 - p % 8)) & 1;
    };
    for (int l = 0, r = m - 1; l < r; ++l, --r) {
      if (bit(l) != bit(r)) return false;
    }
    return true;
  }
};
```

时间复杂度仍为 $O(n)$，额外空间降为 $O(1)$。下一步还能把 8 次逐位比较合并成一次字节比较。

## 最佳实用解：比较字节与 8 位反转

### 算法

1. 写一个固定执行 8 次的 `reverseByte`，把字节的最低位依次移入答案。
2. 对称枚举字符下标 $i$ 与 $n-1-i$。
3. 若左字节不等于右字节的 8 位反转，返回 `false`；全部相等则返回 `true`。

### 正确性证明

把每个字符的 8 位块记作 $B_i$，原二进制串为：

$$
B_0B_1\cdots B_{n-1}.
$$

整个字符串反转后，块的顺序反转，并且每个块内部也反转，所以得到：

$$
\operatorname{rev}(B_{n-1})\operatorname{rev}(B_{n-2})\cdots\operatorname{rev}(B_0).
$$

两个定长分块串相等，当且仅当每个对应块相等。因此原串是回文，当且仅当对每个 $i$ 都有 $B_i=\operatorname{rev}(B_{n-1-i})$。算法逐项检查的正是这个充要条件，故返回值正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  unsigned char reverseByte(unsigned char x) {
    unsigned char y = 0;
    for (int b = 0; b < 8; ++b) {
      y = static_cast<unsigned char>((y << 1) | (x & 1));
      x >>= 1;
    }
    return y;
  }
public:
  bool isPalindromic(string s) {
    int n = static_cast<int>(s.size());
    for (int i = 0; i <= n - 1 - i; ++i) {
      unsigned char left = static_cast<unsigned char>(s[i]);
      unsigned char right = static_cast<unsigned char>(s[n - 1 - i]);
      if (left != reverseByte(right)) return false;
    }
    return true;
  }
};
```

时间复杂度为 $O(n)$，额外空间复杂度为 $O(1)$。`reverseByte` 的 8 次循环是固定常数。

## 同阶方案比较与易错点

- 显式构造：最贴近题意，适合作为基准和面试开场；空间为 $O(n)$。
- 虚拟位双指针：不分配中间串，但每次要做位置映射。
- 字节反转比较：直接揭示结构，空间最小，证明也最清楚，推荐竞赛与面试优先记忆。

常见错误：

- 使用 `bitset<8>(c).to_string()` 以外的普通进制转换，却忘记补足前导零。
- 只检查原字符序列是不是回文；字符相同不代表其 8 位模式一定满足整体条件。
- 只反转字符顺序，却没有反转每个字符内部的位序。
- 中间字符没有自反转时仍返回真。
- 写成依赖平台字节序的内存读取；题目要求的是数值的标准 8 位二进制书写，与机器端序无关。

## 可复现验证

本轮对全部 C++ 代码执行 C++23 编译。最佳解会与显式构造法做穷举和随机对拍：覆盖长度 1、奇偶长度、自反转字节、首尾立即失败以及多对字符共同满足的情况。

## Follow-up 与约束变种

### 变种一：返回第一对不匹配的位位置

**新定义**：若展开后的二进制串不是回文，返回第一对不匹配的零基位下标；若是回文，返回 `{-1,-1}`。

字节级判断只给布尔结论，不能直接恢复具体位。改用虚拟位访问器，从两端逐位比较；时间 $O(n)$、空间 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, int> firstMismatch(const string &s) {
  int m = static_cast<int>(s.size()) * 8;
  auto bit = [&](int p) {
    unsigned char c = static_cast<unsigned char>(s[p / 8]);
    return (c >> (7 - p % 8)) & 1;
  };
  for (int l = 0, r = m - 1; l < r; ++l, --r) {
    if (bit(l) != bit(r)) return {l, r};
  }
  return {-1, -1};
}
int main() {
  string s;
  cin >> s;
  auto [l, r] = firstMismatch(s);
  cout << l << ' ' << r << '\n';
}
```

### 变种二：元素改为固定 $b$ 位整数

**新定义**：给出整数数组 `a` 和统一位宽 $b$，每个元素按恰好 $b$ 位、保留前导零拼接，判断整体是否回文。保证 $1\le b\le 32$ 且 $0\le a_i<2^b$。

原来的分块结论仍成立，只需把 8 位反转推广为 $b$ 位反转。时间复杂度为 $O(nb)$，额外空间为 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
uint32_t reverseBits(uint32_t x, int b) {
  uint32_t y = 0;
  for (int i = 0; i < b; ++i) {
    y = (y << 1) | (x & 1U);
    x >>= 1;
  }
  return y;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, b;
  cin >> n >> b;
  vector<uint32_t> a(n);
  for (uint32_t &x : a) cin >> x;
  for (int i = 0; i <= n - 1 - i; ++i) {
    if (a[i] != reverseBits(a[n - 1 - i], b)) {
      cout << "false\n";
      return 0;
    }
  }
  cout << "true\n";
}
```

### 变种三：在线修改字符并询问整个串

**新定义**：字符串长度固定，支持把位置 $p$ 改成新字符，以及询问当前 8 位展开串是否回文。

维护不匹配对数量 `bad`。一次修改只可能改变包含 $p$ 的那一对对称字符；修改前移除旧贡献，修改后加入新贡献。更新和询问均为 $O(1)$，初始化为 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
unsigned char reverseByte(unsigned char x) {
  unsigned char y = 0;
  for (int i = 0; i < 8; ++i) {
    y = static_cast<unsigned char>((y << 1) | (x & 1));
    x >>= 1;
  }
  return y;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int q;
  cin >> s >> q;
  int n = static_cast<int>(s.size()), bad = 0;
  auto mismatch = [&](int i) {
    int j = n - 1 - i;
    unsigned char x = static_cast<unsigned char>(s[i]);
    unsigned char y = static_cast<unsigned char>(s[j]);
    return x != reverseByte(y);
  };
  for (int i = 0; i <= n - 1 - i; ++i) bad += mismatch(i);
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int p;
      char c;
      cin >> p >> c;
      --p;
      int i = min(p, n - 1 - p);
      bad -= mismatch(i);
      s[p] = c;
      bad += mismatch(i);
    } else {
      cout << (bad == 0 ? "true" : "false") << '\n';
    }
  }
}
```

### 变种四：最少替换多少个小写字母才能满足条件

**新定义**：每次可把一个位置替换为任意小写英文字母，求使 8 位展开串成为回文所需的最少替换次数；无解时返回 `-1`。

对每对对称位置独立处理。枚举左右最终字符 $x,y\in[a,z]$ 且要求 $x=\operatorname{rev}_8(y)$，代价是两端各自是否改变；取最小值。中点则枚举满足 $x=\operatorname{rev}_8(x)$ 的小写字符。每对只检查 $26^2$ 种，时间为 $O(26^2n)$，空间为 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
unsigned char reverseByte(unsigned char x) {
  unsigned char y = 0;
  for (int i = 0; i < 8; ++i) {
    y = static_cast<unsigned char>((y << 1) | (x & 1));
    x >>= 1;
  }
  return y;
}
int main() {
  string s;
  cin >> s;
  int n = static_cast<int>(s.size()), ans = 0;
  for (int l = 0, r = n - 1; l <= r; ++l, --r) {
    int best = 3;
    for (int x = 'a'; x <= 'z'; ++x) {
      for (int y = 'a'; y <= 'z'; ++y) {
        if (x != reverseByte(static_cast<unsigned char>(y))) continue;
        if (l == r && x != y) continue;
        int cost = (s[l] != x);
        if (l != r) cost += (s[r] != y);
        best = min(best, cost);
      }
    }
    if (best == 3) {
      cout << -1 << '\n';
      return 0;
    }
    ans += best;
  }
  cout << ans << '\n';
}
```

## 推荐记忆

把输入看成“固定宽度块的串”，整体反转会同时反转块顺序和块内顺序。这个视角比真的拼出二进制文本更可迁移：字节、定长编码、固定宽整数都能复用同一证明。

## 来源与知识入口

- [力扣官方题目](https://leetcode.cn/problems/check-ascii-palindromic/)
- [力扣第 516 场周赛](https://leetcode.cn/contest/weekly-contest-516/)
- ZeroTracer 社区估算数据于 2026-08-26 查询，本题当前无数值记录。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/check-ascii-palindromic/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2253-b/">[codeforces] CF Educational Round 193 Div.2 B Hypercarp and the Control Panel →</a>
</nav>
