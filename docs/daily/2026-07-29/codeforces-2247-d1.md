---
title: "[codeforces] CF Round 1111 Div.2 D1 XOR Sorting (Easy Version)"
---

# [codeforces] CF Round 1111 Div.2 D1 XOR Sorting (Easy Version)

<p class="daily-archive-kicker">2026-07-29 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../basics/index.md">进入知识专题</a></p>

## 官方原始信息

- 来源：Codeforces
- 比赛：Codeforces Round 1111 (Div. 2)
- 竞赛 ID：2247
- 题号与标题：Div.2 D1 - XOR Sorting (Easy Version)
- 官方分值：1500
- 官方 Rating：未标注
- 官方标签：bitmasks、greedy
- 时间限制：2 秒
- 内存限制：256 MB
- 官方链接：<https://codeforces.com/contest/2247/problem/D1>

### 忠实完整题意

完整官方英文原文请从上方链接查看。这里给出不遗漏语义的教学重述：

对正整数数组 `b`，若允许任意多次交换下标 `i<j` 的元素，但每次必须满足 `(i XOR j) <= k`，并最终能把数组排成非降序，则称 `b` 可被 `k` 排序。定义 `f(b)` 为满足条件的最小非负整数 `k`。

给定数组 `a` 以及 `q` 次持久化单点修改。需要输出初始数组以及每次修改后数组的 `f(a)`。本题是 Easy Version，保证 `q=0`，因此每个测试用例只需处理初始数组。下标从 0 开始。

### 输入与输出

- 第一行是测试用例数 `t`。
- 每个测试用例先给 `n q`，本题中 `q=0`。
- 下一行给 `n` 个正整数。
- 输出每个测试用例的一个答案。

### 全部约束

- $1\le t\le 10^4$。
- $1\le n\le 10^6$，且本题 $q=0$。
- $1\le a_i\le 10^9$。
- 所有测试用例的 $n$ 之和不超过 $10^6$。
- 所有测试用例的 $q$ 之和不超过 $10^6$，在本题中为 0。

### 官方样例

```text
输入
3
3 0
2 3 4
2 0
1000000000 999999999
6 0
2 5 3 4 1 6
输出
0
1
4
```

- `[2,3,4]` 已有序，答案为 0。
- 两个下标只能通过 `0 XOR 1=1` 相连，答案为 1。
- `[2,5,3,4,1,6]` 的关键跨区间逆序需要把下标 0 与 4 放进同一连通块，答案为 4。

## 最优结论

答案一定是 0 或 2 的幂。把下标补到不小于 `n` 的最小 2 的幂，并建立按下标二进制前缀切分的线段树。对节点区间 `[l,r)`：

- 子树内部需要的答案由左右孩子给出。
- 若左半最大值大于右半最小值，存在跨过中点的逆序；要消除它，必须把左右半合并到同一个可交换块，因此至少需要 `k=(r-l)/2`。

节点答案为三者最大值。一次自底向上合并即可，时间 $O(n)$，空间 $O(n)$。

## 约束与观察

若 $2^b\le k<2^{b+1}$，允许的交换图包含所有 XOR 为 $1,2,\ldots,2^b$ 的基边。这些边使每个对齐的长度 $2^{b+1}$ 下标块内部连通，但不同块之间不连通。继续增大 `k`、但尚未到下一个 2 的幂，不会合并新的连通块。因此最小答案只可能是 0 或 2 的幂。

一个对齐区间能在自身内部任意重排后整体有序，当且仅当：

1. 左半可以在自己的限制下有序；
2. 右半可以在自己的限制下有序；
3. 左半所有值不大于右半所有值，即 `max(left) <= min(right)`。

这正好是线段树的递归合并不变量。

## 解法递进

### 解法一：枚举 `k` 并显式建交换图

