---
title: "[atcoder] ABC468 D Pre-Palindrome"
---

# [atcoder] ABC468 D Pre-Palindrome

<p class="daily-archive-kicker">2026-07-29 · 第 1/14 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-29 题目列表</a> · <a href="../../../strings/palindrome-centers/">进入知识专题</a></p>

## 官方原始信息

- 来源：AtCoder
- 比赛：AtCoder Beginner Contest 468
- 题号与标题：D - Pre-Palindrome
- 官方分值：400
- 比赛 Rated Range：0–1999
- AtCoder Problems 社区估算难度：683（抓取于 2026-07-29；不是 AtCoder 官方难度）
- 时间限制：2 秒
- 内存限制：1024 MiB
- 官方英文题面：[AtCoder ABC468 D](https://atcoder.jp/contests/abc468/tasks/abc468_d?lang=en)
- 版权条款：[AtCoder Terms of Use](https://atcoder.jp/tos?lang=en)

!!! info "官方来源与版权"
    AtCoder 是本题的官方来源。其使用条款说明，服务中的文字、图片、程序及其他数据权利归 AtCoder 或相关第三方权利人所有。普通 AtCoder Beginner Contest 题面没有已确认的统一开放再发布许可，因此下方英文题面依据官方内容独立组织与撰写，并完整保留题意、数据契约、约束和样例；事实核验以上方官方题目链接为准。

### Complete English statement

Call a lowercase English string **good** when changing no more than one of its characters can make it a palindrome. Changing zero characters is allowed, so every palindrome is good.

For orientation:

- `a`, `iwai`, and `abcdcza` are good.
- `abcd` and `atcoder` are not good.

You are given a lowercase English string `S`. Count its non-empty contiguous substrings that are good.

A substring occurrence is identified by its interval in `S`. Consequently, equal strings extracted from different positions are counted as different substrings.

A substring is contiguous: it is obtained by deleting zero or more characters from the beginning of `S` and zero or more characters from its end. For example, `ab` is a substring of `abc`, whereas `ac` is not.

#### Constraints

- `S` consists only of lowercase English letters.
- $1\le |S|\le10^4$.

#### Input

The input is supplied through standard input in this form:

```text
S
```

#### Output

Print one integer: the number of non-empty good substring occurrences of `S`.

#### Official sample 1

```text
Input
ababa

Output
13
```

For example, the interval from the 2nd through the 3rd character produces `ba`, and the complete interval from the 1st through the 5th character produces `ababa`; both are good. There are 15 non-empty substring occurrences in total. Exactly two are not good: `abab` at positions 1 through 4 and `baba` at positions 2 through 5. Hence the answer is 13.

#### Official sample 2

```text
Input
atcoder

Output
18
```

#### Official sample 3

```text
Input
abccbacbacb

Output
40
```

The official statement provides no additional explanation for samples 2 and 3 and contains no illustration required to interpret the task.

### 中文解释

如果一个只含小写字母的字符串通过改写零个或一个位置就能变成回文串，就称它为好字符串；因此原本就是回文串的字符串也合法。例如 `a`、`iwai`、`abcdcza` 是好字符串，而 `abcd`、`atcoder` 不是。

给定字符串 `S`，需要统计其中所有非空连续子串里有多少个是好字符串。这里的子串必须对应 `S` 的一段连续区间，等价于只从原串开头和结尾删去若干字符；`ab` 是 `abc` 的子串，而 `ac` 不是。计数对象是区间而不是去重后的字符串内容，所以两个位置不同的子串即使文本相同，也要分别计数。

输入只有一行 `S`，其中 $1\le |S|\le10^4$ 且所有字符都是小写英文字母；输出一个整数表示好子串区间的总数。第一组样例 `ababa` 共有 15 个非空子串，只有位置 1–4 的 `abab` 和位置 2–5 的 `baba` 无法通过至多一次改写变成回文，因此答案为 13。

## 最优结论

围绕每个奇数中心和偶数中心向两侧扩展，维护当前子串中镜像位置不相等的对数。一次字符改写最多修复一对不相等字符，因此不相等对数不超过 1 的子串恰好是好字符串；出现第 2 对不相等字符后，更大的同中心子串不可能恢复为好字符串，可以立即停止。

- 时间复杂度：$O(n^2)$。
- 额外空间复杂度：$O(1)$。
- 推荐记忆：把“改写至多一次成为回文”直接转成“镜像失配对至多一个”，再按回文中心枚举所有子串。

## 约束与观察

长度为 $n$ 的字符串共有 $n(n+1)/2$ 个子串。$n=10^4$ 时，$O(n^3)$ 明显不可行；$O(n^2)$ 约为五千万次中心扩展，符合本题限制。

一个长度为 $L$ 的串共有 $\lfloor L/2\rfloor$ 对镜像位置。改写某个非中心字符只影响它所在的那一对：

- 若失配对数为 0，原串已经是回文。
- 若失配对数为 1，把这一对任意一侧改成另一侧即可。
- 若失配对数至少为 2，一次改写只能修复其中一对，仍不可能成为回文。

所以判定条件不是字符频次，也不是“能否重排成回文”，而是原顺序下镜像失配对数是否至多为 1。

## 解法递进

### 解法一：枚举子串后逐一检查

枚举左右端点，再从两端向中间统计失配对。它覆盖所有子串且判定正确，但每个子串又花 $O(n)$，总时间 $O(n^3)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = static_cast<int>(s.size());
  long long answer = 0;
  for (int left = 0; left < n; ++left) {
    for (int right = left; right < n; ++right) {
      int mismatches = 0;
      for (int i = left, j = right; i < j; ++i, --j) {
        mismatches += s[i] != s[j];
      }
      answer += mismatches <= 1;
    }
  }
  cout << answer << '\n';
  return 0;
}
```

### 解法二：按中心扩展

每个子串有且仅有一个中心：奇数长度中心落在字符上，偶数长度中心落在相邻字符之间。固定中心后，半径每增加一层只新增一对镜像字符，因此可以复用上一层的失配数，消除逐个子串从头检查的重复工作。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = static_cast<int>(s.size());
  long long answer = 0;
  for (int center = 0; center < n; ++center) {
    int mismatches = 0;
    for (int left = center, right = center; left >= 0 && right < n; --left, ++right) {
      mismatches += s[left] != s[right];
      if (mismatches > 1) {
        break;
      }
      ++answer;
    }
  }
  for (int center = 0; center + 1 < n; ++center) {
    int mismatches = 0;
    for (int left = center, right = center + 1; left >= 0 && right < n; --left, ++right) {
      mismatches += s[left] != s[right];
      if (mismatches > 1) {
        break;
      }
      ++answer;
    }
  }
  cout << answer << '\n';
  return 0;
}
```

## 正确性证明

引理 1：字符串能通过至多一次改写成为回文，当且仅当其镜像失配对数至多为 1。

证明：失配数为 0 时无需改写；失配数为 1 时改写唯一失配对的一侧即可。若失配数至少为 2，一次改写最多影响一对镜像位置，至少还有一对失配，无法成为回文。

引理 2：两轮中心枚举恰好枚举每个非空子串一次。

证明：奇数长度子串有唯一字符中心，偶数长度子串有唯一间隙中心；同一中心和半径唯一确定左右端点。

定理：算法输出好子串总数。

证明：由引理 2，每个子串恰被访问一次。算法维护其镜像失配对数，并由引理 1 恰在该数不超过 1 时计数。固定中心向外扩展只会增加或保持失配数，第 2 次失配后继续扩展不可能重新合法，因此提前停止不会漏解。

## 样例手推

对 `ababa` 的奇数中心下标 2：

- 半径 0：`a`，失配数 0，计数。
- 半径 1：`bab`，新增 `b` 与 `b`，失配数仍为 0，计数。
- 半径 2：`ababa`，新增 `a` 与 `a`，失配数仍为 0，计数。

对偶数中心下标 1 与 2 之间：

- `ab` 有一对失配，计数。
- `baba` 新增第二对失配，停止；因此 `baba` 不计数。

## 边界与易错点

- 长度为 1 的子串天然是回文。
- 偶数中心与奇数中心必须分别枚举。
- 第 2 次失配后必须先停止，不能把该层计入答案。
- 答案上界超过 32 位有符号整数，应使用 `long long`。
- 不要把题意误解为允许重排字符；字符顺序不能改变。

## 验证说明

最优实现使用独立 $O(n^3)$ 枚举作为 oracle，对长度 1–10、字母表 `{a,b,c}` 的随机字符串逐一比较；同时覆盖全相同字符、全不相同字符、奇偶长度和两个官方样例结构。

## Follow-up 与变种

### 变种一：允许至多改写 `d` 个字符

新定义：一个子串镜像失配对数不超过 `d` 时合法。中心扩展只需把停止阈值从 1 改为 `d`，复杂度仍为 $O(n^2)$、额外空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int d;
  cin >> s >> d;
  int n = static_cast<int>(s.size());
  long long answer = 0;
  for (int gap = 0; gap < 2; ++gap) {
    for (int center = 0; center < n; ++center) {
      int left = center;
      int right = center + gap;
      int mismatches = 0;
      while (left >= 0 && right < n) {
        mismatches += s[left] != s[right];
        if (mismatches > d) {
          break;
        }
        ++answer;
        --left;
        ++right;
      }
    }
  }
  cout << answer << '\n';
  return 0;
}
```

### 变种二：统计恰好需要一次改写的子串

恰好需要一次改写等价于失配对数恰为 1。仍按中心扩展，遇到第一对失配后开始计数，遇到第二对后停止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = static_cast<int>(s.size());
  long long answer = 0;
  for (int gap = 0; gap < 2; ++gap) {
    for (int center = 0; center < n; ++center) {
      int mismatches = 0;
      for (int left = center, right = center + gap; left >= 0 && right < n; --left, ++right) {
        mismatches += s[left] != s[right];
        if (mismatches > 1) {
          break;
        }
        answer += mismatches == 1;
      }
    }
  }
  cout << answer << '\n';
  return 0;
}
```

