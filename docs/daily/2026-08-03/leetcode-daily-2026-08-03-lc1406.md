---
title: "[力扣每日一题] 2026-08-03｜LC 1406 石子游戏 III"
---

# [力扣每日一题] 2026-08-03｜LC 1406 石子游戏 III

<p class="daily-archive-kicker">2026-08-03 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=f37c57fd274bd7473ff5b789444216fd53cb5040e2209de51163eec20e44ca82 -->
## 官方原始信息

- 来源：力扣中国当天每日一题。
- 日期：2026-08-03（北京时间）。
- 题号：LC 1406。
- 官方中文标题：石子游戏 III。
- 官方难度：困难。
- 原比赛：第 183 场周赛 Q4。
- ZeroTracer 社区估算竞赛分：2026.8957817007（2026-08-03 抓取；非官方难度）。
- 官方链接：[石子游戏 III](https://leetcode.cn/problems/stone-game-iii/?envType=daily-question&envId=2026-08-03)。

### 原始题意

Alice 与 Bob 面前有一排石子，`stoneValue[i]` 是第 $i$ 堆的分值，可能为负。Alice 先手，两人轮流从剩余序列前端拿走 1、2 或 3 堆，并把这些分值加入自己的总分，直到石子取完。双方都最优；Alice 总分更高返回 `"Alice"`，Bob 更高返回 `"Bob"`，相等返回 `"Tie"`。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string stoneGameIII(vector<int>& stoneValue);
};
```

### 全部官方样例

```text
输入：stoneValue = [1,2,3,7]
输出："Bob"
解释：无论 Alice 首轮取 1、2 还是 3 堆，Bob 都能获得更高总分。
```

```text
输入：stoneValue = [1,2,3,-9]
输出："Alice"
解释：Alice 首轮取前三堆得到 6，Bob 只能拿到 -9。
```

```text
输入：stoneValue = [1,2,3,6]
输出："Tie"
解释：Alice 取前三堆得到 6，Bob 取最后一堆也得到 6。
```

### 全部约束

- $1\le stoneValue.length\le5\times10^4$。
- $-1000\le stoneValue_i\le1000$。

## 约束推导与状态选择

每轮至多三个分支，但直接展开整棵博弈树约有 $3^n$ 个节点，$n=5\times10^4$ 完全不可行。后续局面只由“当前第一堆下标”决定，与此前如何到达无关，存在大量重复子问题。

用 `dp[i]` 表示轮到行动者面对后缀 $i..n-1$ 时，自己相对对手能取得的最大分差。若本轮取走 $k$ 堆、分数和为 $take$，后续 `dp[i+k]` 是对手相对自己的最优分差，所以当前分差为

$$
take-dp[i+k].
$$

故

$$
\qquad dp[i]=\max_{1\le k\le3,\ i+k\le n}\left(\sum_{j=i}^{i+k-1}v_j-dp[i+k]\right),\qquad dp[n]=0.
$$

单堆绝对值至多 1000，总分差绝对值至多 $5\times10^7$，`int` 安全；使用 `long long` 也可。负数不能被忽略，因为石子必须全部取完，拿更多堆有时是为了迫使对手接负分。

## 解法递进

### 解法一：完整极大极小递归

递归枚举当前拿 1、2、3 堆，返回最大分差。它按规则覆盖所有策略，但不记忆状态，适合作为短数组 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const vector<int>& values, int index) {
    if (index == static_cast<int>(values.size())) {
      return 0;
    }
    int answer = numeric_limits<int>::min();
    int taken = 0;
    for (int count = 1; count <= 3 && index + count <= static_cast<int>(values.size()); ++count) {
      taken += values[index + count - 1];
      answer = max(answer, taken - search(values, index + count));
    }
    return answer;
  }
public:
  string stoneGameIII(vector<int>& stoneValue) {
    int difference = search(stoneValue, 0);
    return difference > 0 ? "Alice" : difference < 0 ? "Bob" : "Tie";
  }
};
```

时间指数级，递归栈 $O(n)$，只用于小规模定义核验。

### 解法二：后缀分差动态规划

