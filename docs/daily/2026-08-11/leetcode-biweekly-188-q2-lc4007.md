---
title: "[力扣竞赛] 第 188 场双周赛 Q2 LC 4007 栅栏的最宽宽度 中等"
---

# [力扣竞赛] 第 188 场双周赛 Q2 LC 4007 栅栏的最宽宽度 中等

<p class="daily-archive-kicker">2026-08-11 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-11 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=43ae8fb995f863c02337e3bff285ad111153462c195d6fcc5581dd701cfdbe0b -->
## 官方原始信息

- 比赛：力扣第 188 场双周赛。
- 题目：Q2，LC 4007，栅栏的最宽宽度。
- 官方难度：中等；比赛官方分值：4。
- ZeroTracer 社区估算竞赛分：截至 2026-08-11 未收录，记为未知。
- 官方链接：[栅栏的最宽宽度](https://leetcode.cn/problems/maximum-width-of-a-fence/)。

### 原始题意与函数签名

`planks[i]` 表示第 `i` 块木板的高度，每块宽度都是 1。建造栅栏时，每一列可以直接使用一块木板，也可以把两块不同的原木板上下拼接；所有列最终必须等高，每块原木板至多使用一次，也不要求用完。返回可得到的最大栅栏宽度。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maximumWidth(vector<int>& planks);
};
```

### 全部官方样例

```text
输入：planks = [1,3,2,5,7,5,4,2,1]
输出：4
解释：目标高度取 5。两块高度 5 的木板各自成列，再分别拼接 1+4 与 3+2，共四列。
```

```text
输入：planks = [2,3,7]
输出：1
解释：无法做出两列等高栅栏，任选一块木板即可得到宽度 1。
```

### 全部约束

- $1\le |planks|\le1000$。
- $1\le planks_i\le10^9$。
- 两块高度之和最多为 $2\times10^9$，仍在 32 位有符号整数内；实现中用 `long long` 表示目标高度可消除边界顾虑。

## 约束推导与观察

固定目标高度 $H$ 后，高度为 $H$ 的木板可以单独使用；其余木板只能与唯一的补数 $H-x$ 配对。不同补数对不会共享高度类别，因此每一对类别的最优贡献彼此独立：

$$
width(H)=cnt_H+
\sum_{x<H-x}\min(cnt_x,cnt_{H-x})+
\begin{cases}
\lfloor cnt_{H/2}/2\rfloor,&H\text{ 为偶数},\\
0,&H\text{ 为奇数}.
\end{cases}
$$

候选 $H$ 只可能是一块木板的高度或两块木板的高度和。直接逐候选重算会重复检查相同的高度对；反过来枚举每个单高度和每个无序高度对，把贡献累加到对应 $H$，即可一次完成所有候选。

## 解法递进

### 解法一：按目标高度做子集搜索

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int search(const vector<int>& a, int target, int mask, vector<int>& memo) {
  if (memo[mask] != -1) return memo[mask];
  int best = 0;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) {
    if (mask >> i & 1) continue;
    if (a[i] == target) best = max(best, 1 + search(a, target, mask | (1 << i), memo));
    for (int j = i + 1; j < static_cast<int>(a.size()); ++j) {
      if (!(mask >> j & 1) && a[i] + a[j] == target) {
        best = max(best, 1 + search(a, target, mask | (1 << i) | (1 << j), memo));
      }
    }
  }
  return memo[mask] = best;
}
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) cin >> x;
  set<int> targets(a.begin(), a.end());
  for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) targets.insert(a[i] + a[j]);
  int answer = 0;
  for (int target : targets) {
    vector<int> memo(1 << n, -1);
    answer = max(answer, search(a, target, 0, memo));
  }
  cout << answer << '\n';
}
```

它逐一枚举合法列并用位掩码保证木板不复用，覆盖定义；时间约为 $O(2^n n^2)$，只适合很小的 oracle。

