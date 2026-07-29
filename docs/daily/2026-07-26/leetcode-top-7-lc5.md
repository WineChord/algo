---
title: "[力扣 Top 7] LC 5 最长回文子串 中等"
---

# [力扣 Top 7] LC 5 最长回文子串 中等

<p class="daily-archive-kicker">2026-07-26 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../strings/palindrome-centers.md">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：https://leetcode.cn/problems/longest-palindromic-substring/
- 函数签名：`string longestPalindrome(string s)`

### 原始题意

给定字符串 `s`，返回其中长度最大的连续回文子串。若有多个最长答案，返回任意一个。

### 全部官方样例

1. `s = "babad"`，输出可以是 `"bab"`，`"aba"` 也正确。
2. `s = "cbbd"`，输出 `"bb"`。

### 全部约束

- $1\le |s|\le 1000$
- `s` 只由数字和英文字母组成

## 最优结论

中心扩展枚举 $2n-1$ 个奇偶中心，每个中心向两侧扩张并更新最长区间，时间 $O(n^2)$、额外空间 $O(1)$，是本题约束下最推荐的实用解。若追求严格最优渐进复杂度，Manacher 算法可达 $O(n)$ 时间与 $O(n)$ 空间。

## 约束、边界与观察

- “子串”必须连续，不能用最长回文子序列的状态。
- 回文有奇数中心和偶数中心，两类必须都覆盖。
- $n\le1000$ 允许 $O(n^2)$，但 $O(n^3)$ 枚举加检查最坏约 $10^9$ 次字符比较。
- 单字符总是回文，因此答案一定存在。

## 样例手推

对 `"cbbd"`，以两个 `b` 之间为偶中心，第一次比较得到 `"bb"`，再向外比较 `c` 与 `d` 失败，最长区间为 `[1,2]`。

## 解法一：枚举并检查每个子串

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool isPalindrome(const string& s, int l, int r) {
    while (l < r) {
      if (s[l++] != s[r--]) return false;
    }
    return true;
  }
public:
  string longestPalindrome(string s) {
    int bestL = 0, bestLen = 1;
    for (int l = 0; l < (int)s.size(); ++l) {
      for (int r = l; r < (int)s.size(); ++r) {
        int len = r - l + 1;
        if (len > bestLen && isPalindrome(s, l, r)) {
          bestL = l;
          bestLen = len;
        }
      }
    }
    return s.substr(bestL, bestLen);
  }
};
```

时间 $O(n^3)$，空间 $O(1)$。相邻子串反复比较相同的内部区域。

## 解法二：区间动态规划

令 `dp[l][r]` 表示 `s[l..r]` 是否为回文。转移为两端相等且内部长度不超过 1，或内部也是回文。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindrome(string s) {
    int n = s.size();
    vector<vector<char>> dp(n, vector<char>(n));
    int bestL = 0, bestLen = 1;
    for (int r = 0; r < n; ++r) {
      for (int l = r; l >= 0; --l) {
        dp[l][r] = s[l] == s[r] && (r - l <= 2 || dp[l + 1][r - 1]);
        if (dp[l][r] && r - l + 1 > bestLen) {
          bestL = l;
          bestLen = r - l + 1;
        }
      }
    }
    return s.substr(bestL, bestLen);
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$。它把内部回文结果复用起来，但保存了远多于最终答案所需的状态。

## 解法三：中心扩展（最佳实用解）

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindrome(string s) {
    int n = s.size();
    int bestL = 0, bestLen = 1;
    auto expand = [&](int l, int r) {
      while (l >= 0 && r < n && s[l] == s[r]) {
        --l;
        ++r;
      }
      int len = r - l - 1;
      if (len > bestLen) {
        bestL = l + 1;
        bestLen = len;
      }
    };
    for (int i = 0; i < n; ++i) {
      expand(i, i);
      expand(i, i + 1);
    }
    return s.substr(bestL, bestLen);
  }
};
```

每个回文子串都有唯一的奇中心或偶中心，因此枚举全部中心不会漏解。对固定中心，扩张循环结束前枚举了该中心所有回文半径；所记录的最大半径就是该中心的最长回文。取所有中心最大值即为全局最长回文。

时间 $O(n^2)$，额外空间 $O(1)$。

## 解法四：Manacher 线性算法

