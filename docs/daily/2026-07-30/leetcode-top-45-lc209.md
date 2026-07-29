---
title: "[力扣 Top 45] LC 209 长度最小的子数组 中等"
---

# [力扣 Top 45] LC 209 长度最小的子数组 中等

<p class="daily-archive-kicker">2026-07-30 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=441835f624b9943627b53a95ed91349676cf7afef789f9d6e6a39a632361d5b4 -->
## 官方原始信息

- Top 排名：45
- 题号：LC 209
- 官方中文标题：长度最小的子数组
- 官方难度：中等
- 官方链接：[长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/)

### 原始题意

给定由 `n` 个正整数组成的数组和正整数 `target`，求元素和至少为 `target` 的最短非空连续子数组长度；不存在则返回 0。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minSubArrayLen(int target, vector<int>& nums);
};
```

### 全部官方样例

```text
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：[4,3] 是满足条件的最短子数组。
```

```text
输入：target = 4, nums = [1,4,4]
输出：1
```

```text
输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
```

### 全部约束

- $1\le target\le10^9$。
- $1\le n\le10^5$。
- $1\le nums_i\le10^4$。
- 前缀和最大可达 $10^9$，当前约束下 `int` 勉强足够；为扩展与防边界误判，统一用 `long long`。

## 约束推导与单调性

关键条件是所有元素严格为正：

- 右端点右移时窗口和严格增加；
- 固定右端点，若当前窗口已经达标，左端点右移只会缩短窗口且降低和；
- 一旦某个左端点对当前右端点失效，它对更短窗口也不会重新有效。

这使两个指针都只向右移动，总时间为线性。

## 解法递进

### 解法一：枚举左右端点

固定左端点，累加右端点直到达标。时间最坏 $O(n^2)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minSubArrayLen(int target, vector<int>& nums) {
    int answer = numeric_limits<int>::max();
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      long long sum = 0;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        sum += nums[right];
        if (sum >= target) {
          answer = min(answer, right - left + 1);
          break;
        }
      }
    }
    return answer == numeric_limits<int>::max() ? 0 : answer;
  }
};
```

### 解法二：前缀和加二分

正数使前缀和严格递增。对每个左端点，在前缀和数组中二分第一个至少为 `prefix[left]+target` 的右边界。时间 $O(n\log n)$、空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minSubArrayLen(int target, vector<int>& nums) {
    int n = nums.size();
    vector<long long> prefix(n + 1);
    for (int i = 0; i < n; ++i) {
      prefix[i + 1] = prefix[i] + nums[i];
    }
    int answer = n + 1;
    for (int left = 0; left < n; ++left) {
      auto it = lower_bound(prefix.begin() + left + 1, prefix.end(), prefix[left] + target);
      if (it != prefix.end()) {
        answer = min(answer, static_cast<int>(it - prefix.begin()) - left);
      }
    }
    return answer == n + 1 ? 0 : answer;
  }
};
```

### 最佳实用解：可变长滑动窗口

每次把右端点加入窗口；只要窗口和达标，就记录长度并不断右移左端点，直到不再达标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minSubArrayLen(int target, vector<int>& nums) {
    int answer = nums.size() + 1;
    int left = 0;
    long long sum = 0;
    for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
      sum += nums[right];
      while (sum >= target) {
        answer = min(answer, right - left + 1);
        sum -= nums[left++];
      }
    }
    return answer == static_cast<int>(nums.size()) + 1 ? 0 : answer;
  }
};
```

时间复杂度 $O(n)$，空间复杂度 $O(1)$。

## 正确性证明

对每个固定右端点 `right`，循环结束前会枚举所有仍满足和至少为 `target` 的左端点，并持续收缩到再右移一步就不满足。由于元素为正，这一时刻得到的最后一个达标窗口是该右端点对应的最短窗口。

左端点从不需要回退：若某个更小左端点已经被移除，它形成的任何未来窗口都包含当前更短窗口之外的正数，只会更长，不可能优于将来的收缩结果。算法对每个右端点取其最短达标窗口，再取全局最小，因此答案正确。

## 样例手推

对 `target=7`、`[2,3,1,2,4,3]`，右端点到 3 时窗口和为 8，依次收缩为 `[3,1,2]` 后不达标，记录长度 4；到 4 时得到 `[3,1,2,4]`，收缩并记录长度 3；到 5 时窗口 `[4,3]` 达标，记录 2，再收缩后失效。最终答案为 2。

