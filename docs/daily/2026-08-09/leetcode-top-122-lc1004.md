---
title: "[力扣 Top 122] LC 1004 最大连续 1 的个数 III 中等"
---

# [力扣 Top 122] LC 1004 最大连续 1 的个数 III 中等

<p class="daily-archive-kicker">2026-08-09 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b152cdfda4dcd35c59873935e026a8c3e70d774a13b92cc9230499d2255717a2 -->
## 官方原始信息

- Top 排名：122
- 题号：LC 1004
- 官方中文标题：最大连续 1 的个数 III
- 官方难度：中等
- 官方链接：[最大连续 1 的个数 III](https://leetcode.cn/problems/max-consecutive-ones-iii/)

### 原始题意与函数签名

给定二进制数组 `nums` 和整数 `k`，最多把 `k` 个 0 改成 1，返回可得到的最长连续 1 子数组长度。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int longestOnes(vector<int>& nums, int k);
};
```

### 全部官方样例

```text
输入：nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
输出：6
解释：[0,0,1,1,1,1] 中翻转两个 0，可得到 6 个连续 1。
```

```text
输入：nums = [0,0,1,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1], k = 3
输出：10
```

### 全部约束

- $1\le n\le10^5$。
- `nums[i]` 只可能是 0 或 1。
- $0\le k\le n$。

## 约束推导与观察

选择一个连续区间后，最少翻转次数就是其中 0 的个数。因此问题等价为：求“0 的数量不超过 $k$”的最长子数组。右端点右移只会让零数不减；一旦超预算，左端点只需单调右移，这正是滑动窗口的适用条件。

## 解法递进

### 解法一：枚举所有左端点并向右扩展

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestOnes(vector<int>& nums, int k) {
    int answer = 0;
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      int zeros = 0;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        zeros += nums[right] == 0;
        if (zeros > k) {
          break;
        }
        answer = max(answer, right - left + 1);
      }
    }
    return answer;
  }
};
```

时间 $O(n^2)$、空间 $O(1)$，枚举了全部可行区间，是正确的小规模 oracle。

### 解法二：前缀零数加二分

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestOnes(vector<int>& nums, int k) {
    int n = nums.size();
    vector<int> prefix(n + 1);
    for (int i = 0; i < n; ++i) {
      prefix[i + 1] = prefix[i] + (nums[i] == 0);
    }
    int answer = 0;
    for (int right = 1; right <= n; ++right) {
      int need = prefix[right] - k;
      int left = lower_bound(prefix.begin(), prefix.begin() + right + 1, need) - prefix.begin();
      answer = max(answer, right - left);
    }
    return answer;
  }
};
```

前缀零数单调，二分最早合法左端点。时间 $O(n\log n)$、空间 $O(n)$。

### 最佳实用解：可变长滑动窗口

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestOnes(vector<int>& nums, int k) {
    int left = 0;
    int zeros = 0;
    int answer = 0;
    for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
      zeros += nums[right] == 0;
      while (zeros > k) {
        zeros -= nums[left] == 0;
        ++left;
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
```

时间 $O(n)$、空间 $O(1)$。每个元素最多进窗、出窗各一次，是面试和竞赛中最稳定的写法。

## 正确性证明

收缩循环结束后，窗口 `[left,right]` 至多含 $k$ 个零，因此可通过至多 $k$ 次翻转变成全 1。并且 `left` 是当前右端点下尚未被必要收缩越过的最小合法左端点：任何更小左端点若在本轮被移除，都曾令零数超过 $k$，之后右端点只会右移，不会重新合法。因此该窗口是固定 `right` 的最长合法窗口。枚举所有右端点并取最大值，得到全局最优。

## 样例手推

样例 1 扩到第三个连续 0 时零数变为 3，左端点越过第一个 0 后恢复为 2。继续扩到末尾 0 时再次收缩，最大合法窗口长度在 `[5,10]` 处达到 6。若 `k=0`，算法退化为普通最长连续 1；若 `k=n`，整个数组始终合法。

## 易错点与方案比较

- 条件是“最多 $k$ 个零”，应在 `zeros > k` 时收缩，而不是等于时收缩。
- 用 `while` 而非 `if`，因为一次加入可能需要越过多个前导 1 才移走一个零。
- 返回窗口长度，不是实际翻转次数。
- 前缀二分正确但多一个对数和数组；滑动窗口直接利用单调性，优先记忆。

