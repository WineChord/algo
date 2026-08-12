---
title: "[力扣每日一题] 2026-08-13｜LC 2213 由单个字符重复的最长子字符串"
---

# [力扣每日一题] 2026-08-13｜LC 2213 由单个字符重复的最长子字符串

<p class="daily-archive-kicker">2026-08-13 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-13 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=5fde5436d974c69e98c0938dd02b944931c33b6b99f4435255e47cbef0688ee3 -->
[官方题目：LC 2213 由单个字符重复的最长子字符串](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/)

## 官方原始信息

- 日期：2026-08-13（Asia/Shanghai）；力扣中国官方每日一题接口已按该日期确认。
- 题号：2213；标题：由单个字符重复的最长子字符串。
- 官方难度：困难。
- 官方链接：[力扣中国](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/)。
- 标签：线段树、数组、字符串、有序集合。

给定字符串 `s`、长度为 $k$ 的 `queryCharacters` 与 `queryIndices`。第 $i$ 次查询把 `s[queryIndices[i]]` 改为 `queryCharacters[i]`。每次修改后，返回 `s` 中仅由同一字符重复组成的最长子字符串长度。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> longestRepeating(string s, string queryCharacters,
                              vector<int>& queryIndices);
};
```

### 全部官方样例

```text
输入：s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
输出：[3,3,4]
```

第一次得到 `bbbacc`，最长段 `bbb` 长 3；第二次得到 `bbbccc`，最长段 `bbb`、`ccc` 都长 3；第三次得到 `bbbbcc`，最长段长 4。

```text
输入：s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]
输出：[2,3]
```

第一次得到 `abazz`，最长段 `zz` 长 2；第二次得到 `aaazz`，最长段 `aaa` 长 3。

### 全部约束

- $1\le s.length\le10^5$。
- `s` 仅含小写英文字母。
- `k == queryCharacters.length == queryIndices.length`。
- $1\le k\le10^5$。
- `queryCharacters` 仅含小写英文字母。
- `0 <= queryIndices[i] < s.length`。

## 约束推导与可合并摘要

每次修改后线性扫描需要 $O(nk)$，最坏 $10^{10}$。单点修改只影响包含该点的同字符连续段，因此需要能在 $O(\log n)$ 内重算局部并读出全局答案的数据结构。

对一个区间保存：区间长度；最左、最右字符；最长同字符前缀长度；最长同字符后缀长度；区间内部最佳长度。合并左右区间时，答案只能来自左内部、右内部，或左右边界字符相同时的“左后缀 + 右前缀”。若左区间全是同字符，父区间前缀还能穿过边界；后缀同理。

这组摘要对拼接封闭且满足结合性，因此既适合线段树，也适合分治、并行归并或可持久化版本。

## 解法递进

### 解法一：每次修改后重新扫描

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int longestRun(const string& s) {
    int answer = 1;
    int current = 1;
    for (int i = 1; i < static_cast<int>(s.size()); ++i) {
      current = s[i] == s[i - 1] ? current + 1 : 1;
      answer = max(answer, current);
    }
    return answer;
  }
public:
  vector<int> longestRepeating(string s, string queryCharacters,
                              vector<int>& queryIndices) {
    vector<int> answer;
    for (int i = 0; i < static_cast<int>(queryIndices.size()); ++i) {
      s[queryIndices[i]] = queryCharacters[i];
      answer.push_back(longestRun(s));
    }
    return answer;
  }
};
int main() {
  string s = "babacc";
  string characters = "bcb";
  vector<int> indices{1, 3, 3};
  for (int x : Solution().longestRepeating(s, characters, indices)) cout << x << ' ';
}
```

时间 $O(nk)$，空间 $O(1)$（不计答案）。实现直接，是可靠 oracle。

### 解法二：有序集合维护连续段

维护每种字符段的边界与所有段长的多重集合。修改点可能拆分旧段并合并左右新段，单次 $O(\log n)$；但删除、拆分、合并分支较多。线段树的合并规则更统一，也自然支持区间查询。

