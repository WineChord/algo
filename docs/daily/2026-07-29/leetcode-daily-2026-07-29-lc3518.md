---
title: "[力扣每日一题] 2026-07-29｜LC 3518 最小回文排列 II"
---

# [力扣每日一题] 2026-07-29｜LC 3518 最小回文排列 II

<p class="daily-archive-kicker">2026-07-29 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../strings/palindrome-rearrangements.md">进入知识专题</a></p>

## 官方原始信息

- 日期：2026-07-29（Asia/Shanghai）
- 题号：LC 3518
- 官方中文标题：最小回文排列 II
- 官方难度：困难
- ZeroTracer 社区估算竞赛分：2375（抓取于 2026-07-29；不是力扣官方难度）
- 官方链接：<https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/?envType=daily-question&envId=2026-07-29>

### 原始题意

给定一个保证为回文串的字符串 `s` 和整数 `k`。把 `s` 的字符任意重排，取所有互不相同且仍为回文的排列，按字典序排序，返回第 `k` 小者；若不同回文排列不足 `k` 个，返回空字符串。产生相同结果的不同重排方式只算一个排列。


### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string smallestPalindrome(string s, int k);
};
```

### 全部官方样例

样例 1：

```text
输入：s = "abba", k = 2
输出："baab"
```

两个不同回文排列依次为 `abba`、`baab`。

样例 2：

```text
输入：s = "aa", k = 2
输出：""
```

只有一个不同回文排列。

样例 3：

```text
输入：s = "bacab", k = 1
输出："abcba"
```

不同回文排列为 `abcba`、`bacab`，第一个是 `abcba`。

### 全部约束

- $1\le |s|\le 10^4$。
- `s` 只含小写英文字母。
- 保证 `s` 是回文串。
- $1\le k\le 10^6$。

## 最优结论

一个回文排列完全由左半串决定：每个字符在左半出现原频次的一半，奇数频次字符固定放在中点，右半是左半的逆序。因此问题等价为：

> 求一个多重集合的第 `k` 小不同排列。

从左到右构造左半。尝试把字符 `c` 放在当前位置，计算剩余多重集合的不同排列数；若该数小于 `k`，跳过整段并令 `k` 减去该数，否则选择 `c`。组合数只需判断到 `k`，统一截断为 `k`，从而避免大整数溢出。

- 时间复杂度：$O(26^2\cdot n\cdot \log k)$ 的保守上界；由于计数达到 $k\le10^6$ 后立即停止，实际接近 $O(26n\log k)$。
- 额外空间复杂度：$O(26+n)$。
- 推荐记忆：回文排列降维成“半串多重集排列”，再做按块跳过的字典序 unranking。

## 约束与观察

左半长度最多为 5000，而排列数可能远超 64 位。直接计算阶乘会溢出；但决策只关心某个分支的方案数是否至少为当前 `k`，且 `k` 不超过 $10^6$。因此每个组合数和乘积都可以在达到 `k` 时截断。

若剩余频次为 $c_0,c_1,\ldots,c_{25}$，长度为 $m$，不同排列数为

$$
\frac{m!}{\prod_{i=0}^{25}c_i!}.
$$

可以按字符依次并入：已并入 `used` 个元素，再并入 `c` 个相同字符时，有 $\binom{used+c}{c}$ 种插入位置。所有二项式的乘积正好等于上述多项式系数。

## 解法递进

### 解法一：枚举所有不同半串排列

把半串字符排序，用 `next_permutation` 依次生成不同排列；第 `k` 个存在时镜像构造答案。正确但最坏要生成 $k$ 个长度 5000 的排列，达到 $O(k n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string smallestPalindrome(string s, int k) {
    array<int, 26> count{};
    for (char ch : s) {
      ++count[ch - 'a'];
    }
    string half;
    char middle = '\0';
    for (int ch = 0; ch < 26; ++ch) {
      half.append(count[ch] / 2, static_cast<char>('a' + ch));
      if (count[ch] % 2 == 1) {
        middle = static_cast<char>('a' + ch);
      }
    }
    do {
      if (--k == 0) {
        string right = half;
        reverse(right.begin(), right.end());
        return half + (middle == '\0' ? "" : string(1, middle)) + right;
      }
    } while (next_permutation(half.begin(), half.end()));
    return "";
  }
};
```

