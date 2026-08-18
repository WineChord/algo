---
title: "[力扣竞赛] 第 515 场周赛 Q2 LC 4025 交通灯的最大等待时间 中等"
---

# [力扣竞赛] 第 515 场周赛 Q2 LC 4025 交通灯的最大等待时间 中等

<p class="daily-archive-kicker">2026-08-19 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-19 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0ebf5af5346cbc0775ae2649a43b7241aeb7120878decbcbe51b753b97cc4c99 -->
[官方题目：4025. 交通灯的最大等待时间](https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/)

## 官方原始信息

- 比赛：第 515 场周赛；题目位置：Q2；官方竞赛分值：4。
- 题号与标题：LC 4025「交通灯的最大等待时间」；官方难度：中等。
- ZeroTracer 社区估算竞赛分：截至 2026-08-19 的公开数据中尚无可可靠映射的数值，记为未知。
- 函数签名：`int minPenalty(int period, vector<int>& lights, vector<int>& arrivalTime)`。
- 官方链接：[力扣中国题目页](https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/)。

所有交通灯从时间 0 同步开始周期，每个周期长度均为 `period`。第 $i$ 盏灯先绿
`lights[i]` 秒，再红 `period - lights[i]` 秒。第 $j$ 辆车在 `arrivalTime[j]` 到达，必须
选择一盏灯；灯没有容量限制，车辆互不阻塞。

令 $r=arrivalTime_j\bmod period$。若 $r<lights_i$，车辆在第 $i$ 盏灯等待 0 秒；否则
等待 $period-r$ 秒。一次分配的惩罚是所有车辆等待时间的最大值，求可能的最小惩罚。

### 全部官方样例

示例 1：

```text
输入：period = 8, lights = [2,3], arrivalTime = [2,5,8,11]
输出：5
```

余数为 `[2,5,0,3]`。绿灯最长持续 3 秒，所以余数 2 和 0 可零等待；余数 5、3 分别至少
等待 3、5 秒，最大值为 5。

示例 2：

```text
输入：period = 10, lights = [3,6,8], arrivalTime = [4,9,15]
输出：1
```

余数为 `[4,9,5]`，选择绿灯时长 8 的交通灯后，三辆车最小等待分别为 0、1、0。

示例 3：

```text
输入：period = 5, lights = [2], arrivalTime = [2,3,4,5,6]
输出：3
```

唯一交通灯下的等待时间依次为 3、2、1、0、0，最大值为 3。

### 全部官方约束

- $2\le period\le10^9$。
- $1\le\lvert lights\rvert\le10^4$。
- $1\le lights_i\le period-1$。
- $1\le\lvert arrivalTime\rvert\le10^5$。
- $1\le arrivalTime_j\le10^9$。

## 约束推导与独立选择结构

车辆之间没有容量竞争，也不会互相延误，因此每辆车都能独立选择对自己最优的灯。设

$$
G=\max_i lights_i.
$$

对某辆车的周期余数 $r$：

- 若 $r<G$，绿灯长度为 $G$ 的那盏灯仍为绿灯，最小等待为 0。
- 若 $r\ge G$，由于每盏灯的绿灯长度都不超过 $G$，此时所有灯均已进入红灯；它们在下一
  周期又同时变绿，最小等待统一为 $period-r$。

所以完整的灯数组可以压缩成一个最大值 $G$。输入规模要求接近线性算法；所有单车等待小于
`period`，最终最大值放入 `int` 没有溢出风险。

## 样例手推与边界

样例 1 中 $G=3$。余数 2 满足 $2<3$，注意严格不等号使它零等待；余数 3 刚好等于 $G$，
绿灯区间已经结束，需要等待 $8-3=5$ 秒，这正是答案。

- $r=0$：新周期刚开始，必为零等待。
- $r=G$：绿灯按半开区间 $[0,G)$ 计算，必须等待 `period - G`。
- 多盏灯具有同一最大绿灯时长：任选一盏即可，答案不变。
- 到达时间大于一个周期：只看对 `period` 的余数。
- 只有一盏灯：公式仍直接成立。
- 最大惩罚由最差车辆决定，不能把等待时间求和。

## 解法一：逐车枚举全部交通灯

