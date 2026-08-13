---
title: "[力扣 Top 134] LC 509 斐波那契数 简单"
---

# [力扣 Top 134] LC 509 斐波那契数 简单

<p class="daily-archive-kicker">2026-08-14 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-14 题目列表</a> · <a href="../../../dp/linear-recurrences/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=fdbc13fe24a7b064b433e3ac791df9e80b09738745b91545c5384e097064eee5 -->
[官方题目：LC 509 斐波那契数](https://leetcode.cn/problems/fibonacci-number/)

## 官方原始信息

- 题号：509。
- 标题：斐波那契数。
- 官方难度：简单。
- 官方链接：[力扣中国](https://leetcode.cn/problems/fibonacci-number/)。
- 题库顺序：Top 134；权威表格原行标题与当前官方标题一致。
- 标签：递归、记忆化搜索、数学、动态规划。

斐波那契数满足 $F(0)=0$、$F(1)=1$，并且对 $n>1$ 有

$$
F(n)=F(n-1)+F(n-2).
$$

给定整数 `n`，返回 `F(n)`。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int fib(int n);
};
```

### 全部官方样例

样例 1：

```text
输入：n = 2
输出：1
解释：F(2) = F(1) + F(0) = 1 + 0 = 1。
```

样例 2：

```text
输入：n = 3
输出：2
解释：F(3) = F(2) + F(1) = 1 + 1 = 2。
```

样例 3：

```text
输入：n = 4
输出：3
解释：F(4) = F(3) + F(2) = 2 + 1 = 3。
```

### 全部约束

- $0\le n\le30$。

## 约束推导与整数边界

$n$ 只有 30，任何正确方法都能通过，但这道题的教学价值在于识别“重叠子问题”与“状态只依赖前两项”。朴素递归会反复计算相同的 $F(k)$；记忆化把状态数降到 $n+1$；自底向上迭代进一步删除递归栈；滚动变量又把只会被下一步使用的整张表压缩成常数空间。

$F(30)=832040$，远小于 32 位有符号整数上限，因此官方函数返回 `int` 安全。若放大到 $F(47)$，结果就会溢出 `int`；若放大到任意大 $n$，还需取模、矩阵快速幂或大整数。

## 解法递进

### 解法一：按定义递归

递归树完整覆盖定义中的两条分支，因而正确；但同一个状态会在不同分支中重复出现。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
  }
};
int main() {
  cout << Solution().fib(4) << '\n';
}
```

时间 $O(\varphi^n)$，其中 $\varphi$ 为黄金分割比；递归栈空间 $O(n)$。瓶颈是重复求解相同子问题。

### 解法二：记忆化搜索

第一次求出 `fib(x)` 后缓存结果，之后直接复用。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> memo;
  int solve(int n) {
    if (n < 2) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = solve(n - 1) + solve(n - 2);
    return memo[n];
  }
public:
  int fib(int n) {
    memo.assign(n + 1, -1);
    return solve(n);
  }
};
int main() {
  cout << Solution().fib(4) << '\n';
}
```

每个状态只展开一次，时间 $O(n)$；缓存和递归栈空间均为 $O(n)$。

### 解法三：自底向上动态规划

按 $0,1,\ldots,n$ 的顺序计算，使每个转移依赖都已就绪。完整数组适合还要回答许多较小下标或恢复中间状态的场景。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int fib(int n) {
    if (n < 2) return n;
    vector<int> dp(n + 1);
    dp[1] = 1;
    for (int i = 2; i <= n; ++i) dp[i] = dp[i - 1] + dp[i - 2];
    return dp[n];
  }
};
int main() {
  cout << Solution().fib(4) << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

### 最佳实用解：滚动两个状态

转移只读取前两项，无须保存更早状态。令 `previous=F(i-1)`、`current=F(i)`，一次更新得到下一项。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int fib(int n) {
    int previous = 0;
    int current = 1;
    for (int i = 0; i < n; ++i) {
      int next = previous + current;
      previous = current;
      current = next;
    }
    return previous;
  }
};
int main() {
  cout << Solution().fib(4) << '\n';
}
```

时间 $O(n)$，额外空间 $O(1)$。对官方上限，它的证明、常数和实现稳定性最好。

### 同阶之外的优化：快速倍增

由加法公式可得

