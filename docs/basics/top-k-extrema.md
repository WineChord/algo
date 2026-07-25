# 一次扫描维护前 $k$ 个极值

很多题目只需要最大值、次大值或前 $k$ 个元素，却习惯性地先排序整个输入。排序当然正确，但它计算了完整顺序；如果答案只依赖少数极值，就可以在扫描时只保留仍可能影响答案的信息。

## 识别信号

优先考虑维护前 $k$ 个极值的情形：

- 只求最大两个数的和、积、差或对应位置；
- 数据以流的形式到达，无法回看全部历史；
- $k$ 很小而 $n$ 很大；
- 需要频繁合并两个区间的前若干极值；
- 只关心候选集合，不需要完整有序序列。

常用选择如下。

| 目标 | 方法 | 时间 | 空间 |
| --- | --- | --- | --- |
| 最大值、次大值 | 两个变量 | $O(n)$ | $O(1)$ |
| 固定且很小的前 $k$ 个 | 长度为 $k$ 的数组或小根堆 | $O(nk)$ 或 $O(n\log k)$ | $O(k)$ |
| 所有元素完整排序 | 排序 | $O(n\log n)$ | 依实现而定 |
| 动态增删且查询前 $k$ 个 | 计数、平衡树或双堆 | 依值域和操作而定 | 依结构而定 |

## 从数位枚举到两个极值

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
            if (!cnt[d]) continue;
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
            if (!curWays) continue;
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
        if ((int)q.size() < k) q.push(x);
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
        if (!seen[d]) continue;
        if (a == -1) a = d;
        else return a * d;
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
    void insert(int x) {
        ++cnt[x];
    }
    bool erase(int x) {
        if (!cnt[x]) return false;
        --cnt[x];
        return true;
    }
    int query() const {
        int a = -1, b = -1;
        for (int d = 9; d >= 0 && b == -1; --d) {
            int take = min(cnt[d], 2);
            while (take--) {
                if (a == -1) a = d;
                else b = d;
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
        if (i <= m) update(p * 2, l, m, i, x);
        else update(p * 2 + 1, m + 1, r, i, x);
        tr[p] = mergeTopTwo(tr[p * 2], tr[p * 2 + 1]);
    }
    TopTwo query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) return tr[p];
        int m = (l + r) / 2;
        if (qr <= m) return query(p * 2, l, m, ql, qr);
        if (ql > m) return query(p * 2 + 1, m + 1, r, ql, qr);
        return mergeTopTwo(query(p * 2, l, m, ql, qr), query(p * 2 + 1, m + 1, r, ql, qr));
    }
public:
    explicit TopTwoSegTree(const vector<int>& a) : n(a.size()), tr(4 * n) {
        build(1, 0, n - 1, a);
    }
    void update(int i, int x) {
        update(1, 0, n - 1, i, x);
    }
    int rangeProduct(int l, int r) const {
        TopTwo x = query(1, 0, n - 1, l, r);
        return x.b == -1 ? -1 : x.a * x.b;
    }
};
```

建树 $O(n)$，单点修改和区间查询均为 $O(\log n)$，空间 $O(n)$。这里仍假设元素非负；允许负数时，节点还要同时保存最小两个值。

## 从前二到有符号前五：三个数的最大乘积

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
    for (int x : nums) ++cnt[x + 1000];
    array<int, 3> hi{};
    array<int, 2> lo{};
    int hc = 0, lc = 0;
    for (int x = 1000; x >= -1000 && hc < 3; --x) {
      for (int t = 0; t < cnt[x + 1000] && hc < 3; ++t) hi[hc++] = x;
    }
    for (int x = -1000; x <= 1000 && lc < 2; ++x) {
      for (int t = 0; t < cnt[x + 1000] && lc < 2; ++t) lo[lc++] = x;
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
      if (mx[j - 1] == LLONG_MIN) continue;
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
  void insert(long long x) {
    s.insert(x);
  }
  bool eraseOne(long long x) {
    auto it = s.find(x);
    if (it == s.end()) return false;
    s.erase(it);
    return true;
  }
  long long query() const {
    if (s.size() < 3) throw invalid_argument("need at least three values");
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
  for (long long x : a.hi) if (x != LLONG_MIN) high.push_back(x);
  for (long long x : b.hi) if (x != LLONG_MIN) high.push_back(x);
  for (long long x : a.lo) if (x != LLONG_MAX) low.push_back(x);
  for (long long x : b.lo) if (x != LLONG_MAX) low.push_back(x);
  sort(high.begin(), high.end(), greater<long long>());
  sort(low.begin(), low.end());
  ExtremeNode c;
  for (int i = 0; i < min(3, (int)high.size()); ++i) c.hi[i] = high[i];
  for (int i = 0; i < min(2, (int)low.size()); ++i) c.lo[i] = low[i];
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
    if (i <= m) update(p * 2, l, m, i, x);
    else update(p * 2 + 1, m + 1, r, i, x);
    tr[p] = mergeExtreme(tr[p * 2], tr[p * 2 + 1]);
  }
  ExtremeNode query(int p, int l, int r, int ql, int qr) const {
    if (ql <= l && r <= qr) return tr[p];
    int m = (l + r) / 2;
    if (qr <= m) return query(p * 2, l, m, ql, qr);
    if (ql > m) return query(p * 2 + 1, m + 1, r, ql, qr);
    return mergeExtreme(query(p * 2, l, m, ql, qr),
                        query(p * 2 + 1, m + 1, r, ql, qr));
  }
public:
  explicit MaximumProductSegTree(const vector<int>& a)
      : n(a.size()), tr(4 * n) {
    build(1, 0, n - 1, a);
  }
  void update(int i, int x) {
    update(1, 0, n - 1, i, x);
  }
  long long query(int l, int r) const {
    ExtremeNode x = query(1, 0, n - 1, l, r);
    return max(x.hi[0] * x.hi[1] * x.hi[2],
               x.lo[0] * x.lo[1] * x.hi[0]);
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
  if (values.size() < 3) return nullopt;
  vector<long long> a(values.begin(), values.end());
  int n = a.size();
  return max(a[n - 1] * a[n - 2] * a[n - 3],
             a[0] * a[1] * a[n - 1]);
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
    if (x < 0) swap(hi, lo);
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
