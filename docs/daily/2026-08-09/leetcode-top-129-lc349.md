---
title: "[力扣 Top 129] LC 349 两个数组的交集 简单"
---

# [力扣 Top 129] LC 349 两个数组的交集 简单

<p class="daily-archive-kicker">2026-08-09 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c3013d8f0843f88341234679e75ec13b474985278245d4d2e6a8e831d05c06de -->
## 官方原始信息

- Top 排名：129
- 题号：LC 349
- 官方中文标题：两个数组的交集
- 官方难度：简单
- 官方链接：[两个数组的交集](https://leetcode.cn/problems/intersection-of-two-arrays/)

### 原始题意与函数签名

给定两个整数数组，返回它们的集合交集。结果中每个值必须唯一，输出顺序任意。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> intersection(vector<int>& nums1, vector<int>& nums2);
};
```

### 全部官方样例

```text
输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2]
```

```text
输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[9,4]
解释：[4,9] 也正确，顺序不作要求。
```

### 全部约束

- $1\le |nums1|,|nums2|\le1000$。
- $0\le nums1_i,nums2_i\le1000$。

## 约束推导与观察

“交集”按集合语义去重。值域仅 0 到 1000，可用布尔表达到确定性的线性时间和常数值域空间；若忽略小值域，哈希集合是通用选择。数组长度小但双循环仍可能做 $10^6$ 次比较。

## 解法递进

### 解法一：双循环并在结果中去重

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
    vector<int> answer;
    for (int x : nums1) {
      for (int y : nums2) {
        if (x == y && find(answer.begin(), answer.end(), x) == answer.end()) {
          answer.push_back(x);
        }
      }
    }
    return answer;
  }
};
int main() {
}
```

最坏时间 $O(nm+u^2)$，其中 $u$ 为交集不同值数；输出外空间 $O(1)$。

### 解法二：排序后双指针

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
    sort(nums1.begin(), nums1.end());
    sort(nums2.begin(), nums2.end());
    vector<int> answer;
    int i = 0;
    int j = 0;
    while (i < static_cast<int>(nums1.size()) && j < static_cast<int>(nums2.size())) {
      if (nums1[i] < nums2[j]) {
        ++i;
      } else if (nums1[i] > nums2[j]) {
        ++j;
      } else {
        if (answer.empty() || answer.back() != nums1[i]) {
          answer.push_back(nums1[i]);
        }
        ++i;
        ++j;
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n\log n+m\log m)$，排序栈空间视实现而定；会修改输入数组。

### 最佳实用解：布尔存在表

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
    array<bool, 1001> present{};
    for (int x : nums1) {
      present[x] = true;
    }
    vector<int> answer;
    for (int x : nums2) {
      if (present[x]) {
        answer.push_back(x);
        present[x] = false;
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n+m)$、空间 $O(1001)$。把命中位立即清零同时完成去重；本题优先记忆值域表，通用大值域则改用 `unordered_set`。

## 正确性证明

扫描 `nums1` 后，`present[x]` 当且仅当值 `x` 属于第一个数组。扫描 `nums2` 时，只有 `present[x]` 为真才输出，所以每个输出值属于两数组交集；首次输出后清零，保证同一值不再输出。任意交集值在 `nums1` 中令对应位为真，并在 `nums2` 首次出现时被输出，因此没有遗漏。

## 样例手推

样例 1 建表后 1、2 为真。扫描 `nums2` 的第一个 2 时输出并清零，第二个 2 被忽略，结果只有 `[2]`。样例 2 按 `nums2` 顺序可输出 `[9,4]`，题面允许任意顺序。

## 易错点与方案比较

- 题目要集合交集，不按重复次数输出。
- 布尔表大小需要覆盖端点 1000，共 1001 个位置。
- 清零只影响去重，不影响正确性，因为同一值只需输出一次。
- 排序方案会修改输入；若调用者要求保留，需排序副本。

## 变种一：按最小出现次数保留重复值

对应 [LC 350 两个数组的交集 II](https://leetcode.cn/problems/intersection-of-two-arrays-ii/)。改为频次表，每次命中消耗一次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> intersect(vector<int>& nums1, vector<int>& nums2) {
    array<int, 1001> count{};
    for (int x : nums1) {
      ++count[x];
    }
    vector<int> answer;
    for (int x : nums2) {
      if (count[x] > 0) {
        answer.push_back(x);
        --count[x];
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n+m)$、空间 $O(1001)$。

## 变种二：结果必须保持 `nums1` 首次出现顺序

新定义：交集值按它在 `nums1` 中首次出现的顺序返回。先建 `nums2` 集合，再扫描 `nums1`，命中后从集合删除。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> stableIntersection(const vector<int>& a, const vector<int>& b) {
  unordered_set<int> available(b.begin(), b.end());
  vector<int> answer;
  for (int x : a) {
    if (available.erase(x)) {
      answer.push_back(x);
    }
  }
  return answer;
}
int main() {
  for (int x : stableIntersection({4, 9, 4, 5}, {9, 4})) {
    cout << x << ' ';
  }
}
```

期望时间 $O(n+m)$、空间 $O(m)$。

## 变种三：第二个数组是无法全部装入内存的数据流

新定义：第一个数组可驻留内存，第二个数组逐项到达。保存第一个数组的集合；流中首次命中时输出并删除。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> intersectStream(const vector<int>& small, istream& stream) {
  unordered_set<int> needed(small.begin(), small.end());
  vector<int> answer;
  int value;
  while (stream >> value) {
    if (needed.erase(value)) {
      answer.push_back(value);
    }
  }
  return answer;
}
int main() {
  istringstream input("2 2 3 9");
  cout << intersectStream({1, 2, 3}, input).size() << '\n';
}
```

期望时间 $O(n+m)$，内存只与较小数组不同值数有关。

## 变种四：求 `k` 个数组的集合交集

新定义：一个值必须出现在全部数组中。逐轮维护当前交集，避免把同一数组的重复值多计。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> intersectMany(const vector<vector<int>>& arrays) {
  if (arrays.empty()) {
    return {};
  }
  unordered_set<int> current(arrays[0].begin(), arrays[0].end());
  for (int i = 1; i < static_cast<int>(arrays.size()); ++i) {
    unordered_set<int> seen(arrays[i].begin(), arrays[i].end());
    for (auto it = current.begin(); it != current.end();) {
      if (!seen.count(*it)) {
        it = current.erase(it);
      } else {
        ++it;
      }
    }
  }
  return {current.begin(), current.end()};
}
int main() {
  cout << intersectMany({{1, 2, 3}, {2, 3}, {0, 2}}).size() << '\n';
}
```

期望时间与全部输入元素总数成线性关系，空间为当前交集与单个数组的不同值数。

## 可复现验证

对两数组长度 $1..30$、值域 `0..20` 的随机实例，以 `std::set_intersection` 作用于去重有序集合为 oracle，对比布尔表、哈希和双指针结果集合；固定覆盖全重复、无交集、完全相同。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/intersection-of-two-arrays/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-128-lc93/">← [力扣 Top 128] LC 93 复原 IP 地址 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-130-lc437/">[力扣 Top 130] LC 437 路径总和 III 中等 →</a>
</nav>
