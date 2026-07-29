---
title: "[力扣竞赛] 第 511 场周赛 Q2 LC 3997 统计二叉树中支配节点的数量 中等"
---

# [力扣竞赛] 第 511 场周赛 Q2 LC 3997 统计二叉树中支配节点的数量 中等

<p class="daily-archive-kicker">2026-07-27 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

Official problem: [Open the official problem](https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/)

## Official source record

- Platform and contest: LeetCode China, 第 511 场周赛.
- Official problem identity: LC 3997, slug `count-dominant-nodes-in-a-binary-tree`.
- Official Chinese title: 统计二叉树中支配节点的数量.
- Official English title: Count Dominant Nodes in a Binary Tree.
- Official difficulty: 中等 / Medium.
- Official contest position and points: Q2, 4 points.
- ZeroTracer community-estimated contest rating: `1426.5661260433`, retrieved 2026-07-27. This is not an official LeetCode difficulty.
- Official topic tags returned by the current problem API: none.
- Program interface: LeetCode C++ function signature.

## Complete statement semantics

Given the root of a **complete binary tree**, call a node $x$ **dominant** when its value equals the maximum value among every node in the subtree rooted at $x$. Return the total number of dominant nodes.

A complete binary tree has every level except possibly the last completely filled, and its final level is filled from left to right. A subtree rooted at $x$ contains $x$ and all descendants of $x$.

### Official function signature

```text
int countDominantNodes(TreeNode* root)
```

### All official constraints

- The number of nodes is in $[1,10^5]$.
- $1\le\texttt{Node.val}\le10^9$.
- The input is guaranteed to be a complete binary tree.

### All official examples and images

Example 1 official image:

![Example 1 complete binary tree](../../assets/daily/official/91ca4e925060-tnew.png)

- Official image dimensions: 300 by 193 pixels.
- Input: `root = [5,3,8,2,4,7,1]`
- Output: `5`
- Explanation: leaves 2, 4, 7, and 1 are dominant. Node 8 is also dominant because 8 is the maximum in subtree `[8,7,1]`.

Example 2 official image:

![Example 2 complete binary tree](../../assets/daily/official/4be799b743d8-t9.png)

- Official image dimensions: 250 by 183 pixels.
- Input: `root = [1,2,3,1,2]`
- Output: `4`
- Explanation: the three leaves are dominant. The internal node of value 2 with subtree `[2,1,2]` is also dominant.

## 中文题意与样例说明

给定一棵完整二叉树。若节点值等于以该节点为根的整棵子树中的最大值，则称它为支配节点；子树包含节点自身与全部后代。返回整棵树中支配节点的数量。

样例 1 的四个叶子天然满足条件，值为 8 的内部节点也是其子树最大值，所以答案为 5。样例 2 的三个叶子和左侧值为 2 的内部节点满足条件，答案为 4。完整二叉树的最后一层从左到右填充；函数签名、全部约束、示例图片和数据以上方官方信息为准。

## Constraint-driven observations

The definition points from descendants toward their ancestor, so postorder is the natural direction: both child-subtree maxima must be known before deciding the parent. Equality matters—if several nodes tie for the subtree maximum, the subtree root is dominant whenever it has that same value.

Completeness gives height $O(\log n)$. With $n\le10^5$, recursive postorder is safe here and uses only $O(\log n)$ call-stack frames. The values and answer fit in `int`; no sums are required.

Important boundaries:

- A leaf is always dominant.
- A one-node tree returns 1.
- If all values are equal, every node is dominant.
- The root is dominant exactly when it is a global maximum.
- A large descendant invalidates every smaller ancestor on its ancestor chain, but not nodes in unrelated subtrees.

## Example 1 postorder evolution

The leaves return maxima 2, 4, 7, and 1 and each contributes one. Node 3 receives child maxima 2 and 4, so its subtree maximum is 4 and it contributes zero. Node 8 receives 7 and 1, so its subtree maximum remains 8 and it contributes one. Root 5 receives subtree maxima 4 and 8, so its subtree maximum is 8 and it contributes zero. Total: $4+1=5$.

## Solution 1: rescan every subtree

For every node, independently traverse its subtree to obtain the maximum, then recurse to count the same property at its children.

