---
title: "[力扣竞赛] 第 513 场周赛 Q2 LC 4011 按奇偶比统计子数组 I 中等"
---

# [力扣竞赛] 第 513 场周赛 Q2 LC 4011 按奇偶比统计子数组 I 中等

<p class="daily-archive-kicker">2026-08-04 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=82644428a2da6a606e2e06f59b791a3defec37f5058e8d9ba901d72af245ed23 -->
## 官方原始信息

- 来源：力扣中国
- 比赛：第 513 场周赛
- 题目序号：Q2
- 题号：LC 4011
- 官方中文标题：按奇偶比统计子数组 I
- 官方难度：中等
- 官方竞赛分值：4 分
- ZeroTracer 社区估算竞赛分：未知（抓取日期：2026-08-04）
- 官方链接：[按奇偶比统计子数组 I](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-i/)

### 原始题意

给定整数数组 `nums` 以及正整数 `a,b`。对子数组记偶数个数为 $x$、奇数个数为 $y$。当 $y>0$ 且精确有理数比较满足 $x/y\le a/b$ 时，子数组有效。返回有效非空连续子数组数量。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int countRatioSubarrays(vector<int>& nums, int a, int b);
};
```

### 全部官方样例

```text
输入：nums = [1,2,1,2], a = 3, b = 2
输出：7
解释：有效区间为 [0,0]、[0,1]、[0,2]、[0,3]、[1,2]、[2,2]、[2,3]。
```

```text
输入：nums = [2,2,1], a = 2, b = 1
输出：3
解释：[0,2]、[1,2]、[2,2] 有效。
```

```text
输入：nums = [2,2,2], a = 1, b = 1
输出：0
解释：所有子数组的奇数个数都为 0。
```

### 全部约束

- $1\le nums.length\le1000$。
- $1\le nums[i]\le1000$。
- $1\le a,b\le1000$。

## 约束推导：比例变成前缀序关系

不用浮点数，交叉相乘得到 $b x\le a y$。给偶数赋权 $+b$，奇数赋权 $-a$，则有效条件等价于子数组权重和不大于 0。因为 $a,b>0$，全偶数非空子数组的权重严格为正；所以一旦权重和不大于 0，$y>0$ 自动成立，无需额外维护。

设前缀和为 $P_i$，区间 $(l,r]$ 有效当且仅当 $P_r-P_l\le0$，即 $P_l\ge P_r$。问题变成按顺序统计每个当前前缀之前有多少前缀值不小于它。前缀绝对值最多 $10^6$，`int` 可存；答案最多 $n(n+1)/2=500500$，`int` 也安全。

## 解法递进

### 解法一：枚举区间并重新统计奇偶数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countRatioSubarrays(vector<int>& nums, int a, int b) {
    int n = nums.size();
    int answer = 0;
    for (int left = 0; left < n; ++left) {
      for (int right = left; right < n; ++right) {
        int even = 0;
        int odd = 0;
        for (int index = left; index <= right; ++index) {
          nums[index] % 2 == 0 ? ++even : ++odd;
        }
        if (odd > 0 && 1LL * b * even <= 1LL * a * odd) {
          ++answer;
        }
      }
    }
    return answer;
  }
};
```

时间 $O(n^3)$，额外空间 $O(1)$。它完整枚举，可作为短数组 oracle。

### 解法二：固定左端点，向右维护计数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countRatioSubarrays(vector<int>& nums, int a, int b) {
    int answer = 0;
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      int even = 0;
      int odd = 0;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        nums[right] % 2 == 0 ? ++even : ++odd;
        if (odd > 0 && 1LL * b * even <= 1LL * a * odd) {
          ++answer;
        }
      }
    }
    return answer;
  }
};
```

时间降为 $O(n^2)$，空间 $O(1)$；在本题 $n\le1000$ 下已经足够稳健。

### 最佳实用解：前缀权重加 Fenwick 树

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  class Fenwick {
    vector<int> tree;
  public:
    explicit Fenwick(int size) : tree(size + 1) {
    }
    void add(int index) {
      for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
        ++tree[index];
      }
    }
    int prefix(int index) const {
      int answer = 0;
      for (++index; index > 0; index -= index & -index) {
        answer += tree[index];
      }
      return answer;
    }
  };
public:
  int countRatioSubarrays(vector<int>& nums, int a, int b) {
    vector<int> prefix(1, 0);
    for (int value : nums) {
      int weight = value % 2 == 0 ? b : -a;
      prefix.push_back(prefix.back() + weight);
    }
    vector<int> coordinates = prefix;
    sort(coordinates.begin(), coordinates.end());
    coordinates.erase(unique(coordinates.begin(), coordinates.end()), coordinates.end());
    Fenwick fenwick(coordinates.size());
    int seen = 0;
    int answer = 0;
    for (int value : prefix) {
      int rank = lower_bound(coordinates.begin(), coordinates.end(), value) - coordinates.begin();
      answer += seen - fenwick.prefix(rank - 1);
      fenwick.add(rank);
      ++seen;
    }
    return answer;
  }
};
```

时间 $O(n\log n)$，空间 $O(n)$。与 $O(n^2)$ 相比实现略重，但直接迁移到大规模版本；若只面向本题约束，面试中可优先写固定左端点解，竞赛模板中推荐掌握前缀序对解。

## 正确性证明

