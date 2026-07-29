---
title: "[atcoder] ABC468 E Sum of Average"
---

# [atcoder] ABC468 E Sum of Average

<p class="daily-archive-kicker">2026-07-30 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=659a8a8671fbb4126f482b3c072d1cbe80bce46d8eae823b79d899d49ae68d61 -->
## 官方来源与元数据

- 来源：AtCoder。
- 比赛：AtCoder Beginner Contest 468。
- 题号与标题：E - Sum of Average。
- 官方分值：450 分。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- 官方题面：[ABC468 E - Sum of Average](https://atcoder.jp/contests/abc468/tasks/abc468_e?lang=en)。
- 版权条款：[AtCoder Terms of Service](https://atcoder.jp/tos)。

普通 AtCoder 比赛题面没有已确认的统一开放转载许可。下方英文层依据官方题面独立组织，完整保留任务定义、输入输出、约束、样例与必要说明；官方页面仍是事实核验的权威入口。

## Complete English statement

- Contest: AtCoder Beginner Contest 468
- Task: E - Sum of Average
- Official score: 450 points
- Rated range: 0–1999
- Time limit: 2 seconds
- Memory limit: 1024 MiB
- Official task: [ABC468 E - Sum of Average](https://atcoder.jp/contests/abc468/tasks/abc468_e?lang=en)

This self-contained English presentation was independently organized from the official task and preserves its complete mathematical meaning, input, output, constraints, samples, and notes. The official task remains the authoritative source. AtCoder does not provide a confirmed blanket permission for reproducing ordinary contest statements; see the [AtCoder Terms of Service](https://atcoder.jp/tos).

### Problem Statement

You are given a positive integer $N$ and an integer sequence

$$
A=(A_1,A_2,\ldots,A_N).
$$

For $1\le l\le r\le N$, define $f(l,r)$ as the arithmetic mean of

$$
A_l,A_{l+1},\ldots,A_r.
$$

Find

$$
\sum_{1\le l\le r\le N}f(l,r)
$$

modulo $998244353$.

### Rational numbers modulo $998244353$

Under the constraints, the rational answer can be written as an irreducible fraction $P/Q$ with

$$
Q\not\equiv0\pmod{998244353}.
$$

There is therefore a unique integer $R$ satisfying

$$
0\le R<998244353,\qquad RQ\equiv P\pmod{998244353}.
$$

Output this $R$.

### Input

```text
N
A_1 A_2 ... A_N
```

### Output

Output the answer.

### Complete constraints

$$
1\le N\le5\times10^5
$$

$$
0\le A_i<998244353
$$

All input values are integers.

### Official sample 1

```text
2
2 3
```

```text
499122184
```

Here,

$$
f(1,1)=2,\qquad f(1,2)=\frac{2+3}{2}=\frac52,\qquad f(2,2)=3.
$$

Their sum is $15/2$, whose representation modulo $998244353$ is $499122184$.

### Official sample 2

```text
6
1 2 3 4 5 6
```

```text
499122250
```

### Official sample 3

```text
9
3 1 4 1 5 9 2 6 5
```

```text
855638200
```

## 中文题意与元数据说明

给定长度为 $N$ 的数组。对每个非空连续子数组取算术平均数，再把所有平均数相加，输出其在模 $998244353$ 意义下的值。

AtCoder 官方未标注独立题目难度。AtCoder Problems 社区模型在 2026-07-30 的估算难度为 1038；这是社区估算，不是 AtCoder 官方难度。

## 约束推导

子数组数量为 $N(N+1)/2$；当 $N=5\times10^5$ 时约有 $1.25\times10^{11}$ 个，不能逐个枚举。

所有平均数的分母都在 $1$ 到 $N$ 之间，而 $N<998244353$，所以每个分母在模数下都有逆元。设调和前缀为

$$
H_k=\sum_{j=1}^{k}\frac1j,\qquad H_0=0,
$$

其中除法均用模逆元解释。目标对每个 $A_i$ 都是线性的，只要在 $O(N)$ 时间算出它在所有子数组平均数中的总系数即可。

## 解法递进

### 解法一：枚举所有子数组

固定左端点并增量维护区间和；每个合法 $(l,r)$ 恰好访问一次。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int64> a(n + 1), inverse(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
  }
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  int64 answer = 0;
  for (int left = 1; left <= n; ++left) {
    int64 sum = 0;
    for (int right = left; right <= n; ++right) {
      sum = (sum + a[right]) % MOD;
      answer = (answer + sum * inverse[right - left + 1]) % MOD;
    }
  }
  cout << answer << '\n';
}
```

时间复杂度 $O(N^2)$，空间复杂度 $O(N)$；瓶颈是仍枚举全部子数组。

### 最佳实用解：交换求和并统计元素贡献

交换求和顺序：

$$
\sum_{1\le l\le r\le N}f(l,r)
=
\sum_{i=1}^{N}A_i
\sum_{1\le l\le i\le r\le N}\frac1{r-l+1}.
$$

记 $A_i$ 的系数为 $C_i$。固定 $l$ 后，

$$
\sum_{r=i}^{N}\frac1{r-l+1}
=H_{N-l+1}-H_{i-l}.
$$

因此

$$
C_i
=\sum_{l=1}^{i}\left(H_{N-l+1}-H_{i-l}\right)
=\sum_{j=0}^{i-1}(H_{N-j}-H_j),
$$

并得到递推

$$
C_0=0,\qquad
C_i=C_{i-1}+H_{N-i+1}-H_{i-1}.
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int64> a(n + 1), inverse(n + 1), harmonic(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
  }
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  for (int i = 1; i <= n; ++i) {
    harmonic[i] = (harmonic[i - 1] + inverse[i]) % MOD;
  }
  int64 coefficient = 0;
  int64 answer = 0;
  for (int i = 1; i <= n; ++i) {
    coefficient = (coefficient + harmonic[n - i + 1] - harmonic[i - 1] + MOD) % MOD;
    answer = (answer + a[i] * coefficient) % MOD;
  }
  cout << answer << '\n';
}
```

时间复杂度 $O(N)$，空间复杂度 $O(N)$。

### 同阶方案：前缀和展开

设

$$
B_i=\sum_{k=1}^{i}A_k,\qquad B_0=0.
$$

由 $f(l,r)=(B_r-B_{l-1})/(r-l+1)$ 分别聚合正负两部分，可得

$$
\sum_{l\le r}f(l,r)
=\sum_{i=0}^{N}(H_i-H_{N-i})B_i.
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int64> inverse(n + 1), harmonic(n + 1), prefix(n + 1);
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  for (int i = 1; i <= n; ++i) {
    int64 value;
    cin >> value;
    harmonic[i] = (harmonic[i - 1] + inverse[i]) % MOD;
    prefix[i] = (prefix[i - 1] + value) % MOD;
  }
  int64 answer = 0;
  for (int i = 0; i <= n; ++i) {
    int64 weight = (harmonic[i] - harmonic[n - i] + MOD) % MOD;
    answer = (answer + prefix[i] * weight) % MOD;
  }
  cout << answer << '\n';
}
```

两种最优方案都是 $O(N)$ 时间、$O(N)$ 空间。元素贡献的组合意义更直接，便于推广；前缀展开公式更短，但更容易写错 $B_{l-1}$ 与 $H_{N-l+1}$ 的偏移。推荐优先记忆贡献递推。

## 正确性证明

对固定位置 $i$，所有包含它的子数组一一对应于 $1\le l\le i\le r\le N$。在子数组 $[l,r]$ 的平均数中，$A_i$ 的系数恰为 $1/(r-l+1)$，所以 $C_i$ 精确统计了 $A_i$ 在原目标中的全部贡献，没有遗漏或重复。

固定 $l$ 后把区间长度作为求和变量，倒数和为 $H_{N-l+1}-H_{i-l}$。分别重编号两个求和，得到 $C_i$ 的调和数表达式；相邻 $C_i$ 相减后只剩 $H_{N-i+1}-H_{i-1}$，递推成立。最终累加 $\sum_iA_iC_i$ 与原目标完全相同。

## 样例手推

对 $N=2$：

$$
H_0=0,\qquad H_1=1,\qquad H_2=\frac32.
$$

于是

$$
C_1=H_2-H_0=\frac32,
$$

$$
C_2=C_1+H_1-H_1=\frac32.
$$

总和为

$$
2C_1+3C_2=\frac{15}{2},
$$

与官方样例一致。

## 易错点

- 普通整数除法无效，必须乘模逆元。
- 线性逆元递推依赖 $1\le i<MOD$，本题由约束保证。
- $H_0$ 必须定义为 0。
- 模意义下做减法要先加 `MOD`。
- `long long` 足以承接两个模内数的乘积；若扩大模数需重新评估溢出。
- 系数满足镜像对称 $C_i=C_{N-i+1}$，可作为调试不变量。
- 公式中的两个求和是分别重编号，不是把固定 $l$ 的两项强行映射到同一个下标。

## 变种一：区间加后在线输出答案

新定义：每次把 $A_l,\ldots,A_r$ 同时增加 $x$，随后输出新的全部子数组平均数之和。原目标是线性形式 $F(A)=\sum_iC_iA_i$，所以

$$
\Delta F=x\sum_{i=l}^{r}C_i.
$$

预处理系数前缀和即可 $O(1)$ 更新。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int64> a(n + 1), inverse(n + 1), harmonic(n + 1);
  vector<int64> coefficient(n + 1), prefix(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
  }
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  for (int i = 1; i <= n; ++i) {
    harmonic[i] = (harmonic[i - 1] + inverse[i]) % MOD;
  }
  int64 answer = 0;
  for (int i = 1; i <= n; ++i) {
    coefficient[i] = (coefficient[i - 1] + harmonic[n - i + 1] - harmonic[i - 1] + MOD) % MOD;
    prefix[i] = (prefix[i - 1] + coefficient[i]) % MOD;
    answer = (answer + a[i] * coefficient[i]) % MOD;
  }
  while (q--) {
    int left, right;
    int64 delta;
    cin >> left >> right >> delta;
    delta = (delta % MOD + MOD) % MOD;
    int64 weight = (prefix[right] - prefix[left - 1] + MOD) % MOD;
    answer = (answer + delta * weight) % MOD;
    cout << answer << '\n';
  }
}
```

预处理 $O(N)$，每次更新 $O(1)$，空间 $O(N)$。

## 变种二：只统计长度位于 $[L,R]$ 的子数组

设前缀和为 $S_i$，其前缀再记为 $T_i=\sum_{j=0}^{i}S_j$。固定长度 $d$ 的全部窗口和为

$$
(T_N-T_{d-1})-T_{N-d}.
$$

再除以 $d$ 并枚举允许长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, low, high;
  cin >> n >> low >> high;
  vector<int64> inverse(n + 1), prefix(n + 1), prefix_of_prefix(n + 1);
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  for (int i = 1; i <= n; ++i) {
    int64 value;
    cin >> value;
    prefix[i] = (prefix[i - 1] + value) % MOD;
    prefix_of_prefix[i] = (prefix_of_prefix[i - 1] + prefix[i]) % MOD;
  }
  int64 answer = 0;
  for (int length = low; length <= high; ++length) {
    int64 window_sum =
        prefix_of_prefix[n] - prefix_of_prefix[length - 1] - prefix_of_prefix[n - length];
    window_sum = (window_sum % MOD + MOD) % MOD;
    answer = (answer + window_sum * inverse[length]) % MOD;
  }
  cout << answer << '\n';
}
```

时间 $O(N+R-L+1)$，空间 $O(N)$。

## 变种三：圆环上的全部连续段

新定义：数组首尾相接，对每个起点和每个长度 $1$ 至 $N$ 取圆环连续段平均数并求和。固定长度 $d$ 时，每个元素在全部 $N$ 个窗口中恰出现 $d$ 次，除以 $d$ 后总贡献一次。因此每种长度的总和都是 $\sum_iA_i$，答案为

$$
N\sum_iA_i.
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  int64 sum = 0;
  for (int i = 0; i < n; ++i) {
    int64 value;
    cin >> value;
    sum = (sum + value) % MOD;
  }
  cout << sum * n % MOD << '\n';
}
```

时间 $O(N)$，空间 $O(1)$。

## 变种四：分母改为长度的 $p$ 次幂

新定义：求

$$
\sum_{1\le l\le r\le N}
\frac{\sum_{i=l}^{r}A_i}{(r-l+1)^p}.
$$

定义广义调和前缀

$$
G_k^{(p)}=\sum_{t=1}^{k}\frac1{t^p}.
$$

原贡献证明不变，只需把 $H$ 换成 $G^{(p)}$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 MOD = 998244353;
int64 power(int64 base, long long exponent) {
  int64 result = 1;
  while (exponent > 0) {
    if (exponent & 1) {
      result = result * base % MOD;
    }
    base = base * base % MOD;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long p;
  cin >> n >> p;
  vector<int64> a(n + 1), inverse(n + 1), generalized(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
  }
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = MOD - MOD / i * inverse[MOD % i] % MOD;
  }
  for (int i = 1; i <= n; ++i) {
    generalized[i] = (generalized[i - 1] + power(inverse[i], p)) % MOD;
  }
  int64 coefficient = 0;
  int64 answer = 0;
  for (int i = 1; i <= n; ++i) {
    coefficient = (coefficient + generalized[n - i + 1] - generalized[i - 1] + MOD) % MOD;
    answer = (answer + a[i] * coefficient) % MOD;
  }
  cout << answer << '\n';
}
```

时间 $O(N\log p)$，空间 $O(N)$；固定小常数 $p$ 时可直接连乘逆元。

## 可复现验证

- 推荐解应逐项通过三个官方样例。
- 小规模随机数组可将二重枚举作为 oracle，与贡献递推及前缀展开对拍。
- 限制长度、圆环、区间加和长度幂变种都可各自与小规模暴力对拍。
- 所有完整代码按 GNU++23 编译。

## Reference

- [ABC468 E 官方题面](https://atcoder.jp/contests/abc468/tasks/abc468_e?lang=en)
- [ABC468 官方题解](https://atcoder.jp/contests/abc468/editorial/23476?lang=en)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
- [AtCoder Problems 社区估算数据](https://kenkoooo.com/atcoder/resources/problem-models.json)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_e?lang=en)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-41-lc300/">[力扣 Top 41] LC 300 最长递增子序列 中等 →</a>
</nav>
