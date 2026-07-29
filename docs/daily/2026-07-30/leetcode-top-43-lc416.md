---
title: "[力扣 Top 43] LC 416 分割等和子集 中等"
---

# [力扣 Top 43] LC 416 分割等和子集 中等

<p class="daily-archive-kicker">2026-07-30 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b80e9b3ab14237d9779ce7b8e8981a7bc16d755c8a886ded08fa83b3b58760ea -->
## 官方原始信息

- Top 排名：43
- 题号：LC 416
- 官方中文标题：分割等和子集
- 官方难度：中等
- 官方链接：[分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/)

### 原始题意

给定只包含正整数的非空数组 `nums`，判断能否把全部元素分成两个元素和相等的子集。每个数组位置必须且只能属于其中一个子集。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool canPartition(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,5,11,5]
输出：true
解释：可以分成 [1,5,5] 与 [11]。
```

```text
输入：nums = [1,2,3,5]
输出：false
```

### 全部约束

- $1\le n\le200$。
- $1\le nums_i\le100$。
- 总和至多 $2\times10^4$，目标和至多 $10^4$。

## 约束推导与模型转换

设总和为 $S$。两个子集等和的必要条件是 $S$ 为偶数；若能选出一个和为 $S/2$ 的子集，剩余元素自然组成另一个同和子集。因此问题等价为容量为 $S/2$ 的 0-1 背包可达性。

所有数都为正，故超过目标的状态无需保留；`int` 足以存总和。

## 解法递进

### 解法一：枚举每个元素选或不选

递归覆盖所有子集，时间 $O(2^n)$、递归空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool search(const vector<int>& nums, int index, int remain) {
    if (remain == 0) {
      return true;
    }
    if (index == static_cast<int>(nums.size()) || remain < 0) {
      return false;
    }
    return search(nums, index + 1, remain) || search(nums, index + 1, remain - nums[index]);
  }
public:
  bool canPartition(vector<int>& nums) {
    int sum = accumulate(nums.begin(), nums.end(), 0);
    return sum % 2 == 0 && search(nums, 0, sum / 2);
  }
};
```

### 解法二：二维 0-1 背包

`dp[i][s]` 表示只看前 `i` 个元素能否凑出和 `s`：

$$
dp_{i,s}=dp_{i-1,s}\lor dp_{i-1,s-nums_i}.
$$

时间 $O(nS)$，空间 $O(nS)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canPartition(vector<int>& nums) {
    int sum = accumulate(nums.begin(), nums.end(), 0);
    if (sum % 2 == 1) {
      return false;
    }
    int target = sum / 2;
    vector<vector<char>> dp(nums.size() + 1, vector<char>(target + 1));
    dp[0][0] = true;
    for (int i = 1; i <= static_cast<int>(nums.size()); ++i) {
      for (int value = 0; value <= target; ++value) {
        dp[i][value] = dp[i - 1][value];
        if (value >= nums[i - 1]) {
          dp[i][value] |= dp[i - 1][value - nums[i - 1]];
        }
      }
    }
    return dp[nums.size()][target];
  }
};
```

### 最佳实用解：一维倒序 0-1 背包

压缩掉元素维度。处理一个数 `x` 时必须从大到小更新，确保同一位置只使用一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canPartition(vector<int>& nums) {
    int sum = accumulate(nums.begin(), nums.end(), 0);
    if (sum % 2 == 1) {
      return false;
    }
    int target = sum / 2;
    vector<char> reachable(target + 1);
    reachable[0] = true;
    for (int value : nums) {
      for (int current = target; current >= value; --current) {
        reachable[current] |= reachable[current - value];
      }
      if (reachable[target]) {
        return true;
      }
    }
    return false;
  }
};
```

时间复杂度 $O(nS)$，其中 $S$ 是半和；空间复杂度 $O(S)$。

## 正确性证明

不变量：处理前 `i` 个元素后，`reachable[s]` 为真当且仅当能从这 `i` 个位置中选出和为 `s` 的子集。

处理新元素 `x` 时，原有真状态对应“不选 `x`”；由 `reachable[s-x]` 转移到 `reachable[s]` 对应“选择 `x`”。倒序扫描保证读取的 `reachable[s-x]` 仍来自处理 `x` 之前，所以 `x` 不会被重复使用。两种选择覆盖全部子集且互不缺失。最终 `reachable[S/2]` 为真恰好等价于存在等和分割。

## 样例手推

对 `[1,5,11,5]`，总和 22，目标 11。可达集合依次包含：

```text
初始：{0}
加入 1：{0,1}
加入 5：{0,1,5,6}
加入 11：目标 11 可达
```

剩余元素的和也为 11，因此返回真。

## 易错点与方案比较

- 总和为奇数时立即返回假。
- 一维 0-1 背包必须倒序；正序会把同一元素使用多次，变成完全背包。
- 题目按数组位置分配，重复数值仍是不同元素。
- 提前命中目标可以安全返回，因为后续元素可全部放进另一个子集。
- 二维 DP 更直观且便于恢复方案；一维 DP 更省空间，推荐作为面试与竞赛默认实现。

## 变种一：恢复两个具体子集

