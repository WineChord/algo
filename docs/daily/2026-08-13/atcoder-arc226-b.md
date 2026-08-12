---
title: "[atcoder] ARC226 B Bin-ary Packing"
---

# [atcoder] ARC226 B Bin-ary Packing

<p class="daily-archive-kicker">2026-08-13 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-13 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c773807bd1865ae195d764f700a1878524968f96a0da7840c7b91efa1bdfe26d -->
[Official problem: ARC226 B - Bin-ary Packing](https://atcoder.jp/contests/arc226/tasks/arc226_b?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 226。
- 题目：B - Bin-ary Packing；官方分值 500。
- 时间限制：2 秒；内存限制：1024 MiB。
- 官方链接：[ARC226 B](https://atcoder.jp/contests/arc226/tasks/arc226_b?lang=en)。
- AtCoder 官方未标注题目难度；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 于 2026-08-13 给出的社区估算难度为 1207，且不是实验值。
- 下方英文层是模型独立组织的自包含呈现；官方页面与 [AtCoder 服务条款](https://atcoder.jp/tos)仍是权威来源，本页不主张存在题目专属开放转载许可。

## Complete English statement

### Task

There are $N$ bags, numbered from $1$ through $N$. For every integer $i$ with $0\le i<M$, there are $A_i$ packages of weight $2^i$.

Put every package into exactly one bag. A bag may remain empty. The weight of a bag is the sum of the weights of the packages placed in it.

Among all distributions, minimize the maximum weight of a bag and print that minimum. Process $T$ test cases.

### Input

```text
T
N M
A_0 A_1 ... A_{M-1}
...
```

### Output

Print one answer per test case.

### Constraints

- $1\le T\le10^5$.
- $1\le N\le10^6$.
- $1\le M\le40$.
- $0\le A_i\le10^6$.
- The sum of $M$ over all test cases is at most $2\times10^5$.
- Every input value is an integer.

### Sample

```text
4
2 3
3 2 1
1000000 1
0
1 40
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
188075 10
858153 791486 630853 157728 813993 50047 286602 459270 597406 907405
```

```text
6
0
549755813888
3805
```

For the first test case, the weights $1,2,4$ occur $3,2,1$ times. One optimal distribution is `(4,1,1)` and `(2,2,1)`, whose loads are $6$ and $5$. A maximum load of at most $5$ is impossible. The official statement gives no explanation for the other test cases and contains no task-essential image or additional note.

## 中文题意

有 $N$ 个袋子。重量 $2^i$ 的包裹有 $A_i$ 个，每个包裹必须恰好进入一个袋子，袋子可以为空。求所有分配中“最重袋子的重量”的最小值。

## 约束推导与关键观察

包裹总数可能达到 $4\times10^7$，不能逐件模拟；但重量种类只有 $M\le40$，说明应按二进制尺度聚合。只看最大单件与总重量平均值仍不够：三个容量为 3 的袋子无法容纳四个重量为 2 的包裹，虽然总重量 $8\le9$。

对每个尺度 $2^k$，把所有不小于它的包裹换算为 $2^k$ 单位：

$$
U_k=\sum_{i=k}^{M-1}A_i2^{i-k}.
$$

若袋容量上限为 $C$，每个袋子至多容纳 $\lfloor C/2^k\rfloor$ 个这样的单位，所以必须有：

$$
U_k\le N\left\lfloor\frac{C}{2^k}\right\rfloor.
$$

等价地，所有可行 $C$ 都满足：

$$
C\ge2^k\left\lceil\frac{U_k}{N}\right\rceil.
$$

因此候选答案是全部尺度下界的最大值。递推 $U_k=A_k+2U_{k+1}$ 让我们从高位向低位一次扫描。

## 解法递进

### 解法一：逐包裹枚举袋子

若总包裹数为 $P$，每件包裹都有 $N$ 种去向，枚举全部分配并计算最大袋重。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, p;
  cin >> n >> p;
  vector<int> weight(p), load(n);
  for (int& x : weight) cin >> x;
  long long answer = LLONG_MAX;
  function<void(int)> dfs = [&](int index) {
    if (index == p) {
      answer = min(answer, static_cast<long long>(*max_element(load.begin(), load.end())));
      return;
    }
    int previous = -1;
    for (int bag = 0; bag < n; ++bag) {
      if (load[bag] == previous) continue;
      previous = load[bag];
      load[bag] += weight[index];
      dfs(index + 1);
      load[bag] -= weight[index];
    }
  };
  sort(weight.rbegin(), weight.rend());
  dfs(0);
  cout << answer << '\n';
}
```

时间 $O(N^P P)$，空间 $O(N+P)$。它覆盖所有方案，适合作为小规模 oracle，但无法处理正式约束。

### 解法二：二分容量并检查全部尺度

对给定 $C$ 检查所有尺度不等式。可行性对 $C$ 单调，因而可在 $[0,\sum A_i2^i]$ 上二分。

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
    long long n;
    int m;
    cin >> n >> m;
    vector<long long> count(m);
    long long total = 0;
    for (int i = 0; i < m; ++i) {
      cin >> count[i];
      total += count[i] * (1LL << i);
    }
    auto feasible = [&](long long capacity) {
      long long units = 0;
      for (int i = m - 1; i >= 0; --i) {
        units = units * 2 + count[i];
        if (units > n * (capacity >> i)) return false;
      }
      return true;
    };
    long long left = -1;
    long long right = total;
    while (right - left > 1) {
      long long middle = left + (right - left) / 2;
      if (feasible(middle)) right = middle;
      else left = middle;
    }
    cout << right << '\n';
  }
}
```

时间 $O(M\log W)$，其中 $W$ 是总重量；空间 $O(M)$。它已足够快，但二分重复检查了同一组尺度。

### 最佳实用解：直接取全部尺度下界的最大值

边递推 $U_k$，边计算 $2^k\lceil U_k/N\rceil$，取最大值即可。

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
    long long n;
    int m;
    cin >> n >> m;
    vector<long long> count(m);
    for (long long& x : count) cin >> x;
    long long units = 0;
    long long answer = 0;
    for (int i = m - 1; i >= 0; --i) {
      units = units * 2 + count[i];
      long long bags = (units + n - 1) / n;
      answer = max(answer, bags * (1LL << i));
    }
    cout << answer << '\n';
  }
}
```

时间 $O(M)$，额外空间 $O(M)$；所有测试合计 $O(\sum M)$。

## 正确性证明

设上述最大下界为 $C^\star$。必要性已经由每个尺度的槽位总数推出。

证明可达性：把包裹按重量从大到小放入当前最轻的袋子。准备放重量 $s=2^k$ 的包裹时，此前袋重都是 $s$ 的倍数。反设所有袋子都装不下它。写 $C^\star=qs+r$，其中 $0\le r<s$。每个袋重既大于 $C^\star-s=(q-1)s+r$，又是 $s$ 的倍数，所以至少为 $qs$。此前已放入至少 $Nq$ 个 $s$ 单位，再加当前包裹便有 $U_k>Nq$。

另一方面，尺度 $k$ 的下界保证 $\lfloor C^\star/s\rfloor=q\ge\lceil U_k/N\rceil$，即 $Nq\ge U_k$，矛盾。因此每一步都能放入且不超过 $C^\star$。下界可达，算法输出正是最优值。

## 样例手推与边界

第一组从高位扫描：$U_2=1$ 给出下界 $4$；$U_1=2\times1+2=4$ 给出 $4$；$U_0=2\times4+3=11$ 给出 $\lceil11/2\rceil=6$，答案为 6。

- 所有 $A_i=0$ 时答案为 0。
- $N=1$ 时答案等于总重量。
- 空袋合法，$N$ 很大无需特判。
- 最坏总重量 $10^6(2^{40}-1)<1.1\times10^{18}$，有符号 64 位安全。

## 易错点

- 只用平均数与最大单件会漏掉中间尺度的装箱障碍。
- 必须从高位向低位递推，且不能跳过 $A_k=0$ 的尺度。
- 位移要写 `1LL << i`，不能写 32 位 `1 << i`，也不要使用浮点 `pow`。
- 社区难度 1207 不能写成 AtCoder 官方难度。

## 可复现验证

最佳代码用 GNU++23/Clang C++23 严格编译通过；官方四组输出为 `6,0,549755813888,3805`。本轮统一测试另以完整分配 DFS 为 oracle，固定种子生成 9,999 个小实例，全部一致。独立复核又覆盖 1,815 组完全枚举与 50,000 组随机 oracle，总计 51,815 组，零不一致。

## 变种一：恢复一组最优装袋方案

先求 $C^\star$，再按重量降序用最小堆维护袋重与编号。证明已保证每次选择最轻袋不会超容量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, p;
  cin >> n >> p;
  vector<int> weight(p);
  for (int& x : weight) cin >> x;
  sort(weight.rbegin(), weight.rend());
  priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> heap;
  vector<vector<int>> bags(n);
  for (int i = 0; i < n; ++i) heap.push({0, i});
  for (int x : weight) {
    auto [load, id] = heap.top();
    heap.pop();
    bags[id].push_back(x);
    heap.push({load + x, id});
  }
  for (const auto& bag : bags) {
    for (int x : bag) cout << x << ' ';
    cout << '\n';
  }
}
```

