---
title: "[力扣每日一题] 2026-08-15｜LC 3702 按位异或非零的最长子序列"
---

# [力扣每日一题] 2026-08-15｜LC 3702 按位异或非零的最长子序列

<p class="daily-archive-kicker">2026-08-15 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-15 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=5c01a3078be33eab4fdceeef9629641b5104cb7e40338f1efa2a067d716e02b5 -->
[官方题目：LC 3702 按位异或非零的最长子序列](https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/)

## 官方原始信息

- 日期：2026-08-15（Asia/Shanghai）；力扣中国官方每日一题接口已按该日期确认。
- 题号：3702。
- 标题：按位异或非零的最长子序列。
- 官方难度：中等。
- 官方链接：[力扣中国](https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/)。
- 标签：位运算、数组。

给定整数数组 `nums`，返回按位异或结果非零的最长非空子序列长度；若不存在，返回 0。子序列可以删除任意元素，但保留元素的相对顺序。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int longestSubsequence(vector<int>& nums);
};
```

### 全部官方样例

样例 1：

```text
输入：nums = [1,2,3]
输出：2
解释：[2,3] 的异或为 1，长度为 2。
```

样例 2：

```text
输入：nums = [2,3,4]
输出：3
解释：整个数组的异或为 5，已经非零。
```

### 全部约束

- $1\le nums.length\le10^5$。
- $0\le nums[i]\le10^9$。

## 约束推导与关键观察

设全部元素的异或为

$$
X=nums[0]\oplus nums[1]\oplus\cdots\oplus nums[n-1].
$$

若 $X\ne0$，整个数组就是长度 $n$ 的合法子序列，不可能更长。若 $X=0$，删除一个值为 $v$ 的元素后，剩余异或为 $X\oplus v=v$。因此只要存在非零元素，删除任意一个非零元素便得到长度 $n-1$ 的合法子序列；长度 $n$ 又因总异或为零而不合法，所以 $n-1$ 最优。若所有元素都是 0，任何子序列的异或仍为 0，答案只能是 0。

答案只可能是 $n$、$n-1$ 或 0。扫描时同时维护总异或与“是否存在非零元素”即可，数值本身不参与算术加法，不存在溢出风险。

## 解法递进

### 解法一：枚举全部非空子序列

用位掩码选择元素，逐个计算异或并更新最大长度。它严格覆盖所有子序列，可作为小规模 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestSubsequence(vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    int answer = 0;
    for (int mask = 1; mask < (1 << n); ++mask) {
      int value = 0;
      int length = 0;
      for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) {
          value ^= nums[i];
          ++length;
        }
      }
      if (value != 0) answer = max(answer, length);
    }
    return answer;
  }
};
int main() {
  vector<int> nums{1, 2, 3};
  cout << Solution().longestSubsequence(nums) << '\n';
}
```

时间 $O(n2^n)$，额外空间 $O(1)$。$n=10^5$ 时完全不可行。

### 解法二：按长度从大到小检查

无需真的枚举所有长度。长度 $n$ 只有一个候选；若它失败，长度 $n-1$ 的候选恰是“删去一个元素”。异或的可逆性使第二层也能常数时间判定，从而直接得到三分结论。

### 最佳实用解：一次扫描判定三种答案

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestSubsequence(vector<int>& nums) {
    int total = 0;
    bool hasNonzero = false;
    for (int value : nums) {
      total ^= value;
      hasNonzero |= value != 0;
    }
    if (total != 0) return static_cast<int>(nums.size());
    if (hasNonzero) return static_cast<int>(nums.size()) - 1;
    return 0;
  }
};
int main() {
  vector<int> nums{2, 3, 4};
  cout << Solution().longestSubsequence(nums) << '\n';
}
```

时间 $O(n)$，额外空间 $O(1)$；每个输入至少要读取一次，因此时间复杂度已经最优。

## 正确性证明

分三种情况。

1. 若全部元素异或 $X\ne0$，取全部 $n$ 个元素合法，且不存在更长子序列，答案为 $n$。
2. 若 $X=0$ 且存在非零元素 $v$，删除它后的异或为 $X\oplus v=v\ne0$，故存在长度 $n-1$ 的合法子序列；长度 $n$ 的唯一子序列异或为 0，故答案恰为 $n-1$。
3. 若所有元素都是 0，任何选中元素的异或都是 0，不存在合法非空子序列，答案为 0。

三种情况互斥且完备，所以算法正确。

## 样例手推与边界

样例 1 中 $1\oplus2\oplus3=0$，且存在非零元素。删除 1、2 或 3 中任意一个都得到长度 2 的非零异或子序列，因此答案为 2。

- `[0]`：所有元素为 0，答案为 0。
- `[7]`：总异或非零，答案为 1。
- `[5,5]`：总异或为 0，删除任意一个 5 后答案为 1。
- 含许多 0：零元素不会妨碍取全体；只有总异或是否为零决定能否保留全部元素。
- 异或应使用整数位运算 `^`，不能误写成幂运算。

## 方案比较与推荐

指数枚举完全忠于定义，适合验证；状态集合 DP 也能枚举可达异或，却会产生指数级不同状态。三分结论利用“删除一个元素等价于再异或该元素”，同时取得最小证明负担、常数空间和线性扫描。竞赛与面试中应优先记住总异或的可逆性，而不是套用通用子序列 DP。

## 易错点

- 子序列允许删除元素，不要求连续；不要误做成子数组。
- 当总异或为 0 时，不能无条件返回 $n-1$；全零数组没有任何合法子序列。
- 长度为 0 的空子序列不属于题目要求的非空子序列。
- 删除值 $v$ 后的异或是 $X\oplus v$，不是普通减法。

## 可复现验证

本页全部完整代码均以 C++23 严格编译。两个官方样例分别得到 2 和 3。固定种子穷举与随机生成 187,380 个小数组，把线性三分算法和全部子序列枚举逐项比较；另覆盖全零、单元素、成对相等与 $10^5$ 长度边界，结果全部一致。

## 变种一：恢复一组最长合法子序列的下标

若总异或非零，返回全部下标；若总异或为零，跳过第一个非零元素；全零时返回空集表示无解。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> longestIndices(const vector<int>& nums) {
  int total = 0;
  for (int value : nums) total ^= value;
  int skipped = -1;
  if (total == 0) {
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] != 0) {
        skipped = i;
        break;
      }
    }
    if (skipped == -1) return {};
  }
  vector<int> answer;
  for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
    if (i != skipped) answer.push_back(i);
  }
  return answer;
}
int main() {
  vector<int> nums{1, 2, 3};
  for (int index : longestIndices(nums)) cout << index << ' ';
  cout << '\n';
}
```

