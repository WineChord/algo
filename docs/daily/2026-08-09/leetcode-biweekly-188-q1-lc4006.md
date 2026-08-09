---
title: "[力扣竞赛] 第 188 场双周赛 Q1 LC 4006 统计有效前缀数目 简单"
---

# [力扣竞赛] 第 188 场双周赛 Q1 LC 4006 统计有效前缀数目 简单

<p class="daily-archive-kicker">2026-08-09 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=90f22130e9ff3ffb05ffea181edced44a0f5115368f813c2c6b189ec64c329f1 -->
## 官方原始信息

- 比赛：第 188 场双周赛。
- 题号：Q1 / LC 4006。
- 官方中文标题：统计有效前缀数目。
- 官方难度：简单。
- 官方竞赛分值：3 分；ZeroTracer 社区估算竞赛分未知。
- 官方链接：[统计有效前缀数目](https://leetcode.cn/problems/count-valid-prefixes/)

### 原始题意与函数签名

给定二进制字符串 `s`。若一个非空前缀的字符可以重新排列成相邻字符均不同的交替字符串，则该前缀有效。返回有效前缀数量。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int countValidPrefixes(string s);
};
```

### 全部官方样例

```text
输入：s = "00101"
输出：3
解释：有效前缀为 "0"、"001"、"00101"；后两者可分别重排为 "010"、"01010"。
```

```text
输入：s = "101"
输出：3
解释：三个前缀本身都已经交替。
```

### 全部约束

- $1\le |s|\le100$。
- `s` 只由 `0` 和 `1` 构成。
- 前缀必须非空，且只能重排字符，不能增删。

## 约束推导与观察

长度为 $L$ 的交替二进制串，两种字符数量相等（$L$ 为偶数），或较多者恰多 1（$L$ 为奇数）。反过来，只要零、一码数之差不超过 1，就能从较多字符开始交替摆放。因此前缀有效当且仅当

$$
|count_0-count_1|\le1.
$$

扫描前缀时只需维护一个差值，不必真的构造排列。

## 解法递进

### 解法一：枚举前缀的所有不同排列

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool hasAlternatingPermutation(string prefix) {
    sort(prefix.begin(), prefix.end());
    do {
      bool valid = true;
      for (int i = 1; i < static_cast<int>(prefix.size()); ++i) {
        valid &= prefix[i] != prefix[i - 1];
      }
      if (valid) {
        return true;
      }
    } while (next_permutation(prefix.begin(), prefix.end()));
    return false;
  }
public:
  int countValidPrefixes(string s) {
    int answer = 0;
    for (int length = 1; length <= static_cast<int>(s.size()); ++length) {
      answer += hasAlternatingPermutation(s.substr(0, length));
    }
    return answer;
  }
};
int main() {
}
```

它忠实覆盖定义，但最坏时间为 $O(n\cdot n!)$，只适合长度很小的 oracle。

### 解法二：每个前缀重新统计字符

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countValidPrefixes(string s) {
    int answer = 0;
    for (int length = 1; length <= static_cast<int>(s.size()); ++length) {
      int zeros = count(s.begin(), s.begin() + length, '0');
      int ones = length - zeros;
      answer += abs(zeros - ones) <= 1;
    }
    return answer;
  }
};
int main() {
}
```

利用计数判据后，时间降为 $O(n^2)$、空间 $O(1)$，但相邻前缀仍重复统计。

### 最佳实用解：维护前缀计数差

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countValidPrefixes(string s) {
    int difference = 0;
    int answer = 0;
    for (char ch : s) {
      difference += ch == '0' ? 1 : -1;
      answer += abs(difference) <= 1;
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n)$、空间 $O(1)$。只维护 `#0-#1`，是最简且不易错的方案。

## 正确性证明

必要性：交替排列中相同字符不能相邻，所以较多字符只能占首、尾多出的一个槽位，数量差不超过 1。充分性：若数量相等，从任一字符开始交替；若相差 1，从较多字符开始并交替放置，最后也以较多字符结束，所有字符恰好用完且无相邻相同。算法对每个前缀维护精确数量差，并按这一充要条件计数，因此答案正确。

