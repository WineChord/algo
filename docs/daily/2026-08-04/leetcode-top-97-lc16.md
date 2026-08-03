---
title: "[力扣 Top 97] LC 16 最接近的三数之和 中等"
---

# [力扣 Top 97] LC 16 最接近的三数之和 中等

<p class="daily-archive-kicker">2026-08-04 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=17275d1646b2e897b7b50cc1b8dc152714a1e5a3861721674d82aa39b1b95cfb -->
## 官方原始信息

- Top 排名：97
- 题号：LC 16
- 官方中文标题：最接近的三数之和
- 官方难度：中等
- 官方链接：[最接近的三数之和](https://leetcode.cn/problems/3sum-closest/)

### 原始题意

给定长度为 $n$ 的整数数组和目标值，从三个不同下标选数，使三数之和与目标值最接近，返回该和。题目保证答案唯一。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int threeSumClosest(vector<int>& nums, int target);
};
```

### 全部官方样例

```text
输入：nums = [-1,2,1,-4], target = 1
输出：2
解释：-1 + 2 + 1 = 2，与 target 的距离最小。
```

```text
输入：nums = [0,0,0], target = 1
输出：0
```

### 全部约束

- $3\le n\le1000$。
- $-1000\le nums[i]\le1000$。
- $-10^4\le target\le10^4$。
- 每组输入存在唯一答案。

## 约束推导与有序双指针

$n=1000$ 排除 $O(n^3)$ 的全枚举，而 $O(n^2)$ 约为百万次操作。排序后固定 `i`，若当前三数和小于目标，移动左指针是唯一可能增大和的单调动作；若大于目标，移动右指针是唯一可能减小和的动作。三数和范围为 $[-3000,3000]$，`int` 安全；实现中用 `long long` 计算距离，避免将来约束放大或对负数调用不安全的 `abs(int)`。

## 解法递进

### 解法一：枚举所有三元组

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int threeSumClosest(vector<int>& nums, int target) {
    int answer = nums[0] + nums[1] + nums[2];
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        for (int k = j + 1; k < n; ++k) {
          int sum = nums[i] + nums[j] + nums[k];
          if (llabs(static_cast<long long>(sum) - target) <
              llabs(static_cast<long long>(answer) - target)) {
            answer = sum;
          }
        }
      }
    }
    return answer;
  }
};
```

时间 $O(n^3)$，额外空间 $O(1)$，只适合作为小规模 oracle。

### 解法二：固定两数，二分第三数

排序后枚举 `i,j`，在后缀中对 `target-nums[i]-nums[j]` 做 `lower_bound`，检查插入点及其前驱。时间 $O(n^2\log n)$，它消除了第三层线性枚举，但仍未充分利用固定 `i` 后的二维单调性。

### 最佳实用解：排序加相向双指针

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int threeSumClosest(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    int answer = nums[0] + nums[1] + nums[2];
    int n = nums.size();
    for (int i = 0; i + 2 < n; ++i) {
      int left = i + 1;
      int right = n - 1;
      while (left < right) {
        int sum = nums[i] + nums[left] + nums[right];
        if (llabs(static_cast<long long>(sum) - target) <
            llabs(static_cast<long long>(answer) - target)) {
          answer = sum;
        }
        if (sum < target) {
          ++left;
        } else if (sum > target) {
          --right;
        } else {
          return target;
        }
      }
    }
    return answer;
  }
};
```

排序 $O(n\log n)$，扫描 $O(n^2)$，额外空间取决于排序实现，通常为 $O(\log n)$。它证明负担小、常数低，是推荐方案。

## 正确性证明

固定 `i` 后，考察有序矩阵 $a_i+a_l+a_r$。若当前和小于目标，保持 `left` 而减小 `right` 只会让和更小，所以这一整批候选都不可能比向右移动 `left` 更接近目标的另一侧；可安全丢弃当前 `left`。当前和大于目标时对称地丢弃当前 `right`。等于目标时距离为 0，已达全局下界。扫描保存所有实际经过候选中的最小距离，而单调淘汰不会遗漏更优候选，因此最终答案全局最优。

## 样例手推、边界与易错点

`[-1,2,1,-4]` 排序为 `[-4,-1,1,2]`。固定 -4 时先得到 -3，再逐步增大；固定 -1 时两端 1 与 2 得到 2，与目标 1 只差 1，最终返回 2。全重复值、目标远离可达区间、最优和位于最小或最大三数处都由相同扫描覆盖。

- 更新答案必须比较绝对距离，而不是直接比较和。
- 不能复用同一下标；初始答案应来自三个真实元素。
- 题目保证唯一答案；若取消保证，需要明确平局规则。
- 跳过重复值只是常数优化，不是正确性所必需。

## 变种一：返回三个原下标

新定义：返回最接近目标的三个原下标。把值与下标绑定后排序，双指针结构不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, target;
  cin >> n >> target;
  vector<pair<int, int>> numbers(n);
  for (int i = 0; i < n; ++i) {
    cin >> numbers[i].first;
    numbers[i].second = i;
  }
  sort(numbers.begin(), numbers.end());
  long long bestDistance = LLONG_MAX;
  array<int, 3> answer{};
  for (int i = 0; i + 2 < n; ++i) {
    int left = i + 1;
    int right = n - 1;
    while (left < right) {
      long long sum = 1LL * numbers[i].first + numbers[left].first + numbers[right].first;
      if (llabs(sum - target) < bestDistance) {
        bestDistance = llabs(sum - target);
        answer = {numbers[i].second, numbers[left].second, numbers[right].second};
      }
      if (sum < target) {
        ++left;
      } else {
        --right;
      }
    }
  }
  sort(answer.begin(), answer.end());
  cout << answer[0] << ' ' << answer[1] << ' ' << answer[2] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$。

## 变种二：答案不唯一时统计最优下标三元组数

新定义：统计达到最小距离的下标三元组数量。双指针跳过区域会漏计平局，直接全枚举最稳妥；适用于 $n\le300$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  long long target;
  cin >> n >> target;
  vector<long long> numbers(n);
  for (long long& value : numbers) {
    cin >> value;
  }
  long long best = LLONG_MAX;
  long long count = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      for (int k = j + 1; k < n; ++k) {
        long long distance = llabs(numbers[i] + numbers[j] + numbers[k] - target);
        if (distance < best) {
          best = distance;
          count = 1;
        } else if (distance == best) {
          ++count;
        }
      }
    }
  }
  cout << best << ' ' << count << '\n';
}
```

