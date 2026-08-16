---
title: "[力扣每日一题] 2026-08-17｜LC 1563 石子游戏 V"
---

# [力扣每日一题] 2026-08-17｜LC 1563 石子游戏 V

<p class="daily-archive-kicker">2026-08-17 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-17 题目列表</a> · <a href="../../../dp/interval-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a2cd675cad8f73d9f8153c1c984849b1664769580265fb5d05f8405e0b146df8 -->
[力扣 1563：石子游戏 V](https://leetcode.cn/problems/stone-game-v/)

## 官方原始信息

- 每日题日期：2026-08-17（北京时间），已由力扣中国官方每日一题记录核对。
- 题号：1563。
- 官方中文标题：石子游戏 V。
- 官方难度：困难。
- 原比赛：第 203 场周赛第 4 题；官方比赛分值：7 分。
- ZeroTracer 社区估算竞赛分：2087.2049275667，抓取于 2026-08-17；这不是官方难度。
- 函数签名：`int stoneGameV(vector<int>& stoneValue)`。
- 题意：一行石子各有正整数价值。每轮 Alice 把当前行切成两个非空连续部分，Bob 丢弃
  总价值较大的部分，Alice 获得留下部分的总价值；若两边相等，Alice 自选保留哪边。只剩
  一块时结束，求 Alice 能获得的最大总分。

### 全部官方样例

样例 1：

```text
输入：stoneValue = [6,2,3,4,5,5]
输出：18
解释：先切为 [6,2,3] 与 [4,5,5]，保留和为 11 的左边；再切为 [6] 与 [2,3]，
保留和为 5 的右边；最后把 [2,3] 切开并保留 2，总分为 11 + 5 + 2 = 18。
```

样例 2：

```text
输入：stoneValue = [7,7,7,7,7,7,7]
输出：28
```

样例 3：

```text
输入：stoneValue = [4]
输出：0
```

### 全部官方约束

- `1 <= stoneValue.length <= 500`。
- `1 <= stoneValue[i] <= 1000000`。

## 约束推导与状态选择

每轮保留下来的仍是原数组的一个连续区间，故定义 $dp[l][r]$ 为只剩闭区间 `[l,r]` 时的
最大后续得分。枚举切点 $k$，令

$$
L=\operatorname{sum}(l,k),\qquad R=\operatorname{sum}(k+1,r).
$$

- $L<R$ 时右边被丢弃，候选为 $L+dp[l][k]$；
- $L>R$ 时左边被丢弃，候选为 $R+dp[k+1][r]$；
- $L=R$ 时 Alice 选择后续得分更高的一边。

前缀和让每次区间求和降为 $O(1)$，直接区间 DP 是 $O(n^3)$。$n=500$ 时需要继续利用
石子价值均为正数这一关键约束：切点右移时 $L$ 严格增大、$R$ 严格减小，所以两者至多
跨越一次。

总分不会溢出 `int`。每轮保留的部分价值不超过当前总价值的一半，所有得分受一个递减的
几何级数控制，小于初始总和；而初始总和至多 $5\times10^8$。

## 样例手推与边界

样例 1 的第一刀切在 3 与 4 之间：左和 11、右和 14，保留左边并先得 11。区间
`[6,2,3]` 再切为 `[6]` 与 `[2,3]`，保留右边得 5；最后得 2，总分 18。

- 单石子没有合法切法，答案为 0。
- 两块石子只能切一次，得分为两者较小值。
- 两边和相等时不能固定保留左边，要比较两边的后续最优值。
- 全部值为正，分界指针才单调；若允许 0，非严格单调仍可谨慎处理，若允许负数则优化失效。
- 相同总和可能由不同切点产生，状态必须按区间而不是只按总和记忆。

## 解法一：记忆化枚举所有切点

递归遍历当前区间的每个切点，用二维记忆避免重复求同一子区间。这是完整、直接的递推实现，
也是平方优化的可靠 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> prefix;
  vector<vector<int>> memo;
  int sum(int left, int right) const {
    return prefix[right + 1] - prefix[left];
  }
  int solve(int left, int right) {
    if (left == right) return 0;
    int& answer = memo[left][right];
    if (answer != -1) return answer;
    answer = 0;
    for (int middle = left; middle < right; ++middle) {
      int leftSum = sum(left, middle);
      int rightSum = sum(middle + 1, right);
      if (leftSum <= rightSum) {
        answer = max(answer, leftSum + solve(left, middle));
      }
      if (leftSum >= rightSum) {
        answer = max(answer, rightSum + solve(middle + 1, right));
      }
    }
    return answer;
  }
public:
  int stoneGameV(vector<int>& stoneValue) {
    int n = stoneValue.size();
    prefix.assign(n + 1, 0);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + stoneValue[i];
    memo.assign(n, vector<int>(n, -1));
    return solve(0, n - 1);
  }
};
```

状态数 $O(n^2)$，每个状态枚举 $O(n)$ 个切点，总时间 $O(n^3)$、空间 $O(n^2)$。瓶颈是
同一区间里，大量切点只是在重复取一侧的“区间和 + 子问题最优值”的最大值。

## 从三次方到平方：单调分界与区间最大值

定义两张辅助表：

$$
\operatorname{leftBest}[l][k]
=\max_{l\le x\le k}\bigl(\operatorname{sum}(l,x)+dp[l][x]\bigr),
$$

$$
\operatorname{rightBest}[k][r]
=\max_{k\le x\le r}\bigl(\operatorname{sum}(x,r)+dp[x][r]\bigr).
$$

对固定 `[l,r]`，设 $m$ 是满足 `sum(l,m) <= sum(m+1,r)` 的最大切点。所有偏左切点的
候选可由 `leftBest[l][m]` 一次取得；偏右切点由 `rightBest` 一次取得。若 $m$ 处严格
小于，右侧合法切点从 `m + 1` 开始，对应保留段起点 `m + 2`；若恰好相等，`m` 自身也能
保留右边，起点是 `m + 1`。

当 `r` 右移时，正数前缀和保证 $m$ 只向右移动。对每个固定 `l` 用一个指针扫描全部 `r`，
所有分界移动合计 $O(n)$。

## 最佳实用解：单调切点加双向最优表

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int stoneGameV(vector<int>& stoneValue) {
    int n = stoneValue.size();
    vector<int> prefix(n + 1);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + stoneValue[i];
    auto sum = [&](int left, int right) {
      return prefix[right + 1] - prefix[left];
    };
    vector<vector<int>> dp(n, vector<int>(n));
    vector<vector<int>> leftBest(n, vector<int>(n));
    vector<vector<int>> rightBest(n, vector<int>(n));
    for (int left = n - 1; left >= 0; --left) {
      leftBest[left][left] = stoneValue[left];
      rightBest[left][left] = stoneValue[left];
      int boundary = left - 1;
      for (int right = left + 1; right < n; ++right) {
        while (boundary + 1 < right &&
                sum(left, boundary + 1) <= sum(boundary + 2, right)) {
          ++boundary;
        }
        if (boundary >= left) dp[left][right] = leftBest[left][boundary];
        int rightStart = boundary + 2;
        if (boundary >= left &&
            sum(left, boundary) == sum(boundary + 1, right)) {
          rightStart = boundary + 1;
        }
        if (rightStart <= right) {
          dp[left][right] = max(dp[left][right], rightBest[rightStart][right]);
        }
        int total = sum(left, right);
        leftBest[left][right] = max(leftBest[left][right - 1],
            total + dp[left][right]);
        rightBest[left][right] = max(rightBest[left + 1][right],
            total + dp[left][right]);
      }
    }
    return dp[0][n - 1];
  }
};
```

