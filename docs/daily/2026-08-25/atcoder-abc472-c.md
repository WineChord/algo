---
title: "[atcoder] ABC472 C On a Diet"
---

# [atcoder] ABC472 C On a Diet

<p class="daily-archive-kicker">2026-08-25 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-25 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=289a1ead760a3a069260fa56e228bbe3ec1d3ea141e4d36f337bf94c66c051b0 -->
[Official problem: AtCoder ABC472 C — On a Diet](https://atcoder.jp/contests/abc472/tasks/abc472_c?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 472；北京时间 2026-08-22 20:00–21:40；题目：C —
  On a Diet。
- 官方配点：300；比赛 Rated Range：0–1999。
- AtCoder 官方没有为本题标注难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- [AtCoder Problems 社区模型](https://kenkoooo.com/atcoder/resources/problem-models.json)估算难度：
  87，抓取于 2026-08-25；这不是 AtCoder 官方难度。
- 官方英文题面层没有题目图片；站点图标与社交预览图不属于题面资产。
- 下方英文层是逐项核对官方页面后独立组织的自包含完整呈现，不冒充逐字官方原文；来源与
  使用边界参见 [AtCoder 官方题面](https://atcoder.jp/contests/abc472/tasks/abc472_c?lang=en)
  与 [AtCoder Terms of Service](https://atcoder.jp/tos)。

## Complete English statement

Takahashi stays at his parents' house for $N$ days. A snack containing $A_i$ calories is prepared
on day $i$.

He considers the days in the order $i=1,2,\ldots,N$. To decide whether to eat the snack on day
$i$, assume temporarily that he eats it. Add the calories of all snacks actually eaten from day
$\max(i-M+1,1)$ through day $i$. If this total is at most $K$, he eats today's snack; otherwise he
does not eat it. A snack that he skipped contributes zero to every later window.

For every day, determine whether he eats that day's snack.

### Input

The input is given from standard input in the following format:

```text
N M K
A_1 A_2 ... A_N
```

### Output

Print $N$ lines. On line $i$, print `Yes` if Takahashi eats the snack on day $i$, and print `No`
otherwise.

### Constraints

- $1\le M\le N\le2\times10^5$.
- $1\le K\le10^{15}$.
- $1\le A_i\le10^9$ for every $i$.
- Every input value is an integer.

### Official samples

Sample 1:

```text
Input
5 3 83
48 73 59 90 21
Output
Yes
No
No
No
Yes
```

For days 1 through 5, the tentative totals in the most recent three days are respectively
$48,121,107,90,21$. Only the first and fifth totals do not exceed $83$.

Sample 2:

```text
Input
7 4 728
187 816 349 609 255 308 175
Output
Yes
No
Yes
No
Yes
No
Yes
```

Sample 3:

```text
Input
10 3 1368290936
216519459 804733999 297250023 775422599 287963235 999315644 354987425 974810607 653940822 117157941
Output
Yes
Yes
Yes
No
Yes
Yes
No
No
Yes
Yes
```

Source: [AtCoder ABC472 C](https://atcoder.jp/contests/abc472/tasks/abc472_c?lang=en).

## 中文解释与最优结论

每天的决定只依赖最近 $M$ 天中已经吃下的热量。维护这个窗口的已吃热量和 `window`：处理第
$i$ 天前，先删除刚好离开窗口的第 $i-M$ 天贡献；若 `window + A[i] <= K`，就输出 `Yes`
并把 `A[i]` 加入窗口，否则输出 `No` 且记录贡献为 0。

每个元素至多加入、删除各一次，时间复杂度 $O(N)$，空间复杂度 $O(N)$；若用带日期的队列，
空间还可降为 $O(M)$。推荐记忆“接受值数组 + 滑动窗口和”，因为下标边界最容易核对。

## 约束推导、溢出与边界

- $N\le2\times10^5$，逐日重算最近 $M$ 天最坏为 $O(NM)$，必须消除重复求和。
- 已吃窗口和不超过 $K\le10^{15}$，再加 $A_i\le10^9$ 仍安全落在 `long long` 内；`int`
  不足以保存窗口和。
- `M=1` 时，每天只检查自己的热量；上一天贡献必须在本日判断前删除。
- 当 `A_i>K` 时当天必定输出 `No`，但不影响未来窗口。
- 使用按日数组并按固定下标删除时，被拒绝日也要保留 0 占位；若改用只存已接受事件的日期
  队列，则可直接按日期淘汰而不保存拒绝日。
- 判断必须使用 `<= K`；恰好等于上限仍然可以吃。
- 决策是确定性的，不允许为了未来腾空间而主动拒绝一个当前可接受的零食。

## 官方样例手推

样例 1 中 $M=3,K=83$。第 1 天窗口为 48，接受；第 2 天试吃后为 $48+73=121$，拒绝；
第 3 天试吃后为 $48+59=107$，拒绝。第 4 天的三日窗口是第 2–4 天，第 1 天已经离开；
但当天的 90 本身就超过上限，因此仍然拒绝。第 5 天回看第 3–5 天，之前两天都被拒绝，
窗口和为 0，故 21 被接受。

样例 2 可依次得到已吃贡献 $[187,0,349,0,255,0,175]$。任何长度至多 4 的当前后缀中，
只有把当天候选加入后的总和不超过 728 时才保留它，输出与官方结果一致。

样例 3 的十次候选窗口和依次为 $216519459$、$1021253458$、$1318503481$、
$1877406621$、$585213258$、$1287278879$、$1642266304$、$1974126251$、
$653940822$、$771098763$。只在候选和不超过 1368290936 时接受，因此第 4、7、8 天输出
`No`，其余天输出 `Yes`。

## 解法一：逐日重新扫描最近 M 天

令 `eaten[i]` 为当天真正吃下的热量，拒绝时为 0。处理第 $i$ 天时重新扫描
$[\max(0,i-M+1),i-1]$，再尝试加入 $A_i$。它直接照搬定义，因此覆盖正确；时间复杂度
$O(NM)$，空间复杂度 $O(N)$，瓶颈是相邻窗口反复累加同一批贡献。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int m;
  long long k;
  cin >> n >> m >> k;
  vector<long long> calories(n);
  vector<long long> eaten(n, 0);
  for (long long& value : calories)
    cin >> value;
  for (int i = 0; i < n; ++i) {
    long long total = calories[i];
    for (int j = max(0, i - m + 1); j < i; ++j)
      total += eaten[j];
    if (total <= k) {
      eaten[i] = calories[i];
      cout << "Yes\n";
    } else {
      cout << "No\n";
    }
  }
  return 0;
}
```

## 从重复扫描到滑动窗口

第 $i-1$ 天与第 $i$ 天的有效历史只相差一个离开的日期。数组 `eaten` 已经把拒绝记录为 0，
所以只需在 `i >= M` 时执行 `window -= eaten[i - M]`，就能让 `window` 精确表示当天之前仍
留在窗口的已吃热量。

## 最佳实用解：接受值数组加窗口和

### 正确性证明

在处理第 $i$ 天候选之前，先删除 `eaten[i - M]`（若存在）。此后 `window` 恰等于日期
$\max(0,i-M+1)$ 到 $i-1$ 中所有已吃零食的热量和，这是循环不变量。题目定义中的当天
假设总量因此正好是 `window + calories[i]`。

若该值不超过 $K$，算法接受并把当天热量加入 `window`；若超过 $K$，算法拒绝且当天贡献
保持 0。两种分支都与题目唯一规则一致，并为下一天重新建立不变量。由归纳法，全部 $N$ 天
的输出均正确。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int m;
  long long k;
  cin >> n >> m >> k;
  vector<long long> calories(n);
  vector<long long> eaten(n, 0);
  for (long long& value : calories)
    cin >> value;
  long long window = 0;
  for (int i = 0; i < n; ++i) {
    if (i >= m)
      window -= eaten[i - m];
    if (window + calories[i] <= k) {
      eaten[i] = calories[i];
      window += calories[i];
      cout << "Yes\n";
    } else {
      cout << "No\n";
    }
  }
  return 0;
}
```

时间复杂度 $O(N)$，空间复杂度 $O(N)$。

## 同阶方案比较与易错点

队列方案只保存仍在窗口且已接受的 `(日期, 热量)`，空间为 $O(M)$；数组方案会保留全部日期，
但代码更短，且 $N=2\times10^5$ 时内存很小。竞赛中优先记忆数组方案。

- 在本日判断之后才删除第 $i-M$ 天，导致窗口多保留一天。
- 把 `A[i]` 先加入再在失败时忘记撤销。
- 对被拒绝日不留 0 占位，却仍按固定下标删除。
- 使用 `< K`，错误拒绝恰好达到上限的候选。
- 把题目误读成任意选择子集；原题每天只允许按唯一规则接受或拒绝。

## 可复现验证

两份原题程序均以 C++23 编译并通过三个官方样例。额外覆盖 $N=M=1$、`A_i=K`、
`A_i>K`、窗口每步恰有一个元素离开、连续拒绝、$M=N$ 及接近 $10^{15}$ 的窗口和。随机
测试逐项比较 $O(NM)$ 定义模拟与 $O(N)$ 滑动窗口输出。

## Follow-up 与约束变种

### 变种一：按真实时间跨度限制热量

新定义：第 $i$ 份零食在严格递增的非负整数时间 `time[i]` 到达，且
$0\le time_i\le10^{18}$、$1\le T\le10^{18}$；只统计最近 $T$ 秒内，即时间不小于
`time[i] - T + 1` 的已吃零食。该减法仍在 `long long` 范围内。固定下标窗口失效，改用队列
删除过期的已接受事件。每个事件进出队一次，时间 $O(N)$，空间 $O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long duration;
  long long limit;
  cin >> n >> duration >> limit;
  vector<long long> time(n);
  vector<long long> calories(n);
  for (long long& value : time)
    cin >> value;
  for (long long& value : calories)
    cin >> value;
  queue<pair<long long, long long>> eaten;
  long long window = 0;
  for (int i = 0; i < n; ++i) {
    long long firstTime = time[i] - duration + 1;
    while (!eaten.empty() && eaten.front().first < firstTime) {
      window -= eaten.front().second;
      eaten.pop();
    }
    if (window + calories[i] <= limit) {
      window += calories[i];
      eaten.push({time[i], calories[i]});
      cout << "Yes\n";
    } else {
      cout << "No\n";
    }
  }
  return 0;
}
```

### 变种二：每天的回看长度不同

新定义：第 $i$ 天给出 $M_i$，当天只统计最近 $M_i$ 天。窗口不再以固定步长滑动，单个窗口和
不足以回答任意左端点；但所有决策仍按时间追加。令 `prefix[i]` 为前 $i$ 天真正吃下的总热量，
当天历史贡献就是 `prefix[i] - prefix[max(0, i - M_i + 1)]`。时间 $O(N)$，空间 $O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long limit;
  cin >> n >> limit;
  vector<int> lookback(n);
  vector<long long> calories(n);
  for (int& value : lookback)
    cin >> value;
  for (long long& value : calories)
    cin >> value;
  vector<long long> prefix(n + 1, 0);
  for (int i = 0; i < n; ++i) {
    int left = max(0, i - lookback[i] + 1);
    long long total = prefix[i] - prefix[left] + calories[i];
    prefix[i + 1] = prefix[i];
    if (total <= limit) {
      prefix[i + 1] += calories[i];
      cout << "Yes\n";
    } else {
      cout << "No\n";
    }
  }
  return 0;
}
```

### 变种三：同一热量序列上评估多套规则

新定义：给定 $Q$ 组独立的 $(M,K)$，分别输出最终吃到的零食数量。不同阈值会改变早期决策，
继而改变后续窗口，不能复用一套 `eaten` 前缀。对每套规则独立线性模拟，时间 $O(QN)$，
空间 $O(N)$；适合 $QN$ 可控的场景。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  cin >> n >> q;
  vector<long long> calories(n);
  for (long long& value : calories)
    cin >> value;
  while (q--) {
    int m;
    long long limit;
    cin >> m >> limit;
    vector<long long> eaten(n, 0);
    long long window = 0;
    int count = 0;
    for (int i = 0; i < n; ++i) {
      if (i >= m)
        window -= eaten[i - m];
      if (window + calories[i] <= limit) {
        eaten[i] = calories[i];
        window += calories[i];
        ++count;
      }
    }
    cout << count << '\n';
  }
  return 0;
}
```

### 变种四：全程总热量受限时选择最多零食

新定义：令 $M=N$，并允许自由选择吃哪些零食，目标是在总热量不超过 $K$ 时最大化数量。
原题“当前可吃就必须吃”的确定性模拟失效。由于每份零食价值都为 1，交换论证表明最优解
一定优先选择热量最小的项目：排序后从小到大加入，直到下一项会超限。时间 $O(N\log N)$，
空间 $O(N)$。若恢复一般滑动窗口约束，局部删除最大值并不总正确，需要新的全局证明或算法。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long limit;
  cin >> n >> limit;
  vector<long long> calories(n);
  for (long long& value : calories)
    cin >> value;
  sort(calories.begin(), calories.end());
  long long total = 0;
  int answer = 0;
  for (long long value : calories) {
    if (total + value > limit)
      break;
    total += value;
    ++answer;
  }
  cout << answer << '\n';
  return 0;
}
```

## 推荐记忆

看到“按时间顺序决定、只依赖最近固定长度、拒绝项贡献为 0”，先把真实贡献单独存下来，再
维护固定窗口和。不要把原题的确定性规则误改成优化选择问题；变种四缩成单一总量约束后，
才可以安全地按热量排序选择。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc472/tasks/abc472_c?lang=en)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
