---
title: "[atcoder] ARC227 B Know Your Place"
---

# [atcoder] ARC227 B Know Your Place

<p class="daily-archive-kicker">2026-08-18 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-18 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=e4f9465bfb3dcdc16094d3413c585e76412958c910bb879b43b15a41e4f1ff1d -->
[Official problem: ARC227 B — Know Your Place](https://atcoder.jp/contests/arc227/tasks/arc227_b?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227）。
- 题目：B — Know Your Place；任务 slug 为 `arc227_b`。
- 官方分值：500 分；AtCoder 未发布单题官方难度。
- 比赛 rated 范围：1200–2799。
- AtCoder Problems 社区估算难度：1043，核对于 2026-08-18；这不是 AtCoder 官方难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是模型逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)仍是权威来源。

## Complete English statement

You are given a sequence of $N$ non-negative integers
$A=(A_1,A_2,\ldots,A_N)$. Determine whether its elements can be rearranged into a sequence
$B=(B_1,B_2,\ldots,B_N)$ satisfying the following condition for every index $i$:

$$
B_i=\#\{j\mid 1\le j<i,\ B_j<B_i\}.
$$

In words, each value $B_i$ must equal the number of earlier elements that are strictly smaller than it.
If such a rearrangement exists, construct one. If several rearrangements satisfy the condition, any one
of them may be printed.

### Input

The input is given in the following form:

```text
N
A_1 A_2 ... A_N
```

### Output

If no required rearrangement exists, print:

```text
No
```

Otherwise print `Yes` on the first line and one valid sequence on the second line:

```text
Yes
B_1 B_2 ... B_N
```

### Constraints

- $1\le N\le5\times10^5$.
- $0\le A_i<N$.
- Every input value is an integer.

### Official samples

Sample 1:

```text
Input
4
3 0 1 0

Output
Yes
0 1 0 3
```

The numbers of strictly smaller preceding elements are respectively $0,1,0,3$, exactly matching the
four printed values.

Sample 2:

```text
Input
3
0 2 2

Output
No
```

There is only one element smaller than 2 in the entire multiset, so neither copy of 2 can have two
strictly smaller predecessors.

Sample 3:

```text
Input
7
4 1 6 0 4 3 1

Output
Yes
0 1 1 3 4 4 6
```

The numbers of strictly smaller preceding elements are $0,1,1,3,4,4,6$, so the displayed sequence is
valid.

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/arc227/tasks/arc227_b?lang=en) remains the normative
source; reuse is subject to the [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en).

## 中文解释与题解

题目要求把同一个多重集重新排列，使每个数值恰好等于它左侧严格更小元素的数量。这里的
“严格”很关键：相同值不会互相增加计数。

## 约束推导与可行性条件

记值 $x$ 的频次为 $c_x$，比 $x$ 小的元素总数为

$$
P_x=\sum_{v=0}^{x-1}c_v.
$$

若 $c_x>0$，任意一个值为 $x$ 的元素都需要在左侧看到 $x$ 个更小元素，而整个多重集中
一共只有 $P_x$ 个这样的元素，所以必要条件是 $P_x\ge x$。

这个条件也充分。按最大值归纳：取当前最大值 $X$，先递归构造所有更小值；因
$P_X\ge X$，可以把所有 $X$ 插入到这个序列的第 $X$ 个元素之后。它们左侧恰有 $X$ 个
更小值，同值副本不互相计数；加入更大值也不会改变较小元素的计数。

若把数组排序为零基序列 $a_0\le a_1\le\cdots\le a_{N-1}$，上述条件等价于
$a_i\le i$ 对所有 $i$ 成立。但排序结果本身不一定是合法答案：样例 1 排序后为
`0 0 1 3`，其中值 1 的左侧只有一个位置却没有更小值。

$N$ 可达 $5\times10^5$，$O(N^2)$ 插入会超时，需要线性或 $O(N\log N)$ 构造。
所有频次、下标和答案都不超过 $N$，`int` 足够。

## 样例手推与边界

样例 1 的频次为 $c_0=2,c_1=1,c_3=1$。构造过程如下：

1. 当前长度 0，有值 0：立即输出一个 0，把另一个 0 暂存。
2. 当前长度 1，有值 1：立即输出 1。
3. 当前长度 2 没有值 2：取出最近暂存的 0，得到 `0 1 0`。
4. 当前长度 3 有值 3：输出 3，得到 `0 1 0 3`。

- 没有 0：第一个位置左侧计数只能是 0，立即无解。
- 多个 0：第一个 0 输出后，其余副本必须等待；连续输出第二个 0 仍合法，但可能阻塞随后
  必须在长度 1 出现的值 1，所以要遵守统一栈策略。
- 某个值 $x$ 出现多次：第一个副本在答案长度恰为 $x$ 时引入，其余副本不应改变其更小
  前驱数。
