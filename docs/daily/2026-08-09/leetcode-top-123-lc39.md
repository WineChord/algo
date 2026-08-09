---
title: "[力扣 Top 123] LC 39 组合总和 中等"
---

# [力扣 Top 123] LC 39 组合总和 中等

<p class="daily-archive-kicker">2026-08-09 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=cce22567536ae4b45739062b9966064933c3882973d270dfc168482d2e1b71b4 -->
## 官方原始信息

- Top 排名：123
- 题号：LC 39
- 官方中文标题：组合总和
- 官方难度：中等
- 官方链接：[组合总和](https://leetcode.cn/problems/combination-sum/)

### 原始题意与函数签名

给定互不相同的正整数数组 `candidates` 和正整数 `target`，找出和为 `target` 的所有不同组合。每个候选数可重复选任意次；答案中组合顺序不重要，保证不同组合数少于 150。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> combinationSum(vector<int>& candidates, int target);
};
```

### 全部官方样例

```text
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
```

```text
输入：candidates = [2,3,5], target = 8
输出：[[2,2,2,2],[2,3,3],[3,5]]
```

```text
输入：candidates = [2], target = 1
输出：[]
```

### 全部约束

- $1\le candidates.length\le30$。
- $2\le candidates_i\le40$，所有候选数互不相同。
- $1\le target\le40$。
- 不同组合总数少于 150。

## 约束推导与观察

所有候选数为正，因此剩余和严格下降，递归一定终止，深度至多 $target/\min(candidates)$。若把每次选择当作有序序列，会同时生成 `[2,2,3]`、`[2,3,2]` 等排列。为消除重复，规定路径中的候选下标非递减：递归只从当前 `start` 往后选，同一数可继续使用当前下标。

## 解法递进

### 解法一：枚举所有有序选择后用集合去重

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  set<vector<int>> uniqueAnswers;
  vector<int> path;
  void dfs(const vector<int>& candidates, int remaining) {
    if (remaining == 0) {
      vector<int> normalized = path;
      sort(normalized.begin(), normalized.end());
      uniqueAnswers.insert(normalized);
      return;
    }
    for (int x : candidates) {
      if (x <= remaining) {
        path.push_back(x);
        dfs(candidates, remaining - x);
        path.pop_back();
      }
    }
  }
public:
  vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    dfs(candidates, target);
    return {uniqueAnswers.begin(), uniqueAnswers.end()};
  }
};
```

覆盖所有方案，但一个长度为 $d$ 的组合可能生成多达 $d!$ 个排列，时间近似指数级且去重开销大，只适合作 oracle。

### 解法二：下标单调的回溯

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answers;
  vector<int> path;
  void dfs(const vector<int>& candidates, int start, int remaining) {
    if (remaining == 0) {
      answers.push_back(path);
      return;
    }
    for (int i = start; i < static_cast<int>(candidates.size()); ++i) {
      if (candidates[i] > remaining) {
        continue;
      }
      path.push_back(candidates[i]);
      dfs(candidates, i, remaining - candidates[i]);
      path.pop_back();
    }
  }
public:
  vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    dfs(candidates, 0, target);
    return answers;
  }
};
```

它已消除排列重复。最坏时间仍为指数级，递归空间 $O(target/\min candidates)$，另计输出。

### 最佳实用解：排序后剪枝的规范回溯

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answers;
  vector<int> path;
  void dfs(const vector<int>& candidates, int start, int remaining) {
    if (remaining == 0) {
      answers.push_back(path);
      return;
    }
    for (int i = start; i < static_cast<int>(candidates.size()); ++i) {
      int value = candidates[i];
      if (value > remaining) {
        break;
      }
      path.push_back(value);
      dfs(candidates, i, remaining - value);
      path.pop_back();
    }
  }
public:
  vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    sort(candidates.begin(), candidates.end());
    dfs(candidates, 0, target);
    return answers;
  }
};
```

排序使 `value > remaining` 后可以整段停止。时间与输出规模相关，最坏仍为指数级；递归空间 $O(target/\min candidates)$。这是最清晰、最稳定的提交写法。

## 正确性证明

归纳考虑每个合法组合按候选下标非递减排列。根节点从其第一个下标开始选择；递归传入同一 `i`，允许重复使用；后续只选不小于 `i` 的下标，所以该组合对应唯一一条路径。反过来，每条到达 `remaining=0` 的路径都只使用候选值、总和为目标且下标非递减，是合法组合。不同非递减序列不可能表示同一个多重集合，因此既不遗漏也不重复。

