---
title: "[力扣 Top 42] LC 124 二叉树中的最大路径和 困难"
---

# [力扣 Top 42] LC 124 二叉树中的最大路径和 困难

<p class="daily-archive-kicker">2026-07-30 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=909cb5140010f11d55a938862dd1e2b9f32add7a3ce98fa3f2a5e1fff6d0b97e -->
## 官方原始信息

- Top 排名：42
- 题号：LC 124
- 官方中文标题：二叉树中的最大路径和
- 官方难度：困难
- 官方链接：[二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/)

### 原始题意

二叉树中的路径是由相邻节点连接而成、节点不重复且至少包含一个节点的序列；路径不必经过根。路径和是其中所有节点值之和，求整棵树的最大路径和。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  int maxPathSum(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [1,2,3]
输出：6
解释：最优路径为 2 -> 1 -> 3。
```

```text
输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径为 15 -> 20 -> 7。
```

### 全部约束

- 节点数在 $[1,3\times10^4]$ 内。
- $-1000\le Node.val\le1000$。
- 路径至少选择一个节点，因此全负树的答案仍是某个负数。
- 最大绝对路径和不超过 $3\times10^7$，`int` 足够。

## 约束推导与核心模型

枚举路径端点会达到 $O(n^2)$。树上任意简单路径都有唯一最高节点：路径要么只进入它的一棵子树，要么由左侧向上到该节点再向右侧下去。这提示一次后序遍历同时维护：

- 向父节点返回的“单臂贡献”：必须从当前节点出发，只能选择左、右一侧；
- 在当前节点封口的“双臂答案”：可同时接入左右两侧，但不能继续向父亲返回。

## 解法递进

### 解法一：枚举每个节点作为路径起点

先把树转成无向图，再从每个起点遍历所有不回头路径。树中两点间路径唯一，因此能覆盖每条路径，但时间 $O(n^2)$、空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
};
class Solution {
  void collect(TreeNode* node, vector<TreeNode*>& nodes,
      unordered_map<TreeNode*, vector<TreeNode*>>& graph) {
    if (node == nullptr) {
      return;
    }
    nodes.push_back(node);
    if (node->left != nullptr) {
      graph[node].push_back(node->left);
      graph[node->left].push_back(node);
      collect(node->left, nodes, graph);
    }
    if (node->right != nullptr) {
      graph[node].push_back(node->right);
      graph[node->right].push_back(node);
      collect(node->right, nodes, graph);
    }
  }
  void walk(TreeNode* node, TreeNode* parent, int sum,
      unordered_map<TreeNode*, vector<TreeNode*>>& graph, int& answer) {
    sum += node->val;
    answer = max(answer, sum);
    for (TreeNode* next : graph[node]) {
      if (next != parent) {
        walk(next, node, sum, graph, answer);
      }
    }
  }
public:
  int maxPathSum(TreeNode* root) {
    vector<TreeNode*> nodes;
    unordered_map<TreeNode*, vector<TreeNode*>> graph;
    collect(root, nodes, graph);
    int answer = numeric_limits<int>::min();
    for (TreeNode* start : nodes) {
      walk(start, nullptr, 0, graph, answer);
    }
    return answer;
  }
};
```

### 最佳实用解：后序树形动态规划

令 `gain(node)` 为从 `node` 出发向下延伸、且最多选择一棵子树的最大和。负贡献不如不接，故：

$$
g(u)=val_u+\max(0,g(\mathrm{left}_u),g(\mathrm{right}_u)).
$$

以 `u` 为最高节点封口的候选路径为：

$$
val_u+\max(0,g(\mathrm{left}_u))+\max(0,g(\mathrm{right}_u)).
$$

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
};
class Solution {
  int answer;
  int gain(TreeNode* node) {
    if (node == nullptr) {
      return 0;
    }
    int left = max(0, gain(node->left));
    int right = max(0, gain(node->right));
    answer = max(answer, node->val + left + right);
    return node->val + max(left, right);
  }
public:
  int maxPathSum(TreeNode* root) {
    answer = numeric_limits<int>::min();
    gain(root);
    return answer;
  }
};
```

时间复杂度 $O(n)$，递归空间 $O(h)$，其中 $h$ 是树高；最坏退化为 $O(n)$。

## 正确性证明

引理一：`gain(u)` 等于从 `u` 出发向下的最大单臂路径和。任何能继续交给父节点的简单路径到 `u` 后最多进入一棵子树，否则会在 `u` 分叉而不再是一条路径；负子树贡献应舍弃。递推因此完整且最优。

引理二：任意简单路径都有唯一深度最小的节点 `u`。路径在 `u` 左右各至多进入一棵子树，所以它的最大可能和恰由 `u` 的左右非负单臂贡献加上 `u` 本身给出。

算法枚举每个节点作为这个唯一最高节点，因而不会漏掉全局最优路径；取所有候选最大值即为答案。

## 样例手推

在 `[-10,9,20,null,null,15,7]` 中，节点 15、7 的单臂贡献分别为 15、7。节点 20 的封口候选为 $15+20+7=42$，向上只返回 $20+\max(15,7)=35$。根节点 -10 即使接入 9 和 35 也只有 34，所以全局答案保持 42。

## 易错点与方案比较

- 全负树不能把全局答案初始化为 0，应初始化为最小整数。
- 向父节点只能返回一侧；左右两侧同时使用的路径必须在当前节点封口。
- `max(0, childGain)` 是舍弃负贡献，不是允许空路径作为最终答案。
- 节点值总和在 `int` 内，但若约束放大应改用 `long long`。
- 递归写法最清晰；极深树且语言栈较小时可改成显式后序栈。

## 变种一：要求路径必须经过根节点

新定义：路径至少包含根，并可分别向左右子树延伸。只需计算根的两侧最大向下贡献。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long value;
  int left;
  int right;
};
long long gain(int u, const vector<Node>& tree) {
  if (u == -1) {
    return 0;
  }
  long long left = max(0LL, gain(tree[u].left, tree));
  long long right = max(0LL, gain(tree[u].right, tree));
  return tree[u].value + max(left, right);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> tree(n);
  for (Node& node : tree) {
    cin >> node.value >> node.left >> node.right;
  }
  long long left = max(0LL, gain(tree[0].left, tree));
  long long right = max(0LL, gain(tree[0].right, tree));
  cout << tree[0].value + left + right << '\n';
}
```

