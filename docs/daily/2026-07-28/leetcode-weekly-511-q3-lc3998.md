---
title: "[力扣竞赛] 第 511 场周赛 Q3 LC 3998 使用子序列排序转换二进制字符串 中等"
---

# [力扣竞赛] 第 511 场周赛 Q3 LC 3998 使用子序列排序转换二进制字符串 中等

<p class="daily-archive-kicker">2026-07-28 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../basics/prefix-sums-and-difference/">进入知识专题</a></p>

## 官方原始信息

- **来源**：力扣第 511 场周赛 Q3
- **题号**：LC 3998
- **官方中文标题**：使用子序列排序转换二进制字符串
- **官方英文标题**：Transform Binary String Using Subsequence Sort
- **slug**：`transform-binary-string-using-subsequence-sort`
- **官方难度**：中等
- **官方竞赛分值**：5 分
- **ZeroTracer 社区估算竞赛分**：1862.3952723083（抓取日期：2026-07-28；这是社区估算，不是力扣官方难度）
- **官方题目链接**：[打开官方题面](https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/)
- **官方比赛链接**：[打开比赛页面](https://leetcode.cn/contest/weekly-contest-511/)

### 原始题意

给定一个二进制字符串 `s`，以及若干个与 `s` 等长的模式串 `strs[i]`。模式串只含 `'0'`、`'1'`、`'?'`，每个问号可以独立替换成零或一。

对 `s` 可以执行任意次操作：选取任意子序列，把该子序列按非递减顺序排序，再放回原来的那些下标。需要逐个判断：是否存在一种问号替换，使得某个模式串能够由 `s` 经过这些操作得到。

### 官方函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<bool> transformStr(string s, vector<string>& strs);
};
```

### 全部官方样例

#### 示例 1

```text
输入：s = "101", strs = ["1?1","0?1","0?0"]
输出：[true,true,false]
```

- `"1?1"` 把问号填成零，得到原串 `"101"`。
- `"0?1"` 把问号填成一，得到 `"011"`；把 `s` 的全部字符选为子序列并排序即可得到它。
- `"0?0"` 只能补成 `"000"` 或 `"010"`，两者的字符总数都与 `s` 不一致，因此不可达。

#### 示例 2

```text
输入：s = "1100", strs = ["0011","11?1","1?1?"]
输出：[true,false,true]
```

- `"0011"` 是把整个 `s` 排序后的结果。
- `"11?1"` 至少有三个一，但 `s` 只有两个一，不可达。
- `"1?1?"` 把两个问号都填成零得到 `"1010"`；选择原串下标 1、2 的子序列 `"10"` 并排序成 `"01"` 即可。

#### 示例 3

```text
输入：s = "1010", strs = ["0011"]
输出：[true]
```

选择原串下标 0、2、3 的子序列 `"110"`，排序成 `"011"` 后，整串变成 `"0011"`。

### 全部官方约束

- $1 \le n = |s| \le 2000$。
- `s[i]` 是 `'0'` 或 `'1'`。
- $1 \le |\texttt{strs}| \le 2000$。
- 每个 `strs[i]` 的长度都等于 $n$。
- 每个 `strs[i]` 只含 `'0'`、`'1'`、`'?'`。

输入规模最多包含 $n\cdot |\texttt{strs}|=4\times 10^6$ 个模式字符，因此 $O(n|\texttt{strs}|)$ 已经与读取输入同阶；指数枚举和逐查询二次算法都不可接受。计数最多到 2000，使用 `int` 足够；相邻交换次数最多为 $n(n-1)/2<2\times10^6$，但扩展代码仍使用 `long long` 保持稳健。

## 从操作抽象出偏序

在二进制子序列中，非递减排序只会把若干个逆序对 `10` 改成 `01`。特别地，直接选择任意两个下标 $i<j$ 且字符为 `1`、`0`，就是一次合法的二字符子序列排序。因此，所有操作等价于反复执行

$$
10\longrightarrow 01,
$$

也就是让一向右移动、让零向左移动。

令 $S(i)$ 和 $T(i)$ 分别表示源串与确定目标串前 $i$ 个字符中一的个数。一次合法交换不会增加任何前缀中的一的个数，并且不会改变整串一的总数，所以必要条件是

$$
T(i)\le S(i)\quad(1\le i\le n),\qquad T(n)=S(n).
$$

这个条件也充分。把源串和目标串中第 $k$ 个一的位置分别记作 $p_k,q_k$。前缀不等式等价于对每个 $k$ 都有 $p_k\le q_k$。从右向左依次把第 $k$ 个一通过 `10 -> 01` 移到 $q_k$，不会跨越其他一，于是一定能构造出目标串。

## 样例手推与关键边界

以 `s = "101"`、模式 `"0?1"` 为例。源串共有 $K=2$ 个一，模式固定含一个一，因此问号必须补成一，候选目标为 `"011"`。逐前缀比较一的个数：

$$
(0,1,2)\le(1,1,2),
$$

且总数同为二，所以可达。

真正需要覆盖的边界包括：

- $n=1$：没有可改变相对次序的逆序对，只能补成原字符。
- 模式全是问号：必须放入与 `s` 相同数量的一；最安全的放法是把一尽量放到右侧。
- 模式没有问号：直接使用前缀偏序判定。
- 固定一已经超过源串一总数，或即使所有问号都填一仍不足：总数守恒立即否决。
- 总数相同但前缀失败：例如 `s = "01"`、目标 `"10"`，目标第一个前缀已有一个一，而源串对应前缀没有一。
- `s` 全零或全一：只有字符总数完全匹配的补全可达。
- 重复查询完全相同：每个查询仍需读取全部 $n$ 个字符；最优复杂度不受影响。

## 解法一：状态图暴力搜索

枚举模式中所有问号的补法。对每个确定目标，从 `s` 开始做 BFS；每一步枚举所有 `1` 在左、`0` 在右的下标对并交换，直到找到目标或搜索完所有状态。

它显式覆盖了每一种问号补全和每一条合法操作路径，因此正确，但状态数可达 $\binom{n}{K}$，问号补法还有 $2^q$ 种，只适合极小规模，也适合作为随机对拍的 oracle。

<!-- compile:leetcode -->
```cpp
class Solution {
  bool reachableSmall(const string& s, const string& target) {
    if (count(s.begin(), s.end(), '1') != count(target.begin(), target.end(), '1')) return false;
    queue<string> q;
    unordered_set<string> seen;
    q.push(s);
    seen.insert(s);
    while (!q.empty()) {
      string cur = q.front();
      q.pop();
      if (cur == target) return true;
      int n = static_cast<int>(cur.size());
      for (int i = 0; i < n; ++i) {
        if (cur[i] != '1') continue;
        for (int j = i + 1; j < n; ++j) {
          if (cur[j] != '0') continue;
          string next = cur;
          swap(next[i], next[j]);
          if (seen.insert(next).second) q.push(next);
        }
      }
    }
    return false;
  }
  bool enumerate(string& pattern, int pos, const string& s) {
    if (pos == static_cast<int>(pattern.size())) return reachableSmall(s, pattern);
    if (pattern[pos] != '?') return enumerate(pattern, pos + 1, s);
    pattern[pos] = '0';
    if (enumerate(pattern, pos + 1, s)) {
      pattern[pos] = '?';
      return true;
    }
    pattern[pos] = '1';
    bool ok = enumerate(pattern, pos + 1, s);
    pattern[pos] = '?';
    return ok;
  }
public:
  vector<bool> transformStr(string s, vector<string>& strs) {
    vector<bool> ans;
    ans.reserve(strs.size());
    for (string pattern : strs) ans.push_back(enumerate(pattern, 0, s));
    return ans;
  }
};
```

- 时间复杂度：最坏约为 $O(2^q\binom{n}{K}n^2)$ 每个查询。
- 空间复杂度：$O(\binom{n}{K}n)$。
- 瓶颈：重复探索大量可达字符串，且重复验证不同补全。

## 解法二：保留问号枚举，用前缀偏序替代 BFS

已经知道确定目标可达当且仅当一的总数相同且所有前缀满足偏序，因此不必搜索操作序列。仍然枚举全部问号补法，但每个补全只需线性扫描。

<!-- compile:leetcode -->
```cpp
class Solution {
  bool reachable(const string& s, const string& target) {
    int sourceOnes = 0;
    int targetOnes = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      sourceOnes += s[i] == '1';
      targetOnes += target[i] == '1';
      if (targetOnes > sourceOnes) return false;
    }
    return sourceOnes == targetOnes;
  }
  bool enumerate(string& pattern, int pos, const string& s) {
    if (pos == static_cast<int>(pattern.size())) return reachable(s, pattern);
    if (pattern[pos] != '?') return enumerate(pattern, pos + 1, s);
    pattern[pos] = '0';
    if (enumerate(pattern, pos + 1, s)) {
      pattern[pos] = '?';
      return true;
    }
    pattern[pos] = '1';
    bool ok = enumerate(pattern, pos + 1, s);
    pattern[pos] = '?';
    return ok;
  }