$$
F(2k)=F(k)\bigl(2F(k+1)-F(k)\bigr),
$$

$$
F(2k+1)=F(k)^2+F(k+1)^2.
$$

递归返回相邻对 $(F(n),F(n+1))$，每层把下标折半。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  pair<long long, long long> doubling(int n) {
    if (n == 0) return {0, 1};
    auto [a, b] = doubling(n / 2);
    long long even = a * (2 * b - a);
    long long odd = a * a + b * b;
    if (n % 2 == 0) return {even, odd};
    return {odd, even + odd};
  }
public:
  int fib(int n) {
    return static_cast<int>(doubling(n).first);
  }
};
int main() {
  cout << Solution().fib(30) << '\n';
}
```

时间 $O(\log n)$，递归栈空间 $O(\log n)$。官方范围不需要它，但它是大下标版本的基础。

## 正确性证明

对滚动解维护循环不变量：第 $i$ 轮开始时，`previous=F(i)` 且 `current=F(i+1)`。初始 $i=0$ 时分别为 0 和 1，成立。一次更新把二者变为 $F(i+1)$ 与 $F(i)+F(i+1)=F(i+2)$，故不变量保持。执行 $n$ 轮后 `previous=F(n)`，返回值正确。

快速倍增的两式来自斐波那契加法公式；递归基例返回 $(F(0),F(1))$。若子调用正确返回 $(F(k),F(k+1))$，两式就正确产生偶下标对，奇数分支再向前移动一项，因此归纳成立。

## 样例手推与边界

对 `n=4`，滚动状态依次为：

```text
轮前 i=0：(0,1)
轮前 i=1：(1,1)
轮前 i=2：(1,2)
轮前 i=3：(2,3)
结束      ：(3,5)
```

返回第一项 3。

- `n=0`：循环零次，直接返回 0。
- `n=1`：循环一次，返回 1。
- `n=30`：结果 832040，不溢出 `int`。
- 不要把循环写成 `i<=n`，否则会多推进一项。

## 方案比较与推荐

朴素递归最贴近定义，却隐藏指数重复；记忆化展示“缓存状态”；完整 DP 展示拓扑顺序；滚动数组展示依赖宽度决定空间；快速倍增展示代数结构带来的对数优化。面试中优先写滚动解，再根据放大的 $n$、取模或多询问要求升级到快速倍增。

## 易错点

- 官方定义从 $F(0)$ 开始，不能套用以 1、1 开头的另一种编号。
- 同时更新两个变量会覆盖旧值，应先保存 `next`。
- `int` 只因 $n\le30$ 才安全，不能把类型结论机械迁移到放大版。
- 快速倍增中应返回相邻两项，否则奇偶分支无法常数时间组合。
- 取模时 $2F(k+1)-F(k)$ 可能暂时为负，应先加模数再取模。

## 可复现验证

本页全部完整代码均以 C++23 严格编译。三个官方样例分别得到 1、2、3。对 $n=0\ldots30$，递归、记忆化、数组 DP、滚动与快速倍增五种实现逐项一致；边界 $n=30$ 得到 832040，零处不符。

## 变种一：$n$ 很大，结果对给定模数取模

沿用快速倍增，并在每个乘加后取模；下标可放大到 64 位。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class FibonacciModulo {
  long long modulus;
  pair<long long, long long> solve(unsigned long long n) {
    if (n == 0) return {0, 1 % modulus};
    auto [a, b] = solve(n / 2);
    long long factor = (2 * b % modulus - a + modulus) % modulus;
    long long even = static_cast<long long>((__int128)a * factor % modulus);
    long long odd = static_cast<long long>(
        ((__int128)a * a + (__int128)b * b) % modulus);
    if (n % 2 == 0) return {even, odd};
    return {odd, (even + odd) % modulus};
  }
public:
  explicit FibonacciModulo(long long mod) : modulus(mod) {}
  long long value(unsigned long long n) {
    return solve(n).first;
  }
};
int main() {
  cout << FibonacciModulo(1000000007).value(1000000000000000000ULL) << '\n';
}
```

时间 $O(\log n)$，空间 $O(\log n)$；`__int128` 防止两个模内 64 位数相乘溢出。

## 变种二：任意二阶线性递推

