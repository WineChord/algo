---
title: "[codeforces] CF Round 1117 Div.2 E Busy Beaver"
---

# [codeforces] CF Round 1117 Div.2 E Busy Beaver

<p class="daily-archive-kicker">2026-08-22 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-22 题目列表</a> · <a href="../../../basics/greedy-exchange/#nonnegative-segment-closure">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=2b2e34a794311ef38277bac1241c701023ad257da70f9a8dbc04276d401c8a50 -->
[Official problem: Codeforces 2257E — Busy Beaver](https://codeforces.com/contest/2257/problem/E)

## 官方来源与元数据

- 比赛：Codeforces Round 1117 (Div. 2)；Contest ID 2257。
- 题目：Div.2 E — Busy Beaver；没有已确认的跨 division 别名。
- 官方 points：2250；官方 API 未提供本题 rating，故记为未知。
- 官方 tags：brute force、data structures、divide and conquer、dp、greedy、implementation、sortings。
- 时间限制：2 秒；内存限制：512 MB；非交互题。
- 官方题面直达链接见首行；文字依据
  [Codeforces Problems’ Materials Publishing License v0.1](https://codeforces.com/blog/entry/967)
  标注来源。未使用隐藏测试、生成器、checker 或 validator。
- 题面没有理解所必需的图片。

## Complete English statement — model-authored presentation based on the official task

The following self-contained English presentation was independently organized from the official
statement. It preserves the full task contract, but it is not presented as a verbatim official
transcript.

The Beaver has founded a construction company named “Busy Beaver” and wants to improve its
reputation by constructing the tallest possible building.

The company starts with $x$ carrots and has $n$ independent building projects. Project $i$ contains
$m_i$ floor contracts and initially has height zero. Its floors must be built in order. To construct
floor $j$ of project $i$, the company must currently have at least $a_{i,j}$ carrots. It pays those
carrots and immediately receives $b_{i,j}$ carrots, so its capital changes by
$b_{i,j}-a_{i,j}$. A contract may be unprofitable.

You may choose which project supplies the next floor. Different projects may be interleaved
arbitrarily, but within one project floor $j$ cannot be built before all lower floors. A project need
not be started or completed. Maximize the height of one constructed building. If several project
indices can achieve the maximum height, output the smallest such index.

### Input

The first line contains the number of test cases $t$. For each test case:

1. One line contains $n$ and the initial capital $x$.
2. For each project $i=1,2,\ldots,n$:
   - one line contains $m_i$;
   - one line contains $a_{i,1},a_{i,2},\ldots,a_{i,m_i}$;
   - one line contains $b_{i,1},b_{i,2},\ldots,b_{i,m_i}$.

```text
t
n x
m_1
a_1,1 ... a_1,m_1
b_1,1 ... b_1,m_1
...
```

### Output

For every test case, print two integers: the maximum achievable building height and the smallest
project index that can attain that height.

### Constraints

- $1\le t\le3\times10^4$.
- $1\le n\le2\times10^5$.
- $0\le x\le10^{18}$.
- $1\le m_i\le2\times10^5$.
- $0\le a_{i,j},b_{i,j}\le10^9$.
- The sum of all $m_i$ over all test cases does not exceed $2\times10^5$.
- All input values are integers.

### Official sample input

```text
2
1 6
4
4 4 2 1
2 4 1 1
2 3
2
4 4
5 5
2
2 20
4 0
```

### Official sample output

```text
4 1
2 1
```

In the first test case, all four floors of the only project can be built in order. In the second,
building project 2's first floor increases the capital by 2; then both floors of project 1 become
affordable.

Source: [Codeforces problem 2257E](https://codeforces.com/contest/2257/problem/E), published under the
[Codeforces materials license](https://codeforces.com/blog/entry/967).

## 中文解释与结论摘要

先把每个项目切成最短的连续段，使每段总收益
$\sum(b-a)\ge0$。一段执行完后资本不减；它的“准入资金”是按顺序完成段内每一层所需的最小
起始资本。每个项目当前只暴露下一段，把这些段按准入资金放进小根堆。只要堆顶可负担，就完整
执行并暴露同项目下一段；堆顶都不可负担时，任何未执行非负段都不可完成，当前资本已经最大。

然后对每个项目独立试算：从全局阶段已建高度继续，只在该项目上逐层花费，能走多远。取最高
高度，平局取最小编号。总时间 $O(\sum m_i\log n)$，空间 $O(\sum m_i+n)$。

## 约束推导、溢出与边界

- 总楼层数 $M\le2\times10^5$，可线性预处理，但不能搜索全部项目交错顺序。
- 单层可能亏损，不能执行“当前能买就买”的逐层贪心；应先判断它能否通向一个资本不减的段。
- 项目内顺序固定，跨项目可交错，这是把每个项目前缀视作链式依赖的关键。
- 初始资本可以是 0，成本也可以是 0；零成本楼层必须正常处理。
- 资本最多为 $10^{18}$ 加全部奖励，仍在有符号 64 位范围内；段内余额和准入资金也用
  `long long`。
- 每个项目至少一层，所以即使一层都造不起，答案高度仍为 0，编号为 1。

## 官方样例手推

第二组中，项目 1 的两层变化量是 $+1,+1$，第一段准入资金为 4；项目 2 的变化量是
$+2,-20$，其第一段仅含第一层，准入资金为 2、净收益为 2。初始资本 3 先完成项目 2 第一段，
资本变为 5；此时项目 1 两个单层非负段都可完成，高度达到 2。项目 2 的剩余楼层成本 20，
无法继续，因此最优答案是 `2 1`。

## 解法一：小规模全状态搜索

状态是所有项目当前高度向量；同一高度向量只保留最大资本，因为资本更多支配资本更少的状态。
枚举下一层可负担的项目并扩展。状态上界为 $\prod_i(m_i+1)$，只适合总楼层很小，但可作为
随机对拍 oracle。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    long long initial;
    cin >> n >> initial;
    vector<vector<long long>> cost(n), reward(n);
    for (int i = 0; i < n; ++i) {
      int m;
      cin >> m;
      cost[i].resize(m);
      reward[i].resize(m);
      for (long long& value : cost[i]) cin >> value;
      for (long long& value : reward[i]) cin >> value;
    }
    vector<int> start(n);
    map<vector<int>, long long> best;
    queue<vector<int>> pending;
    best[start] = initial;
    pending.push(start);
    int bestHeight = -1;
    int bestProject = n;
    while (!pending.empty()) {
      vector<int> height = pending.front();
      pending.pop();
      long long capital = best[height];
      for (int i = 0; i < n; ++i) {
        if (height[i] > bestHeight ||
            (height[i] == bestHeight && i < bestProject)) {
          bestHeight = height[i];
          bestProject = i;
        }
        if (height[i] == static_cast<int>(cost[i].size())) continue;
        int floor = height[i];
        if (capital < cost[i][floor]) continue;
        vector<int> next = height;
        ++next[i];
        long long nextCapital = capital - cost[i][floor] + reward[i][floor];
        auto found = best.find(next);
        if (found == best.end() || nextCapital > found->second) {
          best[next] = nextCapital;
          pending.push(next);
        }
      }
    }
    cout << bestHeight << ' ' << bestProject + 1 << '\n';
  }
  return 0;
}
```

## 把楼层链切成最短非负收益段

从某个未分段位置开始累加 `balance += b - a`，第一次达到非负就结束当前段。段的准入资金为

$$
need=\max_j\left(a_j-\sum_{k<j}(b_k-a_k)\right),
$$

即确保每个楼层付款前余额都足够的最小起始资本。该段净收益非负。最后若剩下一段所有前缀
收益都为负，就不把它纳入全局“赚钱阶段”，因为完成它必然使资本下降。

这种最短切分不会损失机会：若较长非负段可完成，那么它的第一个最短非负前缀也可完成；先
完成前缀只会使资本不减，再处理后续不差。

## 解法二：扫描所有项目寻找可执行段

每次扫描所有项目，找到任一准入资金不超过当前资本的下一段并执行。每段使资本不减，因此顺序
不影响最终能解锁的闭包。若一次完整扫描找不到可执行段，资本已无法再增长。最后逐项目试算尾部。
该做法正确但每执行一段都可能扫描 $n$ 个项目，最坏 $O(Mn)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long need;
  long long gain;
  int end;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    long long capital;
    cin >> n >> capital;
    vector<vector<long long>> cost(n), reward(n);
    vector<vector<Segment>> segments(n);
    for (int i = 0; i < n; ++i) {
      int m;
      cin >> m;
      cost[i].resize(m);
      reward[i].resize(m);
      for (long long& value : cost[i]) cin >> value;
      for (long long& value : reward[i]) cin >> value;
      long long balance = 0;
      long long need = 0;
      for (int floor = 0; floor < m; ++floor) {
        need = max(need, cost[i][floor] - balance);
        balance += reward[i][floor] - cost[i][floor];
        if (balance >= 0) {
          segments[i].push_back({need, balance, floor + 1});
          balance = 0;
          need = 0;
        }
      }
    }
    vector<int> nextSegment(n);
    vector<int> built(n);
    while (true) {
      int chosen = -1;
      for (int i = 0; i < n; ++i) {
        if (nextSegment[i] == static_cast<int>(segments[i].size())) continue;
        if (segments[i][nextSegment[i]].need <= capital) {
          chosen = i;
          break;
        }
      }
      if (chosen == -1) break;
      const Segment& segment = segments[chosen][nextSegment[chosen]++];
      capital += segment.gain;
      built[chosen] = segment.end;
    }
    int bestHeight = -1;
    int bestProject = -1;
    for (int i = 0; i < n; ++i) {
      long long current = capital;
      int height = built[i];
      while (height < static_cast<int>(cost[i].size()) && current >= cost[i][height]) {
        current += reward[i][height] - cost[i][height];
        ++height;
      }
      if (height > bestHeight) {
        bestHeight = height;
        bestProject = i;
      }
    }
    cout << bestHeight << ' ' << bestProject + 1 << '\n';
  }
  return 0;
}
```

## 从全项目扫描到准入资金小根堆

每个项目在任意时刻只暴露一个“下一段”。把它们按 `need` 放入小根堆：若堆顶都大于资本，
其余段更不可能执行；若堆顶可执行，完成它并把同项目下一段入堆。这样每段只进出堆一次。

## 最佳实用解：非负段闭包 + 单项目尾部

### 正确性证明

**引理 1**：最短非负段的 `need` 恰是完成该段所需的最小起始资本。

每层付款前的资本是起始资本加此前累计变化量，逐层满足付款条件给出公式中的所有下界；取最大
既必要又足够。

**引理 2**：执行任何当前可负担的非负段不会损害最优解。

该段遵守项目依赖，执行中由 `need` 保证合法，结束后资本不减，并且只会暴露更多后继段。把它
提前到任何可行计划之前，不会使计划中其他付款变得不可行。

**引理 3**：堆循环结束时资本已达到所有计划可获得的最大值。

若堆顶 `need > capital`，所有项目的下一非负段都不可完整执行。对任何未切出的尾部，它的每个
前缀净收益均为负；先执行其一部分只会降低资本，也不能解锁别的段。因此不存在能进一步增加
资本的合法动作。

最大资本确定后，若目标是让某一个项目尽量高，所有其余未完成负尾部都只会耗资；只需对每个
候选项目独立连续构造直到首个付不起的楼层。枚举所有项目并按编号处理平局，得到全局最优答案。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long need;
  long long gain;
  int end;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    long long capital;
    cin >> n >> capital;
    vector<vector<long long>> cost(n), reward(n);
    vector<vector<Segment>> segments(n);
    for (int i = 0; i < n; ++i) {
      int m;
      cin >> m;
      cost[i].resize(m);
      reward[i].resize(m);
      for (long long& value : cost[i]) cin >> value;
      for (long long& value : reward[i]) cin >> value;
      long long balance = 0;
      long long need = 0;
      for (int floor = 0; floor < m; ++floor) {
        need = max(need, cost[i][floor] - balance);
        balance += reward[i][floor] - cost[i][floor];
        if (balance >= 0) {
          segments[i].push_back({need, balance, floor + 1});
          balance = 0;
          need = 0;
        }
      }
    }
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> available;
    vector<int> nextSegment(n);
    vector<int> built(n);
    for (int i = 0; i < n; ++i) {
      if (!segments[i].empty()) available.push({segments[i][0].need, i});
    }
    while (!available.empty() && available.top().first <= capital) {
      auto [need, project] = available.top();
      available.pop();
      static_cast<void>(need);
      const Segment& segment = segments[project][nextSegment[project]];
      capital += segment.gain;
      built[project] = segment.end;
      ++nextSegment[project];
      if (nextSegment[project] < static_cast<int>(segments[project].size())) {
        available.push({segments[project][nextSegment[project]].need, project});
      }
    }
    int bestHeight = -1;
    int bestProject = -1;
    for (int i = 0; i < n; ++i) {
      long long current = capital;
      int height = built[i];
      while (height < static_cast<int>(cost[i].size()) && current >= cost[i][height]) {
        current += reward[i][height] - cost[i][height];
        ++height;
      }
      if (height > bestHeight) {
        bestHeight = height;
        bestProject = i;
      }
    }
    cout << bestHeight << ' ' << bestProject + 1 << '\n';
  }
  return 0;
}
```

总时间复杂度 $O(M\log n)$，空间复杂度 $O(M+n)$。

## 同阶方案比较与易错点

有序集合与小根堆都能维护最小准入资金；这里只需删除最小项并插入同项目后继，不需要删除任意
元素，小根堆常数更小。推荐记忆“最短非负段 + 准入阈值 + 堆闭包”。

- 把“总收益非负”误当成“从资本 0 可执行”；段内可能先亏后赚，必须计算 `need`。
- 把最后总收益为负的尾段放进赚钱堆，会破坏资本单调性。
- 只按项目整体总收益切一段，会隐藏更早可执行的非负前缀。
- 全局阶段结束后把所有负尾部都执行；目标只关心一栋楼，其余尾部只会浪费资本。
- 平局必须取最小项目编号；按 0 基下标扫描并只在严格更高时更新即可。

## 可复现验证

最佳代码以 GNU++23 编译并通过官方样例。另生成 2,000 组 `n <= 4`、每项目不超过 4 层、
成本与奖励在 `[0,6]` 的固定种子随机数据；以完整高度向量搜索为 oracle，最大高度和最小编号
全部一致。

## Follow-up 与约束变种

### 变种一：同时输出一条最优施工计划

新定义：除最高高度和编号外，还要输出可复现的楼层施工顺序。全局阶段记录每次完成的非负段，
选定最终项目后再追加其尾部。每条记录为 `(project, floor)`；复杂度仍为 $O(M\log n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long need;
  long long gain;
  int start;
  int end;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long capital;
  cin >> n >> capital;
  vector<vector<long long>> cost(n), reward(n);
  vector<vector<Segment>> segments(n);
  for (int i = 0; i < n; ++i) {
    int m;
    cin >> m;
    cost[i].resize(m);
    reward[i].resize(m);
    for (long long& value : cost[i]) cin >> value;
    for (long long& value : reward[i]) cin >> value;
    long long balance = 0;
    long long need = 0;
    int start = 0;
    for (int floor = 0; floor < m; ++floor) {
      need = max(need, cost[i][floor] - balance);
      balance += reward[i][floor] - cost[i][floor];
      if (balance >= 0) {
        segments[i].push_back({need, balance, start, floor + 1});
        balance = 0;
        need = 0;
        start = floor + 1;
      }
    }
  }
  using Entry = pair<long long, int>;
  priority_queue<Entry, vector<Entry>, greater<Entry>> available;
  vector<int> nextSegment(n), built(n);
  vector<pair<int, int>> plan;
  for (int i = 0; i < n; ++i) {
    if (!segments[i].empty()) available.push({segments[i][0].need, i});
  }
  while (!available.empty() && available.top().first <= capital) {
    int project = available.top().second;
    available.pop();
    const Segment& segment = segments[project][nextSegment[project]];
    for (int floor = segment.start; floor < segment.end; ++floor) {
      plan.push_back({project + 1, floor + 1});
    }
    capital += segment.gain;
    built[project] = segment.end;
    ++nextSegment[project];
    if (nextSegment[project] < static_cast<int>(segments[project].size())) {
      available.push({segments[project][nextSegment[project]].need, project});
    }
  }
  int bestHeight = -1;
  int bestProject = -1;
  for (int i = 0; i < n; ++i) {
    long long current = capital;
    int height = built[i];
    while (height < static_cast<int>(cost[i].size()) && current >= cost[i][height]) {
      current += reward[i][height] - cost[i][height];
      ++height;
    }
    if (height > bestHeight) {
      bestHeight = height;
      bestProject = i;
    }
  }
  for (int floor = built[bestProject]; floor < bestHeight; ++floor) {
    plan.push_back({bestProject + 1, floor + 1});
  }
  cout << bestHeight << ' ' << bestProject + 1 << '\n';
  cout << plan.size() << '\n';
  for (auto [project, floor] : plan) cout << project << ' ' << floor << '\n';
  return 0;
}
```

