---
title: "[atcoder] ARC227 A Fermat Point of Binary Strings"
---

# [atcoder] ARC227 A Fermat Point of Binary Strings

<p class="daily-archive-kicker">2026-08-17 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-17 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=80c2a25a5077ffef48e00b3dd99cd219db7ae3de0e3b86e037921947c3b843b9 -->
[Official problem: ARC227 A - Fermat Point of Binary Strings](https://atcoder.jp/contests/arc227/tasks/arc227_a?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227）。
- 题目：A - Fermat Point of Binary Strings。
- 比赛时间：2026-08-16 21:00–23:00（JST）。
- 官方分值：400 分；比赛 rated 范围：1200–2799。
- 官方难度：AtCoder 未标注。
- 时间限制：2 秒；内存限制：1024 MiB。
- AtCoder Problems 社区估算难度：614，核对于 2026-08-17；这不是 AtCoder 官方难度。
- [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)。

下方英文层是模型逐项阅读官方页面后独立组织的自包含呈现。任务页没有给出题目专属开放
转载许可；官方页面与服务条款仍是权威来源。题面没有理解所必需的图片。

## Complete English statement

A binary string of length $2N$ is called good when it contains exactly $N$ zeros and $N$ ones.

For two good strings $S$ and $T$, define $\operatorname{dist}(S,T)$ as the minimum number of swaps of
adjacent characters needed to transform $S$ into $T$.

You are given three good strings $A$, $B$, and $C$. Among every good string $X$, minimize

$$
\operatorname{dist}(A,X)+\operatorname{dist}(B,X)+\operatorname{dist}(C,X).
$$

Output both the minimum value and one good string $X$ attaining it.

### Input

The input is given from Standard Input in the following format:

```text
N
A
B
C
```

### Output

Let $K$ be the minimum possible sum and let $X$ be a good string attaining it. Output:

```text
K
X
```

If several strings are optimal, any one of them may be printed.

### Constraints

- $1\le N\le2\times10^5$.
- Each of $A$, $B$, and $C$ is a good binary string of length $2N$.
- $N$ is an integer.

### Complete official sample 1

Input:

```text
2
1100
1010
0011
```

Output:

```text
4
1010
```

For $X=1010$, the three distances are $1$, $0$, and $3$, so their sum is $4$; no smaller sum exists.

### Complete official sample 2

Input:

```text
3
101010
101010
101010
```

Output:

```text
0
101010
```

All three inputs are identical, so choosing that same string makes the total distance zero.

## 中文题意解释

三个长度为 $2N$ 的二进制串都恰有 $N$ 个 1。一次操作交换相邻字符。我们要构造另一个
同样平衡的串 $X$，让三个输入串移动到 $X$ 所需的相邻交换总数最小。

把每个串从左到右的 1 的位置依次记为 $p_1,p_2,\ldots,p_N$。相同编号的 1 在任何最优
相邻交换方案中按稳定顺序配对，不会交叉。因此两个串的距离就是对应位置差的绝对值之和；
原问题随即分解为 $N$ 个一维三点中位数问题。

## 约束推导与整数范围

若两个平衡串中第 $k$ 个 1 的位置分别为 $p_k$ 与 $q_k$，则

$$
\operatorname{dist}(S,T)=\sum_{k=1}^{N}|p_k-q_k|.
$$

对输出串第 $k$ 个 1 的位置 $x_k$，目标函数的这一维是

$$
|a_k-x_k|+|b_k-x_k|+|c_k-x_k|,
$$

其最小点是三者中位数。每个输入位置序列都严格递增；三个严格递增序列的逐坐标中位数也
至少递增 1，所以这些独立最优位置自动组成合法的好串，不需要额外的区间 DP。

单项距离至多 $2N-1$，总和可达 $\Theta(N^2)$，当 $N=2\times10^5$ 时会超过 32 位；答案
必须使用 `long long`。位置本身使用 `int` 足够。

## 样例手推与边界

样例 1 中三个 1 位置序列（0 下标）分别是 `[0,1]`、`[0,2]`、`[2,3]`。逐列中位数是
`[0,2]`，对应 `1010`。代价为

$$
(0+0+2)+(1+0+1)=4.
$$

- $N=1$：只需取三个 1 位置的中位数。
- 三个串完全相同：每一维代价都为 0，直接得到原串。
- 某一维有两个位置相同：中位数仍唯一且等于该重复位置。
- 1 全部集中在左侧或右侧：位置差乘以 $N$ 可能很大，但不会超过 64 位。
- 不能按每个字符位做多数表决；逐位多数所得串未必仍恰有 $N$ 个 1。

## 解法一：枚举全部好串作为暴力 oracle

小规模时枚举长度 $2N$ 中所有含 $N$ 个 1 的候选串，直接计算三段距离并保留最优者。它
覆盖所有合法答案，适合验证中位数公式，但候选数为 $\binom{2N}{N}$，无法应对正式约束。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> positions(const string& s) {
  vector<int> answer;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '1') answer.push_back(i);
  }
  return answer;
}
long long distanceTo(const vector<int>& a, const vector<int>& b) {
  long long result = 0;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    result += abs(a[i] - b[i]);
  }
  return result;
}
int main() {
  int n;
  string a, b, c;
  cin >> n >> a >> b >> c;
  vector<int> pa = positions(a);
  vector<int> pb = positions(b);
  vector<int> pc = positions(c);
  string current(2 * n, '0');
  long long best = LLONG_MAX;
  string answer;
  function<void(int, int)> dfs = [&](int index, int left) {
    if (index == 2 * n) {
      if (left != 0) return;
      vector<int> px = positions(current);
      long long value = distanceTo(pa, px) + distanceTo(pb, px) +
          distanceTo(pc, px);
      if (value < best) {
        best = value;
        answer = current;
      }
      return;
    }
    if (2 * n - index > left) dfs(index + 1, left);
    if (left > 0) {
      current[index] = '1';
      dfs(index + 1, left - 1);
      current[index] = '0';
    }
  };
  dfs(0, n);
  cout << best << '\n' << answer << '\n';
}
```

计算一个候选需 $O(N)$，总时间为 $O\!\left(N\binom{2N}{N}\right)$，递归栈与候选串占
$O(N)$ 空间。正式算法必须消除候选串枚举。

## 从暴力到最优：稳定配对与一维中位数

相邻交换不会改变 1 之间的相对次序。把源串第 $k$ 个 1 配到目标串第 $k$ 个 1，可以用
恰好 $|p_k-x_k|$ 次跨越 0 的交换完成；若两条配对线交叉，交换它们的目标不会增大绝对值
和。因此稳定配对同时给出下界与可行方案。

固定 $k$ 后，绝对值和在三点中位数处最小。于是只需扫描三个串、收集各自的 1 位置，再
逐列取中位数并累计代价。重复计算和全局搜索都被消除，复杂度降至输入规模线性。

## 最佳实用解：逐个 1 取位置中位数

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> positions(const string& s) {
  vector<int> answer;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '1') answer.push_back(i);
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  string a, b, c;
  cin >> n >> a >> b >> c;
  vector<int> pa = positions(a);
  vector<int> pb = positions(b);
  vector<int> pc = positions(c);
  string answer(2 * n, '0');
  long long cost = 0;
  for (int k = 0; k < n; ++k) {
    array<int, 3> value{pa[k], pb[k], pc[k]};
    sort(value.begin(), value.end());
    int median = value[1];
    answer[median] = '1';
    cost += median - value[0] + value[2] - median;
  }
  cout << cost << '\n' << answer << '\n';
}
```