This is a correct brute force because it directly evaluates the definition at each node. In a complete tree, level $d$ contains $2^d$ nodes and each such subtree has $O(n/2^d)$ nodes, so every level costs $O(n)$, for $O(n\log n)$ total. Without completeness, a chain would degrade to $O(n^2)$.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
  int subtreeMax(TreeNode* node) {
    if (!node) return INT_MIN;
    return max({node->val, subtreeMax(node->left), subtreeMax(node->right)});
  }
  int count(TreeNode* node) {
    if (!node) return 0;
    return (node->val == subtreeMax(node)) + count(node->left) + count(node->right);
  }
public:
  int countDominantNodes(TreeNode* root) {
    return count(root);
  }
};
```

- Time: $O(n\log n)$ for the guaranteed complete tree.
- Extra space: $O(\log n)$.
- Bottleneck: every descendant maximum is recomputed once for each ancestor.

## Solution 2: one postorder aggregation — recommended

Return two facts from each subtree: its maximum and its dominant-node count. Each node is processed once.

### Correctness proof

Induct on subtree size. The empty subtree returns maximum $-\infty$ and count zero, which is correct. Assume both child results are correct. The current subtree maximum is the maximum of the current value and the two child maxima, so the current node is dominant exactly when its value equals that computed maximum. The dominant nodes in the current subtree are precisely the dominant nodes in the left subtree, those in the right subtree, and possibly the current node; these sets are disjoint. Therefore the returned count and maximum are correct. Induction proves the root result.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
  pair<int, int> dfs(TreeNode* node) {
    if (!node) return {INT_MIN, 0};
    auto [leftMax, leftCount] = dfs(node->left);
    auto [rightMax, rightCount] = dfs(node->right);
    int subtreeMax = max({node->val, leftMax, rightMax});
    int count = leftCount + rightCount + (node->val == subtreeMax);
    return {subtreeMax, count};
  }
public:
  int countDominantNodes(TreeNode* root) {
    return dfs(root).second;
  }
};
```

- Time: $O(n)$.
- Extra space: $O(\log n)$ from the guaranteed complete-tree height.
- Recommendation: remember this postorder “return the aggregate needed by the parent” pattern. It is shorter, asymptotically optimal, and generalizes to arbitrary subtree statistics.

## Same-order alternative: reverse heap order

Completeness means breadth-first order is exactly the implicit heap order: children of index $i$ are $2i+1$ and $2i+2$. Process that array backward.

This avoids recursion but spends $O(n)$ memory. It is useful when the input already arrives in level order or recursion is prohibited.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
public:
  int countDominantNodes(TreeNode* root) {
    vector<TreeNode*> nodes;
    queue<TreeNode*> que;
    que.push(root);
    while (!que.empty()) {
      TreeNode* node = que.front();
      que.pop();
      nodes.push_back(node);
      if (node->left) que.push(node->left);
      if (node->right) que.push(node->right);
    }
    int n = nodes.size();
    vector<int> subtreeMax(n);
    int ans = 0;
    for (int i = n - 1; i >= 0; --i) {
      int value = nodes[i]->val;
      int left = 2 * i + 1;
      int right = 2 * i + 2;
      if (left < n) value = max(value, subtreeMax[left]);
      if (right < n) value = max(value, subtreeMax[right]);
      subtreeMax[i] = value;
      ans += nodes[i]->val == value;
    }
    return ans;
  }
};
```

- Time: $O(n)$.
- Extra space: $O(n)$.
- Trade-off: more memory than recursive postorder, but no call stack and excellent cache locality for array-form input.

## Common mistakes

- Using preorder: the parent cannot be decided before descendant maxima are known.
- Checking `>` instead of equality with the subtree maximum; ties are valid.
- Comparing only with immediate children rather than all descendants.
- Confusing this property with “good nodes” on a root-to-node path.
- Returning the current value instead of the full subtree maximum.
- Assuming `nullptr` has maximum zero in a generalized version that permits negative values; `INT_MIN` is robust.

## Follow-up 1: strict dominance over proper descendants

**New definition.** A node is strictly dominant when its value is greater than every proper descendant. Leaves qualify vacuously.

Equality now invalidates an internal node, so compare with the maximum of the two child subtrees before inserting the current value.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
  pair<int, int> dfs(TreeNode* node) {
    if (!node) return {INT_MIN, 0};
    auto [leftMax, leftCount] = dfs(node->left);
    auto [rightMax, rightCount] = dfs(node->right);
    int descendantMax = max(leftMax, rightMax);
    int count = leftCount + rightCount + (node->val > descendantMax);
    return {max(node->val, descendantMax), count};
  }
public:
  int countStrictDominantNodes(TreeNode* root) {
    return dfs(root).second;
  }
};
```

