---
title: "[力扣每日一题] 2026-08-09｜LC 1140 石子游戏 II"
---

# [力扣每日一题] 2026-08-09｜LC 1140 石子游戏 II

<p class="daily-archive-kicker">2026-08-09 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=6135d3d8d80d515a6cd5e06947d95712f816678cebff55dd10f2dcb4f21f1cf1 -->
## 官方原始信息

- 日期：2026-08-09（北京时间）。
- 题号：LC 1140。
- 官方中文标题：石子游戏 II。
- 官方难度：中等。
- 官方链接：[石子游戏 II](https://leetcode.cn/problems/stone-game-ii/)
- 官方每日一题接口已核对该题日期为 2026-08-09。

### 原始题意与函数签名

正整数石子堆从左到右排列。Alice 与 Bob 轮流从剩余前端取走连续 `X` 堆，初始 `M=1`，每回合满足 $1\le X\le2M$，随后令 $M=\max(M,X)$。Alice 先手，双方最优，返回 Alice 最多能取得的石子数。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int stoneGameII(vector<int>& piles);
};
```

### 全部官方样例

```text
输入：piles = [2,7,9,4,4]
输出：10
解释：Alice 先取一堆，Bob 取两堆，Alice 再取两堆，可得 2+4+4=10；先取两堆只能得 9。
```

```text
输入：piles = [1,2,3,4,5,100]
输出：104
```

### 全部约束

- $1\le n\le100$。
- $1\le piles_i\le10^4$。
- 每回合至少取一堆，至多取当前剩余堆数与 $2M$ 的较小值。
- 所有石子总数不超过 $10^6$，`int` 足够。

## 约束推导与观察

状态由“当前第一堆下标 `i`”和当前 `M` 唯一决定。设 `suffix[i]` 是从 `i` 到末尾的石子总数，`dp(i,M)` 是轮到当前玩家时最终最多能拿到的石子。若本回合取 `X` 堆，剩余局面中对手最多拿 `dp(i+X,max(M,X))`，当前玩家得到

$$
suffix_i-dp(i+X,\max(M,X)).
$$

枚举合法 `X` 取最大值。正石子还带来安全剪枝：若 $2M\ge n-i$，直接取完所有剩余堆最优。

## 解法递进

### 解法一：不记忆的完整极小化搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> suffix;
  int n;
  int solve(int index, int m) {
    if (index == n) {
      return 0;
    }
    int best = 0;
    for (int take = 1; take <= min(2 * m, n - index); ++take) {
      best = max(best, suffix[index] - solve(index + take, max(m, take)));
    }
    return best;
  }
public:
  int stoneGameII(vector<int>& piles) {
    n = piles.size();
    suffix.assign(n + 1, 0);
    for (int i = n - 1; i >= 0; --i) {
      suffix[i] = suffix[i + 1] + piles[i];
    }
    return solve(0, 1);
  }
};
int main() {
}
```

覆盖全部博弈树，分支最多 $2M$、深度至多 $n$，时间指数级，递归空间 $O(n)$，适合小规模 oracle。

### 解法二：记忆化搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> suffix;
  vector<vector<int>> memo;
  int n;
  int solve(int index, int m) {
    if (2 * m >= n - index) {
      return suffix[index];
    }
    int& answer = memo[index][m];
    if (answer != -1) {
      return answer;
    }
    answer = 0;
    for (int take = 1; take <= 2 * m; ++take) {
      answer = max(answer, suffix[index] - solve(index + take, max(m, take)));
    }
    return answer;
  }
public:
  int stoneGameII(vector<int>& piles) {
    n = piles.size();
    suffix.assign(n + 1, 0);
    for (int i = n - 1; i >= 0; --i) {
      suffix[i] = suffix[i + 1] + piles[i];
    }
    memo.assign(n, vector<int>(n + 1, -1));
    return solve(0, 1);
  }
};
int main() {
}
```

状态数 $O(n^2)$，每个状态枚举至多 $O(n)$ 个动作，保守时间 $O(n^3)$、空间 $O(n^2)$；在 $n=100$ 下稳定。

### 最佳实用解：自底向上的后缀博弈 DP

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int stoneGameII(vector<int>& piles) {
    int n = piles.size();
    vector<int> suffix(n + 1);
    for (int i = n - 1; i >= 0; --i) {
      suffix[i] = suffix[i + 1] + piles[i];
    }
    vector<vector<int>> dp(n + 1, vector<int>(n + 1));
    for (int index = n - 1; index >= 0; --index) {
      for (int m = n; m >= 1; --m) {
        if (2 * m >= n - index) {
          dp[index][m] = suffix[index];
          continue;
        }
        for (int take = 1; take <= 2 * m; ++take) {
          dp[index][m] = max(dp[index][m], suffix[index] - dp[index + take][max(m, take)]);
        }
      }
    }
    return dp[0][1];
  }
};
int main() {
}
```

时间 $O(n^3)$、空间 $O(n^2)$。记忆化通常只访问可达状态、常数更小；自底向上没有递归风险且依赖顺序清楚。提交优先选记忆化版，教学时保留表 DP。

## 正确性证明

对剩余堆数归纳。空局面当前玩家得 0；若可一次取完，所有石子为正，取完显然最优。否则任一合法首步 `X` 唯一转移到更短的状态 `(i+X,max(M,X))`。归纳假设给出对手从该状态能取得的最大石子；由于剩余总和固定，当前玩家最终所得恰为 `suffix[i]-opponent`。枚举所有合法 `X` 取最大，既覆盖所有策略又选择最佳回应，因此 `dp` 定义成立，初始状态 `dp(0,1)` 即 Alice 的最优结果。

