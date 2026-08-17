---
title: "[力扣每日一题] 2026-08-18｜LC 3471 找出最大的几近缺失整数"
---

# [力扣每日一题] 2026-08-18｜LC 3471 找出最大的几近缺失整数

<p class="daily-archive-kicker">2026-08-18 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-18 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=9672cbd7dc2bb62004e743e352154474446dae157d90c1fb3df25b9568bde3f9 -->
[力扣 3471：找出最大的几近缺失整数](https://leetcode.cn/problems/find-the-largest-almost-missing-integer/)

## 官方原始信息

- 日期：2026-08-18（北京时间）；力扣中国官方每日一题记录已核对。
- 题号：3471。
- 官方中文标题：找出最大的几近缺失整数。
- 官方难度：简单；原比赛为第 439 场周赛第 1 题，官方分值 3 分。
- ZeroTracer 社区估算竞赛分：1308.2307785298，抓取于 2026-08-18；这不是力扣官方难度。
- 函数签名：`int largestInteger(vector<int>& nums, int k)`。
- 题意：若一个整数恰好出现在 `nums` 的一个长度为 `k` 的连续子数组中，就称它为
  几近缺失整数。这里统计的是“包含该值的窗口数”，同一窗口内出现多次仍只算一个窗口。
  返回最大的几近缺失整数；不存在则返回 -1。

### 全部官方样例

样例 1：

```text
输入：nums = [3,9,2,1,7], k = 3
输出：7
解释：值 1、2、3、7、9 分别出现在 2、3、1、1、2 个长度为 3 的子数组中，
几近缺失整数为 3 和 7，最大值是 7。
```

样例 2：

```text
输入：nums = [3,9,7,2,1,7], k = 4
输出：3
解释：值 1、2、3、7、9 分别出现在 2、3、1、3、2 个长度为 4 的子数组中，
只有 3 恰好出现在一个窗口中。
```

样例 3：

```text
输入：nums = [0,0], k = 1
输出：-1
解释：值 0 出现在两个长度为 1 的子数组中。
```

### 全部官方约束

- $1 \le n=|nums| \le 50$。
- $0 \le nums_i \le 50$。
- $1 \le k \le n$。

## 约束推导与窗口覆盖

暴力枚举窗口只有 $O(nk)$，在 $n\le50$ 时已经足够。但若追问最优结构，可以研究一个
位置属于多少个长度为 $k$ 的窗口。位置 $i$ 能被起点 $l$ 的窗口包含，当且仅当

$$
\max(0,i-k+1)\le l\le\min(i,n-k).
$$

当 $1<k<n$ 时，位置 0 只属于首窗口，位置 $n-1$ 只属于末窗口，而每个内部位置至少
属于两个窗口。因此中间情形只有两个端点上的值可能成为答案，并且该值必须在整个数组中
只出现一次。两个退化边界需要单独处理：

- $k=1$：每个窗口只有一个元素，窗口出现次数就是全局频率。
- $k=n$：全数组只有一个窗口，任何出现过的值都恰好属于这个窗口，与值在窗口内出现几次
  无关，答案就是数组最大值。

值域只有 0 到 50，频率数组安全；不存在乘法与整数溢出。

## 样例手推与边界

样例 1 有三个窗口：`[3,9,2]`、`[9,2,1]`、`[2,1,7]`。首元素 3 只在首窗口，
末元素 7 只在末窗口，且二者均全局唯一，所以候选是 3、7，取 7。内部值 9、2、1 至少
覆盖两个窗口，不能成为答案。

- `n=1,k=1`：唯一值出现在唯一窗口中，应直接返回它。
- `k=n` 且最大值重复：仍返回最大值，例如 `[5,5],k=2` 返回 5。
- `1<k<n` 且首尾相同：该值全局至少出现两次，两端都不合格。
- 值 0 合法，答案哨兵必须是 -1，不能用 0 表示不存在。
- 同一值在一个窗口出现多次：只算该窗口一次，暴力统计时必须先用集合去重。

## 解法一：逐窗口去重计数

枚举每个长度为 $k$ 的窗口，把其中不同的值放入集合，再为这些值的窗口计数加一。最后从
大到小寻找计数恰为 1 的值。该算法完全贴合定义，可作为结构解的 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestInteger(vector<int>& nums, int k) {
    array<int, 51> windowCount{};
    int n = nums.size();
    for (int left = 0; left + k <= n; ++left) {
      array<bool, 51> present{};
      for (int i = left; i < left + k; ++i) present[nums[i]] = true;
      for (int value = 0; value <= 50; ++value) {
        if (present[value]) ++windowCount[value];
      }
    }
    for (int value = 50; value >= 0; --value) {
      if (windowCount[value] == 1) return value;
    }
    return -1;
  }
};
```

时间复杂度 $O((n-k+1)(k+V))$，其中 $V=51$；也可用哈希集合写成 $O(nk)$ 期望
时间。额外空间 $O(V)$。瓶颈是反复扫描高度重叠的窗口。

## 从窗口枚举到位置覆盖

同一个值的窗口出现次数，是它所有出现位置各自覆盖的窗口起点区间之并的长度。一般情形
可以合并区间；本题只关心并长是否等于 1，而固定长度窗口的端点结构更强。

在 $1<k<n$ 时，任何内部位置的覆盖区间长度至少为 2；只要某个值在内部出现，它立刻
失去资格。唯一覆盖一个窗口的位置只有数组两端。再结合全局频率，就把所有滑窗工作化简成
一次计数与两个端点检查。

## 最佳实用解：按 k 分类

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int largestInteger(vector<int>& nums, int k) {
    int n = nums.size();
    if (k == n) return *max_element(nums.begin(), nums.end());
    array<int, 51> frequency{};
    for (int value : nums) ++frequency[value];
    if (k == 1) {
      for (int value = 50; value >= 0; --value) {
        if (frequency[value] == 1) return value;
      }
      return -1;
    }
    int answer = -1;
    if (frequency[nums.front()] == 1) answer = nums.front();
    if (frequency[nums.back()] == 1) answer = max(answer, nums.back());
    return answer;
  }
};
```