### 变种二：达到高度 H 所需的最小初始资本

新定义：给定 `targetHeight`，求至少让某栋楼达到该高度的最小初始资本。对固定资本，原算法给出
的最大高度单调不减，因此可二分资本；每次判定运行一次段闭包。设二分上界为所有成本之和，
复杂度 $O(M\log n\log C)$，空间 $O(M+n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long need;
  long long gain;
  int end;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, targetHeight;
  cin >> n >> targetHeight;
  vector<vector<long long>> cost(n), reward(n);
  vector<vector<Segment>> segments(n);
  long long high = 0;
  for (int i = 0; i < n; ++i) {
    int m;
    cin >> m;
    cost[i].resize(m);
    reward[i].resize(m);
    for (long long& value : cost[i]) {
      cin >> value;
      high += value;
    }
    for (long long& value : reward[i]) cin >> value;
    long long balance = 0;
    long long need = 0;
    for (int floor = 0; floor < m; ++floor) {
      need = max(need, cost[i][floor] - balance);
      balance += reward[i][floor] - cost[i][floor];
      if (balance >= 0) {
        segments[i].push_back({need, balance, floor + 1});
        balance = 0;
        need = 0;
      }
    }
  }
  auto feasible = [&](long long capital) {
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> available;
    vector<int> nextSegment(n), built(n);
    for (int i = 0; i < n; ++i) {
      if (!segments[i].empty()) available.push({segments[i][0].need, i});
    }
    while (!available.empty() && available.top().first <= capital) {
      int project = available.top().second;
      available.pop();
      const Segment& segment = segments[project][nextSegment[project]++];
      capital += segment.gain;
      built[project] = segment.end;
      if (nextSegment[project] < static_cast<int>(segments[project].size())) {
        available.push({segments[project][nextSegment[project]].need, project});
      }
    }
    for (int i = 0; i < n; ++i) {
      long long current = capital;
      int height = built[i];
      while (height < static_cast<int>(cost[i].size()) && current >= cost[i][height]) {
        current += reward[i][height] - cost[i][height];
        ++height;
      }
      if (height >= targetHeight) return true;
    }
    return false;
  };
  if (!feasible(high)) {
    cout << -1 << '\n';
    return 0;
  }
  long long low = 0;
  while (low < high) {
    long long middle = low + (high - low) / 2;
    if (feasible(middle)) {
      high = middle;
    } else {
      low = middle + 1;
    }
  }
  cout << low << '\n';
  return 0;
}
```

### 变种三：多次询问不同初始资本

新定义：项目固定，给出至多 30 个不同的初始资本，分别输出最高高度与最小编号。预处理分段只做
一次；每个询问独立运行堆闭包和尾部试算。时间 $O(QM\log n)$，空间 $O(M+n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long need;
  long long gain;
  int end;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  cin >> n >> queries;
  vector<vector<long long>> cost(n), reward(n);
  vector<vector<Segment>> segments(n);
  for (int i = 0; i < n; ++i) {
    int m;
    cin >> m;
    cost[i].resize(m);
    reward[i].resize(m);
    for (long long& value : cost[i]) cin >> value;
    for (long long& value : reward[i]) cin >> value;
    long long balance = 0;
    long long need = 0;
    for (int floor = 0; floor < m; ++floor) {
      need = max(need, cost[i][floor] - balance);
      balance += reward[i][floor] - cost[i][floor];
      if (balance >= 0) {
        segments[i].push_back({need, balance, floor + 1});
        balance = 0;
        need = 0;
      }
    }
  }
  while (queries--) {
    long long capital;
    cin >> capital;
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> available;
    vector<int> nextSegment(n), built(n);
    for (int i = 0; i < n; ++i) {
      if (!segments[i].empty()) available.push({segments[i][0].need, i});
    }
    while (!available.empty() && available.top().first <= capital) {
      int project = available.top().second;
      available.pop();
      const Segment& segment = segments[project][nextSegment[project]++];
      capital += segment.gain;
      built[project] = segment.end;
      if (nextSegment[project] < static_cast<int>(segments[project].size())) {
        available.push({segments[project][nextSegment[project]].need, project});
      }
    }
    int bestHeight = -1;
    int bestProject = -1;
    for (int i = 0; i < n; ++i) {
      long long current = capital;
      int height = built[i];
      while (height < static_cast<int>(cost[i].size()) && current >= cost[i][height]) {
        current += reward[i][height] - cost[i][height];
        ++height;
      }
      if (height > bestHeight) {
        bestHeight = height;
        bestProject = i;
      }
    }
    cout << bestHeight << ' ' << bestProject + 1 << '\n';
  }
  return 0;
}
```

