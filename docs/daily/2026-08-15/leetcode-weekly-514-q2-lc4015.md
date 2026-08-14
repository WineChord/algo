---
title: "[力扣竞赛] 第 514 场周赛 Q2 LC 4015 树的加权和 中等"
---

# [力扣竞赛] 第 514 场周赛 Q2 LC 4015 树的加权和 中等

<p class="daily-archive-kicker">2026-08-15 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-15 题目列表</a> · <a href="../../../graph/tree-aggregation/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=296598442518aa2450dd0c93d71c212f3fb1601e7bef9343b94bf78456501717 -->
[官方题目：LC 4015 树的加权和](https://leetcode.cn/problems/weighted-sum-of-a-tree/)

## 官方原始信息

- 比赛：第 514 场周赛。
- 题目：Q2，公开题号 LC 4015。
- 标题：树的加权和。
- 官方难度：中等。
- 官方比赛分值：4 分。
- 官方链接：[力扣中国](https://leetcode.cn/problems/weighted-sum-of-a-tree/)。
- ZeroTracer 社区估算竞赛分：截至 2026-08-15 未收录，记为未知。

长度为 $n$ 的数组 `parent` 描述一棵以节点 0 为根、节点编号为 $0\ldots n-1$ 的有效有根树；`parent[0] = -1`，其余 `parent[i]` 是节点 `i` 的父节点。数组 `nums` 给出节点值。

根节点深度为 1，其余节点深度等于从根到该节点的路径所含节点数；树高 $h$ 是最大深度。深度为 $d$ 的节点 `i` 的权重为

$$
nums[i](h-d+1).
$$

返回全部节点权重之和。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  long long weightedSum(vector<int>& parent, vector<int>& nums);
};
```

### 全部官方样例

样例 1：

```text
输入：parent = [-1,0,0,0,2,2], nums = [5,2,3,1,4,6]
输出：37
```

树高为 3。六个节点的深度依次为 `[1,2,2,2,3,3]`，权重依次为 `[15,4,6,2,4,6]`，总和为 37。

样例 2：

```text
输入：parent = [-1,0,1,2], nums = [1,2,3,4]
输出：20
```

这是一条深度为 1 至 4 的链，权重依次为 4、6、6、4，总和为 20。

### 全部约束

- $1\le n\le10^5$。
- `n == parent.length == nums.length`。
- `parent[0] == -1`。
- 对 $1\le i<n$，有 $0\le parent[i]<n$。
- $1\le nums[i]\le10^6$。
- `parent` 保证描述一棵以节点 0 为根的有效树。

## 约束推导与整数边界

直接沿父指针求每个节点深度，在链形树上会重复走同一前缀，最坏为 $O(n^2)$。树的边数恰为 $n-1$，从根进行一次 BFS 或 DFS 就能让每条边只被访问一次，同时得到全部深度和树高。

注意约束没有保证 `parent[i] < i`，所以不能依赖节点编号顺序直接写 `depth[i] = depth[parent[i]] + 1`。构建孩子表后从根遍历不依赖编号拓扑。

单个权重最大约为 $10^6\times10^5=10^{11}$，总和最坏可达 $10^{16}$，超过 32 位整数但小于 64 位有符号整数上限。深度使用 `int`，乘法与答案使用 `long long`。

## 解法递进

### 解法一：每个节点独立沿父指针回到根

对节点 `i` 反复跳到 `parent[i]`，步数就是深度；先求全部深度和高度，再计算权重和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long weightedSum(vector<int>& parent, vector<int>& nums) {
    int n = static_cast<int>(parent.size());
    vector<int> depth(n);
    int height = 0;
    for (int node = 0; node < n; ++node) {
      int current = node;
      int value = 1;
      while (current != 0) {
        current = parent[current];
        ++value;
      }
      depth[node] = value;
      height = max(height, value);
    }
    long long answer = 0;
    for (int node = 0; node < n; ++node) {
      answer += 1LL * nums[node] * (height - depth[node] + 1);
    }
    return answer;
  }
};
int main() {
  vector<int> parent{-1, 0, 0, 0, 2, 2};
  vector<int> nums{5, 2, 3, 1, 4, 6};
  cout << Solution().weightedSum(parent, nums) << '\n';
}
```

链形树上时间 $O(n^2)$，深度数组空间 $O(n)$；$n=10^5$ 时会超时。

### 解法二：记忆化父链深度

深度满足 `depth[0]=1` 与 `depth[i]=depth[parent[i]]+1`。记忆化能把状态数降到 $n$，但递归实现在长度 $10^5$ 的链上可能栈溢出；手写迭代回填则要额外维护当前父链。树遍历能以更直接的方式避免两种问题。

### 最佳实用解：孩子表加 BFS

构建父到子的邻接表，从根开始按层访问。第一次到达孩子时，父深度已经确定，故可直接赋值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long weightedSum(vector<int>& parent, vector<int>& nums) {
    int n = static_cast<int>(parent.size());
    vector<vector<int>> children(n);
    for (int node = 1; node < n; ++node) {
      children[parent[node]].push_back(node);
    }
    vector<int> depth(n);
    queue<int> pending;
    depth[0] = 1;
    pending.push(0);
    int height = 1;
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      for (int child : children[node]) {
        depth[child] = depth[node] + 1;
        height = max(height, depth[child]);
        pending.push(child);
      }
    }
    long long answer = 0;
    for (int node = 0; node < n; ++node) {
      answer += 1LL * nums[node] * (height - depth[node] + 1);
    }
    return answer;
  }
};
int main() {
  vector<int> parent{-1, 0, 1, 2};
  vector<int> nums{1, 2, 3, 4};
  cout << Solution().weightedSum(parent, nums) << '\n';
}
```

建图、遍历和求和均为 $O(n)$；孩子表、深度与队列占 $O(n)$ 空间。

### 同阶方案：迭代 DFS

把队列换成显式栈同样是 $O(n)$ 时间与 $O(n)$ 空间。BFS 的深度语义最直观；DFS 在还要计算子树量时更容易扩展。两者都应使用显式容器，避免链形树递归过深。

## 正确性证明

树中每个非根节点只有一个父节点。BFS 从深度为 1 的根开始；若弹出节点 `u` 时 `depth[u]` 正确，则对每个孩子 `v`，根到 `v` 的唯一路径是在根到 `u` 的路径后再加 `v`，所以 `depth[v]=depth[u]+1` 正确。按遍历顺序归纳，全部节点深度正确。

`height` 取遍历到的全部深度最大值，正是题目定义的树高。最后对每个节点恰加入一次 `nums[i]*(height-depth[i]+1)`，与定义逐项相同，因此总和正确。

## 样例手推与边界

样例 1 的 BFS 层次为：第 1 层 `{0}`，第 2 层 `{1,2,3}`，第 3 层 `{4,5}`，所以 $h=3$。按层系数依次为 3、2、1；各层节点值之和为 5、6、10，答案为 $5\times3+6\times2+10\times1=37$。

- 单节点树：$h=d=1$，答案就是 `nums[0]`。
- 星形树：根系数为 2，全部叶子系数为 1。
- 长链：深度最大为 $n$，显式 BFS 不会发生递归栈溢出。
- 父节点编号可能大于孩子编号，不能按数组自然顺序推深度。
- `height - depth + 1` 至少为 1，不会出现零或负权重系数。

## 方案比较与推荐

逐节点爬父链最接近定义，却重复处理公共祖先；记忆化消除重复，但递归深度与迭代回填增加实现负担；BFS/迭代 DFS 都一次访问每条边。面试中优先写“建孩子表 + BFS”，因为不依赖编号顺序、不怕深链，并能清楚地同步维护最大深度。

## 易错点

- 题目把根深度定义为 1，而不是常见的 0。
- 树高是最大深度，不是边数；公式还带 `+1`。
- 返回类型是 `long long`，乘法前必须提升到 64 位。
- 不能假设 `parent[i] < i`。
- 递归 DFS 在 $10^5$ 长链上可能栈溢出。

## 可复现验证

本页全部完整代码均以 C++23 严格编译。两个官方样例分别得到 37 和 20。固定种子生成 100,000 棵小规模随机有根树并随机重编号，把 BFS 解与逐节点爬父链 oracle 比较；另验证单点、星形、长链、父编号逆序和最大值边界，结果全部一致。

## 变种一：同一棵树回答多组节点值

树结构固定时，预处理每个节点的系数 `height-depth[i]+1`。每组新 `nums` 只做一次点积，无需重复遍历树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class WeightedTree {
  vector<long long> coefficient;
public:
  explicit WeightedTree(const vector<int>& parent) {
    int n = static_cast<int>(parent.size());
    vector<vector<int>> children(n);
    for (int node = 1; node < n; ++node) {
      children[parent[node]].push_back(node);
    }
    vector<int> depth(n);
    queue<int> pending;
    depth[0] = 1;
    pending.push(0);
    int height = 1;
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      for (int child : children[node]) {
        depth[child] = depth[node] + 1;
        height = max(height, depth[child]);
        pending.push(child);
      }
    }
    coefficient.resize(n);
    for (int node = 0; node < n; ++node) {
      coefficient[node] = height - depth[node] + 1;
    }
  }
  long long query(const vector<int>& nums) const {
    long long answer = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      answer += coefficient[i] * nums[i];
    }
    return answer;
  }
};
int main() {
  WeightedTree tree({-1, 0, 1});
  cout << tree.query({2, 3, 4}) << '\n';
}
```

