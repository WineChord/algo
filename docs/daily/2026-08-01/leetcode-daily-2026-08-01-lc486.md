---
title: "[力扣每日一题] 2026-08-01｜LC 486 预测赢家"
---

# [力扣每日一题] 2026-08-01｜LC 486 预测赢家

<p class="daily-archive-kicker">2026-08-01 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../dp/interval-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=310b0b5b1ee7ecc54d6d0a29ec175fa91de5939a50f6a0822b6471b59747d2af -->
## 官方原始信息

- 日期：2026-08-01（Asia/Shanghai）。
- 题号：LC 486。
- 官方中文标题：预测赢家。
- 官方难度：中等。
- 官方链接：[预测赢家](https://leetcode.cn/problems/predict-the-winner/?envType=daily-question&envId=2026-08-01)。

### 原始题意

两个玩家轮流从数组任意一端取一个数并加入自己的得分，玩家 1 先手，双方都采取使自己最终结果最优的策略。数组取空后，若玩家 1 得分不少于玩家 2，则返回 `true`；否则返回 `false`。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool predictTheWinner(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,5,2]
输出：false
解释：玩家 1 无论先取 1 还是 2，玩家 2 都能取到 5，最终玩家 1 得 3、玩家 2 得 5。
```

```text
输入：nums = [1,5,233,7]
输出：true
解释：玩家 1 先取 1，之后无论玩家 2 取 5 还是 7，玩家 1 都能取 233，最终 234 比 12。
```

### 全部约束

- $1\le |nums|\le20$。
- $0\le nums_i\le10^7$。
- 平局也算玩家 1 获胜。

## 约束推导与核心状态

每次只能取区间端点，取完后剩余状态仍是连续区间。若直接记录两人的绝对分数，会把轮次与历史带进状态；改为记录“当前行动者从区间 `[l,r]` 开始，最终能比对手多得多少分”即可得到零和差值状态：

$$
dp[l][r]=\max\bigl(nums_l-dp[l+1][r],\ nums_r-dp[l][r-1]\bigr).
$$

减号表示当前取完后角色互换，子问题中的“当前玩家优势”变成自己的劣势。单元素区间差值就是该元素。最终 $dp[0][n-1]\ge0$ 当且仅当玩家 1 能赢或打平。

$n\le20$ 允许指数搜索，但区间只有 $O(n^2)$ 个；二维 DP 可进一步按长度滚动成一维 $O(n)$ 空间。总分最大 $2\times10^8$，`int` 足够，仍可用 `long long` 使变种支持更大或负值。

## 解法递进

### 解法一：完整极小化极大搜索

枚举当前玩家取左或取右，对手随后也最优选择。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int difference(const vector<int>& nums, int left, int right) {
    if (left == right) {
      return nums[left];
    }
    return max(nums[left] - difference(nums, left + 1, right),
        nums[right] - difference(nums, left, right - 1));
  }
public:
  bool predictTheWinner(vector<int>& nums) {
    return difference(nums, 0, nums.size() - 1) >= 0;
  }
};
```

时间 $O(2^n)$，递归空间 $O(n)$。相同区间会从不同取法反复计算。

### 解法二：记忆化区间搜索

给每个 `[left,right]` 缓存差值后，状态数降为 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> memo;
  vector<vector<char>> seen;
  int solve(const vector<int>& nums, int left, int right) {
    if (left == right) {
      return nums[left];
    }
    if (seen[left][right]) {
      return memo[left][right];
    }
    seen[left][right] = true;
    int takeLeft = nums[left] - solve(nums, left + 1, right);
    int takeRight = nums[right] - solve(nums, left, right - 1);
    return memo[left][right] = max(takeLeft, takeRight);
  }
public:
  bool predictTheWinner(vector<int>& nums) {
    int n = nums.size();
    memo.assign(n, vector<int>(n));
    seen.assign(n, vector<char>(n));
    return solve(nums, 0, n - 1) >= 0;
  }
};
```

时间与空间均为 $O(n^2)$。

### 最佳实用解：一维区间 DP

令 `dp[left]` 在处理右端 `right` 时表示状态 `dp[left][right]`。转移前，`dp[left]` 是 `dp[left][right - 1]`，`dp[left + 1]` 已更新为 `dp[left + 1][right]`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool predictTheWinner(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(nums.begin(), nums.end());
    for (int right = 1; right < n; ++right) {
      for (int left = right - 1; left >= 0; --left) {
        dp[left] = max(nums[left] - dp[left + 1], nums[right] - dp[left]);
      }
    }
    return dp[0] >= 0;
  }
};
```

时间 $O(n^2)$，额外空间 $O(n)$。

## 正确性证明

对区间长度归纳。长度为 1 时，当前玩家取走唯一数字，优势为该值。长度大于 1 时，当前玩家只有两种合法动作：取左后，对手在 `[l+1,r]` 能取得 `dp[l+1][r]` 的相对优势，所以当前玩家净优势为 `nums[l]-dp[l+1][r]`；取右同理为 `nums[r]-dp[l][r-1]`。当前玩家会选择较大者，转移恰好覆盖全部且只覆盖合法策略。

因此 `dp[l][r]` 等于双方最优时当前玩家的真实最大净优势。初始当前玩家就是玩家 1；差值非负恰好表示得分不少于玩家 2，包含题目规定的平局获胜。

