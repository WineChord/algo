---
title: "[力扣竞赛] 第 512 场周赛 Q2 LC 4001 聚合两个时间序列 中等"
---

# [力扣竞赛] 第 512 场周赛 Q2 LC 4001 聚合两个时间序列 中等

<p class="daily-archive-kicker">2026-07-31 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=f53933fb2685265fa206b55e697e0777c42ac5a0c444f8b87f606f64894bd814 -->
## 官方原始信息

- 来源：力扣中国竞赛
- 比赛：第 512 场周赛
- 题目：Q2，LC 4001
- 官方中文标题：聚合两个时间序列
- 官方难度：中等
- 官方竞赛分值：4
- ZeroTracer 社区估算竞赛分：暂无可核验数值
- 官方链接：[聚合两个时间序列](https://leetcode.cn/problems/aggregate-two-time-series/)

### 原始题意

给定两个二维数组 `series1` 与 `series2`，每个元素是 `[timestamp,value]`，且各自按时间戳严格递增。

对于两个序列中至少出现过一次的每个时间戳 `t`，分别确定两个序列在 `t` 的值：

- 若序列中恰有时间戳 `t`，使用该项的值。
- 若缺少 `t`，但存在晚于 `t` 的时间戳，使用最早的那个更晚时间戳对应的值。
- 若不存在更晚时间戳，值为 0。

把两个值相加，按时间戳严格递增返回所有 `[timestamp,summedValue]`。题面中不影响输入、输出和判题语义的隐藏占位变量要求不属于算法契约，无需加入实现。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> aggregateTimeSeries(
      vector<vector<int>>& series1, vector<vector<int>>& series2);
};
```

### 全部官方样例

```text
输入：series1 = [[1,3],[4,1]], series2 = [[2,2],[5,2]]
输出：[[1,5],[2,3],[4,3],[5,2]]
解释：
t=1：series1 取 3，series2 向后看时间戳 2，取 2，和为 5。
t=2：series1 向后看时间戳 4，取 1，series2 取 2，和为 3。
t=4：series1 取 1，series2 向后看时间戳 5，取 2，和为 3。
t=5：series1 已无更晚时间戳，取 0，series2 取 2，和为 2。
```

```text
输入：series1 = [[1,5],[3,1]], series2 = [[2,2]]
输出：[[1,7],[2,3],[3,1]]
解释：
t=1 时取 5+2；t=2 时取 1+2；t=3 时第二个序列已无更晚项，取 1+0。
```

```text
输入：series1 = [[1,5]], series2 = [[1000000000,2]]
输出：[[1,7],[1000000000,2]]
解释：时间戳 1 处，第二个序列向后取时间戳 1000000000 的值 2；到时间戳 1000000000 时，第一个序列取 0。
```

### 全部约束

- $1\le |series1|,|series2|\le10^5$。
- 每个元素长度均为 2。
- $1\le timestamp,value\le10^9$。
- 每个序列都按 `timestamp` 严格递增。
- 两个值之和最多为 $2\times10^9$，仍在有符号 32 位整数范围内。

## 约束推导与关键观察

结果时间戳就是两个有序时间戳集合的并集，最多有 $n+m$ 项。对某个序列和查询时间 `t`，所需项是该序列中第一个时间戳不小于 `t` 的元素，即 `lower_bound(t)`。对并集时间戳从小到大处理时，这个下界指针也只会单调右移，因此不必对每个时间戳重新二分。

## 解法递进

### 解法一：归并时间戳后逐项二分

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int valueAt(const vector<vector<int>>& series, int timestamp) {
    auto iterator = lower_bound(series.begin(), series.end(), timestamp,
        [](const vector<int>& item, int value) { return item[0] < value; });
    return iterator == series.end() ? 0 : (*iterator)[1];
  }
public:
  vector<vector<int>> aggregateTimeSeries(
      vector<vector<int>>& series1, vector<vector<int>>& series2) {
    vector<int> timestamps;
    for (const auto& item : series1) {
      timestamps.push_back(item[0]);
    }
    for (const auto& item : series2) {
      timestamps.push_back(item[0]);
    }
    sort(timestamps.begin(), timestamps.end());
    timestamps.erase(unique(timestamps.begin(), timestamps.end()), timestamps.end());
    vector<vector<int>> answer;
    for (int timestamp : timestamps) {
      answer.push_back({timestamp, valueAt(series1, timestamp) + valueAt(series2, timestamp)});
    }
    return answer;
  }
};
```

