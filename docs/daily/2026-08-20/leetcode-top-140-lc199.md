---
title: "[力扣 Top 140] LC 199 二叉树的右视图 中等"
---

# [力扣 Top 140] LC 199 二叉树的右视图 中等

<p class="daily-archive-kicker">2026-08-20 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-20 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0e8000d45cc89f45e28f01db7e7a9983bc4c2705664f3af3c568777e6c21a2d0 -->
[官方题目：199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/)

## 官方原始信息

- 高频队列位置：Top 140；源表题目为“199. 二叉树的右视图”。
- 题号与标题：199. 二叉树的右视图。
- 官方难度：中等。
- 官方链接：[LeetCode 中国题面](https://leetcode.cn/problems/binary-tree-right-side-view/)。
- 函数签名：`vector<int> rightSideView(TreeNode* root)`。
- 官方标签：树、深度优先搜索、广度优先搜索、二叉树。

给定二叉树根节点 `root`。从树的右侧观察，按从上到下的顺序返回每一层能够看到的节点值。
等价地说，第 $d$ 层应返回按从左到右顺序排列时的最后一个节点。

### 全部官方样例

示例 1：

```text
输入：root = [1,2,3,null,5,null,4]
输出：[1,3,4]
解释：第 0、1、2 层最右节点依次为 1、3、4。
```

示例 2：

```text
输入：root = [1,2,3,4,null,null,null,5]
输出：[1,3,4,5]
```

示例 3：

```text
输入：root = [1,null,3]
输出：[1,3]
```

示例 4：

```text
输入：root = []
输出：[]
```

官方页面的前两例附有树形示意图；节点关系已经由层序数组完整给出，图片不增加判题规则。

### 全部约束

- 二叉树节点数 $n$ 满足 $0\le n\le100$。
- $-100\le\texttt{Node.val}\le100$。

## 约束、定义与边界

节点值可以重复，所以“可见”取决于节点位置，不能按值去重。答案恰有树高 $h$ 个元素；
空树答案为空。任何正确算法至少要查看每个可能成为层最右节点的分支，最坏需要
$\Omega(n)$ 时间，因此一次遍历已经达到渐进最优。

真正的选择是遍历顺序：

- 层序遍历天然把同一深度放在一起，取每层最后一个节点；
- 深度优先搜索若先访问右子树，则某深度第一次遇到的节点就是该层最右节点。

树高最多为 $n$。本题 $n\le100$，递归栈安全；在通用超深树中可改用显式栈或 BFS。

## 样例手推

对示例 1，BFS 队列按层变化为 `[1]`、`[2,3]`、`[5,4]`。每层最后一个值分别是
`1`、`3`、`4`。若改用右优先 DFS，访问顺序从 `1 -> 3 -> 4` 开始，三个深度第一次见到
的节点也正是这三个答案；随后访问 `2`、`5` 时，对应深度已经有答案，不再覆盖。

相关边界包括：空树、单节点、只有左链、只有右链、同层节点值相同，以及“较深节点位于左
子树但较浅右节点仍存在”的非完全树。

## 解法一：逐深度重新搜索

先求树高。对每个深度 $d$，从根开始进行一次右子树优先搜索，找到该深度的第一个节点。
该方法直接表达“每层最右”，覆盖性没有问题，但同一上层节点会被重复访问。

时间复杂度 $O(nh)$，最坏退化为 $O(n^2)$；递归空间 $O(h)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0, TreeNode* l = nullptr, TreeNode* r = nullptr)
      : val(value), left(l), right(r) {}
};
class Solution {
public:
  vector<int> rightSideView(TreeNode* root) {
    vector<int> answer;
    int height = treeHeight(root);
    for (int depth = 0; depth < height; ++depth) {
      int value = 0;
      findAtDepth(root, depth, value);
      answer.push_back(value);
    }
    return answer;
  }
private:
  int treeHeight(TreeNode* node) {
    if (!node) return 0;
    return 1 + max(treeHeight(node->left), treeHeight(node->right));
  }
  bool findAtDepth(TreeNode* node, int depth, int& value) {
    if (!node) return false;
    if (depth == 0) {
      value = node->val;
      return true;
    }
    return findAtDepth(node->right, depth - 1, value) ||
        findAtDepth(node->left, depth - 1, value);
  }
};
```

## 从重复搜索到单次层序遍历

暴力方案为每个深度重新穿过树。BFS 把队列开头的整段节点视为当前层：先固定本层数量，
依次弹出并加入孩子，最后弹出的节点就是当前层最右节点。每个节点只入队、出队一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0, TreeNode* l = nullptr, TreeNode* r = nullptr)
      : val(value), left(l), right(r) {}
};
class Solution {
public:
  vector<int> rightSideView(TreeNode* root) {
    if (!root) return {};
    vector<int> answer;
    queue<TreeNode*> nodes;
    nodes.push(root);
    while (!nodes.empty()) {
      int levelSize = nodes.size();
      for (int index = 0; index < levelSize; ++index) {
        TreeNode* node = nodes.front();
        nodes.pop();
        if (node->left) nodes.push(node->left);
        if (node->right) nodes.push(node->right);
        if (index + 1 == levelSize) answer.push_back(node->val);
      }
    }
    return answer;
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(w)$，其中 $w$ 是最大层宽。

## 最佳实用解：右优先 DFS 的“首次到达”不变量

按“根、右、左”顺序遍历。若当前深度 `depth` 等于 `answer.size()`，说明这是遍历第一次到达
该深度，立即记录；之后同深度的节点必在它左侧，无需覆盖。

### 正确性证明

**引理**：右优先 DFS 在每个深度首次访问的节点是该层最右节点。

证明：对任意节点，遍历会先完整访问其右子树，再访问左子树。若某层在右子树中存在节点，
它一定先于左子树同层节点被访问；递归应用这一顺序，首次访问者就是从根到该层能选择的
最靠右分支。若右侧分支在该层不存在，搜索才转入左侧，而左侧中仍按同样规则选择最右者。

**定理**：算法返回且只返回每层右视图节点。

每个非空深度都会被 DFS 到达，第一次到达时恰满足 `depth == answer.size()`，由引理写入该层
最右节点；同层后续节点不会写入。各深度恰写一次，顺序由浅到深，因此结果正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0, TreeNode* l = nullptr, TreeNode* r = nullptr)
      : val(value), left(l), right(r) {}
};
class Solution {
public:
  vector<int> rightSideView(TreeNode* root) {
    vector<int> answer;
    visit(root, 0, answer);
    return answer;
  }
private:
  void visit(TreeNode* node, int depth, vector<int>& answer) {
    if (!node) return;
    if (depth == static_cast<int>(answer.size())) answer.push_back(node->val);
    visit(node->right, depth + 1, answer);
    visit(node->left, depth + 1, answer);
  }
};
```

