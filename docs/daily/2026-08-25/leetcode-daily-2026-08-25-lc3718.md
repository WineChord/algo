---
title: "[力扣每日一题] 2026-08-25｜LC 3718 缺失的最小倍数"
---

# [力扣每日一题] 2026-08-25｜LC 3718 缺失的最小倍数

<p class="daily-archive-kicker">2026-08-25 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-25 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=6f93f98ab27d7ef98466831613b5d7bb1b1f78a62190456042f863308ba8050c -->
## 官方原始信息

- 日期：2026-08-25（Asia/Shanghai）力扣中国每日一题。
- 官方题目：[LC 3718 缺失的最小倍数](https://leetcode.cn/problems/smallest-missing-multiple-of-k/)。
- 原比赛：[力扣第 472 场周赛 Q1](https://leetcode.cn/contest/weekly-contest-472/problems/smallest-missing-multiple-of-k/)，官方竞赛分值 3 分。
- 官方难度：简单。
- [ZeroTracer 社区估算竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)：
  1227.634，抓取于 2026-08-25；这不是力扣官方难度或分值。
- 函数签名：`int missingMultiple(vector<int>& nums, int k)`。

### 原始题意

给定正整数数组 `nums` 和正整数 `k`，找出最小的、没有出现在 `nums` 中的 `k` 的正倍数。
也就是说，要返回最小的 $qk$，其中 $q$ 是正整数且 $qk\notin nums$。

### 全部官方样例

```text
示例 1
输入：nums = [8,2,3,4,6], k = 2
输出：10
解释：2、4、6、8 都在数组中，而下一个正倍数 10 不在数组中。

示例 2
输入：nums = [1,4,7,10,15], k = 5
输出：5
解释：5 是最小的正倍数，并且没有出现在数组中。
```

### 全部约束

- $1\le\lvert nums\rvert\le100$。
- $1\le nums_i\le100$。
- $1\le k\le100$。

## 最优结论摘要

设 $n=\lvert nums\rvert$。只需关心 `nums` 中能写成 $qk$ 的数，并标记其正整数商 $q$。
数组只有 $n$ 个元素，因此 $1,2,\ldots,n+1$ 这 $n+1$ 个商中至少有一个没有被标记；按商从小到大
找到第一个空位并乘以 $k$，就是答案。

布尔标记解法时间复杂度为 $O(n)$，空间复杂度为 $O(n)$；当前约束下答案不超过
$(n+1)k\le10100$，`int` 足够。面试中优先记忆这种“把值除以步长后转成缺失正整数”的确定性写法。

## 约束推导、溢出与边界

- 候选数不是任意正整数，而是严格递增的 $k,2k,3k,\ldots$；枚举对象应是倍数的商。
- 长度至多 100，即便逐个候选线性扫描数组也能通过，但会重复查找同一批元素。
- `nums` 不保证有序，也未承诺互异；用“出现过”而非出现次数即可。
- 不是 $k$ 倍数的元素不会影响答案，可以直接忽略。
- 若 $k$ 本身缺失，答案立即是 $k$；若前 $n$ 个倍数都出现，答案是 $(n+1)k$。
- 当前答案上界 10100，不会溢出 `int`。若把值域或询问数量放大，应先用 `long long` 做乘法。

## 官方样例手推

样例 1 中 $k=2$。数组里的正倍数对应商集合
$\{8/2,2/2,4/2,6/2\}=\{4,1,2,3\}$。商 1 到 4 都出现，商 5 首次缺失，故答案为
$5\times2=10$。元素 3 不是 2 的倍数，不参与标记。

样例 2 中 $k=5$。数组里只有 10 和 15 是 5 的倍数，对应商 2、3；商 1 没出现，所以无需继续
扫描，直接返回 $1\times5=5$。

最小规模 `nums = [1], k = 1` 中商 1 出现，商 2 缺失，答案为 2；而
`nums = [2], k = 1` 中商 1 缺失，答案为 1。

## 解法一：逐个倍数扫描数组

从 $k$ 开始依次考察 $k,2k,3k,\ldots$。对每个候选遍历 `nums` 判断是否出现；第一个未出现的
候选就是定义所求的最小值。由于前 $n+1$ 个候选中必有缺失者，循环一定终止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingMultiple(vector<int>& nums, int k) {
    int n = nums.size();
    for (int quotient = 1; quotient <= n + 1; ++quotient) {
      int candidate = quotient * k;
      bool found = false;
      for (int value : nums) {
        if (value == candidate) {
          found = true;
          break;
        }
      }
      if (!found)
        return candidate;
    }
    return -1;
  }
};
```

时间复杂度为 $O(n^2)$，空间复杂度为 $O(1)$。瓶颈是每换一个候选都重新扫描整个数组。

## 解法二：哈希集合消除重复查找

先把所有元素放入哈希集合，再按倍数递增询问。集合把每次“是否出现”的平均成本从 $O(n)$
降为 $O(1)$，总时间降为期望 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingMultiple(vector<int>& nums, int k) {
    unordered_set<int> present(nums.begin(), nums.end());
    for (int quotient = 1;; ++quotient) {
      int candidate = quotient * k;
      if (!present.contains(candidate))
        return candidate;
    }
  }
};
```

期望时间复杂度为 $O(n)$，空间复杂度为 $O(n)$。它很短，但复杂度依赖哈希表的平均性能，而且没有
显式利用“至多只需看前 $n+1$ 个商”的边界。

## 最佳实用解：标记倍数的商

建立长度 $n+2$ 的布尔数组。对每个数组元素 `value`，若 `value % k == 0`，令
$q=value/k$；只有 $1\le q\le n+1$ 时才标记。最后从 1 开始找最小未标记商。

### 正确性证明

对任意正整数 $q$，数 $qk$ 出现在 `nums` 中，当且仅当扫描时存在元素 `value = qk`，从而
`value % k == 0` 且 `value / k == q`，算法会把 `seen[q]` 标为真。因此 `seen[q]` 精确表示
第 $q$ 个正倍数是否出现。

数组只有 $n$ 个位置，至多包含 $n$ 个不同倍数；$1,2,\ldots,n+1$ 共 $n+1$ 个商，按鸽巢原理
至少一个未出现。算法按递增顺序返回第一个 `seen[q] == false` 的 $qk$，它已被证明没有出现在
数组中，而所有更小正倍数均已出现，所以返回值恰为最小缺失正倍数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingMultiple(vector<int>& nums, int k) {
    int n = nums.size();
    vector<char> seen(n + 2, false);
    for (int value : nums) {
      if (value % k != 0)
        continue;
      int quotient = value / k;
      if (quotient <= n + 1)
        seen[quotient] = true;
    }
    for (int quotient = 1; quotient <= n + 1; ++quotient) {
      if (!seen[quotient])
        return quotient * k;
    }
    return -1;
  }
};
```

时间复杂度为 $O(n)$，空间复杂度为 $O(n)$。与哈希方案同阶，但布尔数组没有哈希常数和最坏退化
顾虑，答案边界也写在代码中，因此更适合作为最佳实用解。

## 易错点

- 把题目误读成“最小缺失正整数”，忘记答案必须是 $k$ 的倍数。
- 从 0 倍开始枚举；题目要求正倍数，首个候选是 $k$。
- 先排序再只看相邻差，却没有过滤非倍数，导致商序列的缺口判断错误。
- 只开 `n + 1` 个标记位置却访问下标 `n + 1`。
- 无边界地写 `quotient * k`；当前约束安全，放大后要先转成 `long long`。
- 把重复元素计成多个不同倍数；本题只关心是否出现。

## 可复现验证

三种正文解法均以 C++23 编译。验证覆盖两个官方样例、$k$ 本身缺失、前 $n$ 个倍数全部出现、
重复元素、全部元素都不是 $k$ 的倍数以及当前最大值域。再对小数组穷举，并用逐候选线性扫描作
oracle，与布尔标记解逐例比较。

## Follow-up 与约束变种

### 变种一：返回前 $c$ 个缺失正倍数

**新定义**：给定正整数 $c$，按从小到大返回前 $c$ 个没有出现在数组中的 $k$ 的正倍数。

原算法只停止在第一个空位，不能直接给出后续答案。把所有数组元素放入集合，继续递增商，遇到
缺失者就加入结果，直到收集 $c$ 个。检查过的商不超过 $n+c$：前 $n+c$ 个候选中至多有 $n$
个出现，至少有 $c$ 个缺失。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> firstMissingMultiples(const vector<int>& nums, long long k, int count) {
  unordered_set<long long> present(nums.begin(), nums.end());
  vector<long long> answer;
  for (long long quotient = 1; static_cast<int>(answer.size()) < count; ++quotient) {
    long long candidate = quotient * k;
    if (!present.contains(candidate))
      answer.push_back(candidate);
  }
  return answer;
}
int main() {
  vector<int> nums = {2, 4, 8};
  for (long long value : firstMissingMultiples(nums, 2, 3))
    cout << value << ' ';
  cout << '\n';
}
```

