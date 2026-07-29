---
title: "[力扣 Top 30] LC 14 最长公共前缀 简单"
---

# [力扣 Top 30] LC 14 最长公共前缀 简单

<p class="daily-archive-kicker">2026-07-28 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-28 题目列表</a> · <a href="../../strings/index.md">进入知识专题</a></p>

## 官方原始信息

- 官方链接：<https://leetcode.cn/problems/longest-common-prefix/>
- slug：`longest-common-prefix`
- 官方难度：简单；官方竞赛分未提供；ZeroTracer 数据集无记录。
- 函数签名：`string longestCommonPrefix(vector<string>& strs)`
- 题意：返回字符串数组的最长公共前缀；不存在非空公共前缀时返回空串。
- 样例 1：`["flower","flow","flight"]` 输出 `"fl"`。
- 样例 2：`["dog","racecar","car"]` 输出 `""`。
- 约束：$1\le |strs|\le200$，$0\le |strs[i]|\le200$；非空字符串只含小写英文字母。

令全部字符数为 $S$、最短串长度为 $L$。任何算法至少要检查足以证伪或输出的字符，最优量级为 $O(S)$；空字符串会立即把答案限制为空。

## 解法一：枚举第一个字符串的所有前缀

从长到短枚举候选前缀，并逐个字符串比较。正确但会反复比较相同字符。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestCommonPrefix(vector<string>& strs) {
    string first = strs[0];
    for (int length = first.size(); length >= 0; --length) {
      string prefix = first.substr(0, length);
      bool valid = true;
      for (string& word : strs) {
        if (word.compare(0, length, prefix) != 0) {
          valid = false;
          break;
        }
      }
      if (valid) return prefix;
    }
    return "";
  }
};
```

最坏时间 $O(|strs|\cdot L^2)$，候选字符串空间 $O(L)$。

## 解法二：横向归并

维护前若干字符串的最长公共前缀，与下一个字符串逐步缩短。利用结合性 `lcp(lcp(a,b),c)=lcp(a,b,c)`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string common(string a, const string& b) {
    int length = min(a.size(), b.size());
    int i = 0;
    while (i < length && a[i] == b[i]) ++i;
    a.resize(i);
    return a;
  }
public:
  string longestCommonPrefix(vector<string>& strs) {
    string prefix = strs[0];
    for (int i = 1; i < (int)strs.size() && !prefix.empty(); ++i) {
      prefix = common(prefix, strs[i]);
    }
    return prefix;
  }
};
```

时间 $O(S)$，返回值之外空间 $O(L)$。

## 推荐解：纵向逐列检查

枚举第一个字符串的每一列，检查所有字符串该列是否存在且相同。第一次失败时，更长前缀必然也失败，立即返回。

不变量：进入第 `i` 列前，`strs[0][0..i)` 已被证明是全部字符串的公共前缀；若本列全部相同，不变量扩展一位；若有字符串过短或字符不同，则任何长度大于 `i` 的公共前缀都不可能存在，因此当前前缀最长。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestCommonPrefix(vector<string>& strs) {
    for (int i = 0; i < (int)strs[0].size(); ++i) {
      char expected = strs[0][i];
      for (int j = 1; j < (int)strs.size(); ++j) {
        if (i == (int)strs[j].size() || strs[j][i] != expected) {
          return strs[0].substr(0, i);
        }
      }
    }
    return strs[0];
  }
};
```

时间 $O(S)$，返回值之外额外空间 $O(1)$。优先记忆这一解法：终止条件直接对应前缀定义，边界最少。

样例 1：第 0 列均为 `f`，第 1 列均为 `l`，第 2 列分别为 `o,o,i`，故答案恰为 `"fl"`。边界包括单字符串返回自身、任一空串返回空、完全相同返回整串、首字符不同立即返回空。

常见错误：默认数组可能为空而访问 `strs[0]`（本题约束保证非空，但复用代码时需确认）；先访问 `strs[j][i]` 再判断长度；把公共前缀误写成公共子串；对 UTF-8 字节直接逐字符却声称按 Unicode 字符处理。

## Follow-up 1：最长公共后缀

新定义：返回所有字符串最长公共后缀。比较方向改为从末尾向前，原“第一次失配即停止”证明仍成立。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestCommonSuffix(vector<string>& strs) {
    int limit = strs[0].size();
    for (string& word : strs) limit = min(limit, (int)word.size());
    int length = 0;
    while (length < limit) {
      char expected = strs[0][strs[0].size() - 1 - length];
      bool same = true;
      for (int i = 1; i < (int)strs.size(); ++i) {
        if (strs[i][strs[i].size() - 1 - length] != expected) {
          same = false;
          break;
        }
      }
      if (!same) break;
      ++length;
    }
    return strs[0].substr(strs[0].size() - length);
  }
};
```

时间 $O(S)$，返回值之外空间 $O(1)$。

## Follow-up 2：字符串逐个到达，随时查询公共前缀

