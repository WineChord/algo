---
title: "[力扣 Top 19] LC 72 编辑距离 中等"
---

# [力扣 Top 19] LC 72 编辑距离 中等

<p class="daily-archive-kicker">2026-07-27 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-27 题目列表</a> · <a href="../../../dp/sequence-dp/">进入知识专题</a></p>

## 官方原始信息

- 题号：72
- 官方中文标题：编辑距离
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/edit-distance/)
- slug：`edit-distance`
- 函数签名：`int minDistance(string word1, string word2)`
- 官方竞赛分：未标注。官方题面与本轮核对的官方 GraphQL 元数据均未提供竞赛归属或分值，不作推断。
- ZeroTracer 社区估算竞赛分：未收录。本轮于 2026-07-27 按题号与 slug 精确检索其公开 `data.json`，无匹配记录。

### 原始题意

把字符串 `word1` 转换为 `word2`，每次可插入一个字符、删除一个字符或把一个字符替换成另一个字符，三种操作代价都为 1。求最少操作数。

### 全部官方样例

1. `word1 = "horse", word2 = "ros"`，输出 `3`。一种最优过程是 `horse -> rorse`（替换 `h`）、`rorse -> rose`（删除第二个 `r`）、`rose -> ros`（删除 `e`）。
2. `word1 = "intention", word2 = "execution"`，输出 `5`。官方给出的过程为依次删除 `t`，把 `i` 替换为 `e`，把 `n` 替换为 `x`，把另一个 `n` 替换为 `c`，再插入 `u`。

### 全部官方约束

- $0\le |word1|,|word2|\le500$
- 两个字符串都只包含小写英文字母。

## 约束推导与最优结论

一次操作只影响当前前缀末端的匹配关系。令 $dp[i][j]$ 表示把 `word1` 前 $i$ 个字符变成 `word2` 前 $j$ 个字符的最少代价：

$$
dp[i][j]=
\begin{cases}
dp[i-1][j-1],&word1[i-1]=word2[j-1],\\
1+\min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]),&\text{otherwise}.
\end{cases}
$$

三项分别对应删除、插入、替换。边界为 $dp[i][0]=i,dp[0][j]=j$。

$500^2=250000$ 个状态完全可行，二维 DP 时间、空间均为 $O(mn)$。若只求距离，第 `i` 行只依赖上一行与本行左侧，可压缩到 $O(\min(m,n))$ 空间；这是最佳实用解。答案最多 $\max(m,n)\le500$，`int` 足够。

## 样例手推与边界

以 `"horse" -> "ros"` 为例，`dp[5][3]=3`。最后字符 `e` 与 `s` 不同，三个候选分别是：

- 删除 `e`：`dp[4][3]+1=3`；
- 插入目标末字符：`dp[5][2]+1`；
- 把 `e` 替换为 `s`：`dp[4][2]+1`。

最优路径可选择删除。继续回溯可得到官方展示的三步过程。

关键边界：

- 两个字符串都为空，答案 0；
- 一个为空，答案是另一个长度；
- 完全相同；
- 长度相同但字符全不同；
- 重复字符导致多条同代价对齐路径；
- 操作顺序并不唯一，距离只要求最小值；
- 滚动数组交换字符串以让列数更小，不改变编辑距离的对称性。

## 解法一：枚举最后一步的朴素递归

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int solve(const string& first, const string& second, int i, int j) {
    if (i == (int)first.size()) return second.size() - j;
    if (j == (int)second.size()) return first.size() - i;
    if (first[i] == second[j]) return solve(first, second, i + 1, j + 1);
    int erase = solve(first, second, i + 1, j);
    int insert = solve(first, second, i, j + 1);
    int replace = solve(first, second, i + 1, j + 1);
    return 1 + min({erase, insert, replace});
  }
public:
  int minDistance(string word1, string word2) {
    return solve(word1, word2, 0, 0);
  }
};
```

最坏时间指数级，可粗略上界为 $O(3^{m+n})$；递归栈 $O(m+n)$。瓶颈是同一后缀对 `(i,j)` 被不同操作序列反复计算。

## 解法二：记忆化搜索

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> memo;
  int solve(const string& first, const string& second, int i, int j) {
    if (i == (int)first.size()) return second.size() - j;
    if (j == (int)second.size()) return first.size() - i;
    int& answer = memo[i][j];
    if (answer != -1) return answer;
    if (first[i] == second[j]) return answer = solve(first, second, i + 1, j + 1);
    int erase = solve(first, second, i + 1, j);
    int insert = solve(first, second, i, j + 1);
    int replace = solve(first, second, i + 1, j + 1);
    return answer = 1 + min({erase, insert, replace});
  }
public:
  int minDistance(string word1, string word2) {
    memo.assign(word1.size(), vector<int>(word2.size(), -1));
    return solve(word1, word2, 0, 0);
  }
};
```

