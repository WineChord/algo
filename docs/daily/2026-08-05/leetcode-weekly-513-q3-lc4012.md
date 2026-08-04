---
title: "[力扣竞赛] 第 513 场周赛 Q3 LC 4012 统计每个班次结束后的未完成任务数 中等"
---

# [力扣竞赛] 第 513 场周赛 Q3 LC 4012 统计每个班次结束后的未完成任务数 中等

<p class="daily-archive-kicker">2026-08-05 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=98c95446f2206eb21666c3d04ec202b2daf70c3e8359b3cc76c929ba10fa8a74 -->
## 官方原始信息

- 来源：力扣中国第 513 场周赛
- 竞赛题序：Q3
- 题号：LC 4012
- 官方中文标题：统计每个班次结束后的未完成任务数
- 官方难度：中等
- 官方比赛分值：5
- ZeroTracer 社区估算竞赛分：未知（抓取于 2026-08-05）
- 官方链接：[统计每个班次结束后的未完成任务数](https://leetcode.cn/problems/count-of-unfinished-tasks-after-each-shift/)

### 原始题意

`tasks[i]` 是按顺序完成第 `i` 个任务所需时间，`shifts[j]` 是第 `j` 个班次可用时间。未完成任务可在下一班次从原进度继续；但若某班次内完成全部任务，该班次立即结束并丢弃剩余时间，下一班次从任务 0 重新开始。返回每个班次结束后的未完成任务数，正在处理但未完成的任务也计入。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> countTasks(vector<int>& tasks, vector<int>& shifts);
};
```

### 全部官方样例

```text
输入：tasks = [1,4,4], shifts = [9,1,4]
输出：[0,2,1]
解释：首班恰好完成全部任务；第二班完成任务 0；第三班继续并完成任务 1。
```

```text
输入：tasks = [2,3,4], shifts = [20,4,5]
输出：[0,2,0]
解释：首班完成全部任务后丢弃多余 11；后两班从新一轮开始并共同完成全部任务。
```

```text
输入：tasks = [4,2], shifts = [3,6,1]
输出：[2,0,2]
解释：第一班只完成任务 0 的前三单位；第二班完成剩余整轮并丢弃余时；第三班重新处理任务 0。
```

### 全部约束

- $1\le tasks.length\le10^5$。
- $1\le shifts.length\le10^5$。
- $1\le tasks[i]\le10^9$。
- $1\le shifts[i]\le10^9$。

## 约束推导与观察

单轮任务总时间最多 $10^{14}$，进度与前缀和必须使用 64 位。设 `done` 为当前这一轮从任务 0 开始已经完成的工作量，始终保持 $0\le done<total$：

- 若 `done + shift >= total`，本班完成全部任务，答案为 0，并把下一班进度重置为 0；多余时间不能取模延续。
- 否则令 `done += shift`，在严格递增前缀和中二分最后一个不超过 `done` 的前缀。已完整完成 `c` 个任务，未完成数为 `n-c`。

## 解法递进

### 解法一：逐任务模拟每个班次

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> countTasks(vector<int>& tasks, vector<int>& shifts) {
    int n = tasks.size();
    int index = 0;
    long long remaining = tasks[0];
    vector<int> answer;
    for (long long available : shifts) {
      while (available >= remaining) {
        available -= remaining;
        ++index;
        if (index == n) {
          index = 0;
          remaining = tasks[0];
          available = 0;
          break;
        }
        remaining = tasks[index];
      }
      if (available > 0) {
        remaining -= available;
      }
      answer.push_back(index == 0 && remaining == tasks[0] ? 0 : n - index);
    }
    return answer;
  }
};
```

最坏时间 $O(nm)$，空间 $O(m)$。每个很长班次都可能逐个跨越大量任务，是瓶颈。

### 最佳实用解：前缀和加二分

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> countTasks(vector<int>& tasks, vector<int>& shifts) {
    int n = tasks.size();
    vector<long long> prefix(n);
    partial_sum(tasks.begin(), tasks.end(), prefix.begin());
    long long total = prefix.back();
    long long done = 0;
    vector<int> answer;
    answer.reserve(shifts.size());
    for (long long available : shifts) {
      if (done + available >= total) {
        answer.push_back(0);
        done = 0;
        continue;
      }
      done += available;
      int completed = upper_bound(prefix.begin(), prefix.end(), done) - prefix.begin();
      answer.push_back(n - completed);
    }
    return answer;
  }
};
```

预处理 $O(n)$，每个班次 $O(\log n)$，总时间 $O(n+m\log n)$，空间 $O(n+m)$（含返回值）。

## 正确性证明

循环开始时 `done` 等于当前轮已完成的总工作量，且若上一班完成整轮则为 0。若 `done+available>=total`，按题意本班必完成所有任务、答案为 0，并丢弃余时，所以重置保持不变量。否则新进度仍小于 `total`；前缀和 `prefix[i]` 是完成任务 0 到 `i` 的必要且充分累计时间，`upper_bound(done)` 前的前缀恰是不超过当前进度的完整任务，因此 `n-completed` 正好包括当前部分完成任务与其后所有任务。归纳可知每班答案正确。

## 样例手推

样例 1 前缀为 `[1,5,9]`。班次 9 使总量达到 9，输出 0 并重置；班次 1 后 `done=1`，完成一个任务，输出 2；班次 4 后 `done=5`，完成两个，输出 1。样例 2 的首班 20 不能留下 `20 mod 9=2`，必须直接重置为 0。

## 易错点与方案比较

- 完成整轮时要丢弃本班剩余时间，不能循环到下一轮。
- `done` 与前缀和用 `long long`。
- 恰好完成某任务时，该任务不再算未完成，因此使用 `upper_bound`。
- 逐任务模拟易懂但最坏超时；前缀二分稳定且满足规模，应优先记忆。

## 变种一：完成一轮后保留班次剩余时间

新定义：工作连续循环，不丢弃余时。新进度为 `(done+shift)%total`；余数为 0 表示恰在轮末，未完成数为 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  cin >> n >> m;
  vector<long long> prefix(n);
  for (int i = 0; i < n; ++i) {
    cin >> prefix[i];
    if (i) {
      prefix[i] += prefix[i - 1];
    }
  }
  long long total = prefix.back();
  long long done = 0;
  while (m--) {
    long long shift;
    cin >> shift;
    long long raw = done + shift;
    done = raw % total;
    if (done == 0) {
      cout << 0 << '\n';
    } else {
      int completed = upper_bound(prefix.begin(), prefix.end(), done) - prefix.begin();
      cout << n - completed << '\n';
    }
  }
}
```