预处理 $O(n)$，每组询问 $O(n)$，存储 $O(n)$。原题只有一组值，直接计算即可。

## 变种二：在线修改一个节点值并询问总和

树结构不变时系数固定。维护当前总和；把节点值从 `old` 改为 `value`，答案只变化 `(value-old)*coefficient[node]`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicWeightedTree {
  vector<int> values;
  vector<long long> coefficient;
  long long total = 0;
public:
  DynamicWeightedTree(const vector<int>& parent, vector<int> nums)
      : values(move(nums)) {
    int n = static_cast<int>(parent.size());
    vector<vector<int>> children(n);
    for (int node = 1; node < n; ++node) {
      children[parent[node]].push_back(node);
    }
    vector<int> depth(n);
    queue<int> pending;
    depth[0] = 1;
    pending.push(0);
    int height = 1;
    while (!pending.empty()) {
      int node = pending.front();
      pending.pop();
      for (int child : children[node]) {
        depth[child] = depth[node] + 1;
        height = max(height, depth[child]);
        pending.push(child);
      }
    }
    coefficient.resize(n);
    for (int node = 0; node < n; ++node) {
      coefficient[node] = height - depth[node] + 1;
      total += coefficient[node] * values[node];
    }
  }
  void update(int node, int value) {
    total += 1LL * (value - values[node]) * coefficient[node];
    values[node] = value;
  }
  long long query() const {
    return total;
  }
};
int main() {
  DynamicWeightedTree tree({-1, 0, 0}, {5, 2, 3});
  tree.update(1, 7);
  cout << tree.query() << '\n';
}
```

构造 $O(n)$，每次修改与查询均为 $O(1)$，空间 $O(n)$。

## 变种三：返回每一深度层的贡献

先按深度汇总节点值，再乘该层统一系数。各层贡献之和仍是原答案，同时给出可解释的分解。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> contributionByDepth(const vector<int>& parent,
  const vector<int>& nums) {
  int n = static_cast<int>(parent.size());
  vector<vector<int>> children(n);
  for (int node = 1; node < n; ++node) {
    children[parent[node]].push_back(node);
  }
  vector<int> depth(n);
  queue<int> pending;
  depth[0] = 1;
  pending.push(0);
  int height = 1;
  while (!pending.empty()) {
    int node = pending.front();
    pending.pop();
    for (int child : children[node]) {
      depth[child] = depth[node] + 1;
      height = max(height, depth[child]);
      pending.push(child);
    }
  }
  vector<long long> levelSum(height + 1);
  for (int node = 0; node < n; ++node) levelSum[depth[node]] += nums[node];
  vector<long long> answer(height + 1);
  for (int d = 1; d <= height; ++d) {
    answer[d] = levelSum[d] * (height - d + 1);
  }
  return answer;
}
int main() {
  vector<long long> answer = contributionByDepth({-1, 0, 0}, {5, 2, 3});
  for (int d = 1; d < static_cast<int>(answer.size()); ++d) {
    cout << answer[d] << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；若只需原答案，可边汇总边累加，不必返回数组。

## 变种四：边带正整数长度，以根到节点距离定义深度

把每条父子边长度加入根距离，令根距离为 0，树高为最大距离，节点系数为 `height-distance+1`。树上根到节点路径唯一，无需 Dijkstra，一次遍历即可累加距离。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long weightedByDistance(const vector<int>& parent,
  const vector<int>& edgeLength, const vector<int>& nums) {
  int n = static_cast<int>(parent.size());
  vector<vector<pair<int, int>>> children(n);
  for (int node = 1; node < n; ++node) {
    children[parent[node]].push_back({node, edgeLength[node]});
  }
  vector<long long> distance(n);
  vector<int> stack{0};
  long long height = 0;
  while (!stack.empty()) {
    int node = stack.back();
    stack.pop_back();
    for (auto [child, length] : children[node]) {
      distance[child] = distance[node] + length;
      height = max(height, distance[child]);
      stack.push_back(child);
    }
  }
  long long answer = 0;
  for (int node = 0; node < n; ++node) {
    answer += 1LL * nums[node] * (height - distance[node] + 1);
  }
  return answer;
}
int main() {
  cout << weightedByDistance({-1, 0, 1}, {0, 3, 2}, {1, 2, 4}) << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。若图中根到节点不再只有一条路径，才需要按最短路定义改用 Dijkstra。

## 变种五：在线向现有节点添加叶子

保存每个节点深度、当前树高、所有节点值之和与当前答案。新叶深度最多是旧高度加 1；若它创造新高度，所有旧节点的系数都增加 1，答案整体增加旧节点值之和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class GrowingTree {
  vector<int> depth{1};
  int height = 1;
  long long valueSum;
  long long answer;
public:
  explicit GrowingTree(int rootValue)
      : valueSum(rootValue), answer(rootValue) {}
  int addLeaf(int parent, int value) {
    int currentDepth = depth[parent] + 1;
    if (currentDepth > height) {
      answer += valueSum;
      height = currentDepth;
    }
    answer += 1LL * value * (height - currentDepth + 1);
    valueSum += value;
    depth.push_back(currentDepth);
    return static_cast<int>(depth.size()) - 1;
  }
  long long query() const {
    return answer;
  }
};
int main() {
  GrowingTree tree(5);
  int child = tree.addLeaf(0, 2);
  tree.addLeaf(child, 4);
  cout << tree.query() << '\n';
}
```

每次添加与查询均为 $O(1)$，保存深度需要 $O(n)$ 空间；该结论依赖操作只添加叶子，不删除或重新挂接旧节点。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/weighted-sum-of-a-tree/)
- [对应知识专题](../../graph/tree-aggregation.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-135-lc85/">← [力扣 Top 135] LC 85 最大矩形 困难</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-d/">[codeforces] CF Round 1116 Div.1 B / Div.2 D A Ribbon for Tomorrow →</a>
</nav>
