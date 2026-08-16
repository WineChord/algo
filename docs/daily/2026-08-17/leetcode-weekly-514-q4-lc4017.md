---
title: "[力扣竞赛] 第 514 场周赛 Q4 LC 4017 数组中的峰值 II 困难"
---

# [力扣竞赛] 第 514 场周赛 Q4 LC 4017 数组中的峰值 II 困难

<p class="daily-archive-kicker">2026-08-17 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-17 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=fd4a17dc41097baea6d80fde4c4430aca6ae8b818837a413502ebb8aec35e732 -->
[力扣 4017：数组中的峰值 II](https://leetcode.cn/problems/peaks-in-array-ii/)

## 官方原始信息

- 比赛：第 514 场周赛，第 4 题。
- 题号：4017。
- 官方中文标题：数组中的峰值 II。
- 官方难度：困难；官方比赛分值：6 分。
- ZeroTracer 社区估算竞赛分：2515.773375505，抓取于 2026-08-17；这不是力扣官方难度。
- 函数签名：`vector<long long> countOfPeaks(vector<int>& nums, vector<vector<int>>& queries)`。
- 题意：长度至少为 3 的子数组，只要存在一个严格大于左右相邻元素的内部位置，就叫峰值
  子数组。查询一要求统计完全位于 `[left,right]` 内的峰值子数组数；查询二把一个数组元素
  改成新值，并影响之后的所有查询。

### 全部官方样例

样例 1：

```text
输入：nums = [1,3,2,4], queries = [[1,0,3],[2,1,1],[1,0,3]]
输出：[2,0]
解释：首次查询中 [1,3,2] 与 [1,3,2,4] 都以内点 1 为峰；更新后数组为
[1,1,2,4]，不再有峰值子数组。
```

样例 2：

```text
输入：nums = [9,8,9,8], queries = [[1,1,3],[2,2,1],[1,0,2]]
输出：[1,0]
解释：首次只有 [8,9,8]；更新后数组为 [9,8,1,8]，区间 [0,2] 中没有内部峰。
```

样例 3：

```text
输入：nums = [3,6,2,7,1], queries = [[1,1,3],[2,3,0],[1,0,4]]
输出：[0,3]
解释：首次的 [6,2,7] 不是峰值子数组；更新后数组为 [3,6,2,0,1]，包含峰 6
的 [3,6,2]、[3,6,2,0]、[3,6,2,0,1] 共三个。
```

### 全部官方约束

- `3 <= n == nums.length <= 100000`。
- `0 <= nums[i] <= 100000`。
- `1 <= queries.length <= 100000`。
- 每个查询是 `[1,left,right]` 或 `[2,index,value]`。
- 类型一满足 `0 <= left < right <= n - 1`。
- 类型二满足 `0 <= index <= n - 1`、`0 <= value <= 100000`。

## 约束推导与计数模型

一次点更新只会改变 `index - 1`、`index`、`index + 1` 三个位置是否为峰，因此峰位置集合
可以动态维护。真正困难的是：一次区间查询问的是“含至少一个峰的子数组数量”，而不是峰的
个数；同一子数组若含多个峰只能计算一次。

把每个合法子数组唯一归给它的第一个内部峰。设查询区间为 `[l,r]`，某个峰为 $p$，全局
前一个峰为 $q$。要让 $p$ 成为子数组的第一个内部峰，左端可以取
$\max(l,q),\ldots,p-1$，右端可以取 $p+1,\ldots,r$，贡献为

$$
\bigl(p-\max(l,q)\bigr)(r-p).
$$

令 $d_p=p-q$。除查询中的第一个峰外，均有 $q>l$，贡献就是 $d_p(r-p)$。因此维护
$d_p$ 与 $d_pp$ 两个前缀和后，一次查询只需一次区间求和，再修正第一个峰：

$$
\sum_{l<p<r}d_p(r-p)-(l-q_0)(r-p_0).
$$

答案最大为 $n(n-1)/2$，必须使用 `long long`。集合负责找前驱、后继，两个树状数组负责
区间和，所有查询与修改均为 $O(\log n)$。

## 样例手推与边界

样例 1 首次查询只有峰 $p=1$，其前驱用哨兵 $q=0$，$d_p=1$。基础和为
$1\times(3-1)=2$，修正项 $(0-0)\times2=0$，答案为 2。更新 `nums[1]` 后，候选位置
0、1、2 中只有 1 可能原先为峰；删除它后集合为空，第二次查询返回 0。

- 区间长度小于 3，或 `(l,r)` 中没有峰：答案为 0。
- 峰恰在 `l` 或 `r`：它是子数组端点，不能作为内部峰，查询时必须排除。
- 连续两个位置不可能同时为严格峰，但算法不依赖这一事实。
- 更新端点时，只检查仍处于 `[1,n-2]` 的候选位置。
- 前驱峰可以在查询左侧；第一个峰的修正项正是避免把越过 `l` 的左端算进去。

## 解法一：枚举子数组与内部位置

枚举查询区间内所有左右端，再扫描内部是否存在峰。它按定义覆盖所有候选，可作为小规模
oracle，但一次查询最坏 $O(n^3)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<long long> countOfPeaks(vector<int>& nums,
                                  vector<vector<int>>& queries) {
    vector<long long> answer;
    for (const vector<int>& query : queries) {
      if (query[0] == 2) {
        nums[query[1]] = query[2];
        continue;
      }
      int left = query[1];
      int right = query[2];
      long long count = 0;
      for (int begin = left; begin <= right; ++begin) {
        for (int end = begin + 2; end <= right; ++end) {
          bool found = false;
          for (int i = begin + 1; i < end; ++i) {
            if (nums[i] > nums[i - 1] && nums[i] > nums[i + 1]) found = true;
          }
          count += found;
        }
      }
      answer.push_back(count);
    }
    return answer;
  }
};
```

额外空间 $O(1)$；瓶颈是每个子数组反复扫描同一批峰，并且每次更新后重新发现它们。

## 从暴力到可维护贡献

先把每个峰写成布尔标记，便可在 $O(1)$ 判断某个位置。再给峰做前缀和，一次静态查询可
在 $O(n^2)$ 枚举子数组并 $O(1)$ 判断是否含峰，但点更新会让普通前缀和整体失效。

进一步把子数组按“第一个内部峰”分组。对固定峰 $p$，所有可选端点形成两个连续区间，
贡献能够相乘；而相邻峰之间的距离 $d_p$ 只会在插入或删除一个峰时改变该峰及其后继。
这恰好适合有序集合加树状数组：集合维护局部邻接关系，树状数组聚合所有峰的线性贡献。

## 最佳实用解：峰集合加两棵树状数组

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
  vector<long long> tree;
public:
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index, long long delta) {
    for (++index; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  long long prefix(int index) const {
    long long result = 0;
    for (++index; index > 0; index -= index & -index) result += tree[index];
    return result;
  }
  long long range(int left, int right) const {
    if (left > right) return 0;
    return prefix(right) - (left == 0 ? 0 : prefix(left - 1));
  }
};
class Solution {
  vector<int>* values = nullptr;
  set<int> peaks{0};
  Fenwick distance;
  Fenwick weighted;
  bool isPeak(int index) const {
    int n = values->size();
    return index > 0 && index + 1 < n &&
        (*values)[index] > (*values)[index - 1] &&
        (*values)[index] > (*values)[index + 1];
  }
  void change(int index, long long oldDistance, long long newDistance) {
    long long delta = newDistance - oldDistance;
    distance.add(index, delta);
    weighted.add(index, delta * index);
  }
  void insertPeak(int index) {
    auto next = peaks.lower_bound(index);
    int previous = *prev(next);
    if (next != peaks.end()) {
      change(*next, *next - previous, *next - index);
    }
    change(index, 0, index - previous);
    peaks.insert(index);
  }
  void erasePeak(int index) {
    auto current = peaks.find(index);
    if (current == peaks.end()) return;
    int previous = *prev(current);
    auto next = std::next(current);
    change(index, index - previous, 0);
    if (next != peaks.end()) {
      change(*next, *next - index, *next - previous);
    }
    peaks.erase(current);
  }
public:
  explicit Solution() : distance(100005), weighted(100005) {}
  vector<long long> countOfPeaks(vector<int>& nums,
                                  vector<vector<int>>& queries) {
    values = &nums;
    for (int i = 1; i + 1 < static_cast<int>(nums.size()); ++i) {
      if (isPeak(i)) insertPeak(i);
    }
    vector<long long> answer;
    for (const vector<int>& query : queries) {
      if (query[0] == 2) {
        int index = query[1];
        for (int i = index - 1; i <= index + 1; ++i) erasePeak(i);
        nums[index] = query[2];
        for (int i = index - 1; i <= index + 1; ++i) {
          if (isPeak(i)) insertPeak(i);
        }
        continue;
      }
      int left = query[1];
      int right = query[2];
      auto first = peaks.upper_bound(left);
      if (first == peaks.end() || *first >= right) {
        answer.push_back(0);
        continue;
      }
      int firstPeak = *first;
      int previous = *prev(first);
      long long sumDistance = distance.range(left + 1, right - 1);
      long long sumWeighted = weighted.range(left + 1, right - 1);
      long long total = 1LL * right * sumDistance - sumWeighted;
      total -= 1LL * (left - previous) * (right - firstPeak);
      answer.push_back(total);
    }
    return answer;
  }
};
```