时间 $O(n^2)$、空间 $O(n^2)$。相较三次方递推，它没有改变状态或决策，只把同一侧的候选
最大值增量维护起来；证明负担可控，也适合 $n=500$。面试先写清 $O(n^3)$ 递推，再在约束
要求下解释这两张辅助表，是最稳妥的记忆路径。

## 正确性证明

**引理 1：三次方区间递推完整且正确。**

任一第一刀都有唯一切点。Bob 的规则唯一决定保留和较小的一侧；相等时 Alice 可选任一侧。
本轮得分是保留侧的区间和，之后问题与同一侧子区间完全同构。枚举全部切点并取最大值，
因此不漏任何策略且只使用合法策略。

**引理 2：固定 `[l,r]` 的可保留左侧切点构成前缀，可保留右侧切点构成后缀。**

切点右移时左和因正数严格增加，右和严格减少，所以谓词 $L\le R$ 由真至假至多一次；
$L\ge R$ 同理形成后缀，等号切点同时属于二者。

**引理 3：辅助表返回各自切点集合的真实最优值。**

若保留左侧 `[l,k]`，候选恰为 `sum(l,k) + dp[l][k]`；`leftBest` 按右端前缀取最大，
所以覆盖所有 $k\le m$。保留右侧 `[k+1,r]` 时，`rightBest` 按左端后缀取最大，严格
不等与相等两种边界分别从 `m + 2` 与 `m + 1` 开始，恰好覆盖全部合法右侧。

