---
title: "[力扣 Top 35] LC 53 最大子数组和 中等"
---

# [力扣 Top 35] LC 53 最大子数组和 中等

<p class="daily-archive-kicker">2026-07-29 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../dp/linear-recurrences.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：35
- 题号：LC 53
- 官方中文标题：最大子数组和
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/maximum-subarray/>

### 原始题意

给定整数数组 `nums`，求至少包含一个元素的连续子数组的最大元素和。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maxSubArray(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：[4,-1,2,1] 的和为 6
```

```text
输入：nums = [1]
输出：1
```

```text
输入：nums = [5,4,-1,7,8]
输出：23
```

### 全部约束

- $1\le |nums|\le10^5$。
- $-10^4\le nums_i\le10^4$。
- 最坏绝对和不超过 $10^9$，32 位有符号整数可承接；通用模板可使用 64 位。

## 最优结论

令 `ending` 为必须以当前位置结尾的最大子数组和。新元素到来时，最优子数组要么接在此前最优结尾后面，要么从当前位置重新开始：

$$
ending_i=\max(nums_i,ending_{i-1}+nums_i).
$$

扫描中维护所有 `ending` 的最大值。时间 $O(n)$，额外空间 $O(1)$。这是面试与竞赛最应优先记忆的 Kadane 算法。

## 约束与观察

至少选一个元素意味着全负数组不能返回 0；初值必须取 `nums[0]`。一旦此前结尾和为负，它只会拖累任何从当前位置继续的子数组，因此可以丢弃。

## 解法递进

### 解法一：枚举左右端点

固定左端点并逐步累加右端点，消除重复求和后为 $O(n^2)$ 时间、$O(1)$ 空间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxSubArray(vector<int>& nums) {
    int answer = nums[0];
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      int sum = 0;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        sum += nums[right];
        answer = max(answer, sum);
      }
    }
    return answer;
  }
};
```

### 解法二：一维 DP

保存每个位置的 `ending`，时间 $O(n)$、空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxSubArray(vector<int>& nums) {
    vector<int> dp(nums.size());
    dp[0] = nums[0];
    int answer = dp[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      dp[i] = max(nums[i], dp[i - 1] + nums[i]);
      answer = max(answer, dp[i]);
    }
    return answer;
  }
};
```

### 解法三：Kadane 滚动状态

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxSubArray(vector<int>& nums) {
    int ending = nums[0];
    int answer = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      ending = max(nums[i], ending + nums[i]);
      answer = max(answer, ending);
    }
    return answer;
  }
};
```

### 同类可合并方案：分治四元组

每个区间维护总和、最大前缀、最大后缀与最大子段和，可以在线段树中结合。静态单次查询虽也是 $O(n)$，常数与证明负担都高于 Kadane；但它能自然扩展到动态查询。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  struct Node {
    int sum;
    int prefix;
    int suffix;
    int best;
  };
  Node merge(const Node& a, const Node& b) {
    return {a.sum + b.sum, max(a.prefix, a.sum + b.prefix), max(b.suffix, b.sum + a.suffix),
        max({a.best, b.best, a.suffix + b.prefix})};
  }
  Node solve(const vector<int>& nums, int left, int right) {
    if (right - left == 1) {
      int value = nums[left];
      return {value, value, value, value};
    }
    int middle = (left + right) / 2;
    return merge(solve(nums, left, middle), solve(nums, middle, right));
  }
