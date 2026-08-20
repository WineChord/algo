---
title: "[力扣竞赛] 第 515 场周赛 Q4 LC 4027 电梯请求 III 困难"
---

# [力扣竞赛] 第 515 场周赛 Q4 LC 4027 电梯请求 III 困难

<p class="daily-archive-kicker">2026-08-21 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-21 题目列表</a> · <a href="../../../dp/subset-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d987ab1dfdf7c88dc7a652aa5ab67f9f70a513869a6a2aa779a5742db83c5d43 -->
[力扣官方题目：4027. 电梯请求 III](https://leetcode.cn/problems/elevator-requests-iii/)

## 官方原始信息

- 比赛：第 515 场周赛；题目顺序：Q4；题号：LC 4027。
- 官方中文标题：电梯请求 III；官方难度：困难；官方竞赛分值：6 分。
- 官方链接：[https://leetcode.cn/problems/elevator-requests-iii/](https://leetcode.cn/problems/elevator-requests-iii/)
- 函数签名：`long long elevatorRequests(int n, int start, vector<vector<int>>& requests)`。
- 官方标签：位运算、数组、动态规划、位掩码、排序。
- 截至 2026-08-21，ZeroTracer 公开数据尚无可确认的 LC 4027 数值，社区估算竞赛分记为未知。

### 原始题意

一栋楼有 $n$ 层，编号为 $0$ 到 $n-1$。时间 0 时电梯位于 `start`。请求
`requests[i] = [arrival_i, floor_i]` 表示在时间 $arrival_i$ 出现前往 $floor_i$ 的请求。
每秒电梯可上行一层、下行一层或停留。请求只能在到达时间及以后处理；从它到达起，只要
电梯位于对应楼层就立即处理。求处理全部请求的最短时间。

### 全部官方样例

```text
示例 1
输入：n = 9, start = 0, requests = [[0,8],[6,5]]
输出：9
解释：先在时间 5 到达 5 层，等待到 6 处理第二个请求，再于时间 9 到达 8 层。

示例 2
输入：n = 8, start = 5, requests = [[1,7],[7,3]]
输出：7
解释：时间 2 到达 7 层并处理请求，再于时间 6 到达 3 层，等待到时间 7。

示例 3
输入：n = 7, start = 3, requests = [[0,5],[0,1],[6,3]]
输出：8
解释：依次在时间 2、6、8 到达 5、1、3 层，最后一个请求在时间 6 已经出现。
```

### 全部约束

- $1\le n\le10^9$。
- $1\le requests.length\le16$。
- `requests[i] == [arrival_i, floor_i]`。
- $0\le arrival_i\le10^9$。
- $0\le start,floor_i\le n-1$。

## 最优结论摘要

请求数最多只有 16，强烈提示状态压缩。令 `dp[mask][i]` 表示已处理 `mask` 中请求、最后在
请求 $i$ 的楼层完成服务时的最早时间。转移到请求 $j$：

$$
dp[mask\cup\{j\}][j]
=\min\left(dp[mask\cup\{j\}][j],
\max(arrival_j,dp[mask][i]+|floor_i-floor_j|)\right).
$$

相同楼层只需保留最晚到达时间。时间复杂度 $O(2^m m^2)$，空间 $O(2^m m)$，其中
$m\le16$ 是去重后的楼层数。

## 约束与观察

- 楼层总数可达 $10^9$，不能按楼层做 DP；请求数只有 16，状态应围绕请求集合建立。
- 行走时间和到达时间都可达 $10^9$，最多 16 段，必须使用 `long long`。
- 同一楼层若有多个请求，服务最晚到达的那个时，较早请求必已一并处理，因此只保留该楼层
  的最大 `arrival`。
- `n` 只负责约束楼层合法范围；移动代价由两个实际楼层之差决定，转移中不需要枚举空楼层。
- 电梯经过某个请求楼层时可能顺便处理它。把这些首次处理事件按时间插入访问顺序，不增加
  路程，所以“枚举服务顺序”的 DP 仍覆盖最优轨迹。

## 样例手推与边界

样例 1 有两个服务顺序：

- 先 8 后 5：时间 8 到 8 层，再走 3 秒到 5 层，完成时间 11。
- 先 5 后 8：时间 5 到 5 层，等待到 6，再走 3 秒，完成时间 9。

所以答案为 9。若请求是 `[[0,start],[10,start]]`，去重后只剩 `(10,start)`，电梯原地等待到
10 即可。若所有请求到达时间均为 0，问题退化为从 `start` 出发访问一维点集的最短完成时间。

## 解法一：枚举所有服务顺序

对去重后的 $m$ 个楼层枚举全部排列。给定顺序后，最早时间是确定的：走到下一个楼层，若
请求尚未到达就在该楼层等待。覆盖性来自任意可行轨迹都能按请求首次被处理的时间排序。
复杂度 $O(m!\,m)$，只适合作为小规模 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long elevatorRequests(int n, int start, vector<vector<int>>& requests) {
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<pair<int, int>> jobs;
    for (auto [floor, arrival] : latest) jobs.push_back({arrival, floor});
    int m = jobs.size();
    vector<int> order(m);
    iota(order.begin(), order.end(), 0);
    long long answer = numeric_limits<long long>::max();
    do {
      long long time = 0;
      int floor = start;
      for (int index : order) {
        time += abs(floor - jobs[index].second);
        time = max(time, static_cast<long long>(jobs[index].first));
        floor = jobs[index].second;
      }
      answer = min(answer, time);
    } while (next_permutation(order.begin(), order.end()));
    static_cast<void>(n);
    return answer;
  }
};
```

## 从排列到状态压缩

不同排列会共享大量“已处理同一集合，当前位于同一末尾楼层”的前缀。未来只关心三件事：
已处理集合、当前位置、当前最早时间。若两个前缀到达同一状态，只保留时间更早者，因为更早
可以原地等待来模拟更晚者，绝不会使未来更差。

初始转移直接从 `start` 前往第一个请求楼层：

$$
dp[2^i][i]=\max(arrival_i,|start-floor_i|).
$$

之后每次只增加一个新请求，状态图按集合大小严格前进，不需要 Dijkstra。

## 最佳实用解：子集 DP

### 正确性证明

**引理 1**：对固定服务顺序，转移式给出实现该顺序的最早时间。

归纳考虑顺序前缀。到下一楼层至少需要距离所对应的时间，且不能早于请求到达；在两者较大
时刻完成既合法又最早。

**引理 2**：存在一个最优轨迹可表示为某个服务顺序。

沿任意最优轨迹记录每个请求第一次被处理的时刻；同时处理的请求任意打破平局。若某请求在
前往另一目标的途中被顺便处理，就把它插入穿越该楼层的位置，不增加移动或等待。因此得到
一个包含全部请求的顺序。

**引理 3**：`dp[mask][i]` 是所有对应顺序前缀中的最早时间。

初始化覆盖一个请求的顺序；转移枚举倒数第二个请求和新加入的最后请求。由引理 1，每个候选
值可实现；由引理 2，所有顺序都被枚举。取最小值后命题成立。

满集合所有末尾状态的最小值因此就是全局最优完成时间。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long elevatorRequests(int n, int start, vector<vector<int>>& requests) {
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<int> arrival;
    vector<int> floor;
    for (auto [position, time] : latest) {
      floor.push_back(position);
      arrival.push_back(time);
    }
    int m = floor.size();
    int full = 1 << m;
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dp(full, vector<long long>(m, infinity));
    for (int i = 0; i < m; ++i) {
      dp[1 << i][i] = max<long long>(arrival[i], abs(start - floor[i]));
    }
    for (int mask = 1; mask < full; ++mask) {
      for (int last = 0; last < m; ++last) {
        if (dp[mask][last] == infinity) continue;
        for (int next = 0; next < m; ++next) {
          if ((mask >> next) & 1) continue;
          long long reached = dp[mask][last] + abs(floor[last] - floor[next]);
          long long finished = max(reached, static_cast<long long>(arrival[next]));
          int nextMask = mask | (1 << next);
          dp[nextMask][next] = min(dp[nextMask][next], finished);
        }
      }
    }
    static_cast<void>(n);
    return *min_element(dp[full - 1].begin(), dp[full - 1].end());
  }
};
```

时间复杂度 $O(2^m m^2)$，空间复杂度 $O(2^m m)$。在 $m=16$ 时约有一百万个末尾状态，
适合正式约束。

## 同阶方案比较

也可以把 `(mask,last)` 看成图节点运行 Dijkstra，但所有边都只从小集合指向大集合，天然是
有向无环图；按 `mask` 枚举就是拓扑 DP，堆只会增加常数与证明负担。由于 release time 让
单纯的“一维区间只访问最左最右”推理可能需要重复穿越，本题优先记忆子集 DP。

## 易错点

- 不能按请求给出的数组顺序处理；它既不保证按到达时间排序，也不保证是最优服务顺序。
- 到达楼层的时刻要与请求到达时间取最大值，而不是把等待时间重复相加。
- 相同楼层应保留最晚到达请求；保留最早值会漏掉后来的请求。
- `dp` 必须用 `long long`，`infinity + distance` 前先跳过不可达状态。
- 最终答案要在所有 `last` 中取最小，不要求回到 `start`。
- 不需要使用楼层总数 `n` 建数组，也不需要为了无语义作用的占位变量改变算法。

## 验证说明

所有代码块均通过 C++23 语法编译。对去重后请求数不超过 8 的随机实例，子集 DP 与全排列
枚举逐项对拍；额外覆盖相同楼层不同到达时间、起点楼层延迟请求、全部同时到达、必须等待、
途中经过请求楼层以及三个官方样例。

## 变种一：恢复一条最优服务顺序

新定义：除最短时间外，返回一条达到它的请求楼层顺序。每次改善 `dp` 时记录前驱末尾，最后
从满集合最优状态逆推。复杂度仍为 $O(2^m m^2)$，额外前驱空间 $O(2^m m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<long long, vector<int>> bestSchedule(
      int start, const vector<vector<int>>& requests) {
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<int> floor, arrival;
    for (auto [position, time] : latest) {
      floor.push_back(position);
      arrival.push_back(time);
    }
    int m = floor.size();
    int full = 1 << m;
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dp(full, vector<long long>(m, infinity));
    vector<vector<int>> parent(full, vector<int>(m, -1));
    for (int i = 0; i < m; ++i) {
      dp[1 << i][i] = max<long long>(arrival[i], abs(start - floor[i]));
    }
    for (int mask = 1; mask < full; ++mask) {
      for (int last = 0; last < m; ++last) {
        if (dp[mask][last] == infinity) continue;
        for (int next = 0; next < m; ++next) {
          if ((mask >> next) & 1) continue;
          long long candidate = dp[mask][last] + abs(floor[last] - floor[next]);
          candidate = max(candidate, static_cast<long long>(arrival[next]));
          int nextMask = mask | (1 << next);
          if (candidate < dp[nextMask][next]) {
            dp[nextMask][next] = candidate;
            parent[nextMask][next] = last;
          }
        }
      }
    }
    int last = min_element(dp.back().begin(), dp.back().end()) - dp.back().begin();
    long long time = dp.back()[last];
    vector<int> order;
    for (int mask = full - 1; mask != 0;) {
      order.push_back(floor[last]);
      int previous = parent[mask][last];
      mask ^= 1 << last;
      last = previous;
    }
    reverse(order.begin(), order.end());
    return {time, order};
  }
};
```

## 变种二：统计最优服务顺序数量

新定义：相同楼层先合并，统计达到最短完成时间的不同楼层顺序数，答案模 $10^9+7$。为每个
状态同时保存最早时间和达到该时间的顺序数：更优就覆盖，相等就累加。复杂度不变。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countBestOrders(int start, const vector<vector<int>>& requests) {
    constexpr int mod = 1000000007;
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<int> floor, arrival;
    for (auto [position, time] : latest) {
      floor.push_back(position);
      arrival.push_back(time);
    }
    int m = floor.size();
    int full = 1 << m;
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dp(full, vector<long long>(m, infinity));
    vector<vector<int>> ways(full, vector<int>(m));
    for (int i = 0; i < m; ++i) {
      dp[1 << i][i] = max<long long>(arrival[i], abs(start - floor[i]));
      ways[1 << i][i] = 1;
    }
    for (int mask = 1; mask < full; ++mask) {
      for (int last = 0; last < m; ++last) {
        if (dp[mask][last] == infinity) continue;
        for (int next = 0; next < m; ++next) {
          if ((mask >> next) & 1) continue;
          long long value = dp[mask][last] + abs(floor[last] - floor[next]);
          value = max(value, static_cast<long long>(arrival[next]));
          int nextMask = mask | (1 << next);
          if (value < dp[nextMask][next]) {
            dp[nextMask][next] = value;
            ways[nextMask][next] = ways[mask][last];
          } else if (value == dp[nextMask][next]) {
            ways[nextMask][next] += ways[mask][last];
            if (ways[nextMask][next] >= mod) ways[nextMask][next] -= mod;
          }
        }
      }
    }
    long long best = *min_element(dp.back().begin(), dp.back().end());
    int answer = 0;
    for (int last = 0; last < m; ++last) {
      if (dp.back()[last] != best) continue;
      answer += ways.back()[last];
      if (answer >= mod) answer -= mod;
    }
    return answer;
  }
};
```

## 变种三：上行与下行耗时不同

新定义：上行一层耗时 `upCost`，下行一层耗时 `downCost`。原 DP 仍成立，只把绝对值距离
替换为有方向的代价；时间 $O(2^m m^2)$、空间 $O(2^m m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long travel(int from, int to, int upCost, int downCost) {
    if (to >= from) return 1LL * (to - from) * upCost;
    return 1LL * (from - to) * downCost;
  }
public:
  long long elevatorRequestsAsymmetric(
      int start, vector<vector<int>> requests, int upCost, int downCost) {
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<int> floor, arrival;
    for (auto [position, time] : latest) {
      floor.push_back(position);
      arrival.push_back(time);
    }
    int m = floor.size();
    int full = 1 << m;
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dp(full, vector<long long>(m, infinity));
    for (int i = 0; i < m; ++i) {
      dp[1 << i][i] = max<long long>(
          arrival[i], travel(start, floor[i], upCost, downCost));
    }
    for (int mask = 1; mask < full; ++mask) {
      for (int last = 0; last < m; ++last) {
        if (dp[mask][last] == infinity) continue;
        for (int next = 0; next < m; ++next) {
          if ((mask >> next) & 1) continue;
          long long value = dp[mask][last] +
              travel(floor[last], floor[next], upCost, downCost);
          value = max(value, static_cast<long long>(arrival[next]));
          int nextMask = mask | (1 << next);
          dp[nextMask][next] = min(dp[nextMask][next], value);
        }
      }
    }
    return *min_element(dp.back().begin(), dp.back().end());
  }
};
```

## 变种四：两部电梯并行处理

新定义：两部电梯分别从 `startA`、`startB` 于时间 0 出发，请求可分配给任意一部，最小化
全部请求完成的时刻。先分别求每个起点独自处理任意子集的最短时间，再枚举集合划分，取两部
完成时间的最大值。复杂度 $O(2^m m^2)$，空间 $O(2^m m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<long long> allSubsetCosts(
      int start, const vector<int>& floor, const vector<int>& arrival) {
    int m = floor.size();
    int full = 1 << m;
    const long long infinity = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dp(full, vector<long long>(m, infinity));
    vector<long long> cost(full, infinity);
    cost[0] = 0;
    for (int i = 0; i < m; ++i) {
      dp[1 << i][i] = max<long long>(arrival[i], abs(start - floor[i]));
    }
    for (int mask = 1; mask < full; ++mask) {
      for (int last = 0; last < m; ++last) {
        if (dp[mask][last] == infinity) continue;
        cost[mask] = min(cost[mask], dp[mask][last]);
        for (int next = 0; next < m; ++next) {
          if ((mask >> next) & 1) continue;
          long long value = dp[mask][last] + abs(floor[last] - floor[next]);
          value = max(value, static_cast<long long>(arrival[next]));
          int nextMask = mask | (1 << next);
          dp[nextMask][next] = min(dp[nextMask][next], value);
        }
      }
    }
    return cost;
  }
public:
  long long twoElevators(
      int startA, int startB, const vector<vector<int>>& requests) {
    map<int, int> latest;
    for (const auto& request : requests) {
      latest[request[1]] = max(latest[request[1]], request[0]);
    }
    vector<int> floor, arrival;
    for (auto [position, time] : latest) {
      floor.push_back(position);
      arrival.push_back(time);
    }
    vector<long long> first = allSubsetCosts(startA, floor, arrival);
    vector<long long> second = allSubsetCosts(startB, floor, arrival);
    int full = (1 << floor.size()) - 1;
    long long answer = numeric_limits<long long>::max();
    for (int mask = 0; mask <= full; ++mask) {
      answer = min(answer, max(first[mask], second[full ^ mask]));
    }
    return answer;
  }
};
```

## 推荐记忆

看到“空间极大、任务只有十几个、移动后还受 release time 约束”，优先把服务集合压成位掩码。
记住状态的支配关系：同一 `(mask,last)` 中更早到达永远不差，因为等待可以补足任何较晚状态。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/elevator-requests-iii/)
- [对应知识专题](../../dp/subset-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-d/">[codeforces] CF Round 1117 Div.2 D Bermuda Rectangle →</a>
</nav>