时间 $O(mn)$，记忆表 $O(mn)$，递归栈 $O(m+n)$。

## 解法三：二维自底向上 DP

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minDistance(string word1, string word2) {
    int m = word1.size();
    int n = word2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    iota(dp[0].begin(), dp[0].end(), 0);
    for (int i = 1; i <= m; ++i) dp[i][0] = i;
    for (int i = 1; i <= m; ++i) {
      for (int j = 1; j <= n; ++j) {
        if (word1[i - 1] == word2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
        }
      }
    }
    return dp[m][n];
  }
};
```

时间 $O(mn)$，空间 $O(mn)$。它消除了递归开销，并能直接回溯具体方案。

## 解法四：一维滚动 DP（最佳实用解）

让较短字符串作为列，只保存上一行。更新 `dp[j]` 前，它还是上一行的 $dp[i-1][j]$；`dp[j-1]` 已是本行的 $dp[i][j-1]$；变量 `diagonal` 保存被覆盖前的 $dp[i-1][j-1]$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minDistance(string word1, string word2) {
    if (word1.size() < word2.size()) swap(word1, word2);
    int rows = word1.size();
    int columns = word2.size();
    vector<int> dp(columns + 1);
    iota(dp.begin(), dp.end(), 0);
    for (int i = 1; i <= rows; ++i) {
      int diagonal = dp[0];
      dp[0] = i;
      for (int j = 1; j <= columns; ++j) {
        int above = dp[j];
        if (word1[i - 1] == word2[j - 1]) {
          dp[j] = diagonal;
        } else {
          dp[j] = 1 + min({above, dp[j - 1], diagonal});
        }
        diagonal = above;
      }
    }
    return dp[columns];
  }
};
```

时间 $O(mn)$，空间 $O(\min(m,n))$。

### 正确性证明

对二维状态按行归纳。边界 `dp[j]=j` 正确表示从空串插入 `j` 个字符。处理第 `i` 行时：

- 若末字符相等，不需要新操作，最优值等于去掉两个相同末字符后的对角状态；
- 若不同，任意最优编辑序列的最后一步必是删除源末字符、插入目标末字符或替换源末字符之一；去掉最后一步分别得到三个子状态，因此取三者最小值再加 1，既覆盖所有可能又不会低估。

滚动实现中的 `above`、`dp[j-1]`、`diagonal` 与二维递推三项逐一对应，所以得到同一状态值。最终 `dp[columns]` 即完整字符串编辑距离。

## 同阶方案比较与推荐

- 记忆化搜索与二维 DP 都是 $O(mn)$；前者贴近递归定义，后者无栈风险且更适合回溯。
- 一维 DP 把空间降为 $O(\min(m,n))$，仅求距离时优先记忆。
- 若要恢复具体操作、统计路径或使用依赖更多邻居的变种，保留二维表通常更清楚。
- 当允许的最大距离 `k` 很小，可只计算主对角线附近宽度 $2k+1$ 的带状区域，把时间降到 $O(k\min(m,n))$；见后续变种。

## 常见错误

- 混淆“插入到源串”与下标移动：插入对应 `(i,j-1)`，源前缀长度不变。
- 空串边界未初始化。
- 字符相等时仍强制加 1。
- 一维压缩时先覆盖对角值，导致替换转移读到本行数据。
- 只按长度差估计答案；长度相同仍可能需要替换。
- 为恢复路径却只保留一维数组，丢失回溯信息。
- 把 Levenshtein 距离与允许相邻交换的 Damerau 距离混为一谈。

## Follow-up 1：恢复一条最优编辑脚本

