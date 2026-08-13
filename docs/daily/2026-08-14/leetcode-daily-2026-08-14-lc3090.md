---
title: "[力扣每日一题] 2026-08-14｜LC 3090 每个字符最多出现两次的最长子字符串"
---

# [力扣每日一题] 2026-08-14｜LC 3090 每个字符最多出现两次的最长子字符串

<p class="daily-archive-kicker">2026-08-14 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-14 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8dfd83da718623a92d230b17e14be82c0ed87d20d0ccfb85c0d573aa74226cf3 -->
[官方题目：LC 3090 每个字符最多出现两次的最长子字符串](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/)

## 官方原始信息

- 日期：2026-08-14（Asia/Shanghai）；力扣中国官方每日一题接口已按该日期确认。
- 题号：3090。
- 标题：每个字符最多出现两次的最长子字符串。
- 官方难度：简单。
- 官方链接：[力扣中国](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/)。
- 标签：哈希表、字符串、滑动窗口。

给定只含小写英文字母的字符串 `s`。如果一个子字符串中的每个字符至多出现两次，就称它满足条件。返回满足条件的最长子字符串长度。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maximumLengthSubstring(string s);
};
```

### 全部官方样例

样例 1：

```text
输入：s = "bcbbbcba"
输出：4
解释：子字符串 "bcba" 中每个字符至多出现两次，长度为 4。
```

样例 2：

```text
输入：s = "aaaa"
输出：2
解释：最长满足条件的子字符串是 "aa"。
```

### 全部约束

- $2\le s.length\le100$。
- `s` 只含小写英文字母。

## 约束推导与关键观察

$n\le100$，二次枚举也能通过；但“连续子字符串 + 频次上限”天然具有单调性：固定右端点后，若窗口已经违法，再向左扩只会更违法；从左端删除字符只可能恢复合法。这正是双指针滑动窗口的适用条件。

右端加入字符 `x` 前，窗口合法。加入后，只有 `x` 的频次可能从 2 变成 3；其他字符没有变化。因此只需在 `count[x]>2` 时移动左端，无须每轮扫描 26 个计数。字符集固定为 26 个小写字母，频次数组是常数空间，不存在整数溢出风险，答案不超过 100。

## 解法递进

### 解法一：枚举每个子字符串后重新计数

枚举左右端点，再扫描该区间统计字符频次；每个候选都按定义检查。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLengthSubstring(string s) {
    int n = static_cast<int>(s.size());
    int answer = 0;
    for (int left = 0; left < n; ++left) {
      for (int right = left; right < n; ++right) {
        array<int, 26> count{};
        bool valid = true;
        for (int i = left; i <= right; ++i) {
          if (++count[s[i] - 'a'] > 2) valid = false;
        }
        if (valid) answer = max(answer, right - left + 1);
      }
    }
    return answer;
  }
};
int main() {
  cout << Solution().maximumLengthSubstring("bcbbbcba") << '\n';
}
```

时间 $O(n^3)$，空间 $O(1)$。它覆盖全部候选，适合作为小规模 oracle。

### 解法二：固定左端点，增量扩展右端点

同一个左端点下，右端每右移一格只增加一个字符；一旦某字符出现第三次，继续向右也不可能恢复合法，可以结束当前左端点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLengthSubstring(string s) {
    int n = static_cast<int>(s.size());
    int answer = 0;
    for (int left = 0; left < n; ++left) {
      array<int, 26> count{};
      for (int right = left; right < n; ++right) {
        int index = s[right] - 'a';
        if (++count[index] > 2) break;
        answer = max(answer, right - left + 1);
      }
    }
    return answer;
  }
};
int main() {
  cout << Solution().maximumLengthSubstring("aaaa") << '\n';
}
```

时间 $O(n^2)$，空间 $O(1)$。它消除了每个候选的重复计数，但不同左端点仍重复扫描。

### 最佳实用解：滑动窗口

右端只增不减；每次加入新字符后，移动左端直到该字符重新至多出现两次。此时 `[left,right]` 是以 `right` 结尾的最长合法窗口。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLengthSubstring(string s) {
    array<int, 26> count{};
    int left = 0;
    int answer = 0;
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      int index = s[right] - 'a';
      ++count[index];
      while (count[index] > 2) {
        --count[s[left] - 'a'];
        ++left;
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
int main() {
  cout << Solution().maximumLengthSubstring("bcbbbcba") << '\n';
}
```

左右指针各至多移动 $n$ 次，时间 $O(n)$；频次数组固定为 26 项，额外空间 $O(1)$。

### 同阶方案：记录每个字符最近三个位置

当字符 `x` 第三次出现在 `right` 时，窗口左端必须越过它在窗口中的最早一次出现。为每个字符保存出现位置队列也能做到线性时间，但计数窗口更短、更容易推广到任意上限。

## 正确性证明

维护不变量：每轮更新答案前，窗口 `[left,right]` 合法，且它是以 `right` 结尾、左端最靠左的合法窗口。

加入 `s[right]=x` 前，旧窗口合法；加入后只有 `x` 可能超限。循环逐个删除左端字符，直到删除了窗口中最早的一个 `x`，此时 `x` 的频次回到 2，其他字符只减少，因此窗口合法。循环停止前 `x` 仍出现 3 次，所以任何更靠左的窗口都包含这三次 `x` 而违法；停止后的 `left` 因而最小。于是 `right-left+1` 是该右端点的最大合法长度。枚举全部右端点并取最大值，得到全局最优。

