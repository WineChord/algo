---
title: "[力扣每日一题] 2026-08-23｜LC 1927 求和游戏"
---

# [力扣每日一题] 2026-08-23｜LC 1927 求和游戏

<p class="daily-archive-kicker">2026-08-23 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-23 题目列表</a> · <a href="../../../dp/game-dp/#problem-lc-1927">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a5acd9cc49f8d79243d13f5a15e2d70661d0487494d9e405b8c53c94c9f435ea -->
[力扣官方题目：1927. 求和游戏](https://leetcode.cn/problems/sum-game/)

## 官方原始信息

- 日期：2026-08-23（北京时间），经力扣中国每日一题官方记录核对。
- 题号：LC 1927；官方中文标题：求和游戏；官方难度：中等。
- 原比赛：第 56 场双周赛 Q3；官方竞赛分值：5 分。
- ZeroTracer 社区估算竞赛分：2004.535，抓取于 2026-08-23；这不是力扣官方难度或分值。
- 官方链接：[https://leetcode.cn/problems/sum-game/](https://leetcode.cn/problems/sum-game/)
- 函数签名：`bool sumGame(string num)`。
- 官方标签：贪心、数学、字符串、博弈。

### 原始题意

给定一个长度为偶数的字符串 `num`，其中每个字符是数字或问号。Alice 与 Bob 轮流把一个
问号替换为 0–9 中任意数字，Alice 先手；所有问号被替换后，若前半部分的数位和等于后半
部分，Bob 获胜，否则 Alice 获胜。双方都采用最优策略，判断 Alice 是否必胜。

### 全部官方样例

```text
示例 1
输入：num = "5023"
输出：false
解释：没有问号；左半和为 5，右半和也为 5，因此 Bob 获胜。

示例 2
输入：num = "25??"
输出：true
解释：Alice 可以在右半选择一个问号填 9。无论 Bob 如何填另一个问号，右半和都无法等于 7。

示例 3
输入：num = "?3295???"
输出：false
解释：双方最优时 Bob 能让最终两半数位和相等，因此 Alice 不能保证获胜。
```

### 全部约束

- $2\le num.length\le10^5$。
- `num.length` 为偶数。
- `num` 只包含数字与 `?`。

## 最优结论摘要

设已知数字的左右半和之差为 $\Delta=L-R$，左右问号数分别为 $q_L,q_R$，总问号数为
$q=q_L+q_R$。Alice 必胜当且仅当

$$
q\text{ 为奇数}\quad\text{或}\quad2\Delta\ne9(q_R-q_L).
$$

一次扫描统计四个量即可，时间复杂度 $O(n)$，额外空间 $O(1)$。

## 约束推导、溢出与边界

- $n\le10^5$ 排除了博弈树搜索；必须把状态压缩成和差与剩余问号数量。
- 每填一个问号总回合数减一。问号总数为奇数时 Alice 比 Bob 多一步，先手能打破平衡。
- 一个问号可贡献 0–9，成对回合的关键总量是 $0+9=9$，因此判定式出现系数 9。
- 已知半边和的绝对值至多 $9\times50000=450000$，乘 2 后仍远小于 `int` 上限。
- 没有问号时公式退化为 $2(L-R)\ne0$，恰好判断两半和是否不同。
- 问号可以全部在同一半；式子不要求 $q_L=q_R$。

## 官方样例手推

`25??` 中 $L=7,R=0,q_L=0,q_R=2$。总问号为偶数，但
$2\Delta=14$，而 $9(q_R-q_L)=18$，二者不等，因此 Alice 必胜。

`?3295???` 中，左半已知和为 $L=3+2+9=14$，右半已知和为 $R=5$，并且
$q_L=1,q_R=3$。总问号为 4，且 $2\Delta=2\times9=18=9(3-1)$，所以 Bob 获胜。

## 解法一：极小数据上的完整极大极小搜索

每个回合枚举一个尚未填写的位置和 10 个数字。递归函数返回“Alice 从当前状态是否必胜”：
Alice 回合只要存在一个获胜后继就返回真，Bob 回合只有所有后继都让 Alice 获胜时才返回真。
它覆盖每一种合法对局和双方每种策略，因此正确；不记忆化的搜索树约为 $O(10^q q!)$。当前
字符串记忆化版本的唯一部分赋值状态至多为 $11^q$；每个状态还要构造、哈希和扫描长度为
$n$ 的字符串，并枚举至多 $10q$ 个动作，平均时间上界为 $O((n+q)11^q)$，记忆空间为
$O(n11^q)$；仍然远不能处理原约束。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool sumGame(string num) {
    unordered_map<string, bool> memo;
    return solve(num, true, memo);
  }
private:
  bool solve(string& num, bool aliceTurn, unordered_map<string, bool>& memo) {
    string key = num + (aliceTurn ? 'A' : 'B');
    auto found = memo.find(key);
    if (found != memo.end()) return found->second;
    bool finished = true;
    for (char character : num) finished &= character != '?';
    if (finished) {
      int difference = 0;
      int half = static_cast<int>(num.size()) / 2;
      for (int i = 0; i < static_cast<int>(num.size()); ++i) {
        difference += (i < half ? 1 : -1) * (num[i] - '0');
      }
      return memo[key] = difference != 0;
    }
    bool result = !aliceTurn;
    for (int position = 0; position < static_cast<int>(num.size()); ++position) {
      if (num[position] != '?') continue;
      for (char digit = '0'; digit <= '9'; ++digit) {
        num[position] = digit;
        bool child = solve(num, !aliceTurn, memo);
        num[position] = '?';
        if (aliceTurn && child) return memo[key] = true;
        if (!aliceTurn && !child) return memo[key] = false;
      }
    }
    return memo[key] = result;
  }
};
```

## 从博弈树到四个统计量

具体问号位置只通过它属于左半还是右半影响最终和差。把已知数字压缩为 $\Delta=L-R$，把
未知位置压缩为 $q_L,q_R$ 后，所有字符级状态都可以丢弃。

若总问号为奇数，Alice 最后还会多填一次。她可在左右贡献方向与数字极值之间选择，Bob 没有
后续回合消除这一自由度，所以 Alice 必胜。

若总问号为偶数，定义势能

$$
P=2(L-R)+9(q_L-q_R).
$$

每次选择左半问号并填 $d$，$P$ 改变 $2d-9$；选择右半问号则改变 $9-2d$。无论选择哪一半，
单步可实现的变化集合都是 $\{-9,-7,\ldots,7,9\}$。这把位置选择和数字选择统一成同一个
一维博弈。Bob 恰好能守住平局的唯一初始条件是

$$
2(L-R)=9(q_R-q_L).
$$

## 最佳实用解：一次扫描后的数学判定

### 正确性证明

若 $q$ 为奇数，Alice 比 Bob 多一个选择。把最后一个未配对回合视为 Alice 的自由数字，她能
在至少两个不同和差之间选择；至多一个选择会让差为 0，因此能保证非零。

以下设 $q$ 为偶数，并把 Alice 的一步与紧随其后的 Bob 一步配成一组。若组首 $P=0$，Alice
走后产生某个奇数变化 $\delta\in[-9,9]$；Bob 无论剩余问号位于哪一半，都能选择数字实现
$-\delta$，把 $P$ 恢复为 0。重复到终局时 $q_L=q_R=0$，所以 $P=2(L-R)=0$，Bob 获胜。

若组首 $P\ne0$，Alice 选择与 $P$ 同号的变化 9 或 -9，使新势能的绝对值增加 9。Bob 的
单步变化绝对值至多 9，因此不能跨过 0；这一组结束后，$P$ 仍与组首同号且绝对值不减。这个
不变量保持到终局，最终 $2(L-R)=P\ne0$，Alice 获胜。于是偶数回合中，初始 $P=0$ 当且仅当
Bob 必胜；它等价于 $2\Delta=9(q_R-q_L)$，算法判定正确。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool sumGame(string num) {
    int half = static_cast<int>(num.size()) / 2;
    int difference = 0;
    int leftQuestions = 0;
    int rightQuestions = 0;
    for (int i = 0; i < static_cast<int>(num.size()); ++i) {
      if (num[i] == '?') {
        if (i < half) {
          ++leftQuestions;
        } else {
          ++rightQuestions;
        }
      } else {
        difference += (i < half ? 1 : -1) * (num[i] - '0');
      }
    }
    if ((leftQuestions + rightQuestions) % 2 == 1) return true;
    return 2 * difference != 9 * (rightQuestions - leftQuestions);
  }
};
```

时间复杂度 $O(n)$，额外空间 $O(1)$。

## 同阶方案比较与易错点

也可维护势能 $P=2(L-R)+9(q_L-q_R)$ 并判断 `q` 为奇数或 $P\ne0$；它与上式完全等价。
直接保存左右四个量更容易核对符号，竞赛中更推荐。

- 左半问号与右半问号的符号写反；用一个固定公式并拿 `25??` 校验。
- 忘记先判断问号总数奇偶，单看等式会漏掉 Alice 多一步的情况。
- 把数字字符直接加进和，必须先减 `'0'`。
- 误以为双方只会填 0 或 9；极值有助于理解，但完整配对策略会使用 $d$ 与 $9-d$。
- 把题目当作“存在一种填法”，而不是双方最优的对抗博弈。

## 可复现验证

两份原题代码均以 C++23 编译并通过三个官方样例、无问号、单问号、问号全在一侧、已平衡与
最大长度统计边界。随机生成 25,000 个长度不超过 8 的状态，以压缩后的极大极小搜索为 oracle，
与数学判定逐项一致。

## Follow-up 与约束变种

### 变种一：数字改为任意进制

新定义：$2\le B\le10^9$，整数数组长度为 $2$ 到 $10^5$ 的偶数；每项为 `-1` 或
$[0,B-1]$ 内的合法数位，`-1` 表示未知。配对互补总量从 9 变成 $B-1$，其他证明不变。
这些上界也保证下式的 `long long` 计算安全。Alice 必胜当且仅当问号总数为奇数，或
$2\Delta\ne(B-1)(q_R-q_L)$。时间 $O(n)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool sumGameBase(const vector<int>& digits, int base) {
    int half = static_cast<int>(digits.size()) / 2;
    long long difference = 0;
    int leftQuestions = 0;
    int rightQuestions = 0;
    for (int i = 0; i < static_cast<int>(digits.size()); ++i) {
      if (digits[i] == -1) {
        if (i < half) {
          ++leftQuestions;
        } else {
          ++rightQuestions;
        }
      } else {
        difference += (i < half ? 1LL : -1LL) * digits[i];
      }
    }
    if ((leftQuestions + rightQuestions) % 2 == 1) return true;
    return 2 * difference != 1LL * (base - 1) * (rightQuestions - leftQuestions);
  }
};
```

### 变种二：Bob 的目标是固定和差

新定义：Bob 在最终 $L-R=target$ 时获胜，而非只在差为 0 时获胜，并约束
$|target|\le10^{15}$。把固定数字差平移为 $\Delta-target$，原配对分析完全成立；该上界也让
取负与两倍差值都安全落在 `long long` 内。时间 $O(n)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool aliceWinsForTarget(const string& num, long long target) {
    int half = static_cast<int>(num.size()) / 2;
    long long difference = -target;
    int leftQuestions = 0;
    int rightQuestions = 0;
    for (int i = 0; i < static_cast<int>(num.size()); ++i) {
      if (num[i] == '?') {
        if (i < half) {
          ++leftQuestions;
        } else {
          ++rightQuestions;
        }
      } else {
        difference += (i < half ? 1 : -1) * (num[i] - '0');
      }
    }
    if ((leftQuestions + rightQuestions) % 2 == 1) return true;
    return 2 * difference != 9 * (rightQuestions - leftQuestions);
  }
};
```

