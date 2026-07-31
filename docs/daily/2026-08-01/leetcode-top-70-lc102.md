---
title: "[力扣 Top 70] LC 102 二叉树的层序遍历 中等"
---

# [力扣 Top 70] LC 102 二叉树的层序遍历 中等

<p class="daily-archive-kicker">2026-08-01 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../graph/tree-traversals/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=303c30e3f20f3800f81fbee83730b934e9bdb508fc8e1eccb8091e82708afaa8 -->
## 官方原始信息

- Top 排名：70
- 题号：LC 102
- 官方中文标题：二叉树的层序遍历
- 官方难度：中等
- 官方链接：[二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

### 原始题意

给定二叉树根节点 `root`，按深度从小到大逐层返回节点值，每层内部从左到右。

### 函数签名

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  vector<vector<int>> levelOrder(TreeNode* root);
};
```

### 全部官方样例

```text
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

```text
输入：root = [1]
输出：[[1]]
```

```text
输入：root = []
输出：[]
```

### 全部约束

- 节点数 $0\le n\le2000$。
- $-1000\le Node.val\le1000$。

## 约束推导与边界

层序本质是无权图最短层次 BFS。队列按入队先后保证当前层从左到右；处理一层前固定当前 `queue.size()`，只弹出这么多个节点，把它们的孩子留给下一轮，才能保留二维分层边界。

空树应返回空二维数组而不是包含一个空层。每个节点只入队一次，时间 $O(n)$；队列最大保存某一层宽度 $w$，空间 $O(w)$。

## 解法递进

### 解法一：深度优先并按深度归档

递归到节点时，若首次到达该深度就新建一层，再把值加入对应层。先左后右保证同层顺序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
};
class Solution {
  void visit(TreeNode* node, int depth, vector<vector<int>>& answer) {
    if (!node) {
      return;
    }
    if (depth == static_cast<int>(answer.size())) {
      answer.push_back({});
    }
    answer[depth].push_back(node->val);
    visit(node->left, depth + 1, answer);
    visit(node->right, depth + 1, answer);
  }
public:
  vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> answer;
    visit(root, 0, answer);
    return answer;
  }
};
```

时间 $O(n)$，递归空间 $O(h)$，其中 $h$ 为树高。

### 最佳实用解：队列分层 BFS

<!-- compile:standalone -->
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
  vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> answer;
    if (!root) {
      return answer;
    }
    queue<TreeNode*> queue;
    queue.push(root);
    while (!queue.empty()) {
      int layerSize = queue.size();
      vector<int> layer;
      layer.reserve(layerSize);
      while (layerSize--) {
        TreeNode* node = queue.front();
        queue.pop();
        layer.push_back(node->val);
        if (node->left) {
          queue.push(node->left);
        }
        if (node->right) {
          queue.push(node->right);
        }
      }
      answer.push_back(std::move(layer));
    }
    return answer;
  }
};
```

时间 $O(n)$，队列空间 $O(w)$，输出空间 $O(n)$ 不计入额外空间。

## 正确性证明

开始某轮时，队列恰按从左到右顺序保存同一深度的全部节点。固定 `layerSize` 后，算法只弹出这些节点并按队列顺序记录；每个父节点又先左后右地把下一层孩子加入队尾，所以本轮结束时队列恰按从左到右顺序保存下一深度的全部节点。

根节点满足初始不变量。由深度归纳，每轮生成的层内容与要求一致；队列为空时所有节点均恰好访问一次，因此完整结果正确。

## 样例手推

队列先为 `[3]`，固定层长 1，输出 `[3]` 并加入 9、20；下一轮固定层长 2，输出 `[9,20]`，其中 20 加入 15、7；最后输出 `[15,7]`。空树在入队前返回空结果。

## 易错点与方案比较

- 一层开始时必须先保存队列长度，不能让本轮新入队孩子也被立刻处理。
- 子节点按左、右顺序入队，才能维持题目要求的同层顺序。
- DFS 也能得到相同输出，但极深树可能栈溢出；BFS 与题意一致、空间等于最大宽度，推荐优先记忆。
- 节点值可重复，遍历按节点身份而不是值去重。

## 变种一：之字形层序遍历