## 变种一：翻转每个零的代价不同

新定义：位置 `i` 的 0 翻转代价为非负 `cost[i]`，总预算为 `budget`。窗口代价仍随右移单调不减，维护代价和即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int longestWeighted(const vector<int>& nums, const vector<int>& cost, long long budget) {
  int left = 0;
  int answer = 0;
  long long used = 0;
  for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
    if (nums[right] == 0) {
      used += cost[right];
    }
    while (used > budget) {
      if (nums[left] == 0) {
        used -= cost[left];
      }
      ++left;
    }
    answer = max(answer, right - left + 1);
  }
  return answer;
}
int main() {
  cout << longestWeighted({1, 0, 1, 0}, {0, 3, 0, 1}, 3) << '\n';
}
```

时间 $O(n)$、空间 $O(1)$。代价若允许为负，单调性消失，不能直接套窗口。

## 变种二：必须恰好翻转 `k` 个零

新定义：区间必须含恰好 $k$ 个零。窗口保持至多 $k$ 个零；只有零数等于 $k$ 时更新答案。对 $k=0$ 同样成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int longestExactlyKZeros(const vector<int>& nums, int k) {
  int left = 0;
  int zeros = 0;
  int answer = -1;
  for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
    zeros += nums[right] == 0;
    while (zeros > k) {
      zeros -= nums[left++] == 0;
    }
    if (zeros == k) {
      answer = max(answer, right - left + 1);
    }
  }
  return answer;
}
int main() {
  cout << longestExactlyKZeros({1, 0, 1, 0, 1}, 1) << '\n';
}
```

时间 $O(n)$、空间 $O(1)$；返回 `-1` 表示不存在恰含 $k$ 个零的区间。

## 变种三：数据流持续追加

新定义：二进制位逐个到达，每次追加后返回当前最长答案。保存窗口内容与零位置即可在线处理。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OnlineLongestOnes {
  int k;
  int index = -1;
  int left = 0;
  int answer = 0;
  deque<int> zeroPositions;
public:
  explicit OnlineLongestOnes(int limit) : k(limit) {
  }
  int append(int bit) {
    ++index;
    if (bit == 0) {
      zeroPositions.push_back(index);
    }
    if (static_cast<int>(zeroPositions.size()) > k) {
      left = zeroPositions.front() + 1;
      zeroPositions.pop_front();
    }
    answer = max(answer, index - left + 1);
    return answer;
  }
};
int main() {
  OnlineLongestOnes tracker(1);
  for (int x : {1, 0, 1, 0}) {
    cout << tracker.append(x) << ' ';
  }
}
```

每次追加摊还 $O(1)$，空间 $O(k)$。

## 变种四：多次询问不同的 `k`

新定义：同一静态数组有多次独立预算询问。单个窗口状态不能同时复用到任意 `k`；为每个询问各跑一次线性扫描。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> answerBudgets(const vector<int>& nums, const vector<int>& queries) {
  vector<int> answers;
  for (int k : queries) {
    int left = 0;
    int zeros = 0;
    int best = 0;
    for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
      zeros += nums[right] == 0;
      while (zeros > k) {
        zeros -= nums[left++] == 0;
      }
      best = max(best, right - left + 1);
    }
    answers.push_back(best);
  }
  return answers;
}
int main() {
  for (int x : answerBudgets({1, 0, 0, 1}, {0, 1, 2})) {
    cout << x << ' ';
  }
}
```

若询问数为 $q$，时间 $O(nq)$、额外空间 $O(q)$；它明确说明原算法能复用代码但不能共享单一窗口状态。

## 可复现验证

枚举长度不超过 12 的所有二进制数组和全部 $0\le k\le n$，以区间枚举统计零数为 oracle，对比前缀二分与滑动窗口；另覆盖全 0、全 1、`k=0`、`k=n`。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/max-consecutive-ones-iii/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-121-lc238/">← [力扣 Top 121] LC 238 除了自身以外数组的乘积 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-123-lc39/">[力扣 Top 123] LC 39 组合总和 中等 →</a>
</nav>
