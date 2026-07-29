---
title: "[力扣 Top 12] LC 560 和为 K 的子数组 中等"
---

# [力扣 Top 12] LC 560 和为 K 的子数组 中等

<p class="daily-archive-kicker">2026-07-27 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

官方题目：[打开官方题面](https://leetcode.cn/problems/subarray-sum-equals-k/)

## 官方原始信息

- 题号：560
- 官方中文标题：和为 K 的子数组
- 官方英文标题：Subarray Sum Equals K
- slug：`subarray-sum-equals-k`
- 官方难度：中等
- 函数签名：`int subarraySum(vector<int>& nums, int k)`
- 官方竞赛归属与分值：未发现官方竞赛归属，官方分值未知
- ZeroTracer 社区估算竞赛分：无。2026-07-27 检索公开 `data.json`，该 slug 不在数据集中

### 原始题意

给定整数数组 `nums` 与整数 `k`，统计元素和恰好为 `k` 的连续非空子数组个数。不同起止下标视为不同子数组。

### 全部官方样例

1. `nums = [1,1,1], k = 2`，输出 `2`；两个长度为 2 的区间均满足。
2. `nums = [1,2,3], k = 3`，输出 `2`；区间 `[1,2]` 与单元素区间 `[3]` 满足。

### 全部官方约束

- $1\le nums.length\le2\times10^4$
- $-1000\le nums[i]\le1000$
- $-10^7\le k\le10^7$

## 约束推导、样例与边界

数组含负数、零和正数，区间和随右端扩展不单调，普通滑动窗口不能安全移动左端。设前缀和

$$
P[0]=0,\qquad P[i+1]=P[i]+nums[i].
$$

区间 $[l,r]$ 的和为 $P[r+1]-P[l]$，等于 $k$ 当且仅当 $P[l]=P[r+1]-k$。扫描到某个右前缀时，只需知道此前目标前缀出现了多少次。

样例 1 的前缀依次为 0、1、2、3。到前缀 2 时查找 0，得到区间 `[0,1]`；到前缀 3 时查找 1，得到 `[1,2]`，总数 2。

边界：

- 单元素等于 `k` 时应计数一次，这依赖初始频次 `freq[0] = 1`。
- `k = 0` 且有重复前缀和时，同一个当前前缀可能对应多个左端，必须累加频次而非只存存在性。
- 全零数组、`k=0` 时答案为 $n(n+1)/2$；在本题 $n\le2\times10^4$ 下不超过 `int`，但通用版本宜用 `long long` 累加。
- 前缀和绝对值至多 $2\times10^7$，`int` 可容纳；代码使用 `long long` 便于推广。
- 子数组必须连续且非空；先查询再插入当前前缀，可避免把空区间计入 `k=0`。

## 解法一：枚举区间并重新求和

枚举所有 `(l,r)`，再逐项计算该区间和。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int subarraySum(vector<int>& nums, int k) {
    int n = nums.size(), ans = 0;
    for (int l = 0; l < n; ++l) {
      for (int r = l; r < n; ++r) {
        long long sum = 0;
        for (int i = l; i <= r; ++i) sum += nums[i];
        if (sum == k) ++ans;
      }
    }
    return ans;
  }
};
```

时间 $O(n^3)$，空间 $O(1)$。瓶颈是相邻区间重复累加了绝大多数元素。

## 解法二：前缀和枚举所有区间

预处理前缀和后，每个区间和可 $O(1)$ 获得。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int subarraySum(vector<int>& nums, int k) {
    int n = nums.size(), ans = 0;
    vector<long long> prefix(n + 1);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + nums[i];
    for (int l = 0; l < n; ++l) {
      for (int r = l; r < n; ++r) {
        if (prefix[r + 1] - prefix[l] == k) ++ans;
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间 $O(n)$。它消除了区间内部的重复加法，但仍显式枚举全部下标对；$n=2\times10^4$ 时约两亿对，过于勉强。

## 解法三：前缀和频次哈希（最佳实用解）

扫描当前前缀 `prefix` 前，哈希表保存所有更早前缀值的出现次数。所有值为 `prefix - k` 的旧前缀都对应一个以当前位置结束的合法子数组。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int subarraySum(vector<int>& nums, int k) {
    unordered_map<long long, int> freq;
    freq.reserve(nums.size() * 2 + 1);
    freq[0] = 1;
    long long prefix = 0;
    int ans = 0;
    for (int x : nums) {
      prefix += x;
      auto it = freq.find(prefix - k);
      if (it != freq.end()) ans += it->second;
      ++freq[prefix];
    }
    return ans;
  }
};
```

