---
title: "[力扣 Top 63] LC 26 删除有序数组中的重复项 简单"
---

# [力扣 Top 63] LC 26 删除有序数组中的重复项 简单

<p class="daily-archive-kicker">2026-08-01 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=55f5d787298bbd0e50851c5eb0998d582e8d42f203a6de70164b5d75f8afc2d0 -->
## 官方原始信息

- Top 排名：63
- 题号：LC 26
- 官方中文标题：删除有序数组中的重复项
- 官方难度：简单
- 官方链接：[删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)

### 原始题意

给定非递减整数数组 `nums`，原地保留每个不同值的第一次出现，并保持相对顺序。返回唯一元素数 $k$；判题只检查 `nums` 的前 $k$ 项，后缀内容可忽略。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int removeDuplicates(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,1,2]
输出：2, nums = [1,2,_]
```

```text
输入：nums = [0,0,1,1,1,2,2,3,3,4]
输出：5, nums = [0,1,2,3,4,_,_,_,_,_]
```

### 全部约束

- $1\le |nums|\le3\times10^4$。
- $-100\le nums_i\le100$。
- `nums` 已按非递减顺序排列。

## 约束推导与边界

有序性保证相同值形成连续段，因此判断“是否第一次出现”只需比较最后一个已保留值，不需要哈希表。题目保证数组非空，写指针可从 1 开始；若把方法迁移到允许空数组的接口，应显式返回 0。

原地要求并不意味着真的缩短 `vector`：只需覆盖前缀。每个元素至多读写一次，目标自然是 $O(n)$ 时间与 $O(1)$ 额外空间。

## 解法递进

### 解法一：构造唯一值副本再写回

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeDuplicates(vector<int>& nums) {
    vector<int> uniqueValues;
    for (int value : nums) {
      if (uniqueValues.empty() || uniqueValues.back() != value) {
        uniqueValues.push_back(value);
      }
    }
    copy(uniqueValues.begin(), uniqueValues.end(), nums.begin());
    return uniqueValues.size();
  }
};
```

时间 $O(n)$，额外空间 $O(n)$。它说明有序性已把问题化为连续段压缩，但不满足原地空间目标。

### 最佳实用解：读写双指针

`read` 扫描所有元素，`write` 指向下一个可写位置。当前值与 `nums[write-1]` 不同时才写入。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeDuplicates(vector<int>& nums) {
    int write = 1;
    for (int read = 1; read < static_cast<int>(nums.size()); ++read) {
      if (nums[read] != nums[write - 1]) {
        nums[write++] = nums[read];
      }
    }
    return write;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## 正确性证明

处理 `read` 之前维持不变量：`nums[0..write)` 恰是已扫描前缀中的全部不同值，按原顺序各出现一次。若新值等于末尾保留值，有序性说明它仍属于同一重复段，忽略后不变量不变；若不同，它必是尚未出现的新值，把它写到 `write` 后前缀仍准确且有序。

循环结束时已扫描整个数组，因此前 `write` 项正是所有唯一值，`write` 就是题目要求的 $k$。

## 样例手推

对 `[0,0,1,1,1,2,2,3,3,4]`，`write` 依次在读到首个 1、2、3、4 时从 1 增至 5；每次写入后前缀分别为 `[0,1]`、`[0,1,2]`、`[0,1,2,3]`、`[0,1,2,3,4]`。所有相同值、全部互异和单元素数组都直接满足不变量。

## 易错点与方案比较

- 比较对象应是最后一个保留值 `nums[write-1]`，不是固定的原数组前项。
- 返回的是长度，不是最后一个下标。
- 不需要清空后缀，也不应调用导致额外移动的 `erase`。
- 副本法与双指针同为线性时间；双指针同时满足原地要求，推荐记忆“读指针看全部、写指针维护答案前缀”。

## 变种一：每个值最多保留两次

新定义：有序数组中每个值最多保留两次。只要当前值不同于写入前缀倒数第二个值，就可以保留。

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
  int write = 0;
  for (int value : a) {
    if (write < 2 || a[write - 2] != value) {
      a[write++] = value;
    }
  }
  cout << write << '\n';
  for (int i = 0; i < write; ++i) {
    cout << a[i] << (i + 1 == write ? '\n' : ' ');
  }
}
```

时间 $O(n)$，空间 $O(1)$。把常数 2 换成参数 $r$，判断 `write<r || a[write-r]!=value` 即可推广为最多保留 $r$ 次。

## 变种二：删除所有等于目标值的元素

新定义：数组无需有序，原地删除指定值。判断条件从“不同于前一个保留值”改为“不同于目标值”。

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
  int write = 0;
  for (int value : a) {
    if (value != target) {
      a[write++] = value;
    }
  }
  cout << write << '\n';
  for (int i = 0; i < write; ++i) {
    cout << a[i] << (i + 1 == write ? '\n' : ' ');
  }
}
```

时间 $O(n)$，空间 $O(1)$，并保持其余元素的相对顺序。

## 变种三：无序数组稳定去重

新定义：输入不再有序，但仍须保留每个值第一次出现的顺序。有序相邻比较失效，需要哈希集合记录已见值。

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
  unordered_set<int> seen;
  int write = 0;
  for (int value : a) {
    if (seen.insert(value).second) {
      a[write++] = value;
    }
  }
  cout << write << '\n';
  for (int i = 0; i < write; ++i) {
    cout << a[i] << (i + 1 == write ? '\n' : ' ');
  }
}
```

期望时间 $O(n)$，空间 $O(u)$，其中 $u$ 为不同值数量。若值域很小可换成位图，若要求确定性可换成平衡树。

## 变种四：输出游程编码

新定义：不仅保留唯一值，还输出每个连续值段的长度。两个指针分别定位一段的左右边界。

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
  vector<pair<int, int>> runs;
  for (int left = 0; left < n;) {
    int right = left + 1;
    while (right < n && a[right] == a[left]) {
      ++right;
    }
    runs.push_back({a[left], right - left});
    left = right;
  }
  cout << runs.size() << '\n';
  for (auto [value, count] : runs) {
    cout << value << ' ' << count << '\n';
  }
}
```

时间 $O(n)$，输出空间 $O(u)$。它把“唯一前缀”扩展为可逆的有序数组压缩。

## 可复现验证

随机生成非递减数组，把双指针前缀与 `sort+unique` 的结果比较；覆盖单元素、全部相同、全部不同、负数跨零和最长重复段。变种一用计数器 oracle 检查每个值最多出现两次。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-62-lc105/">← [力扣 Top 62] LC 105 从前序与中序遍历序列构造二叉树 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-64-lc48/">[力扣 Top 64] LC 48 旋转图像 中等 →</a>
</nav>
