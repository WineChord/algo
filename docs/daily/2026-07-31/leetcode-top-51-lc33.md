---
title: "[力扣 Top 51] LC 33 搜索旋转排序数组 中等"
---

# [力扣 Top 51] LC 33 搜索旋转排序数组 中等

<p class="daily-archive-kicker">2026-07-31 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=e23f10df22c10bf7f831f54fa95df8d5fe777b4de06b3f21fed0983dc29ca632 -->
## 官方原始信息

- Top 排名：51
- 题号：LC 33
- 官方中文标题：搜索旋转排序数组
- 官方难度：中等
- 官方链接：[搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)

### 原始题意

互异整数数组原本严格升序，随后在未知下标左旋。给定旋转后的 `nums` 与 `target`，返回目标下标；不存在则返回 -1。必须达到 $O(\log n)$。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int search(vector<int>& nums, int target);
};
```

### 全部官方样例

```text
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
```

```text
输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
```

```text
输入：nums = [1], target = 0
输出：-1
```

### 全部约束

- $1\le n\le5000$。
- $-10^4\le nums_i,target\le10^4$。
- `nums` 中的值互不相同。
- 数组由严格升序数组旋转得到。

## 约束推导与边界

线性扫描正确但不满足指定复杂度。旋转数组整体未必有序，但任意二分中点都会让左右至少一半仍严格有序；只需判断目标是否落在该有序半段内。单元素、未旋转、旋转点在首尾、目标不存在都由同一闭区间模板覆盖。

## 解法递进

### 解法一：线性扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int search(vector<int>& nums, int target) {
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (nums[i] == target) {
        return i;
      }
    }
    return -1;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

### 最佳实用解：每轮识别有序半段

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int search(vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;
    while (left <= right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] == target) {
        return middle;
      }
      if (nums[left] <= nums[middle]) {
        if (nums[left] <= target && target < nums[middle]) {
          right = middle - 1;
        } else {
          left = middle + 1;
        }
      } else {
        if (nums[middle] < target && target <= nums[right]) {
          left = middle + 1;
        } else {
          right = middle - 1;
        }
      }
    }
    return -1;
  }
};
```

时间 $O(\log n)$，空间 $O(1)$。

## 正确性证明

在任意区间 `[left,right]` 中，若 `nums[left] <= nums[middle]`，左半段严格有序；否则右半段严格有序。目标若位于有序半段的值域内，就只能在该半段；否则只能在另一半。每轮保留仍可能含目标的区间并至少删去一半。找到时返回真实下标；区间为空时目标不存在。

## 样例手推

对 `[4,5,6,7,0,1,2]` 查找 0：中点值 7，左半有序但 0 不在 `[4,7)`，转向右半；新中点值 1，左半 `[0,1]` 有序且包含 0，最终定位下标 4。

## 易错点与方案比较

- 判断左半有序要用 `<=`，以覆盖单元素区间。
- 有序值域一端含等号、另一端不含，避免重复保留中点。
- 本题值互异；允许重复后无法总在 $O(\log n)$ 内辨认有序半段。
- 推荐记忆闭区间不变量和“先判哪半有序，再判目标是否落入”。

## 变种一：数组允许重复值

当首、中、尾相等时无法判断旋转点在哪侧，只能同时收缩两端，最坏退化为 $O(n)$。

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
  int right = n - 1;
  while (left <= right) {
    int middle = left + (right - left) / 2;
    if (a[middle] == target) {
      cout << "YES\n";
      return 0;
    }
    if (a[left] == a[middle] && a[middle] == a[right]) {
      ++left;
      --right;
    } else if (a[left] <= a[middle]) {
      if (a[left] <= target && target < a[middle]) {
        right = middle - 1;
      } else {
        left = middle + 1;
      }
    } else if (a[middle] < target && target <= a[right]) {
      left = middle + 1;
    } else {
      right = middle - 1;
    }
  }
  cout << "NO\n";
}
```

平均 $O(\log n)$，最坏 $O(n)$，空间 $O(1)$。

## 变种二：求旋转点

新定义：返回最小元素下标，也就是左旋后的断点。

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
  int left = 0;
  int right = n - 1;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (a[middle] > a[right]) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  cout << left << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。

## 变种三：同一数组上有多次查询

预处理旋转点。把逻辑有序下标 `i` 映射到真实下标 `(i+pivot)%n`，每次做普通二分。

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
  int left = 0;
  int right = n - 1;
  while (left < right) {
    int middle = left + (right - left) / 2;
    if (a[middle] > a[right]) {
      left = middle + 1;
    } else {
      right = middle;
    }
  }
  int pivot = left;
  while (q--) {
    int target;
    cin >> target;
    int low = 0;
    int high = n;
    while (low < high) {
      int middle = low + (high - low) / 2;
      int index = (middle + pivot) % n;
      if (a[index] < target) {
        low = middle + 1;
      } else {
        high = middle;
      }
    }
    int index = low == n ? -1 : (low + pivot) % n;
    cout << (index != -1 && a[index] == target ? index : -1) << '\n';
  }
}
```

预处理 $O(\log n)$，每次查询 $O(\log n)$。

## 变种四：统计目标出现次数

允许重复值，并给定一个有效旋转点；两段各自非降，用两次二分统计。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, pivot, target;
  cin >> n >> pivot >> target;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  auto countRange = [&](int left, int right) {
    auto first = lower_bound(a.begin() + left, a.begin() + right, target);
    auto last = upper_bound(a.begin() + left, a.begin() + right, target);
    return last - first;
  };
  cout << countRange(0, pivot) + countRange(pivot, n) << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$；若旋转点也未知且重复值很多，定位断点最坏为 $O(n)$。

## 可复现验证

- 覆盖全部官方样例和未旋转、单元素、目标在两段边界的情况。
- 对小规模严格升序数组枚举所有旋转点与目标，与线性扫描随机对拍。
- 所有完整代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/search-in-rotated-sorted-array/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/search-in-rotated-sorted-array/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc468-f/">← [atcoder] ABC468 F Chmax</a>
<a class="daily-archive-pager__next" href="../leetcode-top-52-lc55/">[力扣 Top 52] LC 55 跳跃游戏 中等 →</a>
</nav>
