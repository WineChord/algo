---
title: "[力扣 Top 1] LC 3286 穿越网格图的安全路径 中等"
---

# [力扣 Top 1] LC 3286 穿越网格图的安全路径 中等

<p class="daily-archive-kicker">2026-07-26 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-26 题目列表</a> · <a href="../../../graph/weighted-parity-states/">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/)
- 函数签名：`bool findSafeWalk(vector<vector<int>>& grid, int health)`

### 原始题意

给定一个 $m\times n$ 的二进制网格和初始健康值 `health`。从左上角出发，每次可以向上下左右移动；进入值为 $1$ 的格子会损失 $1$ 点健康，值为 $0$ 的格子不损失。起点和终点同样计算代价，移动全过程以及到达终点时健康值都必须严格为正。判断能否到达右下角。

### 全部官方样例

1. `grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], health = 1`，输出 `true`。存在一条只经过安全格的路径，总损失为 $0$。
2. `grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3`，输出 `false`。最小总损失为 $4$，无法保持健康值为正。
3. `grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5`，输出 `true`。经过中心安全格可把总损失降为 $4$，到达时健康值为 $1$。

### 全部约束

- `m == grid.length`
- `n == grid[i].length`
- $1\le m,n\le 50$
- $2\le m\cdot n$
- $1\le health\le m+n$
- `grid[i][j]` 只能是 $0$ 或 $1$

## 最优结论

把格子视为点、进入相邻格子的值视为边权，问题就是求起点到终点的最小累计损失。边权只有 $0/1$，使用 0-1 BFS：走向 $0$ 权格子放到双端队列前端，走向 $1$ 权格子放到后端。设最小损失为 $d$，答案是 $d<health$。时间 $O(mn)$，空间 $O(mn)$。面试中优先记忆 0-1 BFS；若权值扩展为任意非负数，再切换 Dijkstra。

## 约束、边界与关键观察

- 起点也会扣血，所以初始距离是 `grid[0][0]`，不是 $0$。
- 要求健康值严格为正，因此比较是 `dist < health`，不是 `dist <= health`。
- 每条边权非负，若某条可行游走含环，删除环不会增加损失。因此只考虑简单路径仍覆盖最优解。
- 累计损失沿路径单调不减；只要终点总损失小于 `health`，所有前缀损失也都小于 `health`。
- 网格最多 $2500$ 个点，Dijkstra 足够快；但 $0/1$ 权结构允许进一步消除堆的对数因子。

## 样例手推

样例 3 从 `(0,0)` 进入时损失 $1$。路径 `(0,0)\to(1,0)\to(1,1)\to(1,2)\to(2,2)` 的格子值依次为 $1,1,0,1,1$，累计损失为 $4$。初始健康值为 $5$，到达时剩余 $1>0$，所以返回 `true`。若避开中心的 $0$，任一路径至少经过五个值为 $1$ 的格子，到达时健康值为 $0$，不合法。

## 解法一：枚举所有简单路径

DFS 枚举每条不重复经过格子的路径，携带累计损失；到达终点时判断损失是否小于健康值。它正确但路径数为指数级，只适合作为极小网格的暴力基准。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int m, n, health;
  vector<vector<int>>* g;
  vector<vector<int>> vis;
  bool dfs(int x, int y, int cost) {
    cost += (*g)[x][y];
    if (cost >= health) return false;
    if (x == m - 1 && y == n - 1) return true;
    vis[x][y] = 1;
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (int d = 0; d < 4; ++d) {
      int nx = x + dx[d], ny = y + dy[d];
      if (nx < 0 || nx >= m || ny < 0 || ny >= n || vis[nx][ny]) continue;
      if (dfs(nx, ny, cost)) return true;
    }
    vis[x][y] = 0;
    return false;
  }
public:
  bool findSafeWalk(vector<vector<int>>& grid, int h) {
    g = &grid;
    m = grid.size();
    n = grid[0].size();
    health = h;
    vis.assign(m, vector<int>(n));
    return dfs(0, 0, 0);
  }
};
```

时间最坏为指数级，可粗略写作 $O(4^{mn})$；递归栈与访问标记为 $O(mn)$。

## 解法二：Dijkstra

状态只需记录格子；`dist[x][y]` 表示到达它的最小累计损失。每次从小根堆取当前距离最小的格子并松弛四个邻居。它把指数路径枚举压缩为每个格子的一个最优状态。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool findSafeWalk(vector<vector<int>>& grid, int health) {
    int m = grid.size(), n = grid[0].size();
    const int inf = 1e9;
    vector<vector<int>> dist(m, vector<int>(n, inf));
    using State = tuple<int, int, int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    dist[0][0] = grid[0][0];
    pq.emplace(dist[0][0], 0, 0);
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!pq.empty()) {
      auto [du, x, y] = pq.top();
      pq.pop();
      if (du != dist[x][y]) continue;
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        int nd = du + grid[nx][ny];
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        pq.emplace(nd, nx, ny);
      }
    }
    return dist[m - 1][n - 1] < health;
  }
};
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## 解法三：0-1 BFS（最佳实用解）

Dijkstra 的堆用于在任意非负距离中找最小值；本题新增代价只有 $0$ 或 $1$。若本次松弛代价为 $0$，新状态与当前层同优先级，放队首；代价为 $1$，放队尾。双端队列因此维持与 Dijkstra 相同的非降距离处理顺序。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool findSafeWalk(vector<vector<int>>& grid, int health) {
    int m = grid.size(), n = grid[0].size();
    const int inf = 1e9;
    vector<vector<int>> dist(m, vector<int>(n, inf));
    deque<pair<int, int>> q;
    dist[0][0] = grid[0][0];
    q.push_front({0, 0});
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
      auto [x, y] = q.front();
      q.pop_front();
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        int nd = dist[x][y] + grid[nx][ny];
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        if (grid[nx][ny] == 0)
          q.push_front({nx, ny});
        else
          q.push_back({nx, ny});
      }
    }
    return dist[m - 1][n - 1] < health;
  }
};
```

