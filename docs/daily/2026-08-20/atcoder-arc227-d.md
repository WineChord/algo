---
title: "[atcoder] ARC227 D Median of Binary Strings"
---

# [atcoder] ARC227 D Median of Binary Strings

<p class="daily-archive-kicker">2026-08-20 · 第 1/5 题 · AtCoder</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-20 题目列表</a> · <a href="../../../math/majority-closure/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=9143ed2a973a05a7c30ad494d186689460a0a8eb8c1844917a33cc4ac5217bc2 -->
[Official problem: ARC227 D — Median of Binary Strings](https://atcoder.jp/contests/arc227/tasks/arc227_d?lang=en)

## 官方来源与元数据

- 比赛：AtCoder Regular Contest 227（ARC227）。
- 题目：D — Median of Binary Strings；任务 slug 为 `arc227_d`。
- 官方分值：700 分；AtCoder 未发布单题官方难度。
- 比赛 rated 范围：1200–2799。
- AtCoder Problems 社区估算难度：2277，抓取于 2026-08-20；这不是 AtCoder 官方难度。
- 时间限制：2 秒；内存限制：1024 MiB。
- 题面没有理解所必需的图片。

下方英文层是逐项阅读官方页面后独立组织的自包含呈现。题目没有已确认的专属开放转载
许可；官方页面与 [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en) 仍是权威来源。

## Complete English statement

You are given $N$ binary strings $S_1,S_2,\ldots,S_N$, each of length $M$. Initially, all these
strings are written on a blackboard.

You may repeat the following operation any number of times, including zero:

1. Choose three strings currently written on the blackboard and call them $A,B,C$. The same written
   string may be selected more than once.
2. Append a new length-$M$ string $D$ to the blackboard. For every position $i$, the bit $D_i$ must
   equal at least two of $A_i,B_i,C_i$; in other words, $D$ is their coordinate-wise majority.

For each of $Q$ query strings $T_1,T_2,\ldots,T_Q$, independently start from the initial blackboard and
determine whether some sequence of operations can make that query string appear.

### Input

```text
N M Q
S_1
S_2
...
S_N
T_1
T_2
...
T_Q
```

### Output

Print $Q$ lines. Line $i$ must contain `Yes` if $T_i$ can be written, and `No` otherwise.

### Constraints

- $1\le N\le500$.
- $1\le M\le500$.
- $1\le Q\le500$.
- Every $S_i$ and $T_i$ is a binary string of length exactly $M$.
- All numeric input values are integers.

### Official samples

Sample 1:

```text
Input
3 3 2
000
011
101
000
001

Output
Yes
Yes
```

The first query is present initially. For the second, the majority of `000`, `011`, and `101` is
`001`, so one operation creates it.

Sample 2:

```text
Input
2 1 2
0
0
0
1

Output
Yes
No
```

Only `0` is initially available, and every majority operation still produces `0`; therefore `1`
cannot appear.

This English presentation is independently organized from the official task semantics. The
[official statement](https://atcoder.jp/contests/arc227/tasks/arc227_d?lang=en) remains normative;
reuse is subject to the [AtCoder Terms of Use](https://atcoder.jp/tos?lang=en).

## 中文解释与题解

黑板上的集合在“逐位三数多数”运算下不断闭包。每个查询都从相同初始集合出发；前一个查询
不会真的改变后一个查询的黑板。关键不是模拟无限操作，而是找出多数闭包的有限判定条件。

## 约束推导与二坐标见证条件

对查询串 $T$，考虑任意两个坐标 $i,j$，允许 $i=j$。若某个可达字符串在这两个坐标上等于
$T_i,T_j$，则初始串中必有一个字符串同时匹配这两个比特。

原因是一次多数操作生成 $D$ 时，三个输入中至少两个在坐标 $i$ 匹配 $D_i$，也至少两个在
坐标 $j$ 匹配 $D_j$；两个大小至少为 2 的三元素下标集合必有交集，所以某个输入串同时匹配
两个坐标。沿生成历史向前归纳，最终得到一个初始串见证。

更惊喜的是，这个必要条件也充分：

> $T$ 可达，当且仅当对每个 $1\le i\le j\le M$，至少存在初始串 $S_k$，使
> $S_k[i]=T[i]$ 且 $S_k[j]=T[j]$。

对角线 $i=j$ 不能省略，它表达“该坐标的目标比特至少在一个初始串中出现”；样例 2 的
$M=1$ 正是最小反例。

预处理每个坐标对出现过的四种二比特模式，查询只需检查 $O(M^2)$ 个模式。直接实现总时间
$O((N+Q)M^2)$、空间 $O(M^2)$；最大约 $2.5\times10^8$ 次很小的整数操作。位集实现把
共同见证测试按机器字并行，常数更稳。

## 样例手推与边界

样例 1 的目标 `001`：坐标对 `(1,2)` 由 `000` 见证，`(1,3)` 由 `011` 见证，`(2,3)`
由 `101` 见证；三个对角线也都有匹配，所以可达，实际一次多数就得到它。

样例 2 查询 `1` 时，唯一对角线 `(1,1)` 没有任何初始串匹配目标比特，立即判 `No`。

- 重复初始串合法，但不会改变“某模式是否出现”。
- 同一个黑板字符串可在一次操作中选多次；暴力闭包与证明都必须允许。
- $N=1$ 时闭包只有唯一初始串。
- $M=1$ 时只检查对角线。
- 查询本身若已在初始集合中，所有坐标对由它自己见证，必为 `Yes`。

## 解法一：显式枚举多数闭包

当 $M$ 很小时，显式保存闭包中的字符串。每发现一个新字符串，就枚举它与当前闭包中另外
两个字符串组成的三元组并加入逐位多数结果；任意三元组在其中最后加入的成员出队时都会被
处理。它忠实覆盖所有有限操作序列，适合作 oracle；若闭包大小为 $K\le2^M$，时间
$O(MK^3)\subseteq O(M2^{3M})$，空间 $O(MK)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  unordered_set<string> seen;
  vector<string> values;
  queue<int> pending;
  for (int i = 0; i < n; ++i) {
    string value;
    cin >> value;
    if (seen.insert(value).second) {
      values.push_back(value);
      pending.push(values.size() - 1);
    }
  }
  while (!pending.empty()) {
    int newest = pending.front();
    pending.pop();
    int count = values.size();
    for (int first = 0; first < count; ++first) {
      for (int second = 0; second < count; ++second) {
        string majority(m, '0');
        for (int position = 0; position < m; ++position) {
          int ones = (values[newest][position] - '0') +
              (values[first][position] - '0') + (values[second][position] - '0');
          majority[position] = static_cast<char>('0' + (ones >= 2));
        }
        if (seen.insert(majority).second) {
          values.push_back(majority);
          pending.push(values.size() - 1);
        }
      }
    }
  }
  while (q--) {
    string target;
    cin >> target;
    cout << (seen.contains(target) ? "Yes\n" : "No\n");
  }
  return 0;
}
```

## 从闭包搜索到坐标对模式

显式闭包重复探索“某字符串怎样生成”。必要性证明告诉我们，任何失败都已经能被至多两个
坐标揭示；充分性则说明通过全部二坐标检查后，不必恢复操作序列。用 4 位掩码保存每对坐标
出现的 `00/01/10/11`，就把指数级状态压成 $O(M^2)$ 个局部事实。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<vector<unsigned char>> patterns(m, vector<unsigned char>(m));
  for (int row = 0; row < n; ++row) {
    string source;
    cin >> source;
    for (int i = 0; i < m; ++i) {
      for (int j = i; j < m; ++j) {
        int code = 2 * (source[i] - '0') + (source[j] - '0');
        patterns[i][j] |= static_cast<unsigned char>(1U << code);
      }
    }
  }
  while (q--) {
    string target;
    cin >> target;
    bool possible = true;
    for (int i = 0; i < m && possible; ++i) {
      for (int j = i; j < m; ++j) {
        int code = 2 * (target[i] - '0') + (target[j] - '0');
        if ((patterns[i][j] & (1U << code)) == 0) possible = false;
      }
    }
    cout << (possible ? "Yes\n" : "No\n");
  }
  return 0;
}
```

时间复杂度 $O((N+Q)M^2)$，空间 $O(M^2)$。它已经足够清晰；下面的位集版本在极限数据上
进一步减少常数。

## 最佳实用解：字面量见证位集与冲突位集

把“坐标 $i$ 取比特 $b$”称为一个字面量 $(i,b)$。`matches[i][b]` 是所有在该坐标取该比特
的初始串编号集合。两个字面量不可同时出现在可达目标中，当且仅当它们的见证集合交集为空。

预处理每个字面量的冲突字面量位集。查询时构造目标选择的 $M$ 个字面量；只要任一已选
字面量与目标集合相交于冲突表，就判 `No`。

### 正确性证明

**必要性**：前述“三个输入中的两个多数集合必相交”论证表明，任何可达 $T$ 的每对已选
字面量都必须有同一个初始串见证。

**充分性**：更强地对任意坐标子集 $K$ 证明，存在可达串在 $K$ 上与 $T$ 一致。若
$|K|\le2$，由二坐标条件直接成立。若 $|K|\ge3$，取 $K$ 中三个不同坐标 $a,b,c$；归纳
构造分别匹配 $K\setminus\{a\}$、$K\setminus\{b\}$、$K\setminus\{c\}$ 的三个可达串。
对 $K$ 中每个坐标，至少两个构造串在该处等于 $T$，它们的逐位多数就在整个 $K$ 上匹配
$T$。操作只新增字符串，三个中间结果可依次保留在黑板上。取 $K$ 为全部坐标即得到 $T$。

因此冲突位集无命中当且仅当查询可达。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int maxStrings = 500;
constexpr int maxLength = 500;
constexpr int maxLiterals = 1000;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<array<bitset<maxStrings>, 2>> matches(m);
  for (int row = 0; row < n; ++row) {
    string source;
    cin >> source;
    for (int position = 0; position < m; ++position) {
      matches[position][source[position] - '0'].set(row);
    }
  }
  vector<array<bitset<maxLiterals>, 2>> conflicts(m);
  for (int i = 0; i < m; ++i) {
    for (int firstBit = 0; firstBit <= 1; ++firstBit) {
      for (int j = 0; j < m; ++j) {
        for (int secondBit = 0; secondBit <= 1; ++secondBit) {
          if ((matches[i][firstBit] & matches[j][secondBit]).none()) {
            conflicts[i][firstBit].set(2 * j + secondBit);
          }
        }
      }
    }
  }
  while (q--) {
    string target;
    cin >> target;
    bitset<maxLiterals> selected;
    for (int i = 0; i < m; ++i) selected.set(2 * i + target[i] - '0');
    bool possible = true;
    for (int i = 0; i < m && possible; ++i) {
      if ((conflicts[i][target[i] - '0'] & selected).any()) possible = false;
    }
    cout << (possible ? "Yes\n" : "No\n");
  }
  return 0;
}
```

机器字复杂度约为
$O(NM+M^2\lceil N/64\rceil+QM\lceil2M/64\rceil)$，空间为 $O(MN+M^2)$ 位。
优先记忆二坐标见证定理；实现上，普通 4 位模式矩阵最直观，位集版适合追求更稳的常数。

## 易错点

- 只检查每个坐标分别出现，漏掉不可能共存的二比特组合。
- 只检查 $i<j$ 而漏掉 $i=j$；$M=1$ 会直接判错。
- 每个查询的每对坐标重新扫描全部 $N$ 个初始串，复杂度退化为 $O(QNM^2)$。
- 充分性不是“总有三个原始串一次生成目标”；它递归构造并保留中间字符串。
- 初始串和一次操作选择都允许重复，不能私自增加互异限制。
- 输出必须严格为 `Yes`、`No`。

## 可复现验证

三份程序按 GNU++23 编译，两组官方样例通过。对 $M\le3$ 的全部非空初始集合显式求多数
闭包，并逐个比较所有查询串与二坐标判定；对 $M=4,5$ 再做随机集合测试。还比较普通模式
矩阵与位集实现，覆盖重复源串、$N=1$、$M=1$、已存在查询和仅缺一个二坐标模式的查询。

## 变种一：查询含通配符，问是否存在可达补全

新定义：查询字符可为 `?`，问能否补成某个可达二进制串并输出一个补全。每个缺失的二坐标
模式都禁止两个字面量同时为真，形成 2-CNF 子句；固定字符形成单位子句。用 2-SAT 求解，
时间 $O(NM+M^2\lceil N/64\rceil+M^2)$，空间为 $O(MN+M^2)$ 位。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int maxStrings = 500;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<array<bitset<maxStrings>, 2>> matches(m);
  for (int row = 0; row < n; ++row) {
    string source;
    cin >> source;
    for (int i = 0; i < m; ++i) matches[i][source[i] - '0'].set(row);
  }
  string pattern;
  cin >> pattern;
  int nodes = 2 * m;
  vector<vector<int>> graph(nodes), reverseGraph(nodes);
  auto negate = [](int literal) { return literal ^ 1; };
  auto addImplication = [&](int from, int to) {
    graph[from].push_back(to);
    reverseGraph[to].push_back(from);
  };
  for (int i = 0; i < m; ++i) {
    for (int firstBit = 0; firstBit <= 1; ++firstBit) {
      for (int j = i; j < m; ++j) {
        for (int secondBit = 0; secondBit <= 1; ++secondBit) {
          if ((matches[i][firstBit] & matches[j][secondBit]).any()) continue;
          int first = 2 * i + firstBit;
          int second = 2 * j + secondBit;
          addImplication(first, negate(second));
          addImplication(second, negate(first));
        }
      }
    }
  }
  for (int i = 0; i < m; ++i) {
    if (pattern[i] == '?') continue;
    int chosen = 2 * i + pattern[i] - '0';
    addImplication(negate(chosen), chosen);
  }
  vector<char> used(nodes);
  vector<int> order;
  function<void(int)> firstDfs = [&](int node) {
    used[node] = true;
    for (int next : graph[node]) if (!used[next]) firstDfs(next);
    order.push_back(node);
  };
  for (int node = 0; node < nodes; ++node) if (!used[node]) firstDfs(node);
  vector<int> component(nodes, -1);
  function<void(int, int)> secondDfs = [&](int node, int id) {
    component[node] = id;
    for (int next : reverseGraph[node]) {
      if (component[next] == -1) secondDfs(next, id);
    }
  };
  reverse(order.begin(), order.end());
  int componentCount = 0;
  for (int node : order) {
    if (component[node] == -1) secondDfs(node, componentCount++);
  }
  string answer(m, '0');
  for (int i = 0; i < m; ++i) {
    if (component[2 * i] == component[2 * i + 1]) {
      cout << "No\n";
      return 0;
    }
    answer[i] = component[2 * i + 1] > component[2 * i] ? '1' : '0';
  }
  cout << "Yes\n" << answer << '\n';
  return 0;
}
```

## 变种二：在线加入或删除初始串

新定义：维护一个多重初始集合，支持 `+ S`、`- S` 与 `? T`。对每个坐标对和二比特模式
维护出现次数；增删一个源串更新 $O(M^2)$ 个计数，查询也检查 $O(M^2)$ 个计数。只要删除
请求保证目标串当前存在，多重计数就能正确恢复模式是否仍有见证。空间 $O(M^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, operations;
  cin >> m >> operations;
  vector<array<int, 4>> count(m * m);
  auto update = [&](const string& value, int delta) {
    for (int i = 0; i < m; ++i) {
      for (int j = i; j < m; ++j) {
        int code = 2 * (value[i] - '0') + value[j] - '0';
        count[i * m + j][code] += delta;
      }
    }
  };
  while (operations--) {
    char type;
    string value;
    cin >> type >> value;
    if (type == '+') update(value, 1);
    else if (type == '-') update(value, -1);
    else {
      bool possible = true;
      for (int i = 0; i < m && possible; ++i) {
        for (int j = i; j < m; ++j) {
          int code = 2 * (value[i] - '0') + value[j] - '0';
          if (count[i * m + j][code] == 0) possible = false;
        }
      }
      cout << (possible ? "Yes\n" : "No\n");
    }
  }
  return 0;
}
```

## 变种三：统计所有可达二进制串

新定义：不再给查询；当 $M\le24$ 时，统计多数闭包中不同字符串数量。缺失的见证模式等价
于一对字面量不能同时选择。DFS 逐坐标选 0/1，并用 64 位冲突掩码即时剪枝。预处理
$O(NM^2)$，搜索最坏 $O(2^M M)$，空间 $O(NM+M^2)$；指数性符合计数 2-SAT 的本质难度。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<string> sources(n);
  for (string& source : sources) cin >> source;
  vector<unsigned long long> conflict(2 * m);
  for (int i = 0; i < m; ++i) {
    for (int firstBit = 0; firstBit <= 1; ++firstBit) {
      for (int j = 0; j < m; ++j) {
        for (int secondBit = 0; secondBit <= 1; ++secondBit) {
          bool witnessed = false;
          for (const string& source : sources) {
            if (source[i] - '0' == firstBit && source[j] - '0' == secondBit) {
              witnessed = true;
              break;
            }
          }
          if (!witnessed) conflict[2 * i + firstBit] |= 1ULL << (2 * j + secondBit);
        }
      }
    }
  }
  function<unsigned long long(int, unsigned long long)> count =
      [&](int position, unsigned long long chosen) -> unsigned long long {
    if (position == m) return 1;
    unsigned long long answer = 0;
    for (int bit = 0; bit <= 1; ++bit) {
      int literal = 2 * position + bit;
      unsigned long long next = chosen | (1ULL << literal);
      if ((conflict[literal] & next) == 0) {
        answer += count(position + 1, next);
      }
    }
    return answer;
  };
  cout << count(0, 0) << '\n';
  return 0;
}
```

## 变种四：对失败查询返回一个至多二坐标反证

新定义：若不可达，除 `No` 外输出一对坐标及目标比特，证明没有任何初始串同时匹配；若
可达仍输出 `Yes`。二坐标定理保证这类反证总存在，查询时记录首个缺失模式即可。预处理与
查询复杂度仍为 $O((N+Q)M^2)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<array<char, 4>> present(m * m);
  for (int row = 0; row < n; ++row) {
    string source;
    cin >> source;
    for (int i = 0; i < m; ++i) {
      for (int j = i; j < m; ++j) {
        int code = 2 * (source[i] - '0') + source[j] - '0';
        present[i * m + j][code] = true;
      }
    }
  }
  while (q--) {
    string target;
    cin >> target;
    int badI = -1, badJ = -1;
    for (int i = 0; i < m && badI == -1; ++i) {
      for (int j = i; j < m; ++j) {
        int code = 2 * (target[i] - '0') + target[j] - '0';
        if (!present[i * m + j][code]) {
          badI = i;
          badJ = j;
          break;
        }
      }
    }
    if (badI == -1) cout << "Yes\n";
    else cout << "No " << badI + 1 << ' ' << badJ + 1 << ' '
              << target[badI] << target[badJ] << '\n';
  }
  return 0;
}
```

## 来源

- [ARC227 D 官方题面](https://atcoder.jp/contests/arc227/tasks/arc227_d?lang=en)，核对于
  2026-08-20。
- [ARC227 D 官方题解](https://atcoder.jp/contests/arc227/editorial/24409?lang=en)。
- [AtCoder Problems 社区难度数据](https://kenkoooo.com/atcoder/#/table/)，抓取于
  2026-08-20；数值为社区估算。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://atcoder.jp/contests/arc227/tasks/arc227_d?lang=en)
- [对应知识专题](../../math/majority-closure.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<span class="daily-archive-pager__empty"></span>
<a class="daily-archive-pager__next" href="../leetcode-top-140-lc199/">[力扣 Top 140] LC 199 二叉树的右视图 中等 →</a>
</nav>
