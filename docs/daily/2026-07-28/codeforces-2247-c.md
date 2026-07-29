---
title: "[codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence"
---

# [codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence

<p class="daily-archive-kicker">2026-07-28 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

## 官方来源与元数据

- 完整官方英文题面：[打开 Codeforces 页面](https://codeforces.com/contest/2247/problem/C)
- 材料许可：[Codeforces 材料使用许可 v0.1](https://codeforces.com/blog/entry/967)
- 比赛：Codeforces Round 1111（Div. 2）
- 比赛 ID：2247
- 题号别名：Div.2 C
- 官方标题：Inversion of a Subsequence
- 官方分值：1250
- 官方题目等级分：未知；当前 Codeforces API 题目对象未提供 `rating`
- 官方标签：`greedy`、`math`
- 比赛状态：已结束
- 北京时间：2026-07-18 22:35 至 2026-07-19 00:35
- 时间限制：2 秒
- 内存限制：256 MB
- 官方题面图片：无
- 程序接口：GNU++23 完整程序，多组测试。

!!! info "来源与许可"
    Codeforces 是本题来源。下方完整英文题面依据 Codeforces 材料使用许可展示，并给出来源署名与官方直达链接；本教学页面不提供自动判题，也不复制隐藏测试、生成器、检查器或校验器。

## Complete English statement

Two binary arrays $a$ and $b$ of length $n$ are given. One operation on the current array $a$ is:

1. choose a nonempty subsequence, equivalently a nonempty set of indices
   $1\le i_1<i_2<\cdots<i_k\le n$;
2. require the selected current values to have odd sum;
3. invert every selected bit: $a_{i_j}\gets1-a_{i_j}$.

The operation may be used any number of times. Find the minimum number of operations needed to turn $a$ into $b$, or print `-1` if the transformation is impossible.

### Input

The first line contains the number of test cases $t$. Each test case contains:

```text
n
a_1 a_2 ... a_n
b_1 b_2 ... b_n
```

### Output

For each test case, print the minimum number of operations, or `-1`.

### Constraints

- $1\le t\le10^4$
- $1\le n\le2\cdot10^5$
- $a_i,b_i\in\{0,1\}$
- the sum of $n$ over all test cases does not exceed $2\cdot10^5$

### Official sample

```text
Input
5
1
0
0
2
1 0
0 1
3
1 1 1
0 0 0
4
1 0 1 0
0 1 0 1
5
1 0 1 0 1
1 1 1 1 1
Output
0
1
1
2
-1
```

- Case 1 already satisfies $a=b$.
- In case 2, selecting both positions has current sum $1$ and swaps `1 0` into `0 1`.
- In case 3, selecting all three ones has odd sum and solves the case once.
- In case 4, the mismatch set contains two current ones, so one operation is invalid but two suffice.
- In case 5, the nontrivial target is all ones, which no valid final operation can produce.

## 中文解释

每组给定两个长度为 $n$ 的二进制数组 $a,b$。一次操作选择一个非空子序列，也就是一组严格递增的下标；只有所选位置在当前数组中的元素和为奇数时，才能把这些位置的 0、1 全部翻转。可以进行任意多次操作，要求输出把 $a$ 变成 $b$ 的最少操作数；无法完成时输出 `-1`。

一次操作若直接完成变换，就必须恰好选择当前所有不匹配位置，不能漏选，也不能翻转已经匹配的位置。官方样例依次覆盖原本相同、一次可行、需要利用奇数个当前 1、需要两次操作，以及目标无法到达五种情况。

## 从约束建立模型

记

$$
D=\{i:a_i\ne b_i\},\qquad
x=\#\{i\in D:a_i=1\}.
$$

若一次操作就能完成变换，它必须恰好选择 $D$：选择原本匹配的位置会把它变错，漏掉不匹配位置则无法修正。该操作恰在 $x$ 为奇数时合法。

两个吸收边界决定了无解情形：

1. 若 $a$ 全为 0 且 $a\ne b$，任意选择的元素和都是 0，没有合法操作。
2. 若 $b$ 全为 1 且 $a\ne b$，考察最后一次操作。它必须恰好选择前一状态中的全部 0；这些被选值之和为 0，故最后一步不可能合法。

除上述情况外，任意变换至多需要两次操作：

- 若 $x\ge2$ 且为偶数，将 $D$ 拆成两个不相交集合，使二者各含奇数个当前为 1 的位置。
- 若 $x=0$，所有不匹配都是 `0 -> 1`。由于 $a$ 不全为 0，存在一个已匹配的 `1`；由于 $b$ 不全为 1，还存在一个已匹配的 `0`。把这两个位置作为临时辅助，并在第二次操作中复原。

因此完整答案为

$$
\begin{cases}
0,&a=b,\\
-1,&a\ne b\text{ and }(\sum a_i=0\text{ or }\sum b_i=n),\\
1,&x\text{ is odd},\\
2,&x\text{ is even}.
\end{cases}
$$

## 暴力基准：在全部二进制状态上做 BFS

在 $n\le20$ 等缩小范围下，可把当前数组编码为位掩码。从状态 `s` 出发，翻转掩码 `m` 恰在 `popcount(s & m)` 为奇数时合法，下一状态为 `s ^ m`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int encode(const vector<int>& bits) {
  int mask = 0;
  for (int i = 0; i < static_cast<int>(bits.size()); ++i) mask |= bits[i] << i;
  return mask;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int start = encode(a), target = encode(b), states = 1 << n;
    vector<int> distance(states, -1);
    queue<int> q;
    distance[start] = 0;
    q.push(start);
    while (!q.empty()) {
      int state = q.front();
      q.pop();
      for (int flip = 1; flip < states; ++flip) {
        if (__builtin_popcount(static_cast<unsigned>(state & flip)) % 2 == 0) continue;
        int next = state ^ flip;
        if (distance[next] != -1) continue;
        distance[next] = distance[state] + 1;
        q.push(next);
      }
    }
    cout << distance[target] << '\n';
  }
}
```

共有 $2^n$ 个状态，每个状态至多尝试 $2^n-1$ 个掩码，因此时间复杂度为 $O(4^n)$，空间复杂度为 $O(2^n)$。它远不能满足官方数据范围，却是极佳的穷举对拍基准。

## 最优 $O(n)$ 解法

扫描一次，判断两个数组是否相等，并统计各自的 1 的数量以及当前不匹配位置中 1 的数量 $x$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    if (a == b) {
      cout << 0 << '\n';
      continue;
    }
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
      continue;
    }
    int mismatchOnes = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i] && a[i] == 1) ++mismatchOnes;
    }
    cout << (mismatchOnes % 2 == 1 ? 1 : 2) << '\n';
  }
}
```

每组时间复杂度为 $O(n)$，总时间复杂度为 $O(\sum n)$；输入数组占用 $O(n)$ 额外空间。

### 正确性证明

若 $a=b$，显然最优答案为 0。由上面的末次操作论证，全零起点与非平凡全一终点均无解。

以下假设两个无解条件均不成立，且 $a\ne b$。

- 若 $x$ 为奇数，直接选择 $D$ 合法且一次完成。零次操作显然不够，所以最优值为 1。
- 若 $x$ 为正偶数，第一次选择一个当前值为 1 的不匹配位置，第二次选择其余全部不匹配位置。第一次所选和为 1；第二个集合与它不交，并含有 $x-1$ 个未改变的当前 1，因此也合法。每个不匹配位置恰翻转一次，两次操作足够；又因 $x$ 为偶数，一次操作不可能。
- 若 $x=0$，选择一个已匹配的 0 位置 $i$ 与一个已匹配的 1 位置 $k$。第一次选择 $D\cup\{i,k\}$，所选和为 1。操作后 $i$ 变为 1、$k$ 变为 0，再选择 $\{i,k\}$ 仍合法，并恢复两个辅助位置。所有不匹配位置仍恰翻转一次；同样因 $x$ 为偶数，一次操作不可能。

因此算法在所有情形下都返回最少操作数。

## 样例状态演化

对 `a = [1,0,1,0]`、`b = [0,1,0,1]`，每个位置都不匹配，且 $x=2$。

- 第一次选择位置 1：`[1,0,1,0] -> [0,0,1,0]`。
- 第二次选择位置 2、3、4，它们当前的元素和为 1：
  `[0,0,1,0] -> [0,1,0,1]`.

$x=2$ 为偶数，排除一次完成的可能，所以最优答案恰为 2。

## 边界与常见错误

- 必须先判断 `a == b`，再做全零与全一的无解检查；相等的全零或全一数组都只需零次操作。
- 判断一次操作可行性时，只统计不匹配位置上的 1。
- 所选元素要按当前状态计算，不一定等于原数组中的值。
- 子序列不必连续，任意按下标有序的集合都可以。
- 对非平凡的全一目标，应考察最后一次操作，不能想当然地把现有的 1 当作辅助。
- `x = 0` 不代表必然无解；已匹配的 0 与 1 可支持两步构造。
- 在 $n=2\cdot10^5$ 时不要模拟任意操作；答案只依赖四个充分统计量。

## 追问一：输出一组最优操作

### 新定义

有解时，输出达到最少操作数的一组实际下标集合。

### 构造

沿用正确性证明中的构造：一次操作时输出全部不匹配位置；当 $x\ge2$ 且为偶数时做奇数/奇数拆分；当 $x=0$ 时使用两个已匹配辅助位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    vector<int> mismatch;
    int mismatchOnes = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i]) {
        mismatch.push_back(i);
        mismatchOnes += a[i];
      }
    }
    if (mismatch.empty()) {
      cout << 0 << '\n';
      continue;
    }
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
      continue;
    }
    vector<vector<int>> operations;
    if (mismatchOnes % 2 == 1) {
      operations.push_back(mismatch);
    } else if (mismatchOnes > 0) {
      vector<int> first, second;
      bool chosenOne = false;
      for (int index : mismatch) {
        if (!chosenOne && a[index] == 1) {
          first.push_back(index);
          chosenOne = true;
        } else {
          second.push_back(index);
        }
      }
      operations = {first, second};
    } else {
      int matchedZero = -1, matchedOne = -1;
      for (int i = 0; i < n; ++i) {
        if (a[i] == b[i] && a[i] == 0) matchedZero = i;
        if (a[i] == b[i] && a[i] == 1) matchedOne = i;
      }
      vector<int> first = mismatch;
      first.push_back(matchedZero);
      first.push_back(matchedOne);
      operations = {first, {matchedZero, matchedOne}};
    }
    cout << operations.size() << '\n';
    for (const vector<int>& operation : operations) {
      cout << operation.size();
      for (int index : operation) cout << ' ' << index + 1;
      cout << '\n';
    }
  }
}
```

时间复杂度为 $O(n)$，输出本身占用 $O(n)$ 空间。每个输出操作均非空，且按当时状态计算的所选元素和为奇数。

## 追问二：目标数组发生在线单点翻转

### 新定义

数组 $a$ 固定。每次询问翻转 $b$ 中一个比特，并立即输出新的最少操作数。

### 方法

维护四个统计量：不匹配位置数、其中固定 `a` 值为 1 的位置数、$a$ 中 1 的总数和 $b$ 中 1 的总数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int answer(int n, int difference, int mismatchOnes, int onesA, int onesB) {
  if (difference == 0) return 0;
  if (onesA == 0 || onesB == n) return -1;
  return mismatchOnes % 2 == 1 ? 1 : 2;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  cin >> n >> queries;
  vector<int> a(n), b(n);
  for (int& x : a) cin >> x;
  for (int& x : b) cin >> x;
  int onesA = accumulate(a.begin(), a.end(), 0);
  int onesB = accumulate(b.begin(), b.end(), 0);
  int difference = 0, mismatchOnes = 0;
  for (int i = 0; i < n; ++i) {
    if (a[i] != b[i]) {
      ++difference;
      mismatchOnes += a[i];
    }
  }
  while (queries--) {
    int position;
    cin >> position;
    --position;
    if (a[position] != b[position]) {
      --difference;
      mismatchOnes -= a[position];
    } else {
      ++difference;
      mismatchOnes += a[position];
    }
    onesB += b[position] == 0 ? 1 : -1;
    b[position] ^= 1;
    cout << answer(n, difference, mismatchOnes, onesA, onesB) << '\n';
  }
}
```

