---
title: "[力扣 Top 16] LC 56 合并区间 中等"
---

# [力扣 Top 16] LC 56 合并区间 中等

<p class="daily-archive-kicker">2026-07-27 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

## 官方原始信息

- 题号：56
- 官方中文标题：合并区间
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/merge-intervals/)
- slug：`merge-intervals`
- 函数签名：`vector<vector<int>> merge(vector<vector<int>>& intervals)`
- 官方竞赛分：未标注。官方题面与本轮核对的官方 GraphQL 元数据均未提供竞赛归属或分值，不作推断。
- ZeroTracer 社区估算竞赛分：未收录。本轮于 2026-07-27 按题号与 slug 精确检索其公开 `data.json`，无匹配记录。

### 原始题意

输入若干闭区间 `intervals[i] = [start_i, end_i]`。把所有有公共点的区间合并，返回一组两两不重叠的闭区间，并且它们覆盖的点集与输入区间的并集完全相同。闭区间端点接触也算重叠，例如 `[1,4]` 与 `[4,5]` 必须合并。

### 全部官方样例

1. 输入 `[[1,3],[2,6],[8,10],[15,18]]`，输出 `[[1,6],[8,10],[15,18]]`。前两个区间相交，合并为 `[1,6]`。
2. 输入 `[[1,4],[4,5]]`，输出 `[[1,5]]`。二者在端点 `4` 相交。
3. 输入 `[[4,7],[1,4]]`，输出 `[[1,7]]`。输入无须预先有序，排序后两个区间在端点 `4` 相交。

### 全部官方约束

- $1\le n=\texttt{intervals.length}\le10^4$
- `intervals[i].length == 2`
- $0\le start_i\le end_i\le10^4$

## 约束推导与最优结论

输入可能完全逆序，必须先建立某种端点顺序。一般模型中，按左端点排序需要 $O(n\log n)$；排序后，只要维护当前并集最后一个区间，就能在线性扫描中完成合并。总时间 $O(n\log n)$，除排序栈与输出外额外空间通常为 $O(\log n)$。

本题端点值域只有 $U=10^4+1$ 个整数，因此还可以按左端点做桶扫描，以 $O(n+U)$ 时间、$O(U)$ 空间规避比较排序。它利用了本题的特殊值域；面试中更值得优先记忆的是“左端点排序 + 扫描”，因为它适用于任意可比较端点，也更容易扩展到浮点时间、时间戳和自定义区间。

整数端点不参与求和或乘法，`int` 足够。输出区间沿用输入端点，不存在算术溢出。

## 样例手推与边界

对 `[[1,3],[2,6],[8,10],[15,18]]` 按左端点排序后顺序不变：

1. 当前并集为 `[1,3]`。
2. 下一区间 `[2,6]` 满足 $2\le3$，有交集，把右端点扩为 $\max(3,6)=6$。
3. `[8,10]` 满足 $8>6$，与当前区间分离，提交 `[1,6]`，开启 `[8,10]`。
4. `[15,18]` 与 `[8,10]` 分离，最终得到三个区间。

必须覆盖的边界包括：

- 单区间与零长度区间，如 `[[3,3]]`；
- 完全相同或大量重复区间；
- 严格包含，如 `[1,10]` 与 `[2,3]`，右端点不能缩短；
- 链式相交，如 `[1,2],[2,3],[3,4]`，应整体合并；
- 端点接触，判断必须是 `nextLeft <= currentRight`；
- 输入逆序；
- 全部分离或全部连成一个区间。

## 解法一：重叠图连通分量（正确暴力）

把每个区间视为一个点；若两个闭区间相交，就连一条无向边。一个连通分量中的区间可通过重叠链连成连续覆盖，其并集恰为该分量最小左端点到最大右端点。枚举所有区间对建图，再搜索连通分量。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> merge(vector<vector<int>>& intervals) {
    int n = intervals.size();
    vector<vector<int>> graph(n);
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        int left = max(intervals[i][0], intervals[j][0]);
        int right = min(intervals[i][1], intervals[j][1]);
        if (left <= right) {
          graph[i].push_back(j);
          graph[j].push_back(i);
        }
      }
    }
    vector<char> seen(n);
    vector<vector<int>> answer;
    for (int start = 0; start < n; ++start) {
      if (seen[start]) continue;
      int left = intervals[start][0];
      int right = intervals[start][1];
      stack<int> pending;
      pending.push(start);
      seen[start] = 1;
      while (!pending.empty()) {
        int u = pending.top();
        pending.pop();
        left = min(left, intervals[u][0]);
        right = max(right, intervals[u][1]);
        for (int v : graph[u]) {
          if (seen[v]) continue;
          seen[v] = 1;
          pending.push(v);
        }
      }
      answer.push_back({left, right});
    }
    sort(answer.begin(), answer.end());
    return answer;
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$；密集重叠时图有二次规模。它证明了“传递重叠属于同一并集块”，但没有利用一维区间排序后只需比较并集末尾这一结构。

