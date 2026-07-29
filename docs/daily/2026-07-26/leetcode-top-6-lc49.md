---
title: "[力扣 Top 6] LC 49 字母异位词分组 中等"
---

# [力扣 Top 6] LC 49 字母异位词分组 中等

<p class="daily-archive-kicker">2026-07-26 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../data-structures/hash-and-cache.md">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：https://leetcode.cn/problems/group-anagrams/
- 函数签名：`vector<vector<string>> groupAnagrams(vector<string>& strs)`

### 原始题意

给定字符串数组 `strs`，把由相同字符及相同出现次数构成、仅排列顺序不同的字符串归入同一组。组与组内元素都允许按任意顺序返回。

### 全部官方样例

1. `strs = ["eat","tea","tan","ate","nat","bat"]`，一种输出为 `[["bat"],["nat","tan"],["ate","eat","tea"]]`。
2. `strs = [""]`，输出 `[[""]]`。
3. `strs = ["a"]`，输出 `[["a"]]`。

### 全部约束

- $1\le |strs|\le 10^4$
- $0\le |strs[i]|\le 100$
- `strs[i]` 只包含小写英文字母

## 最优结论

两个字符串互为字母异位词，当且仅当 26 个字母的频次数组完全相同。把频次数组编码成无歧义键并放入哈希表，扫描一次即可分组。设所有字符串总长度为 $S$，时间为 $O(S+26n)$，除输出外空间为 $O(S+26n)$。若字符集不固定，排序后的字符串是更通用的键。

## 约束、边界与观察

- 允许空串，因此全零频次数组必须能成为合法键。
- 重复字符串当然属于同一组，不能去重。
- 不能把计数直接拼接成 `"1110..."`：`[1,11]` 与 `[11,1]` 会发生歧义，必须加分隔符或使用定长结构。
- $n=10^4$、单串长度至多 100；两两比较最坏接近 $10^8$ 对，不能作为提交方案。

## 样例手推

`"eat"`、`"tea"`、`"ate"` 的频次都满足 `a:1,e:1,t:1`，编码键相同；`"tan"` 与 `"nat"` 的键为 `a:1,n:1,t:1`；`"bat"` 的键只出现一次。因此形成三组。

## 解法一：逐组两两比较

维护已经建立的组。每个新字符串与每组代表串比较频次，找到第一组相同者后加入，否则新建一组。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool same(string& a, string& b) {
    if (a.size() != b.size()) return false;
    array<int, 26> cnt{};
    for (char c : a) ++cnt[c - 'a'];
    for (char c : b) --cnt[c - 'a'];
    for (int x : cnt) {
      if (x != 0) return false;
    }
    return true;
  }
public:
  vector<vector<string>> groupAnagrams(vector<string>& strs) {
    vector<vector<string>> groups;
    for (string& s : strs) {
      bool placed = false;
      for (auto& group : groups) {
        if (same(s, group[0])) {
          group.push_back(s);
          placed = true;
          break;
        }
      }
      if (!placed) groups.push_back({s});
    }
    return groups;
  }
};
```

最坏时间 $O(n^2L)$，其中 $L$ 是单串最大长度；空间主要是输出。瓶颈是相同代表串的频次被反复计算。

## 解法二：排序字符串作为签名

字母异位词排序后必然得到相同字符串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) {
      string key = s;
      sort(key.begin(), key.end());
      groups[key].push_back(s);
    }
    vector<vector<string>> ans;
    ans.reserve(groups.size());
    for (auto& [key, group] : groups) ans.push_back(std::move(group));
    return ans;
  }
};
```

时间 $O(\sum_i |s_i|\log |s_i|)$，空间 $O(S)$。它消除了组间比较，并适用于任意可排序字符集。

## 解法三：26 维频次签名（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string signature(const string& s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    string key;
    for (int x : cnt) {
      key.push_back('#');
      key += to_string(x);
    }
    return key;
  }
