---
title: "[力扣竞赛] 第 516 场周赛 Q2 LC 4031 找到所有数组中消失的数字 II 中等"
---

# [力扣竞赛] 第 516 场周赛 Q2 LC 4031 找到所有数组中消失的数字 II 中等

<p class="daily-archive-kicker">2026-08-27 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-27 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=1c9e12e245b23827c029fb1bf861050a7f51bb299e67052006918e6f744fbb9f -->
## 官方原始信息

- 来源：力扣第 516 场周赛 Q2
- 题号：LC 4031
- 官方中文标题：找到所有数组中消失的数字 II
- 官方难度：中等
- 官方比赛分值：4 分
- ZeroTracer 社区估算竞赛分：未知（公开数据于 2026-08-27 未收录该题）
- 官方链接：[4031. 找到所有数组中消失的数字 II](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/)
- 函数签名：`vector<vector<int>> findDisappearedNumbers(vector<int>& nums, int lower, int upper)`

### 原始题意

给定整数数组 `nums` 和闭区间 `[lower, upper]`。区间内没有在 `nums` 中出现的整数称为缺失整数。把所有缺失整数按数值连续性合并成尽可能长的闭区间，并按递增顺序返回这些区间；若没有缺失整数，返回空数组。

### 全部官方样例

样例 1：

```text
输入：nums = [3,9,7], lower = 1, upper = 12
输出：[[1,2],[4,6],[8,8],[10,12]]
解释：缺失整数为 1、2、4、5、6、8、10、11、12，合并后得到四段连续区间。
```

样例 2：

```text
输入：nums = [1,1], lower = 5, upper = 7
输出：[[5,7]]
解释：5、6、7 都没有出现，因此合并为一个区间。
```

样例 3：

```text
输入：nums = [2,3,5], lower = 2, upper = 3
输出：[]
解释：区间中的 2 和 3 都已出现，没有缺失整数。
```

### 全部约束

- $1\le |\texttt{nums}|\le 10^5$
- $1\le \texttt{nums}[i]\le 10^5$
- $1\le \texttt{lower}\le \texttt{upper}\le 10^5$

## 最优结论与推荐记忆方案

令区间长度为 $R=\texttt{upper}-\texttt{lower}+1$。用长度为 $R$ 的布尔数组记录每个区间内整数是否出现，再从左到右扫描连续的 `false` 段；每一段恰好对应一个答案区间。

时间复杂度为 $O(n+R)$，额外空间复杂度为 $O(R)$。本题 $R\le 10^5$，位图做法确定性强、不修改输入，也直接输出有序的极大缺失区间，是最佳实用解。

推荐记住：**有界稠密值域上的“缺失区间”先转成存在性位图，再对零段做游程编码**。若值域扩大到 $10^9$ 以上，再切换为排序后找相邻间隙。

## 约束推导、整数安全与边界

设 $n=|\texttt{nums}|$，$R=\texttt{upper}-\texttt{lower}+1$：

- 对每个候选整数重新扫描数组需要 $O(nR)$，上界约为 $10^{10}$，不可接受。
- 哈希集合能把成员判断降到期望 $O(1)$，总时间为期望 $O(n+R)$，但有哈希常数与最坏复杂度。
- 因为闭区间端点都不超过 $10^5$，直接位图只需 $O(10^5)$ 空间，复杂度确定。
- 数组元素可能小于 `lower` 或大于 `upper`，它们不影响答案，标记前必须过滤。
- `nums` 可能包含重复值；存在性只需置位一次。

需要覆盖的边界：

- `lower == upper`：答案要么为空，要么是 `[[lower, lower]]`。
- 整个区间都缺失：返回一个完整区间。
- 整个区间都出现：返回空数组。
- 缺失段贴着左端点或右端点：扫描结束时必须正确收尾。
- 单点缺失段必须保留为 `[x,x]`，不能省略端点。

所有数值和下标均不超过 $10^5$，`int` 足够；`upper - lower + 1` 也不会溢出。

## 官方样例手推

样例 1 的目标区间是 $[1,12]$。标记 `3`、`7`、`9` 后，存在性序列按数值为：

```text
值： 1 2 3 4 5 6 7 8 9 10 11 12
在： 0 0 1 0 0 0 1 0 1  0  0  0
```

四段极大零段分别是 $[1,2]$、$[4,6]$、$[8,8]$、$[10,12]$，与官方输出一致。

样例 2 中 `nums` 的两个 `1` 都落在查询区间之外，因此 $[5,7]$ 整段缺失。样例 3 中两个目标值都被标记，扫描不到零段。

## 解法一：逐值线性查找