## 解法二：左端点排序后线性扫描（最佳通用解）

排序后，尚未处理区间的左端点单调不减。维护答案最后一个区间 `[L,R]`：

- 若新左端点 $l\le R$，新段与当前并集相交，只需令 $R\leftarrow\max(R,r)$；
- 若 $l>R$，后续区间的左端点只会更大，因此当前 `[L,R]` 再也不可能被扩展，可以开启新区间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> answer;
    for (const auto& segment : intervals) {
      if (answer.empty() || segment[0] > answer.back()[1]) {
        answer.push_back(segment);
      } else {
        answer.back()[1] = max(answer.back()[1], segment[1]);
      }
    }
    return answer;
  }
};
```

时间 $O(n\log n)$，扫描 $O(n)$；输出之外额外空间取决于排序实现，通常为 $O(\log n)$。

### 正确性证明

维护不变量：扫描前 $i$ 个排序区间后，`answer` 是这 $i$ 个区间并集的唯一升序、两两分离表示。

初始为空显然成立。处理 `[l,r]` 时：

- 若 `answer` 为空或 $l>R$，排序保证以后不会出现左端点小于 $l$ 的区间；新段与最后一段分离，追加后仍完整且两两分离。
- 若 $l\le R$，新段与最后一段相交。此前更早的答案段都严格结束在最后一段左侧，因此新段只可能扩展最后一段；把其右端点改为 $\max(R,r)$ 恰好得到二者并集。

归纳可知不变量始终成立，扫描结束时答案恰好表示全部输入区间的并集。

## 解法三：利用有限值域的左端点桶

对每个左端点只保留能到达的最远右端点，再按坐标从小到大扫描。相同左端点的较短区间必被最长者包含，可以安全丢弃。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> merge(vector<vector<int>>& intervals) {
    const int limit = 10000;
    vector<int> farthest(limit + 1, -1);
    for (const auto& segment : intervals) {
      farthest[segment[0]] = max(farthest[segment[0]], segment[1]);
    }
    vector<vector<int>> answer;
    for (int left = 0; left <= limit; ++left) {
      if (farthest[left] < 0) continue;
      if (answer.empty() || left > answer.back()[1]) {
        answer.push_back({left, farthest[left]});
      } else {
        answer.back()[1] = max(answer.back()[1], farthest[left]);
      }
    }
    return answer;
  }
};
```

时间 $O(n+U)$，空间 $O(U)$，其中 $U=10001$。在当前约束下它是确定性的线性值域算法；若端点是大整数、浮点数或字符串时间戳，排序扫描更稳健。

## 同阶与实用方案比较

- 排序扫描：通用性最佳、证明短、实现稳定，是面试首选。
- 值域桶：在当前小值域上避免比较排序，确定性强，但空间依赖值域且可迁移性弱。
- 重叠图：概念直观却有二次时间和空间，只适合作为正确性 oracle 或暴力起点。
- 若输入已经按左端点有序，直接扫描为 $O(n)$；若输入排序不可破坏，可排序副本，代价为 $O(n)$ 额外空间。

## 常见错误

- 用 `segment[0] >= answer.back()[1]` 判断分离，错误地把端点相接的闭区间拆开。
- 合并时直接赋值右端点为 `segment[1]`，遇到包含关系会把当前并集缩短。
- 只比较相邻原区间，而不是比较“当前已经合并出的区间”。
- 忘记输入未排序。
- 在答案为空时访问 `answer.back()`。
- 把闭区间题的判定机械迁移到半开会议区间；后者通常在 `end == nextStart` 时不冲突。

## Follow-up 1：插入一个新区间

若原区间已经按左端点排序且互不重叠，先输出所有严格位于新区间左侧的段，再吸收所有与新区间相交的段，最后输出右侧剩余段。对应 [LC 57 插入区间](https://leetcode.cn/problems/insert-interval/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
    vector<vector<int>> answer;
    int i = 0;
    while (i < (int)intervals.size() && intervals[i][1] < newInterval[0]) {
      answer.push_back(intervals[i++]);
    }
    while (i < (int)intervals.size() && intervals[i][0] <= newInterval[1]) {
      newInterval[0] = min(newInterval[0], intervals[i][0]);
      newInterval[1] = max(newInterval[1], intervals[i][1]);
      ++i;
    }
    answer.push_back(newInterval);
    while (i < (int)intervals.size()) answer.push_back(intervals[i++]);
    return answer;
  }
};
```

时间 $O(n)$，输出之外额外空间 $O(1)$。

## Follow-up 2：两个有序区间列表求交

两个列表内部各自互不重叠且按左端点有序。当前两段交集为 `[max(left), min(right)]`；之后右端点较小的那一段不可能再与对方当前段或更早位置产生新交集，应前移。对应 [LC 986 区间列表的交集](https://leetcode.cn/problems/interval-list-intersections/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> intervalIntersection(vector<vector<int>>& first, vector<vector<int>>& second) {
    vector<vector<int>> answer;
    int i = 0, j = 0;
    while (i < (int)first.size() && j < (int)second.size()) {
      int left = max(first[i][0], second[j][0]);
      int right = min(first[i][1], second[j][1]);
      if (left <= right) answer.push_back({left, right});
      if (first[i][1] < second[j][1]) ++i;
      else ++j;
    }
    return answer;
  }
};
```