时间复杂度 $O(n)$，递归空间 $O(h)$，答案空间 $O(h)$。这比 BFS 的最坏 $O(w)$ 队列更适合
宽树，代码也直接承载证明不变量。面试中建议优先记忆“观察方向优先 + 每层首次到达”的 DFS；
若递归深度可能失控，则改用 BFS。

## 易错点

- 左优先 DFS 取“首次到达”会得到左视图；若左优先，就必须覆盖到该层最后一个节点。
- 用节点值判断是否已经记录会被重复值破坏；应使用深度与答案长度。
- BFS 必须在进入本层时固定 `levelSize`，不能让新加入的孩子混入本层循环。
- 空树不能把空指针放入队列后再解引用。
- DFS 的空间是 $O(h)$，不能笼统写成 $O(1)$。

## 可复现验证

三份实现均按 C++23 编译。四个官方样例逐一通过；额外生成随机小二叉树，以 BFS 每层最后
节点为 oracle，与右优先 DFS 和逐深度搜索比较。还覆盖空树、单节点、纯左链、纯右链、
重复值、极不平衡树和左右子树高度不同的情形。

## 变种一：改为左视图

新定义：从左侧观察，返回每层最左节点。原不变量仍成立，只需把访问顺序改成“根、左、右”。
时间 $O(n)$，递归空间 $O(h)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0) : val(value), left(nullptr), right(nullptr) {}
};
class LeftView {
public:
  vector<int> view(TreeNode* root) {
    vector<int> answer;
    dfs(root, 0, answer);
    return answer;
  }
private:
  void dfs(TreeNode* node, int depth, vector<int>& answer) {
    if (!node) return;
    if (depth == static_cast<int>(answer.size())) answer.push_back(node->val);
    dfs(node->left, depth + 1, answer);
    dfs(node->right, depth + 1, answer);
  }
};
```

## 变种二：每层从右数第 $k$ 个节点

新定义：只对节点数不少于 $k$ 的层，返回从右向左第 $k$ 个节点。单个“首次到达”不再够用，
因为每层要知道相对次序；BFS 在每层固定大小后，取下标 `levelSize - k`。时间 $O(n)$，
空间 $O(w)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0) : val(value), left(nullptr), right(nullptr) {}
};
class KthRightView {
public:
  vector<int> view(TreeNode* root, int k) {
    if (!root || k <= 0) return {};
    vector<int> answer;
    queue<TreeNode*> nodes;
    nodes.push(root);
    while (!nodes.empty()) {
      int levelSize = nodes.size();
      for (int index = 0; index < levelSize; ++index) {
        TreeNode* node = nodes.front();
        nodes.pop();
        if (index == levelSize - k) answer.push_back(node->val);
        if (node->left) nodes.push(node->left);
        if (node->right) nodes.push(node->right);
      }
    }
    return answer;
  }
};
```