时间 $O((n+m)\log(n+m))$，结果以外空间 $O(n+m)$。

### 最佳实用解：归并时间戳与两个下界指针

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> aggregateTimeSeries(
      vector<vector<int>>& series1, vector<vector<int>>& series2) {
    int first = 0;
    int second = 0;
    vector<vector<int>> answer;
    while (first < static_cast<int>(series1.size()) || second < static_cast<int>(series2.size())) {
      int timestamp;
      if (second == static_cast<int>(series2.size()) ||
          (first < static_cast<int>(series1.size()) && series1[first][0] < series2[second][0])) {
        timestamp = series1[first][0];
      } else {
        timestamp = series2[second][0];
      }
      while (first < static_cast<int>(series1.size()) && series1[first][0] < timestamp) {
        ++first;
      }
      while (second < static_cast<int>(series2.size()) && series2[second][0] < timestamp) {
        ++second;
      }
      int firstValue = first < static_cast<int>(series1.size()) ? series1[first][1] : 0;
      int secondValue = second < static_cast<int>(series2.size()) ? series2[second][1] : 0;
      answer.push_back({timestamp, firstValue + secondValue});
      if (first < static_cast<int>(series1.size()) && series1[first][0] == timestamp) {
        ++first;
      }
      if (second < static_cast<int>(series2.size()) && series2[second][0] == timestamp) {
        ++second;
      }
    }
    return answer;
  }
};
```

时间 $O(n+m)$，除返回结果外空间 $O(1)$。

## 正确性证明

每轮开始时，`first` 与 `second` 分别指向各自尚未处理的最早时间戳；两者较小值就是尚未输出的最小并集时间戳 `t`。两个 `while` 循环丢弃严格早于 `t` 的项，结束后每个指针恰指向本序列第一个时间戳不小于 `t` 的项，若不存在则到达末尾。因此取到的值严格符合题目“下一个更晚时间戳，若无则 0”的定义。输出后把恰等于 `t` 的项移过，保证 `t` 不会重复。归纳可知所有并集时间戳按严格递增顺序恰输出一次，且每项和值正确。

## 样例手推

样例一初始指针指向时间戳 1 与 2，先输出 1：值为 3 与 2。随后第一个指针到 4、第二个仍在 2，输出 2：值为 1 与 2。再依次输出 4、5，得到 `[[1,5],[2,3],[4,3],[5,2]]`。

## 边界、易错点与方案比较

- “缺失时取下一项”不是常见的前值保持，方向不能写反。
- 结果只含原序列出现过的时间戳，不需要填补中间所有整数时间。
- 两个序列时间戳相等时只输出一次，并同时移动两个指针。
- 线性解无需额外哈希或排序，最适合本题已排序输入；二分版更容易从定义直接推出，可作为 oracle。

## 变种一：聚合 k 个时间序列

使用最大堆从大时间戳向小时间戳归并。`current[i]` 保存序列 `i` 已遇到的最早“未来项”值，同时维护所有当前值之和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Entry {
  int timestamp;
  int series;
  int index;
  bool operator<(const Entry& other) const {
    return timestamp < other.timestamp;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k;
  cin >> k;
  vector<vector<pair<int, int>>> series(k);
  priority_queue<Entry> pending;
  for (int i = 0; i < k; ++i) {
    int size;
    cin >> size;
    series[i].resize(size);
    for (auto& [timestamp, value] : series[i]) {
      cin >> timestamp >> value;
    }
    pending.push({series[i].back().first, i, size - 1});
  }
  vector<long long> current(k);
  long long sum = 0;
  vector<pair<int, long long>> reversedAnswer;
  while (!pending.empty()) {
    int timestamp = pending.top().timestamp;
    while (!pending.empty() && pending.top().timestamp == timestamp) {
      Entry entry = pending.top();
      pending.pop();
      sum -= current[entry.series];
      current[entry.series] = series[entry.series][entry.index].second;
      sum += current[entry.series];
      if (entry.index > 0) {
        int previous = entry.index - 1;
        pending.push({series[entry.series][previous].first, entry.series, previous});
      }
    }
    reversedAnswer.push_back({timestamp, sum});
  }
  reverse(reversedAnswer.begin(), reversedAnswer.end());
  for (auto [timestamp, value] : reversedAnswer) {
    cout << timestamp << ' ' << value << '\n';
  }
}
```