- 值域有空洞：若当前长度没有对应新值，可以用最近暂存的副本填充；两者都没有则无解。
- 样例 2 中 $P_2=1<2$，因此无论怎样排列都不可能成功。

## 解法一：枚举所有不同排列

把数组排序后用 `next_permutation` 枚举每个不同排列，逐位置扫描左侧并验证定义。它覆盖
所有可能答案，因此是可靠的小规模 oracle；最坏时间 $O(N!\,N^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool valid(const vector<int>& order) {
  int n = order.size();
  for (int i = 0; i < n; ++i) {
    int smaller = 0;
    for (int j = 0; j < i; ++j) smaller += order[j] < order[i];
    if (smaller != order[i]) return false;
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  sort(values.begin(), values.end());
  do {
    if (!valid(values)) continue;
    cout << "Yes\n";
    for (int i = 0; i < n; ++i) {
      if (i > 0) cout << ' ';
      cout << values[i];
    }
    cout << '\n';
    return 0;
  } while (next_permutation(values.begin(), values.end()));
  cout << "No\n";
  return 0;
}
```

额外空间为 $O(N)$。阶乘级枚举只能用于很小的 $N$，瓶颈是重复尝试本可由频次直接排除的
顺序。

## 解法二：按值递增插入

根据充分性证明，从小到大处理值 $x$。当前序列全部由更小值组成；若长度不足 $x$ 就无解，
否则在第 $x$ 个元素之后插入全部 $x$。这会直接构造正确答案，但 `vector` 中间插入会搬移
后缀，最坏为 $O(N^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> count(n);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++count[value];
  }
  vector<int> answer;
  for (int value = 0; value < n; ++value) {
    if (count[value] == 0) continue;
    if (static_cast<int>(answer.size()) < value) {
      cout << "No\n";
      return 0;
    }
    answer.insert(answer.begin() + value, count[value], value);
  }
  cout << "Yes\n";
  for (int i = 0; i < n; ++i) {
    if (i > 0) cout << ' ';
    cout << answer[i];
  }
  cout << '\n';
  return 0;
}
```

## 从二次插入到线性构造

把“在位置 $x$ 插入一组 $x$”改成在线决定答案。设当前答案长度为 $L$：

- 若多重集中还有值 $L$，它必须现在首次出现；先输出一个，把其余副本压入栈。
- 否则用栈顶副本填充当前位置。
- 两者都没有时，不可能继续。

为什么必须优先输出新值 $L$？若先输出旧副本，答案长度就超过 $L$，值 $L$ 再出现时会
至少看到 $L+1$ 个前驱，无法满足定义。为什么暂存区必须是栈？一个值 $x$ 暂存后，新进入
栈的值都比 $x$ 大；后进先出可保证 $x$ 等待期间只跨过不小于它的值，其严格更小前驱数
始终保持为 $x$。若使用队列，较小旧值可能过早弹出，反而让较大的待放值多看到一个更小
前驱。

## 最佳实用解：频次加后进先出栈

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> count(n);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++count[value];
  }
  vector<int> pending;
  vector<int> answer;
  pending.reserve(n);
  answer.reserve(n);
  for (int length = 0; length < n; ++length) {
    if (count[length] > 0) {
      answer.push_back(length);
      for (int copy = 1; copy < count[length]; ++copy) {
        pending.push_back(length);
      }
      count[length] = 0;
    } else if (!pending.empty()) {
      answer.push_back(pending.back());
      pending.pop_back();
    } else {
      cout << "No\n";
      return 0;
    }
  }
  cout << "Yes\n";
  for (int i = 0; i < n; ++i) {
    if (i > 0) cout << ' ';
    cout << answer[i];
  }
  cout << '\n';
  return 0;
}
```

每个元素只进入答案一次，暂存副本各压栈、弹栈至多一次，时间复杂度 $O(N)$，额外空间
$O(N)$。读取全部输入本身需要 $\Omega(N)$，因此时间复杂度最优。

### 正确性证明

当值 $x$ 在答案长度恰为 $x$ 时首次输出，此前所有已引入的值都小于 $x$，所以它左侧
恰有 $x$ 个更小元素。其余副本被压栈。此后压在它上方的值都是在更晚长度首次引入的，
因此都大于 $x$；栈顶副本弹出时，等待期间新增的元素没有一个严格小于它，它看到的更小
前驱数仍是首次引入时的 $x$。

如果当前长度 $L$ 存在值 $L$，任何合法序列都必须现在引入它，算法的优先选择是强制的。
若不存在，合法填充只能来自已经引入的副本；其中栈顶是最大的待放值，只有先放它才不会
让它跨过更小副本。若连栈也为空，就没有任何值能在当前位置满足定义。故算法每一步都选择
唯一可延续的值；若完成则答案正确，若失败则无解。

## 同阶方案与推荐

可先检查 $P_x\ge x$，再用链表或隐式平衡树实现“按位置插入”，达到 $O(N\log N)$；也可
设计线段树维护动态可选值。它们证明负担、常数和代码长度都更大。栈解直接利用首次引入时刻
和 LIFO 不变量，达到最优 $O(N)$，应优先记忆。

## 易错点

- 把严格小于误成小于等于，错误地让同值副本互相贡献。
- 把必要条件写成 $P_x=x$；正确条件允许 $P_x>x$。
- 认为排好序的数组就是答案；排序只能用来检查 $a_i\le i$。
- 当前长度存在同值时先弹旧栈顶，导致错过该值唯一的首次引入时刻。
- 用队列保存副本；必须后进先出。
- 在 `vector` 中反复按位置插入却声称线性复杂度。

## 验证说明

暴力排列、递增插入和线性栈三份程序均以 GNU++23 编译并通过三组官方样例。另对
$N\le8$ 的全部小规模多重集，以完整排列回溯为 oracle，逐一比较可行性并复核构造序列
每个位置的严格更小前驱数；线性构造结果全部一致。

## 变种一：只判断可行性，不构造

新定义：只输出是否存在答案。排序后条件等价于每个零基位置满足 $a_i\le i$；若某个
$a_i>i$，比它小的元素总数不足。时间 $O(N\log N)$，空间取决于排序实现。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  sort(values.begin(), values.end());
  for (int i = 0; i < n; ++i) {
    if (values[i] > i) {
      cout << "No\n";
      return 0;
    }
  }
  cout << "Yes\n";
  return 0;
}
```

