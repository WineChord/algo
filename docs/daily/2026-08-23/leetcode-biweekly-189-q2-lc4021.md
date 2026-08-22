---
title: "[力扣竞赛] 第 189 场双周赛 Q2 LC 4021 得到旋转回文字符串的最少操作次数 I 中等"
---

# [力扣竞赛] 第 189 场双周赛 Q2 LC 4021 得到旋转回文字符串的最少操作次数 I 中等

<p class="daily-archive-kicker">2026-08-23 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-23 题目列表</a> · <a href="../../../strings/cyclic-normalization/#problem-lc-4021">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=76bad14789a33bdfe32c3889ff459e43730b5775a59c6ff72c4539ceaf062b84 -->
[力扣官方题目：4021. 得到旋转回文字符串的最少操作次数 I](https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/)

## 官方原始信息

- 比赛：第 189 场双周赛；题目顺序：Q2；比赛开始时间：2026-08-15 22:30（北京时间）。
- 题号：LC 4021；官方中文标题：得到旋转回文字符串的最少操作次数 I；官方难度：中等。
- 官方竞赛分值：5 分。
- ZeroTracer 社区估算竞赛分：1517.775，抓取于 2026-08-23；这不是力扣官方难度或分值。
- 官方链接：[https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/](https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/)
- 函数签名：`int minOperations(string s)`。
- 官方标签：字符串、枚举。

### 原始题意

给定只含小写英文字母的字符串 `s`。可以任意次、任意顺序执行两类操作：

1. 选择一个字符，把它替换为字母表中的下一个字符，其中 `z` 的下一个字符是 `a`；
2. 把字符串循环左移一位，即把首字符移到末尾。

求把字符串变成回文串所需的最少操作次数。

### 全部官方样例

```text
示例 1
输入：s = "abc"
输出：2
解释：先左移得到 "bca"，再把末尾的 'a' 增加为 'b'，得到回文串 "bcb"。

示例 2
输入：s = "yb"
输出：3
解释：不旋转时，把 'y' 连续增加三次可变为 'b'，得到 "bb"。
```

### 全部约束

- $2\le s.length\le2000$。
- `s` 只含小写英文字母。

## 最优结论摘要

枚举最终循环左移次数 $r\in[0,n-1]$。旋转后的第 $i$ 个字符来自
`s[(r + i) % n]`；一对字符数值差为 $d$ 时，只允许循环递增却能把二者变成相同字符的最少
代价是 $\min(d,26-d)$。把所有镜像对的代价相加，再加旋转代价 $r$，取最小值。

时间复杂度 $O(n^2)$，额外空间 $O(1)$；在 $n\le2000$ 的 I 版本中，这是实现最稳、证明最短
的方案。

## 约束推导、溢出与边界

- 左移 $n$ 次会回到原串，却多花 $n$ 次操作，所以最优解只需考虑 $0$ 到 $n-1$ 次旋转。
- 先增字符再旋转与先旋转再增对应字符可以交换，因此可把任意操作序列整理成“先选旋转，再让
  镜像字符相等”，不会增加代价。
- 固定旋转后，各镜像对互不共享字符，总代价是各对最小代价之和；奇数长度的中点无需修改。
- 每对代价至多 13，共至多 1000 对，再加最多 1999 次旋转，答案小于 15000，`int` 足够。
- 原串已经是回文时，$r=0$ 给出 0；重复字符、`a` 与 `z` 的环形相邻关系都要正确处理。

## 官方样例手推

对 `abc`：

- $r=0$ 时镜像对是 `a` 与 `c`，字符代价为 2，总计 2；
- $r=1$ 时字符串为 `bca`，镜像对是 `b` 与 `a`，字符代价为 1，再加一次旋转，总计 2；
- $r=2$ 时字符串为 `cab`，字符代价为 1，加两次旋转，总计 3。

最小值为 2。第二个样例 `yb` 的数值差是 23，绕过 `z -> a` 的另一方向只需
$26-23=3$ 次递增，因此答案为 3。

