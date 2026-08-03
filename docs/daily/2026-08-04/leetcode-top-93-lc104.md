---
title: "[力扣 Top 93] LC 104 二叉树的最大深度 简单"
---

# [力扣 Top 93] LC 104 二叉树的最大深度 简单

<p class="daily-archive-kicker">2026-08-04 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d2d1dc57979a7aa36b6e9ebdc961ddb64ff5f7725a2e0d163514744c5d58b18a -->
## 官方原始信息

- Top 排名：93
- 题号：LC 104
- 官方中文标题：二叉树的最大深度
- 官方难度：简单
- 官方链接：[二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

### 原始题意

给定二叉树根节点，返回从根到最远叶子的最长路径所包含的节点数。空树深度为 0。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  int maxDepth(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [3,9,20,null,null,15,7]
输出：3
```

```text
输入：root = [1,null,2]
输出：2
```

### 全部约束

- 节点数在 $[0,10^4]$。
- $-100\le Node.val\le100$。

## 约束推导与状态选择

节点值不影响深度。若把问题定义在任意子树上，空子树贡献 0，非空子树的答案只由两个孩子的答案决定：

$$
d(u)=1+\max\bigl(d(l_u),d(r_u)\bigr).
$$

这是一条后序聚合：先得到孩子摘要，再合成父节点摘要。每个节点只需处理一次，时间下界和最优复杂度都是 $O(n)$。节点数可达 $10^4$，极端链的递归深度同样可达 $10^4$；C++ 常见环境通常能承受，但显式层序遍历完全消除系统栈风险。

## 解法递进

### 解法一：显式保存每条根到叶路径

DFS 到叶子时比较当前路径长度。按值传递路径会在每层复制，退化链上达到 $O(n^2)$，但它直观覆盖所有候选路径。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void enumerate(TreeNode* node, vector<TreeNode*> path, int& answer) {
    if (!node) {
      return;
    }
    path.push_back(node);
    if (!node->left && !node->right) {
      answer = max(answer, static_cast<int>(path.size()));
      return;
    }
    enumerate(node->left, path, answer);
    enumerate(node->right, path, answer);
  }
public:
  int maxDepth(TreeNode* root) {
    int answer = 0;
    enumerate(root, {}, answer);
    return answer;
  }
};
```

最坏时间 $O(nh)$，路径副本峰值 $O(h)$，累计分配成本更高。

### 解法二：后序返回子树深度

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxDepth(TreeNode* root) {
    if (!root) {
      return 0;
    }
    return 1 + max(maxDepth(root->left), maxDepth(root->right));
  }
};
```

时间 $O(n)$，递归栈 $O(h)$。它是最适合解释和默写的版本。

### 最佳实用解：按层 BFS

队列每完整弹出一层，深度加 1；最后处理的层就是最深层。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxDepth(TreeNode* root) {
    if (!root) {
      return 0;
    }
    queue<TreeNode*> nodes;
    nodes.push(root);
    int depth = 0;
    while (!nodes.empty()) {
      int levelSize = nodes.size();
      ++depth;
      while (levelSize--) {
        TreeNode* node = nodes.front();
        nodes.pop();
        if (node->left) {
          nodes.push(node->left);
        }
        if (node->right) {
          nodes.push(node->right);
        }
      }
    }
    return depth;
  }
};
```

时间 $O(n)$，队列 $O(w)$。面试中优先写递归式并说明栈风险；面对高度可能很大的不可信输入时，提交 BFS 更稳健。

## 正确性证明

BFS 初始队列只含深度 1 的根。假设某轮开始时队列恰含当前深度的全部节点；该轮固定 `levelSize`，只弹出这些节点，并把它们的非空孩子加入队尾，因此轮末队列恰含下一深度的全部节点。每轮深度加一，归纳可知计数等于已处理层数。队列为空当且仅当最深层已处理完成，所以最终计数就是最大深度。

## 样例手推

`[3,9,20,null,null,15,7]` 的队列层次依次为 `[3]`、`[9,20]`、`[15,7]`，共 3 轮。`[1,null,2]` 依次为 `[1]`、`[2]`，答案 2。空树在建队列前直接返回 0；单节点树只进行一轮。

## 易错点与方案比较

- 深度按节点数计，不是边数；非空单节点树答案为 1。
- BFS 必须先固定本层大小，不能让刚入队的孩子在同一层被处理。
- 递归式的空树基例为 0，父节点才加 1。
- DFS 额外空间与高度相关，BFS 与最大层宽相关；两者时间同为最优 $O(n)$。

## 变种一：二叉树的最小深度

新定义：求根到最近叶子的节点数。不能简单把 `max` 改为 `min`，因为缺失孩子不是一条有效根到叶路径；BFS 第一次遇到叶子即可停止。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minDepth(TreeNode* root) {
    if (!root) {
      return 0;
    }
    queue<pair<TreeNode*, int>> nodes;
    nodes.push({root, 1});
    while (!nodes.empty()) {
      auto [node, depth] = nodes.front();
      nodes.pop();
      if (!node->left && !node->right) {
        return depth;
      }
      if (node->left) {
        nodes.push({node->left, depth + 1});
      }
      if (node->right) {
        nodes.push({node->right, depth + 1});
      }
    }
    return 0;
  }
};
```

时间 $O(n)$，空间 $O(w)$；遇到浅叶时会提前结束。

## 变种二：恢复一条最深根到叶路径

新定义：除深度外还返回节点值序列。DFS 维护当前路径，遇到更深叶子时复制为答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  int left;
  int right;
};
void search(const vector<Node>& tree, int node, vector<int>& path, vector<int>& answer) {
  if (node < 0) {
    return;
  }
  path.push_back(tree[node].value);
  if (tree[node].left < 0 && tree[node].right < 0 && path.size() > answer.size()) {
    answer = path;
  }
  search(tree, tree[node].left, path, answer);
  search(tree, tree[node].right, path, answer);
  path.pop_back();
}
int main() {
  int n, root;
  cin >> n >> root;
  vector<Node> tree(n);
  for (Node& node : tree) {
    cin >> node.value >> node.left >> node.right;
  }
  vector<int> path, answer;
  search(tree, root, path, answer);
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n+h)$，空间 $O(h)$，其中复制最终路径需要 $O(h)$。若要求字典序最小，平局时比较候选路径。

## 变种三：边带非负权，求最大根到叶距离

新定义：每条父子边有权，答案按权值和而非节点数衡量。后序状态从“深度”改为“最大剩余权和”。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Edge {
  int child;
  long long weight;
};
long long solve(const vector<array<Edge, 2>>& tree, int node) {
  if (node < 0) {
    return LLONG_MIN / 4;
  }
  long long best = 0;
  bool hasChild = false;
  for (const Edge& edge : tree[node]) {
    if (edge.child >= 0) {
      hasChild = true;
      best = max(best, edge.weight + solve(tree, edge.child));
    }
  }
  return hasChild ? best : 0;
}
int main() {
  int n, root;
  cin >> n >> root;
  vector<array<Edge, 2>> tree(n);
  for (auto& edges : tree) {
    cin >> edges[0].child >> edges[0].weight >> edges[1].child >> edges[1].weight;
  }
  cout << (root < 0 ? 0 : solve(tree, root)) << '\n';
}
```