对小规模数据，可以枚举 `k`，把所有满足 `(i XOR j) <= k` 的边加入并查集，再比较每个连通块在原数组与排序后数组中的多重集合。覆盖性直接，但复杂度高达 $O(n^4\log n)$ 量级，只适合作为 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent;
  explicit DSU(int n) : parent(n) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
  }
  void unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a != b) {
      parent[a] = b;
    }
  }
};
bool feasible(const vector<int>& a, int k) {
  int n = static_cast<int>(a.size());
  DSU dsu(n);
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if ((i ^ j) <= k) {
        dsu.unite(i, j);
      }
    }
  }
  vector<int> sorted = a;
  sort(sorted.begin(), sorted.end());
  map<int, multiset<int>> have;
  map<int, multiset<int>> need;
  for (int i = 0; i < n; ++i) {
    have[dsu.find(i)].insert(a[i]);
    need[dsu.find(i)].insert(sorted[i]);
  }
  return have == need;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& value : a) {
      cin >> value;
    }
    int answer = 0;
    while (!feasible(a, answer)) {
      ++answer;
    }
    cout << answer << '\n';
  }
  return 0;
}
```

### 解法二：枚举块大小

只枚举 `k=1,2,4,...`。对于每个候选，把每个长度 `2k` 的对齐块分别排序，检查拼接后是否为全局有序。它把候选数降为 $O(\log n)$，但反复排序使总复杂度达到 $O(n\log^2 n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool works(const vector<int>& a, int k) {
  vector<int> candidate = a;
  int block = 2 * k;
  for (int left = 0; left < static_cast<int>(a.size()); left += block) {
    int right = min(left + block, static_cast<int>(a.size()));
    sort(candidate.begin() + left, candidate.begin() + right);
  }
  return is_sorted(candidate.begin(), candidate.end());
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& value : a) {
      cin >> value;
    }
    if (is_sorted(a.begin(), a.end())) {
      cout << 0 << '\n';
      continue;
    }
    int answer = 1;
    while (!works(a, answer)) {
      answer <<= 1;
    }
    cout << answer << '\n';
  }
  return 0;
}
```

### 解法三：线段树式分治

每个节点只保存区间最小值、最大值、是否为空和该区间内部所需的最大 2 的幂。所有合并均为 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int minimum = INT_MAX;
  int maximum = INT_MIN;
  int answer = 0;
  bool empty = true;
};
Node mergeNode(const Node& left, const Node& right, int halfSize) {
  if (left.empty) {
    return right;
  }
  if (right.empty) {
    return left;
  }
  Node result;
  result.empty = false;
  result.minimum = min(left.minimum, right.minimum);
  result.maximum = max(left.maximum, right.maximum);
  result.answer = max(left.answer, right.answer);
  if (left.maximum > right.minimum) {
    result.answer = max(result.answer, halfSize);
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, q;
    cin >> n >> q;
    int size = 1;
    while (size < n) {
      size <<= 1;
    }
    vector<Node> tree(2 * size);
    for (int i = 0; i < n; ++i) {
      int value;
      cin >> value;
      tree[size + i] = Node{value, value, 0, false};
    }
    for (int node = size - 1; node >= 1; --node) {
      int level = 31 - __builtin_clz(node);
      int halfSize = (size >> level) / 2;
      tree[node] = mergeNode(tree[2 * node], tree[2 * node + 1], halfSize);
    }
    cout << tree[1].answer << '\n';
  }
  return 0;
}
```

上面的层宽计算可读性一般。竞赛中更稳妥的写法是递归建树，直接从区间长度得到半区大小：

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int minimum = INT_MAX;
  int maximum = INT_MIN;
  int answer = 0;
  bool empty = true;
};
Node solve(const vector<int>& a, int left, int right) {
  if (right - left == 1) {
    if (left >= static_cast<int>(a.size())) {
      return {};
    }
    return Node{a[left], a[left], 0, false};
  }
  int middle = (left + right) / 2;
  Node first = solve(a, left, middle);
  Node second = solve(a, middle, right);
  if (first.empty) {
    return second;
  }
  if (second.empty) {
    return first;
  }
  Node result;
  result.empty = false;
  result.minimum = min(first.minimum, second.minimum);
  result.maximum = max(first.maximum, second.maximum);
  result.answer = max(first.answer, second.answer);
  if (first.maximum > second.minimum) {
    result.answer = max(result.answer, (right - left) / 2);
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& value : a) {
      cin >> value;
    }
    int size = 1;
    while (size < n) {
      size <<= 1;
    }
    cout << solve(a, 0, size).answer << '\n';
  }
  return 0;
}
```

## 正确性证明

引理 1：当 $2^b\le k<2^{b+1}$ 时，交换图的连通块恰为对齐的长度 $2^{b+1}$ 下标块与 `[0,n)` 的交集。