若总项数为 $T$，时间 $O(T\log k)$，空间 $O(k+T)$（含结果）。

## 变种二：查询任意时间戳，不限于并集

每次对两个序列分别 `lower_bound`，适合查询数量较少或查询顺序任意的场景。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int valueAt(const vector<pair<int, int>>& series, int timestamp) {
  auto iterator = lower_bound(series.begin(), series.end(), timestamp,
      [](const pair<int, int>& item, int value) { return item.first < value; });
  return iterator == series.end() ? 0 : iterator->second;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<pair<int, int>> first(n), second(m);
  for (auto& [timestamp, value] : first) {
    cin >> timestamp >> value;
  }
  for (auto& [timestamp, value] : second) {
    cin >> timestamp >> value;
  }
  while (q--) {
    int timestamp;
    cin >> timestamp;
    cout << valueAt(first, timestamp) + valueAt(second, timestamp) << '\n';
  }
}
```

每次查询 $O(\log n+\log m)$，空间 $O(n+m)$。

## 变种三：支持在线插入或修改时间点

两个序列改用有序映射。查询时用 `lower_bound` 找下一个不早于目标的时间戳；更新为 $O(\log n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long valueAt(const map<int, long long>& series, int timestamp) {
  auto iterator = series.lower_bound(timestamp);
  return iterator == series.end() ? 0 : iterator->second;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  array<map<int, long long>, 2> series;
  while (q--) {
    char type;
    cin >> type;
    if (type == 'U') {
      int index, timestamp;
      long long value;
      cin >> index >> timestamp >> value;
      series[index][timestamp] = value;
    } else {
      int timestamp;
      cin >> timestamp;
      cout << valueAt(series[0], timestamp) + valueAt(series[1], timestamp) << '\n';
    }
  }
}
```

每次操作 $O(\log n+\log m)$，空间与已存时间点数成正比。

## 变种四：缺失时使用最近的更早值

规则改成常见的“前值保持”。从小到大归并时维护每个序列最近已见值；原题的下界指针含义不再成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<pair<int, long long>> first(n), second(m);
  for (auto& [timestamp, value] : first) {
    cin >> timestamp >> value;
  }
  for (auto& [timestamp, value] : second) {
    cin >> timestamp >> value;
  }
  int i = 0;
  int j = 0;
  long long firstValue = 0;
  long long secondValue = 0;
  while (i < n || j < m) {
    int timestamp;
    if (j == m || (i < n && first[i].first < second[j].first)) {
      timestamp = first[i].first;
    } else {
      timestamp = second[j].first;
    }
    if (i < n && first[i].first == timestamp) {
      firstValue = first[i++].second;
    }
    if (j < m && second[j].first == timestamp) {
      secondValue = second[j++].second;
    }
    cout << timestamp << ' ' << firstValue + secondValue << '\n';
  }
}
```

时间 $O(n+m)$，额外空间 $O(1)$。

## 可复现验证

随机生成两组严格递增时间戳和值，把线性双指针结果与“并集排序后逐项 `lower_bound`”逐例比较；覆盖完全重合、完全错开、只有一个元素、一个序列提前结束和时间戳达到 $10^9$。所有和以 64 位中间变量复核后确认落在官方 32 位范围。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/aggregate-two-time-series/)
- [第 512 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-512/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/aggregate-two-time-series/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-60-lc24/">← [力扣 Top 60] LC 24 两两交换链表中的节点 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-e/">[codeforces] CF Round 1111 Div.2 E Build a Tree →</a>
</nav>