时间复杂度 $O(N)$，额外空间 $O(N)$；输出串本身也需要 $O(N)$。三元素排序是常数操作。
这是应优先记忆的方案：先把相邻交换距离改写成第 $k$ 个 1 的位移，再用中位数最小化
$L_1$ 距离。

## 正确性证明

**引理 1：两个好串的相邻交换距离等于对应 1 位置差之和。**

任意一次相邻的 `01` / `10` 交换只让一个 1 移动一格。按从左到右顺序，把第 $k$ 个 1
从 $p_k$ 移到 $q_k$，至少需要 $|p_k-q_k|$ 次移动，故右式是下界。依次稳定移动各个 1
可以达到该下界，所以等式成立。

**引理 2：逐坐标中位数是合法的位置序列。**

对任一输入串都有 $p_{k+1}\ge p_k+1$。把三个第 $k$ 个位置都加 1 后，仍不超过对应的
三个第 $k+1$ 个位置；顺序统计量保持这种逐项不等式，因此
$x_{k+1}\ge x_k+1$。所以中位数位置互异、递增，并且恰能放置 $N$ 个 1。

**引理 3：每个中位数最小化对应维度的绝对值和。**

在三个数排序为 $u\le v\le w$ 后，函数 $|u-x|+|v-x|+|w-x|$ 在 $x<v$ 时仍有向右
下降的净斜率，在 $x>v$ 时有向右上升的净斜率，故唯一最小点是 $v$。