时间复杂度 $O(n+V)$，固定值域下记为 $O(n)$；额外空间 $O(V)$，固定值域下为 $O(1)$。
这是最佳实用解，因为至少要读取输入以确定频率和最大值。

### 正确性证明

当 $k=1$ 时，每个窗口对应一个数组位置，所以值出现于多少个窗口恰等于它的全局频率；
算法从大到小选择频率 1 的值，正确。

当 $k=n$ 时只有一个窗口。每个出现过的值都出现于这唯一窗口，最大者就是答案。

最后考虑 $1<k<n$。位置 0 只被起点 0 的窗口包含，位置 $n-1$ 只被起点 $n-k$
的窗口包含。对任意内部位置 $i$，既能找到一个包含它且尽量向左的窗口，也能找到另一个
起点不同且包含它的窗口，所以其覆盖数至少为 2。故合格值只能来自首尾。端点值若全局唯一，
恰好只在对应端点窗口出现；若还在其他位置出现，则至少再进入一个窗口而不合格。算法检查
且仅检查这两个必要充分候选并取最大值，因此正确。

## 同阶方案比较

可以为每个值维护出现位置，并合并它覆盖的窗口起点区间。这一通用方法也能做到当前规模下
的线性或近线性复杂度，且可回答“恰好出现于 $q$ 个窗口”的追问；但本题的三个 `k` 情形
把通用区间并压缩成更短的证明和实现。面试中优先记忆分类结论，同时理解区间覆盖模型，
避免只背“看首尾”而无法解释边界。

## 易错点

- 把一个值在窗口内的出现次数当成窗口数，没有先去重。
- 在 $k=n$ 时仍要求全局频率为 1；重复值也只属于唯一窗口。
- 在中间情形只检查端点，却忘记端点值可能在内部或另一端重复。
- 把首尾相同的两个候选当成各自只出现一次。
- 用 0 作为无解初值，无法区分合法答案 0。

## 验证说明

暴力滑窗版与分类最优版均以 GNU++23 编译，并通过全部官方样例及上述边界。对值域
`0..3`、长度 1 到 8、所有合法 `k` 进行全量穷举，以逐窗口集合统计为 oracle；再对官方
范围随机数组差分，结果全部一致。

## 变种一：返回全部几近缺失整数