### 解法二：按首字符分块并用截断组合数计数

每个候选首字符对应一个连续字典序区间。用多重集排列数直接跳过整块，避免实际生成块内字符串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int combinationCapped(int n, int r, int limit) {
    r = min(r, n - r);
    long long value = 1;
    for (int i = 1; i <= r; ++i) {
      __int128 next = static_cast<__int128>(value) * (n - r + i);
      next /= i;
      if (next >= limit) {
        return limit;
      }
      value = static_cast<long long>(next);
    }
    return static_cast<int>(value);
  }
  int permutationsCapped(const array<int, 26>& count, int limit) {
    long long total = 1;
    int used = 0;
    for (int amount : count) {
      if (amount == 0) {
        continue;
      }
      int required = static_cast<int>((limit + total - 1) / total);
      int ways = combinationCapped(used + amount, amount, required);
      if (ways >= required) {
        return limit;
      }
      total *= ways;
      used += amount;
    }
    return static_cast<int>(total);
  }
public:
  string smallestPalindrome(string s, int k) {
    array<int, 26> full{};
    for (char ch : s) {
      ++full[ch - 'a'];
    }
    array<int, 26> halfCount{};
    char middle = '\0';
    int halfLength = 0;
    for (int ch = 0; ch < 26; ++ch) {
      halfCount[ch] = full[ch] / 2;
      halfLength += halfCount[ch];
      if (full[ch] % 2 == 1) {
        middle = static_cast<char>('a' + ch);
      }
    }
    if (permutationsCapped(halfCount, k) < k) {
      return "";
    }
    string left;
    left.reserve(halfLength);
    for (int position = 0; position < halfLength; ++position) {
      for (int ch = 0; ch < 26; ++ch) {
        if (halfCount[ch] == 0) {
          continue;
        }
        --halfCount[ch];
        int ways = permutationsCapped(halfCount, k);
        if (ways >= k) {
          left.push_back(static_cast<char>('a' + ch));
          break;
        }
        k -= ways;
        ++halfCount[ch];
      }
    }
    string right = left;
    reverse(right.begin(), right.end());
    if (middle == '\0') {
      return left + right;
    }
    return left + middle + right;
  }
};
```

## 正确性证明

引理 1：每个不同回文排列与一个不同左半串排列一一对应。

证明：回文要求右半由左半唯一确定；偶数频次的一半必须进入左半，若长度为奇数，唯一奇数频次字符必须位于中心。反过来，任意左半多重集排列加固定中心和镜像右半都构成合法且唯一的回文。

引理 2：固定当前前缀并选择候选字符 `c` 后，该分支包含的字符串数量等于剩余频次的多重集排列数。

证明：剩余位置可任意放置剩余字符；去除相同字符导致的重复后，数量正是多项式系数。

引理 3：截断计数不会改变选支决策。

证明：算法只比较 `ways` 与当前 `k`。若真实方案数至少为 `k`，任何返回 `k` 的截断值都会选择该分支；若真实方案数小于 `k`，计数过程不会触及截断，返回精确值并正确扣除。

定理：算法返回第 `k` 小不同回文排列；若不存在则返回空串。

证明：字典序先按当前位置字符分成从 `a` 到 `z` 的连续块。算法用引理 2 的精确或安全截断块大小依次跳过不足以包含第 `k` 个答案的块，并选择第一个包含它的块；随后对下一位置重复。归纳可知最终左半恰为第 `k` 小多重集排列。由引理 1 镜像后得到目标回文。初始总数小于 `k` 时不存在答案。

## 样例手推

`s="bacab"` 的左半多重集是 `{a,b}`，中心是 `c`：

- 首字符尝试 `a`：剩余 `{b}` 只有 1 种，当前 `k=1`，选择 `a`。
- 下一位只能选 `b`，得到左半 `ab`。
- 镜像为 `ab` + `c` + `ba`，答案 `abcba`。

若 `k=2`，首字符 `a` 的块大小 1 被跳过，选择 `b`，得到 `bacab`。

## 边界与易错点

- 输入保证原串是回文，因此奇数频次字符至多一个；仍应从频次自然取得中心。
- 计数必须针对不同排列，分母中的各字符阶乘不能省略。
- 不能先计算巨大阶乘再截断；溢出发生在比较之前。
- 尝试失败的字符要恢复频次，选中字符则保持减少状态。
- `k` 是 1-based。
- 最终提交源码应保持正常多行、两空格缩进；浏览器传输不得压成单行。

## 验证说明

对半串长度不超过 9 的随机多重集合，枚举并去重全部排列作为 oracle，逐个 `k` 比较最优实现；另覆盖 `k` 恰等于总数、`k` 超界、全相同字符、奇偶长度和 `|s|=10^4` 的压力输入。所有发布代码使用 C++23 编译。

## Follow-up 与变种

### 变种一：返回给定回文排列的字典序排名

从左到右扫描目标左半。对所有比当前位置字符小且仍有剩余频次的候选，累加对应分支大小；再消耗目标字符。以下实现把结果截断到 $10^{18}$，时间结构与 unranking 相同。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  long long comb(int n, int r, long long limit) {
    r = min(r, n - r);
    long long result = 1;
    for (int i = 1; i <= r; ++i) {
      __int128 next = static_cast<__int128>(result) * (n - r + i) / i;
      if (next >= limit) {
        return limit;
      }
      result = static_cast<long long>(next);
    }
    return result;
  }
  long long ways(const array<int, 26>& count, long long limit) {
    long long result = 1;
    int used = 0;
    for (int amount : count) {
      if (amount == 0) {
        continue;
      }
      long long cap = (limit + result - 1) / result;
      long long factor = comb(used + amount, amount, cap);
      if (factor >= cap) {
        return limit;
      }
      result *= factor;
      used += amount;
    }
    return result;
  }
public:
  long long palindromeRank(const string& source, const string& target) {
    const long long limit = 1000000000000000000LL;
    array<int, 26> count{};
    for (char ch : source) {
      ++count[ch - 'a'];
    }
    for (int& amount : count) {
      amount /= 2;
    }
    int half = static_cast<int>(source.size()) / 2;
    long long rank = 1;
    for (int position = 0; position < half; ++position) {
      int current = target[position] - 'a';
      for (int ch = 0; ch < current; ++ch) {
        if (count[ch] == 0) {
          continue;
        }
        --count[ch];
        rank = min(limit, rank + ways(count, limit - rank));
        ++count[ch];
      }
      if (count[current] == 0) {
        return -1;
      }
      --count[current];
    }
    return rank;
  }
};
```