public:
  vector<bool> transformStr(string s, vector<string>& strs) {
    vector<bool> ans;
    ans.reserve(strs.size());
    for (string pattern : strs) ans.push_back(enumerate(pattern, 0, s));
    return ans;
  }
};
```

- 时间复杂度：$O(2^q n)$ 每个查询。
- 空间复杂度：递归栈 $O(n)$。
- 改进：消除了对可达状态图的重复搜索。
- 剩余瓶颈：仍然逐一枚举问号补法。

## 解法三：把必须补的一全部推到最右侧

设源串共有 $K$ 个一；当前模式固定含 $F$ 个一、含 $Q$ 个问号。为了总数守恒，必须在问号中恰好再选

$$
R=K-F
$$

个位置填一。若 $R<0$ 或 $R>Q$，直接不可行。

前缀约束只给一的数量设置上界。因此，在所有恰好选 $R$ 个问号的位置中，把一放在最右边的 $R$ 个问号，能同时最小化每一个前缀中的一的数量。扫描到某个前缀、已经见过 $q_{\mathrm{seen}}$ 个问号时，后缀还剩 $Q-q_{\mathrm{seen}}$ 个问号；为了最终放够 $R$ 个一，当前前缀中不可避免地至少要放

$$
\max\bigl(0,\ R-(Q-q_{\mathrm{seen}})\bigr)
$$

个一。把它与当前前缀固定的一相加，就是所有合法补全能达到的最小前缀一数。

如果这个“逐前缀都最小”的候选仍超过源串前缀上界，其他补法只会更差；反之，该候选本身就是一个合法见证。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<bool> transformStr(string s, vector<string>& strs) {
    int n = static_cast<int>(s.size());
    int totalSourceOnes = count(s.begin(), s.end(), '1');
    vector<bool> ans;
    ans.reserve(strs.size());
    for (const string& pattern : strs) {
      int fixedOnes = count(pattern.begin(), pattern.end(), '1');
      int totalQuestions = count(pattern.begin(), pattern.end(), '?');
      int need = totalSourceOnes - fixedOnes;
      if (need < 0 || need > totalQuestions) {
        ans.push_back(false);
        continue;
      }
      int sourcePrefixOnes = 0;
      int fixedPrefixOnes = 0;
      int seenQuestions = 0;
      bool ok = true;
      for (int i = 0; i < n; ++i) {
        sourcePrefixOnes += s[i] == '1';
        fixedPrefixOnes += pattern[i] == '1';
        seenQuestions += pattern[i] == '?';
        int remainingQuestions = totalQuestions - seenQuestions;
        int forcedPrefixOnes = max(0, need - remainingQuestions);
        if (fixedPrefixOnes + forcedPrefixOnes > sourcePrefixOnes) {
          ok = false;
          break;
        }
      }
      ans.push_back(ok);
    }
    return ans;
  }
};
```

