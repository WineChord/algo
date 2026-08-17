---
title: "[力扣竞赛] 第 515 场周赛 Q1 LC 4024 最近的可用无人机 简单"
---

# [力扣竞赛] 第 515 场周赛 Q1 LC 4024 最近的可用无人机 简单

<p class="daily-archive-kicker">2026-08-18 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-18 题目列表</a> · <a href="../../../basics/top-k-extrema/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=699283eaaad0ddd297648b15cdb185aed9781d4a0b752c0e198469e9e5a3ee11 -->
[力扣 4024：最近的可用无人机](https://leetcode.cn/problems/nearest-available-drone/)

## 官方原始信息

- 比赛：第 515 场周赛，第 1 题。
- 题号：4024。
- 官方中文标题：最近的可用无人机。
- 官方难度：简单；官方比赛分值：3 分。
- ZeroTracer 社区估算竞赛分：未知；截至 2026-08-18 的公开数据中没有可靠条目。
- 函数签名：`int nearestDrone(vector<vector<int>>& drones, vector<int>& target)`。
- 题意：`drones[i] = [x_i,y_i,range_i]` 描述第 `i` 架无人机的位置和最大航程。
  目标点为 `[t_x,t_y]`。若无人机到目标的曼哈顿距离不超过其航程，它就是可用的。
  返回可用无人机中距离最小的下标；距离相同则返回较小下标，没有可用无人机则返回 -1。

### 全部官方样例

样例 1：

```text
输入：drones = [[0,0,8],[2,2,9]], target = [3,4]
输出：1
解释：两架无人机的曼哈顿距离分别为 7 和 3，且都在航程内，因此选择下标 1。
```

样例 2：

```text
输入：drones = [[2,1,5],[4,4,5],[6,6,8]], target = [5,5]
输出：1
解释：距离分别为 7、2、2。下标 0 不可用；后两架同距，选择较小下标 1。
```

样例 3：

```text
输入：drones = [[4,4,5]], target = [8,6]
输出：-1
解释：唯一无人机的距离为 6，大于航程 5。
```

### 全部官方约束

- $1 \le |drones| \le 100$。
- `drones[i].length == 3`，`target.length == 2`。
- $-25 \le x_i,y_i,t_x,t_y \le 25$。
- $1 \le range_i \le 100$。

## 约束推导与选择模型

每架无人机只需独立计算一次

$$
d_i=|x_i-t_x|+|y_i-t_y|.
$$

可行条件是 $d_i\le range_i$，优化目标是让二元组 $(d_i,i)$ 按字典序最小。坐标差的
绝对值至多 50，距离至多 100，`int` 完全安全。数据量虽小到排序也足够，但只求一个最小
元素，没有必要存储和排列所有候选。

## 样例手推与边界

样例 2 中三个候选依次得到 $(7,0)$、$(2,1)$、$(2,2)$。第一个因 $7>5$ 被过滤；
第二个成为当前最优；第三个距离相等但下标更大，不能替换，最终返回 1。

- 距离恰好等于航程：条件是“不超过”，应视为可用。
- 多个候选同距：必须选择最小下标。
- 只有一架且不可用：返回 -1。
- 坐标可以为负数：应先做差再取绝对值。
- 目标与无人机重合：距离为 0，一定在正航程内，但仍要与其他零距离候选比较下标。

## 解法一：收集候选后排序

逐架过滤可用无人机，将 `(距离,下标)` 放入数组后排序。排序的字典序正好同时实现距离和
下标两层规则，因此覆盖所有候选并返回全局最优。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int nearestDrone(vector<vector<int>>& drones, vector<int>& target) {
    vector<pair<int, int>> candidates;
    for (int i = 0; i < static_cast<int>(drones.size()); ++i) {
      int distance = abs(drones[i][0] - target[0]) +
          abs(drones[i][1] - target[1]);
      if (distance <= drones[i][2]) candidates.push_back({distance, i});
    }
    if (candidates.empty()) return -1;
    sort(candidates.begin(), candidates.end());
    return candidates.front().second;
  }
};
```

时间复杂度 $O(n\log n)$，额外空间 $O(n)$。瓶颈在于排序解决了比“找最小值”更强的问题。

## 从排序到一次扫描

题目只要求排序后的第一个元素。扫描下标天然从小到大进行，因此遇到更短距离时替换答案，
遇到相同距离时保留旧答案，就自动保留最小下标。这样既不需要候选数组，也不需要显式写
第二层比较。

## 最佳实用解：可行性过滤加在线最小值

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int nearestDrone(vector<vector<int>>& drones, vector<int>& target) {
    int answer = -1;
    int bestDistance = numeric_limits<int>::max();
    for (int i = 0; i < static_cast<int>(drones.size()); ++i) {
      int distance = abs(drones[i][0] - target[0]) +
          abs(drones[i][1] - target[1]);
      if (distance <= drones[i][2] && distance < bestDistance) {
        bestDistance = distance;
        answer = i;
      }
    }
    return answer;
  }
};
```