期望时间复杂度为 $O(n+c)$，空间复杂度为 $O(n+c)$；乘法使用 `long long`。

### 变种二：在线插入、删除并随时询问

**新定义**：固定 $k$，维护一个允许重复值的动态多重集合；操作是插入一个值、删除一个已存在的
值，或询问当前最小缺失正倍数。已知答案的商始终不超过上界 $U$。

静态布尔数组无法正确处理删除：一个值可能仍有其他副本。维护每个商的出现次数，并用有序集合
保存当前缺失的商。计数从 0 变 1 时删除该商，从 1 变 0 时放回；查询取集合首元素。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MissingMultipleTracker {
  int k;
  int limit;
  vector<int> frequency;
  set<int> missing;
public:
  MissingMultipleTracker(int step, int maxQuotient)
      : k(step), limit(maxQuotient), frequency(maxQuotient + 1, 0) {
    for (int quotient = 1; quotient <= limit; ++quotient)
      missing.insert(quotient);
  }
  void insert(int value) {
    if (value % k != 0)
      return;
    int quotient = value / k;
    if (quotient < 1 || quotient > limit)
      return;
    if (frequency[quotient]++ == 0)
      missing.erase(quotient);
  }
  void erase(int value) {
    if (value % k != 0)
      return;
    int quotient = value / k;
    if (quotient < 1 || quotient > limit)
      return;
    if (--frequency[quotient] == 0)
      missing.insert(quotient);
  }
  long long query() const {
    return 1LL * *missing.begin() * k;
  }
};
int main() {
  MissingMultipleTracker tracker(2, 10);
  tracker.insert(2);
  tracker.insert(4);
  cout << tracker.query() << '\n';
  tracker.erase(2);
  cout << tracker.query() << '\n';
}
```

初始化为 $O(U)$；每次有效更新为 $O(\log U)$，查询为 $O(1)$，空间为 $O(U)$。调用方必须保证
删除的副本真实存在，并保证缺失集合非空。

### 变种三：同一个数组回答多个不同的 $k$

**新定义**：数组不变，给出多个正整数 `ks`，分别返回每个步长的最小缺失正倍数。

单个 $k$ 的商标记不能在不同步长间复用。先把数组值放入一个集合；对每个 $k$ 独立扫描
$k,2k,\ldots,(n+1)k$，第一次集合未命中即为答案。若询问很多且值域较小，可进一步按值域预处理
每个步长的答案；在一般约束下，逐询问扫描更直接。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> missingForSteps(const vector<int>& nums, const vector<int>& steps) {
  unordered_set<long long> present(nums.begin(), nums.end());
  vector<long long> answer;
  int n = nums.size();
  for (long long k : steps) {
    for (int quotient = 1; quotient <= n + 1; ++quotient) {
      long long candidate = quotient * k;
      if (!present.contains(candidate)) {
        answer.push_back(candidate);
        break;
      }
    }
  }
  return answer;
}
int main() {
  vector<int> nums = {2, 4, 6, 9};
  vector<int> steps = {2, 3};
  for (long long value : missingForSteps(nums, steps))
    cout << value << ' ';
  cout << '\n';
}
```