## 样例手推

对 `[2,7,9,4,4]`，Alice 若首取 1 堆，状态变为 `(1,1)`；Bob 的最优回应取 2 堆，Alice 随后可取剩余 2 堆，总得 10。首取 2 堆时 `M=2`，Bob 可把后三堆全部取走，Alice 只有 9。DP 在两个首步中取前者。

## 易错点与方案比较

- 状态值定义为“当前玩家最多拿多少”，不是固定为 Alice；这样才能用 `suffix-opponent`。
- 更新后的 `M` 是 `max(M,X)`，不是简单变成 `X`。
- 只有正石子时，“能取完就取完”剪枝才安全。
- `memo` 的 `M` 维度开到 `n+1` 足够；一旦 `M>=n` 必然触发取完分支。

## 变种一：恢复双方的一条最优取法

新定义：返回每回合取了多少堆。记忆化时保存达到最优值的 `X`，再从初始状态模拟。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> optimalMoves(const vector<int>& piles) {
  int n = piles.size();
  vector<int> suffix(n + 1);
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] + piles[i];
  }
  vector<vector<int>> memo(n, vector<int>(n + 1, -1));
  vector<vector<int>> choice(n, vector<int>(n + 1, 1));
  auto solve = [&](auto&& self, int index, int m) -> int {
    if (2 * m >= n - index) {
      choice[index][m] = n - index;
      return suffix[index];
    }
    int& result = memo[index][m];
    if (result != -1) {
      return result;
    }
    result = -1;
    for (int take = 1; take <= 2 * m; ++take) {
      int current = suffix[index] - self(self, index + take, max(m, take));
      if (current > result) {
        result = current;
        choice[index][m] = take;
      }
    }
    return result;
  };
  solve(solve, 0, 1);
  vector<int> moves;
  for (int index = 0, m = 1; index < n;) {
    int take = choice[index][m];
    moves.push_back(take);
    index += take;
    m = max(m, take);
  }
  return moves;
}
int main() {
  for (int x : optimalMoves({2, 7, 9, 4, 4})) {
    cout << x << ' ';
  }
}
```

时间 $O(n^3)$、空间 $O(n^2)$，输出回合数至多 $n$。

## 变种二：每回合上限改为 `c*M`

新定义：常数 `c>=1`，合法动作变为 $1\le X\le cM$。原状态和零和递推仍成立，只需替换动作上限。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int stoneGameMultiplier(const vector<int>& piles, int c) {
  int n = piles.size();
  vector<int> suffix(n + 1);
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] + piles[i];
  }
  vector<vector<int>> memo(n, vector<int>(n + 1, -1));
  auto solve = [&](auto&& self, int index, int m) -> int {
    if (1LL * c * m >= n - index) {
      return suffix[index];
    }
    int& result = memo[index][m];
    if (result != -1) {
      return result;
    }
    result = 0;
    for (int take = 1; take <= c * m; ++take) {
      result = max(result, suffix[index] - self(self, index + take, max(m, take)));
    }
    return result;
  };
  return solve(solve, 0, 1);
}
int main() {
  cout << stoneGameMultiplier({2, 7, 9, 4, 4}, 3) << '\n';
}
```

保守时间 $O(cn^3)$、空间 $O(n^2)$。

## 变种三：每回合最多固定取 `K` 堆

新定义：删除动态 `M`，每次可取 1 到 `K` 堆。状态只剩下标，复杂度降为 $O(nK)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long fixedLimitGame(const vector<int>& piles, int k) {
  int n = piles.size();
  vector<long long> suffix(n + 1), dp(n + 1);
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] + piles[i];
    for (int take = 1; take <= k && i + take <= n; ++take) {
      dp[i] = max(dp[i], suffix[i] - dp[i + take]);
    }
  }
  return dp[0];
}
int main() {
  cout << fixedLimitGame({2, 7, 9, 4, 4}, 2) << '\n';
}
```

时间 $O(nK)$、空间 $O(n)$。

## 变种四：石子数允许为负

新定义：某些堆是惩罚分，但仍必须最终取完。原“可取完就全部取走”剪枝失效；保留完整动作枚举，递推本身仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long stoneGameWithPenalties(const vector<long long>& piles) {
  int n = piles.size();
  vector<long long> suffix(n + 1);
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] + piles[i];
  }
  vector<vector<long long>> memo(n, vector<long long>(n + 1, LLONG_MIN));
  auto solve = [&](auto&& self, int index, int m) -> long long {
    if (index == n) {
      return 0;
    }
    long long& result = memo[index][m];
    if (result != LLONG_MIN) {
      return result;
    }
    result = LLONG_MIN / 4;
    for (int take = 1; take <= min(2 * m, n - index); ++take) {
      result = max(result, suffix[index] - self(self, index + take, max(m, take)));
    }
    return result;
  };
  return solve(solve, 0, 1);
}
int main() {
  cout << stoneGameWithPenalties({5, -100, 4}) << '\n';
}
```

时间 $O(n^3)$、空间 $O(n^2)$。负数不形成循环，因为下标仍严格增加，但会改变贪心终止条件。

## 可复现验证

对 $n=1..10$、堆值 `1..9` 的随机实例，枚举完整博弈树作 oracle，对比记忆化和表 DP；官方两组样例与单堆、可一次取完、全相等、末尾大堆均覆盖。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/stone-game-ii/)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-f/">← [codeforces] CF Round 1113 Div.2 F Matrix Elimination</a>
<span class="daily-archive-pager__empty"></span>
</nav>