偶数深度从左到右，奇数深度从右到左。BFS 入队顺序不变，只改变写入当前层数组的位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    int left, right;
    cin >> nodes[i].value >> left >> right;
    nodes[i].left = left < 0 ? nullptr : &nodes[left];
    nodes[i].right = right < 0 ? nullptr : &nodes[right];
  }
  queue<Node*> queue;
  if (n) {
    queue.push(&nodes[0]);
  }
  bool reverseOrder = false;
  while (!queue.empty()) {
    int size = queue.size();
    vector<int> layer(size);
    for (int i = 0; i < size; ++i) {
      Node* node = queue.front();
      queue.pop();
      layer[reverseOrder ? size - 1 - i : i] = node->value;
      if (node->left) {
        queue.push(node->left);
      }
      if (node->right) {
        queue.push(node->right);
      }
    }
    for (int value : layer) {
      cout << value << ' ';
    }
    cout << '\n';
    reverseOrder = !reverseOrder;
  }
}
```

时间 $O(n)$，空间 $O(w)$。

## 变种二：二叉树的右视图

每层只保留最后弹出的节点值，因为队列顺序是从左到右。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    int left, right;
    cin >> nodes[i].value >> left >> right;
    nodes[i].left = left < 0 ? nullptr : &nodes[left];
    nodes[i].right = right < 0 ? nullptr : &nodes[right];
  }
  queue<Node*> queue;
  if (n) {
    queue.push(&nodes[0]);
  }
  while (!queue.empty()) {
    int size = queue.size();
    int visible = 0;
    while (size--) {
      Node* node = queue.front();
      queue.pop();
      visible = node->value;
      if (node->left) {
        queue.push(node->left);
      }
      if (node->right) {
        queue.push(node->right);
      }
    }
    cout << visible << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(w)$。

## 变种三：自底向上的层序结果

正常 BFS 生成各层，最后反转层数组；节点总工作量不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    int left, right;
    cin >> nodes[i].value >> left >> right;
    nodes[i].left = left < 0 ? nullptr : &nodes[left];
    nodes[i].right = right < 0 ? nullptr : &nodes[right];
  }
  vector<vector<int>> levels;
  queue<Node*> queue;
  if (n) {
    queue.push(&nodes[0]);
  }
  while (!queue.empty()) {
    int size = queue.size();
    levels.push_back({});
    while (size--) {
      Node* node = queue.front();
      queue.pop();
      levels.back().push_back(node->value);
      if (node->left) {
        queue.push(node->left);
      }
      if (node->right) {
        queue.push(node->right);
      }
    }
  }
  reverse(levels.begin(), levels.end());
  for (const auto& level : levels) {
    for (int value : level) {
      cout << value << ' ';
    }
    cout << '\n';
  }
}
```

时间 $O(n)$，包含输出的空间 $O(n)$。

## 变种四：输出每层平均值

每层累加值并除以固定层长。节点值和层宽可能更大时用 `long long` 累计。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* left = nullptr;
  Node* right = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    int left, right;
    cin >> nodes[i].value >> left >> right;
    nodes[i].left = left < 0 ? nullptr : &nodes[left];
    nodes[i].right = right < 0 ? nullptr : &nodes[right];
  }
  queue<Node*> queue;
  if (n) {
    queue.push(&nodes[0]);
  }
  cout << fixed << setprecision(6);
  while (!queue.empty()) {
    int size = queue.size();
    long long sum = 0;
    for (int i = 0; i < size; ++i) {
      Node* node = queue.front();
      queue.pop();
      sum += node->value;
      if (node->left) {
        queue.push(node->left);
      }
      if (node->right) {
        queue.push(node->right);
      }
    }
    cout << static_cast<double>(sum) / size << '\n';
  }
}
```

时间 $O(n)$，空间 $O(w)$。

## 可复现验证

随机生成二叉树，把 BFS 二维结果扁平化后与先序节点集合比较，确认无遗漏；再与 DFS 按深度归档逐层比较。覆盖空树、单节点、完全树、全左链、全右链和重复值。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/binary-tree-level-order-traversal/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/binary-tree-level-order-traversal/)
- [对应知识专题](../../graph/tree-traversals.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-69-lc138/">← [力扣 Top 69] LC 138 随机链表的复制 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-512-q3-lc4002/">[力扣竞赛] 第 512 场周赛 Q3 LC 4002 统计有效序列数目 中等 →</a>
</nav>
