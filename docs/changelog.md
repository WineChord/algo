# 更新日志

## 2026-08-20

### 每日训练档案

- 新增 [2026-08-20 每日 5 题](daily/2026-08-20/index.md)：[AtCoder ARC227 D](problems/index.md#problem-atcoder-arc227-d)、[力扣 Top 140](problems/index.md#problem-lc-199)、[力扣第 515 场周赛 Q3](problems/index.md#problem-lc-4026)、[Codeforces Round 1117 Div.2 C](problems/index.md#problem-codeforces-2257-c) 与 [LC 3069](problems/index.md#problem-lc-3069)。

### 二坐标见证、极端拼接与树上观测

- 新增[多数闭包](math/majority-closure.md)，把指数生成过程压缩为二坐标共同见证定理，并给出位集冲突图实现与适用边界。
- 扩充[贪心交换](basics/greedy-exchange.md)与[序列扫描](basics/sequence-invariants.md)，加入最早前缀和最晚后缀的可达拼接，以及实时末元素驱动的最小充分状态。
- 扩充[二叉树遍历](graph/tree-traversals.md)与[树上聚合](graph/tree-aggregation.md)，补入观察方向优先的逐层首次到达，以及删边连通块诱导观测等价类的紧下界构造。

### 权威题目条目

- 新增 [ARC227 D](problems/index.md#problem-atcoder-arc227-d)、[LC 199](problems/index.md#problem-lc-199)、[LC 4026](problems/index.md#problem-lc-4026)、[CF 2257C](problems/index.md#problem-codeforces-2257-c) 与 [LC 3069](problems/index.md#problem-lc-3069) 的唯一折叠条目。

## 2026-08-19

### 每日训练档案

- 新增 [2026-08-19 每日 5 题](daily/2026-08-19/index.md)：[AtCoder ARC227 C](problems/index.md#problem-atcoder-arc227-c)、[力扣 Top 139](problems/index.md#problem-lc-79)、[力扣第 515 场周赛 Q2](problems/index.md#problem-lc-4025)、[Codeforces Round 1117 Div.2 B](problems/index.md#problem-codeforces-2257-b) 与 [LC 1386](problems/index.md#problem-lc-1386)。

### 周期同余类、可撤销路径与稀疏异常

- 扩充[字符串](strings/index.md)，把最小周期从静态重复判定推进到圆环合并过程的不可合并同余类与可达构造。
- 扩充[回溯](search/backtracking.md)与[序列扫描](basics/sequence-invariants.md)，加入网格简单路径的原地撤销状态，以及无容量独立选择下的支配极值压缩。
- 扩充[博弈动态规划](dp/game-dp.md)与[哈希滑动窗口](data-structures/hash-and-cache.md)，补入强制过程的耐久望远镜和“规则基线加稀疏异常修正”模型。

### 权威题目条目

- 新增 [ARC227 C](problems/index.md#problem-atcoder-arc227-c)、[LC 79](problems/index.md#problem-lc-79)、[LC 4025](problems/index.md#problem-lc-4025)、[CF 2257B](problems/index.md#problem-codeforces-2257-b) 与 [LC 1386](problems/index.md#problem-lc-1386) 的唯一折叠条目。

## 2026-08-18

### 每日训练档案

- 新增 [2026-08-18 每日 5 题](daily/2026-08-18/index.md)：[AtCoder ARC227 B](problems/index.md#problem-atcoder-arc227-b)、[力扣 Top 138](problems/index.md#problem-lc-459)、[力扣第 515 场周赛 Q1](problems/index.md#problem-lc-4024)、[Codeforces Round 1117 Div.2 A](problems/index.md#problem-codeforces-2257-a) 与 [LC 3471](problems/index.md#problem-lc-3471)。

### 强制引入、周期边界与能力闭包

- 扩充[序列扫描](basics/sequence-invariants.md)，加入唯一首次引入时刻、强制事件优先与 LIFO 暂存构造。
- 扩充[字符串](strings/index.md)，补齐 KMP 最长 border 到完整周期的整除条件，以及新缩写不扩大首字母能力集合的闭包不变量。
- 扩充[极值候选](basics/top-k-extrema.md)与[哈希滑动窗口](data-structures/hash-and-cache.md)，加入可行性过滤后的稳定 `argmin`，以及位置到窗口起点区间的覆盖计数。

### 权威题目条目

- 新增 [ARC227 B](problems/index.md#problem-atcoder-arc227-b)、[LC 4024](problems/index.md#problem-lc-4024)、[CF 2257A](problems/index.md#problem-codeforces-2257-a) 与 [LC 3471](problems/index.md#problem-lc-3471) 的唯一折叠条目；校正并复用 [LC 459](problems/index.md#problem-lc-459) 的权威实现。

## 2026-08-17

### 每日训练档案

- 新增 [2026-08-17 每日 5 题](daily/2026-08-17/index.md)：[AtCoder ARC227 A](problems/index.md#problem-atcoder-arc227-a)、[力扣 Top 137](problems/index.md#problem-lc-516)、[力扣第 514 场周赛 Q4](problems/index.md#problem-lc-4017)、[Codeforces Round 1116 Div.1 D / Div.2 F](problems/index.md#problem-codeforces-2256-f) 与 [LC 1563](problems/index.md#problem-lc-1563)。

### 稳定中位数、动态峰贡献与单调切分

- 扩充[贪心交换](basics/greedy-exchange.md)，加入稳定匹配后的逐坐标中位数，以及二次幂超递增容量下的最大剩余需求交换证明。
- 扩充[序列扫描](basics/sequence-invariants.md)，把局部峰判定推进到“首个内部峰唯一归属 + 相邻峰距离动态聚合”。
- 扩充[回文专题](strings/palindrome-centers.md)与[区间动态规划](dp/interval-dp.md)，加入最长回文子序列的一维时间层，以及正值切分中的单调分界和双向候选最大值。

### 权威题目条目

- 新增 [ARC227 A](problems/index.md#problem-atcoder-arc227-a)、[LC 516](problems/index.md#problem-lc-516)、[LC 4017](problems/index.md#problem-lc-4017)、[CF 2256F / 2255D](problems/index.md#problem-codeforces-2256-f) 与 [LC 1563](problems/index.md#problem-lc-1563) 的唯一折叠条目。

## 2026-08-16

### 每日训练档案

- 新增 [2026-08-16 每日 5 题](daily/2026-08-16/index.md)：[AtCoder ARC226 E](problems/index.md#problem-atcoder-arc226-e)、[力扣 Top 136](problems/index.md#problem-lc-118)、[力扣第 514 场周赛 Q3](problems/index.md#problem-lc-4016)、[Codeforces Round 1116 Div.1 C / Div.2 E](problems/index.md#problem-codeforces-2256-e) 与 [LC 2029](problems/index.md#problem-lc-2029)。

### 仿射特征、精确延迟与几何分割

- 扩充[模构造](math/modular-constructions.md)，加入模重心在仿射变换与反色下的协变性、交换存在性证明，以及 Rule 90 的幂零延迟线与二维边界契约。
- 扩充[组合计数](math/combinatorial-counting.md)，补入杨辉三角递推、输出规模下界及其与乘法公式的适用边界。
- 扩充[网格动态规划](dp/grid-dp.md)与[博弈动态规划](dp/game-dp.md)，加入不相交轴对齐形状的分割线完备性，以及非标准立即失败终局下的模 3 强制序列分类。

### 权威题目条目

- 新增 [ARC226 E](problems/index.md#problem-atcoder-arc226-e)、[LC 118](problems/index.md#problem-lc-118)、[LC 4016](problems/index.md#problem-lc-4016)、[CF 2256E / 2255C](problems/index.md#problem-codeforces-2256-e) 与 [LC 2029](problems/index.md#problem-lc-2029) 的唯一折叠条目。

## 2026-08-15

### 每日训练档案

- 新增 [2026-08-15 每日 5 题](daily/2026-08-15/index.md)：[AtCoder ARC226 D](problems/index.md#problem-atcoder-arc226-d)、[力扣 Top 135](problems/index.md#problem-lc-85)、[力扣第 514 场周赛 Q2](problems/index.md#problem-lc-4015)、[Codeforces Round 1116 Div.1 B / Div.2 D](problems/index.md#problem-codeforces-2256-d) 与 [LC 3702](problems/index.md#problem-lc-3702)。

### 分层归并、二维边界与组成计数

- 扩充[数据结构知识地图](data-structures/index.md)，补入受限 FIFO 接口下的分层稳定归并、基数选择与移动次数摊还证明。
- 扩充[单调栈](data-structures/monotonic-stacks.md)与[树上聚合](graph/tree-aggregation.md)，加入二维矩阵逐行柱状图迁移，以及全局树高与逐点深度需要分阶段计算的边界。
- 扩充[组合计数](math/combinatorial-counting.md)与[异或代数](math/index.md)，补入固定 run 骨架上的两组正整数组成，以及总异或为零时删除一个元素的三分结论。

### 权威题目条目

- 新增 [ARC226 D](problems/index.md#problem-atcoder-arc226-d)、[LC 85](problems/index.md#problem-lc-85)、[LC 4015](problems/index.md#problem-lc-4015)、[CF 2256D / 2255B](problems/index.md#problem-codeforces-2256-d) 与 [LC 3702](problems/index.md#problem-lc-3702) 的唯一折叠条目。

## 2026-08-14

### 每日训练档案

- 新增 [2026-08-14 每日 5 题](daily/2026-08-14/index.md)：[AtCoder ARC226 C](problems/index.md#problem-atcoder-arc226-c)、[力扣 Top 134](problems/index.md#problem-lc-509)、[力扣第 514 场周赛 Q1](problems/index.md#problem-lc-4014)、[Codeforces Round 1116 Div.1 A / Div.2 C](problems/index.md#problem-codeforces-2256-c) 与 [LC 3090](problems/index.md#problem-lc-3090)。

### 偶性上界、乘法交换与末轮值函数

- 扩充[模构造](math/modular-constructions.md)，加入从行列偶性上界到奇数正方形递归构造的完整路径。
- 扩充[线性递推](dp/linear-recurrences.md)与[贪心交换](basics/greedy-exchange.md)，补入同递推不同基例的下标语义，以及大折扣匹配大价格的乘法交换证明。
- 扩充[博弈动态规划](dp/game-dp.md)与[哈希滑动窗口](data-structures/hash-and-cache.md)，补入末轮值函数诱导的早轮鞍点，以及固定字符集下的逐值频次窗口。

### 权威题目条目

- 新增 [ARC226 C](problems/index.md#problem-atcoder-arc226-c)、[LC 509](problems/index.md#problem-lc-509)、[LC 4014](problems/index.md#problem-lc-4014)、[CF 2256C / 2255A](problems/index.md#problem-codeforces-2256-c) 与 [LC 3090](problems/index.md#problem-lc-3090) 的唯一折叠条目。

## 2026-08-13

### 每日训练档案

- 新增 [2026-08-13 每日 5 题](daily/2026-08-13/index.md)：[AtCoder ARC226 B](problems/index.md#problem-atcoder-arc226-b)、[力扣 Top 133](problems/index.md#problem-lc-162)、[力扣第 188 场双周赛 Q4](problems/index.md#problem-lc-4009)、[Codeforces Round 1116 Div.2 B](problems/index.md#problem-codeforces-2256-b) 与 [LC 2213](problems/index.md#problem-lc-2213)。

### 尺度下界、相对时间与可合并摘要

- 扩充[贪心交换](basics/greedy-exchange.md)，加入整除重量链上的逐尺度容量下界及其同时充分性边界。
- 扩充[二分查找](basics/binary-search.md)与[动态规划](dp/index.md)，补入非单调函数上的坡向存在性二分，以及双机调度中消去绝对时钟的相对忙碌状态。
- 扩充[数据结构](data-structures/index.md)与[字符串](strings/index.md)，补入最长同字符段的可合并线段树摘要，以及消去共享中项后得到的隔位约束与四周期候选。

### 权威题目条目

- 新增 [ARC226 B](problems/index.md#problem-atcoder-arc226-b)、[LC 162](problems/index.md#problem-lc-162)、[LC 4009](problems/index.md#problem-lc-4009)、[CF 2256B](problems/index.md#problem-codeforces-2256-b) 与 [LC 2213](problems/index.md#problem-lc-2213) 的唯一折叠条目。

## 2026-08-12

### 每日训练档案

- 新增 [2026-08-12 每日 5 题](daily/2026-08-12/index.md)：[AtCoder ARC226 A](problems/index.md#problem-atcoder-arc226-a)、[力扣 Top 132](problems/index.md#problem-lc-18)、[力扣第 188 场双周赛 Q3](problems/index.md#problem-lc-4008)、[Codeforces Round 1116 Div.2 A](problems/index.md#problem-codeforces-2256-a) 与 [LC 2958](problems/index.md#problem-lc-2958)。

### 区间图、顺序下界与窗口频次

- 扩充[奇偶状态图](graph/weighted-parity-states.md)，加入区间重叠图在最大活跃数为 2 时的森林结构，以及扫描连通分量计数二染色的推导。
- 扩充[序列扫描](basics/sequence-invariants.md)、[前缀状态](basics/prefix-sums-and-difference.md)与[哈希滑动窗口](data-structures/hash-and-cache.md)，补入四数和分层去重、一步进入单调闭包、差分增强后的顺序资源下界和逐值频次上限。

### 权威题目条目

- 新增 [ARC226 A](problems/index.md#problem-atcoder-arc226-a)、[LC 18](problems/index.md#problem-lc-18)、[LC 4008](problems/index.md#problem-lc-4008)、[CF 2256A](problems/index.md#problem-codeforces-2256-a) 与 [LC 2958](problems/index.md#problem-lc-2958) 的唯一折叠条目。

## 2026-08-11

### 每日训练档案

- 新增 [2026-08-11 每日 5 题](daily/2026-08-11/index.md)：[AtCoder ABC469 G](problems/index.md#problem-atcoder-abc469-g)、[力扣 Top 131](problems/index.md#problem-lc-63)、[力扣第 188 场双周赛 Q2](problems/index.md#problem-lc-4007)、[Codeforces Round 1113 Div.2 G](problems/index.md#problem-codeforces-2248-g) 与 [LC 2996](problems/index.md#problem-lc-2996)。
- 日期档案兼容历史 14 题与新的 5 题账目；两种结构共享同一规范正文、权威题目片段和专题入口。

### 群递推、阈值可达与互补频次

- 扩充[线性递推](dp/linear-recurrences.md)，加入二面体群消元、周期方向与周期系数矩阵的推导路径。
- 扩充[动态规划](dp/index.md)与[网格动态规划](dp/grid-dp.md)，补入净增益阈值下的 DAG/gcd 分层，以及障碍清零与一维状态时间层。
- 扩充[哈希分组](data-structures/hash-and-cache.md)与[序列扫描](basics/sequence-invariants.md)，补入互补频次的独立贡献判据，以及顺序前缀边界与全局缺失值的两阶段模型。

### 权威题目条目

- 新增 [ABC469 G](problems/index.md#problem-atcoder-abc469-g)、[LC 63](problems/index.md#problem-lc-63)、[LC 4007](problems/index.md#problem-lc-4007)、[CF 2248G](problems/index.md#problem-codeforces-2248-g) 与 [LC 2996](problems/index.md#problem-lc-2996) 的唯一折叠条目。

## 2026-08-09

### 每日训练档案

- 新增 [2026-08-09 每日 14 题](daily/2026-08-09/index.md)，依次覆盖 [AtCoder ABC469 F](problems/index.md#problem-atcoder-abc469-f)、力扣 Top 121–130、[第 188 场双周赛 Q1](problems/index.md#problem-lc-4006)、[Codeforces Round 1113 Div.2 F](problems/index.md#problem-codeforces-2248-f) 与 [LC 1140](problems/index.md#problem-lc-1140)。
- AtCoder 与 Codeforces 页面保留自包含英文题面层，随后进入中文解释、算法递进、证明与变种；其余页面正文统一使用中文。

### 隐式边层、窗口预算与可撤销路径状态

- 扩充[图论](graph/index.md)，用按公约数降序的隐式边层与并查集模拟完全图上的最大生成树，避免显式生成平方级边集。
- 扩充[前缀状态](basics/prefix-sums-and-difference.md)、[哈希与滑动窗口](data-structures/hash-and-cache.md)、[回溯](search/backtracking.md)、[链表接线](data-structures/linked-lists.md)、[线性递推](dp/linear-recurrences.md)、[字符串](strings/index.md)、[树上聚合](graph/tree-aggregation.md)与[博弈动态规划](dp/game-dp.md)，补入除自身聚合、预算窗口、有限值域集合、固定段切分、循环位移、带代价台阶、周期坐标、根路径前缀撤销与动态动作上限。
- 扩充[序列扫描](basics/sequence-invariants.md)与[贪心交换](basics/greedy-exchange.md)，补入可重排交替序列的前缀平衡判据，以及全局操作逐点支配局部操作的适用边界。

### 权威题目条目

- 新增 [ABC469 F](problems/index.md#problem-atcoder-abc469-f)、[CF 2248F](problems/index.md#problem-codeforces-2248-f)、[LC 4006](problems/index.md#problem-lc-4006)、[LC 1140](problems/index.md#problem-lc-1140) 与力扣 Top 121–130 的唯一折叠条目；校正并复用 [LC 295](problems/index.md#problem-lc-295) 的权威实现。

## 2026-08-06

### 每日训练档案

- 新增 [2026-08-06 每日 14 题](daily/2026-08-06/index.md)，依次覆盖 [AtCoder ABC469 E](problems/index.md#problem-atcoder-abc469-e)、力扣 Top 111–120、[第 513 场周赛 Q4](problems/index.md#problem-lc-4013)、[Codeforces Round 1113 Div.2 E](problems/index.md#problem-codeforces-2248-e) 与 [LC 3345](problems/index.md#problem-lc-3345)。
- AtCoder 与 Codeforces 页面保留自包含英文题面层，随后进入中文解释、算法递进、证明与变种；其余页面正文统一使用中文。

### 可恢复摘要、前缀序与周期分解

- 新增[增广栈](data-structures/augmented-stacks.md)，从“每层即一个版本”推导不可逆聚合、双栈队列与持久化边界。
- 扩充[二分查找](basics/binary-search.md)、[序列扫描](basics/sequence-invariants.md)、[贪心交换](basics/greedy-exchange.md)、[链表接线](data-structures/linked-lists.md)、[函数图](graph/functional-graphs.md)、[回溯](search/backtracking.md)、[字符串动态规划](dp/string-dp.md)、[前缀状态](basics/prefix-sums-and-difference.md)与[数学](math/index.md)，补入区间比率、三次翻转、矩阵内嵌标记、相邻正收益、环入口、拉链重排、子集树、固定宽度解码、动态秩统计、周期奖励与数位积零边界。

### 权威题目条目

- 新增 [ABC469 E](problems/index.md#problem-atcoder-abc469-e)、[CF 2248E](problems/index.md#problem-codeforces-2248-e)、[LC 4013](problems/index.md#problem-lc-4013)、[LC 3345](problems/index.md#problem-lc-3345) 与力扣 Top 111–120 的唯一折叠条目。

## 2026-08-05

### 每日训练档案

- 新增 [2026-08-05 每日 14 题](daily/2026-08-05/index.md)，依次覆盖 [AtCoder ABC469 D](problems/index.md#problem-atcoder-abc469-d)、力扣 Top 101–110、[第 513 场周赛 Q3](problems/index.md#problem-lc-4012)、[Codeforces Round 1113 Div.2 D](problems/index.md#problem-codeforces-2248-d) 与 [LC 3310](problems/index.md#problem-lc-3310)。
- AtCoder 与 Codeforces 页面保留自包含英文题面层，随后进入中文解释、算法递进、证明与变种；其余页面正文统一使用中文。

### 函数图、单调栈与边界定位

- 新增[函数图](graph/functional-graphs.md)，统一唯一后继轨迹中的尾、环、入口、Floyd、拓扑删点与多次后继查询。
- 新增[单调栈](data-structures/monotonic-stacks.md)，从等待未来边界的候选语义推导摊还复杂度、严格性与柱状图面积。
- 扩充[图论](graph/index.md)、[二分查找](basics/binary-search.md)、[链表接线](data-structures/linked-lists.md)、[回文中心](strings/palindrome-centers.md)、[极值候选](basics/top-k-extrema.md)、[序列扫描](basics/sequence-invariants.md)、[字符串](strings/index.md)与[贪心交换](basics/greedy-exchange.md)，补入可达闭包、二元顶点覆盖、整数平方根、循环任务定位、区间反转、频率桶、异值抵消、拼接比较与四类计数不等式。

### 权威题目条目

- 新增 [ABC469 D](problems/index.md#problem-atcoder-abc469-d)、[CF 2248D](problems/index.md#problem-codeforces-2248-d)、[LC 4012](problems/index.md#problem-lc-4012)、[LC 3310](problems/index.md#problem-lc-3310) 与力扣 Top 101–110 的唯一折叠条目。

## 2026-08-04

### 每日训练档案

- 新增 [2026-08-04 每日 14 题](daily/2026-08-04/index.md)，依次覆盖 [AtCoder ABC469 C](problems/index.md#problem-atcoder-abc469-c)、力扣 Top 91–100、[第 513 场周赛 Q2](problems/index.md#problem-lc-4011)、[Codeforces Round 1113 Div.2 C](problems/index.md#problem-codeforces-2248-c) 与 [LC 3731](problems/index.md#problem-lc-3731)。
- AtCoder 与 Codeforces 页面保留自包含英文题面层，并在明确边界后进入中文解释、推导、证明与变种；其余页面正文统一使用中文。

### 单调扫描、逐位算术与可合并摘要

- 扩充[序列扫描](basics/sequence-invariants.md)，把绝对值两端极值、固定首项双指针、有限值域输出和第 $k$ 个阈值事件纳入同一条“每步永久定稿”读者路径。
- 扩充[字符串](strings/index.md)、[二叉树遍历](graph/tree-traversals.md)、[树上后序聚合](graph/tree-aggregation.md)与[链表接线](data-structures/linked-lists.md)，补齐逐位加乘、镜像与深度、树直径及双向哨兵。
- 扩充[前缀状态](basics/prefix-sums-and-difference.md)、[序列动态规划](dp/sequence-dp.md)与[数学](math/index.md)，补入比例约束的前缀序统计、动态删除的原序列分块及乘加前溢出门禁。

### 权威题目条目

- 新增 [ABC469 C](problems/index.md#problem-atcoder-abc469-c)、[CF 2248C](problems/index.md#problem-codeforces-2248-c)、[LC 4011](problems/index.md#problem-lc-4011)、[LC 3731](problems/index.md#problem-lc-3731) 与力扣 Top 91–100 的唯一折叠条目。

## 2026-08-03

### 每日训练档案

- 新增 [2026-08-03 每日 14 题](daily/2026-08-03/index.md)，依次覆盖 [AtCoder ABC469 B](problems/index.md#problem-atcoder-abc469-b)、力扣 Top 81–90、[第 513 场周赛 Q1](problems/index.md#problem-lc-4010)、[Codeforces Round 1113 Div.2 B](problems/index.md#problem-codeforces-2248-b) 与 [LC 1406](problems/index.md#problem-lc-1406)。
- AtCoder 与 Codeforces 题目均在完整英文题面层之后明确切换到中文解释与题解；全部页面复用同一规范源、完整 C++ 与稳定专题入口。

### 字符串状态、零和博弈与局部不变量

- 新增[字符串动态规划](dp/string-dp.md)，统一字典切分的一维可达前缀、模式匹配的二维前缀状态及路径恢复边界。
- 新增[零和博弈动态规划](dp/game-dp.md)，用当前行动者最大分差统一有限取法与极大极小递推，并明确滚动状态和区间博弈的边界。
- 扩充[序列扫描](basics/sequence-invariants.md)、[贪心交换](basics/greedy-exchange.md)、[排列排名](math/permutation-ranking.md)、[链表接线](data-structures/linked-lists.md)、[树遍历](graph/tree-traversals.md)、[数学](math/index.md)与[字符串](strings/index.md)，补入哨兵窗口、单侧下界、见证规范化、字典序后继、迭代归并、严格中序、异或抵消与局部记号解释。

### 权威题目条目

- 新增 [ABC469 B](problems/index.md#problem-atcoder-abc469-b)、[CF 2248B](problems/index.md#problem-codeforces-2248-b)、[LC 4010](problems/index.md#problem-lc-4010)、[LC 1406](problems/index.md#problem-lc-1406) 与力扣 Top 81–90 的唯一折叠条目。

## 2026-08-02

### 每日训练档案

- 新增 [2026-08-02 每日 14 题](daily/2026-08-02/index.md)，覆盖 [AtCoder ABC469 A](problems/index.md#problem-atcoder-abc469-a)、力扣 Top 71–80、[第 512 场周赛 Q4](problems/index.md#problem-lc-4003)、[Codeforces Round 1113 Div.2 A](problems/index.md#problem-codeforces-2248-a) 与 [LC 877](problems/index.md#problem-lc-877)。

### 网格状态、解析上下文与不变量

- 新增[网格动态规划](dp/grid-dp.md)，统一从移动方向、局部邻域、哨兵和滚动顺序推导最小路径和与最大正方形，并明确何时必须转向图最短路。
- 扩充[奇偶状态图](graph/weighted-parity-states.md)、[区间动态规划](dp/interval-dp.md)、[表达式解析](strings/expression-parsing.md)、[链表接线](data-structures/linked-lists.md)与[二叉树遍历](graph/tree-traversals.md)，补入行动奇偶、强不变量、嵌套解码、固定间距和中序祖先栈。
- 在[基础技巧](basics/index.md)、[序列扫描](basics/sequence-invariants.md)、[贪心交换](basics/greedy-exchange.md)、[动态规划](dp/index.md)与[字符串](strings/index.md)中自然补强排序取舍、双向编号、字典序删除、完全背包、Trie 与双序列交织。

### 权威题目条目

- 新增 [ABC469 A](problems/index.md#problem-atcoder-abc469-a)、[LC 912](problems/index.md#problem-lc-912)、[LC 322](problems/index.md#problem-lc-322)、[LC 64](problems/index.md#problem-lc-64)、[LC 394](problems/index.md#problem-lc-394)、[LC 19](problems/index.md#problem-lc-19)、[LC 221](problems/index.md#problem-lc-221)、[LC 1768](problems/index.md#problem-lc-1768)、[LC 94](problems/index.md#problem-lc-94)、[LC 4003](problems/index.md#problem-lc-4003)、[CF 2248A](problems/index.md#problem-codeforces-2248-a) 与 [LC 877](problems/index.md#problem-lc-877) 的唯一折叠条目。
- 校正并复用 [LC 34](problems/index.md#problem-lc-34) 与 [LC 208](problems/index.md#problem-lc-208) 的权威实现，避免专题与训练档案维护分叉。

## 2026-08-01

### 每日训练档案

- 新增 [2026-08-01 每日题目](daily/2026-08-01/index.md)，按 AtCoder、力扣 Top 61–70、力扣第 512 场周赛、Codeforces Round 1111 与力扣每日一题的固定顺序收录 14 道完整题解。
- [AtCoder ABC468 G](problems/index.md#problem-atcoder-abc468-g) 提供独立组织的自包含英文题面层，[Codeforces 2247 F](problems/index.md#problem-codeforces-2247-f) 按官方材料许可呈现完整英文题面；两者之后的解释、证明、复杂度与变种均进入中文题解层。
- 每道页面继续复用同一规范源与 canonical C++，并提供官方题目、稳定专题、当日列表和前后题导航。

### 计数、解析、树遍历与区间状态

- 新增[组合计数](math/combinatorial-counting.md)，把隔板法、补集、奇偶代换、唯一第一事件与块收缩乘法组织成一条可迁移推导路径。
- 新增[二叉树遍历与恢复](graph/tree-traversals.md)、[表达式解析](strings/expression-parsing.md)与[区间动态规划](dp/interval-dp.md)，补齐层边界、遍历唯一性、括号上下文、行动者净优势和滚动方向。
- 新增[支配关系](graph/dominators.md)，区分存在路径与全称路径约束，并说明 DAG 中由前驱 LCA 构造支配树以及双向支配刻画路径签名的方法。
- 扩充[链表局部接线](data-structures/linked-lists.md)与[序列扫描](basics/sequence-invariants.md)，加入结构内临时映射、后半反转恢复、值到槽位的循环置换、有序稳定压缩与二维坐标置换。

### 权威题目条目

- 收录 [AtCoder ABC468 G](problems/index.md#problem-atcoder-abc468-g)、[CF Round 1111 Div.2 F（2247F）](problems/index.md#problem-codeforces-2247-f)、[第 512 场周赛 Q3](problems/index.md#problem-lc-4002) 与 [LeetCode 486](problems/index.md#problem-lc-486)。
- 收录 LeetCode Top 61–70 的十个连续权威题目条目；全部最优实现采用两空格缩进，并与日期档案共享算法结论。

## 2026-07-31

### 每日训练档案

- 新增 [2026-07-31 每日题目](daily/2026-07-31/index.md)，按 AtCoder、力扣 Top 51–60、力扣第 512 场周赛、Codeforces Round 1111 与力扣每日一题的固定顺序收录 14 道完整题解。
- [AtCoder ABC468 F](problems/index.md#problem-atcoder-abc468-f) 在页内提供模型独立组织的自包含英文题面层，[Codeforces 2247 E](problems/index.md#problem-codeforces-2247-e) 按官方材料许可呈现完整英文题面；两者随后均紧接中文解释与中文题解。
- 每道页面保留官方题目、知识专题、当日列表和前后题导航，公式与完整 C++ 在桌面及窄屏下均可直接阅读。

### 单调结构、回溯与局部接线

- 扩充[二分查找](basics/binary-search.md)，把旋转数组、二维单调矩阵与下界插入统一为“每步永久排除不可能区域”的边界证明。
- 扩充[贪心交换](basics/greedy-exchange.md)、[子序列动态规划](dp/sequence-dp.md)、[回溯](search/backtracking.md)、[滑动窗口](data-structures/hash-and-cache.md)与[链表局部接线](data-structures/linked-lists.md)，补齐可达前缀、加权槽位、前缀最大值与 LIS、预处理合法区间、三类攻击线和两两换边。
- 在[序列扫描](basics/sequence-invariants.md)加入有序时间流的最近状态归并，在[图论知识地图](graph/index.md)加入先刻画可行区间、再用固定步长连续覆盖的树构造方法。

### 权威题目条目

- 收录 [AtCoder ABC468 F](problems/index.md#problem-atcoder-abc468-f)、[CF Round 1111 Div.2 E（2247E）](problems/index.md#problem-codeforces-2247-e)、[第 512 场周赛 Q2](problems/index.md#problem-lc-4001) 与 [LeetCode 3016](problems/index.md#problem-lc-3016)。
- 收录 LeetCode Top 51–60 的十个连续权威题目条目；全部最优实现采用两空格缩进，并与日期档案复用同一题意和算法结论。

## 2026-07-30

### 每日训练档案

- 新增 [2026-07-30 每日题目](daily/2026-07-30/index.md)，按 AtCoder、力扣 Top 41–50、力扣第 512 场周赛、Codeforces Round 1111 与力扣每日一题的固定顺序收录 14 道完整题解。
- [AtCoder ABC468 E](problems/index.md#problem-atcoder-abc468-e) 与 [Codeforces 2247 D2](problems/index.md#problem-codeforces-2247-d2) 在页内提供自包含英文题面层和紧接其后的中文解释；其余题目以及所有算法分析、证明、复杂度、易错点和变种统一使用中文。
- 每道页面保留可点击的官方题目、对应知识专题、当日列表和前后题导航，并在移动端继续默认自动折行完整 C++。

### 贪心、子序列与可合并摘要

- 新增[贪心与交换论证](basics/greedy-exchange.md)专题，把便宜槽位分配、数位字典序和连续区间 BFS 分层归纳为交换论证、领先法与层边界三类证明。
- 将原双序列页面扩展为[子序列与双序列动态规划](dp/sequence-dp.md)，从最长递增子序列的最小末尾值推进到最长公共子序列、编辑距离、空间压缩与方案恢复。
- 扩充[树上后序聚合](graph/tree-aggregation.md)、[链表局部接线](data-structures/linked-lists.md)、[序列扫描](basics/sequence-invariants.md)、[数据结构](data-structures/index.md)与[数学](math/index.md)，补齐单支返回与双支闭合、交换起点、正数窗口、二进制块线段树和交换求和。

### 权威题目条目

- 收录 [AtCoder ABC468 E](problems/index.md#problem-atcoder-abc468-e)、[CF Round 1111 Div.2 D2（2247D2）](problems/index.md#problem-codeforces-2247-d2)和[第 512 场周赛 Q1](problems/index.md#problem-lc-4000)。
- 收录 [LeetCode 3014](problems/index.md#problem-lc-3014)，以及 [LeetCode Top 41–50](problems/index.md) 的十个连续权威题目条目；全部最优实现采用两空格缩进，并与日期档案复用同一题意和算法结论。

## 2026-07-29

### 代码阅读

- 全站代码块默认自动换行，长行在桌面与手机上都保持在正文宽度内；每个代码块提供“自动换行”开关，可切换为保留原始长行并仅在代码块内部横向滚动。
- 换行偏好会在页面间保留，并兼容即时导航、键盘操作、复制按钮和无 JavaScript 时的默认换行布局。

### 每日训练档案

- 新增[每日题目](daily/index.md)，在按算法模型组织的知识专题之外，提供按工作日期回看完整训练批次的独立入口。
- 回填 [2026-07-26](daily/2026-07-26/index.md)、[2026-07-27](daily/2026-07-27/index.md)、[2026-07-28](daily/2026-07-28/index.md) 和 [2026-07-29](daily/2026-07-29/index.md) 共 56 道完整题解；日期按新到旧排列，每道题保留官方信息、解法递进、证明、完整 C++、变种与专题入口。
- 竞赛题页面现在直接提供自包含的完整英文题面层与中文解释；AtCoder 页面明确区分官方入口和独立英文呈现，Codeforces 页面就近保留官方来源、直链与材料许可。
- 统一每日单题页的语言分层：AtCoder 与 Codeforces 仅官方英文题面层使用英文，之后的中文解释、算法递进、证明、复杂度、易错点和追问全部使用中文；力扣题解正文统一使用中文，并由共享发布门禁阻止英文分析回归。
- 左侧导航仅展开当前题目所属日期，其他日期保持折叠；新增生成器与结构门禁，保证后续每日账目固定为 1 + 10 + 1 + 1 + 1，并避免时间轴内容与知识专题失去关联。
- 日期、题目、返回、前后题、专题与官方来源均可直接跳转；构建门禁会检查内部路由和锚点，避免源码路径进入线上链接。
- 每日档案发布器只校验并原样嵌入最终规范源，不再改写题面、标题、公式、链接或代码；不合格内容会在任何页面写入前失败并定位到具体题目与行号。

### 公式可靠性

- MathJax 3.2.2 运行文件与全部 CHTML 字体改为站内同版本资源，避免部分客户端只加载数字与运算符字体、却遗漏斜体变量字体。
- 浏览器门禁会显式加载并检查数学斜体、主字体和尺寸字体，同时阻止公式渲染回退到跨域资源。

### 搜索、规范表示与局部状态

- 新增[搜索与枚举知识地图](search/index.md)和[合法前缀回溯](search/backtracking.md)，把状态、选择、剪枝、恢复与输出规模下界整理成统一读者路径。
- 新增[循环等价类](strings/cyclic-normalization.md)专题，以 Booth 最小循环表示解释“先规范化、再分组”，并补齐独立分量签名的充分必要性证明。
- 扩充[线性递推](dp/linear-recurrences.md)、[树上后序聚合](graph/tree-aggregation.md)、[回文中心](strings/palindrome-centers.md)、[回文重排](strings/palindrome-rearrangements.md)、[排列排名](math/permutation-ranking.md)与[数学知识地图](math/index.md)，串联滚动最优状态、指针摘要、近似回文、饱和计数和平方和分类。
- 在基础技巧中补充稳定原地筛选、定长频次窗口、数位半反转、矩阵边界模拟和异或阈值诱导的下标块连通性。

### 权威题目条目

- 收录 [AtCoder ABC468 D](problems/index.md#problem-atcoder-abc468-d)、[CF Round 1111 Div.2 D1（2247D1）](problems/index.md#problem-codeforces-2247-d1)和[第 511 场周赛 Q4](problems/index.md#problem-lc-3999)。
- 收录 [LeetCode 3518](problems/index.md#problem-lc-3518)，以及 [LeetCode Top 31–40](problems/index.md) 的十个连续权威题目条目。
- 统一 14 道题的官方难度与可核验评分口径、完整最优 C++、两空格缩进和窄屏自动折行。

## 2026-07-28

### 图表与渲染

- 复核[学习路线](guide/roadmap.md)、[复杂度分析](guide/complexity.md)、[二分查找](basics/binary-search.md)、[图论](graph/index.md)与[动态规划](dp/index.md)等专题，让不变量、边界和依赖关系优先由正文、表格与可运行代码解释。
- 图表仅在能核对公开来源、版本、许可和页面语义时进入正文；构建检查同时阻止无来源的矢量图、画布绘图和背景图叠字。
- 统一行内公式与正文的基线、溢出和窄屏行为，并为相关技术页补充精选 `Reference`，优先链接原始论文、官方题面、标准库文档与出版社页面。

### 指针、窗口、排列与回文构造

- 新增[链表与局部接线](data-structures/linked-lists.md)、[单调队列](data-structures/monotonic-queues.md)、[排列排名与 Lehmer 码](math/permutation-ranking.md)和[回文重排与字典序](strings/palindrome-rearrangements.md)专题，把哨兵接线、摊还淘汰、字典序分块和半边降维整理为可迁移的不变量。
- 扩充[序列扫描](basics/sequence-invariants.md)、[前缀状态](basics/prefix-sums-and-difference.md)、[二分查找](basics/binary-search.md)与字符串知识地图，补齐稳定压缩、单次交易、前缀偏序可达性、半开区间边界和纵向公共前缀。
- 收录 [AtCoder ABC468 C](problems/index.md#problem-atcoder-abc468-c)、[CF Round 1111 Div.2 C（2247C）](problems/index.md#problem-codeforces-2247-c)、[第 511 场周赛 Q3](problems/index.md#problem-lc-3998)、[LeetCode 3517](problems/index.md#problem-lc-3517)，以及 [LeetCode Top 21–30](problems/index.md) 的权威折叠题目条目。
- 统一相关 C++ 为两空格缩进，并在窄屏保持自动折行；官方分值、平台难度与社区估算分别标注来源，缺失数值不作推断。

## 2026-07-27

### 链接与检索

- 更新日志中的题目名称可直达[对应题目详情](problems/index.md)；带片段的链接会定位并展开目标题目，普通索引仍保持默认折叠。
- 专题、路线、规范和权威来源使用描述性链接，减少在长页面和多级导航中的重复查找。

### 边界状态、后序聚合与构造

- 新增[前缀状态与差分专题](basics/prefix-sums-and-difference.md)，统一解释子数组计数、区间覆盖和在线查询的模型边界。
- 新增[双序列动态规划](dp/sequence-dp.md)、[树上后序聚合](graph/tree-aggregation.md)与[前缀余数构造](math/modular-constructions.md)专题，补齐状态压缩、路径恢复、摘要设计和构造必要性证明。
- 收录 [AtCoder ABC468 B](problems/index.md#problem-atcoder-abc468-b)、[CF Round 1111 Div.2 B（2247B）](problems/index.md#problem-codeforces-2247-b)、[第 511 场周赛 Q2](problems/index.md#problem-lc-3997)，以及 [LeetCode Top 11–20](problems/index.md) 的权威题目条目。
- 扩充[二分分割](basics/binary-search.md)、[链表逐位运算](data-structures/index.md)、[边界收缩](basics/sequence-invariants.md)、[连通分量](graph/index.md)、[秩选择](data-structures/index.md)与[有序归并](basics/sequence-invariants.md)等稳定知识节点，并统一相关 C++ 为两空格缩进。

### 极值候选的分层学习路径

- 将[通用 Top-K 摘要](basics/top-k-extrema.md)、[非负两数乘积](basics/pair-product-extrema.md)和[有符号三数乘积](basics/signed-product-extrema.md)整理为职责清晰的三个专题，保留原极值入口并补齐[导航与路线图](guide/roadmap.md)和[题解索引](problems/index.md)。
- 收录 [LeetCode 1464「数组中两元素的最大乘积」](problems/index.md#problem-lc-1464)，从位置对枚举和排序推导到一次扫描维护前二，并说明平移后的非负单调性。
- 统一相关题目的两空格 C++ 风格，补充重复值、负号、动态删除与区间摘要的模型边界。

## 2026-07-26

### 序列、哈希与状态不变量

- 新增[序列扫描专题](basics/sequence-invariants.md)，串联局部峰值、补数哈希、三数双指针、双端接雨水与连续段唯一扩张起点。
- 新增[哈希分组与 LRU 专题](data-structures/hash-and-cache.md)，补充签名无歧义、滑动窗口失效边界、链表与哈希双不变量。
- 新增 [0-1 权与奇偶状态专题](graph/weighted-parity-states.md)，覆盖二值权最短路、骑士图二分颜色和相邻翻转的 GF(2) 解释。
- 新增[回文中心](strings/palindrome-centers.md)与[线性递推](dp/linear-recurrences.md)专题，比较区间 DP、中心扩展、Manacher、滚动状态与快速倍增。
- 收录 [AtCoder ABC468 A](problems/index.md#problem-atcoder-abc468-a)、[CF Round 1111 Div.2 A（2247A）](problems/index.md#problem-codeforces-2247-a)，以及 [LeetCode 1](problems/index.md#problem-lc-1)、[LeetCode 3](problems/index.md#problem-lc-3)、[LeetCode 5](problems/index.md#problem-lc-5)、[LeetCode 15](problems/index.md#problem-lc-15)、[LeetCode 42](problems/index.md#problem-lc-42)、[LeetCode 49](problems/index.md#problem-lc-49)、[LeetCode 70](problems/index.md#problem-lc-70)、[LeetCode 128](problems/index.md#problem-lc-128)、[LeetCode 146](problems/index.md#problem-lc-146)、[LeetCode 3286](problems/index.md#problem-lc-3286)、[LeetCode 3996](problems/index.md#problem-lc-3996) 的权威折叠题目条目。
- 统一新增与校正代码为[竞赛 C++ 规范](guide/cpp.md)中的两空格缩进与正常横向空格，并保持窄屏自动折行。

### 有符号极值与三数乘积

- 收录 [LeetCode 628「三个数的最大乘积」](problems/index.md#problem-lc-628)，从三重枚举、排序和值域计数推导到一次扫描。
- 解释为什么有负数时必须同时保留三个最大值与两个最小值，并补充正确性证明、样例手推和方案比较。
- 扩展到恢复下标、选择 $k$ 个数、动态增删、区间查询、数值互异和连续子数组等约束变化。
- 改善移动端代码阅读：窄屏下保留源码缩进并自动折行，避免整页或代码块横向滚动。

## 2026-07-25

### 前 $k$ 个极值

- 新增[单次扫描维护前 $k$ 个极值](basics/top-k-extrema.md)的专题，比较枚举、排序、计数和流式维护。
- 收录 [LeetCode 3536「两个数字的最大乘积」](problems/index.md#problem-lc-3536)，补充正确性证明、复杂度下界、重复数位边界与方案选择。
- 系统扩展到恢复答案、最优对计数、选择 $k$ 个数位、数值互异、负数数组、动态增删和区间查询。

## 2026-07-24

### 渲染质量

- 统一公式分隔符并固定 [MathJax](https://docs.mathjax.org/en/v3.2-latest/) 版本，避免合法 TeX 被当作普通文本。
- 发布前校对 Markdown 与公式源、生成的 HTML，以及桌面和移动视口中的真实浏览器渲染。

### 界面精简

- 恢复 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 的原生布局、配色与组件，只保留必要的字体设置。
- 全站正文优先使用苹方，[首页](index.md)改为短标题、直接入口与分类链接。

### 站点初始化

- 建立算法知识库与 [GitHub Pages 自动发布流程](https://github.com/WineChord/algo/actions)。
- 完成[学习路线](guide/roadmap.md)、[统一解题方法](guide/problem-solving.md)、[复杂度分析](guide/complexity.md)与[竞赛 C++ 规范](guide/cpp.md)。
- 建立[基础技巧](basics/index.md)、[数据结构](data-structures/index.md)、[图论](graph/index.md)、[动态规划](dp/index.md)、[数学](math/index.md)和[字符串](strings/index.md)知识地图。
- 发布[二分查找专题](basics/binary-search.md)，覆盖边界二分、答案二分、正确性、易错点与变种。
- 建立[题解索引](problems/index.md)、[写作模板](problems/template.md)、全文搜索、[MathJax](https://docs.mathjax.org/en/v3.2-latest/) 与深浅色主题。

### 视觉系统

- 首页改为学术编辑风格，以摘要、元信息、目录式索引和推理方法替代展示型卡片。
- 统一纸张色背景、衬线标题、细分隔线与克制的酒红强调色，并完善移动端和深色模式。

### 题目详情

- [所有在线评测题](problems/index.md)统一为默认折叠的详情入口，展开后提供题意、思路、复杂度、原题链接和完整 C++ 实现。
- 题目详情采用唯一片段跨专题复用，并增加结构、链接、折叠状态和 [C++ 编译检查](guide/cpp.md)。
