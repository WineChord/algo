---
title: "[力扣竞赛] 第 189 场双周赛 Q1 LC 4020 电梯请求 I 简单"
---

# [力扣竞赛] 第 189 场双周赛 Q1 LC 4020 电梯请求 I 简单

<p class="daily-archive-kicker">2026-08-22 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-22 题目列表</a> · <a href="../../../basics/sequence-invariants/#fixed-order-path-length">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=1361a5b981fca67b2e8afb3221f707c850e8e6830a03a23b8e66fc0e7e641227 -->
[力扣官方题目：4020. 电梯请求 I](https://leetcode.cn/problems/elevator-requests-i/)

## 官方原始信息

- 比赛：第 189 场双周赛；题目顺序：Q1；比赛开始时间：2026-08-15 22:30（北京时间）。
- 题号：LC 4020；官方中文标题：电梯请求 I；官方难度：简单。
- 官方竞赛分值：3 分。
- ZeroTracer 公开数据在 2026-08-22 未收录本题，社区估算竞赛分记为未知。
- 官方链接：[https://leetcode.cn/problems/elevator-requests-i/](https://leetcode.cn/problems/elevator-requests-i/)
- 函数签名：`int elevatorRequests(int n, vector<int>& requests)`。
- 官方标签：数组、模拟。

### 原始题意

一栋楼有 `n` 层，编号为 0 到 `n - 1`。一部电梯初始位于 0 层，必须按数组 `requests`
给出的顺序服务楼层请求。电梯每秒移动一层；若已经在目标楼层，则本次请求耗时为 0。求完成
全部请求的总时间。

### 全部官方样例

```text
示例 1
输入：n = 5, requests = [2,1,4,3]
输出：7
解释：0 -> 2、2 -> 1、1 -> 4、4 -> 3 分别耗时 2、1、3、1 秒。

示例 2
输入：n = 3, requests = [2,0,0]
输出：4
解释：0 -> 2、2 -> 0、0 -> 0 分别耗时 2、2、0 秒。
```

### 全部约束

- $1\le n\le100$。
- $1\le requests.length\le100$。
- $0\le requests[i]\le n-1$。

## 最优结论摘要

相邻楼层间的距离是绝对值。令 $r_0=0$，总时间就是

$$
\sum_{i=1}^{m}|r_i-r_{i-1}|.
$$

按请求顺序维护当前楼层并累加距离即可。时间复杂度 $O(m)$，额外空间 $O(1)$。这是必须读取
全部请求时的渐进最优解。

## 约束推导、溢出与边界

- 请求顺序固定，因此不存在调度或最短路选择；每一段的起点由上一请求唯一确定。
- 一次移动最多跨越 $n-1$ 层，总时间最多为 $100\times99=9900$，`int` 足够。
- 连续相同请求贡献 0，不能错误地为“开门”额外加时；题目只计算移动时间。
- `n=1` 时所有请求只能为 0，答案为 0。
- `n` 只限定合法楼层范围，本身不参与距离公式。

## 样例手推

样例 1 的状态演化为：

$$
0\xrightarrow{2}2\xrightarrow{1}1\xrightarrow{3}4\xrightarrow{1}3,
$$

因此总时间为 $2+1+3+1=7$。样例 2 的最后两个目标楼层相同，最后一段距离为 0。

## 解法一：逐秒模拟

对每个目标楼层，每秒把当前位置向目标移动一层并累加时间。它忠实模拟物理过程，时间复杂度
$O(T)$，其中 $T$ 是最终答案；空间复杂度 $O(1)$。在原约束下也能通过，但它重复执行了本可
一次算出的单位移动。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int elevatorRequests(int n, vector<int>& requests) {
    static_cast<void>(n);
    int floor = 0;
    int time = 0;
    for (int target : requests) {
      while (floor < target) {
        ++floor;
        ++time;
      }
      while (floor > target) {
        --floor;
        ++time;
      }
    }
    return time;
  }
};
```

## 从逐秒移动到整段距离

从楼层 `floor` 到 `target` 的唯一路径包含 `abs(target - floor)` 条相邻楼层边。把逐秒循环替换
为一次绝对值计算，既不改变经过的边，也不改变耗时。每处理完一个请求，再把当前位置更新为
目标楼层。

## 最佳实用解：单次扫描相邻距离

### 正确性证明

**引理**：服务第 $i$ 个请求所需时间恰为 $|r_i-r_{i-1}|$。

电梯每秒只能改变一层，因此至少需要这么多秒；连续朝目标方向移动恰好这么多次即可到达，
所以下界可达。

请求必须按给定顺序处理，第 $i$ 段结束时的位置必为 $r_i$。各段时间没有重叠，故累加所有
相邻距离正好得到完成全部请求的时间，算法正确。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int elevatorRequests(int n, vector<int>& requests) {
    static_cast<void>(n);
    int answer = 0;
    int floor = 0;
    for (int target : requests) {
      answer += abs(target - floor);
      floor = target;
    }
    return answer;
  }
};
```

时间复杂度 $O(m)$，额外空间 $O(1)$。

## 同阶方案比较与易错点

也可以在数组前补一个 0 后计算相邻差，但会修改输入或复制数组；维护一个 `floor` 变量更直接，
也更适合流式请求。竞赛中优先记忆“当前位置 + 相邻距离累加”。

- 忘记初始楼层是 0，会漏掉第一段距离。
- 把 `n` 当作起点或终点；它只是楼层数量。
- 对相同楼层额外加 1；官方规则明确此时无需移动。
- 排序请求会改变强制服务顺序，得到的是另一道调度题。

## 可复现验证

两份原题代码均以 C++23 编译，并通过两个官方样例、`n=1`、连续重复楼层、0 与最高层交替等
边界。随机生成 20,000 组小数据，以逐秒模拟为 oracle，与绝对值解逐项一致。

## Follow-up 与约束变种

### 变种一：任意起点并要求回到指定终点

新定义：电梯从 `start` 出发，仍按固定顺序服务请求，最后还要到 `finish`。原算法完全成立，
只需改变初始位置并补上末段距离。时间 $O(m)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long elevatorRequestsWithEndpoints(
      int start, int finish, const vector<int>& requests) {
    long long answer = 0;
    int floor = start;
    for (int target : requests) {
      answer += abs(target - floor);
      floor = target;
    }
    answer += abs(finish - floor);
    return answer;
  }
};
```

### 变种二：请求可以任意重排

新定义：一部电梯从 `start` 出发，只需至少访问所有请求楼层，结束位置不限。固定顺序公式失效。
去重后只需覆盖最小请求 `low` 到最大请求 `high` 的整段区间；先到较近端点，再走完整区间最优：

$$
(high-low)+\min(|start-low|,|start-high|).
$$

时间 $O(m)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long reorderRequests(int start, const vector<int>& requests) {
    if (requests.empty()) return 0;
    auto [minimum, maximum] = minmax_element(requests.begin(), requests.end());
    long long span = *maximum - *minimum;
    return span + min(abs(start - *minimum), abs(start - *maximum));
  }
};
```