证明：XOR 不超过 $2^b$ 的边不能改变更高位前缀，所以不能跨块；XOR 为 $1,2,\ldots,2^b$ 的基边可以逐位改变低 $b+1$ 位，因此块内连通。

引理 2：对一个对齐区间，若左右半各自可有序，则整个区间无需合并也能有序，当且仅当左半最大值不大于右半最小值。

证明：左右半内部可任意重排。若最大值条件成立，分别排序后拼接即有序；若不成立，存在一个左侧值大于右侧值，二者不能跨半交换，无法消除该逆序。

定理：递归算法返回最小可行 `k`。

证明：左右子树答案分别是清除各自内部逆序的最小阈值。若跨中点存在逆序，由引理 2 必须合并左右半，而引理 1 表明最小新增阈值正是半区长度；若不存在跨中点逆序，无需新增阈值。取三者最大值既必要又充分。

## 样例状态演化

数组 `[2,5,3,4,1,6]` 补到长度 8：

- 长度 2 的节点 `[0,2)` 中 `2<=5`，无需阈值 1。
- 长度 4 的节点 `[0,4)` 中左半最大值 5 大于右半最小值 3，需要阈值 2。
- 根节点 `[0,8)` 中左半最大值 5 大于右半有效部分最小值 1，需要阈值 4。

最终答案为 `max(2,4)=4`。

## 复杂度与易错点

- 时间复杂度：$O(n)$。
- 空间复杂度：$O(n)$；递归深度 $O(\log n)$。
- 必须把下标补到 2 的幂，空叶不能参与最大值/最小值比较。
- 比较的是左半最大值与右半最小值，不是相邻元素。
- 答案是半区长度，不是节点区间总长度。
- 值可重复，严格逆序条件是 `left.maximum > right.minimum`。

## 验证说明

对 $n\le 9$ 的随机数组，最优解与“枚举 `k` + 并查集 + 多重集合”的独立 oracle 对拍；覆盖已排序、逆序、全相等、重复值和非 2 的幂长度。

## Follow-up 与变种

### 变种一：Hard Version 的持久化单点更新

这正是官方 D2。线段树节点不变量完全不变；每次只更新一条根到叶路径，重新合并即可。预处理 $O(n)$，每次修改 $O(\log n)$，每次答案为根节点的 `answer`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int minimum = INT_MAX;
  int maximum = INT_MIN;
  int answer = 0;
  bool empty = true;
};
class SegmentTree {
public:
  explicit SegmentTree(const vector<int>& values) {
    size_ = 1;
    while (size_ < static_cast<int>(values.size())) {
      size_ <<= 1;
    }
    tree_.assign(2 * size_, {});
    for (int i = 0; i < static_cast<int>(values.size()); ++i) {
      tree_[size_ + i] = Node{values[i], values[i], 0, false};
    }
    build(1, 0, size_);
  }
  void update(int index, int value) {
    update(1, 0, size_, index, value);
  }
  int answer() const {
    return tree_[1].answer;
  }
private:
  int size_ = 0;
  vector<Node> tree_;
  Node merge(const Node& left, const Node& right, int halfSize) {
    if (left.empty) {
      return right;
    }
    if (right.empty) {
      return left;
    }
    Node result;
    result.empty = false;
    result.minimum = min(left.minimum, right.minimum);
    result.maximum = max(left.maximum, right.maximum);
    result.answer = max(left.answer, right.answer);
    if (left.maximum > right.minimum) {
      result.answer = max(result.answer, halfSize);
    }
    return result;
  }
  void build(int node, int left, int right) {
    if (right - left == 1) {
      return;
    }
    int middle = (left + right) / 2;
    build(2 * node, left, middle);
    build(2 * node + 1, middle, right);
    tree_[node] = merge(tree_[2 * node], tree_[2 * node + 1], (right - left) / 2);
  }
  void update(int node, int left, int right, int index, int value) {
    if (right - left == 1) {
      tree_[node] = Node{value, value, 0, false};
      return;
    }
    int middle = (left + right) / 2;
    if (index < middle) {
      update(2 * node, left, middle, index, value);
    } else {
      update(2 * node + 1, middle, right, index, value);
    }
    tree_[node] = merge(tree_[2 * node], tree_[2 * node + 1], (right - left) / 2);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& value : a) {
      cin >> value;
    }
    SegmentTree tree(a);
    cout << tree.answer();
    while (q--) {
      int index, value;
      cin >> index >> value;
      tree.update(index, value);
      cout << ' ' << tree.answer();
    }
    cout << '\n';
  }
  return 0;
}
```

### 变种二：交换条件改为 `(i XOR j) < k`

若数组已有序，答案仍为 0。否则原问题所需的最大基边为 $2^b$，严格不等式要求 `k` 至少为 $2^b+1$`。先求原答案再加 1 即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int mn;
  int mx;
  int need;
  bool empty;
};
Node solve(const vector<int>& a, int left, int right) {
  if (right - left == 1) {
    if (left >= static_cast<int>(a.size())) {
      return {INT_MAX, INT_MIN, 0, true};
    }
    return {a[left], a[left], 0, false};
  }
  int middle = (left + right) / 2;
  Node x = solve(a, left, middle);
  Node y = solve(a, middle, right);
  if (x.empty) {
    return y;
  }
  if (y.empty) {
    return x;
  }
  return {min(x.mn, y.mn), max(x.mx, y.mx),
      max({x.need, y.need, x.mx > y.mn ? (right - left) / 2 : 0}), false};
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  int need = solve(a, 0, size).need;
  cout << (need == 0 ? 0 : need + 1) << '\n';
  return 0;
}
```

### 变种三：给定 `k`，只判断能否排序

先用同一线段树不变量求出最小阈值，再比较 `need<=k`。预处理 $O(n)$，判定 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Summary {
  int mn;
  int mx;
  int need;
  bool empty;
};
Summary dfs(const vector<int>& a, int left, int right) {
  if (right - left == 1) {
    if (left == static_cast<int>(a.size())) {
      return {INT_MAX, INT_MIN, 0, true};
    }
    return {a[left], a[left], 0, false};
  }
  int middle = (left + right) / 2;
  Summary x = dfs(a, left, middle);
  Summary y = dfs(a, middle, right);
  if (x.empty) {
    return y;
  }
  if (y.empty) {
    return x;
  }
  int cross = x.mx > y.mn ? (right - left) / 2 : 0;
  return {min(x.mn, y.mn), max(x.mx, y.mx), max({x.need, y.need, cross}), false};
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int size = 1;
  while (size < n) {
    size <<= 1;
  }
  cout << (dfs(a, 0, size).need <= k ? "YES\n" : "NO\n");
  return 0;
}
```