## 样例手推

`00101` 的前缀差依次为 `1,2,1,2,1`，绝对值不超过 1 的位置为 1、3、5，共 3 个。`101` 的差为 `-1,0,-1`，三个前缀都有效。

## 易错点与方案比较

- 问的是“可以重排”，不能只检查原前缀是否已经交替。
- 判据是数量差不超过 1，不是必须相等。
- 前缀从长度 1 开始，空前缀不计数。
- 差值用正负任一方向都可以，但判断必须取绝对值。

## 变种一：字符集不再只有两种

新定义：任意字符多重集合能否重排成相邻不同的串。充要条件是最大频次不超过 $\lceil L/2\rceil$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int countRearrangeablePrefixes(const string& s) {
  array<int, 256> frequency{};
  int maximum = 0;
  int answer = 0;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    int value = ++frequency[static_cast<unsigned char>(s[i])];
    maximum = max(maximum, value);
    answer += maximum <= (i + 2) / 2;
  }
  return answer;
}
int main() {
  cout << countRearrangeablePrefixes("aabac") << '\n';
}
```

时间 $O(n)$、空间 $O(|\Sigma|)$。较少字符提供的间隙数必须足以隔开最高频字符，这给出同一充要条件。

## 变种二：统计所有有效二进制子串

新定义：不再只看前缀，统计可重排成交替串的全部非空子串。令前缀差为 `#0-#1`；子串有效当差值为 -1、0 或 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countValidSubstrings(const string& s) {
  unordered_map<int, int> frequency{{0, 1}};
  int prefix = 0;
  long long answer = 0;
  for (char ch : s) {
    prefix += ch == '0' ? 1 : -1;
    answer += frequency[prefix - 1] + frequency[prefix] + frequency[prefix + 1];
    ++frequency[prefix];
  }
  return answer;
}
int main() {
  cout << countValidSubstrings("00101") << '\n';
}
```

期望时间 $O(n)$、空间 $O(n)$。

## 变种三：二进制流在线追加

新定义：字符逐个到达，每次返回截至当前的有效前缀总数。状态只需差值与答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class PrefixAlternationTracker {
  int difference = 0;
  int answer = 0;
public:
  int append(char bit) {
    if (bit != '0' && bit != '1') {
      throw invalid_argument("bit");
    }
    difference += bit == '0' ? 1 : -1;
    answer += abs(difference) <= 1;
    return answer;
  }
};
int main() {
  PrefixAlternationTracker tracker;
  cout << tracker.append('0') << '\n';
}
```

每次追加 $O(1)$，空间 $O(1)$。

## 变种四：每个前缀最少替换多少字符

新定义：允许把某些位从 0 改 1 或从 1 改 0，求每个前缀变为可重排状态的最少替换数。一次替换把绝对数量差最多减少 2，因此答案为 $\max(0,\lceil(|d|-1)/2\rceil)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> minimumReplacements(const string& s) {
  vector<int> answer;
  int difference = 0;
  for (char ch : s) {
    difference += ch == '0' ? 1 : -1;
    int excess = max(0, abs(difference) - 1);
    answer.push_back((excess + 1) / 2);
  }
  return answer;
}
int main() {
  for (int x : minimumReplacements("00011")) {
    cout << x << ' ';
  }
}
```

时间 $O(n)$、输出外空间 $O(1)$。

## 可复现验证

枚举长度不超过 10 的全部二进制串，对每个前缀枚举全部不同排列检查是否交替，与计数判据和线性实现逐项对照；覆盖全 0、全 1、奇偶长度和已交替串。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/count-valid-prefixes/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-130-lc437/">← [力扣 Top 130] LC 437 路径总和 III 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-f/">[codeforces] CF Round 1113 Div.2 F Matrix Elimination →</a>
</nav>
