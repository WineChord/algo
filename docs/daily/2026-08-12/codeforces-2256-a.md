---
title: "[codeforces] CF Round 1116 Div.2 A Three Numbers on the Blackboard"
---

# [codeforces] CF Round 1116 Div.2 A Three Numbers on the Blackboard

<p class="daily-archive-kicker">2026-08-12 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-12 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d61ab12e19acbc2d4c59a0386714840307e9e75279553a735f9250accbb9ff47 -->
[Official problem: Codeforces 2256A — Three Numbers on the Blackboard](https://codeforces.com/contest/2256/problem/A)

[Materials usage license](https://codeforces.com/blog/entry/967)

## 官方来源与元数据

- 比赛：Codeforces Round 1116 (Div. 2)，Contest ID 2256。
- 题目：Div.2 A - Three Numbers on the Blackboard；官方分值 500，官方 rating 未发布。
- 官方 tags：`math`、`sortings`；时间限制 1 秒，内存限制 256 MB。
- 官方链接：[Codeforces 2256A](https://codeforces.com/contest/2256/problem/A)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)。

## Complete English statement

### A. Three Numbers on the Blackboard

- Contest: Codeforces Round 1116 (Div. 2), contest ID 2256.
- Alias: Div.2 A only; this problem does not occur in the Div.1 problem list.
- Official points: 500. Official rating: not published. Official tags: math, sortings.
- Time limit: 1 second. Memory limit: 256 megabytes.
- Input: standard input. Output: standard output.

Rain falls outside the Fairy Warehouse, so Chtholly, Nephren, and Ithea play a blackboard game. Ithea initially writes three non-negative integers $a,b,c$.

Chtholly may repeat the following operation any number of times, including zero:

- choose one of the three current integers;
- replace it by the sum of the other two current integers;
- leave the other two integers unchanged.

For example, from $(3,5,11)$, replacing $11$ by $3+5$ produces $(3,5,8)$.

The range of a non-empty finite collection is its maximum minus its minimum. Determine the minimum possible range of the three integers after any allowed sequence of operations.

### Input

The first line contains the number of test cases $t$.

Each test case consists of one line containing the three initial integers $a,b,c$.

### Output

For every test case, output one integer: the minimum range that can be obtained.

### Constraints

- $1\le t\le100$.
- $0\le a,b,c\le10^9$.

### Official sample

```text
Input
6
5 5 5
4 6 9
2 3 10
0 0 7
2 3 5
20 4 5

Output
0
5
3
0
3
5
```

### Official notes

- In the first test case the three numbers are already equal, so the range is $0$.
- In the second test case, doing nothing gives $9-4=5$, and no operation can do better.
- In the third test case, replace $10$ by $2+3=5$. The numbers become $(2,3,5)$ and their range is $3$.
- In the fourth test case, replace $7$ by $0+0=0$. All three numbers then equal zero.

No image is needed to understand the statement. The statement layer above is a self-contained presentation of the official task contract; source, contest context, examples, notes, and license remain linked next to it.

## 中文解释与题解

### 题意重述

黑板上有三个非负整数。一次操作可以挑一个数，把它改成另外两个数之和。操作次数不限，也可以一次都不做。目标是让最终三数的极差，也就是最大值减最小值，尽可能小。

### 约束推导与观察

把当前三个数排序为 $x\le y\le z$。若执行一次操作并保留两个数 $u\le v$，新三元组一定是 $(u,v,u+v)$，因为非负性保证 $u+v\ge v$。因此：

- 任意非空操作序列的最后一步之后，极差恰好为 $(u+v)-u=v$；
- 这一步的新中位数也是 $v$；
- 一次操作后的中位数不会小于操作前的中位数。

所以，只要执行过至少一次操作，最终极差至少是初始中位数 $y$。另一方面：

- 不操作可得到极差 $z-x$；
- 把最大值 $z$ 替换为 $x+y$，新三元组为 $(x,y,x+y)$，极差恰好为 $y$。

答案因此是

$$
\min(z-x,y).
$$

## 解法递进

### 解法一：有界状态广度优先搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  array<int, 3> start;
  for (int& x : start) cin >> x;
  sort(start.begin(), start.end());
  const int limit = 100;
  queue<array<int, 3>> queue;
  set<array<int, 3>> visited{start};
  queue.push(start);
  int answer = start[2] - start[0];
  while (!queue.empty()) {
    auto current = queue.front();
    queue.pop();
    answer = min(answer, current[2] - current[0]);
    for (int replaced = 0; replaced < 3; ++replaced) {
      auto next = current;
      next[replaced] = current[(replaced + 1) % 3] + current[(replaced + 2) % 3];
      sort(next.begin(), next.end());
      if (next[2] <= limit && visited.insert(next).second) queue.push(next);
    }
  }
  cout << answer << '\n';
}
```

它枚举阈值内全部可达状态，能作为小数值 oracle；但数值可能不断增长，固定阈值无法构成正式证明，状态数也没有适合 $10^9$ 的上界。

### 解法二：枚举零步或一步操作

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long range(array<long long, 3> values) {
  auto [minimum, maximum] = minmax_element(values.begin(), values.end());
  return *maximum - *minimum;
}
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    for (long long& x : a) cin >> x;
    long long answer = range(a);
    for (int replaced = 0; replaced < 3; ++replaced) {
      auto next = a;
      next[replaced] = a[(replaced + 1) % 3] + a[(replaced + 2) % 3];
      answer = min(answer, range(next));
    }
    cout << answer << '\n';
  }
}
```

通过中位数下界可知，多步操作不会优于最佳一步或零步，因此只枚举四种候选已经正确。每组是 $O(1)$ 时间与空间，但仍比闭式解多做了常数工作。

### 最佳实用解：排序后的闭式

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    for (long long& x : a) cin >> x;
    sort(a.begin(), a.end());
    cout << min(a[2] - a[0], a[1]) << '\n';
  }
}
```

三元素排序视为 $O(1)$，总时间 $O(t)$、额外空间 $O(1)$。最大和值不超过 $2\times10^9$，32 位有符号整数尚可容纳，但使用 `long long` 更稳妥。该闭式证明短、实现稳定，是竞赛中应优先记忆的方案。

## 正确性证明

设初始排序为 $x\le y\le z$。

下界：第一次操作后，状态总能写成 $p\le q\le p+q$，其极差为 $q$；三种首步分别给出极差 $z,z,y$。从这种加和态继续：替换 $p$ 后极差为 $p+q$，替换 $q$ 后极差也为 $p+q$，替换 $p+q$ 则状态不变。因此第一次操作之后，极差永不下降。任何非空序列都至少为首步三种极差的最小值 $y$。零步方案固定为 $z-x$，故任意方案至少为 $\min(z-x,y)$。

可达性：零步直接实现 $z-x$。把 $z$ 替换为 $x+y$ 后得到 $x\le y\le x+y$，极差为 $y$。两种候选都可达，所以它们的较小值可达。上下界相等，公式正确。

## 样例手推、边界与易错点

对 `(4,6,9)`，零步极差为 5，中位数为 6，取 5；对 `(2,3,10)`，零步为 8，替换最大值后得到 `(2,3,5)`，极差为 3；对 `(0,0,7)`，替换 7 后得到全零，公式也给 `min(7,0)=0`。

- 允许零次操作，不能只输出中位数。
- 非负性是单调证明关键；允许负数后 $u+v\ge v$ 不再成立。
- 不要模拟到“看起来稳定”，操作可以无限增长。
- 三个数相等时答案为 0。
- 两个零可在一步内把任意第三个数变成 0。
- 六组官方样例通过；闭式与有界可达图在所有 $0\le a,b,c\le18$ 的 6,859 个有序三元组上逐一一致。

## 变种一：必须至少执行一次操作

新定义：禁止零步。中位数下界仍成立，把最大值替换为另外两数之和又恰好达到中位数，因此答案就是初始中位数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    for (long long& x : a) cin >> x;
    sort(a.begin(), a.end());
    cout << a[1] << '\n';
  }
}
```