保留二维表后从 `(m,n)` 回溯。相等字符沿对角线跳过；否则选择一个满足最优等式的操作。返回的每步记录操作类型及其发生时对应的源/目标前缀坐标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct EditStep {
  string operation;
  int sourcePrefix;
  int targetPrefix;
  char from;
  char to;
};
class Solution {
public:
  vector<EditStep> editScript(const string& first, const string& second) {
    int m = first.size();
    int n = second.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    iota(dp[0].begin(), dp[0].end(), 0);
    for (int i = 1; i <= m; ++i) dp[i][0] = i;
    for (int i = 1; i <= m; ++i) {
      for (int j = 1; j <= n; ++j) {
        int cost = first[i - 1] == second[j - 1] ? 0 : 1;
        dp[i][j] = min({dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost});
      }
    }
    vector<EditStep> reversed;
    int i = m, j = n;
    while (i > 0 || j > 0) {
      if (i > 0 && j > 0 && first[i - 1] == second[j - 1] && dp[i][j] == dp[i - 1][j - 1]) {
        --i;
        --j;
      } else if (i > 0 && j > 0 && dp[i][j] == dp[i - 1][j - 1] + 1) {
        reversed.push_back({"replace", i, j, first[i - 1], second[j - 1]});
        --i;
        --j;
      } else if (i > 0 && dp[i][j] == dp[i - 1][j] + 1) {
        reversed.push_back({"delete", i, j, first[i - 1], '\0'});
        --i;
      } else {
        reversed.push_back({"insert", i, j, '\0', second[j - 1]});
        --j;
      }
    }
    reverse(reversed.begin(), reversed.end());
    return reversed;
  }
};
```

时间与空间均为 $O(mn)$，返回脚本长度不超过 $m+n$。存在多条最优脚本时，本实现按“替换、删除、插入”的回溯优先级选择其中一条。

## Follow-up 2：三种操作有不同代价

把三个转移的 `+1` 替换为各自非负代价。字符相等仍可零代价匹配；若替换代价高于删除加插入，DP 会自动选择后者。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long weightedDistance(const string& first, const string& second, long long insertCost, long long deleteCost, long long replaceCost) {
    int m = first.size();
    int n = second.size();
    vector<vector<long long>> dp(m + 1, vector<long long>(n + 1));
    for (int i = 1; i <= m; ++i) dp[i][0] = dp[i - 1][0] + deleteCost;
    for (int j = 1; j <= n; ++j) dp[0][j] = dp[0][j - 1] + insertCost;
    for (int i = 1; i <= m; ++i) {
      for (int j = 1; j <= n; ++j) {
        long long diagonal = dp[i - 1][j - 1];
        if (first[i - 1] != second[j - 1]) diagonal += replaceCost;
        dp[i][j] = min({dp[i - 1][j] + deleteCost, dp[i][j - 1] + insertCost, diagonal});
      }
    }
    return dp[m][n];
  }
};
```

时间、空间均为 $O(mn)$。使用 `long long` 防止长度或代价扩大后溢出。

## Follow-up 3：允许交换相邻字符

增加一次代价为 1 的相邻转置。当 `first[i-2]==second[j-1]` 且 `first[i-1]==second[j-2]` 时，可从 `dp[i-2][j-2]+1` 转移。这是 optimal string alignment 版本的 Damerau–Levenshtein 距离。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int distanceWithAdjacentSwap(const string& first, const string& second) {
    int m = first.size();
    int n = second.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    iota(dp[0].begin(), dp[0].end(), 0);
    for (int i = 1; i <= m; ++i) dp[i][0] = i;
    for (int i = 1; i <= m; ++i) {
      for (int j = 1; j <= n; ++j) {
        int cost = first[i - 1] == second[j - 1] ? 0 : 1;
        dp[i][j] = min({dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost});
        if (i >= 2 && j >= 2 && first[i - 2] == second[j - 1] && first[i - 1] == second[j - 2]) {
          dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1);
        }
      }
    }
    return dp[m][n];
  }
};
```

时间、空间均为 $O(mn)$。它与不限制重复转置交互的完整 Damerau–Levenshtein 定义并不完全等价，接口应明确采用哪种模型。

## Follow-up 4：只关心距离是否不超过 `k`

若编辑距离不超过 `k`，任意可行路径都满足 $|i-j|\le k$，因为长度差至少需要相应次数的插入或删除。因此只计算主对角线附近的带状状态；返回 `k+1` 表示真实距离超过阈值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int boundedDistance(const string& first, const string& second, int k) {
    int m = first.size();
    int n = second.size();
    if (abs(m - n) > k) return k + 1;
    const int infinity = k + 1;
    vector<int> previous(n + 1, infinity);
    vector<int> current(n + 1, infinity);
    for (int j = 0; j <= min(n, k); ++j) previous[j] = j;
    for (int i = 1; i <= m; ++i) {
      fill(current.begin(), current.end(), infinity);
      if (i <= k) current[0] = i;
      int left = max(1, i - k);
      int right = min(n, i + k);
      for (int j = left; j <= right; ++j) {
        int cost = first[i - 1] == second[j - 1] ? 0 : 1;
        current[j] = min({previous[j] + 1, current[j - 1] + 1, previous[j - 1] + cost, infinity});
      }
      swap(previous, current);
    }
    return min(previous[n], infinity);
  }
};
```

