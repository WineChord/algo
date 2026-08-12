---
title: "[力扣竞赛] 第 188 场双周赛 Q3 LC 4008 击败所有怪物的最小初始强度 中等"
---

# [力扣竞赛] 第 188 场双周赛 Q3 LC 4008 击败所有怪物的最小初始强度 中等

<p class="daily-archive-kicker">2026-08-12 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-12 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4d264835b912a529684b36e71928640f4cc160e91c634d96e6293d72b28757c4 -->
## 官方原始信息

- 比赛：力扣第 188 场双周赛。
- 题目：Q3，LC 4008，击败所有怪物的最小初始强度。
- 官方难度：中等；比赛官方分值：5。
- ZeroTracer 社区估算竞赛分：截至 2026-08-12 未收录，记为未知。
- 官方链接：[击败所有怪物的最小初始强度](https://leetcode.cn/problems/minimum-initial-strength-to-defeat-all-monsters/)。

### 原始题意与函数签名

你必须按下标从左到右击败所有怪物。`monsters[i]` 是第 `i` 个怪物的强度。每条增强 `[l,r,v]` 会在检查区间 `[l,r]` 内任意怪物时临时增加 `v` 点可用强度，重叠增强可以累加；增强只影响能否击败当前怪物，不会保留到之后。若当前实际强度加临时增强不少于怪物强度，就能击败它，随后实际强度变为 `max(0, current - monsters[i])`。求最小非负初始强度。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  long long minInitialStrength(
      vector<int>& monsters, vector<vector<int>>& boosts);
};
```

### 全部官方样例

```text
输入：monsters = [5,10,15], boosts = [[1,1,10]]
输出：30
解释：初始强度 30。依次战斗前实际强度为 30、25、15，均能通过检查；最终为 0。
```

```text
输入：monsters = [5,10,15], boosts = [[1,2,10],[1,2,5]]
输出：5
解释：击败第一个怪物后实际强度为 0；之后两处都得到 15 点临时增强，因此仍可继续击败。
```

### 全部约束

- $1\le n=|monsters|\le5\times10^4$。
- $1\le monsters_i\le10^9$。
- $0\le |boosts|\le5\times10^4$。
- 每条增强满足 $0\le l\le r<n$、$1\le v\le10^9$。
- 总怪物强度和、重叠增强和都可达到 $5\times10^{13}$，必须使用 `long long`。

## 约束推导与观察

区间增强只需得到每个位置的总和，差分数组可在 $O(n+q)$ 完成。设初始强度为 $X$，前 $i$ 个怪物强度之和为 $P_i$，其中 $P_0=0$。由于每次扣减后下限为零，战斗第 $i$ 个怪物前的实际强度恒为

$$
current_i=\max(0,X-P_i).
$$

若位置 $i$ 的增强总和 $B_i\ge monsters_i$，即使实际强度为零也能通过；否则必须满足

$$
X\ge P_i+monsters_i-B_i.
$$

因此答案就是这些必要下界与零的最大值，不需要二分。

## 解法递进

### 解法一：从零开始枚举初始强度

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool works(const vector<int>& monsters, const vector<long long>& bonus, long long initial) {
  long long current = initial;
  for (int i = 0; i < static_cast<int>(monsters.size()); ++i) {
    if (current + bonus[i] < monsters[i]) return false;
    current = max(0LL, current - monsters[i]);
  }
  return true;
}
int main() {
  int n, q;
  cin >> n >> q;
  vector<int> monsters(n);
  for (int& x : monsters) cin >> x;
  vector<long long> difference(n + 1);
  while (q--) {
    int left, right, value;
    cin >> left >> right >> value;
    difference[left] += value;
    difference[right + 1] -= value;
  }
  for (int i = 1; i < n; ++i) difference[i] += difference[i - 1];
  for (long long initial = 0;; ++initial) {
    if (works(monsters, difference, initial)) {
      cout << initial << '\n';
      break;
    }
  }
}
```

检查一次为 $O(n+q)$，但答案可达 $5\times10^{13}$，枚举没有可行上界，只适合作为极小值 oracle。

