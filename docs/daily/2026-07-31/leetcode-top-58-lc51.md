---
title: "[力扣 Top 58] LC 51 N 皇后 困难"
---

# [力扣 Top 58] LC 51 N 皇后 困难

<p class="daily-archive-kicker">2026-07-31 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a82e5be52b472bf4a6af396851ea9bccd6fc0f37f59956de6a7d9de391e0b417 -->
## 官方原始信息

- Top 排名：58
- 题号：LC 51
- 官方中文标题：N 皇后
- 官方难度：困难
- 官方链接：[N 皇后](https://leetcode.cn/problems/n-queens/)

### 原始题意

在 $n\times n$ 棋盘上放置 $n$ 个皇后，使任意两个皇后都不同行、不同列，也不在同一条斜线上。返回所有不同布局，用 `Q` 表示皇后、`.` 表示空格。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<string>> solveNQueens(int n);
};
```

### 全部官方样例

```text
输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：4 皇后共有两种不同解。
```

```text
输入：n = 1
输出：[["Q"]]
```

### 全部约束

- $1\le n\le9$。

## 约束推导与建模

每行必须且只放一个皇后，因此递归层可以直接表示行，避免枚举 $n^2$ 个格子的任意子集。放在 `(row,column)` 的皇后会占用列 `column`、主对角线 `row-column` 和副对角线 `row+column`。$n\le9$ 允许回溯枚举全部解；位掩码可把三类冲突检查降为常数时间。

## 解法递进

### 解法一：放置前扫描已有棋盘

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<string>> answer;
  vector<string> board;
  bool safe(int row, int column) {
    for (int previous = 0; previous < row; ++previous) {
      if (board[previous][column] == 'Q') {
        return false;
      }
    }
    for (int r = row - 1, c = column - 1; r >= 0 && c >= 0; --r, --c) {
      if (board[r][c] == 'Q') {
        return false;
      }
    }
    for (int r = row - 1, c = column + 1; r >= 0 && c < static_cast<int>(board.size()); --r, ++c) {
      if (board[r][c] == 'Q') {
        return false;
      }
    }
    return true;
  }
  void search(int row) {
    int n = board.size();
    if (row == n) {
      answer.push_back(board);
      return;
    }
    for (int column = 0; column < n; ++column) {
      if (safe(row, column)) {
        board[row][column] = 'Q';
        search(row + 1);
        board[row][column] = '.';
      }
    }
  }
public:
  vector<vector<string>> solveNQueens(int n) {
    board.assign(n, string(n, '.'));
    search(0);
    return answer;
  }
};
```

搜索树上界 $O(n!)$，每次冲突检查 $O(n)$；辅助空间 $O(n^2)$。

### 最佳实用解：三类攻击线位掩码

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<string>> answer;
  vector<int> queenColumn;
  int fullMask;
  void search(int row, int columns, int diagonalLeft, int diagonalRight) {
    int n = queenColumn.size();
    if (row == n) {
      vector<string> board(n, string(n, '.'));
      for (int r = 0; r < n; ++r) {
        board[r][queenColumn[r]] = 'Q';
      }
      answer.push_back(board);
      return;
    }
    int available = fullMask & ~(columns | diagonalLeft | diagonalRight);
    while (available) {
      int position = available & -available;
      available -= position;
      queenColumn[row] = countr_zero(static_cast<unsigned int>(position));
      search(row + 1, columns | position, ((diagonalLeft | position) << 1) & fullMask,
          (diagonalRight | position) >> 1);
    }
  }
public:
  vector<vector<string>> solveNQueens(int n) {
    queenColumn.resize(n);
    fullMask = (1 << n) - 1;
    search(0, 0, 0, 0);
    return answer;
  }
};
```

搜索规模仍受解空间支配，常用上界 $O(n!)$；每个节点冲突计算为 $O(1)$，递归空间 $O(n)$，输出构造另需 $O(n^2)$ 每解。

## 正确性证明

递归第 `row` 层恰好为该行选择一列。`columns` 标记已占列；把左斜攻击位左移、右斜攻击位右移后，它们恰好表示下一行被两类对角线攻击的列。因此 `available` 中每个位置且仅有不冲突列。沿合法位置递归保证生成布局合法。任一合法布局在每行都有唯一皇后列，且该列必属于对应层的 `available`，所以搜索会沿唯一分支生成它；没有遗漏或重复。

## 样例手推

`n=4` 时若第一行选列 0，后续所有分支最终冲突；选列 1 可依次选列 3、0、2，得到第一种解；对称地第一行选列 2 得到第二种解。第一行选列 3 与列 0 同样无解。

## 易错点与方案比较

- 两条对角线可用 `row-column` 与 `row+column` 编号；位掩码版则通过每层移位传播攻击范围。
- `position = available & -available` 每次取最低位，记得从 `available` 删除。
- 左移后要与 `fullMask` 相与，避免棋盘外高位干扰。
- 集合版更直观；位掩码常数更小，适合竞赛与计数，推荐理解集合含义后记忆。

## 变种一：只统计解的数量

不构造棋盘，叶子直接累加，适合更大的 `n`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long search(int fullMask, int columns, int diagonalLeft, int diagonalRight) {
  if (columns == fullMask) {
    return 1;
  }
  long long answer = 0;
  int available = fullMask & ~(columns | diagonalLeft | diagonalRight);
  while (available) {
    int position = available & -available;
    available -= position;
    answer += search(fullMask, columns | position, ((diagonalLeft | position) << 1) & fullMask,
        (diagonalRight | position) >> 1);
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  cout << search((1 << n) - 1, 0, 0, 0) << '\n';
}
```

