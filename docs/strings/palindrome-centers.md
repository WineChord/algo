# 回文：区间状态、中心与线性半径

回文题首先要区分连续子串与可跳过的子序列。连续回文由中心和半径唯一描述；这使中心扩展与 Manacher 成为比通用区间 DP 更贴近结构的解法。

<figure class="knowledge-figure" id="figure-palindrome-radius">
  <a class="knowledge-figure__image-link" href="../../assets/figures/palindrome-radius.svg" aria-label="打开回文中心与半径原图">
    <img src="../../assets/figures/palindrome-radius.svg" alt="插入分隔符后的字符串以一个中心和半径表示回文，并展示中心扩展与 Manacher 镜像复用" width="960" height="460" loading="lazy" decoding="async">
  </a>
  <figcaption>分隔符统一奇偶中心；Manacher 先利用最右回文区间中的镜像半径，再只对未知部分继续扩张。</figcaption>
</figure>

## 最长回文子串

--8<-- "includes/problems/lc-5.md"

## 从暴力到最优

### 枚举子串并检查

共有 $O(n^2)$ 个区间，每次双指针检查 $O(n)$，总时间 $O(n^3)$、空间 $O(1)$。它适合作为随机对拍的可靠基准。

### 区间动态规划

定义 `dp[l][r]` 表示 `s[l..r]` 是否回文：

$$
dp[l][r]=(s_l=s_r)\land\bigl(r-l\le2\ \lor\ dp[l+1][r-1]\bigr).
$$

时间、空间均为 $O(n^2)$。循环顺序必须保证内部区间先计算；它复用判断结果，但保存了远多于最终最长区间所需的状态。

### 中心扩展

每个回文有唯一的奇中心或偶中心。枚举 $n$ 个字符中心和 $n-1$ 个字符间中心，分别向两侧扩展，得到每个中心的最大半径。

时间最坏 $O(n^2)$，额外空间 $O(1)$。在 $n\le1000$ 的约束下，它证明短、常数小、边界清晰，是最佳实用解。

### Manacher

在字符间插入分隔符统一奇偶长度。维护当前最右回文区间 `[center-right, center+right]`，对落在区间内的新中心，先从镜像位置复用已知半径，再继续扩展。

最右边界每次只向右推进，总时间 $O(n)$、空间 $O(n)$。它达到读取输入的线性下界，但坐标换算和哨兵边界更易写错；只有约束需要或明确要求线性时优先。

## 正确性抓手

中心扩展的覆盖性来自：

1. 任意奇数回文有唯一字符中心；
2. 任意偶数回文有唯一字符间中心；
3. 固定中心从半径 0 单调扩张，直到第一次失配，恰好得到该中心最长回文；
4. 所有中心的最大值就是全局最大值。

扩展循环退出时两端已经越过合法回文，所以长度是 `right - left - 1`，起点是 `left + 1`。

## 约束变化

### 统计全部回文子串

每次中心扩展成功都唯一发现一个回文，直接累加成功次数，时间 $O(n^2)$、空间 $O(1)$。

### 最长回文子序列

字符可以跳过，中心不再能唯一覆盖选择。状态改为区间最优值：

$$
dp[l][r]=
\begin{cases}
dp[l+1][r-1]+2,&s_l=s_r,\\
\max(dp[l+1][r],dp[l][r-1]),&s_l\ne s_r.
\end{cases}
$$

时间、空间均为 $O(n^2)$。

### 在前面添加最少字符变成回文

问题转化为最长回文前缀。对 `s + "#" + reverse(s)` 求 KMP 前缀函数，末项就是最长回文前缀长度；把剩余后缀逆序加到前面，时间 $O(n)$。

## 易错检查

- 是否同时枚举奇中心和偶中心；
- 处理的是连续子串还是子序列；
- 并列最长答案是否有“最早”或字典序要求；
- 空串与单字符的初值是否正确；
- 字符单位是字节、码点还是用户可见字符；
- Manacher 的变换串半径如何映射回原串起点和长度。

## Reference

- [Manacher, “A New Linear-Time ‘On-Line’ Algorithm for Finding the Smallest Initial Palindrome of a String”](https://doi.org/10.1145/321892.321896)
- [LeetCode 5：最长回文子串](../problems/index.md#problem-lc-5)
