---
title: "[力扣 Top 62] LC 105 从前序与中序遍历序列构造二叉树 中等"
---

# [力扣 Top 62] LC 105 从前序与中序遍历序列构造二叉树 中等

<p class="daily-archive-kicker">2026-08-01 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a60a4b26775ba2a361f8db334a4f69229eacb4741635048d492ef0ec68c64556 -->
## 官方原始信息

- Top 排名：62
- 题号：LC 105
- 官方中文标题：从前序与中序遍历序列构造二叉树
- 官方难度：中等
- 官方链接：[从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

### 原始题意

给定同一棵二叉树的前序遍历 `preorder` 和中序遍历 `inorder`，所有节点值互不相同。构造并返回这棵二叉树。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder);
};
```

### 全部官方样例

```text
输入：preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出：[3,9,20,null,null,15,7]
```

```text
输入：preorder = [-1], inorder = [-1]
输出：[-1]
```

### 全部约束

- $1\le |preorder|=|inorder|\le3000$。
- $-3000\le preorder_i,inorder_i\le3000$。
- 两个数组中的节点值均互不相同，且值集合一致。
- 输入保证分别是同一棵二叉树的合法前序与中序遍历。

## 约束推导与边界

前序遍历的第一个元素必为当前子树根；根在中序遍历中的位置又唯一划分左、右子树。若每次在线性区间中寻找根，最坏退化链会达到 $O(n^2)$。值互异允许预建“值到中序下标”的哈希表，把每次划分降为 $O(1)$，总时间 $O(n)$。

节点数最多 3000，递归深度最坏也是 3000，通常可接受；若运行环境栈很紧，可用迭代栈方案。节点值可为负数，但只作为哈希键，不涉及溢出。

## 解法递进

### 解法一：每层线性寻找根

区间 `[preLeft,preRight)` 的根是 `preorder[preLeft]`，在对应中序区间中线性寻找它，再按左子树长度切分前序区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int value) : val(value), left(nullptr), right(nullptr) {
  }
};
class Solution {
  TreeNode* build(const vector<int>& preorder, int preLeft, int preRight,
      const vector<int>& inorder, int inLeft, int inRight) {
    if (preLeft == preRight) {
      return nullptr;
    }
    int rootValue = preorder[preLeft];
    int middle = inLeft;
    while (inorder[middle] != rootValue) {
      ++middle;
    }
    int leftSize = middle - inLeft;
    TreeNode* root = new TreeNode(rootValue);
    root->left = build(preorder, preLeft + 1, preLeft + 1 + leftSize, inorder, inLeft, middle);
    root->right = build(preorder, preLeft + 1 + leftSize, preRight, inorder, middle + 1, inRight);
    return root;
  }
public:
  TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
    return build(preorder, 0, preorder.size(), inorder, 0, inorder.size());
  }
};
```

最坏时间 $O(n^2)$，递归空间 $O(n)$。瓶颈是同一段中序区间被反复扫描。

### 最佳实用解：中序下标表加前序指针

预处理每个值在中序序列中的唯一位置。递归函数只接收当前中序区间；全局前序指针每创建一个节点恰好前进一次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int value) : val(value), left(nullptr), right(nullptr) {
  }
};
class Solution {
  unordered_map<int, int> inorderIndex;
  int preorderIndex = 0;
  TreeNode* build(const vector<int>& preorder, int left, int right) {
    if (left >= right) {
      return nullptr;
    }
    int value = preorder[preorderIndex++];
    int middle = inorderIndex[value];
    TreeNode* root = new TreeNode(value);
    root->left = build(preorder, left, middle);
    root->right = build(preorder, middle + 1, right);
    return root;
  }
public:
  TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
    inorderIndex.clear();
    preorderIndex = 0;
    for (int i = 0; i < static_cast<int>(inorder.size()); ++i) {
      inorderIndex[inorder[i]] = i;
    }
    return build(preorder, 0, inorder.size());
  }
};
```

期望时间 $O(n)$，哈希表与递归栈空间 $O(n)$。

### 同阶方案：单调栈式迭代构造

前序依次创建节点。栈顶尚未等于当前中序值时，新节点必是栈顶的左孩子；一旦相等，就连续弹出已经完成左子树与自身的祖先，下一节点接到最后弹出节点的右侧。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int value) : val(value), left(nullptr), right(nullptr) {
  }
};
class Solution {
public:
  TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
    TreeNode* root = new TreeNode(preorder[0]);
    vector<TreeNode*> stack{root};
    int inIndex = 0;
    for (int i = 1; i < static_cast<int>(preorder.size()); ++i) {
      TreeNode* node = new TreeNode(preorder[i]);
      if (stack.back()->val != inorder[inIndex]) {
        stack.back()->left = node;
      } else {
        TreeNode* parent = nullptr;
        while (!stack.empty() && stack.back()->val == inorder[inIndex]) {
          parent = stack.back();
          stack.pop_back();
          ++inIndex;
        }
        parent->right = node;
      }
      stack.push_back(node);
    }
    return root;
  }
};
```