从右向左填表，每个状态只看后三个状态，时间降为线性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string stoneGameIII(vector<int>& stoneValue) {
    int n = stoneValue.size();
    vector<int> dp(n + 1);
    for (int i = n - 1; i >= 0; --i) {
      int taken = 0;
      dp[i] = numeric_limits<int>::min();
      for (int count = 1; count <= 3 && i + count <= n; ++count) {
        taken += stoneValue[i + count - 1];
        dp[i] = max(dp[i], taken - dp[i + count]);
      }
    }
    return dp[0] > 0 ? "Alice" : dp[0] < 0 ? "Bob" : "Tie";
  }
};
```

时间 $O(n)$，额外空间 $O(n)$。数组版本最容易扩展到恢复方案。

### 最佳实用解：四槽滚动分差

转移只读取 `dp[i+1]`、`dp[i+2]`、`dp[i+3]`，用下标模 4 的环形数组保留这些值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string stoneGameIII(vector<int>& stoneValue) {
    int n = stoneValue.size();
    array<int, 4> dp{};
    for (int i = n - 1; i >= 0; --i) {
      int taken = 0;
      int best = numeric_limits<int>::min();
      for (int count = 1; count <= 3 && i + count <= n; ++count) {
        taken += stoneValue[i + count - 1];
        best = max(best, taken - dp[(i + count) % 4]);
      }
      dp[i % 4] = best;
    }
    int difference = dp[0];
    return difference > 0 ? "Alice" : difference < 0 ? "Bob" : "Tie";
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。若只需胜负，这是约束闭环的最佳实用解；若要恢复每步选择，则保留完整 `dp` 更合适。

## 正确性证明

对后缀长度作归纳。空后缀 `dp[n]=0` 显然正确。假设所有更短后缀的 `dp` 都表示轮到行动者可保证的最大分差。面对位置 $i$，当前玩家合法选择恰为取 1、2、3 堆中不越界的一种；取走分数 `taken` 后，角色交换，依归纳假设，对手能在后缀 `i+count` 保证相对当前玩家的分差 `dp[i+count]`，所以当前选择最终带来的自身分差是 `taken-dp[i+count]`。当前玩家最优必取这些合法值的最大者，转移因此精确。归纳得 `dp[0]` 是 Alice 相对 Bob 的最优分差；其正、负、零分别对应 Alice、Bob、平局。

滚动数组在写 `dp[i%4]` 前，只读取下标更大的至多三个状态，它们的模 4 槽互不与当前槽冲突，因此数值与完整表逐项相同。

## 样例手推

对 `[1,2,3,6]` 从右向左：`dp[4]=0`；`dp[3]=6`；`dp[2]=max(3-6,3+6-0)=9`；`dp[1]=max(2-9,5-6,11-0)=11`；`dp[0]=max(1-11,3-9,6-6)=0`，所以返回 `Tie`。

对 `[1,2,3,-9]`，Alice 取前三堆后分差候选为 $6-dp[3]=6-(-9)=15$，负尾堆反而扩大 Alice 优势，说明不能把负数当成可跳过元素。

## 易错点与方案比较

- `dp` 是“轮到行动者”的相对分差，不固定属于 Alice；转移必须减去后继状态。
- 每次取的是前端连续 1–3 堆，不能任选位置。
- `dp[n]=0`，靠近末尾时循环必须检查不越界。
- 负分存在时，“本轮拿得最多”不等于全局最优。
- 完整表与滚动数组时间相同；完整表便于恢复路径，滚动版空间更优。竞赛只问胜负时推荐滚动分差模板。

## 变种一：恢复双方完整取法

新定义：输出胜负、每轮拿取堆数及双方最终得分。填 `dp` 时记录最优 `choice[i]`，再从 0 按选择模拟。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> value(n), dp(n + 1), choice(n);
  for (int& score : value) {
    cin >> score;
  }
  for (int i = n - 1; i >= 0; --i) {
    int taken = 0;
    dp[i] = numeric_limits<int>::min();
    for (int count = 1; count <= 3 && i + count <= n; ++count) {
      taken += value[i + count - 1];
      int candidate = taken - dp[i + count];
      if (candidate > dp[i]) {
        dp[i] = candidate;
        choice[i] = count;
      }
    }
  }
  int index = 0;
  int turn = 0;
  array<long long, 2> score{};
  while (index < n) {
    cout << (turn == 0 ? "Alice" : "Bob") << ' ' << choice[index] << '\n';
    for (int step = 0; step < choice[index]; ++step) {
      score[turn] += value[index + step];
    }
    index += choice[index];
    turn ^= 1;
  }
  cout << score[0] << ' ' << score[1] << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。相同最优值时代码保留较少拿取的方案，形成确定性输出。

## 变种二：每轮可以拿 1 到 $K$ 堆

新定义：$K$ 可能很大。若 `best[i]` 表示当前玩家从后缀能拿到的最高总分，后缀总和为 `suffix[i]`，则

$$
best[i]=suffix[i]-\min_{i<j\le i+K}best[j].
$$

用单调队列维护滑动窗口内最小 `best`，把朴素 $O(nK)$ 降为 $O(n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<long long> value(n), suffix(n + 1), best(n + 1);
  for (long long& score : value) {
    cin >> score;
  }
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] + value[i];
  }
  deque<int> minimum;
  minimum.push_back(n);
  for (int i = n - 1; i >= 0; --i) {
    while (!minimum.empty() && minimum.front() > i + k) {
      minimum.pop_front();
    }
    best[i] = suffix[i] - best[minimum.front()];
    while (!minimum.empty() && best[minimum.back()] >= best[i]) {
      minimum.pop_back();
    }
    minimum.push_back(i);
  }
  long long alice = best[0];
  long long bob = suffix[0] - alice;
  cout << (alice > bob ? "Alice" : alice < bob ? "Bob" : "Tie") << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；固定 $K=3$ 时原滚动分差写法更简单。

## 变种三：Alice 与 Bob 的拿取上限不同

新定义：Alice 每轮可拿 1 到 $A$ 堆，Bob 可拿 1 到 $B$ 堆。状态必须加入当前玩家，原单一 `dp[i]` 失效；分别计算从位置 $i$ 开始、轮到 Alice 或 Bob 时的 Alice-Bob 最大化/最小化分差。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, aliceLimit, bobLimit;
  cin >> n >> aliceLimit >> bobLimit;
  vector<int> value(n);
  for (int& score : value) {
    cin >> score;
  }
  vector<long long> aliceTurn(n + 1), bobTurn(n + 1);
  for (int i = n - 1; i >= 0; --i) {
    long long taken = 0;
    aliceTurn[i] = numeric_limits<long long>::min();
    for (int count = 1; count <= aliceLimit && i + count <= n; ++count) {
      taken += value[i + count - 1];
      aliceTurn[i] = max(aliceTurn[i], taken + bobTurn[i + count]);
    }
    taken = 0;
    bobTurn[i] = numeric_limits<long long>::max();
    for (int count = 1; count <= bobLimit && i + count <= n; ++count) {
      taken += value[i + count - 1];
      bobTurn[i] = min(bobTurn[i], aliceTurn[i + count] - taken);
    }
  }
  cout << (aliceTurn[0] > 0 ? "Alice" : aliceTurn[0] < 0 ? "Bob" : "Tie") << '\n';
}
```