新定义：流式加入字符串。当前公共前缀只会缩短，加入新串时与现前缀做一次 LCP 即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class PrefixStream {
  bool empty = true;
  string prefix;
public:
  void add(const string& word) {
    if (empty) {
      prefix = word;
      empty = false;
      return;
    }
    int i = 0;
    while (i < (int)prefix.size() && i < (int)word.size() && prefix[i] == word[i]) ++i;
    prefix.resize(i);
  }
  string query() const {
    return empty ? "" : prefix;
  }
};
```

单次加入 $O(|prefix|+|word|)$ 的实际比较上界，查询 $O(|answer|)$（返回拷贝）。

## Follow-up 3：多次询问字符串下标区间的公共前缀

新定义：给定固定字符串数组，多次查询 `[l,r]`。逐次重算太慢；因 LCP 运算满足结合律，用线段树存每段公共前缀。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class PrefixRange {
  struct Segment {
    string prefix;
    bool valid = false;
  };
  int size = 1;
  vector<Segment> tree;
  string mergePrefix(const string& a, const string& b) const {
    int i = 0, limit = min(a.size(), b.size());
    while (i < limit && a[i] == b[i]) ++i;
    return a.substr(0, i);
  }
  Segment mergeSegment(const Segment& a, const Segment& b) const {
    if (!a.valid) return b;
    if (!b.valid) return a;
    return {mergePrefix(a.prefix, b.prefix), true};
  }
public:
  explicit PrefixRange(const vector<string>& words) {
    while (size < (int)words.size()) size <<= 1;
    tree.assign(size * 2, {});
    for (int i = 0; i < (int)words.size(); ++i) tree[size + i] = {words[i], true};
    for (int i = size - 1; i > 0; --i) tree[i] = mergeSegment(tree[i * 2], tree[i * 2 + 1]);
  }
  string query(int left, int right) const {
    Segment leftAnswer, rightAnswer;
    for (left += size, right += size; left <= right; left >>= 1, right >>= 1) {
      if (left & 1) {
        leftAnswer = mergeSegment(leftAnswer, tree[left]);
        ++left;
      }
      if (!(right & 1)) {
        rightAnswer = mergeSegment(tree[right], rightAnswer);
        --right;
      }
    }
    return mergeSegment(leftAnswer, rightAnswer).prefix;
  }
};
```

建树的字符比较总成本依赖公共前缀长度；每次查询访问 $O(\log n)$ 个节点，并比较这些节点的前缀。

## Follow-up 4：求至少 `k` 个字符串共享的最长前缀

新定义：不要求全部字符串，仅需至少 `k` 个。全局逐列已失效，因为不同字符串子集可形成不同前缀；用 Trie 统计经过每个节点的字符串数，寻找计数至少 `k` 的最深节点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  struct Node {
    array<int, 26> next;
    int count = 0;
    Node() {
      next.fill(-1);
    }
  };
public:
  string longestPrefixAtLeastK(vector<string>& words, int k) {
    vector<Node> trie(1);
    for (const string& word : words) {
      int node = 0;
      for (char c : word) {
        int index = c - 'a';
        if (trie[node].next[index] == -1) {
          trie[node].next[index] = trie.size();
          trie.emplace_back();
        }
        node = trie[node].next[index];
        ++trie[node].count;
      }
    }
    string best, path;
    function<void(int)> dfs = [&](int node) {
      if (path.size() > best.size() || (path.size() == best.size() && path < best)) best = path;
      for (int c = 0; c < 26; ++c) {
        int child = trie[node].next[c];
        if (child == -1 || trie[child].count < k) continue;
        path.push_back(char('a' + c));
        dfs(child);
        path.pop_back();
      }
    };
    dfs(0);
    return best;
  }
};
```

构建与遍历时间 $O(S)$，空间 $O(S)$；并列最长时返回字典序最小者。

## Follow-up 5：忽略 ASCII 大小写，但保留首串原文

新定义：比较时 `A` 与 `a` 等价，返回第一个字符串中的原始拼写。比较函数必须先转为 `unsigned char`，避免 `tolower` 的未定义行为。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestCommonPrefixIgnoreCase(vector<string>& strs) {
    for (int i = 0; i < (int)strs[0].size(); ++i) {
      unsigned char first = strs[0][i];
      int expected = tolower(first);
      for (int j = 1; j < (int)strs.size(); ++j) {
        if (i == (int)strs[j].size()) return strs[0].substr(0, i);
        unsigned char current = strs[j][i];
        if (tolower(current) != expected) return strs[0].substr(0, i);
      }
    }
    return strs[0];
  }
};
```

时间 $O(S)$，返回值之外空间 $O(1)$；这只声明 ASCII/当前 C locale 语义，不冒充完整 Unicode 大小写折叠。

## 可复现验证

随机生成小写字符串数组，将纵向算法与“枚举首串所有前缀”的 oracle 对拍；区间版与逐区间横向 LCP 对拍；至少 `k` 版与枚举所有前缀计数对拍。结果见 `validation-report.json`。

## Reference

- [官方题目](https://leetcode.cn/problems/longest-common-prefix/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-29-lc704.md">← [力扣 Top 29] LC 704 二分查找 简单</a>
<a class="daily-archive-pager__next" href="leetcode-weekly-511-q3-lc3998.md">[力扣竞赛] 第 511 场周赛 Q3 LC 3998 使用子序列排序转换二进制字符串 中等 →</a>
</nav>
