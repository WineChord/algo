---
title: "[力扣竞赛] 第 512 场周赛 Q4 LC 4003 交替方向的最小路径代价 III 困难"
---

# [力扣竞赛] 第 512 场周赛 Q4 LC 4003 交替方向的最小路径代价 III 困难

<p class="daily-archive-kicker">2026-08-02 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../graph/weighted-parity-states/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0d3b5c2f19c26e642f214127b48769a7946ba43f745bf6b157223e1307887be2 -->
## 官方原始信息

- 来源：力扣中国
- 比赛：第 512 场周赛
- 比赛题序：Q4
- 题号：LC 4003
- 官方中文标题：交替方向的最小路径代价 III
- 官方难度：困难
- 官方比赛分值：6
- ZeroTracer 社区估算竞赛分：2122.8602053579（抓取于 2026-08-02）
- 官方链接：[交替方向的最小路径代价 III](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-iii/)
- 社区估算来源：[ZeroTracer LeetCode Problem Rating](https://zerotrac.github.io/leetcode_problem_rating/)

### 原始题意

给定 $m\times n$ 网格与非负整数矩阵 `penalty`。进入格子 $(i,j)$ 的代价是 $(i+1)(j+1)$。从 $(0,0)$ 出发时先支付该格入口代价 1，接下来的行动从 1 编号。每次可等待或移动到上下左右相邻格；奇数行动偏好右、下，偶数行动偏好左、上。按偏好移动只支付目标格入口代价；逆偏好移动还要支付出发格的 `penalty`；等待支付当前格的 `penalty`。每次行动后奇偶性都翻转，求首次到达 $(m-1,n-1)$ 的最小总代价。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  long long minCost(int m, int n, vector<vector<int>>& penalty);
};
```

### 全部官方样例

```text
输入：m = 2, n = 2, penalty = [[5,3],[1,4]]
输出：8
解释：先支付 (0,0) 的入口代价 1。行动 1 向下到 (1,0)，支付 2；行动 2 向右到 (1,1)，支付入口代价 4，并因违反偶数行动方向规则支付 penalty[1][0]=1。总计 1+2+4+1=8。
```

```text
输入：m = 2, n = 2, penalty = [[0,7],[3,2]]
输出：7
解释：先支付 1；行动 1 在 (0,0) 等待，代价 0；行动 2 向右，入口代价 2，逆规则惩罚仍为 0；行动 3 向下，入口代价 4。总计 7。
```

```text
输入：m = 2, n = 3, penalty = [[8,0,9],[7,4,1]]
输出：12
解释：先支付 1；依次向右、向右、向下，代价为 2、3+penalty[0][1]、6，即 1+2+3+0+6=12。
```

### 全部约束

- $1\le m,n\le10^5$。
- $2\le mn\le10^5$。
- `penalty.length == m`，`penalty[i].length == n`。
- $0\le penalty[i][j]\le10^5$。

## 约束推导与建模

只把格子作为状态不够：同一格在“下一步为奇数行动”和“下一步为偶数行动”时，边权不同。把状态扩为 $(i,j,p)$，其中 $p=0$ 表示下一行动为奇数，$p=1$ 表示下一行动为偶数。每个状态有至多五条边：等待边留在原格并翻转 $p$；四条移动边到相邻格并翻转 $p$。

所有入口代价和惩罚均非负，因此状态图上的最短路可用 Dijkstra。状态数 $V=2mn\le2\times10^5$，边数 $E\le5V$，二叉堆复杂度 $O(mn\log(mn))$ 可行。一次路径最多可能绕行，不能用只向右下的网格 DP。最坏总成本可超过 32 位，例如大量行动与单步约 $10^{10}$ 的入口乘积上界组合，距离必须用 `long long`。

## 解法递进

### 解法一：状态图 Bellman-Ford

小规模时枚举全部状态并反复松弛所有等待、移动边，直到不再变化。它不依赖非负边权，是正确的暴力 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long minCost(int m, int n, vector<vector<int>>& penalty) {
    int states = 2 * m * n;
    const long long inf = numeric_limits<long long>::max() / 4;
    vector<long long> distance(states, inf);
    auto id = [n](int row, int column, int parity) { return 2 * (row * n + column) + parity; };
    distance[id(0, 0, 0)] = 1;
    const int dr[4] = {0, 1, 0, -1};
    const int dc[4] = {1, 0, -1, 0};
    for (int iteration = 1; iteration < states; ++iteration) {
      bool changed = false;
      vector<long long> next = distance;
      for (int row = 0; row < m; ++row) {
        for (int column = 0; column < n; ++column) {
          for (int parity = 0; parity < 2; ++parity) {
            int from = id(row, column, parity);
            if (distance[from] == inf) {
              continue;
            }
            int waitTo = id(row, column, parity ^ 1);
            long long waitCost = distance[from] + penalty[row][column];
            if (waitCost < next[waitTo]) {
              next[waitTo] = waitCost;
              changed = true;
            }
            for (int direction = 0; direction < 4; ++direction) {
              int newRow = row + dr[direction];
              int newColumn = column + dc[direction];
              if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
                continue;
              }
              bool preferred = parity == 0 ? direction < 2 : direction >= 2;
              long long edge = 1LL * (newRow + 1) * (newColumn + 1);
              if (!preferred) {
                edge += penalty[row][column];
              }
              int to = id(newRow, newColumn, parity ^ 1);
              if (distance[from] + edge < next[to]) {
                next[to] = distance[from] + edge;
                changed = true;
              }
            }
          }
        }
      }
      distance.swap(next);
      if (!changed) {
        break;
      }
    }
    return min(distance[id(m - 1, n - 1, 0)], distance[id(m - 1, n - 1, 1)]);
  }
};
```