时间 $O(n)$，递归空间 $O(h)$。原算法仍成立，但不再对所有节点更新全局答案。

## 变种二：恢复最大路径上的节点

新定义：返回最大和以及对应节点序列。保存每个单臂贡献选择的下一节点，并记录最佳封口节点与是否采用左右臂。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long value;
  int left;
  int right;
};
long long answer;
int center;
vector<long long> down;
vector<int> next_child;
long long dfs(int u, const vector<Node>& tree) {
  if (u == -1) {
    return 0;
  }
  long long left = max(0LL, dfs(tree[u].left, tree));
  long long right = max(0LL, dfs(tree[u].right, tree));
  long long candidate = tree[u].value + left + right;
  if (candidate > answer) {
    answer = candidate;
    center = u;
  }
  next_child[u] = left >= right && left > 0 ? tree[u].left : (right > 0 ? tree[u].right : -1);
  return down[u] = tree[u].value + max(left, right);
}
vector<int> arm(int u) {
  vector<int> result;
  while (u != -1 && down[u] > 0) {
    result.push_back(u);
    u = next_child[u];
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> tree(n);
  for (Node& node : tree) {
    cin >> node.value >> node.left >> node.right;
  }
  answer = numeric_limits<long long>::min();
  center = -1;
  down.assign(n, 0);
  next_child.assign(n, -1);
  dfs(0, tree);
  vector<int> left = arm(tree[center].left);
  vector<int> right = arm(tree[center].right);
  reverse(left.begin(), left.end());
  vector<int> path = left;
  path.push_back(center);
  path.insert(path.end(), right.begin(), right.end());
  cout << answer << '\n';
  for (int node : path) {
    cout << node << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。若一侧单臂贡献非正，恢复时自然忽略该侧。

## 变种三：边带权树的最大路径

新定义：给定无根树，边权可为负，路径至少包含一个节点；路径价值为所用边权之和。若允许单节点路径，答案至少为 0。树形 DP 改为对每个节点取最大的两条非负子边贡献。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using Edge = pair<int, long long>;
long long answer = 0;
long long dfs(int u, int parent, const vector<vector<Edge>>& graph) {
  long long first = 0;
  long long second = 0;
  for (auto [v, weight] : graph[u]) {
    if (v == parent) {
      continue;
    }
    long long value = max(0LL, weight + dfs(v, u, graph));
    if (value > first) {
      second = first;
      first = value;
    } else if (value > second) {
      second = value;
    }
  }
  answer = max(answer, first + second);
  return first;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<Edge>> graph(n);
  for (int i = 1; i < n; ++i) {
    int u, v;
    long long weight;
    cin >> u >> v >> weight;
    graph[u].push_back({v, weight});
    graph[v].push_back({u, weight});
  }
  dfs(0, -1, graph);
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。若题意要求至少使用一条边且所有边为负，需把答案初始化为最大边权并调整舍弃规则。

## 变种四：路径必须恰好包含 $k$ 个节点

新定义：在节点带权树中，求恰好 $k$ 个节点的最大路径和。对每个节点维护 `down[len]`，表示从该节点向下一条臂选 `len` 个节点的最大和；合并左右臂更新答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long NEG = -(1LL << 60);
struct Node {
  long long value;
  int left;
  int right;
};
int target;
long long answer = NEG;
vector<long long> dfs(int u, const vector<Node>& tree) {
  if (u == -1) {
    return vector<long long>(target + 1, NEG);
  }
  vector<long long> left = dfs(tree[u].left, tree);
  vector<long long> right = dfs(tree[u].right, tree);
  vector<long long> down(target + 1, NEG);
  down[1] = tree[u].value;
  for (int len = 2; len <= target; ++len) {
    down[len] = tree[u].value + max(left[len - 1], right[len - 1]);
  }
  answer = max(answer, down[target]);
  for (int left_len = 1; left_len <= target - 2; ++left_len) {
    int right_len = target - 1 - left_len;
    if (left[left_len] != NEG && right[right_len] != NEG) {
      answer = max(answer, left[left_len] + tree[u].value + right[right_len]);
    }
  }
  return down;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n >> target;
  vector<Node> tree(n);
  for (Node& node : tree) {
    cin >> node.value >> node.left >> node.right;
  }
  dfs(0, tree);
  if (answer == NEG) {
    cout << "impossible\n";
  } else {
    cout << answer << '\n';
  }
}
```

时间 $O(nk)$，空间 $O(nk)$ 加递归栈。二叉树中左右臂长度之和由 $k$ 固定，因此每个节点只枚举 $O(k)$ 种拆分。

## 可复现验证

- 最佳解覆盖两个官方样例、单节点和全负树。
- 小树可枚举任意两个端点的唯一路径作为 oracle，与树形 DP 对拍。
- 所有完整代码按 C++23 编译；恢复版本应额外核对输出路径相邻、节点不重复且节点和等于报告值。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/binary-tree-maximum-path-sum/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/binary-tree-maximum-path-sum/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-41-lc300/">← [力扣 Top 41] LC 300 最长递增子序列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-43-lc416/">[力扣 Top 43] LC 416 分割等和子集 中等 →</a>
</nav>
