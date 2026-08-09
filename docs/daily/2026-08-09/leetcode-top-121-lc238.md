---
title: "[力扣 Top 121] LC 238 除了自身以外数组的乘积 中等"
---

# [力扣 Top 121] LC 238 除了自身以外数组的乘积 中等

<p class="daily-archive-kicker">2026-08-09 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=fc9441fca2024195505447d1966a5c5c81ebd834f9b72a156c0dfeb118fe3e3b -->
## 官方原始信息

- Top 排名：121
- 题号：LC 238
- 官方中文标题：除了自身以外数组的乘积
- 官方难度：中等
- 官方链接：[除了自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/)

### 原始题意与函数签名

给定整数数组 `nums`，返回 `answer`，其中 `answer[i]` 是除 `nums[i]` 外所有元素的乘积。要求不使用除法并在 $O(n)$ 时间内完成；输出数组不计入额外空间。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> productExceptSelf(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3,4]
输出：[24,12,8,6]
```

```text
输入：nums = [-1,1,0,-3,3]
输出：[0,0,9,0,0]
```

### 全部约束

- $2\le n\le10^5$。
- $-30\le nums_i\le30$。
- 输入保证每个 `answer[i]` 以及题目涉及的前缀、后缀乘积均在 32 位有符号整数范围内。
- 禁止使用除法；目标时间为 $O(n)$。

## 约束推导与观察

直接为每个位置重算其余 $n-1$ 个数会重复计算大量公共区间，达到 $O(n^2)$。把“除自身”拆成左侧乘积与右侧乘积后，答案为

$$
answer_i=\left(\prod_{j<i}nums_j\right)\left(\prod_{j>i}nums_j\right).
$$

空侧的乘法单位元为 1。零和负数无需特判；题面保证中间乘积可安全放入 `int`。

## 解法递进

### 解法一：逐位置枚举其余元素

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, 1);
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        if (i != j) {
          answer[i] *= nums[j];
        }
      }
    }
    return answer;
  }
};
```

它完整覆盖定义，时间 $O(n^2)$、输出外空间 $O(1)$，适合作为小规模 oracle。

### 解法二：显式前缀积与后缀积

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> left(n, 1), right(n, 1), answer(n);
    for (int i = 1; i < n; ++i) {
      left[i] = left[i - 1] * nums[i - 1];
    }
    for (int i = n - 2; i >= 0; --i) {
      right[i] = right[i + 1] * nums[i + 1];
    }
    for (int i = 0; i < n; ++i) {
      answer[i] = left[i] * right[i];
    }
    return answer;
  }
};
```

时间 $O(n)$、额外空间 $O(n)$。它清楚展示了分解，但两张辅助表可以继续压缩。

### 最佳实用解：输出数组承载前缀积

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, 1);
    for (int i = 1; i < n; ++i) {
      answer[i] = answer[i - 1] * nums[i - 1];
    }
    int suffix = 1;
    for (int i = n - 1; i >= 0; --i) {
      answer[i] *= suffix;
      suffix *= nums[i];
    }
    return answer;
  }
};
```

时间 $O(n)$，输出外额外空间 $O(1)$。面试优先记忆这一版：两趟扫描、一个后缀标量，零值自然处理。

## 正确性证明

第一趟结束后，`answer[i]` 的循环不变量是它等于 $\prod_{j<i}nums_j$。第二趟从右向左，进入位置 `i` 时 `suffix` 等于 $\prod_{j>i}nums_j$。相乘后恰为除 `nums[i]` 外所有元素的乘积；随后乘入 `nums[i]`，为下一位置维护不变量。所有位置都被处理，因此算法正确。

## 样例手推

对 `[1,2,3,4]`，第一趟得到 `[1,1,2,6]`。右扫时 `suffix` 依次为 `1,4,12,24`，答案依次更新为位置 3 的 6、位置 2 的 8、位置 1 的 12、位置 0 的 24。含一个零时，只有零所在位置能乘到所有非零数；含两个零时所有答案都为零，循环无需分支。

## 易错点与方案比较

- 先使用 `suffix` 再乘入 `nums[i]`，否则会把自身算进去。
- `answer[0]` 与初始 `suffix` 都必须是乘法单位元 1。
- 不能用总乘积除以自身；除法被禁止，且零会使该写法失效。
- 输出数组可复用为前缀表，但不能原地覆盖 `nums` 后再读取原值。

## 变种一：允许除法并正确处理零

