---
title: "[codeforces] CF Round 1116 Div.1 B / Div.2 D A Ribbon for Tomorrow"
---

# [codeforces] CF Round 1116 Div.1 B / Div.2 D A Ribbon for Tomorrow

<p class="daily-archive-kicker">2026-08-15 · 第 4/5 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-15 题目列表</a> · <a href="../../../math/combinatorial-counting/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=48ea84d121cd162474348bc79de69705728e1a247c1b79b27844b5e344b762ff -->
[Official problem: Codeforces 2256D - A Ribbon for Tomorrow](https://codeforces.com/contest/2256/problem/D)

## 官方来源与元数据

- 比赛：Codeforces Round 1116。
- 官方别名：[Div.1 B（2255B）](https://codeforces.com/contest/2255/problem/B) / [Div.2 D（2256D）](https://codeforces.com/contest/2256/problem/D)。
- 官方英文标题：A Ribbon for Tomorrow。
- Div.1 B 官方分值：1000；官方 rating：1600；官方标签：`combinatorics`、`math`。
- Div.2 D 官方分值：2000；官方 rating：1600；官方标签：`math`。
- 时间限制：2 秒；内存限制：256 MB。
- [Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967)。

两个官方页面属于同一 Round、开始时间相同，题名、题面、输入输出、约束与样例逐字符一致，因此按同一道题处理。题面没有图片。

## Complete English statement

Nephren arranges $n$ glass beads in a row. Every bead is white or black. The row is represented by a binary string $s$ of length $n$: `0` denotes a white bead and `1` denotes a black bead.

In one operation, choose positions $l,r$ satisfying

$$
1\le l\le r\le n,
$$

such that $s_l=s_r$ in the current string, then reverse the contiguous substring $s_ls_{l+1}\ldots s_r$. The operation may be performed any number of times, including zero.

Determine the number of distinct binary strings reachable from the initial string. Print the answer modulo $998244353$.

A binary string contains only `0` and `1`. Reversing a string writes its characters in the opposite order. For example, from `00110`, choosing $l=1,r=5$ is legal because both endpoints are `0`, and produces `01100`.

### Input

The first line contains the number of test cases $t$. Each test case consists of an integer $n$ and a binary string $s$ of length $n$.

```text
t
n_1
s_1
n_2
s_2
...
n_t
s_t
```

### Output

For each test case, print the number of distinct reachable strings modulo $998244353$.

### Constraints

- $1\le t\le10^4$.
- $1\le n\le10^6$.
- $s$ is a binary string of length $n$.
- The sum of $n$ over all test cases does not exceed $10^6$.

### Complete official sample

Input:

```text
4
5
00110
6
001010
5
01010
6
111111
```

Output:

```text
2
3
1
1
```

### Complete official note

- In the first test case, exactly `00110` and `01100` are reachable; reversing the whole string produces the second one.
- In the second test case, exactly `001010`, `010010` (reverse the first four characters), and `010100` (reverse the whole string) are reachable.
- In the third test case, every legal interval is already a palindrome, so the string never changes.
- In the fourth test case, every character is `1`, so reversing any interval leaves the string unchanged.

## 中文题意解释

每次只能反转首尾字符相同的连续区间，问经过任意多次操作后能出现多少种不同二进制串。直接搜索操作图是指数级；真正需要找到的是操作保持哪些量，以及这些不变量是否也足以刻画可达集合。

把字符串写成若干个极长同色段，即 run。例如 `0011100` 的 run 长度是 2、3、2。操作不会改变 0 与 1 的总数，也不会改变两种颜色各自的 run 数；反过来，同色相邻 run 之间可以逐个搬运字符，所以 run 长度可以在保持正数的前提下任意重分配。

## 约束推导与暴力搜索

### 解法一：在字符串状态图上 BFS

对每个当前串枚举所有端点相等的区间，反转后作为新状态入队。它准确得到全部可达串，适合小规模 oracle。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string start;
  cin >> start;
  queue<string> pending;
  unordered_set<string> reached;
  reached.insert(start);
  pending.push(start);
  while (!pending.empty()) {
    string current = pending.front();
    pending.pop();
    int n = static_cast<int>(current.size());
    for (int left = 0; left < n; ++left) {
      for (int right = left; right < n; ++right) {
        if (current[left] != current[right]) continue;
        string next = current;
        reverse(next.begin() + left, next.begin() + right + 1);
        if (reached.insert(next).second) pending.push(next);
      }
    }
  }
  cout << reached.size() << '\n';
}
```

可达状态至多 $2^n$，每个状态枚举 $O(n^2)$ 个区间并用 $O(n)$ 复制反转，最坏时间 $O(2^nn^3)$、空间 $O(2^nn)$；$n=10^6$ 时不可行。

## 不变量与充分性

### 必要性：两种颜色的 run 数不变

反转区间内部的相邻异色边只是顺序颠倒，数量不变。区间外若存在左边界，反转前后与外部字符相邻的都是相同端点字符；右边界同理。因此全串相邻字符变化次数不变，首字符与尾字符也不变，0 与 1 的 run 数随之保持。反转还显然保持两种字符总数。

### 充分性：相邻同色 run 间可搬运一个字符

考虑局部形态

$$
x^Ay^Bx^C,\qquad x\ne y,\quad A,B,C\ge1.
$$

若 $A\ge2$，反转首尾都是 $x$ 的子串 $x^2y^Bx$，会产生

$$
x^2y^Bx\longrightarrow xy^Bx^2,
$$

即把一个 $x$ 从左 run 搬到右 run，而中间的 $y$-run 长度不变。逆操作可向左搬运。沿同色 run 链反复做单位搬运，便能把一种正整数长度组成变为任意另一种；调整 0-run 时 1-run 长度不变，因此两种颜色可以先后独立调整。

所以可达串恰好由四个量确定：0 的总数、1 的总数、0-run 数与 1-run 数。

## 计数公式

把 $c$ 个相同字符分进 $r$ 个非空且有序的 run，等价于把 $c$ 写成 $r$ 个正整数之和，方案数为插板法

$$
\binom{c-1}{r-1}.
$$

约定 $c=r=0$ 时方案数为 1。设 0/1 的数量为 $z,o$，run 数为 $r_0,r_1$，答案为

$$
\binom{z-1}{r_0-1}\binom{o-1}{r_1-1}\pmod{998244353}.
$$

预处理到最大 $n$ 的阶乘与逆阶乘，即可常数时间求每个组合数。

## 最佳实用解

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
long long power(long long value, int exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * value % MOD;
    value = value * value % MOD;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testsCount;
  cin >> testsCount;
  vector<pair<int, string>> tests(testsCount);
  int maximum = 0;
  for (auto& [n, s] : tests) {
    cin >> n >> s;
    maximum = max(maximum, n);
  }
  vector<long long> factorial(maximum + 1, 1);
  vector<long long> inverseFactorial(maximum + 1, 1);
  for (int i = 1; i <= maximum; ++i) {
    factorial[i] = factorial[i - 1] * i % MOD;
  }
  inverseFactorial[maximum] = power(factorial[maximum], MOD - 2);
  for (int i = maximum; i > 0; --i) {
    inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
  }
  auto combination = [&](int n, int k) -> long long {
    if (n < 0 || k < 0 || k > n) return 0;
    return factorial[n] * inverseFactorial[k] % MOD *
        inverseFactorial[n - k] % MOD;
  };
  auto compositions = [&](int count, int runs) -> long long {
    if (runs == 0) return count == 0;
    return combination(count - 1, runs - 1);
  };
  for (const auto& [n, s] : tests) {
    int zeros = 0;
    int zeroRuns = 0;
    int oneRuns = 0;
    for (int i = 0; i < n; ++i) {
      zeros += s[i] == '0';
      if (i == 0 || s[i] != s[i - 1]) {
        if (s[i] == '0') ++zeroRuns;
        else ++oneRuns;
      }
    }
    int ones = n - zeros;
    cout << compositions(zeros, zeroRuns) *
            compositions(ones, oneRuns) % MOD << '\n';
  }
}
```

预处理 $O(N)$，其中 $N$ 为最大测试长度；扫描总时间 $O(\sum n)$，空间 $O(N)$。全部乘法在模数平方以内，64 位整数安全。

## 正确性证明

前述必要性证明任何操作都保持两色字符总数和各自 run 数，所以每个可达串都被公式计入的四元组约束。

前述单位搬运证明，在 run 数固定时，同一颜色的任意正整数组成都能互相转化，且调整一种颜色不改变另一种颜色的 run 长。因此公式计入的任意两组 run 长度都对应一个可达串。

每个目标串的首色与交替 run 颜色顺序由原串固定，两组 run 长度唯一确定目标串；不同组成不会重复计数。两个颜色的选择相互独立，故乘积恰是不同可达串总数。

## 样例手推与边界

`001010 = 00|1|0|1|0` 有 4 个 0、2 个 1；0-run 数为 3，1-run 数为 2。因此答案是

$$
\binom{3}{2}\binom{1}{1}=3.
$$

对应 0-run 长度组成 `(2,1,1)`、`(1,2,1)`、`(1,1,2)`，即官方列出的三个字符串。

- 全部同色：唯一 run，组合数为 1，答案为 1。
- 严格交替：每个 run 长度都被迫为 1，答案为 1。
- 某颜色不存在：使用 `ways(0,0)=1`，不能访问负下标阶乘。
- $n=1$：只有原串一种状态。
- 总长度达到 $10^6$：阶乘表和字符串存储均在线性内存范围内。

## 方案比较与推荐

BFS 给出可达集合的定义级验证；不变量只证明“至多”，必须再用单位搬运证明“至少”。最终组合公式将指数状态图压缩为两个独立的正整数组成计数。竞赛中优先记“先找 run 不变量，再证明相邻 run 可局部转移”，不要在只得到必要条件后直接套组合数。

## 易错点

- 只统计 0/1 数量不够；首尾与 run 数同样受操作约束。
- 不变量证明后还必须证明任意合法 run 组成确实可达。
- 区间反转合法性看当前串的两个端点字符是否相同。
- 某颜色完全缺失时，空的 run 组成应贡献 1。
- 组合数上界来自总长度 $10^6$，应一次预处理并复用。
- Div.1 与 Div.2 页面 points、tags 不同，不能把合并后的并集冒充单页字段。

## 可复现验证

六份完整程序均以 GNU++23 严格警告编译。主公式与 BFS 状态图对拍覆盖 $n\le10$ 的全部 2046 个二进制串；可达性判定穷举 $n\le8$ 的 87380 个有序串对；字典序构造覆盖 2046 个起点；有界 run 计数覆盖 18434 组；在线翻转与子串询问各完成 4000 组固定种子随机核验，且 $n=10^6$ 冒烟测试通过。

## 变种一：判定目标串是否可达

两个同长串可达当且仅当首字符、尾字符、1 的数量与相邻变化次数全部相同；这些量等价地确定两色 run 数与字符总数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
tuple<char, char, int, int> signature(const string& s) {
  int ones = count(s.begin(), s.end(), '1');
  int transitions = 0;
  for (int i = 1; i < static_cast<int>(s.size()); ++i) {
    transitions += s[i] != s[i - 1];
  }
  return {s.front(), s.back(), ones, transitions};
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    string source, target;
    cin >> n >> source >> target;
    bool validLength = static_cast<int>(source.size()) == n &&
        static_cast<int>(target.size()) == n;
    cout << (validLength && signature(source) == signature(target) ?
        "YES\n" : "NO\n");
  }
}
```

每组时间 $O(n)$，额外空间 $O(1)$。

## 变种二：构造字典序最小可达串

把多余的 0 全放到第一个 0-run，把多余的 1 全放到最后一个 1-run，其余 run 长均为 1。交换论证表明这会尽早放置 0 并尽量推迟 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int tests;
  cin >> tests;
  while (tests--) {
    int n;
    string s;
    cin >> n >> s;
    int zeros = count(s.begin(), s.end(), '0');
    int zeroRuns = 0;
    int oneRuns = 0;
    for (int i = 0; i < n; ++i) {
      if (i == 0 || s[i] != s[i - 1]) {
        if (s[i] == '0') ++zeroRuns;
        else ++oneRuns;
      }
    }
    int ones = n - zeros;
    vector<int> zeroLength(zeroRuns, 1);
    vector<int> oneLength(oneRuns, 1);
    if (zeroRuns > 0) zeroLength[0] += zeros - zeroRuns;
    if (oneRuns > 0) oneLength.back() += ones - oneRuns;
    int zeroIndex = 0;
    int oneIndex = 0;
    char color = s[0];
    string answer;
    answer.reserve(n);
    for (int run = 0; run < zeroRuns + oneRuns; ++run) {
      int length = color == '0' ? zeroLength[zeroIndex++] :
          oneLength[oneIndex++];
      answer.append(length, color);
      color = color == '0' ? '1' : '0';
    }
    cout << answer << '\n';
  }
}
```