## 解法一：枚举旋转与每对的目标字符

对每个旋转，逐镜像对枚举 26 个可能的最终字符，计算两端分别循环递增到它的次数并取最小。
所有旋转和每对的所有共同目标都被覆盖，因此一定能找到最优解。时间复杂度 $O(26n^2)$，
额外空间 $O(1)$；它适合作为定义级 oracle，但 26 次枚举可以化成闭式。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minOperations(string s) {
    int n = static_cast<int>(s.size());
    int answer = numeric_limits<int>::max();
    for (int rotation = 0; rotation < n; ++rotation) {
      int cost = rotation;
      for (int left = 0; left < n / 2; ++left) {
        int right = n - 1 - left;
        int first = s[(rotation + left) % n] - 'a';
        int second = s[(rotation + right) % n] - 'a';
        int pairCost = numeric_limits<int>::max();
        for (int target = 0; target < 26; ++target) {
          int current = (target - first + 26) % 26;
          current += (target - second + 26) % 26;
          pairCost = min(pairCost, current);
        }
        cost += pairCost;
      }
      answer = min(answer, cost);
    }
    return answer;
  }
};
```

## 从目标字符枚举到环上距离

设两个字符编号为 $a,b$，普通差值 $d=|a-b|$。若把较小者沿字母表递增到较大者，代价是
$d$；若把较大者经过 `z -> a` 递增到较小者，代价是 $26-d$。选择这两条圆弧中较短的一条
即可。任何其他共同目标都位于某条圆弧继续前进的位置，只会在上述代价上再增加非负步数，
所以每对最小代价恰为 $\min(d,26-d)$。

## 最佳实用解：枚举旋转并累加环形距离

### 正确性证明

**引理一**：存在一个最优操作序列，其所有旋转都在所有字符递增之前。

一次递增作用于某个具体字符。把紧邻的“递增、旋转”交换为“旋转、对移动后同一字符递增”，
字符串结果和操作数均不变。反复交换即可得到所述顺序。

**引理二**：固定旋转 $r$ 后，一对镜像字符变得相等的最少代价是
$\min(|a-b|,26-|a-b|)$。

上节给出了沿字母环两条方向可达的上界；任意共同目标必须让二者合计走完两者之间某条圆弧，
不可能短于较短圆弧，故下界与上界相等。

固定旋转后，每个字符至多属于一个镜像对，各对操作互不影响。算法由引理二取到每一对的
最小值，再加恰好 $r$ 次旋转，得到该旋转下的最优代价。算法枚举了引理一中所有可能的
$r\in[0,n-1]$，故全局取小后得到最优答案。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minOperations(string s) {
    int n = static_cast<int>(s.size());
    int answer = numeric_limits<int>::max();
    for (int rotation = 0; rotation < n; ++rotation) {
      int cost = rotation;
      for (int left = 0; left < n / 2; ++left) {
        int right = n - 1 - left;
        int first = s[(rotation + left) % n] - 'a';
        int second = s[(rotation + right) % n] - 'a';
        int difference = abs(first - second);
        cost += min(difference, 26 - difference);
      }
      answer = min(answer, cost);
    }
    return answer;
  }
};
```

时间复杂度 $O(n^2)$，额外空间 $O(1)$。

## 同阶方案比较与易错点

可以真的构造每个旋转串再检查，时间仍为 $O(n^2)$，但每轮复制需要 $O(n)$ 临时空间。用模
下标直接访问原串空间更小，也不会出现旋转恢复错误。面试或竞赛中优先记忆“枚举旋转起点 +
镜像配对 + 字母环距离”。

- 漏加旋转次数 $r$，会错误地只比较回文修改成本。
- 把字符代价写成普通绝对值，遗漏 `z -> a` 的循环递增。
- 枚举到 $r=n$ 及以后没有新字符串，只会增加代价。
- 镜像右端应为 $n-1-i$，旋转后两端都要加 $r$ 再取模。
- 奇数长度的中心字符不需要与自己配对，也不产生代价。