**定理：算法输出全局最优好串。**

由引理 1，总目标是所有 $k$ 的独立绝对值和之和。引理 3 说明算法在每一维都达到下界，
引理 2 又保证这些选择可同时组成合法串，因此总和达到所有好串中的最小值。

## 方案比较与易错点

- 枚举好串定义直接但指数爆炸；中位数法把候选空间完全消掉。
- 逐位多数表决优化的是 Hamming 距离，而且可能破坏 1 的数量，不适用于相邻交换距离。
- 必须配对“第 $k$ 个 1”，不能把每个 1 贪心移动到当前最近的空位。
- 位置采用 0 下标或 1 下标都可以，但计算与构造必须统一。
- 总代价使用 `long long`；`int` 会在极端排列下溢出。
- 输出任意最优串即可，不需要额外追求字典序。

## 验证说明

两组官方样例均通过。对 $1\le N\le4$ 的 61240 组三字符串无序组合，枚举所有候选 $X$
计算真实最小值，并与位置中位数、前缀中位数的代价、输出及最优解唯一性逐项比较；另对
较大随机串用前缀 1 数差公式复核距离。最佳代码和全部变种均以 GNU++23 编译。

## 变种一：只有两个输入串，并求字典序最小的最优串

两点绝对值和在闭区间 $[\min(a_k,b_k),\max(a_k,b_k)]$ 内恒定。二进制字典序更小意味着
尽量晚出现 1，所以每一维取较大的位置；这些位置仍严格递增。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> positions(const string& s) {
  vector<int> result;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '1') result.push_back(i);
  }
  return result;
}
int main() {
  int n;
  string a, b;
  cin >> n >> a >> b;
  vector<int> pa = positions(a);
  vector<int> pb = positions(b);
  string answer(2 * n, '0');
  long long cost = 0;
  for (int k = 0; k < n; ++k) {
    answer[max(pa[k], pb[k])] = '1';
    cost += abs(pa[k] - pb[k]);
  }
  cout << cost << '\n' << answer << '\n';
}
```

时间 $O(N)$、空间 $O(N)$。原来的中位数从单点变成区间；字典序要求决定取区间右端。

## 变种二：给定任意数量的好串

新定义给出 $M$ 个好串，最小化到同一 $X$ 的距离和。每一列取第 $\lfloor(M-1)/2\rfloor$
个顺序统计量；偶数个来源时这是最优区间的左端，仍是合法最优解。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, n;
  cin >> m >> n;
  vector<vector<int>> position(m);
  for (int row = 0; row < m; ++row) {
    string s;
    cin >> s;
    for (int i = 0; i < 2 * n; ++i) {
      if (s[i] == '1') position[row].push_back(i);
    }
  }
  string answer(2 * n, '0');
  long long cost = 0;
  vector<int> value(m);
  for (int k = 0; k < n; ++k) {
    for (int row = 0; row < m; ++row) value[row] = position[row][k];
    nth_element(value.begin(), value.begin() + (m - 1) / 2, value.end());
    int median = value[(m - 1) / 2];
    answer[median] = '1';
    for (int row = 0; row < m; ++row) {
      cost += abs(position[row][k] - median);
    }
  }
  cout << cost << '\n' << answer << '\n';
}
```