时间 $O(n+m\log n)$，空间 $O(n)$。这正是原题“丢弃余时”规则改变后不能复用的状态转移。

## 变种二：同时报告当前任务和该任务已完成时间

新定义：未完成时返回 `(任务下标, 该任务已完成量, 未完成任务数)`；完成整轮时返回 `(-1,0,0)`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  cin >> n >> m;
  vector<long long> prefix(n);
  for (int i = 0; i < n; ++i) {
    cin >> prefix[i];
    if (i) {
      prefix[i] += prefix[i - 1];
    }
  }
  long long done = 0;
  while (m--) {
    long long shift;
    cin >> shift;
    if (done + shift >= prefix.back()) {
      done = 0;
      cout << "-1 0 0\n";
      continue;
    }
    done += shift;
    int index = upper_bound(prefix.begin(), prefix.end(), done) - prefix.begin();
    long long before = index == 0 ? 0 : prefix[index - 1];
    cout << index << ' ' << done - before << ' ' << n - index << '\n';
  }
}
```

时间 $O(n+m\log n)$，空间 $O(n)$。原答案只保留计数，恢复细节需要保留二分位置。

## 变种三：允许零耗时任务

新定义：`tasks[i]` 可为 0，前缀和不再严格递增，但 `upper_bound` 仍会一次跨过所有已完成的零耗时任务；若总时间为 0，每班都输出 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  cin >> n >> m;
  vector<long long> prefix(n);
  for (int i = 0; i < n; ++i) {
    cin >> prefix[i];
    if (i) {
      prefix[i] += prefix[i - 1];
    }
  }
  long long done = 0;
  while (m--) {
    long long shift;
    cin >> shift;
    if (prefix.back() == 0 || done + shift >= prefix.back()) {
      done = 0;
      cout << 0 << '\n';
    } else {
      done += shift;
      int completed = upper_bound(prefix.begin(), prefix.end(), done) - prefix.begin();
      cout << n - completed << '\n';
    }
  }
}
```

时间 $O(n+m\log n)$，空间 $O(n)$。必须显式处理总时间 0，避免后续扩展中的除零或错误状态。

## 变种四：任务时长在线更新，询问从新一轮开始能完成多少任务

新定义：更新单个任务时长；每次独立询问从任务 0 开始、给定工作量，问完整完成多少任务。Fenwick 树支持前缀和更新与前缀上界搜索。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  int n;
  vector<long long> tree;
public:
  explicit Fenwick(int size) : n(size), tree(size + 1) {
  }
  void add(int index, long long delta) {
    for (++index; index <= n; index += index & -index) {
      tree[index] += delta;
    }
  }
  int countPrefixAtMost(long long limit) const {
    int index = 0;
    long long sum = 0;
    int step = 1;
    while (step <= n / 2) {
      step *= 2;
    }
    for (; step; step >>= 1) {
      int next = index + step;
      if (next <= n && sum + tree[next] <= limit) {
        index = next;
        sum += tree[next];
      }
    }
    return index;
  }
};
int main() {
  int n, operations;
  cin >> n >> operations;
  vector<long long> task(n);
  Fenwick fenwick(n);
  for (int i = 0; i < n; ++i) {
    cin >> task[i];
    fenwick.add(i, task[i]);
  }
  while (operations--) {
    char type;
    cin >> type;
    if (type == 'U') {
      int index;
      long long value;
      cin >> index >> value;
      --index;
      fenwick.add(index, value - task[index]);
      task[index] = value;
    } else {
      long long work;
      cin >> work;
      cout << fenwick.countPrefixAtMost(work) << '\n';
    }
  }
}
```

更新与询问均为 $O(\log n)$，空间 $O(n)$。原静态前缀数组无法承受在线修改；这里询问彼此独立，避免修改进行中任务的语义歧义。

## 验证说明

本轮将六段代码按 C++23 编译；前缀二分会与逐任务模拟对拍 40,000 个随机实例，并覆盖恰好完成、超长班次丢弃余时、连续重置、单任务和总和接近 $10^{14}$。四个变种分别使用直接模拟或重建前缀作为 oracle。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/count-of-unfinished-tasks-after-each-shift/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-110-lc84/">← [力扣 Top 110] LC 84 柱状图中最大的矩形 困难</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-d/">[codeforces] CF Round 1113 Div.2 D Good Pair Queries →</a>
</nav>
