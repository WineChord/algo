---
title: "[力扣 Top 48] LC 1143 最长公共子序列 中等"
---

# [力扣 Top 48] LC 1143 最长公共子序列 中等

<p class="daily-archive-kicker">2026-07-30 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../dp/sequence-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=188e2ed49ecb0d6a3a2c6da824de96b43d072b9a7055417f3fe11973d85e07bc -->
## 官方原始信息

- Top 排名：48
- 题号：LC 1143
- 官方中文标题：最长公共子序列
- 官方难度：中等
- 官方链接：[最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)

### 原始题意

给定两个只含小写字母的字符串，返回它们最长公共子序列的长度。子序列可删除字符但不能改变剩余字符的相对顺序；不存在公共字符时返回 0。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int longestCommonSubsequence(string text1, string text2);
};
```

### 全部官方样例

```text
输入：text1 = "abcde", text2 = "ace"
输出：3
解释：最长公共子序列为 "ace"。
```

```text
输入：text1 = "abc", text2 = "abc"
输出：3
```

```text
输入：text1 = "abc", text2 = "def"
输出：0
```

### 全部约束

- $1\le |text1|,|text2|\le1000$。
- 两字符串只含小写英文字母。
- 状态数最多约 $10^6$，二维 DP 可通过。

## 约束推导与状态选择

直接枚举一个字符串的所有子序列是指数级。两个前缀的最优答案只取决于删掉哪个末尾字符，适合定义：

$$
dp_{i,j}=text1[0..i)\text{ 与 }text2[0..j)\text{ 的最长公共子序列长度}.
$$

## 解法递进

### 解法一：递归枚举末尾选择

字符相等时可以同时选入；不等时至少删去一个末尾字符。未记忆化会重复计算同一前缀对，最坏指数时间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int search(const string& a, const string& b, int i, int j) {
    if (i == static_cast<int>(a.size()) || j == static_cast<int>(b.size())) {
      return 0;
    }
    if (a[i] == b[j]) {
      return 1 + search(a, b, i + 1, j + 1);
    }
    return max(search(a, b, i + 1, j), search(a, b, i, j + 1));
  }
public:
  int longestCommonSubsequence(string text1, string text2) {
    return search(text1, text2, 0, 0);
  }
};
```

### 解法二：二维动态规划

递推为：

$$
dp_{i,j}=
\begin{cases}
dp_{i-1,j-1}+1,&a_{i-1}=b_{j-1},\\
\max(dp_{i-1,j},dp_{i,j-1}),&a_{i-1}\ne b_{j-1}.
\end{cases}
$$

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestCommonSubsequence(string text1, string text2) {
    int n = text1.size();
    int m = text2.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= m; ++j) {
        if (text1[i - 1] == text2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1] + 1;
        } else {
          dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
      }
    }
    return dp[n][m];
  }
};
```

时间 $O(nm)$，空间 $O(nm)$。

### 最佳实用解：滚动一维 DP

一行只依赖上一行和本行左侧。`diagonal` 保存覆盖前的 `dp[j-1]`，即二维表左上角值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestCommonSubsequence(string text1, string text2) {
    if (text1.size() < text2.size()) {
      swap(text1, text2);
    }
    vector<int> dp(text2.size() + 1);
    for (char first : text1) {
      int diagonal = 0;
      for (int j = 1; j <= static_cast<int>(text2.size()); ++j) {
        int previous_row = dp[j];
        if (first == text2[j - 1]) {
          dp[j] = diagonal + 1;
        } else {
          dp[j] = max(dp[j], dp[j - 1]);
        }
        diagonal = previous_row;
      }
    }
    return dp.back();
  }
};
```

时间复杂度 $O(nm)$，空间复杂度 $O(\min(n,m))$。

## 正确性证明

考虑两个前缀的末尾字符。若相等，存在一个最优公共子序列使用这对相等末尾字符：把较早匹配的同字符替换到末尾不会减小长度，因此答案为左上状态加 1。若不等，任何公共子序列不可能同时使用两个不同末尾字符，至少舍弃其中一个，最优值就是上方与左方状态的最大值。

边界 `dp[0][*]=dp[*][0]=0` 对应空串。按前缀长度递增填表，所有依赖均已正确求出，归纳得到最终状态正确。一维压缩只改变存储，不改变依赖值。

## 样例手推

对 `"abcde"` 与 `"ace"`，遇到 `a/a` 时状态升为 1；扫描到 `c/c` 时由左上状态加一得到 2；扫描到 `e/e` 时得到 3。其他不等字符只传播上方或左方最大值，最终答案为 3。

## 易错点与方案比较

