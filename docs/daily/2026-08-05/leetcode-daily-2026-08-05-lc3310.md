---
title: "[力扣每日一题] 2026-08-05｜LC 3310 移除可疑的方法"
---

# [力扣每日一题] 2026-08-05｜LC 3310 移除可疑的方法

<p class="daily-archive-kicker">2026-08-05 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b619299c6ff0cada8ab4311a09992da3089e08f03e7bbf9f30b5526cc3a74431 -->
## 官方原始信息

- 日期：2026-08-05（Asia/Shanghai）
- 题号：LC 3310
- 官方中文标题：移除可疑的方法
- 官方难度：中等
- 官方链接：[移除可疑的方法](https://leetcode.cn/problems/remove-methods-from-project/?envType=daily-question&envId=2026-08-05)

### 原始题意

项目有编号 `0..n-1` 的方法，有向边 `[a,b]` 表示方法 `a` 调用 `b`。方法 `k` 有 bug，因此 `k` 以及它直接或间接调用的所有方法都是可疑方法。只有当这组可疑方法没有被组外方法调用时，才能整体移除；能移除则返回全部非可疑方法，否则不移除任何方法并返回全部方法。返回顺序任意。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> remainingMethods(int n, int k, vector<vector<int>>& invocations);
};
```

### 全部官方样例

```text
输入：n = 4, k = 1, invocations = [[1,2],[0,1],[3,2]]
输出：[0,1,2,3]
解释：可疑方法 1、2 分别被组外方法 0、3 调用，所以不能移除任何可疑方法。
```

```text
输入：n = 5, k = 0, invocations = [[1,2],[0,2],[0,1],[3,4]]
输出：[3,4]
解释：可疑集合为 {0,1,2}，没有组外方法调用它们，可以整体移除。
```

```text
输入：n = 3, k = 2, invocations = [[1,2],[0,1],[2,0]]
输出：[]
解释：所有方法都可疑且集合外为空，可以全部移除。
```

### 全部约束

- $1\le n\le10^5$。
- $0\le k<n$。
- $0\le invocations.length\le2\times10^5$。
- 每条调用为 `[a_i,b_i]`，且 $0\le a_i,b_i<n$、$a_i\ne b_i$。
- 调用边互不重复。

## 约束推导与观察

“可疑”就是从 `k` 沿有向调用边可达。先做一次 DFS/BFS 标记集合 `S`，再扫描每条边：若存在 `u` 不在 `S`、`v` 在 `S` 的边，说明组外调用组内，整组不能移除。若没有这种入边，返回补集。

$n+m$ 可达 $3\times10^5$，递归 DFS 可能触发调用栈风险，迭代队列更稳。这里只存下标和布尔标记，无整数溢出。

## 解法递进

### 解法一：为每个方法单独检查是否从 `k` 可达

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool reachable(int start, int target, const vector<vector<int>>& graph) {
    vector<char> seen(graph.size());
    queue<int> pending;
    seen[start] = true;
    pending.push(start);
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      if (node == target) {
        return true;
      }
      for (int next : graph[node]) {
        if (!seen[next]) {
          seen[next] = true;
          pending.push(next);
        }
      }
    }
    return false;
  }
public:
  vector<int> remainingMethods(int n, int k, vector<vector<int>>& invocations) {
    vector<vector<int>> graph(n);
    for (const auto& edge : invocations) {
      graph[edge[0]].push_back(edge[1]);
    }
    vector<char> suspicious(n);
    for (int node = 0; node < n; ++node) {
      suspicious[node] = reachable(k, node, graph);
    }
    for (const auto& edge : invocations) {
      if (!suspicious[edge[0]] && suspicious[edge[1]]) {
        vector<int> all(n);
        iota(all.begin(), all.end(), 0);
        return all;
      }
    }
    vector<int> answer;
    for (int node = 0; node < n; ++node) {
      if (!suspicious[node]) {
        answer.push_back(node);
      }
    }
    return answer;
  }
};
```

