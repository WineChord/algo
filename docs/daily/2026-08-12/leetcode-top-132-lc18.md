---
title: "[力扣 Top 132] LC 18 四数之和 中等"
---

# [力扣 Top 132] LC 18 四数之和 中等

<p class="daily-archive-kicker">2026-08-12 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-12 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=32dc8bf66de2d636bd4aa03a54e18b0061268039381f003df1ef770807201f20 -->
## 官方原始信息

- 题目：LC 18，四数之和。
- 官方难度：中等。
- 官方链接：[四数之和](https://leetcode.cn/problems/4sum/)。

### 原始题意与函数签名

给定整数数组 `nums` 和整数 `target`，返回所有由四个不同下标组成、元素和等于 `target` 的不重复四元组。每个四元组内部及答案顺序均可任意。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> fourSum(vector<int>& nums, int target);
};
```

### 全部官方样例

```text
输入：nums = [1,0,-1,0,-2,2], target = 0
输出：[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
```

```text
输入：nums = [2,2,2,2,2], target = 8
输出：[[2,2,2,2]]
```

### 全部约束

- $1\le |nums|\le200$。
- $-10^9\le nums_i\le10^9$。
- $-10^9\le target\le10^9$。
- 四个数之和可能达到 $\pm4\times10^9$，超过 32 位有符号整数范围；求和、差值与剪枝必须使用 `long long`。

## 约束推导与观察

$n=200$ 时，$O(n^4)$ 约有 $1.6\times10^9$ 次枚举，无法通过；$O(n^3)$ 约为八百万级，能够接受。排序后固定前两个数，剩余问题就是有序区间中的两数之和，可以用双指针在线性时间完成。排序还让相同值相邻，从而能在每一层统一去重。

## 解法递进

### 解法一：枚举全部下标四元组

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  long long target;
  cin >> n >> target;
  vector<long long> a(n);
  for (long long& x : a) cin >> x;
  set<array<long long, 4>> answer;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      for (int k = j + 1; k < n; ++k) {
        for (int l = k + 1; l < n; ++l) {
          if (a[i] + a[j] + a[k] + a[l] != target) continue;
          array<long long, 4> values{a[i], a[j], a[k], a[l]};
          sort(values.begin(), values.end());
          answer.insert(values);
        }
      }
    }
  }
  cout << answer.size() << '\n';
}
```

它按 $i<j<k<l$ 覆盖所有不同下标，集合负责值级去重。时间 $O(n^4\log A)$，其中 $A$ 为答案数；额外空间 $O(A)$。瓶颈是重复扫描同一后缀。

### 解法二：固定三个数，用散列表寻找第四个数

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  long long target;
  cin >> n >> target;
  vector<long long> a(n);
  for (long long& x : a) cin >> x;
  set<array<long long, 4>> answer;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      unordered_set<long long> seen;
      for (int k = j + 1; k < n; ++k) {
        long long need = target - a[i] - a[j] - a[k];
        if (seen.contains(need)) {
          array<long long, 4> values{a[i], a[j], a[k], need};
          sort(values.begin(), values.end());
          answer.insert(values);
        }
        seen.insert(a[k]);
      }
    }
  }
  cout << answer.size() << '\n';
}
```

散列表消除了最内层枚举，期望时间 $O(n^3)$，空间 $O(n+A)$；但答案集合和散列表带来较大常数，去重逻辑也分散。

### 最佳实用解：排序、两层枚举与双指针

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> fourSum(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    vector<vector<int>> answer;
    for (int i = 0; i + 3 < n; ++i) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      long long smallest = 1LL * nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3];
      if (smallest > target) break;
      long long largest = 1LL * nums[i] + nums[n - 1] + nums[n - 2] + nums[n - 3];
      if (largest < target) continue;
      for (int j = i + 1; j + 2 < n; ++j) {
        if (j > i + 1 && nums[j] == nums[j - 1]) continue;
        int left = j + 1, right = n - 1;
        while (left < right) {
          long long sum = 1LL * nums[i] + nums[j] + nums[left] + nums[right];
          if (sum < target) {
            ++left;
          } else if (sum > target) {
            --right;
          } else {
            answer.push_back({nums[i], nums[j], nums[left], nums[right]});
            int low = nums[left], high = nums[right];
            while (left < right && nums[left] == low) ++left;
            while (left < right && nums[right] == high) --right;
          }
        }
      }
    }
    return answer;
  }
};
int main() {
  vector<int> nums{1, 0, -1, 0, -2, 2};
  cout << Solution().fourSum(nums, 0).size() << '\n';
}
```

