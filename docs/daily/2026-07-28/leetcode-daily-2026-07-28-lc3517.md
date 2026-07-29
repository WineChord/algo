---
title: "[力扣每日一题] 2026-07-28｜LC 3517 最小回文排列 I"
---

# [力扣每日一题] 2026-07-28｜LC 3517 最小回文排列 I

<p class="daily-archive-kicker">2026-07-28 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../strings/palindrome-rearrangements/">进入知识专题</a></p>

## 官方原始信息

- 每日题日期：2026-07-28（Asia/Shanghai）
- 题号：LC 3517
- 官方中文标题：最小回文排列 I
- 官方英文标题：Smallest Palindromic Rearrangement I
- 官方难度：中等
- 官方链接：[打开官方页面](https://leetcode.cn/problems/smallest-palindromic-rearrangement-i/?envType=daily-question&envId=2026-07-28)
- 函数签名：`string smallestPalindrome(string s)`
- 竞赛来源：第 445 场周赛 Q2
- 官方竞赛分值：4 分
- ZeroTracer 社区估算竞赛分：1357.0024（数据读取日期：2026-07-28）
- 标签：字符串、计数排序、排序

### 原始题意

给定一个已经是回文串的字符串 `s`。允许重新排列其中全部字符，要求返回所有仍为回文串的排列中字典序最小的一个。

回文串正读与反读相同；排列必须恰好使用原字符串中的每个字符及其原有出现次数。两个等长字符串按第一个不同位置的字符比较字典序。

### 官方样例

1. 输入：`s = "z"`；输出：`"z"`。单字符本身就是唯一且最小的回文排列。
2. 输入：`s = "babab"`；输出：`"abbba"`。频次为 `a:2, b:3`，左半边取 `"ab"`，中心是 `"b"`。
3. 输入：`s = "daccad"`；输出：`"acddca"`。频次为 `a:2, c:2, d:2`，左半边按升序为 `"acd"`。

### 全部约束

- $1 \le |s| \le 10^5$。
- `s` 只包含小写英文字母。
- 保证 `s` 本身是回文串，因此其字符频次一定满足回文排列的奇偶条件。

## 约束推导与核心观察

设字符 $c$ 的出现次数为 $\operatorname{cnt}[c]$，字符串长度为 $n$。

- 回文串的左右两侧必须成对出现，所以左半边恰好含有 $\lfloor n/2 \rfloor$ 个字符，其中字符 $c$ 出现 $\lfloor \operatorname{cnt}[c]/2 \rfloor$ 次。
- 若 $n$ 为奇数，唯一的奇频字符必须放在中心；若 $n$ 为偶数，不存在奇频字符。
- 一个回文排列由“左半边 + 固定中心 + 左半边反转”唯一决定。
- 两个候选回文排列第一次可能不同的位置必在左半边；因此最小化整个回文串等价于把左半边这个多重集合排列成字典序最小的序列。
- 字母表大小固定为 $\sigma=26$。$n$ 可达 $10^5$，阶乘枚举不可行；计数后按字符升序输出可以做到 $O(n+\sigma)$。
- 输出长度为 $n$，所以任何算法的时间复杂度下界都是 $\Omega(n)$。最优解已达到该下界。
- 只做计数和下标运算，不存在整数乘法溢出；计数用 `int` 足够，因为最大为 $10^5$。

## 样例手推

以 `s = "babab"` 为例：

1. 统计得到 $\operatorname{cnt}[a]=2,\operatorname{cnt}[b]=3$。
2. 左半边需要一个 `a` 和一个 `b`，升序得到 `left = "ab"`。
3. `b` 是唯一奇频字符，故 `mid = "b"`。
4. 右半边是 `reverse(left) = "ba"`。
5. 拼接得到 `"ab" + "b" + "ba" = "abbba"`。

如果把左半边换成另一个排列 `"ba"`，得到 `"babab"`；它在第一个字符处已经大于 `"abbba"`，所以不可能更优。

## 解法一：枚举所有不同排列

### 思路

先把 `s` 排序，再用 `next_permutation` 按字典序枚举所有不同排列；第一个满足回文条件的排列就是答案。题目保证至少存在一个。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string smallestPalindrome(string s) {
    sort(s.begin(), s.end());
    do {
      bool ok = true;
      for (int l = 0, r = (int)s.size() - 1; l < r; ++l, --r) {
        if (s[l] != s[r]) {
          ok = false;
          break;
        }
      }
      if (ok) return s;
    } while (next_permutation(s.begin(), s.end()));
    return "";
  }
};
```

### 正确性与复杂度

排序后的排列枚举顺序就是字典序；检查到的第一个回文排列必然是所有回文排列中字典序最小者。若不同排列数为 $U$，时间复杂度为 $O(Un)$，最坏 $U=n!$；额外空间为 $O(1)$。瓶颈是枚举了大量根本不可能满足镜像约束的完整排列。

## 解法二：只构造左半边，再排序

### 优化来源

完整回文只由左半边决定。扫描原串时，每凑齐同一字符的一对，就把一个字符放入左半边；随后仅对长度 $\lfloor n/2 \rfloor$ 的左半边排序，再镜像。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string smallestPalindrome(string s) {
    array<int, 26> cnt{};
    array<int, 26> seen{};
    string left;
    left.reserve(s.size() / 2);
    for (char c : s) {
      int x = c - 'a';
      ++cnt[x];
      if (++seen[x] % 2 == 0) left.push_back(c);
    }
    sort(left.begin(), left.end());
    char mid = 0;
    for (int c = 0; c < 26; ++c) {
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

### 复杂度

时间复杂度为 $O(n\log n)$，额外空间为 $O(n)$。它消除了阶乘枚举，但没有利用字符值域只有 26 的条件。

## 解法三：频次计数直接构造（最佳实用解）

### 算法

1. 统计 26 个小写字母的频次。
2. 从 `a` 到 `z`，向左半边追加 $\lfloor \operatorname{cnt}[c]/2 \rfloor$ 个字符。
3. 记录唯一的奇频字符作为中心。
4. 拼接左半边、中心和左半边的反转。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string smallestPalindrome(string s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    string left;
    left.reserve(s.size() / 2);
    char mid = 0;
    for (int c = 0; c < 26; ++c) {
      left.append(cnt[c] / 2, char('a' + c));
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

### 正确性证明

**引理 1**：任意合法回文排列的左半边中，字符 $c$ 必须恰好出现 $\lfloor \operatorname{cnt}[c]/2 \rfloor$ 次。

证明：除中心外，每个位置必须与镜像位置使用相同字符，因此字符只能成对分配到左右两侧。若字符频次为奇数，多出的唯一一个只能位于中心。故左侧取得每种字符频次的一半向下取整。证毕。

**引理 2**：在固定多重集合的所有排列中，按字符非降序排列得到字典序最小序列。

证明：若某序列存在相邻逆序对 $x>y$，交换二者后，更早位置从 $x$ 变为更小的 $y$，字典序严格下降。不断消除逆序对最终得到非降序序列；任何非非降序序列都可继续变小，因此非降序序列唯一最小。证毕。

**定理**：算法返回字典序最小的回文排列。

证明：由引理 1，算法构造的左半边使用了任意合法答案必须使用的同一多重集合；由引理 2，该左半边是所有可行左半边中字典序最小的。中心字符由奇偶性唯一确定，右半边由镜像唯一确定。两个完整回文的字典序在左半边第一个差异处决定，因此算法所得完整回文也最小。证毕。

### 复杂度

- 时间复杂度：$O(n+\sigma)=O(n)$，其中 $\sigma=26$。
- 额外工作空间：$O(\sigma)=O(1)$；返回字符串占 $O(n)$。

### 推荐记忆

优先记忆“**回文由左半边决定；字典序最小的多重集合排列就是升序排列**”。代码上采用 26 个频次数组直接构造，既达到输出下界，又比显式排序更稳定。

## 边界与易错点

- `s` 长度为 1：左半边为空，唯一字符直接作为中心。
- 全部字符相同：答案仍是原串。
- 偶数长度：不能额外插入中心字符。
- 奇数长度：中心字符由唯一奇频决定，不能为了字典序把它放到左侧。
- 不应直接排序完整字符串；排序结果通常不是回文，例如 `"aabb"` 排序后仍为 `"aabb"`，正确答案是 `"abba"`。
- 构造右半边时必须反转已经排好序的左半边。
- 题目已保证 `s` 为回文串，主解无需额外失败分支；若去掉保证，则必须检查奇频字符数量。

## Follow-up 1：输入不保证存在回文排列

### 新定义

给定任意小写字符串；若能重排成回文，返回字典序最小者，否则返回空串。

### 思路

长度为偶数时奇频字符必须为 0；长度为奇数时必须恰好为 1。统一写成奇频字符数等于 $n\bmod 2$。通过检查后，主算法完全不变。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string smallestPalindromicPermutation(string s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    int odd = 0;
    for (int x : cnt) odd += x % 2;
    if (odd != (int)s.size() % 2) return "";
    string left;
    char mid = 0;
    for (int c = 0; c < 26; ++c) {
      left.append(cnt[c] / 2, char('a' + c));
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

时间复杂度为 $O(n)$，额外工作空间为 $O(1)$。

## Follow-up 2：改求字典序最大的回文排列

### 新定义

仍保证 `s` 可重排成回文，但目标改为字典序最大。

### 思路

中心与字符配额不变；只需把左半边按 `z` 到 `a` 的顺序构造。镜像后即为最大回文。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string largestPalindrome(string s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    string left;
    char mid = 0;
    for (int c = 25; c >= 0; --c) {
      left.append(cnt[c] / 2, char('a' + c));
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

时间复杂度为 $O(n)$，额外工作空间为 $O(1)$。

## Follow-up 3：第 k 小不同回文排列

### 新定义

给定可形成回文的 `s` 和 $1\le k\le 10^6$，返回第 $k$ 个字典序不同的回文排列；不足 $k$ 个时返回空串。它对应 [LC 3518 最小回文排列 II](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/) 的核心模型。

### 原算法为何失效

升序左半边只能得到第 1 个答案。第 $k$ 个答案需要知道固定某个前缀后还有多少个不同排列，从而整段跳过。

### 思路

回文仍只由左半边决定。设剩余半边频次为 $h_c$、剩余长度为 $r$，不同排列数为

$$
\frac{r!}{\prod_c h_c!}.
$$

从小到大尝试当前位置字符。若当前剩余多重集合有 `total` 个不同排列、剩余长度为 $r$，选择字符 $c$ 后的排列数恰好是

$$
\operatorname{ways}_c
=
\operatorname{total}\cdot\frac{h_c}{r}.
$$

若 `ways_c` 至少为 $k$，就固定该字符；否则令 $k$ 减去这一整块并尝试下一个字符。实现同时维护组合数的对数和模 $10^9+7$ 的值：对数明确大于 $4\cdot10^6$ 时，因为 $k\le10^6$，可直接判定该块足够大；否则真实计数远小于模数，模值就是精确整数。这个宽阈值也给浮点误差留下了远大于实际需要的安全间隔。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
  static constexpr long long MOD = 1000000007;
  long long modPow(long long a, long long e) {
    long long r = 1;
    while (e > 0) {
      if (e & 1) r = r * a % MOD;
      a = a * a % MOD;
      e >>= 1;
    }
    return r;
  }
  long long countAfter(const array<int, 26>& cnt, int rem, int chosen,
    const vector<long long>& fact,
    const vector<long long>& invFact) {
    long long ways = fact[rem - 1];
    for (int c = 0; c < 26; ++c) {
      int left = cnt[c] - (c == chosen);
      ways = ways * invFact[left] % MOD;
    }
    return ways;
  }
public:
  string kthSmallestPalindrome(string s, long long k) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    array<int, 26> half{};
    char mid = 0;
    int rem = s.size() / 2;
    for (int c = 0; c < 26; ++c) {
      half[c] = cnt[c] / 2;
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    vector<long long> fact(rem + 1, 1), invFact(rem + 1, 1);
    for (int i = 1; i <= rem; ++i) fact[i] = fact[i - 1] * i % MOD;
    invFact[rem] = modPow(fact[rem], MOD - 2);
    for (int i = rem; i > 0; --i) invFact[i - 1] = invFact[i] * i % MOD;
    long double logTotal = lgammal(rem + 1);
    for (int x : half) logTotal -= lgammal(x + 1);
    const long double large = logl(4000000.0L);
    if (logTotal <= large) {
      long long total = fact[rem];
      for (int x : half) total = total * invFact[x] % MOD;
      if (total < k) return "";
    }
    string left;
    left.reserve(rem);
    while (rem > 0) {
      bool chosen = false;
      for (int c = 0; c < 26; ++c) {
        if (half[c] == 0) continue;
        long double childLog = logTotal + logl(half[c]) - logl(rem);
        long long exact = -1;
        bool enough;
        if (childLog > large) {
          enough = true;
        } else {
          exact = countAfter(half, rem, c, fact, invFact);
          enough = exact >= k;
        }
        if (enough) {
          left.push_back(char('a' + c));
          logTotal = childLog;
          --half[c];
          --rem;
          chosen = true;
          break;
        }
        k -= exact;
      }
      if (!chosen) return "";
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

设半长为 $h=\lfloor n/2\rfloor$。预处理阶乘和逆阶乘为 $O(h)$；每个位置至多尝试 26 个字符，每个需要精确计数的候选扫描 26 类，时间复杂度为 $O(26^2h)=O(n)$（字母表固定），空间复杂度为 $O(h)$。

## Follow-up 4：求严格大于 target 的最小回文排列

### 新定义

给定字符多重集合 `s` 与等长字符串 `target`，返回使用 `s` 全部字符组成、字典序严格大于 `target` 的最小回文；不存在时返回空串。它对应 [LC 3734 大于目标字符串的最小字典序回文排列](https://leetcode.cn/problems/lexicographically-smallest-palindromic-permutation-greater-than-target/) 的模型。

### 思路

先检查 `s` 是否能构成回文。若左半边能逐位匹配 `target` 的前半段，先构造完整回文并直接比较，因为中心或右半边仍可能决定严格大于。否则在第一个无法匹配的位置选择最小的更大字符并把后缀升序填满；若当前位置没有更大字符，就向左回退，恢复已用字符并提升更早的位置。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
  string build(const string& left, char mid) {
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
  string finish(string left, array<int, 26> rem, int c, char mid) {
    left.push_back(char('a' + c));
    --rem[c];
    for (int x = 0; x < 26; ++x) left.append(rem[x], char('a' + x));
    return build(left, mid);
  }
public:
  string smallestPalindromeGreaterThan(string s, string target) {
    if (s.size() != target.size()) return "";
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    int odd = 0;
    char mid = 0;
    array<int, 26> rem{};
    for (int c = 0; c < 26; ++c) {
      odd += cnt[c] % 2;
      rem[c] = cnt[c] / 2;
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    if (odd != (int)s.size() % 2) return "";
    int h = s.size() / 2;
    string left;
    int i = 0;
    while (i < h) {
      int x = target[i] - 'a';
      if (rem[x] == 0) break;
      --rem[x];
      left.push_back(target[i]);
      ++i;
    }
    if (i == h) {
      string sameLeft = build(left, mid);
      if (sameLeft > target) return sameLeft;
      if (next_permutation(left.begin(), left.end())) return build(left, mid);
      return "";
    }
    int need = target[i] - 'a';
    for (int c = need + 1; c < 26; ++c) {
      if (rem[c] > 0) return finish(left, rem, c, mid);
    }
    for (int pos = i - 1; pos >= 0; --pos) {
      int restored = left.back() - 'a';
      left.pop_back();
      ++rem[restored];
      int bound = target[pos] - 'a';
      for (int c = bound + 1; c < 26; ++c) {
        if (rem[c] > 0) return finish(left, rem, c, mid);
      }
    }
    return "";
  }
};
```

