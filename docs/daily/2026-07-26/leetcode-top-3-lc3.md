---
title: "[力扣 Top 3] LC 3 无重复字符的最长子串 中等"
---

# [力扣 Top 3] LC 3 无重复字符的最长子串 中等

<p class="daily-archive-kicker">2026-07-26 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)
- 函数签名：`int lengthOfLongestSubstring(string s)`

### 原始题意

给定字符串 `s`，求其中不含重复字符的最长连续子串长度。题目求的是子串而非子序列。

### 全部官方样例

1. `s = "abcabcbb"`，输出 `3`；`"abc"`、`"bca"`、`"cab"` 都合法。
2. `s = "bbbbb"`，输出 `1`。
3. `s = "pwwkew"`，输出 `3`；`"wke"` 是子串，而 `"pwke"` 只是子序列。

### 全部约束

- $0\le s.length\le 5\times 10^4$
- `s` 由英文字母、数字、符号和空格组成

## 最优结论

维护当前无重复窗口 `[l,r]` 和每个字节最后出现的位置。扫描到 `s[r]` 时，令 `l = max(l, last[s[r]] + 1)`，再更新最后位置与答案。时间 $O(n)$；官方字符范围可用大小 $256$ 的数组，额外空间 $O(1)$。优先记忆“最后位置让左端点直接跳跃”的版本。

## 约束、边界与关键观察

- 连续性使答案可以表示成一个窗口；删除左端字符不会引入新重复，窗口合法性具有单调可修复性。
- 当右端新字符与窗口内字符重复时，左端必须越过那个重复位置；越得更少仍非法，越得更多会无谓丢失候选。
- `l` 只能右移，所以更新必须取 `max`，不能被窗口左侧的陈旧出现位置拉回。
- 空串答案是 $0$；空格和符号都应作为普通字符处理。
- C++ 的 `char` 可能有符号，作为数组下标前转为 `unsigned char`。

## 样例手推

对 `"pwwkew"`：读到 `p,w` 时窗口为 `"pw"`；第二个 `w` 让左端跳到第一个 `w` 之后，窗口变为 `"w"`；随后扩成 `"wke"`，长度 $3$；最后一个 `w` 让左端再次越过旧 `w`，得到 `"kew"`，答案仍为 $3$。

## 解法一：枚举并逐个检查子串

枚举左右端点，再用集合检查子串是否有重复。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int n = s.size(), ans = 0;
    for (int l = 0; l < n; ++l) {
      for (int r = l; r < n; ++r) {
        array<int, 256> seen{};
        bool ok = true;
        for (int i = l; i <= r; ++i) {
          unsigned char c = s[i];
          if (seen[c]) {
            ok = false;
            break;
          }
          seen[c] = 1;
        }
        if (ok) ans = max(ans, r - l + 1);
      }
    }
    return ans;
  }
};
```

时间 $O(n^3)$，额外空间 $O(1)$。

## 解法二：固定左端，向右扩展

对每个左端点只维护一次集合；第一次重复后，更长的同左端子串都不合法，可以停止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int n = s.size(), ans = 0;
    for (int l = 0; l < n; ++l) {
      array<int, 256> seen{};
      for (int r = l; r < n; ++r) {
        unsigned char c = s[r];
        if (seen[c]) break;
        seen[c] = 1;
        ans = max(ans, r - l + 1);
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。它消除了对子串内部的重复扫描，但不同左端点仍反复处理同一字符。

## 解法三：计数滑动窗口

右端只前进一次；若新字符重复，就逐个删除左端字符直到窗口重新合法。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    array<int, 256> count{};
    int l = 0, ans = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
      unsigned char c = s[r];
      ++count[c];
      while (count[c] > 1) {
        --count[(unsigned char)s[l]];
        ++l;
      }
      ans = max(ans, r - l + 1);
    }
    return ans;
  }
};
```

左右指针各移动至多 $n$ 次，时间 $O(n)$，额外空间 $O(1)$。