时间 $O(n(n+m))$，空间 $O(n+m)$。同一可达前缀被重复遍历，是主要瓶颈。

### 最佳实用解：一次可达性搜索加一次边扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> remainingMethods(int n, int k, vector<vector<int>>& invocations) {
    vector<vector<int>> graph(n);
    for (const auto& edge : invocations) {
      graph[edge[0]].push_back(edge[1]);
    }
    vector<char> suspicious(n);
    queue<int> pending;
    suspicious[k] = true;
    pending.push(k);
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      for (int next : graph[node]) {
        if (!suspicious[next]) {
          suspicious[next] = true;
          pending.push(next);
        }
      }
    }
    for (const auto& edge : invocations) {
      if (!suspicious[edge[0]] && suspicious[edge[1]]) {
        vector<int> all(n);
        iota(all.begin(), all.end(), 0);
        return all;
      }
    }
    vector<int> answer;
    for (int node = 0; node < n; ++node) {
      if (!suspicious[node]) {
        answer.push_back(node);
      }
    }
    return answer;
  }
};
```

时间 $O(n+m)$，空间 $O(n+m)$，达到必须读取全部节点与边的下界。

## 正确性证明

BFS 从 `k` 开始，沿且仅沿调用边扩展，因此标记集合恰是 `k` 可达的全部方法，也就是可疑集合 `S`。题目允许移除 `S` 当且仅当不存在集合外到集合内的调用边；第二次扫描逐条检查了这一条件。若发现阻断边，返回全体方法正是“不移除任何方法”；若不存在，返回 `V\S` 正是移除全部可疑方法后的剩余集合。因此算法总与题意一致。

## 样例手推

样例 1 从 1 到达 2，得到 `S={1,2}`；边 `0→1` 已是组外入边，故返回 0..3。样例 2 得到 `S={0,1,2}`，其余边 `3→4` 完全在补集中，没有组外入边，返回 `[3,4]`。样例 3 的 `S` 是全体，补集为空且不可能存在组外入边，返回空数组。

## 易错点与方案比较

- 调用方向是 `a→b`，可疑集合沿正向边扩展。
- 只检查 `k` 的直接入边不够，任意可疑后代的组外入边都会阻止移除。
- 发现阻断时返回全部方法，不是只保留阻断者。
- 返回顺序任意，但按编号递增最稳定。
- 一次 BFS 已是线性最优，SCC 在单次询问中属于过度建模。

## 变种一：返回全部阻断调用边

新定义：除能否移除外，还要诊断每条组外到可疑集合的边。可达性不变，扫描时收集而非提前返回。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<pair<int, int>> edges(m);
  vector<vector<int>> graph(n);
  for (auto& [from, to] : edges) {
    cin >> from >> to;
    graph[from].push_back(to);
  }
  vector<char> suspicious(n);
  queue<int> pending;
  suspicious[k] = true;
  pending.push(k);
  while (!pending.empty()) {
    int node = pending.front();
    pending.pop();
    for (int next : graph[node]) {
      if (!suspicious[next]) {
        suspicious[next] = true;
        pending.push(next);
      }
    }
  }
  vector<pair<int, int>> blockers;
  for (auto edge : edges) {
    if (!suspicious[edge.first] && suspicious[edge.second]) {
      blockers.push_back(edge);
    }
  }
  cout << blockers.size() << '\n';
  for (auto [from, to] : blockers) {
    cout << from << ' ' << to << '\n';
  }
}
```

时间 $O(n+m)$，空间 $O(n+m+答案数)$。

## 变种二：有多个已知 bug 方法