对每辆车计算余数，再枚举每盏灯求该车最小等待，最后取这些最小值的最大值。它直接枚举
所有合法分配边，因而是正确暴力解。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minPenalty(int period, vector<int>& lights, vector<int>& arrivalTime) {
    int answer = 0;
    for (int arrival : arrivalTime) {
      int remainder = arrival % period;
      int best = period;
      for (int green : lights) {
        int wait = remainder < green ? 0 : period - remainder;
        best = min(best, wait);
      }
      answer = max(answer, best);
    }
    return answer;
  }
};
```

时间复杂度为 $O(AC)$，其中 $A=\lvert arrivalTime\rvert$、$C=\lvert lights\rvert$；最坏
达到 $10^9$ 次比较。额外空间 $O(1)$。瓶颈是每辆车都重复寻找相同的最长绿灯。

## 从二维枚举到一个充分统计量

固定余数 $r$ 时，某盏灯能否给出零等待只取决于 `lights[i] > r`。若任何灯满足，最大绿灯
$G$ 必然满足；若最大值都不满足，则没有其他灯满足。不能零等待时，题面公式 `period - r`
又与具体灯无关。因此每辆车无需知道灯的排序或数量，只需共享 $G$。

## 最佳实用解：最长绿灯加一次扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minPenalty(int period, vector<int>& lights, vector<int>& arrivalTime) {
    int longestGreen = *max_element(lights.begin(), lights.end());
    int answer = 0;
    for (int arrival : arrivalTime) {
      int remainder = arrival % period;
      if (remainder >= longestGreen) answer = max(answer, period - remainder);
    }
    return answer;
  }
};
```

时间复杂度为 $O(C+A)$，额外空间 $O(1)$。它必须至少读完灯数组以确定最大值，也必须读完
每个到达时间以发现最坏车辆，因此渐近最优。

### 正确性证明

对任意车辆，设余数为 $r$。若 $r<G$，最大绿灯对应的灯在该周期的第 $r$ 秒仍为绿灯，
车辆可零等待；等待时间不可能小于 0，所以这是最优。若 $r\ge G$，任意灯都有
$lights_i\le G\le r$，全部处于红灯；所有周期同步结束，任意选择都要等到下一周期开始，
恰为 $period-r$。算法逐车算出的正是该车的最小等待。

车辆选择相互独立，所以同时采用各自最优选择是一个合法全局分配。全局惩罚定义为这些最小
等待的最大值，算法恰好取该最大值，故答案最优。

## 同阶方案与推荐

可以先把每个到达时间映射成余数并排序，再检查红灯区间中的最小余数；复杂度会变成
$O(A\log A+C)$，没有收益。也可在扫描时维护“红灯余数的最小值”，最后用
`period - minRemainder`，与直接维护最大等待完全等价。优先记忆“独立决策 + 最大绿灯充分
统计量”，代码更短，证明也直接。

## 易错点

- 把条件写成 `remainder <= longestGreen`；在 $r=G$ 时灯已变红。
- 误以为每辆车必须分配不同交通灯；原题没有容量限制。
- 对到达时间直接与绿灯长度比较，忘记先取模。
- 认为不同灯的红灯结束时间不同；所有灯周期同步，下一次变绿时刻相同。
- 求所有等待之和，而不是最大等待。
- 用最大到达余数决定答案；在红灯区间内余数越小，等待反而越长。

## 验证说明

三组官方样例均通过。额外覆盖 $r=0$、$r=G-1$、$r=G$、$r=period-1$、单灯、多个并列
最大灯和跨多个周期的到达时间。随机对拍可生成小 `period`、灯和车辆数组，将线性公式与
逐车逐灯暴力枚举逐项比较。

## 变种一：返回一组具体分配

新定义：除最小惩罚外，还返回每辆车所选交通灯的下标。选择任意一盏最长绿灯对所有车辆都
达到各自最小等待，因此可以全部指向同一下标。时间 $O(C+A)$，输出之外额外空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int period, lightCount, carCount;
  cin >> period >> lightCount >> carCount;
  vector<int> lights(lightCount);
  vector<int> arrivalTime(carCount);
  for (int& green : lights) cin >> green;
  for (int& arrival : arrivalTime) cin >> arrival;
  int bestLight = max_element(lights.begin(), lights.end()) - lights.begin();
  int penalty = 0;
  for (int arrival : arrivalTime) {
    int remainder = arrival % period;
    if (remainder >= lights[bestLight]) penalty = max(penalty, period - remainder);
  }
  cout << penalty << '\n';
  for (int i = 0; i < carCount; ++i) cout << bestLight << " \n"[i + 1 == carCount];
  return 0;
}
```

## 变种二：把目标改为总等待时间最小

新定义：惩罚是所有车辆等待时间之和。车辆依旧没有耦合，因此每辆车仍独立选择最长绿灯，
但聚合运算从 `max` 改为求和。最多 $10^5$ 辆车、单车等待接近 $10^9$，答案要用
`long long`。时间 $O(C+A)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int period, lightCount, carCount;
  cin >> period >> lightCount >> carCount;
  int longestGreen = 0;
  for (int i = 0; i < lightCount; ++i) {
    int green;
    cin >> green;
    longestGreen = max(longestGreen, green);
  }
  long long totalWait = 0;
  for (int i = 0; i < carCount; ++i) {
    int arrival;
    cin >> arrival;
    int remainder = arrival % period;
    if (remainder >= longestGreen) totalWait += period - remainder;
  }
  cout << totalWait << '\n';
  return 0;
}
```

## 变种三：每盏灯有独立相位

