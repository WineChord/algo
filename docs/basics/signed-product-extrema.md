# 有符号乘积与双端极值

非负数的两数乘积只需保留最大的两个出现；允许负数并选择三个数后，符号奇偶性让最优候选同时依赖数轴两端。本专题聚焦“为何必须保留哪些极值”、这些摘要如何在线维护，以及约束变化何时迫使模型升级。

<figure class="knowledge-figure" id="figure-signed-product-extrema">
  <a class="knowledge-figure__image-link" href="../../assets/figures/signed-product-extrema.svg" aria-label="打开有符号三数乘积双端候选原图">
    <img src="../../assets/figures/signed-product-extrema.svg" alt="有符号数轴上三个最大值与两个最小值加最大值构成的两组三数乘积候选" width="960" height="480" loading="lazy" decoding="async">
  </a>
  <figcaption>正数端给出“三个最大值”，负数端则可能用两个很小的负数把乘积翻回正数；两组候选缺一不可。</figcaption>
</figure>

先阅读[极值候选与 Top-K](top-k-extrema.md) 可以建立通用前缀不变量；若所有候选非负且只选两个数，见[非负两数乘积](pair-product-extrema.md)。

## 三数乘积的候选结构

从非负数中选两个数时，只维护最大值与次大值就够了；改为从有符号整数数组中选三个数后，两个很小的负数相乘也可能成为很大的正数。因此状态必须同时覆盖数轴两端。

--8<-- "includes/problems/lc-628.md"

### 约束与候选结构

设数组长度为 $n$。约束 $3\le n\le 10^4$、$-1000\le a_i\le 1000$ 带来三点结论：

1. 三重枚举的 $O(n^3)$ 最坏达到 $10^{12}$ 级，不能作为提交方案；
2. 值域只有 $2001$ 种，可以用计数代替比较排序；
3. 任意三数乘积位于 $[-10^9,10^9]$，题目接口中的 `int` 足够。

将数组排序为 $x_1\le x_2\le\cdots\le x_n$。最大乘积只可能来自

$$
\max\left(x_{n-2}x_{n-1}x_n,\;x_1x_2x_n\right).
$$

第一项选择最大的三个数；第二项选择最小的两个数和最大数。其余组合若有三个非负因子，可以逐个替换为更大的数；若靠两个负数得到非负乘积，则应让这两个负数尽量小、第三个因子尽量大。

### 暴力：枚举三个位置

枚举 $i<j<k$ 覆盖每个三元组一次，可作为随机测试的可靠基准。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumProduct(vector<int>& nums) {
    int n = nums.size();
    int ans = INT_MIN;
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        for (int k = j + 1; k < n; ++k) {
          ans = max(ans, nums[i] * nums[j] * nums[k]);
        }
      }
    }
    return ans;
  }
};
```

时间 $O(n^3)$，额外空间 $O(1)$。它没有利用“答案只依赖两端极值”的结构。

### 排序：只检查数轴两端

排序后直接计算上面的两个候选。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumProduct(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    int allHigh = nums[n - 1] * nums[n - 2] * nums[n - 3];
    int twoLow = nums[0] * nums[1] * nums[n - 1];
    return max(allHigh, twoLow);
  }
};
```

时间 $O(n\log n)$。若排序原数组，除排序栈空间外可视为额外空间 $O(1)$；代价是求出了完整顺序。

### 小值域计数：把排序降为线性

值域固定在 $[-1000,1000]$，统计每个值的频率后，从两端取出三个最大值和两个最小值。

```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumProduct(vector<int>& nums) {
    array<int, 2001> cnt{};
    for (int x : nums)
      ++cnt[x + 1000];
    array<int, 3> hi{};
    array<int, 2> lo{};
    int hc = 0, lc = 0;
    for (int x = 1000; x >= -1000 && hc < 3; --x) {
      for (int t = 0; t < cnt[x + 1000] && hc < 3; ++t)
        hi[hc++] = x;
    }
    for (int x = -1000; x <= 1000 && lc < 2; ++x) {
      for (int t = 0; t < cnt[x + 1000] && lc < 2; ++t)
        lo[lc++] = x;
    }
    return max(hi[0] * hi[1] * hi[2], lo[0] * lo[1] * hi[0]);
  }
};
```

时间 $O(n+2001)=O(n)$，空间 $O(2001)=O(1)$。它适合还要回答频率或动态值域统计的扩展，但常数与状态都大于五变量扫描。

