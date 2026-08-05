---
title: "[力扣竞赛] 第 513 场周赛 Q4 LC 4013 按奇偶比统计子数组 II 困难"
---

# [力扣竞赛] 第 513 场周赛 Q4 LC 4013 按奇偶比统计子数组 II 困难

<p class="daily-archive-kicker">2026-08-06 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=04916242f0eeabdb3379baba03274505455615829ddcb11514a6808378421f6f -->
## 官方原始信息

- 比赛：第 513 场周赛。
- 题号：Q4 / LC 4013。
- 官方中文标题：按奇偶比统计子数组 II。
- 官方难度：困难。
- 官方竞赛分值：6 分；ZeroTracer 社区估算竞赛分未知。
- 官方链接：[按奇偶比统计子数组 II](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-ii/)

### 原始题意与函数签名

给定数组 `nums` 和正整数 `a,b`。对子数组记偶数数量为 $x$、奇数数量为 $y$。当 $y>0$ 且精确有理数满足 $x/y\le a/b$ 时有效，求有效子数组数量。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  long long countRatioSubarrays(vector<int>& nums, int a, int b);
};
```

### 全部官方样例

```text
输入：nums = [1,2,1,2], a = 3, b = 2
输出：7
```

```text
输入：nums = [2,2,1], a = 2, b = 1
输出：3
```

```text
输入：nums = [2,2,2], a = 1, b = 1
输出：0
解释：所有子数组的奇数数量都为 0。
```

### 全部约束

- $1\le n\le10^5$。
- $1\le nums_i\le10^9$。
- $1\le a,b\le10^9$。

## 约束推导与观察

直接枚举子数组为 $O(n^2)$。设前缀偶数、奇数计数为 $E_i,O_i$，并定义

$$
V_i=bE_i-aO_i.
$$

子数组 $(l,r]$ 满足比例条件，当且仅当

$$
b(E_r-E_l)\le a(O_r-O_l)\iff V_r\le V_l.
$$

若子数组没有奇数，则 $O_r-O_l=0$ 而 $E_r-E_l>0$，原不等式必不成立；因此对非空子数组，`V_l>=V_r` 已自动排除 $y=0$，无需额外维度。问题化为统计前缀序列中满足 $l<r$ 且 $V_l\ge V_r$ 的有序对。$V$ 绝对值最多 $10^{14}$，必须用 64 位。

## 解法递进

### 解法一：枚举所有子数组

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countRatioSubarrays(vector<int>& nums, int a, int b) {
    long long answer = 0;
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      long long even = 0;
      long long odd = 0;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        if (nums[right] % 2) {
          ++odd;
        } else {
          ++even;
        }
        answer += odd > 0 && even * b <= odd * a;
      }
    }
    return answer;
  }
};
```

时间 $O(n^2)$，空间 $O(1)$，作为随机对拍 oracle。