总初始化 $O(n\log n)$，每次查询和更新 $O(\log n)$，额外空间 $O(n)$。若把初始化改成
一次扫描直接填入已排序峰，也可做到 $O(n)$，但不影响总复杂度。优先记住“按第一个峰唯一
归属 + 维护相邻峰距离”这一模型；只维护峰个数无法回答本题。

## 正确性证明

**引理 1：每个峰值子数组恰好归属于一个峰。**

任何峰值子数组至少含一个内部峰，从左到右的第一个内部峰唯一；反之，只要选定端点使某峰
成为第一个内部峰，所得子数组必然是峰值子数组。因此归属既无遗漏也无重复。

**引理 2：峰 $p$ 在查询 `[l,r]` 中的贡献是
$\bigl(p-\max(l,q)\bigr)(r-p)$。**

右端必须从 `p + 1` 到 `r`，共有 $r-p$ 种。左端既要小于 $p$，又不能小于前一峰 $q$，
否则 $q$ 也成为内部峰并抢走“第一个峰”的归属；故左端从 $\max(l,q)$ 到 $p-1$，共有
$p-\max(l,q)$ 种。两端独立，相乘即得贡献。

**引理 3：公式恰好求出所有贡献。**

对查询中的非首峰，前一峰也严格位于查询内部，所以 $\max(l,q)=q$，贡献为
$d_p(r-p)$。首峰的前驱满足 $q\le l$，基础和把左端数误算成 $p-q$，减去
$(l-q)(r-p)$ 后正好成为 $p-l$。两棵树状数组分别给出 $\sum d_p$ 与 $\sum d_pp$，故
$r\sum d_p-\sum d_pp$ 等于全部基础贡献。

