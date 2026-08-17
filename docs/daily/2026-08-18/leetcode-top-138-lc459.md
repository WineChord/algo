---
title: "[力扣 Top 138] LC 459 重复的子字符串 简单"
---

# [力扣 Top 138] LC 459 重复的子字符串 简单

<p class="daily-archive-kicker">2026-08-18 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-18 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d2b0d29853539ee7f16ae03a2dcc65474f977b52afedb0820b9ccd857d058761 -->
[力扣 459：重复的子字符串](https://leetcode.cn/problems/repeated-substring-pattern/)

## 官方原始信息

- 高频排名：Top 138。
- 题号：459。
- 官方中文标题：重复的子字符串。
- 官方难度：简单。
- ZeroTracer 社区估算竞赛分：未知；截至 2026-08-18 的公开数据中没有可靠条目。
- 函数签名：`bool repeatedSubstringPattern(string s)`。
- 题意：给定一个非空小写字母字符串，判断它能否由某个更短的非空子串重复若干次得到。

### 全部官方样例

样例 1：

```text
输入：s = "abab"
输出：true
解释：可以由 "ab" 重复两次得到。
```

样例 2：

```text
输入：s = "aba"
输出：false
```

样例 3：

```text
输入：s = "abcabcabcabc"
输出：true
解释：既可以由 "abc" 重复四次得到，也可以由 "abcabc" 重复两次得到。
```

### 全部官方约束

- $1 \le |s| \le 10^4$。
- `s` 只含小写英文字母。

## 约束推导与周期模型

设字符串长度为 $n$，候选重复单元长度为 $p$。若它确实能平铺整个字符串，首先必须有
$p<n$ 且 $p\mid n$；随后每个位置都应满足 $s_i=s_{i\bmod p}$。直接尝试所有 $p$
已经足以通过 $n=10^4$ 的数据，但会重复比较相同前后缀。

KMP 的前缀函数 $\pi_i$ 表示以 $i$ 结尾的前缀中，最长的真前缀与后缀的公共长度。
令 $L=\pi_{n-1}$。若字符串由最短单元重复，则最后一份单元之前的内容同时是前缀和后缀，
候选最短周期为

$$
p=n-L.
$$

只有 $L>0$ 且 $n\bmod p=0$ 时，这个边界才能平铺全串。前缀函数一次扫描即可求出，
时间为 $O(n)$，不会产生整数溢出。

## 样例手推与边界

对 `abab`，前缀函数依次为 $[0,0,1,2]$。于是 $L=2$、$p=4-2=2$，且
$4\bmod2=0$，答案为真。

对 `aba`，前缀函数为 $[0,0,1]$。虽然首尾有长度 1 的公共部分，但候选周期
$p=3-1=2$ 不能整除 3，所以答案为假。这说明“存在非空公共前后缀”本身并不充分。

- 长度为 1：不存在更短的非空重复单元，答案为假。
- 全部字符相同：最短周期为 1，答案为真。
- 有公共前后缀但不能整除长度：必须返回假，例如 `aba`。
- 存在多个周期：只需判断最短候选周期；样例 3 的 3 和 6 都可行。
- 质数长度：除非所有字符相同且周期为 1，否则答案为假。

## 解法一：枚举重复单元长度

枚举所有严格小于 $n$ 且整除 $n$ 的长度 $p$，逐字符检查 $s_i=s_{i\bmod p}$。
它直接覆盖所有可能的平铺方式，因此是正确的暴力解，也适合作为随机对拍的 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool repeatedSubstringPattern(string s) {
    int n = s.size();
    for (int period = 1; period < n; ++period) {
      if (n % period != 0) continue;
      bool valid = true;
      for (int i = period; i < n; ++i) {
        if (s[i] != s[i % period]) {
          valid = false;
          break;
        }
      }
      if (valid) return true;
    }
    return false;
  }
};
```

时间复杂度最坏为 $O(n^2)$，额外空间为 $O(1)$。瓶颈是不同候选周期会重复验证大量
已经匹配过的前后缀。

## 从暴力到线性算法

枚举法关心的是“把一个前缀向右平移后，能连续匹配多远”。Z 函数可以直接维护这些匹配
长度；KMP 前缀函数则把所有失配后的候选边界压缩成一条失配跳转链。两者都消除了重新从头
比较的工作，均可做到 $O(n)$。

进一步观察，完整重复串的最后 $n-p$ 个字符恰好等于最前面的 $n-p$ 个字符。因此最长公共
真前后缀已经把最短候选周期唯一确定为 $n-\pi_{n-1}$，最后只需检查整除关系，不必枚举
所有边界。

## 最佳实用解：KMP 前缀函数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool repeatedSubstringPattern(string s) {
    int n = s.size();
    vector<int> prefix(n);
    for (int i = 1; i < n; ++i) {
      int matched = prefix[i - 1];
      while (matched > 0 && s[i] != s[matched]) {
        matched = prefix[matched - 1];
      }
      if (s[i] == s[matched]) ++matched;
      prefix[i] = matched;
    }
    int border = prefix[n - 1];
    int period = n - border;
    return border > 0 && n % period == 0;
  }
};
```

