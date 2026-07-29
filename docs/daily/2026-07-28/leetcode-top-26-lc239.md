---
title: "[力扣 Top 26] LC 239 滑动窗口最大值 困难"
---

# [力扣 Top 26] LC 239 滑动窗口最大值 困难

<p class="daily-archive-kicker">2026-07-28 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-28 题目列表</a> · <a href="../../data-structures/monotonic-queues.md">进入知识专题</a></p>

## 官方原始信息

- 官方链接：<https://leetcode.cn/problems/sliding-window-maximum/>
- slug：`sliding-window-maximum`
- 官方难度：困难；官方竞赛分未提供；ZeroTracer 数据集无记录。
- 函数签名：`vector<int> maxSlidingWindow(vector<int>& nums, int k)`
- 题意：长度为 `k` 的窗口从数组最左端逐次右移一格，返回每个窗口中的最大值。
- 样例 1：`nums = [1,3,-1,-3,5,3,6,7], k = 3`，输出 `[3,3,5,5,6,7]`。
- 样例 2：`nums = [1], k = 1`，输出 `[1]`。
- 约束：$1\le n\le10^5$，$-10^4\le nums[i]\le10^4$，$1\le k\le n$。

`n` 达到 $10^5$，逐窗口扫描 $k$ 个元素的 $O(nk)$ 在 $k=\Theta(n)$ 时会退化到 $O(n^2)$。答案仍在输入值域内，不存在整数溢出。

## 样例与边界

样例 1 的窗口依次为 `[1,3,-1]`、`[3,-1,-3]`、`[-1,-3,5]`、`[-3,5,3]`、`[5,3,6]`、`[3,6,7]`。单调队列保存的下标对应值始终递减；读入 `5` 时，旧的 `-1,-3` 都不可能再成为未来最大值，故从队尾删除。

- `k=1`：每个元素就是一个答案。
- `k=n`：只输出全局最大值。
- 重复最大值：删除队尾时使用 `<=`，保留更新、更晚过期的相同值。
- 全递减：队列最多保存 `k` 个下标；全递增：每次只保留最新下标。

## 解法一：逐窗口扫描

枚举每个窗口，再枚举其中全部 `k` 个元素。覆盖性直接，但相邻窗口重复比较 `k-1` 个元素。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    vector<int> ans;
    for (int left = 0; left + k <= (int)nums.size(); ++left) {
      int best = nums[left];
      for (int i = left + 1; i < left + k; ++i) best = max(best, nums[i]);
      ans.push_back(best);
    }
    return ans;
  }
};
```

时间 $O((n-k+1)k)$，答案外额外空间 $O(1)$。

## 解法二：大根堆惰性删除

堆保存 `(值,下标)`。加入新元素后，只要堆顶下标已经离开窗口就弹出。它消除了窗口内部的全量重扫，但堆中可能暂存过期的非堆顶元素。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    priority_queue<pair<int, int>> heap;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
      heap.push({nums[i], i});
      if (i + 1 < k) continue;
      while (heap.top().second <= i - k) heap.pop();
      ans.push_back(heap.top().first);
    }
    return ans;
  }
};
```

时间 $O(n\log n)$，空间 $O(n)$。

## 最佳实用解：单调队列

双端队列只保存“仍在窗口中、且可能成为当前或未来最大值”的下标：

1. 从队首删除 `<= i-k` 的过期下标。
2. 从队尾删除值 `<= nums[i]` 的下标：新元素更大且过期更晚，旧下标被永久支配。
3. 将 `i` 入队；窗口形成后，队首就是答案。

不变量：队列下标严格递增，对应值严格递减，且全部位于当前窗口。步骤 1 保证有效性，步骤 2 保证单调性；任何被删队尾元素都不可能在新元素之前过期后重新变优。因此队首是窗口中未被支配的最大值。每个下标最多入队一次、从两端之一出队一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> q;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
      while (!q.empty() && q.front() <= i - k) q.pop_front();
      while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
      q.push_back(i);
      if (i + 1 >= k) ans.push_back(nums[q.front()]);
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(k)$。优先记忆此解：复杂度最优、在线、常数小，且“不可能再成为答案的候选立即淘汰”可迁移到大量滑动窗口极值问题。

