---
title: "[力扣 Top 31] LC 279 完全平方数 中等"
---

# [力扣 Top 31] LC 279 完全平方数 中等

<p class="daily-archive-kicker">2026-07-29 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../math/index.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：31
- 题号：LC 279
- 官方中文标题：完全平方数
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/perfect-squares/>

### 原始题意

给定整数 `n`，返回和为 `n` 的完全平方数的最少数量。完全平方数是某个整数的平方。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int numSquares(int n);
};
```

### 全部官方样例

```text
输入：n = 12
输出：3
解释：12 = 4 + 4 + 4
```

```text
输入：n = 13
输出：2
解释：13 = 4 + 9
```

### 全部约束

- $1\le n\le10^4$。
- 平方数最多枚举到 $\lfloor\sqrt n\rfloor$。
- 答案由拉格朗日四平方定理保证不超过 4。

## 最优结论

用数论分类：

1. `n` 本身是平方数，答案为 1；
2. 去掉所有因子 4 后若余数模 8 等于 7，由勒让德三平方定理，答案为 4；
3. 枚举一个平方，若剩余部分也是平方，答案为 2；
4. 其余情况答案为 3。

时间复杂度 $O(\sqrt n)$，空间 $O(1)$。面试若不希望依赖数论定理，优先写 $O(n\sqrt n)$ 的完全背包 DP；竞赛追求最优时记数论分类。

## 约束推导与边界

状态 `dp[x]` 表示凑出 `x` 的最少平方数，转移为

$$
dp[x]=1+\min_{j^2\le x}dp[x-j^2].
$$

这给出稳健的 $O(n\sqrt n)$ 基线。数论解把“搜索组合”变成只判断答案属于 1、2、3、4 中哪一类。

边界包括 `n=1`、平方数、两个平方之和、形如 $4^a(8b+7)$ 的四平方类。整数平方判断要在 `sqrt` 结果附近复核，避免浮点误差。

## 解法递进

### 解法一：完全背包 DP

枚举目标和并尝试最后一个平方数，覆盖所有分解。时间 $O(n\sqrt n)$，空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numSquares(int n) {
    vector<int> dp(n + 1, n + 1);
    dp[0] = 0;
    for (int value = 1; value <= n; ++value) {
      for (int root = 1; root * root <= value; ++root) {
        dp[value] = min(dp[value], dp[value - root * root] + 1);
      }
    }
    return dp[n];
  }
};
```

### 解法二：余数图上的 BFS

把每个余数看作节点，从 `x` 向 `x-square` 连边；所有边代价为 1，第一次到达 0 的层数就是答案。复杂度同为 $O(n\sqrt n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numSquares(int n) {
    vector<int> distance(n + 1, -1);
    queue<int> pending;
    distance[n] = 0;
    pending.push(n);
    while (!pending.empty()) {
      int value = pending.front();
      pending.pop();
      for (int root = 1; root * root <= value; ++root) {
        int next = value - root * root;
        if (distance[next] != -1) {
          continue;
        }
        distance[next] = distance[value] + 1;
        if (next == 0) {
          return distance[next];
        }
        pending.push(next);
      }
    }
    return -1;
  }
};
```

### 解法三：四平方与三平方定理

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool isSquare(int value) {
    int root = static_cast<int>(sqrt(value));
    while (1LL * root * root < value) {
      ++root;
    }
    while (1LL * root * root > value) {
      --root;
    }
    return root * root == value;
  }
public:
  int numSquares(int n) {
    if (isSquare(n)) {
      return 1;
    }
    int reduced = n;
    while (reduced % 4 == 0) {
      reduced /= 4;
    }
    if (reduced % 8 == 7) {
      return 4;
    }
    for (int root = 1; root * root <= n; ++root) {
      if (isSquare(n - root * root)) {
        return 2;
      }
    }
    return 3;
  }
};
```

## 正确性证明

拉格朗日四平方定理保证任意正整数最多需要 4 个平方数。平方判断直接识别答案 1。

