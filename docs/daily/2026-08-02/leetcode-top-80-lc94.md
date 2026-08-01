---
title: "[力扣 Top 80] LC 94 二叉树的中序遍历 简单"
---

# [力扣 Top 80] LC 94 二叉树的中序遍历 简单

<p class="daily-archive-kicker">2026-08-02 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a80e097692c30bf07ac6e6bdafb5c083b5e763e61a2ad4ae70a91f9934ee8e9e -->
## 官方原始信息

- Top 排名：80
- 题号：LC 94
- 官方中文标题：二叉树的中序遍历
- 官方难度：简单
- 官方链接：[二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)

### 原始题意

给定二叉树根结点，返回按“左子树、根、右子树”顺序得到的结点值序列。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  vector<int> inorderTraversal(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [1,null,2,3]
输出：[1,3,2]
```

```text
输入：root = []
输出：[]
```

```text
输入：root = [1]
输出：[1]
```

### 全部约束与进阶

- 结点数在 $[0,100]$ 内。
- $-100\le Node.val\le100$。
- 进阶要求用迭代算法完成。

## 约束推导与遍历不变量

输出本身有 $n$ 个元素，时间不可能优于 $O(n)$。递归栈或显式栈需要 $O(h)$ 辅助空间，$h$ 为树高；若要求严格 $O(1)$ 辅助空间，则必须临时利用空指针保存返回路径，这正是 Morris 遍历的切入点。

中序的关键不是“访问每个点”，而是何时输出根：必须在整个左子树处理完之后、右子树处理之前。迭代版维护不变量：栈中是尚未输出、且正在等待左子树完成的祖先链。

## 解法递进

### 解法一：递归深度优先搜索

定义直接对应递归顺序，最适合说明语义。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void traverse(TreeNode* node, vector<int>& order) {
    if (node == nullptr) {
      return;
    }
    traverse(node->left, order);
    order.push_back(node->val);
    traverse(node->right, order);
  }
public:
  vector<int> inorderTraversal(TreeNode* root) {
    vector<int> order;
    traverse(root, order);
    return order;
  }
};
```

时间 $O(n)$，递归栈 $O(h)$；链状树可能产生深递归。

### 最佳实用解：显式栈迭代

不断把当前结点及其左祖先压栈；走到空指针后弹出最深尚未输出的结点，再转向其右子树。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> inorderTraversal(TreeNode* root) {
    vector<int> order;
    stack<TreeNode*> pending;
    TreeNode* current = root;
    while (current != nullptr || !pending.empty()) {
      while (current != nullptr) {
        pending.push(current);
        current = current->left;
      }
      current = pending.top();
      pending.pop();
      order.push_back(current->val);
      current = current->right;
    }
    return order;
  }
};
```

时间 $O(n)$，空间 $O(h)$。它不修改树、无递归深度风险，是面试中优先推荐的实用方案。

### 解法三：Morris 遍历

若当前结点有左子树，就找左子树最右结点，即当前结点的中序前驱。前驱右指针为空时临时指向当前结点并向左；再次遇到这条线索时，说明左子树已完成，恢复空指针、输出当前结点并向右。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> inorderTraversal(TreeNode* root) {
    vector<int> order;
    TreeNode* current = root;
    while (current != nullptr) {
      if (current->left == nullptr) {
        order.push_back(current->val);
        current = current->right;
      } else {
        TreeNode* predecessor = current->left;
        while (predecessor->right != nullptr && predecessor->right != current) {
          predecessor = predecessor->right;
        }
        if (predecessor->right == nullptr) {
          predecessor->right = current;
          current = current->left;
        } else {
          predecessor->right = nullptr;
          order.push_back(current->val);
          current = current->right;
        }
      }
    }
    return order;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$（不计输出）。每条临时线索都会恢复；若遍历可能被异常中断，修改树结构的风险使它不如显式栈稳妥。

## 正确性证明

显式栈算法每次先把当前路径一路向左压栈，因此栈顶结点没有尚未处理的左侧结点。弹出它时，其左子树已全部输出，故此时输出根满足中序定义；随后转向右子树，又以同样方式先处理其最左链。每个结点恰好入栈、出栈一次，且输出发生在左子树后、右子树前，所以所得序列恰为中序遍历。

Morris 中，临时线索只从某结点的中序前驱指回该结点。第一次建立线索后处理完整左子树；第二次沿线索返回时删除它并输出根。因此它模拟了递归返回动作，不遗漏、不重复，结束后所有被修改指针均恢复。

## 样例手推

对 `[1,null,2,3]`：先压入 1，因其无左子树而弹出并输出 1；转到 2，压入 2 再压入其左孩子 3；弹出 3，随后弹出 2，得到 `[1,3,2]`。空树让外层条件一开始即为假，返回空数组。

## 易错点与方案比较

- 中序是左、根、右，不能在压栈时输出根。
- 外层条件必须是“当前结点非空或栈非空”，否则会漏掉等待弹出的祖先。
- Morris 找前驱时必须同时检查 `predecessor->right != current`，并在第二次相遇时恢复指针。
- 递归最简，显式栈最稳，Morris 空间最小但证明与实现负担更高；通常优先记忆显式栈。

## 变种一：改为前序遍历

新定义：输出顺序为根、左、右。用栈时弹出即输出，并先压右孩子再压左孩子，保证左孩子先处理。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> preorderTraversal(TreeNode* root) {
    if (root == nullptr) {
      return {};
    }
    vector<int> order;
    stack<TreeNode*> pending;
    pending.push(root);
    while (!pending.empty()) {
      TreeNode* node = pending.top();
      pending.pop();
      order.push_back(node->val);
      if (node->right != nullptr) {
        pending.push(node->right);
      }
      if (node->left != nullptr) {
        pending.push(node->left);
      }
    }
    return order;
  }
};
```

