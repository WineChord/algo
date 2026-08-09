---
title: "[力扣 Top 130] LC 437 路径总和 III 中等"
---

# [力扣 Top 130] LC 437 路径总和 III 中等

<p class="daily-archive-kicker">2026-08-09 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=5a11f80f8ae91f8e9eb2a063cddf9e6e0a2acc5cf458e965a93c3ba463f5ae46 -->
## 官方原始信息

- Top 排名：130
- 题号：LC 437
- 官方中文标题：路径总和 III
- 官方难度：中等
- 官方链接：[路径总和 III](https://leetcode.cn/problems/path-sum-iii/)

### 原始题意与函数签名

给定二叉树和目标和，统计节点值之和等于目标的向下路径数。路径可从任意节点开始、在任意节点结束，但方向只能从父到子。

<!-- compile:leetcode-tree -->
```cpp
class Solution {
public:
  int pathSum(TreeNode* root, int targetSum);
};
```

### 全部官方样例

```text
输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：存在三条和为 8 的向下路径。
```

```text
输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：3
```

### 全部约束

- 节点数 $n$ 在 $[0,1000]$ 内。
- $-10^9\le Node.val\le10^9$。
- $-1000\le targetSum\le1000$。
- 路径不要求从根或到叶，但必须向下连续。

## 约束推导与观察

路径和可达 $10^{12}$，必须用 64 位。固定终点 `v`，若根到当前节点的前缀和为 `prefix`，一条从某祖先后继到 `v` 的路径和为目标，当且仅当此前祖先前缀和等于 `prefix-target`。DFS 当前根路径上维护前缀和频次，就能一次得到以当前节点结尾的全部合法路径。

## 解法递进

### 解法一：枚举每个起点再向下搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
class Solution {
  long long from(TreeNode* node, long long remaining) {
    if (!node) {
      return 0;
    }
    long long answer = node->val == remaining;
    answer += from(node->left, remaining - node->val);
    answer += from(node->right, remaining - node->val);
    return answer;
  }
public:
  int pathSum(TreeNode* root, int targetSum) {
    if (!root) {
      return 0;
    }
    return from(root, targetSum) + pathSum(root->left, targetSum) + pathSum(root->right, targetSum);
  }
};
int main() {
}
```

每个节点作为起点向下搜索，最坏链状树时间 $O(n^2)$，递归空间 $O(h)$。

### 解法二：保存当前路径的全部前缀和并线性扫描

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
class Solution {
  int target;
  vector<long long> prefixes = {0};
  long long dfs(TreeNode* node, long long prefix) {
    if (!node) {
      return 0;
    }
    prefix += node->val;
    long long answer = 0;
    for (long long old : prefixes) {
      answer += prefix - old == target;
    }
    prefixes.push_back(prefix);
    answer += dfs(node->left, prefix) + dfs(node->right, prefix);
    prefixes.pop_back();
    return answer;
  }
public:
  int pathSum(TreeNode* root, int targetSum) {
    target = targetSum;
    return dfs(root, 0);
  }
};
int main() {
}
```

时间 $O(nh)$、空间 $O(h)$；已经把路径表达成前缀差，但查找仍是线性。

### 最佳实用解：当前根路径上的前缀和频次

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
class Solution {
  unordered_map<long long, int> frequency{{0, 1}};
  long long target;
  long long dfs(TreeNode* node, long long prefix) {
    if (!node) {
      return 0;
    }
    prefix += node->val;
    long long answer = frequency[prefix - target];
    ++frequency[prefix];
    answer += dfs(node->left, prefix);
    answer += dfs(node->right, prefix);
    if (--frequency[prefix] == 0) {
      frequency.erase(prefix);
    }
    return answer;
  }
public:
  int pathSum(TreeNode* root, int targetSum) {
    target = targetSum;
    return dfs(root, 0);
  }
};
int main() {
}
```

期望时间 $O(n)$、空间 $O(h)$。哈希表必须随 DFS 回溯，才能只表示当前祖先链。

## 正确性证明

进入节点 `v` 后，`frequency[x]` 恰等于根到 `v` 父节点这条链上前缀和为 `x` 的位置数，并包含根前的空前缀 0。以 `v` 结尾、和为 `target` 的路径与一个前缀和为 `prefix-target` 的祖先位置一一对应，所以本节点新增计数正确。加入当前前缀后递归子树，使其成为子节点的合法祖先；离开时减去，恢复父调用不变量，避免把另一分支节点误当祖先。所有节点作为终点各处理一次，故总数正确。

## 样例手推

样例 1 沿根到节点 3 的路径，前缀和依次为 10、15、18；当到达 3 时查找 `18-8=10`，命中根后的前缀位置，得到路径 `5→3`。同理得到 `5→2→1` 与 `-3→11`。回溯离开左子树后其前缀被删除，不会与右子树拼出非法路径。

## 易错点与方案比较

- 前缀和必须用 `long long`；节点数乘节点值会超过 32 位。
- 初始 `frequency[0]=1` 用于统计从根开始的路径。
- 查询应发生在加入当前前缀之前，否则 `target=0` 时会错误统计空路径。
- 回溯时必须减频次；全局永久保留会把非祖先节点连成路径。

## 变种一：返回所有合法路径的节点值序列

新定义：不仅计数，还恢复全部向下路径。当前路径保存节点值与前缀和；命中旧前缀时复制对应后缀。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
vector<vector<int>> collectPaths(TreeNode* root, long long target) {
  vector<vector<int>> answers;
  vector<int> values;
  vector<long long> prefix{0};
  auto dfs = [&](auto&& self, TreeNode* node) -> void {
    if (!node) {
      return;
    }
    values.push_back(node->val);
    prefix.push_back(prefix.back() + node->val);
    for (int start = 0; start + 1 < static_cast<int>(prefix.size()); ++start) {
      if (prefix.back() - prefix[start] == target) {
        answers.emplace_back(values.begin() + start, values.end());
      }
    }
    self(self, node->left);
    self(self, node->right);
    prefix.pop_back();
    values.pop_back();
  };
  dfs(dfs, root);
  return answers;
}
int main() {
}
```

查找时间 $O(nh)$，复制输出还需与总输出长度成正比；空间 $O(h)$ 加输出。

## 变种二：同一棵树查询多个目标和

新定义：给定 `q` 个目标，同时统计。每到一个节点，对每个目标查询一次当前前缀频次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
vector<long long> pathSumMany(TreeNode* root, const vector<long long>& targets) {
  vector<long long> answers(targets.size());
  unordered_map<long long, int> frequency{{0, 1}};
  auto dfs = [&](auto&& self, TreeNode* node, long long prefix) -> void {
    if (!node) {
      return;
    }
    prefix += node->val;
    for (int i = 0; i < static_cast<int>(targets.size()); ++i) {
      auto it = frequency.find(prefix - targets[i]);
      if (it != frequency.end()) {
        answers[i] += it->second;
      }
    }
    ++frequency[prefix];
    self(self, node->left, prefix);
    self(self, node->right, prefix);
    --frequency[prefix];
  };
  dfs(dfs, root, 0);
  return answers;
}
int main() {
}
```

期望时间 $O(nq)$、空间 $O(h+q)$。

## 变种三：路径和落在区间 `[low,high]`

新定义：统计和处于闭区间的向下路径。需要统计祖先前缀落在 `[prefix-high,prefix-low]`，坐标压缩所有根前缀后用树状数组维护当前路径。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
long long countPathRange(TreeNode* root, long long low, long long high) {
  vector<long long> coordinates{0};
  auto collect = [&](auto&& self, TreeNode* node, long long prefix) -> void {
    if (!node) {
      return;
    }
    prefix += node->val;
    coordinates.push_back(prefix);
    self(self, node->left, prefix);
    self(self, node->right, prefix);
  };
  collect(collect, root, 0);
  sort(coordinates.begin(), coordinates.end());
  coordinates.erase(unique(coordinates.begin(), coordinates.end()), coordinates.end());
  vector<int> bit(coordinates.size() + 1);
  auto add = [&](long long value, int delta) {
    int index =
        lower_bound(coordinates.begin(), coordinates.end(), value) - coordinates.begin() + 1;
    for (int i = index; i < static_cast<int>(bit.size()); i += i & -i) {
      bit[i] += delta;
    }
  };
  auto countAtMost = [&](long long value) {
    int index = upper_bound(coordinates.begin(), coordinates.end(), value) - coordinates.begin();
    int result = 0;
    for (int i = index; i > 0; i -= i & -i) {
      result += bit[i];
    }
    return result;
  };
  long long answer = 0;
  add(0, 1);
  auto dfs = [&](auto&& self, TreeNode* node, long long prefix) -> void {
    if (!node) {
      return;
    }
    prefix += node->val;
    answer += countAtMost(prefix - low) - countAtMost(prefix - high - 1);
    add(prefix, 1);
    self(self, node->left, prefix);
    self(self, node->right, prefix);
    add(prefix, -1);
  };
  dfs(dfs, root, 0);
  return answer;
}
int main() {
}
```

时间 $O(n\log n)$、空间 $O(n)$。

## 变种四：路径必须恰含 `k` 个节点

新定义：再限制路径长度恰为 `k`。对当前深度，合法起点前的前缀位置唯一，直接比较相差 `k` 层的前缀和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
  explicit TreeNode(int x = 0) : val(x), left(nullptr), right(nullptr) {
  }
};
long long countExactLength(TreeNode* root, int k, long long target) {
  vector<long long> prefix{0};
  long long answer = 0;
  auto dfs = [&](auto&& self, TreeNode* node) -> void {
    if (!node) {
      return;
    }
    prefix.push_back(prefix.back() + node->val);
    int edgesFromRoot = prefix.size() - 1;
    if (edgesFromRoot >= k && prefix.back() - prefix[edgesFromRoot - k] == target) {
      ++answer;
    }
    self(self, node->left);
    self(self, node->right);
    prefix.pop_back();
  };
  dfs(dfs, root);
  return answer;
}
int main() {
}
```

时间 $O(n)$、空间 $O(h)$。

## 可复现验证

随机生成不超过 14 个节点、值域 `-5..5` 的二叉树，对每个目标 `-20..20`，以“枚举起点再 DFS”为 oracle，对比前缀数组和哈希频次；固定覆盖空树、链、全零、重复前缀和。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/path-sum-iii/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-129-lc349/">← [力扣 Top 129] LC 349 两个数组的交集 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-biweekly-188-q1-lc4006/">[力扣竞赛] 第 188 场双周赛 Q1 LC 4006 统计有效前缀数目 简单 →</a>
</nav>
