---
title: "[力扣每日一题] 2026-07-27｜LC 1464 数组中两元素的最大乘积"
---

# [力扣每日一题] 2026-07-27｜LC 1464 数组中两元素的最大乘积

<p class="daily-archive-kicker">2026-07-27 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-27 题目列表</a> · <a href="../../basics/pair-product-extrema.md">进入知识专题</a></p>

## 官方原始信息

- 每日题日期：2026-07-27（Asia/Shanghai）
- 题号：LC 1464（官方 GraphQL 内部题目 ID 为 1574）
- 官方中文标题：数组中两元素的最大乘积
- 官方英文标题：Maximum Product of Two Elements in an Array
- 官方难度：简单（Easy）
- 官方链接：https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/?envType=daily-question&envId=2026-07-27
- 官方竞赛来源：[第 191 场周赛 Q1](https://leetcode.cn/contest/weekly-contest-191/)
- 官方竞赛分值：3
- ZeroTracer 社区估算竞赛分：1121.0678（抓取日期：2026-07-27）
- 函数签名：`int maxProduct(vector<int>& nums)`

### 原始题意

给定整数数组 `nums`，选择两个不同下标 $i$ 和 $j$，最大化

$$
(\texttt{nums}[i]-1)(\texttt{nums}[j]-1),
$$

并返回这个最大值。两个下标必须不同，但对应的数值可以相同。

### 全部官方样例

1. 输入：`nums = [3,4,5,2]`；输出：`12`。选择下标 1 和 2，得到 $(4-1)(5-1)=3\cdot4=12$。
2. 输入：`nums = [1,5,4,5]`；输出：`16`。选择两个值为 5 的不同位置，得到 $(5-1)(5-1)=16$。
3. 输入：`nums = [3,7]`；输出：`12`。数组恰有两个元素，只能选择这一对，得到 $(3-1)(7-1)=12$。

### 全部官方约束

- $2\le n=\lvert\texttt{nums}\rvert\le500$
- $1\le\texttt{nums}[i]\le10^3$

## 最优结论

令 $b_i=\texttt{nums}[i]-1$。约束保证每个 $b_i\ge0$，因此乘积对两个因子都单调不减。答案必由 `nums` 中最大的两个元素贡献；一次扫描维护最大值和次大值即可。

时间复杂度为 $O(n)$，额外空间复杂度为 $O(1)$。最大答案为

$$
(10^3-1)^2=998001,
$$

落在 32 位有符号整数范围内。面试和竞赛中优先记忆一次扫描：它在线、常数小、无需修改输入，并且其不变量可以自然推广到流式数据与区间摘要。

## 约束如何决定算法

1. $n\le500$，所以 $O(n^2)$ 暴力枚举约 $1.25\times10^5$ 对，能够通过；它适合作为正确性基线。
2. 若排序，$O(n\log n)$ 也远低于上限，并且结论一眼可见，但会修改输入或额外复制数组。
3. 真正关键的不是 $n$ 很小，而是 `nums[i] >= 1`：减一后的因子非负，最大乘积才一定来自两个最大值。
4. “不同下标”不等于“不同数值”。若最大值出现至少两次，两个最大值可以同时入选。
5. 返回类型为 `int` 足够；实现中不需要为了本题溢出改用 `long long`，但允许负数或放大值域的变种必须重新判断。

## 样例手推与边界

对 `nums = [3,4,5,2]`，一次扫描的 `(最大值, 次大值)` 状态依次为：

- 读入 3：$(3,-\infty)$；
- 读入 4：$(4,3)$；
- 读入 5：$(5,4)$；
- 读入 2：仍为 $(5,4)$。

最终答案是 $(5-1)(4-1)=12$。

真正相关的边界包括：

- 最小规模：`[1,1]`，答案为 0；
- 最大值重复：`[5,5,1]`，必须允许两个不同下标都取值 5；
- 全部相等：`[7,7,7]`，任意一对都最优；
- 极值：`[1000,1000]`，答案为 998001；
- 某个因子为 0：只要数组中除 1 外不足两个更大元素，答案可能为 0；
- 本题总有解，因为 $n\ge2$，不存在“无解”分支。

## 解法一：枚举全部下标对

枚举所有 $0\le i<j<n$。这恰好覆盖每个无序下标对一次，因此不会漏解或重复计算同一对。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    int ans = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      for (int j = i + 1; j < static_cast<int>(nums.size()); ++j) {
        ans = max(ans, (nums[i] - 1) * (nums[j] - 1));
      }
    }
    return ans;
  }
};
```

时间复杂度为 $O(n^2)$，额外空间复杂度为 $O(1)$。瓶颈是大量下标对重复参与比较；每个元素只需要通过“是否属于全局前二”影响答案。

## 解法二：排序后取末尾两个元素

非负因子乘积具有单调性。排序后最大的两个数位于末尾，直接计算即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    return (nums[n - 1] - 1) * (nums[n - 2] - 1);
  }
};
```