- Time: $O(n)$.
- Extra space: $O(h)$, where $h$ is tree height.

## Follow-up 2: root-to-node “good nodes”

**New definition.** Count nodes whose value is at least every value on the path from the root to that node.

The original bottom-up aggregate no longer matches the dependency. Carry a prefix maximum top-down instead.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
  int dfs(TreeNode* node, int prefixMax) {
    if (!node) return 0;
    int good = node->val >= prefixMax;
    int nextMax = max(prefixMax, node->val);
    return good + dfs(node->left, nextMax) + dfs(node->right, nextMax);
  }
public:
  int countPathDominantNodes(TreeNode* root) {
    return dfs(root, INT_MIN);
  }
};
```

- Time: $O(n)$.
- Extra space: $O(h)$.
- Model change: subtree properties usually aggregate upward; path-prefix properties propagate downward.

## Follow-up 3: recover all dominant heap indices

**New definition.** Return the one-based breadth-first indices of all dominant nodes in increasing order.

The reverse-heap computation already obtains every subtree maximum; record indices whose root value matches it.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
public:
  vector<int> dominantIndices(TreeNode* root) {
    vector<TreeNode*> nodes;
    queue<TreeNode*> que;
    que.push(root);
    while (!que.empty()) {
      TreeNode* node = que.front();
      que.pop();
      nodes.push_back(node);
      if (node->left) que.push(node->left);
      if (node->right) que.push(node->right);
    }
    int n = nodes.size();
    vector<int> subtreeMax(n);
    vector<int> answer;
    for (int i = n - 1; i >= 0; --i) {
      int value = nodes[i]->val;
      if (2 * i + 1 < n) value = max(value, subtreeMax[2 * i + 1]);
      if (2 * i + 2 < n) value = max(value, subtreeMax[2 * i + 2]);
      subtreeMax[i] = value;
      if (nodes[i]->val == value) answer.push_back(i + 1);
    }
    reverse(answer.begin(), answer.end());
    return answer;
  }
};
```

- Time: $O(n)$.
- Extra space: $O(n)$, including the output.

## Follow-up 4: online value updates on a complete tree

**New definition.** The tree shape is fixed and stored in one-based heap order. `U i x` changes node $i$ to value $x$; `Q` asks for the current total dominant count.

Only the updated node and its ancestors can change subtree maxima or dominance. Recompute that $O(\log n)$-length path.

<!-- compile:leetcode -->
```cpp
// STANDALONE
#include <bits/stdc++.h>
using namespace std;
class DominantTracker {
  int n;
  int total = 0;
  vector<long long> value, subtreeMax;
  vector<char> dominant;
  void recalc(int i) {
    long long nextMax = value[i];
    if (2 * i <= n) nextMax = max(nextMax, subtreeMax[2 * i]);
    if (2 * i + 1 <= n) nextMax = max(nextMax, subtreeMax[2 * i + 1]);
    bool nextDominant = value[i] == nextMax;
    total += nextDominant - dominant[i];
    dominant[i] = nextDominant;
    subtreeMax[i] = nextMax;
  }
public:
  explicit DominantTracker(vector<long long> initial) {
    n = (int)initial.size() - 1;
    value = std::move(initial);
    subtreeMax.resize(n + 1);
    dominant.assign(n + 1, false);
    for (int i = n; i >= 1; --i) recalc(i);
  }
  void update(int i, long long x) {
    value[i] = x;
    while (i >= 1) {
      recalc(i);
      i /= 2;
    }
  }
  int count() const {
    return total;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> value(n + 1);
  for (int i = 1; i <= n; ++i) cin >> value[i];
  DominantTracker tracker(std::move(value));
  while (q--) {
    char type;
    cin >> type;
    if (type == 'Q') {
      cout << tracker.count() << '\n';
    } else {
      int i;
      long long x;
      cin >> i >> x;
      tracker.update(i, x);
    }
  }
}
```

