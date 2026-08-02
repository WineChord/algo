---
title: "[力扣 Top 86] LC 136 只出现一次的数字 简单"
---

# [力扣 Top 86] LC 136 只出现一次的数字 简单

<p class="daily-archive-kicker">2026-08-03 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=98fc300cf44589b37900be88892bb21dd8e7cf39281e9911083cc8145cceca9a -->
## 官方原始信息

- Top 排名：86
- 题号：LC 136
- 官方中文标题：只出现一次的数字
- 官方难度：简单
- 官方链接：[只出现一次的数字](https://leetcode.cn/problems/single-number/)

### 原始题意

非空整数数组中，除一个元素只出现一次外，其余元素都恰好出现两次。找出单独元素；要求线性时间且只使用常数额外空间。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int singleNumber(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [2,2,1]
输出：1
```

```text
输入：nums = [4,1,2,1,2]
输出：4
```

```text
输入：nums = [1]
输出：1
```

### 全部约束

- $1\le nums.length\le3\times10^4$。
- $-3\times10^4\le nums_i\le3\times10^4$。
- 除一个元素出现一次外，其余元素都出现两次。

## 约束推导与代数不变量

哈希计数可在线性时间完成，但需 $O(n)$ 空间，不满足常数空间目标。按位异或具有交换律、结合律，并满足 $x\oplus x=0$、$0\oplus x=x$。因此无论元素顺序如何，每对重复值都会抵消，只留下单独值：

$$
\bigoplus_{i=0}^{n-1}nums_i=single.
$$

异或直接作用于整数二进制补码，负数无需特判，也没有算术溢出。

## 解法递进

### 解法一：逐元素统计出现次数

对每个位置再扫描全数组计数，第一个计数为 1 的值即答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int singleNumber(vector<int>& nums) {
    for (int candidate : nums) {
      int count = 0;
      for (int value : nums) {
        count += value == candidate;
      }
      if (count == 1) {
        return candidate;
      }
    }
    return 0;
  }
};
```

时间 $O(n^2)$，空间 $O(1)$，不满足线性时间。

### 解法二：哈希计数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int singleNumber(vector<int>& nums) {
    unordered_map<int, int> frequency;
    for (int value : nums) {
      ++frequency[value];
    }
    for (const auto& [value, count] : frequency) {
      if (count == 1) {
        return value;
      }
    }
    return 0;
  }
};
```

期望时间 $O(n)$，空间 $O(n)$，适合计数规律更复杂的通用场景。

### 最佳实用解：全数组异或折叠

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int singleNumber(vector<int>& nums) {
    int answer = 0;
    for (int value : nums) {
      answer ^= value;
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$，同时满足两项目标。

## 正确性证明

利用异或交换律和结合律，可以任意重排表达式，把每个出现两次的值放在一起。每对 $x\oplus x$ 等于 0，所有这些 0 再异或不改变结果；唯一值只出现一次，最终为 $0\oplus single=single$。循环恰好异或所有元素，所以返回值正确。

## 样例手推

`[4,1,2,1,2]` 的累积值为 $0\oplus4=4$、$4\oplus1$、再异或 2、1、2。重排后等价于 $4\oplus(1\oplus1)\oplus(2\oplus2)=4$。单元素 `[1]` 直接得到 1。

## 易错点与方案比较

- 异或符号是 `^`，不是逻辑或 `||` 或乘方。
- 该技巧依赖“其余值恰好两次”；出现三次时不再两两抵消。
- 不要把求和公式当作首选，和值可能溢出且对出现次数变化不稳健。
- 哈希法更通用，异或法严格贴合成对抵消约束，推荐先从出现次数推导再套用。

## 变种一：恰有两个元素各出现一次

新定义：其余元素仍成对出现，找出两个单独值。全异或得到 $x\oplus y$，取其中一个置位把两数分到不同组，再分别异或。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  unsigned int combined = 0;
  for (int& value : a) {
    cin >> value;
    combined ^= static_cast<unsigned int>(value);
  }
  unsigned int bit = combined & (~combined + 1U);
  int first = 0, second = 0;
  for (int value : a) {
    if (static_cast<unsigned int>(value) & bit)
      first ^= value;
    else
      second ^= value;
  }
  if (first > second)
    swap(first, second);
  cout << first << ' ' << second << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。使用无符号数提取最低置位，避免有符号最小值取负的溢出。

## 变种二：其余元素出现 $K$ 次

新定义：一个值出现一次，其余值都出现 $K\ge2$ 次。逐二进制位统计 1 的个数并对 $K$ 取模，可重建单独值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  array<long long, 32> count{};
  for (int i = 0; i < n; ++i) {
    unsigned int value;
    cin >> value;
    for (int bit = 0; bit < 32; ++bit) {
      count[bit] += value >> bit & 1U;
    }
  }
  unsigned int answer = 0;
  for (int bit = 0; bit < 32; ++bit) {
    if (count[bit] % k)
      answer |= 1U << bit;
  }
  cout << static_cast<int>(answer) << '\n';
}
```

时间 $O(32n)$，空间 $O(1)$；它覆盖负数的补码位模式。

## 变种三：找出 $0..n$ 中缺失的数字

新定义：长度为 $n$ 的数组包含 $0..n$ 中除一个数外的所有数。把所有下标、所有值以及额外的 $n$ 一起异或，成对项抵消后留下缺失值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  int answer = n;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    answer ^= i ^ value;
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(1)$，无需用可能溢出的等差数列求和。

## 变种四：流式到达并随时查询当前异或摘要

新定义：元素逐个到达，在任一满足“当前恰有一个奇数次元素、其余偶数次”的检查点查询该元素。维护一个异或摘要即可，加入相同值两次会自动撤销。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int operationCount;
  cin >> operationCount;
  int summary = 0;
  while (operationCount--) {
    char type;
    cin >> type;
    if (type == '+') {
      int value;
      cin >> value;
      summary ^= value;
    } else {
      cout << summary << '\n';
    }
  }
}
```

每次操作 $O(1)$，空间 $O(1)$。若查询时存在多个奇数次元素，摘要只是它们的异或，不能被解释成某一个真实元素。

## 验证说明

本轮将七段代码按 C++23 编译；异或解会与计数 oracle 在随机成对数组、随机唯一值和随机排列上对拍，并复核三个官方样例、负数、零与单元素边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/single-number/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-85-lc152/">← [力扣 Top 85] LC 152 乘积最大子数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-87-lc148/">[力扣 Top 87] LC 148 排序链表 中等 →</a>
</nav>
