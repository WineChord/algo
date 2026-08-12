---
title: "[力扣每日一题] 2026-08-12｜LC 2958 最多 K 个重复元素的最长子数组"
---

# [力扣每日一题] 2026-08-12｜LC 2958 最多 K 个重复元素的最长子数组

<p class="daily-archive-kicker">2026-08-12 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-12 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=22a48a7252463209474522fdb5060099a9a07f83c5dd83129ac0e0efa2033b5a -->
## 官方原始信息

- 日期：2026-08-12（Asia/Shanghai）。
- 题目：LC 2958，最多 K 个重复元素的最长子数组。
- 官方难度：中等。
- 官方链接：[最多 K 个重复元素的最长子数组](https://leetcode.cn/problems/length-of-longest-subarray-with-at-most-k-frequency/)。

### 原始题意与函数签名

给定正整数数组 `nums` 和正整数 `k`。若一个子数组中每个不同元素的出现次数都不超过 `k`，则称它为好子数组。返回最长好子数组的长度。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maxSubarrayLength(vector<int>& nums, int k);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3,1,2,3,1,2], k = 2
输出：6
解释：例如子数组 [1,2,3,1,2,3] 中每个值恰好出现两次。
```

```text
输入：nums = [1,2,1,2,1,2,1,2], k = 1
输出：2
解释：任意更长的连续区间都会让 1 或 2 至少出现两次。
```

```text
输入：nums = [5,5,5,5,5,5,5], k = 4
输出：4
```

### 全部约束

- $1\le |nums|\le10^5$。
- $1\le nums_i\le10^9$。
- $1\le k\le |nums|$。
- 答案不超过 $10^5$，`int` 足够；元素值域远大于数组长度，不能直接按最大值开频次数组。

## 约束推导与观察

$O(n^2)$ 枚举子数组在 $n=10^5$ 时不可行。把右端点加入窗口时，只有新元素 `nums[right]` 的频次可能从合法变为 $k+1$；不断右移左端点直到它恢复为 $k$，窗口便重新合法。左右端点都只单调前进一次，总代价线性。

核心不变量是：每轮记录答案前，窗口 `[left,right]` 内所有值的频次都不超过 `k`；而对固定 `right`，`left` 是能满足该条件的最小左端点，因此当前窗口也是以 `right` 结尾的最长好子数组。

## 解法递进

### 解法一：枚举起点并向右扩展

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  int answer = 0;
  for (int left = 0; left < n; ++left) {
    unordered_map<int, int> frequency;
    for (int right = left; right < n; ++right) {
      if (++frequency[a[right]] > k) break;
      answer = max(answer, right - left + 1);
    }
  }
  cout << answer << '\n';
}
```

固定起点时，一旦某个频次超限，继续向右只会更坏，故可以提前停止。期望时间 $O(n^2)$、空间 $O(n)$，可作为正确 oracle。

### 解法二：二分长度与定长窗口检查

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool hasGoodWindow(const vector<int>& a, int k, int length) {
  unordered_map<int, int> frequency;
  int excessive = 0;
  for (int right = 0; right < static_cast<int>(a.size()); ++right) {
    if (++frequency[a[right]] == k + 1) ++excessive;
    if (right >= length) {
      if (frequency[a[right - length]]-- == k + 1) --excessive;
    }
    if (right + 1 >= length && excessive == 0) return true;
  }
  return false;
}
int main() {
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  int low = 0, high = n;
  while (low < high) {
    int middle = (low + high + 1) / 2;
    if (hasGoodWindow(a, k, middle)) low = middle;
    else high = middle - 1;
  }
  cout << low << '\n';
}
```

若存在长度 $L$ 的好子数组，它的任意更短连续片段也好，所以长度具有单调性。时间 $O(n\log n)$、空间 $O(n)$；但每次二分都重扫数组。

### 最佳实用解：可变长度滑动窗口

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxSubarrayLength(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    int left = 0, answer = 0;
    for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
      ++frequency[nums[right]];
      while (frequency[nums[right]] > k) {
        --frequency[nums[left++]];
      }
      answer = max(answer, right - left + 1);
    }
    return answer;
  }
};
int main() {
  vector<int> nums{1, 2, 3, 1, 2, 3, 1, 2};
  cout << Solution().maxSubarrayLength(nums, 2) << '\n';
}
```

期望时间 $O(n)$、空间 $O(D)$，其中 $D$ 为窗口中不同值数，最坏 $O(n)$。相比二分方案，它直接利用“加入一个值只可能破坏该值约束”的局部结构，代码与常数均更优，推荐优先记忆。

## 正确性证明

归纳维护窗口合法。加入 `nums[right]` 前窗口合法；加入后其他值频次不变，唯一可能超限的是该新值。`while` 每次移除左端元素，最终必会移除足够多的新值，使其频次恢复到 `k`，于是窗口重新合法。

循环停止时，若把 `left` 向左退一位，则会重新包含刚被排除的某个新值，使该值频次达到 $k+1$；所以 `[left,right]` 是以 `right` 结尾的最长合法窗口。算法对所有右端点取最大值，覆盖全局最优子数组，故返回值正确。

## 样例手推、边界与易错点

样例一读到第三个 `1` 时，其频次变为 3；左端从 0 移到 1 后频次回到 2，窗口变为 `[2,3,1,2,3,1]`，长度仍为 6。继续加入最后一个 `2` 时同理收缩，最大值保持 6。