## 可复现验证

两份原题代码均以 C++23 编译，并通过两个官方样例、已是回文、奇偶长度、全相同字符、`a/z`
相邻和旋转改变最优选择等边界。随机生成 30,000 个长度 2–9 的字符串，以“旋转 + 每对枚举
26 个目标字符”为 oracle，与闭式环形距离实现逐项一致。

## Follow-up 与约束变种

### 变种一：恢复最优旋转和一个最终回文串

新定义：除最少操作数外，还要返回所选旋转次数与一个可达回文串。只算距离无法直接给出共同
字符；对最优旋转的每对重新枚举 26 个目标，选择代价最小且字典序最小者即可。时间
$O(n^2+26n)$，额外空间 $O(n)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  tuple<int, int, string> minOperationsWithPalindrome(const string& s) {
    int n = static_cast<int>(s.size());
    int bestCost = numeric_limits<int>::max();
    int bestRotation = 0;
    for (int rotation = 0; rotation < n; ++rotation) {
      int cost = rotation;
      for (int left = 0; left < n / 2; ++left) {
        int right = n - 1 - left;
        int first = s[(rotation + left) % n] - 'a';
        int second = s[(rotation + right) % n] - 'a';
        int difference = abs(first - second);
        cost += min(difference, 26 - difference);
      }
      if (cost < bestCost) {
        bestCost = cost;
        bestRotation = rotation;
      }
    }
    string palindrome(n, 'a');
    for (int i = 0; i < n; ++i) palindrome[i] = s[(bestRotation + i) % n];
    for (int left = 0; left < n / 2; ++left) {
      int right = n - 1 - left;
      int bestPairCost = numeric_limits<int>::max();
      char bestTarget = 'z';
      for (int target = 0; target < 26; ++target) {
        int first = palindrome[left] - 'a';
        int second = palindrome[right] - 'a';
        int cost = (target - first + 26) % 26;
        cost += (target - second + 26) % 26;
        if (cost < bestPairCost) {
          bestPairCost = cost;
          bestTarget = static_cast<char>('a' + target);
        }
      }
      palindrome[left] = palindrome[right] = bestTarget;
    }
    return {bestCost, bestRotation, palindrome};
  }
};
```

### 变种二：统计达到最少代价的旋转数

新定义：只把旋转次数不同视为不同方案，返回最少代价与达到它的旋转数。原算法仍成立；每次
得到代价后维护最小值和并列计数。时间 $O(n^2)$，额外空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<int, int> minCostAndRotationCount(const string& s) {
    int n = static_cast<int>(s.size());
    int best = numeric_limits<int>::max();
    int count = 0;
    for (int rotation = 0; rotation < n; ++rotation) {
      int cost = rotation;
      for (int left = 0; left < n / 2; ++left) {
        int first = s[(rotation + left) % n] - 'a';
        int second = s[(rotation + n - 1 - left) % n] - 'a';
        int difference = abs(first - second);
        cost += min(difference, 26 - difference);
      }
      if (cost < best) {
        best = cost;
        count = 1;
      } else if (cost == best) {
        ++count;
      }
    }
    return {best, count};
  }
};
```

### 变种三：每次旋转的代价改为给定权重

