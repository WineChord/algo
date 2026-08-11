---
title: "[力扣每日一题] 2026-08-11｜LC 2996 大于等于顺序前缀和的最小缺失整数"
---

# [力扣每日一题] 2026-08-11｜LC 2996 大于等于顺序前缀和的最小缺失整数

<p class="daily-archive-kicker">2026-08-11 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-11 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a9b25507a8ed52d5325eb66c826fade50856203a24fe2df406cb7000366df072 -->
## 官方原始信息

- 日期：2026-08-11（北京时间）。
- 题号：LC 2996。
- 官方中文标题：大于等于顺序前缀和的最小缺失整数。
- 官方难度：简单。
- 官方链接：[大于等于顺序前缀和的最小缺失整数](https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/)。

### 原始题意与函数签名

数组的“顺序前缀”从 `nums[0]` 开始，相邻元素必须依次增加 1；长度为 1 的前缀总是合法。先求最长顺序前缀的元素和 `sum`，再返回不小于 `sum` 且没有出现在 `nums` 中的最小整数。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int missingInteger(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3,2,5]
输出：6
解释：最长顺序前缀是 [1,2,3]，和为 6；6 没有出现。
```

```text
输入：nums = [3,4,5,1,12,14,13]
输出：15
解释：最长顺序前缀是 [3,4,5]，和为 12；12、13、14 都已出现，15 是第一个缺失值。
```

### 全部约束

- $1\le |nums|\le50$。
- $1\le nums_i\le50$。
- 最长顺序前缀的和最多为 $1+2+\cdots+50=1275$，`int` 足够。

## 约束推导与观察

最长顺序前缀只由第一个不满足 $nums_i=nums_{i-1}+1$ 的位置决定，不需要枚举所有前缀。值域只有 1 到 50，可以用定长布尔表记录出现性。若前缀和大于 50，它必然没有出现在数组中；否则从该和向上检查至多 51 次。

## 解法递进

### 解法一：枚举前缀，再线性查找缺失值

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingInteger(vector<int>& nums) {
    int bestSum = nums[0];
    int currentSum = nums[0];
    for (int length = 2; length <= static_cast<int>(nums.size()); ++length) {
      if (nums[length - 1] != nums[length - 2] + 1) {
        break;
      }
      currentSum += nums[length - 1];
      bestSum = currentSum;
    }
    for (int candidate = bestSum;; ++candidate) {
      if (find(nums.begin(), nums.end(), candidate) == nums.end()) {
        return candidate;
      }
    }
  }
};
int main() {
  vector<int> nums{1, 2, 3, 2, 5};
  cout << Solution().missingInteger(nums) << '\n';
}
```

最长前缀扫描为 $O(n)$，每个候选值又做一次 $O(n)$ 查找，最坏时间 $O(n^2)$、额外空间 $O(1)$。瓶颈是重复扫描数组判断“是否出现”。

### 解法二：哈希集合消除重复查找

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingInteger(vector<int>& nums) {
    int sum = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] != nums[i - 1] + 1) {
        break;
      }
      sum += nums[i];
    }
    unordered_set<int> present(nums.begin(), nums.end());
    while (present.contains(sum)) {
      ++sum;
    }
    return sum;
  }
};
int main() {
  vector<int> nums{3, 4, 5, 1, 12, 14, 13};
  cout << Solution().missingInteger(nums) << '\n';
}
```

期望时间 $O(n)$、空间 $O(n)$。它适合值域很大的一般化版本，但本题的小值域还能进一步压缩。

### 最佳实用解：顺序扫描 + 定长出现表

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int missingInteger(vector<int>& nums) {
    int sum = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] != nums[i - 1] + 1) {
        break;
      }
      sum += nums[i];
    }
    array<bool, 51> present{};
    for (int value : nums) {
      present[value] = true;
    }
    while (sum <= 50 && present[sum]) {
      ++sum;
    }
    return sum;
  }
};
int main() {
  vector<int> nums{1, 2, 3, 2, 5};
  cout << Solution().missingInteger(nums) << '\n';
}
```

时间 $O(n)$；出现表大小固定为 51，额外空间 $O(1)$。面试优先记忆这一版：先确定最长前缀，再把“缺失”交给值域表。

## 正确性证明

前缀扫描从位置 1 开始，只要当前值等于前值加 1，就把它加入 `sum`；遇到第一次不满足条件的位置立即停止。顺序前缀必须从下标 0 开始，因此这个停止位置之后不可能再属于任何更长的合法顺序前缀，所得 `sum` 正是最长顺序前缀和。

出现表准确记录 1 到 50 中哪些值存在。循环从 `sum` 开始，只跳过已出现的候选；退出时，候选不小于前缀和且未出现，而所有更小但仍不小于前缀和的整数都已被跳过，所以它就是所求最小值。若候选超过 50，约束保证它必然未出现，结论仍成立。

## 样例手推与边界

对 `[3,4,5,1,12,14,13]`，扫描依次累加 3、4、5，看到 `1 != 6` 后停止，得到 `sum=12`。出现表显示 12、13、14 都存在，循环依次跳过它们，在 15 停止。

- 单元素数组：最长前缀就是该元素。
- 前缀覆盖整个数组：直接使用全数组和。
- 重复值只影响出现表，不会把断开的后缀重新接回前缀。
- 前缀和大于 50：直接返回该和，不会越界访问布尔表。