时间 $O(VE)=O((mn)^2)$，空间 $O(mn)$，只适合小图对拍。

### 最佳实用解：两层状态图上的 Dijkstra

距离数组把格子与下一行动奇偶性共同编码。优先队列每次取当前最小未确定距离；过期条目直接跳过。首次弹出任一目标格状态时就是全局最优答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long minCost(int m, int n, vector<vector<int>>& penalty) {
    const long long inf = numeric_limits<long long>::max() / 4;
    int states = 2 * m * n;
    vector<long long> distance(states, inf);
    auto id = [n](int row, int column, int parity) { return 2 * (row * n + column) + parity; };
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> queue;
    int start = id(0, 0, 0);
    distance[start] = 1;
    queue.push({1, start});
    const int dr[4] = {0, 1, 0, -1};
    const int dc[4] = {1, 0, -1, 0};
    while (!queue.empty()) {
      auto [currentDistance, state] = queue.top();
      queue.pop();
      if (currentDistance != distance[state]) {
        continue;
      }
      int parity = state & 1;
      int cell = state / 2;
      int row = cell / n;
      int column = cell % n;
      if (row == m - 1 && column == n - 1) {
        return currentDistance;
      }
      auto relax = [&](int to, long long edge) {
        if (currentDistance + edge < distance[to]) {
          distance[to] = currentDistance + edge;
          queue.push({distance[to], to});
        }
      };
      relax(id(row, column, parity ^ 1), penalty[row][column]);
      for (int direction = 0; direction < 4; ++direction) {
        int newRow = row + dr[direction];
        int newColumn = column + dc[direction];
        if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
          continue;
        }
        bool preferred = parity == 0 ? direction < 2 : direction >= 2;
        long long edge = 1LL * (newRow + 1) * (newColumn + 1);
        if (!preferred) {
          edge += penalty[row][column];
        }
        relax(id(newRow, newColumn, parity ^ 1), edge);
      }
    }
    return -1;
  }
};
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。所有边非负且图稀疏，这是本题最稳妥的最优实用解。

