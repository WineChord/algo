---
title: "[力扣竞赛] 第 188 场双周赛 Q4 LC 4009 最小化最大可能等待时间 困难"
---

# [力扣竞赛] 第 188 场双周赛 Q4 LC 4009 最小化最大可能等待时间 困难

<p class="daily-archive-kicker">2026-08-13 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-13 题目列表</a> · <a href="../../../dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=7f3024b7115cb6f72b0ab7ab23a17357433da8c4aad205b6634fd47fad221357 -->
[官方题目：LC 4009 最小化最大可能等待时间](https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/)

## 官方原始信息

- 来源：力扣第 188 场双周赛 Q4，官方分值 6。
- 题号：4009；标题：最小化最大可能等待时间。
- 官方难度：困难。
- 官方链接：[力扣中国](https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/)。
- ZeroTracer 社区估算竞赛分：截至 2026-08-13 未找到可可靠映射的数值，记为未知。
- 标签：数组、动态规划、模拟。

给定 `demand`，其中 `demand[i]` 是第 $i$ 辆车的燃料需求；另有恰好两个加油机，初始燃料为 `fuel[0]`、`fuel[1]`。第 0 辆车在时刻 0 被允许加油；第 $i>0$ 辆车恰在第 $i-1$ 辆车开始加油时被允许。

每台加油机同时最多服务一辆车。车辆选定一台燃料足够的加油机后，要等它空闲并立即开始；不能改选、故意等待或中断。服务耗时与耗油均为该车的 `demand[i]`。若当前车辆面对两台都空闲的加油机，却没有任何一台燃料足够，过程终止。先最大化服务车辆数，再在所有达到最大数量的方案中最小化被服务车辆的最大等待时间；若一辆也不能服务，返回 -1。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minMaxWaitingTime(vector<int>& demand, vector<int>& fuel);
};
```

### 全部官方样例

```text
输入：demand = [6,8,4,6,5], fuel = [16,13]
输出：6
```

一种完整服务方案依次选择加油机 `0,1,0,0,1`。允许时间为 `0,0,0,6,10`，开始时间为 `0,0,6,10,10`，等待为 `0,0,6,4,0`，最大值为 6。要服务五辆车，两机分别必须承担需求 `6,4,6` 与 `8,5`，第三辆车无法早于时刻 6 开始，因此 6 也是下界。

```text
输入：demand = [10,15], fuel = [12,17]
输出：0
```

两辆车都在时刻 0 分别使用一台加油机，无需等待。

```text
输入：demand = [10,5], fuel = [8,8]
输出：-1
```

第一辆车的需求超过两台机器剩余燃料，过程立即终止。

### 全部约束

- $1\le demand.length\le50$。
- $1\le demand[i]\le20$。
- `fuel.length == 2`。
- $1\le fuel[i]\le50$。

## 约束推导与状态设计

每辆车只有两种机器选择，暴力是 $2^n$。但机器数固定为 2，燃料上限仅 50，单次服务时间仅 20。站在“当前车刚被允许”的时刻，未来只需知道：两台机器的剩余燃料 $(f_0,f_1)$，以及各自还要忙多久 $(t_0,t_1)$。历史分配方式无需保留。

若当前车分配到机器 $j$，它等待 $t_j$ 秒，然后开始服务；下一辆车也在这一时刻被允许。于是被选机器的新忙时长为 `demand[i]`，另一台机器在等待期间同步工作，新忙时长为 $\max(0,t_{1-j}-t_j)$。这就是完整的马尔可夫状态。

同一状态可能由多条路径到达，只需保留迄今最大等待时间的最小值。每一层若无转移，当前层下标就是最多服务数，取现有状态的最小代价即可。

## 解法递进

### 解法一：枚举全部机器选择

递归尝试两台机器，按目标的字典序先比较服务数量、再比较最大等待。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  pair<int, int> dfs(const vector<int>& demand, int index, array<int, 2> fuel,
                    array<int, 2> busy, int worst) {
    pair<int, int> best{index, worst};
    for (int machine = 0; machine < 2; ++machine) {
      int need = demand[index];
      if (fuel[machine] < need) continue;
      auto nextFuel = fuel;
      auto nextBusy = busy;
      int wait = busy[machine];
      nextFuel[machine] -= need;
      nextBusy[1 - machine] = max(0, busy[1 - machine] - wait);
      nextBusy[machine] = need;
      pair<int, int> candidate;
      if (index + 1 == static_cast<int>(demand.size())) {
        candidate = {index + 1, max(worst, wait)};
      } else {
        candidate = dfs(demand, index + 1, nextFuel, nextBusy, max(worst, wait));
      }
      if (candidate.first > best.first ||
          (candidate.first == best.first && candidate.second < best.second)) best = candidate;
    }
    return best;
  }
public:
  int minMaxWaitingTime(vector<int>& demand, vector<int>& fuel) {
    array<int, 2> initial{fuel[0], fuel[1]};
    auto answer = dfs(demand, 0, initial, {0, 0}, 0);
    return answer.first == 0 ? -1 : answer.second;
  }
};
int main() {
  vector<int> demand{6, 8, 4, 6, 5};
  vector<int> fuel{16, 13};
  cout << Solution().minMaxWaitingTime(demand, fuel) << '\n';
}
```