### 变种三：在线修改字符并随时询问胜负

新定义：字符串固定分半，支持把某个位置改为数字或问号，并在每次修改后判断 Alice 是否
必胜。无需树结构，因为判定只依赖四个全局统计量；删除旧字符贡献、加入新字符贡献即可。
初始化 $O(n)$，每次修改与查询 $O(1)$，空间 $O(n)$ 用于保存当前字符串。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Game {
public:
  explicit Game(string value) : num(move(value)), half(num.size() / 2) {
    for (int i = 0; i < static_cast<int>(num.size()); ++i) add(i, num[i], 1);
  }
  void update(int index, char character) {
    --index;
    add(index, num[index], -1);
    num[index] = character;
    add(index, num[index], 1);
  }
  bool aliceWins() const {
    if ((leftQuestions + rightQuestions) % 2 == 1) return true;
    return 2 * difference != 9 * (rightQuestions - leftQuestions);
  }
private:
  string num;
  int half;
  int difference = 0;
  int leftQuestions = 0;
  int rightQuestions = 0;
  void add(int index, char character, int sign) {
    if (character == '?') {
      (index < half ? leftQuestions : rightQuestions) += sign;
    } else {
      difference += sign * (index < half ? 1 : -1) * (character - '0');
    }
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string num;
  int q;
  cin >> num >> q;
  Game game(num);
  while (q--) {
    int index;
    char character;
    cin >> index >> character;
    game.update(index, character);
    cout << (game.aliceWins() ? "Alice" : "Bob") << '\n';
  }
  return 0;
}
```

### 变种四：不对抗，统计让两半相等的填法数

新定义：所有问号由同一个人任意填写，求最终两半和相等的赋值数量，模 $10^9+7$；为使差值
DP 可行，额外约束问号数 $q\le200$。原博弈配对判定失效，因为现在需要计数所有数字组合。
以当前左右和差为状态，每个左问号加 0–9、每个右问号减 0–9。时间 $O(n+10q^2)$，空间
$O(q)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countBalancedAssignments(const string& num) {
    constexpr int MOD = 1000000007;
    int half = static_cast<int>(num.size()) / 2;
    int knownDifference = 0;
    vector<int> signs;
    for (int i = 0; i < static_cast<int>(num.size()); ++i) {
      int sign = i < half ? 1 : -1;
      if (num[i] == '?') {
        signs.push_back(sign);
      } else {
        knownDifference += sign * (num[i] - '0');
      }
    }
    int limit = 9 * static_cast<int>(signs.size());
    vector<int> ways(2 * limit + 1);
    vector<int> next(2 * limit + 1);
    ways[limit] = 1;
    for (int sign : signs) {
      fill(next.begin(), next.end(), 0);
      for (int difference = -limit; difference <= limit; ++difference) {
        if (ways[difference + limit] == 0) continue;
        for (int digit = 0; digit <= 9; ++digit) {
          int target = difference + sign * digit;
          if (target < -limit || target > limit) continue;
          next[target + limit] += ways[difference + limit];
          if (next[target + limit] >= MOD) next[target + limit] -= MOD;
        }
      }
      ways.swap(next);
    }
    int target = -knownDifference;
    if (target < -limit || target > limit) return 0;
    return ways[target + limit];
  }
};
```

## 推荐记忆

这道题不要背孤立等式。先把字符状态压成“已知和差 + 左右问号数”，再看回合奇偶；偶数回合
中一对互补数字的总量是 9，平衡条件自然变成 $2(L-R)=9(q_R-q_L)$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/sum-game/)
- [对应知识专题](../../dp/game-dp.md#problem-lc-1927)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2257-f1/">← [codeforces] CF Round 1117 Div.2 F1 Beaver&#x27;s Jumping Track (Easy Version)</a>
<span class="daily-archive-pager__empty"></span>
</nav>