新定义：给定根集合 `bugs`，所有从任一根可达的方法都可疑。把 BFS 初始化为多源即可，封闭性检查不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m, b;
  cin >> n >> m >> b;
  vector<int> bugs(b);
  for (int& bug : bugs) {
    cin >> bug;
  }
  vector<pair<int, int>> edges(m);
  vector<vector<int>> graph(n);
  for (auto& [from, to] : edges) {
    cin >> from >> to;
    graph[from].push_back(to);
  }
  vector<char> suspicious(n);
  queue<int> pending;
  for (int bug : bugs) {
    if (!suspicious[bug]) {
      suspicious[bug] = true;
      pending.push(bug);
    }
  }
  while (!pending.empty()) {
    int node = pending.front();
    pending.pop();
    for (int next : graph[node]) {
      if (!suspicious[next]) {
        suspicious[next] = true;
        pending.push(next);
      }
    }
  }
  bool removable = all_of(edges.begin(), edges.end(),
      [&](auto edge) { return suspicious[edge.first] || !suspicious[edge.second]; });
  cout << (removable ? "YES" : "NO") << '\n';
}
```

时间 $O(n+m+b)$，空间 $O(n+m)$。逐个根独立 DFS 会重复遍历共享后代。

## 变种三：允许扩大移除集合，求包含原可疑集合的最小可移除闭包

新定义：若组外方法调用待删方法，也允许把该调用者一并删除；反复加入所有反向祖先，得到没有组外入边的最小超集。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<vector<int>> graph(n), reverseGraph(n);
  for (int i = 0, from, to; i < m; ++i) {
    cin >> from >> to;
    graph[from].push_back(to);
    reverseGraph[to].push_back(from);
  }
  vector<char> removed(n);
  queue<int> pending;
  removed[k] = true;
  pending.push(k);
  while (!pending.empty()) {
    int node = pending.front();
    pending.pop();
    for (int next : graph[node]) {
      if (!removed[next]) {
        removed[next] = true;
        pending.push(next);
      }
    }
  }
  for (int node = 0; node < n; ++node) {
    if (removed[node]) {
      pending.push(node);
    }
  }
  while (!pending.empty()) {
    int node = pending.front();
    pending.pop();
    for (int caller : reverseGraph[node]) {
      if (!removed[caller]) {
        removed[caller] = true;
        pending.push(caller);
      }
    }
  }
  for (int node = 0; node < n; ++node) {
    if (removed[node]) {
      cout << node << ' ';
    }
  }
  cout << '\n';
}
```

时间 $O(n+m)$，空间 $O(n+m)$。原题不允许扩大集合，所以遇到祖先时只能全部放弃；新定义改变了决策目标。

## 变种四：同一调用图上多次查询不同 bug 根

新定义：有多次独立 `k`。一般图上每问做线性 BFS；当查询不多时比构建全点可达闭包更省内存。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<pair<int, int>> edges(m);
  vector<vector<int>> graph(n);
  for (auto& [from, to] : edges) {
    cin >> from >> to;
    graph[from].push_back(to);
  }
  while (q--) {
    int k;
    cin >> k;
    vector<char> suspicious(n);
    queue<int> pending;
    suspicious[k] = true;
    pending.push(k);
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      for (int next : graph[node]) {
        if (!suspicious[next]) {
          suspicious[next] = true;
          pending.push(next);
        }
      }
    }
    bool removable = all_of(edges.begin(), edges.end(),
        [&](auto edge) { return suspicious[edge.first] || !suspicious[edge.second]; });
    cout << (removable ? "YES" : "NO") << '\n';
  }
}
```

每问 $O(n+m)$，空间 $O(n+m)$。若查询接近 $n$ 且图的 SCC 数较小，可进一步缩点并使用位集闭包，在时间与 $O(C^2)$ 内存之间权衡。

## 验证说明

本轮将六段代码按 C++23 编译；最佳解会与“逐节点独立可达”的暴力解对拍 50,000 个随机有向图，并覆盖无边、全图可疑、链、环、重复入路径、可疑后代被外部调用和最大稀疏图。每日提交源码另按两空格、多行、100 列门禁重新编译并跑全部官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/remove-methods-from-project/)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-d/">← [codeforces] CF Round 1113 Div.2 D Good Pair Queries</a>
<span class="daily-archive-pager__empty"></span>
</nav>