时间 $O(n)$，栈 $O(h)$。若允许负权，叶子约束必须保留，不能随意用 0 代表提前停止。

## 变种四：N 叉树最大深度

新定义：每个节点有任意多个孩子。递推中的二元 `max` 改为遍历所有孩子的最大值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int depth(const vector<vector<int>>& children, int node) {
  int best = 0;
  for (int child : children[node]) {
    best = max(best, depth(children, child));
  }
  return best + 1;
}
int main() {
  int n, root;
  cin >> n >> root;
  vector<vector<int>> children(n);
  for (int i = 0; i < n; ++i) {
    int count;
    cin >> count;
    children[i].resize(count);
    for (int& child : children[i]) {
      cin >> child;
    }
  }
  cout << (root < 0 ? 0 : depth(children, root)) << '\n';
}
```

时间 $O(n)$，栈 $O(h)$。可迁移的核心不是“左右孩子”，而是“父状态取所有子状态的最大值再加一”。

## 验证说明

本轮将七段实现按 C++23 编译；递归深度与 BFS 会在 20,000 棵随机二叉树上对拍，并覆盖空树、单节点、单链、满树、最大节点数与两组官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-92-lc226/">← [力扣 Top 92] LC 226 翻转二叉树 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-94-lc43/">[力扣 Top 94] LC 43 字符串相乘 中等 →</a>
</nav>
