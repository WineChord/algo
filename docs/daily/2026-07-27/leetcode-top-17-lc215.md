---
title: "[力扣 Top 17] LC 215 数组中的第 K 个最大元素 中等"
---

# [力扣 Top 17] LC 215 数组中的第 K 个最大元素 中等

<p class="daily-archive-kicker">2026-07-27 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

## 官方原始信息

- 题号：215
- 官方中文标题：数组中的第 K 个最大元素
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/kth-largest-element-in-an-array/)
- slug：`kth-largest-element-in-an-array`
- 函数签名：`int findKthLargest(vector<int>& nums, int k)`
- 官方竞赛分：未标注。官方题面与本轮核对的官方 GraphQL 元数据均未提供竞赛归属或分值，不作推断。
- ZeroTracer 社区估算竞赛分：未收录。本轮于 2026-07-27 按题号与 slug 精确检索其公开 `data.json`，无匹配记录。

### 原始题意

给定整数数组 `nums` 与整数 `k`，返回把全部元素按非递增顺序排列后位于第 `k` 个位置的值。重复元素各自占一个排名位置，题目求的不是第 `k` 个不同值。官方中文题面还要求设计时间复杂度为 $O(n)$ 的算法。

### 全部官方样例

1. 输入 `nums = [3,2,1,5,6,4], k = 2`，输出 `5`。
2. 输入 `nums = [3,2,3,1,2,4,5,5,6], k = 4`，输出 `4`；两个 `5` 分别占据第二、第三个位置。

### 全部官方约束

- $1\le k\le n=\texttt{nums.length}\le10^5$
- $-10^4\le nums[i]\le10^4$

## 约束推导与最优结论

若转为升序下标，答案是第 $t=n-k$ 小的元素。完整排序得到的顺序信息远多于一个秩查询所需；堆只保留当前最大的 `k` 个数；选择算法则通过分区只递归到包含目标秩的一侧。

本题还有非常关键的值域约束：只有 $U=20001$ 个可能整数。频次数组从大到小累计即可在 $O(n+U)$ 时间、$O(U)$ 空间给出确定性答案，满足当前题面的线性要求，且不会遇到随机快选的二次最坏情况。因此：

- 严格针对本题约束，推荐频次数组；
- 面试考察通用 order statistic 时，推荐随机三路快速选择，期望 $O(n)$、额外空间 $O(1)$；
- 若必须保证比较模型最坏 $O(n)$，使用 median-of-medians，但实现和常数明显更大。

所有值与答案在 $[-10^4,10^4]$，计数不超过 $10^5$，`int` 足够。

## 样例手推与边界

样例一中 $n=6,k=2$，升序目标下标为 $t=4$。若某次三路分区把数组分成“小于 pivot / 等于 pivot / 大于 pivot”，只要 $t$ 落入等值段，pivot 就是答案；否则只保留包含 $t$ 的一侧。

边界包括：

- `n=1,k=1`；
- `k=1` 求最大值，`k=n` 求最小值；
- 全部元素相同；
- 大量重复值，必须按出现次数计秩；
- 已升序、已降序；
- 正负值和值域两端；
- 随机快选必须避免固定端点 pivot 在有序输入上稳定退化。

## 解法一：完整排序

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findKthLargest(vector<int>& nums, int k) {
    sort(nums.begin(), nums.end(), greater<int>());
    return nums[k - 1];
  }
};
```

时间 $O(n\log n)$，排序栈通常 $O(\log n)$。它是最直接的正确基线，却计算了全部秩关系。

## 解法二：大小为 `k` 的最小堆

堆中始终保存扫描前缀里最大的 `k` 个元素；堆顶是这 `k` 个元素中最小者，也就是当前前缀第 `k` 大。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int value : nums) {
      heap.push(value);
      if ((int)heap.size() > k) heap.pop();
    }
    return heap.top();
  }
};
```

时间 $O(n\log k)$，空间 $O(k)$。当 $k\ll n$ 或数据以流形式到达时很实用，但在 $k=\Theta(n)$ 时仍是 $O(n\log n)$。

## 解法三：有限值域计数（当前约束下的最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findKthLargest(vector<int>& nums, int k) {
    const int offset = 10000;
    vector<int> frequency(20001);
    for (int value : nums) ++frequency[value + offset];
    for (int index = 20000; index >= 0; --index) {
      k -= frequency[index];
      if (k <= 0) return index - offset;
    }
    throw logic_error("valid k must produce an answer");
  }
};
```

时间 $O(n+U)$，空间 $O(U)$，$U=20001$。

### 正确性证明

从最大值对应的桶向下扫描。处理完值 $v$ 的桶后，从原数组中严格大于 $v$ 的元素与等于 $v$ 的元素已经按非递增顺序占据了前若干名。每跨过一个桶，就从尚未定位的排名 `k` 中减去该值的出现次数。第一次出现 `k <= 0` 时，目标排名落在当前值的重复块内，因此当前值恰为第 `k` 大。所有数组元素都在桶覆盖值域内，合法 `k` 必然返回。

## 解法四：随机三路快速选择

三路分区把重复 pivot 聚成一个连续段，能避免全相等或高重复输入反复缩小一个元素。目标使用升序下标 `n-k`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findKthLargest(vector<int>& nums, int k) {
    int target = nums.size() - k;
    int left = 0, right = nums.size() - 1;
    mt19937 generator(chrono::steady_clock::now().time_since_epoch().count());
    while (left <= right) {
      uniform_int_distribution<int> distribution(left, right);
      int pivot = nums[distribution(generator)];
      int less = left, current = left, greater = right;
      while (current <= greater) {
        if (nums[current] < pivot) {
          swap(nums[less++], nums[current++]);
        } else if (nums[current] > pivot) {
          swap(nums[current], nums[greater--]);
        } else {
          ++current;
        }
      }
      if (target < less) right = less - 1;
      else if (target > greater) left = greater + 1;
      else return pivot;
    }
    throw logic_error("valid target must be found");
  }
};
```