新定义：允许除法。统计零的数量；无零时用总积相除，一个零时只有零位置非零，两个及以上零时全为零。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> exceptSelfWithDivision(const vector<int>& nums) {
  int zeros = count(nums.begin(), nums.end(), 0);
  long long product = 1;
  for (int x : nums) {
    if (x != 0) {
      product *= x;
    }
  }
  vector<long long> answer(nums.size());
  for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
    if (zeros == 0) {
      answer[i] = product / nums[i];
    } else if (zeros == 1 && nums[i] == 0) {
      answer[i] = product;
    }
  }
  return answer;
}
int main() {
  vector<int> a = {1, 2, 0, 4};
  for (long long x : exceptSelfWithDivision(a)) {
    cout << x << ' ';
  }
}
```

时间 $O(n)$、额外空间 $O(1)$（不计输出）。

## 变种二：结果对任意模数取模

新定义：返回除自身乘积对正模数 `mod` 的余数。模数不必为质数，也不需要逆元；原前后缀结构仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> productExceptSelfMod(const vector<long long>& a, long long mod) {
  int n = a.size();
  vector<long long> answer(n, 1 % mod);
  for (int i = 1; i < n; ++i) {
    answer[i] = answer[i - 1] * ((a[i - 1] % mod + mod) % mod) % mod;
  }
  long long suffix = 1 % mod;
  for (int i = n - 1; i >= 0; --i) {
    answer[i] = answer[i] * suffix % mod;
    suffix = suffix * ((a[i] % mod + mod) % mod) % mod;
  }
  return answer;
}
int main() {
  vector<long long> a = {2, 3, 5};
  for (long long x : productExceptSelfMod(a, 7)) {
    cout << x << ' ';
  }
}
```

时间 $O(n)$、输出外空间 $O(1)$。

## 变种三：单点更新与多次除自身查询

新定义：数组支持单点赋值，并询问某位置以外所有元素乘积模 `MOD`。静态两趟扫描失效；线段树维护区间积，查询 `[0,i)` 与 `(i,n)` 后相乘。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class ProductTree {
  static constexpr long long MOD = 1000000007;
  int size = 1;
  vector<long long> tree;
public:
  explicit ProductTree(const vector<int>& a) {
    while (size < static_cast<int>(a.size())) {
      size <<= 1;
    }
    tree.assign(size * 2, 1);
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
      tree[size + i] = (a[i] % MOD + MOD) % MOD;
    }
    for (int i = size - 1; i; --i) {
      tree[i] = tree[i * 2] * tree[i * 2 + 1] % MOD;
    }
  }
  void setValue(int index, int value) {
    int p = size + index;
    tree[p] = (value % MOD + MOD) % MOD;
    for (p >>= 1; p; p >>= 1) {
      tree[p] = tree[p * 2] * tree[p * 2 + 1] % MOD;
    }
  }
  long long rangeProduct(int left, int right) const {
    long long a = 1, b = 1;
    for (left += size, right += size; left < right; left >>= 1, right >>= 1) {
      if (left & 1) {
        a = a * tree[left++] % MOD;
      }
      if (right & 1) {
        b = tree[--right] * b % MOD;
      }
    }
    return a * b % MOD;
  }
  long long except(int index, int n) const {
    return rangeProduct(0, index) * rangeProduct(index + 1, n) % MOD;
  }
};
int main() {
  vector<int> a = {1, 2, 3, 4};
  ProductTree tree(a);
  cout << tree.except(1, a.size()) << '\n';
}
```

构建 $O(n)$，每次更新或查询 $O(\log n)$，空间 $O(n)$。

## 变种四：二维矩阵中除当前格外的乘积

新定义：对每个矩阵格返回其余所有格的乘积。按行优先展平，仍可用同一个前后缀不变量，再还原形状。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<long long>> matrixExceptSelf(const vector<vector<int>>& a) {
  int rows = a.size();
  int cols = a[0].size();
  int n = rows * cols;
  vector<long long> answer(n, 1);
  for (int p = 1; p < n; ++p) {
    answer[p] = answer[p - 1] * a[(p - 1) / cols][(p - 1) % cols];
  }
  long long suffix = 1;
  for (int p = n - 1; p >= 0; --p) {
    answer[p] *= suffix;
    suffix *= a[p / cols][p % cols];
  }
  vector<vector<long long>> result(rows, vector<long long>(cols));
  for (int p = 0; p < n; ++p) {
    result[p / cols][p % cols] = answer[p];
  }
  return result;
}
int main() {
  vector<vector<int>> a = {{1, 2}, {3, 4}};
  cout << matrixExceptSelf(a)[0][0] << '\n';
}
```

时间 $O(rc)$，输出外空间 $O(rc)$ 仅因返回矩阵布局；核心扫描额外空间为 $O(1)$。

## 可复现验证

对长度 $2..9$、元素值域 `-3..3` 的随机数组，以双循环暴力为 oracle，对比显式前后缀与最佳实用解；固定覆盖零个、一个、多个零，全负数与边界长度。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/product-of-array-except-self/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-f/">← [atcoder] ABC469 F GCD Maximum Spanning Tree</a>
<a class="daily-archive-pager__next" href="../leetcode-top-122-lc1004/">[力扣 Top 122] LC 1004 最大连续 1 的个数 III 中等 →</a>
</nav>
