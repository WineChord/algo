---
title: "[力扣 Top 82] LC 139 单词拆分 中等"
---

# [力扣 Top 82] LC 139 单词拆分 中等

<p class="daily-archive-kicker">2026-08-03 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../dp/string-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ad33d9988240e28b5a933a9e61da560bc761fe816d52b7e74e56c4968db778bf -->
## 官方原始信息

- Top 排名：82
- 题号：LC 139
- 官方中文标题：单词拆分
- 官方难度：中等
- 官方链接：[单词拆分](https://leetcode.cn/problems/word-break/)

### 原始题意

给定字符串 `s` 和互不相同的单词列表 `wordDict`，判断能否用字典中的一个或多个单词按顺序拼接出 `s`。字典单词可以重复使用。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool wordBreak(string s, vector<string>& wordDict);
};
```

### 全部官方样例

```text
输入：s = "leetcode", wordDict = ["leet","code"]
输出：true
```

```text
输入：s = "applepenapple", wordDict = ["apple","pen"]
输出：true
解释：字典单词可以重复使用。
```

```text
输入：s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
输出：false
```

### 全部约束

- $1\le s.length\le300$。
- $1\le wordDict.length\le1000$。
- $1\le wordDict_i.length\le20$。
- `s` 与字典单词只含小写英文字母。
- `wordDict` 中字符串互不相同。

## 约束推导与状态

切分点有 $n-1$ 个，暴力选择或不选择会产生 $2^{n-1}$ 种分割。真正影响后续的只有“已经匹配到的前缀长度”，因此定义 `dp[i]`：前缀 `s[0..i)` 是否可由字典拼出。

字典单词最大长度只有 20。把字典建成 Trie 后，从每个可达起点最多向后走 20 个字符，遇到单词结尾就标记新状态，复杂度为 $O(nL+\sum |word|)$，其中 $L\le20$。这比对每个 `i,j` 构造子串并哈希更稳定，也自然支持大量共享前缀。

空串不在官方输入中，但初始化 `dp[0]=true` 是所有转移的起点；“一个或多个单词”由 `s` 非空自动满足。

## 解法递进

### 解法一：枚举当前位置可选单词

从下标 0 开始，尝试每个能匹配当前位置的字典词并递归。它完整覆盖所有分割，但同一下标会被不同前缀反复访问。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool search(const string& s, const vector<string>& words, int index) {
    if (index == static_cast<int>(s.size())) {
      return true;
    }
    for (const string& word : words) {
      if (index + word.size() <= s.size() && s.compare(index, word.size(), word) == 0 &&
          search(s, words, index + word.size())) {
        return true;
      }
    }
    return false;
  }
public:
  bool wordBreak(string s, vector<string>& wordDict) {
    return search(s, wordDict, 0);
  }
};
```

最坏时间指数级，递归栈 $O(n)$，适合作为短串 oracle。

### 解法二：哈希集合上的前缀 DP

枚举终点与长度不超过 20 的最后一个单词；若前缀可达且子串在字典中，则新前缀可达。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> words(wordDict.begin(), wordDict.end());
    int maximumLength = 0;
    for (const string& word : wordDict) {
      maximumLength = max(maximumLength, static_cast<int>(word.size()));
    }
    vector<char> dp(s.size() + 1);
    dp[0] = true;
    for (int end = 1; end <= static_cast<int>(s.size()); ++end) {
      for (int length = 1; length <= maximumLength && length <= end; ++length) {
        if (dp[end - length] && words.count(s.substr(end - length, length))) {
          dp[end] = true;
          break;
        }
      }
    }
    return dp[s.size()];
  }
};
```

忽略子串复制时为 $O(nL)$，实际字符工作为 $O(nL^2)$，空间 $O(n+\sum|word|)$。

### 最佳实用解：Trie 驱动可达前缀

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  struct Node {
    array<int, 26> next;
    bool terminal = false;
    Node() {
      next.fill(-1);
    }
  };
public:
  bool wordBreak(string s, vector<string>& wordDict) {
    vector<Node> trie(1);
    for (const string& word : wordDict) {
      int node = 0;
      for (char character : word) {
        int letter = character - 'a';
        if (trie[node].next[letter] == -1) {
          trie[node].next[letter] = trie.size();
          trie.emplace_back();
        }
        node = trie[node].next[letter];
      }
      trie[node].terminal = true;
    }
    vector<char> reachable(s.size() + 1);
    reachable[0] = true;
    for (int start = 0; start < static_cast<int>(s.size()); ++start) {
      if (!reachable[start]) {
        continue;
      }
      int node = 0;
      for (int end = start; end < static_cast<int>(s.size()); ++end) {
        int letter = s[end] - 'a';
        node = trie[node].next[letter];
        if (node == -1) {
          break;
        }
        if (trie[node].terminal) {
          reachable[end + 1] = true;
        }
      }
    }
    return reachable[s.size()];
  }
};
```