排序 $O(n\log n)$，主体 $O(n^3)$，除答案外额外空间取决于排序实现，通常为 $O(\log n)$。相比同阶散列表方案，它直接生成有序且唯一的四元组，常数、证明负担和实现稳定性都更好，面试与竞赛中应优先记忆。

## 正确性证明

固定排序后下标 $i,j$。双指针维护尚未排除的区间 `[left,right]`。若当前和小于目标，因为数组有序，固定 `right` 时任何不大于当前 `left` 的值都不会更大，故只能右移 `left`；大于目标时对称地只能左移 `right`。相等时得到一个合法四元组，并跳过两端相同值；这些相同值只会生成同一个值四元组。

任意合法值四元组按非降序排列后，都对应某组 $i<j<left<right$。外层只跳过相同的首值或次值，保留其第一次出现；双指针又不会跨过仍可能达到目标的组合，所以它必被找到。每层均跳过相同值，因此答案不重复。算法既无遗漏又无重复，结论成立。

## 样例手推、边界与易错点

样例一排序后为 `[-2,-1,0,0,1,2]`。固定 `-2,-1` 时双指针找到 `1,2`；固定 `-2,0` 时找到 `0,2`；固定 `-1,0` 时找到 `0,1`，最终恰好三组。样例二的相同元素在每层都被跳过，只保留 `[2,2,2,2]`。

- $n<4$ 时直接返回空答案。
- 重复值去重必须按“同一层”判断，不能全局跳过。
- 命中后左右两端都要跳过重复值。
- `target` 虽在 32 位范围内，中间四数和不在；先转 `long long` 再相加。
- 最小和剪枝可 `break`，最大和不足只能 `continue`。
- 两个官方样例通过；最优解与四重枚举 oracle 在 30,000 组固定种子随机数组上逐一一致。

## 变种一：通用 K 数之和

新定义：返回和为 `target` 的不重复 $k$ 元组。两数时双指针，其余层递归固定一个数，原理不变，时间 $O(n^{k-1})$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void kSum(const vector<int>& a, int start, int k, long long target,
          vector<int>& path, vector<vector<int>>& answer) {
  if (k == 2) {
    int left = start, right = a.size() - 1;
    while (left < right) {
      long long sum = 1LL * a[left] + a[right];
      if (sum < target) ++left;
      else if (sum > target) --right;
      else {
        path.push_back(a[left]);
        path.push_back(a[right]);
        answer.push_back(path);
        path.pop_back();
        path.pop_back();
        int x = a[left], y = a[right];
        while (left < right && a[left] == x) ++left;
        while (left < right && a[right] == y) --right;
      }
    }
    return;
  }
  for (int i = start; i + k <= static_cast<int>(a.size()); ++i) {
    if (i > start && a[i] == a[i - 1]) continue;
    path.push_back(a[i]);
    kSum(a, i + 1, k - 1, target - a[i], path, answer);
    path.pop_back();
  }
}
int main() {
  vector<int> a{1, 0, -1, 0, -2, 2};
  sort(a.begin(), a.end());
  vector<int> path;
  vector<vector<int>> answer;
  kSum(a, 0, 4, 0, path, answer);
  cout << answer.size() << '\n';
}
```

## 变种二：只返回字典序最小四元组

新定义：若有解，只返回排序后字典序最小的一组。排序枚举的产生顺序就是字典序，首次命中即可结束；时间上界仍为 $O(n^3)$，答案空间降为 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
optional<array<int, 4>> smallestFourSum(vector<int> a, long long target) {
  sort(a.begin(), a.end());
  int n = a.size();
  for (int i = 0; i + 3 < n; ++i) {
    if (i > 0 && a[i] == a[i - 1]) continue;
    for (int j = i + 1; j + 2 < n; ++j) {
      if (j > i + 1 && a[j] == a[j - 1]) continue;
      int left = j + 1, right = n - 1;
      while (left < right) {
        long long sum = 1LL * a[i] + a[j] + a[left] + a[right];
        if (sum < target) ++left;
        else if (sum > target) --right;
        else return array<int, 4>{a[i], a[j], a[left], a[right]};
      }
    }
  }
  return nullopt;
}
int main() {
  auto answer = smallestFourSum({1, 0, -1, 0, -2, 2}, 0);
  if (answer) for (int x : *answer) cout << x << ' ';
  cout << '\n';
}
```

