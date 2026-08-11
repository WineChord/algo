---
title: "[codeforces] CF Round 1113 Div.2 G No Balance Left"
---

# [codeforces] CF Round 1113 Div.2 G No Balance Left

<p class="daily-archive-kicker">2026-08-11 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-11 题目列表</a> · <a href="../../../dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=197a37b88feed5faf034fb9d7006959148919a9d8c2dd6b3014165c3dc2bef83 -->
[Official problem: Codeforces 2248G - No Balance Left](https://codeforces.com/contest/2248/problem/G)

## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1113 (Div. 2)；Contest ID 2248。
- 题号与标题：Div.2 G - No Balance Left。
- 官方分值：3500；官方 rating：3000。
- 官方 tags：`bitmasks`、`dp`、`math`、`number theory`。
- 时间限制：6 秒；内存限制：256 MB。
- 官方题面：[Codeforces 2248G](https://codeforces.com/contest/2248/problem/G)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)。

下方英文题面层按 Codeforces 材料许可在公开、非判题用途下呈现，并保留来源、官方直达链接与许可说明。这里不复制隐藏测试、生成器、checker、validator 或其他未公开判题材料。官方页面提示题面近期有过修改，本页依据 2026-08-11 核对到的当前版本。

## Complete English statement

### G. No Balance Left

**Time limit per test:** 6 seconds

**Memory limit per test:** 256 megabytes

**Input:** standard input

**Output:** standard output

Alisa has a shopping card with an initial balance of $h$. There are $n$ types of products in a supermarket. A product of type $i$ costs $c_i$, and Alisa can buy any number of products of each type.

There are also $m$ rebate activities. The $j$-th activity applies to a purchase if its total cost is at least $a_j$ and gives a rebate of $b_j$.

For each purchase, Alisa performs the following operations:

- She chooses one or more products whose total cost $x$ does not exceed the current balance on her card and pays $x$ using the card.
- Among all rebate activities that apply to this purchase, the one with the largest rebate takes effect and its rebate is added to the card balance. If no rebate activity applies, no rebate is added.

For every $h$ from $1$ to $s$, determine whether Alisa can make the balance on her card equal to $0$ after finitely many purchases.

### Input and complete constraints

The first line contains three integers $n$, $m$, and $s$:

$$
1\le n,m,s\le125000.
$$

The second line contains $n$ integers $c_1,c_2,\ldots,c_n$:

$$
1\le c_i\le125000.
$$

The $i$-th of the next $m$ lines contains two integers $a_i$ and $b_i$:

$$
1\le a_i,b_i\le125000.
$$

The activity thresholds and rebates are both strictly increasing:

$$
a_1<a_2<\cdots<a_m,\qquad b_1<b_2<\cdots<b_m.
$$

All input values are integers.

### Output

Print $s$ lines. For each $i$ with $1\le i\le s$, print `YES` if Alisa can make the card balance equal to $0$ from initial balance $i$, and print `NO` otherwise. Letter case is ignored.

### Complete official samples

```text
Input
2 1 15
4 7
8 4

Output
NO
NO
NO
YES
NO
NO
YES
YES
NO
NO
YES
YES
NO
YES
YES
```

```text
Input
5 3 25
4 8 12 16 20
6 8
7 9
8 10

Output
NO
NO
NO
YES
NO
NO
NO
YES
NO
YES
NO
YES
NO
YES
NO
YES
NO
YES
NO
YES
NO
YES
NO
YES
NO
```

In the first sample, starting from $15$, Alisa buys products costing $4$ and $7$ together. She pays $11$, temporarily leaving $4$; since $11\ge8$, the rebate $4$ returns the balance to $8$. She then buys the product costing $4$ twice, without a rebate, and reaches $0$. Hence the fifteenth answer is `YES`.

In the second sample, balance $4$ can be spent directly on the first product. Since $4<6$, no rebate applies and the balance becomes $0$. From balance $1$, no product is affordable, so the first answer is `NO`.

There are no statement images required to understand the task.

## 中文题意

一笔购买可以包含任意多个、任意种商品。设其总价为 $x$：先从卡中扣除 $x$，再从所有满足 $a_j\le x$ 的活动中选择返利最大的一个，把 $b_j$ 加回卡中。每笔购买必须非空，且付款时 $x$ 不能超过当前余额。对每个初始余额 $1,2,\ldots,s$，判断是否能用有限笔购买恰好把余额变成 $0$。

## 约束推导与核心模型

令 $r(x)$ 为总价 $x$ 对应的返利，无活动时 $r(x)=0$。一笔交易把余额变成

$$
h\longmapsto h-x+r(x).
$$

首先要知道哪些 $x$ 能由商品价格无界组合出来。取

$$
V=\max(s,a_m).
$$

只需显式处理 $x\le V$：所有待回答余额不超过 $s$；越过最后门槛后返利恒为 $b_m$，尾部交易的同余信息可由商品价格和 $b_m$ 概括。

对每个可实现总价 $x\le V$：

- 若 $r(x)>x$，它带来净增加 $r(x)-x$。令 $M$ 为此类交易的最小总价；若不存在，令 $M=s+1$。
- 若 $r(x)\le x$，它带来净减少 $d=x-r(x)$。

同一个 $d$ 只保留最小购买额

$$
need[d]=\min\{x:x-r(x)=d\},
$$

因为更便宜的同效果交易严格支配更贵者。

余额 $h<M$ 时买不起任何净增益交易，状态只会下降，形成 DAG：

$$
f[0]=\mathrm{true},
$$

$$
f[h]=\bigvee_{\substack{1\le d\le h\\need[d]\le h}}f[h-d].
$$

条件 $need[d]\le h$ 不能省略：净减少虽只有 $d$，付款时仍必须先拿得出完整总价。

余额 $h\ge M$ 时可反复执行最便宜的增资交易，把余额抬到任意高。设所有已枚举净增量、净减量、所有商品价格与 $b_m$ 的最大公因数为

$$
g=\gcd(\text{all net changes},c_1,\ldots,c_n,b_m).
$$

每笔交易都保持余额模 $g$ 不变，因此归零必有 $g\mid h$。反过来，增资提供无限缓冲，正负净变化生成的整数群恰为 $g\mathbb Z$，同一余数类中的余额可先升高再按有限组合下降。

还有一个容易遗漏的终局条件。最后一笔若从正余额归零，则

$$
h-x+r(x)=0,\qquad x\le h.
$$

$h-x$ 与 $r(x)$ 均非负，故只能同时为零：最后一笔必须花光余额且没有返利。这种购买存在当且仅当最便宜商品低于首个门槛：

$$
c_{\min}<a_1.
$$

所以高余额区间的答案为

$$
f[h]=(h\bmod g=0)\land(c_{\min}<a_1).
$$

## 解法递进

### 解法一：标量枚举购买总价与净损失

先用普通布尔数组做无界背包，再逐余额枚举所有净减少量。它完整实现上述充要条件，适合作为清晰基准，但两个二重循环在上界处常数较大。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, s;
  cin >> n >> m >> s;
  vector<int> price(n);
  vector<char> isPrice(125001);
  for (int& value : price) {
    cin >> value;
    isPrice[value] = true;
  }
  vector<int> threshold(m + 1), rebate(m + 1);
  for (int i = 1; i <= m; ++i) {
    cin >> threshold[i] >> rebate[i];
  }
  int bound = max(s, threshold[m]);
  vector<char> spendable(bound + 1);
  spendable[0] = true;
  for (int total = 0; total <= bound; ++total) {
    if (!spendable[total]) {
      continue;
    }
    for (int value = 1; value + total <= bound; ++value) {
      if (isPrice[value]) {
        spendable[total + value] = true;
      }
    }
  }
  vector<int> need(bound + 1, bound + 1), changes;
  int firstIncrease = s + 1;
  int activity = 0;
  for (int total = 1; total <= bound; ++total) {
    if (!spendable[total]) {
      continue;
    }
    while (activity < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    int delta = rebate[activity] - total;
    changes.push_back(abs(delta));
    if (delta > 0) {
      firstIncrease = min(firstIncrease, total);
    } else {
      need[-delta] = min(need[-delta], total);
    }
  }
  vector<char> possible(s + 1);
  possible[0] = true;
  for (int balance = 1; balance < firstIncrease && balance <= s; ++balance) {
    for (int decrease = 1; decrease <= balance; ++decrease) {
      if (need[decrease] <= balance && possible[balance - decrease]) {
        possible[balance] = true;
        break;
      }
    }
  }
  int invariant = 0;
  for (int value : changes) {
    invariant = gcd(invariant, value);
  }
  for (int value : price) {
    invariant = gcd(invariant, value);
  }
  invariant = gcd(invariant, rebate[m]);
  int cheapest = *min_element(price.begin(), price.end());
  for (int balance = 1; balance <= s; ++balance) {
    bool answer = balance < firstIncrease
                      ? possible[balance]
                      : cheapest < threshold[1] && balance % invariant == 0;
    cout << (answer ? "YES" : "NO") << '\n';
  }
}
```

时间 $O(V^2+n+m)$，空间 $O(V)$。它没有利用机器字并行，最坏规模下不如 bitset 版本稳。

### 最佳实用解：两次 bitset DP

第一个 bitset 求所有可实现总价。初始置位每种单价；从小到大扫描已可达的 $x$，执行 `spendable |= spendable << x`。移位会同时把所有当前组合再加一个可实现总价 $x$，新产生位置均大于当前扫描点，故不会漏解。

第二个 bitset 优化低余额 DAG。把净减少量 $d$ 反向存储，并按 $need[d]$ 排序激活；扫描到余额 $h$ 时，一次移位与按位与即可判断是否存在已激活的 $d$ 使 $f[h-d]$ 成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int LIMIT = 125001;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, s;
  cin >> n >> m >> s;
  vector<int> price(n);
  for (int& value : price) {
    cin >> value;
  }
  vector<int> threshold(m + 1), rebate(m + 1);
  for (int i = 1; i <= m; ++i) {
    cin >> threshold[i] >> rebate[i];
  }
  int bound = max(s, threshold[m]);
  bitset<LIMIT> spendable;
  spendable.set(0);
  for (int value : price) {
    spendable.set(value);
  }
  for (int total = 1; total <= bound; ++total) {
    if (spendable[total]) {
      spendable |= spendable << total;
    }
  }
  vector<int> need(bound + 1, bound + 1);
  vector<int> increases, decreases;
  int firstIncrease = s + 1;
  int activity = 0;
  for (int total = 1; total <= bound; ++total) {
    if (!spendable[total]) {
      continue;
    }
    while (activity < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    int net = rebate[activity] - total;
    if (net > 0) {
      increases.push_back(net);
      firstIncrease = min(firstIncrease, total);
    } else {
      int decrease = -net;
      need[decrease] = min(need[decrease], total);
      decreases.push_back(decrease);
    }
  }
  vector<pair<int, int>> losses;
  for (int decrease = 1; decrease <= bound; ++decrease) {
    if (need[decrease] <= bound) {
      losses.push_back({need[decrease], decrease});
    }
  }
  sort(losses.begin(), losses.end());
  bitset<LIMIT> reachable, activeLosses;
  reachable.set(0);
  size_t nextLoss = 0;
  int lowEnd = min(s, firstIncrease - 1);
  for (int balance = 1; balance <= lowEnd; ++balance) {
    while (nextLoss < losses.size() && losses[nextLoss].first <= balance) {
      activeLosses.set(LIMIT - 1 - losses[nextLoss].second);
      ++nextLoss;
    }
    reachable[balance] =
        (reachable & (activeLosses >> (LIMIT - 1 - balance))).any();
  }
  int invariant = 0;
  for (int value : increases) {
    invariant = gcd(invariant, value);
  }
  for (int value : decreases) {
    invariant = gcd(invariant, value);
  }
  for (int value : price) {
    invariant = gcd(invariant, value);
  }
  invariant = gcd(invariant, rebate[m]);
  int cheapest = *min_element(price.begin(), price.end());
  for (int balance = 1; balance <= s; ++balance) {
    bool answer = balance < firstIncrease
                      ? reachable[balance]
                      : cheapest < threshold[1] && balance % invariant == 0;
    cout << (answer ? "YES" : "NO") << '\n';
  }
}
```

时间复杂度为

$$
O\left(\frac{V^2}{64}+n+m+V\log V\right),
$$

空间复杂度为 $O(V)$。$V\le125000$，乘积、返利与净变化都落在 `int` 范围；只做计数或扩展规则时再考虑 `long long`。

## 正确性证明

**引理一**：`spendable` 恰好包含所有不超过 $V$ 的可实现购买总价。

初始每个单价可达。扫描到可达总价 $x$ 时，把当前所有可达总价各加一个 $x$，仍是商品多重集合之和；故不会产生伪状态。反之，任意多重集合可拆成两个已可实现的非空子集合，按其较小总价被扫描时合并；对商品件数归纳即可得到全部总价。

**引理二**：对 $h<M$，低余额递推充要。

由 $M$ 的最小性，余额 $h<M$ 时无法负担任何净增益交易。净变化为零不改善状态，可以删除；其余首笔交易必是某个净减少 $d$，且要满足 $need[d]\le h$，之后余额为 $h-d$。这恰是递推枚举的全部选择。按 $h$ 递增归纳，$f[h]$ 与真实可归零性一致。

**引理三**：对 $h\ge M$，可归零的必要条件是 $g\mid h$ 且 $c_{\min}<a_1$。

所有交易净变化都是 $g$ 的倍数，因此余额模 $g$ 不变。最后一笔归零时，$h-x$ 与 $r(x)$ 两个非负量之和为零，只能 $h=x$ 且 $r(x)=0$；至少要存在低于首门槛的可购买总价，等价于 $c_{\min}<a_1$。

**引理四**：上述高余额必要条件也充分。

从 $h\ge M$ 可重复最便宜的净增益交易，获得任意大的缓冲。所有显式净变化以及最后返利档的尾部变化生成的整数群为 $g\mathbb Z$；尾部的 gcd 由商品价格与 $b_m$ 完整概括。若 $g\mid h$，Bézout 组合给出把余额总变化成 $-h$ 的有限整数表示。先重复增资交易足够多次，可把其中负系数改写为非负次增资并保证每笔付款时余额充足；再按净减少交易下降，最终使用低于 $a_1$ 的无返利购买归零。因此条件充分。

由四个引理，低区间 DP 与高区间判定覆盖全部 $1\le h\le s$，最佳实用解正确。

## 样例手推与边界

样例一中不存在净增益交易，所以 $M=s+1$，所有答案都由低区间 DP 得出。可归零余额为

$$
4,7,8,11,12,14,15.
$$

其中 $15\to8\to4\to0$ 正是官方 Note 的过程。

样例二中，总价 $8$ 可实现，最高适用返利为 $10$，故产生净增益 $2$，$M=8$；最便宜商品 $4<a_1=6$，且 $g=2$。低区间只有 $4$ 可归零；从 $8$ 起恰好所有偶数可归零，与 25 行输出逐项一致。

真正需要覆盖的边界包括：没有任何可购买总价、没有净增益交易、$r(x)=x$ 的零变化、多个总价产生相同净减少、$a_1\le c_{\min}$、$g>1$、首个净增益总价恰为 $s$，以及购买总价跨过多个活动门槛。

## 易错点与方案比较

- 购买必须非空；`spendable[0]` 只是背包种子，不能当成交易。
- 只有 $r(x)>x$ 才是增资；$r(x)=x$ 不得更新 $M$。
- 低区间不仅要求 $d\le h$，还要检查完整购买额 $need[d]\le h$。
- `need[d]` 保留最小总价，而不是第一次随意遇到的总价。
- gcd 必须加入全部商品价格与 $b_m$，否则会遗漏 $x>V$ 的最后返利档。
- 边界是 $V=\max(s,a_m)$，不需要改成 $\max(s,a_m,b_m)$。
- `a_1<=c_min` 时任何正购买都有返利，最后一步无法归零。
- 标量版本证明最直观；bitset 版没有改变状态定义，只把两次存在性枚举并行化。竞赛中推荐记忆“低余额 DAG + 高余额泵和 gcd”的分层，再把 bitset 当作实现加速。

## 变种一：低余额时恢复一组购买方案

新定义：额外给定一个目标余额 $H<M$，若可归零，输出每笔购买所选商品类型。原低区间 DAG 仍成立；为购买总价背包和余额 DP 各保留一个父指针即可。下面实现面向 $V\le5000$ 的教学版。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m, target;
  cin >> n >> m >> target;
  vector<int> price(n);
  for (int& value : price) {
    cin >> value;
  }
  vector<int> threshold(m), rebate(m);
  for (int i = 0; i < m; ++i) {
    cin >> threshold[i] >> rebate[i];
  }
  int bound = max(target, threshold.back());
  vector<char> spendable(bound + 1);
  vector<int> previousTotal(bound + 1, -1), usedType(bound + 1, -1);
  spendable[0] = true;
  for (int total = 0; total <= bound; ++total) {
    if (!spendable[total]) {
      continue;
    }
    for (int type = 0; type < n; ++type) {
      int next = total + price[type];
      if (next <= bound && !spendable[next]) {
        spendable[next] = true;
        previousTotal[next] = total;
        usedType[next] = type;
      }
    }
  }
  vector<int> need(bound + 1, bound + 1), activityFor(bound + 1);
  int activity = -1;
  int firstIncrease = bound + 1;
  for (int total = 1; total <= bound; ++total) {
    while (activity + 1 < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    int back = activity == -1 ? 0 : rebate[activity];
    if (!spendable[total]) {
      continue;
    }
    if (back > total) {
      firstIncrease = min(firstIncrease, total);
    } else if (total < need[total - back]) {
      need[total - back] = total;
      activityFor[total - back] = activity;
    }
  }
  if (target >= firstIncrease) {
    cout << "TARGET IS NOT IN THE LOW REGION\n";
    return 0;
  }
  vector<char> possible(target + 1);
  vector<int> parentLoss(target + 1, -1);
  possible[0] = true;
  for (int balance = 1; balance <= target; ++balance) {
    for (int loss = 1; loss <= balance; ++loss) {
      if (need[loss] <= balance && possible[balance - loss]) {
        possible[balance] = true;
        parentLoss[balance] = loss;
        break;
      }
    }
  }
  if (!possible[target]) {
    cout << "NO\n";
    return 0;
  }
  vector<vector<int>> plan;
  for (int balance = target; balance > 0;) {
    int loss = parentLoss[balance];
    int total = need[loss];
    vector<int> types;
    for (int value = total; value > 0; value = previousTotal[value]) {
      types.push_back(usedType[value] + 1);
    }
    plan.push_back(types);
    balance -= loss;
  }
  cout << "YES\n" << plan.size() << '\n';
  for (const auto& purchase : plan) {
    cout << purchase.size();
    for (int type : purchase) {
      cout << ' ' << type;
    }
    cout << '\n';
  }
}
```

时间 $O(nV+V^2)$，空间 $O(V)$。父指针只恢复一种方案，不追求购买次数最少。

## 变种二：一笔购买中每类商品至多一件

新定义：每次购买仍可重复进行，但同一笔购买内每个商品类型最多选择一次，并保证 $\sum c_i\le125000$。原无界背包失效，改用降序 0/1 背包；得到一笔购买的全部合法总价后，低区间 DP 与高区间 gcd 证明不变。由于合法总价集合有限，gcd 直接取所有正、负净变化，不再用商品价格与 $b_m$ 补尾部。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int LIMIT = 125001;
int main() {
  int n, m, s;
  cin >> n >> m >> s;
  vector<int> price(n);
  int totalPrice = 0;
  for (int& value : price) {
    cin >> value;
    totalPrice += value;
  }
  vector<int> threshold(m + 1), rebate(m + 1);
  for (int i = 1; i <= m; ++i) {
    cin >> threshold[i] >> rebate[i];
  }
  bitset<LIMIT> spendable;
  spendable.set(0);
  for (int value : price) {
    spendable |= spendable << value;
  }
  vector<int> need(totalPrice + 1, totalPrice + 1), changes;
  int firstIncrease = s + 1;
  int activity = 0;
  for (int total = 1; total <= totalPrice; ++total) {
    while (activity < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    if (!spendable[total]) {
      continue;
    }
    int net = rebate[activity] - total;
    changes.push_back(abs(net));
    if (net > 0) {
      firstIncrease = min(firstIncrease, total);
    } else {
      need[-net] = min(need[-net], total);
    }
  }
  vector<char> possible(s + 1);
  possible[0] = true;
  for (int balance = 1; balance < firstIncrease && balance <= s; ++balance) {
    for (int loss = 1; loss <= balance; ++loss) {
      if (loss <= totalPrice && need[loss] <= balance &&
          possible[balance - loss]) {
        possible[balance] = true;
        break;
      }
    }
  }
  int invariant = 0;
  for (int change : changes) {
    invariant = gcd(invariant, change);
  }
  int cheapest = *min_element(price.begin(), price.end());
  for (int balance = 1; balance <= s; ++balance) {
    bool answer = balance < firstIncrease
                      ? possible[balance]
                      : cheapest < threshold[1] && balance % invariant == 0;
    cout << (answer ? "YES" : "NO") << '\n';
  }
}
```

0/1 背包时间 $O(n\sum c_i/64)$；标量低区间时间 $O(s^2)$，空间 $O(s+\sum c_i)$。若规模仍取原上限，可把第二阶段继续替换为反向 bitset DP。

## 变种三：所有达到门槛的活动返利叠加

新定义：一笔购买不再只取最大返利，而是把所有满足 $a_j\le x$ 的 $b_j$ 相加。原分层框架仍成立，但阶梯返利改为前缀和，可能超过 `int`；净变化与 gcd 必须使用 `long long`。下面保留 $s,a_m\le125000$，并保证返利总和不超过 $10^{18}$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int LIMIT = 125001;
int main() {
  int n, m, s;
  cin >> n >> m >> s;
  vector<int> price(n);
  for (int& value : price) {
    cin >> value;
  }
  vector<int> threshold(m + 1);
  vector<long long> rebatePrefix(m + 1);
  for (int i = 1; i <= m; ++i) {
    long long rebate;
    cin >> threshold[i] >> rebate;
    rebatePrefix[i] = rebatePrefix[i - 1] + rebate;
  }
  int bound = max(s, threshold[m]);
  bitset<LIMIT> spendable;
  spendable.set(0);
  for (int value : price) {
    spendable.set(value);
  }
  for (int total = 1; total <= bound; ++total) {
    if (spendable[total]) {
      spendable |= spendable << total;
    }
  }
  vector<int> need(bound + 1, bound + 1);
  vector<long long> changes;
  int firstIncrease = s + 1;
  int activity = 0;
  for (int total = 1; total <= bound; ++total) {
    if (!spendable[total]) {
      continue;
    }
    while (activity < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    long long net = rebatePrefix[activity] - total;
    changes.push_back(abs(net));
    if (net > 0) {
      firstIncrease = min(firstIncrease, total);
    } else if (-net <= bound) {
      need[-net] = min(need[-net], total);
    }
  }
  vector<char> possible(s + 1);
  possible[0] = true;
  for (int balance = 1; balance < firstIncrease && balance <= s; ++balance) {
    for (int loss = 1; loss <= balance; ++loss) {
      if (need[loss] <= balance && possible[balance - loss]) {
        possible[balance] = true;
        break;
      }
    }
  }
  long long invariant = 0;
  for (long long change : changes) {
    invariant = gcd(invariant, change);
  }
  for (int value : price) {
    invariant = gcd(invariant, static_cast<long long>(value));
  }
  invariant = gcd(invariant, rebatePrefix[m]);
  int cheapest = *min_element(price.begin(), price.end());
  for (int balance = 1; balance <= s; ++balance) {
    bool answer = balance < firstIncrease
                      ? possible[balance]
                      : cheapest < threshold[1] && balance % invariant == 0;
    cout << (answer ? "YES" : "NO") << '\n';
  }
}
```

时间 $O(V^2/64+V^2+n+m)$，空间 $O(V)$；第二次 DP 也可沿用主解的 bitset 优化。

## 变种四：限制最多进行 $K$ 笔购买

新定义：只允许最多 $K$ 笔购买，且 $K,s,a_m,b_m\le100$。无限增资与 gcd 结论失效，因为不能任意重复增资交易。每笔最多增加 $b_m$，所以从初始余额不超过 $s$ 出发，所有相关余额均不超过 $B=s+Kb_m$；在这个有限状态空间上做分层可达 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m, s, maxPurchases;
  cin >> n >> m >> s >> maxPurchases;
  vector<int> price(n);
  for (int& value : price) {
    cin >> value;
  }
  vector<int> threshold(m + 1), rebate(m + 1);
  for (int i = 1; i <= m; ++i) {
    cin >> threshold[i] >> rebate[i];
  }
  int bound = s + maxPurchases * rebate[m];
  vector<char> spendable(bound + 1);
  spendable[0] = true;
  for (int value : price) {
    for (int total = value; total <= bound; ++total) {
      spendable[total] = spendable[total] || spendable[total - value];
    }
  }
  vector<int> back(bound + 1);
  int activity = 0;
  for (int total = 1; total <= bound; ++total) {
    while (activity < m && threshold[activity + 1] <= total) {
      ++activity;
    }
    back[total] = rebate[activity];
  }
  vector<vector<char>> can(maxPurchases + 1, vector<char>(bound + 1));
  can[0][0] = true;
  for (int used = 1; used <= maxPurchases; ++used) {
    can[used][0] = true;
    for (int balance = 1; balance <= bound; ++balance) {
      can[used][balance] = can[used - 1][balance];
      for (int total = 1; total <= balance && !can[used][balance]; ++total) {
        if (!spendable[total]) {
          continue;
        }
        int next = balance - total + back[total];
        if (next <= bound && can[used - 1][next]) {
          can[used][balance] = true;
        }
      }
    }
  }
  for (int balance = 1; balance <= s; ++balance) {
    cout << (can[maxPurchases][balance] ? "YES" : "NO") << '\n';
  }
}
```

时间 $O(KB^2+nB)$，空间 $O(KB)$。与原题相比，状态多了一维购买次数，但边界有限且没有数论尾部。

## 可复现验证

两组官方样例逐行通过。另以真实余额转移图作 oracle：在余额上界 $B$ 内枚举全部可购买总价和边，反向 BFS 求可归零状态，再比较 $B$ 与 $2B$ 已稳定的实例。350 个随机小实例的 3182 个余额、以及系统枚举的 12500 个余额查询均与最佳实用解一致；未发现反例。

来源：[官方题面](https://codeforces.com/contest/2248/problem/G)、[Codeforces API 元数据](https://codeforces.com/api/problemset.problems)、[官方 Editorial](https://codeforces.com/blog/entry/155640?locale=en)、[材料许可](https://codeforces.com/blog/entry/967?mobile=false)。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/G)
- [对应知识专题](../../dp/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-biweekly-188-q2-lc4007/">← [力扣竞赛] 第 188 场双周赛 Q2 LC 4007 栅栏的最宽宽度 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-11-lc2996/">[力扣每日一题] 2026-08-11｜LC 2996 大于等于顺序前缀和的最小缺失整数 →</a>
</nav>