- 时间复杂度：$O(n|\texttt{strs}|)$，最坏 $4\times10^6$ 次字符处理。
- 额外空间复杂度：除返回值外 $O(1)$。
- 最优性：输入本身有 $\Theta(n|\texttt{strs}|)$ 个字符，任一字符都可能把答案从真改成假，因此渐近时间已经最优。

## 正确性证明

**引理 1**：对确定目标串 `t`，`t` 可由 `s` 得到，当且仅当两者一的总数相同，且每个前缀中 `t` 的一数不超过 `s`。

**证明**：每次把 `10` 变成 `01` 都保持总数，并且只会让覆盖左端但不覆盖右端的前缀少一个一，所以条件必要。反过来，设第 $k$ 个一在两串中的位置为 $p_k,q_k$。前缀条件等价于 $p_k\le q_k$。从最右边的一开始，把它逐步向右移到 $q_k$，再处理前一个一；这些移动互不交叉，最终得到目标。故条件充分。∎

**引理 2**：在恰好把 $R$ 个问号填一的所有补全中，把一放在最右侧的 $R$ 个问号，会同时最小化每一个前缀的一数。

**证明**：对任一前缀，若其后缀仅剩 $u$ 个问号，那么前缀中至少要承担 $\max(0,R-u)$ 个被选问号。选择最右侧的 $R$ 个问号恰好达到这个下界；因此它在所有前缀上同时最小。∎