### 最佳实用解：坐标压缩 + Fenwick 树

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  vector<int> tree;
public:
  explicit Fenwick(int n) : tree(n + 1) {
  }
  void add(int index) {
    for (; index < static_cast<int>(tree.size()); index += index & -index) {
      ++tree[index];
    }
  }
  int sum(int index) const {
    int answer = 0;
    for (; index > 0; index -= index & -index) {
      answer += tree[index];
    }
    return answer;
  }
};
class Solution {
public:
  long long countRatioSubarrays(vector<int>& nums, int a, int b) {
    int n = nums.size();
    vector<long long> value(n + 1);
    long long even = 0;
    long long odd = 0;
    for (int i = 0; i < n; ++i) {
      even += nums[i] % 2 == 0;
      odd += nums[i] % 2 != 0;
      value[i + 1] = even * b - odd * a;
    }
    vector<long long> order = value;
    sort(order.begin(), order.end());
    order.erase(unique(order.begin(), order.end()), order.end());
    Fenwick fenwick(order.size());
    long long answer = 0;
    for (int i = 0; i <= n; ++i) {
      int rank = lower_bound(order.begin(), order.end(), value[i]) - order.begin() + 1;
      answer += i - fenwick.sum(rank - 1);
      fenwick.add(rank);
    }
    return answer;
  }
};
```

处理 `V_r` 时，已加入 Fenwick 的恰是更早前缀；`i - count(<V_r)` 就是 `count(>=V_r)`。时间 $O(n\log n)$，空间 $O(n)$，适合在线逐前缀计数，优先记忆。

### 同阶方案：归并排序计数

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countPairs(vector<long long>& a, int left, int right, vector<long long>& buffer) {
  if (right - left <= 1) {
    return 0;
  }
  int middle = (left + right) / 2;
  long long answer = countPairs(a, left, middle, buffer);
  answer += countPairs(a, middle, right, buffer);
  int j = middle;
  for (int i = left; i < middle; ++i) {
    while (j < right && a[j] <= a[i]) {
      ++j;
    }
    answer += j - middle;
  }
  merge(a.begin() + left, a.begin() + middle, a.begin() + middle, a.begin() + right,
      buffer.begin() + left);
  copy(buffer.begin() + left, buffer.begin() + right, a.begin() + left);
  return answer;
}
class Solution {
public:
  long long countRatioSubarrays(vector<int>& nums, int a, int b) {
    vector<long long> value(nums.size() + 1);
    long long even = 0, odd = 0;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      even += nums[i] % 2 == 0;
      odd += nums[i] % 2 != 0;
      value[i + 1] = even * b - odd * a;
    }
    vector<long long> buffer(value.size());
    return countPairs(value, 0, value.size(), buffer);
  }
};
```

时间 $O(n\log n)$，空间 $O(n)$。归并常数较小但“相等也计数”的边界更难写；Fenwick 的不等式更直观。

## 正确性证明

前缀代数已证明每个有效子数组与一个 `l<r,V_l>=V_r` 前缀对一一对应。对于零奇数的非空子数组，`V_r-V_l=b(E_r-E_l)>0`，不可能满足 `V_l>=V_r`，所以 $y>0$ 没有漏检。Fenwick 从左到右处理前缀，查询时只含所有 `l<r`；用已处理总数减去严格小于 `V_r` 的数量，得到且仅得到 `V_l>=V_r` 的前缀数。逐 `r` 相加即为全部有效子数组数。

## 样例手推

样例 1 取 $a=3,b=2$，前缀 $V$ 为 `[0,-3,-1,-4,-2]`。对每个新值统计此前不小于它的值，依次贡献 1、0、3、3，总计 7。全偶数数组的 $V$ 严格递增，每一步都没有此前值不小于当前值，答案 0。

## 易错点与方案比较

- 比例用交叉乘法，不能转浮点。
- 不等式含等号，所以统计的是 `>=`，不是严格逆序对 `>`。
- 前缀 0 必须加入，它代表从下标 0 开始的子数组。
- `a,b` 与计数相乘必须先提升到 `long long`。

## 变种一：比例必须严格小于 `a/b`

条件变为 $V_r<V_l$，查询此前严格大于当前值的数量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Fenwick {
  vector<int> tree;
  explicit Fenwick(int n) : tree(n + 1) {
  }
  void add(int i) {
    for (; i < static_cast<int>(tree.size()); i += i & -i)
      ++tree[i];
  }
  int sum(int i) {
    int s = 0;
    for (; i; i -= i & -i)
      s += tree[i];
    return s;
  }
};
int main() {
  int n;
  long long a, b;
  cin >> n >> a >> b;
  vector<long long> value(n + 1), order;
  long long even = 0, odd = 0;
  for (int i = 1, x; i <= n; ++i) {
    cin >> x;
    even += x % 2 == 0;
    odd += x % 2 != 0;
    value[i] = even * b - odd * a;
  }
  order = value;
  sort(order.begin(), order.end());
  order.erase(unique(order.begin(), order.end()), order.end());
  Fenwick bit(order.size());
  long long answer = 0;
  for (int i = 0; i <= n; ++i) {
    int rank = lower_bound(order.begin(), order.end(), value[i]) - order.begin() + 1;
    answer += i - bit.sum(rank);
    bit.add(rank);
  }
  cout << answer << '\n';
}
```

时间 $O(n\log n)$，空间 $O(n)$。

## 变种二：比例必须恰好等于 `a/b`

条件是 $V_l=V_r$，用哈希统计相同前缀值；非空全偶子数组仍不会产生相等值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  long long a, b;
  cin >> n >> a >> b;
  unordered_map<long long, long long> frequency;
  frequency.reserve(2 * n + 1);
  frequency[0] = 1;
  long long even = 0, odd = 0, answer = 0;
  for (int i = 0, x; i < n; ++i) {
    cin >> x;
    even += x % 2 == 0;
    odd += x % 2 != 0;
    long long value = even * b - odd * a;
    answer += frequency[value];
    ++frequency[value];
  }
  cout << answer << '\n';
}
```

