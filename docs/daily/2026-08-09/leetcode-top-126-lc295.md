---
title: "[力扣 Top 126] LC 295 数据流的中位数 困难"
---

# [力扣 Top 126] LC 295 数据流的中位数 困难

<p class="daily-archive-kicker">2026-08-09 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c613cacf6f9edaa1a6c74344ccdfe3f0682e5076fc6b3301c76ba7b1549b4a0d -->
## 官方原始信息

- Top 排名：126
- 题号：LC 295
- 官方中文标题：数据流的中位数
- 官方难度：困难
- 官方链接：[数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/)

### 原始题意与函数签名

实现 `MedianFinder`：不断加入整数，并返回当前全部元素的中位数。奇数个元素时取有序序列中间值；偶数个元素时取两个中间值的平均数。

<!-- compile:leetcode -->
```cpp
class MedianFinder {
public:
  MedianFinder();
  void addNum(int num);
  double findMedian();
};
```

### 全部官方样例

```text
输入：
["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
[[],[1],[2],[],[3],[]]
输出：[null,null,null,1.5,null,2.0]
解释：加入 1、2 后中位数为 1.5；再加入 3 后中位数为 2.0。
```

### 全部约束

- $-10^5\le num\le10^5$。
- 调用 `findMedian` 前至少已有一个元素。
- `addNum` 与 `findMedian` 总调用次数至多 $5\times10^4$。
- 允许误差不超过 $10^{-5}$。

## 约束推导与观察

中位数只依赖有序序列中央的一到两个元素，无需维护全部顺序。把数据分成较小的一半 `lower` 与较大的一半 `upper`，保持：`lower` 的所有值不大于 `upper`，且 `lower` 的大小等于或比 `upper` 多 1。此时中位数就在两个堆顶。

## 解法递进

### 解法一：每次查询时排序

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MedianFinder {
  vector<int> values;
public:
  void addNum(int num) {
    values.push_back(num);
  }
  double findMedian() {
    vector<int> sorted = values;
    sort(sorted.begin(), sorted.end());
    int n = sorted.size();
    if (n & 1) {
      return sorted[n / 2];
    }
    return (static_cast<long long>(sorted[n / 2 - 1]) + sorted[n / 2]) / 2.0;
  }
};
int main() {
}
```

加入 $O(1)$，查询 $O(n\log n)$，额外空间 $O(n)$；多次查询会重复排序。

### 解法二：始终维护有序数组

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MedianFinder {
  vector<int> values;
public:
  void addNum(int num) {
    values.insert(lower_bound(values.begin(), values.end(), num), num);
  }
  double findMedian() {
    int n = values.size();
    if (n & 1) {
      return values[n / 2];
    }
    return (static_cast<long long>(values[n / 2 - 1]) + values[n / 2]) / 2.0;
  }
};
int main() {
}
```

查询 $O(1)$，但数组插入搬移元素为 $O(n)$。

### 最佳实用解：大根堆与小根堆

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MedianFinder {
  priority_queue<int> lower;
  priority_queue<int, vector<int>, greater<int>> upper;
public:
  MedianFinder() = default;
  void addNum(int num) {
    lower.push(num);
    upper.push(lower.top());
    lower.pop();
    if (upper.size() > lower.size()) {
      lower.push(upper.top());
      upper.pop();
    }
  }
  double findMedian() {
    if (lower.size() > upper.size()) {
      return lower.top();
    }
    return (static_cast<long long>(lower.top()) + upper.top()) / 2.0;
  }
};
int main() {
}
```

每次加入 $O(\log n)$，查询 $O(1)$，空间 $O(n)$。两次搬运同时维护顺序与大小不变量，代码最稳定。

## 正确性证明

加入时先放入 `lower`，再把其最大值移到 `upper`，因此移动后 `lower` 中每个值都不大于 `upper` 的最小值。若 `upper` 更大，再把其最小值移回 `lower`，顺序关系仍成立，且大小满足 `lower=upper` 或 `lower=upper+1`。奇数个元素时 `lower.top()` 是第 $(n+1)/2$ 小；偶数时两个堆顶是第 $n/2$ 与 $n/2+1$ 小，按定义取均值。因此查询正确。

## 样例手推

加入 1 后 `lower=[1]`；加入 2 后 `lower=[1]`,`upper=[2]`，均值为 1.5；加入 3 后重平衡为 `lower` 含 1、2，`upper` 含 3，中位数为 `lower.top()=2`。

## 易错点与方案比较

- 偶数中位数相加前转为 64 位，避免更大值域下整数溢出。
- 大小不变量要固定一种方向；这里让 `lower` 可多一个。
- 不能只按大小平衡而忽略所有 `lower<=upper` 的顺序不变量。
- 两堆适合只增不删；需要删除时应换可删除结构或懒删除。

## 变种一：支持删除任意一个已存在的值

新定义：加入、删除、查询中位数。两个 `multiset` 分别保存两半，可按值删除并重平衡。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicMedian {
  multiset<int> lower;
  multiset<int> upper;
  void rebalance() {
    while (lower.size() < upper.size()) {
      lower.insert(*upper.begin());
      upper.erase(upper.begin());
    }
    while (lower.size() > upper.size() + 1) {
      auto it = prev(lower.end());
      upper.insert(*it);
      lower.erase(it);
    }
  }
public:
  void add(int x) {
    if (lower.empty() || x <= *prev(lower.end())) {
      lower.insert(x);
    } else {
      upper.insert(x);
    }
    rebalance();
  }
  bool eraseOne(int x) {
    auto it = lower.find(x);
    if (it != lower.end()) {
      lower.erase(it);
    } else if ((it = upper.find(x)) != upper.end()) {
      upper.erase(it);
    } else {
      return false;
    }
    rebalance();
    return true;
  }
  double median() const {
    if (lower.size() > upper.size()) {
      return *prev(lower.end());
    }
    return (static_cast<long long>(*prev(lower.end())) + *upper.begin()) / 2.0;
  }
};
int main() {
}
```