## 正确性证明

构造图中，每个真实局面与且仅与一个状态 $(i,j,p)$ 对应。等待边支付当前格惩罚并翻转奇偶；移动边支付目标入口代价，若方向不满足当前奇偶规则再加出发格惩罚，并翻转奇偶。因此任一合法行动序列逐步对应图中一条同权路径，反之每条图路径也逐边还原为合法行动序列，二者总成本相等。

所有边权非负。Dijkstra 的标准不变量是：状态首次以当前最短距离弹出时，该距离已经是从起点到它的最短路。算法枚举了该状态的全部五类合法后继并正确松弛。目标格的两个奇偶状态都代表“已经到达”，所以优先队列首次弹出的目标状态在两者及所有未弹出状态中距离最小，即为所求最小总代价。

## 样例手推

样例 1 起点状态为 `(0,0,奇数)`，距离 1。向下是奇数行动偏好方向，转到 `(1,0,偶数)`，距离 3。此时向右违反偶数方向规则，边权为目标入口 4 加出发格惩罚 1，得到目标距离 8。其他等待或绕行候选由堆按成本比较，均不能更小。

样例 2 中起点等待边权为 0，把状态切到偶数；随后向右虽逆规则，但附加惩罚仍为 0，最终路径成本 7，说明“等待”不能被简单删除。

## 易错点与方案比较

- 状态记录的是“下一次行动”的奇偶性；起点支付入口代价后，下一步为奇数。
- 不论等待、顺规则移动还是逆规则移动，每次行动后都翻转奇偶。
- 逆规则惩罚取移动前的格子，不是目标格。
- 目标格两个奇偶状态都可结束；无需再额外行动。
- 普通网格 DP 忽略回退、等待和奇偶层，会漏解；Dijkstra 比 Bellman-Ford 从二次复杂度降到近线性对数复杂度。

## 变种一：恢复一条最优行动序列

