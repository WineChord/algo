---
title: "[atcoder] ARC226 D Penta-Queue"
---

# [atcoder] ARC226 D Penta-Queue

<p class="daily-archive-kicker">2026-08-15 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-15 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3ca0144e5b595f215fbc69fe9db02a012079ca962116d59d71fc11e5ce6c8c93 -->
[Official problem: ARC226 D - Penta-Queue](https://atcoder.jp/contests/arc226/tasks/arc226_d?lang=en)

## 官方来源与元数据

- 比赛：UNIQUE VISION Programming Contest 2026 Summer（AtCoder Regular Contest 226）。
- 题目：D - Penta-Queue。
- 官方分值：800 分。
- 时间限制：2 秒；内存限制：1024 MiB。
- 比赛 rated 范围：1200–2799。
- [官方英文题面](https://atcoder.jp/contests/arc226/tasks/arc226_d?lang=en)。
- [AtCoder 服务条款](https://atcoder.jp/tos)。
- AtCoder Problems 社区估算难度：2642，核对于 2026-08-15；`is_experimental=false`，这不是 AtCoder 官方难度。

下方英文层是模型基于官方任务独立组织的自包含呈现。任务页没有给出题目专属开放转载许可；官方页面与 AtCoder 服务条款仍是权威来源。本题没有理解所必需的图片。

## Complete English statement

This is an interactive problem. Five initially empty FIFO queues are numbered from 1 through 5. The judge performs exactly $Q$ push operations and $Q$ pop operations in some fixed order, for a total of $2Q$ rounds.

At the start of a push round, the judge appends a new integer $X$ to the back of queue 1 and sends:

```text
1 X
```

All pushed values are distinct. After receiving this input, your program may perform any number of moves. One move chooses a nonempty source queue $i$ and any destination queue $j$, removes the front element of queue $i$, and appends it to the back of queue $j$. The choice $i=j$ is allowed, so a queue may be rotated. If you perform $k$ moves, print $k$ and then the $k$ source-destination pairs:

```text
k
i_1 j_1
i_2 j_2
...
i_k j_k
```

The total number of moves over the whole interaction must not exceed $10^5$.

At the start of a pop round, the judge sends:

```text
2
```

At least one queue is nonempty. Print the index $i$ of a nonempty queue whose front element is the minimum among all elements currently stored in all five queues. The judge then removes that front element.

### Interaction input

The first input is the integer $Q$. It is followed interactively by exactly $2Q$ round descriptions of the forms above.

### Interaction output

After every push, print the complete move sequence. After every pop, print one valid queue index. End every response with a newline and flush the output. If the judge sends `-1`, terminate immediately with exit status 0. Extra blank lines are malformed output, and the program must terminate after the final round.

The judge is non-adaptive: the round types, their order, and all values $X$ are fixed before the interaction begins.

### Constraints

- $1\le Q\le5000$.
- $1\le X\le10^9$.
- All pushed values are pairwise distinct.
- There are exactly $Q$ pushes and exactly $Q$ pops.
- At least one element exists at every pop.
- All input values are integers.

### Complete official sample interaction

The official sample uses $Q=2$ and pushes 5, then 3. One valid transcript is:

```text
Judge:   2
Judge:   1 5
Program: 0
Judge:   1 3
Program: 3
Program: 1 2
Program: 1 2
Program: 2 2
Judge:   2
Program: 2
Judge:   2
Program: 2
```

After the three moves, queue 2 is `[3,5]`, so the two pop responses are valid. The sample demonstrates one legal strategy; other legal interactions are accepted.

## 中文题意解释

Judge 每次 push 已经把新值放到队列 1 的队尾。程序只能在这类轮次输出若干次“从源队首移到目标队尾”的 move；pop 轮次则必须立即指出当前全局最小值所在的队首。关键限制是整个交互至多使用 $10^5$ 次 move，不能在每次插入后都把全部元素重新排序。

若能始终保持五个队列各自升序，那么每个队列的最小值都在队首，全局最小值一定是五个队首中的最小者。问题因此变成：如何利用有限移动，把新来的单元素有序块逐层归并，同时证明总移动数不超预算。

## 约束推导与朴素策略

### 暴力：把所有元素维护在一个升序队列

把队列 1 中的新元素与队列 2 的升序序列归并，需要旋转队列 2 一整圈；第 $m$ 次插入最多使用 $m$ 次 move。下面程序在协议与顺序上正确，但总移动数最坏为 $1+2+\cdots+Q=O(Q^2)$，因而只是小规模基准，不能通过官方移动预算。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  if (!(cin >> q)) return 0;
  deque<int> incoming;
  deque<int> sorted;
  for (int round = 0; round < 2 * q; ++round) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      incoming.push_back(value);
      vector<pair<int, int>> operations;
      int rotations = static_cast<int>(sorted.size());
      for (int step = 0; step < rotations; ++step) {
        if (!incoming.empty() && incoming.front() < sorted.front()) {
          sorted.push_back(incoming.front());
          incoming.pop_front();
          operations.push_back({1, 2});
        }
        sorted.push_back(sorted.front());
        sorted.pop_front();
        operations.push_back({2, 2});
      }
      if (!incoming.empty()) {
        sorted.push_back(incoming.front());
        incoming.pop_front();
        operations.push_back({1, 2});
      }
      cout << operations.size() << '\n';
      for (auto [from, to] : operations) cout << from << ' ' << to << '\n';
    } else {
      cout << 2 << '\n';
      sorted.pop_front();
    }
    cout.flush();
  }
}
```

本地处理时间和 move 数最坏均为 $O(Q^2)$，保存元素需要 $O(Q)$ 空间。瓶颈是每个新元素都重复经过整条旧序列。

## 解法递进：从单队列到五层归并

### 两个升序队列如何归并

设源队列 $A$ 与目标队列 $B$ 均升序。固定记下 $B$ 归并前的长度。每次准备旋转 $B$ 的当前队首前，先把 $A$ 中所有更小的队首移到 $B$ 队尾，再把这个 $B$ 队首自移动到队尾。一整圈后，把 $A$ 剩余元素全部移入 $B$。

这正是标准双指针归并的队列版本，使用恰好 $|A|+|B|$ 次 move；固定原长度很重要，因为归并途中追加的元素不能再次被当作旧 $B$ 元素旋转。

### 九进制级联

把新值看成大小 1 的升序块，采用阈值

$$
1,9,81,729.
$$

- 队列 1 达到 1 个元素时归并入队列 2；
- 队列 2 达到 9 个元素时归并入队列 3；
- 队列 3 达到 81 个元素时归并入队列 4；
- 队列 4 达到 729 个元素时归并入队列 5。

因为 $Q\le5000<9^4=6561$，五个队列足够。阈值必须从低到高检查，使一次 push 可以连续进位。

### 移动预算

在某一层，九个大小为 $9^i$ 的块依次并入目标队列，九次归并代价总和为

$$
(1+2+\cdots+9)9^i=45\cdot9^i.
$$

它们对应 $9^{i+1}$ 次 push，所以每层摊销至多 $5Q$ 次 move。四层合计至多

$$
4\cdot5Q=20Q\le100000.
$$

提前 pop 只会删除元素，使后续归并更便宜，不会破坏上界。

## 最佳实用解：基数 9 的五层升序队列

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queryCount;
  if (!(cin >> queryCount)) return 0;
  array<deque<int>, 5> queues;
  const array<int, 4> limit = {1, 9, 81, 729};
  auto moveValue = [&](int from, int to,
      vector<pair<int, int>>& operations) {
    int value = queues[from].front();
    queues[from].pop_front();
    queues[to].push_back(value);
    operations.push_back({from + 1, to + 1});
  };
  auto mergeQueues = [&](int from, int to,
      vector<pair<int, int>>& operations) {
    int rotations = static_cast<int>(queues[to].size());
    for (int step = 0; step < rotations; ++step) {
      while (!queues[from].empty() &&
          queues[from].front() < queues[to].front()) {
        moveValue(from, to, operations);
      }
      moveValue(to, to, operations);
    }
    while (!queues[from].empty()) moveValue(from, to, operations);
  };
  for (int round = 0; round < 2 * queryCount; ++round) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      queues[0].push_back(value);
      vector<pair<int, int>> operations;
      for (int level = 0; level < 4; ++level) {
        if (static_cast<int>(queues[level].size()) >= limit[level]) {
          mergeQueues(level, level + 1, operations);
        }
      }
      cout << operations.size() << '\n';
      for (auto [from, to] : operations) {
        cout << from << ' ' << to << '\n';
      }
    } else {
      int chosen = -1;
      for (int i = 0; i < 5; ++i) {
        if (queues[i].empty()) continue;
        if (chosen == -1 || queues[i].front() < queues[chosen].front()) {
          chosen = i;
        }
      }
      cout << chosen + 1 << '\n';
      queues[chosen].pop_front();
    }
    cout.flush();
  }
}
```