- Build: $O(n)$.
- Update: $O(\log n)$.
- Query: $O(1)$.
- Space: $O(n)$.

## Follow-up 5: value lies among the subtree’s top $k$

**New definition.** A node qualifies when fewer than $k$ nodes in its subtree have a strictly larger value. Equal values share rank.

Keep only the $k$ largest values from each subtree. If at least $k$ descendants exceed the current value, all those $k$ witnesses survive truncation; otherwise every larger value survives, so the decision is exact.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
  struct State {
    vector<int> top;
    int count;
  };
  State dfs(TreeNode* node, int k) {
    if (!node) return {{}, 0};
    State left = dfs(node->left, k);
    State right = dfs(node->right, k);
    vector<int> top = std::move(left.top);
    top.insert(top.end(), right.top.begin(), right.top.end());
    int greaterCount = 0;
    for (int value : top) greaterCount += value > node->val;
    int count = left.count + right.count + (greaterCount < k);
    top.push_back(node->val);
    sort(top.begin(), top.end(), std::greater<int>());
    if ((int)top.size() > k) top.resize(k);
    return {std::move(top), count};
  }
public:
  int countTopKSubtreeNodes(TreeNode* root, int k) {
    return dfs(root, k).count;
  }
};
```

- Time: $O(nk\log k)$.
- Extra space: $O(kh)$ plus temporary merge storage.
- When $k=1$, this becomes the original non-strict dominance definition.

## Follow-up 6: arbitrary deep binary tree without recursion

**New definition.** Drop completeness and allow a tree whose height may be $n$.

The recursive algorithm risks stack overflow. Build a traversal order explicitly, then process it backward as postorder. Unlike the complete-tree heap alternative, this works with arbitrary missing children.

<!-- compile:leetcode-tree -->
```cpp
// LEETCODE_SNIPPET
class Solution {
public:
  int countDominantNodesIterative(TreeNode* root) {
    vector<TreeNode*> order;
    vector<TreeNode*> stack = {root};
    while (!stack.empty()) {
      TreeNode* node = stack.back();
      stack.pop_back();
      order.push_back(node);
      if (node->left) stack.push_back(node->left);
      if (node->right) stack.push_back(node->right);
    }
    unordered_map<TreeNode*, int> subtreeMax;
    int ans = 0;
    for (auto it = order.rbegin(); it != order.rend(); ++it) {
      TreeNode* node = *it;
      int value = node->val;
      if (node->left) value = max(value, subtreeMax[node->left]);
      if (node->right) value = max(value, subtreeMax[node->right]);
      subtreeMax[node] = value;
      ans += node->val == value;
    }
    return ans;
  }
};
```

- Time: expected $O(n)$.
- Extra space: $O(n)$.

## Reproducible verification plan

- Compile every snippet in C++23 mode with the official `TreeNode` contract supplied by the harness.
- Generate random complete trees and compare the $O(n\log n)$ subtree-rescan oracle, recursive postorder, and reverse-heap implementations.
- Include duplicate-heavy, strictly increasing heap-order, strictly decreasing heap-order, all-equal, and one-node trees.
- For the update tracker, randomly mutate heap positions and compare each query with full bottom-up recomputation.

## Sources

- Official problem and GraphQL metadata: [Open the official problem](https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/)
- Official contest discussion and 4-point assignment: [Open the official contest](https://leetcode.cn/discuss/post/3998508/di-511-chang-li-kou-zhou-sai-by-leetcode-4cwf/)
- Official contest page: [Open the official contest](https://leetcode.cn/contest/weekly-contest-511/)
- ZeroTracer dataset: [打开来源页面](https://github.com/zerotrac/leetcode_problem_rating/blob/main/ratings.txt)

## Reference

- [官方题目](https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-20-lc54/">← [力扣 Top 20] LC 54 螺旋矩阵 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-b/">[codeforces] CF Round 1111 Div.2 B Yet Another Constructive →</a>
</nav>