### 最优：一次扫描维护三个最大值和两个最小值

扫描前缀后维持

$$
h_1\ge h_2\ge h_3,\qquad l_1\le l_2.
$$

每个新数分别插入最大值链和最小值链。结束时，两个可能的最优三元组所需信息都仍在状态中；完整实现见本节开头的折叠题目条目。

循环不变量是：处理完任意前缀后，$h_1,h_2,h_3$ 是该前缀按出现位置计数的三个最大值，$l_1,l_2$ 是两个最小值。更新时只把被新元素超越的值依次下放，因此不变量保持。扫描结束后，候选结构证明说明全局最优必为 $h_1h_2h_3$ 或 $l_1l_2h_1$，比较二者即得到答案。

时间 $O(n)$，额外空间 $O(1)$。由于任何位置都可能包含唯一的极值，最坏情况下必须读取全部元素，故时间下界为 $\Omega(n)$。

!!! tip "重复值必须按出现位置保留"

    输入 `[5,5,5]` 时三个 `5` 都要进入最大值链。更新最大值使用 `>=`，并把旧值依次下放，不能先对数值去重。

### 样例手推

对 `[-10,-10,1,2,3]` 依次扫描，最终状态为

| 状态 | 数值 |
| --- | --- |
| 三个最大值 | $h_1=3,\ h_2=2,\ h_3=1$ |
| 两个最小值 | $l_1=-10,\ l_2=-10$ |
| 三个最大值之积 | $3\times2\times1=6$ |
| 两小一大之积 | $(-10)\times(-10)\times3=300$ |

因此答案为 $300$。只有三个负数的样例 `[-1,-2,-3]` 中，三个最大值是 `-1,-2,-3`，乘积为 $-6$；另一个候选也是 $-6$。

### 方案比较

| 方案 | 时间 | 空间 | 证明与实现 | 更适合的用途 |
| --- | --- | --- | --- | --- |
| 三重枚举 | $O(n^3)$ | $O(1)$ | 最直接 | 小规模基准、随机对拍 |
| 排序 | $O(n\log n)$ | 依实现而定 | 最容易记忆 | 后续还需要完整顺序 |
| 值域计数 | $O(n+V)$ | $O(V)$ | 依赖小值域 | 频率、动态计数 |
| 五变量扫描 | $O(n)$ | $O(1)$ | 需维护双端不变量 | 流式输入、最低常数 |

面试和竞赛优先记忆“五变量扫描”：它达到读入下界、无需修改输入，也准确体现“负数使答案同时依赖两端极值”。排序法适合作为不容易写错的次选方案。

### 验证方法

对 $n=3\ldots 9$、元素位于 $[-20,20]$ 的随机数组，同时运行三重枚举与五变量扫描；逐例比较返回值。极端样例还应覆盖全负数、全零、重复最大值、两个大负数、最小长度和 `-1000/1000` 边界。

## 三数乘积的追问与约束变种

### 1. 返回一组最优下标

若要恢复方案，给五个极值同时保存原下标。两个最小值可能与最大值链在数值上重合，因此构造“两小一大”候选时，从三个最大值位置中选一个未被两个最小位置使用的下标。

```cpp
#include <bits/stdc++.h>
using namespace std;
array<int, 3> maximumProductIndices(const vector<int>& nums) {
  array<pair<int, int>, 3> hi{{{INT_MIN, -1}, {INT_MIN, -1}, {INT_MIN, -1}}};
  array<pair<int, int>, 2> lo{{{INT_MAX, -1}, {INT_MAX, -1}}};
  for (int i = 0; i < (int)nums.size(); ++i) {
    pair<int, int> p{nums[i], i};
    if (p.first >= hi[0].first) {
      hi[2] = hi[1];
      hi[1] = hi[0];
      hi[0] = p;
    } else if (p.first >= hi[1].first) {
      hi[2] = hi[1];
      hi[1] = p;
    } else if (p.first > hi[2].first) {
      hi[2] = p;
    }
    if (p.first <= lo[0].first) {
      lo[1] = lo[0];
      lo[0] = p;
    } else if (p.first < lo[1].first) {
      lo[1] = p;
    }
  }
  array<int, 3> a{hi[0].second, hi[1].second, hi[2].second};
  int top = -1;
  for (auto [value, index] : hi) {
    if (index != lo[0].second && index != lo[1].second) {
      top = index;
      break;
    }
  }
  array<int, 3> b{lo[0].second, lo[1].second, top};
  long long pa = 1LL * nums[a[0]] * nums[a[1]] * nums[a[2]];
  long long pb = 1LL * nums[b[0]] * nums[b[1]] * nums[b[2]];
  array<int, 3> ans = pa >= pb ? a : b;
  sort(ans.begin(), ans.end());
  return ans;
}
```