- `k=1` 退化为最长无重复元素子数组。
- 全部元素相同，答案是 `min(n,k)`。
- `k=n` 时整个数组一定合法。
- 收缩条件只需检查刚加入的值；写成扫描全部频次会退化。
- 必须先增加右端频次，再收缩，再更新答案。
- 大值域用散列表或坐标压缩，不能开长度 $10^9$ 的数组。
- 三个官方样例通过；最优解与二重枚举 oracle 在 100,000 组固定种子小数组上逐一一致。

## 变种一：返回最优子数组的左右端点

新定义：返回一个最长好子数组的闭区间；同长度时取最小左端点。每次更新最大长度时同时记录窗口即可，复杂度不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
pair<int, int> longestRange(const vector<int>& a, int k) {
  unordered_map<int, int> frequency;
  int left = 0, bestLeft = 0, bestRight = -1;
  for (int right = 0; right < static_cast<int>(a.size()); ++right) {
    ++frequency[a[right]];
    while (frequency[a[right]] > k) --frequency[a[left++]];
    if (right - left > bestRight - bestLeft) {
      bestLeft = left;
      bestRight = right;
    }
  }
  return {bestLeft, bestRight};
}
int main() {
  auto [left, right] = longestRange({1, 2, 3, 1, 2, 3, 1, 2}, 2);
  cout << left << ' ' << right << '\n';
}
```

## 变种二：统计全部好子数组

新定义：返回好子数组总数。窗口合法后，以 `right` 结尾的所有起点 `left..right` 都合法，贡献 `right-left+1`；时间 $O(n)$，答案用 `long long`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countGoodSubarrays(const vector<int>& a, int k) {
  unordered_map<int, int> frequency;
  int left = 0;
  long long answer = 0;
  for (int right = 0; right < static_cast<int>(a.size()); ++right) {
    ++frequency[a[right]];
    while (frequency[a[right]] > k) --frequency[a[left++]];
    answer += right - left + 1;
  }
  return answer;
}
int main() {
  cout << countGoodSubarrays({1, 2, 1}, 1) << '\n';
}
```

## 变种三：每个值有独立频次上限

新定义：映射 `limit[x]` 给出每个值允许次数，未出现的值上限为零。加入新值后仍只有它可能违约，原滑窗保持成立；期望时间 $O(n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int longestWithLimits(const vector<int>& a, const unordered_map<int, int>& limit) {
  unordered_map<int, int> frequency;
  int left = 0, answer = 0;
  for (int right = 0; right < static_cast<int>(a.size()); ++right) {
    int cap = limit.contains(a[right]) ? limit.at(a[right]) : 0;
    ++frequency[a[right]];
    while (frequency[a[right]] > cap) --frequency[a[left++]];
    answer = max(answer, right - left + 1);
  }
  return answer;
}
int main() {
  unordered_map<int, int> limit{{1, 2}, {2, 1}};
  cout << longestWithLimits({1, 2, 1, 2}, limit) << '\n';
}
```

## 变种四：数据流持续追加

新定义：元素逐个到达，每次追加后返回当前历史中的最长好子数组。保存窗口队列、频次和历史答案即可，每个元素均摊 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class GoodSubarrayStream {
  int k, answer = 0;
  deque<int> window;
  unordered_map<int, int> frequency;
public:
  explicit GoodSubarrayStream(int cap) : k(cap) {}
  int append(int value) {
    window.push_back(value);
    ++frequency[value];
    while (frequency[value] > k) {
      --frequency[window.front()];
      window.pop_front();
    }
    answer = max(answer, static_cast<int>(window.size()));
    return answer;
  }
};
int main() {
  GoodSubarrayStream stream(2);
  for (int x : {1, 2, 1, 2, 1}) cout << stream.append(x) << ' ';
  cout << '\n';
}
```

## 变种五：同一数组回答多个 K

新定义：给出多个独立的 `k`，分别返回最长长度。每次查询独立运行线性滑窗，时间 $O(nq)$、空间 $O(n)$；当询问量适中且值域巨大时，这是最稳健的方案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int solve(const vector<int>& a, int k) {
  unordered_map<int, int> frequency;
  int left = 0, answer = 0;
  for (int right = 0; right < static_cast<int>(a.size()); ++right) {
    ++frequency[a[right]];
    while (frequency[a[right]] > k) --frequency[a[left++]];
    answer = max(answer, right - left + 1);
  }
  return answer;
}
int main() {
  vector<int> a{1, 2, 3, 1, 2, 3, 1, 2};
  for (int k : {1, 2, 3}) cout << solve(a, k) << ' ';
  cout << '\n';
}
```

## 验证说明

所有完整代码块均按 C++23 编译。随机对拍生成长度 $1$ 到 $20$、值域 $[1,7]$、随机 `k` 的 100,000 组数组；最优滑窗与枚举所有子数组的 oracle 逐组比较，全部一致。另执行三个官方样例以及单元素、全相等、全不同、`k=1`、`k=n` 和大值域用例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/length-of-longest-subarray-with-at-most-k-frequency/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-a/">← [codeforces] CF Round 1116 Div.2 A Three Numbers on the Blackboard</a>
<span class="daily-archive-pager__empty"></span>
</nav>
