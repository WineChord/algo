---
title: "[力扣每日一题] 2026-08-20｜LC 3069 将元素分配到两个数组中 I"
---

# [力扣每日一题] 2026-08-20｜LC 3069 将元素分配到两个数组中 I

<p class="daily-archive-kicker">2026-08-20 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-20 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3c7e47cc05473308fe37c2dca06d8f25b02ce0a6ef0d75dd5db7d4b69f6c86af -->
[官方题目：3069. 将元素分配到两个数组中 I](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/)

## 官方原始信息

- 题号与标题：3069. 将元素分配到两个数组中 I。
- 官方难度：简单。
- 官方链接：[LeetCode 中国题面](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/)。
- 工作日期：2026-08-20（Asia/Shanghai）；力扣中国官方“每日一题”接口将本题标为当天题目。
- 函数签名：`vector<int> resultArray(vector<int>& nums)`。
- 官方标签：数组、模拟。
- 本题曾作为第 387 场周赛 Q1；ZeroTracer 社区估算竞赛分为 1203.80，抓取于
  2026-08-20，这不是力扣官方难度或官方分值。

给定一个按题意从 1 开始编号、元素互不相同的数组 `nums`。通过 $n$ 次操作把所有元素按
原顺序分配到 `arr1`、`arr2`：

1. 第一个元素追加到 `arr1`；
2. 第二个元素追加到 `arr2`；
3. 对之后每个元素，若 `arr1` 的末元素严格大于 `arr2` 的末元素，就追加到 `arr1`，
   否则追加到 `arr2`。

最后返回 `arr1` 后接 `arr2` 的连接结果。

### 全部官方样例

示例 1：

```text
输入：nums = [2,1,3]
输出：[2,3,1]
解释：先得到 arr1 = [2]、arr2 = [1]；因为 2 > 1，3 进入 arr1。
```

示例 2：

```text
输入：nums = [5,4,3,8]
输出：[5,3,4,8]
解释：3 先因 5 > 4 进入 arr1；随后 4 > 3，8 进入 arr2。
```

### 全部约束

- $3\le n\le50$。
- $1\le\texttt{nums}[i]\le100$。
- `nums` 中所有元素互不相同。

## 约束与模型

每一步的去向只依赖两个数组当前末元素，没有搜索、排序或全局最优选择。按照规则模拟就是
完整算法；至少要读取 $n$ 个输入并返回 $n$ 个输出，因此 $\Theta(n)$ 时间已经最优。

两个数组合计保存所有元素，空间为 $\Theta(n)$，而返回值本身也占 $\Theta(n)$。值域和
元素互异并不要求计数结构；互异只意味着本题中两个末元素不会相等，但实现仍应忠实保留
“不大于时进入 `arr2`”的规则。

## 样例手推与边界

示例 2 的状态依次为：

```text
处理 5：arr1 = [5]，arr2 = []
处理 4：arr1 = [5]，arr2 = [4]
处理 3：5 > 4，arr1 = [5,3]，arr2 = [4]
处理 8：3 < 4，arr1 = [5,3]，arr2 = [4,8]
连接后：[5,3,4,8]
```

最小规模 $n=3$ 只做一次比较；后续元素可能始终进入同一数组，也可能来回切换。判断使用的
是更新后的实时 `back()`，不是数组最大值、首元素、长度或原数组相邻值。连接顺序固定为
`arr1 + arr2`，两个数组内部都保持稳定的原始相对顺序。

## 解法：正确模拟与最佳实用解

这道题的“暴力”就是逐条执行定义，同时也是渐进最优解，没有可以消除的重复状态。实现时
分别预留容量，避免小数组多次扩容；最后把 `arr2` 追加到 `arr1` 并返回。

### 正确性证明

对已处理前缀长度 $i$ 做归纳。