初始化为 $O(n)$；每次更新与回答均为 $O(1)$，数组存储占用 $O(n)$。

## 追问三：每次操作必须恰好选择两个位置

### 新定义

每次操作恰好选择两个位置，且它们当前值之和必须为奇数。

### 新不变量

被选中的两个比特必为一个 0 和一个 1；同时翻转等价于交换二者，因此 1 的总数保持不变。当两个数组的 1 数量相等时，把每个 `1 -> 0` 不匹配与一个 `0 -> 1` 不匹配配对即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    if (onesA != onesB) {
      cout << -1 << '\n';
      continue;
    }
    int oneToZero = 0;
    for (int i = 0; i < n; ++i) {
      if (a[i] == 1 && b[i] == 0) ++oneToZero;
    }
    cout << oneToZero << '\n';
  }
}
```

时间复杂度为 $O(n)$，除输入外只需 $O(1)$ 额外空间。每次操作恰好修复两个方向各一个不匹配，由此同时证明可行性与最优性。

## 追问四：先最少操作，再最小化带权翻转成本

### 新定义

每个下标有正权重 $w_i$。第一目标仍是最少操作数；在所有最少操作方案中，再最小化每次操作中每个下标出现时的权重总和。

### 方法

每个不匹配位置至少要翻转一次。一次操作方案以及正偶数 $x$ 的拆分方案都会让每个不匹配位置恰翻转一次。当 $x=0$ 时，任意两步方案都必须使用奇数个已匹配 1 和奇数个已匹配 0 作为翻转两次的辅助位置；分别选择权重最小的一个即可。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    vector<long long> weight(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    for (long long& x : weight) cin >> x;
    int difference = 0, mismatchOnes = 0;
    int onesA = accumulate(a.begin(), a.end(), 0);
    int onesB = accumulate(b.begin(), b.end(), 0);
    long long mismatchCost = 0;
    long long cheapestMatchedZero = LLONG_MAX;
    long long cheapestMatchedOne = LLONG_MAX;
    for (int i = 0; i < n; ++i) {
      if (a[i] != b[i]) {
        ++difference;
        mismatchOnes += a[i];
        mismatchCost += weight[i];
      } else if (a[i] == 0) {
        cheapestMatchedZero = min(cheapestMatchedZero, weight[i]);
      } else {
        cheapestMatchedOne = min(cheapestMatchedOne, weight[i]);
      }
    }
    if (difference == 0) {
      cout << "0 0\n";
    } else if (onesA == 0 || onesB == n) {
      cout << -1 << '\n';
    } else if (mismatchOnes % 2 == 1) {
      cout << "1 " << mismatchCost << '\n';
    } else if (mismatchOnes > 0) {
      cout << "2 " << mismatchCost << '\n';
    } else {
      long long cost = mismatchCost + 2 * (cheapestMatchedZero + cheapestMatchedOne);
      cout << "2 " << cost << '\n';
    }
  }
}
```