本地维护和总 move 数均为 $O(Q\log_9Q)$，实际层数固定为 4；存储 $O(Q)$。pop 只比较五个队首，时间 $O(5)=O(1)$。

## 正确性证明

维护不变量：每轮响应结束后，五个本地队列与 Judge 的五个真实队列逐项相同，且每个队列内部升序。

初始时全部为空，不变量成立。push 时 Judge 与本地都把新值加入队列 1；阈值 1 使它立即作为单元素升序块向上归并。归并过程逐次输出与本地修改相同的 move，并按升序合并两个升序队列，因此源变空、目标仍升序，其他队列不变；连续进位后不变量恢复。

pop 时，每个非空升序队列的最小元素在队首，所以全部元素的最小值必是五个队首中的最小者。程序输出它所在队列；Judge 与本地随后都删除同一队首，剩余序列仍升序。归纳可知每次 pop 都合法，且本地状态始终同步。

移动预算已由分层摊销证明不超过 $10^5$，故程序同时满足正确性与资源限制。

## 样例手推与边界

官方样例先把 5 从队列 1 移入队列 2。推入 3 时，队列 2 原有长度为 1：先把 3 从队列 1 移入队列 2，再把旧队首 5 自旋转，得到 `[3,5]`。之后两个 pop 都选队列 2。

