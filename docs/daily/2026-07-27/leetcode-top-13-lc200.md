---
title: "[力扣 Top 13] LC 200 岛屿数量 中等"
---

# [力扣 Top 13] LC 200 岛屿数量 中等

<p class="daily-archive-kicker">2026-07-27 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

官方题目：[打开官方题面](https://leetcode.cn/problems/number-of-islands/)

## 官方原始信息

- 题号：200
- 官方中文标题：岛屿数量
- 官方英文标题：Number of Islands
- slug：`number-of-islands`
- 官方难度：中等
- 函数签名：`int numIslands(vector<vector<char>>& grid)`
- 官方竞赛归属与分值：未发现官方竞赛归属，官方分值未知
- ZeroTracer 社区估算竞赛分：无。2026-07-27 检索其公开 `data.json`，该 slug 不在数据集中；这类非竞赛题不据主观难度补分

### 原始题意

给定只含字符 `'0'` 与 `'1'` 的二维网格。`'1'` 表示陆地，`'0'` 表示水；上下左右相邻的陆地属于同一座岛，斜对角不连通。网格边界外视为水，返回岛屿总数。

### 全部官方样例

样例 1：

```text
grid = [
  ['1','1','1','1','0'],
  ['1','1','0','1','0'],
  ['1','1','0','0','0'],
  ['0','0','0','0','0']
]
输出：1
```

样例 2：

```text
grid = [
  ['1','1','0','0','0'],
  ['1','1','0','0','0'],
  ['0','0','1','0','0'],
  ['0','0','0','1','1']
]
输出：3
```

### 全部官方约束

- `m == grid.length`
- `n == grid[i].length`
- $1\le m,n\le 300$
- `grid[i][j]` 为 `'0'` 或 `'1'`

## 约束推导、样例与边界

网格最多有 $9\times 10^4$ 个格子。把每个陆地格看成图节点、四邻陆地间看成无向边，题目就是求隐式图的连通分量数。任何算法至少要查看所有格子才能区分“全水”和“最后一个格子是陆地”，因此时间下界是 $\Omega(mn)$；一次遍历的洪泛搜索已经达到最优时间。

样例 2 中，从左上角开始只能覆盖左上 $2\times2$ 陆块；位于 `(2,2)` 的单格陆地与右下两格陆地均不四连通，所以依次启动三次搜索，答案为 3。

真正相关的边界：

- 单格水域 `[['0']]`：答案 0。
- 单格陆地 `[['1']]`：答案 1。
- 全陆地：无论形状多大都只有一座岛。
- 棋盘格：每个 `'1'` 都可能是独立岛屿，岛数可达 $\lceil mn/2\rceil$。
- 只有斜角接触：仍属于不同岛屿。
- $300\times300$ 全陆地时，递归 DFS 深度可能接近 $mn$，在栈较小的环境中有栈溢出风险。

## 解法一：显式建图后统计连通分量

最直观的图论写法为每个陆地格建立节点，并枚举右、下邻居建立双向边；随后对每个尚未访问的陆地节点启动 DFS。每次启动恰好对应一个连通分量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numIslands(vector<vector<char>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<vector<int>> graph(m * n);
    static const int dx[2] = {1, 0};
    static const int dy[2] = {0, 1};
    for (int x = 0; x < m; ++x) {
      for (int y = 0; y < n; ++y) {
        if (grid[x][y] != '1') continue;
        int u = x * n + y;
        for (int d = 0; d < 2; ++d) {
          int nx = x + dx[d], ny = y + dy[d];
          if (nx >= m || ny >= n || grid[nx][ny] != '1') continue;
          int v = nx * n + ny;
          graph[u].push_back(v);
          graph[v].push_back(u);
        }
      }
    }
    vector<char> seen(m * n);
    int ans = 0;
    for (int x = 0; x < m; ++x) {
      for (int y = 0; y < n; ++y) {
        int s = x * n + y;
        if (grid[x][y] != '1' || seen[s]) continue;
        ++ans;
        stack<int> st;
        st.push(s);
        seen[s] = 1;
        while (!st.empty()) {
          int u = st.top();
          st.pop();
          for (int v : graph[u]) {
            if (seen[v]) continue;
            seen[v] = 1;
            st.push(v);
          }
        }
      }
    }
    return ans;
  }
};
```

时间复杂度 $O(mn)$，显式邻接表与访问数组占 $O(mn)$ 空间。瓶颈不是时间，而是把规则固定的四邻关系重复存了一遍。

## 解法二：隐式图 BFS

搜索时现场计算四个邻居，不再建邻接表。`seen` 保证每个陆地格只进入队列一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numIslands(vector<vector<char>>& grid) {
    int m = grid.size(), n = grid[0].size(), ans = 0;
    vector<vector<char>> seen(m, vector<char>(n));
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (int sx = 0; sx < m; ++sx) {
      for (int sy = 0; sy < n; ++sy) {
        if (grid[sx][sy] != '1' || seen[sx][sy]) continue;
        ++ans;
        queue<pair<int, int>> q;
        q.push({sx, sy});
        seen[sx][sy] = 1;
        while (!q.empty()) {
          auto [x, y] = q.front();
          q.pop();
          for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
            if (grid[nx][ny] != '1' || seen[nx][ny]) continue;
            seen[nx][ny] = 1;
            q.push({nx, ny});
          }
        }
      }
    }
    return ans;
  }
};
```