时间 $O(km)$，空间 $O(n)$；还可只保存宽度 $O(k)$ 的带状数组。`k` 远小于字符串长度时收益显著。

## Follow-up 5：统计最优编辑对齐的数量

每个状态同时保存最短距离与达到该距离的 DP 路径数。插入、删除、匹配/替换三个前驱都参与比较；相同最优代价的路径数相加并取模。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<int, int> countOptimalAlignments(const string& first, const string& second, int modulus) {
    int m = first.size();
    int n = second.size();
    const int infinity = m + n + 1;
    vector<vector<int>> distance(m + 1, vector<int>(n + 1, infinity));
    vector<vector<int>> ways(m + 1, vector<int>(n + 1));
    distance[0][0] = 0;
    ways[0][0] = 1;
    for (int i = 0; i <= m; ++i) {
      for (int j = 0; j <= n; ++j) {
        if (i == 0 && j == 0) continue;
        auto consider = [&](int candidate, int count) {
          if (candidate < distance[i][j]) {
            distance[i][j] = candidate;
            ways[i][j] = count;
          } else if (candidate == distance[i][j]) {
            ways[i][j] = (ways[i][j] + count) % modulus;
          }
        };
        if (i > 0) consider(distance[i - 1][j] + 1, ways[i - 1][j]);
        if (j > 0) consider(distance[i][j - 1] + 1, ways[i][j - 1]);
        if (i > 0 && j > 0) {
          int cost = first[i - 1] == second[j - 1] ? 0 : 1;
          consider(distance[i - 1][j - 1] + cost, ways[i - 1][j - 1]);
        }
      }
    }
    return {distance[m][n], ways[m][n]};
  }
};
```

时间、空间均为 $O(mn)$。这里统计的是不同 DP 对齐路径；若产品定义要把产生同一最终字符序列的操作交换视为同一种方案，还需要额外等价关系，不能直接套用此计数。

## Follow-up 6：禁止替换，只允许插入和删除

保留最长公共子序列的字符不动，删除源串其余 $m-L$ 个字符，再插入目标串其余 $n-L$ 个字符，最少操作数为 $m+n-2L$。对应 [LC 583 两个字符串的删除操作](https://leetcode.cn/problems/delete-operation-for-two-strings/) 的核心结构。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int insertDeleteDistance(const string& first, const string& second) {
    vector<int> dp(second.size() + 1);
    for (int i = 1; i <= (int)first.size(); ++i) {
      int diagonal = 0;
      for (int j = 1; j <= (int)second.size(); ++j) {
        int above = dp[j];
        if (first[i - 1] == second[j - 1]) dp[j] = diagonal + 1;
        else dp[j] = max(dp[j], dp[j - 1]);
        diagonal = above;
      }
    }
    int lcs = dp.back();
    return first.size() + second.size() - 2 * lcs;
  }
};
```

时间 $O(mn)$，空间 $O(n)$。

## 验证说明

- 对短随机字符串，用朴素递归作 oracle，比较记忆化、二维 DP 与一维 DP。
- 固定覆盖两个官方样例、双空串、单边空串、相同串、全不同串和重复字符。
- 阈值算法与完整距离逐一比较：真实距离不超过 `k` 时必须相等，否则必须返回 `k+1`。
- 本文每个 C++ 代码块均按 C++23 单独做语法编译；随机种子、用例规模与真实结果记录在同目录机器报告中。

## Reference

- [官方题目](https://leetcode.cn/problems/edit-distance/)
- [对应知识专题](../../dp/sequence-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-18-lc88/">← [力扣 Top 18] LC 88 合并两个有序数组 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-20-lc54/">[力扣 Top 20] LC 54 螺旋矩阵 中等 →</a>
</nav>