枚举 `[lower, upper]` 中每个整数，并线性扫描 `nums` 判断是否出现；用 `start` 维护当前缺失段起点。它直接按定义检查全部候选，因此正确，但重复扫描同一数组。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> findDisappearedNumbers(vector<int>& nums, int lower, int upper) {
    vector<vector<int>> answer;
    int start = -1;
    for (int value = lower; value <= upper; ++value) {
      bool found = false;
      for (int x : nums) {
        if (x == value) {
          found = true;
          break;
        }
      }
      if (!found && start == -1)
        start = value;
      if (found && start != -1) {
        answer.push_back({start, value - 1});
        start = -1;
      }
    }
    if (start != -1)
      answer.push_back({start, upper});
    return answer;
  }
};
```

时间复杂度为 $O(nR)$，答案之外的额外空间复杂度为 $O(1)$。瓶颈是每个候选值都重复读取整个 `nums`。

## 解法二：哈希集合消除重复成员查询

把 `nums` 的值放入哈希集合后，每个候选值只做一次期望 $O(1)$ 的成员查询，再把连续缺失值合并。该方案已达到期望线性时间，但确定性和内存局部性不如位图。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> findDisappearedNumbers(vector<int>& nums, int lower, int upper) {
    unordered_set<int> present;
    present.reserve(nums.size() * 2 + 1);
    for (int x : nums) {
      if (lower <= x && x <= upper)
        present.insert(x);
    }
    vector<vector<int>> answer;
    int value = lower;
    while (value <= upper) {
      if (present.contains(value)) {
        ++value;
        continue;
      }
      int start = value;
      while (value <= upper && !present.contains(value))
        ++value;
      answer.push_back({start, value - 1});
    }
    return answer;
  }
};
```

期望时间复杂度为 $O(n+R)$，额外空间复杂度为 $O(n)$。

## 最佳实用解：区间位图与极大零段

### 算法

1. 建立长度为 $R$ 的 `present`；下标 $i$ 对应整数 `lower + i`。
2. 对每个 `nums` 元素，若它位于目标区间，就把对应位置设为 `true`。
3. 从左到右扫描：遇到 `true` 直接前进；遇到 `false` 时记下起点，并前进到下一处 `true` 或数组末尾。
4. 把刚扫描完的极大 `false` 段转换回数值闭区间并加入答案。

### 正确性证明

**引理 1**：`present[i]` 为真当且仅当整数 `lower + i` 在 `nums` 中出现。

**证明**：初始化时所有位置为假。算法只对位于目标区间的数组值 $x$ 设置唯一对应下标 $x-\texttt{lower}$；每个出现值都会被处理，区间外值不会误置位。证毕。

**引理 2**：扫描得到的每个 `false` 极大连续段恰好对应一个应返回的缺失区间。

**证明**：由引理 1，段内每个位置对应的整数都缺失；下标连续意味着整数连续。段两侧若存在位置必为 `true`，因此该段无法再扩展，正是一个极大缺失区间。证毕。

**引理 3**：每个缺失整数恰好被一个输出区间覆盖。

**证明**：每个缺失整数对应唯一 `false` 位置，而线性扫描把每个 `false` 位置纳入其唯一极大连续段，且扫描指针不会回退。证毕。

**定理**：算法按递增顺序返回全部且仅有的极大连续缺失区间。

**证明**：由引理 2，所有输出都合法且极大；由引理 3，没有缺失整数被遗漏或重复。扫描顺序与数值顺序一致，所以答案递增。证毕。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> findDisappearedNumbers(vector<int>& nums, int lower, int upper) {
    int range = upper - lower + 1;
    vector<char> present(range, false);
    for (int x : nums) {
      if (lower <= x && x <= upper)
        present[x - lower] = true;
    }
    vector<vector<int>> answer;
    int i = 0;
    while (i < range) {
      if (present[i]) {
        ++i;
        continue;
      }
      int start = i;
      while (i < range && !present[i])
        ++i;
      answer.push_back({lower + start, lower + i - 1});
    }
    return answer;
  }
};
```

## 解法四：排序后只找相邻间隙

排序适合值域很大、但数组相对稀疏的版本。本题中它是同样稳定的备选：过滤区间外值和重复值，用 `next` 表示尚未覆盖的最小整数；每遇到更大的出现值，就输出中间间隙。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> findDisappearedNumbers(vector<int>& nums, int lower, int upper) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> answer;
    int next = lower;
    for (int x : nums) {
      if (x < next)
        continue;
      if (x > upper)
        break;
      if (x > next)
        answer.push_back({next, x - 1});
      next = x + 1;
    }
    if (next <= upper)
      answer.push_back({next, upper});
    return answer;
  }
};
```

时间复杂度为 $O(n\log n)$；若排序原数组，除排序栈外额外空间为 $O(\log n)$。它会修改输入，且在本题稠密有界值域下没有位图直接。

## 同阶方案比较

位图和哈希集合都可写成 $O(n+R)$：位图具有确定性、连续内存和更小常数；哈希集合适合无法按值域开数组的场景。排序方案为 $O(n\log n)$，却只访问真正出现的值，适合 `upper - lower` 极大而 `n` 较小的版本。

面试与竞赛中，本题优先记忆位图扫描；同时把“值域扩大就改用排序找 gap”作为约束变化后的自然切换。

## 常见错误