时间复杂度为 $O(n)$，额外空间为 $O(1)$。这是面试与竞赛中最值得记忆的写法：先过滤
不可行项，再维护目标函数与稳定的下标决胜规则。

### 循环不变量与正确性证明

处理下标 $i$ 之前，`answer` 是区间 `[0,i-1]` 内所有可用无人机中二元组
`(distance,index)` 最小者；若不存在则为 -1。若第 $i$ 架不可用，它不属于候选集，不变量
不变。若它可用且距离更小，就应替换；若距离相等，因为 $i$ 大于所有已扫描下标，旧答案
更优；若距离更大，也不替换。故处理后不变量对 `[0,i]` 成立。扫描结束时覆盖全部下标，
返回值就是题目要求的答案。

## 同阶写法比较

也可以直接比较 `pair<int,int>`，在可用时用 `min(best, pair{distance,i})`。它同样是
$O(n)$ 时间、$O(1)$ 额外空间，对多层决胜规则更易扩展；当前写法利用扫描顺序省掉一次
显式下标比较，变量含义更直观。若决胜键超过两层，优先使用元组；本题优先记忆严格小于
才替换的扫描法。

## 易错点

- 把曼哈顿距离错写成欧几里得距离或平方距离。
- 使用 `< range`，漏掉距离恰好等于航程的无人机。
- 相同距离时用 `<=` 替换，错误地保留了较大下标。
- 先选全局最近再检查航程；不可用候选必须先过滤。
- 用无符号数保存坐标差，负差会下溢。

## 验证说明

排序版和一次扫描版均以 GNU++23 编译，通过全部官方样例、负坐标、恰好到达、全不可用、
多架同距等边界。另穷举小坐标、航程和目标，并以排序版为 oracle 对一次扫描版做逐项差分；
随后运行更大规模随机对拍，结果一致。

## 变种一：返回全部并列最近者

新定义：返回所有可用且距离达到最小值的下标，按升序排列。原扫描仍成立，但遇到更小距离
要清空旧集合，遇到相同距离要追加。时间 $O(n)$，答案之外额外空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, targetX, targetY;
  cin >> n >> targetX >> targetY;
  int bestDistance = numeric_limits<int>::max();
  vector<int> answer;
  for (int i = 0; i < n; ++i) {
    int x, y, range;
    cin >> x >> y >> range;
    int distance = abs(x - targetX) + abs(y - targetY);
    if (distance > range) continue;
    if (distance < bestDistance) {
      bestDistance = distance;
      answer.clear();
    }
    if (distance == bestDistance) answer.push_back(i);
  }
  if (answer.empty()) cout << -1;
  else for (int index : answer) cout << index << ' ';
  cout << '\n';
  return 0;
}
```

## 变种二：返回最近的前 k 架可用无人机

新定义：按 `(距离,下标)` 排序，返回前 $k$ 个。只维护大小不超过 $k$ 的大根堆，堆顶是
当前最差保留项；新候选更优时替换。时间 $O(n\log k)$，空间 $O(k)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k, targetX, targetY;
  cin >> n >> k >> targetX >> targetY;
  priority_queue<pair<int, int>> chosen;
  for (int i = 0; i < n; ++i) {
    int x, y, range;
    cin >> x >> y >> range;
    int distance = abs(x - targetX) + abs(y - targetY);
    if (distance > range) continue;
    chosen.push({distance, i});
    if (static_cast<int>(chosen.size()) > k) chosen.pop();
  }
  vector<pair<int, int>> answer;
  while (!chosen.empty()) {
    answer.push_back(chosen.top());
    chosen.pop();
  }
  sort(answer.begin(), answer.end());
  for (auto [distance, index] : answer) cout << index << ' ';
  cout << '\n';
  return 0;
}
```

