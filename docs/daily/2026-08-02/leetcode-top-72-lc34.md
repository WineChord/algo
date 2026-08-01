---
title: "[力扣 Top 72] LC 34 在排序数组中查找元素的第一个和最后一个位置 中等"
---

# [力扣 Top 72] LC 34 在排序数组中查找元素的第一个和最后一个位置 中等

<p class="daily-archive-kicker">2026-08-02 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a3894e88d60e720f9122d0970d5b8b325b654acfc54560fdd854afb31ffcd089 -->
## 官方原始信息

- Top 排名：72
- 题号：LC 34
- 官方中文标题：在排序数组中查找元素的第一个和最后一个位置
- 官方难度：中等
- 官方链接：[在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)

### 原始题意

给定一个按非递减顺序排列的整数数组 `nums` 与目标值 `target`，返回目标值第一次和最后一次出现的下标；不存在时返回 `[-1,-1]`。要求时间复杂度为 $O(\log n)$。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> searchRange(vector<int>& nums, int target);
};
```

### 全部官方样例

```text
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
```

```text
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
```

```text
输入：nums = [], target = 0
输出：[-1,-1]
```

### 全部约束

- $0\le n\le10^5$。
- $-10^9\le nums_i,target\le10^9$。
- `nums` 非递减。
- 目标时间复杂度为 $O(\log n)$。

## 约束推导与边界

有序性把“等于 `target` 的位置”压成一个连续区间。与其分别寻找某个命中点再向两侧扩张，不如直接寻找两条单调边界：第一个满足 `nums[i] >= target` 的位置，以及第一个满足 `nums[i] > target` 的位置。二者分别是闭区间左端和右端后一位。

不能用 `target+1` 替代严格上界，因为 `target` 可能等于 $10^9$，虽然本题加一仍未溢出 `int`，这种写法在更宽接口上不稳健。空数组的两个边界都为 0，必须在访问前检查左边界是否在数组内且确实等于目标。

## 解法递进

### 解法一：线性扫描

第一次遇到目标时记录左端，持续覆盖右端；由于数组有序，遇到更大值即可停止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> searchRange(vector<int>& nums, int target) {
    int first = -1;
    int last = -1;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] == target) {
        if (first == -1) {
          first = i;
        }
        last = i;
      } else if (nums[i] > target) {
        break;
      }
    }
    return {first, last};
  }
};
```

时间 $O(n)$，额外空间 $O(1)$；正确但没有利用约束要求的对数复杂度。

### 最佳实用解：两次下界二分

统一函数 `firstAtLeast(value)` 返回半开区间 `[0,n]` 中第一个满足 `nums[i] >= value` 的位置；上界则单独用严格比较，避免算术哨兵。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int lowerBound(const vector<int>& nums, int target, bool strict) {
    int left = 0;
    int right = nums.size();
    while (left < right) {
      int middle = left + (right - left) / 2;
      bool moveLeft = strict ? nums[middle] > target : nums[middle] >= target;
      if (moveLeft) {
        right = middle;
      } else {
        left = middle + 1;
      }
    }
    return left;
  }