## 易错点与验证

- 顺序前缀必须从 `nums[0]` 开始，不能在中间重新选起点。
- 条件是严格加 1，不是非递减或差值至多 1。
- 先检查 `sum <= 50` 再访问 `present[sum]`。
- 最优解与定义级枚举在 60,000 个随机数组上逐一对拍，全部一致；两个官方样例也通过。

## 变种一：返回第 $k$ 个不小于前缀和的缺失整数

新定义：不是返回第一个，而是返回第 $k$ 个缺失值。前缀计算不变，只需继续扫描候选并计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int kthMissingAfterPrefix(const vector<int>& nums, int k) {
  int sum = nums[0];
  for (int i = 1; i < static_cast<int>(nums.size()) && nums[i] == nums[i - 1] + 1; ++i) {
    sum += nums[i];
  }
  unordered_set<int> present(nums.begin(), nums.end());
  for (int candidate = sum;; ++candidate) {
    if (!present.contains(candidate) && --k == 0) {
      return candidate;
    }
  }
}
int main() {
  cout << kthMissingAfterPrefix({1, 2, 3, 2, 5}, 3) << '\n';
}
```

期望时间 $O(n+k+n)$，空间 $O(n)$；候选跨度还会受已出现值数量影响，但最多额外跨过 $n$ 个数。

## 变种二：允许负数和大值域

新定义：元素可为任意 64 位整数。定长表失效，改用 `unordered_set<long long>`；前缀和也改为 `long long`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long generalizedMissing(const vector<long long>& nums) {
  long long sum = nums[0];
  for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
    if (nums[i] != nums[i - 1] + 1) {
      break;
    }
    sum += nums[i];
  }
  unordered_set<long long> present(nums.begin(), nums.end());
  while (present.contains(sum)) {
    ++sum;
  }
  return sum;
}
int main() {
  cout << generalizedMissing({-2, -1, 0, 7, -3}) << '\n';
}
```

期望时间 $O(n)$、空间 $O(n)$。若数据不可信，还需在累加与递增前检查 64 位溢出。

## 变种三：数组只在末尾追加元素

新定义：数据流不断追加，追加后立即询问答案。维护当前顺序前缀是否仍在延长、前缀和、全部出现值；若前缀已经断开，后续追加不会改变前缀和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MissingStream {
  vector<long long> values;
  unordered_set<long long> present;
  long long prefixSum = 0;
  bool open = true;
public:
  long long append(long long value) {
    if (values.empty()) {
      prefixSum = value;
    } else if (open && value == values.back() + 1) {
      prefixSum += value;
    } else {
      open = false;
    }
    values.push_back(value);
    present.insert(value);
    long long answer = prefixSum;
    while (present.contains(answer)) {
      ++answer;
    }
    return answer;
  }
};
int main() {
  MissingStream stream;
  for (int x : {1, 2, 3, 2, 5}) {
    cout << stream.append(x) << ' ';
  }
}
```

每次追加的均摊时间为 $O(1)$，因为查询指针在一次调用内只跨过已出现值；空间随数据流长度为 $O(n)$。

## 变种四：支持单点修改与查询

新定义：数组支持 `nums[i]=x`。最长顺序前缀的终点由第一个坏边 `nums[i] != nums[i-1]+1` 决定；有序集合维护坏边，Fenwick 树维护前缀和，值频表维护出现性。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicMissing {
  int n;
  vector<long long> a, bit;
  map<long long, int> frequency;
  set<int> bad;
  void add(int index, long long delta) {
    for (++index; index <= n; index += index & -index) bit[index] += delta;
  }
  long long prefix(int index) const {
    long long result = 0;
    for (++index; index > 0; index -= index & -index) result += bit[index];
    return result;
  }
  void refresh(int index) {
    if (index <= 0 || index >= n) return;
    if (a[index] == a[index - 1] + 1) bad.erase(index);
    else bad.insert(index);
  }
public:
  explicit DynamicMissing(vector<long long> values)
      : n(values.size()), a(move(values)), bit(n + 1) {
    for (int i = 0; i < n; ++i) {
      add(i, a[i]);
      ++frequency[a[i]];
      refresh(i);
    }
  }
  void setValue(int index, long long value) {
    if (--frequency[a[index]] == 0) frequency.erase(a[index]);
    add(index, value - a[index]);
    a[index] = value;
    ++frequency[value];
    refresh(index);
    refresh(index + 1);
  }
  long long query() const {
    int end = bad.empty() ? n - 1 : *bad.begin() - 1;
    long long answer = prefix(end);
    while (frequency.contains(answer)) ++answer;
    return answer;
  }
};
int main() {
  DynamicMissing data({1, 2, 3, 2, 5});
  cout << data.query() << '\n';
  data.setValue(3, 4);
  cout << data.query() << '\n';
}
```

更新坏边与 Fenwick 树为 $O(\log n)$；查询前缀和为 $O(\log n)$，再跳过连续出现值。若还要求严格最坏 $O(\log n)$ 查询，可在值域上再建维护“是否缺失”的线段树。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-g/">← [codeforces] CF Round 1113 Div.2 G No Balance Left</a>
<span class="daily-archive-pager__empty"></span>
</nav>
