---
title: "[力扣 Top 52] LC 55 跳跃游戏 中等"
---

# [力扣 Top 52] LC 55 跳跃游戏 中等

<p class="daily-archive-kicker">2026-07-31 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b4ae94c7f5365ddac949c8f2b63530fa6ca2042a472f67ac31e366de9497c818 -->
## 官方原始信息

- Top 排名：52
- 题号：LC 55
- 官方中文标题：跳跃游戏
- 官方难度：中等
- 官方链接：[跳跃游戏](https://leetcode.cn/problems/jump-game/)

### 原始题意

给定非负整数数组 `nums`，初始位于下标 0。`nums[i]` 表示从位置 `i` 最多能向右跳多少步，判断能否到达最后一个下标。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool canJump(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [2,3,1,1,4]
输出：true
解释：可以先从下标 0 跳到下标 1，再从下标 1 跳到最后一个下标。
```

```text
输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样都会被下标 3 的零挡住，无法到达最后一个下标。
```

### 全部约束

- $1\le n\le10^4$。
- $0\le nums_i\le10^5$。

## 约束推导与边界

从一个位置可以到达一段连续区间，因此不必记录每条具体路径，只需维护当前所有可达位置能覆盖到的最远右端点。长度为 1 时起点就是终点；遇到 0 并不必然失败，只有该位置超过已有最远边界时才不可达。计算 `i + nums[i]` 在本题范围内不会溢出 `int`。

## 解法递进

### 解法一：可达状态动态规划

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canJump(vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    vector<char> reachable(n);
    reachable[0] = true;
    for (int i = 0; i < n; ++i) {
      if (!reachable[i]) {
        continue;
      }
      for (int j = i + 1; j < n && j <= i + nums[i]; ++j) {
        reachable[j] = true;
      }
    }
    return reachable[n - 1];
  }
};
```

它显式枚举每条跳边，时间 $O(n^2)$，空间 $O(n)$。

### 最佳实用解：维护最远可达位置

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool canJump(vector<int>& nums) {
    int farthest = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (i > farthest) {
        return false;
      }
      farthest = max(farthest, i + nums[i]);
      if (farthest >= static_cast<int>(nums.size()) - 1) {
        return true;
      }
    }
    return true;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 正确性证明

处理下标 `i` 前，`farthest` 等于所有已处理且可达位置能覆盖的最远下标。若 `i > farthest`，没有已处理位置能够跳到 `i`，而所有未来位置更靠右，也不可能先被到达，因此答案为假。否则 `i` 可达，把 `i + nums[i]` 纳入最大值后不变量继续成立。若边界覆盖末尾，就存在一条由可达位置延伸到末尾的路径；若扫描完成仍未失败，最后一个位置必然可达。

## 样例手推

对 `[2,3,1,1,4]`，最远边界依次为 2、4，处理下标 1 后已覆盖末尾。对 `[3,2,1,0,4]`，边界最多为 3；扫描到下标 4 时有 `4 > 3`，因此失败。

## 易错点与方案比较

- `nums[i]` 是最大步长，可以跳任意 $1$ 到 `nums[i]` 步。
- 只有可达位置才能扩展边界，必须先检查 `i <= farthest`。
- 无需真的选择某一步；“当前可达集合的并集仍是前缀”才是贪心成立的核心。
- 推荐记忆 $O(n)$ 的最远边界不变量；动态规划只适合作为小规模验证 oracle。

## 变种一：求到达末尾的最少跳跃次数

保证末尾可达。把当前可达区间看成一层 BFS，扫描到层边界时才增加一次跳跃。

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
  int jumps = 0;
  int layerEnd = 0;
  int nextEnd = 0;
  for (int i = 0; i + 1 < n; ++i) {
    nextEnd = max(nextEnd, i + a[i]);
    if (i == layerEnd) {
      ++jumps;
      layerEnd = nextEnd;
    }
  }
  cout << jumps << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：恢复任意一条可达路径

用动态规划记录每个位置第一次被到达时的前驱；若末尾不可达则输出 -1。

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
  vector<int> parent(n, -2);
  parent[0] = -1;
  for (int i = 0; i < n; ++i) {
    if (parent[i] == -2) {
      continue;
    }
    for (int j = i + 1; j < n && j <= i + a[i]; ++j) {
      if (parent[j] == -2) {
        parent[j] = i;
      }
    }
  }
  if (parent[n - 1] == -2) {
    cout << -1 << '\n';
    return 0;
  }
  vector<int> path;
  for (int current = n - 1; current != -1; current = parent[current]) {
    path.push_back(current);
  }
  reverse(path.begin(), path.end());
  for (int i = 0; i < static_cast<int>(path.size()); ++i) {
    cout << path[i] << " \n"[i + 1 == static_cast<int>(path.size())];
  }
}
```

时间 $O(n^2)$，空间 $O(n)$。

## 变种三：统计到达末尾的不同跳法

位置序列不同即视为不同方案，答案对 $10^9+7$ 取模。只记录最远边界已不足以保留计数信息。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const int mod = 1000000007;
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  vector<int> ways(n);
  ways[0] = 1;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n && j <= i + a[i]; ++j) {
      ways[j] += ways[i];
      if (ways[j] >= mod) {
        ways[j] -= mod;
      }
    }
  }
  cout << ways[n - 1] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$；规模放大时可用差分维护区间加法降为 $O(n)$。

## 变种四：部分位置禁止落脚

起点与终点保证可用。禁用点会让可达集合不再必然是连续前缀，因此改用显式 BFS。

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
  vector<int> blocked(n);
  for (int& value : a) {
    cin >> value;
  }
  for (int& value : blocked) {
    cin >> value;
  }
  vector<char> visited(n);
  queue<int> pending;
  visited[0] = true;
  pending.push(0);
  while (!pending.empty()) {
    int current = pending.front();
    pending.pop();
    for (int next = current + 1; next < n && next <= current + a[current]; ++next) {
      if (!blocked[next] && !visited[next]) {
        visited[next] = true;
        pending.push(next);
      }
    }
  }
  cout << (visited[n - 1] ? "YES\n" : "NO\n");
}
```

时间 $O(n^2)$，空间 $O(n)$。

## 可复现验证

最佳解与动态规划 oracle 在长度 $1$ 到 $10$、元素 $0$ 到 $6$ 的随机数组上逐例比较；另覆盖单元素、全零、一步直达和边界恰好落在末尾。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/jump-game/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/jump-game/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-51-lc33/">← [力扣 Top 51] LC 33 搜索旋转排序数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-53-lc207/">[力扣 Top 53] LC 207 课程表 中等 →</a>
</nav>