**引理 4：算法计算顺序满足全部依赖。**

`left` 从右向左、`right` 从左向右时，所有真子区间 `dp` 已完成；两张辅助表分别从相邻
前缀与相邻后缀增量得到。分界指针只向右移动，仍为每个区间找到引理 2 的最大 $m$。

由四个引理，平方算法与完整区间递推在每个状态上取到相同最大值，最终答案正确。

## 方案比较与易错点

- 不能贪心选择“当前两边最接近”的切点；当前得分相同或相近时，后续区间价值可能不同。
- 两边相等时要比较两个子问题，不能任意固定一边。
- `boundary` 是满足 `leftSum <= rightSum` 的最后切点；右侧候选的起点要区分等号。
- `leftBest/rightBest` 存的是“区间和 + dp”，不是单独的 `dp`。
- 正数约束支撑分界单调；允许负数时必须退回完整枚举或换模型。
- 单石子的 `dp` 是 0，但辅助表基值是该石子价值，因为它代表下一轮保留该区间时的
  “本轮得分 + 后续得分”。
- 前缀和与答案用 `int` 安全，但推导整数上界后再决定类型，不能仅凭函数返回类型猜测。

## 验证说明

三组官方样例均通过。对 $1\le n\le9$、小正整数随机数组，将记忆化 $O(n^3)$ oracle 与
$O(n^2)$ 实现逐状态比较；另穷举全 1、严格递增、严格递减、重复值、等和多切点与最大值
边界。全部发布代码均以 C++23 编译。

## 变种一：恢复一条最优切分与保留路径

保留三次方 DP 中取得最优值的切点和方向，再从完整区间一路回溯到单石子。输出每轮当前
区间、切点和保留方向；若同分，下面代码稳定选择先遇到的方案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Choice {
  int middle = -1;
  bool keepLeft = true;
};
int main() {
  int n;
  cin >> n;
  vector<int> value(n), prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    cin >> value[i];
    prefix[i + 1] = prefix[i] + value[i];
  }
  auto sum = [&](int left, int right) {
    return prefix[right + 1] - prefix[left];
  };
  vector<vector<int>> dp(n, vector<int>(n));
  vector<vector<Choice>> choice(n, vector<Choice>(n));
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      for (int middle = left; middle < right; ++middle) {
        int leftSum = sum(left, middle);
        int rightSum = sum(middle + 1, right);
        if (leftSum <= rightSum) {
          int candidate = leftSum + dp[left][middle];
          if (candidate > dp[left][right]) {
            dp[left][right] = candidate;
            choice[left][right] = {middle, true};
          }
        }
        if (leftSum >= rightSum) {
          int candidate = rightSum + dp[middle + 1][right];
          if (candidate > dp[left][right]) {
            dp[left][right] = candidate;
            choice[left][right] = {middle, false};
          }
        }
      }
    }
  }
  cout << dp[0][n - 1] << '\n';
  int left = 0;
  int right = n - 1;
  while (left < right) {
    Choice current = choice[left][right];
    cout << left << ' ' << right << ' ' << current.middle << ' '
          << (current.keepLeft ? "LEFT" : "RIGHT") << '\n';
    if (current.keepLeft) right = current.middle;
    else left = current.middle + 1;
  }
}
```

时间 $O(n^3)$、空间 $O(n^2)$，输出路径至多 $n-1$ 轮。若要同时保留平方时间，可在辅助
最大值表中额外存放取得最大值的端点。

## 变种二：石子价值允许为负数

Bob 仍丢弃数值和较大的部分。区间递推本身继续成立，但切点右移时两边和不再单调，平方
优化失效；必须枚举全部切点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<long long> value(n), prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    cin >> value[i];
    prefix[i + 1] = prefix[i] + value[i];
  }
  auto sum = [&](int left, int right) {
    return prefix[right + 1] - prefix[left];
  };
  vector<vector<long long>> dp(n, vector<long long>(n));
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      dp[left][right] = LLONG_MIN;
      for (int middle = left; middle < right; ++middle) {
        long long leftSum = sum(left, middle);
        long long rightSum = sum(middle + 1, right);
        if (leftSum <= rightSum) {
          dp[left][right] = max(dp[left][right],
                                leftSum + dp[left][middle]);
        }
        if (leftSum >= rightSum) {
          dp[left][right] = max(dp[left][right],
                                rightSum + dp[middle + 1][right]);
        }
      }
    }
  }
  cout << dp[0][n - 1] << '\n';
}
```