### 变种二：`k` 扩大到最多 38 位十进制数

`int` 截断不再够用，但 38 位十进制非负数仍可放入 `unsigned __int128`。组合数继续只计算到当前 `k`，乘法前用除法判断是否会越过截断值，避免溢出。时间结构不变。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  using UInt = unsigned __int128;
  UInt parse(const string& value) {
    UInt result = 0;
    for (char digit : value) {
      result = result * 10 + digit - '0';
    }
    return result;
  }
  UInt combinationCapped(int n, int r, UInt cap) {
    r = min(r, n - r);
    UInt result = 1;
    for (int i = 1; i <= r; ++i) {
      unsigned long long numerator = n - r + i;
      unsigned long long denominator = i;
      unsigned long long common = gcd(numerator, denominator);
      numerator /= common;
      denominator /= common;
      result /= denominator;
      if (result > cap / numerator) {
        return cap;
      }
      result *= numerator;
      if (result >= cap) {
        return cap;
      }
    }
    return result;
  }
  UInt permutationsCapped(const array<int, 26>& count, UInt cap) {
    UInt result = 1;
    int used = 0;
    for (int amount : count) {
      if (amount == 0) {
        continue;
      }
      UInt required = (cap - 1) / result + 1;
      UInt factor = combinationCapped(used + amount, amount, required);
      if (factor >= required) {
        return cap;
      }
      result *= factor;
      used += amount;
    }
    return result;
  }
