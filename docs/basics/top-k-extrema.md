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

## 追问与约束变种

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

## 易错检查

- “两个数字”通常指两个出现位置，不一定要求数值不同；
- 相等元素能否重复选择取决于出现次数，不能凭数值去重；
- 更新最大值时是否把旧最大值下放给次大值；
- 负数出现后是否还错误地只看最大两个值；
- 动态删除时是否仍在使用不可恢复历史信息的流式状态；
- 乘法是否在提升到足够宽的类型之后发生。

## 复盘

识别信号是“答案只依赖很少几个极值”。核心不变量是扫描前缀后，状态始终保存该前缀中仍可能参与最终答案的前 $k$ 个候选。出现负数、删除、计数或区间查询时，不要强行沿用两个变量，而应分别补充最小值、频率或可合并的数据结构状态。
