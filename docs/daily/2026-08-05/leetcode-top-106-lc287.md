---
title: "[力扣 Top 106] LC 287 寻找重复数 中等"
---

# [力扣 Top 106] LC 287 寻找重复数 中等

<p class="daily-archive-kicker">2026-08-05 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../graph/functional-graphs/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b9d7795ec81ee48b597d95361f804cdc2dc2069b7b42b0df5e944f2eeebe5577 -->
## 官方原始信息

- Top 排名：106
- 题号：LC 287
- 官方中文标题：寻找重复数
- 官方难度：中等
- 官方链接：[寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/)

### 原始题意

数组长度为 $n+1$，所有值都在 `[1,n]`。恰有一个数出现两次或多次，其余数各出现一次。返回重复数；不得修改数组，且额外空间必须为 $O(1)$。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int findDuplicate(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,3,4,2,2]
输出：2
```

```text
输入：nums = [3,1,3,4,2]
输出：3
```

```text
输入：nums = [3,3,3,3,3]
输出：3
```

### 全部约束

- $1\le n\le10^5$。
- `nums.length == n + 1`。
- $1\le nums[i]\le n$。
- 只有一个整数出现两次或多次，其余整数各出现一次。
- 解法不得修改 `nums`，且只能使用 $O(1)$ 额外空间。
- 进阶目标为线性时间。

## 约束推导与观察

$n+1$ 个位置映射到仅 $n$ 个值，鸽巢原理保证重复。把每个下标 `i` 的下一跳定义为 `nums[i]`：从下标 0 出发后始终落在 `[1,n]`，有限状态必进入环。唯一重复值有至少两个不同前驱，恰是从 0 出发函数图中的入环点。

所有下标和值都在 `int` 范围，不涉及算术溢出。Floyd 判圈只读数组并维护常数个下标，正好同时满足两个限制。

## 解法递进

### 解法一：哈希集合

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int value : nums) {
      if (!seen.insert(value).second) {
        return value;
      }
    }
    return -1;
  }
};
```

平均时间 $O(n)$，空间 $O(n)$，违反常量空间要求。

### 解法二：值域二分计数

若 `[1,middle]` 中数组元素个数大于 `middle`，重复值必在左半值域；否则在右半。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findDuplicate(vector<int>& nums) {
    int left = 1;
    int right = nums.size() - 1;
    while (left < right) {
      int middle = left + (right - left) / 2;
      int count = 0;
      for (int value : nums) {
        count += value <= middle;
      }
      if (count > middle) {
        right = middle;
      } else {
        left = middle + 1;
      }
    }
    return left;
  }
};
```

时间 $O(n\log n)$，空间 $O(1)$，不修改输入。它不依赖函数图，但尚未达到线性进阶目标。

### 最佳实用解：Floyd 环入口

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findDuplicate(vector<int>& nums) {
    int slow = nums[0];
    int fast = nums[0];
    do {
      slow = nums[slow];
      fast = nums[nums[fast]];
    } while (slow != fast);
    slow = nums[0];
    while (slow != fast) {
      slow = nums[slow];
      fast = nums[fast];
    }
    return slow;
  }
};
```

时间 $O(n)$，空间 $O(1)$，只读数组，达到全部要求。推荐记忆“值作下一下标、重复值是环入口”的模型，而非死记指针代码。

## 正确性证明

从 0 沿 `f(i)=nums[i]` 行走，后续节点均在 `[1,n]`，因此最终进入一个环。因只有一个数重复，其值对应的节点有至少两个前驱：一条来自入环前路径，另一条来自环内；它就是环入口。Floyd 第一阶段快慢指针必在环内相遇。设起点到入口距离为 $\mu$、环长为 $\lambda$，相遇点距入口为满足同余关系的位置；把慢指针重置到起点后，两指针同速前进，经过 $\mu$ 步恰在入口相遇。返回值因此就是唯一重复数。

## 样例手推

