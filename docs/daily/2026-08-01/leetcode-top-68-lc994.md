---
title: "[力扣 Top 68] LC 994 腐烂的橘子 中等"
---

# [力扣 Top 68] LC 994 腐烂的橘子 中等

<p class="daily-archive-kicker">2026-08-01 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=cfb5298107c5c994285c2acc2c5fc1cb067cf9305713bc35c15a830c6e16f5f7 -->
## 官方原始信息

- Top 排名：68
- 题号：LC 994
- 官方中文标题：腐烂的橘子
- 官方难度：中等
- 官方链接：[腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/)

### 原始题意

在 $m\times n$ 网格中，0 表示空格，1 表示新鲜橘子，2 表示腐烂橘子。每分钟，腐烂橘子会让上下左右相邻的新鲜橘子腐烂。返回没有新鲜橘子所需的最少分钟数；若永远无法全部腐烂，返回 -1。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int orangesRotting(vector<vector<int>>& grid);
};
```

### 全部官方样例

```text
输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
输出：4
```

```text
输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
输出：-1
解释：左下角新鲜橘子与所有腐烂源不连通。
```

```text
输入：grid = [[0,2]]
输出：0
解释：初始时已经没有新鲜橘子。
```

### 全部约束

- $m=|grid|$，$n=|grid_i|$。
- $1\le m,n\le10$。
- 每个格子只可能为 0、1 或 2。

## 约束推导与边界

多个初始腐烂橘子会同时传播，不能从每个源分别跑搜索再简单相加。把所有源在第 0 层一起入队，多源 BFS 等价于增加一个到所有源距离为 0 的超级源；某新鲜格第一次被访问的层数，就是它到最近初始腐烂源的最短四连通距离，也就是最早腐烂时间。

应先统计新鲜橘子数：若为 0，答案是 0；BFS 后仍有新鲜橘子则不可达。时间最多为可达新鲜格数，不会溢出。

## 解法递进

### 解法一：逐分钟全网格扫描

每轮先找出当前所有腐烂橘子能感染的新鲜格，暂存后统一修改，避免同一分钟连锁传播多层。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int orangesRotting(vector<vector<int>>& grid) {
    int rows = grid.size();
    int columns = grid[0].size();
    int minutes = 0;
    const int direction[5] = {-1, 0, 1, 0, -1};
    while (true) {
      vector<pair<int, int>> changed;
      for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
          if (grid[row][column] != 1) {
            continue;
          }
          for (int d = 0; d < 4; ++d) {
            int nextRow = row + direction[d];
            int nextColumn = column + direction[d + 1];
            if (0 <= nextRow && nextRow < rows && 0 <= nextColumn && nextColumn < columns &&
                grid[nextRow][nextColumn] == 2) {
              changed.push_back({row, column});
              break;
            }
          }
        }
      }
      if (changed.empty()) {
        break;
      }
      for (auto [row, column] : changed) {
        grid[row][column] = 2;
      }
      ++minutes;
    }
    for (const auto& row : grid) {
      if (find(row.begin(), row.end(), 1) != row.end()) {
        return -1;
      }
    }
    return minutes;
  }
};
```

最坏时间 $O((mn)^2)$，临时空间 $O(mn)$。重复扫描已经稳定的格子是瓶颈。

