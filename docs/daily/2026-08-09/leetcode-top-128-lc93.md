---
title: "[力扣 Top 128] LC 93 复原 IP 地址 中等"
---

# [力扣 Top 128] LC 93 复原 IP 地址 中等

<p class="daily-archive-kicker">2026-08-09 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=81ce420af822f914c329bfbee26600604bbbc724c1461de6ecb498406250e187 -->
## 官方原始信息

- Top 排名：128
- 题号：LC 93
- 官方中文标题：复原 IP 地址
- 官方难度：中等
- 官方链接：[复原 IP 地址](https://leetcode.cn/problems/restore-ip-addresses/)

### 原始题意与函数签名

有效 IPv4 地址恰由四个十进制整数构成，每段在 0 到 255 之间且不能有前导零。给定只含数字的字符串 `s`，只能插入三个点，不能删除、重排字符，返回所有有效地址。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<string> restoreIpAddresses(string s);
};
```

### 全部官方样例

```text
输入：s = "25525511135"
输出：["255.255.11.135","255.255.111.35"]
```

```text
输入：s = "0000"
输出：["0.0.0.0"]
```

```text
输入：s = "101023"
输出：["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]
```

### 全部约束

- $1\le |s|\le20$。
- `s` 只由数字组成。
- 每段值在 $[0,255]$，多位段不能以 `0` 开头。

## 约束推导与观察

四段各长 1 到 3，所以只有 $4\le |s|\le12$ 时可能有解。选择前三个切点便唯一确定四段；回溯时若还剩 `parts` 段和 `remaining` 个字符，必须满足 $parts\le remaining\le3parts$，可提前剪枝。每段最多三位，解析不会溢出。

## 解法递进

### 解法一：枚举三个点的位置

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool valid(const string& part) {
    if (part.empty() || part.size() > 3) {
      return false;
    }
    if (part.size() > 1 && part[0] == '0') {
      return false;
    }
    return stoi(part) <= 255;
  }
public:
  vector<string> restoreIpAddresses(string s) {
    vector<string> answer;
    int n = s.size();
    for (int a = 1; a < n; ++a) {
      for (int b = a + 1; b < n; ++b) {
        for (int c = b + 1; c < n; ++c) {
          string p1 = s.substr(0, a);
          string p2 = s.substr(a, b - a);
          string p3 = s.substr(b, c - b);
          string p4 = s.substr(c);
          if (valid(p1) && valid(p2) && valid(p3) && valid(p4)) {
            answer.push_back(p1 + '.' + p2 + '.' + p3 + '.' + p4);
          }
        }
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n^3)$，每段至多 3 位，额外空间 $O(1)$（不计输出）。它完整枚举切分，是可靠 oracle。

### 解法二：逐段回溯

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<string> answer;
  vector<string> parts;
  void dfs(const string& s, int position) {
    if (parts.size() == 4) {
      if (position == static_cast<int>(s.size())) {
        answer.push_back(parts[0] + '.' + parts[1] + '.' + parts[2] + '.' + parts[3]);
      }
      return;
    }
    int value = 0;
    for (int end = position; end < static_cast<int>(s.size()) && end < position + 3; ++end) {
      if (end > position && s[position] == '0') {
        break;
      }
      value = value * 10 + s[end] - '0';
      if (value > 255) {
        break;
      }
      parts.push_back(s.substr(position, end - position + 1));
      dfs(s, end + 1);
      parts.pop_back();
    }
  }
public:
  vector<string> restoreIpAddresses(string s) {
    dfs(s, 0);
    return answer;
  }
};
int main() {
}
```

搜索树分支至多 3、深度固定 4，时间可视为常数上界，通用表达为 $O(3^4)$ 加输出；递归空间 $O(4)$。

### 最佳实用解：剩余长度剪枝的回溯

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<string> answer;
  array<string, 4> parts;
  void dfs(const string& s, int position, int part) {
    int remaining = s.size() - position;
    int slots = 4 - part;
    if (remaining < slots || remaining > 3 * slots) {
      return;
    }
    if (part == 4) {
      answer.push_back(parts[0] + '.' + parts[1] + '.' + parts[2] + '.' + parts[3]);
      return;
    }
    int value = 0;
    for (int length = 1; length <= 3 && position + length <= static_cast<int>(s.size()); ++length) {
      if (length > 1 && s[position] == '0') {
        break;
      }
      value = value * 10 + s[position + length - 1] - '0';
      if (value > 255) {
        break;
      }
      parts[part] = s.substr(position, length);
      dfs(s, position + length, part + 1);
    }
  }
public:
  vector<string> restoreIpAddresses(string s) {
    dfs(s, 0, 0);
    return answer;
  }
};
int main() {
}
```

时间为有效搜索节点数加输出，最坏 $O(3^4)$，递归空间 $O(4)$。固定数组和长度剪枝使它最稳定。

## 正确性证明

在深度 `part`，算法枚举下一段所有可能长度 1、2、3，并仅保留无前导零且值不超过 255 的段。任何合法地址的下一段必在这三种长度中，因此对应分支不会遗漏；每条到深度 4 且用完字符串的路径恰有四个合法段，是有效地址。切分位置序列唯一决定地址，所以不同路径不会重复。长度剪枝只排除无法为剩余段各分配 1 到 3 个字符的状态，不会排除合法解。

## 样例手推

`25525511135` 先取 `255.255`。第三段取 `11` 时余下 `135` 合法，得到 `255.255.11.135`；第三段取 `111` 时余下 `35` 合法。若第三段再短或更长，剩余长度或数值约束会剪掉。`0000` 中每段遇到第二位 0 就停止，只生成 `0.0.0.0`。

## 易错点与方案比较

- 单独的 `0` 合法，`00`、`01` 不合法。
- 只有恰好四段且恰好消费完字符串时才能收集答案。
- `stoi` 不是必需；逐位累积可在超过 255 时立即停止。
- 输入长度大于 12 直接被长度剪枝拒绝，不能为了凑四段删除数字。

## 变种一：恢复不含压缩写法的 IPv6 地址

新定义：字符串由十六进制字符组成，插入七个冒号形成八段，每段 1 到 4 位；这里不允许 `::` 压缩。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<string> restoreIPv6(const string& s) {
  vector<string> answer;
  array<string, 8> parts;
  auto dfs = [&](auto&& self, int position, int part) -> void {
    int remaining = s.size() - position;
    int slots = 8 - part;
    if (remaining < slots || remaining > 4 * slots) {
      return;
    }
    if (part == 8) {
      string address = parts[0];
      for (int i = 1; i < 8; ++i) {
        address += ':' + parts[i];
      }
      answer.push_back(address);
      return;
    }
    for (int length = 1; length <= 4 && position + length <= static_cast<int>(s.size()); ++length) {
      parts[part] = s.substr(position, length);
      self(self, position + length, part + 1);
    }
  };
  if (all_of(s.begin(), s.end(), [](unsigned char c) { return isxdigit(c); })) {
    dfs(dfs, 0, 0);
  }
  return answer;
}
int main() {
  cout << restoreIPv6("20010db8000000000000000000000001").size() << '\n';
}
```