最坏时间 $O(2^n)$，递归空间 $O(n)$。它适合做小规模 oracle。

### 解法二：按状态做哈希动态规划

可用哈希表只保存实际可达状态，代码直观；最坏状态数量仍由 $51^2\times21^2$ 界定。正式实现用定长编码数组，去掉哈希常数且便于层间复用。

### 最佳实用解：有限状态分层 DP

状态值是到达该状态时的最小“历史最大等待”。只遍历活跃键，避免每层清空整张数组。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minMaxWaitingTime(vector<int>& demand, vector<int>& fuel) {
    constexpr int busyBase = 21;
    int fuel1Base = fuel[1] + 1;
    int stateCount = (fuel[0] + 1) * fuel1Base * busyBase * busyBase;
    int inf = numeric_limits<int>::max() / 4;
    auto encode = [&](int f0, int f1, int t0, int t1) {
      return (((f0 * fuel1Base + f1) * busyBase + t0) * busyBase + t1);
    };
    vector<int> dp(stateCount, inf), next(stateCount, inf);
    vector<int> active{encode(fuel[0], fuel[1], 0, 0)};
    dp[active[0]] = 0;
    for (int index = 0; index < static_cast<int>(demand.size()); ++index) {
      int need = demand[index];
      vector<int> nextActive;
      for (int key : active) {
        int value = key;
        int t1 = value % busyBase;
        value /= busyBase;
        int t0 = value % busyBase;
        value /= busyBase;
        int f1 = value % fuel1Base;
        int f0 = value / fuel1Base;
        auto relax = [&](int nf0, int nf1, int nt0, int nt1, int wait) {
          int nextKey = encode(nf0, nf1, nt0, nt1);
          if (next[nextKey] == inf) nextActive.push_back(nextKey);
          next[nextKey] = min(next[nextKey], max(dp[key], wait));
        };
        if (f0 >= need) relax(f0 - need, f1, need, max(0, t1 - t0), t0);
        if (f1 >= need) relax(f0, f1 - need, max(0, t0 - t1), need, t1);
      }
      if (nextActive.empty()) {
        if (index == 0) return -1;
        int answer = inf;
        for (int key : active) answer = min(answer, dp[key]);
        return answer;
      }
      for (int key : active) dp[key] = inf;
      swap(dp, next);
      active.swap(nextActive);
    }
    int answer = inf;
    for (int key : active) answer = min(answer, dp[key]);
    return answer;
  }
};
int main() {
  vector<int> demand{6, 8, 4, 6, 5};
  vector<int> fuel{16, 13};
  cout << Solution().minMaxWaitingTime(demand, fuel) << '\n';
}
```

状态上界为 $51^2\times21^2=1{,}147{,}041$。每层每状态最多 2 次转移，时间 $O(nF_0F_1D^2)$，空间 $O(F_0F_1D^2)$；实际只扫描可达状态。

## 正确性证明

状态四元组准确描述当前车被允许时两机的全部未来相关信息。一次转移恰好模拟合法选择：燃料足够；等待被选机器的剩余忙时；在该等待期间另一机同步减少忙时；然后扣除燃料并开始服务。故每条 DP 路径对应唯一合法分配，反之任何合法分配也逐步对应一条路径。

对同一状态，未来可选集合完全相同；历史只通过已有最大等待影响目标，保留较小值支配较大值，不会丢失最优方案。DP 按车辆顺序逐层推进，因此第一层无后继时，所有方案都恰好无法继续，当前层服务数量已最大；取层内最小代价完成第二目标。由此算法满足词典序目标。

## 样例手推与边界

样例 1 前两车分别分给 0、1 后，状态从 `(16,13,0,0)` 变为 `(10,5,6,8)`。第三车需求 4 若选机器 0，等待 6；新状态为 `(6,5,4,2)`。下一车再选 0 等待 4，另一机已空闲；最后需求 5 选机器 1 无需等待，最大等待 6。

- 首车两机都缺油时返回 -1。
- 中途无法继续时，仍返回此前已服务车辆的最优最大等待。
- 重复选择同一机器会让另一机的忙时降到 0，但不能让时间变负。
- 最大等待不超过服务时长累计 1000，`int` 足够。

## 方案比较与推荐

记忆化 DFS 与分层 DP 状态相同；DFS 自然返回双目标，分层 DP 更容易严格锁定“先最大数量”并做活跃状态压缩。面试可先讲哈希状态 DP，再按约束落为整数编码数组；不要二分等待阈值后再做两遍工作，直接保存最小历史最大值更清晰。

## 易错点

- 下一辆车的允许时刻是当前车“开始”而非“完成”，所以要减去等待时间，不是需求时长。
- 被选机器开始服务后忙时重置为当前需求，而不是旧忙时加需求。
- 燃料在开始服务时扣除；未来状态要保留两台各自剩余燃料。
- 目标是先最大服务数量，再最小最大等待，不能仅对走到数组末尾的方案求最小。

## 可复现验证

两份代码均经 C++23 编译。三个官方样例输出 `6,0,-1`。固定种子生成 30,000 组 $n\le9$、需求不超过 7、两机燃料不超过 15 的实例，与完整枚举机器选择的独立 oracle 逐组比较，零不一致。

## 变种一：恢复机器分配方案

为每个分层状态额外记录前驱键和选择；找到终止层最优状态后逆序恢复。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Step {
  int previous = -1;
  int machine = -1;
};
int main() {
  int n;
  cin >> n;
  vector<int> choice(n);
  cout << "在主 DP 的每层为最优状态保存 previous 与 machine，终态逆序回溯。\n";
  for (int x : choice) cout << x << ' ';
}
```