时间 $O(n)$，run 长数组空间 $O(n)$。原题只计数，不要求构造代表串。

## 变种三：在线翻转一个位置后询问答案

维护字符数量与两色 run 数。翻转位置 `p` 只会改变 `p` 和 `p+1` 是否为 run 起点；先删除旧贡献，翻位，再加入新贡献即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
long long power(long long value, int exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * value % MOD;
    value = value * value % MOD;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  string s;
  cin >> n >> queries >> s;
  vector<long long> factorial(n + 1, 1), inverseFactorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i % MOD;
  inverseFactorial[n] = power(factorial[n], MOD - 2);
  for (int i = n; i > 0; --i) {
    inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
  }
  auto combination = [&](int a, int b) -> long long {
    if (a < 0 || b < 0 || b > a) return 0;
    return factorial[a] * inverseFactorial[b] % MOD *
        inverseFactorial[a - b] % MOD;
  };
  auto ways = [&](int countValue, int runs) -> long long {
    if (runs == 0) return countValue == 0;
    return combination(countValue - 1, runs - 1);
  };
  int zeros = count(s.begin(), s.end(), '0');
  int zeroRuns = 0;
  int oneRuns = 0;
  for (int i = 0; i < n; ++i) {
    if (i == 0 || s[i] != s[i - 1]) {
      if (s[i] == '0') ++zeroRuns;
      else ++oneRuns;
    }
  }
  auto eraseStart = [&](int index) {
    if (index < 0 || index >= n) return;
    if (index == 0 || s[index] != s[index - 1]) {
      if (s[index] == '0') --zeroRuns;
      else --oneRuns;
    }
  };
  auto addStart = [&](int index) {
    if (index < 0 || index >= n) return;
    if (index == 0 || s[index] != s[index - 1]) {
      if (s[index] == '0') ++zeroRuns;
      else ++oneRuns;
    }
  };
  while (queries--) {
    int position;
    cin >> position;
    --position;
    eraseStart(position);
    eraseStart(position + 1);
    if (s[position] == '0') {
      s[position] = '1';
      --zeros;
    } else {
      s[position] = '0';
      ++zeros;
    }
    addStart(position);
    addStart(position + 1);
    int ones = n - zeros;
    cout << ways(zeros, zeroRuns) * ways(ones, oneRuns) % MOD << '\n';
  }
}
```

预处理 $O(n)$，每次翻转与回答 $O(1)$，空间 $O(n)$。

## 变种四：固定字符串上的多次子串询问

每次给 `[l,r]`，只允许在该子串内操作，问子串可达串数。前缀统计 0、`10` 边与 `01` 边，即可在 $O(1)$ 得到字符数与两色 run 数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
long long power(long long value, int exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * value % MOD;
    value = value * value % MOD;
    exponent >>= 1;
  }
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queries;
  string s;
  cin >> n >> queries >> s;
  vector<long long> factorial(n + 1, 1), inverseFactorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) factorial[i] = factorial[i - 1] * i % MOD;
  inverseFactorial[n] = power(factorial[n], MOD - 2);
  for (int i = n; i > 0; --i) {
    inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
  }
  auto combination = [&](int a, int b) -> long long {
    if (a < 0 || b < 0 || b > a) return 0;
    return factorial[a] * inverseFactorial[b] % MOD *
        inverseFactorial[a - b] % MOD;
  };
  auto ways = [&](int countValue, int runs) -> long long {
    if (runs == 0) return countValue == 0;
    return combination(countValue - 1, runs - 1);
  };
  vector<int> prefixZero(n + 1), prefix10(n), prefix01(n);
  for (int i = 0; i < n; ++i) {
    prefixZero[i + 1] = prefixZero[i] + (s[i] == '0');
  }
  for (int i = 1; i < n; ++i) {
    prefix10[i] = prefix10[i - 1] +
                  (s[i - 1] == '1' && s[i] == '0');
    prefix01[i] = prefix01[i - 1] +
                  (s[i - 1] == '0' && s[i] == '1');
  }
  while (queries--) {
    int left, right;
    cin >> left >> right;
    --left;
    --right;
    int zeros = prefixZero[right + 1] - prefixZero[left];
    int ones = right - left + 1 - zeros;
    int zeroRuns = (s[left] == '0') + prefix10[right] - prefix10[left];
    int oneRuns = (s[left] == '1') + prefix01[right] - prefix01[left];
    cout << ways(zeros, zeroRuns) * ways(ones, oneRuns) % MOD << '\n';
  }
}
```

