---
title: "[力扣 Top 41] LC 300 最长递增子序列 中等"
---

# [力扣 Top 41] LC 300 最长递增子序列 中等

<p class="daily-archive-kicker">2026-07-30 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../dp/sequence-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d48f81620f06ff48d81520a0eff87c57ce0674711ff4f73cc3630d0ec9a86079 -->
## 官方原始信息

- Top 排名：41
- 题号：LC 300
- 官方中文标题：最长递增子序列
- 官方难度：中等
- 官方链接：[最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/)

### 原始题意

给定整数数组 `nums`，求最长严格递增子序列的长度。子序列可以删除任意元素，但必须保留其余元素的相对顺序。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int lengthOfLIS(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：可以选择 [2,3,7,101]。
```

```text
输入：nums = [0,1,0,3,2,3]
输出：4
```

```text
输入：nums = [7,7,7,7,7,7,7]
输出：1
```

### 全部约束

- $1\le n\le2500$。
- $-10^4\le nums_i\le10^4$。
- “严格递增”要求相邻所选值满足小于，重复值不能接在彼此后面。
- 官方进阶要求达到 $O(n\log n)$。

## 约束推导与边界

$n=2500$ 排除了枚举全部 $2^n$ 个子序列，但允许 $O(n^2)$ 动态规划；进阶再利用“相同长度只需保留最小末尾值”降到 $O(n\log n)$。答案至多为 $n$，`int` 足够。

边界包括单元素、全相等、严格递减、严格递增以及含重复值的序列。空数组不在官方输入范围内，但实现自然返回 0。

## 解法递进

### 解法一：枚举选或不选

深搜每个位置的两种选择，并携带上一个被选值。它覆盖全部子序列，时间 $O(2^n)$、递归空间 $O(n)$，只适合作为小规模正确性 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const vector<int>& nums, int index, long long last) {
    if (index == static_cast<int>(nums.size())) {
      return 0;
    }
    int answer = search(nums, index + 1, last);
    if (nums[index] > last) {
      answer = max(answer, 1 + search(nums, index + 1, nums[index]));
    }
    return answer;
  }
public:
  int lengthOfLIS(vector<int>& nums) {
    return search(nums, 0, numeric_limits<long long>::min());
  }
};
```

### 解法二：以当前位置结尾的动态规划

令 `dp[i]` 为必须选择 `nums[i]` 时的最长长度。枚举所有 `j<i`，只在 `nums[j]<nums[i]` 时转移：

$$
dp_i=1+\max_{\substack{0\le j<i\\nums_j<nums_i}}dp_j.
$$

时间 $O(n^2)$，空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLIS(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 1);
    int answer = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < i; ++j) {
        if (nums[j] < nums[i]) {
          dp[i] = max(dp[i], dp[j] + 1);
        }
      }
      answer = max(answer, dp[i]);
    }
    return answer;
  }
};
```

### 最佳实用解：最小末尾值与二分

维护 `tails[len-1]`：当前扫描前缀中，长度为 `len` 的严格递增子序列能够达到的最小末尾值。处理 `x` 时，用 `lower_bound` 找第一个不小于 `x` 的位置并替换；若不存在则追加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int lengthOfLIS(vector<int>& nums) {
    vector<int> tails;
    for (int value : nums) {
      auto it = lower_bound(tails.begin(), tails.end(), value);
      if (it == tails.end()) {
        tails.push_back(value);
      } else {
        *it = value;
      }
    }
    return tails.size();
  }
};
```

时间复杂度 $O(n\log n)$，空间复杂度 $O(n)$。

## 正确性证明

不变量：扫描任意前缀后，`tails[k]` 是该前缀内所有长度为 $k+1$ 的严格递增子序列中最小的末尾值，并且 `tails` 严格递增。

处理 `x` 时，设 `p` 是第一个满足 `tails[p]\ge x` 的位置。若 $p>0$，`tails[p-1]<x`，所以存在长度为 $p$ 的子序列可接上 `x`，得到长度 $p+1$。把 `tails[p]` 换成更小或相等的 `x` 不会丢掉任何长度，只会给未来留下更宽松的接续条件。若 `p` 等于当前长度，则 `x` 能把最长长度增加 1。反之，若某个更长严格递增子序列已经存在，其末尾必会促使数组增长。因此最终长度恰为最长严格递增子序列长度。

## 样例手推

对 `[10,9,2,5,3,7,101,18]`，`tails` 依次为：