时间 $O(n)$，空间 $O(h)$ 到 $O(n)$，取决于树形。

## 变种二：改为后序遍历

新定义：输出左、右、根。单栈记录上次完成的结点；栈顶无未处理孩子时才输出。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> postorderTraversal(TreeNode* root) {
    vector<int> order;
    stack<TreeNode*> pending;
    TreeNode* current = root;
    TreeNode* completed = nullptr;
    while (current != nullptr || !pending.empty()) {
      if (current != nullptr) {
        pending.push(current);
        current = current->left;
      } else {
        TreeNode* node = pending.top();
        if (node->right != nullptr && node->right != completed) {
          current = node->right;
        } else {
          order.push_back(node->val);
          completed = node;
          pending.pop();
        }
      }
    }
    return order;
  }
};
```

时间 $O(n)$，空间 $O(h)$。

## 变种三：二叉搜索树第 $k$ 小元素

新定义：树满足 BST 性质，只需第 $k$ 小值。BST 中序序列单调递增；迭代到第 $k$ 次弹栈即可提前返回。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int kthSmallest(TreeNode* root, int k) {
    stack<TreeNode*> pending;
    TreeNode* current = root;
    while (current != nullptr || !pending.empty()) {
      while (current != nullptr) {
        pending.push(current);
        current = current->left;
      }
      current = pending.top();
      pending.pop();
      if (--k == 0) {
        return current->val;
      }
      current = current->right;
    }
    throw invalid_argument("k exceeds the node count");
  }
};
```

时间 $O(h+k)$，空间 $O(h)$；普通二叉树没有排序性质，不能据此提前停止求第 $k$ 小。

## 变种四：惰性中序迭代器

新定义：不一次性返回全部序列，而是反复调用 `next()` 获取下一个值、用 `hasNext()` 判断是否结束。构造和每次转向右子树时只压入左链。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class BSTIterator {
  stack<TreeNode*> pending;
  void pushLeft(TreeNode* node) {
    while (node != nullptr) {
      pending.push(node);
      node = node->left;
    }
  }
public:
  explicit BSTIterator(TreeNode* root) {
    pushLeft(root);
  }
  int next() {
    TreeNode* node = pending.top();
    pending.pop();
    pushLeft(node->right);
    return node->val;
  }
  bool hasNext() const {
    return !pending.empty();
  }
};
```

构造 $O(h)$，每个结点只入栈出栈一次，因此 `next()` 摊还 $O(1)$，空间 $O(h)$。

## 可复现验证

随机生成二叉树，把递归结果作为 oracle，与显式栈和 Morris 输出逐项比较；Morris 完成后再次递归，确认树结构未被改变。覆盖空树、单结点、纯左链、纯右链、完全树与重复值。所有代码均以 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/binary-tree-inorder-traversal/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-79-lc208/">← [力扣 Top 79] LC 208 实现 Trie (前缀树) 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-512-q4-lc4003/">[力扣竞赛] 第 512 场周赛 Q4 LC 4003 交替方向的最小路径代价 III 困难 →</a>
</nav>
