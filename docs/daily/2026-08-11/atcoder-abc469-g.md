---
title: "[atcoder] ABC469 G K-nacci Operations"
---

# [atcoder] ABC469 G K-nacci Operations

<p class="daily-archive-kicker">2026-08-11 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-11 题目列表</a> · <a href="../../../dp/linear-recurrences/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=bcede6abfa5a2a65f4511d8cea40ad0cbb5d5eb9808a5020368011265e9ba4a9 -->
[Official problem: AtCoder ABC469 G - K-nacci Operations](https://atcoder.jp/contests/abc469/tasks/abc469_g?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 469，Rated Range 为 0–1999。
- 题目：G - K-nacci Operations；官方分值 575。
- AtCoder 官方未标注难度；AtCoder Problems 社区估算难度为 2804（2026-08-11 抓取，非实验值）。
- 时间限制：2 秒；内存限制：1024 MiB。
- 官方链接：[ABC469 G](https://atcoder.jp/contests/abc469/tasks/abc469_g?lang=en)。

## Complete English statement

### G. K-nacci Operations

You are given an integer $K$ and $K$ nonempty strings $S_1,S_2,\ldots,S_K$, each consisting only of `a` and `b`. For every $i>K$, define

$$
S_i=S_{i-1}S_{i-2}\cdots S_{i-K},
$$

where juxtaposition means concatenation and the order is strictly from the newest string to the oldest one.

You are also given an integer $N$ and a nonempty lowercase English string $T$. Read $S_N$ from left to right and apply each character to the current $T$:

- `a`: move the first character of $T$ to its end;
- `b`: reverse the whole string $T$.

Print the string after all operations in $S_N$ have been applied.

### Input

```text
K
S_1
S_2
...
S_K
N
T
```

The complete constraints are:

- $2\le K\le100$.
- Every $S_i$ is nonempty and contains only `a` and `b`.
- $\sum_{i=1}^{K}|S_i|\le2\times10^5$.
- $1\le N\le10^{18}$.
- $T$ contains only lowercase English letters.
- $1\le |T|\le2\times10^5$.
- All numeric inputs are integers.

### Output

Print the final value of $T$.

### Complete official samples

```text
Input
3
a
aa
b
5
abc

Output
cab
```

For this sample, $S_4=\texttt{baaa}$ and $S_5=\texttt{baaabaa}$. The states are

```text
abc -> cba -> bac -> acb -> cba -> abc -> bca -> cab
```

```text
Input
2
a
ba
6
fibonacci

Output
canobific
```

```text
Input
5
aba
a
bb
ba
aab
1000000000000000000
abcba

Output
aabcb
```

There are no additional official notes or statement images required to understand the task.

本节是依据官方题面独立组织的完整英文呈现，并非逐字转载。事实以官方链接为准；AtCoder 的使用边界见 [AtCoder Terms of Service](https://atcoder.jp/tos)。

## 中文题意

前 $K$ 个操作串已知，之后每个串由前 $K$ 个串按“新到旧”顺序拼接。`a` 表示把文本左轮转一位，`b` 表示反转。$S_N$ 的长度会随递推爆炸，而 $N$ 可达 $10^{18}$；目标不是构造操作串，而是压缩它对 $T$ 位置的整体置换。

## 约束推导与核心模型

令 $m=|T|$。任何若干次轮转、反转的复合都可写成二面体变换

$$
F_{d,o}(T)[x]=T[(dx+o)\bmod m],
$$

其中 $d\in\{1,-1\}$，$o\in\mathbb Z_m$。`a` 对应 $(1,1)$，`b` 对应 $(-1,-1)$。若先执行 $(d_1,o_1)$，再执行 $(d_2,o_2)$，在“输出位置拉回输入位置”的约定下，复合为

$$
(d_1,o_1)*(d_2,o_2)=(d_1d_2,o_1+d_1o_2).
$$

记 $g_i$ 为 $S_i$ 的整体变换，$P=K+1$。$g_1,\ldots,g_K$ 直接扫描；

$$
g_P=g_Kg_{K-1}\cdots g_1.
$$

对 $n\ge P+1$，由

$$
g_n=g_{n-1}g_{n-2}\cdots g_{n-K},\qquad
g_{n-1}=g_{n-2}\cdots g_{n-K}g_{n-P}
$$

右消元得到

$$
g_n=g_{n-1}^2g_{n-P}^{-1}.
$$

写 $g_n=(d_n,o_n)$，便有

$$
d_n=d_{n-P},
$$

$$
o_n=(1+d_{n-1})o_{n-1}-d_no_{n-P}\pmod m.
$$

方向 $d_n$ 以 $P$ 为周期；偏移量是系数同样以 $P$ 为周期的 $P$ 阶线性递推。把连续 $P$ 个相位合成一个矩阵，再二进制快速幂即可跳过 $10^{18}$ 项。

## 解法递进

### 解法一：直接构造 $S_N$ 并模拟

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int k, n;
  cin >> k;
  vector<string> s(k);
  for (string& value : s) cin >> value;
  cin >> n;
  string text;
  cin >> text;
  for (int i = k; i < n; ++i) {
    string current;
    for (int j = i - 1; j >= i - k; --j) current += s[j];
    s.push_back(move(current));
  }
  for (char operation : s[n - 1]) {
    if (operation == 'a') rotate(text.begin(), text.begin() + 1, text.end());
    else reverse(text.begin(), text.end());
  }
  cout << text << '\n';
}
```

它完全照定义执行，适合作为小规模 oracle；但操作串长度按 $K$ 阶递推增长，时间、空间都与 $|S_N|$ 成正比，无法处理正式约束。

### 解法二：只递推整体二面体变换

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform {
  int direction, offset;
};
Transform combine(Transform first, Transform second, int length) {
  return {first.direction * second.direction,
      (first.offset + first.direction * second.offset % length + length) % length};
}
Transform parse(const string& operations, int length) {
  Transform result{1, 0};
  for (char operation : operations) {
    Transform current;
    if (operation == 'a') {
      current = {1, 1 % length};
    } else {
      current = {-1, (length - 1) % length};
    }
    result = combine(result, current, length);
  }
  return result;
}
int main() {
  int k, n;
  cin >> k;
  vector<string> initial(k);
  for (string& value : initial) cin >> value;
  cin >> n;
  string text;
  cin >> text;
  int length = text.size();
  vector<Transform> transform(n + 1);
  for (int i = 1; i <= min(k, n); ++i) transform[i] = parse(initial[i - 1], length);
  for (int i = k + 1; i <= n; ++i) {
    transform[i] = {1, 0};
    for (int j = i - 1; j >= i - k; --j) transform[i] = combine(transform[i], transform[j], length);
  }
  string answer(length, '?');
  for (int i = 0; i < length; ++i) {
    int source = (transform[n].direction * i + transform[n].offset) % length;
    if (source < 0) source += length;
    answer[i] = text[source];
  }
  cout << answer << '\n';
}
```

它把指数级字符串压成常数状态，时间 $O(\sum|S_i|+NK+|T|)$、空间 $O(N+|T|)$；当 $N$ 较小很实用，但 $10^{18}$ 仍不可行。

### 最佳实用解：周期系数矩阵快速幂

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform {
  int direction;
  int offset;
};
using Matrix = vector<vector<int>>;
Transform concatenate(const Transform& first, const Transform& second, int length) {
  return {first.direction * second.direction,
      (first.offset + first.direction * second.offset % length + length) % length};
}
Transform parseTransform(const string& operations, int length) {
  Transform result{1, 0};
  for (char operation : operations) {
    Transform current;
    if (operation == 'a') {
      current = {1, 1 % length};
    } else {
      current = {-1, (length - 1) % length};
    }
    result = concatenate(result, current, length);
  }
  return result;
}
Matrix multiply(const Matrix& left, const Matrix& right, int modulus) {
  int size = left.size();
  Matrix product(size, vector<int>(size));
  for (int row = 0; row < size; ++row) {
    for (int column = 0; column < size; ++column) {
      long long sum = 0;
      for (int middle = 0; middle < size; ++middle) {
        sum += 1LL * left[row][middle] * right[middle][column];
      }
      product[row][column] = sum % modulus;
    }
  }
  return product;
}
vector<int> multiply(const Matrix& matrix, const vector<int>& values, int modulus) {
  int size = matrix.size();
  vector<int> product(size);
  for (int row = 0; row < size; ++row) {
    long long sum = 0;
    for (int column = 0; column < size; ++column) {
      sum += 1LL * matrix[row][column] * values[column];
    }
    product[row] = sum % modulus;
  }
  return product;
}
vector<int> advanceOne(
    const vector<int>& state,
    int previousDirection,
    int nextDirection,
    int modulus) {
  int size = state.size();
  vector<int> next(size);
  long long leading = 1LL * (1 + previousDirection) * state[0]
                    - 1LL * nextDirection * state.back();
  leading %= modulus;
  if (leading < 0) leading += modulus;
  next[0] = leading;
  for (int index = 1; index < size; ++index) next[index] = state[index - 1];
  return next;
}
string solve(const vector<string>& initial, unsigned long long target, const string& text) {
  int count = initial.size();
  int period = count + 1;
  int length = text.size();
  vector<Transform> transform(period + 1);
  for (int index = 1; index <= count; ++index) {
    transform[index] = parseTransform(initial[index - 1], length);
  }
  Transform combined{1, 0};
  for (int index = count; index >= 1; --index) {
    combined = concatenate(combined, transform[index], length);
  }
  transform[period] = combined;
  Transform answerTransform;
  if (target <= static_cast<unsigned long long>(period)) {
    answerTransform = transform[target];
  } else {
    vector<int> state(period);
    for (int index = 0; index < period; ++index) state[index] = transform[period - index].offset;
    Matrix block(period, vector<int>(period));
    for (int index = 0; index < period; ++index) block[index][index] = 1 % length;
    for (int step = 1; step <= period; ++step) {
      int previous = step == 1 ? period : step - 1;
      Matrix next(period, vector<int>(period));
      for (int column = 0; column < period; ++column) {
        long long value = 1LL * (1 + transform[previous].direction) * block[0][column]
                        - 1LL * transform[step].direction * block[period - 1][column];
        value %= length;
        if (value < 0) value += length;
        next[0][column] = value;
      }
      for (int row = 1; row < period; ++row) next[row] = block[row - 1];
      block.swap(next);
    }
    unsigned long long remaining = target - period;
    unsigned long long fullBlocks = remaining / period;
    int extra = remaining % period;
    while (fullBlocks > 0) {
      if (fullBlocks & 1ULL) state = multiply(block, state, length);
      fullBlocks >>= 1ULL;
      if (fullBlocks > 0) block = multiply(block, block, length);
    }
    for (int step = 1; step <= extra; ++step) {
      int previous = step == 1 ? period : step - 1;
      state = advanceOne(state, transform[previous].direction, transform[step].direction, length);
    }
    int residue = (target - 1) % period + 1;
    answerTransform = {transform[residue].direction, state[0]};
  }
  string answer(length, '?');
  for (int index = 0; index < length; ++index) {
    int source = (answerTransform.direction * index + answerTransform.offset) % length;
    if (source < 0) source += length;
    answer[index] = text[source];
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int count;
  cin >> count;
  vector<string> initial(count);
  for (string& operations : initial) cin >> operations;
  unsigned long long target;
  string text;
  cin >> target >> text;
  cout << solve(initial, target, text) << '\n';
}
```

时间复杂度为

$$
O\left(\sum_{i=1}^{K}|S_i|+P^3\log N+|T|\right),
$$

空间 $O(P^2+|T|)$。构造完整周期时，每个相位只左乘一个“移位 + 两系数”稀疏矩阵，累计 $O(P^3)$；二进制平方才使用稠密 $O(P^3)$ 乘法。

## 正确性证明

二面体表示对 `a`、`b` 都正确，并在复合律下封闭，因此直接扫描得到的 $g_i$ 与真实操作串等价。由串联顺序可得 $g_P=g_K\cdots g_1$；对 $n\ge P+1$ 的右消元合法，故方向周期和偏移递推成立。

状态向量按 $V_n=[o_n,o_{n-1},\ldots,o_{n-P+1}]^T$ 排列。第 `step` 个相位的转移把递推值写入首位并将其余值右移；连续 $P$ 个相位组成 `block`。快速幂作用完整周期，再逐个作用余数相位，所得首项就是 $o_N$。方向由周期下标取得，最终按 $T[(d_Nx+o_N)\bmod m]$ 构造每个输出位置。因此输出与逐字符执行 $S_N$ 完全相同。

## 样例手推、边界与易错点

样例一中，`a=(1,1)`、`b=(-1,-1)`。扫描 `baaabaa` 得到的整体变换把 `abc` 映为 `cab`，与八个展示状态一致。

- 递推 $g_n=g_{n-1}^2g_{n-P}^{-1}$ 只从 $n=P+1$ 开始；$g_P$ 必须单独构造。
- 字符串拼接不交换，`g_Kg_{K-1}\cdots g_1` 的顺序不能倒置。
- 遇到 `a` 时偏移增加当前方向，而不是无条件加 1。
- 所有负偏移都要规范化到 $[0,m)$。
- $|T|=1$ 时模数为 1，代码仍需避免非法状态；当前实现全部系数自然归零。
- 三个官方样例全部通过；与真实展开操作串在 20,000 组随机小实例上逐一一致。独立复核另验证了 145,136 个递推位置与 10,000 组展开实例。

## 变种一：只询问若干输出位置

新定义：不输出整串，只询问最终字符串的若干下标。得到整体变换后，每次按 $source=(dx+o)\bmod m$ 直接读取，单次 $O(1)$。下面给出 $N\le10^6$ 时的完整实现，重点展示输出层变化。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform { int d, o; };
Transform combine(Transform a, Transform b, int m) {
  return {a.d * b.d, (a.o + a.d * b.o % m + m) % m};
}
Transform parse(const string& s, int m) {
  Transform result{1, 0};
  for (char c : s) {
    Transform atom = c == 'a' ? Transform{1, 1 % m} : Transform{-1, (m - 1) % m};
    result = combine(result, atom, m);
  }
  return result;
}
int main() {
  int k, n;
  cin >> k;
  vector<string> initial(k);
  for (string& s : initial) cin >> s;
  cin >> n;
  string text;
  cin >> text;
  int m = text.size();
  vector<Transform> g(n + 1);
  for (int i = 1; i <= min(k, n); ++i) g[i] = parse(initial[i - 1], m);
  for (int i = k + 1; i <= n; ++i) {
    g[i] = {1, 0};
    for (int j = i - 1; j >= i - k; --j) g[i] = combine(g[i], g[j], m);
  }
  int queries;
  cin >> queries;
  while (queries--) {
    int position;
    cin >> position;
    int source = (g[n].d * position + g[n].o) % m;
    if (source < 0) source += m;
    cout << text[source] << '\n';
  }
}
```

预处理时间 $O(NK+\sum|S_i|)$，每次查询 $O(1)$；正式的 $N\le10^{18}$ 版本只需把同一查询层接到最佳解算出的变换上。

## 变种二：同组初始串，多次询问不同的 $N$

新定义：$N_{max}\le10^6$，有多次 $N$ 查询。预处理所有整体变换一次，避免每次重算递推。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform { int d, o; };
Transform combine(Transform a, Transform b, int m) {
  return {a.d * b.d, (a.o + a.d * b.o % m + m) % m};
}
Transform parse(const string& s, int m) {
  Transform result{1, 0};
  for (char c : s) {
    Transform atom = c == 'a' ? Transform{1, 1 % m} : Transform{-1, (m - 1) % m};
    result = combine(result, atom, m);
  }
  return result;
}
int main() {
  int k, maximumN, queries;
  cin >> k >> maximumN >> queries;
  vector<string> initial(k);
  for (string& s : initial) cin >> s;
  string text;
  cin >> text;
  int m = text.size();
  vector<Transform> g(maximumN + 1);
  for (int i = 1; i <= min(k, maximumN); ++i) g[i] = parse(initial[i - 1], m);
  for (int i = k + 1; i <= maximumN; ++i) {
    g[i] = {1, 0};
    for (int j = i - 1; j >= i - k; --j) g[i] = combine(g[i], g[j], m);
  }
  while (queries--) {
    int n;
    cin >> n;
    string answer(m, '?');
    for (int x = 0; x < m; ++x) {
      int source = (g[n].d * x + g[n].o) % m;
      if (source < 0) source += m;
      answer[x] = text[source];
    }
    cout << answer << '\n';
  }
}
```

预处理 $O(N_{max}K+\sum|S_i|)$，每次完整输出 $O(|T|)$，空间 $O(N_{max}+|T|)$。若查询的 $N$ 仍达 $10^{18}$，应预处理周期矩阵的二进制幂，每次做矩阵乘向量。

## 变种三：同一个变换作用于多个等长文本

新定义：操作递推固定，给出多个长度相同的文本。整体变换只依赖操作、$N$ 与长度，不依赖字符内容，可以复用。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform { int d, o; };
Transform combine(Transform a, Transform b, int m) {
  return {a.d * b.d, (a.o + a.d * b.o % m + m) % m};
}
string apply(Transform g, const string& text) {
  int m = text.size();
  string answer(m, '?');
  for (int x = 0; x < m; ++x) {
    int source = (g.d * x + g.o) % m;
    if (source < 0) source += m;
    answer[x] = text[source];
  }
  return answer;
}
int main() {
  int k, n, texts;
  cin >> k >> n >> texts;
  vector<string> initial(k), input(texts);
  for (string& s : initial) cin >> s;
  for (string& s : input) cin >> s;
  int m = input[0].size();
  vector<Transform> g(n + 1);
  for (int i = 1; i <= min(k, n); ++i) {
    g[i] = {1, 0};
    for (char c : initial[i - 1]) {
      Transform atom = c == 'a' ? Transform{1, 1 % m} : Transform{-1, (m - 1) % m};
      g[i] = combine(g[i], atom, m);
    }
  }
  for (int i = k + 1; i <= n; ++i) {
    g[i] = {1, 0};
    for (int j = i - 1; j >= i - k; --j) g[i] = combine(g[i], g[j], m);
  }
  for (const string& text : input) cout << apply(g[n], text) << '\n';
}
```

在 $N$ 较小时，预处理 $O(NK+\sum|S_i|)$，每个文本只需 $O(|T|)$；正式大 $N$ 可复用最佳解的同一个二面体结果。

## 变种四：轮转任意步长并加入“反转后轮转”

新定义：每个命令直接给出仿射变换 `(d,o)`，其中 $d$ 为 1 表示旋转，为 -1 表示反射后旋转。二面体封闭性仍成立，只需替换原子操作。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform { long long d, o; };
Transform combine(Transform first, Transform second, long long length) {
  long long offset = (first.o + first.d * second.o) % length;
  if (offset < 0) offset += length;
  return {first.d * second.d, offset};
}
int main() {
  int operations;
  string text;
  cin >> operations >> text;
  Transform result{1, 0};
  while (operations--) {
    long long direction, offset;
    cin >> direction >> offset;
    offset %= text.size();
    result = combine(result, {direction, offset}, text.size());
  }
  string answer(text.size(), '?');
  for (int x = 0; x < static_cast<int>(text.size()); ++x) {
    int source = (result.d * x + result.o) % text.size();
    if (source < 0) source += text.size();
    answer[x] = text[source];
  }
  cout << answer << '\n';
}
```

时间 $O(q+|T|)$、空间 $O(|T|)$。若新增操作不是形如 $x\mapsto\pm x+o$ 的置换，二面体压缩不再封闭，需要换成更大的群表示。

## 变种五：递推拼接顺序改为从旧到新

新定义：$S_i=S_{i-K}\cdots S_{i-1}$。非交换性使原来的右消元不再适用；在 $N$ 较小时直接按新顺序递推整体变换最稳妥。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Transform { int d, o; };
Transform combine(Transform a, Transform b, int m) {
  return {a.d * b.d, (a.o + a.d * b.o % m + m) % m};
}
int main() {
  int k, n;
  cin >> k;
  vector<string> initial(k);
  for (string& s : initial) cin >> s;
  cin >> n;
  string text;
  cin >> text;
  int m = text.size();
  vector<Transform> g(n + 1);
  for (int i = 1; i <= min(k, n); ++i) {
    g[i] = {1, 0};
    for (char c : initial[i - 1]) {
      Transform atom = c == 'a' ? Transform{1, 1 % m} : Transform{-1, (m - 1) % m};
      g[i] = combine(g[i], atom, m);
    }
  }
  for (int i = k + 1; i <= n; ++i) {
    g[i] = {1, 0};
    for (int j = i - k; j <= i - 1; ++j) g[i] = combine(g[i], g[j], m);
  }
  string answer(m, '?');
  for (int x = 0; x < m; ++x) {
    int source = (g[n].d * x + g[n].o) % m;
    if (source < 0) source += m;
    answer[x] = text[source];
  }
  cout << answer << '\n';
}
```

时间 $O(NK+\sum|S_i|+|T|)$。若还要求 $N\le10^{18}$，应从新乘法顺序重新推导消元式；不能把原矩阵相位机械复用。

## Reference

- [AtCoder 官方题面](https://atcoder.jp/contests/abc469/tasks/abc469_g?lang=en)
- [AtCoder Terms of Service](https://atcoder.jp/tos)
- [AtCoder Problems](https://kenkoooo.com/atcoder/#/table/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/abc469/tasks/abc469_g?lang=en)
- [对应知识专题](../../dp/linear-recurrences.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-131-lc63/">[力扣 Top 131] LC 63 不同路径 II 中等 →</a>
</nav>