时间 $O(n^3)$，空间 $O(1)$。计数目标改变后，原先只保留一个候选的淘汰证明不够。

## 变种三：最接近的 $k$ 数之和

新定义：选择固定的 $k$ 个不同下标，使和最接近目标。排序后递归固定元素，在 $k=2$ 时使用双指针。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long solve(const vector<int>& numbers, int start, int count, long long target) {
  if (count == 2) {
    int left = start;
    int right = numbers.size() - 1;
    long long best = numbers[left] + numbers[right];
    while (left < right) {
      long long sum = numbers[left] + numbers[right];
      if (llabs(sum - target) < llabs(best - target)) {
        best = sum;
      }
      sum < target ? ++left : --right;
    }
    return best;
  }
  long long best = 0;
  bool initialized = false;
  int n = numbers.size();
  for (int i = start; i + count <= n; ++i) {
    long long rest = solve(numbers, i + 1, count - 1, target - numbers[i]);
    long long sum = numbers[i] + rest;
    if (!initialized || llabs(sum - target) < llabs(best - target)) {
      initialized = true;
      best = sum;
    }
  }
  return best;
}
int main() {
  int n, count;
  long long target;
  cin >> n >> count >> target;
  vector<int> numbers(n);
  for (int& value : numbers) {
    cin >> value;
  }
  sort(numbers.begin(), numbers.end());
  cout << solve(numbers, 0, count, target) << '\n';
}
```

对固定 $k$，时间 $O(n^{k-1})$，递归空间 $O(k)$。

## 变种四：同一数组上的多次目标询问

新定义：数组固定，回答 $q$ 个目标。预处理所有不同下标三元组的和并排序，每次二分最近值；当 $q$ 很大且 $n$ 较小时有意义。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, queryCount;
  cin >> n >> queryCount;
  vector<int> numbers(n);
  for (int& value : numbers) {
    cin >> value;
  }
  vector<long long> sums;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      for (int k = j + 1; k < n; ++k) {
        sums.push_back(1LL * numbers[i] + numbers[j] + numbers[k]);
      }
    }
  }
  sort(sums.begin(), sums.end());
  while (queryCount--) {
    long long target;
    cin >> target;
    auto it = lower_bound(sums.begin(), sums.end(), target);
    long long answer = it == sums.end() ? sums.back() : *it;
    if (it != sums.begin() && llabs(*prev(it) - target) < llabs(answer - target)) {
      answer = *prev(it);
    }
    cout << answer << '\n';
  }
}
```

预处理时间与空间 $O(n^3)$，每问 $O(\log n)$；它以大量空间换取查询速度。

## 可复现验证

全部代码块按 GNU++23 编译。最佳解与三重枚举在随机短数组、重复值、负数和远端目标上对拍；同时覆盖 $n=3$、恰好命中目标及两个边界方向。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/3sum-closest/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-96-lc7/">← [力扣 Top 96] LC 7 整数反转 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-98-lc543/">[力扣 Top 98] LC 543 二叉树的直径 简单 →</a>
</nav>
