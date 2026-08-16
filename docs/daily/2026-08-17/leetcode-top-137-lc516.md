---
title: "[力扣 Top 137] LC 516 最长回文子序列 中等"
---

# [力扣 Top 137] LC 516 最长回文子序列 中等

<p class="daily-archive-kicker">2026-08-17 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-17 题目列表</a> · <a href="../../../strings/palindrome-centers/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=13f966365b05999b5d14ae35af75a621c8fc162396b7788ba8108a4199a2d0dc -->
[力扣 516：最长回文子序列](https://leetcode.cn/problems/longest-palindromic-subsequence/)

## 官方原始信息

- 题号：516。
- 官方中文标题：最长回文子序列。
- 官方难度：中等。
- 函数签名：`int longestPalindromeSubseq(string s)`。
- 题意：给定只含小写英文字母的字符串 `s`，可以删除任意字符但不能改变剩余字符的相对
  顺序；返回能够得到的最长回文子序列长度。

### 全部官方样例

样例 1：

```text
输入：s = "bbbab"
输出：4
解释：可以选择回文子序列 "bbbb"。
```

样例 2：

```text
输入：s = "cbbd"
输出：2
解释：可以选择回文子序列 "bb"。
```

### 全部官方约束

- `1 <= s.length <= 1000`。
- `s` 只含小写英文字母。

## 约束、状态选择与整数范围

子序列共有 $2^n$ 个，直接枚举不可能通过 $n=1000$。回文的决定发生在区间两端：若
`s[left] == s[right]`，可以把这两个字符同时放到答案两端；否则至少舍弃其中一个。
因此自然状态是区间 `[left,right]` 的最优长度，共 $O(n^2)$ 个状态。

答案不超过 $n\le1000$，`int` 足够。二维 DP 约有 $10^6$ 个整数，内存约 4 MB；若只求
长度，可以把依赖压成一维 $O(n)$ 空间。

## 样例手推与边界

对 `bbbab`，先看整个区间：首尾都是 `b`，选择它们后转成内部 `bba`。内部最优回文是
`bb`，所以得到长度 4 的 `bbbb`。对 `cbbd`，两端不同，分别舍弃 `c` 或 `d`；区间
`bb` 给出长度 2。

- 单字符：本身就是长度 1 的回文。
- 全部字符相同：答案为 $n$。
- 所有字符互异：答案为 1。
- 偶数与奇数长度回文使用同一递推；单字符基例自然充当奇数中心。
- 子序列不要求连续，不能套用回文子串的中心扩展。

## 解法一：枚举所有子序列

每个位置都有“选或不选”两种决定。到达叶子时检查当前子序列是否回文并更新最大长度。
这忠实覆盖所有候选，可作为很小规模的 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int best = 0;
  string chosen;
  void search(const string& s, int index) {
    if (index == static_cast<int>(s.size())) {
      bool palindrome = true;
      for (int left = 0, right = static_cast<int>(chosen.size()) - 1;
            left < right; ++left, --right) {
        if (chosen[left] != chosen[right]) palindrome = false;
      }
      if (palindrome) best = max(best, static_cast<int>(chosen.size()));
      return;
    }
    search(s, index + 1);
    chosen.push_back(s[index]);
    search(s, index + 1);
    chosen.pop_back();
  }
public:
  int longestPalindromeSubseq(string s) {
    search(s, 0);
    return best;
  }
};
```

时间 $O(n2^n)$，递归栈与当前子序列占 $O(n)$。瓶颈是不同删除方案反复求解相同区间。

## 从暴力到二维区间 DP

定义 $dp[l][r]$ 为闭区间 `s[left..right]` 的最长回文子序列长度。

若两端相同，把它们放在同一个最优回文的两端不会吃亏：

$$
dp[l][r]=dp[l+1][r-1]+2.
$$

若两端不同，任何回文子序列不可能同时用这两个端点，所以至少舍弃一个：

$$
dp[l][r]=\max(dp[l+1][r],dp[l][r-1]).
$$

基例是 $dp[i][i]=1$。按区间长度递增计算，所有依赖都已就绪。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestPalindromeSubseq(string s) {
    int n = s.size();
    vector<vector<int>> dp(n, vector<int>(n));
    for (int i = 0; i < n; ++i) dp[i][i] = 1;
    for (int length = 2; length <= n; ++length) {
      for (int left = 0; left + length <= n; ++left) {
        int right = left + length - 1;
        if (s[left] == s[right]) {
          dp[left][right] = length == 2 ? 2 : dp[left + 1][right - 1] + 2;
        } else {
          dp[left][right] = max(dp[left + 1][right], dp[left][right - 1]);
        }
      }
    }
    return dp[0][n - 1];
  }
};
```

