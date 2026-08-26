---
title: "[力扣每日一题] 2026-08-27｜LC 3720 大于目标字符串的最小字典序排列"
---

# [力扣每日一题] 2026-08-27｜LC 3720 大于目标字符串的最小字典序排列

<p class="daily-archive-kicker">2026-08-27 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-27 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=efc6dc693b485395985df4f7671c4ddc819e167bb9c7dbeee250572000bfd902 -->
## 官方原始信息

- 来源：力扣中国 2026-08-27 每日一题；历史来源为第 472 场周赛 Q3
- 题号：LC 3720
- 官方中文标题：大于目标字符串的最小字典序排列
- 官方难度：中等
- 官方比赛分值：5 分
- ZeroTracer 社区估算竞赛分：1958.15（公开数据抓取于 2026-08-27）
- 官方链接：[3720. 大于目标字符串的最小字典序排列](https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/)
- 函数签名：`string lexGreaterPermutation(string s, string target)`

### 原始题意

给定两个等长小写字符串 `s` 与 `target`。重新排列 `s` 的全部字符，求字典序严格大于
`target` 的排列中最小的一个；若不存在，返回空字符串。每个字符必须按它在 `s` 中的出现次数
恰好使用，不能丢失、添加或替换字符。

### 全部官方样例

样例 1：

```text
输入：s = "abc", target = "bba"
输出："bca"
解释："bca" 是 s 的排列，严格大于 "bba"；不存在更小且仍严格大于 target 的排列。
```

样例 2：

```text
输入：s = "leet", target = "code"
输出："eelt"
解释："eelt" 已在第一个字符处大于 "code"，并且是满足条件的最小排列。
```

样例 3：

```text
输入：s = "baba", target = "bbaa"
输出：""
解释：s 的最大排列就是 "bbaa"，无法得到严格更大的排列。
```

### 全部约束

- $1\le |s|=|\texttt{target}|\le 300$
- `s` 和 `target` 只含小写英文字母

## 最优结论与推荐记忆方案

答案与 `target` 必有一个首次不同位置 $p$：前缀 $[0,p)$ 完全相同，而答案的第 $p$ 个
字符严格更大。先尽量用频次数组匹配 `target` 前缀；在当前位置尝试最小可用的更大字符，
若不存在就恢复上一位并向左回退。找到最靠右的可行枢轴后，把剩余字符升序填入后缀。

字母表大小固定为 26，时间复杂度为 $O(26n)=O(n)$，频次数组使用 $O(26)$ 额外空间，
返回字符串占 $O(n)$。推荐记忆为：**多重集合的严格字典序后继 = 最靠右可增大的枢轴 +
最小增大字符 + 升序最小后缀。**

## 约束推导、整数安全与边界

- 不同排列数量最坏可达 $n!$，即便用 `next_permutation` 去重，也无法承受 $n=300$。
- 只要首次不同位置已经选了更大字符，后续无论如何排列都仍严格大于 `target`；因此后缀只需
  做到尽可能小，即按字符升序排列。
- 为让整个答案尽量小，首次不同位置应尽可能靠右；这解释了为什么先匹配，再向左回退。
- 重复字符不能按原下标区分，应使用 26 个频次；每个频次至多 300，`int` 足够。
- 若 `target` 本身能由 `s` 排列得到，仍不能返回相等串，必须回退寻找严格后继。

需要覆盖的边界：

- $n=1$：仅当 `s[0] > target[0]` 时返回 `s`。
- `s` 的升序排列已经大于 `target`：答案就是升序排列。
- `s` 的降序排列小于或等于 `target`：不存在答案。
- 多个重复字符跨越枢轴：回退时必须把此前匹配字符恢复到频次数组。
- 前缀在某处无法匹配：仍可能直接用更大字符完成答案，不能立即判无解。

## 官方样例手推

对 `s = "abc"`、`target = "bba"`：

1. 频次为 `a:1, b:1, c:1`。第 0 位匹配 `b`，剩余 `a:1, c:1`。
2. 第 1 位还想匹配 `b`，但没有可用的 `b`。
3. 在第 1 位寻找严格大于 `b` 的最小剩余字符，得到 `c`。
4. 剩余 `a` 升序放入后缀，答案为 `"bca"`。

对 `s = "baba"`、`target = "bbaa"`，四位可以全部匹配，得到的只是相等串。算法从末位开始
逐位恢复字符，却在每个位置都找不到可用的更大字符，最终正确返回空串。

## 解法一：枚举全部排列