时间复杂度 $O(mn)$，额外空间 $O(mn)$。它比显式建图少一层数据结构，且不修改输入。

## 解法三：原地标记的迭代 DFS（最佳实用解）

若允许修改 `grid`，发现新岛时把搜索到的每个 `'1'` 改成 `'0'`。网格自身就承担访问标记；使用显式栈避开深递归风险。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numIslands(vector<vector<char>>& grid) {
    int m = grid.size(), n = grid[0].size(), ans = 0;
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (int sx = 0; sx < m; ++sx) {
      for (int sy = 0; sy < n; ++sy) {
        if (grid[sx][sy] != '1') continue;
        ++ans;
        stack<pair<int, int>> st;
        st.push({sx, sy});
        grid[sx][sy] = '0';
        while (!st.empty()) {
          auto [x, y] = st.top();
          st.pop();
          for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
            if (grid[nx][ny] != '1') continue;
            grid[nx][ny] = '0';
            st.push({nx, ny});
          }
        }
      }
    }
    return ans;
  }
};
```

### 正确性证明

对外层扫描归纳。扫描到某个尚为 `'1'` 的格子时，它不可能属于此前发现的岛，否则此前洪泛搜索已沿四邻路径访问并把它改为 `'0'`；因此它属于一座尚未计数的新岛。随后 DFS 沿全部四邻陆地边扩展，既不会越过水域进入另一座岛，也会到达该岛中所有与起点连通的陆地格，所以恰好把这一整座岛标记。每座岛只会触发一次计数，最终 `ans` 等于岛屿数。

时间复杂度 $O(mn)$。显式栈最坏占 $O(mn)$；除搜索栈外不再分配访问矩阵。面试中优先记忆“外层扫描 + 洪泛搜索”这一不变量；实现时若题目允许改输入，推荐原地迭代 DFS，若不允许则选 BFS + `seen`。

## 同阶方案比较与常见错误

- BFS、递归 DFS、迭代 DFS 都是 $O(mn)$。BFS 队列峰值常与波前宽度相关；递归 DFS 最短但有栈深风险；迭代 DFS 的资源行为最可控。
- 并查集同样可做到近似 $O(mn)$，但静态单次查询的常数和代码量都更大；它真正擅长“陆地逐次加入”的动态变种。
- 显式建图的证明最贴近“连通分量”，但存储固定邻接关系没有必要。

常见错误：

- 把斜对角也当作连通。
- 在出队/弹栈时才标记，导致同一格被多次入队。
- 忘记输入可能只有一行或一列。
- 原地修改输入后仍假设调用者可以复用原网格。
- 递归 DFS 未考虑 $9\times10^4$ 深度的最坏链状岛。

## Follow-up 1：八方向相邻也算同一岛

### 新定义与变化

上下左右和四个对角方向均可连通。原框架仍成立，只需把邻接关系从 4 个方向扩成 8 个；原答案可能变小，因为原先分离的斜角陆地会合并。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numIslands8(vector<vector<char>> grid) {
    int m = grid.size(), n = grid[0].size(), ans = 0;
    for (int sx = 0; sx < m; ++sx) {
      for (int sy = 0; sy < n; ++sy) {
        if (grid[sx][sy] != '1') continue;
        ++ans;
        queue<pair<int, int>> q;
        q.push({sx, sy});
        grid[sx][sy] = '0';
        while (!q.empty()) {
          auto [x, y] = q.front();
          q.pop();
          for (int dx = -1; dx <= 1; ++dx) {
            for (int dy = -1; dy <= 1; ++dy) {
              if (dx == 0 && dy == 0) continue;
              int nx = x + dx, ny = y + dy;
              if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
              if (grid[nx][ny] != '1') continue;
              grid[nx][ny] = '0';
              q.push({nx, ny});
            }
          }
        }
      }
    }
    return ans;
  }
};
```

时间 $O(mn)$，空间 $O(mn)$。

## Follow-up 2：陆地在线加入后的岛数（LC 305 模型）

### 新定义与变化

初始全水，每次把一个位置变成陆地，并立即返回当前岛数。每次重新洪泛整个网格会达到 $O(qmn)$；并查集可以维护连通分量合并。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> p, sz;
  int find(int x) {
    return p[x] == x ? x : p[x] = find(p[x]);
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b);
    p[b] = a;
    sz[a] += sz[b];
    return true;
  }
