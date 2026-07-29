---
title: "[力扣 Top 49] LC 45 跳跃游戏 II 中等"
---

# [力扣 Top 49] LC 45 跳跃游戏 II 中等

<p class="daily-archive-kicker">2026-07-30 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=7c466b98ecae7464fa94fa876dd0d5f161707813086b229a044dd4683d37a6aa -->
## 官方原始信息

- Top 排名：49
- 题号：LC 45
- 官方中文标题：跳跃游戏 II
- 官方难度：中等
- 官方链接：[跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/)

### 原始题意

给定从 0 开始编号的数组 `nums`，站在下标 `i` 时可向右跳至任意 `i+j`，其中 $0\le j\le nums_i$ 且不越界。初始位于 0，求到达最后一个下标的最少跳跃次数。官方保证终点可达。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int jump(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [2,3,1,1,4]
输出：2
解释：0 -> 1 -> 4。
```

```text
输入：nums = [2,3,0,1,4]
输出：2
```

### 全部约束

- $1\le n\le10^4$。
- $0\le nums_i\le1000$。
- 官方保证下标 $n-1$ 可达。
- 当 $n=1$ 时已经位于终点，答案为 0。

## 约束推导与分层视角

把每个下标看作图节点，从 `i` 向区间 `[i+1,i+nums[i]]` 连边，问题是无权图最短路。显式建边最坏 $O(n^2)$。由于所有出边都是向右的连续区间，可以按 BFS 层维护：

- `currentEnd`：当前跳数能覆盖的最右端；
- `farthest`：扫描当前层所有节点后，下一层能覆盖的最右端。

扫描到当前层边界时，跳数增加并把边界推进到 `farthest`。

## 解法递进

### 解法一：前缀动态规划

`dp[i]` 为到达 `i` 的最少跳数，枚举所有更早且能跳到 `i` 的位置。时间 $O(n^2)$、空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int jump(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, n + 1);
    dp[0] = 0;
    for (int i = 1; i < n; ++i) {
      for (int j = 0; j < i; ++j) {
        if (j + nums[j] >= i) {
          dp[i] = min(dp[i], dp[j] + 1);
        }
      }
    }
    return dp[n - 1];
  }
};
```

### 解法二：显式 BFS 扩展区间

逐层扫描新覆盖的下标；若不做“每个下标只入队一次”的区间去重，仍可能重复访问大量边。利用最右已入队位置可做到线性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int jump(vector<int>& nums) {
    int n = nums.size();
    if (n == 1) {
      return 0;
    }
    queue<int> queue;
    queue.push(0);
    int visited_right = 0;
    int steps = 0;
    while (!queue.empty()) {
      int layer = queue.size();
      ++steps;
      while (layer--) {
        int index = queue.front();
        queue.pop();
        int reach = min(n - 1, index + nums[index]);
        for (int next = max(visited_right + 1, index + 1); next <= reach; ++next) {
          if (next == n - 1) {
            return steps;
          }
          queue.push(next);
        }
        visited_right = max(visited_right, reach);
      }
    }
    return -1;
  }
};
```

### 最佳实用解：贪心压缩 BFS 层

无需保存层内所有节点，只要扫描其连续区间并维护下一层最远边界。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int jump(vector<int>& nums) {
    int steps = 0;
    int current_end = 0;
    int farthest = 0;
    for (int i = 0; i + 1 < static_cast<int>(nums.size()); ++i) {
      farthest = max(farthest, i + nums[i]);
      if (i == current_end) {
        ++steps;
        current_end = farthest;
      }
    }
    return steps;
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(1)$。

## 正确性证明

不变量：开始扫描一层时，所有不大于 `currentEnd` 的尚未扫描位置恰好能用 `steps` 次跳跃到达；扫描这些位置期间，`farthest` 是再跳一次能到达的最右位置。

从当前层任一位置出发的所有目标形成向右区间，其并集就是不超过 `farthest` 的下一段连续位置。因此扫描到 `currentEnd` 时，必须再跳一次才能进入后续位置，把边界更新为 `farthest` 与 BFS 进入下一层完全等价。第一次覆盖终点所用的层数就是无权图最短距离，故贪心跳数最少。

## 样例手推

对 `[2,3,1,1,4]`：

```text
初始层只含下标 0，扫描后 farthest=2，跳数变为 1，currentEnd=2。
扫描下标 1、2，最远可达 4。
到达旧边界 2 时，跳数变为 2，currentEnd=4。
```

终点已覆盖，答案为 2。

## 易错点与方案比较

- 循环只扫描到 `n-2`；扫描终点并再次加跳数会多算一次。
- `currentEnd` 是当前层边界，`farthest` 是下一层边界，不能混为一个变量。
- 当前题保证可达，所以边界一定前进；若不保证，必须检测 `farthest==currentEnd`。
- 不需要在每一步选择一个具体落点；贪心选择的是整层的最远覆盖范围。
- 推荐记忆“区间图 BFS 的常数空间压缩”，比“每步跳最远”这一不严谨口号更可靠。

## 变种一：终点可能不可达

新定义：不可达时返回 -1。到达层边界时若 `farthest` 没有前进，说明下一层为空。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int steps = 0;
  int current_end = 0;
  int farthest = 0;
  for (int i = 0; i + 1 < n; ++i) {
    if (i > farthest) {
      cout << -1 << '\n';
      return 0;
    }
    farthest = max(farthest, i + a[i]);
    if (i == current_end) {
      if (farthest == current_end) {
        cout << -1 << '\n';
        return 0;
      }
      ++steps;
      current_end = farthest;
      if (current_end >= n - 1) {
        break;
      }
    }
  }
  cout << (n == 1 ? 0 : steps) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：恢复一条最少跳跃路径

新定义：输出实际下标路径。显式 BFS 在某个下标首次入队时保存父节点；连续区间去重仍保证总扫描线性。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n), parent(n, -1);
  for (int& value : a) {
    cin >> value;
  }
  queue<int> queue;
  queue.push(0);
  int visited_right = 0;
  while (!queue.empty() && parent[n - 1] == -1) {
    int index = queue.front();
    queue.pop();
    int reach = min(n - 1, index + a[index]);
    for (int next = max(visited_right + 1, index + 1); next <= reach; ++next) {
      parent[next] = index;
      queue.push(next);
    }
    visited_right = max(visited_right, reach);
  }
  if (n > 1 && parent[n - 1] == -1) {
    cout << "NONE\n";
    return 0;
  }
  vector<int> path;
  for (int node = n - 1; node != -1; node = parent[node]) {
    path.push_back(node);
  }
  reverse(path.begin(), path.end());
  cout << path.size() - 1 << '\n';
  for (int node : path) {
    cout << node << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种三：统计最少跳跃路径条数

新定义：统计从 0 到终点的最少跳数路径数量并取模。区间中的每条边都可能贡献计数，使用按距离层的差分数组，把当前层每个节点对下一连续区间的方案数做区间加。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 1'000'000'007;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  vector<int> ways(n);
  ways[0] = 1;
  int left = 0;
  int right = 0;
  int distance = 0;
  while (right < n - 1) {
    vector<long long> difference(n + 1);
    int next_right = right;
    for (int i = left; i <= right; ++i) {
      int begin = right + 1;
      int end = min(n - 1, i + a[i]);
      if (begin <= end) {
        difference[begin] += ways[i];
        difference[end + 1] -= ways[i];
        next_right = max(next_right, end);
      }
    }
    if (next_right == right) {
      cout << "-1 0\n";
      return 0;
    }
    long long running = 0;
    for (int i = right + 1; i <= next_right; ++i) {
      running = (running + difference[i]) % MOD;
      ways[i] = (running + MOD) % MOD;
    }
    left = right + 1;
    right = next_right;
    ++distance;
  }
  cout << distance << ' ' << ways[n - 1] << '\n';
}
```