先排序 `s`，再按字典序枚举全部不同排列，返回第一个严格大于 `target` 的排列。排序后的枚举
顺序保证首个合法排列最小；若共有 $P$ 个不同排列，时间复杂度为 $O(Pn)$，排序及枚举使用
$O(n)$ 空间保存字符串。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string lexGreaterPermutation(string s, string target) {
    sort(s.begin(), s.end());
    do {
      if (s > target)
        return s;
    } while (next_permutation(s.begin(), s.end()));
    return "";
  }
};
```

它适合作为 $n\le 9$ 的暴力 oracle，但排列数的阶乘增长使其无法用于正式约束。

## 解法二：频次 DFS 与前缀剪枝

逐位从小到大选择尚有频次的字符，并维护当前前缀与 `target` 的关系。前缀已经更大时，后缀
可以直接升序填充；前缀仍相等时继续尝试。频次数组消除了重复排列，但最坏仍可能探索指数级
状态，时间上界与不同排列数量同阶，递归栈和当前串占 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string target;
  array<int, 26> count{};
  bool search(int position, bool greater, string& current) {
    int n = static_cast<int>(target.size());
    if (position == n)
      return greater;
    if (greater) {
      for (int c = 0; c < 26; ++c) {
        current.append(count[c], static_cast<char>('a' + c));
      }
      return true;
    }
    int start = target[position] - 'a';
    for (int c = start; c < 26; ++c) {
      if (count[c] == 0)
        continue;
      --count[c];
      current.push_back(static_cast<char>('a' + c));
      if (search(position + 1, c > start, current))
        return true;
      current.pop_back();
      ++count[c];
    }
    return false;
  }
public:
  string lexGreaterPermutation(string s, string targetInput) {
    target = move(targetInput);
    for (char c : s)
      ++count[c - 'a'];
    string answer;
    if (search(0, false, answer))
      return answer;
    return "";
  }
};
```

该写法展示了“前缀一旦更大就贪心结束”的结构，但仍会反复尝试多个相等前缀的分支。

## 解法三：枚举枢轴并重建后缀

枚举首次不同位置 $p$，检查 `target[0..p)` 是否能由字符频次组成，再选最小可用的大于
`target[p]` 的字符并升序重建后缀。按 $p=n-1,n-2,\ldots,0$ 枚举，首个候选就是答案。
若每次都从头统计前缀，复杂度为 $O(26n^2)$，空间为 $O(26+n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string lexGreaterPermutation(string s, string target) {
    int n = static_cast<int>(s.size());
    for (int pivot = n - 1; pivot >= 0; --pivot) {
      array<int, 26> count{};
      for (char c : s)
        ++count[c - 'a'];
      bool possible = true;
      for (int i = 0; i < pivot; ++i) {
        int c = target[i] - 'a';
        if (count[c] == 0) {
          possible = false;
          break;
        }
        --count[c];
      }
      if (!possible)
        continue;
      for (int c = target[pivot] - 'a' + 1; c < 26; ++c) {
        if (count[c] == 0)
          continue;
        string answer = target.substr(0, pivot);
        answer.push_back(static_cast<char>('a' + c));
        --count[c];
        for (int x = 0; x < 26; ++x) {
          answer.append(count[x], static_cast<char>('a' + x));
        }
        return answer;
      }
    }
    return "";
  }
};
```

下一步优化的关键是：相邻两个枢轴的前缀只差一个字符，不必每次重新统计。

## 最佳实用解：匹配前缀后向左恢复

### 算法

1. 统计 `s` 的 26 个字符频次。
2. 从左到右尽量消耗字符，匹配 `target` 的最长可构造前缀，令其长度为 `i`。
3. 在位置 `i` 尝试最小的可用字符 `c > target[i]`；成功时，前缀、`c` 与升序剩余字符
   组成候选并立即返回。
4. 若当前位置没有可增大的字符，就令 `i` 左移一位，并把刚离开前缀的 `target[i]` 恢复到
   频次数组，再重复步骤 3。
5. 回退到位置 0 仍失败，返回空串。

### 正确性证明

**引理 1**：任意严格大于 `target` 的等长字符串都存在唯一首次不同位置 $p$，并且该位置
字符严格大于 `target[p]`。

**证明**：两个不相等的等长字符串必有最左不同位置。字典序由这一位置决定；若整个字符串
更大，则该位置字符必更大。证毕。

**引理 2**：在所有可行答案中，首次不同位置越靠右，答案越小。

**证明**：设答案 $A$ 在 $p$ 首次变大，答案 $B$ 在更靠右的 $q>p$ 首次变大。位置 $p$
处，$B[p]=\texttt{target}[p]<A[p]$，所以 $B<A$。证毕。

**引理 3**：固定首次不同位置 $p$ 后，选择最小可用的大于 `target[p]` 的字符，再把剩余字符
升序排列，得到该枢轴下的最小答案。

**证明**：首先应最小化位置 $p$，因为它早于所有后缀位置；固定该字符后，剩余多重集合的
升序排列是其最小排列。证毕。

**定理**：算法返回全局最小的严格较大排列；返回空串时不存在合法排列。

**证明**：算法先匹配最长可构造前缀，再逐位向左恢复，检查枢轴的顺序正是从最靠右到最靠
左。由引理 2，首个可行枢轴优于所有更靠左的枢轴；由引理 3，该枢轴内构造出的候选最小。
若所有枢轴都失败，由引理 1，任何合法答案所需的首次不同位置都不存在。证毕。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string lexGreaterPermutation(string s, string target) {
    array<int, 26> count{};
    for (char c : s)
      ++count[c - 'a'];
    int n = static_cast<int>(s.size());
    int i = 0;
    while (i < n && count[target[i] - 'a'] > 0) {
      --count[target[i] - 'a'];
      ++i;
    }
    while (true) {
      if (i < n) {
        for (int c = target[i] - 'a' + 1; c < 26; ++c) {
          if (count[c] == 0)
            continue;
          string answer = target.substr(0, i);
          answer.push_back(static_cast<char>('a' + c));
          --count[c];
          for (int x = 0; x < 26; ++x) {
            answer.append(count[x], static_cast<char>('a' + x));
          }
          return answer;
        }
      }
      if (i == 0)
        break;
      --i;
      ++count[target[i] - 'a'];
    }
    return "";
  }
};
```

