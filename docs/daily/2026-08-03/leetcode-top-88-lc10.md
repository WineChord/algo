---
title: "[力扣 Top 88] LC 10 正则表达式匹配 困难"
---

# [力扣 Top 88] LC 10 正则表达式匹配 困难

<p class="daily-archive-kicker">2026-08-03 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../dp/string-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=312d2f80ccda8d55d73e58e68c148f3b00bacc0e2cadaf1d9dfaa043a78a45d3 -->
## 官方原始信息

- Top 排名：88
- 题号：LC 10
- 官方中文标题：正则表达式匹配
- 官方难度：困难
- 官方链接：[正则表达式匹配](https://leetcode.cn/problems/regular-expression-matching/)

### 原始题意

给定字符串 `s` 与模式 `p`，实现完整字符串匹配。`.` 匹配任意单个字符，`*` 表示其前一个元素重复零次或多次；匹配必须覆盖 `s` 的全部字符。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool isMatch(string s, string p);
};
```

### 全部官方样例

```text
输入：s = "aa", p = "a"
输出：false
解释：模式不能覆盖整个字符串。
```

```text
输入：s = "aa", p = "a*"
输出：true
解释：`*` 让 `a` 重复两次。
```

```text
输入：s = "ab", p = ".*"
输出：true
解释：`.*` 可以匹配任意字符串。
```

### 全部约束

- $1\le s.length\le20$。
- $1\le p.length\le20$。
- `s` 只含小写英文字母。
- `p` 只含小写英文字母、`.` 与 `*`。
- 每个 `*` 都保证有合法前导元素。

## 约束推导与状态

每个 `*` 都能选择匹配 0、1、2……个字符，直接回溯会反复探索同一字符串前缀与模式前缀。定义 `dp[i][j]` 表示 `s` 的前 $i$ 个字符是否与 `p` 的前 $j$ 个字符完整匹配。

普通字符或 `.` 只能消费双方各一个字符。若 `p[j-1]=='*'`，则有两类互斥来源：

- 重复零次：丢弃模式末尾的 `x*`，看 `dp[i][j-2]`；
- 重复至少一次：当前字符能与 `x` 匹配，并由同一个 `x*` 继续承担前 $i-1$ 个字符，即 `dp[i-1][j]`。

空字符串只可能被若干 `x*` 匹配，因此初始化 `dp[0][j]=dp[0][j-2]`。表仅 $21\times21$，无性能风险。

## 解法递进

### 解法一：按 `*` 两种选择递归

从字符串与模式当前下标出发。若下一模式字符是 `*`，选择跳过 `x*` 或在首字符匹配时消费一个字符串字符并保留模式位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool search(const string& s, const string& p, int i, int j) {
    if (j == static_cast<int>(p.size())) {
      return i == static_cast<int>(s.size());
    }
    bool firstMatches = i < static_cast<int>(s.size()) && (p[j] == '.' || p[j] == s[i]);
    if (j + 1 < static_cast<int>(p.size()) && p[j + 1] == '*') {
      return search(s, p, i, j + 2) || (firstMatches && search(s, p, i + 1, j));
    }
    return firstMatches && search(s, p, i + 1, j + 1);
  }
public:
  bool isMatch(string s, string p) {
    return search(s, p, 0, 0);
  }
};
```

最坏时间指数级，递归栈 $O(n+m)$，适合作为短串 oracle。

### 解法二：记忆化递归

给每个 `(i,j)` 缓存真假，令每个状态只计算一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> memo;
  bool search(const string& s, const string& p, int i, int j) {
    int& result = memo[i][j];
    if (result != -1)
      return result;
    if (j == static_cast<int>(p.size()))
      return result = i == static_cast<int>(s.size());
    bool firstMatches = i < static_cast<int>(s.size()) && (p[j] == '.' || p[j] == s[i]);
    if (j + 1 < static_cast<int>(p.size()) && p[j + 1] == '*') {
      return result = search(s, p, i, j + 2) || (firstMatches && search(s, p, i + 1, j));
    }
    return result = firstMatches && search(s, p, i + 1, j + 1);
  }
