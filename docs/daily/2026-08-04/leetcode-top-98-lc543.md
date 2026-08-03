---
title: "[力扣 Top 98] LC 543 二叉树的直径 简单"
---

# [力扣 Top 98] LC 543 二叉树的直径 简单

<p class="daily-archive-kicker">2026-08-04 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=84d2934b768963a7b650c27aa8315a0e9a062ab69b87d541e2bdcdb52dcfe9e6 -->
## 官方原始信息

- Top 排名：98
- 题号：LC 543
- 官方中文标题：二叉树的直径
- 官方难度：简单
- 官方链接：[二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)

### 原始题意

给定二叉树，返回任意两节点间最长路径的长度；长度按边数计算，路径不一定经过根。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  int diameterOfBinaryTree(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [1,2,3,4,5]
输出：3
解释：路径 [4,2,1,3] 或 [5,2,1,3] 含 3 条边。
```

```text
输入：root = [1,2]
输出：1
```

### 全部约束

- 节点数 $1\le n\le10^4$。
- $-100\le Node.val\le100$。

## 约束推导与后序信息

若一条最长路径的最高节点为 `u`，它由 `u` 左子树中最长向下链和右子树中最长向下链拼成。子树只需向父亲返回一个量：向下最大深度；同时用左右深度之和更新全局直径。$n=10^4$ 要求近线性算法；值与答案无关，最大直径为 $n-1$，`int` 安全。

## 解法递进

### 解法一：把每个节点都当作路径最高点，重复求深度

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int depth(TreeNode* node) {
    if (node == nullptr) {
      return 0;
    }
    return 1 + max(depth(node->left), depth(node->right));
  }
  int enumerate(TreeNode* node) {
    if (node == nullptr) {
      return 0;
    }
    int through = depth(node->left) + depth(node->right);
    return max({through, enumerate(node->left), enumerate(node->right)});
  }
public:
  int diameterOfBinaryTree(TreeNode* root) {
    return enumerate(root);
  }
};
```

最坏时间 $O(n^2)$，递归空间 $O(h)$。瓶颈是同一子树深度被祖先反复计算。

### 最佳实用解：一次后序遍历同时返回深度和更新答案

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int answer = 0;
  int depth(TreeNode* node) {
    if (node == nullptr) {
      return 0;
    }
    int leftDepth = depth(node->left);
    int rightDepth = depth(node->right);
    answer = max(answer, leftDepth + rightDepth);
    return 1 + max(leftDepth, rightDepth);
  }
public:
  int diameterOfBinaryTree(TreeNode* root) {
    depth(root);
    return answer;
  }
};
```

时间 $O(n)$，递归栈 $O(h)$。每个子树信息只计算一次，达到读取输入的下界，推荐优先记忆。

## 正确性证明

对任一节点 `u`，递归返回值按归纳假设是从 `u` 向下到叶子的最大节点数。以 `u` 为最高点的简单路径必须分别取左、右子树中的至多一条向下链，因此最大边数正是 `leftDepth + rightDepth`。树中任意简单路径都有唯一最高节点，算法遍历所有节点并检查这一候选，所以不会遗漏全局直径；取最大值即为答案。

## 样例手推、边界与易错点

在 `[1,2,3,4,5]` 中，节点 2 返回深度 2，并以 `1+1=2` 更新；根节点收到左深度 2、右深度 1，以 3 更新答案。单节点左右深度都为 0，直径为 0。

- 深度按节点数返回，直径按边数更新，两者恰由左右深度之和连接。
- 不能只计算经过根的路径。
- 极端链高达 $10^4$，通常递归可用；更严格栈限制下应改显式后序栈。
- 节点值与直径无关。

## 变种一：带非负边权的树直径

新定义：一般树的边有非负权，求最大权重路径。任选起点做一次最远点搜索，再从该点搜索最远距离。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, long long> farthest(const vector<vector<pair<int, int>>>& graph, int start) {
  pair<int, long long> answer = {start, 0};
  stack<tuple<int, int, long long>> work;
  work.push({start, -1, 0});
  while (!work.empty()) {
    auto [node, parent, distance] = work.top();
    work.pop();
    if (distance > answer.second) {
      answer = {node, distance};
    }
    for (auto [next, weight] : graph[node]) {
      if (next != parent) {
        work.push({next, node, distance + weight});
      }
    }
  }
  return answer;
}
int main() {
  int n;
  cin >> n;
  vector<vector<pair<int, int>>> graph(n);
  for (int i = 1; i < n; ++i) {
    int u, v, weight;
    cin >> u >> v >> weight;
    graph[u].push_back({v, weight});
    graph[v].push_back({u, weight});
  }
  int endpoint = farthest(graph, 0).first;
  cout << farthest(graph, endpoint).second << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。非负权保证最远点性质。

## 变种二：恢复一条直径路径

新定义：除长度外输出节点序列。两次搜索的第二次记录父节点，再从终点回溯。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, vector<int>> search(const vector<vector<int>>& graph, int start) {
  int n = graph.size();
  vector<int> parent(n, -1), distance(n, -1);
  queue<int> work;
  work.push(start);
  distance[start] = 0;
  int far = start;
  while (!work.empty()) {
    int node = work.front();
    work.pop();
    if (distance[node] > distance[far]) {
      far = node;
    }
    for (int next : graph[node]) {
      if (distance[next] == -1) {
        distance[next] = distance[node] + 1;
        parent[next] = node;
        work.push(next);
      }
    }
  }
  return {far, parent};
}
int main() {
  int n;
  cin >> n;
  vector<vector<int>> graph(n);
  for (int i = 1; i < n; ++i) {
    int u, v;
    cin >> u >> v;
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  int first = search(graph, 0).first;
  auto [second, parent] = search(graph, first);
  vector<int> path;
  for (int node = second; node != -1; node = parent[node]) {
    path.push_back(node);
  }
  reverse(path.begin(), path.end());
  cout << path.size() - 1 << '\n';
  for (int node : path) {
    cout << node << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种三：N 叉树直径

新定义：每个节点子节点数任意。对每个节点保留最大的两条子树深度，二者之和形成穿过该点的候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int answer = 0;
int depth(int node, int parent, const vector<vector<int>>& graph) {
  int first = 0;
  int second = 0;
  for (int next : graph[node]) {
    if (next == parent) {
      continue;
    }
    int candidate = 1 + depth(next, node, graph);
    if (candidate > first) {
      second = first;
      first = candidate;
    } else if (candidate > second) {
      second = candidate;
    }
  }
  answer = max(answer, first + second);
  return first;
}
int main() {
  int n;
  cin >> n;
  vector<vector<int>> graph(n);
  for (int i = 1; i < n; ++i) {
    int u, v;
    cin >> u >> v;
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  depth(0, -1, graph);
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(h)$。

## 变种四：只允许经过被启用节点的最长路径

新定义：树中部分节点禁用，路径只能由启用节点组成。禁用节点返回深度 0，并把各启用连通块自然截断。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int answer = 0;
int depth(int node, int parent, const vector<vector<int>>& graph, const vector<int>& enabled) {
  if (!enabled[node]) {
    return 0;
  }
  int first = 0;
  int second = 0;
  for (int next : graph[node]) {
    if (next == parent) {
      continue;
    }
    int candidate = depth(next, node, graph, enabled);
    if (candidate > first) {
      second = first;
      first = candidate;
    } else if (candidate > second) {
      second = candidate;
    }
  }
  answer = max(answer, first + second);
  return 1 + first;
}
int main() {
  int n;
  cin >> n;
  vector<int> enabled(n);
  for (int& value : enabled) {
    cin >> value;
  }
  vector<vector<int>> graph(n);
  for (int i = 1; i < n; ++i) {
    int u, v;
    cin >> u >> v;
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  depth(0, -1, graph, enabled);
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(h)$。若根被禁用，需要对其每个启用邻接分支分别启动；更通用实现可遍历所有未访问启用节点。

## 可复现验证

所有代码块按 GNU++23 编译。最佳后序解与枚举最高点解在随机小树、链、星形树、完全树和单节点上对拍。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/diameter-of-binary-tree/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-97-lc16/">← [力扣 Top 97] LC 16 最接近的三数之和 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-99-lc707/">[力扣 Top 99] LC 707 设计链表 中等 →</a>
</nav>