搜索上界 $O(4^8)$，实际受总长度强约束；空间 $O(8)$ 加输出。

## 变种二：只统计有效 IPv4 切分数

新定义：不返回字符串，只计数。用 `dp[position][parts]` 记忆化，避免在更一般的段数版本中重复子问题。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int countIPv4(const string& s) {
  vector<array<int, 5>> memo(s.size() + 1);
  for (auto& row : memo) {
    row.fill(-1);
  }
  auto solve = [&](auto&& self, int position, int parts) -> int {
    if (parts == 4) {
      return position == static_cast<int>(s.size());
    }
    int& result = memo[position][parts];
    if (result != -1) {
      return result;
    }
    result = 0;
    int value = 0;
    for (int length = 1; length <= 3 && position + length <= static_cast<int>(s.size()); ++length) {
      if (length > 1 && s[position] == '0') {
        break;
      }
      value = value * 10 + s[position + length - 1] - '0';
      if (value > 255) {
        break;
      }
      result += self(self, position + length, parts + 1);
    }
    return result;
  };
  return solve(solve, 0, 0);
}
int main() {
  cout << countIPv4("101023") << '\n';
}
```

状态数 $O(4n)$，每个状态尝试三段，时间 $O(n)$、空间 $O(n)$。

## 变种三：数字串含通配符 `?`

新定义：每个 `?` 可独立替换为任一数字，统计“替换方案 + 切分方案”的数量。枚举单段所有替换，再递归下一段。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countWildcardIPv4(const string& s) {
  vector<array<long long, 5>> memo(s.size() + 1);
  for (auto& row : memo) {
    row.fill(-1);
  }
  auto segmentWays = [&](int position, int length) {
    int ways = 0;
    auto build = [&](auto&& self, int offset, int value) -> void {
      if (offset == length) {
        ways += value <= 255;
        return;
      }
      char c = s[position + offset];
      for (int digit = 0; digit <= 9; ++digit) {
        if (c != '?' && c - '0' != digit) {
          continue;
        }
        if (offset == 0 && length > 1 && digit == 0) {
          continue;
        }
        self(self, offset + 1, value * 10 + digit);
      }
    };
    build(build, 0, 0);
    return ways;
  };
  auto solve = [&](auto&& self, int position, int part) -> long long {
    if (part == 4) {
      return position == static_cast<int>(s.size());
    }
    long long& result = memo[position][part];
    if (result != -1) {
      return result;
    }
    result = 0;
    for (int length = 1; length <= 3 && position + length <= static_cast<int>(s.size()); ++length) {
      result += 1LL * segmentWays(position, length) * self(self, position + length, part + 1);
    }
    return result;
  };
  return solve(solve, 0, 0);
}
int main() {
  cout << countWildcardIPv4("?.?.?.?") << '\n';
}
```