时间 $O(n)$，显式栈空间 $O(n)$。递归版的区间含义更直接、证明更短，推荐面试优先讲递归；迭代版不依赖调用栈，适合极深树。

## 正确性证明

对任意递归调用的中序区间 `[left,right)`，前序指针指向该子树在前序中的第一个尚未消费元素，因此它就是子树根。值互异保证哈希表返回唯一 `middle`；中序性质保证 `[left,middle)` 恰为左子树节点，`(middle,right)` 恰为右子树节点。

算法先递归构造左区间，再构造右区间，与前序“根、左、右”的消费顺序一致。空区间返回空指针。按区间长度归纳，两棵子树均被唯一正确构造并接到根上，所以整个返回树的两种遍历正好等于输入；唯一划分也说明不存在另一棵不同的合法树。

## 样例手推

前序首项 3 是根；3 在中序下标 1，把 `[9]` 划为左子树、`[15,20,7]` 划为右子树。前序指针随后读 9，构造叶子；再读 20，20 的中序位置把 15 与 7 分到两侧，得到样例树。

单节点时两个区间一次划分后都为空。完全偏斜树会形成深递归，但每个节点仍只创建一次。

## 易错点与方案比较

- 前序下标不能按中序下标直接切；应使用左子树长度，或使用单调前序指针。
- 区间统一采用半开形式，空区间条件是 `left>=right`。
- 哈希表与前序指针是对象成员时，每次调用入口必须清空／归零。
- 唯一性依赖节点值互异；允许重复值时，仅凭两种遍历一般不能唯一恢复。
- 递归哈希版结构最清晰；迭代版的常数略小且规避调用栈，但不变量更难讲。

## 变种一：由中序与后序遍历构造

后序末尾是根。若从后往前消费，顺序为“根、右、左”，所以必须先递归构造右子树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
  explicit Node(int value) : value(value) {
  }
};
unordered_map<int, int> position;
int postIndex;
Node* build(const vector<int>& postorder, int left, int right) {
  if (left >= right) {
    return nullptr;
  }
  int value = postorder[postIndex--];
  int middle = position[value];
  Node* root = new Node(value);
  root->right = build(postorder, middle + 1, right);
  root->left = build(postorder, left, middle);
  return root;
}
void printPreorder(Node* root) {
  if (!root) {
    return;
  }
  cout << root->value << ' ';
  printPreorder(root->left);
  printPreorder(root->right);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> inorder(n), postorder(n);
  for (int& value : inorder) {
    cin >> value;
  }
  for (int& value : postorder) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    position[inorder[i]] = i;
  }
  postIndex = n - 1;
  printPreorder(build(postorder, 0, n));
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种二：前序与后序恢复满二叉树

