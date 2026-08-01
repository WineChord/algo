---
title: "[力扣每日一题] 2026-08-02｜LC 877 石子游戏"
---

# [力扣每日一题] 2026-08-02｜LC 877 石子游戏

<p class="daily-archive-kicker">2026-08-02 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../dp/interval-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=7d0d9d2b687ee40b96a04c43e89e325a47bebdfdc266a2efd4e673c0bd68a349 -->
## 官方原始信息

- 日期：2026-08-02（Asia/Shanghai）
- 题号：LC 877
- 官方中文标题：石子游戏
- 官方难度：中等
- 官方链接：[石子游戏（2026-08-02 每日题入口）](https://leetcode.cn/problems/stone-game/?envType=daily-question&envId=2026-08-02)

### 原始题意

偶数堆正整数石子排成一行，石子总数为奇数。Alice 与 Bob 轮流从当前行首或行尾拿走整堆石子，Alice 先手，双方都采用最优策略；当 Alice 最终石子数更多时返回 `true`，否则返回 `false`。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool stoneGame(vector<int>& piles);
};
```

### 全部官方样例

```text
输入：piles = [5,3,4,5]
输出：true
解释：Alice 先取 5。无论 Bob 取 3 还是 5，Alice 都能在下一回合拿到 4，并最终获胜。
```

```text
输入：piles = [3,7,2,3]
输出：true
```

### 全部约束

- $2\le piles.length\le500$。
- `piles.length` 为偶数。
- $1\le piles[i]\le500$。
- 石子总数为奇数。

## 约束推导与博弈表示

直接枚举双方每回合从两端二选一会形成 $2^n$ 级决策树。通用做法是把子问题压成区间：`dp[l][r]` 表示当前玩家面对区间 $[l,r]$ 时，相对另一玩家最多能多拿多少石子。取左端后的净优势是 `piles[l]-dp[l+1][r]`，取右端同理。

本题还有更强结构：堆数为偶数。按原数组下标奇偶分成两组，先手可在第一步选择其中一组，并在以后每轮继续拿到该组的端点。总石子数为奇数，所以两组和不相等；Alice 选择和更大的那组即可严格获胜。因此本题最终答案恒为真，甚至无需读取具体数值。通用 DP 仍值得保留，因为一旦取消“偶数堆”或改变取法，奇偶策略立即失效。

最大总石子数为 $500\times500=250000$，`int` 安全。

## 解法递进

### 解法一：递归极大极小搜索

枚举当前玩家取左或取右，返回最大分差。故意不记忆化，作为最直接的暴力定义。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int difference(const vector<int>& piles, int left, int right) {
    if (left == right) {
      return piles[left];
    }
    return max(piles[left] - difference(piles, left + 1, right),
        piles[right] - difference(piles, left, right - 1));
  }
public:
  bool stoneGame(vector<int>& piles) {
    return difference(piles, 0, piles.size() - 1) > 0;
  }
};
```

时间 $O(2^n)$，递归空间 $O(n)$；瓶颈是同一区间被不同取法反复求解。

### 解法二：区间动态规划

