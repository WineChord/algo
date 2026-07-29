---
title: "[力扣 Top 44] LC 28 找出字符串中第一个匹配项的下标 简单"
---

# [力扣 Top 44] LC 28 找出字符串中第一个匹配项的下标 简单

<p class="daily-archive-kicker">2026-07-30 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=41fdde7b5be048a7d028b615ed029854a0ea75ad4233d09b8f6b64fa98b15b37 -->
## 官方原始信息

- Top 排名：44
- 题号：LC 28
- 官方中文标题：找出字符串中第一个匹配项的下标
- 官方难度：简单
- 官方链接：[找出字符串中第一个匹配项的下标](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)

### 原始题意

给定字符串 `haystack` 与 `needle`，返回 `needle` 在 `haystack` 中第一次完整出现的起始下标；不存在则返回 -1。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int strStr(string haystack, string needle);
};
```

### 全部官方样例

```text
输入：haystack = "sadbutsad", needle = "sad"
输出：0
解释：匹配起点为 0 和 6，返回第一个。
```

```text
输入：haystack = "leetcode", needle = "leeto"
输出：-1
```

### 全部约束

- $1\le |haystack|,|needle|\le10^4$。
- 两个字符串只含小写英文字母。
- 官方约束排除了空 `needle`；实现仍可自然兼容空模式并返回 0。

## 约束推导

朴素匹配最坏比较 $O(nm)$ 次，在当前 $10^4$ 范围可能达到 $10^8$。重复比较来自模式串前缀与后缀的重合。KMP 用前缀函数记录失配后仍可保留的最长已匹配前缀，使文本指针永不回退，达到线性时间。

## 解法递进

### 解法一：枚举起点并逐字符比较

每个合法起点都完整检查一次，时间 $O((n-m+1)m)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int strStr(string haystack, string needle) {
    if (needle.empty()) {
      return 0;
    }
    for (int start = 0;
        start + static_cast<int>(needle.size()) <= static_cast<int>(haystack.size()); ++start) {
      int matched = 0;
      while (matched < static_cast<int>(needle.size()) &&
          haystack[start + matched] == needle[matched]) {
        ++matched;
      }
      if (matched == static_cast<int>(needle.size())) {
        return start;
      }
    }
    return -1;
  }
};
```

### 最佳实用解：KMP 前缀函数

`prefix[i]` 表示 `needle[0..i]` 的最长真前缀与后缀的公共长度。失配时把已匹配长度回退到 `prefix[matched-1]`，而不移动文本位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int strStr(string haystack, string needle) {
    if (needle.empty()) {
      return 0;
    }
    vector<int> prefix(needle.size());
    for (int i = 1; i < static_cast<int>(needle.size()); ++i) {
      int matched = prefix[i - 1];
      while (matched > 0 && needle[i] != needle[matched]) {
        matched = prefix[matched - 1];
      }
      if (needle[i] == needle[matched]) {
        ++matched;
      }
      prefix[i] = matched;
    }
    int matched = 0;
    for (int i = 0; i < static_cast<int>(haystack.size()); ++i) {
      while (matched > 0 && haystack[i] != needle[matched]) {
        matched = prefix[matched - 1];
      }
      if (haystack[i] == needle[matched]) {
        ++matched;
      }
      if (matched == static_cast<int>(needle.size())) {
        return i - matched + 1;
      }
    }
    return -1;
  }
};
```

时间复杂度 $O(n+m)$，空间复杂度 $O(m)$。

## 正确性证明

不变量：扫描到文本位置 `i` 前，`matched` 是已扫描文本后缀与模式前缀能够相等的最大长度。

若新字符匹配，最长长度增加 1。若失配，任何仍可能延续的候选必须同时是当前已匹配模式前缀的后缀和模式的前缀；最长候选正是 `prefix[matched-1]`，反复回退枚举了所有可能边界而不遗漏。当 `matched=m` 时，最近 $m$ 个文本字符与完整模式相等；由于文本从左到右扫描，首次达到该状态的起点就是最小匹配下标。

## 样例手推

对 `haystack="sadbutsad"`、`needle="sad"`，模式前缀函数为 `[0,0,0]`。文本前三个字符依次把 `matched` 推到 1、2、3，于位置 2 首次完整匹配，起点为 $2-3+1=0$。

## 易错点与方案比较

- 前缀函数统计真前缀，不能把完整字符串自身计入。
- 失配回退的是模式长度，文本下标不回退。
- 返回起点公式为 `i - m + 1`。
- 找全部重叠匹配时，命中后不能清零，应回退到 `prefix[m-1]`。
- 只做一次且数据很小时朴素法更短；需要稳定线性上界、流式匹配或复用模式时优先 KMP。

## 变种一：返回全部匹配起点并允许重叠

命中后继续把 `matched` 回退到最长真边界，因而 `"aaa"` 中的 `"aa"` 会得到起点 0、1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string text, pattern;
  cin >> text >> pattern;
  vector<int> prefix(pattern.size());
  for (int i = 1; i < static_cast<int>(pattern.size()); ++i) {
    int j = prefix[i - 1];
    while (j > 0 && pattern[i] != pattern[j]) {
      j = prefix[j - 1];
    }
    if (pattern[i] == pattern[j]) {
      ++j;
    }
    prefix[i] = j;
  }
  int matched = 0;
  for (int i = 0; i < static_cast<int>(text.size()); ++i) {
    while (matched > 0 && text[i] != pattern[matched]) {
      matched = prefix[matched - 1];
    }
    if (text[i] == pattern[matched]) {
      ++matched;
    }
    if (matched == static_cast<int>(pattern.size())) {
      cout << i - matched + 1 << '\n';
      matched = prefix[matched - 1];
    }
  }
}
```