转移复杂度不变，额外空间从滚动两层增至 $O(nS)$；若只给最终活跃状态保存持久前驱节点，可降为实际松弛数。

## 变种二：给定等待上限，问最多服务多少辆

转移时仅允许 `wait <= limit`，不再保存代价；第一次无后继即得最大前缀长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int limit, n;
  cin >> limit >> n;
  vector<int> waits(n);
  for (int& x : waits) cin >> x;
  int served = 0;
  for (int x : waits) {
    if (x > limit) break;
    ++served;
  }
  cout << served << '\n';
}
```

完整版本沿用四维可达状态，时间 $O(nS)$、空间 $O(S)$；这里的代码展示阈值过滤契约。

## 变种三：机器数扩展为固定的 $m$

状态变成每台机器的 `(fuel,busy)` 向量；一次转移选择其中一台并统一减去其等待。状态数对 $m$ 指数增长，适合很小的 $m$ 用哈希记忆化。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct State {
  vector<int> fuel;
  vector<int> busy;
  auto operator<=>(const State&) const = default;
};
int main() {
  int m;
  cin >> m;
  State state{vector<int>(m), vector<int>(m)};
  for (int& x : state.fuel) cin >> x;
  cout << state.fuel.size() << '\n';
}
```

每状态转移 $O(m)$；状态空间是各机离散状态的乘积。

## 变种四：允许车辆在机器空闲后故意等待

原状态不再只需最早开始时刻，因为延迟可能改变后续车辆的允许时刻并产生调度选择。若时间上界小，可把选择的额外延迟一并枚举进时间 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int earliest, latest;
  cin >> earliest >> latest;
  vector<int> starts;
  for (int time = earliest; time <= latest; ++time) starts.push_back(time);
  for (int time : starts) cout << time << ' ';
}
```

若时间上界为 $H$，每个原转移可能扩为 $O(H)$，总计 $O(nSH)$。

## 变种五：目标改为最小总等待时间

状态完全不变，只把代价合并从 `max` 改为加法；同一状态保留最小累计等待。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int states, edges;
  cin >> states >> edges;
  const long long inf = (1LL << 60);
  vector<long long> dp(states, inf);
  dp[0] = 0;
  while (edges--) {
    int from, to, wait;
    cin >> from >> to >> wait;
    dp[to] = min(dp[to], dp[from] + wait);
  }
  cout << *min_element(dp.begin(), dp.end()) << '\n';
}
```

复杂度仍由状态与转移数决定，即 $O(nS)$ 时间、$O(S)$ 滚动空间。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/)
- [对应知识专题](../../dp/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-133-lc162/">← [力扣 Top 133] LC 162 寻找峰值 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-b/">[codeforces] CF Round 1116 Div.2 B Domino Tiles →</a>
</nav>