每个位置最多扫描 26 个字符，回退时每个位置只处理一次，时间复杂度为 $O(n+\sigma n)=O(n)$，额外空间为 $O(n)$。

## Follow-up 5：统计不同回文排列数

### 新定义

给定任意小写字符串，统计其不同回文排列数，结果对 $10^9+7$ 取模。

### 思路

若奇频条件不成立则答案为 0。否则只需统计左半边多重集合的不同排列：

$$
\operatorname{ans}
=
\frac{h!}{\prod_c (\operatorname{cnt}[c]/2)!}
\pmod {10^9+7},
\qquad h=\left\lfloor\frac n2\right\rfloor.
$$

模数为质数，用费马小定理计算阶乘逆元。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
  static constexpr long long MOD = 1000000007;
  long long modPow(long long a, long long e) {
    long long r = 1;
    while (e > 0) {
      if (e & 1) r = r * a % MOD;
      a = a * a % MOD;
      e >>= 1;
    }
    return r;
  }
public:
  int countPalindromicPermutations(string s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    int odd = 0;
    for (int x : cnt) odd += x % 2;
    if (odd != (int)s.size() % 2) return 0;
    int h = s.size() / 2;
    vector<long long> fact(h + 1, 1);
    for (int i = 1; i <= h; ++i) fact[i] = fact[i - 1] * i % MOD;
    long long ans = fact[h];
    for (int x : cnt) ans = ans * modPow(fact[x / 2], MOD - 2) % MOD;
    return ans;
  }
};
```

时间复杂度为 $O(n+\sigma\log MOD)$，空间复杂度为 $O(n)$；阶乘表也可与多次查询共享。

## Follow-up 6：动态增删字符并查询最小回文

### 新定义

维护一个字符多重集合，支持插入字符、删除一个已有字符，以及查询当前字符是否能组成回文；若能，输出字典序最小回文。

### 思路

维护 26 个频次、总长度和奇频字符数。每次更新只改变一个字符的奇偶性，故为 $O(1)$；查询必须输出长度为 $n$ 的字符串，按频次构造即可，耗时 $O(n+\sigma)$，已经达到输出下界。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class PalindromeMultiset {
  array<int, 26> cnt{};
  int n = 0;
  int odd = 0;
  void change(int x, int delta) {
    odd -= cnt[x] % 2;
    cnt[x] += delta;
    odd += cnt[x] % 2;
    n += delta;
  }
public:
  void add(char c) {
    change(c - 'a', 1);
  }
  bool erase(char c) {
    int x = c - 'a';
    if (cnt[x] == 0) return false;
    change(x, -1);
    return true;
  }
  string smallest() const {
    if (odd != n % 2) return "";
    string left;
    char mid = 0;
    for (int c = 0; c < 26; ++c) {
      left.append(cnt[c] / 2, char('a' + c));
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
};
```