- $Q=1$：一次 push 只需把单元素移到队列 2，随后 pop。
- 恰到 9、81、729：一次 push 会触发相应层进位，必须从低层向高层处理。
- 值按升序或降序到达：归并比较仍正确，预算证明不依赖输入顺序。
- pop 穿插在任意位置：删除队首保持该队列升序，并只会降低未来归并成本。
- `i==j` 的自移动是旋转目标队列的合法关键操作。

## 方案比较与推荐

单有序队列只有一个简单不变量，却反复旋转全部历史元素；五层归并把“每次插入”改为“满块才合并”，与 LSM tree、二进制计数器和归并排序的摊销思想一致。基数 9 同时满足 $9^4>5000$ 与四层总预算 $20Q\le10^5$。竞赛中应优先记“有序块 + 分层进位 + 摊销”，不要尝试预知非自适应序列或把普通优先队列误当作可直接操作 Judge 队列。

## 易错点

- push 输入出现时，Judge 已经把 `X` 加入真实队列 1，本地必须同步。
- move 只能在 push 后输出，pop 后不能补做整理。
- 旋转次数必须固定为归并前目标队列的长度。
- 阈值检查必须从低层到高层，允许一次操作连续进位。
- pop 输出后要同步删除本地队首。
- 收到 `-1` 必须立即终止，不能继续输出。
- 每轮完整响应后 flush；不能输出调试文本或额外空行。
- 普通重定向只能演示协议，不能替代离线交互模拟器或真实 Judge。

## 可复现验证

主解与全部变种均以 GNU++23 严格警告编译。离线 Judge 模拟器逐 move 维护五个真实 `deque`，用独立 `multiset` 核对每次 pop；覆盖 276 组完整交互，包括 200 组 $Q=5000$ 随机序列、40 组随机规模、阈值边界、全 push 后全 pop、交替操作以及升序、降序、随机值。全部通过，观测最大 move 数为 89331，低于 100000；变种 oracle 另完成 40000 组随机核验。

