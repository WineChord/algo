---
title: "[力扣竞赛] 第 511 场周赛 Q1 LC 3996 偶数次骑士移动 简单"
---

# [力扣竞赛] 第 511 场周赛 Q1 LC 3996 偶数次骑士移动 简单

<p class="daily-archive-kicker">2026-07-26 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../graph/weighted-parity-states.md">进入知识专题</a></p>

## 官方原始信息

- 比赛：第 511 场周赛
- 竞赛顺序：Q1
- 题号：LC 3996（官方 GraphQL 内部题目 ID 为 4369）
- 官方中文标题：偶数次骑士移动
- 官方英文标题：Even Number of Knight Moves
- 难度：简单
- 官方链接：https://leetcode.cn/problems/even-number-of-knight-moves/
- 官方竞赛链接：https://leetcode.cn/contest/weekly-contest-511/
- 函数签名：`bool canReach(vector<int>& start, vector<int>& target)`
- 官方示意图：https://assets.leetcode.com/uploads/2018/10/12/knight.png

### 原始题意

`start = [x,y]` 与 `target = [x,y]` 表示标准 $8\times8$ 国际象棋棋盘中、坐标均在 $0$ 到 $7$ 的两个格子。骑士每一步沿一个坐标移动 2、另一个坐标移动 1。判断是否存在一条从 `start` 到 `target` 的路径，其移动次数为偶数；0 次移动也属于偶数。

![骑士一步的八种移动](../../assets/daily/official/71a2fa1b1b3a-knight.png)

### 全部官方样例

1. `start = [1,1], target = [2,2]`，输出 `true`。例如 `(1,1) -> (3,2) -> (2,4) -> (4,3) -> (2,2)` 共 4 步。
2. `start = [4,5], target = [6,6]`，输出 `false`；不存在偶数步路径。

### 全部官方约束

- `start.length == target.length == 2`
- $0\le start[i],target[i]\le7$

## 最优结论

骑士一步的坐标和变化为 $\pm2\pm1$，奇偶性一定改变，因此每走一步棋盘黑白颜色翻转。标准 $8\times8$ 骑士图连通，所以存在偶数步路径当且仅当起点与终点同色：

$$
(x_s+y_s)\bmod2=(x_t+y_t)\bmod2.
$$

时间 $O(1)$、空间 $O(1)$。

## 约束、边界与观察

- 起终点相同可走 0 步，答案为 `true`。
- 黑白异色时，所有路径长度都为奇数；走一个 2 步往返只会把长度增加 2，无法改变奇偶。
- 在标准 $8\times8$ 棋盘上骑士图连通；若棋盘变小或加入障碍，同色只是必要条件，不再总是充分。
- 不需要计算最短路；题目只问是否存在某个偶数长度。

## 样例手推

样例 1 中起点坐标和为 2，终点为 4，均为偶数，所以同色，存在偶数步路径。样例 2 的坐标和分别为 9 与 12，颜色不同，任意路径步数都为奇数。