public:
  int maxSubArray(vector<int>& nums) {
    return solve(nums, 0, static_cast<int>(nums.size())).best;
  }
};
```

## 正确性证明

归纳证明状态：处理到下标 `i` 时，`ending` 是所有以 `i` 结尾的非空子数组中的最大和。

任一以 `i` 结尾的子数组，要么只含 `nums[i]`，要么由某个以 `i-1` 结尾的子数组追加 `nums[i]`。追加情况下选择最大的前一结尾和最优，因此转移恰好覆盖且不遗漏。所有非空子数组都有唯一右端点，取所有 `ending` 的最大值即全局答案。

## 样例手推

对 `[-2,1,-3,4,-1,2,1,-5,4]`，`ending` 依次为 `-2,1,-2,4,3,5,6,1,5`，全局最大值在下标 6 达到 6。

## 易错点

- 不能把答案初始化为 0，否则全负数组错误。
- 子数组必须连续，不能跳过中间负数后仍视为同一段。
- 若要求恢复区间，应在“重新开始”时更新左端点。
- 动态修改场景不能只保存一个 Kadane 值。

## 验证说明

以 $O(n^2)$ 枚举为 oracle，对随机正负数组、全负、全正、单元素和零值数组对拍。

## Follow-up 与变种

### 变种一：返回最大和区间

当 `ending + nums[i] < nums[i]` 时从 `i` 重启，并记录候选左端点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  tuple<long long, int, int> maximumSubarray(const vector<int>& nums) {
    long long ending = nums[0];
    long long best = nums[0];
    int candidateLeft = 0;
    int bestLeft = 0;
    int bestRight = 0;
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      if (ending < 0) {
        ending = nums[i];
        candidateLeft = i;
      } else {
        ending += nums[i];
      }
      if (ending > best) {
        best = ending;
        bestLeft = candidateLeft;
        bestRight = i;
      }
    }
    return {best, bestLeft, bestRight};
  }
};
```

### 变种二：环形最大子数组

答案要么不跨边界，用普通 Kadane；要么跨边界，等于总和减去最小子数组和。全负数组不能选择空补集。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxSubarraySumCircular(vector<int>& nums) {
    int total = nums[0];
    int maxEnding = nums[0];
    int maxAnswer = nums[0];
    int minEnding = nums[0];
    int minAnswer = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      total += nums[i];
      maxEnding = max(nums[i], maxEnding + nums[i]);
      maxAnswer = max(maxAnswer, maxEnding);
      minEnding = min(nums[i], minEnding + nums[i]);
      minAnswer = min(minAnswer, minEnding);
    }
    if (maxAnswer < 0) {
      return maxAnswer;
    }
    return max(maxAnswer, total - minAnswer);
  }
};
```

### 变种三：单点修改后查询最大子数组和

线段树维护四元组，每次修改和查询均为 $O(\log n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MaxSubarrayTree {
  struct Node {
    long long sum;
    long long prefix;
    long long suffix;
    long long best;
  };
  int size = 1;
  vector<Node> tree;
  Node merge(const Node& a, const Node& b) {
    return {a.sum + b.sum, max(a.prefix, a.sum + b.prefix), max(b.suffix, b.sum + a.suffix),
        max({a.best, b.best, a.suffix + b.prefix})};
  }
public:
  explicit MaxSubarrayTree(const vector<int>& values) {
    while (size < static_cast<int>(values.size())) {
      size <<= 1;
    }
    const long long neg = numeric_limits<long long>::min() / 4;
    tree.assign(2 * size, Node{0, neg, neg, neg});
    for (int i = 0; i < static_cast<int>(values.size()); ++i) {
      tree[size + i] = {values[i], values[i], values[i], values[i]};
    }
    for (int node = size - 1; node >= 1; --node) {
      tree[node] = merge(tree[2 * node], tree[2 * node + 1]);
    }
  }
  void update(int index, int value) {
    int node = size + index;
    tree[node] = {value, value, value, value};
    for (node /= 2; node >= 1; node /= 2) {
      tree[node] = merge(tree[2 * node], tree[2 * node + 1]);
      if (node == 1) {
        break;
      }
    }
  }
  long long query() const {
    return tree[1].best;
  }
};
```

### 变种四：最大乘积子数组

负数会交换最大与最小角色，因此同时维护以当前位置结尾的最大积和最小积。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    long long maximum = nums[0];
    long long minimum = nums[0];
    long long answer = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      long long value = nums[i];
      long long oldMaximum = maximum;
      maximum = max({value, maximum * value, minimum * value});
      minimum = min({value, oldMaximum * value, minimum * value});
      answer = max(answer, maximum);
    }
    return static_cast<int>(answer);
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/maximum-subarray/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/maximum-subarray/)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-34-lc9.md">← [力扣 Top 34] LC 9 回文数 简单</a>
<a class="daily-archive-pager__next" href="leetcode-top-36-lc198.md">[力扣 Top 36] LC 198 打家劫舍 中等 →</a>
</nav>
