---
title: "[力扣 Top 37] LC 438 找到字符串中所有字母异位词 中等"
---

# [力扣 Top 37] LC 438 找到字符串中所有字母异位词 中等

<p class="daily-archive-kicker">2026-07-29 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-29 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

## 官方原始信息

- Top 排名：37
- 题号：LC 438
- 官方中文标题：找到字符串中所有字母异位词
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

### 原始题意

给定两个只含小写英文字母的字符串 `s` 和 `p`，找出 `s` 中所有与 `p` 互为字母异位词的连续子串，并按起点升序返回这些起点。字母异位词必须拥有完全相同的字符及出现次数，但字符顺序可以不同。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> findAnagrams(string s, string p);
};
```

### 全部官方样例

```text
输入：s = "cbaebabacd", p = "abc"
输出：[0,6]
解释："cba" 和 "bac" 都是 "abc" 的字母异位词。
```

```text
输入：s = "abab", p = "ab"
输出：[0,1,2]
解释："ab"、"ba"、"ab" 都满足要求。
```

### 全部约束

- $1\le |s|,|p|\le 3\times10^4$。
- `s` 和 `p` 仅由小写英文字母组成。
- 若 $|p|>|s|$，答案必为空。

## 最优结论

长度为 $m=|p|$ 的候选只可能是 `s` 的定长窗口。维护

$$
diff_c=count_p(c)-count_{window}(c)
$$

以及当前 `diff` 中非零槽位数。窗口右移时只改变离开字符和进入字符；非零槽位数为 0 当且仅当 26 个字符计数全部相同。时间 $O(|s|+|p|)$，额外空间 $O(1)$。

## 约束与观察

- 候选子串长度被固定为 $|p|$，无需枚举终点。
- 排序能判断异位词，却会对相邻窗口反复处理绝大多数相同字符。
- 字母表只有 26 个字符，计数状态是常数规模；进一步维护“非零计数个数”后，每次移动只需 $O(1)$。
- 返回下标最多有 $|s|-|p|+1$ 个，输出空间不计入辅助空间。

## 解法递进

### 解法一：逐窗口排序

枚举所有长度为 $m$ 的窗口，各自排序后与排好序的 `p` 比较。覆盖了全部候选，但重复排序使时间达到 $O((n-m+1)m\log m)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findAnagrams(string s, string p) {
    vector<int> answer;
    if (p.size() > s.size()) {
      return answer;
    }
    string target = p;
    sort(target.begin(), target.end());
    int length = static_cast<int>(p.size());
    for (int left = 0; left + length <= static_cast<int>(s.size()); ++left) {
      string candidate = s.substr(left, length);
      sort(candidate.begin(), candidate.end());
      if (candidate == target) {
        answer.push_back(left);
      }
    }
    return answer;
  }
};
```

### 解法二：滑动窗口加 26 位计数

相邻窗口只删除一个字符、加入一个字符。每次比较两个 26 位数组，时间 $O(26n)=O(n)$，空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findAnagrams(string s, string p) {
    vector<int> answer;
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(p.size());
    if (m > n) {
      return answer;
    }
    array<int, 26> need{};
    array<int, 26> window{};
    for (char c : p) {
      ++need[c - 'a'];
    }
    for (int right = 0; right < n; ++right) {
      ++window[s[right] - 'a'];
      if (right >= m) {
        --window[s[right - m] - 'a'];
      }
      if (right + 1 >= m && window == need) {
        answer.push_back(right - m + 1);
      }
    }
    return answer;
  }
};
```

### 解法三：维护非零差值数

比较数组仍会固定扫描 26 项。维护非零槽位数后，每个字符更新都只触及一个槽位。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findAnagrams(string s, string p) {
    vector<int> answer;
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(p.size());
    if (m > n) {
      return answer;
    }
    array<int, 26> difference{};
    int nonzero = 0;
    auto change = [&](int letter, int delta) {
      if (difference[letter] == 0) {
        ++nonzero;
      }
      difference[letter] += delta;
      if (difference[letter] == 0) {
        --nonzero;
      }
    };
    for (char c : p) {
      change(c - 'a', 1);
    }
    for (int i = 0; i < m; ++i) {
      change(s[i] - 'a', -1);
    }
    if (nonzero == 0) {
      answer.push_back(0);
    }
    for (int right = m; right < n; ++right) {
      change(s[right - m] - 'a', 1);
      change(s[right] - 'a', -1);
      if (nonzero == 0) {
        answer.push_back(right - m + 1);
      }
    }
    return answer;
  }
};
```

## 正确性证明

初始化后，`difference[c]` 恰为模式串中字符 `c` 的出现次数减去首个窗口中的出现次数。窗口从 `[l,l+m)` 移到 `[l+1,l+m+1)` 时，离开字符在窗口中的计数减一，因此对应差值加一；进入字符的窗口计数加一，因此差值减一。不变量对每次移动都成立。

两个等长字符串互为字母异位词，当且仅当每种字符的出现次数相同，也就是所有 `difference[c]` 均为 0。变量 `nonzero` 精确记录非零槽位数，所以算法加入且只加入全部合法窗口起点。

## 样例手推

对 `s="cbaebabacd"`、`p="abc"`：

- 首窗 `"cba"` 的 26 项差值全为 0，记录 0；
- 窗口右移后依次得到 `"bae"`、`"aeb"`、`"eba"`、`"bab"`、`"aba"`，都至少有一个非零槽位；
- 起点 6 的窗口 `"bac"` 再次使差值全为 0，记录 6。

## 易错点

