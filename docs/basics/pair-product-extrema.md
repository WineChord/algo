# 非负两数乘积：从枚举到双极值

从不同位置选择两个非负量并最大化乘积时，答案只依赖按出现位置计数的最大值与次大值。真正需要先核对的是：目标函数在合法值域上是否随每个自变量单调不减、重复值能否按出现次数使用，以及变换之后是否仍然非负。

这条路径建立在[极值候选与 Top-K](top-k-extrema.md) 的前缀不变量上；允许负数或改为选择三个数时，应转到[有符号乘积与双端极值](signed-product-extrema.md)。

## 数组中的平移乘积

LeetCode 1464 要最大化

$$
(a_i-1)(a_j-1),\qquad i\ne j.
$$

令 $b_i=a_i-1$。由 $1\le a_i\le 1000$ 可知 $b_i\ge0$，而平移不改变元素大小关系。因此最大化 $b_ib_j$ 等价于选择原数组中最大的两个出现。

--8<-- "includes/problems/lc-1464.md"

### 约束先决定复杂度

数组长度满足 $2\le n\le500$。枚举所有位置对的 $O(n^2)$ 只有约 $1.25\times10^5$ 个候选，足以通过并适合作为验证基准；排序为 $O(n\log n)$；若只保留两个极值，则达到 $O(n)$。答案上界为 $999^2=998001$，`int` 足够。

### 暴力：枚举所有位置对

枚举 $i<j$ 后，每个合法位置对恰好出现一次。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    int ans = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
      for (int j = i + 1; j < (int)nums.size(); ++j) {
        ans = max(ans, (nums[i] - 1) * (nums[j] - 1));
      }
    }
    return ans;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。瓶颈是重复比较大量不可能进入前二的元素。

### 排序：把候选集中到数组末端

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    return (nums[n - 1] - 1) * (nums[n - 2] - 1);
  }
};
```

时间 $O(n\log n)$。原地排序时，除排序栈空间外额外空间可视为 $O(1)$；代价是修改输入并计算了不需要的完整顺序。

### 最优：一次扫描维护前二

处理完任意前缀后，令 $a\ge b$ 为该前缀按出现位置计数的最大值和次大值。读到新值 $x$ 时：

1. 若 $x\ge a$，则新状态为 $(x,a)$；
2. 否则若 $x>b$，则新状态为 $(a,x)$；
3. 否则状态不变。

三种情况恰好覆盖 $x$ 在有序前缀中的插入位置，所以不变量保持。扫描结束后，由 $x\mapsto x-1$ 在合法值域上递增且非负，任意候选的任一因子替换为更大的未使用出现都不会让乘积变小，因此前两个极值给出全局最优。完整实现见上方折叠条目。

时间 $O(n)$，额外空间 $O(1)$；任何算法最坏都必须查看全部输入，所以也达到 $\Omega(n)$ 的读入下界。

!!! tip "重复最大值必须保留两次"

    对 `[1,5,4,5]`，第二个 `5` 应把旧最大值下放为次大值，得到 $(5-1)^2=16$。更新最大值使用 `>=` 可以自然保留不同位置上的相等值。

### 样例手推

扫描 `[3,4,5,2]` 时，前二状态依次为 $(3,0)$、$(4,3)$、$(5,4)$、$(5,4)$，最终答案为 $(5-1)(4-1)=12$。最小规模 `[3,7]` 会得到 $(7,3)$，答案同样为 $12$。

### 方案比较

| 方案 | 时间 | 空间 | 输入副作用 | 推荐用途 |
| --- | --- | --- | --- | --- |
| 枚举位置对 | $O(n^2)$ | $O(1)$ | 无 | 朴素基准、随机对拍 |
| 排序 | $O(n\log n)$ | 依实现而定 | 通常修改数组 | 最容易临场写对 |
| 两变量扫描 | $O(n)$ | $O(1)$ | 无 | 面试与竞赛首选 |

优先记忆“两变量扫描”，因为它直接表达答案所需的最小充分状态；排序法适合作为证明和实现都很稳的备用方案。

## 数位特例：从枚举到两个极值

以“从十进制整数中选两个数位，使乘积最大”为例。设数位数为 $d$。约束 $10\le n\le 10^9$ 保证至少有两个数位且 $d\le 10$；每个数位位于 $[0,9]$，答案至多为 $81$，`int` 足够。

### 暴力：枚举所有位置对

先提取所有数位，再枚举 $i<j$。每个合法位置对恰好被检查一次，因此一定得到正确答案。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(int n) {
    vector<int> a;
    while (n) {
      a.push_back(n % 10);
      n /= 10;
    }
    int ans = 0;
    for (int i = 0; i < (int)a.size(); ++i)
      for (int j = i + 1; j < (int)a.size(); ++j)
        ans = max(ans, a[i] * a[j]);
    return ans;
  }
};
```