## 样例手推与边界

对 `bcbbbcba`，读入前三个字符后窗口为 `bcb`。读入下一个 `b` 时，`b` 达到 3 次，左端越过第一个 `b`，窗口变成 `cbb`；继续读入 `b` 又触发收缩，窗口变成 `bb`。后续扩展到末尾得到 `bcba`，长度 4。

- 全部字符互不相同：窗口不收缩，答案为 $n$。
- 全部相同：第三个字符起每次把左端推进一格，答案为 2。
- 某字符恰好出现两次仍合法，条件是“至多两次”而非“少于两次”。
- 移动左端时必须先减少被移出字符的计数。

## 方案比较与推荐

三次枚举最贴近定义；二次枚举利用固定左端下的单调失败；滑动窗口进一步复用相邻左端的统计。位置队列与滑窗同为 $O(n)$，但滑窗只维护一个统一不变量，常数空间清楚，也自然支持一般的频次上限。面试中优先记“右端加入，违法时左端收缩，合法后更新答案”。

## 易错点

- 题目要求子字符串，必须连续；不能按全局频次选择字符。
- `while` 不能机械改成 `if`；一般上限或批量加入时可能需要删除多个字符。
- 只有新加入字符可能超限，但删除时要更新实际离开窗口的字符。
- 应在窗口恢复合法后更新答案。
- 固定 26 长数组依赖“小写英文字母”约束，字符集变化时需改用映射。

## 可复现验证

三种完整解均以 C++23 严格编译，两个官方样例得到 4 和 2。本轮固定种子对长度 2 至 30、字符集 `abcd` 的 100,000 个随机字符串，把线性滑窗与三次枚举定义 oracle 比较，零处不符；另核对全相同、全不同、恰好两次和频繁交替等边界。

## 变种一：每个字符至多出现 $k$ 次

把常数 2 改成参数 `k`，滑动窗口不变量完全不变；若 $k=0$，最长合法长度为 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLength(string s, int k) {
    if (k == 0) return 0;
    array<int, 26> count{};
    int left = 0;
    int answer = 0;
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      int index = s[right] - 'a';
      ++count[index];
      while (count[index] > k) {
        --count[s[left] - 'a'];
        ++left;
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
int main() {
  cout << Solution().maximumLength("abacaba", 2) << '\n';
}
```

时间 $O(n)$，额外空间 $O(1)$。

## 变种二：每个字符有不同上限

输入 `limit[26]`。加入字符 `x` 后只可能违反 `x` 自己的上限，仍只需围绕它收缩；上限为 0 的字符会被立即移出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLength(string s, const array<int, 26>& limit) {
    array<int, 26> count{};
    int left = 0;
    int answer = 0;
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      int index = s[right] - 'a';
      ++count[index];
      while (count[index] > limit[index]) {
        --count[s[left] - 'a'];
        ++left;
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
int main() {
  array<int, 26> limit;
  limit.fill(2);
  limit[0] = 1;
  cout << Solution().maximumLength("abacaba", limit) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$；原题是所有上限均为 2 的特例。

## 变种三：统计所有满足条件的子字符串

窗口恢复合法后，以 `right` 结尾的合法子字符串恰为左端在 `[left,right]` 的全部选择，共 `right-left+1` 个。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countSubstrings(string s) {
    array<int, 26> count{};
    int left = 0;
    long long answer = 0;
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      int index = s[right] - 'a';
      ++count[index];
      while (count[index] > 2) {
        --count[s[left] - 'a'];
        ++left;
      }
      answer += right - left + 1;
    }
    return answer;
  }
};
int main() {
  cout << Solution().countSubstrings("aaaa") << '\n';
}
```

时间 $O(n)$，空间 $O(1)$；计数最多为 $n(n+1)/2$，需用 64 位整数。

## 变种四：恢复最早出现的最长子字符串

记录最优左端；长度相等时不覆盖，便自然保留最早出现者。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string earliestMaximum(string s) {
    array<int, 26> count{};
    int left = 0;
    int bestLeft = 0;
    int bestLength = 0;
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      int index = s[right] - 'a';
      ++count[index];
      while (count[index] > 2) {
        --count[s[left] - 'a'];
        ++left;
      }
      int length = right - left + 1;
      if (length > bestLength) {
        bestLength = length;
        bestLeft = left;
      }
    }
    return s.substr(bestLeft, bestLength);
  }
};
int main() {
  cout << Solution().earliestMaximum("bcbbbcba") << '\n';
}
```

扫描时间 $O(n)$，最后复制答案 $O(L)$，额外统计空间 $O(1)$。

## 变种五：字符来自任意可哈希整数流

固定数组失效，改用哈希表维护频次；双指针结构仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumLength(vector<int>& values, int limit) {
    unordered_map<int, int> count;
    int left = 0;
    int answer = 0;
    for (int right = 0; right < static_cast<int>(values.size()); ++right) {
      int value = values[right];
      ++count[value];
      while (count[value] > limit) {
        int removed = values[left++];
        if (--count[removed] == 0) count.erase(removed);
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
int main() {
  vector<int> values{100, 2, 100, 100, 3};
  cout << Solution().maximumLength(values, 2) << '\n';
}
```

期望时间 $O(n)$，空间 $O(u)$，其中 $u$ 为当前窗口内不同值数量。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-c/">← [codeforces] CF Round 1116 Div.1 A / Div.2 C Hot Potatoes at the Fairy Warehouse</a>
<span class="daily-archive-pager__empty"></span>
</nav>