时间复杂度为 $O(26n)=O(n)$：每个前缀字符至多被消耗、恢复一次，每次枢轴检查最多扫描
26 个字符；构造答案也只需 $O(n)$。频次数组使用 $O(26)$ 额外空间，返回值占 $O(n)$。

## 同阶与实用方案比较

频次 DFS 与最优解都利用了字符多重集合，但 DFS 仍承担指数级搜索风险。逐枢轴重建已把问题
压到多项式，却重复计算前缀。向左恢复版本只维护一份频次，复杂度线性、实现短而稳定。

若字符表固定且没有位置限制，优先记忆向左恢复。若加入位置可放字符限制，升序后缀不再自动
可行，就应退回“枢轴枚举 + 可行性判定”的更通用框架。

## 常见错误

- 完整匹配 `target` 后直接返回，违反“严格大于”。
- 当前字符无法匹配就判无解，漏掉在该位置换成更大字符的答案。
- 回退时只移动下标，没有恢复此前消耗的字符频次。
- 找到枢轴后仍尝试匹配 `target` 的后缀；此时只需把剩余字符升序排列。
- 选择最靠左的可增大位置，得到合法但不是最小的答案。
- 按字符下标做 `used`，导致重复字符产生大量重复搜索。

## 可复现验证

把全部不同排列的暴力解作为 oracle。对字母表 `{a,b,c}`、长度 $1$ 到 $5$ 的所有 `s` 和
`target` 共 66,429 组组合逐项比较：最优解的返回值与 oracle 完全一致。另覆盖三个官方样例、
完整相等后回退、升序串直接可用、降序上界无解和大量重复字符。所有发布代码块均使用 C++23
完成语法编译。

## Follow-up 与约束变种

### 变种一：求严格小于目标的最大排列

新定义：用 `s` 的全部字符构造字典序严格小于 `target` 的最大排列。原证明完全镜像：首次
不同位置尽量靠右，该位置取最大的可用较小字符，后缀降序。时间 $O(26n)$，空间 $O(26)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string lexSmallerPermutation(string s, string target) {
    array<int, 26> count{};
    for (char c : s)
      ++count[c - 'a'];
    int n = static_cast<int>(s.size());
    int i = 0;
    while (i < n && count[target[i] - 'a'] > 0) {
      --count[target[i] - 'a'];
      ++i;
    }
    while (true) {
      if (i < n) {
        for (int c = target[i] - 'a' - 1; c >= 0; --c) {
          if (count[c] == 0)
            continue;
          string answer = target.substr(0, i);
          answer.push_back(static_cast<char>('a' + c));
          --count[c];
          for (int x = 25; x >= 0; --x) {
            answer.append(count[x], static_cast<char>('a' + x));
          }
          return answer;
        }
      }
      if (i == 0)
        break;
      --i;
      ++count[target[i] - 'a'];
    }
    return "";
  }
};
```

### 变种二：允许答案等于目标

新定义：求大于或等于 `target` 的最小排列。前缀若完整匹配，原算法之所以回退只是因为严格
不等号；本变种应立即返回 `target`。否则仍执行同一向左恢复过程，复杂度不变。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string lexAtLeastPermutation(string s, string target) {
    array<int, 26> count{};
    for (char c : s)
      ++count[c - 'a'];
    int n = static_cast<int>(s.size());
    int i = 0;
    while (i < n && count[target[i] - 'a'] > 0) {
      --count[target[i] - 'a'];
      ++i;
    }
    if (i == n)
      return target;
    while (true) {
      for (int c = target[i] - 'a' + 1; c < 26; ++c) {
        if (count[c] == 0)
          continue;
        string answer = target.substr(0, i);
        answer.push_back(static_cast<char>('a' + c));
        --count[c];
        for (int x = 0; x < 26; ++x) {
          answer.append(count[x], static_cast<char>('a' + x));
        }
        return answer;
      }
      if (i == 0)
        break;
      --i;
      ++count[target[i] - 'a'];
    }
    return "";
  }
};
```