## 变种三：改用欧几里得距离

新定义：航程和最近关系都按欧几里得距离判断。开平方会引入浮点误差，比较平方距离
$d_i^2=(x_i-t_x)^2+(y_i-t_y)^2$ 与 $range_i^2$ 即可。时间 $O(n)$，空间 $O(1)$；
坐标放大时应改用 `long long`。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long targetX, targetY;
  cin >> n >> targetX >> targetY;
  long long best = numeric_limits<long long>::max();
  int answer = -1;
  for (int i = 0; i < n; ++i) {
    long long x, y, range;
    cin >> x >> y >> range;
    long long dx = x - targetX;
    long long dy = y - targetY;
    long long squaredDistance = dx * dx + dy * dy;
    if (squaredDistance <= range * range && squaredDistance < best) {
      best = squaredDistance;
      answer = i;
    }
  }
  cout << answer << '\n';
  return 0;
}
```

## 变种四：网格中存在障碍

新定义：无人机只能在四联通网格的可通行格移动，航程按最短路步数计算。曼哈顿距离只再是
下界，原公式失效。从目标格做一次 BFS，得到每个可达格的真实距离，再扫描无人机。设网格
为 $h\times w$，复杂度 $O(hw+n)$，空间 $O(hw)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int h, w;
  cin >> h >> w;
  vector<string> grid(h);
  for (string& row : grid) cin >> row;
  int targetX, targetY, n;
  cin >> targetX >> targetY >> n;
  vector<array<int, 3>> drones(n);
  for (auto& drone : drones) cin >> drone[0] >> drone[1] >> drone[2];
  vector<vector<int>> distance(h, vector<int>(w, -1));
  queue<pair<int, int>> pending;
  if (grid[targetX][targetY] != '#') {
    distance[targetX][targetY] = 0;
    pending.push({targetX, targetY});
  }
  const int dx[4] = {1, -1, 0, 0};
  const int dy[4] = {0, 0, 1, -1};
  while (!pending.empty()) {
    auto [x, y] = pending.front();
    pending.pop();
    for (int direction = 0; direction < 4; ++direction) {
      int nextX = x + dx[direction];
      int nextY = y + dy[direction];
      if (nextX < 0 || nextX >= h || nextY < 0 || nextY >= w) continue;
      if (grid[nextX][nextY] == '#' || distance[nextX][nextY] != -1) continue;
      distance[nextX][nextY] = distance[x][y] + 1;
      pending.push({nextX, nextY});
    }
  }
  int answer = -1;
  int bestDistance = numeric_limits<int>::max();
  for (int i = 0; i < n; ++i) {
    auto [x, y, range] = drones[i];
    int current = distance[x][y];
    if (current != -1 && current <= range && current < bestDistance) {
      bestDistance = current;
      answer = i;
    }
  }
  cout << answer << '\n';
  return 0;
}
```

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/nearest-available-drone/)
- [第 515 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-515/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/nearest-available-drone/)
- [对应知识专题](../../basics/top-k-extrema.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-138-lc459/">← [力扣 Top 138] LC 459 重复的子字符串 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-a/">[codeforces] CF Round 1117 Div.2 A Creating Abbreviations →</a>
</nav>