### 变种四：禁止项目之间交错

新定义：一旦开始某项目，就只能继续该项目，不能靠其他项目先赚资本再回来。全局非负段闭包
不再合法；每个项目从同一初始资本独立逐层模拟，取最高高度和最小编号即可。时间 $O(M)$，
空间 $O(M)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long initial;
  cin >> n >> initial;
  int bestHeight = -1;
  int bestProject = -1;
  for (int i = 0; i < n; ++i) {
    int m;
    cin >> m;
    vector<long long> cost(m), reward(m);
    for (long long& value : cost) cin >> value;
    for (long long& value : reward) cin >> value;
    long long capital = initial;
    int height = 0;
    while (height < m && capital >= cost[height]) {
      capital += reward[height] - cost[height];
      ++height;
    }
    if (height > bestHeight) {
      bestHeight = height;
      bestProject = i;
    }
  }
  cout << bestHeight << ' ' << bestProject + 1 << '\n';
  return 0;
}
```

## 推荐记忆

链式项目中，一段若最终不亏，就可以安全地纳入“资本增长闭包”；真正困难的是它在段内可能先亏，
所以必须同时维护准入资金。最短非负段保证依赖暴露最早，小根堆则把所有项目的下一段统一按阈值
推进。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2257/problem/E)
- [对应知识专题](../../basics/greedy-exchange.md#nonnegative-segment-closure)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-189-q1-lc4020/">← [力扣竞赛] 第 189 场双周赛 Q1 LC 4020 电梯请求 I 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-22-lc3622/">[力扣每日一题] 2026-08-22｜LC 3622 判断整除性 →</a>
</nav>