### 最佳实用解：多源分层 BFS

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int orangesRotting(vector<vector<int>>& grid) {
    int rows = grid.size();
    int columns = grid[0].size();
    queue<pair<int, int>> queue;
    int fresh = 0;
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (grid[row][column] == 2) {
          queue.push({row, column});
        } else if (grid[row][column] == 1) {
          ++fresh;
        }
      }
    }
    const int direction[5] = {-1, 0, 1, 0, -1};
    int minutes = 0;
    while (fresh > 0 && !queue.empty()) {
      int layerSize = queue.size();
      while (layerSize--) {
        auto [row, column] = queue.front();
        queue.pop();
        for (int d = 0; d < 4; ++d) {
          int nextRow = row + direction[d];
          int nextColumn = column + direction[d + 1];
          if (nextRow < 0 || nextRow >= rows || nextColumn < 0 || nextColumn >= columns ||
              grid[nextRow][nextColumn] != 1) {
            continue;
          }
          grid[nextRow][nextColumn] = 2;
          --fresh;
          queue.push({nextRow, nextColumn});
        }
      }
      ++minutes;
    }
    return fresh == 0 ? minutes : -1;
  }
};
```

时间 $O(mn)$，队列空间 $O(mn)$。

## 正确性证明

初始队列包含且仅包含时间 0 已腐烂的所有源。假设开始处理第 $t$ 层时，队列中的格子恰在第 $t$ 分钟腐烂；它们把所有仍新鲜的四邻格在第 $t+1$ 分钟标记并入下一层。提前标记保证同一格只入队一次，且任何更晚路径都不会覆盖它。

由 BFS 最短路性质，每个被访问格的层数是到任一源的最短距离，也就是传播规则允许的最早腐烂时间。若最终 `fresh==0`，最后处理的层给出全部腐烂的最短时间；否则剩余格与所有源不连通，任何传播序列都无法到达，返回 -1。

## 样例手推

样例 1 的第 0 层只有左上角；第 1 分钟感染其右、下两格，第 2 分钟到达 `(0,2)` 与 `(1,1)`，第 3 分钟到达 `(1,2)` 与 `(2,1)`，第 4 分钟到达 `(2,2)`，因此答案为 4。

只有空格或腐烂橘子时 `fresh=0`，循环不执行并返回 0；没有初始腐烂源但存在新鲜橘子时队列为空，返回 -1。

## 易错点与方案比较

- 多源必须同时入队，不能顺序完成某个源后再处理另一个源。
- 新鲜格应在入队时立刻改为 2，避免被多个邻居重复入队。
- 分钟数只在确实处理一层传播时增加；用 `fresh>0` 约束可避免多算最后一分钟。
- 全网扫描适合直观 oracle；多源 BFS 消除重复扫描，是竞赛与面试应优先记忆的模型。

## 变种一：允许八个方向传播

只改变邻接关系，多源 BFS 不变量不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<vector<int>> grid(rows, vector<int>(columns));
  queue<tuple<int, int, int>> queue;
  int fresh = 0;
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      cin >> grid[i][j];
      if (grid[i][j] == 2) {
        queue.push({i, j, 0});
      } else if (grid[i][j] == 1) {
        ++fresh;
      }
    }
  }
  int answer = 0;
  while (!queue.empty()) {
    auto [row, column, time] = queue.front();
    queue.pop();
    answer = max(answer, time);
    for (int dr = -1; dr <= 1; ++dr) {
      for (int dc = -1; dc <= 1; ++dc) {
        int nr = row + dr;
        int nc = column + dc;
        if ((dr || dc) && 0 <= nr && nr < rows && 0 <= nc && nc < columns && grid[nr][nc] == 1) {
          grid[nr][nc] = 2;
          --fresh;
          queue.push({nr, nc, time + 1});
        }
      }
    }
  }
  cout << (fresh == 0 ? answer : -1) << '\n';
}
```

时间 $O(mn)$，空间 $O(mn)$。

## 变种二：每个格子的腐烂延迟不同

从已腐烂格进入新鲜格 $(i,j)$ 需要 `delay[i][j]` 分钟。边权不再统一，BFS 失效，改用多源 Dijkstra。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using State = tuple<long long, int, int>;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  vector<vector<int>> delay(rows, vector<int>(columns));
  for (auto& row : delay) {
    for (int& value : row) {
      cin >> value;
    }
  }
  const long long infinity = numeric_limits<long long>::max() / 4;
  vector<vector<long long>> distance(rows, vector<long long>(columns, infinity));
  priority_queue<State, vector<State>, greater<State>> heap;
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      if (grid[i][j] == '2') {
        distance[i][j] = 0;
        heap.push({0, i, j});
      }
    }
  }
  const int direction[5] = {-1, 0, 1, 0, -1};
  while (!heap.empty()) {
    auto [current, row, column] = heap.top();
    heap.pop();
    if (current != distance[row][column]) {
      continue;
    }
    for (int d = 0; d < 4; ++d) {
      int nr = row + direction[d];
      int nc = column + direction[d + 1];
      if (nr < 0 || nr >= rows || nc < 0 || nc >= columns || grid[nr][nc] == '0') {
        continue;
      }
      long long candidate = current + delay[nr][nc];
      if (candidate < distance[nr][nc]) {
        distance[nr][nc] = candidate;
        heap.push({candidate, nr, nc});
      }
    }
  }
  long long answer = 0;
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      if (grid[i][j] == '1') {
        if (distance[i][j] == infinity) {
          cout << -1 << '\n';
          return 0;
        }
        answer = max(answer, distance[i][j]);
      }
    }
  }
  cout << answer << '\n';
}
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## 变种三：输出每个橘子的最早腐烂时间