时间由搜索树决定，辅助空间 $O(n)$。

## 变种二：返回皇后列序列字典序最小的解

按列从小到大尝试，找到第一份完整解就停止；这里字典序定义在每行皇后列组成的整数序列上。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool search(int row, int n, vector<int>& placement, vector<char>& column,
    vector<char>& diagonalDown, vector<char>& diagonalUp) {
  if (row == n) {
    return true;
  }
  for (int current = 0; current < n; ++current) {
    int down = row - current + n - 1;
    int up = row + current;
    if (column[current] || diagonalDown[down] || diagonalUp[up]) {
      continue;
    }
    placement[row] = current;
    column[current] = diagonalDown[down] = diagonalUp[up] = true;
    if (search(row + 1, n, placement, column, diagonalDown, diagonalUp)) {
      return true;
    }
    column[current] = diagonalDown[down] = diagonalUp[up] = false;
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> placement(n);
  vector<char> column(n), diagonalDown(2 * n - 1), diagonalUp(2 * n - 1);
  if (!search(0, n, placement, column, diagonalDown, diagonalUp)) {
    cout << -1 << '\n';
    return 0;
  }
  for (int value : placement) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

最坏仍遍历指数级搜索树，辅助空间 $O(n)$。

## 变种三：棋盘含禁用格，统计合法布局

每行额外给出可用列掩码，和攻击掩码共同过滤。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long search(int row, int fullMask, const vector<int>& allowed, int columns, int diagonalLeft,
    int diagonalRight) {
  if (row == static_cast<int>(allowed.size())) {
    return 1;
  }
  long long answer = 0;
  int available = allowed[row] & fullMask & ~(columns | diagonalLeft | diagonalRight);
  while (available) {
    int position = available & -available;
    available -= position;
    answer += search(row + 1, fullMask, allowed, columns | position,
        ((diagonalLeft | position) << 1) & fullMask, (diagonalRight | position) >> 1);
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> allowed(n);
  for (int row = 0; row < n; ++row) {
    string cells;
    cin >> cells;
    for (int column = 0; column < n; ++column) {
      if (cells[column] == '.') {
        allowed[row] |= 1 << column;
      }
    }
  }
  cout << search(0, (1 << n) - 1, allowed, 0, 0, 0) << '\n';
}
```

时间由剩余搜索树决定，空间 $O(n)$。

## 变种四：在 m×n 棋盘放恰好 k 个皇后

允许某些行不放皇后；新增“跳过本行”分支，并用剩余行数剪枝。列和两类对角线仍用布尔集合维护。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long answer = 0;
void search(int row, int m, int n, int k, int placed, vector<char>& column,
    vector<char>& diagonalDown, vector<char>& diagonalUp) {
  if (placed == k) {
    ++answer;
    return;
  }
  if (row == m || placed + (m - row) < k) {
    return;
  }
  search(row + 1, m, n, k, placed, column, diagonalDown, diagonalUp);
  for (int current = 0; current < n; ++current) {
    int down = row - current + n - 1;
    int up = row + current;
    if (column[current] || diagonalDown[down] || diagonalUp[up]) {
      continue;
    }
    column[current] = diagonalDown[down] = diagonalUp[up] = true;
    search(row + 1, m, n, k, placed + 1, column, diagonalDown, diagonalUp);
    column[current] = diagonalDown[down] = diagonalUp[up] = false;
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, k;
  cin >> m >> n >> k;
  vector<char> column(n), diagonalDown(m + n - 1), diagonalUp(m + n - 1);
  search(0, m, n, k, 0, column, diagonalDown, diagonalUp);
  cout << answer << '\n';
}
```

时间为指数级搜索，递归空间 $O(m)$。

## 可复现验证

对 $n\le8$，把位掩码版的解集合与逐格扫描版排序后逐项比较；每份棋盘再独立检查行、列和两类对角线。计数结果同时与公开已知小规模序列 $1,0,0,2,10,4,40,92$ 核对。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/n-queens/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/n-queens/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-57-lc76/">← [力扣 Top 57] LC 76 最小覆盖子串 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-59-lc35/">[力扣 Top 59] LC 35 搜索插入位置 简单 →</a>
</nav>
