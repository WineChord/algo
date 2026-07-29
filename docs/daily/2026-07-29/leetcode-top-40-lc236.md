---
title: "[力扣 Top 40] LC 236 二叉树的最近公共祖先 中等"
---

# [力扣 Top 40] LC 236 二叉树的最近公共祖先 中等

<p class="daily-archive-kicker">2026-07-29 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../graph/tree-aggregation.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：40
- 题号：LC 236
- 官方中文标题：二叉树的最近公共祖先
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/>

### 原始题意

给定一棵二叉树以及树中两个不同节点 `p`、`q`，返回它们的最近公共祖先：该节点同时是 `p`、`q` 的祖先，并且深度最大。按定义，节点可以是自己的祖先。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q);
};
```

### 全部官方样例

```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3。
```

```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点可以是自己的祖先，因此答案是节点 5。
```

```text
输入：root = [1,2], p = 1, q = 2
输出：1
```

### 全部约束

- 树中节点数在 $[2,10^5]$ 内。
- $-10^9\le Node.val\le10^9$。
- 所有节点值互不相同。
- `p != q`，且 `p`、`q` 均存在于树中。

## 最优结论

后序 DFS 对每棵子树返回三种语义之一：未找到目标、只找到一个目标、已经汇合为最近公共祖先。若当前节点就是目标，返回当前节点；否则递归得到左右结果：

- 左右都非空，两个目标分居两侧，当前节点就是最近公共祖先；
- 只有一侧非空，答案或已找到的目标完全位于该侧；
- 两侧都空，当前子树不含目标。

每个节点访问一次，时间 $O(n)$、递归栈 $O(h)$。面试中优先记这个三行不变量；生产环境若树可能退化到 $10^5$ 层，则用迭代父指针方案避免调用栈溢出。

## 约束与观察

- 题目给的是节点指针，不能只凭值推断一般版本；唯一值仅让示例可读。
- “节点可以是自己的祖先”决定了遇到 `p` 或 `q` 时应直接返回当前节点。
- 两条根到目标路径的最后公共节点就是答案，这是最直接的暴力基线。
- 单次查询不需要构造完整倍增表；多次查询时，预处理才值得。

## 解法递进

### 解法一：分别寻找两条根路径

DFS 保存根到 `p`、`q` 的路径，再从头比较至首次分叉。时间 $O(n)$，路径与递归空间 $O(h)$；同一棵树最多被搜索两次。

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
  bool findPath(TreeNode* node, TreeNode* target, vector<TreeNode*>& path) {
    if (node == nullptr) {
      return false;
    }
    path.push_back(node);
    if (node == target) {
      return true;
    }
    if (findPath(node->left, target, path) || findPath(node->right, target, path)) {
      return true;
    }
    path.pop_back();
    return false;
  }
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    vector<TreeNode*> pathP;
    vector<TreeNode*> pathQ;
    findPath(root, p, pathP);
    findPath(root, q, pathQ);
    TreeNode* answer = nullptr;
    int common = min(pathP.size(), pathQ.size());
    for (int i = 0; i < common && pathP[i] == pathQ[i]; ++i) {
      answer = pathP[i];
    }
    return answer;
  }
};
```

### 解法二：一次后序 DFS

一次遍历就把“是否含目标”向上汇总，是单次查询最简洁的最优方案。

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
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (root == nullptr || root == p || root == q) {
      return root;
    }
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    if (left != nullptr && right != nullptr) {
      return root;
    }
    return left != nullptr ? left : right;
  }
};
```

### 解法三：迭代建立父指针

先遍历到 `p`、`q` 都已发现，再把 `p` 的祖先加入集合，沿 `q` 的父链向上找到首个命中。仍为 $O(n)$ 时间、$O(n)$ 空间，但不会因退化树产生深递归。

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
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    unordered_map<TreeNode*, TreeNode*> parent;
    parent[root] = nullptr;
    stack<TreeNode*> pending;
    pending.push(root);
    while (!parent.contains(p) || !parent.contains(q)) {
      TreeNode* node = pending.top();
      pending.pop();
      if (node->left != nullptr) {
        parent[node->left] = node;
        pending.push(node->left);
      }
      if (node->right != nullptr) {
        parent[node->right] = node;
        pending.push(node->right);
      }
    }
    unordered_set<TreeNode*> ancestors;
    for (TreeNode* node = p; node != nullptr; node = parent[node]) {
      ancestors.insert(node);
    }
    for (TreeNode* node = q; node != nullptr; node = parent[node]) {
      if (ancestors.contains(node)) {
        return node;
      }
    }
    return nullptr;
  }
};
```

## 正确性证明

考虑后序 DFS 的返回值。若当前节点是 `p` 或 `q`，当前节点必然是这棵子树向父层汇报的最低候选，因为它可能就是最终祖先。否则：

- 左右递归都非空时，两目标分别在两个子树中；任何更深节点都不可能同时覆盖两侧，所以当前节点恰为最近公共祖先；
- 只有一侧非空时，两个目标的汇合点或唯一已发现目标只能在该侧，原样向上传递不会错过更低答案；
- 两侧都为空时，该子树不含目标。

由题设两个目标都存在，根调用最终一定返回且只会返回深度最大的共同祖先。

## 样例手推

第二个样例中，DFS 到节点 5 时立刻返回 5。节点 1 的子树返回节点 4 所在方向的目标信息；在根节点 3 处，左侧候选已经是 5，右侧对目标 4 实际为空，因为 4 位于 5 的子树中。返回值沿左侧保持为 5，所以答案正确体现“节点可以是自己的祖先”。