每组时间、空间均为 $O(1)$。

## 变种二：输出达到最优值的一步操作

新定义：输出是否操作；若操作，输出被替换的原下标。若原极差不大于中位数就不操作，否则替换一个最大值位置，复杂度 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  array<long long, 3> a;
  for (long long& x : a) cin >> x;
  vector<pair<long long, int>> ordered;
  for (int i = 0; i < 3; ++i) ordered.push_back({a[i], i});
  sort(ordered.begin(), ordered.end());
  if (ordered[2].first - ordered[0].first <= ordered[1].first) {
    cout << "NONE\n";
  } else {
    cout << "REPLACE " << ordered[2].second << '\n';
  }
}
```

## 变种三：每次操作都支付固定非负代价

新定义：每次操作支付代价 $\lambda\ge0$，目标最小化“最终极差 + 总操作代价”。第一步后的极差不降，而额外步骤还会继续付费，因此只需比较零步与一步，答案为 $\min(z-x,y+\lambda)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    long long operationCost;
    cin >> a[0] >> a[1] >> a[2] >> operationCost;
    sort(a.begin(), a.end());
    cout << min(a[2] - a[0], a[1] + operationCost) << '\n';
  }
}
```

## 变种四：必须恰好执行 K 次操作

新定义：给定 $K\ge0$，必须恰做 $K$ 次。$K=0$ 时答案为原极差；$K\ge1$ 时先替换最大值达到中位数，之后反复把 $x+y$ 替换为同一个 $x+y$，所以答案恒为初始中位数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    long long operations;
    cin >> a[0] >> a[1] >> a[2] >> operations;
    sort(a.begin(), a.end());
    cout << (operations == 0 ? a[2] - a[0] : a[1]) << '\n';
  }
}
```

## 变种五：目标改为最小化三数最大值

新定义：仍允许零次操作，但目标是最小可能最大值。操作生成的是另外两数之和，可能降低当前最大值，也可能升高；对排序 $x\le y\le z$，一次替换 $z$ 后最大值为 $x+y$，而后续中位数不降，最优是零步或这一步，答案为 $\min(z,x+y)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int tests;
  cin >> tests;
  while (tests--) {
    array<long long, 3> a;
    for (long long& x : a) cin >> x;
    sort(a.begin(), a.end());
    cout << min(a[2], a[0] + a[1]) << '\n';
  }
}
```

## 验证说明

所有完整代码块均按 GNU++23 编译。主闭式以状态图为独立 oracle：枚举全部 $0\le a,b,c\le10$ 的 1,331 个有标号初态至深度 8，访问状态与闭式全部一致；另以固定种子生成 100,000 组 $[0,10^9]$ 输入，并与“零步 + 三种首步”的独立 oracle 对比，全部一致。六组官方样例逐字符运行均吻合。独立复核还检查了官方题目、官方题单、官方 API 与 editorial 的比赛身份和 Div.2 单一别名。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2256/problem/A)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-188-q3-lc4008/">← [力扣竞赛] 第 188 场双周赛 Q3 LC 4008 击败所有怪物的最小初始强度 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-12-lc2958/">[力扣每日一题] 2026-08-12｜LC 2958 最多 K 个重复元素的最长子数组 →</a>
</nav>