public:
  vector<int> searchRange(vector<int>& nums, int target) {
    int first = lowerBound(nums, target, false);
    if (first == static_cast<int>(nums.size()) || nums[first] != target) {
      return {-1, -1};
    }
    int afterLast = lowerBound(nums, target, true);
    return {first, afterLast - 1};
  }
};
```

时间 $O(\log n)$，额外空间 $O(1)$。

## 正确性证明

在下界二分中维护：`[0,left)` 全部不满足边界谓词，`[right,n)` 全部满足。检查中点后，若满足就令 `right=middle`，否则令 `left=middle+1`，不变量保持。终止时 `left==right`，其左侧全不满足、该位置起全满足，所以它是第一满足位置。

非严格边界给出第一个 `>= target` 的位置。若该位置越界或不等于目标，数组中不存在目标。否则严格边界给出第一个 `> target` 的位置；由于相等值连续，两边界之间恰好全是目标，故返回 `[first,afterLast-1]` 正确。

## 样例手推

`[5,7,7,8,8,10]` 中，第一个 `>=8` 的位置为 3，第一个 `>8` 的位置为 5，答案 `[3,4]`。对目标 6，第一个 `>=6` 的位置为 1，但 `nums[1]=7`，因此不存在。空数组边界为 0，越界检查直接返回 `[-1,-1]`。

## 易错点与方案比较

- 二分区间采用 `[left,right)`；初始化 `right=n`，答案允许等于 $n$。
- 右端点是“第一个大于目标的位置减一”，不是另一套模糊的命中二分。
- 必须先检查左边界有效再访问 `nums[first]`。
- 命中后线性扩张在全数组相等时退化到 $O(n)$。
- 推荐统一记忆“下界／上界描述谓词”，比死记四种开闭区间更稳定。

## 变种一：只统计目标出现次数

新定义：不返回下标，只返回目标出现次数。严格上界减非严格下界即为连续区间长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int boundary(const vector<int>& a, int target, bool strict) {
  int left = 0;
  int right = a.size();
  while (left < right) {
    int middle = (left + right) / 2;
    if (strict ? a[middle] > target : a[middle] >= target) {
      right = middle;
    } else {
      left = middle + 1;
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
  cout << boundary(a, target, true) - boundary(a, target, false) << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。

## 变种二：只在给定下标子区间中查找

新定义：每次给出半开下标区间 `[L,R)`，只在其中找目标边界。二分初始区间改为查询范围即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int boundary(const vector<int>& a, int left, int right, int target, bool strict) {
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (strict ? a[middle] > target : a[middle] >= target) {
      right = middle;
    } else {
      left = middle + 1;
    }
  }
  return left;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, left, right, target;
  cin >> n >> left >> right >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int first = boundary(a, left, right, target, false);
  int after = boundary(a, left, right, target, true);
  if (first == after) {
    cout << -1 << ' ' << -1 << '\n';
  } else {
    cout << first << ' ' << after - 1 << '\n';
  }
}
```

每次查询 $O(\log(R-L))$，空间 $O(1)$。

## 变种三：同一数组回答大量目标值

新定义：给定 $Q$ 个独立目标。数组保持有序，每个目标仍做两次二分；无需额外预处理。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int boundary(const vector<int>& a, int target, bool strict) {
  int left = 0;
  int right = a.size();
  while (left < right) {
    int middle = (left + right) / 2;
    if (strict ? a[middle] > target : a[middle] >= target) {
      right = middle;
    } else {
      left = middle + 1;
    }
  }
  return left;
}
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
    int first = boundary(a, target, false);
    int after = boundary(a, target, true);
    cout << (first == after ? -1 : first) << ' ' << (first == after ? -1 : after - 1) << '\n';
  }
}
```

总时间 $O(Q\log n)$，额外空间 $O(1)$。

## 变种四：固定下标数组支持点修改与位置查询

新定义：数组不再有序，但长度固定；支持把位置 `i` 改成新值，以及查询某值当前最左／最右位置。二分原数组失效，为每个值维护有序下标集合。

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
  unordered_map<int, set<int>> positions;
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
    positions[a[i]].insert(i);
  }
  while (q--) {
    char type;
    cin >> type;
    if (type == 'U') {
      int index, value;
      cin >> index >> value;
      positions[a[index]].erase(index);
      a[index] = value;
      positions[value].insert(index);
    } else {
      int target;
      cin >> target;
      auto& indices = positions[target];
      if (indices.empty()) {
        cout << -1 << ' ' << -1 << '\n';
      } else {
        cout << *indices.begin() << ' ' << *indices.rbegin() << '\n';
      }
    }
  }
}
```

每次修改和查询为 $O(\log n)$，总空间 $O(n)$；这是静态有序性消失后必须换数据结构的边界。

## 验证说明

最优解与线性扫描对 10000 个随机非递减数组及随机目标逐项对拍，并覆盖空数组、全相等、目标在两端和目标缺失；六段 C++23 代码均通过编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-71-lc912/">← [力扣 Top 71] LC 912 排序数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-73-lc322/">[力扣 Top 73] LC 322 零钱兑换 中等 →</a>
</nav>
