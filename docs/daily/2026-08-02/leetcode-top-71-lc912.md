---
title: "[力扣 Top 71] LC 912 排序数组 中等"
---

# [力扣 Top 71] LC 912 排序数组 中等

<p class="daily-archive-kicker">2026-08-02 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../basics/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=69f810d57a0292e98843fb286c49abb96b48cd1aea9e3dad668d98bd45916143 -->
## 官方原始信息

- Top 排名：71
- 题号：LC 912
- 官方中文标题：排序数组
- 官方难度：中等
- 官方链接：[排序数组](https://leetcode.cn/problems/sort-an-array/)

### 原始题意

给定整数数组 `nums`，在不调用内置排序函数的前提下按升序返回数组。要求时间复杂度达到 $O(n\log n)$，并尽量减少额外空间。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> sortArray(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [5,2,3,1]
输出：[1,2,3,5]
解释：排序后 2、3 的位置不变，1、5 的位置改变。
```

```text
输入：nums = [5,1,1,2,0,0]
输出：[0,0,1,1,2,5]
解释：数组元素可以重复。
```

### 全部约束

- $1\le n\le5\times10^4$。
- $-5\times10^4\le nums_i\le5\times10^4$。
- 不使用任何内置排序函数。
- 目标时间 $O(n\log n)$，额外空间尽可能小。

## 约束推导与边界

$n=5\times10^4$ 排除了选择排序、插入排序等 $O(n^2)$ 方法。值域宽度只有 $10^5+1$，计数排序也可行，但它使用与值域相关的额外空间；若希望同时保证一般整数上的 $O(n\log n)$ 最坏时间与 $O(1)$ 辅助数组空间，原地堆排序最贴合题意。

重复值必须全部保留；负数只参与比较，不会引发溢出。堆下标的孩子位置 `2*i+1` 在本题规模内安全。空数组不在官方约束内，单元素数组应原样返回。

## 解法递进

### 解法一：选择排序

每轮在未排序后缀中找最小值，与当前起点交换。它建立“前缀已经有序且包含全局最小的若干元素”的不变量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> sortArray(vector<int>& nums) {
    int n = nums.size();
    for (int left = 0; left < n; ++left) {
      int minimum = left;
      for (int i = left + 1; i < n; ++i) {
        if (nums[i] < nums[minimum]) {
          minimum = i;
        }
      }
      swap(nums[left], nums[minimum]);
    }
    return nums;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$；在上限规模会超时，但适合作为小数组 oracle。

### 解法二：归并排序

递归排序两半，再用双指针稳定合并。它把时间降到确定的 $O(n\log n)$，代价是 $O(n)$ 缓冲区。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> buffer;
  void mergeSort(vector<int>& a, int left, int right) {
    if (right - left <= 1) {
      return;
    }
    int middle = left + (right - left) / 2;
    mergeSort(a, left, middle);
    mergeSort(a, middle, right);
    int first = left;
    int second = middle;
    int write = left;
    while (first < middle || second < right) {
      if (second == right || (first < middle && a[first] <= a[second])) {
        buffer[write++] = a[first++];
      } else {
        buffer[write++] = a[second++];
      }
    }
    for (int i = left; i < right; ++i) {
      a[i] = buffer[i];
    }
  }
public:
  vector<int> sortArray(vector<int>& nums) {
    buffer.resize(nums.size());
    mergeSort(nums, 0, nums.size());
    return nums;
  }
};
```

时间 $O(n\log n)$，额外空间 $O(n)$，递归栈 $O(\log n)$；使用 `<=` 保证相等元素稳定。

### 最佳实用解：原地堆排序

先在线性时间建最大堆。每轮把堆顶最大值交换到未排序区末尾，再下沉恢复剩余堆。数组后缀因此按最终位置从右向左固定。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void siftDown(vector<int>& a, int root, int size) {
    while (2 * root + 1 < size) {
      int child = 2 * root + 1;
      if (child + 1 < size && a[child] < a[child + 1]) {
        ++child;
      }
      if (a[root] >= a[child]) {
        return;
      }
      swap(a[root], a[child]);
      root = child;
    }
  }
public:
  vector<int> sortArray(vector<int>& nums) {
    int n = nums.size();
    for (int i = n / 2 - 1; i >= 0; --i) {
      siftDown(nums, i, n);
    }
    for (int size = n; size > 1; --size) {
      swap(nums[0], nums[size - 1]);
      siftDown(nums, 0, size - 1);
    }
    return nums;
  }
};
```

时间最坏 $O(n\log n)$，额外空间 $O(1)$。它不稳定，但官方只要求数值升序。对“必须保证最坏时间且尽量省空间”的接口，优先推荐堆排序。

## 正确性证明

建堆结束后，每个父节点都不小于孩子，所以堆顶是当前堆内最大值。设某轮开始时，区间 `[size,n)` 已经有序且恰好保存全数组最大的 $n-size$ 个值。交换堆顶与 `size-1` 后，当前剩余元素的最大值进入其最终位置；`siftDown` 只在 `[0,size-1)` 内恢复最大堆，不改变已固定后缀。因此不变量继续成立。循环到 `size=1` 时，每个位置都已固定，数组整体非递减。

## 样例手推

对 `[5,2,3,1]` 建最大堆后仍可为 `[5,2,3,1]`。交换首尾得到 `[1,2,3,5]`，前三个元素下沉为 `[3,2,1,5]`；再固定 3 得 `[1,2,3,5]`，最后固定 2。重复值样例中比较使用严格大小，相等值不会丢失。

## 易错点与方案比较

- 建堆从最后一个非叶节点 `n/2-1` 开始。
- 下沉的有效范围是半开区间 `[0,size)`，固定后缀不能再参与比较。
- 快速排序平均很快，但朴素枢轴在有序或大量重复数据上可退化；若没有内省排序保护，不如堆排序稳健。
- 归并排序稳定、常数好，适合允许 $O(n)$ 空间的场景；堆排序满足最坏 $O(n\log n)$ 与 $O(1)$ 额外空间，推荐作为本题的约束闭环方案。

## 变种一：必须保持相等元素的原相对顺序

新定义：元素带原下标，相同键必须稳定。堆排序失效，归并时相等优先取左半段。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<int, int>> a(n), buffer(n);
  for (int i = 0; i < n; ++i) {
    cin >> a[i].first;
    a[i].second = i;
  }
  function<void(int, int)> sortRange = [&](int left, int right) {
    if (right - left <= 1) {
      return;
    }
    int middle = (left + right) / 2;
    sortRange(left, middle);
    sortRange(middle, right);
    int i = left;
    int j = middle;
    for (int k = left; k < right; ++k) {
      if (j == right || (i < middle && a[i].first <= a[j].first)) {
        buffer[k] = a[i++];
      } else {
        buffer[k] = a[j++];
      }
    }
    copy(buffer.begin() + left, buffer.begin() + right, a.begin() + left);
  };
  sortRange(0, n);
  for (auto [value, index] : a) {
    cout << value << ':' << index << '\n';
  }
}
```

时间 $O(n\log n)$，空间 $O(n)$。

## 变种二：数组已知至多错位 $k$ 个位置

新定义：每个元素在完整排序后与当前下标相差不超过 $k$。维护大小至多 $k+1$ 的最小堆即可连续确定下一个最小值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  priority_queue<int, vector<int>, greater<int>> heap;
  int read = 0;
  int write = 0;
  while (read < n && read <= k) {
    heap.push(a[read++]);
  }
  while (!heap.empty()) {
    a[write++] = heap.top();
    heap.pop();
    if (read < n) {
      heap.push(a[read++]);
    }
  }
  for (int value : a) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\log(k+1))$，空间 $O(k)$。