### 变种三：求最长好子串及其位置

每次合法扩展时更新最长区间。仍为 $O(n^2)$ 时间和 $O(1)$ 额外空间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = static_cast<int>(s.size());
  int bestLeft = 0;
  int bestRight = 0;
  for (int gap = 0; gap < 2; ++gap) {
    for (int center = 0; center < n; ++center) {
      int mismatches = 0;
      for (int left = center, right = center + gap; left >= 0 && right < n; --left, ++right) {
        mismatches += s[left] != s[right];
        if (mismatches > 1) {
          break;
        }
        if (right - left > bestRight - bestLeft) {
          bestLeft = left;
          bestRight = right;
        }
      }
    }
  }
  cout << bestLeft + 1 << ' ' << bestRight + 1 << '\n';
  cout << s.substr(bestLeft, bestRight - bestLeft + 1) << '\n';
  return 0;
}
```

### 变种四：多次区间询问

新定义：$n\le 2000$，每个询问给出区间 $[l,r]$，求完全位于该区间内的好子串数。先用区间 DP 求每个子串的失配数，再用二维容斥递推区间答案，预处理 $O(n^2)$，每次询问 $O(1)$，空间 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int q;
  cin >> s >> q;
  int n = static_cast<int>(s.size());
  vector<vector<unsigned short>> mismatch(n, vector<unsigned short>(n, 0));
  vector<vector<long long>> count(n, vector<long long>(n, 0));
  for (int length = 1; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      if (length >= 2) {
        mismatch[left][right] =
            (length == 2 ? 0 : mismatch[left + 1][right - 1]) + (s[left] != s[right]);
      }
      long long insideLeft = left + 1 <= right ? count[left + 1][right] : 0;
      long long insideRight = left <= right - 1 ? count[left][right - 1] : 0;
      long long overlap = left + 1 <= right - 1 ? count[left + 1][right - 1] : 0;
      count[left][right] = insideLeft + insideRight - overlap + (mismatch[left][right] <= 1);
    }
  }
  while (q--) {
    int left, right;
    cin >> left >> right;
    --left;
    --right;
    cout << count[left][right] << '\n';
  }
  return 0;
}
```

## Reference

- [AtCoder 官方题面](https://atcoder.jp/contests/abc468/tasks/abc468_d?lang=en)
- [AtCoder 官方比赛页](https://atcoder.jp/contests/abc468)
- [AtCoder Problems 社区难度表](https://kenkoooo.com/atcoder/#/table/)

### 延伸阅读

- [官方题目](https://atcoder.jp/contests/abc468/tasks/abc468_d?lang=en)
- [对应知识专题](../../strings/palindrome-centers.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-31-lc279/">[力扣 Top 31] LC 279 完全平方数 中等 →</a>
</nav>
