---
title: "[力扣 Top 38] LC 46 全排列 中等"
---

# [力扣 Top 38] LC 46 全排列 中等

<p class="daily-archive-kicker">2026-07-29 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../search/backtracking.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：38
- 题号：LC 46
- 官方中文标题：全排列
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/permutations/>

### 原始题意

给定一个元素互不相同的整数数组 `nums`，返回其所有可能的排列。排列的输出顺序任意。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> permute(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

```text
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

```text
输入：nums = [1]
输出：[[1]]
```

### 全部约束

- $1\le |nums|\le6$。
- $-10\le nums_i\le10$。
- `nums` 中所有整数互不相同。
- 输出本身包含 $n!$ 个长度为 $n$ 的排列，因此任何完整输出算法都需要 $\Omega(n\cdot n!)$ 时间与输出空间。

## 最优结论

回溯树的第 `position` 层决定排列的第 `position` 个元素。将尚未使用的元素逐个交换到当前位置，递归处理后再交换回来。每个合法前缀只生成一次，不产生需要过滤的重复状态。

时间 $O(n\cdot n!)$，递归栈 $O(n)$；若不计返回结果，只需原地数组和递归栈。该复杂度已经达到输出下界。

## 约束与观察

- “元素互不相同”意味着无需同层去重。
- 不能只给复杂度写成 $O(n!)$：复制每个长度为 $n$ 的答案也需要 $O(n)$。
- 暴力生成所有长度为 $n$ 的序列会有 $n^n$ 个候选，其中绝大多数重复使用元素。
- 回溯的核心不是模板，而是维护不变量：前缀已经确定，后缀恰好保存仍可选择的元素。

## 解法递进

### 解法一：生成所有长度为 `n` 的序列后过滤

每个位置都从 `n` 个元素中选择，最后检查是否恰好各用一次。覆盖全部排列，但遍历 $n^n$ 个候选，时间 $O(n^{n+1})$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer_;
  vector<int> path_;
  void generate(const vector<int>& nums, int length) {
    if (static_cast<int>(path_.size()) == length) {
      set<int> distinct(path_.begin(), path_.end());
      if (static_cast<int>(distinct.size()) == length) {
        answer_.push_back(path_);
      }
      return;
    }
    for (int value : nums) {
      path_.push_back(value);
      generate(nums, length);
      path_.pop_back();
    }
  }
public:
  vector<vector<int>> permute(vector<int>& nums) {
    answer_.clear();
    path_.clear();
    generate(nums, nums.size());
    return answer_;
  }
};
```

### 解法二：使用标记数组剪掉非法前缀

在选择时阻止重复使用元素，只访问合法排列树。时间 $O(n\cdot n!)$，额外空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer_;
  vector<int> path_;
  vector<bool> used_;
  void search(const vector<int>& nums) {
    if (path_.size() == nums.size()) {
      answer_.push_back(path_);
      return;
    }
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (used_[i]) {
        continue;
      }
      used_[i] = true;
      path_.push_back(nums[i]);
      search(nums);
      path_.pop_back();
      used_[i] = false;
    }
  }
public:
  vector<vector<int>> permute(vector<int>& nums) {
    answer_.clear();
    path_.clear();
    used_.assign(nums.size(), false);
    search(nums);
    return answer_;
  }
};
```

### 解法三：原地交换回溯

数组区间 `[0,position)` 是已确定前缀，`[position,n)` 是尚未使用元素。交换可同时完成“选择”和“使用标记”。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer_;
  void search(vector<int>& nums, int position) {
    if (position == static_cast<int>(nums.size())) {
      answer_.push_back(nums);
      return;
    }
    for (int i = position; i < static_cast<int>(nums.size()); ++i) {
      swap(nums[position], nums[i]);
      search(nums, position + 1);
      swap(nums[position], nums[i]);
    }
  }
public:
  vector<vector<int>> permute(vector<int>& nums) {
    answer_.clear();
    search(nums, 0);
    return answer_;
  }
};
```

### 解法四：按字典序迭代