**定理**：最优算法对每个模式返回真，当且仅当存在可达的问号补全。

**证明**：若总数区间不含 $K$，由字符总数守恒，不存在补全。否则算法检查引理 2 给出的逐前缀最小补全。若它违反某个前缀上界，任何其他补全在该前缀的一数都不少，也都违反引理 1；返回假正确。若所有前缀均通过，该补全总一数为 $K$，由引理 1 可达；返回真正确。∎

## 最佳实用解的实现要点

面试和竞赛中优先记忆“**固定目标的前缀偏序 + 把必须的一推到最右侧**”：

- 它直接由操作单向性推导，不依赖猜结论。
- 不需要构造字符串，不需要 DP，也不需要复杂数据结构。
- 与输入规模同阶，常数小，额外空间为常数。
- 证明可以拆成“可达偏序”和“最小前缀补全”两个清晰引理。

同阶实现也可以真的复制模式，并从右向左把最后 $R$ 个问号填一，再扫描前缀；它更直观，但每个查询要构造一个 $O(n)$ 临时串。上面的计数实现避免了分配和写入，通常更稳。

## 常见错误

- 只检查一的总数，不检查前缀偏序；`"01"` 不能变成 `"10"`。
- 误以为排序任意子序列可以随意重排；操作只能消除 `10` 逆序，不能制造逆序。
- 把必须的一放到最左侧问号；这会让前缀约束最难满足，方向恰好相反。
- 使用某一种贪心补法失败后就返回假，却没有证明它对所有前缀同时最优。
- 忽略固定一已经超过 $K$，或问号全填一仍达不到 $K$。
- 把题面中无语义的隐藏变量名当成接口要求，污染正确实现。
- 写成 $O(n^2|\texttt{strs}|)$ 的逐目标模拟；上界可到约 $8\times10^9$。

## Follow-up 1：目标串不含问号

**新定义**：给定确定的二进制目标 `target`，判断是否可达。

**变化**：不再需要补全贪心；前缀偏序就是完整充要条件。

<!-- compile:leetcode -->
```cpp
class FixedTargetReachability {
public:
  bool canTransform(const string& s, const string& target) {
    if (s.size() != target.size()) return false;
    int sourceOnes = 0;
    int targetOnes = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      sourceOnes += s[i] == '1';
      targetOnes += target[i] == '1';
      if (targetOnes > sourceOnes) return false;
    }
    return sourceOnes == targetOnes;
  }
};
```

- 时间复杂度：$O(n)$。
- 额外空间复杂度：$O(1)$。

## Follow-up 2：恢复字典序最小的可达补全