### 解法二：二分答案

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool feasible(const vector<int>& a, const vector<long long>& bonus, long long initial) {
  long long current = initial;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    if (current + bonus[i] < a[i]) return false;
    current = max(0LL, current - a[i]);
  }
  return true;
}
int main() {
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  vector<long long> bonus(n + 1);
  while (q--) {
    int left, right, value;
    cin >> left >> right >> value;
    bonus[left] += value;
    bonus[right + 1] -= value;
  }
  for (int i = 1; i < n; ++i) bonus[i] += bonus[i - 1];
  long long low = 0, high = accumulate(a.begin(), a.end(), 0LL);
  while (low < high) {
    long long middle = low + (high - low) / 2;
    if (feasible(a, bonus, middle)) high = middle;
    else low = middle + 1;
  }
  cout << low << '\n';
}
```

可行性关于初始强度单调，故二分正确。时间 $O(n\log\sum monsters+q)$、空间 $O(n)$，已经能通过，但重复模拟了同一前缀。

### 最佳实用解：差分与前缀下界

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long minInitialStrength(vector<int>& monsters, vector<vector<int>>& boosts) {
    int n = monsters.size();
    vector<long long> difference(n + 1);
    for (const auto& boost : boosts) {
      difference[boost[0]] += boost[2];
      difference[boost[1] + 1] -= boost[2];
    }
    long long bonus = 0, defeated = 0, answer = 0;
    for (int i = 0; i < n; ++i) {
      bonus += difference[i];
      if (bonus < monsters[i]) {
        answer = max(answer, defeated + monsters[i] - bonus);
      }
      defeated += monsters[i];
    }
    return answer;
  }
};
int main() {
  vector<int> monsters{5, 10, 15};
  vector<vector<int>> boosts{{1, 1, 10}};
  cout << Solution().minInitialStrength(monsters, boosts) << '\n';
}
```

时间 $O(n+q)$、空间 $O(n)$。它只扫描一次，证明和实现都最短，推荐优先记忆“差分求点值，再取前缀约束最大值”这一模型。

## 正确性证明

先证状态公式。对 $i$ 归纳：第零只怪物前实际强度为 $X=\max(0,X-P_0)$。若第 $i$ 只之前为 $\max(0,X-P_i)$，扣除 `monsters[i]` 再与零取最大，得到 $\max(0,X-P_{i+1})$，归纳成立。

若 $B_i\ge monsters_i$，检查自动通过。否则检查式

$$
\max(0,X-P_i)+B_i\ge monsters_i
$$

右侧缺口为正，迫使 $X-P_i\ge monsters_i-B_i$，等价于算法记录的下界。任何可行初始强度都必须不小于所有下界；取所有下界最大值时，每个位置的检查又都成立。因此算法答案既是必要下界也是可行构造，必为最小值。

## 样例手推、边界与易错点

样例一的点增强为 `[0,10,0]`。第 0 处下界为 5；第 1 处增强已经足够，不产生约束；第 2 处下界为 $15+15=30$，答案 30。样例二的点增强为 `[0,15,15]`，只有第 0 处产生下界 5，后两处即使实际强度归零也可通过，答案正是 5。

- 区间右端的差分撤销位置是 `r+1`，数组需开到 `n+1`。
- 临时增强是否参与战后扣减是模型关键，不能凭题名猜测。
- 前缀和与增强和都必须是 `long long`。
- 两个官方样例与最优公式通过；随机对拍以逐步模拟为 oracle，覆盖 50,000 组小实例。

## 变种一：返回每个前缀的最小初始强度

新定义：对每个 $r$，求只击败 `[0,r]` 所需的最小初始强度。扫描时记录当前下界最大值即可，时间 $O(n+q)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> prefixAnswers(const vector<int>& a, vector<long long> bonus) {
  long long defeated = 0, answer = 0;
  vector<long long> result;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    if (bonus[i] < a[i]) answer = max(answer, defeated + a[i] - bonus[i]);
    result.push_back(answer);
    defeated += a[i];
  }
  return result;
}
int main() {
  for (long long x : prefixAnswers({5, 10, 15}, {0, 10, 0})) cout << x << ' ';
  cout << '\n';
}
```

## 变种二：结束时还需保留指定强度

新定义：击败所有怪物后实际强度至少为 `reserve>0`。除原检查外还需 $X\ge\sum monsters+reserve$，取二者最大值即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minimumWithReserve(
    const vector<int>& a, const vector<long long>& bonus, long long reserve) {
  long long defeated = 0, answer = 0;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    if (bonus[i] < a[i]) answer = max(answer, defeated + a[i] - bonus[i]);
    defeated += a[i];
  }
  return max(answer, defeated + reserve);
}
int main() {
  cout << minimumWithReserve({5, 10, 15}, {0, 10, 0}, 7) << '\n';
}
```