## 变种三：改为顶部视图

新定义：给根的水平坐标为 0，左孩子减 1、右孩子加 1；从上方观察时，每个水平坐标只保留
深度最小的节点。若同深节点落在同一列，约定取从左到右 BFS 中先访问者。深度而非层内左右
顺序成为关键，因此用 BFS 保证首次到达某横坐标时满足该规则，再用有序映射按横坐标输出。
时间 $O(n\log n)$，空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  TreeNode(int value = 0) : val(value), left(nullptr), right(nullptr) {}
};
class TopView {
public:
  vector<int> view(TreeNode* root) {
    if (!root) return {};
    map<int, int> first;
    queue<pair<TreeNode*, int>> nodes;
    nodes.push({root, 0});
    while (!nodes.empty()) {
      auto [node, column] = nodes.front();
      nodes.pop();
      first.try_emplace(column, node->val);
      if (node->left) nodes.push({node->left, column - 1});
      if (node->right) nodes.push({node->right, column + 1});
    }
    vector<int> answer;
    for (auto [column, value] : first) {
      static_cast<void>(column);
      answer.push_back(value);
    }
    return answer;
  }
};
```

## 变种四：N 叉树的右视图

新定义：每个节点有按从左到右排列的任意多个孩子。二叉树的 `right` 优先不再存在，但只要
逆序遍历孩子，首次到达不变量完全保留。设总孩子边数为 $n-1$，时间 $O(n)$，递归空间
$O(h)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int val;
  vector<Node*> children;
  explicit Node(int value = 0) : val(value) {}
};
class NaryRightView {
public:
  vector<int> view(Node* root) {
    vector<int> answer;
    dfs(root, 0, answer);
    return answer;
  }
private:
  void dfs(Node* node, int depth, vector<int>& answer) {
    if (!node) return;
    if (depth == static_cast<int>(answer.size())) answer.push_back(node->val);
    for (auto it = node->children.rbegin(); it != node->children.rend(); ++it) {
      dfs(*it, depth + 1, answer);
    }
  }
};
```

## 来源

- [LeetCode 199 官方题面](https://leetcode.cn/problems/binary-tree-right-side-view/)，核对于 2026-08-20。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/binary-tree-right-side-view/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc227-d/">← [atcoder] ARC227 D Median of Binary Strings</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-515-q3-lc4026/">[力扣竞赛] 第 515 场周赛 Q3 LC 4026 工位的最大间隔 中等 →</a>
</nav>