新定义：除最小成本外，还输出一条最优序列。每次成功松弛时记录前驱状态和动作；目标出堆后沿前驱回溯。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n;
  cin >> m >> n;
  vector<vector<int>> penalty(m, vector<int>(n));
  for (auto& row : penalty) {
    for (int& value : row) {
      cin >> value;
    }
  }
  auto id = [n](int row, int column, int parity) { return 2 * (row * n + column) + parity; };
  int states = 2 * m * n;
  const long long inf = numeric_limits<long long>::max() / 4;
  vector<long long> distance(states, inf);
  vector<int> parent(states, -1);
  vector<char> action(states, '?');
  using Entry = pair<long long, int>;
  priority_queue<Entry, vector<Entry>, greater<Entry>> queue;
  distance[id(0, 0, 0)] = 1;
  queue.push({1, id(0, 0, 0)});
  const int dr[4] = {0, 1, 0, -1};
  const int dc[4] = {1, 0, -1, 0};
  const char label[4] = {'R', 'D', 'L', 'U'};
  int target = -1;
  while (!queue.empty()) {
    auto [currentDistance, state] = queue.top();
    queue.pop();
    if (currentDistance != distance[state]) {
      continue;
    }
    int parity = state & 1;
    int cell = state / 2;
    int row = cell / n;
    int column = cell % n;
    if (row == m - 1 && column == n - 1) {
      target = state;
      break;
    }
    auto relax = [&](int to, long long edge, char move) {
      if (currentDistance + edge < distance[to]) {
        distance[to] = currentDistance + edge;
        parent[to] = state;
        action[to] = move;
        queue.push({distance[to], to});
      }
    };
    relax(id(row, column, parity ^ 1), penalty[row][column], 'W');
    for (int direction = 0; direction < 4; ++direction) {
      int newRow = row + dr[direction];
      int newColumn = column + dc[direction];
      if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
        continue;
      }
      bool preferred = parity == 0 ? direction < 2 : direction >= 2;
      long long edge = 1LL * (newRow + 1) * (newColumn + 1);
      if (!preferred) {
        edge += penalty[row][column];
      }
      relax(id(newRow, newColumn, parity ^ 1), edge, label[direction]);
    }
  }
  string path;
  for (int state = target; parent[state] != -1; state = parent[state]) {
    path.push_back(action[state]);
  }
  reverse(path.begin(), path.end());
  cout << distance[target] << '\n' << path << '\n';
}
```

时间与空间仍为 $O(mn\log(mn))$ 和 $O(mn)$，额外保存两个前驱数组。

## 变种二：任意起点、终点与初始奇偶

新定义：输入起点、终点以及下一行动是奇数还是偶数；起点入口代价仍先支付。状态图不变，只需改变起始状态和终止判定。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, startRow, startColumn, targetRow, targetColumn, startParity;
  cin >> m >> n >> startRow >> startColumn >> targetRow >> targetColumn >> startParity;
  vector<vector<int>> penalty(m, vector<int>(n));
  for (auto& row : penalty) {
    for (int& value : row) {
      cin >> value;
    }
  }
  auto id = [n](int row, int column, int parity) { return 2 * (row * n + column) + parity; };
  const long long inf = numeric_limits<long long>::max() / 4;
  vector<long long> distance(2 * m * n, inf);
  using Entry = pair<long long, int>;
  priority_queue<Entry, vector<Entry>, greater<Entry>> queue;
  int start = id(startRow, startColumn, startParity);
  distance[start] = 1LL * (startRow + 1) * (startColumn + 1);
  queue.push({distance[start], start});
  const int dr[4] = {0, 1, 0, -1};
  const int dc[4] = {1, 0, -1, 0};
  while (!queue.empty()) {
    auto [currentDistance, state] = queue.top();
    queue.pop();
    if (currentDistance != distance[state]) {
      continue;
    }
    int parity = state & 1;
    int cell = state / 2;
    int row = cell / n;
    int column = cell % n;
    if (row == targetRow && column == targetColumn) {
      cout << currentDistance << '\n';
      return 0;
    }
    auto relax = [&](int to, long long edge) {
      if (currentDistance + edge < distance[to]) {
        distance[to] = currentDistance + edge;
        queue.push({distance[to], to});
      }
    };
    relax(id(row, column, parity ^ 1), penalty[row][column]);
    for (int direction = 0; direction < 4; ++direction) {
      int newRow = row + dr[direction];
      int newColumn = column + dc[direction];
      if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
        continue;
      }
      bool preferred = parity == 0 ? direction < 2 : direction >= 2;
      long long edge = 1LL * (newRow + 1) * (newColumn + 1);
      edge += preferred ? 0 : penalty[row][column];
      relax(id(newRow, newColumn, parity ^ 1), edge);
    }
  }
}
```

时间 $O(mn\log(mn))$，空间 $O(mn)$。

## 变种三：方向规则按长度 $k$ 的周期变化