### 正确性证明

循环不变量：处理当前元素前，`freq[s]` 等于所有已扫描前缀中前缀和为 $s$ 的个数，且不含当前右边界对应的前缀。加入 `nums[r]` 后得到 $P[r+1]$。对每个旧前缀 $P[l]=P[r+1]-k$，区间 $[l,r]$ 的和恰为 $k$；反之，每个以 `r` 结尾的合法子数组都有唯一左边界 `l`，必对应表中的一次出现。因此加上 `freq[prefix-k]` 恰好计入所有且仅有的新合法区间。随后插入当前前缀，保持不变量供未来使用。

期望时间 $O(n)$，空间 $O(n)$；`unordered_map` 的理论最坏时间可能退化，若需确定性界可改用 `map` 得到 $O(n\log n)$。面试优先记忆“当前前缀减目标 = 所需历史前缀”的等式和先查后插顺序。

## 同阶方案比较与常见错误

- 哈希表：期望 $O(n)$，常数低，适合单次统计。
- 有序映射：$O(n\log n)$，最坏界稳定，且可扩展到前缀值范围查询。
- 对所有前缀离散化后用频次数组也可 $O(n\log n)$ 预处理、$O(n)$ 扫描，但这里只做精确值查找，哈希更直接。

常见错误：

- 使用普通滑动窗口；负数会破坏单调性，例如右扩后和反而减小。
- 忘记 `freq[0] = 1`，漏掉从下标 0 开始的区间。
- 只用 `set` 存前缀，丢失重复前缀对应的多个答案。
- 先插入当前前缀再查询，使 `k=0` 时错误计入空区间。
- 把“子数组”当成任意子序列。

## Follow-up 1：恢复一个和为 $k$ 的区间

### 新定义与变化

返回任意一组 `[l,r]`，不存在则返回空。计数需要频次；恢复一组只需为每个前缀和保存一个历史下标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findSubarray(vector<int>& nums, long long k) {
    unordered_map<long long, int> first;
    first[0] = -1;
    long long prefix = 0;
    for (int r = 0; r < static_cast<int>(nums.size()); ++r) {
      prefix += nums[r];
      auto it = first.find(prefix - k);
      if (it != first.end()) return {it->second + 1, r};
      if (!first.count(prefix)) first[prefix] = r;
    }
    return {};
  }
};
```

期望时间 $O(n)$，空间 $O(n)$。若要求最长区间，保留每个前缀最早下标并遍历全部右端更新最大长度；若要求最短则需保留最新下标。

## Follow-up 2：数组元素保证非负

### 新定义与变化

当 `nums[i] >= 0` 时，窗口和对右扩单调不减。精确等于 $k$ 的区间数可写成“和至多 $k$ 的区间数减去和至多 $k-1$ 的区间数”，自然处理零造成的多个左端。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long atMost(const vector<int>& nums, long long limit) {
    if (limit < 0) return 0;
    long long sum = 0, ans = 0;
    int left = 0;
    for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
      sum += nums[right];
      while (sum > limit) sum -= nums[left++];
      ans += right - left + 1;
    }
    return ans;
  }
public:
  long long subarraySumNonnegative(vector<int>& nums, int k) {
    return atMost(nums, k) - atMost(nums, static_cast<long long>(k) - 1);
  }
};
```

时间 $O(n)$，空间 $O(1)$。原题允许负数，所以这一优化不能反向套回原题。

## Follow-up 3：数据流逐个追加，固定 $k$

### 新定义与变化