若总包裹数为 $P$，时间 $O((N+P)\log N)$，空间 $O(N+P)$。

## 变种二：同一批包裹回答多个袋数

预处理全部 $U_k$；每个查询 $N_q$ 重新取 $\max_k2^k\lceil U_k/N_q\rceil$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m, q;
  cin >> m >> q;
  vector<long long> count(m), units(m);
  for (long long& x : count) cin >> x;
  for (int i = m - 1; i >= 0; --i) units[i] = count[i] + (i + 1 < m ? 2 * units[i + 1] : 0);
  while (q--) {
    long long n;
    cin >> n;
    long long answer = 0;
    for (int i = 0; i < m; ++i) answer = max(answer, ((units[i] + n - 1) / n) * (1LL << i));
    cout << answer << '\n';
  }
}
```

预处理 $O(M)$，每个查询 $O(M)$。

## 变种三：重量是一条任意整除链

若 $w_0\mid w_1\mid\cdots\mid w_{M-1}$，把递推改为 $U_k=A_k+(w_{k+1}/w_k)U_{k+1}$，答案为 $\max_kw_k\lceil U_k/N\rceil$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int m;
  long long n;
  cin >> n >> m;
  vector<long long> weight(m), count(m);
  for (long long& x : weight) cin >> x;
  for (long long& x : count) cin >> x;
  __int128 units = 0;
  __int128 answer = 0;
  for (int i = m - 1; i >= 0; --i) {
    if (i + 1 < m) units *= weight[i + 1] / weight[i];
    units += count[i];
    answer = max(answer, ((units + n - 1) / n) * weight[i]);
  }
  string out;
  do {
    out.push_back('0' + answer % 10);
    answer /= 10;
  } while (answer > 0);
  reverse(out.begin(), out.end());
  cout << out << '\n';
}
```