排序后反复调用 `next_permutation` 也会恰好访问每个排列一次，时间同为 $O(n\cdot n!)$。它适合需要字典序输出的场景，但不如回溯容易附加约束。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> permute(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> answer;
    do {
      answer.push_back(nums);
    } while (next_permutation(nums.begin(), nums.end()));
    return answer;
  }
};
```

## 正确性证明

对交换回溯按 `position` 归纳。进入一层时，前缀 `[0,position)` 已固定，后缀包含且仅包含尚未使用的元素。循环把后缀中的每个元素恰好一次交换到 `position`，所以覆盖当前位置的所有可能选择；递归根据归纳假设生成该前缀下的全部后缀排列。不同循环分支在当前位置取值不同，彼此不重叠。回溯交换恢复进入本层时的状态，因此不会污染其他分支。最终每个排列恰好产生一次。

## 样例手推

`[1,2,3]` 的第一层依次把 1、2、3 放到位置 0。以首位 1 为例，第二层依次保留 2 或交换入 3，得到 `[1,2,3]`、`[1,3,2]`；另外两棵子树同理各产生两个排列，共 $3!=6$ 个。

## 易错点

- 递归返回后必须交换恢复，否则后续分支不再基于同一候选集合。
- 结果数组应复制当前排列，不能保存指向同一可变容器的引用。
- 若输入允许重复值，当前交换写法会产生重复答案。
- `next_permutation` 方案必须先排序，否则只能枚举当前排列之后的字典序后缀。

## 验证说明

对 $n=1\ldots8$ 的随机互异数组，将四种方法的结果分别排序去重后比较；检查答案数为 $n!$、每个答案长度为 $n$ 且元素多重集与输入相同。

## Follow-up 与变种

### 变种一：输入可能含重复元素

先排序；同一递归层中，相同值只能作为当前位置的第一个未使用候选。时间仍由不同排列数 $U$ 决定，为 $O(nU)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer_;
  vector<int> path_;
  vector<bool> used_;
  void search(const vector<int>& nums) {
    if (path_.size() == nums.size()) {
      answer_.push_back(path_);
      return;
    }
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (used_[i]) {
        continue;
      }
      if (i > 0 && nums[i] == nums[i - 1] && !used_[i - 1]) {
        continue;
      }
      used_[i] = true;
      path_.push_back(nums[i]);
      search(nums);
      path_.pop_back();
      used_[i] = false;
    }
  }
public:
  vector<vector<int>> permuteUnique(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    answer_.clear();
    path_.clear();
    used_.assign(nums.size(), false);
    search(nums);
    return answer_;
  }
};
```

### 变种二：求 `[1,n]` 的第 `k` 个字典序排列

第一个元素的每个候选都对应 $(n-1)!$ 个连续排列，可直接跳过整块。设 $1\le n\le20$、$1\le k\le n!$，时间 $O(n^2)$、空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> kthPermutation(int n, long long k) {
    vector<long long> factorial(n + 1, 1);
    for (int i = 1; i <= n; ++i) {
      factorial[i] = factorial[i - 1] * i;
    }
    vector<int> available(n);
    iota(available.begin(), available.end(), 1);
    vector<int> answer;
    --k;
    for (int remaining = n; remaining >= 1; --remaining) {
      long long block = factorial[remaining - 1];
      int index = static_cast<int>(k / block);
      k %= block;
      answer.push_back(available[index]);
      available.erase(available.begin() + index);
    }
    return answer;
  }
};
```

### 变种三：求一个排列的字典序排名

当前位置之前仍未使用且比当前值小的元素数，乘以后缀阶乘，即为该位置跳过的整块数量。$1\le n\le20$ 时，时间 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long permutationRank(const vector<int>& permutation) {
    int n = static_cast<int>(permutation.size());
    vector<long long> factorial(n + 1, 1);
    for (int i = 1; i <= n; ++i) {
      factorial[i] = factorial[i - 1] * i;
    }
    vector<int> available = permutation;
    sort(available.begin(), available.end());
    long long rank = 1;
    for (int i = 0; i < n; ++i) {
      auto it = lower_bound(available.begin(), available.end(), permutation[i]);
      long long smaller = it - available.begin();
      rank += smaller * factorial[n - i - 1];
      available.erase(it);
    }
    return rank;
  }
};
```

### 变种四：只生成没有任何元素留在原位置的错排

在第 `position` 层跳过原下标也是 `position` 的元素。仍为回溯，时间与实际搜索树规模成正比，最坏 $O(n\cdot n!)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer_;
  vector<int> path_;
  vector<bool> used_;
  void search(int n) {
    int position = static_cast<int>(path_.size());
    if (position == n) {
      answer_.push_back(path_);
      return;
    }
    for (int value = 0; value < n; ++value) {
      if (used_[value] || value == position) {
        continue;
      }
      used_[value] = true;
      path_.push_back(value);
      search(n);
      path_.pop_back();
      used_[value] = false;
    }
  }
public:
  vector<vector<int>> derangements(int n) {
    answer_.clear();
    path_.clear();
    used_.assign(n, false);
    search(n);
    return answer_;
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/permutations/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/permutations/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-37-lc438.md">← [力扣 Top 37] LC 438 找到字符串中所有字母异位词 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-39-lc59.md">[力扣 Top 39] LC 59 螺旋矩阵 II 中等 →</a>
</nav>