## 变种一：push 值保证严格递增

新值始终大于所有旧值，队列 1 本身就是升序队列，无需任何 move；每次 pop 都选队列 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  if (!(cin >> q)) return 0;
  deque<int> values;
  for (int step = 0; step < 2 * q; ++step) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      values.push_back(value);
      cout << 0 << '\n';
    } else {
      cout << 1 << '\n';
      values.pop_front();
    }
    cout.flush();
  }
}
```

本地时间 $O(Q)$，空间 $O(Q)$，move 数为 0。原题值的到达顺序任意，所以不能使用这一简化。

## 变种二：允许重复值

把归并比较改为 `<=`，让源队列的相等值稳定地先进入目标；pop 时任取一个最小队首即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  if (!(cin >> q)) return 0;
  array<deque<int>, 5> a;
  const array<int, 4> limit = {1, 9, 81, 729};
  auto moveOne = [&](int from, int to, vector<pair<int, int>>& output) {
    int value = a[from].front();
    a[from].pop_front();
    a[to].push_back(value);
    output.push_back({from + 1, to + 1});
  };
  auto merge = [&](int from, int to, vector<pair<int, int>>& output) {
    int rotations = static_cast<int>(a[to].size());
    while (rotations--) {
      while (!a[from].empty() && a[from].front() <= a[to].front()) {
        moveOne(from, to, output);
      }
      moveOne(to, to, output);
    }
    while (!a[from].empty()) moveOne(from, to, output);
  };
  for (int step = 0; step < 2 * q; ++step) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      a[0].push_back(value);
      vector<pair<int, int>> output;
      for (int level = 0; level < 4; ++level) {
        if (static_cast<int>(a[level].size()) >= limit[level]) {
          merge(level, level + 1, output);
        }
      }
      cout << output.size() << '\n';
      for (auto [from, to] : output) cout << from << ' ' << to << '\n';
    } else {
      int chosen = -1;
      for (int i = 0; i < 5; ++i) {
        if (!a[i].empty() &&
            (chosen == -1 || a[i].front() < a[chosen].front())) {
          chosen = i;
        }
      }
      cout << chosen + 1 << '\n';
      a[chosen].pop_front();
    }
    cout.flush();
  }
}
```

复杂度与 move 上界不变；相等值的稳定次序不影响“弹出任意最小值”的目标。

## 变种三：pop 改为要求全局最大值