保留 BFS 距离矩阵；空格输出 -2，不可达新鲜橘子输出 -1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<vector<int>> grid(rows, vector<int>(columns));
  vector<vector<int>> time(rows, vector<int>(columns, -1));
  queue<pair<int, int>> queue;
  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < columns; ++j) {
      cin >> grid[i][j];
      if (grid[i][j] == 2) {
        time[i][j] = 0;
        queue.push({i, j});
      } else if (grid[i][j] == 0) {
        time[i][j] = -2;
      }
    }
  }
  const int direction[5] = {-1, 0, 1, 0, -1};
  while (!queue.empty()) {
    auto [row, column] = queue.front();
    queue.pop();
    for (int d = 0; d < 4; ++d) {
      int nr = row + direction[d];
      int nc = column + direction[d + 1];
      if (0 <= nr && nr < rows && 0 <= nc && nc < columns && time[nr][nc] == -1) {
        time[nr][nc] = time[row][column] + 1;
        queue.push({nr, nc});
      }
    }
  }
  for (const auto& row : time) {
    for (int j = 0; j < columns; ++j) {
      cout << row[j] << (j + 1 == columns ? '\n' : ' ');
    }
  }
}
```

时间与空间均为 $O(mn)$。

## 变种四：最少穿过多少堵墙才能让感染到达终点

新定义：0 为可走格、1 为墙；从多个源到目标，进入墙的代价为 1，求最小破墙数。边权只有 0/1，使用 0-1 BFS。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns, sourceCount;
  cin >> rows >> columns >> sourceCount;
  vector<string> grid(rows);
  for (string& row : grid) {
    cin >> row;
  }
  const int infinity = 1e9;
  vector<vector<int>> distance(rows, vector<int>(columns, infinity));
  deque<pair<int, int>> deque;
  while (sourceCount--) {
    int row, column;
    cin >> row >> column;
    distance[row][column] = 0;
    deque.push_back({row, column});
  }
  int targetRow, targetColumn;
  cin >> targetRow >> targetColumn;
  const int direction[5] = {-1, 0, 1, 0, -1};
  while (!deque.empty()) {
    auto [row, column] = deque.front();
    deque.pop_front();
    for (int d = 0; d < 4; ++d) {
      int nr = row + direction[d];
      int nc = column + direction[d + 1];
      if (nr < 0 || nr >= rows || nc < 0 || nc >= columns) {
        continue;
      }
      int cost = grid[nr][nc] == '1';
      if (distance[row][column] + cost < distance[nr][nc]) {
        distance[nr][nc] = distance[row][column] + cost;
        if (cost) {
          deque.push_back({nr, nc});
        } else {
          deque.push_front({nr, nc});
        }
      }
    }
  }
  cout << distance[targetRow][targetColumn] << '\n';
}
```

时间 $O(mn)$，空间 $O(mn)$。目标从“统一时间传播”改变为 0/1 加权最短路，普通 BFS 不再正确。

## 可复现验证

对所有 $3\times3$ 网格状态枚举，比较逐分钟扫描与多源 BFS；随机更大网格再把 BFS 时间矩阵与从每个源分别计算的最短距离最小值比较。覆盖无新鲜橘子、无腐烂源、孤岛和多个源同分钟抵达。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/rotting-oranges/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/rotting-oranges/)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-67-lc234/">← [力扣 Top 67] LC 234 回文链表 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-69-lc138/">[力扣 Top 69] LC 138 随机链表的复制 中等 →</a>
</nav>