时间 $O(n)$，额外空间 $O(1)$。若要求字典序最小下标组，需要在相等数值的更新中加入下标比较规则。

### 2. 选择恰好 $k$ 个数，使乘积最大

$k$ 不再固定为三时，极值个数随 $k$ 增长，且负号奇偶性使简单维护前 $k$ 大失效。动态规划同时记录“从当前前缀选 $j$ 个数”的最大乘积与最小乘积；乘以负数时二者会交换角色。

```cpp
#include <bits/stdc++.h>
using namespace std;
long long maximumProductK(const vector<int>& nums, int k) {
  vector<long long> mx(k + 1, LLONG_MIN);
  vector<long long> mn(k + 1, LLONG_MAX);
  mx[0] = mn[0] = 1;
  int used = 0;
  for (long long x : nums) {
    ++used;
    for (int j = min(k, used); j >= 1; --j) {
      if (mx[j - 1] == LLONG_MIN)
        continue;
      long long a = mx[j - 1] * x;
      long long b = mn[j - 1] * x;
      mx[j] = max({mx[j], a, b});
      mn[j] = min({mn[j], a, b});
    }
  }
  return mx[k];
}
```

时间 $O(nk)$，空间 $O(k)$。这里假设 $1\le k\le n$ 且答案能放入 `long long`。

### 3. 在线插入、删除并查询

流式五变量状态无法删除当前极值。使用 `multiset` 保存全部元素，更新为 $O(\log n)$；查询只读取有序集合两端的五个元素。

```cpp
#include <bits/stdc++.h>
using namespace std;
class DynamicMaximumProduct {
  multiset<long long> s;
public:
  void insert(long long x) { s.insert(x); }
  bool eraseOne(long long x) {
    auto it = s.find(x);
    if (it == s.end())
      return false;
    s.erase(it);
    return true;
  }
  long long query() const {
    if (s.size() < 3)
      throw invalid_argument("need at least three values");
    auto r = s.rbegin();
    long long hi1 = *r++;
    long long hi2 = *r++;
    long long hi3 = *r;
    auto l = s.begin();
    long long lo1 = *l++;
    long long lo2 = *l;
    return max(hi1 * hi2 * hi3, lo1 * lo2 * hi1);
  }
};
```

插入、删除为 $O(\log n)$，查询为 $O(1)$，空间 $O(n)$。

### 4. 区间查询并支持单点修改

在线段树节点中保存三个最大值和两个最小值。合并节点时，前三大只需从左右节点的六个最大值候选中产生，前两小同理。