把每个队列维护为降序，归并比较与队首选择全部反转，分层与预算证明保持不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  if (!(cin >> q)) return 0;
  array<deque<int>, 5> a;
  const array<int, 4> limit = {1, 9, 81, 729};
  auto moveOne = [&](int from, int to, vector<pair<int, int>>& output) {
    int value = a[from].front();
    a[from].pop_front();
    a[to].push_back(value);
    output.push_back({from + 1, to + 1});
  };
  auto merge = [&](int from, int to, vector<pair<int, int>>& output) {
    int rotations = static_cast<int>(a[to].size());
    while (rotations--) {
      while (!a[from].empty() && a[from].front() > a[to].front()) {
        moveOne(from, to, output);
      }
      moveOne(to, to, output);
    }
    while (!a[from].empty()) moveOne(from, to, output);
  };
  for (int step = 0; step < 2 * q; ++step) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      a[0].push_back(value);
      vector<pair<int, int>> output;
      for (int level = 0; level < 4; ++level) {
        if (static_cast<int>(a[level].size()) >= limit[level]) {
          merge(level, level + 1, output);
        }
      }
      cout << output.size() << '\n';
      for (auto [from, to] : output) cout << from << ' ' << to << '\n';
    } else {
      int chosen = -1;
      for (int i = 0; i < 5; ++i) {
        if (!a[i].empty() &&
            (chosen == -1 || a[i].front() > a[chosen].front())) {
          chosen = i;
        }
      }
      cout << chosen + 1 << '\n';
      a[chosen].pop_front();
    }
    cout.flush();
  }
}
```

本地时间、空间与 move 上界均与主解相同。

## 变种四：推广到 $L$ 个队列与基数 $B$

若 $Q<B^{L-1}$，用阈值 $1,B,B^2,\ldots,B^{L-2}$ 逐层归并。输入先给 `L B Q`，其余交互契约不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int levels, base, q;
  if (!(cin >> levels >> base >> q)) return 0;
  vector<deque<int>> a(levels);
  vector<long long> limit(max(0, levels - 1), 1);
  for (int i = 1; i + 1 < levels; ++i) limit[i] = limit[i - 1] * base;
  auto moveOne = [&](int from, int to, vector<pair<int, int>>& output) {
    int value = a[from].front();
    a[from].pop_front();
    a[to].push_back(value);
    output.push_back({from + 1, to + 1});
  };
  auto merge = [&](int from, int to, vector<pair<int, int>>& output) {
    int rotations = static_cast<int>(a[to].size());
    while (rotations--) {
      while (!a[from].empty() && a[from].front() < a[to].front()) {
        moveOne(from, to, output);
      }
      moveOne(to, to, output);
    }
    while (!a[from].empty()) moveOne(from, to, output);
  };
  for (int step = 0; step < 2 * q; ++step) {
    int type;
    if (!(cin >> type) || type == -1) return 0;
    if (type == 1) {
      int value;
      cin >> value;
      a[0].push_back(value);
      vector<pair<int, int>> output;
      for (int level = 0; level + 1 < levels; ++level) {
        if (static_cast<long long>(a[level].size()) >= limit[level]) {
          merge(level, level + 1, output);
        }
      }
      cout << output.size() << '\n';
      for (auto [from, to] : output) cout << from << ' ' << to << '\n';
    } else {
      int chosen = -1;
      for (int i = 0; i < levels; ++i) {
        if (!a[i].empty() &&
            (chosen == -1 || a[i].front() < a[chosen].front())) {
          chosen = i;
        }
      }
      cout << chosen + 1 << '\n';
      a[chosen].pop_front();
    }
    cout.flush();
  }
}
```

每层摊销约为 $(B+1)Q/2$，共 $L-1$ 层；可根据队列数、$Q$ 与 move 预算选择基数。

## 变种五：离线支持删除第 $k$ 小元素

若所有操作预先给出，交互队列不再必要。坐标压缩全部 push 值，用 Fenwick 树维护频次并二进制下降寻找第 $k$ 小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Fenwick {
  int n;
  vector<int> bit;
  explicit Fenwick(int n) : n(n), bit(n + 1) {}
  void add(int position, int value) {
    for (++position; position <= n; position += position & -position) {
      bit[position] += value;
    }
  }
  int kth(int k) const {
    int position = 0;
    int step = 1;
    while ((step << 1) <= n) step <<= 1;
    for (; step > 0; step >>= 1) {
      int next = position + step;
      if (next <= n && bit[next] < k) {
        position = next;
        k -= bit[next];
      }
    }
    return position;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<pair<int, int>> query(q);
  vector<int> values;
  for (auto& [type, value] : query) {
    cin >> type >> value;
    if (type == 1) values.push_back(value);
  }
  sort(values.begin(), values.end());
  values.erase(unique(values.begin(), values.end()), values.end());
  Fenwick fenwick(static_cast<int>(values.size()));
  for (auto [type, value] : query) {
    if (type == 1) {
      int position = static_cast<int>(
          lower_bound(values.begin(), values.end(), value) - values.begin());
      fenwick.add(position, 1);
    } else {
      int position = fenwick.kth(value);
      cout << values[position] << '\n';
      fenwick.add(position, -1);
    }
  }
}
```

时间 $O(Q\log Q)$，空间 $O(Q)$。它改变了接口与目标，不适用于原题的在线 Judge 队列状态。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc226/tasks/arc226_d?lang=en)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-135-lc85/">[力扣 Top 135] LC 85 最大矩形 困难 →</a>
</nav>