新定义：第 $i$ 盏灯每周期在 `offset[i]` 开始，连续绿 `length[i]` 秒，区间可跨周期边界；
车辆仍可自由选灯。最大绿灯长度不再足够，因为相位决定覆盖位置。若灯和车辆均不超过
2000，可逐车逐灯计算到下一个绿色区间的循环等待，时间 $O(AC)$、空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int waitTime(int period, int offset, int length, int arrival) {
  int position = (arrival % period - offset + period) % period;
  if (position < length) return 0;
  return period - position;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int period, lightCount, carCount;
  cin >> period >> lightCount >> carCount;
  vector<int> offset(lightCount), length(lightCount);
  for (int i = 0; i < lightCount; ++i) cin >> offset[i] >> length[i];
  int answer = 0;
  for (int car = 0; car < carCount; ++car) {
    int arrival;
    cin >> arrival;
    int best = period;
    for (int light = 0; light < lightCount; ++light) {
      best = min(best, waitTime(period, offset[light], length[light], arrival));
    }
    answer = max(answer, best);
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种四：每盏灯有总容量

新定义：第 $i$ 盏灯最多接收 `capacity[i]` 辆车，仍最小化最大等待；车辆数和灯数均不超过
200。独立性失效，某个阈值 $T$ 是否可行变成带容量二分图匹配：车辆向等待不超过 $T$ 的
灯连边，灯到汇点容量为其接车数。可行性随 $T$ 单调，二分 $[0,period-1]$ 并用最大流判定。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Dinic {
  struct Edge { int to, reverse, capacity; };
  vector<vector<Edge>> graph;
  vector<int> level, nextEdge;
  explicit Dinic(int n) : graph(n), level(n), nextEdge(n) {}
  void addEdge(int from, int to, int capacity) {
    Edge forward{to, static_cast<int>(graph[to].size()), capacity};
    Edge backward{from, static_cast<int>(graph[from].size()), 0};
    graph[from].push_back(forward);
    graph[to].push_back(backward);
  }
  bool bfs(int source, int sink) {
    fill(level.begin(), level.end(), -1);
    queue<int> order;
    level[source] = 0;
    order.push(source);
    while (!order.empty()) {
      int node = order.front();
      order.pop();
      for (const Edge& edge : graph[node]) {
        if (edge.capacity > 0 && level[edge.to] == -1) {
          level[edge.to] = level[node] + 1;
          order.push(edge.to);
        }
      }
    }
    return level[sink] != -1;
  }
  int dfs(int node, int sink, int flow) {
    if (node == sink) return flow;
    for (int& index = nextEdge[node]; index < static_cast<int>(graph[node].size()); ++index) {
      Edge& edge = graph[node][index];
      if (edge.capacity == 0 || level[edge.to] != level[node] + 1) continue;
      int pushed = dfs(edge.to, sink, min(flow, edge.capacity));
      if (pushed == 0) continue;
      edge.capacity -= pushed;
      graph[edge.to][edge.reverse].capacity += pushed;
      return pushed;
    }
    return 0;
  }
  int maxFlow(int source, int sink) {
    int flow = 0;
    while (bfs(source, sink)) {
      fill(nextEdge.begin(), nextEdge.end(), 0);
      while (int pushed = dfs(source, sink, numeric_limits<int>::max())) flow += pushed;
    }
    return flow;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int period, lightCount, carCount;
  cin >> period >> lightCount >> carCount;
  vector<int> lights(lightCount), capacity(lightCount), arrivalTime(carCount);
  for (int& green : lights) cin >> green;
  for (int& limit : capacity) cin >> limit;
  for (int& arrival : arrivalTime) cin >> arrival;
  auto feasible = [&](int threshold) {
    int source = carCount + lightCount;
    int sink = source + 1;
    Dinic flow(sink + 1);
    for (int car = 0; car < carCount; ++car) {
      flow.addEdge(source, car, 1);
      int remainder = arrivalTime[car] % period;
      for (int light = 0; light < lightCount; ++light) {
        int wait = remainder < lights[light] ? 0 : period - remainder;
        if (wait <= threshold) flow.addEdge(car, carCount + light, 1);
      }
    }
    for (int light = 0; light < lightCount; ++light) {
      flow.addEdge(carCount + light, sink, capacity[light]);
    }
    return flow.maxFlow(source, sink) == carCount;
  };
  if (!feasible(period - 1)) {
    cout << -1 << '\n';
    return 0;
  }
  int low = 0;
  int high = period - 1;
  while (low < high) {
    int middle = low + (high - low) / 2;
    if (feasible(middle)) high = middle;
    else low = middle + 1;
  }
  cout << low << '\n';
  return 0;
}
```

## 来源

- [力扣中国：第 515 场周赛](https://leetcode.cn/contest/weekly-contest-515/)
- [力扣中国：4025. 交通灯的最大等待时间](https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-139-lc79/">← [力扣 Top 139] LC 79 单词搜索 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-b/">[codeforces] CF Round 1117 Div.2 B Gigantomachy →</a>
</nav>