public:
  bool isMatch(string s, string p) {
    memo.assign(s.size() + 1, vector<int>(p.size() + 1, -1));
    return search(s, p, 0, 0);
  }
};
```

时间 $O(nm)$，空间 $O(nm)$ 加递归栈。

### 最佳实用解：前缀动态规划

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isMatch(string s, string p) {
    int n = s.size();
    int m = p.size();
    vector<vector<char>> dp(n + 1, vector<char>(m + 1));
    dp[0][0] = true;
    for (int j = 2; j <= m; ++j) {
      if (p[j - 1] == '*')
        dp[0][j] = dp[0][j - 2];
    }
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= m; ++j) {
        if (p[j - 1] == '*') {
          dp[i][j] = dp[i][j - 2];
          bool matches = p[j - 2] == '.' || p[j - 2] == s[i - 1];
          dp[i][j] |= matches && dp[i - 1][j];
        } else {
          bool matches = p[j - 1] == '.' || p[j - 1] == s[i - 1];
          dp[i][j] = matches && dp[i - 1][j - 1];
        }
      }
    }
    return dp[n][m];
  }
};
```

时间 $O(nm)$，空间 $O(nm)$。表格不受递归深度影响，初始化与转移边界清楚，是最佳实用解。

## 正确性证明

对 `(i,j)` 的前缀长度和归纳。普通末字符要完整匹配，必须二者字符相容且此前前缀匹配，转移充分必要。末尾为 `x*` 时，任一完整匹配中 `x*` 要么使用零次，对应删掉它后的 `dp[i][j-2]`；要么使用至少一次，此时末字符必须与 `x` 相容，移除这一次匹配后仍由同一 `x*` 匹配更短字符串，对应 `dp[i-1][j]`。两类覆盖所有重复次数。空串初始化恰好连续跳过零次 `x*`。故整表语义成立，`dp[n][m]` 正确。

## 样例手推

`s="aa",p="a*"`：`dp[0][2]=true` 表示 `a*` 取零次；`dp[1][2]` 由字符匹配与 `dp[0][2]` 得真；`dp[2][2]` 再由 `dp[1][2]` 得真。`s="aa",p="a"` 只能消费一个字符，`dp[2][1]=false`。`.*` 中点号与任意字符相容，星号可反复使用，因而匹配 `ab`。

## 易错点与方案比较

- 题目要求完整匹配，不是子串搜索。
- `*` 修饰前一个元素，转移读取 `p[j-2]`；输入保证 `*` 不会出现在非法首位。
- `x*` 取零次时模式退两格，取至少一次时字符串退一格而模式不退。
- 空串初始化不能把所有偶数长度模式都置真，必须逐个确认末尾是 `*` 且前态可达。
- 记忆化更贴近语义，表格 DP 更便于审查边界和恢复路径；推荐表格版。

## 变种一：通配符 `?` 与 `*`

新定义：`?` 匹配一个任意字符，`*` 自身匹配任意长度字符串，不再修饰前导元素。`*` 的转移变为跳过自身或消费一个字符。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, pattern;
  cin >> s >> pattern;
  vector<vector<char>> dp(s.size() + 1, vector<char>(pattern.size() + 1));
  dp[0][0] = true;
  for (int j = 1; j <= static_cast<int>(pattern.size()); ++j) {
    if (pattern[j - 1] == '*')
      dp[0][j] = dp[0][j - 1];
  }
  for (int i = 1; i <= static_cast<int>(s.size()); ++i) {
    for (int j = 1; j <= static_cast<int>(pattern.size()); ++j) {
      if (pattern[j - 1] == '*') {
        dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
      } else {
        dp[i][j] = (pattern[j - 1] == '?' || pattern[j - 1] == s[i - 1]) && dp[i - 1][j - 1];
      }
    }
  }
  cout << (dp[s.size()][pattern.size()] ? "YES" : "NO") << '\n';
}
```

时间 $O(nm)$，空间 $O(nm)$；不能把两种星号语义混用。

## 变种二：加入 `+` 量词

新定义：`x+` 表示前导元素重复至少一次。预处理把每个 `x+` 改写为 `xx*`，再运行原 DP；该等价式保留至少一次的第一份 `x`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, inputPattern;
  cin >> s >> inputPattern;
  string pattern;
  for (char token : inputPattern) {
    if (token == '+') {
      pattern.push_back(pattern.back());
      pattern.push_back('*');
    } else {
      pattern.push_back(token);
    }
  }
  vector<vector<char>> dp(s.size() + 1, vector<char>(pattern.size() + 1));
  dp[0][0] = true;
  for (int j = 2; j <= static_cast<int>(pattern.size()); ++j) {
    if (pattern[j - 1] == '*')
      dp[0][j] = dp[0][j - 2];
  }
  for (int i = 1; i <= static_cast<int>(s.size()); ++i) {
    for (int j = 1; j <= static_cast<int>(pattern.size()); ++j) {
      if (pattern[j - 1] == '*') {
        bool matches = pattern[j - 2] == '.' || pattern[j - 2] == s[i - 1];
        dp[i][j] = dp[i][j - 2] || (matches && dp[i - 1][j]);
      } else {
        bool matches = pattern[j - 1] == '.' || pattern[j - 1] == s[i - 1];
        dp[i][j] = matches && dp[i - 1][j - 1];
      }
    }
  }
  cout << (dp[s.size()][pattern.size()] ? "YES" : "NO") << '\n';
}
```

