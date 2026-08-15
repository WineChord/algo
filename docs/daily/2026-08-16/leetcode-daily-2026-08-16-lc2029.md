---
title: "[力扣每日一题] 2026-08-16｜LC 2029 石子游戏 IX"
---

# [力扣每日一题] 2026-08-16｜LC 2029 石子游戏 IX

<p class="daily-archive-kicker">2026-08-16 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-16 题目列表</a> · <a href="../../../dp/game-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b59c3296533fd8c585d4b540217278ca8c1d841e62eb55718d37e7fd732ab6e9 -->
[力扣 2029：石子游戏 IX](https://leetcode.cn/problems/stone-game-ix/)

## 官方原始信息

- 工作日期：2026-08-16（Asia/Shanghai）；力扣中国官方每日一题接口核对为当天题目。
- 题号：2029。
- 官方中文标题：石子游戏 IX。
- 官方难度：中等。
- 来源：第 261 场周赛 Q3；官方竞赛分值：5 分。
- ZeroTracer 社区估算竞赛分：2277.3595662538，抓取于 2026-08-16；这不是官方难度。
- 函数签名：`bool stoneGameIX(vector<int>& stones)`。

Alice 和 Bob 轮流移除一颗石子，Alice 先手。若某位玩家移除后，已移除石子的总和能被 3
整除，该玩家立即输；若全部石子都被移除且此前无人因整除而输，则 Bob 获胜。两人都采用
最优策略，判断 Alice 能否获胜。

### 全部官方样例

样例 1：

```text
输入：stones = [2,1]
输出：true
```

Alice 先移除 2，总和为 2；Bob 只能移除 1，使总和变为 3，因此 Bob 输。

样例 2：

```text
输入：stones = [2]
输出：false
```

Alice 移除唯一石子后没有触发 3 的倍数，但石子耗尽，按规则 Bob 获胜。

样例 3：

```text
输入：stones = [5,1,2,4,3]
输出：false
```

无论 Alice 如何开始，Bob 都能应对并获胜。

### 全部官方约束

- `1 <= stones.length <= 100000`。
- `1 <= stones[i] <= 10000`。

## 约束、状态压缩与整数范围

胜负只由总和模 3 决定，每颗石子的具体值可压缩为余数 0、1、2 的数量
$c_0,c_1,c_2$。若对原数组做极小极大搜索，状态数指数增长；$10^5$ 的规模要求把博弈完整
归纳为常数个计数条件。

余数 0 不改变当前总和。开局总和为 0，第一手若拿余数 0 会立即输；开局选了 1 或 2 后，
余数 0 是一张安全的“换手牌”，只改变轮到谁继续非零序列。因此它的数量只需保留奇偶性。
计数最多 $10^5$，`int` 足够。

## 样例手推与边界

样例 1 的计数是 $(c_0,c_1,c_2)=(0,1,1)$。Alice 选任一非零余数，Bob 被迫拿另一个余数
并立即凑成 3 的倍数，所以先手胜。

样例 3 的余数为 `2,1,2,1,0`，即 $(1,2,2)$。0 的数量为奇数，而两类非零石子数量差
为 0，不足以消化一次额外换手，Bob 胜。

- 只有余数 0：Alice 第一手立即输。
- 只有一类非零余数：当 $c_0$ 为偶数时 Alice 不能赢；当 $c_0$ 为奇数时，至少 3 颗同余
  非零石子才可能形成数量差优势。
- $c_1=c_2$ 且 $c_0$ 偶数：Alice 可选任一非零类获胜。
- 大量相同原值不需要去重；只统计余数。
- 石子耗尽不是“无子可走者输”，而是 Bob 固定获胜，不能套普通 normal-play 结论。

## 解法一：完整极小极大搜索作为暴力 oracle

对小数组用位掩码记录剩余石子，并保留当前总和模 3 与轮次。Alice 的节点取“存在一个后继
使 Alice 胜”，Bob 的节点取“所有后继都使 Alice 胜”；某一步凑成 0 时，当前行动者输。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> residue;
vector<array<array<int, 2>, 3>> memo;
bool aliceWins(int mask, int sum, int aliceTurn) {
  if (mask == 0) return false;
  int& cached = memo[mask][sum][aliceTurn];
  if (cached != -1) return cached;
  bool result = !aliceTurn;
  for (int i = 0; i < static_cast<int>(residue.size()); ++i) {
    if (!(mask >> i & 1)) continue;
    int nextSum = (sum + residue[i]) % 3;
    bool nextResult;
    if (nextSum == 0) nextResult = !aliceTurn;
    else nextResult = aliceWins(mask ^ (1 << i), nextSum, !aliceTurn);
    if (aliceTurn) result = result || nextResult;
    else result = result && nextResult;
  }
  return cached = result;
}
int main() {
  int n;
  cin >> n;
  residue.resize(n);
  for (int& value : residue) {
    cin >> value;
    value %= 3;
  }
  memo.assign(1 << n, {});
  for (auto& states : memo) {
    for (auto& turns : states) turns.fill(-1);
  }
  cout << boolalpha << aliceWins((1 << n) - 1, 0, true) << '\n';
}
```

时间 $O(n2^n)$、空间 $O(2^n)$，只能用于约 $n\le20$ 的验证。它忠实实现终局规则，可作为
计数公式的独立 oracle。

## 从博弈树到两张胜负表

第一手只能选余数 1 或 2。以先选 1 为例，忽略随时可插入的余数 0，安全的非零余数序列为

$$
1,1,2,1,2,1,2,\ldots
$$

因为当前和为 1 时不能拿 2，为 2 时不能拿 1。先选 2 完全对称。余数 0 在当前和非零时
安全且不改变所需的下一类，只交换行动者；因此只看 $c_0$ 的奇偶。对这条强制序列从末端
反推，得到第一手的完整胜负表：

- $c_0$ 为偶数：先选 1 当且仅当 $0<c_1\le c_2$ 时获胜；先选 2 当且仅当
  $0<c_2\le c_1$ 时获胜。
- $c_0$ 为奇数：先选 1 当且仅当 $c_1>c_2+2$；先选 2 当且仅当
  $c_2>c_1+2$。

把 Alice 可以任选第一手这一点合并，便得到

$$
\text{AliceWin}=
\begin{cases}
c_1>0\land c_2>0, & c_0\equiv0\pmod2,\\
|c_1-c_2|>2, & c_0\equiv1\pmod2.
\end{cases}
$$

## 最佳实用解：一次计数后套判定式

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool stoneGameIX(vector<int>& stones) {
    array<int, 3> count{};
    for (int value : stones) ++count[value % 3];
    if (count[0] % 2 == 0) return count[1] > 0 && count[2] > 0;
    return abs(count[1] - count[2]) > 2;
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(1)$。这是面试和竞赛中应优先记忆的方案：先把元素压成
模 3 计数，再明确分析 0 类换手牌的奇偶，而不是凭样例猜数量关系。

## 正确性证明

**引理 1：余数 0 只贡献换手奇偶。**

第一手拿 0 立即输。此后只要游戏未结束，当前和
只能是 1 或 2；拿 0 不改变它，也不会立即输，只把同一个“下一安全非零余数”交给对手。
所以所有 0 的具体位置无关，偶数张抵消换手，奇数张额外交换一次行动权。

**引理 2：给定第一手后，安全非零序列唯一。**

当前和为 1 时，拿 2 会输，唯一非零安全
选择是 1；当前和为 2 时同理只能拿 2。故先手选择 1 后的序列是
`1,1,2,1,2,...`，选择 2 时对称。

**引理 3：上节两张胜负表完备。**

在唯一非零序列上，某类先耗尽时，轮到必须拿该类的
玩家要么被迫拿会凑成 0 的另一类而输，要么所有石子耗尽使 Bob 获胜。插入全部 0 只按
引理 1 改变最终行动者。分别按偶、奇代入并比较两类消耗量，恰得到
$0<c_1\le c_2$ / $c_1>c_2+2$ 及其对称条件。

**定理：算法返回值正确。**

Alice 可以在余数 1、2 两种合法开局中选任一获胜者。$c_0$
偶数时两张表的并集正是 $c_1,c_2$ 都非零；$c_0$ 奇数时并集正是两者差的绝对值大于 2。
算法逐字实现这两个充要条件，因此恰在 Alice 有必胜策略时返回 `true`。

## 方案比较与易错点

位掩码极小极大搜索没有遗漏策略，但指数级；三维计数 DP 仍会有
$O(c_0c_1c_2)$ 状态。闭式条件把唯一安全余数序列和 0 类奇偶彻底用完，达到读入下界。

- 不能只检查 `c1 != c2`；奇数个 0 时必须相差至少 3。
- 偶数个 0 时，两类非零余数都必须存在，即使一类数量远多于另一类也仍可选少数类开局。
- `stones[i]` 的原值和总和都不必保存；只取模计数。
- 不要把“拿到 3 的倍数者输”写成“让对手面对 3 的倍数”。失败发生在落子瞬间。
- 空集终局固定判 Bob 胜，是暴力 oracle 最容易写错的基例。

## 验证说明

三份官方样例均通过。对所有 $c_0+c_1+c_2\le12$ 的计数组合，把闭式结果与完整极小极大
搜索逐项比较；另对长度 1 到 12 的随机原数组对拍，未发现差异。最佳代码及全部变种分别以
C++23 语法编译。

## 变种一：返回一个必胜的第一手下标

新定义不仅判断胜负，还要返回 Alice 可采用的原数组下标；无必胜第一手返回 -1。偶数个 0
时选数量较少的非零余数类，数量相等时任选；奇数个 0 时选数量领先至少 3 的类。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int winningFirstMove(vector<int>& stones) {
    array<int, 3> count{};
    for (int value : stones) ++count[value % 3];
    int residue = -1;
    if (count[0] % 2 == 0) {
      if (count[1] == 0 || count[2] == 0) return -1;
      residue = count[1] <= count[2] ? 1 : 2;
    } else if (count[1] > count[2] + 2) {
      residue = 1;
    } else if (count[2] > count[1] + 2) {
      residue = 2;
    } else {
      return -1;
    }
    for (int i = 0; i < static_cast<int>(stones.size()); ++i) {
      if (stones[i] % 3 == residue) return i;
    }
    return -1;
  }
};
```

时间 $O(n)$、空间 $O(1)$。原判定仍成立，但现在使用了两张“指定第一手”的更细胜负表。

## 变种二：统计所有必胜第一手

新定义把不同原数组下标视为不同第一手，求其中能保证 Alice 获胜的个数。相同余数的石子在
后续博弈中完全等价，所以只需把胜利开局余数对应的计数相加。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countWinningFirstMoves(vector<int>& stones) {
    array<int, 3> count{};
    for (int value : stones) ++count[value % 3];
    int answer = 0;
    if (count[0] % 2 == 0) {
      if (count[1] > 0 && count[1] <= count[2]) answer += count[1];
      if (count[2] > 0 && count[2] <= count[1]) answer += count[2];
    } else {
      if (count[1] > count[2] + 2) answer += count[1];
      if (count[2] > count[1] + 2) answer += count[2];
    }
    return answer;
  }
};
```

时间 $O(n)$、空间 $O(1)$。当 $c_0$ 偶且 $c_1=c_2>0$ 时，两类第一手都获胜，不能只
统计其中一类。

## 变种三：在线修改石子值并询问胜负

新定义给定初始数组，支持把某个位置改成新值以及随时询问 Alice 是否必胜。更新只会让两个
余数计数各增减 1，查询直接复用闭式条件。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  cin >> n >> queries;
  vector<int> stones(n);
  array<int, 3> count{};
  for (int& value : stones) {
    cin >> value;
    ++count[value % 3];
  }
  auto aliceWins = [&]() {
    if (count[0] % 2 == 0) return count[1] > 0 && count[2] > 0;
    return abs(count[1] - count[2]) > 2;
  };
  while (queries--) {
    int type;
    cin >> type;
    if (type == 1) {
      int index, value;
      cin >> index >> value;
      --index;
      --count[stones[index] % 3];
      stones[index] = value;
      ++count[stones[index] % 3];
    } else {
      cout << (aliceWins() ? "Alice" : "Bob") << '\n';
    }
  }
}
```