常见错误：队列保存值而无法判断过期；先输出再清理过期下标；只弹出 `<` 而保留大量等值；把 `i-k` 写成 `i-k+1`；误称嵌套 `while` 为 $O(nk)$，忽略摊还分析。

## Follow-up 1：滑动窗口最小值

新定义：返回每个窗口最小值。支配方向反转，队列值应严格递增。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> minSlidingWindow(vector<int>& nums, int k) {
    deque<int> q;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
      while (!q.empty() && q.front() <= i - k) q.pop_front();
      while (!q.empty() && nums[q.back()] >= nums[i]) q.pop_back();
      q.push_back(i);
      if (i + 1 >= k) ans.push_back(nums[q.front()]);
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(k)$。

## Follow-up 2：流式输入，只保留最近 `k` 个数的最大值

新定义：元素逐个到达，每次 `add` 返回最近至多 `k` 个元素的最大值。原算法本来就是在线的，只需把下标计数与队列封装为状态。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class WindowMaximum {
  int k;
  int index = -1;
  deque<pair<int, int>> q;
public:
  explicit WindowMaximum(int windowSize) : k(windowSize) {}
  int add(int value) {
    ++index;
    while (!q.empty() && q.front().second <= index - k) q.pop_front();
    while (!q.empty() && q.back().first <= value) q.pop_back();
    q.push_back({value, index});
    return q.front().first;
  }
};
```

每次摊还 $O(1)$，空间 $O(k)$。

## Follow-up 3：任意离线区间最大值查询

新定义：窗口长度和左右端点不固定，回答多次 `[l,r]` 最大值。单调队列依赖端点单向移动，不能直接复用；改用线段树。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class RangeMaximum {
  int size = 1;
  vector<int> tree;
public:
  explicit RangeMaximum(const vector<int>& nums) {
    while (size < (int)nums.size()) size <<= 1;
    tree.assign(size * 2, INT_MIN);
    for (int i = 0; i < (int)nums.size(); ++i) tree[size + i] = nums[i];
    for (int i = size - 1; i > 0; --i) tree[i] = max(tree[i * 2], tree[i * 2 + 1]);
  }
  int query(int left, int right) {
    int ans = INT_MIN;
    for (left += size, right += size; left <= right; left >>= 1, right >>= 1) {
      if (left & 1) ans = max(ans, tree[left++]);
      if (!(right & 1)) ans = max(ans, tree[right--]);
    }
    return ans;
  }
};
```

建树 $O(n)$，每次查询 $O(\log n)$，空间 $O(n)$。

## Follow-up 4：窗口最大值与出现次数

新定义：每个窗口返回 `(最大值, 最大值出现次数)`。单调队列用 `<=` 会删除相同值并丢失次数；平衡树按值维护频次更稳妥。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<pair<int, int>> maxWithCount(vector<int>& nums, int k) {
    map<int, int> frequency;
    vector<pair<int, int>> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
      ++frequency[nums[i]];
      if (i >= k) {
        int value = nums[i - k];
        if (--frequency[value] == 0) frequency.erase(value);
      }
      if (i + 1 >= k) {
        auto [value, count] = *frequency.rbegin();
        ans.push_back({value, count});
      }
    }
    return ans;
  }
};
```

时间 $O(n\log k)$，空间 $O(k)$。

## 可复现验证

最优解与暴力解应在随机 `n<=40`、随机 `k`、含负数和重复值的数组上逐项对拍；编译与对拍结果见同目录 `validation-report.json`。

## Reference

- [官方题目](https://leetcode.cn/problems/sliding-window-maximum/)
- [对应知识专题](../../data-structures/monotonic-queues.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-25-lc2235.md">← [力扣 Top 25] LC 2235 两整数相加 简单</a>
<a class="daily-archive-pager__next" href="leetcode-top-27-lc121.md">[力扣 Top 27] LC 121 买卖股票的最佳时机 简单 →</a>
</nav>