时间 $O(\sum|word|+nL)$，空间 $O(\sum|word|+n)$。官方 $L\le20$，这是兼顾复杂度、重复前缀和扩展性的最佳实用解。

## 正确性证明

不变量：处理起点 `start` 前，`reachable[i]` 为真当且仅当 `s[0..i)` 可由字典词拼出。`reachable[0]=true` 对空前缀成立。只有可达起点才沿 Trie 扫描；每次到达终止节点，`s[start..end]` 恰是一个字典词，把它接在已有合法前缀后得到合法前缀 `end+1`，所以不会误标。反之，任一合法分割的最后一个词从某个合法起点开始；归纳假设使该起点可达，Trie 扫描必经过该完整单词的终止节点，从而标记终点。最终 `reachable[n]` 精确表示整个字符串可拆分。

## 样例手推

`leetcode` 中 `reachable[0]=true`。从 0 沿 Trie 读到 `leet` 的终止节点，标记 4；从 4 读到 `code`，标记 8，于是返回真。`catsandog` 可到达 3（`cat`）、4（`cats`）和 7（`sand`/`and`），但从 7 的 `og` 不在 Trie 中，位置 9 不可达，返回假。

## 易错点与方案比较

- 单词可重复使用，不能在匹配后从字典删除。
- `dp[0]` 必须为真；它表示尚未取词的合法空前缀。
- Trie 扫描一旦缺边就应停止当前起点，不能跳过字符。
- 只要存在一种分割就返回真，不要贪心选择最长或最短词；`cars`/`car` 一类前缀会让贪心失败。
- 哈希 DP 更短，Trie 避免反复构造子串并复用公共前缀；需要多次查询或恢复路径时推荐 Trie。

## 变种一：恢复一种单词拆分

新定义：若可拆分，输出一组单词。记录每个首次可达终点的前驱下标，最终逆向恢复。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int count;
  cin >> s >> count;
  vector<string> words(count);
  for (string& word : words) {
    cin >> word;
  }
  unordered_set<string> dictionary(words.begin(), words.end());
  int maximumLength = 0;
  for (const string& word : words) {
    maximumLength = max(maximumLength, static_cast<int>(word.size()));
  }
  vector<int> previous(s.size() + 1, -1);
  previous[0] = 0;
  for (int end = 1; end <= static_cast<int>(s.size()); ++end) {
    for (int length = 1; length <= maximumLength && length <= end; ++length) {
      int start = end - length;
      if (previous[start] != -1 && dictionary.count(s.substr(start, length))) {
        previous[end] = start;
        break;
      }
    }
  }
  if (previous[s.size()] == -1) {
    cout << "NO\n";
    return 0;
  }
  vector<string> answer;
  for (int end = s.size(); end > 0; end = previous[end]) {
    answer.push_back(s.substr(previous[end], end - previous[end]));
  }
  reverse(answer.begin(), answer.end());
  for (const string& word : answer) {
    cout << word << ' ';
  }
  cout << '\n';
}
```

时间 $O(nL^2)$（含子串复制），空间 $O(n+\sum|word|)$。

## 变种二：统计拆分方案数

新定义：统计按切分位置区分的全部方案数，对 $10^9+7$ 取模。布尔可达改为计数累加。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  string s;
  int count;
  cin >> s >> count;
  unordered_set<string> dictionary;
  int maximumLength = 0;
  while (count--) {
    string word;
    cin >> word;
    maximumLength = max(maximumLength, static_cast<int>(word.size()));
    dictionary.insert(word);
  }
  vector<long long> ways(s.size() + 1);
  ways[0] = 1;
  for (int end = 1; end <= static_cast<int>(s.size()); ++end) {
    for (int length = 1; length <= maximumLength && length <= end; ++length) {
      int start = end - length;
      if (dictionary.count(s.substr(start, length))) {
        ways[end] = (ways[end] + ways[start]) % mod;
      }
    }
  }
  cout << ways[s.size()] << '\n';
}
```

