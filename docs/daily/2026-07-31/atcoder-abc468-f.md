---
title: "[atcoder] ABC468 F Chmax"
---

# [atcoder] ABC468 F Chmax

<p class="daily-archive-kicker">2026-07-31 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../dp/sequence-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=24f74edd06143b299e37360f35e1298da67372db905892ca7dfe1fe5a9542eb3 -->
## 官方来源与元数据

- 来源：AtCoder。
- 比赛：AtCoder Beginner Contest 468。
- 题号与标题：F - Chmax。
- 官方分值：500 分。
- 比赛 Rated Range：0–1999。
- 时间限制：2 秒。
- 内存限制：1024 MiB。
- 官方题面：[ABC468 F - Chmax](https://atcoder.jp/contests/abc468/tasks/abc468_f?lang=en)。
- 版权条款：[AtCoder Terms of Service](https://atcoder.jp/tos)。

普通 AtCoder 比赛题面没有已确认的统一开放转载许可。下方英文层依据官方题面独立组织，完整保留任务定义、输入输出、约束、样例与必要说明；官方页面仍是事实核验的权威入口。

## Complete English statement

- Contest: AtCoder Beginner Contest 468
- Task: F - Chmax
- Official score: 500 points
- Rated range: 0–1999
- Time limit: 2 seconds
- Memory limit: 1024 MiB
- Official task: [ABC468 F - Chmax](https://atcoder.jp/contests/abc468/tasks/abc468_f?lang=en)

This self-contained English presentation was independently organized from the official task and preserves its complete meaning, input, output, constraints, and samples. It is not represented as a verbatim reproduction. See the official task and the [AtCoder Terms of Service](https://atcoder.jp/tos).

### Problem Statement

You are given a positive integer $N$ and a permutation

$$
P=(P_1,P_2,\ldots,P_N)
$$

of $(1,2,\ldots,N)$.

There are three variables $x,y,c$. Initially,

$$
x=y=c=0.
$$

For $k=1,2,\ldots,N$ in this order, perform exactly one of the following operations:

- **Operation 1:** if $x<P_k$, increase $c$ by $1$. Then replace $x$ with $\max(x,P_k)$.
- **Operation 2:** if $y<P_k$, increase $c$ by $1$. Then replace $y$ with $\max(y,P_k)$.

Find the maximum possible final value of $c$.

### Input

```text
N
P_1 P_2 ... P_N
```

### Output

Output the maximum possible final value of $c$.

### Complete Constraints

$$
1\le N\le5\times10^5
$$

$P$ is a permutation of $(1,2,\ldots,N)$, and all input values are integers.

### Official Sample 1

```text
5
4 3 1 2 5
```

```text
4
```

One optimal operation sequence is $1,1,2,2,2$. The states $(x,y,c)$ become

```text
(4,0,1)
(4,0,1)
(4,1,2)
(4,2,3)
(4,5,4)
```

No operation sequence can make $c$ exceed $4$.

### Official Sample 2

```text
6
6 5 4 3 2 1
```

```text
2
```

### Official Sample 3

```text
9
3 6 5 2 7 8 9 1 4
```

```text
7
```

The official statement gives no additional explanation for Samples 2 and 3.

## 中文题意与元数据说明

把每个排列元素依次交给变量 `x` 或 `y`。若它严格大于所选变量的历史最大值，就得到 1 分，然后该变量更新为二者最大值。目标是最大化总得分。

AtCoder 官方未标注独立题目难度。AtCoder Problems 社区模型在 2026-07-31 的估算难度为 1693；这是社区估算，不是 AtCoder 官方难度。

## 约束推导

$N$ 达到 $5\times10^5$，不能保留所有 $(x,y)$ 状态，更不能枚举 $2^N$ 个操作序列。关键是处理完任意前缀后，

$$
\max(x,y)=\max(P_1,\ldots,P_k).
$$

若 $P_k$ 是新的严格前缀最大值，它同时大于 `x` 与 `y`，必然得分。把它交给当前较大变量会保留较小变量的低门槛；交给较小变量只会把低门槛抬到旧前缀最大值，后者被前者支配。

删除全部严格前缀最大值，得到序列 $Q$。其余元素只有在交给较小变量且严格大于该变量时才得分，因此所有这类得分元素按出现顺序组成 $Q$ 的严格递增子序列。

## 解法递进

### 解法一：枚举全部操作序列

对每个位置枚举选择操作 1 或 2，完整覆盖所有 $2^N$ 种方案。它只适合小规模对拍。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n);
  for (int& value : p) {
    cin >> value;
  }
  int answer = 0;
  function<void(int, int, int, int)> dfs = [&](int i, int x, int y, int score) {
    if (i == n) {
      answer = max(answer, score);
      return;
    }
    dfs(i + 1, max(x, p[i]), y, score + (x < p[i]));
    dfs(i + 1, x, max(y, p[i]), score + (y < p[i]));
  };
  dfs(0, 0, 0, 0);
  cout << answer << '\n';
}
```

时间 $O(2^N)$，递归空间 $O(N)$。

### 最佳实用解：前缀最大值计数加 LIS

扫描排列：

- 新的严格前缀最大值必得 1 分，计入 `records`；
- 其余元素放入序列 $Q$，用最小末尾值数组 `tails` 求严格 LIS。

答案为

$$
records+\operatorname{LIS}(Q).
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  int maximum = 0;
  int records = 0;
  vector<int> tails;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    if (value > maximum) {
      maximum = value;
      ++records;
    } else {
      auto it = lower_bound(tails.begin(), tails.end(), value);
      if (it == tails.end()) {
        tails.push_back(value);
      } else {
        *it = value;
      }
    }
  }
  cout << records + static_cast<int>(tails.size()) << '\n';
}
```

时间复杂度 $O(N\log N)$，空间复杂度 $O(N)$。答案不超过 $N$，`int` 足够。

## 正确性证明

每个严格前缀最大值都大于两个变量，因此无论选择哪种操作都得分。把它交给当前较大变量不会改变较小变量；另一选择会把较小变量抬高到旧前缀最大值，不可能增加未来选择，所以存在最优方案采用前者。

对非前缀最大值，交给较大变量既不得分也不改变状态；只有严格大于较小变量时交给较小变量才得分，并把较小变量更新为该值。因此这些得分元素严格递增，数量至多为 $\operatorname{LIS}(Q)$。

反过来，取 $Q$ 的任意一条最长严格递增子序列：前缀最大值与未选中的 $Q$ 元素交给较大变量，LIS 元素交给较小变量。每个前缀最大值和每个 LIS 元素都恰好得分，所以达到上界，公式成立。

## 样例手推

样例 3 的严格前缀最大值为 $3,6,7,8,9$，共 5 个。删除后

$$
Q=(5,2,1,4),
$$

其 LIS 长度为 2，例如 $(1,4)$，答案为 $5+2=7$。

## 易错点与方案比较

- 删除的是严格前缀最大值，不是局部峰值或后缀最大值。
- 严格 LIS 必须使用 `lower_bound`；重复值变种中也一样。
- 不能把问题误写成“用两个递增子序列覆盖最多元素”，前缀最大值会固定占用并抬高较大变量。
- 枚举解适合作 oracle；最优解只保留 LIS 的最小末尾值，推荐记忆“必得记录点 + 可选严格 LIS”这一分解。

## 变种一：每个成功位置带权

新定义：位置 $i$ 成功时获得权重 $w_i$。前缀最大值权重全部计入；其余位置求最大权严格递增子序列。坐标压缩后用 Fenwick 树维护值域前缀最大权。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n);
  vector<int64> weight(n);
  for (int& value : p) {
    cin >> value;
  }
  for (int64& value : weight) {
    cin >> value;
  }
  vector<int> values = p;
  sort(values.begin(), values.end());
  values.erase(unique(values.begin(), values.end()), values.end());
  vector<int64> bit(values.size() + 1);
  auto query = [&](int index) {
    int64 answer = 0;
    for (; index > 0; index -= index & -index) {
      answer = max(answer, bit[index]);
    }
    return answer;
  };
  auto update = [&](int index, int64 value) {
    for (; index < static_cast<int>(bit.size()); index += index & -index) {
      bit[index] = max(bit[index], value);
    }
  };
  int maximum = numeric_limits<int>::min();
  int64 fixed = 0;
  for (int i = 0; i < n; ++i) {
    if (p[i] > maximum) {
      maximum = p[i];
      fixed += weight[i];
      continue;
    }
    int rank = lower_bound(values.begin(), values.end(), p[i]) - values.begin() + 1;
    update(rank, query(rank - 1) + max<int64>(0, weight[i]));
  }
  cout << fixed + query(values.size()) << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。若权重允许为负，非前缀最大值可以跳过。

## 变种二：恢复一组最优操作

新定义：输出最大分数以及每一步选择的操作编号。恢复 $Q$ 的一条 LIS，再按证明中的构造模拟两个变量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> p(n), parent(n, -1), tailValue, tailIndex, record(n);
  for (int& value : p) {
    cin >> value;
  }
  int maximum = 0;
  for (int i = 0; i < n; ++i) {
    if (p[i] > maximum) {
      maximum = p[i];
      record[i] = 1;
      continue;
    }
    int position = lower_bound(tailValue.begin(), tailValue.end(), p[i]) - tailValue.begin();
    if (position > 0) {
      parent[i] = tailIndex[position - 1];
    }
    if (position == static_cast<int>(tailValue.size())) {
      tailValue.push_back(p[i]);
      tailIndex.push_back(i);
    } else {
      tailValue[position] = p[i];
      tailIndex[position] = i;
    }
  }
  vector<int> chosen(n);
  if (!tailIndex.empty()) {
    for (int at = tailIndex.back(); at != -1; at = parent[at]) {
      chosen[at] = 1;
    }
  }
  int x = 0;
  int y = 0;
  vector<int> operation;
  for (int i = 0; i < n; ++i) {
    if (chosen[i]) {
      if (x <= y) {
        x = max(x, p[i]);
        operation.push_back(1);
      } else {
        y = max(y, p[i]);
        operation.push_back(2);
      }
    } else {
      if (x >= y) {
        x = max(x, p[i]);
        operation.push_back(1);
      } else {
        y = max(y, p[i]);
        operation.push_back(2);
      }
    }
  }
  cout << count(record.begin(), record.end(), 1) + tailValue.size() << '\n';
  for (int value : operation) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。

## 变种三：输入允许重复值与任意正整数

新定义：输入不再是排列。结论保持不变：严格前缀最大值按 `value > maximum` 判断，剩余序列求严格 LIS。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  long long maximum = numeric_limits<long long>::min();
  int records = 0;
  vector<long long> tails;
  for (int i = 0; i < n; ++i) {
    long long value;
    cin >> value;
    if (value > maximum) {
      maximum = value;
      ++records;
    } else {
      auto it = lower_bound(tails.begin(), tails.end(), value);
      if (it == tails.end()) {
        tails.push_back(value);
      } else {
        *it = value;
      }
    }
  }
  cout << records + static_cast<int>(tails.size()) << '\n';
}
```

时间 $O(N\log N)$，空间 $O(N)$。

## 变种四：每次追加后询问当前前缀答案

新定义：元素流式到达，每读入一个元素就输出当前前缀的最优分数。记录点计数与 `tails` 都可在线维护。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  long long maximum = numeric_limits<long long>::min();
  int records = 0;
  vector<long long> tails;
  while (q--) {
    long long value;
    cin >> value;
    if (value > maximum) {
      maximum = value;
      ++records;
    } else {
      auto it = lower_bound(tails.begin(), tails.end(), value);
      if (it == tails.end()) {
        tails.push_back(value);
      } else {
        *it = value;
      }
    }
    cout << records + tails.size() << '\n';
  }
}
```

每次追加 $O(\log N)$，总空间 $O(N)$。

## 可复现验证

- 三组官方样例分别得到 4、2、7。
- 对 $N\le8$ 的全部排列枚举所有 $2^N$ 个操作序列，并与“记录点计数 + LIS”逐项一致。
- 所有完整代码按 C++23 编译。

## Reference

- [AtCoder 官方题面](https://atcoder.jp/contests/abc468/tasks/abc468_f?lang=en)
- [AtCoder 官方题解](https://atcoder.jp/contests/abc468/editorial/23738)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
- [AtCoder Problems](https://kenkoooo.com/atcoder/#/table/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_f?lang=en)
- [对应知识专题](../../dp/sequence-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-51-lc33/">[力扣 Top 51] LC 33 搜索旋转排序数组 中等 →</a>
</nav>