**新定义**：不只回答真假；若可行，返回字典序最小的可达确定字符串，否则返回空串。

**思路**：由于 `'0' < '1'`，把必须补的一放到最右侧问号不仅最小化所有前缀一数，也正好得到字典序最小补全。构造后再做前缀检查。

<!-- compile:leetcode -->
```cpp
class LexicographicallySmallestCompletion {
public:
  string construct(const string& s, string pattern) {
    if (s.size() != pattern.size()) return "";
    int sourceOnes = count(s.begin(), s.end(), '1');
    int fixedOnes = count(pattern.begin(), pattern.end(), '1');
    int questions = count(pattern.begin(), pattern.end(), '?');
    int need = sourceOnes - fixedOnes;
    if (need < 0 || need > questions) return "";
    for (int i = static_cast<int>(pattern.size()) - 1; i >= 0; --i) {
      if (pattern[i] != '?') continue;
      if (need > 0) {
        pattern[i] = '1';
        --need;
      } else {
        pattern[i] = '0';
      }
    }
    int sourcePrefix = 0;
    int targetPrefix = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      sourcePrefix += s[i] == '1';
      targetPrefix += pattern[i] == '1';
      if (targetPrefix > sourcePrefix) return "";
    }
    return pattern;
  }
};
```

- 时间复杂度：$O(n)$。
- 额外空间复杂度：返回串之外 $O(1)$。

## Follow-up 3：统计所有可达补全

**新定义**：对一个模式串，计算可达补全数量，答案对 $10^9+7$ 取模。

**原贪心为何不够**：最右补一只能给出一个存在性见证，无法统计其他合法选择。

**新思路**：设 `dp[j]` 为处理完当前前缀、填出 $j$ 个一且从未突破源串前缀上界的方案数。固定字符只有一个转移，问号有填零和填一两个转移；每一层删掉 $j>S(i)$ 的状态，最终取 `dp[K]`。

<!-- compile:leetcode -->
```cpp
class ReachableCompletionCounter {
  static constexpr int MOD = 1000000007;
public:
  int countWays(const string& s, const string& pattern) {
    if (s.size() != pattern.size()) return 0;
    int n = static_cast<int>(s.size());
    int totalOnes = count(s.begin(), s.end(), '1');
    vector<int> dp(totalOnes + 1);
    dp[0] = 1;
    int sourcePrefix = 0;
    for (int i = 0; i < n; ++i) {
      sourcePrefix += s[i] == '1';
      vector<int> next(totalOnes + 1);
      for (int ones = 0; ones <= totalOnes; ++ones) {
        if (dp[ones] == 0) continue;
        if (pattern[i] != '1' && ones <= sourcePrefix) {
          next[ones] += dp[ones];
          if (next[ones] >= MOD) next[ones] -= MOD;
        }
        if (pattern[i] != '0' && ones + 1 <= totalOnes && ones + 1 <= sourcePrefix) {
          next[ones + 1] += dp[ones];
          if (next[ones + 1] >= MOD) next[ones + 1] -= MOD;
        }
      }
      dp.swap(next);
    }
    return dp[totalOnes];
  }
};
```

- 时间复杂度：$O(nK)$，其中 $K$ 是源串一的总数。
- 空间复杂度：$O(K)$。

## Follow-up 4：固定目标的最少相邻交换次数

**新定义**：每一步只能把相邻的 `10` 交换成 `01`，求到确定目标的最少步数；不可达返回 $-1$。

**思路**：第 $k$ 个一不能越过其他一，只能从源位置 $p_k$ 走到目标位置 $q_k$。可达要求 $p_k\le q_k$，最少交换次数就是所有一的右移距离之和。

<!-- compile:leetcode -->
```cpp
class MinimumAdjacentSwaps {
public:
  long long minimumSwaps(const string& s, const string& target) {
    if (s.size() != target.size()) return -1;
    vector<int> sourcePos;
    vector<int> targetPos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') sourcePos.push_back(i);
      if (target[i] == '1') targetPos.push_back(i);
    }
    if (sourcePos.size() != targetPos.size()) return -1;
    long long answer = 0;
    for (int i = 0; i < static_cast<int>(sourcePos.size()); ++i) {
      if (sourcePos[i] > targetPos[i]) return -1;
      answer += targetPos[i] - sourcePos[i];
    }
    return answer;
  }
};
```