更新时间复杂度为 $O(1)$，查询时间复杂度为 $O(n)$，维护状态空间为 $O(1)$。

## Follow-up 7：变到最小回文所需的最少相邻交换次数

### 新定义

给定任意可重排成回文的字符串 `s`，每次只能交换相邻字符；求把它变成字典序最小回文所需的最少交换次数。

### 思路

先构造唯一目标串 `target`。对每种字符，把目标中的出现位置按升序保存；源串中第 $j$ 次出现的同一字符匹配目标中第 $j$ 次出现的位置，这种同字符的非交叉匹配最优。于是源串变为一个目标下标排列，最少相邻交换次数就是该排列的逆序对数，用树状数组计算。

### 完整 C++

<!-- compile:leetcode -->
```cpp
class Solution {
  struct Fenwick {
    vector<int> bit;
    explicit Fenwick(int n) : bit(n + 1) {}
    void add(int x) {
      for (++x; x < (int)bit.size(); x += x & -x) ++bit[x];
    }
    int sumPrefix(int x) {
      int sum = 0;
      for (; x > 0; x -= x & -x) sum += bit[x];
      return sum;
    }
  };
  string target(string s) {
    array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    int odd = 0;
    char mid = 0;
    string left;
    for (int c = 0; c < 26; ++c) {
      odd += cnt[c] % 2;
      left.append(cnt[c] / 2, char('a' + c));
      if (cnt[c] % 2 == 1) mid = char('a' + c);
    }
    if (odd != (int)s.size() % 2) return "";
    string ans = left;
    if (mid != 0) ans.push_back(mid);
    for (auto it = left.rbegin(); it != left.rend(); ++it) ans.push_back(*it);
    return ans;
  }
public:
  long long minAdjacentSwapsToSmallestPalindrome(string s) {
    string t = target(s);
    if (t.empty() && !s.empty()) return -1;
    vector<vector<int>> pos(26);
    for (int i = 0; i < (int)t.size(); ++i) pos[t[i] - 'a'].push_back(i);
    array<int, 26> used{};
    Fenwick fw(s.size());
    long long inversions = 0;
    for (int i = 0; i < (int)s.size(); ++i) {
      int c = s[i] - 'a';
      int p = pos[c][used[c]++];
      inversions += i - fw.sumPrefix(p + 1);
      fw.add(p);
    }
    return inversions;
  }
};
```

时间复杂度为 $O(n\log n)$，空间复杂度为 $O(n)$。

## 验证说明

- 三种原题解与完整排列暴力 oracle 做小规模随机对拍。
- 第 $k$ 小、严格大于 `target`、计数和最少相邻交换变种分别用不同排列枚举或状态 BFS 做小规模核验。
- 所有代码块按 C++23 独立编译；检查无制表符、无代码块空行，并保持两空格逻辑缩进。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/smallest-palindromic-rearrangement-i/?envType=daily-question&envId=2026-07-28)
- [第 445 场周赛官方讨论与分值](https://leetcode.cn/discuss/post/lxCsvq/)
- [ZeroTracer 社区估算竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/smallest-palindromic-rearrangement-i/)
- [对应知识专题](../../strings/palindrome-rearrangements.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2247-c/">← [codeforces] CF Round 1111 Div.2 C Inversion of a Subsequence</a>
<span class="daily-archive-pager__empty"></span>
</nav>