- 把 `nums` 的所有值都映射到 `present`，没有过滤区间外元素，导致负下标或越界。
- 没有处理重复值，排序方案把同一个出现值错误地推进多次。
- 只输出缺失整数列表，没有合并成极大连续区间。
- 扫描到数组末尾时忘记提交最后一段。
- 把闭区间长度写成 `upper - lower`，漏掉一个端点。
- 单点缺失输出成一个数字，而不是题目要求的 `[x,x]`。

## 可复现验证

可把逐值线性查找作为 oracle：枚举小值域上的所有 `lower`、`upper` 和含重复值、区间外值的短数组，比较位图解与 oracle 的二维数组完全一致。定向覆盖三个官方样例、单点区间、全缺失、全出现、左右端缺失以及重复元素。对最大 $n=10^5$、$R=10^5$ 的随机输入检查运行时间与边界访问。

## Follow-up 与约束变种

### 变种一：端点扩大到 $10^{18}$

新定义：`nums`、`lower`、`upper` 都是 64 位整数，区间长度可能极大。位图和逐值扫描失效；排序区间内的不同出现值，只在相邻出现值之间输出缺口。输出规模本身至多为 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MissingRanges64 {
public:
  vector<array<long long, 2>> solve(vector<long long> nums, long long lower, long long upper) {
    sort(nums.begin(), nums.end());
    vector<array<long long, 2>> answer;
    long long next = lower;
    for (long long x : nums) {
      if (x < next)
        continue;
      if (x > upper)
        break;
      if (x > next)
        answer.push_back({next, x - 1});
      if (x == upper)
        return answer;
      next = x + 1;
    }
    if (next <= upper)
      answer.push_back({next, upper});
    return answer;
  }
};
```

时间复杂度为 $O(n\log n)$，额外空间复杂度取决于排序实现；代码用 `x == upper` 提前结束，避免在右端点上执行加一。

### 变种二：支持在线插入、删除与区间查询

新定义：动态维护一个多重集合，支持插入值、删除一次出现，以及查询任意 `[lower, upper]` 的缺失区间。静态位图不能适应任意大值域和删除；用频次哈希表维护重复次数，用有序集合维护当前出现的不同值。查询只遍历落在区间中的出现值。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicMissing {
  unordered_map<int, int> frequency;
  set<int> present;
public:
  void insert(int x) {
    if (++frequency[x] == 1)
      present.insert(x);
  }
  void erase(int x) {
    auto it = frequency.find(x);
    if (it == frequency.end())
      return;
    if (--it->second == 0) {
      frequency.erase(it);
      present.erase(x);
    }
  }
  vector<pair<int, int>> query(int lower, int upper) const {
    vector<pair<int, int>> answer;
    int next = lower;
    for (auto it = present.lower_bound(lower); it != present.end() && *it <= upper; ++it) {
      int x = *it;
      if (x > next)
        answer.push_back({next, x - 1});
      next = x + 1;
    }
    if (next <= upper)
      answer.push_back({next, upper});
    return answer;
  }
};
```

插入和删除的期望/最坏组合复杂度为 $O(1)+O(\log D)$；若查询区间内有 $k$ 个不同出现值，查询为 $O(\log D+k)$，其中 $D$ 是全局不同值数。

### 变种三：只求缺失整数总数

新定义：不需要区间列表，只返回 `[lower, upper]` 内缺失整数的数量。无需逐值扫描；统计区间内不同出现值的数量 $d$，答案是区间长度减去 $d$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MissingCount {
public:
  long long solve(const vector<int>& nums, int lower, int upper) {
    unordered_set<int> distinct;
    distinct.reserve(nums.size() * 2 + 1);
    for (int x : nums) {
      if (lower <= x && x <= upper)
        distinct.insert(x);
    }
    return static_cast<long long>(upper) - lower + 1 - distinct.size();
  }
};
```

期望时间复杂度为 $O(n)$，额外空间复杂度为 $O(d)$。输出目标改变后，原来的 $O(R)$ 扫描已没有必要。

### 变种四：输入本身是已出现区间的并集

新定义：不再给出单个出现值，而是给出若干已按起点排序、互不相交的闭区间；求它们在 `[lower, upper]` 内的补集。逐点位图可能浪费巨大空间，直接裁剪并合并区间边界即可。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class IntervalComplement {
public:
  vector<pair<long long, long long>> solve(
    const vector<pair<long long, long long>>& present, long long lower, long long upper) {
    vector<pair<long long, long long>> answer;
    long long next = lower;
    for (auto [left, right] : present) {
      if (right < next)
        continue;
      if (left > upper)
        break;
      if (left > next)
        answer.push_back({next, min(upper, left - 1)});
      if (right >= upper)
        return answer;
      next = max(next, right + 1);
    }
    if (next <= upper)
      answer.push_back({next, upper});
    return answer;
  }
};
```

若输入有 $k$ 个区间，时间复杂度为 $O(k)$，答案之外额外空间为 $O(1)$。若输入区间可能重叠或无序，应先排序并合并。

## 来源

- [力扣 4031 官方题目](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/)
- [力扣第 516 场周赛](https://leetcode.cn/contest/weekly-contest-516/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2253-c/">[codeforces] CF Educational Round 193 Div.2 C Sum of Distinct Values in a Matrix →</a>
</nav>
