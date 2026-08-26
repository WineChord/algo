---
title: "[codeforces] CF Educational Round 193 Div.2 C Sum of Distinct Values in a Matrix"
---

# [codeforces] CF Educational Round 193 Div.2 C Sum of Distinct Values in a Matrix

<p class="daily-archive-kicker">2026-08-27 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-27 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=043102da72da9d3e2bde56a9addf3fb1f4e222637d93adc3e2c56ea2887affc0 -->
[Codeforces 2253C — Sum of Distinct Values in a Matrix（官方英文题面）](https://codeforces.com/contest/2253/problem/C)

## 官方来源与元数据

- 来源：Educational Codeforces Round 193 (Rated for Div. 2)，Div.2 C
- Contest ID：2253
- 官方 rating：1500
- 官方 points：未知（官方 API 未提供）
- 官方 tags：`greedy`、`sortings`、`two pointers`
- 时间限制：2 秒
- 内存限制：512 MB
- 题面入口：[Codeforces 官方题面](https://codeforces.com/contest/2253/problem/C)
- 许可说明：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)

下列英文题面层依据 Codeforces 官方页面呈现，保留完整任务定义、输入输出、约束、样例和官方说明；与输入、输出及判题契约无关的实现文字不属于题意。

## Complete English statement

You are given an $n\times m$ matrix whose entries are initially all zero. You are also given two strictly increasing arrays of positive integers,

$$
a=[a_1,a_2,\ldots,a_x],\qquad b=[b_1,b_2,\ldots,b_y].
$$

You may perform any number of operations, including zero. An operation is one of the following:

- choose a value $c$ from array $a$ and choose one row, then set every entry of that row to $c$;
- choose a value $d$ from array $b$ and choose one column, then set every entry of that column to $d$.

Operations may be performed in any order. The same row, column, or chosen value may be used more than once.

The cost of a matrix is the sum of all distinct values that occur in at least one cell. Find the maximum possible cost.

### Input

The first line contains the number of test cases $t$. Each test case contains:

```text
n m x y
a_1 a_2 ... a_x
b_1 b_2 ... b_y
```

### Output

For every test case, print one integer: the maximum attainable matrix cost.

### Constraints

- $1\le t\le 10^4$
- $1\le n,m\le 10^5$
- $1\le x,y\le n+m$
- $1\le a_1<a_2<\cdots<a_x\le n+m$
- $1\le b_1<b_2<\cdots<b_y\le n+m$
- the sum of $n$ over all test cases is at most $10^5$
- the sum of $m$ over all test cases is at most $10^5$

### Official sample

```text
Input
7
1 3 3 3
1 2 3
1 2 3
2 2 2 2
1 4
2 3
2 2 1 1
1
1
4 1 1 5
5
1 2 3 4 5
1 1 2 2
1 2
1 2
7 2 9 1
1 2 3 4 5 6 7 8 9
9
9 9 12 12
1 3 4 6 7 9 10 12 13 15 16 18
2 3 5 6 8 9 11 12 14 15 17 18

Output
6
9
1
9
2
44
170
```

In the first test case, assign `3` to the only row, then assign `1` and `2` to two columns. The final matrix contains `1`, `2`, and `3`, so its cost is `6`. In the second test case, assign `2` and `3` to the columns, then assign `4` to one row; the distinct values are `2`, `3`, and `4`, for cost `9`.

## 中文题意解释

行操作只能写入数组 `a` 中的值，列操作只能写入数组 `b` 中的值；后执行的操作会覆盖交叉单元格。目标不是最大化矩阵元素总和，而是最大化最终至少出现一次的不同数值之和。

把一个数按来源分为三类：只在 `a`、只在 `b`、同时在两者。真正的核心是判断一组不同值能否各自在最终矩阵中留下至少一个单元格，而不是模拟所有操作次序。

## 最优结论与推荐记忆方案

设选中的不同值集合为 $S$，并记

$$
A_0=A\setminus B,\qquad B_0=B\setminus A.
$$

$S$ 可实现当且仅当：

$$
|S\cap A_0|\le n,\qquad |S\cap B_0|\le m,\qquad |S|\le n+m-1.
$$

所有值都为正，因此把 $A\cup B$ 从大到小扫描：公共值只占总数配额；`A-only` 值同时占总数和行专属配额；`B-only` 值同时占总数和列专属配额。当前值若不违反三条配额就立刻选取。

两个输入数组已严格递增，可用双指针从末尾线性合并。时间复杂度为 $O(x+y)$，额外空间复杂度为 $O(1)$，答案使用 `long long`。

推荐记住：**先证明可实现集合由“两个互斥子配额 + 一个全局配额”刻画，再按权值降序做层级配额贪心**。矩阵操作只是证明配额充分性的构造外壳。

## 约束推导、可实现集合与溢出

### 为什么每个独占值需要一条对应方向的线

一个只在 `a` 中的值若最终出现，必然来自某一行最后一次有效写入；同一行的最终行操作至多贡献一个不同值，因此这类值最多有 $n$ 个。只在 `b` 中的值同理最多有 $m$ 个。公共值可以任选一条仍有容量的行或列承载。

### 为什么总数最多是 $n+m-1$

假设能保留 $n+m$ 个不同的正值，那么每一行和每一列都必须各自贡献一个不同值。考察这些行、列各自最后一次写入中最早发生的那个操作。若它是行操作，则所有列的最后操作都更晚，会覆盖该行的每个单元格；它写入的值最终完全消失。列操作对称。于是 $n+m$ 个不同值不可能全部保留，总数上限为 $n+m-1$。

### 为什么三条配额已经充分

先把 `A-only` 值分配给不同的行，把 `B-only` 值分配给不同的列；再把公共值任意放入剩余行列容量。三条不等式保证容量足够，并且至少有一条行或列未使用。

- 若有未使用列：先执行所有选中行操作，再执行所有选中列操作。每个行值在未使用列中保留，每个列值在其整列中出现。
- 若所有列都使用：由总数上限必有未使用行。先执行所有列操作，再执行所有行操作。列值在未使用行中保留，行值在各自行中出现。

因此所有选中值都能同时出现。

### 整数范围

不同值最多 $n+m-1\le 2\times 10^5-1$ 个，每个值最多 $n+m\le2\times10^5$，总和可达约 $4\times10^{10}$，必须使用 64 位整数。

## 官方样例手推

第二组中 $n=m=2$，`a = [1,4]`，`b = [2,3]`。四个值都为独占值，但全局上限是 $n+m-1=3$。从大到小选 `4`、`3`、`2`，总和为 $9$；值 `1` 因总数配额已满而舍弃。执行两列写入 `2,3`，再把一行写成 `4`，三者都保留。

第四组中 $n=4,m=1$，值 `5` 同时属于两侧，而 `1,2,3,4` 只属于 `b`。列专属配额只有 $1$，因此可选公共值 `5` 和最大的一个列独占值 `4`，答案为 $9$。

第六组中 `9` 是公共值，`1..8` 只在 `a`。全局上限为 $8$，行专属配额为 $7$；选择公共值 `9` 与最大的七个行独占值 `8..2`，和为 $44$。

## 解法一：枚举不同值子集

对很小的并集，可以递归枚举每个值选或不选，并用三条充要配额检查可行性。这是正确 oracle，但并集规模可达 $4\times10^5$，指数复杂度无法用于正式约束。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Item {
  int value;
  int type;
};
long long dfs(const vector<Item>& items, int index, int n, int m, int total, int onlyA, int onlyB) {
  if (index == static_cast<int>(items.size()))
    return 0;
  long long best = dfs(items, index + 1, n, m, total, onlyA, onlyB);
  const Item& item = items[index];
  bool allowed = total < n + m - 1;
  if (item.type == 1)
    allowed = allowed && onlyA < n;
  if (item.type == 2)
    allowed = allowed && onlyB < m;
  if (allowed) {
    long long take = item.value + dfs(items, index + 1, n, m, total + 1, onlyA + (item.type == 1),
                                    onlyB + (item.type == 2));
    best = max(best, take);
  }
  return best;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, x, y;
  cin >> n >> m >> x >> y;
  vector<int> a(x), b(y);
  for (int& value : a)
    cin >> value;
  for (int& value : b)
    cin >> value;
  vector<Item> items;
  int i = 0, j = 0;
  while (i < x || j < y) {
    if (j == y || (i < x && a[i] < b[j])) {
      items.push_back({a[i++], 1});
    } else if (i == x || b[j] < a[i]) {
      items.push_back({b[j++], 2});
    } else {
      items.push_back({a[i], 3});
      ++i;
      ++j;
    }
  }
  cout << dfs(items, 0, n, m, 0, 0, 0) << '\n';
}
```

时间复杂度为 $O(2^{|A\cup B|})$，递归空间为 $O(|A\cup B|)$。瓶颈是重复比较大量只差一个低价值元素的子集。

## 从子集枚举到降序贪心

三条可行性约束只关心元素类别和已用配额，不关心选取顺序。因为所有元素权重就是正的数值：

1. 全局配额满时，当前值小于所有已处理并被选中的值，替换不会增优。
2. 行专属配额满时，当前 `A-only` 值小于已选的 $n$ 个 `A-only` 值；任何包含它的可行解都必须舍弃其中至少一个更大值。
3. 列专属配额同理。
4. 公共值不占专属配额，只要全局配额未满就应选。

因此降序扫描时的每个拒绝都有不可改善的配额证据，无需动态规划。

## 最佳实用解：双指针合并与层级配额贪心

### 算法

1. 指针 `i`、`j` 分别从 `a`、`b` 的末尾开始。
2. 较大的末尾值是当前并集最大值；若相等，它是公共值并同时移动两指针。
3. 在全局配额未满时：公共值直接选；`A-only` 还要求行专属计数小于 $n$；`B-only` 还要求列专属计数小于 $m$。
4. 累加所有被选值，直到两个数组扫描完。

### 正确性证明

**引理 1**：集合 $S$ 可实现当且仅当满足三条配额不等式。

**证明**：必要性来自每个独占值需要不同的对应方向线，以及最早最终操作导致总数至多 $n+m-1$。充分性由“分配到不同线 + 至少一条未用线 + 按未用线方向安排操作次序”的构造成立。证毕。

**引理 2**：贪心拒绝一个 `A-only` 值时，不存在通过选它而得到更大总和的可行解。

**证明**：若全局配额已满，已选值都不小于当前值；任何加入都需删去一个不小的值。否则只能是行专属配额已满，已选中已有 $n$ 个更大的 `A-only` 值。根据引理 1，任何包含当前值的可行集合必须删掉至少一个这些更大值，仍不增优。证毕。

**引理 3**：对 `B-only` 值的拒绝同样安全；公共值只在全局配额满时被拒绝，也同样安全。

**定理**：降序贪心得到最大可能成本。

**证明**：从任意最优解出发，按扫描顺序逐项用引理 2、3 的交换把它调整为包含全部贪心选择且不降低总和。扫描结束时得到与贪心相同的选择，总和最优；再由引理 1，它必可实现。证毕。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int t;
  cin >> t;
  while (t--) {
    int n, m, x, y;
    cin >> n >> m >> x >> y;
    vector<int> a(x), b(y);
    for (int& value : a)
      cin >> value;
    for (int& value : b)
      cin >> value;
    int i = x - 1, j = y - 1;
    int used = 0, onlyA = 0, onlyB = 0;
    int limit = n + m - 1;
    long long answer = 0;
    while (i >= 0 || j >= 0) {
      int value, type;
      if (j < 0 || (i >= 0 && a[i] > b[j])) {
        value = a[i--];
        type = 1;
      } else if (i < 0 || b[j] > a[i]) {
        value = b[j--];
        type = 2;
      } else {
        value = a[i];
        type = 3;
        --i;
        --j;
      }
      bool take = used < limit;
      if (type == 1)
        take = take && onlyA < n;
      if (type == 2)
        take = take && onlyB < m;
      if (!take)
        continue;
      answer += value;
      ++used;
      onlyA += type == 1;
      onlyB += type == 2;
    }
    cout << answer << '\n';
  }
}
```

## 复杂度与实现边界

- 两指针各自只减小，时间复杂度为 $O(x+y)$。
- 除输入数组外只用常数状态，额外空间复杂度为 $O(1)$。
- 答案必须用 `long long`；配额、下标和值本身可用 `int`。
- 两数组各自严格递增，所以相等时只需同时移动一次；公共值不能重复计入成本。
- 初始值 `0` 即使保留也不增加成本，不需要作为候选。

## 同阶与替代方案比较

可以显式构造三类值，分别排序，再用最大堆反复取当前最大可行值，复杂度为 $O((x+y)\log(x+y))$，证明仍依赖同一配额结构。由于输入已经排序，双指针直接得到全局降序，常数更小、额外空间更少。

也可把可行集合视为一个层级配额系统：`A-only`、`B-only` 是互斥子集合，总集合再受一个上限。标准最大权独立集贪心解释很短，但竞赛实现只需保留三条计数，不必引入抽象数据结构。

## 常见错误

- 把公共值同时占用行、列两个配额；它只需由一条线承载。
- 认为最多能保留 $n+m$ 个值，忽略最早最终操作必被全部异向线覆盖。
- 只取 `a` 最大的 $n$ 个和 `b` 最大的 $m$ 个，再简单去重；这可能超过全局 $n+m-1$ 配额。
- 用 `int` 累加，最大答案会溢出 32 位。
- 把官方 rating `1500` 写成 points；官方 API 的 points 字段缺失。
- 忽略数组严格递增，额外做不必要的去重或把公共值算两次。

## 可复现验证

小规模可枚举每条行、列最终使用哪个值或不使用，并枚举这些最终操作的所有相对顺序，直接构造矩阵后计算不同值之和；将其作为 oracle，与贪心比较。定向覆盖七个官方样例、$n=m=1$、集合完全相同、完全不交、某一侧容量为 $1$、公共值很多以及答案超过 32 位的情形。

## Follow-up 与约束变种

### 变种一：还要输出一组实现最优值的操作

新定义：除最大成本外，还要输出一组行列操作。先按主算法保存选中的值，再把独占值和公共值分配到不同线。若有未用列，先写行再写列；否则必有未用行，先写列再写行。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Pick {
  int value;
  int type;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, x, y;
  cin >> n >> m >> x >> y;
  vector<int> a(x), b(y);
  for (int& value : a)
    cin >> value;
  for (int& value : b)
    cin >> value;
  vector<Pick> chosen;
  int i = x - 1, j = y - 1, onlyA = 0, onlyB = 0;
  while ((i >= 0 || j >= 0) && chosen.size() < static_cast<size_t>(n + m - 1)) {
    Pick item;
    if (j < 0 || (i >= 0 && a[i] > b[j]))
      item = {a[i--], 1};
    else if (i < 0 || b[j] > a[i])
      item = {b[j--], 2};
    else {
      item = {a[i], 3};
      --i;
      --j;
    }
    if (item.type == 1 && onlyA == n)
      continue;
    if (item.type == 2 && onlyB == m)
      continue;
    chosen.push_back(item);
    onlyA += item.type == 1;
    onlyB += item.type == 2;
  }
  vector<int> rows, columns;
  for (Pick item : chosen) {
    if (item.type == 1)
      rows.push_back(item.value);
    else if (item.type == 2)
      columns.push_back(item.value);
    else if (rows.size() < static_cast<size_t>(n))
      rows.push_back(item.value);
    else
      columns.push_back(item.value);
  }
  long long sum = 0;
  for (Pick item : chosen)
    sum += item.value;
  cout << sum << '\n' << chosen.size() << '\n';
  if (columns.size() < static_cast<size_t>(m)) {
    for (int r = 0; r < static_cast<int>(rows.size()); ++r) {
      cout << "R " << r + 1 << ' ' << rows[r] << '\n';
    }
    for (int c = 0; c < static_cast<int>(columns.size()); ++c) {
      cout << "C " << c + 1 << ' ' << columns[c] << '\n';
    }
  } else {
    for (int c = 0; c < static_cast<int>(columns.size()); ++c) {
      cout << "C " << c + 1 << ' ' << columns[c] << '\n';
    }
    for (int r = 0; r < static_cast<int>(rows.size()); ++r) {
      cout << "R " << r + 1 << ' ' << rows[r] << '\n';
    }
  }
}
```

选择仍为 $O(x+y)$；输出操作数为 $O(n+m)$，额外空间为 $O(n+m)$。

### 变种二：每个候选有独立收益，收益可为负

新定义：值标签不再等于收益，每个候选给出可用方向掩码和权重。可行性配额不变，但应按权重降序，并跳过非正收益；标签重复已在输入层合并成一个候选。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Item {
  long long weight;
  int mask;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, k;
  cin >> n >> m >> k;
  vector<Item> items(k);
  for (Item& item : items)
    cin >> item.weight >> item.mask;
  sort(
    items.begin(), items.end(), [](const Item& p, const Item& q) { return p.weight > q.weight; });
  int total = 0, onlyA = 0, onlyB = 0;
  long long answer = 0;
  for (Item item : items) {
    if (item.weight <= 0 || total == n + m - 1)
      break;
    if (item.mask == 1 && onlyA == n)
      continue;
    if (item.mask == 2 && onlyB == m)
      continue;
    answer += item.weight;
    ++total;
    onlyA += item.mask == 1;
    onlyB += item.mask == 2;
  }
  cout << answer << '\n';
}
```

时间复杂度为 $O(k\log k)$，额外空间为 $O(k)$。若权重可以相同，任意同权顺序都不影响最大收益。

### 变种三：必须恰好保留 $K$ 个不同值

新定义：要求最终恰好出现 $K$ 个给定正值；若不可能输出 `-1`，否则最大化它们的和。把全局上限改为 $K$，仍按值降序接受可行候选；最后不足 $K$ 才无解。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Item {
  int value;
  int type;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, k, q;
  cin >> n >> m >> k >> q;
  vector<Item> items(q);
  for (Item& item : items)
    cin >> item.value >> item.type;
  sort(items.begin(), items.end(), [](const Item& p, const Item& r) { return p.value > r.value; });
  if (k > n + m - 1) {
    cout << -1 << '\n';
    return 0;
  }
  int total = 0, onlyA = 0, onlyB = 0;
  long long answer = 0;
  for (Item item : items) {
    if (total == k)
      break;
    if (item.type == 1 && onlyA == n)
      continue;
    if (item.type == 2 && onlyB == m)
      continue;
    answer += item.value;
    ++total;
    onlyA += item.type == 1;
    onlyB += item.type == 2;
  }
  cout << (total == k ? answer : -1) << '\n';
}
```

排序后时间复杂度为 $O(q\log q)$。若候选已按值递减给出，可降到 $O(q)$。

### 变种四：操作总数至多为 $Q$

新定义：最多执行 $Q$ 次行列写入。每个保留的不同值至少需要一条最终线操作，因此全局配额变为 $\min(Q,n+m-1)$；两个方向专属配额不变，主贪心只需替换上限。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Item {
  int value;
  int type;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q, count;
  cin >> n >> m >> q >> count;
  vector<Item> items(count);
  for (Item& item : items)
    cin >> item.value >> item.type;
  sort(items.begin(), items.end(), [](const Item& p, const Item& r) { return p.value > r.value; });
  int limit = min(q, n + m - 1);
  int used = 0, onlyA = 0, onlyB = 0;
  long long answer = 0;
  for (Item item : items) {
    if (used == limit)
      break;
    if (item.type == 1 && onlyA == n)
      continue;
    if (item.type == 2 && onlyB == m)
      continue;
    answer += item.value;
    ++used;
    onlyA += item.type == 1;
    onlyB += item.type == 2;
  }
  cout << answer << '\n';
}
```

时间复杂度为 $O(k\log k)$，其中 $k$ 是候选数；若输入保持递增并按来源给出，可继续使用双指针做到线性。

## 来源

- [Codeforces 2253C 官方题面](https://codeforces.com/contest/2253/problem/C)
- [Educational Codeforces Round 193](https://codeforces.com/contest/2253)
- [Codeforces API](https://codeforces.com/apiHelp)
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2253/problem/C)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-516-q2-lc4031/">← [力扣竞赛] 第 516 场周赛 Q2 LC 4031 找到所有数组中消失的数字 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-27-lc3720/">[力扣每日一题] 2026-08-27｜LC 3720 大于目标字符串的最小字典序排列 →</a>
</nav>
