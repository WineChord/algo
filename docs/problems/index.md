# 题解索引

题解按“核心模型”而不是按提交日期组织。一道题可以出现在多个专题中，但应有一个主入口，避免知识被平台和编号切碎。

## 当前题解

| 题目 | 难度 | 主模型 | 关键结论 |
| --- | --- | --- | --- |
| [LeetCode 704. 二分查找](https://leetcode.cn/problems/binary-search/) | 简单 | [边界二分](../basics/binary-search.md#leetcode-704) | 统一为第一个 `>= target` |
| [LeetCode 34. 查找首尾位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) | 中等 | [左右边界](../basics/binary-search.md#leetcode-34) | `lower_bound` + `upper_bound` |
| [LeetCode 875. 爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/) | 中等 | [答案二分](../basics/binary-search.md#leetcode-875) | 最小可行速度 |
| [LeetCode 410. 分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/) | 困难 | [答案二分 + 贪心](../basics/binary-search.md#leetcode-410) | 最小化最大段和 |

## 题解之间如何连接

每篇完整题解至少连接三类节点：

- **前置知识**：理解本题需要的算法、数据结构和数学结论；
- **同构题**：故事不同，但状态或判定结构相同；
- **条件变种**：约束改变后，原解法失效并需要新工具。

例如“在有序数组中查找”连接边界二分；“最小化最大值”连接答案二分；加入动态修改后则可能转向平衡树或线段树。

## 推荐阅读顺序

1. 先读对应专题的核心不变量；
2. 尝试只看题目和约束写出暴力；
3. 对照题解定位优化发生在哪一步；
4. 独立写出最优解并构造边界测试；
5. 完成至少一个条件变化后的变种。

新增内容的结构参考[题解写作模板](template.md)。