## 易错点

- 遇到目标节点时不要继续要求另一目标必须在另一子树；另一目标可能就在其后代中。
- 若题目不保证 `p`、`q` 都存在，简洁 DFS 需要额外计数才能区分“只找到一个目标”。
- $10^5$ 个节点可能形成链，递归实现存在语言调用栈风险。
- 多查询场景重复执行 $O(n)$ DFS 会超时，应预处理。

## 验证说明

对随机二叉树随机选择不同节点，以根路径法作为 oracle，对比后序 DFS 和迭代父指针结果；覆盖一方是另一方祖先、分居根两侧、深链和最小两节点树。

## Follow-up 与变种

### 变种一：同一棵静态树有大量 LCA 查询

一次 BFS 建深度，并预处理每个节点的 $2^j$ 级祖先。每次查询先抬平深度，再从高位同步上跳。预处理 $O(n\log n)$，单次查询 $O(\log n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
};
class LcaIndex {
  vector<TreeNode*> nodes_;
  unordered_map<TreeNode*, int> id_;
  vector<int> depth_;
  vector<vector<int>> up_;
public:
  explicit LcaIndex(TreeNode* root) {
    queue<TreeNode*> pending;
    pending.push(root);
    id_[root] = 0;
    nodes_.push_back(root);
    depth_.push_back(0);
    vector<int> parent{0};
    while (!pending.empty()) {
      TreeNode* node = pending.front();
      pending.pop();
      int nodeId = id_[node];
      for (TreeNode* child : {node->left, node->right}) {
        if (child == nullptr) {
          continue;
        }
        int childId = nodes_.size();
        id_[child] = childId;
        nodes_.push_back(child);
        depth_.push_back(depth_[nodeId] + 1);
        parent.push_back(nodeId);
        pending.push(child);
      }
    }
    int levels = 1;
    while ((1 << levels) <= static_cast<int>(nodes_.size())) {
      ++levels;
    }
    up_.assign(levels, vector<int>(nodes_.size()));
    up_[0] = parent;
    for (int level = 1; level < levels; ++level) {
      for (int node = 0; node < static_cast<int>(nodes_.size()); ++node) {
        up_[level][node] = up_[level - 1][up_[level - 1][node]];
      }
    }
  }
  TreeNode* query(TreeNode* first, TreeNode* second) const {
    int a = id_.at(first);
    int b = id_.at(second);
    if (depth_[a] < depth_[b]) {
      swap(a, b);
    }
    int difference = depth_[a] - depth_[b];
    for (int level = 0; level < static_cast<int>(up_.size()); ++level) {
      if ((difference >> level) & 1) {
        a = up_[level][a];
      }
    }
    if (a == b) {
      return nodes_[a];
    }
    for (int level = static_cast<int>(up_.size()) - 1; level >= 0; --level) {
      if (up_[level][a] != up_[level][b]) {
        a = up_[level][a];
        b = up_[level][b];
      }
    }
    return nodes_[up_[0][a]];
  }
};
```

### 变种二：树是二叉搜索树

若 `p`、`q` 都小于当前值，答案在左子树；都大于时在右子树；否则当前节点就是分叉点。时间 $O(h)$、空间 $O(1)$。

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
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    int low = min(p->val, q->val);
    int high = max(p->val, q->val);
    while (root != nullptr) {
      if (root->val < low) {
        root = root->right;
      } else if (root->val > high) {
        root = root->left;
      } else {
        return root;
      }
    }
    return nullptr;
  }
};
```

### 变种三：每个节点已有父指针

先计算两节点深度，抬升更深者，再同步向上。无需访问其他节点，时间 $O(h)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int val;
  Node* left;
  Node* right;
  Node* parent;
};
class Solution {
  int depth(Node* node) {
    int result = 0;
    while (node != nullptr) {
      ++result;
      node = node->parent;
    }
    return result;
  }
public:
  Node* lowestCommonAncestor(Node* first, Node* second) {
    int firstDepth = depth(first);
    int secondDepth = depth(second);
    while (firstDepth > secondDepth) {
      first = first->parent;
      --firstDepth;
    }
    while (secondDepth > firstDepth) {
      second = second->parent;
      --secondDepth;
    }
    while (first != second) {
      first = first->parent;
      second = second->parent;
    }
    return first;
  }
};
```

### 变种四：求 `k` 个目标节点的最近公共祖先

把目标集合中的任一当前节点视为有效返回值；否则合并左右子树结果。目标均存在时，逻辑与双目标完全一致。时间 $O(n)$、空间 $O(h+k)$。

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
  TreeNode* search(TreeNode* node, const unordered_set<TreeNode*>& targets) {
    if (node == nullptr || targets.contains(node)) {
      return node;
    }
    TreeNode* left = search(node->left, targets);
    TreeNode* right = search(node->right, targets);
    if (left != nullptr && right != nullptr) {
      return node;
    }
    return left != nullptr ? left : right;
  }
public:
  TreeNode* lowestCommonAncestor(TreeNode* root, const vector<TreeNode*>& nodes) {
    unordered_set<TreeNode*> targets(nodes.begin(), nodes.end());
    return search(root, targets);
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-39-lc59.md">← [力扣 Top 39] LC 59 螺旋矩阵 II 中等</a>
<a class="daily-archive-pager__next" href="leetcode-weekly-511-q4-lc3999.md">[力扣竞赛] 第 511 场周赛 Q4 LC 3999 字符串变换后的最少分组数 困难 →</a>
</nav>
