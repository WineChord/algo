---
title: "[力扣竞赛] 第 515 场周赛 Q3 LC 4026 工位的最大间隔 中等"
---

# [力扣竞赛] 第 515 场周赛 Q3 LC 4026 工位的最大间隔 中等

<p class="daily-archive-kicker">2026-08-20 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-20 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ad4cdef42ab232435be0ff5017b900944b8b591fe9aee8f8b2f48ddb54e168f3 -->
[官方题目：4026. 工位的最大间隔](https://leetcode.cn/problems/maximum-gap-between-stations/)

## 官方原始信息

- 比赛：第 515 场周赛，Q3。
- 题号与标题：4026. 工位的最大间隔。
- 官方难度：中等；比赛页面给出的题目分值为 5 分。
- ZeroTracer 社区估算竞赛分：截至 2026-08-20 的公开数据中未找到本题数值，记为未知。
- 官方链接：[LeetCode 中国题面](https://leetcode.cn/problems/maximum-gap-between-stations/)。
- 函数签名：`int maximumGap(string skill, string station)`。

给定长度分别为 $n$ 和 $m$ 的字符串 `skill`、`station`。工人 $i$ 需要字符
`skill[i]` 所代表的技能，工位 $j$ 支持 `station[j]`。要为每名工人选择互不相同的工位
$j_0,j_1,\ldots,j_{n-1}$，并满足

$$
\texttt{station}[j_i]=\texttt{skill}[i],\qquad
j_0<j_1<\cdots<j_{n-1}.
$$

一个分配的间隔定义为 $\max_{1\le i<n}(j_i-j_{i-1})$；若 $n=1$，间隔为 0。返回所有
有效分配中可能得到的最大间隔。题目保证至少存在一种有效分配。

### 全部官方样例

示例 1：

```text
输入：skill = "aa", station = "aaaa"
输出：3
解释：选择工位 [0,3]，唯一相邻差为 3。
```

示例 2：

```text
输入：skill = "xyz", station = "xyzz"
输出：2
解释：选择 [0,1,3]，相邻差为 [1,2]，间隔为 2。
```

示例 3：

```text
输入：skill = "cbc", station = "cbcdbc"
输出：4
解释：选择 [0,1,5]，相邻差为 [1,4]，间隔为 4。
```

### 全部约束

- `skill.length == n`。
- `station.length == m`。
- $1\le n\le m\le10^5$。
- 两个字符串都只含小写英文字母。
- 至少存在一种完整有效分配。

## 约束推导与核心转折

$m$ 可达 $10^5$，不能枚举所有子序列嵌入。目标里虽然有一个 `max`，但任何具体分配的
最大间隔一定由某个相邻分界 $i-1\mid i$ 实现。固定这个分界后，要把差
$j_i-j_{i-1}$ 拉到最大：

- 左半边工人 $0\ldots i-1$ 应尽量靠左，尤其让 $j_{i-1}$ 最小；
- 右半边工人 $i\ldots n-1$ 应尽量靠右，尤其让 $j_i$ 最大。

从左贪心匹配得到 `earliest[i]`，即工人 $i$ 在任意有效前缀分配中的最小可能工位；从右
贪心匹配得到 `latest[i]`，即任意有效后缀分配中的最大可能工位。于是答案为

$$
\max_{1\le i<n}\bigl(\texttt{latest}[i]-\texttt{earliest}[i-1]\bigr).
$$

下标差至多 $m-1<10^5$，`int` 足够。

## 样例手推与边界

示例 3 中 `skill = "cbc"`、`station = "cbcdbc"`：

- 从左匹配得 `earliest = [0,1,2]`；
- 从右匹配得 `latest = [3,4,5]`；
- 两处分界分别给出 $4-0=4$ 与 $5-1=4$，答案为 4。

把第一处分界的左前缀 `[0]` 与右后缀 `[4,5]` 拼接，得到有效分配 `[0,4,5]`；官方的
`[0,1,5]` 则在第二处分界达到同样答案。

边界包括：$n=1$ 时没有相邻对，答案为 0；$n=m>1$ 时唯一分配是全部位置，答案为 1，而
$n=m=1$ 时仍为 0；重复字符可能让最早、最晚位置相距很远；某处分界的极值不要求其他
分界也同时最优。

## 解法一：枚举全部子序列嵌入

DFS 依次为每名工人选择一个更靠后的同技能工位；完成一组分配后计算其最大相邻差并更新
答案。它枚举了定义允许的每个分配，所以正确，但最坏有 $\binom{m}{n}$ 个状态。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumGap(string skill, string station) {
    vector<int> positions;
    int answer = 0;
    enumerate(skill, station, 0, 0, positions, answer);
    return answer;
  }
private:
  void enumerate(const string& skill, const string& station, int worker,
      int start, vector<int>& positions, int& answer) {
    if (worker == static_cast<int>(skill.size())) {
      int gap = 0;
      for (int i = 1; i < static_cast<int>(positions.size()); ++i) {
        gap = max(gap, positions[i] - positions[i - 1]);
      }
      answer = max(answer, gap);
      return;
    }
    int remaining = skill.size() - worker;
    for (int position = start;
        position + remaining <= static_cast<int>(station.size()); ++position) {
      if (station[position] != skill[worker]) continue;
      positions.push_back(position);
      enumerate(skill, station, worker + 1, position + 1, positions, answer);
      positions.pop_back();
    }
  }
};
```

时间复杂度为 $O(\binom{m}{n}n)$，递归与当前方案空间为 $O(n)$。瓶颈是对大量方案重复求
相同前缀的最早位置与相同后缀的最晚位置。

## 从暴力到最优：把方案极值压缩成两个数组

左到右扫描 `station`，对 `skill[i]` 取第一个可用匹配；交换论证表明，任何更晚选择都不会
让当前或后续工人的最早位置更小，因此得到真正的 `earliest`。反向同理得到 `latest`。

固定分界 $i$ 时，任意完整分配 $p$ 都满足

$$
\texttt{earliest}[i-1]\le p_{i-1}<p_i\le\texttt{latest}[i].
$$

所以该分界的差至多为公式值。反过来，取左侧最早前缀与右侧最晚后缀即可同时达到这两个
端点；上式还保证连接处严格递增，故它们可以拼成完整分配。

## 最佳实用解：双向贪心

### 正确性证明

**引理 1**：`earliest[i]` 是工人 $i$ 在所有有效前缀分配中的最小工位。

对 $i=0$ 显然成立。若前 $i-1$ 人已取各自最早位置，任何其他有效前缀的第 $i-1$ 个位置
不会更早；从更晚起点寻找 `skill[i]` 的首次出现也不会早于算法结果，归纳成立。

**引理 2**：`latest[i]` 是工人 $i$ 在所有有效后缀分配中的最大工位。

把引理 1 的方向全部反转即可。

**引理 3**：固定 $i$，最大可能的 $j_i-j_{i-1}$ 等于
`latest[i] - earliest[i - 1]`。

上界由引理 1、2 得出。题目保证存在完整分配 $p$，所以
`earliest[i - 1] <= p[i - 1] < p[i] <= latest[i]`；最早前缀与最晚后缀在分界处可拼接，
达到该上界。

**定理**：算法返回所有有效分配中的最大间隔。

任一方案的间隔由某个分界产生，引理 3 给出该分界可达到的精确最大值；枚举所有分界并取
最大，既不遗漏任何方案上界，也构造性地可达到，因此答案正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumGap(string skill, string station) {
    int n = skill.size();
    int m = station.size();
    if (n == 1) return 0;
    vector<int> earliest(n), latest(n);
    int position = 0;
    for (int worker = 0; worker < n; ++worker) {
      while (station[position] != skill[worker]) ++position;
      earliest[worker] = position++;
    }
    position = m - 1;
    for (int worker = n - 1; worker >= 0; --worker) {
      while (station[position] != skill[worker]) --position;
      latest[worker] = position--;
    }
    int answer = 0;
    for (int worker = 1; worker < n; ++worker) {
      answer = max(answer, latest[worker] - earliest[worker - 1]);
    }
    return answer;
  }
};
```

时间复杂度 $O(n+m)$，额外空间 $O(n)$。也可以只保留 `earliest`，在反向扫描时即时计算，
仍为 $O(n)$ 空间。建议记住“枚举目标中的相邻分界，再用最早前缀与最晚后缀把两端拉开”；
它比对答案二分更直接，也给出精确构造。

## 易错点

- 把答案写成 `latest[i] - earliest[i]`；间隔两端属于相邻工人 $i-1$ 与 $i$。
- 只求整个 `skill` 的最早、最晚嵌入后比较首尾；目标是最大相邻差，不是总跨度。
- 误认为每个相邻差必须在同一组“全局最早/最晚”方案中同时取到；我们只需某处分界达到
  全局最大。
- $n=1$ 时循环没有分界，应返回 0。
- 忘记题目已保证可匹配，若迁移到不保证可行的版本，双向扫描必须增加越界判断。

## 可复现验证

三组官方样例均通过。最佳实现按 C++23 编译；对小写字母表、$1\le n\le m\le9$ 的随机
实例，先筛出 `skill` 为 `station` 子序列的情况，再与 DFS 枚举全部嵌入的答案逐项比较。
测试覆盖单工人、唯一嵌入、全同字符、答案在首处分界、答案在末处分界和多个分界并列。

## 变种一：恢复一组达到最大间隔的分配

新定义：同时返回答案与一组工位下标。记录取得最大值的分界 $i$，拼接
`earliest[0..i-1]` 与 `latest[i..n-1]`。引理 3 已证明拼接合法。时间 $O(n+m)$，空间
$O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class AssignmentSolution {
public:
  pair<int, vector<int>> maximumGap(string skill, string station) {
    int n = skill.size();
    int m = station.size();
    vector<int> earliest(n), latest(n);
    for (int i = 0, p = 0; i < n; ++i) {
      while (station[p] != skill[i]) ++p;
      earliest[i] = p++;
    }
    for (int i = n - 1, p = m - 1; i >= 0; --i) {
      while (station[p] != skill[i]) --p;
      latest[i] = p--;
    }
    if (n == 1) return {0, {earliest[0]}};
    int split = 1;
    for (int i = 2; i < n; ++i) {
      if (latest[i] - earliest[i - 1] >
          latest[split] - earliest[split - 1]) split = i;
    }
    vector<int> assignment;
    assignment.insert(assignment.end(), earliest.begin(), earliest.begin() + split);
    assignment.insert(assignment.end(), latest.begin() + split, latest.end());
    return {latest[split] - earliest[split - 1], assignment};
  }
};
```

## 变种二：统计全部有效分配

新定义：返回 `skill` 作为 `station` 子序列的嵌入数，模 $10^9+7$。极值数组不再能表达
计数；令 DP 表示上一个工人恰好放在各工位的方案数，并用前缀和转移。时间 $O(nm)$，空间
$O(m)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class CountAssignments {
public:
  int count(string skill, string station) {
    constexpr int mod = 1000000007;
    int m = station.size();
    vector<int> ways(m);
    for (int j = 0; j < m; ++j) ways[j] = station[j] == skill[0];
    for (int i = 1; i < static_cast<int>(skill.size()); ++i) {
      vector<int> next(m);
      long long prefix = 0;
      for (int j = 0; j < m; ++j) {
        if (station[j] == skill[i]) next[j] = prefix;
        prefix += ways[j];
        prefix %= mod;
      }
      ways.swap(next);
    }
    return accumulate(ways.begin(), ways.end(), 0LL) % mod;
  }
};
```

## 变种三：最大化最小相邻间隔

新定义：目标改为最大化 $\min_{1\le i<n}(j_i-j_{i-1})$。最早/最晚的一处分界公式失效，
因为现在所有分界都要同时满足下界。对候选距离 $d$，从最早的首字符开始，每次在对应字符
的位置表中二分第一个不小于 `last + d` 的工位；最早选择为后续留下最多空间，故贪心判定
正确。$n>1$ 时真实答案至少为 1，因此只判定 $d\ge1$，既保持下标严格递增，也避开 $d=0$
时重复使用同一工位。可行性对 $d$ 单调，二分答案。时间 $O(n\log m\log m)$，空间 $O(m)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MaximizeMinimumGap {
public:
  int solve(string skill, string station) {
    if (skill.size() == 1) return 0;
    vector<vector<int>> positions(26);
    for (int i = 0; i < static_cast<int>(station.size()); ++i) {
      positions[station[i] - 'a'].push_back(i);
    }
    auto feasible = [&](int distance) {
      int last = -distance;
      for (char required : skill) {
        const auto& list = positions[required - 'a'];
        auto it = lower_bound(list.begin(), list.end(), last + distance);
        if (it == list.end()) return false;
        last = *it;
      }
      return true;
    };
    int low = 1;
    int high = station.size();
    while (low + 1 < high) {
      int middle = (low + high) / 2;
      if (feasible(middle)) low = middle;
      else high = middle;
    }
    return low;
  }
};
```

## 变种四：固定工位串上的多次技能查询

新定义：`station` 固定，回答很多 `skill`。预处理 26 个字符的位置表；每个查询用二分分别
求最早与最晚嵌入，若不可行返回 -1。单次长度为 $n$ 的查询耗时 $O(n\log m)$，共享预处理
空间 $O(m)$；当查询很短时比每次扫描整个工位串更合适。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class StationIndex {
public:
  explicit StationIndex(const string& station) {
    for (int i = 0; i < static_cast<int>(station.size()); ++i) {
      positions_[station[i] - 'a'].push_back(i);
    }
  }
  int maximumGap(const string& skill) const {
    int n = skill.size();
    if (n == 1) return positions_[skill[0] - 'a'].empty() ? -1 : 0;
    vector<int> earliest(n), latest(n);
    int last = -1;
    for (int i = 0; i < n; ++i) {
      const auto& list = positions_[skill[i] - 'a'];
      auto it = upper_bound(list.begin(), list.end(), last);
      if (it == list.end()) return -1;
      earliest[i] = last = *it;
    }
    last = numeric_limits<int>::max();
    for (int i = n - 1; i >= 0; --i) {
      const auto& list = positions_[skill[i] - 'a'];
      auto it = lower_bound(list.begin(), list.end(), last);
      if (it == list.begin()) return -1;
      latest[i] = last = *prev(it);
    }
    int answer = 0;
    for (int i = 1; i < n; ++i) {
      answer = max(answer, latest[i] - earliest[i - 1]);
    }
    return answer;
  }
private:
  array<vector<int>, 26> positions_;
};
```

## 来源

- [LeetCode 4026 官方题面](https://leetcode.cn/problems/maximum-gap-between-stations/)，核对于 2026-08-20。
- [第 515 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-515/)，核对于 2026-08-20。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximum-gap-between-stations/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-140-lc199/">← [力扣 Top 140] LC 199 二叉树的右视图 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-c/">[codeforces] CF Round 1117 Div.2 C Spying on the Beaver →</a>
</nav>