时间 $O(n+m)$，输出之外额外空间 $O(1)$。

## Follow-up 3：最少会议室数

会议通常建模为半开区间 `[start,end)`，所以一个会议结束时另一个可以立刻开始。按开始时间排序，用最小堆保存当前占用房间的结束时间；开始新会议前释放所有 `end <= start` 的房间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minMeetingRooms(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    priority_queue<int, vector<int>, greater<int>> endings;
    int answer = 0;
    for (const auto& meeting : intervals) {
      while (!endings.empty() && endings.top() <= meeting[0]) endings.pop();
      endings.push(meeting[1]);
      answer = max(answer, (int)endings.size());
    }
    return answer;
  }
};
```

时间 $O(n\log n)$，空间 $O(n)$。模型变化的关键是半开区间端点相等不冲突，与原题闭区间规则相反。

## Follow-up 4：删除最少区间使剩余区间互不重叠

目标从“求并集”改为“保留最多个互不重叠区间”。按右端点升序，每次选择最早结束且与上次选择兼容的区间，能给后续留下最大空间。对应 [LC 435 无重叠区间](https://leetcode.cn/problems/non-overlapping-intervals/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
      if (a[1] != b[1]) return a[1] < b[1];
      return a[0] < b[0];
    });
    int kept = 0;
    int lastEnd = numeric_limits<int>::min();
    for (const auto& segment : intervals) {
      if (segment[0] >= lastEnd) {
        ++kept;
        lastEnd = segment[1];
      }
    }
    return intervals.size() - kept;
  }
};
```

时间 $O(n\log n)$，额外空间通常 $O(\log n)$。这里按题目常用的兼容定义，`end == nextStart` 可同时保留。

## Follow-up 5：动态区间增删与离线点查询

预先知道所有可能查询坐标 `points`，但区间会在线加入或删除。对查询坐标压缩后，用差分 Fenwick 树做闭区间覆盖次数的区间加、单点查；加入 `[l,r]` 加 `+1`，删除同一区间加 `-1`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class RangeCoverage {
  vector<int> coordinates;
  vector<int> bit;
  void addPoint(int index, int delta) {
    for (int i = index + 1; i < (int)bit.size(); i += i & -i) bit[i] += delta;
  }
public:
  explicit RangeCoverage(vector<int> points) {
    sort(points.begin(), points.end());
    points.erase(unique(points.begin(), points.end()), points.end());
    coordinates = move(points);
    bit.assign(coordinates.size() + 1, 0);
  }
  void addInterval(int left, int right, int delta) {
    int first = lower_bound(coordinates.begin(), coordinates.end(), left) - coordinates.begin();
    int after = upper_bound(coordinates.begin(), coordinates.end(), right) - coordinates.begin();
    if (first < (int)coordinates.size()) addPoint(first, delta);
    if (after < (int)coordinates.size()) addPoint(after, -delta);
  }
  int query(int point) const {
    int index = lower_bound(coordinates.begin(), coordinates.end(), point) - coordinates.begin();
    if (index == (int)coordinates.size() || coordinates[index] != point) {
      throw invalid_argument("query point was not registered");
    }
    int answer = 0;
    for (int i = index + 1; i > 0; i -= i & -i) answer += bit[i];
    return answer;
  }
};
```

设预注册点数为 $q$，每次区间增删和单点查询均为 $O(\log q)$，空间 $O(q)$。

## 验证说明

- 主问题将排序扫描和值域桶分别与重叠图 oracle 在小规模随机闭区间上比较。
- 固定覆盖三个官方样例，以及单点、完全包含、端点接触、全分离、全连通和逆序输入。
- 本文每个 C++ 代码块均按 C++23 单独做语法编译；随机种子、用例规模与真实结果记录在同目录机器报告中。

## Reference

- [官方题目](https://leetcode.cn/problems/merge-intervals/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-15-lc4/">← [力扣 Top 15] LC 4 寻找两个正序数组的中位数 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-17-lc215/">[力扣 Top 17] LC 215 数组中的第 K 个最大元素 中等 →</a>
</nav>
