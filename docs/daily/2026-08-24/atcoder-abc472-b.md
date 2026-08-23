---
title: "[atcoder] ABC472 B Break a Stick"
---

# [atcoder] ABC472 B Break a Stick

<p class="daily-archive-kicker">2026-08-24 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-24 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=374201606981820b2795e51fae6591c3d6cab649cd7ad80ac7ffd3d9c64fc632 -->
[Official problem: AtCoder ABC472 B — Break a Stick](https://atcoder.jp/contests/abc472/tasks/abc472_b?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 472；北京时间 2026-08-22 20:00–21:40；题目：B —
  Break a Stick。
- 官方配点：200；比赛 Rated Range：0–1999。
- AtCoder 官方没有为本题标注难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- [AtCoder Problems 社区模型](https://kenkoooo.com/atcoder/resources/problem-models.json)估算难度：
  -521，抓取于 2026-08-24；这不是 AtCoder 官方难度。
- 题面没有理解所必需的图片。
- 下方英文层是逐项核对官方页面后独立组织的自包含完整呈现，不冒充逐字官方原文；来源与
  使用边界参见 [AtCoder 官方题面](https://atcoder.jp/contests/abc472/tasks/abc472_b?lang=en)
  与 [AtCoder Terms of Service](https://atcoder.jp/tos)。

## Complete English statement

One stick is divided by $N-1$ notches into $N$ consecutive parts. From one end to the other, the
lengths of the parts are $L_1,L_2,\ldots,L_N$.

Choose exactly one of the notches and break the stick there. The two resulting stick lengths are the
sums of the part lengths on the two sides of that notch. The notch width is negligible. Determine
the minimum possible absolute difference between the two resulting lengths.

### Input

The input is given from standard input in the following format:

```text
N
L_1 L_2 ... L_N
```

### Output

Print the minimum possible absolute difference.

### Constraints

- $2\le N\le100$.
- $1\le L_i\le10^5$ for every $i$.
- Every input value is an integer.

### Official samples

Sample 1:

```text
Input
4
5 2 3 8
Output
2
```

At the three notches, the two lengths are respectively $(5,13)$, $(7,11)$, and $(10,8)$, so the
absolute differences are $8,4,2$ and the answer is $2$.

Sample 2:

```text
Input
7
31 41 59 26 53 58 97
Output
51
```

Sample 3:

```text
Input
10
67011 35764 33042 24098 63738 98760 17199 68579 21812 45408
Output
28105
```

Source: [AtCoder ABC472 B](https://atcoder.jp/contests/abc472/tasks/abc472_b?lang=en).

## 中文解释与最优结论

切口只能位于相邻部分之间。设整根棒总长为 $S$，切在第 $i$ 个切口后，左边长度是前缀和
$P_i$，右边长度是 $S-P_i$，差为

$$
|P_i-(S-P_i)|=|2P_i-S|.
$$

先求总和，再从左到右累加前缀并枚举 $N-1$ 个切口即可。时间复杂度 $O(N)$，额外空间
$O(1)$。这是最适合竞赛记忆的方案：把“切成两段”立即改写成“总和减前缀和”。

## 约束推导、溢出与边界

- $N\le100$，即使 $O(N^2)$ 也能通过；但线性写法更直接地消除了对右段的重复求和。
- 总长度至多 $100\times10^5=10^7$，`int` 足够；代码仍使用 `long long`，便于迁移到更大范围。
- 必须选择一个真实切口，所以只枚举 $i=1,2,\ldots,N-1$；不能切在两端得到空棒。
- $N=2$ 时只有一个切口，答案就是 $|L_1-L_2|$。
- 所有 $L_i>0$，前缀和严格递增；原题虽然不需要二分，这一性质会在多询问变种中使用。
- 当 $S$ 为奇数时答案不可能为 0；当存在 $P_i=S/2$ 时答案恰为 0。

## 官方样例手推

样例 1 的总长为 $18$。前缀和依次为 $5,7,10$，对应
$|2P_i-18|=8,4,2$，最小值为 2。第三个切口把棒分成长度 10 与 8 的两段。

下面两段是根据官方样例数据做的独立教学推算；官方只解释了样例 1。

- 样例 2 的总长为 $365$，六个切口的前缀和为 $31,72,131,157,210,268$，差依次为
  $303,221,103,51,55,171$。第 4 个切口得到 $157$ 与 $208$，答案为 51。
- 样例 3 的总长为 $475411$。第 5 个切口得到 $223653$ 与 $251758$，差为 28105；第 6 个
  切口越过一半后差已增至 169415。由于后续正数前缀继续增大，答案就是 28105。

## 解法一：对每个切口重新求两侧总和

枚举切口 $i$，分别扫描 $[0,i)$ 与 $[i,N)$ 求和。每个合法切口都被枚举一次，所以覆盖性
正确。时间复杂度 $O(N^2)$，额外空间 $O(1)$；瓶颈是相邻切口反复累加几乎相同的部分。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> length(n);
  for (long long& value : length) cin >> value;
  long long answer = numeric_limits<long long>::max();
  for (int cut = 1; cut < n; ++cut) {
    long long left = 0;
    long long right = 0;
    for (int i = 0; i < cut; ++i) left += length[i];
    for (int i = cut; i < n; ++i) right += length[i];
    answer = min(answer, abs(left - right));
  }
  cout << answer << '\n';
  return 0;
}
```

## 从重复求和到前缀增量

切口右移一格时，只有一个部分从右段转入左段。先求固定总长 $S$，维护当前左长 $P$；切口
经过 $L_i$ 后只需执行 `P += L_i`，右长永远是 `S - P`。这样每个部分只参与常数次运算。

## 最佳实用解：总和加一次前缀扫描

### 正确性证明

循环处理完 `length[i]` 时，`left` 恰等于前 $i+1$ 个部分之和，因此对应唯一切口
$i+1$。`total - left` 恰是其右侧所有部分之和，算法计算的
`abs(2 * left - total)` 就是该切口的两棒长度差。循环遍历 $i=0$ 到 $N-2$，不重不漏地
覆盖全部合法切口；对这些真实差值取最小，所得必为题目答案。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> length(n);
  long long total = 0;
  for (long long& value : length) {
    cin >> value;
    total += value;
  }
  long long left = 0;
  long long answer = numeric_limits<long long>::max();
  for (int i = 0; i + 1 < n; ++i) {
    left += length[i];
    answer = min(answer, abs(2 * left - total));
  }
  cout << answer << '\n';
  return 0;
}
```

时间复杂度 $O(N)$，额外空间 $O(1)$（不计输入数组；也可边读边存后再扫描）。

## 同阶方案比较与易错点

也可以先构造完整前缀数组，时间 $O(N)$、空间 $O(N)$。本题只需顺序访问，标量前缀更省空间；
若后续有区间询问，则前缀数组更易扩展。竞赛中优先记忆标量扫描。

- 把切口枚举到 `i == n - 1`，相当于让右棒为空。
- 忘记绝对值，或写成 `left - right` 后只取最小。
- 每轮重新计算右段，虽能过本题，却掩盖了可复用的总和结构。
- 用浮点数比较是否接近一半；整数式 $|2P-S|$ 更准确。
- 扩大数据范围后仍用 `int` 计算 `2 * left`，可能先溢出再赋给 `long long`。

## 可复现验证

两份原题程序均以 C++23 编译，并逐项通过三个官方样例、$N=2$、恰好平分、总长为奇数、
全部相等及单个部分远大于其余部分等边界。随机测试将线性解与二次暴力对比，作为本轮独立
oracle 验证。

## Follow-up 与约束变种

### 变种一：输出全部最优切口

新定义：除最小差外，还要输出达到最小差的切口数量及其从 1 开始的编号。原算法仍成立，
只需在得到更优值时清空答案表，得到相同值时追加。时间 $O(N)$，空间 $O(N)$ 用于输出。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> length(n);
  long long total = 0;
  for (long long& value : length) {
    cin >> value;
    total += value;
  }
  long long left = 0;
  long long best = numeric_limits<long long>::max();
  vector<int> cuts;
  for (int i = 0; i + 1 < n; ++i) {
    left += length[i];
    long long difference = abs(2 * left - total);
    if (difference < best) {
      best = difference;
      cuts.clear();
    }
    if (difference == best) cuts.push_back(i + 1);
  }
  cout << best << ' ' << cuts.size() << '\n';
  for (int i = 0; i < static_cast<int>(cuts.size()); ++i) {
    if (i) cout << ' ';
    cout << cuts[i];
  }
  cout << '\n';
  return 0;
}
```

### 变种二：多次静态区间询问

新定义：长度仍全为正，给出 $Q$ 个闭区间 $[l,r]$，每次必须在其中某个相邻部分之间切开，
输出该子棒的最小两段差；保证 $l<r$。完整前缀和严格递增，最优切口的前缀值最接近区间
总和的一半。对 `lower_bound` 的位置及其前驱各检查一次。预处理 $O(N)$，每问 $O(\log N)$，
空间 $O(N)$。

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
  vector<long long> prefix(n + 1);
  for (int i = 1; i <= n; ++i) {
    long long value;
    cin >> value;
    prefix[i] = prefix[i - 1] + value;
  }
  while (q--) {
    int left;
    int right;
    cin >> left >> right;
    long long targetTwice = prefix[left - 1] + prefix[right];
    auto first = prefix.begin() + left;
    auto last = prefix.begin() + right;
    auto position = lower_bound(first, last, (targetTwice + 1) / 2);
    long long answer = numeric_limits<long long>::max();
    if (position != last) answer = min(answer, abs(2 * *position - targetTwice));
    if (position != first) {
      --position;
      answer = min(answer, abs(2 * *position - targetTwice));
    }
    cout << answer << '\n';
  }
  return 0;
}
```

### 变种三：在线修改后询问整根棒

新定义：所有长度保持正数，支持 `1 i v` 修改第 $i$ 段长度，支持 `2` 输出当前整根棒的最小
差。静态前缀失效，但树状数组可维护总和与动态前缀和；利用正数保证前缀严格递增，用树状数组
的二进制提升找到第一个达到一半的位置，再检查相邻合法切口。每次操作 $O(\log N)$，空间
$O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
public:
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index, long long delta) {
    for (; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  long long sum(int index) const {
    long long answer = 0;
    for (; index > 0; index -= index & -index) answer += tree[index];
    return answer;
  }
  int lowerBound(long long target) const {
    int index = 0;
    long long accumulated = 0;
    int step = 1;
    while (step * 2 < static_cast<int>(tree.size())) step *= 2;
    for (; step > 0; step /= 2) {
      int next = index + step;
      if (next < static_cast<int>(tree.size()) && accumulated + tree[next] < target) {
        index = next;
        accumulated += tree[next];
      }
    }
    return index + 1;
  }
private:
  vector<long long> tree;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int q;
  cin >> n >> q;
  vector<long long> length(n + 1);
  Fenwick fenwick(n);
  for (int i = 1; i <= n; ++i) {
    cin >> length[i];
    fenwick.add(i, length[i]);
  }
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int index;
      long long value;
      cin >> index >> value;
      fenwick.add(index, value - length[index]);
      length[index] = value;
    } else {
      long long total = fenwick.sum(n);
      int cut = fenwick.lowerBound((total + 1) / 2);
      long long answer = numeric_limits<long long>::max();
      for (int candidate : {cut - 1, cut}) {
        if (1 <= candidate && candidate < n) {
          answer = min(answer, abs(2 * fenwick.sum(candidate) - total));
        }
      }
      cout << answer << '\n';
    }
  }
  return 0;
}
```

### 变种四：切成恰好 K 个非空连续段

新定义：所有长度仍为正数，把棒切成恰好 $K$ 个非空连续段，最小化最长一段的长度。原题只
枚举一个切口的目标已经失效。二分答案 `limit`；从左到右贪心地让每段尽量长，可得到不超过
`limit` 时所需的最少段数，因而判定是否能再细分成恰好 $K$ 段。确定最优上界后再次扫描，
在下一项会超限或必须为剩余各段各留一项时切开，即可恢复切口。时间
$O(N\log\sum L_i)$，空间 $O(N)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  int k;
  cin >> n >> k;
  vector<long long> length(n);
  long long low = 0;
  long long high = 0;
  for (long long& value : length) {
    cin >> value;
    low = max(low, value);
    high += value;
  }
  auto feasible = [&](long long limit) {
    int pieces = 1;
    long long sum = 0;
    for (long long value : length) {
      if (sum + value > limit) {
        ++pieces;
        sum = value;
      } else {
        sum += value;
      }
    }
    return pieces <= k;
  };
  while (low < high) {
    long long middle = low + (high - low) / 2;
    if (feasible(middle)) {
      high = middle;
    } else {
      low = middle + 1;
    }
  }
  vector<int> cuts;
  long long sum = 0;
  int piecesLeft = k;
  for (int i = 0; i < n; ++i) {
    sum += length[i];
    if (piecesLeft > 1) {
      bool nextOverflows = i + 1 < n && sum + length[i + 1] > low;
      bool mustLeaveOneEach = n - i - 1 == piecesLeft - 1;
      if (nextOverflows || mustLeaveOneEach) {
        cuts.push_back(i + 1);
        sum = 0;
        --piecesLeft;
      }
    }
  }
  cout << low << '\n';
  for (int i = 0; i < static_cast<int>(cuts.size()); ++i) {
    if (i) cout << ' ';
    cout << cuts[i];
  }
  cout << '\n';
  return 0;
}
```

## 推荐记忆

看到“按一个切口分成左右两段”，先固定总和 $S$，把目标写成 $|2P-S|$。单次求解用一次
前缀扫描；只有多询问、在线修改或切分目标改变时，才升级为二分、树状数组或答案二分。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc472/tasks/abc472_b?lang=en)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