时间复杂度为 $O(n)$，额外空间为 $O(n)$。只需要最终答案时可以讨论压缩状态，但标准前缀
函数最清楚、最稳定，也便于扩展到后续变种。

### 正确性证明

若算法返回真，则 $L=\pi_{n-1}>0$，长度为 $L$ 的前缀等于后缀，并且
$p=n-L$ 整除 $n$。公共前后缀关系意味着对每个 $i\ge p$ 都有 $s_i=s_{i-p}$；沿着
步长 $p$ 反复回退，每个字符都等于前 $p$ 个字符中的对应位置，因此全串由长度 $p$ 的
前缀重复得到。

反之，若字符串由长度 $q<n$ 的单元重复，则前 $n-q$ 个字符与后 $n-q$ 个字符相同，
所以 $L\ge n-q$，候选 $p=n-L\le q$。字符串的边界周期性质保证该最小候选周期也是
字符串周期，并且所有完整重复单元使 $p\mid n$。因此算法必定返回真。

## 同阶方案：Z 函数

Z 函数的 $z_i$ 表示从位置 $i$ 开始与整个字符串前缀相同的最长长度。只要存在
$i<n$，满足 $n\bmod i=0$ 且 $z_i=n-i$，长度 $i$ 就能平铺全串。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool repeatedSubstringPattern(string s) {
    int n = s.size();
    vector<int> z(n);
    for (int i = 1, left = 0, right = 0; i < n; ++i) {
      if (i <= right) z[i] = min(right - i + 1, z[i - left]);
      while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
      if (i + z[i] - 1 > right) {
        left = i;
        right = i + z[i] - 1;
      }
    }
    for (int period = 1; period < n; ++period) {
      if (n % period == 0 && z[period] == n - period) return true;
    }
    return false;
  }
};
```

它同样是 $O(n)$ 时间、$O(n)$ 空间。Z 函数更直观地表达“从周期起点向后匹配”，KMP
则只看最终边界即可下结论，代码更短，也更容易顺带求最短重复单元，因此优先记忆 KMP。

## 易错点

- 忘记要求重复至少两次，导致把整个字符串本身当成重复单元。
- 只判断 `prefix[n - 1] > 0`，漏掉候选周期必须整除长度。
- 在失配时把 `matched` 简单减一，而不是跳到 `prefix[matched - 1]`。
- 把“周期长度”误写成最长边界长度；正确候选是 `n - border`。
- 使用 `(s + s).find(s)` 技巧时忘记去掉首尾字符，造成任何字符串都匹配自身。

## 验证说明

三份主方案均以 GNU++23 编译。除全部官方样例和上述边界外，还对小写字母表上的短字符串
穷举，并用枚举周期的暴力解与 KMP、Z 函数逐项比较；另对更长随机串做差分，结果一致。

## 变种一：返回最短重复单元

新定义：若字符串可重复构成，返回最短单元；否则返回空串。KMP 已经给出候选周期
$p=n-\pi_{n-1}$，所以原算法直接成立。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = s.size();
  vector<int> prefix(n);
  for (int i = 1; i < n; ++i) {
    int matched = prefix[i - 1];
    while (matched > 0 && s[i] != s[matched]) matched = prefix[matched - 1];
    if (s[i] == s[matched]) ++matched;
    prefix[i] = matched;
  }
  int period = n - prefix[n - 1];
  if (prefix[n - 1] == 0 || n % period != 0) cout << "NONE\n";
  else cout << s.substr(0, period) << '\n';
  return 0;
}
```