- 时间复杂度：$O(n)$。
- 空间复杂度：$O(K)$；也可用两个扫描指针降到 $O(1)$。

## Follow-up 5：输出一条实际操作序列

**新定义**：先取字典序最小的可达补全，再输出一组相邻 `10 -> 01` 交换下标作为证书。

**思路**：得到目标中各个一的位置后，从最右边的一开始移动。右侧的一先就位，后续移动不会跨越它，也不会破坏已完成位置。

<!-- compile:leetcode -->
```cpp
class TransformationWitness {
  string buildTarget(const string& s, string pattern) {
    int sourceOnes = count(s.begin(), s.end(), '1');
    int fixedOnes = count(pattern.begin(), pattern.end(), '1');
    int questions = count(pattern.begin(), pattern.end(), '?');
    int need = sourceOnes - fixedOnes;
    if (need < 0 || need > questions) return "";
    for (int i = static_cast<int>(pattern.size()) - 1; i >= 0; --i) {
      if (pattern[i] != '?') continue;
      pattern[i] = need > 0 ? '1' : '0';
      if (need > 0) --need;
    }
    int a = 0;
    int b = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      a += s[i] == '1';
      b += pattern[i] == '1';
      if (b > a) return "";
    }
    return pattern;
  }
public:
  vector<pair<int, int>> build(const string& s, const string& pattern) {
    string target = buildTarget(s, pattern);
    if (target.empty() && !s.empty()) return {};
    vector<int> sourcePos;
    vector<int> targetPos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') sourcePos.push_back(i);
      if (target[i] == '1') targetPos.push_back(i);
    }
    string current = s;
    vector<pair<int, int>> operations;
    for (int k = static_cast<int>(sourcePos.size()) - 1; k >= 0; --k) {
      int pos = sourcePos[k];
      while (pos < targetPos[k]) {
        swap(current[pos], current[pos + 1]);
        operations.push_back({pos, pos + 1});
        ++pos;
      }
    }
    return operations;
  }
};
```

- 时间复杂度：$O(n+\text{输出操作数})$。
- 空间复杂度：$O(n+\text{输出操作数})$。
- 输出长度恰好等于最少相邻交换次数。

## Follow-up 6：源串在线翻转，固定目标反复询问

**新定义**：目标串固定且不含问号；源串支持单点 `0/1` 翻转，每次翻转后询问目标是否可达。

**原算法为何不够**：每次重扫全部前缀需要 $O(n)$。

**新思路**：维护

$$
D(i)=S(i)-T(i).
$$

翻转源串位置 `pos` 会让所有 $D(i)$（$i\ge pos$）统一加一或减一，是一次后缀区间加。线段树维护全局最小值，再单独维护总一数；可达当且仅当总数相等且 $\min_i D(i)\ge0$。