`[1,3,4,2,2]` 形成 `0→1→3→2→4→2...`，环入口为 2。`[3,3,3,3,3]` 从 `0→3→3`，入口仍为重复值 3。最小 `n=1` 时数组只能是 `[1,1]`，算法在 1 相遇并返回 1。

## 易错点与方案比较

- 这是在“值域”上二分，不是对未排序数组下标二分。
- Floyd 的起点统一设为 `nums[0]`，避免 0 不在值域导致证明混乱。
- `fast = nums[nums[fast]]` 的两次数组访问都安全，因为值在 `[1,n]`。
- 哈希最直观；值域二分约束更宽；Floyd 在唯一重复、值可作下标时同时最优。

## 变种一：允许修改数组

新定义：可原地重排。把每个值 `v` 交换到下标 `v`；若目标位置已经存同值，则找到重复。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> values(n + 1);
  for (int& value : values) {
    cin >> value;
  }
  while (values[0] != values[values[0]]) {
    swap(values[0], values[values[0]]);
  }
  cout << values[0] << '\n';
}
```

时间 $O(n)$，空间 $O(1)$，但破坏输入；原题明确禁止这种方案。

## 变种二：数组中一个数缺失、另一个数出现两次

新定义：长度为 $n$，值域 `[1,n]`。同时返回重复值与缺失值。用和与平方和建立两元方程，并用 64 位避免溢出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n;
  cin >> n;
  long long sum = 0;
  long long squareSum = 0;
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    sum += value;
    squareSum += 1LL * value * value;
  }
  long long expectedSum = n * (n + 1) / 2;
  long long expectedSquares = n * (n + 1) * (2 * n + 1) / 6;
  long long difference = sum - expectedSum;
  long long sumOfPair = (squareSum - expectedSquares) / difference;
  long long duplicate = (difference + sumOfPair) / 2;
  long long missing = duplicate - difference;
  cout << duplicate << ' ' << missing << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。这里函数图不再直接给出缺失值，代数不变量更合适。

## 变种三：返回重复数的出现次数

新定义保持原约束，但还要返回频次。Floyd 找值后再线性扫描计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> values(n + 1);
  for (int& value : values) {
    cin >> value;
  }
  int slow = values[0];
  int fast = values[0];
  do {
    slow = values[slow];
    fast = values[values[fast]];
  } while (slow != fast);
  slow = values[0];
  while (slow != fast) {
    slow = values[slow];
    fast = values[fast];
  }
  int frequency = count(values.begin(), values.end(), slow);
  cout << slow << ' ' << frequency << '\n';
}
```

时间 $O(n)$，空间 $O(1)$；恢复次数需要额外一遍，但不改变渐进复杂度。

## 变种四：一般函数图中求环入口和环长

新定义：给定 `next[0..n-1]`，每个节点恰有一条出边，并给起点。返回从起点可达的环入口与环长。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, start;
  cin >> n >> start;
  vector<int> next(n);
  for (int& node : next) {
    cin >> node;
  }
  int slow = start;
  int fast = start;
  do {
    slow = next[slow];
    fast = next[next[fast]];
  } while (slow != fast);
  slow = start;
  while (slow != fast) {
    slow = next[slow];
    fast = next[fast];
  }
  int entry = slow;
  int length = 1;
  for (int node = next[entry]; node != entry; node = next[node]) {
    ++length;
  }
  cout << entry << ' ' << length << '\n';
}
```

时间 $O(\mu+\lambda)$，空间 $O(1)$。本题是该通用模型在数组值域上的特例。

## 验证说明

本轮将七段代码按 C++23 编译；Floyd 与值域二分会与哈希 oracle 对拍 50,000 个随机合法数组，并覆盖重复值出现 2 次、出现 $n+1$ 次、重复值在边界 1 或 `n`。函数图变种另随机生成映射并与访问时间戳法比较入口和环长。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-the-duplicate-number/)
- [对应知识专题](../../graph/functional-graphs.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-105-lc169/">← [力扣 Top 105] LC 169 多数元素 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-107-lc179/">[力扣 Top 107] LC 179 最大数 中等 →</a>
</nav>
