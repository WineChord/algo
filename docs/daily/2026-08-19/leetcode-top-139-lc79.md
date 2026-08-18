---
title: "[力扣 Top 139] LC 79 单词搜索 中等"
---

# [力扣 Top 139] LC 79 单词搜索 中等

<p class="daily-archive-kicker">2026-08-19 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-19 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d522506117b337326aa8b2772bd5695e7b83fadcaed8114babfff8101edda621 -->
[官方题目：79. 单词搜索](https://leetcode.cn/problems/word-search/)

## 官方原始信息

- 高频队列位置：Top 139；权威表中的题目为 `79. 单词搜索`。
- 官方中文标题：单词搜索；官方难度：中等。
- 函数签名：`bool exist(vector<vector<char>>& board, string word)`。
- 官方链接：[力扣中国题目页](https://leetcode.cn/problems/word-search/)。

给定一个 $m\times n$ 的字符网格 `board` 和字符串 `word`。需要判断能否从某个格子出发，
每一步移动到水平或竖直相邻格子，使沿途字符依次等于 `word`。一条路径中同一格不能重复
使用。

### 全部官方样例

示例 1：

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true
```

一条可行路径依次经过字符 `A -> B -> C -> C -> E -> D`。

示例 2：

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
输出：true
```

示例 3：

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
输出：false
```

第三个样例若想拼出最后一个 `B`，只能回到已经使用过的格子，因此不合法。

### 全部官方约束

- $m=\lvert board\rvert$，$n=\lvert board_i\rvert$。
- $1\le m,n\le6$。
- $1\le\lvert word\rvert\le15$。
- `board` 与 `word` 仅由大小写英文字母组成。
- 官方进阶要求考虑搜索剪枝，使网格扩大时仍尽量快。

## 约束推导与搜索状态

状态至少要包含当前位置、已经匹配的前缀长度和本条路径用过的格子。网格最多只有 36 个
格子，单词长度最多 15，指数搜索是可接受的；但不能用普通二维可达性 DP，因为“某格是否
还能使用”取决于整条历史路径。

从起点之后，搜索不能立即回到上一个格子，所以一层最多产生 3 个新分支。最坏上界可写成
$O(mn\cdot3^{L-1})$，其中 $L=\lvert word\rvert$。实际还可先做两个必要条件剪枝：

1. 若 $L>mn$，路径必定不存在。
2. 若网格中某字符的数量少于 `word` 所需数量，必定不存在。

此外，从网格里出现次数更少的一端开始搜索，往往能显著减少起点和浅层分支。把 `word`
反转不会改变答案，因为任何合法路径倒序后仍是合法路径。

## 样例手推与边界

样例 1 从左上角 `A` 出发，依次向右、向右、向下、向左、向下，得到 `ABCCED`；每个格子
只进入一次。样例 3 的前缀 `ABC` 可以匹配，但目标末尾的 `B` 不能通过未使用的相邻格得到。

- 单字符单词：只要网格中存在该字符就成功。
- 单行或单列网格：方向减少，但仍要保留访问标记，不能折返复用。
- 大小写敏感：`A` 与 `a` 是不同字符。
- 重复字符很多：频次条件只负责判否，不能代替路径连通性。
- `word` 长于格子数：即使字符数量看似足够，也因禁止复用而失败。
- 找到一条路径即可立刻返回，不需要枚举全部路径。

## 解法一：枚举所有不重复路径

从每个可能起点开始深度优先搜索。每进入一个格子就把它标记为已使用，回溯时恢复。这个
枚举覆盖了所有起点和每一步的四个方向，因此是正确暴力解，也适合作为小规模 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int rows;
  int cols;
  vector<vector<bool>> used;
  bool dfs(const vector<vector<char>>& board, const string& word, int row, int col, int index) {
    if (board[row][col] != word[index]) return false;
    if (index + 1 == static_cast<int>(word.size())) return true;
    used[row][col] = true;
    static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (auto& direction : directions) {
      int nextRow = row + direction[0];
      int nextCol = col + direction[1];
      if (nextRow < 0 || nextRow >= rows || nextCol < 0 || nextCol >= cols) continue;
      if (!used[nextRow][nextCol] && dfs(board, word, nextRow, nextCol, index + 1)) {
        used[row][col] = false;
        return true;
      }
    }
    used[row][col] = false;
    return false;
  }
public:
  bool exist(vector<vector<char>>& board, string word) {
    rows = board.size();
    cols = board[0].size();
    used.assign(rows, vector<bool>(cols));
    for (int row = 0; row < rows; ++row) {
      for (int col = 0; col < cols; ++col) {
        if (dfs(board, word, row, col, 0)) return true;
      }
    }
    return false;
  }
};
```

时间复杂度最坏为 $O(mn\cdot4^{L-1})$，额外空间为 $O(mn+L)$。瓶颈是未先排除不可能的
字符频次，也没有利用第一步之后不能原路返回这一结构。

## 从暴力到剪枝回溯

先统计字符频次可在 $O(mn+L)$ 时间内拒绝一整类无解输入。随后比较 `word.front()` 与
`word.back()` 在网格中的频次：若末字符更少，就反转单词，从更稀缺的一端开始。搜索过程
把当前格临时写成不可能出现在输入中的 `\0`，可省去独立访问矩阵；回溯恢复字符，因而不会
污染其他分支。

这不会改变指数级最坏界，但消除了大量现实分支。长度上界只有 15，稳定、清晰的回溯比把
36 个格子压入复杂状态 DP 更合适。

## 最佳实用解：频次剪枝、稀缺端反转与原地标记

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int rows;
  int cols;
  bool dfs(vector<vector<char>>& board, const string& word, int row, int col, int index) {
    if (board[row][col] != word[index]) return false;
    if (index + 1 == static_cast<int>(word.size())) return true;
    char saved = board[row][col];
    board[row][col] = '\0';
    static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (auto& direction : directions) {
      int nextRow = row + direction[0];
      int nextCol = col + direction[1];
      if (nextRow < 0 || nextRow >= rows || nextCol < 0 || nextCol >= cols) continue;
      if (dfs(board, word, nextRow, nextCol, index + 1)) {
        board[row][col] = saved;
        return true;
      }
    }
    board[row][col] = saved;
    return false;
  }
public:
  bool exist(vector<vector<char>>& board, string word) {
    rows = board.size();
    cols = board[0].size();
    if (static_cast<int>(word.size()) > rows * cols) return false;
    array<int, 128> available{};
    array<int, 128> needed{};
    for (const auto& row : board) {
      for (char letter : row) ++available[static_cast<unsigned char>(letter)];
    }
    for (char letter : word) ++needed[static_cast<unsigned char>(letter)];
    for (int code = 0; code < 128; ++code) {
      if (needed[code] > available[code]) return false;
    }
    if (available[static_cast<unsigned char>(word.front())] >
        available[static_cast<unsigned char>(word.back())]) {
      reverse(word.begin(), word.end());
    }
    for (int row = 0; row < rows; ++row) {
      for (int col = 0; col < cols; ++col) {
        if (board[row][col] == word[0] && dfs(board, word, row, col, 0)) return true;
      }
    }
    return false;
  }
};
```

时间复杂度最坏为 $O(mn\cdot3^{L-1})$，频次预处理为 $O(mn+L)$；递归栈额外空间
$O(L)$。网格字符会在单个递归分支内临时变化，但所有返回路径都先恢复，因此调用结束后
`board` 与输入逐字符一致。所有计数都不超过 36 或 15，`int` 足够。

### 正确性证明

频次与长度剪枝都只是合法路径存在的必要条件，拒绝时答案必为假。反转 `word` 时，任意原
路径倒序后从终点回到起点，仍只走四邻接边且不重复格子，所以存在性不变。

对 DFS 归纳。调用 `dfs(row,col,index)` 只在当前格字符等于 `word[index]` 时继续，并把该格
临时标记，故后续递归不能重复使用它。循环恰好枚举四个合法相邻格；若某条递归链匹配到
最后一个字符，就构成一条完整合法路径。反之，若存在从当前状态出发的合法后缀路径，它的
下一步必在这四个未使用相邻格之一，算法会枚举到并由归纳假设返回真。外层枚举全部起点，
所以算法返回真当且仅当题目要求的路径存在。

## 同阶方案与推荐

独立 `used` 数组和原地标记的渐近复杂度相同。`used` 不修改输入，语义直观；原地标记少一块
状态，也更贴近竞赛常见写法。位掩码可以把 36 个访问状态装入 `uint64_t`，但并不会消除
指数分支，代码更易出现坐标编号错误。面试和竞赛优先记忆“DFS + 回溯恢复”，再补上频次
剪枝和稀缺端反转。

## 易错点

- 只恢复失败分支、忘记在成功提前返回前恢复当前格，会修改调用者的 `board`。
- 把对角格也当作相邻格；原题只有上下左右。
- 用全局永久访问标记，导致一个起点失败后阻塞其他起点。
- 把字符频次充分条件化；频次足够不代表这些格子能连成路径。
- 反转网格而不是反转 `word`，或忘记说明反向路径保持四邻接与不重复性质。
- 使用可能与输入字符相同的标记；输入仅含英文字母，`\0` 才安全。

## 验证说明

三组官方样例均通过。验证还覆盖单格、单行折返、大小写不同、单词长于格子数、重复字符
不足，以及成功返回后网格完全恢复。对所有不超过 $3\times3$ 的小网格与短单词，可用显式
路径枚举作为 oracle，对频次剪枝版做随机对拍。

## 变种一：返回一条坐标路径

新定义：若单词存在，输出一条路径上的零基坐标；否则输出 `-1`。存在性 DFS 仍成立，但
进入格子时把坐标压入 `path`，失败回溯时弹出，首次成功时保留。时间复杂度仍为
$O(mn\cdot3^{L-1})$，额外空间 $O(mn+L)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int rows, cols;
vector<vector<char>> board;
string word;
vector<vector<bool>> used;
vector<pair<int, int>> path;
bool dfs(int row, int col, int index) {
  if (board[row][col] != word[index]) return false;
  used[row][col] = true;
  path.push_back({row, col});
  if (index + 1 == static_cast<int>(word.size())) return true;
  static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
  for (auto& direction : directions) {
    int nextRow = row + direction[0];
    int nextCol = col + direction[1];
    if (nextRow < 0 || nextRow >= rows || nextCol < 0 || nextCol >= cols) continue;
    if (!used[nextRow][nextCol] && dfs(nextRow, nextCol, index + 1)) return true;
  }
  path.pop_back();
  used[row][col] = false;
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> rows >> cols;
  board.assign(rows, vector<char>(cols));
  for (auto& row : board) for (char& letter : row) cin >> letter;
  cin >> word;
  used.assign(rows, vector<bool>(cols));
  for (int row = 0; row < rows; ++row) {
    for (int col = 0; col < cols; ++col) {
      if (dfs(row, col, 0)) {
        for (auto [x, y] : path) cout << x << ' ' << y << '\n';
        return 0;
      }
    }
  }
  cout << -1 << '\n';
  return 0;
}
```

## 变种二：统计所有合法简单路径

新定义：不同坐标序列视为不同方案，求方案数。原算法的“找到即返回”失效，必须累加所有
分支，并在每次返回前恢复访问状态。若网格扩大，答案可能溢出，应按题目要求改用大整数或
取模；下面假设结果能放入 `long long`。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int rows, cols;
vector<vector<char>> board;
string word;
long long dfs(int row, int col, int index) {
  if (board[row][col] != word[index]) return 0;
  if (index + 1 == static_cast<int>(word.size())) return 1;
  char saved = board[row][col];
  board[row][col] = '\0';
  long long ways = 0;
  static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
  for (auto& direction : directions) {
    int nextRow = row + direction[0];
    int nextCol = col + direction[1];
    if (nextRow < 0 || nextRow >= rows || nextCol < 0 || nextCol >= cols) continue;
    ways += dfs(nextRow, nextCol, index + 1);
  }
  board[row][col] = saved;
  return ways;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> rows >> cols;
  board.assign(rows, vector<char>(cols));
  for (auto& row : board) for (char& letter : row) cin >> letter;
  cin >> word;
  long long answer = 0;
  for (int row = 0; row < rows; ++row) {
    for (int col = 0; col < cols; ++col) answer += dfs(row, col, 0);
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种三：允许重复使用格子

新定义：路径仍按上下左右移动，但同一格可出现多次。访问历史不再影响未来，指数回溯可
压缩为按单词位置推进的可达性 DP。`reachable[row][col]` 表示当前字符匹配后能否停在该格；
每层只看上一层四邻居。时间 $O(Lmn)$，空间 $O(mn)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, cols;
  cin >> rows >> cols;
  vector<vector<char>> board(rows, vector<char>(cols));
  for (auto& row : board) for (char& letter : row) cin >> letter;
  string word;
  cin >> word;
  vector<vector<bool>> reachable(rows, vector<bool>(cols));
  for (int row = 0; row < rows; ++row) {
    for (int col = 0; col < cols; ++col) reachable[row][col] = board[row][col] == word[0];
  }
  static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
  for (int index = 1; index < static_cast<int>(word.size()); ++index) {
    vector<vector<bool>> next(rows, vector<bool>(cols));
    for (int row = 0; row < rows; ++row) {
      for (int col = 0; col < cols; ++col) {
        if (board[row][col] != word[index]) continue;
        for (auto& direction : directions) {
          int previousRow = row + direction[0];
          int previousCol = col + direction[1];
          if (previousRow < 0 || previousRow >= rows) continue;
          if (previousCol < 0 || previousCol >= cols) continue;
          next[row][col] = next[row][col] || reachable[previousRow][previousCol];
        }
      }
    }
    reachable.swap(next);
  }
  bool answer = false;
  for (const auto& row : reachable) for (bool value : row) answer = answer || value;
  cout << (answer ? "true\n" : "false\n");
  return 0;
}
```

## 变种四：同一网格查询很多单词

新定义：给定词典，一次找出网格中能形成的全部单词，对应
[212. 单词搜索 II](https://leetcode.cn/problems/word-search-ii/)。逐词运行原算法会重复搜索
公共前缀；把词典建成 Trie，从每个格子只搜索一次，走到终止节点就收集单词。设所有实际
探索的 Trie 状态数为 $V$，时间与有效网格路径和 Trie 分支有关，最坏仍指数，但共享前缀
只处理一次；Trie 空间为词典总字符数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  struct Node {
    array<int, 26> next;
    int wordIndex;
    Node() : wordIndex(-1) { next.fill(-1); }
  };
  vector<Node> trie;
  vector<string> answer;
  int rows;
  int cols;
  void dfs(vector<vector<char>>& board, int row, int col, int node, vector<string>& words) {
    char letter = board[row][col];
    int child = trie[node].next[letter - 'a'];
    if (child == -1) return;
    if (trie[child].wordIndex != -1) {
      answer.push_back(words[trie[child].wordIndex]);
      trie[child].wordIndex = -1;
    }
    board[row][col] = '#';
    static const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (auto& direction : directions) {
      int nextRow = row + direction[0];
      int nextCol = col + direction[1];
      if (nextRow < 0 || nextRow >= rows || nextCol < 0 || nextCol >= cols) continue;
      if (board[nextRow][nextCol] != '#') dfs(board, nextRow, nextCol, child, words);
    }
    board[row][col] = letter;
  }
public:
  vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
    trie.assign(1, Node());
    for (int index = 0; index < static_cast<int>(words.size()); ++index) {
      int node = 0;
      for (char letter : words[index]) {
        int code = letter - 'a';
        if (trie[node].next[code] == -1) {
          trie[node].next[code] = trie.size();
          trie.emplace_back();
        }
        node = trie[node].next[code];
      }
      trie[node].wordIndex = index;
    }
    rows = board.size();
    cols = board[0].size();
    for (int row = 0; row < rows; ++row) {
      for (int col = 0; col < cols; ++col) dfs(board, row, col, 0, words);
    }
    return answer;
  }
};
```

## 来源

- [力扣中国：79. 单词搜索](https://leetcode.cn/problems/word-search/)
- [力扣中国：212. 单词搜索 II](https://leetcode.cn/problems/word-search-ii/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/word-search/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc227-c/">← [atcoder] ARC227 C Follow the Letters</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-515-q2-lc4025/">[力扣竞赛] 第 515 场周赛 Q2 LC 4025 交通灯的最大等待时间 中等 →</a>
</nav>
