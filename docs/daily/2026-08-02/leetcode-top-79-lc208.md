---
title: "[力扣 Top 79] LC 208 实现 Trie (前缀树) 中等"
---

# [力扣 Top 79] LC 208 实现 Trie (前缀树) 中等

<p class="daily-archive-kicker">2026-08-02 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b8dae734bde594062253f3a8b4f1d1098fcf8cc316657532b131a69cb9c2ae72 -->
## 官方原始信息

- Top 排名：79
- 题号：LC 208
- 官方中文标题：实现 Trie (前缀树)
- 官方难度：中等
- 官方链接：[实现 Trie (前缀树)](https://leetcode.cn/problems/implement-trie-prefix-tree/)

### 原始题意

实现一个前缀树，支持初始化、插入单词、查询完整单词是否存在，以及查询是否存在以给定字符串开头的已插入单词。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Trie {
public:
  Trie();
  void insert(string word);
  bool search(string word);
  bool startsWith(string prefix);
};
```

### 全部官方样例

```text
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");
trie.search("app");     // 返回 true
```

### 全部约束

- $1\le word.length,prefix.length\le2000$。
- `word` 和 `prefix` 只含小写英文字母。
- 三种操作总调用次数不超过 $3\times10^4$。

## 约束推导与模型

若每次查询都扫描所有已插入单词，最坏需要比较约 $6\times10^7$ 个字符，而且重复前缀会被反复比较。Trie 把每个字符串看成从根出发的一条字符路径：共享前缀只存一次。一个结点是否可达回答 `startsWith`；结点的结束标记回答 `search`，二者不可混淆。

所有字符均为 `a` 到 `z`，因此每个结点可用长度 26 的数组保存儿子编号，省去哈希开销。设所有插入字符串的总长度为 $S$，结点数至多 $S+1$；单次操作只沿输入字符串走一遍，时间 $O(L)$。极端上界虽可达到 $6\times10^7$ 个字符，但在线测试的总输入受内存与数据规模共同限制；实现仍应避免为每个结点保存重量级对象。

## 解法递进

### 解法一：保存所有字符串并线性扫描

插入直接追加；完整查询比较相等，前缀查询逐字符比较。它覆盖所有情况，可作为小规模 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Trie {
  vector<string> words;
public:
  Trie() = default;
  void insert(string word) {
    words.push_back(move(word));
  }
  bool search(string word) {
    for (const string& stored : words) {
      if (stored == word) {
        return true;
      }
    }
    return false;
  }
  bool startsWith(string prefix) {
    for (const string& stored : words) {
      if (stored.size() >= prefix.size() && equal(prefix.begin(), prefix.end(), stored.begin())) {
        return true;
      }
    }
    return false;
  }
};
```

设已存字符串总长度为 $S$，插入时间 $O(L)$（保存字符串），查询最坏 $O(S)$，空间 $O(S)$。瓶颈是相同前缀被重复扫描。

### 最佳实用解：数组下标 Trie

用 `vector<array<int,26>>` 集中存储结点；`-1` 表示对应边不存在。插入时按需新建结点，查询共用一个 `walk` 函数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Trie {
  vector<array<int, 26>> next;
  vector<char> terminal;
  int walk(const string& text) const {
    int node = 0;
    for (char character : text) {
      int edge = character - 'a';
      if (next[node][edge] == -1) {
        return -1;
      }
      node = next[node][edge];
    }
    return node;
  }
  int newNode() {
    next.push_back({});
    next.back().fill(-1);
    terminal.push_back(false);
    return static_cast<int>(next.size()) - 1;
  }
public:
  Trie() {
    newNode();
  }
  void insert(string word) {
    int node = 0;
    for (char character : word) {
      int edge = character - 'a';
      if (next[node][edge] == -1) {
        next[node][edge] = newNode();
      }
      node = next[node][edge];
    }
    terminal[node] = true;
  }
  bool search(string word) {
    int node = walk(word);
    return node != -1 && terminal[node];
  }
  bool startsWith(string prefix) {
    return walk(prefix) != -1;
  }
};
```

每次操作时间 $O(L)$，总空间 $O(26S)$ 个整数的稠密上界。字母表固定且查询频繁时，数组版常数稳定；字符集稀疏而巨大时应换哈希边。

## 正确性证明

对任意已处理前缀长度 $k$，维护不变量：当前结点恰表示该字符串前 $k$ 个字符。根表示空前缀；处理下一个字符时，沿对应字符边前进或在插入时创建它，因此不变量归纳成立。

插入结束时，把完整路径末端标为终止结点，所以且仅所以某完整单词插入过，`search` 才返回真。`startsWith` 只要求整条前缀路径存在；任何已插入单词都会创建其所有前缀路径，反之可达结点至少来自某次插入路径，故前缀查询也精确。终止标记独立于路径存在性，因此 `apple` 不会使 `search("app")` 误判为真。

## 样例手推

插入 `apple` 后形成 `root→a→p→p→l→e`，仅 `e` 结点有结束标记。查询 `apple` 可达且末端有标记，返回真；查询 `app` 可达但末端未标记，返回假；前缀查询 `app` 只检查可达性，返回真。随后插入 `app`，同一路径无需新建结点，只把第二个 `p` 标成终止结点。

## 易错点与方案比较

- 路径存在不等于完整单词存在，必须保存 `terminal`。
- 新结点的 26 条边必须全部初始化为 `-1`。
- 重复插入不应破坏结构；基础题只需布尔终止标记。
- 用指针逐个 `new` 容易产生碎片；数组下标更适合竞赛实现。
- `unordered_map` 支持大字符集，但本题固定 26 个字符，数组更快、更稳定，推荐优先记忆数组版。

## 变种一：支持重复单词与删除

新定义：同一单词可插入多次；删除一次只减少一次计数。每个结点保存经过次数 `pass` 和结束次数 `end`。删除前先确认存在，再沿路径减计数；当子树经过次数降为 0 时可断开父边。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  array<int, 26> next;
  int pass = 0;
  int end = 0;
  Node() {
    next.fill(-1);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  vector<Node> trie(1);
  auto find = [&](const string& word) {
    int node = 0;
    for (char character : word) {
      int edge = character - 'a';
      if (trie[node].next[edge] == -1) {
        return -1;
      }
      node = trie[node].next[edge];
    }
    return node;
  };
  int queries;
  cin >> queries;
  while (queries--) {
    string operation, word;
    cin >> operation >> word;
    if (operation == "insert") {
      int node = 0;
      for (char character : word) {
        int edge = character - 'a';
        if (trie[node].next[edge] == -1) {
          trie[node].next[edge] = trie.size();
          trie.emplace_back();
        }
        node = trie[node].next[edge];
        ++trie[node].pass;
      }
      ++trie[node].end;
    } else if (operation == "erase") {
      int last = find(word);
      if (last == -1 || trie[last].end == 0) {
        continue;
      }
      vector<pair<int, int>> path;
      int node = 0;
      for (char character : word) {
        int edge = character - 'a';
        path.push_back({node, edge});
        node = trie[node].next[edge];
      }
      --trie[last].end;
      for (int index = path.size() - 1; index >= 0; --index) {
        int parent = path[index].first;
        int edge = path[index].second;
        int child = trie[parent].next[edge];
        --trie[child].pass;
        if (trie[child].pass == 0) {
          trie[parent].next[edge] = -1;
        }
      }
    } else {
      int node = find(word);
      cout << (node == -1 ? 0 : trie[node].end) << '\n';
    }
  }
}
```

每次操作 $O(L)$，空间 $O(S)$ 个结点；断边后结点槽位未复用，但逻辑已释放。

## 变种二：统计具有给定前缀的单词数

新定义：查询有多少次插入以某前缀开头。插入时把路径上每个结点的 `pass` 加一，查询到前缀末端直接返回其计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  array<int, 26> next;
  int pass = 0;
  Node() {
    next.fill(-1);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  vector<Node> trie(1);
  int queries;
  cin >> queries;
  while (queries--) {
    string operation, text;
    cin >> operation >> text;
    if (operation == "insert") {
      int node = 0;
      for (char character : text) {
        int edge = character - 'a';
        if (trie[node].next[edge] == -1) {
          trie[node].next[edge] = trie.size();
          trie.emplace_back();
        }
        node = trie[node].next[edge];
        ++trie[node].pass;
      }
    } else {
      int node = 0;
      for (char character : text) {
        int edge = character - 'a';
        node = trie[node].next[edge];
        if (node == -1) {
          break;
        }
      }
      cout << (node == -1 ? 0 : trie[node].pass) << '\n';
    }
  }
}
```

插入和查询均为 $O(L)$，空间 $O(S)$。

## 变种三：单词查询允许通配符点号

新定义：查询串中的 `.` 可匹配任意一个小写字母。遇到普通字符仍唯一转移，遇到点号要 DFS 枚举现有儿子；原来的单路径查询因此失效。

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
  int count;
  cin >> count;
  vector<Node> trie(1);
  while (count--) {
    string word;
    cin >> word;
    int node = 0;
    for (char character : word) {
      int edge = character - 'a';
      if (trie[node].next[edge] == -1) {
        trie[node].next[edge] = trie.size();
        trie.emplace_back();
      }
      node = trie[node].next[edge];
    }
    trie[node].terminal = true;
  }
  function<bool(int, int, const string&)> match = [&](int node, int index, const string& pattern) {
    if (index == static_cast<int>(pattern.size())) {
      return trie[node].terminal;
    }
    if (pattern[index] != '.') {
      int child = trie[node].next[pattern[index] - 'a'];
      return child != -1 && match(child, index + 1, pattern);
    }
    for (int child : trie[node].next) {
      if (child != -1 && match(child, index + 1, pattern)) {
        return true;
      }
    }
    return false;
  };
  int queries;
  cin >> queries;
  while (queries--) {
    string pattern;
    cin >> pattern;
    cout << (match(0, 0, pattern) ? "true" : "false") << '\n';
  }
}
```

无通配符时 $O(L)$；有 $w$ 个点号时最坏枚举 $O(26^w)$ 条路径，实际由 Trie 中存在的结点数限制。

## 变种四：按字典序返回前缀补全结果

新定义：给定前缀和上限 $k$，返回字典序最小的至多 $k$ 个已存单词。先走到前缀结点，再按字符从小到大 DFS，并在结果满时剪枝。

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
  int count;
  cin >> count;
  vector<Node> trie(1);
  while (count--) {
    string word;
    cin >> word;
    int node = 0;
    for (char character : word) {
      int edge = character - 'a';
      if (trie[node].next[edge] == -1) {
        trie[node].next[edge] = trie.size();
        trie.emplace_back();
      }
      node = trie[node].next[edge];
    }
    trie[node].terminal = true;
  }
  string prefix;
  int limit;
  cin >> prefix >> limit;
  int node = 0;
  for (char character : prefix) {
    node = trie[node].next[character - 'a'];
    if (node == -1) {
      break;
    }
  }
  vector<string> answer;
  string current = prefix;
  function<void(int)> collect = [&](int currentNode) {
    if (answer.size() == static_cast<size_t>(limit)) {
      return;
    }
    if (trie[currentNode].terminal) {
      answer.push_back(current);
    }
    for (int edge = 0; edge < 26 && answer.size() < static_cast<size_t>(limit); ++edge) {
      int child = trie[currentNode].next[edge];
      if (child != -1) {
        current.push_back('a' + edge);
        collect(child);
        current.pop_back();
      }
    }
  };
  if (node != -1) {
    collect(node);
  }
  for (const string& word : answer) {
    cout << word << '\n';
  }
}
```

走前缀为 $O(L)$；之后访问输出相关子树，时间为 $O(L+V)$，其中 $V$ 是为产生前 $k$ 个答案实际访问的结点数，空间为 DFS 深度。

## 可复现验证

基础数组 Trie 与字符串集合 oracle 在随机插入、完整查询和前缀查询序列上逐项比较；另覆盖重复插入、单字符、一个单词是另一个单词前缀、完全不存在的首字符等边界。所有代码以 GNU++23 编译，并保持两空格缩进且无制表符。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/implement-trie-prefix-tree/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-78-lc1768/">← [力扣 Top 78] LC 1768 交替合并字符串 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-80-lc94/">[力扣 Top 80] LC 94 二叉树的中序遍历 简单 →</a>
</nav>