按区间长度从小到大计算最大分差，消除重复子问题。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool stoneGame(vector<int>& piles) {
    int n = piles.size();
    vector<vector<int>> dp(n, vector<int>(n));
    for (int index = 0; index < n; ++index) {
      dp[index][index] = piles[index];
    }
    for (int length = 2; length <= n; ++length) {
      for (int left = 0; left + length <= n; ++left) {
        int right = left + length - 1;
        dp[left][right] =
            max(piles[left] - dp[left + 1][right], piles[right] - dp[left][right - 1]);
      }
    }
    return dp[0][n - 1] > 0;
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$。滚动数组可降到 $O(n)$，但二维表更便于恢复方案和回答区间询问。

### 最佳实用解：奇偶下标策略

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool stoneGame(vector<int>& piles) {
    (void)piles;
    return true;
  }
};
```

时间 $O(1)$，空间 $O(1)$。这是利用全部官方约束后的最优解；面试中应先讲清区间 DP，再指出奇偶策略为何把答案压缩成常量。

## 正确性证明

### 区间 DP

对长度 1 的区间，当前玩家拿走唯一一堆，净优势就是该堆石子数。对长度大于 1 的区间，当前玩家只能取左端或右端；取走一端后，对手在剩余区间能取得的最大净优势已由更短区间状态给出，所以当前玩家的净优势分别是“所取石子数减去对手优势”。取两者最大值覆盖了全部合法首步，并假设双方后续最优，递推正确。

### 奇偶策略

原数组有偶数个位置，所以当前区间每当轮到 Alice 时，两个端点的原下标奇偶性不同。Alice 第一次可以选择拿奇下标组或偶下标组；此后无论 Bob 拿走哪个端点，Alice 下一回合仍能从两个端点中拿到自己承诺的奇偶组。归纳可知 Alice 能拿完所选组的全部石子。两组总和之和为奇数，因此两组和不相等；选择较大者后 Alice 得分严格超过一半，必胜。故 `return true` 对所有合法输入成立。

## 样例手推

对 `[5,3,4,5]`，偶下标组和为 $5+4=9$，奇下标组和为 $3+5=8$。Alice 承诺拿偶下标组：先拿左端 5；Bob 取一端后，原下标为 2 的 4 必会成为 Alice 可选端点，Alice 拿到 4，总计 9，大于 Bob 的 8。

## 易错点与方案比较

- DP 状态应表示“当前玩家相对对手的分差”，才能统一处理双方最优决策。
- 递推是减去对手优势，不是加上子区间最大值。
- 常量答案依赖“堆数为偶数、总和为奇数、只能取两端”三项条件；任一改变都不能照搬。
- 只交题时常量解最短；教学和迁移时区间 DP 更通用。推荐同时掌握：先用 DP 建模，再用约束证明恒真。

## 变种一：堆数任意且总和可能为偶数

新定义：堆数可奇可偶，并允许平局；仍问先手是否严格获胜。奇偶分组策略不再保证，使用一维压缩区间 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> piles(n);
  for (int& pile : piles) {
    cin >> pile;
  }
  vector<int> dp = piles;
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      dp[left] = max(piles[left] - dp[left + 1], piles[right] - dp[left]);
    }
  }
  cout << (dp[0] > 0 ? "Alice" : dp[0] == 0 ? "Draw" : "Bob") << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$。

## 变种二：恢复双方的一条最优取法

新定义：输出在双方最优下每回合取左还是取右。保留二维分差表，再从整段开始按等式选择动作并缩小区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> piles(n);
  for (int& pile : piles) {
    cin >> pile;
  }
  vector<vector<int>> dp(n, vector<int>(n));
  for (int index = 0; index < n; ++index) {
    dp[index][index] = piles[index];
  }
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      dp[left][right] = max(piles[left] - dp[left + 1][right], piles[right] - dp[left][right - 1]);
    }
  }
  int left = 0;
  int right = n - 1;
  string moves;
  while (left < right) {
    int takeLeft = piles[left] - dp[left + 1][right];
    if (takeLeft == dp[left][right]) {
      moves.push_back('L');
      ++left;
    } else {
      moves.push_back('R');
      --right;
    }
  }
  moves.push_back('L');
  cout << dp[0][n - 1] << '\n' << moves << '\n';
}
```

时间 $O(n^2)$，空间 $O(n^2)$；相等时固定选左得到确定性方案。

## 变种三：多次询问任意子区间的最优分差

新定义：数组固定，之后有多次 $[l,r]$ 查询，问轮到当前玩家时的最优净胜分。预处理全部区间，单次直接查表。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> piles(n);
  for (int& pile : piles) {
    cin >> pile;
  }
  vector<vector<int>> dp(n, vector<int>(n));
  for (int index = 0; index < n; ++index) {
    dp[index][index] = piles[index];
  }
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      dp[left][right] = max(piles[left] - dp[left + 1][right], piles[right] - dp[left][right - 1]);
    }
  }
  int queries;
  cin >> queries;
  while (queries--) {
    int left, right;
    cin >> left >> right;
    cout << dp[left][right] << '\n';
  }
}
```

预处理时间和空间均为 $O(n^2)$，每次询问 $O(1)$。

## 变种四：每回合可从任一端拿一堆或连续两堆

新定义：若剩余至少两堆，可从左端或右端一次拿连续两堆。原来的奇偶控制失效；区间 DP 枚举四种首步并减去剩余区间的对手优势。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> piles(n);
  for (int& pile : piles) {
    cin >> pile;
  }
  vector<vector<int>> dp(n, vector<int>(n));
  for (int index = 0; index < n; ++index) {
    dp[index][index] = piles[index];
  }
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      int best = max(piles[left] - dp[left + 1][right], piles[right] - dp[left][right - 1]);
      int afterLeftTwo = left + 2 <= right ? dp[left + 2][right] : 0;
      int afterRightTwo = left <= right - 2 ? dp[left][right - 2] : 0;
      best = max(best, piles[left] + piles[left + 1] - afterLeftTwo);
      best = max(best, piles[right] + piles[right - 1] - afterRightTwo);
      dp[left][right] = best;
    }
  }
  cout << dp[0][n - 1] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n^2)$。每个区间只多枚举常数个动作。

## 可复现验证

对小规模正整数数组，用指数极大极小搜索作为 oracle，逐项比较二维 DP、一维 DP；对满足原题全部约束的偶数长度、奇数总和数组，验证分差始终为正，并检查奇偶组策略确实可执行。覆盖两堆、重复值、极端大堆、左右对称和接近打平等边界。所有代码以 GNU++23 编译；实际提交源码另经固定 clang-format、多行排版、两空格缩进和官方样例门禁。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/stone-game/?envType=daily-question&envId=2026-08-02)
- [对应知识专题](../../dp/interval-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-a/">← [codeforces] CF Round 1113 Div.2 A You Delete, I Delete</a>
<span class="daily-archive-pager__empty"></span>
</nav>
