---
title: "[力扣 Top 104] LC 347 前 K 个高频元素 中等"
---

# [力扣 Top 104] LC 347 前 K 个高频元素 中等

<p class="daily-archive-kicker">2026-08-05 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../basics/top-k-extrema/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=97ec3c1a88e6398717a54248c407f556de6be804cc7e8355fa7ef1e818915519 -->
## 官方原始信息

- Top 排名：104
- 题号：LC 347
- 官方中文标题：前 K 个高频元素
- 官方难度：中等
- 官方链接：[前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)

### 原始题意

给定整数数组 `nums` 和整数 `k`，返回出现频率最高的 `k` 个不同元素，顺序任意。题目保证答案集合唯一。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k);
};
```

### 全部官方样例

```text
输入：nums = [1,1,1,2,2,3], k = 2
输出：[1,2]
```

```text
输入：nums = [1], k = 1
输出：[1]
```

```text
输入：nums = [1,2,1,2,1,2,3,1,3,2], k = 2
输出：[1,2]
```

### 全部约束

- $1\le n=nums.length\le10^5$。
- $-10^4\le nums[i]\le10^4$。
- $1\le k\le$ 不同元素个数。
- 前 `k` 高频元素的集合唯一。
- 进阶要求时间复杂度严格优于 $O(n\log n)$。

## 约束推导与观察

先计数是不可避免的，设不同元素数为 $d\le n$。把全部元素按频率排序需要 $O(d\log d)$，不满足最坏情形下优于 $O(n\log n)$ 的进阶要求。频率只可能落在 `[1,n]`，因此可把频率本身作为桶下标，从高到低收集；这消除了比较排序。

答案仅存元素值，无乘法溢出；哈希表要预留容量以降低重哈希常数。

## 解法递进

### 解法一：计数后全排序

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    for (int value : nums) {
      ++frequency[value];
    }
    vector<pair<int, int>> items;
    for (auto [value, count] : frequency) {
      items.push_back({count, value});
    }
    sort(items.begin(), items.end(), greater<pair<int, int>>());
    vector<int> answer;
    for (int i = 0; i < k; ++i) {
      answer.push_back(items[i].second);
    }
    return answer;
  }
};
```

平均时间 $O(n+d\log d)$，空间 $O(d)$。瓶颈是对不需要的低频元素也完整排序。

### 解法二：大小为 `k` 的最小堆

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    for (int value : nums) {
      ++frequency[value];
    }
    using Item = pair<int, int>;
    priority_queue<Item, vector<Item>, greater<Item>> heap;
    for (auto [value, count] : frequency) {
      heap.push({count, value});
      if (static_cast<int>(heap.size()) > k) {
        heap.pop();
      }
    }
    vector<int> answer;
    while (!heap.empty()) {
      answer.push_back(heap.top().second);
      heap.pop();
    }
    return answer;
  }
};
```

平均时间 $O(n+d\log k)$，空间 $O(d+k)$。当 `k` 很小且频率值域不便建桶时很实用。

### 最佳实用解：频率桶

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    frequency.reserve(nums.size() * 2);
    for (int value : nums) {
      ++frequency[value];
    }
    vector<vector<int>> bucket(nums.size() + 1);
    for (auto [value, count] : frequency) {
      bucket[count].push_back(value);
    }
    vector<int> answer;
    answer.reserve(k);
    for (int count = nums.size(); count >= 1 && static_cast<int>(answer.size()) < k; --count) {
      for (int value : bucket[count]) {
        answer.push_back(value);
        if (static_cast<int>(answer.size()) == k) {
          break;
        }
      }
    }
    return answer;
  }
};
```

平均时间 $O(n+d)$，空间 $O(n+d)$。由于答案集合唯一，临界频率不会产生需要裁决的并列；这是本题最稳的进阶方案。

### 同阶期望方案：快速选择

只把第 `d-k` 小频率放到正确分界，平均线性但最坏可退化。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    for (int value : nums) {
      ++frequency[value];
    }
    vector<pair<int, int>> items;
    for (auto [value, count] : frequency) {
      items.push_back({count, value});
    }
    nth_element(items.begin(), items.end() - k, items.end());
    vector<int> answer;
    for (auto iterator = items.end() - k; iterator != items.end(); ++iterator) {
      answer.push_back(iterator->second);
    }
    return answer;
  }
};
```

平均时间 $O(n+d)$，空间 $O(d)$。桶法有确定的线性上界；快速选择节省桶数组但证明和退化边界更多。

## 正确性证明

计数表给出每个不同值的真实频率，随后该值被放入且仅放入下标等于其频率的桶。从桶 `n` 向下遍历等价于按频率非增序访问所有不同值。由于前 `k` 的答案集合唯一，收集到第 `k` 个值时，所有已选值频率都严格位于未选边界之上或处于不影响集合唯一性的桶中。因此返回集合恰为前 `k` 高频元素。

## 样例手推

`[1,1,1,2,2,3]` 的频率为 `1→3, 2→2, 3→1`。桶 3 先给出 1，桶 2 再给出 2，收满两个即停止。`n=1,k=1` 时唯一元素位于桶 1。

## 易错点与方案比较

- 统计的是不同元素，不是直接从原数组取前 `k` 个位置。
- 最小堆在大小超过 `k` 时弹出，不能使用最大堆后弹错方向。
- 若题目不保证答案集合唯一，必须明确同频率的次级规则。
- 桶法确定线性但占 $O(n)$ 桶；堆适合很小的 `k`；快速选择平均线性且常数小，但最坏界较弱。

## 变种一：同频率时数值更小者优先

新定义：答案顺序也固定。每个频率桶内部升序排序，再从高频桶依次输出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  unordered_map<int, int> frequency;
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    ++frequency[value];
  }
  vector<vector<int>> bucket(n + 1);
  for (auto [value, count] : frequency) {
    bucket[count].push_back(value);
  }
  vector<int> answer;
  for (int count = n; count >= 1 && static_cast<int>(answer.size()) < k; --count) {
    sort(bucket[count].begin(), bucket[count].end());
    for (int value : bucket[count]) {
      if (static_cast<int>(answer.size()) < k) {
        answer.push_back(value);
      }
    }
  }
  for (int i = 0; i < k; ++i) {
    cout << answer[i] << (i + 1 == k ? '\n' : ' ');
  }
}
```