时间 $O(d^2)$，空间 $O(d)$。本题中 $d\le 10$，它已经足以通过，也是很好的对拍基准；瓶颈是检查了绝大多数不可能成为答案的位置对。

### 排序：把候选集中到一端

数位非负，若降序排序，前两个数位的乘积最大。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(int n) {
    vector<int> a;
    while (n) {
      a.push_back(n % 10);
      n /= 10;
    }
    sort(a.begin(), a.end(), greater<int>());
    return a[0] * a[1];
  }
};
```

时间 $O(d\log d)$，空间 $O(d)$。它利用了顺序结构，却仍然求出了答案不需要的完整次序。

### 小值域计数

数位只有十种，可以统计频率，再从 $9$ 到 $0$ 取两个出现次数允许的最大值。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(int n) {
    array<int, 10> cnt{};
    while (n) {
      ++cnt[n % 10];
      n /= 10;
    }
    int a = -1, b = -1;
    for (int d = 9; d >= 0; --d) {
      if (!cnt[d])
        continue;
      if (a == -1) {
        a = d;
        if (cnt[d] >= 2) {
          b = d;
          break;
        }
      } else {
        b = d;
        break;
      }
    }
    return a * b;
  }
};
```

时间 $O(d+10)=O(d)$，空间 $O(10)=O(1)$。计数法适合后续还要回答频率、去重或组合数量的问题。

### 最优：单次扫描维护最大与次大

扫描到数位 `x` 时只有三种情况：

1. `x >= a`：`x` 成为新最大值，旧最大值下放为次大值；
2. `a > x > b`：只更新次大值；
3. `x <= b`：它不可能进入当前前两名。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(int n) {
    int a = -1, b = -1;
    while (n) {
      int x = n % 10;
      if (x >= a) {
        b = a;
        a = x;
      } else if (x > b) {
        b = x;
      }
      n /= 10;
    }
    return a * b;
  }
};
```

循环不变量是：处理完任意前缀后，`a`、`b` 分别是该前缀按出现位置计算的最大和次大数位。初始化时没有已处理数位，`-1` 小于所有合法数位；三类更新保持不变量。结束时所有数位都已处理，而非负数集合中任意两数的最大乘积必由最大的两个出现组成，所以 `a * b` 最优。

时间 $O(d)$，额外空间 $O(1)$。任何正确算法在最坏情况下都要查看每个数位，否则未查看位置可能是会改变答案的 `9`，因此 $\Omega(d)$ 的下界也成立。

!!! tip "为什么更新条件是 `>=`"

    输入 `22` 时，第二个 `2` 必须把旧的最大值保存在 `b` 中。如果写成 `x > a`，又没有单独处理相等情况，就会丢失重复出现。

### 样例手推

对 `n = 124`，按取模顺序读到 `4,2,1`：

| 新数位 | `a` | `b` |
| --- | ---: | ---: |
| 4 | 4 | -1 |
| 2 | 4 | 2 |
| 1 | 4 | 2 |

最终答案为 $4\times2=8$。对 `n = 22`，第二个 `2` 触发 `x >= a`，状态从 `(2,-1)` 变为 `(2,2)`。

### 方案选择

| 方案 | 证明与实现 | 时间 | 空间 | 更适合的扩展 |
| --- | --- | --- | --- | --- |
| 枚举位置对 | 最直接，适合基准 | $O(d^2)$ | $O(d)$ | 随机对拍 |
| 排序 | 简单但信息过量 | $O(d\log d)$ | $O(d)$ | 后续需要完整顺序 |
| 十进制计数 | 值域固定，频率清楚 | $O(d)$ | $O(1)$ | 计数、去重、动态频率 |
| 两变量扫描 | 最少状态，常数最小 | $O(d)$ | $O(1)$ | 流式输入、恢复候选 |

优先记忆“两变量扫描”：它直接表达“只保留答案所需信息”的思想。计数法也应掌握，因为值域很小时，它常能让复杂的动态或计数追问变得稳定。

--8<-- "includes/problems/lc-3536.md"

## 两个数位问题的追问与约束变种

下面每个变种都先明确改变了什么，再选择与新约束匹配的状态。

### 1. 返回构成答案的两个数位

若不仅要乘积，还要恢复一组最优数位，维护状态本身已经保存了答案。

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> maxProductDigits(int n) {
  int a = -1, b = -1;
  while (n) {
    int x = n % 10;
    if (x >= a) {
      b = a;
      a = x;
    } else if (x > b) {
      b = x;
    }
    n /= 10;
  }
  return {a, b};
}
```