```cpp
#include <bits/stdc++.h>
using namespace std;
struct ExtremeNode {
  array<long long, 3> hi{LLONG_MIN, LLONG_MIN, LLONG_MIN};
  array<long long, 2> lo{LLONG_MAX, LLONG_MAX};
};
ExtremeNode mergeExtreme(ExtremeNode a, ExtremeNode b) {
  vector<long long> high, low;
  for (long long x : a.hi)
    if (x != LLONG_MIN)
      high.push_back(x);
  for (long long x : b.hi)
    if (x != LLONG_MIN)
      high.push_back(x);
  for (long long x : a.lo)
    if (x != LLONG_MAX)
      low.push_back(x);
  for (long long x : b.lo)
    if (x != LLONG_MAX)
      low.push_back(x);
  sort(high.begin(), high.end(), greater<long long>());
  sort(low.begin(), low.end());
  ExtremeNode c;
  for (int i = 0; i < min(3, (int)high.size()); ++i)
    c.hi[i] = high[i];
  for (int i = 0; i < min(2, (int)low.size()); ++i)
    c.lo[i] = low[i];
  return c;
}
class MaximumProductSegTree {
  int n;
  vector<ExtremeNode> tr;
  void build(int p, int l, int r, const vector<int>& a) {
    if (l == r) {
      tr[p].hi[0] = tr[p].lo[0] = a[l];
      return;
    }
    int m = (l + r) / 2;
    build(p * 2, l, m, a);
    build(p * 2 + 1, m + 1, r, a);
    tr[p] = mergeExtreme(tr[p * 2], tr[p * 2 + 1]);
  }
  void update(int p, int l, int r, int i, int x) {
    if (l == r) {
      tr[p] = ExtremeNode();
      tr[p].hi[0] = tr[p].lo[0] = x;
      return;
    }
    int m = (l + r) / 2;
    if (i <= m)
      update(p * 2, l, m, i, x);
    else
      update(p * 2 + 1, m + 1, r, i, x);
    tr[p] = mergeExtreme(tr[p * 2], tr[p * 2 + 1]);
  }
  ExtremeNode query(int p, int l, int r, int ql, int qr) const {
    if (ql <= l && r <= qr)
      return tr[p];
    int m = (l + r) / 2;
    if (qr <= m)
      return query(p * 2, l, m, ql, qr);
    if (ql > m)
      return query(p * 2 + 1, m + 1, r, ql, qr);
    return mergeExtreme(query(p * 2, l, m, ql, qr), query(p * 2 + 1, m + 1, r, ql, qr));
  }
public:
  explicit MaximumProductSegTree(const vector<int>& a) : n(a.size()), tr(4 * n) {
    build(1, 0, n - 1, a);
  }
  void update(int i, int x) { update(1, 0, n - 1, i, x); }
  long long query(int l, int r) const {
    ExtremeNode x = query(1, 0, n - 1, l, r);
    return max(x.hi[0] * x.hi[1] * x.hi[2], x.lo[0] * x.lo[1] * x.hi[0]);
  }
};
```

建树 $O(n)$，单点修改和区间查询均为 $O(\log n)$，空间 $O(n)$；查询区间长度必须至少为三。

### 5. 三个数值必须两两不同

“三个不同位置”改成“三个不同数值”后，重复出现不能重复选。先把值去重并排序，再复用两端候选公式。

```cpp
#include <bits/stdc++.h>
using namespace std;
optional<long long> maximumProductDistinctValues(const vector<int>& nums) {
  set<long long> values(nums.begin(), nums.end());
  if (values.size() < 3)
    return nullopt;
  vector<long long> a(values.begin(), values.end());
  int n = a.size();
  return max(a[n - 1] * a[n - 2] * a[n - 3], a[0] * a[1] * a[n - 1]);
}
```

设不同值数量为 $u$，时间 $O(n\log u)$，空间 $O(u)$；不足三个不同值时返回空结果。

### 6. 改为连续子数组

任取三个位置改成“选择一个非空连续子数组”后，极值候选不再足够。扫描到 $x$ 时，同时维护以当前位置结尾的最大乘积与最小乘积；负数会让二者交换。

```cpp
#include <bits/stdc++.h>
using namespace std;
long long maximumProductSubarray(const vector<int>& nums) {
  long long hi = nums[0], lo = nums[0], ans = nums[0];
  for (int i = 1; i < (int)nums.size(); ++i) {
    long long x = nums[i];
    if (x < 0)
      swap(hi, lo);
    hi = max(x, hi * x);
    lo = min(x, lo * x);
    ans = max(ans, hi);
  }
  return ans;
}
```

时间 $O(n)$，额外空间 $O(1)$。这里的核心状态从“全局前几个极值”变为“以当前位置结尾的最大/最小乘积”。

## 易错检查

- “两个数字”通常指两个出现位置，不一定要求数值不同；
- 相等元素能否重复选择取决于出现次数，不能凭数值去重；
- 更新最大值时是否把旧最大值下放给次大值；
- 负数出现后是否还错误地只看最大两个值；
- 三数乘积是否漏掉“两个最小值乘最大值”；
- 最大值链和最小值链是否都正确保留重复出现；
- 动态删除时是否仍在使用不可恢复历史信息的流式状态；
- 乘法是否在提升到足够宽的类型之后发生。

## 复盘

识别信号是“答案只依赖很少几个极值”。核心不变量是扫描前缀后，状态始终保存该前缀中仍可能参与最终答案的候选；有符号三数乘积需要的是三个最大值与两个最小值。出现负数、删除、计数、区间查询或连续性约束时，不要强行沿用两个变量，而应分别补充数轴另一端、频率、可合并状态或前缀动态规划。

## Reference

- [LeetCode 628：三个数的最大乘积](../problems/index.md#problem-lc-628)
- [std::multiset — cppreference](https://en.cppreference.com/w/cpp/container/multiset)