时间 $O(n^3)$、空间 $O(n^2)$，并改用 `long long`；负得分使原来的几何上界也不再是合适
的类型依据。

## 变种三：统计最优决策路径数量

把一次决策定义为“第一刀切点 + 等和时选择保留哪边”。除最大分数外维护方案数；多个切点
同分时相加，等和且两边后续同分时两种保留方向都计入，模 $10^9+7$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;
int main() {
  int n;
  cin >> n;
  vector<int> value(n), prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    cin >> value[i];
    prefix[i + 1] = prefix[i] + value[i];
  }
  auto sum = [&](int left, int right) {
    return prefix[right + 1] - prefix[left];
  };
  vector<vector<int>> best(n, vector<int>(n));
  vector<vector<int>> ways(n, vector<int>(n, 1));
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      ways[left][right] = 0;
      auto relax = [&](int score, int count) {
        if (score > best[left][right]) {
          best[left][right] = score;
          ways[left][right] = count;
        } else if (score == best[left][right]) {
          ways[left][right] = (ways[left][right] + count) % MOD;
        }
      };
      for (int middle = left; middle < right; ++middle) {
        int leftSum = sum(left, middle);
        int rightSum = sum(middle + 1, right);
        if (leftSum < rightSum) {
          relax(leftSum + best[left][middle], ways[left][middle]);
        } else if (leftSum > rightSum) {
          relax(rightSum + best[middle + 1][right],
                ways[middle + 1][right]);
        } else {
          relax(leftSum + best[left][middle], ways[left][middle]);
          relax(rightSum + best[middle + 1][right],
                ways[middle + 1][right]);
        }
      }
    }
  }
  cout << best[0][n - 1] << ' ' << ways[0][n - 1] << '\n';
}
```

时间 $O(n^3)$、空间 $O(n^2)$。原平方表只保存最大值，无法直接承载“同分方案数相加”的
全部信息；若规模仍为 500，应再为辅助表设计最大值与计数的合并规则。

## 变种四：同一数组回答大量初始区间询问

每次询问 `[left,right]`，游戏直接从该子区间开始。一次预处理全部 $dp$ 状态后即可
$O(1)$ 返回；下面沿用平方算法。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queryCount;
  cin >> n >> queryCount;
  vector<int> value(n), prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    cin >> value[i];
    prefix[i + 1] = prefix[i] + value[i];
  }
  auto sum = [&](int left, int right) {
    return prefix[right + 1] - prefix[left];
  };
  vector<vector<int>> dp(n, vector<int>(n));
  vector<vector<int>> leftBest(n, vector<int>(n));
  vector<vector<int>> rightBest(n, vector<int>(n));
  for (int left = n - 1; left >= 0; --left) {
    leftBest[left][left] = value[left];
    rightBest[left][left] = value[left];
    int boundary = left - 1;
    for (int right = left + 1; right < n; ++right) {
      while (boundary + 1 < right &&
              sum(left, boundary + 1) <= sum(boundary + 2, right)) {
        ++boundary;
      }
      if (boundary >= left) dp[left][right] = leftBest[left][boundary];
      int rightStart = boundary + 2;
      if (boundary >= left &&
          sum(left, boundary) == sum(boundary + 1, right)) {
        rightStart = boundary + 1;
      }
      if (rightStart <= right) {
        dp[left][right] = max(dp[left][right], rightBest[rightStart][right]);
      }
      int total = sum(left, right);
      leftBest[left][right] = max(leftBest[left][right - 1],
          total + dp[left][right]);
      rightBest[left][right] = max(rightBest[left + 1][right],
          total + dp[left][right]);
    }
  }
  while (queryCount--) {
    int left, right;
    cin >> left >> right;
    cout << dp[left][right] << '\n';
  }
}
```

预处理时间、空间均为 $O(n^2)$，单次查询 $O(1)$。若数组发生点更新，大量区间状态都会
失效，不能只局部修改三项；那会进入动态区间 DP 的全新问题。

## Reference

- [力扣 1563 官方题面](https://leetcode.cn/problems/stone-game-v/)
- [第 203 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-203/)
- [ZeroTracer 社区估算数据](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/stone-game-v/)
- [对应知识专题](../../dp/interval-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-f/">← [codeforces] CF Round 1116 Div.1 D / Div.2 F How Long Until Nothing Remains?</a>
<span class="daily-archive-pager__empty"></span>
</nav>