预处理和 DP 总时间 $O(nm)$，空间 $O(nm)$；输入应保证 `+` 有合法前导元素。

## 变种三：恢复每个星号匹配的字符数

新定义：输出一种成功解析中每个模式元素消耗的字符数。DP 保存父转移，回溯时 `dp[i-1][j]` 对当前 `x*` 的计数加一，跳过 `x*` 时记零。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, p;
  cin >> s >> p;
  int n = s.size(), m = p.size();
  vector<vector<char>> dp(n + 1, vector<char>(m + 1));
  vector<vector<char>> parent(n + 1, vector<char>(m + 1));
  dp[0][0] = true;
  for (int j = 2; j <= m; ++j) {
    if (p[j - 1] == '*' && dp[0][j - 2])
      dp[0][j] = true, parent[0][j] = 'Z';
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      if (p[j - 1] == '*') {
        if (dp[i][j - 2])
          dp[i][j] = true, parent[i][j] = 'Z';
        bool match = p[j - 2] == '.' || p[j - 2] == s[i - 1];
        if (!dp[i][j] && match && dp[i - 1][j])
          dp[i][j] = true, parent[i][j] = 'R';
      } else {
        bool match = p[j - 1] == '.' || p[j - 1] == s[i - 1];
        if (match && dp[i - 1][j - 1])
          dp[i][j] = true, parent[i][j] = 'O';
      }
    }
  }
  if (!dp[n][m]) {
    cout << "NO\n";
    return 0;
  }
  vector<int> repetitions(m);
  for (int i = n, j = m; i || j;) {
    if (parent[i][j] == 'R')
      ++repetitions[j - 1], --i;
    else if (parent[i][j] == 'Z')
      j -= 2;
    else
      --i, --j;
  }
  cout << "YES\n";
  for (int j = 1; j < m; ++j) {
    if (p[j] == '*')
      cout << j << ' ' << repetitions[j] << '\n';
  }
}
```

时间 $O(nm)$，空间 $O(nm)$。多种解析存在时，父指针确定其中一种。

## 变种四：寻找第一个匹配子串

新定义：模式不必覆盖全文，输出最小起点及在该起点下最短的匹配非空子串。枚举起点与终点，并调用同一完整匹配 DP；适合原约束的小规模版本。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool fullMatch(const string& s, const string& p) {
  vector<vector<char>> dp(s.size() + 1, vector<char>(p.size() + 1));
  dp[0][0] = true;
  for (int j = 2; j <= static_cast<int>(p.size()); ++j) {
    if (p[j - 1] == '*')
      dp[0][j] = dp[0][j - 2];
  }
  for (int i = 1; i <= static_cast<int>(s.size()); ++i) {
    for (int j = 1; j <= static_cast<int>(p.size()); ++j) {
      if (p[j - 1] == '*') {
        bool match = p[j - 2] == '.' || p[j - 2] == s[i - 1];
        dp[i][j] = dp[i][j - 2] || (match && dp[i - 1][j]);
      } else {
        bool match = p[j - 1] == '.' || p[j - 1] == s[i - 1];
        dp[i][j] = match && dp[i - 1][j - 1];
      }
    }
  }
  return dp[s.size()][p.size()];
}
int main() {
  string text, pattern;
  cin >> text >> pattern;
  for (int left = 0; left < static_cast<int>(text.size()); ++left) {
    for (int right = left + 1; right <= static_cast<int>(text.size()); ++right) {
      if (fullMatch(text.substr(left, right - left), pattern)) {
        cout << left << ' ' << right - 1 << '\n';
        return 0;
      }
    }
  }
  cout << -1 << '\n';
}
```

时间 $O(n^3m)$（含子串与重复 DP），空间 $O(nm)$。规模放大时应构建 NFA 并一次扫描文本。

## 验证说明

本轮将七段代码按 C++23 编译；表格 DP 会与递归定义在随机长度不超过 7 的字符串与合法模式上对拍，并复核三个官方样例、空匹配链 `a*b*`、多个星号、点号与完整匹配边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/regular-expression-matching/)
- [对应知识专题](../../dp/string-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-87-lc148/">← [力扣 Top 87] LC 148 排序链表 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-89-lc98/">[力扣 Top 89] LC 98 验证二叉搜索树 中等 →</a>
</nav>