设询问数为 $Q$，期望时间复杂度为 $O(n+Qn)$，空间复杂度为 $O(n+Q)$。

### 变种四：允许非正数，并寻找最小缺失非负倍数

**新定义**：数组可含负数与重复值，返回最小缺失的非负倍数 $qk$，其中 $q\ge0$、$k>0$。

原题从商 1 开始；新目标必须从商 0 开始，因此若 0 缺失答案立即为 0。负倍数不影响非负候选。
数组长度为 $n$ 时，$0,1,\ldots,n$ 共 $n+1$ 个商仍保证至少一个缺失。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long missingNonnegativeMultiple(const vector<long long>& nums, long long k) {
  int n = nums.size();
  vector<char> seen(n + 1, false);
  for (long long value : nums) {
    if (value < 0 || value % k != 0)
      continue;
    long long quotient = value / k;
    if (quotient <= n)
      seen[quotient] = true;
  }
  for (int quotient = 0; quotient <= n; ++quotient) {
    if (!seen[quotient])
      return 1LL * quotient * k;
  }
  return -1;
}
int main() {
  vector<long long> nums = {-3, 0, 6, 6};
  cout << missingNonnegativeMultiple(nums, 3) << '\n';
}
```

时间复杂度为 $O(n)$，空间复杂度为 $O(n)$。与原题相比，关键变化是候选域包含 0，而不是负数或
重复值本身。

## 来源与知识入口

- [力扣官方题目](https://leetcode.cn/problems/smallest-missing-multiple-of-k/)
- [力扣第 472 场周赛](https://leetcode.cn/contest/weekly-contest-472/)
- [有限值域与哈希专题](https://www.wineandchord.com/algo/data-structures/hash-and-cache/)
- [2026-08-25 每日训练档案](https://www.wineandchord.com/algo/daily/2026-08-25/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/smallest-missing-multiple-of-k/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2253-a/">← [codeforces] CF Educational Round 193 Div.2 A The Best Card</a>
<span class="daily-archive-pager__empty"></span>
</nav>