每段最多枚举 $10^3$ 种替换，状态固定为 $O(n)$；时间 $O(10^3n)$、空间 $O(n)$。

## 变种四：推广到 `g` 段、每段上限 `M`

新定义：十进制串切成 `groups` 段，每段无前导零且值不超过 `limit`。最大段长由 `digits(limit)` 决定。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<string>> splitBounded(const string& s, int groups, int limit) {
  vector<vector<string>> answers;
  vector<string> parts;
  int maxLength = to_string(limit).size();
  auto dfs = [&](auto&& self, int position) -> void {
    int slots = groups - parts.size();
    int remaining = s.size() - position;
    if (remaining < slots || remaining > slots * maxLength) {
      return;
    }
    if (slots == 0) {
      answers.push_back(parts);
      return;
    }
    long long value = 0;
    for (int length = 1; length <= maxLength && position + length <= static_cast<int>(s.size());
        ++length) {
      if (length > 1 && s[position] == '0') {
        break;
      }
      value = value * 10 + s[position + length - 1] - '0';
      if (value > limit) {
        break;
      }
      parts.push_back(s.substr(position, length));
      self(self, position + length);
      parts.pop_back();
    }
  };
  dfs(dfs, 0);
  return answers;
}
int main() {
  cout << splitBounded("1234", 2, 99).size() << '\n';
}
```

时间为搜索树规模，最坏 $O(d^g)$，其中 $d$ 为最大段长；递归空间 $O(g)$。

## 可复现验证

枚举长度 $1..12$ 的随机数字串，以三切点枚举为 oracle，对比两种回溯的答案集合；逐项检查四段、无前导零、值域与拼接回原串。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/restore-ip-addresses/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-127-lc6/">← [力扣 Top 127] LC 6 Z 字形变换 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-129-lc349/">[力扣 Top 129] LC 349 两个数组的交集 简单 →</a>
</nav>