期望时间 $O(MN)$，空间 $O(MN)$。固定秩的顺序统计量对严格递增输入序列仍严格递增。

## 变种三：每个来源串带正权重

目标变为 $\sum_j w_j\operatorname{dist}(S_j,X)$。每一维取加权中位数：按位置排序后，
第一个使累计权重至少达到总权重一半的位置即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n;
  cin >> m >> n;
  vector<long long> weight(m);
  for (long long& value : weight) cin >> value;
  vector<vector<int>> position(m);
  for (int row = 0; row < m; ++row) {
    string s;
    cin >> s;
    for (int i = 0; i < 2 * n; ++i) {
      if (s[i] == '1') position[row].push_back(i);
    }
  }
  long long totalWeight = accumulate(weight.begin(), weight.end(), 0LL);
  string answer(2 * n, '0');
  long long cost = 0;
  vector<pair<int, long long>> order(m);
  for (int k = 0; k < n; ++k) {
    for (int row = 0; row < m; ++row) {
      order[row] = {position[row][k], weight[row]};
    }
    sort(order.begin(), order.end());
    long long prefix = 0;
    int median = order.back().first;
    for (auto [positionValue, weightValue] : order) {
      prefix += weightValue;
      if (2 * prefix >= totalWeight) {
        median = positionValue;
        break;
      }
    }
    answer[median] = '1';
    for (int row = 0; row < m; ++row) {
      cost += weight[row] * abs(position[row][k] - median);
    }
  }
  cout << cost << '\n' << answer << '\n';
}
```

时间 $O(NM\log M)$、空间 $O(NM)$。正权重固定不变时，加权分位点同样至少逐列右移 1。

## 变种四：代价改为任意交换次数

若一次可以交换任意两个位置，两个好串的距离是 Hamming 距离的一半。对多个来源求和时，
目标等价于在恰好 $N$ 个位置放 1，并优先选择来源串中 1 出现次数最多的位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, n;
  cin >> m >> n;
  vector<string> strings(m);
  for (string& s : strings) cin >> s;
  vector<pair<int, int>> order;
  for (int i = 0; i < 2 * n; ++i) {
    int ones = 0;
    for (const string& s : strings) ones += s[i] == '1';
    order.push_back({-ones, i});
  }
  sort(order.begin(), order.end());
  string answer(2 * n, '0');
  for (int i = 0; i < n; ++i) answer[order[i].second] = '1';
  long long hamming = 0;
  for (const string& s : strings) {
    for (int i = 0; i < 2 * n; ++i) hamming += s[i] != answer[i];
  }
  cout << hamming / 2 << '\n' << answer << '\n';
}
```

时间 $O(MN+N\log N)$，空间 $O(N)$。原中位数模型失效，因为任意交换不再关心第 $k$ 个
1 的位移；新的稳定结构是每个位置的出现频率与全局“恰选 $N$ 位”约束。

## Reference

- [ARC227 A 官方题面](https://atcoder.jp/contests/arc227/tasks/arc227_a?lang=en)
- [ARC227 官方比赛页](https://atcoder.jp/contests/arc227?lang=en)
- [AtCoder Problems 社区难度数据](https://kenkoooo.com/atcoder/resources/problem-models.json)
- [AtCoder 服务条款](https://atcoder.jp/tos?lang=en)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_a?lang=en)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-137-lc516/">[力扣 Top 137] LC 516 最长回文子序列 中等 →</a>
</nav>