新定义：第 $t$ 类行动允许的方向由字符串 `rule[t]` 给出，行动后转到 $(t+1)\bmod k$；逆规则仍支付出发格惩罚。奇偶两层扩展为 $k$ 层。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n, k;
  cin >> m >> n >> k;
  vector<string> rule(k);
  for (string& allowed : rule) {
    cin >> allowed;
  }
  vector<vector<int>> penalty(m, vector<int>(n));
  for (auto& row : penalty) {
    for (int& value : row) {
      cin >> value;
    }
  }
  auto id = [n, k](int row, int column, int phase) { return (row * n + column) * k + phase; };
  const long long inf = numeric_limits<long long>::max() / 4;
  vector<long long> distance(m * n * k, inf);
  using Entry = pair<long long, int>;
  priority_queue<Entry, vector<Entry>, greater<Entry>> queue;
  distance[id(0, 0, 0)] = 1;
  queue.push({1, id(0, 0, 0)});
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  const char label[4] = {'U', 'D', 'L', 'R'};
  while (!queue.empty()) {
    auto [currentDistance, state] = queue.top();
    queue.pop();
    if (currentDistance != distance[state]) {
      continue;
    }
    int phase = state % k;
    int cell = state / k;
    int row = cell / n;
    int column = cell % n;
    if (row == m - 1 && column == n - 1) {
      cout << currentDistance << '\n';
      return 0;
    }
    int nextPhase = (phase + 1) % k;
    auto relax = [&](int to, long long edge) {
      if (currentDistance + edge < distance[to]) {
        distance[to] = currentDistance + edge;
        queue.push({distance[to], to});
      }
    };
    relax(id(row, column, nextPhase), penalty[row][column]);
    for (int direction = 0; direction < 4; ++direction) {
      int newRow = row + dr[direction];
      int newColumn = column + dc[direction];
      if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
        continue;
      }
      long long edge = 1LL * (newRow + 1) * (newColumn + 1);
      if (rule[phase].find(label[direction]) == string::npos) {
        edge += penalty[row][column];
      }
      relax(id(newRow, newColumn, nextPhase), edge);
    }
  }
}
```

状态数变为 $kmn$，时间 $O(kmn\log(kmn))$，空间 $O(kmn)$。

## 变种四：行动代价只有 0 或 1

新定义：取消入口代价；顺规则移动代价 0，等待或逆规则移动代价 1。此时所有边权属于 $\{0,1\}$，二叉堆可替换为 0-1 BFS：0 边压队首，1 边压队尾。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n;
  cin >> m >> n;
  auto id = [n](int row, int column, int parity) { return 2 * (row * n + column) + parity; };
  const int inf = numeric_limits<int>::max() / 4;
  vector<int> distance(2 * m * n, inf);
  deque<int> queue;
  distance[id(0, 0, 0)] = 0;
  queue.push_front(id(0, 0, 0));
  const int dr[4] = {0, 1, 0, -1};
  const int dc[4] = {1, 0, -1, 0};
  while (!queue.empty()) {
    int state = queue.front();
    queue.pop_front();
    int parity = state & 1;
    int cell = state / 2;
    int row = cell / n;
    int column = cell % n;
    auto relax = [&](int to, int weight) {
      if (distance[state] + weight < distance[to]) {
        distance[to] = distance[state] + weight;
        if (weight == 0) {
          queue.push_front(to);
        } else {
          queue.push_back(to);
        }
      }
    };
    relax(id(row, column, parity ^ 1), 1);
    for (int direction = 0; direction < 4; ++direction) {
      int newRow = row + dr[direction];
      int newColumn = column + dc[direction];
      if (newRow < 0 || newRow >= m || newColumn < 0 || newColumn >= n) {
        continue;
      }
      bool preferred = parity == 0 ? direction < 2 : direction >= 2;
      relax(id(newRow, newColumn, parity ^ 1), preferred ? 0 : 1);
    }
  }
  cout << min(distance[id(m - 1, n - 1, 0)], distance[id(m - 1, n - 1, 1)]) << '\n';
}
```

时间 $O(mn)$，空间 $O(mn)$；只有边权严格为 0/1 时才能使用，原题入口代价并不满足这一条件。

## 可复现验证

对随机小网格，逐项比较 Bellman-Ford 与 Dijkstra 的两个目标奇偶状态，并覆盖 $1\times n$、$m\times1$、全零惩罚、最大惩罚、必须等待更优和逆规则直接走更优等情形。三组官方样例均得到 8、7、12。所有代码以 GNU++23 编译，距离统一使用 64 位整数。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-iii/)
- [对应知识专题](../../graph/weighted-parity-states.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-80-lc94/">← [力扣 Top 80] LC 94 二叉树的中序遍历 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-a/">[codeforces] CF Round 1113 Div.2 A You Delete, I Delete →</a>
</nav>