每次 `add(x)` 后返回截至目前的累计合法子数组数。前缀频次本来就是在线状态，无需保存整个数组。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class SubarraySumStream {
  long long k, prefix = 0, answer = 0;
  unordered_map<long long, long long> freq;
public:
  explicit SubarraySumStream(long long target) : k(target) {
    freq[0] = 1;
  }
  long long add(int x) {
    prefix += x;
    auto it = freq.find(prefix - k);
    if (it != freq.end()) answer += it->second;
    ++freq[prefix];
    return answer;
  }
};
```

每次期望 $O(1)$，存储 $O(t)$ 个不同前缀值。若还要删除流的最旧元素形成滑动时间窗，历史前缀的有效范围会变化，需要队列与频次删除，且统计口径必须重新定义。

## Follow-up 4：同一数组上大量不同 $k$ 查询

### 新定义与变化

若查询数很多且 $n$ 较小，可以一次枚举所有子数组和，建立“和到出现次数”的索引；之后每个目标 $k$ 为 $O(1)$ 期望查询。原单次 $O(n)$ 算法对每个新 `k` 都要重扫。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class SubarraySumIndex {
  unordered_map<long long, long long> count;
public:
  explicit SubarraySumIndex(const vector<int>& nums) {
    count.reserve(nums.size() * nums.size() / 2 + 1);
    for (int l = 0; l < static_cast<int>(nums.size()); ++l) {
      long long sum = 0;
      for (int r = l; r < static_cast<int>(nums.size()); ++r) {
        sum += nums[r];
        ++count[sum];
      }
    }
  }
  long long query(long long k) const {
    auto it = count.find(k);
    return it == count.end() ? 0 : it->second;
  }
};
```

预处理时间 $O(n^2)$，最坏空间 $O(n^2)$，单次查询期望 $O(1)$。对原题 $n=2\times10^4$ 不适用；只有在 $n$ 小、查询极多时才值得交换成本。

## Follow-up 5：二维矩阵中和为目标的子矩阵（LC 1074）

### 新定义与变化

连续区间扩展为连续行列构成的矩形。固定上下边界后，把各列在这两行之间的和压成一维数组，再复用前缀频次算法。为降低平方维度，必要时先转置，使枚举的是较短维。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numSubmatrixSumTarget(vector<vector<int>>& matrix, int target) {
    int m = matrix.size(), n = matrix[0].size();
    if (m > n) {
      vector<vector<int>> transposed(n, vector<int>(m));
      for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) transposed[j][i] = matrix[i][j];
      }
      matrix.swap(transposed);
      swap(m, n);
    }
    int ans = 0;
    vector<long long> col(n);
    for (int top = 0; top < m; ++top) {
      fill(col.begin(), col.end(), 0);
      for (int bottom = top; bottom < m; ++bottom) {
        for (int c = 0; c < n; ++c) col[c] += matrix[bottom][c];
        unordered_map<long long, int> freq;
        freq[0] = 1;
        long long prefix = 0;
        for (long long x : col) {
          prefix += x;
          auto it = freq.find(prefix - target);
          if (it != freq.end()) ans += it->second;
          ++freq[prefix];
        }
      }
    }
    return ans;
  }
};
```

令短边为 $s$、长边为 $t$，期望时间 $O(s^2t)$，空间 $O(t)$。对应官方题：[LC 1074 元素和为目标值的子矩阵数量](https://leetcode.cn/problems/number-of-submatrices-that-sum-to-target/)。

## 可复现验证

- 官方元数据、两组样例与全部约束通过力扣中国 GraphQL `question(titleSlug: "subarray-sum-equals-k")` 于 2026-07-27 核对。
- ZeroTracer `data.json` 同日检索无此 slug。
- 最优哈希方案以短数组、随机正负值和随机 `k` 对比 $O(n^2)$ 前缀枚举；二维变种以小矩阵四边界枚举作 oracle。
- 所有代码块应以 C++23 独立编译。

## Reference

- [力扣中国 LC 560 官方题面](https://leetcode.cn/problems/subarray-sum-equals-k/)
- [力扣中国 LC 1074 官方题面](https://leetcode.cn/problems/number-of-submatrices-that-sum-to-target/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/subarray-sum-equals-k/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-11-lc2/">← [力扣 Top 11] LC 2 两数相加 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-13-lc200/">[力扣 Top 13] LC 200 岛屿数量 中等 →</a>
</nav>