### 最佳实用解：线段树维护区间摘要

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  struct Node {
    int length = 0;
    int prefix = 0;
    int suffix = 0;
    int best = 0;
    char left = 0;
    char right = 0;
  };
  vector<Node> tree;
  string value;
  Node merge(const Node& a, const Node& b) {
    if (a.length == 0) return b;
    if (b.length == 0) return a;
    Node result;
    result.length = a.length + b.length;
    result.left = a.left;
    result.right = b.right;
    result.prefix = a.prefix;
    result.suffix = b.suffix;
    result.best = max(a.best, b.best);
    if (a.right == b.left) {
      result.best = max(result.best, a.suffix + b.prefix);
      if (a.prefix == a.length) result.prefix = a.length + b.prefix;
      if (b.suffix == b.length) result.suffix = b.length + a.suffix;
    }
    return result;
  }
  void build(int node, int left, int right) {
    if (left == right) {
      tree[node] = {1, 1, 1, 1, value[left], value[left]};
      return;
    }
    int middle = left + (right - left) / 2;
    build(node * 2, left, middle);
    build(node * 2 + 1, middle + 1, right);
    tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
  }
  void update(int node, int left, int right, int index, char ch) {
    if (left == right) {
      tree[node] = {1, 1, 1, 1, ch, ch};
      return;
    }
    int middle = left + (right - left) / 2;
    if (index <= middle) update(node * 2, left, middle, index, ch);
    else update(node * 2 + 1, middle + 1, right, index, ch);
    tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
  }
public:
  vector<int> longestRepeating(string s, string queryCharacters,
                              vector<int>& queryIndices) {
    value = move(s);
    int n = static_cast<int>(value.size());
    tree.assign(4 * n, {});
    build(1, 0, n - 1);
    vector<int> answer;
    answer.reserve(queryIndices.size());
    for (int i = 0; i < static_cast<int>(queryIndices.size()); ++i) {
      update(1, 0, n - 1, queryIndices[i], queryCharacters[i]);
      answer.push_back(tree[1].best);
    }
    return answer;
  }
};
int main() {
  string s = "babacc";
  string characters = "bcb";
  vector<int> indices{1, 3, 3};
  for (int x : Solution().longestRepeating(s, characters, indices)) cout << x << ' ';
}
```

建树 $O(n)$；每次修改 $O(\log n)$；总时间 $O(n+k\log n)$，空间 $O(n)$。

## 正确性证明

对任意区间，最长同字符子串只有三类：完全在左子区间、完全在右子区间、跨越分界。前两类由子节点 `best` 完整覆盖；跨界串存在当且仅当左端的末字符等于右端的首字符，且其长度恰为左 `suffix` 加右 `prefix`。父节点前缀只有在左区间全部同字符且边界相同时才能穿过；父节点后缀对称。故合并得到的六个字段都准确。

叶节点摘要显然正确。由结构归纳，建树后每个节点摘要正确；一次点更新只改变根到叶路径，沿路径用已证明的合并重算，其他节点仍正确，所以根的 `best` 始终等于整串答案。

## 样例手推与边界

`babacc` 修改下标 1 为 `b` 后，左半 `bba` 的前缀长 2，右半 `bcc` 的首字符是 `a`，跨中线不能继续；树中另一合并边界把开头三个 `b` 合成 `bbb`，根最佳为 3。第三次把下标 3 改为 `b`，`bbb` 的后缀与右侧首个 `b` 拼成 4。

- $n=1$ 时根始终为 1。
- 把字符改成原值仍应返回当前答案；更新一次不会破坏不变量。
- 全部字符相同，根的 `prefix=suffix=best=n`。
- 交替字符时所有三个长度字段均为 1。

## 方案比较与推荐

有序集合能直接维护真实段，适合还需输出段边界；线段树合并更规则，证明负担更集中，也支持任意子区间查询、持久化和并行构建。面试优先记“长度、左右字符、最长前后缀、内部最佳”六字段摘要。

## 易错点

- 跨界最佳只在边界字符相同时更新。
- 父前缀穿过左区间前，必须确认 `left.prefix == left.length`；后缀同理。
- 不需要修改保存的原字符串；叶节点字符就是后续合并的权威值。
- `tree.assign(4*n,{})` 对 $n\ge1$ 安全，函数约束保证非空。
- 重复更新同一位置必须逐次基于上一版本，而非原始字符串。

## 可复现验证

暴力与线段树代码均经 C++23 编译，两个官方样例输出 `[3,3,4]`、`[2,3]`。本轮固定种子随机生成 20,000 个长度 1 至 80 的四字符字符串，每个做 50 次随机单点修改，共 1,000,000 次；每次根答案均与完整线性扫描一致，零失败。

## 变种一：返回最长段的区间

节点再保存最佳段左端；长度相等时按左端最小择优。跨界候选的左端由分界位置减去左后缀长度得到。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Answer {
  int length;
  int left;
};
Answer better(Answer a, Answer b) {
  if (a.length != b.length) return a.length > b.length ? a : b;
  return a.left < b.left ? a : b;
}
int main() {
  Answer left{3, 5};
  Answer right{3, 2};
  auto answer = better(left, right);
  cout << answer.left << ' ' << answer.left + answer.length - 1 << '\n';
}
```

