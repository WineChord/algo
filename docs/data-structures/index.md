# 数据结构知识地图

数据结构的本质是：为了让某类操作更快，持续维护一组足够回答问题的信息。选择结构前，先列出需要支持的操作和它们的频率。

## 从操作选择结构

| 需求 | 常用结构 | 单次复杂度 |
| --- | --- | --- |
| 按下标访问、尾部追加 | 动态数组 `vector` | 访问 \(O(1)\)，追加均摊 \(O(1)\) |
| 两端插入删除 | 双端队列 `deque` | \(O(1)\) |
| 最近加入者优先 | 栈 | \(O(1)\) |
| 最早加入者优先 | 队列 | \(O(1)\) |
| 动态取最小或最大 | 堆 | 插入、弹出 \(O(\log n)\) |
| 按键查找 | 哈希表 | 期望 \(O(1)\) |
| 动态维护有序集合 | 平衡树 | \(O(\log n)\) |
| 判断连通、合并集合 | 并查集 | 均摊近似 \(O(1)\) |
| 前缀聚合、单点修改 | 树状数组 | \(O(\log n)\) |
| 通用区间查询与修改 | 线段树 | \(O(\log n)\) |

## 线性结构

### 栈

栈适合处理“最近尚未完成”的对象：

- 括号匹配与表达式求值；
- DFS 的显式调用栈；
- 单调栈寻找左/右侧第一个更大或更小元素；
- 撤销操作。

代表题目：

- [LeetCode 20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/)
- [LeetCode 84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/)
- [LeetCode 739. 每日温度](https://leetcode.cn/problems/daily-temperatures/)

### 队列与双端队列

普通队列表达按层扩展，是 BFS 的核心。双端队列还能维护单调候选，用于滑动窗口最值。

- [LeetCode 239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/)
- [LeetCode 862. 和至少为 K 的最短子数组](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/)

## 堆

堆只保证堆顶最优，不保证整体有序。适合：

- 动态维护最大/最小值；
- 多路归并；
- Top-K；
- Dijkstra 中取当前最短距离；
- 调度与事件模拟。

若需要删除任意元素、找前驱后继或遍历有序结果，优先考虑 `set` / `multiset`，而不是强行给堆做惰性删除。

代表题目：

- [LeetCode 215. 数组中的第 K 个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/)
- [LeetCode 295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/)
- [LeetCode 23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/)

## 哈希表与有序映射

哈希表牺牲顺序换取期望常数查找；平衡树保留顺序并支持前驱、后继和范围操作。

选择时追问：

- 是否需要按键有序遍历？
- 是否需要 `lower_bound`？
- 是否担心对抗数据导致哈希退化？
- 键是否适合稳定哈希？

## 并查集 { #disjoint-set }

并查集维护不断合并的集合划分，支持：

- `find(x)`：找到代表元；
- `union(a,b)`：合并两个集合；
- 判断两点是否连通；
- 维护集合大小、权值或相对关系。

路径压缩与按大小/秩合并同时使用时，\(m\) 次操作复杂度为 \(O(m\alpha(n))\)，其中 \(\alpha\) 是增长极慢的反阿克曼函数。

局限：普通并查集擅长合并，不擅长删除和回答路径细节。

代表题目：

- [LeetCode 684. 冗余连接](https://leetcode.cn/problems/redundant-connection/)
- [LeetCode 721. 账户合并](https://leetcode.cn/problems/accounts-merge/)
- [洛谷 P3367【模板】并查集](https://www.luogu.com.cn/problem/P3367)

## 树状数组与线段树

### 树状数组

代码短、常数小，适合具有逆运算的前缀聚合，最典型是单点加、前缀和。通过差分还能支持区间修改或区间查询的组合。

### 线段树

每个节点维护一个区间摘要，父节点由两个子节点合并。适用条件是摘要具有可结合的合并操作。进一步可以支持：

- 单点修改、区间查询；
- 区间修改、懒标记；
- 找第一个满足条件的位置；
- 动态开点、可持久化等变种。

不要见到区间题就上线段树：静态查询优先前缀和或稀疏表，离线问题可能有更简单的排序扫描。

## 学习每种结构的统一模板

1. **信息**：每个节点或容器元素保存什么；
2. **不变量**：操作后必须保持什么；
3. **合并**：局部信息如何得到全局信息；
4. **复杂度**：最坏、期望还是均摊；
5. **失效条件**：删除、在线、顺序或值域变化后是否仍适用。