**引理 4：点更新后的数据结构仍表示真实峰集合。**

峰判定只依赖自身及相邻两值，修改一个元素只可能改变三个候选。插入或删除峰时，只有它
自己的前驱距离和其后继的前驱距离变化；代码恰好同步这两项，其他项不变。

由四个引理，每次查询都不重不漏地统计当前数组中所有合法峰值子数组。

## 方案比较与易错点

- 单棵树状数组维护“是不是峰”只能数峰，不能数包含峰的子数组。
- 必须按第一个峰归属；逐峰直接加 `(p-l)*(r-p)` 会重复计算含多个峰的子数组。
- 查询只纳入 `(l,r)` 的峰，端点峰不算内部峰。
- 首峰需要单独修正；其全局前驱可能位于查询左侧。
- 更新一个值要先删除三个旧峰，再改值、插入三个新峰，不能边检查边修改导致邻接关系混乱。
- 插入或删除时别忘了同步后继峰的 $d$。
- 类成员在单次力扣调用内初始化；答案和树状数组都用 `long long`。

## 验证说明

三组官方样例均通过。对 1600 组 $3\le n\le10$ 的随机数组与随机查询流，用三重枚举版本
作为 oracle，与最优实现逐次比较；覆盖无峰、单峰、多峰、相邻更新、端点更新和完整区间。
全部发布代码均以 C++23 编译。

## 变种一：没有更新，回答大量区间询问