```text
[10]
[9]
[2]
[2,5]
[2,3]
[2,3,7]
[2,3,7,101]
[2,3,7,18]
```

最终长度为 4。注意 `tails` 只保存每种长度的最佳末尾，并不一定是原数组中的同一条最终答案。

## 易错点与方案比较

- 严格递增使用 `lower_bound`；非递减才使用 `upper_bound`。
- 不能把排序后的数组当作子序列，因为排序破坏原相对顺序。
- $O(n^2)$ DP 更容易恢复方案和解释；$O(n\log n)$ 是竞赛与进阶的首选。
- 替换 `tails` 中的元素不会减少已存在的长度，它只压低同长度的末尾。
- 推荐优先记忆“最小末尾值 + `lower_bound`”，同时保留 $O(n^2)$ DP 作为推导基线。

## 变种一：恢复一条最长递增子序列

新定义：不仅返回长度，还返回任意一条最长严格递增子序列。为每个位置记录前驱，并在 `tails` 中保存对应原下标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n), tails, tail_index, parent(n, -1);
  for (int& value : a) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    int p = lower_bound(tails.begin(), tails.end(), a[i]) - tails.begin();
    if (p > 0) {
      parent[i] = tail_index[p - 1];
    }
    if (p == static_cast<int>(tails.size())) {
      tails.push_back(a[i]);
      tail_index.push_back(i);
    } else {
      tails[p] = a[i];
      tail_index[p] = i;
    }
  }
  vector<int> answer;
  for (int i = tail_index.back(); i != -1; i = parent[i]) {
    answer.push_back(a[i]);
  }
  reverse(answer.begin(), answer.end());
  cout << answer.size() << '\n';
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\log n)$，空间 $O(n)$。

## 变种二：统计最长递增子序列的条数

新定义：返回最长长度对应的不同下标序列数量。令 `length[i]` 与 `count[i]` 分别表示以 `i` 结尾的最佳长度和方案数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n), length(n, 1);
  vector<long long> count(n, 1);
  for (int& value : a) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < i; ++j) {
      if (a[j] >= a[i]) {
        continue;
      }
      if (length[j] + 1 > length[i]) {
        length[i] = length[j] + 1;
        count[i] = count[j];
      } else if (length[j] + 1 == length[i]) {
        count[i] += count[j];
      }
    }
  }
  int best = *max_element(length.begin(), length.end());
  long long answer = 0;
  for (int i = 0; i < n; ++i) {
    if (length[i] == best) {
      answer += count[i];
    }
  }
  cout << best << ' ' << answer << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$。若方案数可能很大，应按题意取模或使用大整数。

## 变种三：最长非递减子序列

新定义：允许相邻所选值相等。唯一关键变化是让相等值接在已有序列后面，因此用 `upper_bound` 找第一个严格大于当前值的位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> tails;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    auto it = upper_bound(tails.begin(), tails.end(), value);
    if (it == tails.end()) {
      tails.push_back(value);
    } else {
      *it = value;
    }
  }
  cout << tails.size() << '\n';
}
```

时间 $O(n\log n)$，空间 $O(n)$。

## 变种四：在线追加并查询当前答案

新定义：数值按流式顺序逐个追加，每次追加后输出当前最长严格递增长度。顺序只向尾部增长，所以直接维护同一个 `tails` 即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<int> tails;
  while (q--) {
    int value;
    cin >> value;
    auto it = lower_bound(tails.begin(), tails.end(), value);
    if (it == tails.end()) {
      tails.push_back(value);
    } else {
      *it = value;
    }
    cout << tails.size() << '\n';
  }
}
```

每次追加 $O(\log n)$，总空间 $O(n)$。若允许修改历史位置，`tails` 不再可局部修补，需要更复杂的分块或线段树状态。

## 可复现验证

- 所有完整代码按 C++23 编译。
- 最优解覆盖三个官方样例及单元素、全相等、严格递减、严格递增边界。
- 小规模随机数组可把枚举解作为 oracle，与 $O(n^2)$ DP 和二分解逐项对拍。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/longest-increasing-subsequence/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/longest-increasing-subsequence/)
- [对应知识专题](../../dp/sequence-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc468-e/">← [atcoder] ABC468 E Sum of Average</a>
<a class="daily-archive-pager__next" href="../leetcode-top-42-lc124/">[力扣 Top 42] LC 124 二叉树中的最大路径和 困难 →</a>
</nav>