初始两步中，程序与定义都把 `nums[0]` 放入 `arr1`、`nums[1]` 放入 `arr2`，状态一致。
假设处理前 $i$ 个元素后两边状态完全一致。第 $i$ 个新元素到来时，程序读取的两个
`back()` 就是定义中的两个当前末元素，所以严格大于时与定义同样选择 `arr1`，其余情况
同样选择 `arr2`；追加操作也保持数组内部顺序。于是处理 $i+1$ 个元素后状态仍一致。

归纳到 $n$，程序得到的两个数组与题意唯一过程完全相同；最后又按规定连接 `arr1`、
`arr2`，故返回结果正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> resultArray(vector<int>& nums) {
    vector<int> first{nums[0]};
    vector<int> second{nums[1]};
    first.reserve(nums.size());
    second.reserve(nums.size());
    for (int i = 2; i < static_cast<int>(nums.size()); ++i) {
      if (first.back() > second.back()) first.push_back(nums[i]);
      else second.push_back(nums[i]);
    }
    first.insert(first.end(), second.begin(), second.end());
    return first;
  }
};
```

时间复杂度 $O(n)$，包括最终连接；除返回结果外，临时存储也是 $O(n)$。若允许移动并改变
输入，可以复用部分缓冲区，但渐进空间不会优于必需的输出。

## 方案比较与推荐

- 两个 `vector` 直接模拟最贴近定义，证明负担和出错面都最小。
- 可以只记录每个原元素的去向位，再稳定收集两组；仍是 $O(n)$，但多一层间接表示。
- 使用 `list` 能常数时间拼接，却会产生逐节点分配和较差缓存局部性；本题不值得。

优先记忆“状态只由两个末元素构成，直接模拟”，不要把简单模拟误做成排序或堆问题。

## 易错点

- 题面叙述从 1 开始编号，C++ 数组从 0 开始；循环应从 `i = 2` 开始。
- 比较必须是严格 `>`；即使变种允许相等，相等也进入 `arr2`。
- 每次比较实时末元素，不能比较两个数组的最大值或长度。
- 最终必须先放完整 `arr1`，再放完整 `arr2`，不能按处理顺序原样返回。
- 不要在遍历 `nums` 时把结果追加回同一个 `nums`，否则迭代范围与输入语义会漂移。

## 可复现验证

代码按 C++23 编译并通过两组官方样例。独立 oracle 只维护两个末元素和每个原下标的去向，
最后按去向稳定收集；对 $3\le n\le8$ 的排列进行穷举，并随机生成到 $n=50$ 的互异值数组，
与双 `vector` 实现逐项比较。测试覆盖连续进入第一组、连续进入第二组、交替分支和值域端点。

## 变种一：同时返回每个原元素的去向

新定义：除连接结果外，还返回每个 `nums[i]` 被放入第 1 组还是第 2 组。原算法仍成立，只需
在追加时记录标签；时间和空间均为 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Distribution {
  vector<int> result;
  vector<int> group;
};
class AssignmentTrace {
public:
  Distribution distribute(const vector<int>& nums) {
    vector<int> first{nums[0]}, second{nums[1]};
    vector<int> group(nums.size());
    group[0] = 1;
    group[1] = 2;
    for (int i = 2; i < static_cast<int>(nums.size()); ++i) {
      if (first.back() > second.back()) {
        first.push_back(nums[i]);
        group[i] = 1;
      } else {
        second.push_back(nums[i]);
        group[i] = 2;
      }
    }
    first.insert(first.end(), second.begin(), second.end());
    return {first, group};
  }
};
```

## 变种二：推广到 $k$ 个数组