预处理 $O(n)$，每次询问 $O(1)$，空间 $O(n)$。

## 变种五：限制每个 run 长度至多为 $L$

正整数拆分增加上界 $1\le x_i\le L$。令 $y_i=x_i-1$，用容斥得到

$$
\operatorname{bounded}(c,r,L)=
\sum_{j=0}^{r}(-1)^j\binom rj\binom{c-jL-1}{r-1}.
$$

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
long long power(long long value, int exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * value % MOD;
    value = value * value % MOD;
    exponent >>= 1;
  }
  return result;
}
struct Test {
  int n;
  int limit;
  string s;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testsCount;
  cin >> testsCount;
  vector<Test> tests(testsCount);
  int maximum = 0;
  for (auto& [n, limit, s] : tests) {
    cin >> n >> limit >> s;
    maximum = max(maximum, n);
  }
  vector<long long> factorial(maximum + 1, 1);
  vector<long long> inverseFactorial(maximum + 1, 1);
  for (int i = 1; i <= maximum; ++i) {
    factorial[i] = factorial[i - 1] * i % MOD;
  }
  inverseFactorial[maximum] = power(factorial[maximum], MOD - 2);
  for (int i = maximum; i > 0; --i) {
    inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
  }
  auto combination = [&](int n, int k) -> long long {
    if (n < 0 || k < 0 || k > n) return 0;
    return factorial[n] * inverseFactorial[k] % MOD *
        inverseFactorial[n - k] % MOD;
  };
  auto bounded = [&](int countValue, int runs, int limit) -> long long {
    if (runs == 0) return countValue == 0;
    long long answer = 0;
    for (int chosen = 0; chosen <= runs; ++chosen) {
      long long top = 1LL * countValue - 1LL * chosen * limit - 1;
      if (top < runs - 1) break;
      long long term = combination(runs, chosen) *
          combination(static_cast<int>(top), runs - 1) % MOD;
      answer += chosen & 1 ? -term : term;
    }
    answer %= MOD;
    if (answer < 0) answer += MOD;
    return answer;
  };
  for (const auto& [n, limit, s] : tests) {
    int zeros = 0;
    int zeroRuns = 0;
    int oneRuns = 0;
    for (int i = 0; i < n; ++i) {
      zeros += s[i] == '0';
      if (i == 0 || s[i] != s[i - 1]) {
        if (s[i] == '0') ++zeroRuns;
        else ++oneRuns;
      }
    }
    int ones = n - zeros;
    cout << bounded(zeros, zeroRuns, limit) *
            bounded(ones, oneRuns, limit) % MOD << '\n';
  }
}
```

每组时间 $O(r_0+r_1)$，全局阶乘空间 $O(N)$。原题没有 run 上界，普通插板公式就是该容斥的无限上界特例。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2256/problem/D)
- [对应知识专题](../../math/combinatorial-counting.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-514-q2-lc4015/">← [力扣竞赛] 第 514 场周赛 Q2 LC 4015 树的加权和 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-15-lc3702/">[力扣每日一题] 2026-08-15｜LC 3702 按位异或非零的最长子序列 →</a>
</nav>
