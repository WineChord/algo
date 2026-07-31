---
title: "[力扣竞赛] 第 512 场周赛 Q3 LC 4002 统计有效序列数目 中等"
---

# [力扣竞赛] 第 512 场周赛 Q3 LC 4002 统计有效序列数目 中等

<p class="daily-archive-kicker">2026-08-01 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../math/combinatorial-counting/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a5ab896157ca4519c5a2d5eb28d60bec162f609996bf0304795dcc2fe9169726 -->
## 官方原始信息

- 来源：力扣中国。
- 比赛：第 512 场周赛。
- 比赛题号：Q3。
- 题号：LC 4002。
- 官方中文标题：统计有效序列数目。
- 官方难度：中等。
- 官方分值：5 分。
- ZeroTracer 社区估算竞赛分：截至 2026-08-01 未收录，记为未知。
- 官方链接：[统计有效序列数目](https://leetcode.cn/problems/count-valid-sequences/)。

### 原始题意

给定正整数 `n` 与 `k`。有效序列是由 $k$ 个正整数组成、元素和为 $n$，且所有元素乘积为偶数的有序序列。下标不同即视为不同序列。返回有效序列数量对 $10^9+7$ 取模的结果。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int countValidSequences(int n, int k);
};
```

### 全部官方样例

```text
输入：n = 5, k = 3
输出：3
解释：六个正整数拆分序列中，[1,2,2]、[2,1,2]、[2,2,1] 的乘积为偶数。
```

```text
输入：n = 3, k = 2
输出：2
解释：[1,2] 与 [2,1] 均有效。
```

```text
输入：n = 5, k = 5
输出：0
解释：唯一序列 [1,1,1,1,1] 的乘积为奇数。
```

### 全部约束

- $1\le n\le5\times10^5$。
- $1\le k\le n$。

## 约束推导与核心观察

直接枚举正整数拆分的数量为组合数级别。先数所有长度为 $k$、和为 $n$ 的正整数序列：隔板法给出

$$
\binom{n-1}{k-1}.
$$

乘积为奇数当且仅当每一项均为奇数。写成 $a_i=2x_i+1$，其中 $x_i\ge0$，则

$$
\sum x_i=\frac{n-k}{2}.
$$

若 $n-k$ 为奇数，全奇序列不存在；否则其数量为

$$
\binom{(n-k)/2+k-1}{k-1}
=\binom{(n+k)/2-1}{k-1}.
$$

答案就是“全部序列减去全奇序列”。最大组合数上标不超过 $n-1$，可在 $O(n)$ 时间预处理阶乘与逆阶乘。乘法用 `long long`，再对模数取余。

## 解法递进

### 解法一：递归枚举全部正整数拆分

枚举前 $k-1$ 项，末项由剩余和确定，同时记录是否已经选过偶数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  static constexpr int mod = 1000000007;
  int search(int remaining, int slots, bool hasEven) {
    if (slots == 1) {
      return hasEven || remaining % 2 == 0;
    }
    int answer = 0;
    for (int value = 1; value <= remaining - slots + 1; ++value) {
      answer += search(remaining - value, slots - 1, hasEven || value % 2 == 0);
      if (answer >= mod) {
        answer -= mod;
      }
    }
    return answer;
  }
public:
  int countValidSequences(int n, int k) {
    return search(n, k, false);
  }
};
```

时间与拆分数同阶，最坏指数级；递归空间 $O(k)$。它只适合小规模对拍。

### 解法二：按和与是否出现偶数做动态规划

状态 `dp[length][sum][parity]` 可逐项加入正整数，复杂度仍过高；利用前缀和优化最后一维枚举后，可做到 $O(nk)$，但 $n,k$ 同时达到 $5\times10^5$ 时仍不可行。真正需要消掉的是整个“逐项构造”维度。

### 最佳实用解：隔板法减去全奇序列

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  static constexpr long long mod = 1000000007;
  long long power(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
      if (exponent & 1) {
        result = result * base % mod;
      }
      base = base * base % mod;
      exponent >>= 1;
    }
    return result;
  }