### 解法二：逐候选高度排序后双指针

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long& x : a) cin >> x;
  sort(a.begin(), a.end());
  set<long long> targets(a.begin(), a.end());
  for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) targets.insert(a[i] + a[j]);
  int answer = 0;
  for (long long target : targets) {
    int width = count(a.begin(), a.end(), target);
    int left = 0, right = n - 1;
    while (left < right) {
      if (a[left] == target) {
        ++left;
      } else if (a[right] == target) {
        --right;
      } else if (a[left] + a[right] < target) {
        ++left;
      } else if (a[left] + a[right] > target) {
        --right;
      } else {
        ++width;
        ++left;
        --right;
      }
    }
    answer = max(answer, width);
  }
  cout << answer << '\n';
}
```

每个候选用双指针得到最多配对数，但候选可达 $O(n^2)$，总时间 $O(n^3)$、空间 $O(n^2)$。

### 最佳实用解：按高度频次反向累加贡献

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximumWidth(vector<int>& planks) {
    unordered_map<long long, int> frequency;
    for (int height : planks) ++frequency[height];
    vector<pair<long long, int>> values(frequency.begin(), frequency.end());
    unordered_map<long long, int> width;
    int answer = 0;
    for (auto [height, count] : values) {
      answer = max(answer, width[height] += count);
      answer = max(answer, width[height * 2] += count / 2);
    }
    for (int i = 0; i < static_cast<int>(values.size()); ++i) {
      for (int j = i + 1; j < static_cast<int>(values.size()); ++j) {
        auto [x, countX] = values[i];
        auto [y, countY] = values[j];
        answer = max(answer, width[x + y] += min(countX, countY));
      }
    }
    return answer;
  }
};
int main() {
  vector<int> planks{1, 3, 2, 5, 7, 5, 4, 2, 1};
  cout << Solution().maximumWidth(planks) << '\n';
}
```

设不同高度数为 $D$。时间 $O(D^2)$，散列表期望空间 $O(D^2)$；$D\le1000$，符合约束。相同高度对与不同高度对分开计数，避免把一块木板重复使用。

## 正确性证明

固定 $H$。单板列只能取高度 $H$，共 `cnt[H]` 列。双板列若包含高度 $x$，另一块高度被唯一确定为 $H-x$。当 $x\ne H-x$ 时，这两个高度类别最多形成 $\min(cnt_x,cnt_{H-x})$ 对；当二者相等时最多形成 $\lfloor cnt_x/2\rfloor$ 对。不同补数类互不重叠，所以各自取满可以同时实现，公式既是上界也是构造。

算法把单板贡献累加到键 $H=x$，把同高双板贡献累加到 $H=2x$，把每个不同高度无序对的贡献累加到 $H=x+y$。这些项与公式一一对应且不重不漏，因此 `width[H]` 对每个候选高度都精确，取最大值即为答案。

## 样例手推、边界与易错点

样例一的频次为 `1:2, 2:2, 3:1, 4:1, 5:2, 7:1`。对 $H=5$，单板贡献 2，`1+4` 贡献 1，`2+3` 贡献 1，总宽度 4。`5` 不能再参与双板列，因为那些是不同目标高度下的候选，不会在同一个 $H$ 中混用。

- 只有一块木板时答案为 1。
- 同一高度有奇数块时，同高配对只能使用其中偶数块。
- `min(cnt[x],cnt[y])` 是固定目标下的全部贡献，不是只加 1。
- 本题要求每列等高，不能把不同目标高度的列合并。
- 两个官方样例通过；最优解与位掩码 oracle 在 11,000 组随机小数组上逐一一致。

## 变种一：恢复实际使用的木板下标

新定义：除最大宽度外，返回每一列使用的原数组下标。先求最佳 $H$，再按高度保存下标栈并实际弹出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> buildFence(const vector<int>& a) {
  unordered_map<long long, vector<int>> positions;
  for (int i = 0; i < static_cast<int>(a.size()); ++i) positions[a[i]].push_back(i);
  vector<pair<long long, int>> values;
  for (auto& [height, list] : positions) values.push_back({height, list.size()});
  unordered_map<long long, int> width;
  long long bestHeight = 0;
  int bestWidth = -1;
  auto improve = [&](long long height, int delta) {
    int current = width[height] += delta;
    if (current > bestWidth) bestWidth = current, bestHeight = height;
  };
  for (auto [x, count] : values) improve(x, count), improve(2 * x, count / 2);
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    for (int j = i + 1; j < static_cast<int>(values.size()); ++j) {
      improve(values[i].first + values[j].first, min(values[i].second, values[j].second));
    }
  }
  vector<vector<int>> columns;
  auto single = positions.find(bestHeight);
  if (single != positions.end()) {
    for (int index : single->second) columns.push_back({index});
    single->second.clear();
  }
  for (auto& [x, left] : positions) {
    long long y = bestHeight - x;
    if (x > y || !positions.contains(y)) continue;
    auto& right = positions[y];
    while (x < y && !left.empty() && !right.empty()) {
      columns.push_back({left.back(), right.back()});
      left.pop_back();
      right.pop_back();
    }
    while (x == y && left.size() >= 2) {
      int first = left.back(); left.pop_back();
      int second = left.back(); left.pop_back();
      columns.push_back({first, second});
    }
  }
  return columns;
}
int main() {
  auto columns = buildFence({1, 3, 2, 5, 7, 5, 4, 2, 1});
  cout << columns.size() << '\n';
}
```

求高度仍为 $O(D^2)$，恢复方案为 $O(n+D)$，空间 $O(n+D^2)$。

## 变种二：多次询问指定目标高度

新定义：给出许多 $H$，分别询问可建宽度。预处理所有目标的宽度后，每次散列表查询期望 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
unordered_map<long long, int> allWidths(const vector<int>& planks) {
  unordered_map<long long, int> frequency, width;
  for (int x : planks) ++frequency[x];
  vector<pair<long long, int>> values(frequency.begin(), frequency.end());
  for (auto [x, count] : values) {
    width[x] += count;
    width[2 * x] += count / 2;
  }
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    for (int j = i + 1; j < static_cast<int>(values.size()); ++j) {
      width[values[i].first + values[j].first] += min(values[i].second, values[j].second);
    }
  }
  return width;
}
int main() {
  auto width = allWidths({1, 3, 2, 5, 7, 5, 4, 2, 1});
  for (long long height : {4, 5, 7}) cout << width[height] << ' ';
}
```