### 变种三：统计严格大于目标的不同排列数并取模

新定义：返回 `s` 的不同排列中严格大于 `target` 的数量，对 $10^9+7$ 取模。线性后继算法
只能找一个答案，不能计数。先计算多重集合的排列总数，再按字典序排名：长度为 $m$ 的剩余
集合共有 $T$ 个排列，若首字符取频次为 `count[c]` 的字符，则该块大小为
$T\cdot\texttt{count}[c]/m$。由于 $m\le300<10^9+7$，除法可用模逆元完成。代码约做
$O(26n)$ 次模运算，预处理阶乘和逆元为 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  static constexpr long long kMod = 1000000007;
  long long power(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
      if (exponent & 1)
        result = result * base % kMod;
      base = base * base % kMod;
      exponent >>= 1;
    }
    return result;
  }
public:
  int countGreaterPermutations(string s, string target) {
    array<int, 26> count{};
    for (char c : s)
      ++count[c - 'a'];
    vector<long long> factorial(s.size() + 1, 1);
    for (int i = 1; i <= static_cast<int>(s.size()); ++i) {
      factorial[i] = factorial[i - 1] * i % kMod;
    }
    long long total = factorial[s.size()];
    for (int value : count)
      total = total * power(factorial[value], kMod - 2) % kMod;
    long long all = total;
    long long notGreater = 0;
    int remaining = static_cast<int>(s.size());
    bool targetIsPermutation = true;
    for (char ch : target) {
      int wanted = ch - 'a';
      long long inverseRemaining = power(remaining, kMod - 2);
      for (int c = 0; c < wanted; ++c) {
        long long block = total * count[c] % kMod * inverseRemaining % kMod;
        notGreater = (notGreater + block) % kMod;
      }
      if (count[wanted] == 0) {
        targetIsPermutation = false;
        break;
      }
      total = total * count[wanted] % kMod * inverseRemaining % kMod;
      --count[wanted];
      --remaining;
    }
    if (targetIsPermutation)
      notGreater = (notGreater + 1) % kMod;
    return static_cast<int>((all - notGreater + kMod) % kMod);
  }
};
```

这里 `notGreater` 统计字典序小于 `target` 的完整块，并在 `target` 本身是一个排列时再计入
相等项；总排列数减去它，正好得到严格较大数量。所有运算都在模意义下进行。

### 变种四：自定义且规模很大的有序字符表

新定义：字符不再局限于 26 个小写字母，而是任意可比较整数符号。数组扫描 26 个槽位不再
合适；用有序 `map` 保存频次，`upper_bound` 找最小更大符号，回退时恢复频次。后缀按键序
输出。时间复杂度为 $O(n\log\Sigma)$，空间为 $O(\Sigma+n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> nextPermutationOfMultiset(vector<int> symbols, const vector<int>& target) {
    map<int, int> count;
    for (int value : symbols)
      ++count[value];
    int n = static_cast<int>(symbols.size());
    int i = 0;
    while (i < n) {
      auto it = count.find(target[i]);
      if (it == count.end())
        break;
      if (--it->second == 0)
        count.erase(it);
      ++i;
    }
    while (true) {
      if (i < n) {
        auto greater = count.upper_bound(target[i]);
        if (greater != count.end()) {
          vector<int> answer(target.begin(), target.begin() + i);
          answer.push_back(greater->first);
          if (--greater->second == 0)
            count.erase(greater);
          for (auto [value, frequency] : count) {
            answer.insert(answer.end(), frequency, value);
          }
          return answer;
        }
      }
      if (i == 0)
        break;
      --i;
      ++count[target[i]];
    }
    return {};
  }
};
```

若进一步加入“每个位置只能使用特定字符”的限制，升序后缀会失效；应对每个枢轴候选用
二分图匹配或最大流检查剩余字符与位置的可行性，再借同一判定逐位构造最小后缀。

## 来源

- [力扣官方题目](https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/)
- [力扣第 472 场周赛](https://leetcode.cn/contest/weekly-contest-472/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2253-c/">← [codeforces] CF Educational Round 193 Div.2 C Sum of Distinct Values in a Matrix</a>
<span class="daily-archive-pager__empty"></span>
</nav>