一维更新按 `right` 递增、`left` 递减，读取的两个子区间分别保持为本轮已更新值与上轮旧值，所以与二维转移完全等价。

## 样例手推

`[1,5,2]` 的长度 2 差值为：`[1,5]` 得 4，`[5,2]` 得 3。全区间差值为

$$
\max(1-3,\ 2-4)=-2,
$$

所以玩家 1 必输。`[1,5,233,7]` 的最终差值为 222，大于 0，返回真。

单元素总能获胜；两个相等元素最终差值为 0，平局按规则返回真；全零数组也返回真。

## 易错点与方案比较

- 状态是“轮到行动者的净优势”，不是固定玩家 1 的得分。
- 转移必须减去子问题结果，因为轮到对手。
- 平局条件是 `>=0`，不能写成 `>0`。
- 一维压缩必须让 `left` 从右向左更新，否则会覆盖仍需读取的旧状态。
- 记忆化最贴近博弈递归；二维表最便于恢复路径；只求布尔结果时推荐一维差值 DP。

## 变种一：恢复双方的一组最优取法

保留二维差值表。从全区间开始，若取左能达到当前最优值就输出 `L`，否则输出 `R`，然后缩短区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> values(n);
  for (long long& value : values) {
    cin >> value;
  }
  vector<vector<long long>> dp(n, vector<long long>(n));
  for (int i = 0; i < n; ++i) {
    dp[i][i] = values[i];
  }
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      dp[left][right] =
          max(values[left] - dp[left + 1][right], values[right] - dp[left][right - 1]);
    }
  }
  int left = 0;
  int right = n - 1;
  while (left <= right) {
    if (left == right || values[left] - dp[left + 1][right] == dp[left][right]) {
      cout << 'L';
      ++left;
    } else {
      cout << 'R';
      --right;
    }
  }
  cout << '\n';
}
```

时间与空间均为 $O(n^2)$；相等时固定优先左端，得到确定性方案。

## 变种二：统计双方都最优时的完整对局序列数

若左右动作都达到同一最优差值，两者都计入。`ways[l][r]` 累加所有最优子局面的方案数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> values(n);
  for (long long& value : values) {
    cin >> value;
  }
  vector<vector<long long>> dp(n, vector<long long>(n));
  vector<vector<long long>> ways(n, vector<long long>(n, 1));
  for (int i = 0; i < n; ++i) {
    dp[i][i] = values[i];
  }
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      long long takeLeft = values[left] - dp[left + 1][right];
      long long takeRight = values[right] - dp[left][right - 1];
      dp[left][right] = max(takeLeft, takeRight);
      ways[left][right] = 0;
      if (takeLeft == dp[left][right]) {
        ways[left][right] += ways[left + 1][right];
      }
      if (takeRight == dp[left][right]) {
        ways[left][right] += ways[left][right - 1];
      }
      ways[left][right] %= mod;
    }
  }
  cout << dp[0][n - 1] << ' ' << ways[0][n - 1] << '\n';
}
```

时间与空间均为 $O(n^2)$。单元素只有一种动作，左右指向同一元素时不重复计数。

## 变种三：允许数组元素为负数

差值递推完全不依赖非负性，只需扩大整数类型。玩家可能被迫取得负分，但仍选择使净优势最大的端点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> values(n), dp(n);
  for (long long& value : values) {
    cin >> value;
  }
  dp = values;
  for (int right = 1; right < n; ++right) {
    for (int left = right - 1; left >= 0; --left) {
      dp[left] = max(values[left] - dp[left + 1], values[right] - dp[left]);
    }
  }
  cout << dp[0] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$；输出为先手最优净优势。

## 变种四：每回合可从一端取一个或两个数

状态仍是区间净优势，但动作扩展为四种；取两个数时将其和减去缩短两格后的对手优势。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> values(n);
  for (long long& value : values) {
    cin >> value;
  }
  vector<vector<long long>> dp(n, vector<long long>(n));
  auto get = [&](int left, int right) -> long long { return left > right ? 0 : dp[left][right]; };
  for (int length = 1; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      long long best =
          max(values[left] - get(left + 1, right), values[right] - get(left, right - 1));
      if (length >= 2) {
        best = max(best, values[left] + values[left + 1] - get(left + 2, right));
        best = max(best, values[right - 1] + values[right] - get(left, right - 2));
      }
      dp[left][right] = best;
    }
  }
  cout << dp[0][n - 1] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n^2)$。动作数是常数，区间状态数量不变。

## 可复现验证

对长度 1 到 12、值域 0 到 20 的随机数组，用完整极小化极大搜索作为 oracle，与记忆化、二维和一维 DP 对拍；覆盖官方样例、平局、单元素、全零和强烈不均衡端点。所有发布代码按 C++23 编译。

## 来源

- [力扣中国官方每日一题](https://leetcode.cn/problems/predict-the-winner/?envType=daily-question&envId=2026-08-01)
- [力扣中国官方题面](https://leetcode.cn/problems/predict-the-winner/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/predict-the-winner/?envType=daily-question&envId=2026-08-01)
- [对应知识专题](../../dp/interval-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2247-f/">← [codeforces] CF Round 1111 Div.2 F Paths on a Grid</a>
<span class="daily-archive-pager__empty"></span>
</nav>