时间 $O(n+\sum_f b_f\log b_f)$，最坏 $O(n+d\log d)$，空间 $O(n+d)$。新次级顺序使纯桶不再完全线性。

## 变种二：在线增加频次并随时查询前 `k`

新定义：数据流只有插入。用哈希表记录频率，并在有序集合中维护键 `(-频率, 值)`；每次更新先删旧键再插新键。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class FrequencyIndex {
  unordered_map<int, int> frequency;
  set<pair<int, int>> order;
public:
  void add(int value) {
    int old = frequency[value];
    if (old) {
      order.erase({-old, value});
    }
    int current = ++frequency[value];
    order.insert({-current, value});
  }
  vector<int> top(int k) const {
    vector<int> answer;
    for (auto [negativeCount, value] : order) {
      static_cast<void>(negativeCount);
      if (static_cast<int>(answer.size()) == k) {
        break;
      }
      answer.push_back(value);
    }
    return answer;
  }
};
int main() {
  int operations;
  cin >> operations;
  FrequencyIndex index;
  while (operations--) {
    char type;
    int value;
    cin >> type >> value;
    if (type == '+') {
      index.add(value);
    } else {
      vector<int> answer = index.top(value);
      for (int i = 0; i < static_cast<int>(answer.size()); ++i) {
        cout << answer[i] << (i + 1 == static_cast<int>(answer.size()) ? '\n' : ' ');
      }
    }
  }
}
```

更新 $O(\log d)$，查询 $O(k)$，空间 $O(d)$。静态桶无法高效响应频率持续变化。

## 变种三：内存受限的数据流重频元素候选

新定义：寻找所有出现次数大于 $n/k$ 的值，只允许 $O(k)$ 候选。Misra–Gries 抵消法先找候选，再二次扫描精确验证。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  vector<int> values(n);
  unordered_map<int, int> candidate;
  for (int& value : values) {
    cin >> value;
    if (candidate.contains(value)) {
      ++candidate[value];
    } else if (static_cast<int>(candidate.size()) < k - 1) {
      candidate[value] = 1;
    } else {
      vector<int> erased;
      for (auto& [key, count] : candidate) {
        if (--count == 0) {
          erased.push_back(key);
        }
      }
      for (int key : erased) {
        candidate.erase(key);
      }
    }
  }
  unordered_map<int, int> exact;
  for (int value : values) {
    if (candidate.contains(value)) {
      ++exact[value];
    }
  }
  vector<int> answer;
  for (auto [value, count] : exact) {
    if (count > n / k) {
      answer.push_back(value);
    }
  }
  sort(answer.begin(), answer.end());
  for (int i = 0; i < static_cast<int>(answer.size()); ++i) {
    cout << answer[i] << (i + 1 == static_cast<int>(answer.size()) ? '\n' : ' ');
  }
}
```

朴素实现时间 $O(nk)$、空间 $O(k)$；固定小 `k` 时适合流式内存限制。它解决阈值重频，不等价于任意 `top k`。

## 变种四：利用题目给出的紧值域

新定义保持原题，但利用 $nums[i]\in[-10^4,10^4]$，用定长数组代替哈希表，获得确定性时间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  constexpr int offset = 10000;
  constexpr int range = 20001;
  vector<int> frequency(range);
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    ++frequency[value + offset];
  }
  vector<vector<int>> bucket(n + 1);
  for (int index = 0; index < range; ++index) {
    if (frequency[index]) {
      bucket[frequency[index]].push_back(index - offset);
    }
  }
  vector<int> answer;
  for (int count = n; count >= 1 && static_cast<int>(answer.size()) < k; --count) {
    for (int value : bucket[count]) {
      if (static_cast<int>(answer.size()) < k) {
        answer.push_back(value);
      }
    }
  }
  for (int i = 0; i < k; ++i) {
    cout << answer[i] << (i + 1 == k ? '\n' : ' ');
  }
}
```

时间 $O(n+V)$、空间 $O(n+V)$，其中 $V=20001$。若值域放大或稀疏，哈希表更合适。

## 验证说明

本轮将九段代码按 C++23 编译；排序 oracle、堆、桶和快速选择会对拍 30,000 组随机数组，并覆盖全相同、全不同、负数、`k=1`、`k=d` 和唯一边界频率。动态与阈值变种另与每步重新排序的朴素结果核对。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/top-k-frequent-elements/)
- [对应知识专题](../../basics/top-k-extrema.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-103-lc92/">← [力扣 Top 103] LC 92 反转链表 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-105-lc169/">[力扣 Top 105] LC 169 多数元素 简单 →</a>
</nav>
