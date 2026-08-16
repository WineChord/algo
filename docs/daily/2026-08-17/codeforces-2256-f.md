---
title: "[codeforces] CF Round 1116 Div.1 D / Div.2 F How Long Until Nothing Remains?"
---

# [codeforces] CF Round 1116 Div.1 D / Div.2 F How Long Until Nothing Remains?

<p class="daily-archive-kicker">2026-08-17 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-17 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=48e6ecb9ef8908cb20f1eea19cf5d9e346bdb63f97b0352c34dfe49f0a06e1de -->
[Official problem: Codeforces Round 1116, Div. 1 D / Div. 2 F - How Long Until Nothing Remains?](https://codeforces.com/problemset/problem/2256/F?locale=en)

## 官方来源与元数据

- 比赛：Codeforces Round 1116（Div. 1 与 Div. 2）。
- 同一官方题目的完整别名：Div. 1 D（contest 2255, problem D）/ Div. 2 F（contest 2256,
  problem F）。
- 官方英文标题：How Long Until Nothing Remains?
- 官方分值：Div. 1 为 1750 points，Div. 2 为 3000 points。
- Codeforces 官方 rating：2300。
- 官方标签：binary search、bitmasks、greedy、math；Div. 1 页面另列 data structures、sortings。
- 时间限制：2 秒；内存限制：256 MB。
- 来源：Codeforces；题面直达链接见首行。
- [Codeforces materials usage license v0.1](https://codeforces.com/page/254)。
- [Codeforces 官方材料发布说明](https://codeforces.com/blog/entry/967?locale=en)。

下方英文层在 Codeforces 许可覆盖范围内自包含呈现公开题面，不包含隐藏测试、生成器、
checker 或 validator。官方题面没有理解所必需的图片。

## Complete English statement

Before Chtholly's last sortie, she asks Willem three questions. Her first question is how many seconds
remain before everything disappears if the end cannot be avoided. Willem models that question with the
following process.

You are given an array $a$ of $n$ positive integers. Every second, choose exactly one index $p$
($1\le p\le n$), and update all array elements simultaneously as follows:

- replace $a_p$ with $\left\lfloor a_p/2\right\rfloor$;
- for every $i\ne p$, replace $a_i$ with $\left\lceil a_i/2\right\rceil$.

Find the minimum number of seconds after which every array element becomes zero.

### Input

The first line contains the number of test cases $t$. Each test case has two lines:

```text
n
a_1 a_2 ... a_n
```

### Output

For every test case, print one integer: the minimum number of seconds until all elements are zero.

### Constraints

- $1\le t\le10^4$.
- $1\le n\le2\times10^5$.
- $1\le a_i\le10^9$.
- The sum of $n$ over all test cases does not exceed $2\times10^5$.

### Complete official sample

Input:

```text
5
1
3
3
1 1 1
3
1 2 4
2
5 2
6
1 2 3 4 5 6
```

Output:

```text
2
3
3
3
6
```

### Complete official sample notes

1. With one element, its values are `3 -> 1 -> 0`, so the answer is 2.
2. An element equal to 1 becomes zero only in a second when its own index is selected. Therefore
   three seconds are necessary for `[1,1,1]`, and selecting every index once is sufficient.
3. One optimal sequence for `[1,2,4]` is: select $p=1$ to get `[0,1,2]`, select $p=2$ to get
   `[0,0,1]`, then select $p=3$ to get `[0,0,0]`.
4. One optimal sequence for `[5,2]` is
   `[5,2] -> [2,1] -> [1,0] -> [0,0]`, selecting indices `1,2,1` respectively.
5. The official statement gives no additional note for the fifth test case.

## 中文题意解释

每秒必须选一个下标：被选元素向下取整除以 2，其余元素向上取整除以 2，所有变化同时
发生。要求全数组变成 0 的最少秒数。

向前模拟时，一个元素的变化既依赖数值又依赖每秒是否被选，很难直接贪心。固定总秒数
$T$ 后反推，则“第几秒选择谁”会变成把二进制权值分配给各元素的覆盖问题，结构清晰得多。

## 约束推导：把取整过程反推成二进制权值

把秒数从 0 开始编号。若第 $s$ 秒选择元素 $i$，记 $b_{i,s}=1$，否则为 0。反复展开
取整递推，可得 $T$ 秒后

$$
a_i(T)=\left\lfloor
\frac{a_i+(2^T-1)-B_i}{2^T}
\right\rfloor,
\qquad
B_i=\sum_{s=0}^{T-1}b_{i,s}2^s.
$$

因此 $a_i(T)=0$ 当且仅当 $B_i\ge a_i$。每一秒恰好选一个下标，正等价于把权值
$1,2,4,\ldots,2^{T-1}$ 各分配给一个元素，使每个元素收到的权值和至少为其初值。

因为 $a_i\ge1$，每个元素至少要收到一个权值，所以 $T\ge n$。又因为 $a_i<2^{30}$，
在 $T=n+30$ 时有至少 $n$ 个不小于 $2^{30}$ 的权值，可让每个元素各得一个，故答案一定
位于 `[n,n+30]`。固定 $T$ 的可行性单调，可以二分。

## 样例手推与边界

对 `[5,2]` 检查 $T=2$：权值只有 2 与 1，总和 3 甚至小于需求总和 7，必不可行。
$T=3$ 时权值 4、2、1：把 4 与 1 给需求 5，把 2 给需求 2，二者恰好被覆盖，所以答案
是 3，对应官方选择顺序 `1,2,1`。

- $n=1$：答案是使 $2^T\ge a_1$ 的最小正整数 $T$。
- 全部为 1：每个元素都必须至少被选一次，答案恰为 $n$。
- 大权值可以远超需求，超出的容量无需回收，不影响可行性。
- 不能只比较总权值与总需求；单个权值不能拆给多个元素。
- 答案最多 $n+30$，但直接计算 $2^{n+29}$ 会溢出；位数不小于 30 时只利用“它能独自
  覆盖任意需求”这一事实。

## 解法一：广度优先搜索所有数组状态

小规模时从初始数组出发，枚举下一秒选择的下标。元素身份对答案没有影响，所以每次排序
状态以合并排列相同的节点；第一次到达全零状态的层数就是最短时间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int solve(vector<int> start) {
  sort(start.begin(), start.end());
  queue<vector<int>> queueStates;
  map<vector<int>, int> distance;
  queueStates.push(start);
  distance[start] = 0;
  while (!queueStates.empty()) {
    vector<int> current = queueStates.front();
    queueStates.pop();
    if (current.back() == 0) return distance[current];
    for (int chosen = 0; chosen < static_cast<int>(current.size()); ++chosen) {
      vector<int> next = current;
      for (int i = 0; i < static_cast<int>(next.size()); ++i) {
        next[i] = i == chosen ? next[i] / 2 : (next[i] + 1) / 2;
      }
      sort(next.begin(), next.end());
      if (!distance.count(next)) {
        distance[next] = distance[current] + 1;
        queueStates.push(next);
      }
    }
  }
  return -1;
}
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    vector<int> values(n);
    for (int& value : values) cin >> value;
    cout << solve(values) << '\n';
  }
}
```

状态数随 $n$ 和数值指数增长，只适合做 oracle。它的瓶颈是重复探索许多选择历史，而这些
历史对终态的影响其实只由每个元素收到的二进制权值总和决定。

## 从状态搜索到固定秒数的覆盖判定

对固定 $T$，按权值从大到小处理，每次把当前权值给“尚未满足且剩余需求最大”的元素，
再把该需求减去权值；需求不大于 0 时移除。最大堆即可维护最大剩余需求。

为什么是最大需求优先？设当前权值为 $w$、最大剩余需求为 $x$。若 $x>w$，全部更小权值
之和只有 $w-1$，所以任何可行方案都必须把 $w$ 给 $x$。若 $x\le w$，设某个可行方案把
$w$ 给较小需求 $y$，而用后续权值集合 $S$ 满足 $x$；交换后用 $w$ 满足 $x$，再用 $S$
满足 $y$，因为 $\sum S\ge x\ge y$，仍然可行。因此贪心判定既充分又必要。

高于第 29 位的权值都大于所有需求，每个都直接消掉一个最大需求；无需真的构造大整数。
剩余至多处理 30 个安全的 `1LL << bit` 权值。

## 最佳实用解：最大堆判定加二分答案

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool feasible(const vector<int>& values, int seconds) {
  priority_queue<long long> remaining;
  for (int value : values) remaining.push(value);
  int largeWeights = max(0, seconds - 30);
  while (largeWeights-- > 0 && !remaining.empty()) remaining.pop();
  for (int bit = min(29, seconds - 1); bit >= 0 && !remaining.empty(); --bit) {
    long long need = remaining.top();
    remaining.pop();
    need -= 1LL << bit;
    if (need > 0) remaining.push(need);
  }
  return remaining.empty();
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    vector<int> values(n);
    for (int& value : values) cin >> value;
    int low = n - 1;
    int high = n + 30;
    while (high - low > 1) {
      int middle = low + (high - low) / 2;
      if (feasible(values, middle)) high = middle;
      else low = middle;
    }
    cout << high << '\n';
  }
}
```

一次判定建堆 $O(n)$，至多做 $n+30$ 次弹出或 30 次减法，复杂度 $O(n\log n)$；二分区间
长度仅 31，调用次数为常数，因此每个测试总时间 $O(n\log n)$、空间 $O(n)$。也可从 $n$
起线性试到 $n+30$，但二分更直接利用单调性。

## 正确性证明

**引理 1：固定 $T$ 秒后元素 $i$ 为 0 当且仅当 $B_i\ge a_i$。**

对秒数归纳展开 `floor((x + unselected) / 2)`，得到上式。终值为 0 等价于分子严格小于
$2^T$，即 $a_i-1<B_i$；两者为整数，所以等价于 $B_i\ge a_i$。

**引理 2：操作序列与权值分配一一对应。**

第 $s$ 秒选择谁，就把唯一权值 $2^s$ 分给谁；反过来，每个权值的接收者唯一决定该秒选择
的下标。由引理 1，全零恰好等价于所有需求都被覆盖。

**引理 3：降序权值给最大剩余需求的贪心不改变可行性。**

设最大剩余需求为 $x$。若 $x>w$，所有后续更小权值之和为 $w-1$，不给 $x$ 当前权值便
永远无法满足它。若 $x\le w$，设一份可行分配把 $w$ 给需求 $y\le x$，把后续权值集合
$S$ 给 $x$；交换后 $w$ 单独满足 $x$，且 $\sum S\ge x\ge y$，所以 $S$ 足以满足 $y$。
两种情况都能保留一份首步与贪心相同的可行方案，再对余下权值归纳。

**引理 4：`feasible` 精确实现该贪心。**

最大堆顶始终是最大剩余需求。位数至少 30 的权值大于任意初始需求，必然一次满足堆顶；
较低 30 位逐项安全相减。堆空表示所有需求满足，非空表示贪心也无法覆盖，依引理 3 即不
存在其他可行分配。

**定理：二分结果是最少秒数。**

增加一秒只增加一个可任意分配的更大权值，不会破坏已有可行分配，所以可行性单调。
`n - 1` 必不可行，`n + 30` 必可行；二分返回区间内第一个可行 $T$，即最优答案。

## 方案比较与易错点

- 直接模拟“当前最大元素”没有可靠依据；早期与晚期选择对应的二进制权值完全不同。
- 权值必须按时间位分配，不能只检查 $2^T-1\ge\sum a_i$。
- 固定 $T$ 的贪心从最大权值向下，且每次处理最大剩余需求。
- 每一位权值只能给一个元素，不能拆分。
- $T$ 可能达到 $n+30$；禁止执行超大左移。
- 大于等于 $2^{30}$ 的权值只需弹出一个需求，不需要减法。
- 二分下界 `n - 1` 是严格不可行点；全部 $a_i$ 都是正数。

## 验证说明

五组官方样例均通过。对 $n\le5$、$1\le a_i\le8$ 的 1286 个非降数组，使用原操作 BFS
求真实最短时间，与二分贪心全部一致；另做 29364 组随机固定秒数检查，确认完整大整数贪心
与“30 位截断”实现一致。最佳解、暴力和全部变种均以 GNU++23 编译。

## 变种一：同时输出一条最优选择序列

在最优 $T$ 上重新执行贪心，记录每个二进制位分给的元素。堆空后的剩余秒任选下标 1，
不会让已经为 0 的元素复活。按位从低到高输出，即为从第一秒到第 $T$ 秒的选择顺序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using Node = pair<long long, int>;
bool build(const vector<int>& values, int seconds, vector<int>* schedule) {
  priority_queue<Node> heap;
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    heap.push({values[i], i});
  }
  vector<int> owner(seconds, 0);
  for (int bit = seconds - 1; bit >= 30; --bit) {
    if (!heap.empty()) {
      owner[bit] = heap.top().second;
      heap.pop();
    }
  }
  for (int bit = min(29, seconds - 1); bit >= 0; --bit) {
    if (heap.empty()) continue;
    auto [need, index] = heap.top();
    heap.pop();
    owner[bit] = index;
    need -= 1LL << bit;
    if (need > 0) heap.push({need, index});
  }
  if (!heap.empty()) return false;
  if (schedule != nullptr) *schedule = move(owner);
  return true;
}
int main() {
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  int low = n - 1;
  int high = n + 30;
  while (high - low > 1) {
    int middle = (low + high) / 2;
    if (build(values, middle, nullptr)) high = middle;
    else low = middle;
  }
  vector<int> schedule;
  build(values, high, &schedule);
  cout << high << '\n';
  for (int index : schedule) cout << index + 1 << ' ';
  cout << '\n';
}
```

时间、空间仍为 $O(n\log n)$ 与 $O(n)$，另需 $O(T)$ 保存答案。原算法本就构造了权值归属，
恢复无需 DP 回溯。

## 变种二：每秒最多选择 $c$ 个不同下标

被选元素向下取整，其余仍向上取整。现在每个权值 $2^s$ 有 $c$ 份，但同一元素在同一秒
最多收到一份。对每一位，临时取出至多 $c$ 个最大剩余需求，各减一份权值后再放回；同一位
不会重复选择同一元素。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool feasible(const vector<int>& values, int capacity, int seconds) {
  priority_queue<long long> heap(values.begin(), values.end());
  for (int bit = seconds - 1; bit >= 0 && !heap.empty(); --bit) {
    vector<long long> changed;
    int take = min(capacity, static_cast<int>(heap.size()));
    while (take--) {
      long long need = heap.top();
      heap.pop();
      if (bit >= 30) need = 0;
      else need -= 1LL << bit;
      if (need > 0) changed.push_back(need);
    }
    for (long long need : changed) heap.push(need);
  }
  return heap.empty();
}
int main() {
  int n, capacity;
  cin >> n >> capacity;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  int low = (n + capacity - 1) / capacity - 1;
  int high = (n + capacity - 1) / capacity + 30;
  while (high - low > 1) {
    int middle = (low + high) / 2;
    if (feasible(values, capacity, middle)) high = middle;
    else low = middle;
  }
  cout << high << '\n';
}
```

