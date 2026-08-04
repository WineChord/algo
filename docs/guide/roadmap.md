# 学习路线

算法知识不是一条严格的直线，更像一张有依赖关系的图。下面的路线强调“先建立可运行的最小闭环，再逐层扩展”，每一阶段都应该同时包含概念、实现和题目。

## 阶段 0：建立解题闭环

先做到能够独立完成以下循环：

1. 读懂输入、输出、约束和样例。
2. 写出最直接的正确算法。
3. 计算时间与空间复杂度，判断能否通过。
4. 找到瓶颈并尝试优化。
5. 用极端数据验证边界。
6. 赛后把关键结论整理成自己的语言。

配套阅读：

- [解题方法](problem-solving.md)
- [复杂度分析](complexity.md)
- [竞赛 C++](cpp.md)
- [每日题目](../daily/index.md)：按日期复盘完整训练批次，再回到专题归纳可迁移模型。

## 阶段 1：基础工具箱

这一阶段的目标不是追求难题，而是让常见操作变成条件反射。

| 模块 | 必会内容 | 识别信号 |
| --- | --- | --- |
| 排序 | 比较排序、稳定性、自定义比较器 | 顺序不重要、相邻关系、离线处理 |
| [极值候选与 Top-K](../basics/top-k-extrema.md) | 固定变量、小根堆、可合并摘要 | 只需要少量候选、流式输入 |
| [乘积极值](../basics/pair-product-extrema.md) | 非负前二与[有符号双端候选](../basics/signed-product-extrema.md) | 目标对因子单调、负号改变候选 |
| 二分 | 边界查找、答案二分 | 单调性、最小可行值、最大合法值 |
| [序列扫描](../basics/sequence-invariants.md) | 局部窗口、补数哈希、双指针、双端结算 | 局部贡献、单调移动、唯一扩张起点 |
| [前缀与差分](../basics/prefix-sums-and-difference.md) | 前缀状态频次、区间事件 | 子数组统计、批量区间覆盖 |
| 位运算 | 掩码、lowbit、子集枚举 | 状态压缩、二进制性质 |

推荐练习：

--8<-- "includes/problems/lc-704.md"

--8<-- "includes/problems/lc-3.md"

--8<-- "includes/problems/lc-560.md"

--8<-- "includes/problems/lc-56.md"

--8<-- "includes/problems/lc-3536.md"

--8<-- "includes/problems/lc-1464.md"

--8<-- "includes/problems/lc-628.md"

## 阶段 2：数据结构与搜索

先掌握标准库能直接提供的结构，再学习需要手写维护信息的结构。

```text
数组 / 链表
├── 栈、队列、双端队列
├── 哈希表、集合
├── 堆、单调栈、单调队列
└── 树与图的 DFS / BFS
    ├── 并查集
    ├── Trie
    ├── 树状数组
    └── 线段树
```

学习每种结构时固定回答四个问题：

1. 它维护的抽象信息是什么？
2. 每个操作的复杂度是什么？
3. 不变量是什么？
4. 什么条件变化会让它不再适用？

配套专题：

- [搜索与枚举知识地图](../search/index.md)；
- [回溯：只展开仍可能完成的前缀](../search/backtracking.md)；
- [链表：指针不变量与局部接线](../data-structures/linked-lists.md)；
- [单调栈：等待未来关闭的边界](../data-structures/monotonic-stacks.md)；
- [单调队列：维护仍可能最优的窗口候选](../data-structures/monotonic-queues.md)；
- [哈希分组、滑动窗口与 LRU](../data-structures/hash-and-cache.md)。
- [二叉树遍历：顺序、边界与恢复](../graph/tree-traversals.md)。

## 阶段 3：动态规划、贪心与图论

这三个模块最能训练“从问题结构推导算法”的能力。

### 动态规划

从线性 DP、背包和区间 DP 开始。不要先背转移式，先说清：

- 状态包含了哪些足以决定未来的信息；
- 每个状态从哪些更小状态转移；
- 依赖关系是否构成有向无环图；
- 初值和非法状态如何表示。

固定阶状态的入门推导见[线性递推：从递归树到滚动状态](../dp/linear-recurrences.md)。

最长递增子序列、最长公共子序列、双序列前缀状态与路径恢复见[子序列与双序列动态规划](../dp/sequence-dp.md)。

字典切分、通配模式与前缀状态维度见[字符串动态规划：前缀可达与模式匹配](../dp/string-dp.md)。

零和轮流行动、分差状态与有限取法见[零和博弈动态规划](../dp/game-dp.md)。

移动方向、局部邻域、哨兵与滚动状态见[网格动态规划：方向、邻域与滚动状态](../dp/grid-dp.md)。

两端选择、最后切分与滚动方向见[区间动态规划：从两端选择到合并顺序](../dp/interval-dp.md)。

### 贪心

重点不是“选择当前最优”，而是证明这个选择不会损害全局最优。常见证明有交换论证、领先法、反证法和拟阵结构。

从便宜槽位分配、数位字典序到区间出边的 BFS 分层，见[贪心：交换论证、领先法与分层边界](../basics/greedy-exchange.md)。

### 图论

先把 DFS、BFS、拓扑排序和最短路练熟，再进入函数图、最小生成树、强连通分量、最近公共祖先和网络流。详见[图论知识地图](../graph/index.md)、[函数图：唯一后继、环与入口](../graph/functional-graphs.md)与 [0-1 权、二分图和操作奇偶](../graph/weighted-parity-states.md)。

树上子问题先于父问题的统一接口见[树上后序聚合](../graph/tree-aggregation.md)。

“每条路径都必须经过”的全称路径约束见[支配关系](../graph/dominators.md)。

## 阶段 4：专题化与比赛化

当基础算法能独立实现后，开始按题型做专题训练：

- 字符串匹配、字典树、字符串哈希、[表达式解析](../strings/expression-parsing.md)、[循环等价类](../strings/cyclic-normalization.md)、[回文重排](../strings/palindrome-rearrangements.md)与[回文中心](../strings/palindrome-centers.md)；
- 数论、[组合计数](../math/combinatorial-counting.md)、[排列排名](../math/permutation-ranking.md)、概率与期望；
- 树上问题、连通性、网络流；
- 状态压缩、数位 DP、优化 DP；
- 计算几何、多项式等进阶主题。

同时引入比赛节奏：

- **赛前**：检查模板、编译参数和常见整数范围。
- **赛中**：先通读，按“把握 × 收益 ÷ 时间”排序。
- **卡题**：回到小规模、特殊情形和暴力枚举寻找结构。
- **赛后**：补题时重做推导，不直接照抄题解。

## 如何判断“真正掌握”

一个算法至少通过四层检验：

1. **识别**：看到信号能想到候选算法。
2. **解释**：能从不变量或状态定义解释正确性。
3. **实现**：不看模板可以稳定写出。
4. **迁移**：约束变化后能判断原解法是否仍成立。

!!! warning "不要用题量代替复盘"

    十道只记住答案的题，通常不如两道能讲清模型、证明、边界和变种的题。题量有价值，但前提是每道题都在扩展或加固知识图谱。

## Reference

- [Introduction to Algorithms, Fourth Edition — MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [CSES Problem Set](https://cses.fi/problemset/)