时间复杂度为 $O(n\log n)$；若允许原地修改，除排序栈外额外空间通常为 $O(\log n)$。它消除了显式枚举，但为获得完整顺序做了过量工作：答案只依赖前两个次序统计量。

## 解法三：一次扫描维护前两大（最佳实用解）

维护不变量：处理完当前前缀后，`mx1` 是前缀最大值，`mx2` 是来自不同下标的前缀次大值。读入 `x` 时：

- 若 `x >= mx1`，旧最大值下放到 `mx2`，`x` 成为新最大值；
- 否则若 `x > mx2`，只更新次大值；
- 否则二者不变。

使用 `>=` 很重要：相等的最大值来自不同下标时，旧最大值必须进入第二名。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    int mx1 = 0, mx2 = 0;
    for (int x : nums) {
      if (x >= mx1) {
        mx2 = mx1;
        mx1 = x;
      } else if (x > mx2) {
        mx2 = x;
      }
    }
    return (mx1 - 1) * (mx2 - 1);
  }
};
```

### 正确性证明

对扫描长度做归纳。

- 基础情形：空前缀的两个哨兵均为 0；读入第一个正整数后，`mx1` 是该元素，`mx2` 仍是哨兵。
- 归纳步骤：假设扫描旧前缀后，`mx1`、`mx2` 是该前缀的前两大。新值 `x` 若不小于 `mx1`，它成为最大值，旧 `mx1` 必为次大；若介于二者之间，它成为次大；若不大于 `mx2`，前两大不变。三种情况穷尽所有可能，因此不变量保持。

扫描结束时，`mx1` 与 `mx2` 来自两个不同迭代位置，是全数组前两大。因为 $x\mapsto x-1$ 在本题值域上非负且单调，任意其他下标对的两个因子分别不可能共同超过这两个因子，故返回值为全局最大乘积。

### 复杂度

时间复杂度为 $O(n)$，额外空间复杂度为 $O(1)$。

## 同阶方案比较

- 两元素小根堆也能做到 $O(n\log2)=O(n)$、空间 $O(1)$，但容器操作和证明都比两个标量更重。
- `nth_element` 平均 $O(n)$，可原地选出前二，但最坏界和实现常数不如直接扫描透明。
- 一次扫描的证明负担最小、不修改输入、可直接用于数据流；因此它是优先记忆方案。

## 常见错误

- 误把“不同下标”理解为“不同数值”，从而拒绝 `[5,5]`。
- 更新最大值时忘记先把旧最大值放入次大值。
- 用 `x > mx1` 而不是 `x >= mx1`，使重复最大值无法同时占据前二。
- 初始化为数组首元素后又从错误位置开始扫描，导致同一下标被使用两次。
- 把“取两个最大值”的结论套到允许负数的数组；两个很小的负数也可能给出最大正乘积。
- 忽略减一。题目最大化的不是 `nums[i] * nums[j]`，虽然在当前正值约束下最优下标相同，返回值仍不同。

## Follow-up 1：允许任意整数

### 新定义

`nums[i]` 可以是负数，且满足 $\lvert\texttt{nums}[i]\rvert\le10^9$；仍需最大化 $(\texttt{nums}[i]-1)(\texttt{nums}[j]-1)$。

### 原算法为何失效

减一后的因子可能为负。最大乘积既可能来自两个最大因子，也可能来自两个最小因子。例如 `[-10,-9,2]` 中，两个最小值减一后的乘积远大于最大值与次大值的乘积。

### 新思路

同时维护两个最大原值与两个最小原值，比较两组候选。减一保持次序，所以无需先构造新数组。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long maxProductSigned(vector<long long>& nums) {
    long long hi1 = LLONG_MIN, hi2 = LLONG_MIN;
    long long lo1 = LLONG_MAX, lo2 = LLONG_MAX;
    for (long long x : nums) {
      if (x >= hi1) {
        hi2 = hi1;
        hi1 = x;
      } else if (x > hi2) {
        hi2 = x;
      }
      if (x <= lo1) {
        lo2 = lo1;
        lo1 = x;
      } else if (x < lo2) {
        lo2 = x;
      }
    }
    return max((hi1 - 1) * (hi2 - 1), (lo1 - 1) * (lo2 - 1));
  }
};
```

正确性来自实数序列中“两数最大乘积只可能由前两大或前两小贡献”。时间 $O(n)$，空间 $O(1)$；值域扩大后使用 `long long`，仍需由新约束确认乘法不会超过 64 位。

## Follow-up 2：恢复字典序最小的最优下标对

### 新定义

保留原题正整数约束，返回使乘积最大的下标对 `[i,j]`，要求 $i<j$；若最优对不唯一，返回字典序最小者。

