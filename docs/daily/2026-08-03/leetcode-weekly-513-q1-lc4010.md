---
title: "[力扣竞赛] 第 513 场周赛 Q1 LC 4010 数对的最大强度 简单"
---

# [力扣竞赛] 第 513 场周赛 Q1 LC 4010 数对的最大强度 简单

<p class="daily-archive-kicker">2026-08-03 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=df84edd09a1811b8c209b649f66962c25ac31c1e01b04c3f1d9e3b0bbd2609bc -->
## 官方原始信息

- 来源：力扣中国。
- 比赛：第 513 场周赛。
- 比赛题号：Q1。
- 题号：LC 4010。
- 官方中文标题：数对的最大强度。
- 官方难度：简单。
- 官方比赛分值：3 分。
- ZeroTracer 社区估算竞赛分：未知（2026-08-03 抓取时公开数据尚无该题数值）。
- 官方链接：[数对的最大强度](https://leetcode.cn/problems/maximize-pair-strength-using-gcd/)。

### 原始题意

给定正整数数组 `nums`。下标不同的两个元素 `nums[i]` 与 `nums[j]` 的强度定义为

$$
\frac{nums_i\cdot nums_j}{\gcd(nums_i,nums_j)^2}.
$$

求所有数对中的最大强度。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  long long maxPairStrength(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [2,3,5]
输出：15
解释：选择 3 和 5，最大公约数为 1，强度为 3×5=15。
```

```text
输入：nums = [4,6,8]
输出：12
解释：选择 6 和 8，gcd=2，强度为 6×8/4=12。
```

```text
输入：nums = [3,3]
输出：1
解释：唯一数对的 gcd 为 3，强度为 9/9=1。
```

### 全部约束

- $2\le nums.length\le2000$。
- $1\le nums_i\le10^5$。

## 约束推导与边界

$n\le2000$ 意味着数对数量最多约 $2\times10^6$，$O(n^2\log V)$ 可行；试图枚举所有公因数的 $O(n^2V)$ 则过慢。令 $g=\gcd(a,b)$，把两数同时约去 $g$：

$$
\frac{ab}{g^2}=\left(\frac a g\right)\left(\frac b g\right).
$$

这既避免了先乘后除的中间风险，也揭示了强度就是约分后两个互质部分的乘积。每个约分后因子不超过 $10^5$，答案不超过 $10^{10}$，必须使用 `long long`；`int` 会溢出。

重复值允许，两个相等值的强度为 1。所有值为 1 时答案仍为 1；互质大数通常产生较大强度，但不能只选原值乘积最大的两数，因为较大的公共因子会被平方消去。

## 解法递进

### 解法一：枚举公因数求最大公约数

枚举每个数对，再从 1 扫到两数较小值，记录最后一个同时整除它们的数。它完全按定义计算，可作小规模 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long maxPairStrength(vector<int>& nums) {
    long long answer = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      for (int j = i + 1; j < static_cast<int>(nums.size()); ++j) {
        int common = 1;
        for (int divisor = 1; divisor <= min(nums[i], nums[j]); ++divisor) {
          if (nums[i] % divisor == 0 && nums[j] % divisor == 0) {
            common = divisor;
          }
        }
        answer = max(answer, 1LL * (nums[i] / common) * (nums[j] / common));
      }
    }
    return answer;
  }
};
```

时间 $O(n^2V)$，额外空间 $O(1)$；上限会超时，瓶颈是重复试除。

### 最佳实用解：欧几里得算法逐对约分

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long maxPairStrength(vector<int>& nums) {
    long long answer = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      for (int j = i + 1; j < static_cast<int>(nums.size()); ++j) {
        long long common = gcd(nums[i], nums[j]);
        long long strength = 1LL * (nums[i] / common) * (nums[j] / common);
        answer = max(answer, strength);
      }
    }
    return answer;
  }
};
```

时间 $O(n^2\log V)$，额外空间 $O(1)$。在 $n=2000$ 时约两百万次数对计算，结构直接、常数稳定，是应优先记忆的方案。

## 正确性证明

算法枚举所有且仅所有满足 $0\le i<j<n$ 的合法下标对。对任一枚举对，欧几里得算法返回其精确最大公约数 $g$；整数 $a/g$ 与 $b/g$ 均无余数，乘积严格等于题目定义的 $ab/g^2$。算法用 `answer` 保存已处理数对强度的最大值，因此循环结束后，它等于全部合法数对强度的最大值，正是所求。

## 样例手推

对 `[4,6,8]`：$(4,6)$ 的 $g=2$，强度 $2\times3=6$；$(4,8)$ 的 $g=4$，强度 $1\times2=2$；$(6,8)$ 的 $g=2$，强度 $3\times4=12$，最大值为 12。

对 `[3,3]`，约分后为 $(1,1)$，强度为 1。`[99991,100000]` 若互质，乘积接近 $10^{10}$，验证了 64 位类型的必要性。

## 易错点与方案比较

- 分母是 $g^2$，不是 $g$；本题强度不等于最小公倍数。
- 先做 `nums[i] * nums[j]` 会在 `int` 中溢出，即使赋给 `long long` 也来不及；应先约分并用 `1LL`。
- 数对要求下标不同，循环必须从 `j=i+1` 开始；重复数值仍可组成合法数对。
- 最大元素对不保证最优，因为公共因子平方会显著降低强度。
- 质因数分解可以复用信息，但在 $n=2000$ 下实现更复杂且无渐进收益；逐对 `gcd` 的证明与边界最稳健。

## 变种一：同时恢复最优下标对

新定义：返回最大强度以及一组字典序最小的一基下标。枚举顺序本身按字典序递增，只在严格变大时更新即可保留最早数对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> nums(n);
  for (int& value : nums) {
    cin >> value;
  }
  long long best = -1;
  pair<int, int> indices;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      long long common = gcd(nums[i], nums[j]);
      long long current = 1LL * (nums[i] / common) * (nums[j] / common);
      if (current > best) {
        best = current;
        indices = {i + 1, j + 1};
      }
    }
  }
  cout << best << '\n' << indices.first << ' ' << indices.second << '\n';
}
```