public:
  vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) groups[signature(s)].push_back(s);
    vector<vector<string>> ans;
    ans.reserve(groups.size());
    for (auto& [key, group] : groups) ans.push_back(std::move(group));
    return ans;
  }
};
```

### 正确性证明

对任意字符串 $s$，签名逐项记录每个小写字母的出现次数。若两个字符串互为字母异位词，它们每个字母的次数相同，签名相同，必进入同一哈希桶；反之，签名相同意味着 26 个计数逐项相等，两串包含完全相同的字符多重集合，因此必互为字母异位词。哈希桶恰好等于题目要求的等价类。

### 复杂度与选择

构造频次需要 $O(S)$，序列化每个键需要 $O(26n)$；哈希表平均时间 $O(S+26n)$，空间 $O(S+26n)$。固定 26 字母时优先记忆频次签名；需要支持 Unicode、大小写或任意字符时，排序签名更稳健。

## 常见错误

- 忘记空串，导致空键或全零键处理异常。
- 用字符集合而非频次数组，错误地把 `"abb"` 与 `"ab"` 归为一组。
- 计数拼接不加分隔符，产生键碰撞。
- 依赖 `unordered_map` 的遍历顺序去匹配某个固定输出；题目允许任意顺序。
- 把移动后的 `group` 或原字符串再次使用。

## Follow-up 1：输出顺序必须确定

规定组内字典序升序，组之间按各组第一个字符串升序。先按频次分组，再排序即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string keyOf(const string& s) {
    string key = s;
    sort(key.begin(), key.end());
    return key;
  }
public:
  vector<vector<string>> groupAnagrams(vector<string>& strs) {
    map<string, vector<string>> groups;
    for (string& s : strs) groups[keyOf(s)].push_back(s);
    vector<vector<string>> ans;
    for (auto& [key, group] : groups) {
      sort(group.begin(), group.end());
      ans.push_back(std::move(group));
    }
    sort(ans.begin(), ans.end(), [](const auto& a, const auto& b) { return a[0] < b[0]; });
    return ans;
  }
};
```

时间由排序主导，为 $O(\sum |s_i|\log |s_i|+\sum |G_j|\log |G_j|)$。

## Follow-up 2：字符串在线到达

封装为在线分组器，每次插入只更新一个桶；查询时返回当前快照。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class AnagramGrouper {
  unordered_map<string, vector<string>> groups;
  string keyOf(const string& s) const {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    string key;
    for (int x : cnt) key += "#" + to_string(x);
    return key;
  }
public:
  void add(string s) {
    groups[keyOf(s)].push_back(std::move(s));
  }
  vector<vector<string>> snapshot() const {
    vector<vector<string>> ans;
    ans.reserve(groups.size());
    for (const auto& [key, group] : groups) ans.push_back(group);
    return ans;
  }
};
```

单次插入平均 $O(|s|+26)$，保存全部字符串需要 $O(S)$。

## Follow-up 3：字符集不再限定为小写字母

对任意字节串采用排序键，不再依赖固定维度。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) {
      string key = s;
      sort(key.begin(), key.end(), [](unsigned char a, unsigned char b) { return a < b; });
      groups[key].push_back(s);
    }
    vector<vector<string>> ans;
    for (auto& [key, group] : groups) ans.push_back(std::move(group));
    return ans;
  }
};
```

时间 $O(\sum |s_i|\log |s_i|)$。真正的 Unicode 文本还应先按同一规范做归一化并按码点排序，而不能把 UTF-8 字节当字符。

## Follow-up 4：只求异位词下标对数量

同一签名此前出现过 $c$ 次时，新字符串新增 $c$ 个配对。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string keyOf(const string& s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    string key;
    for (int x : cnt) key += "#" + to_string(x);
    return key;
  }
public:
  long long countAnagramPairs(vector<string>& strs) {
    unordered_map<string, long long> freq;
    long long ans = 0;
    for (string& s : strs) {
      string key = keyOf(s);
      ans += freq[key];
      ++freq[key];
    }
    return ans;
  }
};
```

平均时间 $O(S+26n)$，空间 $O(26n)$；答案最多为 $\binom n2$，必须使用 `long long`。

## 验证

可用排序签名方案作 oracle，随机生成长度 $0\ldots 8$、字母集 `abc` 的字符串数组；把两种输出都规范化为“组内排序、组间排序”后比较。边界覆盖全部空串、全部相同、全部不同、重复字符串和相同字符集合但计数不同。

## Reference

- [官方题目](https://leetcode.cn/problems/group-anagrams/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-5-lc42.md">← [力扣 Top 5] LC 42 接雨水 困难</a>
<a class="daily-archive-pager__next" href="leetcode-top-7-lc5.md">[力扣 Top 7] LC 5 最长回文子串 中等 →</a>
</nav>
