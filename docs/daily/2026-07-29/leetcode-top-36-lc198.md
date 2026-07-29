---
title: "[力扣 Top 36] LC 198 打家劫舍 中等"
---

# [力扣 Top 36] LC 198 打家劫舍 中等

<p class="daily-archive-kicker">2026-07-29 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../dp/linear-recurrences.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：36
- 题号：LC 198
- 官方中文标题：打家劫舍
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/house-robber/>

### 原始题意

给定一排房屋的非负金额。相邻房屋不能同时选择，求可选择金额总和的最大值。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int rob(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：[1,2,3,1]
输出：4
解释：选择金额 1 和 3
```

```text
输入：[2,7,9,3,1]
输出：12
解释：选择 2、9、1
```

### 全部约束

- $1\le |nums|\le100$。
- $0\le nums_i\le400$。
- 答案最多 40000，32 位整数安全。

## 最优结论

处理当前房屋时只有两种互斥选择：

- 不选它：继承前一位置最优值；
- 选它：前一间必须不选，所以取前两位置最优值加当前金额。

$$
dp_i=\max(dp_{i-1},dp_{i-2}+nums_i).
$$

滚动保存前两项即可，时间 $O(n)$、额外空间 $O(1)$。

## 约束与观察

这不是“局部选较大金额”的贪心：`[2,1,1,2]` 中选择两端得到 4，逐对贪心容易失效。约束只依赖前一个位置，说明一维 DP 足够。

## 解法递进

### 解法一：选或不选的递归

每个位置分两支，时间 $O(2^n)$，递归空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const vector<int>& nums, int index) {
    if (index >= static_cast<int>(nums.size())) {
      return 0;
    }
    return max(search(nums, index + 1), nums[index] + search(nums, index + 2));
  }
public:
  int rob(vector<int>& nums) {
    return search(nums, 0);
  }
};
```

### 解法二：数组 DP

记忆重复子问题后为 $O(n)$ 时间、$O(n)$ 空间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int rob(vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    vector<int> dp(n + 1, 0);
    dp[1] = nums[0];
    for (int i = 2; i <= n; ++i) {
      dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1]);
    }
    return dp[n];
  }
};
```

### 解法三：滚动 DP

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int rob(vector<int>& nums) {
    int twoBack = 0;
    int oneBack = 0;
    for (int money : nums) {
      int current = max(oneBack, twoBack + money);
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
};
```

## 正确性证明

设 `dp[i]` 为前 `i` 间房屋的最大收益。任一最优方案对第 `i` 间只有两种情况：

- 不选择它，收益不超过 `dp[i-1]`，且该值可实现；
- 选择它，则第 `i-1` 间不能选，剩余部分最优为 `dp[i-2]`，总收益为 `dp[i-2]+nums[i-1]`。

两类穷尽且互斥，取最大即得最优。滚动变量始终分别保存这两个状态，所以返回值正确。

## 样例手推

`[2,7,9,3,1]` 的滚动值：

- 2 后为 2；
- 7 后为 7；
- 9 后为 `max(7,2+9)=11`；
- 3 后仍为 11；
- 1 后为 `max(11,11+1)=12`。

## 易错点

- 更新两个滚动变量时要先计算 `current`，避免覆盖依赖。
- 输入金额非负，但“允许不选任何房”仍由初值 0 自然处理。
- 环形房屋不能直接使用同一线性转移。
- 若需要恢复方案，常数空间状态不够。

## 验证说明

用指数递归作为小规模 oracle，对长度 1–20 的随机数组与滚动 DP 对拍；覆盖全零、单元素、严格递增和交替大值。

## Follow-up 与变种

### 变种一：房屋首尾相邻

首尾不能同时选。最优方案必然排除首房或排除尾房，分别跑线性 DP 后取最大。时间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int linear(const vector<int>& nums, int left, int right) {
    int twoBack = 0;
    int oneBack = 0;
    for (int i = left; i < right; ++i) {
      int current = max(oneBack, twoBack + nums[i]);
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
public:
  int rob(vector<int>& nums) {
    if (nums.size() == 1) {
      return nums[0];
    }
    int n = static_cast<int>(nums.size());
    return max(linear(nums, 0, n - 1), linear(nums, 1, n));
  }
};
```

### 变种二：恢复具体房屋下标

保存完整 DP，逆序比较 `dp[i]` 与 `dp[i-1]` 判断是否选取第 `i` 间。时间和空间均为 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> selectedHouses(const vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    vector<int> dp(n + 1, 0);
    if (n > 0) {
      dp[1] = nums[0];
    }
    for (int i = 2; i <= n; ++i) {
      dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1]);
    }
    vector<int> answer;
    for (int i = n; i >= 1;) {
      if (dp[i] == dp[i - 1]) {
        --i;
      } else {
        answer.push_back(i - 1);
        i -= 2;
      }
    }
    reverse(answer.begin(), answer.end());
    return answer;
  }
};
```

### 变种三：任意两间被选房屋至少间隔 `d` 间

选择下标 `i` 后，下一个可依赖状态是 `i-d-1`。转移为 `dp[i]=max(dp[i-1], value[i]+dp[max(0,i-d-1)])`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long maximumWithGap(const vector<int>& value, int d) {
    int n = static_cast<int>(value.size());
    vector<long long> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
      int previous = max(0, i - d - 1);
      dp[i] = max(dp[i - 1], dp[previous] + value[i - 1]);
    }
    return dp[n];
  }
};
```

### 变种四：房屋构成二叉树

树节点选择后不能选择直接孩子。DFS 返回 `{不选当前, 选当前}` 两个状态，时间 $O(n)$、递归空间 $O(h)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct TreeNode {
  int val;
  TreeNode* left;
  TreeNode* right;
};
class Solution {
  pair<int, int> dfs(TreeNode* node) {
    if (node == nullptr) {
      return {0, 0};
    }
    auto [leftSkip, leftTake] = dfs(node->left);
    auto [rightSkip, rightTake] = dfs(node->right);
    int skip = max(leftSkip, leftTake) + max(rightSkip, rightTake);
    int take = node->val + leftSkip + rightSkip;
    return {skip, take};
  }
public:
  int rob(TreeNode* root) {
    auto [skip, take] = dfs(root);
    return max(skip, take);
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/house-robber/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/house-robber/)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-35-lc53.md">← [力扣 Top 35] LC 53 最大子数组和 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-37-lc438.md">[力扣 Top 37] LC 438 找到字符串中所有字母异位词 中等 →</a>
</nav>