时间 $O(n(A+B))$，空间 $O(n)$。两个角色可选动作不同，必须区分状态所有者。

## 变种四：统计最优对局序列数量

新定义：双方每一步都只选能达到最优分差的拿法，统计从初始状态出发的最优拿法序列数，对 $10^9+7$ 取模。为每个状态同时维护最佳分差与达到它的后继计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  int n;
  cin >> n;
  vector<int> value(n), dp(n + 1);
  vector<long long> ways(n + 1);
  for (int& score : value) {
    cin >> score;
  }
  ways[n] = 1;
  for (int i = n - 1; i >= 0; --i) {
    int taken = 0;
    dp[i] = numeric_limits<int>::min();
    for (int count = 1; count <= 3 && i + count <= n; ++count) {
      taken += value[i + count - 1];
      int candidate = taken - dp[i + count];
      if (candidate > dp[i]) {
        dp[i] = candidate;
        ways[i] = ways[i + count];
      } else if (candidate == dp[i]) {
        ways[i] = (ways[i] + ways[i + count]) % mod;
      }
    }
  }
  cout << dp[0] << ' ' << ways[0] << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。这里统计的是拿取数量序列；若石子分值相同但下标不同，前缀规则仍使每个拿取数量唯一确定被取下标。

## 验证说明

本轮将所有代码按 C++23 编译；最佳滚动 DP 会与指数极大极小在随机长度 1–11、分值 $[-8,8]$ 的数组上对拍，并复核三个官方样例、单堆、全负、正负交替、全零与长度接近 3 的边界。每日提交使用同一份经 `clang-format` 规范化的最佳源码。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/stone-game-iii/?envType=daily-question&envId=2026-08-03)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-b/">← [codeforces] CF Round 1113 Div.2 B Merge to Match</a>
<span class="daily-archive-pager__empty"></span>
</nav>