## 样例手推

排序 `[2,3,6,7]`。先选 2，剩余 5；再选 2，剩余 3；候选 2 继续会超出，选 3 得到 `[2,2,3]`。回溯到根后直接选 7 得到 `[7]`。选择 3 后递归不会回头选 2，因此不会生成 `[3,2,2]`。

## 易错点与方案比较

- 递归时传 `i` 而非 `i+1`，因为本题允许重复使用当前数。
- `candidates` 全为正数是终止与剪枝的关键；若允许 0 或负数，无限使用会产生无限解或循环。
- 组合顺序无关，必须建立规范顺序，而不是生成后昂贵去重。
- `answers` 和 `path` 若是成员变量，新的调用前应保证对象未复用旧状态；在线评测通常每例新建对象。

## 变种一：每个数只能用一次且输入可重复

对应 [LC 40 组合总和 II](https://leetcode.cn/problems/combination-sum-ii/)。递归传 `i+1`，同一层跳过相同值，才能同时满足“一次使用”和“结果不重复”。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answers;
  vector<int> path;
  void dfs(const vector<int>& a, int start, int remaining) {
    if (remaining == 0) {
      answers.push_back(path);
      return;
    }
    for (int i = start; i < static_cast<int>(a.size()) && a[i] <= remaining; ++i) {
      if (i > start && a[i] == a[i - 1]) {
        continue;
      }
      path.push_back(a[i]);
      dfs(a, i + 1, remaining - a[i]);
      path.pop_back();
    }
  }
public:
  vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
    sort(candidates.begin(), candidates.end());
    dfs(candidates, 0, target);
    return answers;
  }
};
```

最坏时间 $O(2^n)$，递归空间 $O(n)$。

## 变种二：只统计组合数量

对应 [LC 518 零钱兑换 II](https://leetcode.cn/problems/coin-change-ii/)。不需恢复方案时，用一维完全背包；先枚举硬币保证统计组合而非排列。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int change(int amount, vector<int>& coins) {
    vector<unsigned long long> ways(amount + 1);
    ways[0] = 1;
    for (int coin : coins) {
      for (int sum = coin; sum <= amount; ++sum) {
        ways[sum] += ways[sum - coin];
      }
    }
    return static_cast<int>(ways[amount]);
  }
};
```

时间 $O(n\cdot target)$、空间 $O(target)$。

## 变种三：求使用元素的最少个数

对应 [LC 322 零钱兑换](https://leetcode.cn/problems/coin-change/)。目标从“枚举所有组合”改成最优化，用完全背包取最小值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int sum = 1; sum <= amount; ++sum) {
      for (int coin : coins) {
        if (coin <= sum) {
          dp[sum] = min(dp[sum], dp[sum - coin] + 1);
        }
      }
    }
    return dp[amount] > amount ? -1 : dp[amount];
  }
};
```

时间 $O(n\cdot target)$、空间 $O(target)$。

## 变种四：允许负数，但每个元素至多使用一次

新定义：候选可含负数或零，每个下标最多选一次，找出和为目标的下标组合。原“剩余和变小”剪枝失效，但有限使用保证递归终止；按下标前进枚举。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> subsetTarget(const vector<int>& a, long long target) {
  vector<vector<int>> answers;
  vector<int> chosen;
  auto dfs = [&](auto&& self, int index, long long sum) -> void {
    if (index == static_cast<int>(a.size())) {
      if (sum == target) {
        answers.push_back(chosen);
      }
      return;
    }
    self(self, index + 1, sum);
    chosen.push_back(index);
    self(self, index + 1, sum + a[index]);
    chosen.pop_back();
  };
  dfs(dfs, 0, 0);
  return answers;
}
int main() {
  cout << subsetTarget({-2, 0, 3}, 1).size() << '\n';
}
```

时间 $O(2^n)$、递归空间 $O(n)$。若负数还能无限使用，解集可能无限，必须增加使用上限或重新定义问题。

## 可复现验证

对候选集合大小不超过 7、值域 `2..10`、目标不超过 25 的随机实例，以“有序选择+集合去重”为 oracle，对比两种规范回溯并对每个输出检查和、下标单调性和唯一性。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/combination-sum/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-122-lc1004/">← [力扣 Top 122] LC 1004 最大连续 1 的个数 III 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-124-lc61/">[力扣 Top 124] LC 61 旋转链表 中等 →</a>
</nav>