public:
  string kthPalindrome(string s, string decimalK) {
    array<int, 26> full{};
    for (char ch : s) {
      ++full[ch - 'a'];
    }
    array<int, 26> count{};
    int remaining = 0;
    char middle = '\0';
    for (int ch = 0; ch < 26; ++ch) {
      count[ch] = full[ch] / 2;
      remaining += count[ch];
      if (full[ch] % 2 == 1) {
        middle = static_cast<char>('a' + ch);
      }
    }
    UInt k = parse(decimalK);
    if (permutationsCapped(count, k) < k) {
      return "";
    }
    string left;
    while (remaining > 0) {
      for (int ch = 0; ch < 26; ++ch) {
        if (count[ch] == 0) {
          continue;
        }
        --count[ch];
        UInt block = permutationsCapped(count, k);
        if (block >= k) {
          left.push_back(static_cast<char>('a' + ch));
          --remaining;
          break;
        }
        k -= block;
        ++count[ch];
      }
    }
    string right = left;
    reverse(right.begin(), right.end());
    return left + (middle == '\0' ? "" : string(1, middle)) + right;
  }
};
```

### 变种三：一般多重集合的第 `k` 小排列

去掉“取一半并镜像”步骤，直接对原频次做同样的 unranking。复杂度和截断策略不变。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int comb(int n, int r, int cap) {
    r = min(r, n - r);
    long long value = 1;
    for (int i = 1; i <= r; ++i) {
      value = value * (n - r + i) / i;
      if (value >= cap) {
        return cap;
      }
    }
    return static_cast<int>(value);
  }
  int ways(const array<int, 26>& count, int cap) {
    long long result = 1;
    int used = 0;
    for (int amount : count) {
      if (amount == 0) {
        continue;
      }
      int need = static_cast<int>((cap + result - 1) / result);
      int factor = comb(used + amount, amount, need);
      if (factor >= need) {
        return cap;
      }
      result *= factor;
      used += amount;
    }
    return static_cast<int>(result);
  }
public:
  string kthPermutation(string multisetString, int k) {
    array<int, 26> count{};
    for (char ch : multisetString) {
      ++count[ch - 'a'];
    }
    if (ways(count, k) < k) {
      return "";
    }
    string answer;
    for (int position = 0; position < static_cast<int>(multisetString.size()); ++position) {
      for (int ch = 0; ch < 26; ++ch) {
        if (count[ch] == 0) {
          continue;
        }
        --count[ch];
        int block = ways(count, k);
        if (block >= k) {
          answer.push_back(static_cast<char>('a' + ch));
          break;
        }
        k -= block;
        ++count[ch];
      }
    }
    return answer;
  }
};
```

### 变种四：只求回文排列数量模 $10^9+7$

若奇数频次字符超过一个则答案为 0；否则答案是半串的多项式系数。预处理阶乘与逆阶乘，时间 $O(n+26)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  static constexpr long long mod = 1000000007;
  long long power(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
      if (exponent & 1) {
        result = result * base % mod;
      }
      base = base * base % mod;
      exponent >>= 1;
    }
    return result;
  }
public:
  int countPalindromicPermutations(string s) {
    array<int, 26> count{};
    for (char ch : s) {
      ++count[ch - 'a'];
    }
    int odd = 0;
    int half = 0;
    for (int amount : count) {
      odd += amount % 2;
      half += amount / 2;
    }
    if (odd > 1) {
      return 0;
    }
    vector<long long> factorial(half + 1, 1);
    for (int i = 1; i <= half; ++i) {
      factorial[i] = factorial[i - 1] * i % mod;
    }
    long long answer = factorial[half];
    for (int amount : count) {
      answer = answer * power(factorial[amount / 2], mod - 2) % mod;
    }
    return static_cast<int>(answer);
  }
};
```

## Reference

- [力扣中国 2026-07-29 每日一题](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/?envType=daily-question&envId=2026-07-29)
- [力扣中国官方题面](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/)
- [ZeroTracer 社区估算竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/)
- [对应知识专题](../../strings/palindrome-rearrangements.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="codeforces-2247-d1.md">← [codeforces] CF Round 1111 Div.2 D1 XOR Sorting (Easy Version)</a>
<span class="daily-archive-pager__empty"></span>
</nav>