新定义：一次左移花费非负整数 `rotationCost`，字符递增仍花费 1，并约束
$0\le rotationCost\le10^{15}$。原题只需把 $r$ 改为 $r\cdot rotationCost$；旋转与修改仍可
交换，各镜像对也仍独立。非负性保证多转完整的 $n$ 圈不会更优；给定上界又保证乘积在
`long long` 内。时间 $O(n^2)$，额外空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long minWeightedOperations(const string& s, long long rotationCost) {
    int n = static_cast<int>(s.size());
    long long answer = numeric_limits<long long>::max();
    for (int rotation = 0; rotation < n; ++rotation) {
      long long cost = rotationCost * rotation;
      for (int left = 0; left < n / 2; ++left) {
        int first = s[(rotation + left) % n] - 'a';
        int second = s[(rotation + n - 1 - left) % n] - 'a';
        int difference = abs(first - second);
        cost += min(difference, 26 - difference);
      }
      answer = min(answer, cost);
    }
    return answer;
  }
};
```

### 变种四：同一字符串回答大量旋转权重询问

新定义：字符串固定，给出 $1\le q\le2\times10^5$ 个询问，每个 `rotationCost` 都满足
$0\le w\le10^{15}$，求对应最小总代价。每次重跑会花 $O(qn^2)$。先用 $O(n^2)$ 算出每个
旋转的字符代价 $C_r$；每个候选成为直线
$C_r+r\cdot w$。在全部询问坐标上建立离散 Li Chao 树，插入 $n$ 条直线后逐点查询。总时间
$O(n^2+(n+q)\log q)$，空间 $O(q)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
constexpr int64 INF = numeric_limits<int64>::max() / 4;
struct Line {
  int64 slope = 0;
  int64 intercept = INF;
  int64 value(int64 x) const {
    return slope * x + intercept;
  }
};
class LiChao {
public:
  explicit LiChao(vector<int64> coordinates)
      : xs(move(coordinates)), tree(xs.size() * 4) {}
  void add(Line line) {
    add(1, 0, static_cast<int>(xs.size()) - 1, line);
  }
  int64 query(int index) const {
    return query(1, 0, static_cast<int>(xs.size()) - 1, index);
  }
private:
  vector<int64> xs;
  vector<Line> tree;
  void add(int node, int left, int right, Line line) {
    int middle = (left + right) / 2;
    bool betterLeft = line.value(xs[left]) < tree[node].value(xs[left]);
    bool betterMiddle = line.value(xs[middle]) < tree[node].value(xs[middle]);
    if (betterMiddle) swap(line, tree[node]);
    if (left == right) return;
    if (betterLeft != betterMiddle) {
      add(node * 2, left, middle, line);
    } else {
      add(node * 2 + 1, middle + 1, right, line);
    }
  }
  int64 query(int node, int left, int right, int index) const {
    int64 answer = tree[node].value(xs[index]);
    if (left == right) return answer;
    int middle = (left + right) / 2;
    if (index <= middle) return min(answer, query(node * 2, left, middle, index));
    return min(answer, query(node * 2 + 1, middle + 1, right, index));
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int q;
  cin >> s >> q;
  vector<int64> queries(q);
  for (int64& value : queries) cin >> value;
  vector<int64> xs = queries;
  sort(xs.begin(), xs.end());
  xs.erase(unique(xs.begin(), xs.end()), xs.end());
  LiChao hull(xs);
  int n = static_cast<int>(s.size());
  for (int rotation = 0; rotation < n; ++rotation) {
    int64 characterCost = 0;
    for (int left = 0; left < n / 2; ++left) {
      int first = s[(rotation + left) % n] - 'a';
      int second = s[(rotation + n - 1 - left) % n] - 'a';
      int difference = abs(first - second);
      characterCost += min(difference, 26 - difference);
    }
    hull.add({rotation, characterCost});
  }
  for (int64 value : queries) {
    int index = lower_bound(xs.begin(), xs.end(), value) - xs.begin();
    cout << hull.query(index) << '\n';
  }
  return 0;
}
```

## 推荐记忆

先把操作顺序规范化，再枚举真正的全局选择（旋转次数），最后利用固定选择下的局部独立性。
字母循环递增的两字符合并代价不是普通差值，而是 26 环上的最短距离。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/)
- [对应知识专题](../../strings/cyclic-normalization.md#problem-lc-4021)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-f1/">[codeforces] CF Round 1117 Div.2 F1 Beaver&#x27;s Jumping Track (Easy Version) →</a>
</nav>