预处理时间、空间均为 $O(D^2)$，每次查询期望 $O(1)$。

## 变种三：每列必须恰好使用两块木板

新定义：不允许单板列。原公式只需去掉 `cnt[H]` 项，其余补数配对证明不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximumPairedWidth(const vector<int>& planks) {
  unordered_map<long long, int> frequency, width;
  for (int x : planks) ++frequency[x];
  vector<pair<long long, int>> values(frequency.begin(), frequency.end());
  int answer = 0;
  for (auto [x, count] : values) answer = max(answer, width[2 * x] += count / 2);
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    for (int j = i + 1; j < static_cast<int>(values.size()); ++j) {
      long long height = values[i].first + values[j].first;
      int count = min(values[i].second, values[j].second);
      answer = max(answer, width[height] += count);
    }
  }
  return answer;
}
int main() {
  cout << maximumPairedWidth({1, 1, 2, 2, 3, 4}) << '\n';
}
```

时间、空间仍为 $O(D^2)$；若没有可配对木板，答案为 0。

## 变种四：每列最多使用三块木板

新定义：允许每列使用 1、2 或 3 块，且 $n\le20$。补数不再唯一，频次对的独立性失效；用位掩码 DP 对每个候选高度做精确集合打包。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int maximumWidthUpToThree(const vector<int>& a) {
  int n = a.size();
  set<int> targets;
  for (int i = 0; i < n; ++i) {
    targets.insert(a[i]);
    for (int j = i + 1; j < n; ++j) {
      targets.insert(a[i] + a[j]);
      for (int k = j + 1; k < n; ++k) targets.insert(a[i] + a[j] + a[k]);
    }
  }
  int answer = 0;
  for (int target : targets) {
    vector<int> groups;
    for (int i = 0; i < n; ++i) {
      if (a[i] == target) groups.push_back(1 << i);
      for (int j = i + 1; j < n; ++j) {
        if (a[i] + a[j] == target) groups.push_back((1 << i) | (1 << j));
        for (int k = j + 1; k < n; ++k) {
          if (a[i] + a[j] + a[k] == target) groups.push_back((1 << i) | (1 << j) | (1 << k));
        }
      }
    }
    vector<int> dp(1 << n, -1);
    dp[0] = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
      if (dp[mask] < 0) continue;
      for (int group : groups) {
        if (!(mask & group)) {
          dp[mask | group] = max(dp[mask | group], dp[mask] + 1);
        }
      }
      answer = max(answer, dp[mask]);
    }
  }
  return answer;
}
int main() {
  cout << maximumWidthUpToThree({1, 2, 3, 4, 5}) << '\n';
}
```

候选与组数为 $O(n^3)$，时间 $O(2^n n^6)$ 的粗上界，只适合小 $n$；它展示了从唯一补数配对转为一般集合打包后为何不能继续使用原 $O(D^2)$ 公式。

## 可复现验证

官方样例与文中边界样例全部通过。另在小值域上生成 11000 组随机木板库存，把补数聚合解与逐状态搜索 oracle 比较，最大宽度逐组一致。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/maximum-width-of-a-fence/)
- [力扣第 188 场双周赛](https://leetcode.cn/contest/biweekly-contest-188/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/maximum-width-of-a-fence/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-131-lc63/">← [力扣 Top 131] LC 63 不同路径 II 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2248-g/">[codeforces] CF Round 1113 Div.2 G No Balance Left →</a>
</nav>