期望时间 $O(n)$，空间 $O(n)$。

## 变种三：恢复任意一个有效子数组

维护此前最大的 $V_l$ 及其下标；若它不小于当前 $V_r$，立即得到一个答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  long long a, b;
  cin >> n >> a >> b;
  long long even = 0, odd = 0;
  long long maximum = 0;
  int maximumIndex = 0;
  for (int right = 1, x; right <= n; ++right) {
    cin >> x;
    even += x % 2 == 0;
    odd += x % 2 != 0;
    long long value = even * b - odd * a;
    if (maximum >= value) {
      cout << maximumIndex + 1 << ' ' << right << '\n';
      return 0;
    }
    if (value > maximum) {
      maximum = value;
      maximumIndex = right;
    }
  }
  cout << "-1 -1\n";
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种四：对多个比例询问分别计数

新定义：数组固定，给出 $q$ 个 `(a,b)`；当 $q$ 较小时，复用奇偶前缀并为每问压缩计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Fenwick {
  vector<int> tree;
  explicit Fenwick(int n) : tree(n + 1) {
  }
  void add(int i) {
    for (; i < static_cast<int>(tree.size()); i += i & -i)
      ++tree[i];
  }
  int sum(int i) {
    int s = 0;
    for (; i; i -= i & -i)
      s += tree[i];
    return s;
  }
};
int main() {
  int n, q;
  cin >> n >> q;
  vector<long long> even(n + 1), odd(n + 1);
  for (int i = 1, x; i <= n; ++i) {
    cin >> x;
    even[i] = even[i - 1] + (x % 2 == 0);
    odd[i] = odd[i - 1] + (x % 2 != 0);
  }
  while (q--) {
    long long a, b;
    cin >> a >> b;
    vector<long long> value(n + 1), order;
    for (int i = 0; i <= n; ++i)
      value[i] = even[i] * b - odd[i] * a;
    order = value;
    sort(order.begin(), order.end());
    order.erase(unique(order.begin(), order.end()), order.end());
    Fenwick bit(order.size());
    long long answer = 0;
    for (int i = 0; i <= n; ++i) {
      int rank = lower_bound(order.begin(), order.end(), value[i]) - order.begin() + 1;
      answer += i - bit.sum(rank - 1);
      bit.add(rank);
    }
    cout << answer << '\n';
  }
}
```

时间 $O(qn\log n)$，空间 $O(n)$；大规模多询问需要进一步利用比例离线结构，原单问算法不能直接降为一次预处理。

## 可复现验证

对长度 $1..60$、随机正整数数组和随机 $a,b\le20$，以二次枚举作 oracle，与 Fenwick 和归并计数逐项对比；固定覆盖全偶、全奇、比例等号、大乘积和单元素。发布代码通过 GNU++23 编译及三组官方样例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-ii/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-120-lc74/">← [力扣 Top 120] LC 74 搜索二维矩阵 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-e/">[codeforces] CF Round 1113 Div.2 E Excuse for Breaks →</a>
</nav>
