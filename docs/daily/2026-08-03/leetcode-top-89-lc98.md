---
title: "[力扣 Top 89] LC 98 验证二叉搜索树 中等"
---

# [力扣 Top 89] LC 98 验证二叉搜索树 中等

<p class="daily-archive-kicker">2026-08-03 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d01b2eb300a7b0e75b1b6869d56d0a522eedcb31429bf162dd7af86682b2f561 -->
## 官方原始信息

- Top 排名：89
- 题号：LC 98
- 官方中文标题：验证二叉搜索树
- 官方难度：中等
- 官方链接：[验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/)

### 原始题意

判断一棵二叉树是否为有效二叉搜索树：每个节点左子树的所有值都严格小于该节点，右子树的所有值都严格大于该节点，并且左右子树本身也满足同一条件。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  bool isValidBST(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [2,1,3]
输出：true
```

```text
输入：root = [5,1,4,null,null,3,6]
输出：false
解释：根节点 5 的右子节点值为 4，不严格大于 5。
```

### 全部约束

- 节点数在 $[1,10^4]$。
- $-2^{31}\le Node.val\le2^{31}-1$。

## 约束推导与全局不变量

只比较节点与直接孩子不够：例如根 5 的右子树深处出现 3，局部可能满足父子关系，却违反根的全局下界。每个递归位置都应携带由所有祖先共同限定的开区间 `(lower,upper)`；左子树收紧上界为当前值，右子树收紧下界为当前值。

节点值覆盖完整 `int` 范围，若用 `INT_MIN/INT_MAX` 作严格边界，会错误拒绝边界值或需要脆弱的加减一。使用 `long long` 初始边界 `LLONG_MIN/LLONG_MAX`，并直接做严格比较。

另一等价性质是：有效 BST 的中序遍历值序列严格递增。迭代中序只需保存前一个值，避免最坏深度 $10^4$ 的递归栈风险，但显式栈仍为 $O(h)$。

## 解法递进

### 解法一：每个节点重新扫描左右子树极值

对每个节点求左子树最大值、右子树最小值，再递归验证。它直接覆盖定义，但退化链上重复扫描导致平方时间。

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long minimum(TreeNode* node) {
    if (!node)
      return LLONG_MAX;
    return min<long long>(node->val, min(minimum(node->left), minimum(node->right)));
  }
  long long maximum(TreeNode* node) {
    if (!node)
      return LLONG_MIN;
    return max<long long>(node->val, max(maximum(node->left), maximum(node->right)));
  }
public:
  bool isValidBST(TreeNode* root) {
    if (!root)
      return true;
    if (maximum(root->left) >= root->val || minimum(root->right) <= root->val)
      return false;
    return isValidBST(root->left) && isValidBST(root->right);
  }
};
```

最坏时间 $O(n^2)$，递归栈 $O(h)$。

### 解法二：祖先开区间递归

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool validate(TreeNode* node, long long lower, long long upper) {
    if (!node)
      return true;
    if (node->val <= lower || node->val >= upper)
      return false;
    return validate(node->left, lower, node->val) && validate(node->right, node->val, upper);
  }
public:
  bool isValidBST(TreeNode* root) {
    return validate(root, LLONG_MIN, LLONG_MAX);
  }
};
```

时间 $O(n)$，递归栈 $O(h)$，证明最直接。

### 最佳实用解：迭代中序严格递增

<!-- compile:leetcode-tree -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isValidBST(TreeNode* root) {
    vector<TreeNode*> stack;
    TreeNode* current = root;
    long long previous = LLONG_MIN;
    while (current || !stack.empty()) {
      while (current) {
        stack.push_back(current);
        current = current->left;
      }
      current = stack.back();
      stack.pop_back();
      if (current->val <= previous)
        return false;
      previous = current->val;
      current = current->right;
    }
    return true;
  }
};
```

时间 $O(n)$，空间 $O(h)$。它不依赖系统递归深度，对高度 $10^4$ 的链更稳健，是最佳实用解。

## 正确性证明

二叉树的中序顺序先遍历全部左子树，再访问根，最后遍历全部右子树。若树为 BST，左侧所有值严格小于根、右侧所有值严格大于根，并对子树递归成立，因此中序序列严格递增。反之，若中序序列严格递增，则任一节点之前连续出现的左子树全部值小于它，之后连续出现的右子树全部值大于它；对子树的中序子序列同样严格递增，递归满足 BST 定义。因此“中序严格递增”与有效 BST 等价。算法按中序逐节点访问并检查相邻值严格递增，故返回结果正确。

## 样例手推

`[2,1,3]` 的中序为 1、2、3，严格递增。`[5,1,4,null,null,3,6]` 的中序为 1、5、3、4、6；访问 3 时发现 $3\le5$，立即返回假，准确捕获右子树深处违反根下界的问题。

## 易错点与方案比较

- BST 是严格不等，重复值无论在左还是右都非法。
- 只比较父子节点会漏掉祖先约束。
- 初始前值必须比 `INT_MIN` 更小，使用 `long long` 哨兵。
- 中序检查的是严格递增 `current > previous`，不能写成非递减。
- 边界递归最便于证明，中序迭代避免递归栈溢出；工程实现优先迭代版。

## 变种一：返回第一个中序违规节点