## 变种三：四数和最接近目标

新定义：返回与目标绝对差最小的四数和。失去“命中后去重收集”的需求，但双指针的单调移动仍成立；时间 $O(n^3)$、额外空间 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long fourSumClosest(vector<int> a, long long target) {
  sort(a.begin(), a.end());
  long long best = 1LL * a[0] + a[1] + a[2] + a[3];
  for (int i = 0; i + 3 < static_cast<int>(a.size()); ++i) {
    for (int j = i + 1; j + 2 < static_cast<int>(a.size()); ++j) {
      int left = j + 1, right = a.size() - 1;
      while (left < right) {
        long long sum = 1LL * a[i] + a[j] + a[left] + a[right];
        if (llabs(sum - target) < llabs(best - target)) best = sum;
        if (sum < target) ++left;
        else if (sum > target) --right;
        else return target;
      }
    }
  }
  return best;
}
int main() {
  cout << fourSumClosest({1, 0, -1, 0, -2, 2}, 3) << '\n';
}
```

## 变种四：统计下标四元组数量

新定义：相同值但下标不同的方案分别计数。值级去重反而错误；可枚举中间分界并维护左侧两数和频次，在 $O(n^3)$ 时间、$O(n^2)$ 空间内计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countIndexQuadruples(const vector<int>& a, long long target) {
  unordered_map<long long, long long> leftPairs;
  long long answer = 0;
  for (int k = 1; k + 1 < static_cast<int>(a.size()); ++k) {
    for (int i = 0; i < k; ++i) ++leftPairs[1LL * a[i] + a[k]];
    for (int l = k + 2; l < static_cast<int>(a.size()); ++l) {
      long long need = target - a[k + 1] - a[l];
      if (leftPairs.contains(need)) answer += leftPairs[need];
    }
  }
  return answer;
}
int main() {
  cout << countIndexQuadruples({2, 2, 2, 2, 2}, 8) << '\n';
}
```

## 变种五：同一数组回答多次目标询问

新定义：数组固定，给出多个 `target`。预处理所有下标对并按和分组；每次查询枚举互补和并检查两对下标互异，适合询问很多但 $n$ 较小的场景。预处理 $O(n^2)$，单次最坏 $O(n^4)$，实际取决于命中桶大小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class FourSumQueries {
  unordered_map<long long, vector<pair<int, int>>> pairs;
public:
  explicit FourSumQueries(const vector<int>& a) {
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
      for (int j = i + 1; j < static_cast<int>(a.size()); ++j) {
        pairs[1LL * a[i] + a[j]].push_back({i, j});
      }
    }
  }
  bool exists(long long target) const {
    for (const auto& [sum, first] : pairs) {
      auto it = pairs.find(target - sum);
      if (it == pairs.end()) continue;
      for (auto [i, j] : first) {
        for (auto [k, l] : it->second) {
          if (i != k && i != l && j != k && j != l) return true;
        }
      }
    }
    return false;
  }
};
int main() {
  FourSumQueries queries({1, 0, -1, 0, -2, 2});
  cout << queries.exists(0) << '\n';
}
```

## 验证说明

所有完整代码块均按 C++23 编译。随机验证生成长度 $1$ 到 $11$、值域 $[-8,8]$ 的 30,000 组数组和目标值；把最优解结果内部排序后，与四重枚举得到的集合逐项比较，全部一致。另覆盖空答案、全相等、极值溢出、重复值密集和 $n=4$ 边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/4sum/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc226-a/">← [atcoder] ARC226 A Meeting Division</a>
<a class="daily-archive-pager__next" href="../leetcode-biweekly-188-q3-lc4008/">[力扣竞赛] 第 188 场双周赛 Q3 LC 4008 击败所有怪物的最小初始强度 中等 →</a>
</nav>
