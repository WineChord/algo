---
tags:
  - 二分
  - 单调性
  - 边界
  - 答案二分
---

# 二分查找

二分的本质不是“在有序数组里找数”，而是：

> 在一个单调布尔序列中，找到 `false` 与 `true` 的分界点。

一旦能定义单调谓词 `check(x)`，数组、答案范围、时间或距离都可以成为二分对象。

## 1. 从线性扫描到对数查找

假设有序数组 `a` 中存在一段 `< target`，随后是一段 `>= target`：

```text
false false false true true true
                  ↑ first true
```

线性扫描需要 $O(n)$，每次检查中点并排除一半区间只需 $O(\log n)$。二分正确的核心是：

1. 谓词在搜索范围上单调；
2. 每次更新都保留答案；
3. 区间严格缩小并最终终止。

## 2. 推荐记忆：半开区间找第一个满足

维护搜索区间 $[l,r)$，循环不变量是“第一个满足条件的位置仍在 $[l,r]$ 中”，其中 `r` 可以是末尾哨兵。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class F>
int first_true(int l, int r, F check) {
    while (l < r) {
        int m = l + (r - l) / 2;
        if (check(m)) r = m;
        else l = m + 1;
    }
    return l;
}
int main() {
    vector<int> a{1, 2, 2, 4, 7};
    int x = 2;
    int p = first_true(0, (int)a.size(), [&](int i) { return a[i] >= x; });
    cout << p << '\n';
}
```

这个版本对应标准库 `lower_bound`。推荐把它作为手写边界二分的主模板，因为：

- 区间长度始终是 `r - l`；
- 空区间自然表示为 `l == r`；
- 中点属于区间，不需要访问 `a[n]`；
- 返回 `n` 可以统一表示“不存在满足条件的元素”。

--8<-- "includes/problems/lc-35.md"

### 找最后一个满足怎么办

最稳妥的方法通常不是再背一套更新规则，而是转换问题：

- 最后一个 `< x` = 第一个 `>= x` 的位置减一；
- 最后一个 `<= x` = 第一个 `> x` 的位置减一。

这样所有边界查找都归一到“第一个满足”，减少模板数量。

## 3. 精确查找：LeetCode 704 { #leetcode-704 }

--8<-- "includes/problems/lc-704.md"

若只需要判断是否存在，标准库写法更短：`binary_search(nums.begin(), nums.end(), target)`。

### 整数平方根：在答案值域找最后一个合法值

对非负整数 $x$，谓词 $m^2\le x$ 随 $m$ 单调，因此可以二分最大的合法整数。实现时用 `m <= x / m` 代替直接计算 `m * m`，同时处理 $m=0$，就能避免乘法溢出。

--8<-- "includes/problems/lc-69.md"

## 4. 左右边界：LeetCode 34 { #leetcode-34 }

--8<-- "includes/problems/lc-34.md"

### 为什么不搜索 `target + 1`

当 `target == INT_MAX` 时，`target + 1` 会溢出。直接使用 `>` 谓词更安全。

使用 `lower_bound` 和 `upper_bound` 也是同一算法复杂度，实际提交时推荐优先使用标准库；手写版本用于真正理解区间语义和应对自定义谓词。

## 5. 答案二分：把最优化转成判定

最优化问题常能改写为：

> 给定候选答案 $x$，能否在限制内完成？

若 `check(x)` 随 $x$ 单调，就可以二分最小可行值或最大合法值。

完整流程：

1. 确定答案上下界；
2. 写出 `check(x)`；
3. 证明 `check` 单调；
4. 选择找第一个 `true` 或最后一个 `true`；
5. 计算总复杂度：二分次数乘单次检查成本。

### LeetCode 875：最小速度

--8<-- "includes/problems/lc-875.md"

### LeetCode 410：最小化最大段和

--8<-- "includes/problems/lc-410.md"

### 前缀和定位：一次跨过整轮，再找当前边界

循环任务先用总和跳过完整轮次，再在一轮前缀和中用 `upper_bound` 找当前时长能完成的最长前缀。这里不是二分答案本身，而是在单调前缀数组中定位第一个超出预算的位置。

--8<-- "includes/problems/lc-4012.md"

## 6. 在分割线上二分：两个有序数组的中位数

有序数组不只支持“找某个值”。把两个数组各切一刀，使左半部分总元素数固定；若同时满足

$$
leftA\le rightB,\qquad leftB\le rightA,
$$

那么左半部分恰好包含合并序列中最小的一半元素。对较短数组的切分位置二分，就能在 $O(\log\min(m,n))$ 时间找到中位数。

--8<-- "includes/problems/lc-4.md"

这里的单调性来自：切分位置向右移动时，`leftA` 不减、`rightA` 不减；若 `leftA > rightB`，必须左移，若 `leftB > rightA`，必须右移。

## 7. 浮点二分

浮点数不存在简单的相邻关系，通常固定迭代次数：

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    double x;
    cin >> x;
    double l = 0, r = max(1.0, x);
    for (int it = 0; it < 100; ++it) {
        double m = (l + r) / 2;
        if (m * m >= x) r = m;
        else l = m;
    }
    cout << fixed << setprecision(10) << (l + r) / 2 << '\n';
}
```