public:
  int countValidSequences(int n, int k) {
    vector<long long> factorial(n + 1, 1), inverseFactorial(n + 1, 1);
    for (int i = 1; i <= n; ++i) {
      factorial[i] = factorial[i - 1] * i % mod;
    }
    inverseFactorial[n] = power(factorial[n], mod - 2);
    for (int i = n; i > 0; --i) {
      inverseFactorial[i - 1] = inverseFactorial[i] * i % mod;
    }
    auto combination = [&](int top, int choose) -> long long {
      if (choose < 0 || choose > top) {
        return 0;
      }
      return factorial[top] * inverseFactorial[choose] % mod * inverseFactorial[top - choose] % mod;
    };
    long long all = combination(n - 1, k - 1);
    long long allOdd = 0;
    if ((n - k) % 2 == 0) {
      allOdd = combination((n + k) / 2 - 1, k - 1);
    }
    return (all - allOdd + mod) % mod;
  }
};
```

时间 $O(n+\log MOD)$，空间 $O(n)$；若同一进程处理多次查询，可把阶乘表全局预处理一次，使单次查询为 $O(1)$。

## 正确性证明

所有正整数序列与在 $n$ 个单位之间选择 $k-1$ 个隔板一一对应，因此总数为 $\binom{n-1}{k-1}$。一个整数乘积为奇数，当且仅当每个因子都为奇数；这与“至少存在一个偶数”恰好互补。

对全奇序列作双射 $a_i=2x_i+1$。若 $n-k$ 为奇数，右侧非整数，故数量为 0；否则得到 $k$ 个非负整数和为 $(n-k)/2$，弱隔板法数量为 $\binom{(n+k)/2-1}{k-1}$。从全部序列中减去这个互补集合，恰好得到且不重不漏地数出所有有效序列。

## 样例手推

`n=5,k=3` 时全部正整数序列数为 $\binom42=6$。$n-k=2$ 为偶数，全奇序列数为 $\binom32=3$，所以答案 $6-3=3$。`n=3,k=2` 时全序列数 2，而 $n-k$ 为奇数，全奇序列数 0，答案 2。`n=k=5` 时两项组合数都为 1，答案 0。

## 易错点与方案比较

- “乘积为偶数”是至少一个元素为偶数，最方便的计数方式是减去“全部为奇数”。
- 正整数拆分使用 $\binom{n-1}{k-1}$；变为非负整数时才是 $\binom{n+k-1}{k-1}$。
- 全奇变换后必须先检查 $n-k$ 的奇偶性。
- 模减法要加一次模数再取模。
- 组合公式把 $O(nk)$ 状态压成两次 $O(1)$ 查询，是本题应优先记忆的“总数减补集 + 奇偶代换”。

## 变种一：乘积恰有 $r$ 个偶数因子

先选出 $r$ 个偶数位置。偶数写作 $2(y+1)$，奇数写作 $2x+1$；最小和为 $k+r$，剩余必须为非负偶数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
long long power(long long base, long long exponent) {
  long long result = 1;
  while (exponent) {
    if (exponent & 1) {
      result = result * base % mod;
    }
    base = base * base % mod;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k, evenCount;
  cin >> n >> k >> evenCount;
  int limit = n + k;
  vector<long long> factorial(limit + 1, 1), inverse(limit + 1, 1);
  for (int i = 1; i <= limit; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  inverse[limit] = power(factorial[limit], mod - 2);
  for (int i = limit; i > 0; --i) {
    inverse[i - 1] = inverse[i] * i % mod;
  }
  auto choose = [&](int top, int take) -> long long {
    if (take < 0 || take > top) {
      return 0;
    }
    return factorial[top] * inverse[take] % mod * inverse[top - take] % mod;
  };
  int residual = n - k - evenCount;
  long long answer = 0;
  if (0 <= evenCount && evenCount <= k && residual >= 0 && residual % 2 == 0) {
    int units = residual / 2;
    answer = choose(k, evenCount) * choose(units + k - 1, k - 1) % mod;
  }
  cout << answer << '\n';
}
```

时间 $O(n+k)$，空间 $O(n+k)$。

## 变种二：序列元素允许为零