期望时间 $O(n)$，最坏时间 $O(n^2)$，额外空间 $O(1)$。

### 分区不变量与正确性

三路循环始终保持 `[left,less)` 小于 pivot，`[less,current)` 等于 pivot，`(greater,right]` 大于 pivot，而 `[current,greater]` 尚未分类。结束后：

- 若目标下标小于 `less`，目标只可能在小值段；
- 若大于 `greater`，只可能在大值段；
- 否则目标位于等值段，答案就是 pivot。

每轮丢弃至少等值段及目标另一侧；返回时对应的升序秩为 $n-k$，也就是第 `k` 大。

## 解法五：median-of-medians 的最坏线性选择

每五个元素取中位数，再递归选择这些中位数的中位数作 pivot。它保证两侧都能丢弃固定比例元素，从而满足递推 $T(n)\le T(n/5)+T(7n/10)+O(n)=O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int selectValue(vector<int>& values, int left, int right, int target) {
    if (right - left + 1 <= 5) {
      sort(values.begin() + left, values.begin() + right + 1);
      return values[target];
    }
    int medians = 0;
    for (int start = left; start <= right; start += 5) {
      int finish = min(start + 4, right);
      sort(values.begin() + start, values.begin() + finish + 1);
      int median = start + (finish - start) / 2;
      swap(values[left + medians], values[median]);
      ++medians;
    }
    int pivot = selectValue(values, left, left + medians - 1, left + medians / 2);
    int less = left, current = left, greater = right;
    while (current <= greater) {
      if (values[current] < pivot) {
        swap(values[less++], values[current++]);
      } else if (values[current] > pivot) {
        swap(values[current], values[greater--]);
      } else {
        ++current;
      }
    }
    if (target < less) return selectValue(values, left, less - 1, target);
    if (target > greater) return selectValue(values, greater + 1, right, target);
    return pivot;
  }
public:
  int findKthLargest(vector<int>& nums, int k) {
    return selectValue(nums, 0, nums.size() - 1, nums.size() - k);
  }
};
```

最坏时间 $O(n)$，递归栈 $O(\log n)$。理论保证最强，但常数、代码长度和证明负担都高于随机快选；除非面试官明确追问最坏线性选择，一般不优先手写。

## 常见错误

- 把第 `k` 大误当成第 `k` 个不同值。
- 升序目标写成 `n-k+1`，发生一位偏移。
- 最小堆超过 `k` 时没有弹出，最后堆顶变成全局最小。
- 快选分区后两边都递归，退化为完整快速排序。
- 对重复值使用不严谨的二路分区，可能停滞或严重退化。
- 声称随机快选“最坏 $O(n)$”；它只有期望线性。
- 忽略值域偏移，负数访问频次数组越界。

## Follow-up 1：数据流中的第 `k` 大

数据持续到达，无法回看或排序全部历史。维护大小为 `k` 的最小堆；每次加入后的堆顶就是当前第 `k` 大。对应 [LC 703 数据流中的第 K 大元素](https://leetcode.cn/problems/kth-largest-element-in-a-stream/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class KthLargest {
  int k;
  priority_queue<int, vector<int>, greater<int>> heap;
public:
  KthLargest(int rank, vector<int>& nums) : k(rank) {
    for (int value : nums) add(value);
  }
  int add(int value) {
    heap.push(value);
    if ((int)heap.size() > k) heap.pop();
    return heap.top();
  }
};
```

初始化 $O(n\log k)$，每次加入 $O(\log k)$，空间 $O(k)$。

## Follow-up 2：前 `k` 个高频元素