时间 $O(n^2)$、空间 $O(n^2)$。二维表最适合需要恢复具体方案的扩展。

## 最佳实用解：一维区间 DP

外层让 `left` 从右向左移动。更新 `dp[right]` 前，它表示旧状态 $dp[l+1][r]$；更新后的
`dp[right-1]` 已表示本轮状态 $dp[l][r-1]$；变量 `inside` 保存被覆盖前的
$dp[l+1][r-1]$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestPalindromeSubseq(string s) {
    int n = s.size();
    vector<int> dp(n, 1);
    for (int left = n - 2; left >= 0; --left) {
      int inside = 0;
      for (int right = left + 1; right < n; ++right) {
        int old = dp[right];
        if (s[left] == s[right]) dp[right] = inside + 2;
        else dp[right] = max(dp[right], dp[right - 1]);
        inside = old;
      }
    }
    return dp[n - 1];
  }
};
```

时间 $O(n^2)$、额外空间 $O(n)$。只返回长度时，这是应优先记忆的实现：保留区间递推的
直接证明，同时把内存从平方降到线性。

## 同阶方案：与逆序串求最长公共子序列

令 `t = reverse(s)`。`s` 的任意回文子序列在 `t` 中仍按同一字符顺序出现；反过来，
二者最长公共子序列的长度等于最长回文子序列长度。使用标准 LCS 也可得到 $O(n^2)$ 时间、
$O(n)$ 空间的答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestPalindromeSubseq(string s) {
    string reversed = s;
    reverse(reversed.begin(), reversed.end());
    int n = s.size();
    vector<int> dp(n + 1);
    for (char first : s) {
      int diagonal = 0;
      for (int j = 1; j <= n; ++j) {
        int old = dp[j];
        if (first == reversed[j - 1]) dp[j] = diagonal + 1;
        else dp[j] = max(dp[j], dp[j - 1]);
        diagonal = old;
      }
    }
    return dp[n];
  }
};
```

复杂度与一维区间 DP 相同。LCS 模板复用性强，但“公共子序列为何能取成回文”的证明比
直接区间递推更绕；本题面试中优先记忆一维区间 DP。

## 正确性证明

对区间长度归纳。

基例：长度 1 的区间只有一个字符，最优长度为 1。

归纳步骤：考虑 `[left,right]`。若两端相同，内部任意最优回文两侧加上这两个相同字符，
得到长度 $dp[l+1][r-1]+2$；同时可取到使用两端的最优解，因此递推正确。若两端
不同，回文子序列不能同时以这两个不同字符作为两端，故至少不使用左端或不使用右端；两种
情况恰由 $dp[l+1][r]$ 与 $dp[l][r-1]$ 覆盖，取较大者即最优。

一维实现按照从右到左的 `left` 与从左到右的 `right` 顺序，分别从 `dp[right]`、
`dp[right-1]` 与 `inside` 读取上述三个旧状态，所以它逐项计算出与二维表完全相同的值。

## 方案比较与易错点

- 枚举子序列是指数级；区间 DP 把重复区间合并成 $O(n^2)$ 个状态。
- 二维 DP 便于恢复方案；一维 DP 只求长度时内存更稳。
- 两端相等时直接取内部加 2；不要误写成回文子串那样只扩展连续中心。
- 一维压缩的 `inside` 必须在覆盖 `dp[right]` 前保存旧值。
- `left` 必须从右向左，否则 `dp[right]` 不是下一层区间。
- LCS 方案应与整个逆序串比较，不能只比较相邻字符。

## 验证说明

两组官方样例均通过。对 500 个长度不超过 12 的随机字符串枚举全部子序列作 oracle，并对
1000 个长度不超过 45 的随机字符串用独立二维区间 DP 复核一维实现；另覆盖全相同、全不
同、奇偶长度和首尾重复等边界。全部发布代码以 C++23 编译。

## 变种一：恢复一个最长回文子序列

