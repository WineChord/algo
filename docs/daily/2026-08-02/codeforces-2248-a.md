---
title: "[codeforces] CF Round 1113 Div.2 A You Delete, I Delete"
---

# [codeforces] CF Round 1113 Div.2 A You Delete, I Delete

<p class="daily-archive-kicker">2026-08-02 · 第 13/14 题 · Codeforces</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=523f1b6c918edfc2a0be811dbbad9db72604ba90076e2eaefc49ce7a9536f843 -->
## 官方来源与元数据

- 来源：Codeforces。
- 比赛：Codeforces Round 1113 (Div. 2)。
- Contest ID：2248。
- 题号与标题：Div.2 A - You Delete, I Delete。
- 官方 points：500。
- 官方 rating：未知（2026-08-02 核对时官方 API 未提供）。
- 官方 tags：未知（2026-08-02 核对时官方 API 未提供）。
- 时间限制：1 秒。
- 内存限制：256 MB。
- 官方题面：[Codeforces 2248A - You Delete, I Delete](https://codeforces.com/contest/2248/problem/A)。
- 材料许可：[Codeforces materials usage license v0.1](https://codeforces.com/blog/entry/967?mobile=false)。

下方英文题面层按 Codeforces 材料许可在公开、非判题用途下呈现，并保留来源、官方直达链接与许可说明。这里不复制隐藏测试、生成器、checker、validator 或其他未公开判题材料。

## Complete English statement

### A. You Delete, I Delete

- **Time limit per test:** 1 second
- **Memory limit per test:** 256 megabytes
- **Input:** standard input
- **Output:** standard output
- **Official task:** [Codeforces 2248A](https://codeforces.com/contest/2248/problem/A)

Alice and Bob are given a binary string $s$ of length $n$. The string contains at least one `0` and at least one `1`.

They perform exactly one operation each, in this order:

1. Alice chooses one occurrence of `0` in $s$ and deletes it.
2. Bob chooses one occurrence of `1` in the resulting string and deletes it.

Alice wants the final string to be lexicographically as large as possible. Bob wants the final string to be lexicographically as small as possible. Determine the final string when both players act optimally.

A binary string contains only `0` and `1`. For two distinct binary strings of the same length, the lexicographically smaller one is the string with the smaller digit at the first position where they differ.

### Input

The first line contains the number of test cases $t$:

$$
1\le t\le100.
$$

Each test case consists of one binary string $s$ of length $n$:

$$
3\le n\le100.
$$

Every $s$ contains at least one `0` and at least one `1`.

### Complete Constraints

For every test file and test case, all of the following conditions hold:

$$
1\le t\le100,\qquad 3\le n\le100.
$$

Each $s$ is a binary string of length $n$ and contains at least one `0` and at least one `1`.

### Output

For each test case, output the final string produced by optimal play.

### Official Sample

```text
Input
4
101
11001
0010
0101010000010100100101
```

```text
Output
1
101
00
01010000010100100101
```

### Official Sample Explanation

- For `101`, Alice must delete its only `0`. Bob may delete either `1`; the result is `1`.
- For `11001`, Alice may delete either `0`. Bob optimally deletes one of the first two `1` characters; the result is `101`.
- For `0010`, Alice may delete any `0`. Bob then deletes the only `1`; the result is `00`.
- The official statement gives no additional explanation for the fourth test case and contains no required image.

## 中文题意

Alice 先删掉一个 `0`，Bob 再从新串中删掉一个 `1`。Alice 最大化最终二进制串的字典序，Bob 最小化；两人都最优时输出终局。

## 约束推导与关键引理

$n\le100$ 允许枚举，但每组枚举 Alice 的位置、Bob 的位置并构造字符串需要 $O(n^3)$。更重要的结构是“删除一个指定字符后的字典序最优位置”。

比较删除同一种字符的两个位置可得到支配策略：

- Alice 删除原串最左边的 `0`，所得串最大。若两个候选 `0` 之间全是 `0`，结果相同；否则删除更左的 `0` 会让中间第一个 `1` 更早出现，结果严格更大。
- Bob 删除当前串最左边的 `1`，所得串最小。若两个候选 `1` 之间全是 `1`，结果相同；否则删除更左的 `1` 会让中间第一个 `0` 更早出现，结果严格更小。

Alice 删除 `0` 不改变所有 `1` 的相对次序，因此 Bob 无论面对 Alice 的哪种选择，最优动作始终是删掉原串最左的 `1`。对称地，Bob 删除 `1` 不改变 `0` 的相对次序。故双方的支配策略可以独立确定，也可以交换执行次序。

实现上，删除最左 `0` 与“删除第一个 `01` 中的 `0`，不存在则删最后一个 `0`”产生同一字符串，因为最左的一段连续 `0` 删除其中任意一个结果相同。Bob 的 `10` 规则与删除最左 `1` 同理。

最终长度固定为 $n-2$，不涉及整数运算或溢出。

## 解法递进

### 解法一：完整极大极小枚举

枚举 Alice 删除的每个 `0`；对每个中间串枚举 Bob 删除的每个 `1`，取 Bob 能得到的最小串；Alice 再在这些回应中取最大。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    string s;
    cin >> s;
    string answer;
    bool hasAnswer = false;
    for (int alice = 0; alice < static_cast<int>(s.size()); ++alice) {
      if (s[alice] != '0') {
        continue;
      }
      string afterAlice = s.substr(0, alice) + s.substr(alice + 1);
      string bobBest;
      bool hasBobBest = false;
      for (int bob = 0; bob < static_cast<int>(afterAlice.size()); ++bob) {
        if (afterAlice[bob] != '1') {
          continue;
        }
        string finalString = afterAlice.substr(0, bob) + afterAlice.substr(bob + 1);
        if (!hasBobBest || finalString < bobBest) {
          bobBest = finalString;
          hasBobBest = true;
        }
      }
      if (!hasAnswer || bobBest > answer) {
        answer = bobBest;
        hasAnswer = true;
      }
    }
    cout << answer << '\n';
  }
}
```

每组时间 $O(n^3)$，额外空间 $O(n)$。它覆盖全部策略，是小规模对拍 oracle。

### 最佳实用解：两次局部逆序修复

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void eraseForMaximum(string& s, char wanted) {
  for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
    if (s[i] == wanted && s[i] < s[i + 1]) {
      s.erase(s.begin() + i);
      return;
    }
  }
  s.erase(s.begin() + s.rfind(wanted));
}
void eraseForMinimum(string& s, char wanted) {
  for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
    if (s[i] == wanted && s[i] > s[i + 1]) {
      s.erase(s.begin() + i);
      return;
    }
  }
  s.erase(s.begin() + s.rfind(wanted));
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int testCount;
  cin >> testCount;
  while (testCount--) {
    string s;
    cin >> s;
    eraseForMaximum(s, '0');
    eraseForMinimum(s, '1');
    cout << s << '\n';
  }
}
```

每组时间 $O(n)$，额外空间 $O(1)$（不计输入串自身；`erase` 搬移字符仍为线性总量）。

## 正确性证明

设两个可删 `0` 的位置为 $i<j$。删除结果在 $i$ 之前相同。若 $s_i\ldots s_j$ 全是 `0`，删除任一位置得到同一串；否则该区间内第一个 `1` 在删除 $i$ 后会比删除 $j$ 后提前一位，于首个差异处前者为 `1`、后者为 `0`，所以删除更左的 `0` 更优。由此 Alice 删除最左 `0` 是支配策略。对 `1` 对称比较：两个候选之间若出现 `0`，删除更左的 `1` 会让这个 `0` 更早出现，所得串更小；故 Bob 删除最左 `1` 是支配策略。

删除 `0` 不会改变 `1` 的相对顺序，所以 Alice 的任何动作都不会改变“最左 `1`”是哪一个原字符；Bob 的支配策略与 Alice 的选择无关。Bob 删除 `1` 也不改变 `0` 的相对顺序。于是两人分别删除原串最左的 `0` 与最左的 `1`，得到唯一的最优终局。代码中的首个 `01`、首个 `10` 规则恰好生成同一终局，因此算法正确。

## 样例手推

对 `11001`，第一个 `01` 是末尾边界，Alice 删除其中的 `0`，得到 `1101`。其中第一个 `10` 的边界在第二个 `1`，Bob 删除该 `1`，得到 `101`。

对 `0010`，Alice 删除第一个 `01` 的 `0` 后得到 `010`；Bob 删除其中 `10` 的 `1`，得到 `00`。`101` 中 Alice 删除唯一的 `0` 得 `11`，Bob 删除任意 `1` 都得到 `1`。

## 易错点与方案比较

- Alice 与 Bob 的目标相反，不能把两次删除都写成同一种边界。
- Alice 找 `01` 并删除 `0`；Bob 找 `10` 并删除 `1`。
- 找不到目标边界时要删除最后一个目标字符；此时相同字符已集中在单调后缀，选择不影响结果。
- 先删后串长度变化，Bob 的下标属于中间串。
- 枚举法证明定义最直接，线性法利用首个差异，竞赛中推荐记忆“删一位获得字典序最优串”的单调栈式局部规则。

## 变种一：同时输出双方删除的原始下标

新定义：除终局外，输出 Alice 和 Bob 删除字符在原串中的一基下标。保留一个与字符同步删除的原下标数组即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int choose(const string& s, char wanted, bool maximize) {
  for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
    if (s[i] == wanted && (maximize ? s[i] < s[i + 1] : s[i] > s[i + 1])) {
      return i;
    }
  }
  return s.rfind(wanted);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  vector<int> original(s.size());
  iota(original.begin(), original.end(), 1);
  int alice = choose(s, '0', true);
  int aliceOriginal = original[alice];
  s.erase(s.begin() + alice);
  original.erase(original.begin() + alice);
  int bob = choose(s, '1', false);
  int bobOriginal = original[bob];
  s.erase(s.begin() + bob);
  cout << s << '\n' << aliceOriginal << ' ' << bobOriginal << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；额外数组用于恢复原坐标。

## 变种二：任意有序字母表中删除一个指定字符

新定义：给出字符串、保证至少出现一次的指定字符，以及目标 `MAX` 或 `MIN`，只执行一次删除。原引理不依赖二进制，只依赖字符全序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, goal;
  char wanted;
  cin >> s >> wanted >> goal;
  bool maximize = goal == "MAX";
  int chosen = -1;
  for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
    bool improves = maximize ? s[i] < s[i + 1] : s[i] > s[i + 1];
    if (s[i] == wanted && improves) {
      chosen = i;
      break;
    }
  }
  if (chosen == -1) {
    chosen = s.rfind(wanted);
  }
  s.erase(s.begin() + chosen);
  cout << s << '\n';
}
```

时间 $O(n)$，额外空间 $O(1)$。

## 变种三：交换行动顺序

新定义：Bob 先删一个 `1` 并最小化中间串，Alice 再删一个 `0` 并最大化终局。双方仍分别采用“最左目标字符”的支配策略；删除不同字符的动作可交换，因此终局与原题相同。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
void eraseBest(string& s, char wanted, bool maximize) {
  for (int i = 0; i + 1 < static_cast<int>(s.size()); ++i) {
    bool improves = maximize ? s[i] < s[i + 1] : s[i] > s[i + 1];
    if (s[i] == wanted && improves) {
      s.erase(s.begin() + i);
      return;
    }
  }
  s.erase(s.begin() + s.rfind(wanted));
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  eraseBest(s, '1', false);
  eraseBest(s, '0', true);
  cout << s << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。Bob 删除 `1` 不改变 `0` 的相对顺序，Alice 删除 `0` 也不改变 `1` 的相对顺序，所以交换行动只改变中间过程，不改变最终删除的两个原字符与终局。

## 变种四：双方交替进行多轮删除

新定义：Alice 与 Bob 各执行 $r$ 次，仍分别删 `0` 最大化和删 `1` 最小化，并保证原串至少有 $r$ 个 `0` 和 $r$ 个 `1`。支配策略逐轮成立：Alice 删除原串从左到右最早尚存的 $r$ 个 `0`，Bob 删除最早尚存的 $r$ 个 `1`；不同字符的删除互不改变各自相对顺序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int rounds;
  cin >> s >> rounds;
  int removedZeros = 0;
  int removedOnes = 0;
  string answer;
  for (char character : s) {
    if (character == '0' && removedZeros < rounds) {
      ++removedZeros;
    } else if (character == '1' && removedOnes < rounds) {
      ++removedOnes;
    } else {
      answer.push_back(character);
    }
  }
  cout << answer << '\n';
}
```

每个字符扫描一次，时间 $O(n)$，输出外额外空间 $O(1)$。逐轮应用单次支配策略，且删 `0`、删 `1` 的动作两两可交换，所以直接跳过最早的 $r$ 个 `0` 与 $r$ 个 `1` 即得到最优终局。

## 验证说明

线性算法与完整极大极小枚举对所有长度 $3..12$、同时含 `0` 与 `1` 的二进制串逐项比较，共 8164 组；独立复核进一步穷举到长度 16，共 131036 组，零反例。另外运行全部官方样例并以 GNU++23 编译六段代码。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://codeforces.com/contest/2248/problem/A)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-weekly-512-q4-lc4003/">← [力扣竞赛] 第 512 场周赛 Q4 LC 4003 交替方向的最小路径代价 III 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-daily-2026-08-02-lc877/">[力扣每日一题] 2026-08-02｜LC 877 石子游戏 →</a>
</nav>