勒让德三平方定理说明整数能写成三个平方之和，当且仅当它不形如 $4^a(8b+7)$；因此该特殊形式既不是 1 或 2 个平方之和，也不能用 3 个，只能为 4。

排除答案 1 与 4 后，枚举 `root` 检查 `n-root²` 是否为平方，恰好识别答案 2。剩余整数由三平方定理可用至多 3 个，又不能用 1 或 2 个，所以答案为 3。

## 样例手推

`n=12` 不是平方；去掉因子 4 得 3，非 `7 mod 8`；不存在两个平方之和，因此答案 3。`n=13` 枚举到 `root=2` 时剩余 9 是平方，答案 2。

## 易错点

- 勒让德判定前必须反复除去因子 4。
- 两平方枚举要允许剩余为 0；不过答案 1 已提前返回。
- `root*root` 在本题范围安全，但通用实现可用 `long long`。
- 数论解只返回数量；若需恢复方案，应改用带父指针 DP。

## 验证说明

对 `n=1..10000`，数论解与完全背包 DP 逐一比较；同时单测平方数、两个平方之和及 $4^a(8b+7)$ 类。

## Follow-up 与变种

### 变种一：恢复一组最短分解

DP 记录最后选取的平方，随后反向恢复。时间 $O(n\sqrt n)$，空间 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> decompose(int n) {
    vector<int> dp(n + 1, n + 1);
    vector<int> choice(n + 1, -1);
    dp[0] = 0;
    for (int value = 1; value <= n; ++value) {
      for (int root = 1; root * root <= value; ++root) {
        int square = root * root;
        if (dp[value - square] + 1 < dp[value]) {
          dp[value] = dp[value - square] + 1;
          choice[value] = square;
        }
      }
    }
    vector<int> answer;
    while (n > 0) {
      answer.push_back(choice[n]);
      n -= choice[n];
    }
    return answer;
  }
};
```

### 变种二：大量 `n` 查询

预先对最大值做一次 DP，之后每次 $O(1)$ 回答。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<int> queries(q);
  int maximum = 0;
  for (int& value : queries) {
    cin >> value;
    maximum = max(maximum, value);
  }
  vector<int> dp(maximum + 1, maximum + 1);
  dp[0] = 0;
  for (int value = 1; value <= maximum; ++value) {
    for (int root = 1; root * root <= value; ++root) {
      dp[value] = min(dp[value], dp[value - root * root] + 1);
    }
  }
  for (int value : queries) {
    cout << dp[value] << '\n';
  }
  return 0;
}
```

### 变种三：统计恰用 `k` 个平方数的有序表示数

顺序不同视为不同方案。令 `dp[used][sum]` 逐个位置添加平方，复杂度 $O(kn\sqrt n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countOrdered(int n, int k, int mod) {
    vector<vector<int>> dp(k + 1, vector<int>(n + 1, 0));
    dp[0][0] = 1;
    for (int used = 0; used < k; ++used) {
      for (int sum = 0; sum <= n; ++sum) {
        for (int root = 1; sum + root * root <= n; ++root) {
          int& target = dp[used + 1][sum + root * root];
          target = (target + dp[used][sum]) % mod;
        }
      }
    }
    return dp[k][n];
  }
};
```

### 变种四：每个平方数有不同代价

目标从最少个数变为最小总代价，完全背包转移中的 `+1` 改为对应平方的代价。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long minimumCost(int n, const vector<long long>& cost) {
    const long long inf = numeric_limits<long long>::max() / 4;
    vector<long long> dp(n + 1, inf);
    dp[0] = 0;
    for (int sum = 1; sum <= n; ++sum) {
      for (int root = 1; root * root <= sum; ++root) {
        dp[sum] = min(dp[sum], dp[sum - root * root] + cost[root]);
      }
    }
    return dp[n];
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/perfect-squares/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/perfect-squares/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="atcoder-abc468-d.md">← [atcoder] ABC468 D Pre-Palindrome</a>
<a class="daily-archive-pager__next" href="leetcode-top-32-lc22.md">[力扣 Top 32] LC 22 括号生成 中等 →</a>
</nav>