新定义：若无效，输出中序遍历中第一个不大于前驱的节点值；若有效输出 `VALID`。保存前一节点指针即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long value;
  Node* left;
  Node* right;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, rootIndex;
  cin >> n >> rootIndex;
  vector<Node> nodes(n);
  vector<int> left(n), right(n);
  for (int i = 0; i < n; ++i)
    cin >> nodes[i].value >> left[i] >> right[i];
  for (int i = 0; i < n; ++i) {
    nodes[i].left = left[i] == -1 ? nullptr : &nodes[left[i]];
    nodes[i].right = right[i] == -1 ? nullptr : &nodes[right[i]];
  }
  vector<Node*> stack;
  Node* current = rootIndex == -1 ? nullptr : &nodes[rootIndex];
  Node* previous = nullptr;
  while (current || !stack.empty()) {
    while (current)
      stack.push_back(current), current = current->left;
    current = stack.back();
    stack.pop_back();
    if (previous && current->value <= previous->value) {
      cout << current->value << '\n';
      return 0;
    }
    previous = current;
    current = current->right;
  }
  cout << "VALID\n";
}
```

时间 $O(n)$，空间 $O(h)$。

## 变种二：允许重复值只出现在右子树

新定义：左子树严格小于根，右子树允许大于等于根。边界必须携带开闭属性；这里用 `long long` 下界并在右递归允许等号，左侧仍严格。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long value;
  Node* left;
  Node* right;
};
bool validate(Node* node, long long lower, long long upper, bool lowerInclusive) {
  if (!node)
    return true;
  if (node->value < lower || (!lowerInclusive && node->value == lower) || node->value >= upper)
    return false;
  return validate(node->left, lower, node->value, lowerInclusive) &&
      validate(node->right, node->value, upper, true);
}
int main() {
  int n, root;
  cin >> n >> root;
  vector<Node> nodes(n);
  vector<int> left(n), right(n);
  for (int i = 0; i < n; ++i)
    cin >> nodes[i].value >> left[i] >> right[i];
  for (int i = 0; i < n; ++i) {
    nodes[i].left = left[i] < 0 ? nullptr : &nodes[left[i]];
    nodes[i].right = right[i] < 0 ? nullptr : &nodes[right[i]];
  }
  cout << (validate(&nodes[root], LLONG_MIN, LLONG_MAX, true) ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，栈 $O(h)$。若节点值允许 `LLONG_MIN`，应改用 `optional` 边界而非哨兵。

## 变种三：求最大 BST 子树的节点数

新定义：整棵树可能无效，求其中节点数最多的、完整以某节点为根的 BST 子树。后序返回子树是否有效、极值、大小和全局最佳。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left;
  Node* right;
};
struct Info {
  bool valid;
  long long minimum;
  long long maximum;
  int size;
  int best;
};
Info solve(Node* node) {
  if (!node)
    return {true, LLONG_MAX, LLONG_MIN, 0, 0};
  Info left = solve(node->left);
  Info right = solve(node->right);
  if (left.valid && right.valid && left.maximum < node->value && node->value < right.minimum) {
    int size = left.size + right.size + 1;
    return {true, min<long long>(left.minimum, node->value),
        max<long long>(right.maximum, node->value), size, size};
  }
  return {false, 0, 0, 0, max(left.best, right.best)};
}
int main() {
  int n, root;
  cin >> n >> root;
  vector<Node> nodes(n);
  vector<int> left(n), right(n);
  for (int i = 0; i < n; ++i)
    cin >> nodes[i].value >> left[i] >> right[i];
  for (int i = 0; i < n; ++i) {
    nodes[i].left = left[i] < 0 ? nullptr : &nodes[left[i]];
    nodes[i].right = right[i] < 0 ? nullptr : &nodes[right[i]];
  }
  cout << solve(&nodes[root]).best << '\n';
}
```

时间 $O(n)$，递归栈 $O(h)$。

## 变种四：动态插入后保持 BST 有效

新定义：从空树开始依次插入互异键，并在每次插入后输出当前中序。按比较沿唯一搜索路径接到空孩子，构造过程保持全局边界不变量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
void insert(Node*& root, Node* node) {
  if (!root) {
    root = node;
    return;
  }
  if (node->value < root->value)
    insert(root->left, node);
  else
    insert(root->right, node);
}
void print(Node* root) {
  if (!root)
    return;
  print(root->left);
  cout << root->value << ' ';
  print(root->right);
}
int main() {
  int n;
  cin >> n;
  vector<Node> nodes(n);
  Node* root = nullptr;
  for (Node& node : nodes) {
    cin >> node.value;
    insert(root, &node);
  }
  print(root);
  cout << '\n';
}
```

平均时间 $O(n\log n)$、最坏 $O(n^2)$，栈为树高；要保证对数高度需平衡树。

## 验证说明

本轮将六段代码按 C++23 编译；迭代中序会与祖先边界递归在随机二叉树上对拍，并覆盖官方样例、单节点、`INT_MIN/INT_MAX`、重复值、祖孙违规与高度链。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/validate-binary-search-tree/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-88-lc10/">← [力扣 Top 88] LC 10 正则表达式匹配 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-90-lc1929/">[力扣 Top 90] LC 1929 数组串联 简单 →</a>
</nav>
