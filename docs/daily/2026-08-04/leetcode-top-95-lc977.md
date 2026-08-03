---
title: "[力扣 Top 95] LC 977 有序数组的平方 简单"
---

# [力扣 Top 95] LC 977 有序数组的平方 简单

<p class="daily-archive-kicker">2026-08-04 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=e9d141c74dd1f01725d41560994ebd80d8ad6871fd2435ac70a3580dcf72ce6d -->
## 官方原始信息

- Top 排名：95
- 题号：LC 977
- 官方中文标题：有序数组的平方
- 官方难度：简单
- 官方链接：[有序数组的平方](https://leetcode.cn/problems/squares-of-a-sorted-array/)

### 原始题意

给定一个非递减整数数组，返回每个元素平方后的非递减数组。进阶要求线性时间。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> sortedSquares(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [-4,-1,0,3,10]
输出：[0,1,9,16,100]
解释：平方后为 [16,1,0,9,100]，排序后得到答案。
```

```text
输入：nums = [-7,-3,2,3,11]
输出：[4,9,9,49,121]
```

### 全部约束

- $1\le nums.length\le10^4$。
- $-10^4\le nums[i]\le10^4$。
- `nums` 已按非递减顺序排列。

## 约束推导与双端单调性

平方函数在非负区间单调递增，在负数区间按原数组顺序却单调递减，所以“逐个平方”会破坏全局顺序。但当前未取元素中绝对值最大者一定在区间两端：左端可能是最负值，右端是最大非负值。比较两端绝对值，把较大平方放到答案末尾，再收缩对应端点，就能每轮永久确定一个位置。

最大平方为 $10^8$，`int` 安全。输出本身有 $n$ 个元素，时间下界为 $\Omega(n)$。

## 解法递进

### 解法一：平方后排序

它不利用输入有序性，但直接正确，可作为对拍基准。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> sortedSquares(vector<int>& nums) {
    vector<int> answer;
    answer.reserve(nums.size());
    for (int value : nums) {
      answer.push_back(value * value);
    }
    sort(answer.begin(), answer.end());
    return answer;
  }
};
```

时间 $O(n\log n)$，输出空间 $O(n)$。

### 最佳实用解：双端取最大值，倒序写答案

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> sortedSquares(vector<int>& nums) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;
    vector<int> answer(nums.size());
    for (int write = right; write >= 0; --write) {
      if (abs(nums[left]) > abs(nums[right])) {
        answer[write] = nums[left] * nums[left];
        ++left;
      } else {
        answer[write] = nums[right] * nums[right];
        --right;
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，除输出外额外空间 $O(1)$，达到下界。它用“候选最大值只在两端”的不变量，适合优先记忆。

### 同阶方案：分割正负区间后归并

找到第一个非负数；负数部分从右向左平方后递增，非负部分从左向右平方也递增，再做标准二路归并。时间和空间同为 $O(n)$，但边界分支更多，适合需要沿正负两路继续处理的变种。

## 正确性证明

任一轮未处理区间仍是原数组的连续子区间。其内部若为负数，越靠左绝对值越大；若为非负数，越靠右绝对值越大；跨过零时绝对值最小。因此未处理元素的最大绝对值必在左、右端之一。算法比较两端，把更大平方写入当前最大的空位，写入值不会小于后续任何值。收缩一端后不变量继续成立。归纳到所有位置填满，答案非递减且包含每个元素平方恰好一次。

## 样例手推

`[-4,-1,0,3,10]` 两端绝对值先比较 4 与 10，末位写 100；再比较 4 与 3，写 16；随后写 9、1、0，得到 `[0,1,9,16,100]`。全负数组会不断移动左端，全非负数组会不断移动右端；重复绝对值任取一端都不影响排序。

## 易错点与方案比较

- 写指针必须从答案末尾向前，因为每轮确定的是最大剩余平方。
- 比较绝对值后再平方，不能比较原值大小。
- 当前约束下 `abs(-10000)` 安全；若值可能为 `INT_MIN`，应先转 `long long`。
- 排序解最通用；双指针解利用有序性达到线性，是进阶要求的推荐答案。

## 变种一：同时返回原下标

新定义：输出 `(平方值, 原下标)`，平方相同时按原下标升序。双端任选会破坏平局规则，直接构造对并稳定排序更清晰。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<pair<long long, int>> answer;
  for (int i = 0; i < n; ++i) {
    long long value;
    cin >> value;
    answer.push_back({value * value, i});
  }
  sort(answer.begin(), answer.end());
  for (const auto& [square, index] : answer) {
    cout << square << ' ' << index << '\n';
  }
}
```

时间 $O(n\log n)$，空间 $O(n)$。恢复信息与稳定平局要求改变了最简实现的取舍。

## 变种二：负数与非负数分别存放

新定义：输入给出两个有序数组：负数数组递增、非负数组递增。把负数数组反向平方，与非负平方流归并。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int negativeCount, nonnegativeCount;
  cin >> negativeCount >> nonnegativeCount;
  vector<long long> negative(negativeCount), nonnegative(nonnegativeCount);
  for (long long& value : negative) {
    cin >> value;
  }
  for (long long& value : nonnegative) {
    cin >> value;
  }
  int left = negativeCount - 1;
  int right = 0;
  while (left >= 0 || right < nonnegativeCount) {
    long long first = left >= 0 ? negative[left] * negative[left] : LLONG_MAX;
    long long second =
        right < nonnegativeCount ? nonnegative[right] * nonnegative[right] : LLONG_MAX;
    if (first <= second) {
      cout << first << ' ';
      --left;
    } else {
      cout << second << ' ';
      ++right;
    }
  }
  cout << '\n';
}
```

时间 $O(n)$，除输入外额外空间 $O(1)$。这正是分割归并方案的接口化版本。

## 变种三：多次询问平方不超过 $T^2$ 的元素数

新定义：不输出排序结果，而是对每个非负 $T$ 统计 $|nums_i|\le T$。原数组有序，合法值落在区间 $[-T,T]$，两次二分即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> numbers(n);
  for (long long& value : numbers) {
    cin >> value;
  }
  while (q--) {
    long long threshold;
    cin >> threshold;
    auto left = lower_bound(numbers.begin(), numbers.end(), -threshold);
    auto right = upper_bound(numbers.begin(), numbers.end(), threshold);
    cout << right - left << '\n';
  }
}
```

每问 $O(\log n)$，空间 $O(1)$。多次阈值查询时无需真正构造平方数组。

## 变种四：有界值域下在线增删与阈值查询

新定义：维护整数多重集合，值域为 $[-10^4,10^4]$；支持插入、删除，以及询问平方不超过 $T^2$ 的数量。Fenwick 树按绝对值维护频次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  vector<int> tree;
public:
  explicit Fenwick(int size) : tree(size + 1) {
  }
  void add(int index, int delta) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  int sumPrefix(int index) const {
    int answer = 0;
    for (++index; index > 0; index -= index & -index) {
      answer += tree[index];
    }
    return answer;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queryCount;
  cin >> queryCount;
  Fenwick fenwick(10001);
  map<int, int> frequency;
  while (queryCount--) {
    char type;
    int value;
    cin >> type >> value;
    if (type == '+') {
      ++frequency[value];
      fenwick.add(abs(value), 1);
    } else if (type == '-') {
      if (frequency[value] > 0) {
        --frequency[value];
        fenwick.add(abs(value), -1);
      }
    } else {
      cout << fenwick.sumPrefix(min(abs(value), 10000)) << '\n';
    }
  }
}
```

每次操作 $O(\log V)$，空间 $O(V+U)$。静态双指针无法直接支持插入和删除，值域结构接管了排序信息。

## 验证说明

本轮将六段完整代码按 C++23 编译；线性双指针会与平方后排序在 30,000 组随机非递减数组上对拍，并覆盖全负、全正、零、重复绝对值、极值与两组官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/squares-of-a-sorted-array/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-94-lc43/">← [力扣 Top 94] LC 43 字符串相乘 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-96-lc7/">[力扣 Top 96] LC 7 整数反转 中等 →</a>
</nav>
