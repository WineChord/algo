---
title: "[力扣 Top 24] LC 283 移动零 简单"
---

# [力扣 Top 24] LC 283 移动零 简单

<p class="daily-archive-kicker">2026-07-28 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-28 题目列表</a> · <a href="../../basics/sequence-invariants.md">进入知识专题</a></p>

## 官方原始信息

- 难度：LeetCode 官方「简单」；非竞赛题，无官方分值与 ZeroTracer 竞赛分。
- 官方链接：https://leetcode.cn/problems/move-zeroes/
- slug：`move-zeroes`
- 函数签名：`void moveZeroes(vector<int>& nums)`，结果写回参数。
- 题意：原地把所有零移到末尾，同时保持非零元素相对顺序。
- 示例：`[0,1,0,3,12] -> [1,3,12,0,0]`；`[0] -> [0]`。
- 约束：$1\le n\le10^4$；$-2^{31}\le nums_i\le2^{31}-1$。
- 官方进阶：尽量减少操作次数。

## 约束、样例与边界

必须原地、必须稳定，排除了排序和普通双向分区。所有元素至少查看一次，时间下界 $\Omega(n)$。全零、无零、零在首尾、交替零、负数和 `INT_MIN` 都只依赖“是否等于零”，没有溢出问题。

## 暴力：辅助数组收集非零值

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void moveZeroes(vector<int>& nums) {
    vector<int> next;
    for (int x : nums) if (x != 0) next.push_back(x);
    next.resize(nums.size(), 0);
    nums.swap(next);
  }
};
```

时间 $O(n)$，空间 $O(n)$。扫描顺序保证稳定，但不满足原地要求。

## 最优：稳定压缩后填零

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void moveZeroes(vector<int>& nums) {
    int write = 0;
    for (int x : nums) {
      if (x != 0) nums[write++] = x;
    }
    while (write < (int)nums.size()) nums[write++] = 0;
  }
};
```

循环不变量：扫描到位置 `read` 前，`nums[0..write)` 恰好是原前缀中的全部非零值且顺序不变；`write` 是下一个非零应写位置。结束后前缀已经是稳定非零序列，剩余位置数量恰好等于零的数量，填零即完成。时间 $O(n)$，空间 $O(1)$。

对 `[0,1,0,3,12]`，非零压缩过程得到前缀 `[1]`、`[1,3]`、`[1,3,12]`，`write=3`，再填两个零。优先记忆该版本：证明最直接、写次数容易精确分析。

## Follow-up 1：交换版，避免无意义自赋值

仍保持稳定；当 `read==write` 时不写，否则把非零值与 `write` 位置的零交换。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void moveZeroes(vector<int>& nums) {
    int write = 0;
    for (int read = 0; read < (int)nums.size(); ++read) {
      if (nums[read] == 0) continue;
      if (read != write) swap(nums[read], nums[write]);
      ++write;
    }
  }
};
```

时间 $O(n)$，空间 $O(1)$。当零很少时减少自赋值；一次 `swap` 通常包含多次底层写入，不必笼统宣称写次数一定更少。

## Follow-up 2：把任意目标值稳定移到末尾

只把判定 `x!=0` 泛化为 `x!=target`，最后填目标值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void moveTargetToEnd(vector<int>& nums, int target) {
  int write = 0;
  for (int x : nums) {
    if (x != target) nums[write++] = x;
  }
  while (write < (int)nums.size()) nums[write++] = target;
}
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 3：稳定地把零移到开头

从右向左稳定压缩非零值；逆向扫描与逆向写入共同保持原相对顺序。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void moveZeroesToFront(vector<int>& nums) {
  int write = (int)nums.size() - 1;
  for (int read = (int)nums.size() - 1; read >= 0; --read) {
    if (nums[read] != 0) nums[write--] = nums[read];
  }
  while (write >= 0) nums[write--] = 0;
}
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 4：不要求稳定，尽量减少扫描区间

用左右指针把左侧零与右侧非零交换；相对顺序可能改变，因此不能用于原题。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void moveZeroesUnstable(vector<int>& nums) {
  int left = 0, right = (int)nums.size() - 1;
  while (left < right) {
    while (left < right && nums[left] != 0) ++left;
    while (left < right && nums[right] == 0) --right;
    if (left < right) swap(nums[left++], nums[right--]);
  }
}
```

时间 $O(n)$，空间 $O(1)$；适合只要求分区、不要求稳定的场景。

## Follow-up 5：删除指定值并返回新长度

新定义：把不等于 `val` 的元素稳定写到前缀，返回有效前缀长度；后缀内容无要求。对应 LC 27。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeElement(vector<int>& nums, int val) {
    int write = 0;
    for (int x : nums) {
      if (x != val) nums[write++] = x;
    }
    return write;
  }
};
```

时间 $O(n)$，空间 $O(1)$。与移动零相比，不需要填充后缀。

## 易错点与验证

- 原题要求稳定，不能排序或直接左右交换。
- 范围 `for (int x : nums)` 按值读取，避免本轮写入影响后续读取值。
- 填零从 `write` 开始而不是从最后一个非零位置开始。
- 随机验证：随机整数数组与“筛出非零后补零”的辅助数组 oracle 比较；检查元素多重集、非零相对顺序、长度和原地接口。

## Reference

- [官方题目](https://leetcode.cn/problems/move-zeroes/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-23-lc21.md">← [力扣 Top 23] LC 21 合并两个有序链表 简单</a>
<a class="daily-archive-pager__next" href="leetcode-top-25-lc2235.md">[力扣 Top 25] LC 2235 两整数相加 简单 →</a>
</nav>
