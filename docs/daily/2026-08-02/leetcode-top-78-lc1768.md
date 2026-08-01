---
title: "[力扣 Top 78] LC 1768 交替合并字符串 简单"
---

# [力扣 Top 78] LC 1768 交替合并字符串 简单

<p class="daily-archive-kicker">2026-08-02 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=eda1f4d8ac90658b019109ffc5b2a1d34fced03598877a54f5cd81d505607989 -->
## 官方原始信息

- Top 排名：78
- 题号：LC 1768
- 官方中文标题：交替合并字符串
- 官方难度：简单
- 官方链接：[交替合并字符串](https://leetcode.cn/problems/merge-strings-alternately/)

### 原始题意

从 `word1` 开始，交替取 `word1`、`word2` 的下一个字符；某个字符串耗尽后，把另一个字符串的剩余字符追加到末尾，返回合并结果。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string mergeAlternately(string word1, string word2);
};
```

### 全部官方样例

```text
输入：word1 = "abc", word2 = "pqr"
输出："apbqcr"
```

```text
输入：word1 = "ab", word2 = "pqrs"
输出："apbqrs"
解释：word2 多出的 "rs" 追加到末尾。
```

```text
输入：word1 = "abcd", word2 = "pq"
输出："apbqcd"
解释：word1 多出的 "cd" 追加到末尾。
```

### 全部约束

- $1\le |word1|,|word2|\le100$。
- 两个字符串只含小写英文字母。

## 约束推导与不变量

输出长度固定为两串长度之和，每个字符恰好复制一次，因此最优时间下界是 $O(|word1|+|word2|)$。按共同下标 $i$ 扫描：若 `word1[i]` 存在先追加它，若 `word2[i]` 存在再追加它。这样无需为“共同前缀”和“剩余后缀”写两套循环。

预先 `reserve` 总长度可避免动态扩容，但不改变渐进复杂度。下标使用 `size_t` 与字符串长度类型一致，不涉及溢出。

## 解法递进

### 解法一：先处理共同长度，再追加后缀

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string mergeAlternately(string word1, string word2) {
    string answer;
    int common = min(word1.size(), word2.size());
    for (int i = 0; i < common; ++i) {
      answer.push_back(word1[i]);
      answer.push_back(word2[i]);
    }
    answer += word1.substr(common);
    answer += word2.substr(common);
    return answer;
  }
};
```

时间 $O(|word1|+|word2|)$，输出外额外空间 $O(1)$。它正确，但共同段与后缀有不同控制流。

### 最佳实用解：统一下标扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string mergeAlternately(string word1, string word2) {
    string answer;
    answer.reserve(word1.size() + word2.size());
    size_t length = max(word1.size(), word2.size());
    for (size_t i = 0; i < length; ++i) {
      if (i < word1.size()) {
        answer.push_back(word1[i]);
      }
      if (i < word2.size()) {
        answer.push_back(word2[i]);
      }
    }
    return answer;
  }
};
```

时间 $O(|word1|+|word2|)$，返回值本身占 $O(|word1|+|word2|)$；除此之外只用常数空间。

## 正确性证明

对循环下标 $i$ 归纳。处理前 $i$ 轮后，`answer` 恰好是两串前 $i$ 个字符按 `word1`、`word2` 顺序交替形成的序列，其中越过某串长度的字符自然缺席。第 $i$ 轮先追加存在的 `word1[i]`，再追加存在的 `word2[i]`，正好扩展到前 $i+1$ 个字符并保持规定顺序。循环到两串最大长度时，每个字符都恰好被追加一次，较长串的剩余字符也按原序位于末尾，答案正确。

## 样例手推

`abc` 与 `pqr` 的三轮分别追加 `ap`、`bq`、`cr`。`ab` 与 `pqrs` 的前两轮得到 `apbq`，随后 `word1` 已耗尽，只追加 `r`、`s`，得到 `apbqrs`。

## 易错点与方案比较

- 每轮必须从 `word1` 开始，不能交换追加顺序。
- 循环上界是较长字符串长度；每次访问前独立判断该串是否还有字符。
- 不要在一个字符串结束时提前退出，否则会丢失另一串后缀。
- 两种主解同阶；统一扫描分支少、自然推广到多串，推荐优先记忆。

## 变种一：指定由第二个字符串先开始

新定义：每轮顺序改为 `word2` 再 `word1`。只交换两次条件追加的顺序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string first, second;
  cin >> first >> second;
  string answer;
  for (size_t i = 0; i < max(first.size(), second.size()); ++i) {
    if (i < second.size()) {
      answer.push_back(second[i]);
    }
    if (i < first.size()) {
      answer.push_back(first[i]);
    }
  }
  cout << answer << '\n';
}
```

时间与输出空间均为 $O(|first|+|second|)$。

## 变种二：每次从一串取 $k$ 个字符

新定义：按块交替，先从第一串取至多 $k$ 个，再从第二串取至多 $k$ 个，直到两串耗尽。状态变成两个独立读指针。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string first, second;
  int block;
  cin >> first >> second >> block;
  string answer;
  size_t i = 0;
  size_t j = 0;
  while (i < first.size() || j < second.size()) {
    for (int used = 0; used < block && i < first.size(); ++used) {
      answer.push_back(first[i++]);
    }
    for (int used = 0; used < block && j < second.size(); ++used) {
      answer.push_back(second[j++]);
    }
  }
  cout << answer << '\n';
}
```

时间 $O(|first|+|second|)$，输出外空间 $O(1)$。

## 变种三：轮转合并 $q$ 个字符串

新定义：每轮按输入顺序从每个尚未耗尽的字符串取一个字符。维护每串当前位置，直到一轮没有输出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int count;
  cin >> count;
  vector<string> words(count);
  vector<size_t> position(count);
  for (string& word : words) {
    cin >> word;
  }
  string answer;
  while (true) {
    bool changed = false;
    for (int i = 0; i < count; ++i) {
      if (position[i] < words[i].size()) {
        answer.push_back(words[i][position[i]++]);
        changed = true;
      }
    }
    if (!changed) {
      break;
    }
  }
  cout << answer << '\n';
}
```

若总字符数为 $L$，时间 $O(L+q\cdot R)$，其中 $R$ 为最长串长度；空间 $O(q)$。

## 变种四：不构造结果，直接流式输出

新定义：结果可能很大，只需写入输出流。仍保持两个读指针，但省去完整结果缓冲。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string first, second;
  cin >> first >> second;
  for (size_t i = 0; i < max(first.size(), second.size()); ++i) {
    if (i < first.size()) {
      cout.put(first[i]);
    }
    if (i < second.size()) {
      cout.put(second[i]);
    }
  }
  cout.put('\n');
}
```

时间 $O(|first|+|second|)$，除输入外额外空间 $O(1)$；若输入本身也是字符流，可进一步只保留各流当前字符。

## 验证说明

统一扫描与共同前缀法对 10000 对随机小写字符串逐项比较，覆盖长度相等、悬殊与单字符输入；六段 C++23 代码均通过编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/merge-strings-alternately/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-77-lc221/">← [力扣 Top 77] LC 221 最大正方形 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-79-lc208/">[力扣 Top 79] LC 208 实现 Trie (前缀树) 中等 →</a>
</nav>