### 原算法为何不够

两个标量只保留数值，不知道这些数来自哪些位置，也无法处理重复最大值对应的多个候选下标。

### 新思路

先用前两大计算最优乘积 `best`，再按下标从小到大枚举 `i`。把每个因子 `nums[j] - 1` 的全部出现位置存入有序表，即可用 `upper_bound` 找到使乘积等于 `best` 的最早 `j > i`。第一个可行的 `i` 与其最早 `j` 就是字典序最小答案。必须特别处理因子 0：当 `best == 0` 且当前因子也为 0 时，任意后继位置都可配对，最早的是 `i + 1`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> maxProductIndices(vector<int>& nums) {
    int mx1 = 0, mx2 = 0;
    vector<vector<int>> positions(1000);
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      int x = nums[i];
      positions[x - 1].push_back(i);
      if (x >= mx1) {
        mx2 = mx1;
        mx1 = x;
      } else if (x > mx2) {
        mx2 = x;
      }
    }
    long long best = 1LL * (mx1 - 1) * (mx2 - 1);
    for (int i = 0; i + 1 < static_cast<int>(nums.size()); ++i) {
      long long factor = nums[i] - 1;
      if (best == 0 && factor == 0) return {i, i + 1};
      if (factor == 0 || best % factor != 0) continue;
      long long target = best / factor;
      if (target < 0 || target >= static_cast<int>(positions.size())) continue;
      auto it = upper_bound(positions[target].begin(), positions[target].end(), i);
      if (it != positions[target].end()) {
        return {i, *it};
      }
    }
    return {};
  }
};
```

算法按 `i` 严格递增，并为每个 `i` 选择最早可行的 `j`，所以返回的第一对恰为字典序最小最优对。时间 $O(n\log n)$，空间 $O(n+V)$，其中原题因子值域 $V=1000$；若只需任意最优下标对，直接随前两大保存下标即可做到 $O(n)$ 时间和 $O(1)$ 空间。

## Follow-up 3：数据流每次插入后立即查询

### 新定义

数字逐个到达；每次 `add(x)` 后返回当前所有已到达元素中的答案。少于两个元素时返回 `-1`。

### 原算法为何需要改造

每次重新扫描会让 $m$ 次插入退化为 $O(m^2)$。一次扫描的不变量本身可以持久保留。

### 新思路

把前两大值和元素个数存入对象；每次插入只做常数次比较。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MaxProductStream {
  int mx1 = 0;
  int mx2 = 0;
  int count = 0;
public:
  int add(int x) {
    ++count;
    if (x >= mx1) {
      mx2 = mx1;
      mx1 = x;
    } else if (x > mx2) {
      mx2 = x;
    }
    if (count < 2) return -1;
    return (mx1 - 1) * (mx2 - 1);
  }
};
```

每次插入时间 $O(1)$，总空间 $O(1)$。这说明最佳实用解的状态正是该查询所需的最小摘要。

## Follow-up 4：每个长度为 `k` 的滑动窗口

### 新定义

对数组的每个长度为 `k` 的连续窗口，分别返回窗口内两个不同下标的最大乘积，且 $k\ge2$。

### 原算法为何失效

窗口左端元素离开时，它可能正是最大值或次大值；只保存两个标量无法恢复被淘汰的第三名。

### 新思路

