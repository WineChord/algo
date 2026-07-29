---
title: "[力扣 Top 18] LC 88 合并两个有序数组 简单"
---

# [力扣 Top 18] LC 88 合并两个有序数组 简单

<p class="daily-archive-kicker">2026-07-27 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-27 题目列表</a> · <a href="../../basics/sequence-invariants.md">进入知识专题</a></p>

## 官方原始信息

- 题号：88
- 官方中文标题：合并两个有序数组
- 官方难度：简单
- 官方链接：https://leetcode.cn/problems/merge-sorted-array/
- slug：`merge-sorted-array`
- 函数签名：`void merge(vector<int>& nums1, int m, vector<int>& nums2, int n)`
- 官方竞赛分：未标注。官方题面与本轮核对的官方 GraphQL 元数据均未提供竞赛归属或分值，不作推断。
- ZeroTracer 社区估算竞赛分：未收录。本轮于 2026-07-27 按题号与 slug 精确检索其公开 `data.json`，无匹配记录。

### 原始题意

`nums1` 的前 `m` 个元素与 `nums2` 的 `n` 个元素分别按非递减顺序排列。`nums1` 总长度为 `m+n`，尾部 `n` 个位置只是预留容量，不属于第一组有效数据。把两组有效数据合并成一个非递减序列，并原地写回 `nums1`；函数不返回新数组。

### 全部官方样例

1. `nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3`，结束后 `nums1 = [1,2,2,3,5,6]`。
2. `nums1 = [1], m = 1, nums2 = [], n = 0`，结束后 `nums1 = [1]`。
3. `nums1 = [0], m = 0, nums2 = [1], n = 1`，结束后 `nums1 = [1]`。原来的 `0` 只是容量占位，不是有效元素。

### 全部官方约束

- `nums1.length == m + n`
- `nums2.length == n`
- $0\le m,n\le200$
- $1\le m+n\le200$
- $-10^9\le nums1[i],nums2[j]\le10^9$
- 官方进阶：设计 $O(m+n)$ 时间算法。

## 约束推导与最优结论

两段输入已经有序，比较两个当前候选就能决定合并序列的下一项，因此不需要重新排序。难点是结果必须写回 `nums1`：若从左向右覆盖，尚未读取的 `nums1` 有效元素可能丢失；从右向左填充则不同，因为 `nums1` 尾部恰有 `n` 个空位，而最大剩余元素一定属于两个数组尾部之一。

维护 `i=m-1`、`j=n-1` 与写指针 `write=m+n-1`，每次把较大值写到最右空位。时间 $O(m+n)$，额外空间 $O(1)$，是最佳实用解。只移动和比较 `int`，不存在算术溢出。

## 样例手推与边界

样例一从尾部开始：

1. 比较 `3` 与 `6`，写入位置 5；
2. 比较 `3` 与 `5`，写入位置 4；
3. 比较 `3` 与 `2`，写入位置 3；
4. 比较 `2` 与 `2`，写入一个 `2`；
5. `nums2` 仍有 `2`，复制到剩余位置；`nums1` 的 `1` 已在正确位置。

关键边界：

- `m=0`：必须把 `nums2` 全部写入；
- `n=0`：无需改动；
- 一个数组所有值都小于另一个；
- 重复值；
- 有效值本身可以是 `0`，不能按数值识别占位区，只能信任 `m`；
- 负数和值域端点；
- 接口要求修改 `nums1`，不能只返回局部结果。

## 解法一：拼接后完整排序

先把 `nums2` 写进预留区，再排序全部 `m+n` 个位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    for (int j = 0; j < n; ++j) nums1[m + j] = nums2[j];
    sort(nums1.begin(), nums1.end());
  }
};
```

时间 $O((m+n)\log(m+n))$，排序栈通常 $O(\log(m+n))$。正确但浪费了输入已有顺序。

## 解法二：辅助数组正向归并

像归并排序一样，每次取两个未消费前缀的较小值。因为先写到辅助数组，不会覆盖 `nums1` 尚未读取的数据。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    vector<int> merged;
    merged.reserve(m + n);
    int i = 0, j = 0;
    while (i < m || j < n) {
      if (j == n || (i < m && nums1[i] <= nums2[j])) {
        merged.push_back(nums1[i++]);
      } else {
        merged.push_back(nums2[j++]);
      }
    }
    nums1 = move(merged);
  }
};
```

