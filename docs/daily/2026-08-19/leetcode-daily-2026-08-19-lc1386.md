---
title: "[力扣每日一题] 2026-08-19｜LC 1386 安排电影院座位"
---

# [力扣每日一题] 2026-08-19｜LC 1386 安排电影院座位

<p class="daily-archive-kicker">2026-08-19 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-19 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=667b96e6e1e56cfc68083a757aaf0acacc8749f7f9cfd3c912ad8ce29b62fdf3 -->
[官方题目：1386. 安排电影院座位](https://leetcode.cn/problems/cinema-seat-allocation/)

## 官方原始信息

- 题号与标题：1386. 安排电影院座位。
- 难度：中等。
- ZeroTracer 社区估算竞赛分：1636.69，抓取于 2026-08-19；这不是力扣官方难度。
- 官方链接：[LeetCode 中国题面](https://leetcode.cn/problems/cinema-seat-allocation/)。
- 工作日期：2026-08-19（Asia/Shanghai）；力扣中国官方“每日一题”接口已将本题标为当天题目。
- 函数签名：`int maxNumberOfFamilies(int n, vector<vector<int>>& reservedSeats)`。

影厅有 $n$ 行，每行恰好 10 个座位，行号为 $1\ldots n$、座位号为 $1\ldots10$。
`reservedSeats[i]=[row_i,seat_i]` 表示一个已预约座位。一个四人小组必须坐在同一行，并且
只能选择座位块 `2,3,4,5`、`4,5,6,7` 或 `6,7,8,9`。块内四座都未预约时才可使用，
而每个座位至多属于一个小组。返回最多能安排的四人小组数。

题面示意图只把上述三种连续座位块可视化，文字已经完整定义判题语义；
[官方页面](https://leetcode.cn/problems/cinema-seat-allocation/)保留原图。

### 全部官方样例

示例 1：

```text
输入：n = 3, reservedSeats = [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]
输出：4
解释：第 1 行只能安排中间块，第 2 行只能安排左块；第 3 行的 1、10 号预约不影响左右
两个块，所以该行能安排两组，总数为 4。
```

示例 2：

```text
输入：n = 2, reservedSeats = [[2,1],[1,8],[2,6]]
输出：2
```

示例 3：

```text
输入：n = 4, reservedSeats = [[4,3],[1,4],[4,6],[1,7]]
输出：4
```

### 全部约束

- $1\le n\le10^9$。
- $1\le\lvert\texttt{reservedSeats}\rvert\le\min(10n,10^4)$。
- `reservedSeats[i] == [row_i, seat_i]`。
- $1\le row_i\le n$。
- $1\le seat_i\le10$。
- 所有预约位置互不相同。

## 约束与观察

$n$ 可达 $10^9$，逐行扫描必然超时；但预约记录最多 $10^4$ 条，真正可能偏离“每行安排
两组”的行非常稀疏。

1 号和 10 号座位不属于任何候选块，可以完全忽略。对其余座位，用一个整数的第 `seat`
位记录是否预约。每个未出现的行贡献 2；每个出现的行只需检查三个固定掩码：

$$
L=\{2,3,4,5\},\qquad M=\{4,5,6,7\},\qquad R=\{6,7,8,9\}.
$$

若 $L,R$ 都空闲，能安排两组；否则，只要 $L,M,R$ 中任一块空闲，就能安排一组；都被
挡住则为零。答案最大为 $2n\le2\times10^9$，仍在有符号 32 位 `int` 范围内，但乘法用
`2LL*n` 计算后再返回更稳妥。

## 样例手推与边界

示例 1 中：

- 第 1 行预约 2、3、8，左右块均受阻，但中间块 4–7 空闲，贡献 1。
- 第 2 行预约 6，左块空闲，贡献 1。
- 第 3 行只预约 1、10，这两个座位不参与任何块，贡献 2。
- 总计 $1+1+2=4$。

边界上，完全没有相关预约的行贡献 2；一个 4 或 7 号预约可能同时阻塞两个候选块；只有
中间块空闲时仍能贡献 1；只有 1、10 号预约时不能误减答案；同一行多条预约必须用按位或
合并，不能覆盖旧掩码。

## 解法一：逐行显式检查

建立所有 $n$ 行的 11 个布尔座位，标记预约后逐行判断左右块能否同时使用，否则检查三块
是否至少一块可用。该解法直接覆盖定义，适合小规模 oracle。

时间复杂度 $O(n+R)$，空间复杂度 $O(n)$，其中 $R$ 是预约数。$n=10^9$ 时无法运行。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxNumberOfFamilies(int n, vector<vector<int>>& reservedSeats) {
    vector<array<bool, 11>> reserved(n + 1);
    for (const auto& seat : reservedSeats) reserved[seat[0]][seat[1]] = true;
    int answer = 0;
    for (int row = 1; row <= n; ++row) {
      bool left = true;
      bool middle = true;
      bool right = true;
      for (int seat = 2; seat <= 5; ++seat) left &= !reserved[row][seat];
      for (int seat = 4; seat <= 7; ++seat) middle &= !reserved[row][seat];
      for (int seat = 6; seat <= 9; ++seat) right &= !reserved[row][seat];
      if (left && right) {
        answer += 2;
      } else if (left || middle || right) {
        ++answer;
      }
    }
    return answer;
  }
};
```

## 从暴力到最优：稀疏记录偏离基线的行

暴力方案在绝大多数无预约行上重复做完全相同的三次块检查。先假设每行都贡献 2，得到
$2n$；哈希表只保存座位 2–9 中至少有一处预约的行。对每个这样的行，先撤销基线的 2，
再按其掩码加回真实贡献。这样消除了对 $n$ 的依赖。

## 最佳实用解：哈希行号加座位位掩码

### 正确性证明

**引理 1**：未出现在哈希表中的行一定能安排两组。

这类行在 2–9 号座位中没有预约，互不相交的左块 2–5 与右块 6–9 都可用，所以贡献 2；
1、10 号座位与任何候选块都无关。

**引理 2**：对任意受影响行，程序计算的贡献是该行最优值。

一行最多安排两组，而唯一一对互不相交的候选块是左块与右块。因此两者都空闲时最优值
恰为 2。若它们不能同时使用，就不可能安排两组；此时三块中任一块空闲当且仅当能安排
一组，否则为 0。程序正好按这三个互斥情形返回。

**定理**：程序返回全影厅的最大安排数。

各行座位互不共享，行间选择完全独立。由引理 1 和引理 2，程序对每行都取到最优贡献，
将这些贡献相加即为全局最优。

### 完整 C++

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxNumberOfFamilies(int n, vector<vector<int>>& reservedSeats) {
    unordered_map<int, int> masks;
    for (const auto& reserved : reservedSeats) {
      int row = reserved[0];
      int seat = reserved[1];
      if (seat >= 2 && seat <= 9) masks[row] |= 1 << seat;
    }
    constexpr int left = (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5);
    constexpr int middle = (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7);
    constexpr int right = (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9);
    long long answer = 2LL * n;
    for (const auto& [row, mask] : masks) {
      static_cast<void>(row);
      answer -= 2;
      if ((mask & left) == 0 && (mask & right) == 0) {
        answer += 2;
      } else if ((mask & left) == 0 || (mask & middle) == 0 ||
                (mask & right) == 0) {
        ++answer;
      }
    }
    return static_cast<int>(answer);
  }
};
```

设 $R=\lvert\texttt{reservedSeats}\rvert$，时间复杂度期望为 $O(R)$，额外空间期望为
$O(\min(R,n))$。若希望确定性上界，可把 `unordered_map` 换成 `map`，得到 $O(R\log R)$。

## 方案比较与推荐

- 逐行布尔数组最贴近题意，也最适合作 oracle，但复杂度依赖巨大 $n$。
- 也可把预约按 `(row, seat)` 排序后分组，时间 $O(R\log R)$、额外空间可降到 $O(R)$；
  最坏复杂度确定，但会改动输入或另存副本。
- 哈希加掩码只访问受影响行，常数小、实现稳定，是面试和竞赛最值得优先记忆的方案。

## 易错点

- 中间块 4–7 只能安排一组，不能和左块或右块同时使用。
- 两组的唯一组合是左块加右块；不能只数三个“空闲块”。
- 1、10 号预约不影响任何四人块，过滤它们可避免创建无意义的受影响行。
- 同一行的多个座位要用 `|=` 合并。
- 不能分配 $O(n)$ 的数组；$n$ 远大于预约数。
- `2*n` 先用 64 位计算，最后由题目上界确认可安全转回 `int`。

## 可复现验证

所有代码按 C++23 编译。最佳解通过三组官方样例；随机生成小规模影厅和互不重复预约，将
稀疏位掩码答案与逐行布尔 oracle 比较。验证中特别覆盖仅预约 1/10、左右同时空闲、只剩
中间块、三个块全阻塞以及 $n=10^9$ 的整数边界。

## 变种一：返回每个受影响行的具体座位块

新定义：除最大组数外，还要列出每个有 2–9 号预约行所采用的块；未受影响行统一说明使用
左右两块，不展开十亿行。原算法仍成立，只需在判断贡献时记录 `[2,5]`、`[4,7]`、
`[6,9]`。时间和空间期望均为 $O(R)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Allocation {
  long long total;
  vector<pair<int, vector<pair<int, int>>>> affectedRows;
};
class Solution {
public:
  Allocation allocate(int n, const vector<vector<int>>& reservedSeats) {
    unordered_map<int, int> masks;
    for (const auto& reserved : reservedSeats) {
      if (reserved[1] >= 2 && reserved[1] <= 9) {
        masks[reserved[0]] |= 1 << reserved[1];
      }
    }
    constexpr int left = 0b0000111100;
    constexpr int middle = 0b0011110000;
    constexpr int right = 0b1111000000;
    Allocation result{2LL * n, {}};
    for (const auto& [row, mask] : masks) {
      vector<pair<int, int>> blocks;
      result.total -= 2;
      if ((mask & left) == 0 && (mask & right) == 0) {
        blocks = {{2, 5}, {6, 9}};
      } else if ((mask & left) == 0) {
        blocks = {{2, 5}};
      } else if ((mask & middle) == 0) {
        blocks = {{4, 7}};
      } else if ((mask & right) == 0) {
        blocks = {{6, 9}};
      }
      result.total += blocks.size();
      result.affectedRows.push_back({row, blocks});
    }
    sort(result.affectedRows.begin(), result.affectedRows.end());
    return result;
  }
};
```

## 变种二：每行宽度、组大小与允许起点可变

新定义：行宽 $W\le20$、每组占连续 $g$ 个座位，并给定允许的起点集合。所有块等长，
所以对一行过滤掉与预约相交的块后，按右端点递增贪心即可最大化不相交块数。先算空行
基线，再只重算受影响行，期望时间 $O((R+n_a)B)$，其中 $B$ 是允许块数、$n_a$ 是受影响
行数；空间 $O(R)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class GeneralCinema {
public:
  long long maxGroups(long long rows, int width, int groupSize,
                      const vector<int>& allowedStarts,
                      const vector<pair<int, int>>& reservedSeats) {
    vector<int> starts = allowedStarts;
    sort(starts.begin(), starts.end());
    starts.erase(remove_if(starts.begin(), starts.end(), [&](int start) {
      return start < 1 || start + groupSize - 1 > width;
    }), starts.end());
    unordered_map<int, unsigned> masks;
    for (auto [row, seat] : reservedSeats) masks[row] |= 1U << (seat - 1);
    auto best = [&](unsigned mask) {
      int count = 0;
      int lastEnd = 0;
      for (int start : starts) {
        int end = start + groupSize - 1;
        unsigned block = ((1U << groupSize) - 1) << (start - 1);
        if (start <= lastEnd || (mask & block) != 0) continue;
        ++count;
        lastEnd = end;
      }
      return count;
    };
    int baseline = best(0);
    long long answer = rows * baseline;
    for (const auto& [row, mask] : masks) {
      static_cast<void>(row);
      answer += best(mask) - baseline;
    }
    return answer;
  }
};
```

## 变种三：在线预约、取消与总数查询

新定义：预约会动态加入或取消，每次操作后询问当前最大组数。维护每行 10 位掩码和该行
旧贡献；更新一个座位前先从总数减旧贡献，改掩码，再加新贡献。每次更新时间期望 $O(1)$，
空间 $O(A)$，其中 $A$ 是当前有相关预约的行数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OnlineCinema {
public:
  explicit OnlineCinema(int rows) : total_(2LL * rows) {}
  void reserve(int row, int seat) { update(row, seat, true); }
  void cancel(int row, int seat) { update(row, seat, false); }
  long long query() const { return total_; }
private:
  static int groups(int mask) {
    constexpr int left = 0b0000111100;
    constexpr int middle = 0b0011110000;
    constexpr int right = 0b1111000000;
    if ((mask & left) == 0 && (mask & right) == 0) return 2;
    return (mask & left) == 0 || (mask & middle) == 0 || (mask & right) == 0;
  }
  void update(int row, int seat, bool reserved) {
    if (seat < 2 || seat > 9) return;
    int oldMask = masks_[row];
    int bit = 1 << seat;
    int newMask = reserved ? oldMask | bit : oldMask & ~bit;
    if (newMask == oldMask) return;
    total_ += groups(newMask) - groups(oldMask);
    if (newMask == 0) {
      masks_.erase(row);
    } else {
      masks_[row] = newMask;
    }
  }
  unordered_map<int, int> masks_;
  long long total_;
};
```

## 变种四：三个座位块具有不同收益

新定义：左、中、右块安排一组的收益分别给定，目标最大化总收益。原来只分三种情形的
计数贪心失效：例如中间块收益可能大于左右两块之和。每个受影响行枚举三个块的 8 个子集，
同时检查预约冲突和块间重叠；空行也用同一函数求基线。时间期望 $O(R)$、空间 $O(R)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class WeightedCinema {
public:
  long long maxValue(int n, const vector<vector<int>>& reservedSeats,
                    const array<int, 3>& value) {
    const array<int, 3> blocks = {
        0b0000111100, 0b0011110000, 0b1111000000};
    auto best = [&](int reserved) {
      int answer = 0;
      for (int subset = 0; subset < 8; ++subset) {
        int used = 0;
        int score = 0;
        bool valid = true;
        for (int index = 0; index < 3; ++index) {
          if ((subset & (1 << index)) == 0) continue;
          if ((reserved & blocks[index]) != 0 || (used & blocks[index]) != 0) {
            valid = false;
            break;
          }
          used |= blocks[index];
          score += value[index];
        }
        if (valid) answer = max(answer, score);
      }
      return answer;
    };
    unordered_map<int, int> masks;
    for (const auto& reserved : reservedSeats) {
      if (reserved[1] >= 2 && reserved[1] <= 9) {
        masks[reserved[0]] |= 1 << reserved[1];
      }
    }
    int baseline = best(0);
    long long answer = 1LL * n * baseline;
    for (const auto& [row, mask] : masks) {
      static_cast<void>(row);
      answer += best(mask) - baseline;
    }
    return answer;
  }
};
```

## 来源与 Algo 状态

- [LeetCode 中国官方题面](https://leetcode.cn/problems/cinema-seat-allocation/)
- [力扣中国每日一题入口](https://leetcode.cn/problemset/)
- Algo 对应知识入口与发布状态在本轮发布核验后写入邮件尾部。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/cinema-seat-allocation/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-b/">← [codeforces] CF Round 1117 Div.2 B Gigantomachy</a>
<span class="daily-archive-pager__empty"></span>
</nav>