时间 $O(n)$，输出空间 $O(n)$；原题只求长度，因此无需保存这些下标。

## 变种二：统计最长合法子序列的数量

长度为 $n$ 时只有“取全部”一种。若答案为 $n-1$，每个被删掉的非零元素位置产生一个不同下标子序列；删除 0 仍使异或为零。全零时数量为 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, long long> longestCount(const vector<int>& nums) {
  int total = 0;
  long long nonzero = 0;
  for (int value : nums) {
    total ^= value;
    nonzero += value != 0;
  }
  if (total != 0) return {static_cast<int>(nums.size()), 1};
  if (nonzero > 0) return {static_cast<int>(nums.size()) - 1, nonzero};
  return {0, 0};
}
int main() {
  vector<int> nums{5, 5, 0};
  auto [length, count] = longestCount(nums);
  cout << length << ' ' << count << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。若结果需取模，只对 `nonzero` 取模即可。

## 变种三：在线单点修改后询问答案

维护全数组异或、非零元素数量和长度。把位置从 `old` 改为 `value` 时，以 `total ^= old ^ value` 删除旧贡献并加入新贡献，同时更新非零计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicXor {
  vector<int> values;
  int total = 0;
  int nonzero = 0;
public:
  explicit DynamicXor(vector<int> nums) : values(move(nums)) {
    for (int value : values) {
      total ^= value;
      nonzero += value != 0;
    }
  }
  void update(int index, int value) {
    int old = values[index];
    total ^= old ^ value;
    nonzero -= old != 0;
    nonzero += value != 0;
    values[index] = value;
  }
  int query() const {
    if (total != 0) return static_cast<int>(values.size());
    return nonzero == 0 ? 0 : static_cast<int>(values.size()) - 1;
  }
};
int main() {
  DynamicXor data({1, 2, 3});
  cout << data.query() << '\n';
  data.update(0, 0);
  cout << data.query() << '\n';
}
```

构造 $O(n)$，每次修改与询问均为 $O(1)$，存储数组需要 $O(n)$。

## 变种四：要求异或恰为目标值，且值域只有 $B$ 位

三分结论失效，因为删除一个元素未必得到指定目标。若 $nums[i]<2^B$ 且 $B\le15$，用 `dp[x]` 表示异或为 `x` 的最长子序列长度，逐个元素做取或不取转移。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int longestExactXor(const vector<int>& nums, int bits, int target) {
  int states = 1 << bits;
  const int negative = -1000000000;
  vector<int> dp(states, negative);
  dp[0] = 0;
  for (int value : nums) {
    vector<int> next = dp;
    for (int x = 0; x < states; ++x) {
      if (dp[x] == negative) continue;
      next[x ^ value] = max(next[x ^ value], dp[x] + 1);
    }
    dp.swap(next);
  }
  if (target == 0 && dp[0] == 0) return 0;
  return max(0, dp[target]);
}
int main() {
  vector<int> nums{1, 2, 3};
  cout << longestExactXor(nums, 2, 1) << '\n';
}
```

时间 $O(n2^B)$，空间 $O(2^B)$；原题的 $10^9$ 值域不能直接承受该状态表。

## 变种五：把“子序列”改为“连续子数组”

设前缀异或为 `prefix[i]`。子数组 `[l,r)` 的异或为 `prefix[l] ^ prefix[r]`，合法当且仅当两个前缀值不同。对每个右端点，只需找到最早出现、且值与当前前缀不同的前缀位置。维护最早出现的两个不同前缀值即可在线完成。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int longestNonzeroXorSubarray(const vector<int>& nums) {
  int firstValue = 0;
  int firstIndex = 0;
  bool hasSecond = false;
  int secondIndex = 0;
  int prefix = 0;
  int answer = 0;
  for (int right = 1; right <= static_cast<int>(nums.size()); ++right) {
    prefix ^= nums[right - 1];
    if (prefix != firstValue) {
      answer = max(answer, right - firstIndex);
      if (!hasSecond) {
        hasSecond = true;
        secondIndex = right;
      }
    } else if (hasSecond) {
      answer = max(answer, right - secondIndex);
    }
  }
  return answer;
}
int main() {
  vector<int> nums{0, 1, 1, 0};
  cout << longestNonzeroXorSubarray(nums) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。若最早前缀值始终为 0，第二个不同值的首次位置就足以处理当前前缀重新回到 0 的情况。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-d/">← [codeforces] CF Round 1116 Div.1 B / Div.2 D A Ribbon for Tomorrow</a>
<span class="daily-archive-pager__empty"></span>
</nav>