时间 $O(m+n)$，额外空间 $O(m+n)$。它消除了重复排序，但尚未利用 `nums1` 尾部容量。

## 解法三：从后向前原地归并（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    int i = m - 1;
    int j = n - 1;
    int write = m + n - 1;
    while (j >= 0) {
      if (i >= 0 && nums1[i] > nums2[j]) nums1[write--] = nums1[i--];
      else nums1[write--] = nums2[j--];
    }
  }
};
```

时间 $O(m+n)$，额外空间 $O(1)$。循环只需以 `j >= 0` 为条件：若 `nums2` 已耗尽，剩余 `nums1` 元素本来就在正确位置；若 `nums1` 先耗尽，循环会继续复制 `nums2`。

### 正确性证明

维护不变量：每轮开始时，`nums1[write+1..m+n-1]` 已经是全部未初始处理元素中最大的那一段，并位于最终正确位置；`nums1[0..i]` 与 `nums2[0..j]` 仍保持有序且尚未写入。

两个剩余有序前缀的全局最大值只能是 `nums1[i]` 或 `nums2[j]`。把较大者写到 `write`，恰好确定当前最右未定位置，且写入位置严格在 `i` 右侧，不会破坏 `nums1[0..i]`。归纳可知不变量持续成立。`nums2` 耗尽时，所有来自它的元素及被移动的 `nums1` 元素已经就位，未移动的 `nums1` 前缀也自然正确，因此最终数组完整有序。

## 方案比较与推荐

- 拼接排序：最短的基线，时间不是线性。
- 辅助数组正向归并：容易证明，可用于接口允许返回新数组或要求稳定记录来源的情形。
- 反向原地归并：同时达到线性时间和常数额外空间，充分利用输出缓冲区，是必须掌握的面试方案。
- 两种线性方案在渐进时间上相同；反向方案空间更优，辅助方案的控制流略直观并更易扩展到不可覆盖的输入。

## 常见错误

- 把 `nums1` 尾部的 `0` 当作有效数据或用数值判断占位；有效范围只能由 `m` 决定。
- 正向直接写 `nums1`，覆盖尚未读取的元素。
- 写指针初始化为 `m+n` 而越界。
- 只在 `i >= 0` 时循环，遗漏 `nums2` 的剩余前缀。
- 使用无符号下标后执行 `--i`，从 `0` 下溢成极大值。
- 把相等元素处理错误本身通常不影响数值答案，但需要来源稳定性时必须明确 tie-breaking。

## Follow-up 1：合并 `k` 个有序数组

每个数组只把当前首元素放入最小堆。弹出最小值后，只推进它所属数组的下标并加入下一个元素。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> mergeKArrays(vector<vector<int>>& arrays) {
    using Entry = tuple<int, int, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> heap;
    for (int array = 0; array < (int)arrays.size(); ++array) {
      if (!arrays[array].empty()) heap.emplace(arrays[array][0], array, 0);
    }
    vector<int> answer;
    while (!heap.empty()) {
      auto [value, array, index] = heap.top();
      heap.pop();
      answer.push_back(value);
      if (index + 1 < (int)arrays[array].size()) {
        heap.emplace(arrays[array][index + 1], array, index + 1);
      }
    }
    return answer;
  }
};
```

设总元素数为 $N$、数组数为 $k$，时间 $O(N\log k)$，空间 $O(k)$。

## Follow-up 2：合并两个有序链表