### 变种三：上行和下行速度不同

新定义：上行一层耗时 `upTime`，下行一层耗时 `downTime`。绝对值的对称性失效，但每段方向
仍唯一；按方向乘对应单价即可。时间 $O(m)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long asymmetricElevator(
      int start, const vector<int>& requests, int upTime, int downTime) {
    long long answer = 0;
    int floor = start;
    for (int target : requests) {
      if (target >= floor) {
        answer += 1LL * (target - floor) * upTime;
      } else {
        answer += 1LL * (floor - target) * downTime;
      }
      floor = target;
    }
    return answer;
  }
};
```

### 变种四：两部电梯共同服务固定顺序请求

新定义：两部电梯都从 0 层出发；请求仍按给定顺序出现，但每个请求可交给任意一部，求最小
总移动时间。单一当前位置不再足够，状态改为两部电梯所在楼层。每个请求尝试由 A 或 B 服务，
对相同位置对只保留最小代价。楼层数为 `n` 时，时间 $O(mn^2)$，空间 $O(n^2)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int twoElevators(int n, const vector<int>& requests) {
    const int infinity = numeric_limits<int>::max() / 4;
    vector<vector<int>> dp(n, vector<int>(n, infinity));
    dp[0][0] = 0;
    for (int target : requests) {
      vector<vector<int>> next(n, vector<int>(n, infinity));
      for (int first = 0; first < n; ++first) {
        for (int second = 0; second < n; ++second) {
          if (dp[first][second] == infinity) continue;
          next[target][second] = min(
              next[target][second], dp[first][second] + abs(target - first));
          next[first][target] = min(
              next[first][target], dp[first][second] + abs(target - second));
        }
      }
      dp.swap(next);
    }
    int answer = infinity;
    for (const auto& row : dp) {
      answer = min(answer, *min_element(row.begin(), row.end()));
    }
    return answer;
  }
};
```

## 推荐记忆

固定顺序、线性楼层、单位速度时，不需要搜索：把每个请求当作路径上的下一个端点，直接累加
相邻绝对值。只有请求顺序、终点、速度或电梯数量改变时，模型才会升级。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/elevator-requests-i/)
- [对应知识专题](../../basics/sequence-invariants.md#fixed-order-path-length)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-e/">[codeforces] CF Round 1117 Div.2 E Busy Beaver →</a>
</nav>