一般二叉树仅给前序与后序并不唯一；若保证每个内部节点都有两个孩子，则前序中根后的元素必为左子树根，可在后序中确定左子树大小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
  explicit Node(int value) : value(value) {
  }
};
unordered_map<int, int> postPosition;
Node* build(const vector<int>& preorder, int preLeft, int preRight, const vector<int>& postorder,
    int postLeft, int postRight) {
  if (preLeft >= preRight) {
    return nullptr;
  }
  Node* root = new Node(preorder[preLeft]);
  if (preRight - preLeft == 1) {
    return root;
  }
  int leftRoot = preorder[preLeft + 1];
  int leftSize = postPosition[leftRoot] - postLeft + 1;
  root->left = build(
      preorder, preLeft + 1, preLeft + 1 + leftSize, postorder, postLeft, postLeft + leftSize);
  root->right = build(
      preorder, preLeft + 1 + leftSize, preRight, postorder, postLeft + leftSize, postRight - 1);
  return root;
}
void printInorder(Node* root) {
  if (!root) {
    return;
  }
  printInorder(root->left);
  cout << root->value << ' ';
  printInorder(root->right);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> preorder(n), postorder(n);
  for (int& value : preorder) {
    cin >> value;
  }
  for (int& value : postorder) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    postPosition[postorder[i]] = i;
  }
  printInorder(build(preorder, 0, n, postorder, 0, n));
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；若不保证满二叉树，单孩子究竟在左还是在右无法判定。

## 变种三：只验证两种遍历是否可能来自同一棵树

新定义：输入不再保证合法，且无需保留树。递归划分时检查长度、集合、根位置和前序消费边界，失败即返回 `false`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool validate(const vector<int>& preorder, int preLeft, int preRight, int inLeft, int inRight,
    const unordered_map<int, int>& position) {
  if (preRight - preLeft != inRight - inLeft) {
    return false;
  }
  if (preLeft == preRight) {
    return true;
  }
  auto it = position.find(preorder[preLeft]);
  if (it == position.end() || it->second < inLeft || it->second >= inRight) {
    return false;
  }
  int leftSize = it->second - inLeft;
  if (preLeft + 1 + leftSize > preRight) {
    return false;
  }
  return validate(preorder, preLeft + 1, preLeft + 1 + leftSize, inLeft, it->second, position) &&
      validate(preorder, preLeft + 1 + leftSize, preRight, it->second + 1, inRight, position);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> preorder(n), inorder(n);
  for (int& value : preorder) {
    cin >> value;
  }
  unordered_map<int, int> position;
  bool unique = true;
  for (int i = 0; i < n; ++i) {
    cin >> inorder[i];
    unique &= position.emplace(inorder[i], i).second;
  }
  unordered_set<int> seen;
  for (int value : preorder) {
    unique &= seen.insert(value).second;
  }
  cout << (unique && validate(preorder, 0, n, 0, n, position) ? "YES" : "NO") << '\n';
}
```

期望时间 $O(n)$，空间 $O(n)$。

## 变种四：不建树，直接求后序遍历

若目标只是输出后序序列，可用同样的区间划分先递归左、右区间，最后输出根，省去所有节点对象。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void emitPostorder(const vector<int>& preorder, int preLeft, int preRight, int inLeft, int inRight,
    const unordered_map<int, int>& position, vector<int>& answer) {
  if (preLeft == preRight) {
    return;
  }
  int value = preorder[preLeft];
  int middle = position.at(value);
  int leftSize = middle - inLeft;
  emitPostorder(preorder, preLeft + 1, preLeft + 1 + leftSize, inLeft, middle, position, answer);
  emitPostorder(preorder, preLeft + 1 + leftSize, preRight, middle + 1, inRight, position, answer);
  answer.push_back(value);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> preorder(n), inorder(n), answer;
  for (int& value : preorder) {
    cin >> value;
  }
  unordered_map<int, int> position;
  for (int i = 0; i < n; ++i) {
    cin >> inorder[i];
    position[inorder[i]] = i;
  }
  emitPostorder(preorder, 0, n, 0, n, position, answer);
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，除输出与哈希表外只需 $O(h)$ 递归空间，不分配树节点。

## 可复现验证

随机生成最多 100 个互异节点的二叉树，取其前序／中序后分别运行递归与迭代构造，再重新遍历结果，要求两种序列逐项等于输入；另覆盖单节点、全左链、全右链和完全树。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-61-lc41/">← [力扣 Top 61] LC 41 缺失的第一个正数 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-63-lc26/">[力扣 Top 63] LC 26 删除有序数组中的重复项 简单 →</a>
</nav>