最坏时间 $O(n^2)$，因为每层重新分配并扫描长度为 $n$ 的差分数组；将差分结构复用并只清理触及区间可降到按层区间总量，或用树状数组实现。这里强调计数会让仅保留最远边界的信息不足。

## 变种四：存在禁止落脚的位置

新定义：部分下标不能落脚，但可以从其上方跨过；求到终点的最少跳数。可达位置不再形成完整连续层，单一最远边界不足。BFS 配合有序集合保存尚未访问且允许落脚的下标，每个出边区间只取出其中的未访问位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, blocked_count;
  cin >> n >> blocked_count;
  vector<int> a(n), blocked(n);
  for (int& value : a) {
    cin >> value;
  }
  for (int i = 0; i < blocked_count; ++i) {
    int index;
    cin >> index;
    blocked[index] = true;
  }
  if (blocked[0] || blocked[n - 1]) {
    cout << -1 << '\n';
    return 0;
  }
  set<int> unvisited;
  for (int i = 1; i < n; ++i) {
    if (!blocked[i]) {
      unvisited.insert(i);
    }
  }
  vector<int> distance(n, -1);
  queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    int index = queue.front();
    queue.pop();
    int right = min(n - 1, index + a[index]);
    auto it = unvisited.lower_bound(index + 1);
    while (it != unvisited.end() && *it <= right) {
      int next = *it;
      it = unvisited.erase(it);
      distance[next] = distance[index] + 1;
      queue.push(next);
    }
  }
  cout << distance[n - 1] << '\n';
}
```

每个允许位置只从集合中删除一次，时间 $O(n\log n)$，空间 $O(n)$。禁止位置破坏了原题的连续覆盖不变量，因此需要显式保存尚未访问的离散位置。

## 可复现验证

- 两个官方样例、单元素、一步直达、含零但可绕过以及不可达变种均应覆盖。
- 小规模数组可用 $O(n^2)$ DP 作为 oracle，与 BFS 层和贪心解对拍。
- 路径恢复结果应逐跳检查距离限制，并确认跳数等于最优值。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/jump-game-ii/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/jump-game-ii/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-48-lc1143/">← [力扣 Top 48] LC 1143 最长公共子序列 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-50-lc32/">[力扣 Top 50] LC 32 最长有效括号 困难 →</a>
</nav>
