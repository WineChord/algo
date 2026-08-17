---
title: "[codeforces] CF Round 1117 Div.2 A Creating Abbreviations"
---

# [codeforces] CF Round 1117 Div.2 A Creating Abbreviations

<p class="daily-archive-kicker">2026-08-18 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-18 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=70fe73f9661e785a8e8bba2f8ec4b274f067227628784d358dfae6d3c4a548db -->
[Official problem: Codeforces Round 1117 (Div. 2), A — Creating Abbreviations](https://codeforces.com/contest/2257/problem/A?locale=en)

## 官方来源与元数据

- 比赛 ID：2257；正式比赛名：Codeforces Round 1117 (Div. 2)。
- 题目：Div.2 A — Creating Abbreviations，没有跨组别别名。
- 官方分值：500；官方当前未给出 problem rating。
- 官方标签：`brute force`、`strings`，核对于 2026-08-18 的实时官方 API。
- 时间限制：1 秒；内存限制：256 MB。
- 题面没有理解所必需的图片。

下方是 Codeforces 官方英文题面的自包含呈现，并就近保留官方来源与许可链接。

## Complete English statement

You initially have a set $S$ containing $n$ lowercase English words. You then want to perform $m$
operations. In one operation, choose a non-empty sequence of words currently belonging to $S$; the
same word may be chosen more than once. Form an abbreviation by concatenating the first letter of each
chosen word, converted to uppercase, and add the resulting word to $S$. A word created earlier may be
used in a later operation.

For example, choosing `birch`, `OAK`, `birch`, and `redwood` in that order creates the abbreviation
`BOBR`.

You are given the $n$ original words and all $m$ abbreviations that should be created, but the listed
order of those abbreviations does not have to be their creation order. Determine whether there exists
some ordering in which every requested abbreviation can be created.

### Input

The first line contains the number of test cases $t$ ($1\le t\le500$). Each test case has the following
form:

```text
n m
w_1
w_2
...
w_n
a_1
a_2
...
a_m
```

Here $1\le n,m\le100$. Each $w_i$ is a lowercase English string and each $a_i$ is an uppercase
English string. Every string has length from 1 through 20, and all $n+m$ strings in a test case are
pairwise distinct. The sum of the lengths of all strings over all test cases does not exceed 50000.

### Constraints

- $1\le t\le500$.
- $1\le n,m\le100$ in every test case.
- Every $w_i$ consists only of lowercase English letters.
- Every $a_i$ consists only of uppercase English letters.
- Every input string has length from 1 through 20.
- All $n+m$ strings in one test case are pairwise distinct.
- The sum of all input-string lengths over all test cases does not exceed 50000.

### Output

For each test case, print `YES` if a suitable creation order exists, or `NO` otherwise. Any mixture of
uppercase and lowercase letters in these two answers is accepted.

### Official sample

```text
Input
4
6 4
apple
grand
banana
great
cherry
good
AG
BG
CG
ABC
1 1
apple
AA
1 2
apple
A
AA
2 2
apple
avocado
B
BA

Output
YES
YES
YES
NO
```

In the first test case, one suitable order is `AG`, `BG`, `CG`, then `ABC`: use `apple` with `grand`,
`banana` with `great`, and `cherry` with `good` for the first three, then use `AG`, `BG`, and `CG`
for `ABC`. In the second case, `apple` may be used twice to form `AA`. In the third case, first form
`A` from `apple`, then use `apple` together with the new word `A` to form `AA`. In the fourth case no
suitable order exists.

Statement source: [Codeforces problem 2257A](https://codeforces.com/contest/2257/problem/A?locale=en).
Codeforces permits this public, non-judge presentation under its
[materials usage license v0.1](https://codeforces.com/page/254); see also the
[official materials notice](https://codeforces.com/blog/entry/967?locale=en).

## 中文解释与题解

初始集合中有若干小写单词。每次可以选任意多个当前已有单词，按顺序取它们的首字母组成
一个大写缩写，再把缩写加入集合；同一个单词允许重复选。给定所有目标缩写，问是否存在
某种生成顺序。

## 约束推导与首字母不变量

表面看像拓扑排序：新缩写可以成为后续缩写的原料，似乎应搜索生成顺序。但一次生成操作
真正关心的只有“集合里目前有哪些首字母”。设可用首字母集合为 $C$。

若缩写 $a=a_1a_2\cdots a_k$ 能被生成，则它的每个字符 $a_i$ 都已经属于 $C$。把 $a$
加入集合后，唯一新增单词的首字母是 $a_1$，而 $a_1$ 本来就是生成它所需的字符之一，
因此仍属于原来的 $C$。所以任何操作都不能扩大可用首字母集合：

$$
C_{\text{after}}=C_{\text{before}}=C_{\text{initial}}.
$$

于是顺序完全无关。一个目标缩写可生成，当且仅当它的每个字符都是某个初始单词的首字母；
若成立，甚至可以直接对每个字符选一个对应的初始单词来构造它。字母表只有 26 个字符，
用位掩码或布尔数组即可。总字符串长度不超过 50000，线性扫描最优；没有整数溢出风险。

## 样例手推与边界

样例 1 的初始首字母集合为 `{A,B,C,G}`。`AG`、`BG`、`CG`、`ABC` 的所有字符都在
集合中，所以四个目标都可直接生成；题面给出的顺序只是一个可行示例，并非必须依赖前面
缩写才获得新字母。

样例 4 的初始首字母只有 `A`。目标 `B` 含不可用字母 B，任何先前操作都无法创造新的首
字母种类，因此 `B` 和 `BA` 不可能全部生成。

- 同一单词可重复使用，所以 `apple` 足以直接生成任意长度的 `AAAA...A`。
- 长度为 1 的缩写仍要检查该字母是否为初始首字母。
- 多个初始单词首字母相同只提供同一种能力；频次在原题中无关。
- 某个目标缩写的首字母可用、但后续字符不可用：仍然失败，必须检查全部字符。
- 目标给出的顺序与答案无关，也不需要真的把可行缩写加入数据结构。

## 解法一：枚举目标生成顺序

递归尝试尚未生成的每个缩写。判断某个缩写能否生成时，扫描当前集合中所有单词的首字母；
可生成就临时加入集合并继续。它会覆盖所有 $m!$ 种顺序，因而正确，但复杂度最坏为
$O(m!\,mL)$，只适合极小实例和作为 oracle。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool canCreate(const string& target, const vector<string>& words) {
  array<bool, 26> available{};
  for (const string& word : words) {
    available[toupper(static_cast<unsigned char>(word.front())) - 'A'] = true;
  }
  for (char letter : target) {
    if (!available[letter - 'A']) return false;
  }
  return true;
}
bool search(const vector<string>& targets, vector<bool>& used, vector<string>& words,
            int created) {
  if (created == static_cast<int>(targets.size())) return true;
  for (int i = 0; i < static_cast<int>(targets.size()); ++i) {
    if (used[i] || !canCreate(targets[i], words)) continue;
    used[i] = true;
    words.push_back(targets[i]);
    if (search(targets, used, words, created + 1)) return true;
    words.pop_back();
    used[i] = false;
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    vector<string> words(n);
    vector<string> targets(m);
    for (string& word : words) cin >> word;
    for (string& target : targets) cin >> target;
    vector<bool> used(m);
    cout << (search(targets, used, words, 0) ? "YES\n" : "NO\n");
  }
  return 0;
}
```

额外空间为 $O(n+m)$ 加递归栈。瓶颈是枚举了其实不会改变首字母能力的所有顺序。

## 从顺序搜索到闭包不变量

若只做普通优化，可以反复扫描所有未完成目标，把当前可生成者加入集合，直到没有变化；
这类似拓扑排序，复杂度约为 $O(m^2L)$。但检查一次更新会发现：新词的首字母就是其缩写
第一个字符，而这个字符若不可用，缩写根本无法生成；若可生成，它早已在集合中。

因此“闭包扩张”从第一轮开始就不会发生。所有目标共享同一个固定判定条件，只需检查初始
首字母掩码。

## 最佳实用解：26 位首字母掩码

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    int n, m;
    cin >> n >> m;
    unsigned int available = 0;
    for (int i = 0; i < n; ++i) {
      string word;
      cin >> word;
      available |= 1U << (word.front() - 'a');
    }
    bool possible = true;
    for (int i = 0; i < m; ++i) {
      string abbreviation;
      cin >> abbreviation;
      for (char letter : abbreviation) {
        if ((available & (1U << (letter - 'A'))) == 0) possible = false;
      }
    }
    cout << (possible ? "YES\n" : "NO\n");
  }
  return 0;
}
```

时间复杂度是 $O(T)$，其中 $T$ 为输入全部字符串的总长度；额外空间 $O(1)$。任何算法都
必须读取每个目标字符以发现潜在的不可用字母，因此渐近最优。

### 正确性证明

必要性：设目标缩写中的某个字符 $c$ 不在初始首字母集合。假设第一次有某个操作让首字母
$c$ 可用，那么新加入缩写的第一个字符必须是 $c$；但生成这个缩写时已经需要选择一个首
字母为 $c$ 的旧单词，和“第一次”矛盾。因此 $c$ 永远不可用，该目标无法生成。

充分性：若目标缩写的每个字符都在初始集合中，就为每个字符任选一个对应首字母的初始单词，
按字符顺序排列这些单词；允许重复使用，所以总能直接得到该缩写。对每个目标分别如此构造，
即可按任意顺序完成全部操作。算法恰好检查这个必要充分条件，所以输出正确。

## 同阶方案比较

使用 `array<bool,26>` 与位掩码都为 $O(T)$ 时间、$O(1)$ 空间。布尔数组更直白，位掩码
更紧凑，并能用一次按位运算检查预先汇总的字符集合。当前代码逐字符读取，既简单又能处理
总长度约束。竞赛中优先记忆“不变量先于拓扑排序”，容器选择只是次要实现细节。

## 易错点

- 误以为生成缩写会带来新的首字母种类，从而编写不必要的拓扑排序。
- 只检查缩写的第一个字符；后续每个字符也必须对应一个可选单词。
- 忘记原题允许同一单词重复使用，错误地按首字母频次限制重复字符。
- 大小写映射错位；初始词为小写、目标缩写为大写，位号都应归一到 0 到 25。
- 把缓存中的短暂元数据当成稳定事实；应以发布前实时官方 API 的 `brute force`、
  `strings` 标签为准。

## 验证说明

暴力顺序搜索和位掩码解均以 GNU++23 编译并通过全部官方样例。另对小字母表中的初始词
首字母集合与短缩写集合做穷举，以完整顺序回溯为 oracle；再对官方总长度范围内的随机实例
差分，结果一致。

## 变种一：输出每个缩写的构造见证

新定义：可行时，为目标中的每个字符输出一个可选初始单词编号。给每个字母保存任意一个
代表下标，逐字符输出即可。时间 $O(T)$，空间 $O(26)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  array<int, 26> representative;
  representative.fill(-1);
  for (int i = 1; i <= n; ++i) {
    string word;
    cin >> word;
    representative[word.front() - 'a'] = i;
  }
  vector<string> targets(m);
  for (string& target : targets) cin >> target;
  for (const string& target : targets) {
    for (char letter : target) {
      if (representative[letter - 'A'] == -1) {
        cout << "NO\n";
        return 0;
      }
    }
  }
  cout << "YES\n";
  for (const string& target : targets) {
    for (char letter : target) cout << representative[letter - 'A'] << ' ';
    cout << '\n';
  }
  return 0;
}
```

## 变种二：一次操作内不允许重复使用同一单词

新定义：构造一个缩写时，同一个现有单词最多选一次；不同操作之间仍可再次使用。此时字母
频次变得重要。一个目标可生成，当且仅当每个字母的需求量不超过当前以该字母开头的单词数；
成功后新增一个以目标首字母开头的单词。能力只会增加，反复选择任意当前可行目标即可。
复杂度 $O(m^2L)$，空间 $O(m)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  array<int, 26> available{};
  for (int i = 0; i < n; ++i) {
    string word;
    cin >> word;
    ++available[word.front() - 'a'];
  }
  vector<string> targets(m);
  for (string& target : targets) cin >> target;
  vector<bool> created(m);
  int completed = 0;
  while (true) {
    bool changed = false;
    for (int i = 0; i < m; ++i) {
      if (created[i]) continue;
      array<int, 26> needed{};
      for (char letter : targets[i]) ++needed[letter - 'A'];
      bool possible = true;
      for (int letter = 0; letter < 26; ++letter) {
        if (needed[letter] > available[letter]) possible = false;
      }
      if (!possible) continue;
      created[i] = true;
      ++completed;
      ++available[targets[i].front() - 'A'];
      changed = true;
    }
    if (!changed) break;
  }
  cout << (completed == m ? "YES\n" : "NO\n");
  return 0;
}
```

## 变种三：初始单词支持在线增删与询问

新定义：动态加入或删除初始单词，并询问某个缩写当前能否直接生成；删除操作保证对应单词
当前存在。维护 26 个首字母频次；增删为 $O(1)$，询问为 $O(|a|)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queryCount;
  cin >> queryCount;
  array<int, 26> count{};
  while (queryCount--) {
    char type;
    string word;
    cin >> type >> word;
    int letter = tolower(static_cast<unsigned char>(word.front())) - 'a';
    if (type == '+') ++count[letter];
    else if (type == '-') --count[letter];
    else {
      bool possible = true;
      for (char ch : word) {
        int index = tolower(static_cast<unsigned char>(ch)) - 'a';
        if (count[index] == 0) possible = false;
      }
      cout << (possible ? "YES\n" : "NO\n");
    }
  }
  return 0;
}
```

## 变种四：统计固定长度的可生成缩写数

新定义：给定正整数长度 $L$，问有多少个不同的大写字符串可由初始单词生成，答案对
$10^9+7$ 取模。设可用首字母种类数为 $c$。每个位置独立选择一种首字母，重复允许，
所以答案为 $c^L$。快速幂时间 $O(\log L)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  int n;
  long long length;
  cin >> n >> length;
  array<bool, 26> available{};
  for (int i = 0; i < n; ++i) {
    string word;
    cin >> word;
    available[word.front() - 'a'] = true;
  }
  long long base = count(available.begin(), available.end(), true);
  long long answer = 1;
  while (length > 0) {
    if (length & 1LL) answer = answer * base % mod;
    base = base * base % mod;
    length >>= 1;
  }
  cout << answer << '\n';
  return 0;
}
```

## 来源

- [Codeforces 官方题面](https://codeforces.com/contest/2257/problem/A?locale=en)
- [Codeforces Round 1117 官方比赛页](https://codeforces.com/contest/2257)
- [Codeforces materials usage license v0.1](https://codeforces.com/page/254)
- [Codeforces 官方 API](https://codeforces.com/api/contest.standings?contestId=2257)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/A?locale=en)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-515-q1-lc4024/">← [力扣竞赛] 第 515 场周赛 Q1 LC 4024 最近的可用无人机 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-18-lc3471/">[力扣每日一题] 2026-08-18｜LC 3471 找出最大的几近缺失整数 →</a>
</nav>