静态数组中峰序列不变。预先保存每个峰与前峰距离的前缀和、加权前缀和；查询时二分得到
`(l,r)` 内的峰范围，并使用相同首峰修正式。预处理 $O(n)$，每次查询 $O(\log n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queryCount;
  cin >> n >> queryCount;
  vector<int> nums(n);
  for (int& value : nums) cin >> value;
  vector<int> peak{0};
  for (int i = 1; i + 1 < n; ++i) {
    if (nums[i] > nums[i - 1] && nums[i] > nums[i + 1]) peak.push_back(i);
  }
  int m = peak.size();
  vector<long long> prefixDistance(m), prefixWeighted(m);
  for (int i = 1; i < m; ++i) {
    long long gap = peak[i] - peak[i - 1];
    prefixDistance[i] = prefixDistance[i - 1] + gap;
    prefixWeighted[i] = prefixWeighted[i - 1] + gap * peak[i];
  }
  while (queryCount--) {
    int left, right;
    cin >> left >> right;
    int first = upper_bound(peak.begin(), peak.end(), left) - peak.begin();
    int after = lower_bound(peak.begin(), peak.end(), right) - peak.begin();
    if (first == after) {
      cout << 0 << '\n';
      continue;
    }
    long long sumDistance = prefixDistance[after - 1] -
        (first == 0 ? 0 : prefixDistance[first - 1]);
    long long sumWeighted = prefixWeighted[after - 1] -
        (first == 0 ? 0 : prefixWeighted[first - 1]);
    long long answer = 1LL * right * sumDistance - sumWeighted;
    answer -= 1LL * (left - peak[first - 1]) * (right - peak[first]);
    cout << answer << '\n';
  }
}
```

没有更新后，有序集合与动态树状数组都可退化为数组前缀和；计数公式本身仍成立。

## 变种二：查询区间内有多少个峰

若类型一只问 `(left,right)` 中的峰位置数量，就不需要端点组合与相邻峰距离。以一棵树状
数组维护峰标记，点更新仍只重算三个位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> countOfPeaks(vector<int>& nums, vector<vector<int>>& queries) {
    int n = nums.size();
    vector<int> bit(n + 1), peak(n);
    auto add = [&](int index, int delta) {
      for (++index; index <= n; index += index & -index) bit[index] += delta;
    };
    auto sum = [&](int index) {
      int result = 0;
      for (++index; index > 0; index -= index & -index) result += bit[index];
      return result;
    };
    auto refresh = [&](int index) {
      if (index <= 0 || index + 1 >= n) return;
      int now = nums[index] > nums[index - 1] && nums[index] > nums[index + 1];
      add(index, now - peak[index]);
      peak[index] = now;
    };
    for (int i = 1; i + 1 < n; ++i) refresh(i);
    vector<int> answer;
    for (const vector<int>& query : queries) {
      if (query[0] == 1) {
        int left = query[1] + 1;
        int right = query[2] - 1;
        answer.push_back(left > right ? 0 : sum(right) - sum(left - 1));
      } else {
        nums[query[1]] = query[2];
        for (int i = query[1] - 1; i <= query[1] + 1; ++i) refresh(i);
      }
    }
    return answer;
  }
};
```

时间 $O((n+q)\log n)$、空间 $O(n)$。这对应
[力扣 3187：数组中的峰值](https://leetcode.cn/problems/peaks-in-array/)，它与本题的统计对象不同。

## 变种三：静态数组中，统计至少含 $t$ 个内部峰的全部子数组

给定阈值 $t\ge1$，对每个左端 `left`，二分找到严格位于其右侧的第 $t$ 个峰 $p$。右端
至少为 `p + 1`，所以贡献 $n-p-1$；若不存在则为 0。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, required;
  cin >> n >> required;
  vector<int> nums(n), peak;
  for (int& value : nums) cin >> value;
  for (int i = 1; i + 1 < n; ++i) {
    if (nums[i] > nums[i - 1] && nums[i] > nums[i + 1]) peak.push_back(i);
  }
  long long answer = 0;
  for (int left = 0; left < n; ++left) {
    int first = upper_bound(peak.begin(), peak.end(), left) - peak.begin();
    int target = first + required - 1;
    if (target < static_cast<int>(peak.size())) answer += n - peak[target] - 1;
  }
  cout << answer << '\n';
}
```

时间 $O(n\log n)$、空间 $O(n)$；也可双指针降为 $O(n)$。原来的“第一个峰”唯一归属不再
足够，阈值改由第 $t$ 个峰决定最早右端。

## 变种四：静态数组中，统计恰含一个内部峰的全部子数组

设峰序列中的相邻三项为 `previous, current, next`，并加入边界哨兵 `-1` 与 `n`。为了让
`current` 成为唯一内部峰，左端可取 `previous..current-1`，右端可取
`current+1..next`，贡献为 `(current-previous)*(next-current)`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> nums(n), peak{-1};
  for (int& value : nums) cin >> value;
  for (int i = 1; i + 1 < n; ++i) {
    if (nums[i] > nums[i - 1] && nums[i] > nums[i + 1]) peak.push_back(i);
  }
  peak.push_back(n);
  long long answer = 0;
  for (int i = 1; i + 1 < static_cast<int>(peak.size()); ++i) {
    answer += 1LL * (peak[i] - peak[i - 1]) * (peak[i + 1] - peak[i]);
  }
  cout << answer << '\n';
}
```

时间 $O(n)$、空间 $O(n)$。若要求“至少一个峰”，多个峰只归给第一个；若要求“恰好一个
峰”，左右两个相邻峰共同限定端点范围。

## Reference

- [力扣 4017 官方题面](https://leetcode.cn/problems/peaks-in-array-ii/)
- [第 514 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-514/)
- [ZeroTracer 社区估算数据](https://zerotrac.github.io/leetcode_problem_rating/)
- [力扣 3187 官方题面](https://leetcode.cn/problems/peaks-in-array/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/peaks-in-array-ii/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-137-lc516/">← [力扣 Top 137] LC 516 最长回文子序列 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2256-f/">[codeforces] CF Round 1116 Div.1 D / Div.2 F How Long Until Nothing Remains? →</a>
</nav>