## 易错点与方案比较

- 滑动窗口成立依赖所有数为正；允许负数后不能使用同一不变量。
- 条件是“大于等于”，循环应写 `sum >= target`。
- 不存在答案时返回 0，而不是哨兵值。
- 左、右下标均包含时，长度是 `right-left+1`。
- 推荐优先记忆线性滑窗；前缀和二分展示了官方进阶中的 $O(n\log n)$ 方案，也为负数版本的前缀思想做铺垫。

## 变种一：允许负数

新定义：数组元素可正可负，仍求和至少为目标的最短非空子数组。前缀和不再单调，使用单调队列维护前缀和递增的候选下标：当前前缀足够大时弹出队首并更新答案；当前前缀更小则淘汰队尾。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long target;
  cin >> n >> target;
  vector<long long> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    long long value;
    cin >> value;
    prefix[i + 1] = prefix[i] + value;
  }
  deque<int> candidates;
  int answer = n + 1;
  for (int right = 0; right <= n; ++right) {
    while (!candidates.empty() && prefix[right] - prefix[candidates.front()] >= target) {
      answer = min(answer, right - candidates.front());
      candidates.pop_front();
    }
    while (!candidates.empty() && prefix[candidates.back()] >= prefix[right]) {
      candidates.pop_back();
    }
    candidates.push_back(right);
  }
  cout << (answer == n + 1 ? -1 : answer) << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。这正是原滑窗失效后需要更强数据结构的典型转折。

## 变种二：同时返回最短区间

新定义：返回最短长度及其左右下标；若并列，取左端点最小者。在线性滑窗中更新答案时保存区间即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long target;
  cin >> n >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int best_length = n + 1;
  int best_left = -1;
  int best_right = -1;
  int left = 0;
  long long sum = 0;
  for (int right = 0; right < n; ++right) {
    sum += a[right];
    while (sum >= target) {
      int length = right - left + 1;
      if (length < best_length || (length == best_length && left < best_left)) {
        best_length = length;
        best_left = left;
        best_right = right;
      }
      sum -= a[left++];
    }
  }
  if (best_left == -1) {
    cout << "NONE\n";
  } else {
    cout << best_length << ' ' << best_left << ' ' << best_right << '\n';
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：统计和至少为目标的子数组数量

新定义：元素仍为正，统计所有和至少为目标的连续子数组。对每个右端点收缩到最小合法左端点；若窗口 `[left,right]` 达标，则所有更小左端点也达标，数量为 `left+1`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long target;
  cin >> n >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  long long answer = 0;
  long long sum = 0;
  int left = 0;
  for (int right = 0; right < n; ++right) {
    sum += a[right];
    while (left <= right && sum - a[left] >= target) {
      sum -= a[left++];
    }
    if (sum >= target) {
      answer += left + 1;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。计数最多为 $n(n+1)/2$，需使用 `long long`。

## 变种四：流式追加与当前最短答案

新定义：正整数逐个到达，每次追加后输出当前前缀内的全局最短达标长度。维护滑窗和全局最优即可，不需要保存已从左侧移除的元素之外的数据；这里用队列保留当前窗口。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  long long target;
  cin >> q >> target;
  int operations = q;
  queue<int> window;
  long long sum = 0;
  int answer = operations + 1;
  while (q--) {
    int value;
    cin >> value;
    window.push(value);
    sum += value;
    while (sum >= target) {
      answer = min(answer, static_cast<int>(window.size()));
      sum -= window.front();
      window.pop();
    }
    cout << (answer == operations + 1 ? 0 : answer) << '\n';
  }
}
```

每个元素入队、出队各一次，摊还 $O(1)$；空间为当前窗口长度。哨兵使用初始操作数，而不是循环中递减的 `q`。

## 可复现验证

- 官方三个样例及单元素、总和不足、首元素即达标、答案位于尾部均应覆盖。
- 正数小数组可用 $O(n^2)$ 解作为 oracle，与二分及滑窗解对拍。
- 负数变种应与枚举所有区间的 oracle 对拍。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/minimum-size-subarray-sum/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/minimum-size-subarray-sum/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-44-lc28/">← [力扣 Top 44] LC 28 找出字符串中第一个匹配项的下标 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-46-lc739/">[力扣 Top 46] LC 739 每日温度 中等 →</a>
</nav>