固定 100 次对 `double` 通常足够稳定；若按误差终止，要同时考虑绝对误差和相对误差。

## 8. 常见错误

### 没有证明单调性

答案二分之前必须明确：候选答案变大时，可行性只会朝一个方向变化。若 `check` 呈现 `false → true → false`，普通二分不适用。

### 区间语义混用

在同一段代码里把 `r` 一会儿当作可访问下标、一会儿当作开区间端点，会产生越界或漏解。先固定 $[l,r)$ 或 $[l,r]$，再推导更新。

### 中点或求和溢出

使用 `l + (r - l) / 2`，答案范围和累计值可能超过 `int` 时使用 `long long`。

### 判定函数方向写反

先画出布尔序列，标出要找 `first true` 还是 `last true`，再决定更新方向。

### 边界不是可行答案

二分前确认搜索区间包含答案。若使用末尾哨兵，还要在返回后判断是否越界。

## 9. 追问与变种

| 变化 | 原方法是否可用 | 对应方向 |
| --- | --- | --- |
| 数组降序 | 可用，但谓词方向改变 | 重新定义单调 `check` |
| 数组旋转后仍分段有序 | 需要判断哪一半有序 | LeetCode 33（见下方） |
| 存在大量重复且旋转 | 最坏可能退化到 $O(n)$ | LeetCode 81（见下方） |
| 不知道右边界 | 先指数扩张，再二分 | 无界有序序列搜索 |
| 数据动态插入删除 | 静态数组二分不足 | `set`、平衡树、值域数据结构 |
| 求第 $k$ 小配对距离 | 对距离做答案二分，双指针判定 | LeetCode 719（见下方） |
| 求矩阵第 $k$ 小 | 对值域二分，计数判定 | LeetCode 378（见下方） |

### 对应题目

--8<-- "includes/problems/lc-33.md"

二维矩阵同时按行、按列有序时，右上角具有更强的二维单调性：当前值过大就能排除整列，过小就能排除整行。它不需要对每一行分别二分，却与二分共享“每一步永久排除一块不可能区域”的证明结构。

--8<-- "includes/problems/lc-240.md"

--8<-- "includes/problems/lc-81.md"

--8<-- "includes/problems/lc-719.md"

--8<-- "includes/problems/lc-378.md"

## 最终记忆建议

只记两件事：

1. **边界查找**：半开区间 $[l,r)$，统一找第一个满足 `check` 的位置；
2. **答案二分**：先写判定、证明单调，再找最小可行或最大合法。

`lower_bound`、`upper_bound` 应当会用；手写模板应当能从不变量重新推导。不要同时死记多套只差一个等号的代码。

## Reference

- [std::lower_bound — cppreference](https://en.cppreference.com/w/cpp/algorithm/lower_bound)
- [LeetCode 704：二分查找](../problems/index.md#problem-lc-704)
- [LeetCode 34：在排序数组中查找元素的第一个和最后一个位置](../problems/index.md#problem-lc-34)
- [LeetCode 35：搜索插入位置](../problems/index.md#problem-lc-35)
- [LeetCode 240：搜索二维矩阵 II](../problems/index.md#problem-lc-240)
