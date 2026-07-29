---
title: "[力扣 Top 21] LC 20 有效的括号 简单"
---

# [力扣 Top 21] LC 20 有效的括号 简单

<p class="daily-archive-kicker">2026-07-28 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-28 题目列表</a> · <a href="../../data-structures/index.md">进入知识专题</a></p>

## 官方原始信息

- 难度：LeetCode 官方「简单」；非竞赛题，官方分值与 ZeroTracer 社区估算竞赛分均无可用值。
- 官方链接：https://leetcode.cn/problems/valid-parentheses/
- slug：`valid-parentheses`
- 函数签名：`bool isValid(string s)`
- 题意：字符串只含 `()[]{}`。判断每个左括号是否被同类型右括号按正确嵌套顺序闭合，且每个右括号都有对应左括号。
- 示例：`"()" -> true`；`"()[]{}" -> true`；`"(]" -> false`；`"([])" -> true`；`"([)]" -> false`。
- 约束：$1\le |s|\le10^4$；字符仅来自 `()[]{}`。

## 约束、样例与边界

线性扫描是目标复杂度；最深嵌套可达 $|s|/2$，栈空间最坏 $O(n)$。奇数长度必不合法，可提前返回。空栈遇右括号、类型错配、扫描后仍有左括号都必须失败。`"([)]"` 说明仅统计三类括号数量不够，顺序才是核心。

## 暴力：反复消去相邻匹配对

任何合法括号串都存在最内层相邻匹配对；反复删除 `()`、`[]`、`{}`，最终为空当且仅当原串合法。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isValid(string s) {
    bool changed = true;
    while (changed) {
      changed = false;
      string next;
      for (int i = 0; i < (int)s.size();) {
        if (i + 1 < (int)s.size() &&
            ((s[i] == '(' && s[i + 1] == ')') ||
            (s[i] == '[' && s[i + 1] == ']') ||
            (s[i] == '{' && s[i + 1] == '}'))) {
          i += 2;
          changed = true;
        } else {
          next.push_back(s[i++]);
        }
      }
      s.swap(next);
    }
    return s.empty();
  }
};
```

最坏需要 $O(n)$ 轮、每轮 $O(n)$，时间 $O(n^2)$，空间 $O(n)$。瓶颈是每轮重新扫描已知无法立即消去的字符。

## 最优：栈保存尚未闭合的左括号

遇左括号入栈；遇右括号时，它只能闭合当前最内层、也就是栈顶左括号。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool isValid(string s) {
    if (s.size() % 2) return false;
    unordered_map<char, char> need{{')', '('}, {']', '['}, {'}', '{'}};
    vector<char> st;
    for (char c : s) {
      if (!need.count(c)) {
        st.push_back(c);
      } else {
        if (st.empty() || st.back() != need[c]) return false;
        st.pop_back();
      }
    }
    return st.empty();
  }
};
```

循环不变量：处理完前缀后，`st` 自底向上恰好保存该前缀尚未匹配的左括号。右括号若不能匹配栈顶，则任何后续字符也无法修复已经违反的嵌套次序；若扫描结束栈为空，所有括号恰好配对。时间 $O(n)$，空间 $O(n)$，达到必须读取全部字符的下界。

样例 `"([])"` 的栈依次为 `(`、`([`、`(`、空；`"([)]"` 在读到 `)` 时栈顶为 `[`，立即失败。竞赛优先记忆栈解，因为不变量直接对应语法嵌套；暴力消去适合作为小规模 oracle。

## Follow-up 1：返回第一处错误位置