初始化 $O(n)$，每次更新与查询均为 $O(1)$，空间 $O(n)$。静态线性扫描不再合适，但真正的
充分统计量仍只有三个计数。

## 变种四：除数改为任意 $k$，小规模精确求解

新定义把失败条件改成“累计和能被 $k$ 整除”，且 $n\le20$。模 3 的强制序列闭式不再直接
成立；保留掩码、当前和模 $k$ 与轮次做完整极小极大搜索。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, divisor;
  cin >> n >> divisor;
  vector<int> value(n);
  for (int& item : value) {
    cin >> item;
    item %= divisor;
  }
  int states = 1 << n;
  vector<vector<array<int, 2>>> memo(
      states, vector<array<int, 2>>(divisor, array<int, 2>{-1, -1}));
  function<bool(int, int, int)> solve = [&](int mask, int sum, int turn) {
    if (mask == 0) return false;
    int& result = memo[mask][sum][turn];
    if (result != -1) return result != 0;
    bool aliceResult = !turn;
    for (int i = 0; i < n; ++i) {
      if (!(mask >> i & 1)) continue;
      int nextSum = (sum + value[i]) % divisor;
      bool child = nextSum == 0 ? !turn : solve(mask ^ (1 << i), nextSum, !turn);
      if (turn) aliceResult = aliceResult || child;
      else aliceResult = aliceResult && child;
    }
    result = aliceResult;
    return aliceResult;
  };
  cout << (solve(states - 1, 0, 1) ? "Alice" : "Bob") << '\n';
}
```

时间 $O(nk2^n)$、空间 $O(k2^n)$。值域变化破坏了只有两类安全非零选择的结构，指数搜索只
适用于小规模；更大 $k,n$ 需要另找周期或 Sprague–Grundy 类结构。

## 变种五：把耗尽规则改为 normal play

新定义保留“凑成 3 的倍数者立即输”，但若安全地拿完最后一颗，则下一位无子可拿者输，
不再固定 Bob 获胜。原闭式的终端归纳失效；对适中计数可直接在
$(c_0,c_1,c_2,s,turn)$ 上记忆化，其中 $s$ 表示当前模 3 的和。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
map<array<int, 5>, bool> memo;
bool currentPlayerWins(array<int, 3> count, int sum, int turn) {
  if (count[0] + count[1] + count[2] == 0) return false;
  array<int, 5> state = {count[0], count[1], count[2], sum, turn};
  if (memo.count(state)) return memo[state];
  for (int residue = 0; residue < 3; ++residue) {
    if (count[residue] == 0) continue;
    int nextSum = (sum + residue) % 3;
    if (nextSum == 0) continue;
    --count[residue];
    bool opponentWins = currentPlayerWins(count, nextSum, turn ^ 1);
    ++count[residue];
    if (!opponentWins) return memo[state] = true;
  }
  return memo[state] = false;
}
int main() {
  int n;
  cin >> n;
  array<int, 3> count{};
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    ++count[value % 3];
  }
  cout << (currentPlayerWins(count, 0, 0) ? "First" : "Second") << '\n';
}
```

状态数至多 $O(c_0c_1c_2)$，每个状态 3 个转移，适合计数较小的变种。终局契约一改，原题
“空集必为 Bob 胜”的非对称条件消失，必须重新建模而不能沿用原公式。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/stone-game-ix/)
- [第 261 场周赛](https://leetcode.cn/contest/weekly-contest-261/)
- [ZeroTracer 社区竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/stone-game-ix/)
- [对应知识专题](../../dp/game-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2256-e/">← [codeforces] CF Round 1116 Div.1 C / Div.2 E Even If the World Turns</a>
<span class="daily-archive-pager__empty"></span>
</nav>