若 $G(n)=pG(n-1)+qG(n-2)$，快速倍增公式不再直接成立，但状态向量可用 $2\times2$ 矩阵快速幂推进。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Matrix {
  long long a00, a01, a10, a11;
};
Matrix multiply(const Matrix& a, const Matrix& b) {
  return {
      a.a00 * b.a00 + a.a01 * b.a10,
      a.a00 * b.a01 + a.a01 * b.a11,
      a.a10 * b.a00 + a.a11 * b.a10,
      a.a10 * b.a01 + a.a11 * b.a11};
}
long long recurrence(long long first, long long second, long long p,
  long long q, int n) {
  if (n == 0) return first;
  Matrix result{1, 0, 0, 1};
  Matrix base{p, q, 1, 0};
  int exponent = n - 1;
  while (exponent > 0) {
    if (exponent & 1) result = multiply(result, base);
    base = multiply(base, base);
    exponent >>= 1;
  }
  return result.a00 * second + result.a01 * first;
}
int main() {
  cout << recurrence(2, 3, 1, 1, 5) << '\n';
}
```

在数值不溢出的前提下，时间 $O(\log n)$，空间 $O(1)$。取模版只需在矩阵乘法内取模。

## 变种三：一次回答大量较小下标

先读完所有询问并预处理到最大下标，之后每问 $O(1)$；比对每个询问单独快速倍增更适合最大值不大的批处理。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queries;
  cin >> queries;
  vector<int> request(queries);
  int maximum = 0;
  for (int& n : request) {
    cin >> n;
    maximum = max(maximum, n);
  }
  vector<unsigned long long> fib(maximum + 2);
  fib[1] = 1;
  for (int i = 2; i <= maximum; ++i) fib[i] = fib[i - 1] + fib[i - 2];
  for (int n : request) cout << fib[n] << '\n';
}
```

预处理 $O(N)$，每问 $O(1)$，空间 $O(N)$；示例类型在 $N\le93$ 时无符号 64 位安全。

## 变种四：返回精确大整数

不取模且 $n$ 达数千时，用十进制高位在后的数组保存任意精度整数；状态转移仍是滚动 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using BigInteger = vector<int>;
BigInteger add(const BigInteger& a, const BigInteger& b) {
  BigInteger result;
  int carry = 0;
  int length = static_cast<int>(max(a.size(), b.size()));
  for (int i = 0; i < length || carry; ++i) {
    int value = carry;
    if (i < static_cast<int>(a.size())) value += a[i];
    if (i < static_cast<int>(b.size())) value += b[i];
    result.push_back(value % 10);
    carry = value / 10;
  }
  return result;
}
BigInteger exactFibonacci(int n) {
  BigInteger previous{0};
  BigInteger current{1};
  for (int i = 0; i < n; ++i) {
    BigInteger next = add(previous, current);
    previous = current;
    current = next;
  }
  return previous;
}
int main() {
  BigInteger answer = exactFibonacci(1000);
  for (auto it = answer.rbegin(); it != answer.rend(); ++it) cout << *it;
  cout << '\n';
}
```

需进行 $O(n)$ 次大整数加法，总位运算量为 $O(n^2)$；空间由结果位数主导，$F(n)$ 的十进制位数为 $\Theta(n)$。

## 变种五：允许负下标

把递推向左延伸可得负斐波那契恒等式

$$
F(-n)=(-1)^{n+1}F(n).
$$

先求绝对值下标，再按奇偶恢复符号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long nonnegativeFibonacci(int n) {
  long long previous = 0;
  long long current = 1;
  for (int i = 0; i < n; ++i) {
    long long next = previous + current;
    previous = current;
    current = next;
  }
  return previous;
}
long long fibonacci(int n) {
  if (n >= 0) return nonnegativeFibonacci(n);
  int positive = -n;
  long long value = nonnegativeFibonacci(positive);
  return positive % 2 == 0 ? -value : value;
}
int main() {
  cout << fibonacci(-8) << '\n';
}
```

时间 $O(|n|)$，空间 $O(1)$；可再与快速倍增结合为 $O(\log|n|)$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/fibonacci-number/)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc226-c/">← [atcoder] ARC226 C Square Corner Packing</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-514-q1-lc4014/">[力扣竞赛] 第 514 场周赛 Q1 LC 4014 应用折扣后的最低总价 中等 →</a>
</nav>