时间复杂度 $O(n)$，额外空间 $O(n)$。

## 变种二：列出所有可行重复单元长度

新定义：输出所有满足 $p<n$ 且前缀 `s[0..p-1]` 能平铺全串的 $p$。逐个枚举 $n$ 的
真因数并检查即可；因数个数很少，整体比较量为 $O(n\tau(n))$，额外空间 $O(1)$（不计
答案）。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = s.size();
  vector<int> answer;
  for (int period = 1; period < n; ++period) {
    if (n % period != 0) continue;
    bool valid = true;
    for (int i = period; i < n; ++i) {
      if (s[i] != s[i % period]) {
        valid = false;
        break;
      }
    }
    if (valid) answer.push_back(period);
  }
  cout << answer.size() << '\n';
  for (int period : answer) cout << period << ' ';
  cout << '\n';
  return 0;
}
```

## 变种三：至多修改一个字符后变成重复串

新定义：允许替换至多一个位置，判断能否得到重复串。原 KMP 边界会随修改整体变化，不能
直接套用。枚举 $n$ 的每个真因数 $p$，把下标按模 $p$ 分组；每组保留出现次数最多的字符，
其余字符都要修改。若总修改数不超过 1 即可。复杂度为 $O(n\tau(n))$，空间为 $O(p)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = s.size();
  for (int period = 1; period < n; ++period) {
    if (n % period != 0) continue;
    int changes = 0;
    for (int residue = 0; residue < period; ++residue) {
      array<int, 26> count{};
      int groupSize = 0;
      for (int i = residue; i < n; i += period) {
        ++count[s[i] - 'a'];
        ++groupSize;
      }
      changes += groupSize - *max_element(count.begin(), count.end());
    }
    if (changes <= 1) {
      cout << "YES\n";
      return 0;
    }
  }
  cout << "NO\n";
  return 0;
}
```

## 变种四：字符在线追加，逐前缀报告

新定义：字符依次到达，每追加一个字符就判断当前整个前缀能否重复构成。前缀函数可以在线
延长；新状态只沿旧失配链回退，总摊还时间 $O(n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string stream;
  cin >> stream;
  string current;
  vector<int> prefix;
  for (char ch : stream) {
    int matched = prefix.empty() ? 0 : prefix.back();
    while (matched > 0 && ch != current[matched]) matched = prefix[matched - 1];
    if (!current.empty() && ch == current[matched]) ++matched;
    current.push_back(ch);
    prefix.push_back(matched);
    int length = current.size();
    int period = length - prefix.back();
    bool repeated = prefix.back() > 0 && length % period == 0;
    cout << (repeated ? "YES" : "NO") << '\n';
  }
  return 0;
}
```

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/repeated-substring-pattern/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/repeated-substring-pattern/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc227-b/">← [atcoder] ARC227 B Know Your Place</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-515-q1-lc4024/">[力扣竞赛] 第 515 场周赛 Q1 LC 4024 最近的可用无人机 简单 →</a>
</nav>
