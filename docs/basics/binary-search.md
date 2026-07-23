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

线性扫描需要 \(O(n)\)，每次检查中点并排除一半区间只需 \(O(\log n)\)。二分正确的核心是：

1. 谓词在搜索范围上单调；
2. 每次更新都保留答案；
3. 区间严格缩小并最终终止。

## 2. 推荐记忆：半开区间找第一个满足

维护搜索区间 \([l,r)\)，循环不变量是“第一个满足条件的位置仍在 \([l,r]\) 中”，其中 `r` 可以是末尾哨兵。

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

### 找最后一个满足怎么办

最稳妥的方法通常不是再背一套更新规则，而是转换问题：

- 最后一个 `< x` = 第一个 `>= x` 的位置减一；
- 最后一个 `<= x` = 第一个 `> x` 的位置减一。

这样所有边界查找都归一到“第一个满足”，减少模板数量。

## 3. 精确查找：LeetCode 704 { #leetcode-704 }

[LeetCode 704. 二分查找](https://leetcode.cn/problems/binary-search/)

### 暴力

从左到右扫描，时间 \(O(n)\)、额外空间 \(O(1)\)。

### 最优

数组已升序，可以用二分。找到第一个 `>= target` 的位置，再检查是否相等。时间 \(O(\log n)\)、额外空间 \(O(1)\)。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size();
        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] >= target) r = m;
            else l = m + 1;
        }
        return l < nums.size() && nums[l] == target ? l : -1;
    }
};
```

若只需要判断是否存在，标准库写法更短：`binary_search(nums.begin(), nums.end(), target)`。

## 4. 左右边界：LeetCode 34 { #leetcode-34 }

[LeetCode 34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)

先找第一个 `>= target` 的位置 `l`，再找第一个 `> target` 的位置 `r`。答案是 \([l,r)\) 对应的闭区间 \([l,r-1]\)。

### 为什么不搜索 `target + 1`

当 `target == INT_MAX` 时，`target + 1` 会溢出。直接使用 `>` 谓词更安全。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    vector<int> searchRange(vector<int>& a, int target) {
        int n = a.size();
        auto first = [&](bool upper) {
            int l = 0, r = n;
            while (l < r) {
                int m = l + (r - l) / 2;
                if (upper ? a[m] > target : a[m] >= target) r = m;
                else l = m + 1;
            }
            return l;
        };
        int l = first(false);
        if (l == n || a[l] != target) return vector<int>{-1, -1};
        return vector<int>{l, first(true) - 1};
    }
};
```

时间 \(O(\log n)\)，额外空间 \(O(1)\)。使用 `lower_bound` 和 `upper_bound` 也是同一算法复杂度，实际提交时推荐优先使用标准库；手写版本用于真正理解区间语义和应对自定义谓词。

## 5. 答案二分：把最优化转成判定

最优化问题常能改写为：

> 给定候选答案 \(x\)，能否在限制内完成？

若 `check(x)` 随 \(x\) 单调，就可以二分最小可行值或最大合法值。

完整流程：

1. 确定答案上下界；
2. 写出 `check(x)`；
3. 证明 `check` 单调；
4. 选择找第一个 `true` 或最后一个 `true`；
5. 计算总复杂度：二分次数乘单次检查成本。

### LeetCode 875：最小速度

[LeetCode 875. 爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/)

速度越大，所需时间越少，因此“能在 `h` 小时内吃完”对速度单调。答案范围是 \([1,\max(piles)]\)。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int l = 1, r = *max_element(piles.begin(), piles.end());
        auto ok = [&](int k) {
            long long hours = 0;
            for (int x : piles) hours += (x + k - 1LL) / k;
            return hours <= h;
        };
        while (l < r) {
            int m = l + (r - l) / 2;
            if (ok(m)) r = m;
            else l = m + 1;
        }
        return l;
    }
};
```

设最大堆为 \(M\)，二分 \(O(\log M)\) 次，每次扫描 \(n\) 堆，总时间 \(O(n\log M)\)，额外空间 \(O(1)\)。

### LeetCode 410：最小化最大段和

[LeetCode 410. 分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/)

若规定每段和不能超过 \(x\)，可以贪心地尽量延长当前段；一旦加入下一个数会超过 \(x\)，就新开一段。这种策略得到所需段数的最小值。

- 下界：单个元素不能拆开，所以至少是 \(\max a_i\)；
- 上界：所有元素放在一段，所以至多是 \(\sum a_i\)；
- \(x\) 越大，所需段数不会增加，判定单调。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        long long l = *max_element(nums.begin(), nums.end());
        long long r = accumulate(nums.begin(), nums.end(), 0LL);
        auto ok = [&](long long limit) {
            int parts = 1;
            long long sum = 0;
            for (int x : nums) {
                if (sum + x > limit) ++parts, sum = 0;
                sum += x;
            }
            return parts <= k;
        };
        while (l < r) {
            long long m = l + (r - l) / 2;
            if (ok(m)) r = m;
            else l = m + 1;
        }
        return (int)l;
    }
};
```

设数组和为 \(S\)，总时间 \(O(n\log S)\)，额外空间 \(O(1)\)。

## 6. 浮点二分

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

## 7. 常见错误

### 没有证明单调性

答案二分之前必须明确：候选答案变大时，可行性只会朝一个方向变化。若 `check` 呈现 `false → true → false`，普通二分不适用。

### 区间语义混用

在同一段代码里把 `r` 一会儿当作可访问下标、一会儿当作开区间端点，会产生越界或漏解。先固定 \([l,r)\) 或 \([l,r]\)，再推导更新。

### 中点或求和溢出

使用 `l + (r - l) / 2`，答案范围和累计值可能超过 `int` 时使用 `long long`。

### 判定函数方向写反

先画出布尔序列，标出要找 `first true` 还是 `last true`，再决定更新方向。

### 边界不是可行答案

二分前确认搜索区间包含答案。若使用末尾哨兵，还要在返回后判断是否越界。

## 8. 追问与变种

| 变化 | 原方法是否可用 | 对应方向 |
| --- | --- | --- |
| 数组降序 | 可用，但谓词方向改变 | 重新定义单调 `check` |
| 数组旋转后仍分段有序 | 需要判断哪一半有序 | [LeetCode 33](https://leetcode.cn/problems/search-in-rotated-sorted-array/) |
| 存在大量重复且旋转 | 最坏可能退化到 \(O(n)\) | [LeetCode 81](https://leetcode.cn/problems/search-in-rotated-sorted-array-ii/) |
| 不知道右边界 | 先指数扩张，再二分 | 无界有序序列搜索 |
| 数据动态插入删除 | 静态数组二分不足 | `set`、平衡树、值域数据结构 |
| 求第 \(k\) 小配对距离 | 对距离做答案二分，双指针判定 | [LeetCode 719](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/) |
| 求矩阵第 \(k\) 小 | 对值域二分，计数判定 | [LeetCode 378](https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/) |

## 最终记忆建议

只记两件事：

1. **边界查找**：半开区间 \([l,r)\)，统一找第一个满足 `check` 的位置；
2. **答案二分**：先写判定、证明单调，再找最小可行或最大合法。

`lower_bound`、`upper_bound` 应当会用；手写模板应当能从不变量重新推导。不要同时死记多套只差一个等号的代码。
