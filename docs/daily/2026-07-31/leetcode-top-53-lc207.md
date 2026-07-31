---
title: "[力扣 Top 53] LC 207 课程表 中等"
---

# [力扣 Top 53] LC 207 课程表 中等

<p class="daily-archive-kicker">2026-07-31 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../graph/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=6ddb012959f81c1b237a8a6effa9e3225036295325c717ed2ebadc46898a2921 -->
## 官方原始信息

- Top 排名：53
- 题号：LC 207
- 官方中文标题：课程表
- 官方难度：中等
- 官方链接：[课程表](https://leetcode.cn/problems/course-schedule/)

### 原始题意

有 `numCourses` 门课程，编号为 0 到 `numCourses - 1`。先修关系 `[a,b]` 表示学习 `a` 前必须先完成 `b`。判断能否完成所有课程。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool canFinish(int numCourses, vector<vector<int>>& prerequisites);
};
```

### 全部官方样例

```text
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：先学课程 0，再学课程 1。
```

```text
输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
解释：两门课程互相依赖，形成环。
```

### 全部约束

- $1\le numCourses\le2000$。
- $0\le prerequisites.length\le5000$。
- 每个先修关系长度为 2。
- $0\le a_i,b_i<numCourses$。
- 所有先修课程对互不相同。

## 约束推导与建模

把先修关系 `[a,b]` 建成有向边 $b\to a$。所有课程能完成，当且仅当该有向图无环，也等价于存在包含全部顶点的拓扑序。顶点和边规模允许 $O(V+E)$ 图算法；递归 DFS 需留意栈深，Kahn 算法更稳定。

## 解法递进

### 解法一：反复扫描可修课程

每轮找入度为零且尚未删除的课程，再扫描全部边更新入度。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
    vector<int> indegree(numCourses);
    for (const auto& edge : prerequisites) {
      ++indegree[edge[0]];
    }
    vector<char> removed(numCourses);
    for (int step = 0; step < numCourses; ++step) {
      int course = -1;
      for (int i = 0; i < numCourses; ++i) {
        if (!removed[i] && indegree[i] == 0) {
          course = i;
          break;
        }
      }
      if (course == -1) {
        return false;
      }
      removed[course] = true;
      for (const auto& edge : prerequisites) {
        if (edge[1] == course) {
          --indegree[edge[0]];
        }
      }
    }
    return true;
  }
};
```

时间 $O(V(V+E))$，空间 $O(V)$。

### 最佳实用解：Kahn 拓扑排序

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
    vector<vector<int>> graph(numCourses);
    vector<int> indegree(numCourses);
    for (const auto& edge : prerequisites) {
      graph[edge[1]].push_back(edge[0]);
      ++indegree[edge[0]];
    }
    queue<int> pending;
    for (int course = 0; course < numCourses; ++course) {
      if (indegree[course] == 0) {
        pending.push(course);
      }
    }
    int completed = 0;
    while (!pending.empty()) {
      int course = pending.front();
      pending.pop();
      ++completed;
      for (int next : graph[course]) {
        if (--indegree[next] == 0) {
          pending.push(next);
        }
      }
    }
    return completed == numCourses;
  }
};
```

时间 $O(V+E)$，空间 $O(V+E)$。

## 正确性证明

入度为零的课程没有尚未完成的前置要求，可以安全加入学习顺序；删除它及其出边后，同样判断剩余图。若算法删除全部顶点，删除顺序就是合法拓扑序。若队列提前为空，剩余每个顶点入度都大于零；从任一点沿前驱不断走，有限图中必然重复顶点，因而存在环，所有环上课程互相等待，无法全部完成。

## 样例手推

`[[1,0]]` 的入度为 `[0,1]`，先弹出 0，把课程 1 的入度降为 0，再弹出 1。第二个样例初始入度均为 1，队列为空，立即判定有环。

## 易错点与方案比较

- `[a,b]` 的边方向是 $b\to a$，不是反过来。
- 最终要比较已弹出顶点数，而非只看队列是否曾经非空。
- DFS 三色标记也是 $O(V+E)$，适合顺便恢复环；Kahn 无递归深度风险，推荐作为默认实现。
- 重复边虽被官方排除，但通用实现若允许重复边，建图与入度必须同时保留或同时去重。

## 变种一：返回一份合法学习顺序

若有环输出 -1，否则输出 Kahn 算法得到的拓扑序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<int>> graph(n);
  vector<int> indegree(n);
  while (m--) {
    int course, prerequisite;
    cin >> course >> prerequisite;
    graph[prerequisite].push_back(course);
    ++indegree[course];
  }
  priority_queue<int, vector<int>, greater<int>> pending;
  for (int i = 0; i < n; ++i) {
    if (indegree[i] == 0) {
      pending.push(i);
    }
  }
  vector<int> order;
  while (!pending.empty()) {
    int current = pending.top();
    pending.pop();
    order.push_back(current);
    for (int next : graph[current]) {
      if (--indegree[next] == 0) {
        pending.push(next);
      }
    }
  }
  if (static_cast<int>(order.size()) != n) {
    cout << -1 << '\n';
    return 0;
  }
  for (int i = 0; i < n; ++i) {
    cout << order[i] << " \n"[i + 1 == n];
  }
}
```