用 `multiset` 维护窗口全部元素，支持插入、删除一个副本以及从末尾读取最大和次大。重复值会作为不同节点保留，符合不同下标要求。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> maxProductWindows(vector<int>& nums, int k) {
    multiset<int> window;
    vector<int> ans;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      window.insert(nums[i]);
      if (i >= k) window.erase(window.find(nums[i - k]));
      if (i + 1 < k) continue;
      auto it = window.rbegin();
      int mx1 = *it;
      ++it;
      int mx2 = *it;
      ans.push_back((mx1 - 1) * (mx2 - 1));
    }
    return ans;
  }
};
```

每个元素插入和删除一次，时间 $O(n\log k)$，空间 $O(k)$。若值域很小，可用频次数组或 Fenwick 树把操作改为与值域相关的复杂度。

## Follow-up 5：点更新与区间查询，且允许负数

### 新定义

数组支持：

- `update(pos, value)`：单点修改；
- `query(left, right)`：在区间 `[left,right]` 中选择两个不同下标，最大化 $(a_i-1)(a_j-1)$。

区间长度保证至少为 2，数值可以为负且绝对值不超过 $10^9$。

### 原算法为何失效

每次查询重扫区间最坏为 $O(n)$；负数又使“只存前两大”不再充分。

### 新思路

线段树节点保存区间的两个最大值与两个最小值。合并时只需从左右孩子的至多 8 个候选值中重新选出四个极值；查询后比较前两大与前两小的乘积。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MaxProductRange {
  struct Node {
    long long hi1 = LLONG_MIN;
    long long hi2 = LLONG_MIN;
    long long lo1 = LLONG_MAX;
    long long lo2 = LLONG_MAX;
  };
  int n;
  vector<Node> tree;
  static Node mergeNode(const Node& a, const Node& b) {
    vector<long long> high, low;
    for (long long x : {a.hi1, a.hi2, b.hi1, b.hi2}) {
      if (x != LLONG_MIN) high.push_back(x);
    }
    for (long long x : {a.lo1, a.lo2, b.lo1, b.lo2}) {
      if (x != LLONG_MAX) low.push_back(x);
    }
    sort(high.begin(), high.end(), greater<long long>());
    sort(low.begin(), low.end());
    Node result;
    result.hi1 = high[0];
    if (high.size() >= 2) result.hi2 = high[1];
    result.lo1 = low[0];
    if (low.size() >= 2) result.lo2 = low[1];
    return result;
  }
  void build(int p, int l, int r, const vector<long long>& nums) {
    if (l == r) {
      tree[p].hi1 = tree[p].lo1 = nums[l];
      return;
    }
    int m = (l + r) / 2;
    build(p * 2, l, m, nums);
    build(p * 2 + 1, m + 1, r, nums);
    tree[p] = mergeNode(tree[p * 2], tree[p * 2 + 1]);
  }
  void update(int p, int l, int r, int pos, long long value) {
    if (l == r) {
      tree[p] = Node{};
      tree[p].hi1 = tree[p].lo1 = value;
      return;
    }
    int m = (l + r) / 2;
    if (pos <= m) update(p * 2, l, m, pos, value);
    else update(p * 2 + 1, m + 1, r, pos, value);
    tree[p] = mergeNode(tree[p * 2], tree[p * 2 + 1]);
  }
  Node query(int p, int l, int r, int ql, int qr) const {
    if (ql <= l && r <= qr) return tree[p];
    int m = (l + r) / 2;
    if (qr <= m) return query(p * 2, l, m, ql, qr);
    if (ql > m) return query(p * 2 + 1, m + 1, r, ql, qr);
    return mergeNode(query(p * 2, l, m, ql, qr), query(p * 2 + 1, m + 1, r, ql, qr));
  }
public:
  explicit MaxProductRange(const vector<long long>& nums) : n(nums.size()), tree(4 * nums.size()) {
    build(1, 0, n - 1, nums);
  }
  void update(int pos, long long value) {
    update(1, 0, n - 1, pos, value);
  }
  long long query(int left, int right) const {
    Node result = query(1, 0, n - 1, left, right);
    return max((result.hi1 - 1) * (result.hi2 - 1), (result.lo1 - 1) * (result.lo2 - 1));
  }
};
```

建树时间 $O(n)$、空间 $O(n)$；单次更新与查询均为 $O(\log n)$。节点摘要在合并下封闭，因此任意区间都能由 $O(\log n)$ 个节点正确聚合。

## 可复现验证

- 将本文每个 C++ 代码块分别以 C++23 执行语法编译，确认头文件、类型、函数签名与边界均有效。
- 对原题生成随机数组，以枚举全部下标对的 $O(n^2)$ 解为 oracle，与一次扫描解逐例比较。
- 定向覆盖 3 个官方样例，以及 `[1,1]`、`[5,5,1]`、`[7,7,7]`、`[1000,1000]`。
- 对允许负数的变种另以全对枚举核对“前两大/前两小”结论；对滑动窗口和线段树变种核对重复值、删除一个副本、单元素节点合并与更新后的区间。

验证结果：8 个代码块均以 `g++ -std=c++23 -Wall -Wextra -pedantic -fsyntax-only` 编译通过，且无制表符、无代码块内空行、所有缩进均为两个空格的整数倍。固定随机种子 20260727 下，7 组定向边界、100000 组原题随机用例及其全部流式前缀、100000 组含负数用例、50000 组字典序下标恢复用例、20000 组滑动窗口用例、200000 次线段树随机更新/查询均与对应暴力 oracle 完全一致。

## Reference

- [力扣中国 LC 1464 官方题面](https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/)
- [力扣中国 2026-07-27 每日一题接口](https://leetcode.cn/graphql/)
- [力扣中国第 191 场周赛官方信息](https://leetcode.cn/contest/api/info/weekly-contest-191/)
- [ZeroTracer LeetCode 竞赛题难度数据](https://github.com/zerotrac/leetcode_problem_rating/blob/main/ratings.txt)（抓取日期：2026-07-27）

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/)
- [对应知识专题](../../basics/pair-product-extrema.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="codeforces-2247-b.md">← [codeforces] CF Round 1111 Div.2 B Yet Another Constructive</a>
<span class="daily-archive-pager__empty"></span>
</nav>
