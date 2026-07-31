# 数学知识地图

算法竞赛中的数学不只是套公式。常见任务是把巨大搜索空间转化为代数关系、计数结构或周期性质，并确保整数范围、取模和精度全部正确。

## 数论基础

### 最大公约数

欧几里得算法基于

$$
\gcd(a,b)=\gcd(b,a\bmod b)
$$

时间复杂度 $O(\log \min(a,b))$。最小公倍数应先除后乘以降低溢出风险：

$$
\operatorname{lcm}(a,b)=\frac{a}{\gcd(a,b)}\cdot b
$$

### 扩展欧几里得

扩展欧几里得求整数 $x,y$ 使

$$
ax+by=\gcd(a,b)
$$

它是求线性同余方程和模逆元的基础。$ax\equiv 1\pmod m$ 有解当且仅当 $\gcd(a,m)=1$。

### 素数与筛法

| 任务 | 常用方法 | 复杂度 |
| --- | --- | --- |
| 判断单个较小整数 | 试除到 $\sqrt n$ | $O(\sqrt n)$ |
| 求 $1\ldots n$ 的素数 | 埃氏筛 | $O(n\log\log n)$ |
| 同时求最小质因子 | 线性筛 | $O(n)$ |
| 64 位整数判素 | Miller–Rabin 固定底数 | $O(k\log^3 n)$ 量级 |

### 平方和分类

拉格朗日四平方定理保证每个正整数都能写成至多四个整数平方之和。勒让德三平方定理进一步指出：把 $n$ 中所有因子 $4$ 除掉后，若余数模 $8$ 等于 $7$，它不能由三个平方表示，因此最少需要四项。

于是最少平方数可以按下列顺序判定：

1. $n$ 本身是平方数，答案为 1；
2. 约去因子 $4$ 后满足 $n\bmod8=7$，答案为 4；
3. 枚举一个平方，若余数也是平方，答案为 2；
4. 其余情况由定理保证答案为 3。

整数平方判断要在修正浮点平方根后，用足够宽的整数做乘法确认。

--8<-- "includes/problems/lc-279.md"

## 模运算

若只涉及加法、减法和乘法：

$$
(a+b)\bmod m=((a\bmod m)+(b\bmod m))\bmod m
$$

$$
(ab)\bmod m=((a\bmod m)(b\bmod m))\bmod m
$$

除法不能直接取模。要把除以 $b$ 转成乘 $b^{-1}$，且逆元存在需要相应条件。

当题目要求构造“最短模零区间”一类对象时，先把子数组条件改写为前缀余数碰撞，再用鸽巢原理与周期结构判断存在性。完整推导见[前缀余数与模构造](modular-constructions.md)。

### 快速幂

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
ll qpow(ll a, long long e, ll mod) {
    ll r = 1 % mod;
    for (a %= mod; e; e >>= 1, a = (__int128)a * a % mod)
        if (e & 1) r = (__int128)r * a % mod;
    return r;
}
int main() {
    long long a, b, mod;
    cin >> a >> b >> mod;
    cout << qpow(a, b, mod) << '\n';
}
```

指数每次减半，时间 $O(\log b)$。这里用 `__int128` 避免两个 64 位模数内的数相乘溢出。

### 交换求和与线性贡献

当目标是大量区间或组合对象的总和时，直接枚举对象常会重复计算同一元素。若每个对象的值能写成元素贡献之和，可以交换求和次序：

$$
\sum_{\text{object}}\sum_i contribution(i,\text{object})
=
\sum_i\sum_{\text{object}}contribution(i,\text{object}).
$$

ABC468 E 的子数组数量达到 $\Theta(n^2)$，但固定位置 $i$ 后，它在包含自身的每个子数组平均数中只贡献长度倒数。预处理模逆元和调和前缀，就能把该位置的全部系数递推出来。这里的关键不是某个公式，而是先确认目标对数组元素是线性的。

--8<-- "includes/problems/atcoder-abc468-e.md"

若后续允许区间加，线性形式还能直接用系数前缀和更新答案；若分母、合法区间集合或目标函数依赖元素值，原有线性分解可能失效。

## 组合计数

基本工具：

- 加法原理：互斥类别的方案数相加；
- 乘法原理：连续独立选择的方案数相乘；
- 容斥原理：纠正集合交集的重复计数；
- 鸽巢原理：用数量关系证明必然存在；
- 二项式系数：$\binom nk$；
- Catalan 数：合法括号、二叉树形态等；
- Burnside / Pólya：对称下的本质不同方案。

当模数是质数 $p$ 且规模适中，可预处理阶乘与逆阶乘：

$$
\binom nk\equiv n!\,(k!)^{-1}\,((n-k)!)^{-1}\pmod p
$$

若 $n\ge p$、模数非质数或询问规模特殊，需要 Lucas、中国剩余定理或质因数分解等不同工具，不能直接沿用这一公式的实现。

字典序排列计数把固定前缀后的方案看成连续块。普通排列的块大小是阶乘，多重集合排列的块大小是多项式系数；排名、逆排名和第 $k$ 个排列的统一推导见[排列排名：从字典序块到 Lehmer 码](permutation-ranking.md)。

正整数拆分、补集计数、唯一第一事件与块收缩乘法的统一方法，见[组合计数：补集、双射与唯一分块](combinatorial-counting.md)。

## 矩阵与线性递推

矩阵乘法能组合线性变换。若状态满足固定线性递推，可以把一次转移写成矩阵 $A$，通过快速幂求 $A^n$，把线性递推从 $O(n)$ 降为 $O(k^3\log n)$，其中 $k$ 是状态维度。

斐波那契是最小示例：

$$
\begin{bmatrix}F_{n+1}\\F_n\end{bmatrix}
=
\begin{bmatrix}1&1\\1&0\end{bmatrix}^n
\begin{bmatrix}1\\0\end{bmatrix}
$$

## 概率与期望

期望的线性性不要求随机变量独立：

$$
\mathbb E\left[\sum_i X_i\right]=\sum_i\mathbb E[X_i]
$$

计数某种结构的期望数量时，常给每个候选结构定义指示变量，再分别计算出现概率。

含有“留在原状态”的期望递推要移项。例如

$$
E=p(E+1)+(1-p)\cdot 1
$$

不能直接按普通 DAG DP 计算，需要先解方程。

## 代表题目

--8<-- "includes/problems/atcoder-abc468-c.md"

--8<-- "includes/problems/codeforces-2247-b.md"

--8<-- "includes/problems/codeforces-2247-c.md"

--8<-- "includes/problems/lc-50.md"

--8<-- "includes/problems/lc-204.md"

--8<-- "includes/problems/lc-372.md"

--8<-- "includes/problems/lc-878.md"

--8<-- "includes/problems/luogu-p3383.md"

--8<-- "includes/problems/luogu-p1082.md"

## 易错检查

- 负数取模后是否规范到 $[0,m)$；
- 中间乘法是否在转型前溢出；
- 模逆元是否存在；
- 组合数预处理范围是否覆盖询问；
- 浮点比较是否使用合适误差；
- 公式是否只在质数模数或互质条件下成立；
- 多组测试的筛表和阶乘能否一次预处理复用。

## Reference

- [LeetCode 279：完全平方数](../problems/index.md#problem-lc-279)
- [Introduction to Algorithms, Fourth Edition — MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
