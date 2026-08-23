---
title: "[力扣每日一题] 2026-08-24｜LC 1872 石子游戏 VIII"
---

# [力扣每日一题] 2026-08-24｜LC 1872 石子游戏 VIII

<p class="daily-archive-kicker">2026-08-24 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-24 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=80ff203c622bca51d7d68f20a53b4b7d06da7ab1abe9377d076fc94cac8822c8 -->
[力扣官方题目：1872. 石子游戏 VIII](https://leetcode.cn/problems/stone-game-viii/?envType=daily-question&envId=2026-08-24)

## 官方原始信息

- 北京时间日期：2026-08-24；题号：LC 1872。
- 官方中文标题：石子游戏 VIII；官方难度：困难。
- 原竞赛：第 242 场周赛 Q4；官方竞赛分值：6 分。
- ZeroTracer 社区估算竞赛分：2439.734，抓取于 2026-08-24；这不是官方难度或分值。
- 官方链接：[石子游戏 VIII](https://leetcode.cn/problems/stone-game-viii/?envType=daily-question&envId=2026-08-24)。
- 函数签名：`int stoneGameVIII(vector<int>& stones)`。

### 原始题意

Alice 与 Bob 面对从左到右排列的 `n` 颗石子，Alice 先手。只要石子多于一颗，当前玩家就
选择 $x>1$，移除最左边的 $x$ 颗石子，把它们的价值总和加入自己的分数，再把一颗价值等于
该总和的新石子放回最左端。只剩一颗石子时结束。Alice 最大化“Alice 得分减 Bob 得分”，
Bob 最小化它；返回双方最优时的分数差。

### 全部官方样例

```text
示例 1
输入：stones = [-1,2,-3,4,-5]
输出：5
解释：Alice 合并前 4 颗，得到 2 分和序列 [2,-5]；Bob 合并两颗，得到 -3 分。
最终分差为 2-(-3)=5。

示例 2
输入：stones = [7,-6,5,10,5,-2,-6]
输出：13
解释：Alice 一次合并全部石子，得到 13 分，游戏结束。

示例 3
输入：stones = [-10,-12]
输出：-22
解释：Alice 只有合并全部石子这一种操作，得到 -22 分。
```

### 全部约束

- `n == stones.length`。
- $2\le n\le10^5$。
- $-10^4\le stones[i]\le10^4$。

## 最优结论摘要

一次操作合并的前缀在以后始终作为一颗石子留在最左端，因此每个局面只需用“已经合并到
哪个原下标”表示。先把 `stones` 原地改成前缀和。设当前最优分差为 `best`，从右向左考察新
前缀和 $P_i$ 时，当前玩家可以立刻取得 $P_i$，再把后续局面交给对手，候选值为
$P_i-best$；也可以沿用已经覆盖更长前缀的最优选择。转移为

$$
best\leftarrow\max(best,P_i-best).
$$

时间复杂度 $O(n)$，额外空间 $O(1)$。推荐记忆“前缀和把局面压成下标，再用当前得分减对手
最优值”的博弈差值 DP。

## 约束推导、溢出与边界

- 每次合并后，左端新石子的值正是某个原数组前缀和；操作只会让此前缀继续扩大。
- 朴素状态有 $O(n)$ 个，每个状态枚举下一次合并终点会达到 $O(n^2)$，对 $10^5$ 不可行。
- 前缀和与最终分差的绝对值至多 $10^9$，`int` 在原约束内安全；推导和变种代码使用
  `long long`，避免扩展约束时溢出。
- 第一次至少合并两颗，所以线性循环只考察前缀 $P_1$ 到 $P_{n-2}$；$P_{n-1}$ 是“一次合并
  全部”的初始候选。
- `n=2` 时没有别的选择，答案就是两颗石子的和。
- 元素允许负数，不能使用“前缀和递增”或贪心取最大前缀的错误假设。

## 官方样例手推

样例 1 的前缀和为 $[-1,1,-2,2,-3]$。先令 `best=-3`，表示直接合并全部石子。反向处理
$P_3=2$ 得到 $\max(-3,2-(-3))=5$；再处理 $P_2=-2$ 与 $P_1=1$ 都不能改善 5，故答案为
5。这对应 Alice 首先合并前 4 颗，Bob 再处理余下局面。

样例 3 只有两颗石子，初始化值就是总和 $-22$，循环为空，正确保留唯一操作。

## 解法一：枚举每个局面的下一次合并终点

令 $dp[i]$ 表示左端已经合并到原下标 $i$ 后，轮到当前玩家时能取得的最大分差；终点状态
$dp[n-1]=0$。当前玩家下一次可把前缀扩到任意 $j>i$，本轮获得 $P_j$，以后双方角色交换，
所以

$$
dp[i]=\max_{j>i}\{P_j-dp[j]\}.
$$

它完整枚举了每个合法下一步，时间 $O(n^2)$、空间 $O(n)$，适合作为小规模 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int stoneGameVIII(vector<int>& stones) {
    int n = stones.size();
    vector<long long> prefix(n);
    prefix[0] = stones[0];
    for (int i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + stones[i];
    vector<long long> dp(n);
    for (int i = n - 2; i >= 0; --i) {
      dp[i] = numeric_limits<long long>::lowest();
      for (int j = i + 1; j < n; ++j) {
        dp[i] = max(dp[i], prefix[j] - dp[j]);
      }
    }
    return static_cast<int>(dp[0]);
  }
};
```

## 从二次枚举到后缀最优值

把 $dp[i]$ 的候选分成两类：下一步恰好到 $i+1$，值为 $P_{i+1}-dp[i+1]$；或下一步越过
$i+1$。后一类正是 $dp[i+1]$ 已保存的所有更远候选。因此

$$
dp[i]=\max\bigl(dp[i+1],P_{i+1}-dp[i+1]\bigr).
$$

无需保存整张表：从总前缀开始反向维护一个 `best` 即可。

## 最佳实用解：原地前缀和加一维博弈 DP

### 正确性证明

**状态充分性**：无论此前怎样操作，最左端合并石子的值都是某个原数组前缀和，右侧石子
保持原顺序；所以“已合并到下标 $i$”足以描述未来。

**转移完备性**：在状态 $i$，下一步终点要么是 $i+1$，得到
$P_{i+1}-dp[i+1]$；要么更远，这些选择的最大值恰为 $dp[i+1]$。两类不重不漏，取最大得到
正确的 $dp[i]$。

**归纳**：$dp[n-1]=0$ 正确，因为只剩一颗石子；从右向左应用完备转移，依次得到全部状态
的正确值。初始局面的合法第一步至少合并两颗，对应 $dp[0]$，故返回值正确。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int stoneGameVIII(vector<int>& stones) {
    int n = stones.size();
    for (int i = 1; i < n; ++i) {
      stones[i] += stones[i - 1];
    }
    int best = stones[n - 1];
    for (int i = n - 2; i >= 1; --i) {
      best = max(best, stones[i] - best);
    }
    return best;
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(1)$。原地前缀和会修改输入；若调用方要求保留数组，可用一个
`long long` 前缀数组，时间不变、空间 $O(n)$。

## 同阶方案比较与易错点

可以保留完整 `dp` 与 `prefix` 数组，仍为 $O(n)$ 时间，但多用 $O(n)$ 空间，优势是方便恢复
策略和回答变种。面试或竞赛只求值时优先记忆原地一变量版本；需要策略证据时改用数组版。

- 把状态理解成“还剩多少颗石子”，却忘记左端石子的值包含历史前缀。
- 写成 `best=max(best,prefix[i])`，漏掉轮到对手后的分差取反。
- 循环处理到 `i=0`，等价于允许第一次只合并一颗，违反 $x>1$。
- 把 `best` 初始化为 0；全负数组时会虚构“不操作”的选择。
- 误以为负分对当前玩家一定不利；当前玩家优化的是最终分差，而不是只看本轮得分。

## 可复现验证

两份原题函数均以 C++23 编译，逐项通过全部三个官方样例，以及 `n=2`、全正、全负、前缀和
反复变号和总和为零等边界。随机生成 $n\le10$、值域 $[-8,8]$ 的数组，以二次 DP 为 oracle
对拍线性解。

## Follow-up 与约束变种

### 变种一：恢复 Alice 的一个最优首步

新定义：同时返回最优分差和 Alice 第一次合并到的 0-based 末下标。反向维护最优值时，再保存
产生该值的终点；严格改善时更新终点，相等时保留更靠右的已有方案。时间 $O(n)$，空间
$O(n)$ 用于不修改输入的前缀和。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<long long> stoneGameVIIIWithFirstMove(vector<int>& stones) {
    int n = stones.size();
    vector<long long> prefix(n);
    prefix[0] = stones[0];
    for (int i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + stones[i];
    long long best = prefix[n - 1];
    int firstEnd = n - 1;
    for (int i = n - 2; i >= 1; --i) {
      long long candidate = prefix[i] - best;
      if (candidate > best) {
        best = candidate;
        firstEnd = i;
      }
    }
    return {best, firstEnd};
  }
};
```

### 变种二：每次至多合并 m 颗当前石子

新定义：每步仍至少合并两颗，但至多合并 $m$ 颗。原转移中的任意 $j>i$ 缩成
$i<j\le i+m-1$，后缀最大值失效。维护窗口内 $P_j-dp[j]$ 的多重集合，可在反向扫描中插入
新右端并删除过远状态。时间 $O(n\log m)$，空间 $O(m)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long stoneGameWithMergeCap(vector<int>& stones, int m) {
    int n = stones.size();
    vector<long long> prefix(n);
    prefix[0] = stones[0];
    for (int i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + stones[i];
    vector<long long> dp(n);
    multiset<long long> candidates;
    for (int i = n - 2; i >= 0; --i) {
      candidates.insert(prefix[i + 1] - dp[i + 1]);
      int expired = i + m;
      if (expired < n) {
        candidates.erase(candidates.find(prefix[expired] - dp[expired]));
      }
      dp[i] = *candidates.rbegin();
    }
    return dp[0];
  }
};
```

### 变种三：统计 Alice 的最优首步数量

新定义：返回能达到最优分差的不同第一次合并长度数量。先用线性递推保存每个 $dp[i]$；首次
选到 $j$ 的值为 $P_j-dp[j]$，逐个与 $dp[0]$ 比较即可。时间 $O(n)$，空间 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countOptimalFirstMoves(vector<int>& stones) {
    int n = stones.size();
    vector<long long> prefix(n);
    prefix[0] = stones[0];
    for (int i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + stones[i];
    vector<long long> dp(n);
    for (int i = n - 2; i >= 0; --i) {
      dp[i] = max(dp[i + 1], prefix[i + 1] - dp[i + 1]);
    }
    int count = 0;
    for (int end = 1; end < n; ++end) {
      if (prefix[end] - dp[end] == dp[0]) ++count;
    }
    return count;
  }
};
```

### 变种四：Alice 的第一次操作必须合并恰好 m 颗

新定义：只有第一次被限制为 $2\le m\le n$，之后仍可任意合并。原初始最优选择失效，但
从前缀 $P_{m-1}$ 进入的后续局面仍由同一 $dp[m-1]$ 描述，所以答案是
$P_{m-1}-dp[m-1]$。预处理 $O(n)$，单次指定 $m$ 的回答 $O(1)$，空间 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long fixedFirstMove(vector<int>& stones, int m) {
    int n = stones.size();
    vector<long long> prefix(n);
    prefix[0] = stones[0];
    for (int i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + stones[i];
    vector<long long> dp(n);
    for (int i = n - 2; i >= 0; --i) {
      dp[i] = max(dp[i + 1], prefix[i + 1] - dp[i + 1]);
    }
    return prefix[m - 1] - dp[m - 1];
  }
};
```

## 推荐记忆

前缀合并博弈先问两件事：合并后的值能否写成原数组前缀和，未来是否只由“前缀边界”决定。
若都成立，优先写分差 DP；再检查转移候选是否恰好是一个可滚动的后缀最优值。

## 来源与 Algo 状态

- [力扣中国官方题面](https://leetcode.cn/problems/stone-game-viii/?envType=daily-question&envId=2026-08-24)
- [第 242 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-242/)
- [ZeroTracer 社区评分数据](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/stone-game-viii/)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-f2/">← [codeforces] CF Round 1117 Div.2 F2 Beaver&#x27;s Jumping Track (Hard Version)</a>
<span class="daily-archive-pager__empty"></span>
</nav>