时间 $O(M)$；实现用 `__int128` 防止整除链乘法溢出。

## 变种四：要求每个袋子非空

若包裹总数 $P<N$，无解；否则原最优值不变。降序放入当前最轻袋时，前 $N$ 件会分别进入空袋，之后沿用原证明。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n;
  int m;
  cin >> n >> m;
  vector<long long> count(m);
  long long packages = 0;
  for (long long& x : count) {
    cin >> x;
    packages += x;
  }
  if (packages < n) {
    cout << -1 << '\n';
    return 0;
  }
  long long units = 0;
  long long answer = 0;
  for (int i = m - 1; i >= 0; --i) {
    units = units * 2 + count[i];
    answer = max(answer, ((units + n - 1) / n) * (1LL << i));
  }
  cout << answer << '\n';
}
```

时间 $O(M)$，空间 $O(M)$。

## 变种五：重量不再满足整除链

原充分性证明失效；即使 $N=2$，一般整数重量也包含 PARTITION。小总重量时可做子集和 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> weight(n);
  int total = 0;
  for (int& x : weight) {
    cin >> x;
    total += x;
  }
  vector<char> reachable(total + 1);
  reachable[0] = true;
  for (int x : weight) {
    for (int sum = total; sum >= x; --sum) reachable[sum] |= reachable[sum - x];
  }
  int answer = total;
  for (int sum = 0; sum <= total; ++sum) {
    if (reachable[sum]) answer = min(answer, max(sum, total - sum));
  }
  cout << answer << '\n';
}
```

时间 $O(PW)$、空间 $O(W)$，其中 $P$ 是物品数、$W$ 是总重量；这也刻画了二次幂条件带来的结构收益。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc226/tasks/arc226_b?lang=en)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-133-lc162/">[力扣 Top 133] LC 162 寻找峰值 中等 →</a>
</nav>