使用小根堆可得到字典序最小拓扑序，时间 $O((V+E)\log V)$。

## 变种二：恢复一条依赖环

三色 DFS 中遇到指向灰色顶点的边时，沿父指针恢复环。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> graph;
vector<int> color;
vector<int> parentNode;
vector<int> cycle;
bool dfs(int current) {
  color[current] = 1;
  for (int next : graph[current]) {
    if (color[next] == 0) {
      parentNode[next] = current;
      if (dfs(next)) {
        return true;
      }
    } else if (color[next] == 1) {
      cycle.push_back(next);
      for (int node = current; node != next; node = parentNode[node]) {
        cycle.push_back(node);
      }
      cycle.push_back(next);
      reverse(cycle.begin(), cycle.end());
      return true;
    }
  }
  color[current] = 2;
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  graph.assign(n, {});
  color.assign(n, 0);
  parentNode.assign(n, -1);
  while (m--) {
    int course, prerequisite;
    cin >> course >> prerequisite;
    graph[prerequisite].push_back(course);
  }
  for (int i = 0; i < n && cycle.empty(); ++i) {
    if (color[i] == 0) {
      dfs(i);
    }
  }
  if (cycle.empty()) {
    cout << -1 << '\n';
  } else {
    for (int i = 0; i < static_cast<int>(cycle.size()); ++i) {
      cout << cycle[i] << " \n"[i + 1 == static_cast<int>(cycle.size())];
    }
  }
}
```

时间 $O(V+E)$，空间 $O(V+E)$。

## 变种三：每学期可并行修任意多门，求最少学期

每一轮同时取出当前所有入度为零的课程；轮数就是最长依赖链长度。若有环输出 -1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<int>> graph(n);
  vector<int> indegree(n);
  while (m--) {
    int course, prerequisite;
    cin >> course >> prerequisite;
    graph[prerequisite].push_back(course);
    ++indegree[course];
  }
  queue<int> pending;
  for (int i = 0; i < n; ++i) {
    if (indegree[i] == 0) {
      pending.push(i);
    }
  }
  int semesters = 0;
  int completed = 0;
  while (!pending.empty()) {
    int layerSize = pending.size();
    ++semesters;
    while (layerSize--) {
      int current = pending.front();
      pending.pop();
      ++completed;
      for (int next : graph[current]) {
        if (--indegree[next] == 0) {
          pending.push(next);
        }
      }
    }
  }
  cout << (completed == n ? semesters : -1) << '\n';
}
```

时间 $O(V+E)$，空间 $O(V+E)$。

## 变种四：在线增加先修关系并逐次询问

每次永久加入一条边后重新运行 Kahn 算法。它不是最强动态拓扑结构，但定义清楚、实现稳定，适合中等规模。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool acyclic(const vector<vector<int>>& graph) {
  int n = graph.size();
  vector<int> indegree(n);
  for (const auto& edges : graph) {
    for (int next : edges) {
      ++indegree[next];
    }
  }
  queue<int> pending;
  for (int i = 0; i < n; ++i) {
    if (indegree[i] == 0) {
      pending.push(i);
    }
  }
  int count = 0;
  while (!pending.empty()) {
    int current = pending.front();
    pending.pop();
    ++count;
    for (int next : graph[current]) {
      if (--indegree[next] == 0) {
        pending.push(next);
      }
    }
  }
  return count == n;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<vector<int>> graph(n);
  while (m--) {
    int course, prerequisite;
    cin >> course >> prerequisite;
    graph[prerequisite].push_back(course);
  }
  while (q--) {
    int course, prerequisite;
    cin >> course >> prerequisite;
    graph[prerequisite].push_back(course);
    cout << (acyclic(graph) ? "YES\n" : "NO\n");
  }
}
```

若当前边数为 $E$，每次查询 $O(V+E)$，总空间 $O(V+E)$。

## 可复现验证

对不超过 8 个顶点的随机有向图，把 Kahn 结果与枚举全部顶点排列是否存在合法拓扑序逐例比较；另覆盖空边图、自环、单环和多个连通分量。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/course-schedule/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/course-schedule/)
- [对应知识专题](../../graph/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-52-lc55/">← [力扣 Top 52] LC 55 跳跃游戏 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-54-lc240/">[力扣 Top 54] LC 240 搜索二维矩阵 II 中等 →</a>
</nav>