需要输出方案时保留二维表，并从整个区间向内回溯。两端相同且符合最优值时同时选择；否则
走向值不减的一侧。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string s;
  cin >> s;
  int n = s.size();
  vector<vector<int>> dp(n, vector<int>(n));
  for (int i = 0; i < n; ++i) dp[i][i] = 1;
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      if (s[left] == s[right]) {
        dp[left][right] = (length == 2 ? 0 : dp[left + 1][right - 1]) + 2;
      } else {
        dp[left][right] = max(dp[left + 1][right], dp[left][right - 1]);
      }
    }
  }
  string prefix, suffix;
  int left = 0;
  int right = n - 1;
  while (left <= right) {
    if (left == right) {
      prefix.push_back(s[left]);
      break;
    }
    int inside = left + 1 > right - 1 ? 0 : dp[left + 1][right - 1];
    if (s[left] == s[right] && dp[left][right] == inside + 2) {
      prefix.push_back(s[left]);
      suffix.push_back(s[right]);
      ++left;
      --right;
    } else if (dp[left + 1][right] >= dp[left][right - 1]) {
      ++left;
    } else {
      --right;
    }
  }
  reverse(suffix.begin(), suffix.end());
  cout << prefix + suffix << '\n';
}
```

时间与空间均为 $O(n^2)$，回溯为 $O(n)$。一维压缩失效，因为恢复需要比较历史区间。

## 变种二：最少删除或插入多少字符才能得到回文

保留一个最长回文子序列，删除其余字符即可得到回文，所以最少删除数是
$n-\operatorname{LPS}(s)$。最少插入数也等于这个值，对应
[力扣 1312：让字符串成为回文串的最少插入次数](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minInsertions(string s) {
    int n = s.size();
    vector<int> dp(n, 1);
    for (int left = n - 2; left >= 0; --left) {
      int inside = 0;
      for (int right = left + 1; right < n; ++right) {
        int old = dp[right];
        if (s[left] == s[right]) dp[right] = inside + 2;
        else dp[right] = max(dp[right], dp[right - 1]);
        inside = old;
      }
    }
    return n - dp[n - 1];
  }
};
```

时间 $O(n^2)$、空间 $O(n)$。原 DP 仍成立，最终目标从“保留最多”改写为“改动最少”。

## 变种三：改求最长回文子串

子串必须连续，区间删除模型不再适用。以每个字符和字符缝隙为中心向两侧扩展，可在
$O(n^2)$ 时间、$O(1)$ 额外空间内求解
[力扣 5：最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/)。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindrome(string s) {
    int bestLeft = 0;
    int bestLength = 1;
    auto expand = [&](int left, int right) {
      while (left >= 0 && right < static_cast<int>(s.size()) &&
              s[left] == s[right]) {
        if (right - left + 1 > bestLength) {
          bestLeft = left;
          bestLength = right - left + 1;
        }
        --left;
        ++right;
      }
    };
    for (int center = 0; center < static_cast<int>(s.size()); ++center) {
      expand(center, center);
      expand(center, center + 1);
    }
    return s.substr(bestLeft, bestLength);
  }
};
```

原问题的“跳过端点”变成非法操作；新的结构是回文的中心对称扩展。

## 变种四：同一字符串上回答大量区间询问

若每次询问 `[left,right]` 的最长回文子序列长度，先完整计算二维 DP，之后每次直接返回
对应单元格。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int queries;
  cin >> s >> queries;
  int n = s.size();
  vector<vector<int>> dp(n, vector<int>(n));
  for (int i = 0; i < n; ++i) dp[i][i] = 1;
  for (int length = 2; length <= n; ++length) {
    for (int left = 0; left + length <= n; ++left) {
      int right = left + length - 1;
      if (s[left] == s[right]) {
        dp[left][right] = (length == 2 ? 0 : dp[left + 1][right - 1]) + 2;
      } else {
        dp[left][right] = max(dp[left + 1][right], dp[left][right - 1]);
      }
    }
  }
  while (queries--) {
    int left, right;
    cin >> left >> right;
    cout << dp[left][right] << '\n';
  }
}
```

预处理时间与空间均为 $O(n^2)$，单次询问 $O(1)$。一维压缩不再可用，因为所有区间答案
都需要长期保留。

## Reference

- [力扣 516 官方题面](https://leetcode.cn/problems/longest-palindromic-subsequence/)
- [力扣 1312 官方题面](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/)
- [力扣 5 官方题面](https://leetcode.cn/problems/longest-palindromic-substring/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/longest-palindromic-subsequence/)
- [对应知识专题](../../strings/palindrome-centers.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc227-a/">← [atcoder] ARC227 A Fermat Point of Binary Strings</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-514-q4-lc4017/">[力扣竞赛] 第 514 场周赛 Q4 LC 4017 数组中的峰值 II 困难 →</a>
</nav>