每次判定至多执行 $O(n+30c)$ 次堆操作，空间 $O(n)$。当 $c=1$ 时退化为原题；多个相同
权值必须分给不同元素，这是相较原模型新增的批容量约束。

## 变种三：未被选元素也向下取整

若每秒所有元素都执行 `floor(value / 2)`，选择下标不再影响数值。最大元素的二进制位数就
是答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    cin >> n;
    int maximum = 0;
    while (n--) {
      int value;
      cin >> value;
      maximum = max(maximum, value);
    }
    int seconds = 0;
    while (maximum > 0) {
      maximum /= 2;
      ++seconds;
    }
    cout << seconds << '\n';
  }
}
```

时间 $O(n+\log\max a_i)$、额外空间 $O(1)$。原题的组合困难恰来自 `ceil` 会让奇数在未被
选中时停留；改成统一 `floor` 后各元素完全独立。

## 变种四：每个下标至多选择一次，且允许某秒不选择

每个需求只能得到至多一个二进制权值。把需求从小到大排序，依次分配不小于它的最小二次
幂，并要求所用位严格递增；最后一个位加 1 就是所需时间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  sort(values.begin(), values.end());
  int nextBit = 0;
  for (int value : values) {
    int requiredBit = 0;
    long long weight = 1;
    while (weight < value) {
      weight <<= 1;
      ++requiredBit;
    }
    nextBit = max(nextBit, requiredBit);
    ++nextBit;
  }
  cout << nextBit << '\n';
}
```

时间 $O(n\log n+n\log\max a_i)$、空间 $O(n)$。原题允许同一元素累计多个权值，必须用
剩余需求堆；加入“至多一次”后变成需求与互异二次幂的有序匹配。

## Reference

- [Codeforces 2256F 官方题面](https://codeforces.com/problemset/problem/2256/F?locale=en)
- [Codeforces 2255D 官方题面](https://codeforces.com/problemset/problem/2255/D?locale=en)
- [Codeforces Round 1116 官方比赛页](https://codeforces.com/contests/2256?locale=en)
- [Codeforces materials usage license v0.1](https://codeforces.com/page/254)
- [Codeforces 官方材料发布说明](https://codeforces.com/blog/entry/967?locale=en)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://codeforces.com/problemset/problem/2256/F?locale=en)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-514-q4-lc4017/">← [力扣竞赛] 第 514 场周赛 Q4 LC 4017 数组中的峰值 II 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-17-lc1563/">[力扣每日一题] 2026-08-17｜LC 1563 石子游戏 V →</a>
</nav>