时间 $O(nL^2)$，空间 $O(n+\sum|word|)$。字典词互异，避免同一个切分被重复计数。

## 变种三：使用最少单词完成拆分

新定义：可拆分时求最少词数，否则输出 -1。状态从布尔值升级为最短路距离，每条匹配单词的边代价为 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int count;
  cin >> s >> count;
  unordered_set<string> dictionary;
  int maximumLength = 0;
  while (count--) {
    string word;
    cin >> word;
    maximumLength = max(maximumLength, static_cast<int>(word.size()));
    dictionary.insert(word);
  }
  const int infinity = 1e9;
  vector<int> minimumWords(s.size() + 1, infinity);
  minimumWords[0] = 0;
  for (int end = 1; end <= static_cast<int>(s.size()); ++end) {
    for (int length = 1; length <= maximumLength && length <= end; ++length) {
      int start = end - length;
      if (dictionary.count(s.substr(start, length))) {
        minimumWords[end] = min(minimumWords[end], minimumWords[start] + 1);
      }
    }
  }
  cout << (minimumWords[s.size()] == infinity ? -1 : minimumWords[s.size()]) << '\n';
}
```

时间 $O(nL^2)$，空间 $O(n+\sum|word|)$。

## 变种四：同一字典处理多次查询

新定义：字典固定，有 $Q$ 个字符串需要判断。Trie 只构建一次，每个查询独立运行可达 DP，避免重复哈希与建树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  array<int, 26> next;
  bool terminal = false;
  Node() {
    next.fill(-1);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int wordCount, queryCount;
  cin >> wordCount >> queryCount;
  vector<Node> trie(1);
  while (wordCount--) {
    string word;
    cin >> word;
    int node = 0;
    for (char character : word) {
      int letter = character - 'a';
      if (trie[node].next[letter] == -1) {
        trie[node].next[letter] = trie.size();
        trie.emplace_back();
      }
      node = trie[node].next[letter];
    }
    trie[node].terminal = true;
  }
  while (queryCount--) {
    string s;
    cin >> s;
    vector<char> reachable(s.size() + 1);
    reachable[0] = true;
    for (int start = 0; start < static_cast<int>(s.size()); ++start) {
      if (!reachable[start]) {
        continue;
      }
      int node = 0;
      for (int end = start; end < static_cast<int>(s.size()); ++end) {
        node = trie[node].next[s[end] - 'a'];
        if (node == -1) {
          break;
        }
        reachable[end + 1] |= trie[node].terminal;
      }
    }
    cout << (reachable[s.size()] ? "YES" : "NO") << '\n';
  }
}
```

建树 $O(\sum|word|)$；每个长度为 $n_q$ 的查询耗时 $O(n_qL)$、空间 $O(n_q)$。

## 验证说明

本轮将七段代码按 C++23 编译；Trie 解会与指数递归在随机短串与随机字典上对拍，并复核三个官方样例、单字符、重复使用同一词、多个共享前缀和“前缀可达但末尾不可达”的边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/word-break/)
- [对应知识专题](../../dp/string-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-81-lc31/">← [力扣 Top 81] LC 31 下一个排列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-83-lc13/">[力扣 Top 83] LC 13 罗马数字转整数 简单 →</a>
</nav>