<!-- compile:leetcode -->
```cpp
class DynamicReachability {
  int n;
  int sourceOnes;
  int targetOnes;
  string source;
  vector<int> minimum;
  vector<int> lazy;
  void build(int node, int left, int right, const vector<int>& diff) {
    if (left == right) {
      minimum[node] = diff[left];
      return;
    }
    int mid = left + (right - left) / 2;
    build(node * 2, left, mid, diff);
    build(node * 2 + 1, mid + 1, right, diff);
    minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1]);
  }
  void apply(int node, int delta) {
    minimum[node] += delta;
    lazy[node] += delta;
  }
  void push(int node) {
    if (lazy[node] == 0) return;
    apply(node * 2, lazy[node]);
    apply(node * 2 + 1, lazy[node]);
    lazy[node] = 0;
  }
  void add(int node, int left, int right, int queryLeft, int queryRight, int delta) {
    if (queryLeft <= left && right <= queryRight) {
      apply(node, delta);
      return;
    }
    push(node);
    int mid = left + (right - left) / 2;
    if (queryLeft <= mid) add(node * 2, left, mid, queryLeft, queryRight, delta);
    if (queryRight > mid) add(node * 2 + 1, mid + 1, right, queryLeft, queryRight, delta);
    minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1]);
  }
public:
  DynamicReachability(string s, const string& target)
      : n(static_cast<int>(s.size())), sourceOnes(0), targetOnes(0), source(std::move(s)),
        minimum(4 * max(1, n)), lazy(4 * max(1, n)) {
    vector<int> diff(n);
    int a = 0;
    int b = 0;
    for (int i = 0; i < n; ++i) {
      a += source[i] == '1';
      b += target[i] == '1';
      diff[i] = a - b;
    }
    sourceOnes = a;
    targetOnes = b;
    if (n > 0) build(1, 0, n - 1, diff);
  }
  void flip(int pos) {
    int delta = source[pos] == '0' ? 1 : -1;
    source[pos] = source[pos] == '0' ? '1' : '0';
    sourceOnes += delta;
    add(1, 0, n - 1, pos, n - 1, delta);
  }
  bool canTransform() const {
    return sourceOnes == targetOnes && (n == 0 || minimum[1] >= 0);
  }
};
```

- 构建时间：$O(n)$。
- 单次翻转与查询：$O(\log n)$ 与 $O(1)$。
- 空间复杂度：$O(n)$。

## Follow-up 7：允许升序或降序排序子序列

**新定义**：每次可以自行选择把子序列按非递减或非递增顺序排序。

**变化**：现在既能把 `10` 变成 `01`，也能把 `01` 变成 `10`，所以任意两个不同字符都能交换。前缀偏序不再存在；只需目标能够补成与源串一的总数相同。

<!-- compile:leetcode -->
```cpp
class BidirectionalSubsequenceSort {
public:
  vector<bool> transformStr(const string& s, const vector<string>& patterns) {
    int sourceOnes = count(s.begin(), s.end(), '1');
    vector<bool> answer;
    answer.reserve(patterns.size());
    for (const string& pattern : patterns) {
      int fixedOnes = count(pattern.begin(), pattern.end(), '1');
      int questions = count(pattern.begin(), pattern.end(), '?');
      answer.push_back(fixedOnes <= sourceOnes && sourceOnes <= fixedOnes + questions);
    }
    return answer;
  }
};
```

- 时间复杂度：$O(n|\texttt{patterns}|)$，与输入规模同阶。
- 额外空间复杂度：除返回值外 $O(1)$。

## 可复现验证

- 抽取本文全部 C++ 代码块，统一包入 C++23 标准头文件环境，使用 Apple Clang 以 `-std=c++23 -Wall -Wextra -Werror -fsyntax-only` 逐块编译。
- 检查所有代码块：不存在制表符；每级缩进恰为两个 ASCII 空格；代码块内部没有空行。
- 穷举 $1\le n\le8$ 的全部二进制源串和全部三进制模式串（`0/1/?`），用“枚举补全 + BFS 枚举合法交换”的暴力 oracle 与最优算法逐项比较。
- 另对固定目标判定、字典序最小补全、补全计数、最少交换次数、操作证书和双向排序变种做独立穷举校验。
- 真实命令、样本总数与 SHA-256 记录在同目录验证报告中；只有实际通过的结果才写作 PASS。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/)
- [力扣第 511 场周赛](https://leetcode.cn/contest/weekly-contest-511/)
- [力扣官方赛后讨论与 5 分标注](https://leetcode.cn/discuss/post/3998508/di-511-chang-li-kou-zhou-sai-by-leetcode-4cwf/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/transform-binary-string-using-subsequence-sort/)
- [对应知识专题](../../basics/prefix-sums-and-difference.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-30-lc14/">← [力扣 Top 30] LC 14 最长公共前缀 简单</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-c/">[codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence →</a>
</nav>