新定义：合法返回 `-1`；否则返回第一个无法匹配的右括号下标。若仅因左括号未闭合，则返回最早仍未闭合左括号的下标。栈需同时保存位置。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int firstBracketError(const string& s) {
  unordered_map<char, char> need{{')', '('}, {']', '['}, {'}', '{'}};
  vector<pair<char, int>> st;
  for (int i = 0; i < (int)s.size(); ++i) {
    char c = s[i];
    if (!need.count(c)) {
      st.push_back({c, i});
    } else {
      if (st.empty() || st.back().first != need[c]) return i;
      st.pop_back();
    }
  }
  return st.empty() ? -1 : st.front().second;
}
```

时间 $O(n)$，空间 $O(n)$。

## Follow-up 2：加入通配符 `*`

新定义：只含 `(`、`)`、`*`，其中 `*` 可解释为空、左括号或右括号。确定栈失效，因为同一前缀有多种可能状态；维护未闭合左括号数量的最小值与最大值区间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  bool checkValidString(string s) {
    int low = 0, high = 0;
    for (char c : s) {
      if (c == '(') {
        ++low;
        ++high;
      } else if (c == ')') {
        low = max(0, low - 1);
        --high;
      } else {
        low = max(0, low - 1);
        ++high;
      }
      if (high < 0) return false;
    }
    return low == 0;
  }
};
```

时间 $O(n)$，空间 $O(1)$；对应 LC 678。

## Follow-up 3：删除最少字符使圆括号合法

新定义：字符串含普通字符和圆括号，删除最少括号后返回任一合法结果。一次扫描删除无匹配左括号的 `)`，再删除栈中剩余的 `(`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string minRemoveToMakeValid(string s) {
    vector<int> st;
    vector<bool> removed(s.size());
    for (int i = 0; i < (int)s.size(); ++i) {
      if (s[i] == '(') st.push_back(i);
      if (s[i] == ')') {
        if (st.empty()) removed[i] = true;
        else st.pop_back();
      }
    }
    for (int i : st) removed[i] = true;
    string ans;
    for (int i = 0; i < (int)s.size(); ++i) {
      if (!removed[i]) ans.push_back(s[i]);
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(n)$；对应 LC 1249。

## Follow-up 4：最长合法圆括号子串

新定义：求连续子串的最大合法长度。栈要保存“最近无法跨越的边界”与左括号下标，而不是字符类型。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestValidParentheses(string s) {
    vector<int> st{-1};
    int ans = 0;
    for (int i = 0; i < (int)s.size(); ++i) {
      if (s[i] == '(') {
        st.push_back(i);
      } else {
        st.pop_back();
        if (st.empty()) st.push_back(i);
        else ans = max(ans, i - st.back());
      }
    }
    return ans;
  }
};
```

时间 $O(n)$，空间 $O(n)$；对应 LC 32。

## Follow-up 5：生成全部合法括号串

新定义：给定 $n$ 对圆括号，生成所有合法串。验证变成构造；前缀中右括号数不得超过左括号数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<string> ans;
  void dfs(int n, int open, int close, string& path) {
    if ((int)path.size() == 2 * n) {
      ans.push_back(path);
      return;
    }
    if (open < n) {
      path.push_back('(');
      dfs(n, open + 1, close, path);
      path.pop_back();
    }
    if (close < open) {
      path.push_back(')');
      dfs(n, open, close + 1, path);
      path.pop_back();
    }
  }
public:
  vector<string> generateParenthesis(int n) {
    string path;
    dfs(n, 0, 0, path);
    return ans;
  }
};
```

输出规模为第 $n$ 个 Catalan 数，时间 $O(C_n n)$，递归空间 $O(n)$；对应 LC 22。

## 易错点与验证

- 数量相等不代表嵌套顺序正确。
- 右括号前必须检查空栈。
- 扫描结束仍要检查栈空。
- 重复消去法每轮必须基于本轮剩余串。
- 随机验证：对长度 $0\ldots12$ 的随机括号串比较消去法与栈法；另覆盖单字符、全左、全右、类型错配和最大嵌套。

## Reference

- [官方题目](https://leetcode.cn/problems/valid-parentheses/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="atcoder-abc468-c.md">← [atcoder] ABC468 C Between P and Q</a>
<a class="daily-archive-pager__next" href="leetcode-top-22-lc206.md">[力扣 Top 22] LC 206 反转链表 简单 →</a>
</nav>