- 子序列不要求连续；若要求连续，失配时必须清零，模型变为最长公共子串。
- 二维下标使用前缀长度，访问字符时要减一。
- 一维压缩必须在覆盖前保存左上角；直接使用更新后的 `dp[j-1]` 会破坏递推。
- 若要恢复具体序列，保留二维表最稳妥；只求长度时优先一维 DP。
- 字符相等时直接取左上加一是成立的，不需要再与上、左比较。

## 变种一：恢复一条最长公共子序列

新定义：输出任意一条最长公共子序列。保留完整 DP 表，从右下角反向追踪。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string a, b;
  cin >> a >> b;
  vector<vector<int>> dp(a.size() + 1, vector<int>(b.size() + 1));
  for (int i = 1; i <= static_cast<int>(a.size()); ++i) {
    for (int j = 1; j <= static_cast<int>(b.size()); ++j) {
      if (a[i - 1] == b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  string answer;
  int i = a.size();
  int j = b.size();
  while (i > 0 && j > 0) {
    if (a[i - 1] == b[j - 1]) {
      answer.push_back(a[i - 1]);
      --i;
      --j;
    } else if (dp[i - 1][j] >= dp[i][j - 1]) {
      --i;
    } else {
      --j;
    }
  }
  reverse(answer.begin(), answer.end());
  cout << answer << '\n';
}
```

时间与空间均为 $O(nm)$。并列时不同追踪方向可能得到不同但同样最优的序列。

## 变种二：最长公共子串

新定义：所选字符必须在两个字符串中都连续。令 `dp[j]` 为以当前字符对结尾的公共子串长度；失配时必须置零。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string a, b;
  cin >> a >> b;
  vector<int> dp(b.size() + 1);
  int answer = 0;
  for (int i = 1; i <= static_cast<int>(a.size()); ++i) {
    for (int j = b.size(); j >= 1; --j) {
      if (a[i - 1] == b[j - 1]) {
        dp[j] = dp[j - 1] + 1;
        answer = max(answer, dp[j]);
      } else {
        dp[j] = 0;
      }
    }
  }
  cout << answer << '\n';
}
```

时间 $O(nm)$，空间 $O(m)$。倒序是为了保留上一行的左上角。

## 变种三：三个字符串的最长公共子序列

新定义：求三个字符串共同子序列的最大长度。状态增加一维；三个末尾相等时左上角三维状态加一，否则舍弃任意一个末尾。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string a, b, c;
  cin >> a >> b >> c;
  int n = a.size();
  int m = b.size();
  int p = c.size();
  vector<vector<vector<int>>> dp(n + 1, vector<vector<int>>(m + 1, vector<int>(p + 1)));
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      for (int k = 1; k <= p; ++k) {
        if (a[i - 1] == b[j - 1] && b[j - 1] == c[k - 1]) {
          dp[i][j][k] = dp[i - 1][j - 1][k - 1] + 1;
        } else {
          dp[i][j][k] = max({dp[i - 1][j][k], dp[i][j - 1][k], dp[i][j][k - 1]});
        }
      }
    }
  }
  cout << dp[n][m][p] << '\n';
}
```

时间与空间均为 $O(nmp)$，规模稍大就需要滚动第一维或换模型。

## 变种四：只允许删除时让两个字符串相等

新定义：每次可从任一字符串删除一个字符，求让两串相等的最少删除次数。最终保留的最长部分应当是一个 LCS；保留长度为 $L$ 时，需要删除

$$
|a|-L+|b|-L.
$$

因此先求 LCS 长度，再返回 $|a|+|b|-2L$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string a, b;
  cin >> a >> b;
  vector<int> dp(b.size() + 1);
  for (int i = 1; i <= static_cast<int>(a.size()); ++i) {
    int diagonal = 0;
    for (int j = 1; j <= static_cast<int>(b.size()); ++j) {
      int previous = dp[j];
      if (a[i - 1] == b[j - 1]) {
        dp[j] = diagonal + 1;
      } else {
        dp[j] = max(dp[j], dp[j - 1]);
      }
      diagonal = previous;
    }
  }
  cout << a.size() + b.size() - 2 * dp.back() << '\n';
}
```

时间 $O(nm)$，空间 $O(m)$。若允许替换操作，模型会变为完整编辑距离，不能再只看 LCS。

## 可复现验证

- 三个官方样例、完全相同、完全不交、单字符与大量重复字符均应覆盖。
- 短字符串可枚举所有子序列集合，作为长度与恢复结果的 oracle。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/longest-common-subsequence/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/longest-common-subsequence/)
- [对应知识专题](../../dp/sequence-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-47-lc160/">← [力扣 Top 47] LC 160 相交链表 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-49-lc45/">[力扣 Top 49] LC 45 跳跃游戏 II 中等 →</a>
</nav>