每次操作 $O(\log n)$，空间 $O(n)$。

## 变种二：固定长度滑动窗口中位数

对应 [LC 480 滑动窗口中位数](https://leetcode.cn/problems/sliding-window-median/)。复用可删除中位数结构，每右移一步删出、加入并查询。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  multiset<int> low, high;
  void balance() {
    while (low.size() < high.size()) {
      low.insert(*high.begin());
      high.erase(high.begin());
    }
    while (low.size() > high.size() + 1) {
      auto it = prev(low.end());
      high.insert(*it);
      low.erase(it);
    }
  }
  void add(int x) {
    (low.empty() || x <= *prev(low.end()) ? low : high).insert(x);
    balance();
  }
  void remove(int x) {
    auto it = low.find(x);
    if (it != low.end()) {
      low.erase(it);
    } else {
      high.erase(high.find(x));
    }
    balance();
  }
  double get() const {
    if (low.size() > high.size()) {
      return *prev(low.end());
    }
    return (static_cast<long long>(*prev(low.end())) + *high.begin()) / 2.0;
  }
public:
  vector<double> medianSlidingWindow(vector<int>& nums, int k) {
    vector<double> answer;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      add(nums[i]);
      if (i >= k) {
        remove(nums[i - k]);
      }
      if (i + 1 >= k) {
        answer.push_back(get());
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n\log k)$、空间 $O(k)$。

## 变种三：值域固定时用树状数组求第 `k` 小

新定义：值域仍为 $[-10^5,10^5]$，需要同时查询任意分位数。树状数组维护频次，通过二进制提升找第 `k` 小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class FrequencyQuantiles {
  static constexpr int OFFSET = 100001;
  static constexpr int SIZE = 200003;
  vector<int> bit = vector<int>(SIZE + 1);
  int count = 0;
public:
  void add(int value) {
    for (int i = value + OFFSET; i <= SIZE; i += i & -i) {
      ++bit[i];
    }
    ++count;
  }
  int kth(int k) const {
    int index = 0;
    int accumulated = 0;
    for (int step = 1 << 18; step; step >>= 1) {
      int next = index + step;
      if (next <= SIZE && accumulated + bit[next] < k) {
        index = next;
        accumulated += bit[next];
      }
    }
    return index + 1 - OFFSET;
  }
  double median() const {
    return (static_cast<long long>(kth((count + 1) / 2)) + kth((count + 2) / 2)) / 2.0;
  }
};
int main() {
}
```

加入和分位数查询均为 $O(\log V)$，空间 $O(V)$。

## 变种四：每个数带正权重，求加权中位数

新定义：数值 `x` 带权重 `w`，求最小的 `x` 使累计权重至少达到总权重的一半。坐标压缩后用树状数组维护权重。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long weightedMedian(vector<pair<int, long long>> items) {
  vector<int> coordinates;
  long long total = 0;
  for (auto [x, weight] : items) {
    coordinates.push_back(x);
    total += weight;
  }
  sort(coordinates.begin(), coordinates.end());
  coordinates.erase(unique(coordinates.begin(), coordinates.end()), coordinates.end());
  vector<long long> bit(coordinates.size() + 1);
  for (auto [x, weight] : items) {
    int index = lower_bound(coordinates.begin(), coordinates.end(), x) - coordinates.begin() + 1;
    for (int i = index; i < static_cast<int>(bit.size()); i += i & -i) {
      bit[i] += weight;
    }
  }
  long long target = (total + 1) / 2;
  int index = 0;
  long long sum = 0;
  int step = 1;
  while (step * 2 < static_cast<int>(bit.size())) {
    step *= 2;
  }
  for (; step; step >>= 1) {
    int next = index + step;
    if (next < static_cast<int>(bit.size()) && sum + bit[next] < target) {
      index = next;
      sum += bit[next];
    }
  }
  return coordinates[index];
}
int main() {
  cout << weightedMedian({{1, 2}, {5, 3}, {9, 1}}) << '\n';
}
```

构建 $O(n\log n)$，单次结果查询 $O(\log n)$，空间 $O(n)$。

## 可复现验证

对长度 $1..200$、值域 `-30..30` 的随机数据流，每次加入后都复制排序得到 oracle，中间所有查询均与两堆结果一致；固定覆盖重复值、全相等、奇偶长度和负数。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-median-from-data-stream/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-125-lc746/">← [力扣 Top 125] LC 746 使用最小花费爬楼梯 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-127-lc6/">[力扣 Top 127] LC 6 Z 字形变换 中等 →</a>
</nav>
