---
hide:
  - navigation
  - toc
---

<div class="algo-hero" markdown>
<div class="algo-kicker">Algorithm · Contest · Reasoning</div>
# 把每道题，变成可复用的能力

从约束出发，先得到可靠的朴素解，再沿着重复计算、状态冗余与数据结构瓶颈逐步优化。这里不只收藏代码，更关心<strong>为什么想到、为什么正确、什么时候还能再用</strong>。

[开始学习](guide/roadmap.md){ .md-button .md-button--primary }
[浏览题解](problems/index.md){ .md-button }
</div>

## 知识地图

<div class="algo-grid" markdown>
<a class="algo-card" href="guide/problem-solving/">
<strong>解题方法</strong>
<span>读约束、建模、暴力、优化、证明、实现与测试。</span>
</a>
<a class="algo-card" href="basics/">
<strong>基础技巧</strong>
<span>排序、二分、双指针、前缀和、差分与位运算。</span>
</a>
<a class="algo-card" href="data-structures/">
<strong>数据结构</strong>
<span>栈队列、堆、并查集、树状数组、线段树与平衡树。</span>
</a>
<a class="algo-card" href="graph/">
<strong>图论</strong>
<span>遍历、最短路、拓扑序、生成树、连通性与网络流。</span>
</a>
<a class="algo-card" href="dp/">
<strong>动态规划</strong>
<span>状态设计、转移依赖、空间优化与常见模型。</span>
</a>
<a class="algo-card" href="math/">
<strong>数学</strong>
<span>数论、组合计数、概率、矩阵与多项式。</span>
</a>
<a class="algo-card" href="strings/">
<strong>字符串</strong>
<span>KMP、Trie、字符串哈希、AC 自动机与后缀结构。</span>
</a>
<a class="algo-card" href="problems/">
<strong>题解索引</strong>
<span>按平台、难度、核心技巧与变种关系组织题目。</span>
</a>
</div>

## 一道题真正值得留下什么

=== "思路"

    从输入规模和题目结构推导算法。记录朴素解为何成立、瓶颈在哪里，以及每一步优化消除了什么成本。

=== "证明"

    明确不变量、贪心交换论证或动态规划的无后效性。代码通过样例不等于算法正确。

=== "实现"

    保留可以在比赛中稳定写出的 C++，写清边界、整数范围与复杂度，避免为了短而短。

=== "迁移"

    把追问和变种接到同一知识节点：条件改变后，原算法在哪里失效，又该换成什么模型。

!!! tip "推荐入口"

    第一次来可以先读[解题方法](guide/problem-solving.md)，再完成[二分查找](basics/binary-search.md)专题。前者给出统一的推理流程，后者展示如何把流程落实成可证明、可复用的模板。

## 核心约定

- **先约束，后算法**：\(n\) 的数量级往往比题目故事更诚实。
- **先正确，后更快**：朴素解既是思考起点，也是随机对拍时的答案生成器。
- **模板服务于不变量**：背代码之前，先能解释每个区间和每次更新的含义。
- **复杂度写全**：同时考虑时间、额外空间、预处理和多次询问。
- **边界主动构造**：空集、单元素、全相等、严格单调、极值和溢出都应进入测试。

> 算法学习的目标不是记住尽可能多的代码，而是让陌生问题逐渐落入熟悉的结构。