时间 $O(n+m)$，空间 $O(m)$。

## 变种二：文本以字符流到达

模式预处理一次，每收到一个字符更新 KMP 状态并立即报告以当前位置结尾的匹配；无需保存完整文本。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string pattern, stream;
  cin >> pattern >> stream;
  vector<int> prefix(pattern.size());
  for (int i = 1; i < static_cast<int>(pattern.size()); ++i) {
    int j = prefix[i - 1];
    while (j > 0 && pattern[i] != pattern[j]) {
      j = prefix[j - 1];
    }
    if (pattern[i] == pattern[j]) {
      ++j;
    }
    prefix[i] = j;
  }
  int matched = 0;
  long long position = -1;
  for (char ch : stream) {
    ++position;
    while (matched > 0 && ch != pattern[matched]) {
      matched = prefix[matched - 1];
    }
    if (ch == pattern[matched]) {
      ++matched;
    }
    if (matched == static_cast<int>(pattern.size())) {
      cout << position - matched + 1 << '\n';
      matched = prefix[matched - 1];
    }
  }
}
```

每个字符摊还 $O(1)$，状态空间 $O(m)$。

## 变种三：同时匹配很多模式串

新定义：在同一文本中找出多个模式的出现位置。逐模式跑 KMP 为 $O(\sum m_i+kn)$；Aho-Corasick 把模式前缀合并成字典树，并为失配建立失败指针。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  array<int, 26> next{};
  int fail = 0;
  vector<int> output;
  Node() {
    next.fill(-1);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k;
  cin >> k;
  vector<string> patterns(k);
  vector<Node> trie(1);
  for (int id = 0; id < k; ++id) {
    cin >> patterns[id];
    int node = 0;
    for (char ch : patterns[id]) {
      int c = ch - 'a';
      if (trie[node].next[c] == -1) {
        trie[node].next[c] = trie.size();
        trie.emplace_back();
      }
      node = trie[node].next[c];
    }
    trie[node].output.push_back(id);
  }
  queue<int> queue;
  for (int c = 0; c < 26; ++c) {
    int child = trie[0].next[c];
    if (child == -1) {
      trie[0].next[c] = 0;
    } else {
      queue.push(child);
    }
  }
  while (!queue.empty()) {
    int node = queue.front();
    queue.pop();
    int failure = trie[node].fail;
    trie[node].output.insert(
        trie[node].output.end(), trie[failure].output.begin(), trie[failure].output.end());
    for (int c = 0; c < 26; ++c) {
      int child = trie[node].next[c];
      if (child == -1) {
        trie[node].next[c] = trie[failure].next[c];
      } else {
        trie[child].fail = trie[failure].next[c];
        queue.push(child);
      }
    }
  }
  string text;
  cin >> text;
  int node = 0;
  for (int i = 0; i < static_cast<int>(text.size()); ++i) {
    node = trie[node].next[text[i] - 'a'];
    for (int id : trie[node].output) {
      cout << id << ' ' << i - static_cast<int>(patterns[id].size()) + 1 << '\n';
    }
  }
}
```

构建 $O(\sum m_i\cdot|\Sigma|)$ 的保守上界，扫描文本加输出为 $O(n+\text{matches})$。

## 变种四：模式中 `?` 可匹配任意单字符

普通 KMP 的前缀相等关系不再能简单复用，因为两个 `?` 与具体字符之间的兼容性不具传递性。若规模不大，可直接枚举起点，逐位用“相等或模式为 `?`”判断。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string text, pattern;
  cin >> text >> pattern;
  for (int start = 0; start + static_cast<int>(pattern.size()) <= static_cast<int>(text.size());
      ++start) {
    bool ok = true;
    for (int j = 0; j < static_cast<int>(pattern.size()); ++j) {
      if (pattern[j] != '?' && pattern[j] != text[start + j]) {
        ok = false;
        break;
      }
    }
    if (ok) {
      cout << start << '\n';
      return 0;
    }
  }
  cout << -1 << '\n';
}
```

时间 $O(nm)$，空间 $O(1)$。规模很大时可用卷积、位并行或专门的通配符匹配算法，不能把普通 KMP 比较器机械替换后宣称正确。

## 可复现验证

- 两个官方样例、模式长于文本、首尾命中、完全相等、重复字符与重叠匹配均应覆盖。
- 小规模随机字符串可将朴素结果作为 oracle，与 KMP 的首个及全部匹配结果对拍。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-43-lc416/">← [力扣 Top 43] LC 416 分割等和子集 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-45-lc209/">[力扣 Top 45] LC 209 长度最小的子数组 中等 →</a>
</nav>