## 解法一：在“位置 × 步数奇偶”状态图上 BFS

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canReach(vector<int>& start, vector<int>& target) {
    static const int dx[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    static const int dy[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    bool seen[8][8][2]{};
    queue<array<int, 3>> q;
    seen[start[0]][start[1]][0] = true;
    q.push({start[0], start[1], 0});
    while (!q.empty()) {
      auto [x, y, parity] = q.front();
      q.pop();
      if (x == target[0] && y == target[1] && parity == 0) return true;
      for (int d = 0; d < 8; ++d) {
        int nx = x + dx[d], ny = y + dy[d], np = parity ^ 1;
        if (nx < 0 || nx >= 8 || ny < 0 || ny >= 8 || seen[nx][ny][np]) continue;
        seen[nx][ny][np] = true;
        q.push({nx, ny, np});
      }
    }
    return false;
  }
};
```

状态数固定为 128，时间与空间均为 $O(1)$；推广到 $H\times W$ 棋盘时为 $O(HW)$。它正确但保存了本题不需要的整张图。

## 解法二：利用棋盘二分图颜色（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canReach(vector<int>& start, vector<int>& target) {
    return ((start[0] + start[1]) & 1) == ((target[0] + target[1]) & 1);
  }
};
```

### 正确性证明

每次骑士移动让一个坐标改变奇数 1、另一个改变偶数 2，因此坐标和的奇偶性恰好翻转。故偶数步后颜色不变，异色终点不可能在偶数步到达。反过来，标准 $8\times8$ 棋盘的骑士图连通，所以同色两点之间存在路径；图的每条边都连接异色点，任意同色两点间路径长度必为偶数。因此条件充要。

### 复杂度

时间 $O(1)$，额外空间 $O(1)$。它直接利用二分图不变量，是面试与竞赛首选。

## 常见错误

- 把骑士移动误认为保持颜色；$2+1=3$ 是奇数，所以每步换色。
- 只检查横纵坐标各自奇偶，而不是坐标和奇偶。
- 认为必须走正偶数步，错误地把起终点相同判为 `false`。
- 将标准棋盘的连通性结论无条件推广到狭窄棋盘或有障碍棋盘。

## Follow-up 1：求最少移动次数

颜色只给奇偶，无法给最短距离；在 64 个格子上 BFS。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minKnightMoves(vector<int> start, vector<int> target) {
    static const int dx[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    static const int dy[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    vector<vector<int>> dist(8, vector<int>(8, -1));
    queue<pair<int, int>> q;
    dist[start[0]][start[1]] = 0;
    q.push({start[0], start[1]});
    while (!q.empty()) {
      auto [x, y] = q.front();
      q.pop();
      if (x == target[0] && y == target[1]) return dist[x][y];
      for (int d = 0; d < 8; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= 8 || ny < 0 || ny >= 8 || dist[nx][ny] != -1) continue;
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
      }
    }
    return -1;
  }
};
```

时间与空间均为 $O(64)$。

## Follow-up 2：恰好走 `k` 步

仅颜色相同不够，因为还受步数上限约束。做 `k` 层可达 DP。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canReachExactly(vector<int> start, vector<int> target, int k) {
    static const int dx[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    static const int dy[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    bool current[8][8]{};
    current[start[0]][start[1]] = true;
    while (k--) {
      bool next[8][8]{};
      for (int x = 0; x < 8; ++x) {
        for (int y = 0; y < 8; ++y) {
          if (!current[x][y]) continue;
          for (int d = 0; d < 8; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (0 <= nx && nx < 8 && 0 <= ny && ny < 8) next[nx][ny] = true;
          }
        }
      }
      memcpy(current, next, sizeof(current));
    }
    return current[target[0]][target[1]];
  }
};
```

时间 $O(64\cdot8\cdot k)$，空间 $O(64)$；若 $k$ 极大，可对 64 状态邻接矩阵做布尔矩阵快速幂。

## Follow-up 3：棋盘加入障碍

在 `(格子, 步数奇偶)` 上 BFS；同色仍必要，但障碍可能破坏连通性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool evenPathWithObstacles(vector<string> board, vector<int> start, vector<int> target) {
    int h = board.size(), w = board[0].size();
    static const int dx[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    static const int dy[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    vector<vector<array<char, 2>>> seen(h, vector<array<char, 2>>(w));
    queue<array<int, 3>> q;
    seen[start[0]][start[1]][0] = 1;
    q.push({start[0], start[1], 0});
    while (!q.empty()) {
      auto [x, y, parity] = q.front();
      q.pop();
      if (x == target[0] && y == target[1] && parity == 0) return true;
      for (int d = 0; d < 8; ++d) {
        int nx = x + dx[d], ny = y + dy[d], np = parity ^ 1;
        if (nx < 0 || nx >= h || ny < 0 || ny >= w || board[nx][ny] == '#') continue;
        if (!seen[nx][ny][np]) {
          seen[nx][ny][np] = 1;
          q.push({nx, ny, np});
        }
      }
    }
    return false;
  }
};
```

时间 $O(HW)$，空间 $O(HW)$。

## Follow-up 4：任意尺寸无障碍棋盘

小棋盘的骑士图可能不连通，因此直接在棋盘上 BFS 并记录距离；距离奇偶即所有路径的奇偶。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canReachEvenOnBoard(int h, int w, vector<int> start, vector<int> target) {
    static const int dx[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    static const int dy[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    vector<vector<int>> dist(h, vector<int>(w, -1));
    queue<pair<int, int>> q;
    dist[start[0]][start[1]] = 0;
    q.push({start[0], start[1]});
    while (!q.empty()) {
      auto [x, y] = q.front();
      q.pop();
      for (int d = 0; d < 8; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= h || ny < 0 || ny >= w || dist[nx][ny] != -1) continue;
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
      }
    }
    int d = dist[target[0]][target[1]];
    return d != -1 && d % 2 == 0;
  }
};
```

时间 $O(HW)$，空间 $O(HW)$。

## 验证

枚举标准棋盘的全部 $64^2$ 个起终点，用奇偶公式与 `(位置,奇偶)` BFS 比较；再单独验证官方两个样例和 `start == target`。图像来自官方题面资产。

## Reference

- [官方题目](https://leetcode.cn/problems/even-number-of-knight-moves/)
- [对应知识专题](../../graph/weighted-parity-states.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-10-lc70.md">← [力扣 Top 10] LC 70 爬楼梯 简单</a>
<a class="daily-archive-pager__next" href="codeforces-2247-a.md">[codeforces] CF Round 1111 Div.2 A Zero Sum →</a>
</nav>