新定义：返回所有恰好出现于一个长度为 $k$ 的窗口的值，按降序排列。分类结论不变，只需
收集所有满足条件的值并去重。时间 $O(n+V)$，空间 $O(V)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> nums(n);
  array<int, 51> frequency{};
  for (int& value : nums) {
    cin >> value;
    ++frequency[value];
  }
  vector<int> answer;
  if (k == n) {
    for (int value = 50; value >= 0; --value) {
      if (frequency[value] > 0) answer.push_back(value);
    }
  } else if (k == 1) {
    for (int value = 50; value >= 0; --value) {
      if (frequency[value] == 1) answer.push_back(value);
    }
  } else {
    set<int, greater<int>> candidates;
    if (frequency[nums.front()] == 1) candidates.insert(nums.front());
    if (frequency[nums.back()] == 1) candidates.insert(nums.back());
    answer.assign(candidates.begin(), candidates.end());
  }
  if (answer.empty()) cout << -1;
  else for (int value : answer) cout << value << ' ';
  cout << '\n';
  return 0;
}
```

## 变种二：恰好出现于 q 个窗口

新定义：给定 $q$，返回最大的、恰好被 $q$ 个长度为 $k$ 的窗口包含的值。每个出现位置
$i$ 覆盖一个窗口起点区间；按值收集这些区间并合并，并长就是窗口数。复杂度
$O(n\log n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k, q;
  cin >> n >> k >> q;
  map<int, vector<pair<int, int>>> intervals;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    int left = max(0, i - k + 1);
    int right = min(i, n - k);
    intervals[value].push_back({left, right});
  }
  int answer = -1;
  for (auto& [value, ranges] : intervals) {
    sort(ranges.begin(), ranges.end());
    int covered = 0;
    int left = ranges[0].first;
    int right = ranges[0].second;
    for (int i = 1; i < static_cast<int>(ranges.size()); ++i) {
      if (ranges[i].first > right + 1) {
        covered += right - left + 1;
        left = ranges[i].first;
        right = ranges[i].second;
      } else {
        right = max(right, ranges[i].second);
      }
    }
    covered += right - left + 1;
    if (covered == q) answer = max(answer, value);
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种三：固定 k、单点修改后反复询问

新定义：窗口长度固定，数组支持赋值更新，每次更新后输出当前答案。分类结构仍成立：维护
全局频率；$k=1$ 时维护频率为 1 的值集合，$k=n$ 时维护全部值的多重集合，中间情形只
检查更新后的首尾。每次更新和查询为 $O(\log n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k, queryCount;
  cin >> n >> k >> queryCount;
  vector<int> nums(n);
  map<int, int> frequency;
  multiset<int> values;
  for (int& value : nums) {
    cin >> value;
    ++frequency[value];
    values.insert(value);
  }
  set<int> uniqueValues;
  for (auto [value, count] : frequency) {
    if (count == 1) uniqueValues.insert(value);
  }
  auto changeFrequency = [&](int value, int delta) {
    uniqueValues.erase(value);
    frequency[value] += delta;
    if (frequency[value] == 1) uniqueValues.insert(value);
    if (frequency[value] == 0) frequency.erase(value);
  };
  while (queryCount--) {
    int index, value;
    cin >> index >> value;
    values.erase(values.find(nums[index]));
    changeFrequency(nums[index], -1);
    nums[index] = value;
    changeFrequency(value, 1);
    values.insert(value);
    int answer = -1;
    if (k == n) answer = *values.rbegin();
    else if (k == 1) {
      if (!uniqueValues.empty()) answer = *uniqueValues.rbegin();
    } else {
      if (frequency[nums.front()] == 1) answer = nums.front();
      if (frequency[nums.back()] == 1) answer = max(answer, nums.back());
    }
    cout << answer << '\n';
  }
  return 0;
}
```

## 变种四：把连续子数组改为固定长度子序列

新定义：在 $n\le60$ 时，统计包含某个值的长度为 $k$ 的下标子序列数。若该值全局出现
$c$ 次，包含它的子序列数为 $\binom nk-\binom{n-c}k$。$\binom{60}{30}$ 仍在
`unsigned long long` 范围内；对每个不同值计算后取计数等于 1 的最大者。设不同值数为
$u$，复杂度 $O(un)$，空间 $O(u)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
unsigned long long choose(int n, int k) {
  if (k < 0 || k > n) return 0;
  k = min(k, n - k);
  unsigned long long result = 1;
  for (int i = 1; i <= k; ++i) {
    result *= n - k + i;
    result /= i;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  map<int, int> frequency;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++frequency[value];
  }
  unsigned long long total = choose(n, k);
  int answer = -1;
  for (auto [value, count] : frequency) {
    unsigned long long containing = total - choose(n - count, k);
    if (containing == 1) answer = max(answer, value);
  }
  cout << answer << '\n';
  return 0;
}
```

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/find-the-largest-almost-missing-integer/)
- [第 439 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-439/)
- [ZeroTracer 社区估算数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-the-largest-almost-missing-integer/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-a/">← [codeforces] CF Round 1117 Div.2 A Creating Abbreviations</a>
<span class="daily-archive-pager__empty"></span>
</nav>