新定义：$1\le k\le n$，前 $k$ 个元素依次初始化 $k$ 个数组；之后把新元素放入“当前末元素
最大”的数组，若并列取编号最小者；最终按编号连接。两个末元素的常数状态变成 $k$ 个候选，
最大堆始终只保存每组当前末元素：选中堆顶后先弹出，再压入更新值。每次追加 $O(\log k)$，
总时间 $O(n\log k)$，空间 $O(n+k)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class KWayDistribution {
public:
  vector<int> distribute(const vector<int>& nums, int k) {
    vector<vector<int>> groups(k);
    priority_queue<pair<int, int>> candidates;
    for (int i = 0; i < k; ++i) {
      groups[i].push_back(nums[i]);
      candidates.push({nums[i], -i});
    }
    for (int i = k; i < static_cast<int>(nums.size()); ++i) {
      int group = -candidates.top().second;
      candidates.pop();
      groups[group].push_back(nums[i]);
      candidates.push({nums[i], -group});
    }
    vector<int> result;
    result.reserve(nums.size());
    for (const auto& group : groups) {
      result.insert(result.end(), group.begin(), group.end());
    }
    return result;
  }
};
```

## 变种三：在线追加并支持撤销

新定义：数字逐个到来，仍遵守原规则，并支持撤销最近一次追加。记录每步进入哪一组，撤销时
从对应数组末尾弹出即可；恢复后的两个末元素天然就是上一状态。追加、撤销均摊 $O(1)$，
导出连接结果 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OnlineDistribution {
public:
  void append(int value) {
    int group;
    if (history_.empty()) group = 0;
    else if (history_.size() == 1) group = 1;
    else group = first_.back() > second_.back() ? 0 : 1;
    if (group == 0) first_.push_back(value);
    else second_.push_back(value);
    history_.push_back(group);
  }
  bool undo() {
    if (history_.empty()) return false;
    int group = history_.back();
    history_.pop_back();
    if (group == 0) first_.pop_back();
    else second_.pop_back();
    return true;
  }
  vector<int> result() const {
    vector<int> answer = first_;
    answer.insert(answer.end(), second_.begin(), second_.end());
    return answer;
  }
private:
  vector<int> first_;
  vector<int> second_;
  vector<int> history_;
};
```

## 变种四：升级为 3072. 将元素分配到两个数组中 II

在线评测题：[3072. 将元素分配到两个数组中 II](https://leetcode.cn/problems/distribute-elements-into-two-arrays-ii/)。
新规则比较两个数组中严格大于当前值的元素个数；计数相同时选更短数组，再相同选 `arr1`。
末元素状态已失效，需要坐标压缩加两个树状数组维护前缀频数。每步查询“大于当前值”的数量
并更新所选结构，时间 $O(n\log n)$，空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
public:
  explicit Fenwick(int n) : tree_(n + 1) {}
  void add(int index, int value) {
    for (; index < static_cast<int>(tree_.size()); index += index & -index) {
      tree_[index] += value;
    }
  }
  int prefix(int index) const {
    int sum = 0;
    for (; index > 0; index -= index & -index) sum += tree_[index];
    return sum;
  }
private:
  vector<int> tree_;
};
class Solution {
public:
  vector<int> resultArray(vector<int>& nums) {
    vector<int> values = nums;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    Fenwick firstCount(values.size()), secondCount(values.size());
    vector<int> first{nums[0]}, second{nums[1]};
    auto rank = [&](int value) {
      return lower_bound(values.begin(), values.end(), value) - values.begin() + 1;
    };
    firstCount.add(rank(nums[0]), 1);
    secondCount.add(rank(nums[1]), 1);
    for (int i = 2; i < static_cast<int>(nums.size()); ++i) {
      int position = rank(nums[i]);
      int greaterFirst = first.size() - firstCount.prefix(position);
      int greaterSecond = second.size() - secondCount.prefix(position);
      if (greaterFirst > greaterSecond ||
          (greaterFirst == greaterSecond && first.size() <= second.size())) {
        first.push_back(nums[i]);
        firstCount.add(position, 1);
      } else {
        second.push_back(nums[i]);
        secondCount.add(position, 1);
      }
    }
    first.insert(first.end(), second.begin(), second.end());
    return first;
  }
};
```

## 来源

- [LeetCode 3069 官方题面](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/)，
  核对于 2026-08-20。
- [ZeroTracer 公开竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/)，抓取于
  2026-08-20；数值为社区估算。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-c/">← [codeforces] CF Round 1117 Div.2 C Spying on the Beaver</a>
<span class="daily-archive-pager__empty"></span>
</nav>