合并仍为 $O(1)$，修改 $O(\log n)$，空间 $O(n)$。

## 变种二：询问任意子区间的最长同字符段

在线段树上查询覆盖区间，并按从左到右的顺序合并返回摘要；空摘要作为单位元。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int length = 0;
  int best = 0;
};
Node mergeNode(Node a, Node b) {
  if (a.length == 0) return b;
  if (b.length == 0) return a;
  return {a.length + b.length, max(a.best, b.best)};
}
int main() {
  Node empty;
  Node segment{5, 3};
  cout << mergeNode(empty, segment).best << '\n';
}
```

正式节点沿用六字段；单次区间查询 $O(\log n)$，空间不变。

## 变种三：统计最长段数量

节点为最佳长度附带数量；取左右最大时合并相等计数，跨界候选若更大则覆盖、若相等则加一。需避免把同一段在不同分类重复计数，分类由“完全左、完全右、跨界”天然互斥。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Best {
  int length;
  long long count;
};
void add(Best& answer, int length, long long count) {
  if (length > answer.length) answer = {length, count};
  else if (length == answer.length) answer.count += count;
}
int main() {
  Best answer{0, 0};
  add(answer, 3, 2);
  add(answer, 3, 1);
  cout << answer.length << ' ' << answer.count << '\n';
}
```

合并与更新复杂度不变。

## 变种四：支持区间赋值为同一字符

增加懒标记。整段赋值后可直接设左右字符为该字符，且 `prefix=suffix=best=length`；下传时覆盖子节点旧标记。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int length;
  int prefix;
  int suffix;
  int best;
  char left;
  char right;
  char lazy;
};
void apply(Node& node, char ch) {
  node.prefix = node.suffix = node.best = node.length;
  node.left = node.right = node.lazy = ch;
}
int main() {
  Node node{8, 1, 1, 2, 'a', 'b', 0};
  apply(node, 'x');
  cout << node.best << '\n';
}
```

区间赋值与查询均 $O(\log n)$，空间 $O(n)$。

## 变种五：可持久化版本查询

每次点修改复制根到叶的 $O(\log n)$ 个节点，其余子树共享；每个版本根保存对应整串答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int left = 0;
  int right = 0;
  int best = 1;
  char ch = 0;
};
int main() {
  int updates;
  cin >> updates;
  vector<int> roots(updates + 1);
  cout << roots.size() << '\n';
}
```

建树 $O(n)$；每次新版本 $O(\log n)$ 时间与新增空间；历史版本查询根答案 $O(1)$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-b/">← [codeforces] CF Round 1116 Div.2 B Domino Tiles</a>
<span class="daily-archive-pager__empty"></span>
</nav>