## 解法四：最后位置直接跳跃（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    array<int, 256> last;
    last.fill(-1);
    int l = 0, ans = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
      unsigned char c = s[r];
      l = max(l, last[c] + 1);
      last[c] = r;
      ans = max(ans, r - l + 1);
    }
    return ans;
  }
};
```

### 正确性证明

循环开始处理 $r$ 时，`[l,r-1]` 无重复。若 `s[r]` 最近一次出现在位置 $p<l$ 或从未出现，加入它后窗口仍合法；若 $p\ge l$，任何包含 $p$ 和 $r$ 的窗口都重复，所以新左端至少为 $p+1$。取 `max(l,p+1)` 恰好删除必要的最短前缀，并保留最长合法窗口。由归纳，每次更新后 `[l,r]` 是以 $r$ 结尾的最长无重复子串，所有右端点取最大即得全局答案。

### 复杂度与方案比较

- 立方暴力适合验证小串。
- 二次扩展暴露“不同左端重复扫描”这一瓶颈。
- 计数窗口与最后位置都为 $O(n)$；计数版更容易推广到频次约束，最后位置版常数更小、代码更短。

## 常见错误

- 把子序列当作子串。
- 写成 `l = last[c] + 1`，让左端点倒退。
- 使用 `char` 直接索引数组，遇到高位字节产生负下标。
- 忘记空串。
- 发现重复后只移动左端一次，而旧重复字符可能仍在窗口内。

## Follow-up 1：返回实际最长子串

记录答案的起点和长度即可；同长度时这里保留最早出现者。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestUniqueSubstring(string s) {
    array<int, 256> last;
    last.fill(-1);
    int l = 0, bestL = 0, bestLen = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
      unsigned char c = s[r];
      l = max(l, last[c] + 1);
      last[c] = r;
      int len = r - l + 1;
      if (len > bestLen) {
        bestLen = len;
        bestL = l;
      }
    }
    return s.substr(bestL, bestLen);
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## Follow-up 2：最长子串至多含 $k$ 种字符

最后位置跳跃不再足够，因为非法原因是“种类总数”而非某个字符重复；维护窗口频次和不同字符数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLongestSubstringKDistinct(string s, int k) {
    if (k == 0) return 0;
    array<int, 256> count{};
    int l = 0, kinds = 0, ans = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
      unsigned char c = s[r];
      if (count[c]++ == 0) ++kinds;
      while (kinds > k) {
        unsigned char d = s[l++];
        if (--count[d] == 0) --kinds;
      }
      ans = max(ans, r - l + 1);
    }
    return ans;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## Follow-up 3：每个字符最多出现 $k$ 次

窗口非法只可能由刚加入的字符触发，持续删除左端直到其频次不超过 $k$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestAtMostKOccurrences(string s, int k) {
    if (k == 0) return 0;
    array<int, 256> count{};
    int l = 0, ans = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
      unsigned char c = s[r];
      ++count[c];
      while (count[c] > k) {
        --count[(unsigned char)s[l]];
        ++l;
      }
      ans = max(ans, r - l + 1);
    }
    return ans;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## Follow-up 4：字符流在线到达

保存当前位置、左边界和最后位置；每加入一个字符就更新截至当前的全局答案，无需保存完整字符串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LongestUniqueStream {
  array<long long, 256> last;
  long long pos = 0, left = 0, best = 0;
public:
  LongestUniqueStream() {
    last.fill(-1);
  }
  long long add(unsigned char c) {
    left = max(left, last[c] + 1);
    last[c] = pos;
    best = max(best, pos - left + 1);
    ++pos;
    return best;
  }
};
```

每次加入 $O(1)$，总空间 $O(1)$。

## Reference

- 官方题面与接口：[打开力扣中国页面](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-2-lc1/">← [力扣 Top 2] LC 1 两数之和 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-4-lc146/">[力扣 Top 4] LC 146 LRU 缓存 中等 →</a>
</nav>
