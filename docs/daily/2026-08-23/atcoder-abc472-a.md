---
title: "[atcoder] ABC472 A A"
---

# [atcoder] ABC472 A A

<p class="daily-archive-kicker">2026-08-23 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-23 题目列表</a> · <a href="../../../strings/#problem-atcoder-abc472-a">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b9ed3f8b36c1db0475e897aa4e421c628fa8545402ab09a1bafbd7cdafb3737d -->
[Official problem: ABC472 A — A](https://atcoder.jp/contests/abc472/tasks/abc472_a?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Beginner Contest 472（ABC472），比赛时长 100 分钟，rated 范围为 0–1999。
- 题目：A — A；任务 slug 为 `abc472_a`。
- 官方分值：100 分；AtCoder 未发布单题官方难度。
- AtCoder Problems 社区模型原始估算为 -955，低分段界面校正后约为 14，抓取于
  2026-08-23；两者都不是 AtCoder 官方难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en) 仍是权威来源。

## Complete English statement

You are given a string $S$ consisting only of uppercase English letters. Replace every character of
$S$ other than `A` with a period (`.`), leave every `A` unchanged, and print the resulting string.

### Input

```text
S
```

### Output

Print the string obtained by keeping each `A` in $S$ and replacing every other character with `.`.

### Constraints

- $S$ consists of uppercase English letters.
- $1\le |S|\le100$.

### Official samples

Sample 1 input:

```text
ATCODER
```

Sample 1 output:

```text
A......
```

Only the first character is `A`; the other six characters become periods.

Sample 2 input:

```text
BANANA
```

Sample 2 output:

```text
.A.A.A
```

The `A` characters at positions 2, 4, and 6 remain unchanged.

Sample 3 input:

```text
CORRECT
```

Sample 3 output:

```text
.......
```

There is no `A`, so every character becomes a period.

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/abc472/tasks/abc472_a?lang=en) remains normative;
reuse is subject to the [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en).

## 中文解释与最优结论

逐字符查看字符串：字符等于 `A` 时原样保留，否则改成 `.`。每个位置的答案只取决于该位置
本身，不需要统计、排序或查看相邻字符。时间复杂度为 $O(n)$，若原地修改则额外空间为
$O(1)$；读取和输出长度为 $n$ 的字符串本身就需要 $\Omega(n)$，所以这也是渐进最优解。

## 约束推导、溢出与边界

- $|S|\le100$，任何线性扫描都绰绰有余；真正要避免的是把简单映射误写成全局逻辑。
- 输出与输入等长，位置次序完全不变，因此可以安全原地覆盖字符。
- 只处理大写英文字母，不需要考虑小写 `a`、空格或 Unicode 字符。
- 字符串至少含一个字符，不存在空串输入；全是 `A` 时输出不变，全无 `A` 时输出全是点。
- 题目没有数值运算，因此不存在整数溢出。

## 官方样例手推

对 `BANANA` 从左到右处理：`B` 变为 `.`，第一个 `A` 保留，`N` 变为 `.`，之后重复同样规则，
状态依次为 `.ANANA`、`.A.ANA`、`.A.A.A`，最终得到官方输出。

## 解法一：逐位置枚举允许的输出字符

把每个位置的候选输出看成 `.` 与 26 个大写字母，共 27 种。逐一枚举候选，找到唯一满足
“输入为 `A` 时输出 `A`，否则输出 `.`”的字符。它完整覆盖每个位置的全部候选，因此正确；
时间复杂度 $O(27n)=O(n)$，额外空间 $O(n)$，但常数和表达都不必要地复杂。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  string answer;
  for (char original : s) {
    for (int candidate = 0; candidate < 27; ++candidate) {
      char output = candidate == 0 ? '.' : static_cast<char>('A' + candidate - 1);
      bool valid = original == 'A' ? output == 'A' : output == '.';
      if (valid) {
        answer.push_back(output);
        break;
      }
    }
  }
  cout << answer << '\n';
  return 0;
}
```

## 从枚举到直接映射

每个位置的合法输出其实由一个条件唯一确定。删去 27 个候选的枚举，直接用条件表达式选择
`A` 或 `.` 即可；不同位置互不影响，所以逐位置的局部选择拼起来就是唯一的全局答案。

## 最佳实用解：原地字符映射

### 正确性证明

对任意位置 $i$：若 $S_i$ 是 `A`，算法不修改它，符合题意；若 $S_i$ 不是 `A`，算法把它
改为 `.`，也符合题意。所有位置都逐一处理且保持原顺序，因此输出字符串在每个位置上都与
题目规定一致，算法正确。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  for (char& character : s) {
    if (character != 'A') character = '.';
  }
  cout << s << '\n';
  return 0;
}
```

时间复杂度 $O(n)$，额外空间 $O(1)$（不计输入与输出字符串）。

## 同阶方案比较与易错点

也可以另建结果字符串，时间仍为 $O(n)$，但会多用 $O(n)$ 空间；这里输入之后不再需要原串，
原地修改更短且更稳定。竞赛中优先记忆“遍历引用并按条件覆盖”。