总数变为和为 $n$ 的 $k$ 元非负序列 $\binom{n+k-1}{k-1}$。乘积仍只有在全部元素为奇数时才为奇数；全奇计数公式保持不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
long long power(long long base, long long exponent) {
  long long result = 1;
  while (exponent) {
    if (exponent & 1) {
      result = result * base % mod;
    }
    base = base * base % mod;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  int limit = n + k;
  vector<long long> factorial(limit + 1, 1), inverse(limit + 1, 1);
  for (int i = 1; i <= limit; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  inverse[limit] = power(factorial[limit], mod - 2);
  for (int i = limit; i > 0; --i) {
    inverse[i - 1] = inverse[i] * i % mod;
  }
  auto choose = [&](int top, int take) -> long long {
    if (take < 0 || take > top) {
      return 0;
    }
    return factorial[top] * inverse[take] % mod * inverse[top - take] % mod;
  };
  long long all = choose(n + k - 1, k - 1);
  long long odd = 0;
  if (n >= k && (n - k) % 2 == 0) {
    odd = choose((n + k) / 2 - 1, k - 1);
  }
  cout << (all - odd + mod) % mod << '\n';
}
```

时间与空间均为 $O(n+k)$。

## 变种三：同一模数下回答大量 $(n,k)$ 查询

先读完查询并按最大 $n$ 一次预处理，随后每个答案只做常数次组合数运算。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
long long power(long long base, long long exponent) {
  long long result = 1;
  while (exponent) {
    if (exponent & 1) {
      result = result * base % mod;
    }
    base = base * base % mod;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queryCount;
  cin >> queryCount;
  vector<pair<int, int>> queries(queryCount);
  int limit = 0;
  for (auto& [n, k] : queries) {
    cin >> n >> k;
    limit = max(limit, n);
  }
  vector<long long> factorial(limit + 1, 1), inverse(limit + 1, 1);
  for (int i = 1; i <= limit; ++i) {
    factorial[i] = factorial[i - 1] * i % mod;
  }
  inverse[limit] = power(factorial[limit], mod - 2);
  for (int i = limit; i > 0; --i) {
    inverse[i - 1] = inverse[i] * i % mod;
  }
  auto choose = [&](int top, int take) -> long long {
    if (take < 0 || take > top) {
      return 0;
    }
    return factorial[top] * inverse[take] % mod * inverse[top - take] % mod;
  };
  for (auto [n, k] : queries) {
    long long answer = choose(n - 1, k - 1);
    if ((n - k) % 2 == 0) {
      answer -= choose((n + k) / 2 - 1, k - 1);
    }
    cout << (answer % mod + mod) % mod << '\n';
  }
}
```

预处理 $O(N_{max})$，每次查询 $O(1)$，空间 $O(N_{max})$。

## 变种四：模数可能是合数且规模较小

费马逆元不再可用。直接用帕斯卡递推预处理组合数，不做除法，适用于任意正模数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k, modulus;
  cin >> n >> k >> modulus;
  vector<vector<int>> combination(n + 1, vector<int>(k + 1));
  combination[0][0] = 1 % modulus;
  for (int top = 1; top <= n; ++top) {
    combination[top][0] = 1 % modulus;
    for (int take = 1; take <= min(top, k); ++take) {
      combination[top][take] =
          (combination[top - 1][take - 1] + combination[top - 1][take]) % modulus;
    }
  }
  int answer = combination[n - 1][k - 1];
  if ((n - k) % 2 == 0) {
    answer -= combination[(n + k) / 2 - 1][k - 1];
  }
  cout << (answer % modulus + modulus) % modulus << '\n';
}
```

时间与空间均为 $O(nk)$；可用滚动数组把空间降为 $O(k)$。这是以规模换取对合数模数的稳健支持。

## 可复现验证

对 $1\le k\le n\le14$，递归枚举全部正整数序列，按实际乘积奇偶计数，并与组合公式逐项比较；另外校验三组官方样例和模减边界。全部代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/count-valid-sequences/)
- [第 512 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-512/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/count-valid-sequences/)
- [对应知识专题](../../math/combinatorial-counting.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-70-lc102/">← [力扣 Top 70] LC 102 二叉树的层序遍历 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-f/">[codeforces] CF Round 1111 Div.2 F Paths on a Grid →</a>
</nav>
