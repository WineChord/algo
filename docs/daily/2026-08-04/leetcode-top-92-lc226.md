---
title: "[力扣 Top 92] LC 226 翻转二叉树 简单"
---

# [力扣 Top 92] LC 226 翻转二叉树 简单

<p class="daily-archive-kicker">2026-08-04 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8fa2a3e9345bf71d2095c885943214e3cabd27575b83ad9f0687f243e1f9e062 -->
## 官方原始信息

- Top 排名：92
- 题号：LC 226
- 官方中文标题：翻转二叉树
- 官方难度：简单
- 官方链接：[翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)

### 原始题意

给定二叉树根节点，把每个节点的左、右子树交换，返回翻转后的根节点。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  TreeNode* invertTree(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

```text
输入：root = [2,1,3]
输出：[2,3,1]
```

```text
输入：root = []
输出：[]
```

### 全部约束

- 节点数在 $[0,100]$。
- $-100\le Node.val\le100$。

## 约束推导与递归结构

翻转不是只交换根的两个孩子，而是对每个节点递归执行同一操作。节点值完全无关，决定算法的是树的结构。任何正确算法至少访问每个节点一次，时间下界为 $\Omega(n)$。

可以先翻转左右子树再交换，也可以先交换再递归；两种顺序都实现映射

$$
\mathcal{M}(u)=\bigl(v_u,\mathcal{M}(r_u),\mathcal{M}(l_u)\bigr).
$$

$n\le100$ 时递归深度安全；若把同一算法迁移到极深树，显式队列能避开系统栈限制。

## 解法递进

### 解法一：构造一棵新的镜像树

每个原节点新建一个对应节点，递归把原右子树接到新左侧、原左子树接到新右侧。它不修改输入，但额外分配整棵树。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  TreeNode* mirrorCopy(TreeNode* node) {
    if (!node) {
      return nullptr;
    }
    return new TreeNode(node->val, mirrorCopy(node->right), mirrorCopy(node->left));
  }
public:
  TreeNode* invertTree(TreeNode* root) {
    return mirrorCopy(root);
  }
};
```

时间 $O(n)$，新树与递归栈共占 $O(n+h)$。它适合需要保留原树的接口，但原题可以原地完成。

### 解法二：递归原地交换

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  TreeNode* invertTree(TreeNode* root) {
    if (!root) {
      return nullptr;
    }
    TreeNode* left = invertTree(root->left);
    TreeNode* right = invertTree(root->right);
    root->left = right;
    root->right = left;
    return root;
  }
};
```

时间 $O(n)$，递归栈 $O(h)$，代码和归纳证明最直接。

### 最佳实用解：层序遍历原地交换

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  TreeNode* invertTree(TreeNode* root) {
    if (!root) {
      return nullptr;
    }
    queue<TreeNode*> nodes;
    nodes.push(root);
    while (!nodes.empty()) {
      TreeNode* node = nodes.front();
      nodes.pop();
      swap(node->left, node->right);
      if (node->left) {
        nodes.push(node->left);
      }
      if (node->right) {
        nodes.push(node->right);
      }
    }
    return root;
  }
};
```

时间 $O(n)$，队列最坏 $O(w)$，其中 $w$ 是最大层宽。当前约束下递归版更短；工程中若树高不受控，推荐迭代版以避免栈溢出。

## 正确性证明

层序算法把根加入队列。每次取出节点时，交换其左右孩子，因此该节点满足镜像定义；交换后的所有非空孩子又被加入队列。每个可达节点有且仅有一个父节点，所以除根外恰被加入一次，最终所有节点都执行一次交换。节点集合和值未改变，而每条父子边的左右方向都反转，故得到的整棵树正是原树镜像。

## 样例手推

样例 1 先处理根 4，把孩子 2、7 交换为 7、2；随后处理 7，把 6、9 交换为 9、6；处理 2，把 1、3 交换为 3、1。叶子交换两个空指针后不变，层序结果为 `[4,7,2,9,6,3,1]`。空树直接返回空，单节点树也保持原状。

## 易错点与方案比较

- 交换后入队左右孩子，或交换前保存孩子再入队，都可以；不要因覆盖指针漏掉子树。
- 返回值仍是原根指针，只有内部边方向改变。
- 节点值可以重复，算法不应依赖值查找节点。
- 新树方案保留输入但占 $O(n)$ 新空间；原地递归最简，迭代方案对深树最稳。

## 变种一：只翻转前 $D$ 层

新定义：根为第 1 层，只交换深度不超过 $D$ 的节点；更深子树保持原方向。层序队列携带深度即可。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  TreeNode* invertFirstLevels(TreeNode* root, int depthLimit) {
    if (!root || depthLimit <= 0) {
      return root;
    }
    queue<pair<TreeNode*, int>> nodes;
    nodes.push({root, 1});
    while (!nodes.empty()) {
      auto [node, depth] = nodes.front();
      nodes.pop();
      if (depth <= depthLimit) {
        swap(node->left, node->right);
      }
      if (node->left) {
        nodes.push({node->left, depth + 1});
      }
      if (node->right) {
        nodes.push({node->right, depth + 1});
      }
    }
    return root;
  }
};
```