### 正确性证明

初始状态的距离等于进入起点的损失。每次松弛都把当前最小已知损失加上进入邻格的真实代价，所以所有候选距离都对应实际路径。双端队列把 $0$ 权松弛放在当前层前部、$1$ 权松弛放到后一层，等价于按非降距离执行 Dijkstra；因此松弛结束后 `dist[x][y]` 是到每个格子的最小损失。又因为损失非负，终点最小损失小于 `health` 当且仅当存在全过程健康值严格为正的路径。

### 复杂度与方案比较

- DFS：证明直观，但指数级，只能做小规模 oracle。
- Dijkstra：适配任意非负权，时间 $O(mn\log(mn))$，扩展性最好。
- 0-1 BFS：利用二值权，时间 $O(mn)$、空间 $O(mn)$，本题最简洁高效。

## 常见错误

- 忘记计入 `grid[0][0]`。
- 把严格条件写成 `dist <= health`。
- 用普通 BFS；它只最小化步数，不最小化危险格数量。
- 用“访问过就永不再入队”，阻止更小损失的后续松弛。
- 只向右和向下移动；官方允许四个方向。

## Follow-up 1：恢复一条最小损失路径

为每次成功松弛记录前驱，结束后从终点反向恢复。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<pair<int, int>> safestPath(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    const int inf = 1e9;
    vector<vector<int>> dist(m, vector<int>(n, inf));
    vector<vector<pair<int, int>>> pre(m, vector<pair<int, int>>(n, {-1, -1}));
    deque<pair<int, int>> q;
    dist[0][0] = grid[0][0];
    q.push_front({0, 0});
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
      auto [x, y] = q.front();
      q.pop_front();
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        int nd = dist[x][y] + grid[nx][ny];
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        pre[nx][ny] = {x, y};
        if (grid[nx][ny] == 0)
          q.push_front({nx, ny});
        else
          q.push_back({nx, ny});
      }
    }
    vector<pair<int, int>> path;
    for (pair<int, int> p = {m - 1, n - 1}; p.first != -1; p = pre[p.first][p.second]) {
      path.push_back(p);
    }
    reverse(path.begin(), path.end());
    return path;
  }
};
```

时间和空间仍为 $O(mn)$。

## Follow-up 2：格子损失是任意非负整数

0-1 BFS 失效，因为队首/队尾不能表示多级权重；恢复为 Dijkstra。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool findSafeWalk(vector<vector<int>>& cost, int health) {
    int m = cost.size(), n = cost[0].size();
    vector<vector<long long>> dist(m, vector<long long>(n, LLONG_MAX));
    using State = tuple<long long, int, int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    dist[0][0] = cost[0][0];
    pq.emplace(dist[0][0], 0, 0);
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!pq.empty()) {
      auto [du, x, y] = pq.top();
      pq.pop();
      if (du != dist[x][y]) continue;
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        long long nd = du + cost[nx][ny];
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        pq.emplace(nd, nx, ny);
      }
    }
    return dist[m - 1][n - 1] < health;
  }
};
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## Follow-up 3：同一网格回答多次健康值询问

最小损失与询问无关，只运行一次 0-1 BFS，再对每个健康值判断 `minCost < health`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<bool> canSurvive(vector<vector<int>>& grid, vector<int>& healths) {
    int m = grid.size(), n = grid[0].size();
    const int inf = 1e9;
    vector<vector<int>> dist(m, vector<int>(n, inf));
    deque<pair<int, int>> q;
    dist[0][0] = grid[0][0];
    q.push_front({0, 0});
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
      auto [x, y] = q.front();
      q.pop_front();
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        int nd = dist[x][y] + grid[nx][ny];
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        if (grid[nx][ny] == 0)
          q.push_front({nx, ny});
        else
          q.push_back({nx, ny});
      }
    }
    vector<bool> ans;
    for (int health : healths) ans.push_back(dist[m - 1][n - 1] < health);
    return ans;
  }
};
```

预处理 $O(mn)$，每次询问 $O(1)$。

## Follow-up 4：先最小化损失，再最小化步数

距离改成二元组 `(damage, steps)`，按字典序比较；普通 0-1 BFS 不再足够，使用 Dijkstra。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<int, int> bestRoute(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    using Cost = pair<int, int>;
    const Cost inf = {INT_MAX, INT_MAX};
    vector<vector<Cost>> dist(m, vector<Cost>(n, inf));
    using State = tuple<int, int, int, int>;
    priority_queue<State, vector<State>, greater<State>> pq;
    dist[0][0] = {grid[0][0], 0};
    pq.emplace(grid[0][0], 0, 0, 0);
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    while (!pq.empty()) {
      auto [damage, steps, x, y] = pq.top();
      pq.pop();
      if (dist[x][y] != Cost{damage, steps}) continue;
      for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        Cost nd = {damage + grid[nx][ny], steps + 1};
        if (nd >= dist[nx][ny]) continue;
        dist[nx][ny] = nd;
        pq.emplace(nd.first, nd.second, nx, ny);
      }
    }
    return dist[m - 1][n - 1];
  }
};
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## Reference

- 官方题面与接口：[打开力扣中国页面](https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/)
- [对应知识专题](../../graph/weighted-parity-states.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc468-a/">← [atcoder] ABC468 A Maximal Value</a>
<a class="daily-archive-pager__next" href="../leetcode-top-2-lc1/">[力扣 Top 2] LC 1 两数之和 简单 →</a>
</nav>