public:
  vector<int> numIslands2(int m, int n, vector<vector<int>>& positions) {
    p.resize(m * n);
    iota(p.begin(), p.end(), 0);
    sz.assign(m * n, 1);
    vector<char> land(m * n);
    vector<int> ans;
    int count = 0;
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (auto& pos : positions) {
      int x = pos[0], y = pos[1], u = x * n + y;
      if (!land[u]) {
        land[u] = 1;
        ++count;
        for (int d = 0; d < 4; ++d) {
          int nx = x + dx[d], ny = y + dy[d];
          if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
          int v = nx * n + ny;
          if (land[v] && unite(u, v)) --count;
        }
      }
      ans.push_back(count);
    }
    return ans;
  }
};
```

若有 $q$ 次操作，时间 $O((mn+q)\alpha(mn))$，空间 $O(mn)$。重复添加同一位置必须保持岛数不变。

## Follow-up 3：不同形状的岛屿数量

### 新定义与变化

平移后形状相同的岛视为同一种，旋转和翻转暂不等价。只计岛数不再够用；每次洪泛时记录所有格子相对起点的坐标，并排序形成规范表示。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numDistinctIslands(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    set<vector<pair<int, int>>> shapes;
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (int sx = 0; sx < m; ++sx) {
      for (int sy = 0; sy < n; ++sy) {
        if (grid[sx][sy] == 0) continue;
        vector<pair<int, int>> shape;
        stack<pair<int, int>> st;
        st.push({sx, sy});
        grid[sx][sy] = 0;
        while (!st.empty()) {
          auto [x, y] = st.top();
          st.pop();
          shape.push_back({x - sx, y - sy});
          for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
            if (grid[nx][ny] == 0) continue;
            grid[nx][ny] = 0;
            st.push({nx, ny});
          }
        }
        sort(shape.begin(), shape.end());
        shapes.insert(shape);
      }
    }
    return shapes.size();
  }
};
```

设陆地数为 $L$，时间 $O(mn+L\log L)$，空间 $O(L)$。排序消除了 DFS 访问顺序的影响。

## Follow-up 4：最多把一个水格改为陆地后的最大岛（LC 827）

### 新定义与变化

目标从“数连通分量”变为“选择一个水格合并相邻分量并最大化面积”。先给每座岛染不同编号并记录面积，再枚举每个水格，只把四邻出现的不同编号面积相加一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestIsland(vector<vector<int>>& grid) {
    int n = grid.size(), id = 2, ans = 0;
    vector<int> area(2, 0);
    static const int dx[4] = {1, -1, 0, 0};
    static const int dy[4] = {0, 0, 1, -1};
    for (int sx = 0; sx < n; ++sx) {
      for (int sy = 0; sy < n; ++sy) {
        if (grid[sx][sy] != 1) continue;
        int count = 0;
        stack<pair<int, int>> st;
        st.push({sx, sy});
        grid[sx][sy] = id;
        while (!st.empty()) {
          auto [x, y] = st.top();
          st.pop();
          ++count;
          for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
            if (grid[nx][ny] != 1) continue;
            grid[nx][ny] = id;
            st.push({nx, ny});
          }
        }
        area.push_back(count);
        ans = max(ans, count);
        ++id;
      }
    }
    for (int x = 0; x < n; ++x) {
      for (int y = 0; y < n; ++y) {
        if (grid[x][y] != 0) continue;
        int cur = 1;
        int ids[4], count = 0;
        for (int d = 0; d < 4; ++d) {
          int nx = x + dx[d], ny = y + dy[d];
          if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
          int v = grid[nx][ny];
          if (v < 2 || find(ids, ids + count, v) != ids + count) continue;
          ids[count++] = v;
          cur += area[v];
        }
        ans = max(ans, cur);
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$（编号直接存入输入网格，面积表至多 $n^2$ 项）。若全是陆地，没有水格可枚举，初次染色得到的 $n^2$ 已保存在 `ans`。

## 可复现验证

- 官方元数据与题面通过力扣中国 GraphQL `question(titleSlug: "number-of-islands")` 于 2026-07-27 核对。
- 评分数据通过 ZeroTracer `data.json` 于 2026-07-27 检索，未发现该 slug。
- 本文全部 C++ 代码块应以 C++23 独立语法编译；基础最优解另以小网格穷举连通分量作 oracle 随机对拍。

## Reference

- [力扣中国 LC 200 官方题面](https://leetcode.cn/problems/number-of-islands/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/number-of-islands/)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-12-lc560/">← [力扣 Top 12] LC 560 和为 K 的子数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-14-lc11/">[力扣 Top 14] LC 11 盛最多水的容器 中等 →</a>
</nav>