## 变种三：怪物强度支持在线单点修改

新定义：点增强固定，在线修改某个怪物强度并询问答案。对每次修改后重新线性扫描下界，单次 $O(n)$、空间 $O(1)$；它舍弃了静态前缀和，换取简单且稳定的在线接口。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long evaluateUpdates(const vector<long long>& monsters,
                          const vector<long long>& bonus) {
  long long prefix = 0, answer = 0;
  for (int i = 0; i < static_cast<int>(monsters.size()); ++i) {
    if (bonus[i] < monsters[i]) {
      answer = max(answer, prefix + monsters[i] - bonus[i]);
    }
    prefix += monsters[i];
  }
  return answer;
}
int main() {
  vector<long long> monsters{5, 10, 15}, bonus{0, 10, 0};
  monsters[1] = 12;
  cout << evaluateUpdates(monsters, bonus) << '\n';
}
```

## 变种四：允许任意安排怪物顺序

新定义：每只怪物的增强固定绑定自身，但可以任意排序。只有 $b_i<m_i$ 的怪物会形成下界。两只有下界的怪物相邻时，先 $i$ 后 $j$ 的局部下界为 $m_i+m_j-b_j$，反序则为 $m_i+m_j-b_i$，所以应按 $b_i$ 非降序排列；没有下界的怪物放在最后，内部顺序任意。排序后扫描即可，时间 $O(n\log n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minimumInAnyOrder(const vector<int>& monster, const vector<long long>& bonus) {
  struct Task {
    bool unconstrained;
    long long bonus;
    long long strength;
  };
  vector<Task> tasks;
  for (int i = 0; i < static_cast<int>(monster.size()); ++i) {
    tasks.push_back({bonus[i] >= monster[i], bonus[i], monster[i]});
  }
  sort(tasks.begin(), tasks.end(), [](const Task& lhs, const Task& rhs) {
    return pair{lhs.unconstrained, lhs.bonus} < pair{rhs.unconstrained, rhs.bonus};
  });
  long long spent = 0, answer = 0;
  for (const Task& task : tasks) {
    if (!task.unconstrained) {
      answer = max(answer, spent + task.strength - task.bonus);
    }
    spent += task.strength;
  }
  return answer;
}
int main() {
  cout << minimumInAnyOrder({5, 10, 15}, {0, 10, 0}) << '\n';
}
```

## 变种五：所有增强中至多选择一条生效

新定义：每条增强仍覆盖一个区间，但全程至多激活一条。枚举所选增强，差分得到其点值并运行线性公式；总时间 $O(qn)$、空间 $O(n)$，适合增强数量较小的版本。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long evaluate(const vector<int>& a, int left, int right, long long value) {
  long long prefix = 0, answer = 0;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    long long bonus = left <= i && i <= right ? value : 0;
    if (bonus < a[i]) answer = max(answer, prefix + a[i] - bonus);
    prefix += a[i];
  }
  return answer;
}
int main() {
  vector<int> a{5, 10, 15};
  vector<array<int, 3>> boosts{{1, 1, 10}, {1, 2, 15}};
  long long answer = evaluate(a, 1, 0, 0);
  for (auto [left, right, value] : boosts) {
    answer = min(answer, evaluate(a, left, right, value));
  }
  cout << answer << '\n';
}
```

## 验证说明

所有完整代码块均按 C++23 编译。主算法以逐初始强度模拟作为小规模 oracle，使用固定种子生成 50,000 组 $n\le9$、随机区间增强实例，并检查公式答案可行且答案减一不可行；全部一致。官方两个样例逐项复核，区间差分、重叠增强、强度归零与 64 位极值均单独覆盖。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-initial-strength-to-defeat-all-monsters/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-132-lc18/">← [力扣 Top 132] LC 18 四数之和 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-a/">[codeforces] CF Round 1116 Div.2 A Three Numbers on the Blackboard →</a>
</nav>
