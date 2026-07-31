---
title: "[力扣 Top 59] LC 35 搜索插入位置 简单"
---

# [力扣 Top 59] LC 35 搜索插入位置 简单

<p class="daily-archive-kicker">2026-07-31 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=97a2cecc5206ef46acf7ac4851fd80d9643836cd273a25e26d83ecf844afe14c -->
## 官方原始信息

- Top 排名：59
- 题号：LC 35
- 官方中文标题：搜索插入位置
- 官方难度：简单
- 官方链接：[搜索插入位置](https://leetcode.cn/problems/search-insert-position/)

### 原始题意

给定严格升序、元素互异的整数数组 `nums` 和目标值 `target`。若目标存在，返回其下标；否则返回按顺序插入后的位置。要求 $O(\log n)$。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int searchInsert(vector<int>& nums, int target);
};
```

### 全部官方样例

```text
输入：nums = [1,3,5,6], target = 5
输出：2
```

```text
输入：nums = [1,3,5,6], target = 2
输出：1
```

```text
输入：nums = [1,3,5,6], target = 7
输出：4
```

### 全部约束

- $1\le |nums|\le10^4$。
- $-10^4\le nums_i,target\le10^4$。
- `nums` 严格升序，且所有值互不相同。

## 约束推导与边界

答案正是第一个大于等于 `target` 的位置，也就是 `lower_bound`。插入点可能为 0，也可能为 `n`，所以半开区间 `[left,right)` 比闭区间更自然：`right=n` 本身就是合法答案。严格升序让命中下标唯一，但算法也可直接推广到重复值数组的首次出现位置。

## 解法递进

### 解法一：线性寻找第一个不小于目标的位置

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int searchInsert(vector<int>& nums, int target) {
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] >= target) {
        return i;
      }
    }
    return nums.size();
  }
};
```

时间 $O(n)$，空间 $O(1)$。

### 最佳实用解：半开区间二分下界

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int searchInsert(vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] < target) {
        left = middle + 1;
      } else {
        right = middle;
      }
    }
    return left;
  }
};
```

时间 $O(\log n)$，空间 $O(1)$。

## 正确性证明

循环始终保持：`left` 左侧所有元素都小于 `target`，`right` 及其右侧的数组内元素都大于等于 `target`，答案位于 `[left,right]`。若中点值小于目标，中点及其左侧不可能是答案，令 `left=middle+1`；否则中点可能是首个合格位置，保留它并令 `right=middle`。区间长度严格缩小；结束时 `left==right`，由两侧性质可知它恰为第一个不小于目标的位置。

## 样例手推

`[1,3,5,6]` 查找 2：初始 `[0,4)`，中点 2 的值 5 不小于 2，右端变 2；中点 1 的值 3 不小于 2，右端变 1；中点 0 的值 1 小于 2，左端变 1，返回 1。

## 易错点与方案比较

- 半开区间模板的初始右端是 `n`，不是 `n-1`。
- `nums[middle] < target` 才丢弃中点；相等时要继续向左寻找下界。
- 中点用 `left + (right-left)/2`，避免通用大范围整数溢出。
- 标准库 `lower_bound` 等价；面试中推荐先讲清不变量，再根据约定使用库函数。

## 变种一：相等时插到所有相等元素之后

数组允许重复，求第一个严格大于 `target` 的位置，即 `upper_bound`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, target;
  cin >> n >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int left = 0;
  int right = n;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (a[middle] <= target) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  cout << left << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。

## 变种二：返回目标值的首尾下标

允许重复，分别求 `lower_bound(target)` 与 `upper_bound(target)`；不存在则输出 `-1 -1`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int firstAtLeast(const vector<int>& a, int target) {
  int left = 0;
  int right = a.size();
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (a[middle] < target) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  return left;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, target;
  cin >> n >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int first = firstAtLeast(a, target);
  int after = firstAtLeast(a, target + 1);
  if (first == n || a[first] != target) {
    cout << "-1 -1\n";
  } else {
    cout << first << ' ' << after - 1 << '\n';
  }
}
```

时间 $O(\log n)$，空间 $O(1)$。若 `target` 可能为 `INT_MAX`，第二次边界应直接写 `upper_bound` 比较，不能计算 `target+1`。

## 变种三：数组按严格降序排列

插入后仍保持降序，答案是第一个小于等于目标的位置，比较方向相反。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, target;
  cin >> n >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int left = 0;
  int right = n;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (a[middle] > target) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  cout << left << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。

## 变种四：同一数组上有多次插入位置查询

数组不实际修改，每次独立求下界。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  while (q--) {
    int target;
    cin >> target;
    int left = 0;
    int right = n;
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (a[middle] < target) {
        left = middle + 1;
      } else {
        right = middle;
      }
    }
    cout << left << '\n';
  }
}
```

每次查询 $O(\log n)$，额外空间 $O(1)$。

## 可复现验证

对随机严格升序数组和随机目标，把手写二分与线性扫描、标准库 `lower_bound` 三者比较；覆盖目标小于首项、等于某项、落在间隙和大于末项。重复值变种与 `upper_bound` 交叉核对。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/search-insert-position/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/search-insert-position/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-58-lc51/">← [力扣 Top 58] LC 51 N 皇后 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-60-lc24/">[力扣 Top 60] LC 24 两两交换链表中的节点 中等 →</a>
</nav>