时间 $O(d)$，空间 $O(1)$。若还要求原数中的位置，需要让状态同时保存 `(数值, 位置)`，并先确定重复最优解的下标字典序规则。

### 2. 统计达到最大乘积的位置对数量

只保存两个极值不再足够，因为答案还依赖频率。统计十个数位的出现次数，枚举数位值对；当最大乘积为 $0$ 时，这种写法也会正确累计 `0×0` 和 `0×正数` 等所有位置对。

```cpp
#include <bits/stdc++.h>
using namespace std;
long long countMaxProductPairs(int n) {
  array<long long, 10> cnt{};
  while (n) {
    ++cnt[n % 10];
    n /= 10;
  }
  int best = -1;
  long long ways = 0;
  for (int a = 0; a <= 9; ++a) {
    for (int b = a; b <= 9; ++b) {
      long long curWays = a == b ? cnt[a] * (cnt[a] - 1) / 2 : cnt[a] * cnt[b];
      if (!curWays)
        continue;
      int product = a * b;
      if (product > best) {
        best = product;
        ways = curWays;
      } else if (product == best) {
        ways += curWays;
      }
    }
  }
  return ways;
}
```

时间 $O(d+10^2)=O(d)$，空间 $O(1)$。

### 3. 选择恰好 $k$ 个数位，使乘积最大

数位全都非负，因此应选择最大的 $k$ 个出现。用大小不超过 $k$ 的小根堆维护当前候选；堆顶是候选中最容易被淘汰的元素。

```cpp
#include <bits/stdc++.h>
using namespace std;
long long maxProductKDigits(int n, int k) {
  priority_queue<int, vector<int>, greater<int>> q;
  while (n) {
    int x = n % 10;
    if ((int)q.size() < k)
      q.push(x);
    else if (x > q.top()) {
      q.pop();
      q.push(x);
    }
    n /= 10;
  }
  long long ans = 1;
  while (!q.empty()) {
    ans *= q.top();
    q.pop();
  }
  return ans;
}
```

假设 $2\le k\le d$。时间 $O(d\log k)$，空间 $O(k)$；在本题最多十个数位的范围内，乘积不超过 $9^{10}$，`long long` 足够。

### 4. 两个数位的值必须不同

“不同位置”改成“不同数值”后，重复的最大数位不能选两次。十进制值域固定，记录出现过的数位并从大到小取两个不同值即可。

```cpp
#include <bits/stdc++.h>
using namespace std;
int maxProductDistinctDigits(int n) {
  array<bool, 10> seen{};
  while (n) {
    seen[n % 10] = true;
    n /= 10;
  }
  int a = -1;
  for (int d = 9; d >= 0; --d) {
    if (!seen[d])
      continue;
    if (a == -1)
      a = d;
    else
      return a * d;
  }
  return -1;
}
```

时间 $O(d+10)=O(d)$，空间 $O(1)$；不足两个不同数位时返回 `-1`。

### 5. 输入改为允许负数的整数数组

“最大的两个数相乘”在有负数时不再总是最优：两个绝对值很大的负数也可能给出最大正积。需要同时维护最大两个值和最小两个值。

```cpp
#include <bits/stdc++.h>
using namespace std;
long long maxProductPair(const vector<int>& nums) {
  long long hi1 = LLONG_MIN, hi2 = LLONG_MIN;
  long long lo1 = LLONG_MAX, lo2 = LLONG_MAX;
  for (long long x : nums) {
    if (x >= hi1) {
      hi2 = hi1;
      hi1 = x;
    } else if (x > hi2) {
      hi2 = x;
    }
    if (x <= lo1) {
      lo2 = lo1;
      lo1 = x;
    } else if (x < lo2) {
      lo2 = x;
    }
  }
  return max(hi1 * hi2, lo1 * lo2);
}
```