对任一非空子数组，权重和为 $bx-ay$。若它不大于 0，则不可能没有奇数，因为全偶数时 $bx>0$；因此该条件与题目两个条件完全等价。又有 $bx-ay=P_r-P_l$，所以有效区间与前缀对 $(l,r)$ 满足 $l<r$ 且 $P_l\ge P_r$ 一一对应。算法处理 `P_r` 时，Fenwick 树恰含所有更早前缀，并统计其中不小于当前值者；每个有效区间计一次，非法区间不计，故答案正确。

## 样例手推、边界与易错点

样例一中偶数权重为 2、奇数权重为 -3，前缀为 `[0,-3,-1,-4,-2]`。依次统计此前不小于当前值的数量为 0、1、1、3、2，总计 7。全偶数时前缀严格递增，计数为 0；单个奇数总被计入。

- 必须用交叉乘法，不能用浮点除法。
- Fenwick 查询是“此前不小于当前”，方向写反会统计互补集合。
- 应先查询再插入，避免把空区间计入。
- `prefix(rank - 1)` 必须允许 `rank==0`，本实现返回 0。

## 变种一：比例必须恰好等于 $a/b$

新定义：要求 $bx=ay$ 且 $y>0$。权重和必须为 0，所以统计相同前缀；另维护奇数前缀，排除零奇数区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, a, b;
  cin >> n >> a >> b;
  map<pair<int, int>, long long> frequency;
  int score = 0;
  int odd = 0;
  long long answer = 0;
  frequency[{0, 0}] = 1;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    if (value % 2 == 0) {
      score += b;
    } else {
      score -= a;
      ++odd;
    }
    for (auto it = frequency.lower_bound({score, INT_MIN});
        it != frequency.end() && it->first.first == score; ++it) {
      if (it->first.second < odd) {
        answer += it->second;
      }
    }
    ++frequency[{score, odd}];
  }
  cout << answer << '\n';
}
```

该直观实现最坏 $O(n^2)$；若 $a,b>0$ 且等式成立的非空区间必有奇数，也可只按 `score` 哈希，将时间降到期望 $O(n)$。

## 变种二：严格小于 $a/b$

新定义：要求 $bx<ay$。前缀条件从 $P_l\ge P_r$ 改为 $P_l>P_r$，Fenwick 查询排除相等值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, a, b;
  cin >> n >> a >> b;
  vector<int> prefix(1, 0);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    prefix.push_back(prefix.back() + (value % 2 == 0 ? b : -a));
  }
  vector<int> sorted = prefix;
  sort(sorted.begin(), sorted.end());
  sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
  vector<int> tree(sorted.size() + 1);
  auto add = [&](int index) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      ++tree[index];
    }
  };
  auto sum = [&](int index) {
    int result = 0;
    for (++index; index > 0; index -= index & -index) {
      result += tree[index];
    }
    return result;
  };
  long long answer = 0;
  int seen = 0;
  for (int value : prefix) {
    int rank = lower_bound(sorted.begin(), sorted.end(), value) - sorted.begin();
    answer += seen - sum(rank);
    add(rank);
    ++seen;
  }
  cout << answer << '\n';
}
```

时间 $O(n\log n)$，空间 $O(n)$。

## 变种三：比例必须落在闭区间 $[p/q,a/b]$

新定义：同时满足 $qx\ge py$ 与 $bx\le ay$。两个线性不等式不能由单个全序前缀值同时表达，短约束下直接固定左端点维护计数最清晰。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, p, q, a, b;
  cin >> n >> p >> q >> a >> b;
  vector<int> numbers(n);
  for (int& value : numbers) {
    cin >> value;
  }
  long long answer = 0;
  for (int left = 0; left < n; ++left) {
    int even = 0;
    int odd = 0;
    for (int right = left; right < n; ++right) {
      numbers[right] % 2 == 0 ? ++even : ++odd;
      if (odd > 0 && 1LL * q * even >= 1LL * p * odd && 1LL * b * even <= 1LL * a * odd) {
        ++answer;
      }
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n^2)$，空间 $O(1)$。规模再放大时需要二维偏序计数。

## 变种四：在线追加元素并随时询问累计答案

新定义：比例固定，已知最多追加 `limit` 个元素；每次追加后输出当前数组所有有效子数组数。预先按可能前缀范围建立 Fenwick 树。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int limit, a, b;
  cin >> limit >> a >> b;
  int offset = a * limit;
  int size = (a + b) * limit + 1;
  vector<int> tree(size + 1);
  auto add = [&](int index) {
    for (++index; index <= size; index += index & -index) {
      ++tree[index];
    }
  };
  auto sum = [&](int index) {
    int result = 0;
    for (++index; index > 0; index -= index & -index) {
      result += tree[index];
    }
    return result;
  };
  int prefix = 0;
  int seen = 1;
  long long answer = 0;
  add(offset);
  for (int i = 0; i < limit; ++i) {
    int value;
    cin >> value;
    prefix += value % 2 == 0 ? b : -a;
    int rank = prefix + offset;
    answer += seen - sum(rank - 1);
    add(rank);
    ++seen;
    cout << answer << '\n';
  }
}
```

每次追加 $O(\log((a+b)n))$，空间 $O((a+b)n)$；值域过大时改用动态坐标压缩或平衡树。

## 可复现验证

所有代码块按 GNU++23 编译。Fenwick 解与 $O(n^2)$ 解在随机奇偶数组、随机正 `a,b`、全奇、全偶和交替数组上对拍；样例逐项复现。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-i/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-100-lc67/">← [力扣 Top 100] LC 67 二进制求和 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-c/">[codeforces] CF Round 1113 Div.2 C Maximize the Score →</a>
</nav>