## 变种二：把等号放宽为不等号

新定义：要求 $B_i\le\#\{j<i\mid B_j<B_i\}$。原栈的精确时刻不再必要。仍需
$P_x\ge x$，并且把数组升序输出即可：每个 $x$ 左侧已经包含全部 $P_x$ 个更小值。
时间 $O(N\log N)$，额外空间由排序决定。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) cin >> value;
  sort(values.begin(), values.end());
  for (int i = 0; i < n; ++i) {
    if (values[i] > i) {
      cout << "No\n";
      return 0;
    }
  }
  cout << "Yes\n";
  for (int i = 0; i < n; ++i) {
    if (i > 0) cout << ' ';
    cout << values[i];
  }
  cout << '\n';
  return 0;
}
```

## 变种三：相同数值的副本带有不同标签

新定义：每个副本可区分，问合法标签排列数，答案对 $10^9+7$ 取模。原值序列若可行则由
强制选择唯一确定；同值副本可在其所有位置任意置换，因此答案是 $\prod_x c_x!$，否则为
0。时间 $O(N)$，空间 $O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  int n;
  cin >> n;
  vector<int> count(n);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++count[value];
  }
  int smaller = 0;
  long long ways = 1;
  for (int value = 0; value < n; ++value) {
    if (count[value] > 0 && smaller < value) {
      cout << 0 << '\n';
      return 0;
    }
    for (int factor = 1; factor <= count[value]; ++factor) {
      ways = ways * factor % mod;
    }
    smaller += count[value];
  }
  cout << ways << '\n';
  return 0;
}
```

## 变种四：验证给定排列

新定义：输入原多重集与候选序列，验证候选是否既是重排，又满足每个位置的等式。先比较
频次，再用树状数组统计已出现值中严格小于当前值的数量。时间 $O(N\log N)$，空间
$O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  vector<int> tree;
public:
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      ++tree[index];
    }
  }
  int prefix(int index) const {
    int result = 0;
    for (++index; index > 0; index -= index & -index) result += tree[index];
    return result;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> balance(n);
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    ++balance[value];
  }
  vector<int> candidate(n);
  for (int& value : candidate) {
    cin >> value;
    if (value < 0 || value >= n) {
      cout << "No\n";
      return 0;
    }
    --balance[value];
  }
  if (any_of(balance.begin(), balance.end(), [](int value) { return value != 0; })) {
    cout << "No\n";
    return 0;
  }
  Fenwick seen(n);
  for (int value : candidate) {
    int smaller = value == 0 ? 0 : seen.prefix(value - 1);
    if (smaller != value) {
      cout << "No\n";
      return 0;
    }
    seen.add(value);
  }
  cout << "Yes\n";
  return 0;
}
```

## 来源

- [AtCoder 官方题面](https://atcoder.jp/contests/arc227/tasks/arc227_b?lang=en)
- [ARC227 官方比赛页](https://atcoder.jp/contests/arc227?lang=en)
- [AtCoder Terms of Service](https://atcoder.jp/tos?lang=en)
- [AtCoder Problems 社区难度模型](https://kenkoooo.com/atcoder/resources/problem-models.json)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_b?lang=en)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-138-lc459/">[力扣 Top 138] LC 459 重复的子字符串 简单 →</a>
</nav>