假设数组长度至少为二。时间 $O(n)$，空间 $O(1)$；`int` 转为 `long long` 后再乘，避免 32 位乘法溢出。

### 6. 在线插入、删除并查询最大乘积

两变量状态不支持删除：删掉当前最大值后，不知道被丢弃的历史元素。数位值域只有十种，可以维护频率，更新 $O(1)$，查询时扫描十个桶。

```cpp
#include <bits/stdc++.h>
using namespace std;
class DigitProductMultiset {
  array<int, 10> cnt{};
public:
  void insert(int x) { ++cnt[x]; }
  bool erase(int x) {
    if (!cnt[x])
      return false;
    --cnt[x];
    return true;
  }
  int query() const {
    int a = -1, b = -1;
    for (int d = 9; d >= 0 && b == -1; --d) {
      int take = min(cnt[d], 2);
      while (take--) {
        if (a == -1)
          a = d;
        else
          b = d;
      }
    }
    return b == -1 ? -1 : a * b;
  }
};
```

插入、删除为 $O(1)$，查询为 $O(10)=O(1)$，空间 $O(10)=O(1)$。

### 7. 区间查询并支持单点修改

若输入变为数位数组，需要查询任意区间内两个数的最大乘积并修改单点，可以在线段树节点中保存该区间的前两个极值。合并两个节点时，只需从四个候选中再选前两个。

```cpp
#include <bits/stdc++.h>
using namespace std;
struct TopTwo {
  int a = -1, b = -1;
};
TopTwo mergeTopTwo(TopTwo x, TopTwo y) {
  array<int, 4> v{x.a, x.b, y.a, y.b};
  sort(v.begin(), v.end(), greater<int>());
  return {v[0], v[1]};
}
class TopTwoSegTree {
  int n;
  vector<TopTwo> tr;
  void build(int p, int l, int r, const vector<int>& a) {
    if (l == r) {
      tr[p] = {a[l], -1};
      return;
    }
    int m = (l + r) / 2;
    build(p * 2, l, m, a);
    build(p * 2 + 1, m + 1, r, a);
    tr[p] = mergeTopTwo(tr[p * 2], tr[p * 2 + 1]);
  }
  void update(int p, int l, int r, int i, int x) {
    if (l == r) {
      tr[p] = {x, -1};
      return;
    }
    int m = (l + r) / 2;
    if (i <= m)
      update(p * 2, l, m, i, x);
    else
      update(p * 2 + 1, m + 1, r, i, x);
    tr[p] = mergeTopTwo(tr[p * 2], tr[p * 2 + 1]);
  }
  TopTwo query(int p, int l, int r, int ql, int qr) const {
    if (ql <= l && r <= qr)
      return tr[p];
    int m = (l + r) / 2;
    if (qr <= m)
      return query(p * 2, l, m, ql, qr);
    if (ql > m)
      return query(p * 2 + 1, m + 1, r, ql, qr);
    return mergeTopTwo(query(p * 2, l, m, ql, qr), query(p * 2 + 1, m + 1, r, ql, qr));
  }
public:
  explicit TopTwoSegTree(const vector<int>& a) : n(a.size()), tr(4 * n) { build(1, 0, n - 1, a); }
  void update(int i, int x) { update(1, 0, n - 1, i, x); }
  int rangeProduct(int l, int r) const {
    TopTwo x = query(1, 0, n - 1, l, r);
    return x.b == -1 ? -1 : x.a * x.b;
  }
};
```

建树 $O(n)$，单点修改和区间查询均为 $O(\log n)$，空间 $O(n)$。这里仍假设元素非负；允许负数时，节点还要同时保存最小两个值。

## 迁移边界

- 若允许负数，“最大的两个值”可能输给“最小的两个值”，需要同时保留数轴两端；
- 若要求动态删除，只有前二的流式状态无法恢复被淘汰历史，应保存频率或有序集合；
- 若查询区间，节点摘要必须可合并，通常保存前二最大值；允许负数时再保存前二最小值；
- 若选择数量由二变为一般的 $k$，使用小根堆、选择算法或同时维护最大/最小乘积的动态规划，取决于符号与是否在线。

## Reference

- [LeetCode 1464：数组中两元素的最大乘积](../problems/index.md#problem-lc-1464)
- [AtCoder Beginner Contest 468 B](../problems/index.md#problem-atcoder-abc468-b)
- [Introduction to Algorithms, Fourth Edition — MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