排名对象从“元素值”变成“出现频率”。先计数，再把值按频率放入桶，从高频桶向下收集。对应 [LC 347 前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    for (int value : nums) ++frequency[value];
    vector<vector<int>> buckets(nums.size() + 1);
    for (auto [value, count] : frequency) buckets[count].push_back(value);
    vector<int> answer;
    for (int count = nums.size(); count >= 1 && (int)answer.size() < k; --count) {
      for (int value : buckets[count]) {
        answer.push_back(value);
        if ((int)answer.size() == k) break;
      }
    }
    return answer;
  }
};
```

期望时间 $O(n)$，空间 $O(n)$。

## Follow-up 3：每个滑动窗口的第 `k` 大

窗口既加入又删除。用两个 `multiset`：`high` 始终保存窗口中最大的 `k` 个元素，答案是 `*high.begin()`；`low` 保存其余元素。重复值由多重集合自然处理。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  multiset<int> low;
  multiset<int> high;
  int k;
  void rebalance() {
    while ((int)high.size() > k) {
      auto it = high.begin();
      low.insert(*it);
      high.erase(it);
    }
    while ((int)high.size() < k && !low.empty()) {
      auto it = prev(low.end());
      high.insert(*it);
      low.erase(it);
    }
    while (!low.empty() && !high.empty() && *prev(low.end()) > *high.begin()) {
      auto lowIt = prev(low.end());
      auto highIt = high.begin();
      int lowValue = *lowIt;
      int highValue = *highIt;
      low.erase(lowIt);
      high.erase(highIt);
      low.insert(highValue);
      high.insert(lowValue);
    }
  }
  void add(int value) {
    if (high.empty() || value >= *high.begin()) high.insert(value);
    else low.insert(value);
    rebalance();
  }
  void remove(int value) {
    auto highIt = high.find(value);
    if (highIt != high.end()) high.erase(highIt);
    else {
      auto lowIt = low.find(value);
      if (lowIt == low.end()) throw logic_error("value must exist in window");
      low.erase(lowIt);
    }
    rebalance();
  }
public:
  vector<int> kthLargestInWindows(vector<int>& nums, int window, int rank) {
    if (rank < 1 || rank > window || window > (int)nums.size()) return {};
    k = rank;
    low.clear();
    high.clear();
    for (int i = 0; i < window; ++i) add(nums[i]);
    vector<int> answer = {*high.begin()};
    for (int right = window; right < (int)nums.size(); ++right) {
      remove(nums[right - window]);
      add(nums[right]);
      answer.push_back(*high.begin());
    }
    return answer;
  }
};
```

每次滑动 $O(\log w)$，空间 $O(w)$，其中 $w$ 是窗口长度。

## Follow-up 4：行列有序矩阵中的第 `k` 小

对答案值二分。对给定 `mid`，从左下角出发可在 $O(n)$ 时间统计不大于 `mid` 的元素数。对应 [LC 378 有序矩阵中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int countAtMost(const vector<vector<int>>& matrix, int value) {
    int n = matrix.size();
    int row = n - 1, column = 0, count = 0;
    while (row >= 0 && column < n) {
      if (matrix[row][column] <= value) {
        count += row + 1;
        ++column;
      } else {
        --row;
      }
    }
    return count;
  }
public:
  int kthSmallest(vector<vector<int>>& matrix, int k) {
    int left = matrix.front().front();
    int right = matrix.back().back();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (countAtMost(matrix, middle) >= k) right = middle;
      else left = middle + 1;
    }
    return left;
  }
};
```

时间 $O(n\log V)$，空间 $O(1)$，其中 $V$ 是矩阵最大最小值之差。

## Follow-up 5：第 `k` 个不同的最大值

现在重复值只占一个排名。先去重，再维护大小为 `k` 的最小堆；若不同值不足 `k` 个，明确报告无答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  optional<int> kthDistinctLargest(vector<int>& nums, int k) {
    unordered_set<int> seen;
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int value : nums) {
      if (!seen.insert(value).second) continue;
      heap.push(value);
      if ((int)heap.size() > k) heap.pop();
    }
    if ((int)heap.size() < k) return nullopt;
    return heap.top();
  }
};
```

期望时间 $O(n\log k)$，空间 $O(d+k)$，其中 $d$ 是不同值数量。

## Follow-up 6：同一静态数组的大量秩查询

若数组不更新但有很多不同 `k`，一次排序后每次 $O(1)$ 回答，比为每个查询重复快选更合适。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OrderStatistics {
  vector<int> values;
public:
  explicit OrderStatistics(vector<int> nums) : values(move(nums)) {
    sort(values.begin(), values.end());
  }
  int kthLargest(int k) const {
    if (k < 1 || k > (int)values.size()) throw out_of_range("invalid rank");
    return values[values.size() - k];
  }
  int kthSmallest(int k) const {
    if (k < 1 || k > (int)values.size()) throw out_of_range("invalid rank");
    return values[k - 1];
  }
};
```

预处理 $O(n\log n)$，空间 $O(n)$；每个查询 $O(1)$。

## 验证说明

- 对随机数组的每个合法 `k`，用完整排序作 oracle，比较最小堆、频次数组、随机三路快选与 median-of-medians。
- 特别覆盖全相等、高重复、单元素、升序、降序、`k=1`、`k=n` 及值域端点。
- 本文每个 C++ 代码块均按 C++23 单独做语法编译；随机种子、用例规模与真实结果记录在同目录机器报告中。

## Reference

- [官方题目](https://leetcode.cn/problems/kth-largest-element-in-an-array/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-16-lc56/">← [力扣 Top 16] LC 56 合并区间 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-18-lc88/">[力扣 Top 18] LC 88 合并两个有序数组 简单 →</a>
</nav>