时间 $O(n^2\log V)$，空间 $O(1)$。

## 变种二：统计达到最大强度的下标对数量

新定义：除最大值外，统计有多少下标对达到它。遇到更大值时重置计数，遇到相等值时累加；计数上限为 $\binom n2$，使用 `long long`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> nums(n);
  for (int& value : nums) {
    cin >> value;
  }
  long long best = -1;
  long long count = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      long long common = gcd(nums[i], nums[j]);
      long long current = 1LL * (nums[i] / common) * (nums[j] / common);
      if (current > best) {
        best = current;
        count = 1;
      } else if (current == best) {
        ++count;
      }
    }
  }
  cout << best << ' ' << count << '\n';
}
```

时间 $O(n^2\log V)$，空间 $O(1)$；重复值会增加不同下标对，不能先去重。

## 变种三：在线追加数字并报告当前最大值

新定义：数字逐个到达；从第二个数字开始，每次输出当前数组的最大强度。新答案只可能来自“旧答案”或“新数与任一旧数”的数对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<int> nums;
  long long answer = 0;
  while (q--) {
    int value;
    cin >> value;
    for (int previous : nums) {
      long long common = gcd(previous, value);
      answer = max(answer, 1LL * (previous / common) * (value / common));
    }
    nums.push_back(value);
    if (nums.size() >= 2) {
      cout << answer << '\n';
    }
  }
}
```

第 $k$ 次追加耗时 $O(k\log V)$，总时间 $O(q^2\log V)$，空间 $O(q)$；它避免每次从头重算旧数对。

## 变种四：数组很长但值域很小

新定义：$n$ 很大、$nums_i\le V$，其中 $V$ 较小。先统计频率，只枚举出现过的数值对；相同值只有频率至少 2 才合法。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, maximumValue;
  cin >> n >> maximumValue;
  vector<int> frequency(maximumValue + 1);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++frequency[value];
  }
  vector<int> values;
  for (int value = 1; value <= maximumValue; ++value) {
    if (frequency[value] > 0) {
      values.push_back(value);
    }
  }
  long long answer = 0;
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    for (int j = i; j < static_cast<int>(values.size()); ++j) {
      if (i == j && frequency[values[i]] < 2) {
        continue;
      }
      long long common = gcd(values[i], values[j]);
      answer = max(answer, 1LL * (values[i] / common) * (values[j] / common));
    }
  }
  cout << answer << '\n';
}
```

设不同值数量为 $U$，时间 $O(n+V+U^2\log V)$，空间 $O(V)$。当重复很多、$U\ll n$ 时优于逐下标枚举。

## 验证说明

本轮将所有代码按 C++23 编译；最佳解会与试除法 oracle 在随机长度 2–10、值域 1–50 的数组上对拍，并覆盖全 1、全部相等、互质大数和公共因子很大的数对。官方三个样例逐项复核。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximize-pair-strength-using-gcd/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-90-lc1929/">← [力扣 Top 90] LC 1929 数组串联 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-b/">[codeforces] CF Round 1113 Div.2 B Merge to Match →</a>
</nav>