### 变种四：允许交换图由任意边集给出

XOR 的分块结构消失，不能再用线段树。先用并查集求连通块；一个数组可排序当且仅当每个连通块中的原值多重集合等于排序目标在这些下标上的多重集合。复杂度 $O((n+m)\alpha(n)+n\log n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
  vector<int> parent;
  vector<int> size;
  explicit DSU(int n) : parent(n), size(n, 1) {
    iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
  }
  void unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
      return;
    }
    if (size[a] < size[b]) {
      swap(a, b);
    }
    parent[b] = a;
    size[a] += size[b];
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  DSU dsu(n);
  while (m--) {
    int u, v;
    cin >> u >> v;
    dsu.unite(u, v);
  }
  vector<int> target = a;
  sort(target.begin(), target.end());
  map<int, vector<int>> have;
  map<int, vector<int>> need;
  for (int i = 0; i < n; ++i) {
    have[dsu.find(i)].push_back(a[i]);
    need[dsu.find(i)].push_back(target[i]);
  }
  for (auto& [root, values] : have) {
    sort(values.begin(), values.end());
    sort(need[root].begin(), need[root].end());
    if (values != need[root]) {
      cout << "NO\n";
      return 0;
    }
  }
  cout << "YES\n";
  return 0;
}
```

## Reference

- [Codeforces 官方题面](https://codeforces.com/contest/2247/problem/D1)
- [Codeforces Round 1111 官方比赛页](https://codeforces.com/contest/2247)
- [Codeforces 官方题解](https://codeforces.com/blog/entry/155337)

### 延伸阅读

- [官方题目](https://codeforces.com/contest/2247/problem/D1)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-weekly-511-q4-lc3999.md">← [力扣竞赛] 第 511 场周赛 Q4 LC 3999 字符串变换后的最少分组数 困难</a>
<a class="daily-archive-pager__next" href="leetcode-daily-2026-07-29-lc3518.md">[力扣每日一题] 2026-07-29｜LC 3518 最小回文排列 II →</a>
</nav>