时间复杂度为 $O(n)$，额外工作空间为 $O(1)$。在 $w_i\le10^9$、总 $n\le2\cdot10^5$ 下，`long long` 足够。

## 追问五：每次选择的子序列长度至多为 $L$

### 新定义

保留原有奇数和规则，但每次操作至多翻转 $L$ 个位置。在 $n\le18$ 下求真实最少操作数。

### 闭式结论为何失效

原来的一步或两步构造可能选中超过 $L$ 个位置。此时不匹配位置的具体分布会影响答案，必须保留完整状态，并在满足长度上限的合法掩码上做 BFS。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int encode(const vector<int>& bits) {
  int mask = 0;
  for (int i = 0; i < static_cast<int>(bits.size()); ++i) mask |= bits[i] << i;
  return mask;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCases;
  cin >> testCases;
  while (testCases--) {
    int n, limit;
    cin >> n >> limit;
    vector<int> a(n), b(n);
    for (int& x : a) cin >> x;
    for (int& x : b) cin >> x;
    int states = 1 << n;
    vector<int> masks;
    for (int mask = 1; mask < states; ++mask) {
      if (__builtin_popcount(static_cast<unsigned>(mask)) <= limit) masks.push_back(mask);
    }
    int start = encode(a), target = encode(b);
    vector<int> distance(states, -1);
    queue<int> q;
    distance[start] = 0;
    q.push(start);
    while (!q.empty()) {
      int state = q.front();
      q.pop();
      for (int flip : masks) {
        if (__builtin_popcount(static_cast<unsigned>(state & flip)) % 2 == 0) continue;
        int next = state ^ flip;
        if (distance[next] != -1) continue;
        distance[next] = distance[state] + 1;
        q.push(next);
      }
    }
    cout << distance[target] << '\n';
  }
}
```

时间复杂度为

$$
O\!\left(2^n\sum_{k=1}^{L}\binom{n}{k}\right),
$$

空间复杂度为 $O(2^n)$。这是刻意面向小规模的精确解法；长度上限破坏了原题只依赖少量充分统计量的结构。

## 可复现验证

- 每个代码块都以 GNU++23 模式独立编译，并开启编译警告。
- 检查官方五组样例，以及 `a == b`、全零起点、全一终点、$x=0$、$x=1$ 与正偶数 $x$ 等明确边界。
- 在较小的二进制状态空间中枚举每一对有序起点和终点，将 $O(n)$ 公式与有向 BFS 穷举结果对拍。
- 回放每份构造输出：每个集合必须非空、当前所选和为奇数，并在声称的最少操作数内到达目标。
- 随机翻转目标数组后，将在线统计量与完整重算比较。
- 将恰选两个位置的公式与其完整状态图比较。
- 对小规模与随机正权重，将带权次级目标公式与一步、两步操作的完整枚举比较。

验证结果：7 个 GNU++23 代码块均以 `-Wall -Wextra -pedantic` 独立编译通过；代码中没有制表符或空白源码行，每级缩进均为两个空格。对 $n\le8$ 的完整有向状态图，共核对 87380 对有序起点/终点与闭式结论，回放 85874 份构造答案，并在同样的 87380 对状态上验证恰选两个位置的变种。使用固定种子 20260728，500000 次在线目标翻转均与完整重算一致，100000 组带权次级目标测试均与一步、两步穷举一致。官方五组样例全部通过。

## 来源

- [Codeforces 2247C 官方题面](https://codeforces.com/contest/2247/problem/C)
- [Codeforces Round 1111 官方比赛页](https://codeforces.com/contest/2247)
- [Codeforces Round 1111 官方题解](https://codeforces.com/blog/entry/155337)
- [Codeforces 官方 API 题库数据](https://codeforces.com/api/problemset.problems)
- [Codeforces 官方 API 比赛列表](https://codeforces.com/api/contest.list?gym=false)

## 参考资料

- [官方题目](https://codeforces.com/contest/2247/problem/C)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-511-q3-lc3998/">← [力扣竞赛] 第 511 场周赛 Q3 LC 3998 使用子序列排序转换二进制字符串 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-07-28-lc3517/">[力扣每日一题] 2026-07-28｜LC 3517 最小回文排列 I →</a>
</nav>