- 必须固定窗口长度为 `p.size()`，不能把本题套成可变长度覆盖窗口。
- 移动时要让离开字符恢复到模式侧、进入字符计入窗口侧，符号不能写反。
- `p` 比 `s` 长时应提前返回，避免初始化越界。
- 相同起点只记录一次；本题窗口天然按起点递增，无需额外排序。

## 验证说明

以逐窗口排序为 oracle，对长度 1–12 的随机小写字符串逐一比较所有返回下标；另测模式比文本长、全相同字符、无解、每个窗口均有解和两个样例。

## Follow-up 与变种

### 变种一：字符集不再局限于 26 个小写字母

若输入是任意字节字符，固定数组失效。使用哈希表保存非零差值；每次更新后删除值为 0 的键，哈希表为空即匹配。期望时间 $O(n+m)$，空间 $O(\sigma)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findAnagrams(string s, string p) {
    vector<int> answer;
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(p.size());
    if (m > n) {
      return answer;
    }
    unordered_map<unsigned char, int> difference;
    auto change = [&](unsigned char c, int delta) {
      int value = difference[c] + delta;
      if (value == 0) {
        difference.erase(c);
      } else {
        difference[c] = value;
      }
    };
    for (unsigned char c : p) {
      change(c, 1);
    }
    for (int i = 0; i < m; ++i) {
      change(static_cast<unsigned char>(s[i]), -1);
    }
    if (difference.empty()) {
      answer.push_back(0);
    }
    for (int right = m; right < n; ++right) {
      change(static_cast<unsigned char>(s[right - m]), 1);
      change(static_cast<unsigned char>(s[right]), -1);
      if (difference.empty()) {
        answer.push_back(right - m + 1);
      }
    }
    return answer;
  }
};
```

### 变种二：文本以数据流分块到达

不能保存完整文本时，只保留最近 $m$ 个字符及其计数。每个字符摊还 $O(1)$，内存 $O(m)$；返回全局起点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class AnagramStream {
  array<int, 26> need_{};
  array<int, 26> window_{};
  deque<char> recent_;
  int length_;
  long long seen_ = 0;
public:
  explicit AnagramStream(const string& pattern) : length_(static_cast<int>(pattern.size())) {
    for (char c : pattern) {
      ++need_[c - 'a'];
    }
  }
  vector<long long> feed(const string& chunk) {
    vector<long long> answer;
    for (char c : chunk) {
      long long position = seen_++;
      recent_.push_back(c);
      ++window_[c - 'a'];
      if (static_cast<int>(recent_.size()) > length_) {
        --window_[recent_.front() - 'a'];
        recent_.pop_front();
      }
      if (static_cast<int>(recent_.size()) == length_ && window_ == need_) {
        answer.push_back(position - length_ + 1);
      }
    }
    return answer;
  }
};
```

### 变种三：模式串允许 `?` 匹配任意单个小写字母

只需保证窗口对每个固定字符的计数不少于需求；窗口剩余位置必然由通配符吸收。维护固定字符的总缺口，时间 $O(n+m)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> wildcardAnagrams(const string& s, const string& pattern) {
    vector<int> answer;
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(pattern.size());
    if (m > n) {
      return answer;
    }
    array<int, 26> need{};
    array<int, 26> window{};
    for (char c : pattern) {
      if (c != '?') {
        ++need[c - 'a'];
      }
    }
    int missing = accumulate(need.begin(), need.end(), 0);
    auto add = [&](char c) {
      int index = c - 'a';
      if (window[index] < need[index]) {
        --missing;
      }
      ++window[index];
    };
    auto remove = [&](char c) {
      int index = c - 'a';
      --window[index];
      if (window[index] < need[index]) {
        ++missing;
      }
    };
    for (int right = 0; right < n; ++right) {
      add(s[right]);
      if (right >= m) {
        remove(s[right - m]);
      }
      if (right + 1 >= m && missing == 0) {
        answer.push_back(right - m + 1);
      }
    }
    return answer;
  }
};
```

### 变种四：同一文本需要查询许多模式串

按模式长度分组。每个不同长度只扫描文本一次，并用 26 维计数向量建立窗口索引；同组模式直接查表。设不同长度集合为 $L$，时间 $O(26\sum_{\ell\in L}n)$，空间为所有被索引窗口。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> findMany(const string& s, const vector<string>& patterns) {
    map<int, vector<int>> queriesByLength;
    for (int i = 0; i < static_cast<int>(patterns.size()); ++i) {
      queriesByLength[patterns[i].size()].push_back(i);
    }
    vector<vector<int>> answer(patterns.size());
    for (const auto& [length, queryIds] : queriesByLength) {
      if (length > static_cast<int>(s.size())) {
        continue;
      }
      map<array<int, 26>, vector<int>> starts;
      array<int, 26> window{};
      for (int right = 0; right < static_cast<int>(s.size()); ++right) {
        ++window[s[right] - 'a'];
        if (right >= length) {
          --window[s[right - length] - 'a'];
        }
        if (right + 1 >= length) {
          starts[window].push_back(right - length + 1);
        }
      }
      for (int queryId : queryIds) {
        array<int, 26> signature{};
        for (char c : patterns[queryId]) {
          ++signature[c - 'a'];
        }
        auto it = starts.find(signature);
        if (it != starts.end()) {
          answer[queryId] = it->second;
        }
      }
    }
    return answer;
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-36-lc198/">← [力扣 Top 36] LC 198 打家劫舍 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-38-lc46/">[力扣 Top 38] LC 46 全排列 中等 →</a>
</nav>