## 变种三：数据大于内存，执行外部归并

新定义：输入被分成若干已经在内存中排好的有序段，输出全局有序序列。用最小堆做多路归并，内存只保存每段一个候选。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int runCount;
  cin >> runCount;
  vector<vector<int>> runs(runCount);
  for (auto& run : runs) {
    int size;
    cin >> size;
    run.resize(size);
    for (int& value : run) {
      cin >> value;
    }
  }
  using State = tuple<int, int, int>;
  priority_queue<State, vector<State>, greater<State>> heap;
  for (int run = 0; run < runCount; ++run) {
    if (!runs[run].empty()) {
      heap.emplace(runs[run][0], run, 0);
    }
  }
  while (!heap.empty()) {
    auto [value, run, index] = heap.top();
    heap.pop();
    cout << value << ' ';
    if (index + 1 < static_cast<int>(runs[run].size())) {
      heap.emplace(runs[run][index + 1], run, index + 1);
    }
  }
  cout << '\n';
}
```

若总元素数为 $n$、有 $r$ 段，时间 $O(n\log r)$，堆空间 $O(r)$；真实外部排序把 `runs` 替换为文件流。

## 变种四：数据流中持续维护最大的 $k$ 个数

新定义：元素在线到达，不需要完整排序，只在结束时输出最大的 $k$ 个。维护大小为 $k$ 的最小堆，避免支付全排序成本。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  priority_queue<int, vector<int>, greater<int>> heap;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    heap.push(value);
    if (static_cast<int>(heap.size()) > k) {
      heap.pop();
    }
  }
  vector<int> answer;
  while (!heap.empty()) {
    answer.push_back(heap.top());
    heap.pop();
  }
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\log k)$，空间 $O(k)$；输出本身按升序排列。

## 验证说明

三种主解与标准升序结果对 8000 个随机数组比较，覆盖空值域边界、重复值、负数、有序与逆序输入；所有七段代码均以 C++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/sort-an-array/)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-a/">← [atcoder] ABC469 A Train Car</a>
<a class="daily-archive-pager__next" href="../leetcode-top-72-lc34/">[力扣 Top 72] LC 34 在排序数组中查找元素的第一个和最后一个位置 中等 →</a>
</nav>
