---
title: "[力扣竞赛] 第 189 场双周赛 Q4 LC 4023 电梯请求 II 困难"
---

# [力扣竞赛] 第 189 场双周赛 Q4 LC 4023 电梯请求 II 困难

<p class="daily-archive-kicker">2026-08-25 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-25 题目列表</a> · <a href="../../../dp/interval-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=bf6d31dbf64daf20e9e861156d09a25aa2e3d221cb16a9588cd4c0af93ed2a25 -->
## 官方原始信息

- 来源：[力扣第 189 场双周赛 Q4](https://leetcode.cn/contest/biweekly-contest-189/problems/elevator-requests-ii/)
- 官方题目：[LC 4023 电梯请求 II](https://leetcode.cn/problems/elevator-requests-ii/)
- 官方难度：困难；官方竞赛分值：6 分。
- [ZeroTracer 社区估算竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)：
  2279.903，抓取于 2026-08-25；这不是力扣官方难度或分值。
- 函数签名：`long long elevatorRequests(int n, int start, vector<int>& requests)`。

### 原始题意

一栋楼有编号 $0$ 到 $n-1$ 的楼层。电梯从 `start` 出发，`requests` 中互不相同的请求在
时间 0 同时到达。电梯在所有请求完成前每秒恰好向上或向下移动一层；第一次到达请求楼层时
立即完成该请求。若 `start` 本身被请求，它在时间 0 完成。

一个请求在时间 $t$ 完成就贡献 $t$ 点惩罚。返回所有请求完成时间之和的最小可能值。

### 全部官方样例

```text
示例 1
输入：n = 6, start = 4, requests = [1,5]
输出：6
解释：先到 5 用时 1，再到 1 时刻为 5，总惩罚 1 + 5 = 6。

示例 2
输入：n = 8, start = 3, requests = [3,7,1]
输出：10
解释：3 在时刻 0 完成；先到 1 的时刻为 2，再到 7 的时刻为 8，总惩罚 10。

示例 3
输入：n = 10, start = 5, requests = [0,2,9]
输出：22
解释：依次到 2、0、9 的完成时刻为 3、5、14，总惩罚 22。
```

### 全部约束

- $1\le n\le10^9$。
- $1\le\lvert requests\rvert\le1500$。
- $0\le start,requests_i\le n-1$。
- `requests` 中所有楼层互不相同。

## 最优结论摘要

把请求楼层排序并插入起点。已经走过的最左、最右楼层之间的所有请求必然都已完成，所以状态
只需记录已覆盖区间 $[l,r]$ 以及电梯停在左端还是右端。若还有 $k$ 个请求未完成，移动距离
$d$ 的途中所有这些请求都会多等待 $d$ 秒，转移代价就是 $k\cdot d$。

区间 DP 有 $O(m^2)$ 个状态，每个状态常数次转移，时间和空间均为 $O(m^2)$，其中
$m=\lvert requests\rvert$。这是约束 $m\le1500$ 下最稳妥的实用解。

## 约束推导、溢出与边界

- 楼层总数可达 $10^9$，不能按楼层建图；只有至多 1500 个请求楼层有意义。
- 枚举请求访问顺序是 $m!$，必须利用一维有序结构。
- 走过区间内部时会自动完成内部请求，因此“已完成集合”总能压缩为排序后的连续区间。
- 若 `start` 在 `requests` 中，先删掉这一个请求；它贡献 0，不能计入后续 `remaining`。
- 位置数组插入一个权重为 0 的 `start` 后，区间包含的请求数恰为 $r-l$。
- 最坏完成时间和可达约 $1500^2\times10^9$，必须使用 `long long`。
- 只有一个请求时，答案就是它与 `start` 的距离；请求恰在起点时答案为 0。

## 官方样例手推

样例 3 排序后位置为 $[0,2,5,9]$，起点下标为 2。初始尚有 3 个请求。先从 5 到 2，距离
3，使全部 3 个请求各多等 3 秒，新增 9；再从 2 到 0，距离 2，尚有 2 个请求，新增 4；
最后从 0 到 9，距离 9，只剩 1 个请求，新增 9。总计 $9+4+9=22$，等价于完成时刻
$3+5+14$。

样例 1 若先向左到 1，则代价为 $2\times3+1\times4=10$；先向右到 5，则代价为
$2\times1+1\times4=6$，故官方答案为 6。

## 解法一：枚举全部访问顺序

对小规模请求枚举一个目标访问排列，依次直达排列中的楼层，按到达时刻累加惩罚。路线前往较远
目标时可能提前经过另一个请求，因此并非每个排列都能成为真实的首达顺序；此时程序把被经过
请求记得更晚，只会高估同一路线的真实惩罚。另一方面，任意最优路线的真实首达顺序必是某个
枚举排列，按该排列直达相邻首达楼层时不会漏过新的请求，程序算出的惩罚与最优路线完全相同。
所以所有排列的计算值下界不低于真实最优值，且至少一个恰好等于真实最优值，取最小仍然正确。
时间 $O(m!\,m)$，空间 $O(m)$，仅适合作为随机对拍 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long best;
  void dfs(const vector<int>& request, vector<char>& used, int position, long long time,
      long long penalty, int done) {
    if (done == static_cast<int>(request.size())) {
      best = min(best, penalty);
      return;
    }
    if (penalty >= best)
      return;
    for (int i = 0; i < static_cast<int>(request.size()); ++i) {
      if (used[i])
        continue;
      used[i] = true;
      long long nextTime = time + abs(position - request[i]);
      dfs(request, used, request[i], nextTime, penalty + nextTime, done + 1);
      used[i] = false;
    }
  }
public:
  long long elevatorRequests(int n, int start, vector<int>& requests) {
    (void)n;
    vector<int> pending;
    for (int floor : requests) {
      if (floor != start)
        pending.push_back(floor);
    }
    best = numeric_limits<long long>::max();
    vector<char> used(pending.size(), false);
    dfs(pending, used, start, 0, 0, 0);
    return best == numeric_limits<long long>::max() ? 0 : best;
  }
};
```

## 从排列到连续区间

把请求与起点一起排序。假设当前已经到过最左位置 $a_l$ 和最右位置 $a_r$。在一维线上，从
一端走到另一端会经过中间的全部请求，因此区间内不可能还有未完成请求；下一次新完成请求只
可能是 $a_{l-1}$ 或 $a_{r+1}$。这把任意集合状态压缩成区间两端。

直接累加每个完成时刻不方便转移，但可交换求和顺序：移动一段距离 $d$ 时，每个尚未完成的
请求都把完成时刻增加 $d$，故总惩罚增加 `remaining * d`。

## 最佳实用解：排序加双端区间 DP

先删除恰在起点、已于时刻 0 完成的请求，令剩余待处理请求数为 $q$。令
`dp[l,r,0/1]` 表示恰好完成区间 $[l,r]$ 内全部请求并停在左/右端的最小累计惩罚。
区间始终包含起点。该区间含有 $r-l$ 个真实请求，所以扩展前剩余
$q-(r-l)$ 个请求。

### 正确性证明

**区间引理**：任一路线到达当前最左请求和最右请求后，两者之间的请求均已完成。因为电梯
沿整数楼层连续移动，连接两端的路径必经过所有中间楼层。

由区间引理，任何未完成请求只在当前区间两侧。最优路线的下一次首次完成请求必是紧邻区间的
$a_{l-1}$ 或 $a_{r+1}$；若越过它去更远位置，经过它时已经先完成，与所述转移等价。

对任一状态，算法分别从当前左端和右端走向两个可能的新端点。移动距离 $d$ 时恰有
`remaining` 个请求仍未完成，因此每个完成时刻都增加 $d$，转移新增惩罚精确为
`remaining * d`。初态只含起点、代价为 0；全部区间状态按长度递增计算，不漏掉任何最优
首达次序。最终覆盖所有请求，两个端点状态取小即为全局最优。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long elevatorRequests(int n, int start, vector<int>& requests) {
    (void)n;
    vector<int> position;
    for (int floor : requests) {
      if (floor != start)
        position.push_back(floor);
    }
    int requestCount = position.size();
    position.push_back(start);
    sort(position.begin(), position.end());
    int size = position.size();
    int source = lower_bound(position.begin(), position.end(), start) - position.begin();
    constexpr long long INF = 4000000000000000000LL;
    vector<array<long long, 2>> dp(size * size, array<long long, 2>{INF, INF});
    auto state = [size](int left, int right) { return left * size + right; };
    dp[state(source, source)][0] = 0;
    dp[state(source, source)][1] = 0;
    for (int length = 1; length <= size; ++length) {
      for (int left = 0; left + length <= size; ++left) {
        int right = left + length - 1;
        if (left > source || right < source)
          continue;
        int remaining = requestCount - (right - left);
        if (remaining == 0)
          continue;
        auto current = dp[state(left, right)];
        if (left > 0) {
          long long fromLeft = position[left] - position[left - 1];
          long long fromRight = position[right] - position[left - 1];
          auto& next = dp[state(left - 1, right)][0];
          next = min(next, current[0] + remaining * fromLeft);
          next = min(next, current[1] + remaining * fromRight);
        }
        if (right + 1 < size) {
          long long fromLeft = position[right + 1] - position[left];
          long long fromRight = position[right + 1] - position[right];
          auto& next = dp[state(left, right + 1)][1];
          next = min(next, current[0] + remaining * fromLeft);
          next = min(next, current[1] + remaining * fromRight);
        }
      }
    }
    return min(dp[state(0, size - 1)][0], dp[state(0, size - 1)][1]);
  }
};
```

时间复杂度 $O(m^2)$，空间复杂度 $O(m^2)$。

## 同阶方案比较与易错点

自顶向下记忆化与自底向上区间 DP 都是 $O(m^2)$。递归写法只访问可达区间，但深度可达
1500；自底向上没有栈风险，状态顺序和剩余请求数也更直观，竞赛中优先记忆后者。

- 把移动代价只加一次距离，忘记乘尚未完成请求数。
- 扩展后才计算 `remaining`，少算刚到达请求在这段路上的等待。
- `start` 已在请求中时仍把它计作未完成请求。
- 用 `int` 保存惩罚或计算 `remaining * distance`。
- 认为下一请求可以任意选择；排序后只能扩展当前区间的相邻端点。
- 把楼层总数 $n$ 当作 DP 规模；真正规模是请求数。

## 可复现验证

暴力排列与区间 DP 均以 C++23 编译，并通过三个官方样例、单请求、请求在起点、全部请求位于
同一侧、起点在两请求之间及最大坐标差边界。随机生成至多 8 个互异请求，逐例比较排列 oracle
与 $O(m^2)$ DP；更大随机集另与独立的同状态递归实现比较。

## Follow-up 与约束变种

### 变种一：恢复一条最优访问顺序

新定义：除最小惩罚外，还返回一条“时刻 0 之后的待处理请求”的最优首达顺序。若 `start`
本身被请求，它已在时刻 0 完成，不重复放进这个序列。每次松弛保存前驱区间与前驱端点，从最终
较优状态回溯；当前区间相对前驱新增的那一端就是本步请求。复杂度仍为 $O(m^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Parent {
  short left = -1;
  short right = -1;
  char side = -1;
};
pair<long long, vector<int>> solve(int start, vector<int> requests) {
  requests.erase(remove(requests.begin(), requests.end(), start), requests.end());
  int requestCount = requests.size();
  requests.push_back(start);
  sort(requests.begin(), requests.end());
  int size = requests.size();
  int source = lower_bound(requests.begin(), requests.end(), start) - requests.begin();
  constexpr long long INF = 4000000000000000000LL;
  vector<array<long long, 2>> dp(size * size, array<long long, 2>{INF, INF});
  vector<array<Parent, 2>> parent(size * size);
  auto id = [size](int left, int right) { return left * size + right; };
  dp[id(source, source)] = {0, 0};
  auto relax = [&](int nl, int nr, int ns, long long value, int pl, int pr, int ps) {
    if (value < dp[id(nl, nr)][ns]) {
      dp[id(nl, nr)][ns] = value;
      parent[id(nl, nr)][ns] = Parent{short(pl), short(pr), char(ps)};
    }
  };
  for (int length = 1; length <= size; ++length) {
    for (int left = 0; left + length <= size; ++left) {
      int right = left + length - 1;
      if (left > source || right < source)
        continue;
      int remaining = requestCount - (right - left);
      if (!remaining)
        continue;
      for (int side = 0; side < 2; ++side) {
        long long current = dp[id(left, right)][side];
        if (current == INF)
          continue;
        int at = side ? requests[right] : requests[left];
        if (left) {
          relax(left - 1, right, 0, current + 1LL * remaining * abs(at - requests[left - 1]), left,
              right, side);
        }
        if (right + 1 < size) {
          relax(left, right + 1, 1, current + 1LL * remaining * abs(at - requests[right + 1]), left,
              right, side);
        }
      }
    }
  }
  int left = 0;
  int right = size - 1;
  int side = dp[id(left, right)][0] <= dp[id(left, right)][1] ? 0 : 1;
  long long answer = dp[id(left, right)][side];
  vector<int> order;
  while (left != source || right != source) {
    Parent previous = parent[id(left, right)][side];
    if (left < previous.left)
      order.push_back(requests[left]);
    else
      order.push_back(requests[right]);
    left = previous.left;
    right = previous.right;
    side = previous.side;
  }
  reverse(order.begin(), order.end());
  return {answer, order};
}
int main() {
  int m;
  int start;
  cin >> m >> start;
  vector<int> requests(m);
  for (int& floor : requests)
    cin >> floor;
  auto [penalty, order] = solve(start, requests);
  cout << penalty << '\n';
  for (int i = 0; i < static_cast<int>(order.size()); ++i) {
    if (i)
      cout << ' ';
    cout << order[i];
  }
  cout << '\n';
  return 0;
}
```

### 变种二：请求带权或同层重复

新定义：至多 1500 个请求，楼层仍在 $[0,10^9]$；每个楼层 $x_i$ 有正整数权重
$1\le w_i\le1000$，未完成每秒贡献 $w_i$；同一楼层可出现多次并合并权重。正权保证无意义
绕路不会获益，给定上界也使答案严格小于代码的 `INF = 4e18`。原来的“剩余个数”改成“剩余
总权重”。排序压缩楼层后，用前缀权重计算区间已完成权重。若 $u$ 为不同请求楼层数，时间为
$O(m\log u+u^2)$，空间为 $O(u^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long weightedElevator(int start, const vector<int>& floor, const vector<long long>& weight) {
  map<int, long long> merged;
  for (int i = 0; i < static_cast<int>(floor.size()); ++i) {
    if (floor[i] != start)
      merged[floor[i]] += weight[i];
  }
  merged[start] += 0;
  vector<int> position;
  vector<long long> value;
  for (auto [x, w] : merged) {
    position.push_back(x);
    value.push_back(w);
  }
  int size = position.size();
  int source = lower_bound(position.begin(), position.end(), start) - position.begin();
  vector<long long> prefix(size + 1, 0);
  for (int i = 0; i < size; ++i)
    prefix[i + 1] = prefix[i] + value[i];
  long long totalWeight = prefix.back();
  constexpr long long INF = 4000000000000000000LL;
  vector<array<long long, 2>> dp(size * size, array<long long, 2>{INF, INF});
  auto id = [size](int left, int right) { return left * size + right; };
  dp[id(source, source)] = {0, 0};
  for (int length = 1; length <= size; ++length) {
    for (int left = 0; left + length <= size; ++left) {
      int right = left + length - 1;
      if (left > source || right < source)
        continue;
      long long visited = prefix[right + 1] - prefix[left];
      long long remaining = totalWeight - visited;
      auto current = dp[id(left, right)];
      if (left) {
        dp[id(left - 1, right)][0] = min(dp[id(left - 1, right)][0],
            current[0] + remaining * (position[left] - position[left - 1]));
        dp[id(left - 1, right)][0] = min(dp[id(left - 1, right)][0],
            current[1] + remaining * (position[right] - position[left - 1]));
      }
      if (right + 1 < size) {
        dp[id(left, right + 1)][1] = min(dp[id(left, right + 1)][1],
            current[0] + remaining * (position[right + 1] - position[left]));
        dp[id(left, right + 1)][1] = min(dp[id(left, right + 1)][1],
            current[1] + remaining * (position[right + 1] - position[right]));
      }
    }
  }
  return min(dp[id(0, size - 1)][0], dp[id(0, size - 1)][1]);
}
int main() {
  int m;
  int start;
  cin >> m >> start;
  vector<int> floor(m);
  vector<long long> weight(m);
  for (int& value : floor)
    cin >> value;
  for (long long& value : weight)
    cin >> value;
  cout << weightedElevator(start, floor, weight) << '\n';
  return 0;
}
```

### 变种三：上行和下行每层耗时不同

新定义：楼层和请求数沿用原题，并规定上行、下行每层耗时都是 $[1,1000]$ 内的正整数。
正耗时保证绕路不会获益，范围上界使答案严格小于代码的 `INF = 4e18`。区间性质仍成立，只需
把绝对距离改成有向移动时间；转移仍乘剩余请求数，复杂度 $O(m^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long asymmetricElevator(
    int start, vector<int> requests, long long upTime, long long downTime) {
  requests.erase(remove(requests.begin(), requests.end(), start), requests.end());
  int requestCount = requests.size();
  requests.push_back(start);
  sort(requests.begin(), requests.end());
  int size = requests.size();
  int source = lower_bound(requests.begin(), requests.end(), start) - requests.begin();
  auto travel = [&](int from, int to) {
    return from <= to ? 1LL * (to - from) * upTime : 1LL * (from - to) * downTime;
  };
  constexpr long long INF = 4000000000000000000LL;
  vector<array<long long, 2>> dp(size * size, array<long long, 2>{INF, INF});
  auto id = [size](int left, int right) { return left * size + right; };
  dp[id(source, source)] = {0, 0};
  for (int length = 1; length <= size; ++length) {
    for (int left = 0; left + length <= size; ++left) {
      int right = left + length - 1;
      if (left > source || right < source)
        continue;
      int remaining = requestCount - (right - left);
      for (int side = 0; side < 2; ++side) {
        long long current = dp[id(left, right)][side];
        if (current == INF)
          continue;
        int at = side ? requests[right] : requests[left];
        if (left) {
          dp[id(left - 1, right)][0] =
              min(dp[id(left - 1, right)][0], current + remaining * travel(at, requests[left - 1]));
        }
        if (right + 1 < size) {
          dp[id(left, right + 1)][1] = min(
              dp[id(left, right + 1)][1], current + remaining * travel(at, requests[right + 1]));
        }
      }
    }
  }
  return min(dp[id(0, size - 1)][0], dp[id(0, size - 1)][1]);
}
int main() {
  int m;
  int start;
  long long upTime;
  long long downTime;
  cin >> m >> start >> upTime >> downTime;
  vector<int> requests(m);
  for (int& floor : requests)
    cin >> floor;
  cout << asymmetricElevator(start, requests, upTime, downTime) << '\n';
  return 0;
}
```

### 变种四：目标改为最小化最后完成时间

新定义：不再求完成时间之和，只求处理全部请求的最短总时间。此时无需关心中间请求的等待；
只要覆盖最左请求 $L$ 和最右请求 $R$。先去左端再到右端，或先去右端再到左端，取较小者，
时间 $O(m)$，空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minimumMakespan(int start, const vector<int>& requests) {
  int left = *min_element(requests.begin(), requests.end());
  int right = *max_element(requests.begin(), requests.end());
  long long leftFirst = 1LL * abs(start - left) + right - left;
  long long rightFirst = 1LL * abs(right - start) + right - left;
  return min(leftFirst, rightFirst);
}
int main() {
  int m;
  int start;
  cin >> m >> start;
  vector<int> requests(m);
  for (int& floor : requests)
    cin >> floor;
  cout << minimumMakespan(start, requests) << '\n';
  return 0;
}
```

## 推荐记忆

一维线上“走过两端就顺便覆盖中间”是状态压缩的根。再把完成时间和改写成“每段移动距离 ×
尚未完成请求数”，就得到标准双端区间 DP。推荐优先记住这个代价交换视角，而不是死背四条转移。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/elevator-requests-ii/)
- [对应知识专题](../../dp/interval-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2253-a/">[codeforces] CF Educational Round 193 Div.2 A The Best Card →</a>
</nav>