插入分隔符统一奇偶回文。`p[i]` 表示变换串中以 `i` 为中心的最大半径，利用当前最右回文区间及镜像位置复用已知半径。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindrome(string s) {
    string t = "^";
    for (char c : s) {
      t.push_back('#');
      t.push_back(c);
    }
    t += "#$";
    vector<int> p(t.size());
    int center = 0, right = 0;
    int bestCenter = 0, bestLen = 0;
    for (int i = 1; i + 1 < (int)t.size(); ++i) {
      int mirror = 2 * center - i;
      if (i < right) p[i] = min(right - i, p[mirror]);
      while (t[i + 1 + p[i]] == t[i - 1 - p[i]]) ++p[i];
      if (i + p[i] > right) {
        center = i;
        right = i + p[i];
      }
      if (p[i] > bestLen) {
        bestLen = p[i];
        bestCenter = i;
      }
    }
    int start = (bestCenter - bestLen) / 2;
    return s.substr(start, bestLen);
  }
};
```

每个字符只会推动最右边界向右，总时间 $O(n)$，空间 $O(n)$。它渐进最优，但边界与坐标映射更易写错；本题 $n\le1000$ 时面试优先中心扩展，明确要求线性时再写 Manacher。

## 常见错误

- 只扩展 `(i,i)`，漏掉 `"cbbd"` 的偶数回文。
- 扩展退出后把长度写成 `r-l+1`；此时两端已经越界，应为 `r-l-1`。
- DP 按错误方向枚举，读取尚未计算的 `dp[l+1][r-1]`。
- 把“任意一个最长答案”误读为必须返回最早或字典序最小者。
- Manacher 的原串起点换算少除以 2。

## Follow-up 1：并列时返回最早出现者

只在长度严格变大时更新；中心从左到右枚举即可保留最早起点。为使规则显式，也可比较起点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindromeEarliest(string s) {
    int n = s.size(), bestL = 0, bestLen = 1;
    auto expand = [&](int l, int r) {
      while (l >= 0 && r < n && s[l] == s[r]) {
        --l;
        ++r;
      }
      int start = l + 1, len = r - l - 1;
      if (len > bestLen || (len == bestLen && start < bestL)) {
        bestL = start;
        bestLen = len;
      }
    };
    for (int i = 0; i < n; ++i) {
      expand(i, i);
      expand(i, i + 1);
    }
    return s.substr(bestL, bestLen);
  }
};
```

时间 $O(n^2)$，空间 $O(1)$。

## Follow-up 2：统计所有回文子串

对应 [LeetCode 647 · 回文子串](https://leetcode.cn/problems/palindromic-substrings/)。每次成功扩张都恰好发现一个由该中心唯一标识的回文。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countSubstrings(string s) {
    int n = s.size(), ans = 0;
    auto countFrom = [&](int l, int r) {
      int count = 0;
      while (l >= 0 && r < n && s[l] == s[r]) {
        ++count;
        --l;
        ++r;
      }
      return count;
    };
    for (int i = 0; i < n; ++i) {
      ans += countFrom(i, i);
      ans += countFrom(i, i + 1);
    }
    return ans;
  }
};
```

时间 $O(n^2)$，空间 $O(1)$。

## Follow-up 3：改为最长回文子序列

对应 [LeetCode 516 · 最长回文子序列](https://leetcode.cn/problems/longest-palindromic-subsequence/)。字符可以跳过，中心扩展不再覆盖全部选择；使用区间 DP。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestPalindromeSubseq(string s) {
    int n = s.size();
    vector<vector<int>> dp(n, vector<int>(n));
    for (int i = n - 1; i >= 0; --i) {
      dp[i][i] = 1;
      for (int j = i + 1; j < n; ++j) {
        if (s[i] == s[j]) {
          dp[i][j] = 2 + (i + 1 <= j - 1 ? dp[i + 1][j - 1] : 0);
        } else {
          dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
        }
      }
    }
    return dp[0][n - 1];
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$。

## Follow-up 4：在字符串前添加最少字符使其成为回文

对应 [LeetCode 214 · 最短回文串](https://leetcode.cn/problems/shortest-palindrome/)。关键变为寻找最长回文前缀，可对 `s + "#" + reverse(s)` 计算 KMP 前缀函数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string shortestPalindrome(string s) {
    string rev = s;
    reverse(rev.begin(), rev.end());
    string t = s + "#" + rev;
    vector<int> pi(t.size());
    for (int i = 1; i < (int)t.size(); ++i) {
      int j = pi[i - 1];
      while (j > 0 && t[i] != t[j]) j = pi[j - 1];
      if (t[i] == t[j]) ++j;
      pi[i] = j;
    }
    string add = s.substr(pi.back());
    reverse(add.begin(), add.end());
    return add + s;
  }
};
```

时间 $O(n)$，空间 $O(n)$。

## 验证

随机生成长度 $1\ldots12$、字符集 `abc` 的字符串，以三重枚举为 oracle，比较中心扩展和 Manacher 返回长度，并逐字符验证返回值确为原串子串且为回文。边界覆盖单字符、全相同、全不同、奇偶最长回文并列和最长回文位于两端。

## Reference

- [官方题目](https://leetcode.cn/problems/longest-palindromic-substring/)
- [对应知识专题](../../strings/palindrome-centers.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-6-lc49.md">← [力扣 Top 6] LC 49 字母异位词分组 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-8-lc128.md">[力扣 Top 8] LC 128 最长连续序列 中等 →</a>
</nav>