- 写成“只输出所有 `A`”会丢失原长度；非 `A` 必须输出占位点。
- 把 `A` 也替换成点，或反过来只替换 `A`，都会颠倒条件。
- 不要把 `.` 当作字符串 `"."` 赋给单个 `char`。
- 输出中不能添加空格，末尾换行不影响判定。

## 可复现验证

两份原题程序均以 GNU++23 编译，并通过全部三个官方样例、单字符 `A`、单字符 `Z`、全 `A`、
全非 `A` 与随机大写字符串。随机测试对 20,000 个长度 1–100 的字符串逐字符比较两种实现，
结果完全一致。

## Follow-up 与约束变种

### 变种一：保留任意给定字符集合

新定义：输入两个无空格字符串 `s keep`，其中 $1\le|s|\le10^5$，`keep` 由 1–26 个互异
大写字母组成；输出保留集合内字符、其余变点的字符串。原来的单字符判断不再够用，但位置
独立性仍成立；用 26 位布尔表即可。时间复杂度 $O(n+|keep|)$，额外空间 $O(1)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  string keep;
  cin >> s >> keep;
  array<bool, 26> allowed{};
  for (char character : keep) allowed[character - 'A'] = true;
  for (char& character : s) {
    if (!allowed[character - 'A']) character = '.';
  }
  cout << s << '\n';
  return 0;
}
```

### 变种二：多次区间字符计数

新定义：先输入字符串 `s` 和询问数 $q$，再输入 $q$ 行 `l r c`；下标从 1 开始，$[l,r]$
为闭区间，询问若只保留字符 `c` 会留下多少个非点字符。约束为
$1\le l\le r\le|s|\le10^5$、$q\le10^5$，每个答案单独输出。原题逐次重扫会变成
$O(nq)$；为 26 个字符建立前缀计数，每次用两个前缀相减。预处理 $O(26n)$，单次询问
$O(1)$，空间 $O(26n)$。

<!-- compile:program -->
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
  vector<array<int, 26>> prefix(n + 1);
  for (int i = 0; i < n; ++i) {
    prefix[i + 1] = prefix[i];
    ++prefix[i + 1][s[i] - 'A'];
  }
  while (q--) {
    int left;
    int right;
    char character;
    cin >> left >> right >> character;
    cout << prefix[right][character - 'A'] - prefix[left - 1][character - 'A'] << '\n';
  }
  return 0;
}
```

### 变种三：在线修改并查询区间中 `A` 的个数

新定义：先输入 `s q`，每项操作是 `1 i c`（把 1-based 位置 $i$ 改成大写字母 `c`）或
`2 l r`（输出闭区间 $[l,r]$ 中 `A` 的个数）；所有下标合法，$|s|,q\le2\times10^5$。
静态前缀和会因修改失效；用树状数组维护每个位置是否为 `A`。单次修改和查询均为
$O(\log n)$，空间 $O(n)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Fenwick {
public:
  explicit Fenwick(int n) : tree(n + 1) {}
  void add(int index, int delta) {
    for (; index < static_cast<int>(tree.size()); index += index & -index) {
      tree[index] += delta;
    }
  }
  int sum(int index) const {
    int answer = 0;
    for (; index > 0; index -= index & -index) answer += tree[index];
    return answer;
  }
private:
  vector<int> tree;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int q;
  cin >> s >> q;
  Fenwick fenwick(static_cast<int>(s.size()));
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == 'A') fenwick.add(i + 1, 1);
  }
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int index;
      char character;
      cin >> index >> character;
      fenwick.add(index, (character == 'A') - (s[index - 1] == 'A'));
      s[index - 1] = character;
    } else {
      int left;
      int right;
      cin >> left >> right;
      cout << fenwick.sum(right) - fenwick.sum(left - 1) << '\n';
    }
  }
  return 0;
}
```

### 变种四：输入是超长字符串的游程编码

新定义：先输入 $m$，再输入 $m$ 行 `character length`；每个字符是大写字母，每个长度为
正整数，输入游程相邻字符不同，且展开总长度不超过 `long long`。输出合并后的游程数，再逐行
输出 `character length`。逐字符展开不可行。每个 `A` 游程原样保留，其他游程都变成点，并
合并相邻点游程。时间复杂度 $O(m)$，空间 $O(m)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m;
  cin >> m;
  vector<pair<char, long long>> answer;
  for (int i = 0; i < m; ++i) {
    char character;
    long long length;
    cin >> character >> length;
    char output = character == 'A' ? 'A' : '.';
    if (!answer.empty() && answer.back().first == output) {
      answer.back().second += length;
    } else {
      answer.push_back({output, length});
    }
  }
  cout << answer.size() << '\n';
  for (auto [character, length] : answer) cout << character << ' ' << length << '\n';
  return 0;
}
```

## 推荐记忆

看到“每个字符独立替换”时，先确认输出是否保持长度与顺序；若是，通常只需一次原地扫描。
只有出现多次查询、在线修改或压缩输入，才需要前缀和、树状数组或游程级处理。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/abc472/tasks/abc472_a?lang=en)
- [对应知识专题](../../strings/index.md#problem-atcoder-abc472-a)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-141-lc62/">[力扣 Top 141] LC 62 不同路径 中等 →</a>
</nav>