链表节点可直接重连，不需要数组式尾部容量。维护哨兵尾指针，每次接上较小头节点。对应 [LC 21 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {}
};
class Solution {
public:
  ListNode* mergeTwoLists(ListNode* first, ListNode* second) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (first && second) {
      if (first->val <= second->val) {
        tail->next = first;
        first = first->next;
      } else {
        tail->next = second;
        second = second->next;
      }
      tail = tail->next;
    }
    tail->next = first ? first : second;
    return dummy.next;
  }
};
```

时间 $O(m+n)$，额外空间 $O(1)$。

## Follow-up 3：两个数组都没有预留空间，但要求整体原地有序

要求合并后较小的前 `m` 个元素留在 `first`，其余留在 `second`。把两个数组视为一条虚拟连续序列，使用 Shell-sort 风格的 gap 比较交换；空间 $O(1)$，代价是多轮扫描。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void mergeWithoutBuffer(vector<int>& first, vector<int>& second) {
    int m = first.size();
    int total = m + second.size();
    auto at = [&](int index) -> int& {
      if (index < m) return first[index];
      return second[index - m];
    };
    for (int gap = (total + 1) / 2; gap > 0; gap = gap == 1 ? 0 : (gap + 1) / 2) {
      for (int left = 0; left + gap < total; ++left) {
        int right = left + gap;
        if (at(left) > at(right)) swap(at(left), at(right));
      }
    }
  }
};
```

时间通常写作 $O((m+n)\log(m+n))$，空间 $O(1)$。它不是稳定归并；若要求稳定性或严格线性时间，需要更复杂的原地归并技术或额外缓冲区。

## Follow-up 4：合并两个大到无法装入内存的有序流

每个输入流只保留一个当前值，像外部归并排序一样逐个写到输出流。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void mergeStreams(istream& first, istream& second, ostream& output) {
    int leftValue = 0, rightValue = 0;
    bool hasLeft = static_cast<bool>(first >> leftValue);
    bool hasRight = static_cast<bool>(second >> rightValue);
    bool needSpace = false;
    while (hasLeft || hasRight) {
      int value;
      if (!hasRight || (hasLeft && leftValue <= rightValue)) {
        value = leftValue;
        hasLeft = static_cast<bool>(first >> leftValue);
      } else {
        value = rightValue;
        hasRight = static_cast<bool>(second >> rightValue);
      }
      if (needSpace) output << ' ';
      output << value;
      needSpace = true;
    }
  }
};
```

时间 $O(m+n)$，内存 $O(1)$，但输出只能顺序产生，不能随机访问或回写过去位置。

## Follow-up 5：稳定保留每个元素的来源

当相等值需要保持“第一输入优先”，为元素附带来源与原下标；相等时选择 `first` 即可保证跨数组稳定性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TaggedValue {
  int value;
  int source;
  int index;
};
class Solution {
public:
  vector<TaggedValue> stableMerge(const vector<int>& first, const vector<int>& second) {
    vector<TaggedValue> answer;
    answer.reserve(first.size() + second.size());
    int i = 0, j = 0;
    while (i < (int)first.size() || j < (int)second.size()) {
      if (j == (int)second.size() || (i < (int)first.size() && first[i] <= second[j])) {
        answer.push_back({first[i], 0, i});
        ++i;
      } else {
        answer.push_back({second[j], 1, j});
        ++j;
      }
    }
    return answer;
  }
};
```

时间 $O(m+n)$，输出空间 $O(m+n)$。`source,index` 使来源信息可恢复。

## Follow-up 6：合并并去重

若目标是有序集合并集，而不是多重集合归并，遇到相同值只输出一次；辅助 `append` 同时消除各数组内部重复。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> mergeUnique(const vector<int>& first, const vector<int>& second) {
    vector<int> answer;
    int i = 0, j = 0;
    auto append = [&](int value) {
      if (answer.empty() || answer.back() != value) answer.push_back(value);
    };
    while (i < (int)first.size() || j < (int)second.size()) {
      if (j == (int)second.size() || (i < (int)first.size() && first[i] <= second[j])) {
        append(first[i++]);
      } else {
        append(second[j++]);
      }
    }
    return answer;
  }
};
```

时间 $O(m+n)$，输出之外额外空间 $O(1)$。

## 验证说明

- 对随机有序数组，使用“拼接后排序”作 oracle，比较辅助归并与反向原地归并。
- 覆盖三个官方样例，以及 `m=0`、`n=0`、重复值、负值、交错序列和完全分离序列。
- 本文每个 C++ 代码块均按 C++23 单独做语法编译；随机种子、用例规模与真实结果记录在同目录机器报告中。

## Reference

- [官方题目](https://leetcode.cn/problems/merge-sorted-array/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-17-lc215.md">← [力扣 Top 17] LC 215 数组中的第 K 个最大元素 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-19-lc72.md">[力扣 Top 19] LC 72 编辑距离 中等 →</a>
</nav>