时间 $O(n)$，空间 $O(w)$。深度条件改变了哪些节点执行局部不变量，但不改变遍历方式。

## 变种二：判断两棵树是否互为镜像

新定义：不修改树，只判断第一棵的左侧结构是否逐点对应第二棵的右侧结构。递归同时比较交叉孩子。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
bool areMirrors(Node* first, Node* second) {
  if (!first || !second) {
    return first == second;
  }
  return first->value == second->value && areMirrors(first->left, second->right) &&
      areMirrors(first->right, second->left);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> first(n), second(n);
  for (vector<Node>* tree : {&first, &second}) {
    for (int i = 0; i < n; ++i) {
      int left, right;
      cin >> (*tree)[i].value >> left >> right;
      (*tree)[i].left = left < 0 ? nullptr : &(*tree)[left];
      (*tree)[i].right = right < 0 ? nullptr : &(*tree)[right];
    }
  }
  cout << (areMirrors(n ? &first[0] : nullptr, n ? &second[0] : nullptr) ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，递归栈 $O(h)$。原地交换不再适合，因为接口只允许观察。

## 变种三：翻转 N 叉树

新定义：镜像一棵有序 N 叉树。每个节点递归翻转所有孩子后，再反转孩子数组顺序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  vector<int> children;
};
void mirror(vector<Node>& tree, int node) {
  for (int child : tree[node].children) {
    mirror(tree, child);
  }
  reverse(tree[node].children.begin(), tree[node].children.end());
}
void preorder(const vector<Node>& tree, int node) {
  cout << tree[node].value << ' ';
  for (int child : tree[node].children) {
    preorder(tree, child);
  }
}
int main() {
  int n;
  cin >> n;
  vector<Node> tree(n);
  for (int i = 0; i < n; ++i) {
    int count;
    cin >> tree[i].value >> count;
    tree[i].children.resize(count);
    for (int& child : tree[i].children) {
      cin >> child;
    }
  }
  mirror(tree, 0);
  preorder(tree, 0);
  cout << '\n';
}
```

时间 $O(n)$，除递归栈外原地完成。二叉树的左右交换是“反转孩子序列”的特例。

## 变种四：不修改树，直接输出镜像层序

新定义：原树必须保持不变，只需输出其镜像的层序序列。访问节点时按“右孩子、左孩子”的次序入队即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  int left;
  int right;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, root;
  cin >> n >> root;
  vector<Node> tree(n);
  for (Node& node : tree) {
    cin >> node.value >> node.left >> node.right;
  }
  if (root < 0) {
    cout << '\n';
    return 0;
  }
  queue<int> nodes;
  nodes.push(root);
  while (!nodes.empty()) {
    int node = nodes.front();
    nodes.pop();
    cout << tree[node].value << ' ';
    if (tree[node].right >= 0) {
      nodes.push(tree[node].right);
    }
    if (tree[node].left >= 0) {
      nodes.push(tree[node].left);
    }
  }
  cout << '\n';
}
```

时间 $O(n)$，队列 $O(w)$，原树额外修改为零。若后续还需在镜像树上更新，就应真正构造或交换指针。

## 验证说明

本轮将七段实现按 C++23 编译；递归原地版、迭代版和新树版会在 20,000 棵随机二叉树上比较序列化结果，并覆盖空树、单节点、退化链、完整树、重复值与官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/invert-binary-tree/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-91-lc415/">← [力扣 Top 91] LC 415 字符串相加 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-93-lc104/">[力扣 Top 93] LC 104 二叉树的最大深度 简单 →</a>
</nav>