新定义：若可分，输出一个目标子集的下标，剩余下标组成另一个子集。使用二维可达表反向判断某个元素是否被选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int sum = accumulate(a.begin(), a.end(), 0);
  if (sum % 2 == 1) {
    cout << "NO\n";
    return 0;
  }
  int target = sum / 2;
  vector<vector<char>> dp(n + 1, vector<char>(target + 1));
  dp[0][0] = true;
  for (int i = 1; i <= n; ++i) {
    for (int s = 0; s <= target; ++s) {
      dp[i][s] = dp[i - 1][s];
      if (s >= a[i - 1]) {
        dp[i][s] |= dp[i - 1][s - a[i - 1]];
      }
    }
  }
  if (!dp[n][target]) {
    cout << "NO\n";
    return 0;
  }
  vector<char> chosen(n);
  for (int i = n, s = target; i > 0; --i) {
    if (s >= a[i - 1] && dp[i - 1][s - a[i - 1]]) {
      chosen[i - 1] = true;
      s -= a[i - 1];
    }
  }
  cout << "YES\n";
  for (int i = 0; i < n; ++i) {
    if (chosen[i]) {
      cout << i << ' ';
    }
  }
  cout << '\n';
  for (int i = 0; i < n; ++i) {
    if (!chosen[i]) {
      cout << i << ' ';
    }
  }
  cout << '\n';
}
```

时间和空间均为 $O(nS)$。

## 变种二：统计目标子集数量

新定义：统计下标子集和为目标值的方案数并对给定模数取模。布尔状态改成计数，仍倒序更新。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, target, mod;
  cin >> n >> target >> mod;
  vector<int> ways(target + 1);
  ways[0] = 1;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    for (int sum = target; sum >= value; --sum) {
      ways[sum] += ways[sum - value];
      if (ways[sum] >= mod) {
        ways[sum] -= mod;
      }
    }
  }
  cout << ways[target] << '\n';
}
```

时间 $O(nS)$，空间 $O(S)$。等和分割若把两个无序子集视作同一种，通常还要除以 2；但空数组或零值会改变计数口径，必须先明确题意。

## 变种三：数组允许负数

新定义：元素可正可负，仍判断能否分成等和两组。可达和范围为 $[neg,pos]$，用偏移量保存状态；正负数都会把旧状态平移。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  int total = 0;
  int positive = 0;
  int negative = 0;
  for (int& value : a) {
    cin >> value;
    total += value;
    positive += max(value, 0);
    negative += min(value, 0);
  }
  if (total % 2 != 0) {
    cout << "NO\n";
    return 0;
  }
  int offset = -negative;
  vector<char> reachable(positive - negative + 1);
  reachable[offset] = true;
  for (int value : a) {
    vector<char> next = reachable;
    for (int sum = negative; sum <= positive; ++sum) {
      if (!reachable[sum + offset]) {
        continue;
      }
      int moved = sum + value;
      if (negative <= moved && moved <= positive) {
        next[moved + offset] = true;
      }
    }
    reachable.swap(next);
  }
  cout << (reachable[total / 2 + offset] ? "YES\n" : "NO\n");
}
```

设值域宽度为 $W=pos-neg$，时间 $O(nW)$、空间 $O(W)$。原来依赖正数与目标上界的倒序技巧不再直接成立。

## 变种四：分成 $k$ 个等和子集

新定义：把所有正整数分成 $k$ 个非空、等和子集。普通一维背包只证明一个子集存在，不能保证剩余部分还能继续分。可按降序回溯装桶并做对称剪枝。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool place(const vector<int>& a, int index, int target, vector<int>& bucket) {
  if (index == static_cast<int>(a.size())) {
    return true;
  }
  for (int i = 0; i < static_cast<int>(bucket.size()); ++i) {
    if (bucket[i] + a[index] > target) {
      continue;
    }
    if (i > 0 && bucket[i] == bucket[i - 1]) {
      continue;
    }
    bucket[i] += a[index];
    if (place(a, index + 1, target, bucket)) {
      return true;
    }
    bucket[i] -= a[index];
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int sum = accumulate(a.begin(), a.end(), 0);
  if (sum % k != 0) {
    cout << "NO\n";
    return 0;
  }
  sort(a.rbegin(), a.rend());
  int target = sum / k;
  if (a[0] > target) {
    cout << "NO\n";
    return 0;
  }
  vector<int> bucket(k);
  cout << (place(a, 0, target, bucket) ? "YES\n" : "NO\n");
}
```

最坏仍为指数时间，适合 $n$ 较小的情形；按降序放置、大数越界和等容量桶去重能显著剪枝。

## 可复现验证

- 所有完整代码按 C++23 编译。
- 官方样例、奇数总和、单元素、全相等与目标恰由单元素组成的边界均应覆盖。
- 小规模随机数组可枚举所有子集，与二维及一维 DP 对拍。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/partition-equal-subset-sum/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/partition-equal-subset-sum/)
- [对应知识专题](../../dp/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-42-lc124/">← [力扣 Top 42] LC 124 二叉树中的最大路径和 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-44-lc28/">[力扣 Top 44] LC 28 找出字符串中第一个匹配项的下标 简单 →</a>
</nav>
