---
title: "[力扣 Top 50] LC 32 最长有效括号 困难"
---

# [力扣 Top 50] LC 32 最长有效括号 困难

<p class="daily-archive-kicker">2026-07-30 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=6a28bb6c5729fa37643f1c73eaa3f27ca1ae6a28c16afd55bb7b8dde7402b27d -->
## 官方原始信息

- Top 排名：50
- 题号：LC 32
- 官方中文标题：最长有效括号
- 官方难度：困难
- 官方链接：[最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/)

### 原始题意

给定只含 `(` 和 `)` 的字符串，求最长连续且格式正确的括号子串长度。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int longestValidParentheses(string s);
};
```

### 全部官方样例

```text
输入：s = "(()"
输出：2
解释：最长有效子串为 "()"。
```

```text
输入：s = ")()())"
输出：4
解释：最长有效子串为 "()()"。
```

```text
输入：s = ""
输出：0
```

### 全部约束

- $0\le |s|\le3\times10^4$。
- 每个字符为 `(` 或 `)`。
- 答案一定为偶数且不超过字符串长度。

## 约束推导与边界

枚举所有子串并检查平衡最坏 $O(n^3)$；增量维护平衡可降到 $O(n^2)$，仍不理想。有效括号串具有递归结构：它要么在某个 `)` 处新闭合一对并连接前面的有效段，要么被无法匹配的 `)` 截断。DP、栈和双向计数都能达到线性时间。

## 解法递进

### 解法一：枚举起点并维护平衡

从每个起点向右扫描，`(` 加一、`)` 减一；平衡为 0 时更新答案，变负时停止。时间 $O(n^2)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestValidParentheses(string s) {
    int answer = 0;
    for (int left = 0; left < static_cast<int>(s.size()); ++left) {
      int balance = 0;
      for (int right = left; right < static_cast<int>(s.size()); ++right) {
        balance += s[right] == '(' ? 1 : -1;
        if (balance < 0) {
          break;
        }
        if (balance == 0) {
          answer = max(answer, right - left + 1);
        }
      }
    }
    return answer;
  }
};
```

### 解法二：以当前位置结尾的动态规划

`dp[i]` 表示以 `s[i]` 结尾的最长有效子串长度。只有 `s[i]=')'` 才可能非零；跳过前一个有效段后，检查它前面的字符是否为 `(`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestValidParentheses(string s) {
    vector<int> dp(s.size());
    int answer = 0;
    for (int i = 1; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '(') {
        continue;
      }
      int opening = i - dp[i - 1] - 1;
      if (opening >= 0 && s[opening] == '(') {
        dp[i] = dp[i - 1] + 2;
        if (opening > 0) {
          dp[i] += dp[opening - 1];
        }
        answer = max(answer, dp[i]);
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(n)$。

### 最佳实用解：栈保存未匹配位置

栈先放入虚拟边界 -1。遇到 `(` 压入下标；遇到 `)` 先弹出一个候选左括号。若栈空，当前 `)` 成为新失效边界；否则当前有效后缀长度是 `i-stack.top()`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int longestValidParentheses(string s) {
    vector<int> stack = {-1};
    int answer = 0;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '(') {
        stack.push_back(i);
      } else {
        stack.pop_back();
        if (stack.empty()) {
          stack.push_back(i);
        } else {
          answer = max(answer, i - stack.back());
        }
      }
    }
    return answer;
  }
};
```

时间复杂度 $O(n)$，空间复杂度 $O(n)$。若只求长度，也可用左右两次扫描把空间降为 $O(1)$。

## 正确性证明

栈中除底部边界外，保存尚未被匹配的左括号下标。处理右括号时：

- 若能弹出一个左括号，当前右括号与它配对；弹出后栈顶是当前有效后缀之前最近的未匹配位置，所以二者下标差就是以当前字符结尾的最长有效长度。
- 若弹出后栈空，说明右括号过多，任何跨过当前位置的子串都不可能有效，因此把当前位置设为新边界。

每个以右括号结尾的有效子串都在对应时刻被计算，取最大值即为全局最长。

## 样例手推

对 `")()())"`，初始栈为 `[-1]`。位置 0 的 `)` 使栈空，于是边界改为 0。位置 1 的 `(` 入栈；位置 2 的 `)` 匹配后长度为 $2-0=2$。位置 3、4 再闭合一对后长度为 $4-0=4$。位置 5 的多余 `)` 建立新边界，最终答案为 4。

## 易错点与方案比较

- 栈需要虚拟边界 -1，否则从下标 0 开始的有效串长度难以统一计算。
- 遇到 `)` 必须先弹，再判断栈是否为空。
- 题目求连续子串，不是可删除字符的最长合法子序列。
- DP 最适合扩展到计数或恢复；栈方案最直观稳健；双向计数空间最省但不直接恢复区间。
- 空字符串答案为 0，栈初始化后不需特殊处理。

## 变种一：返回最长区间

新定义：返回一个最长有效括号子串的左右下标；并列取最小左端点。栈方案更新长度时同步保存区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  vector<int> stack = {-1};
  int best_length = 0;
  int best_left = -1;
  int best_right = -1;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '(') {
      stack.push_back(i);
      continue;
    }
    stack.pop_back();
    if (stack.empty()) {
      stack.push_back(i);
      continue;
    }
    int length = i - stack.back();
    int left = stack.back() + 1;
    if (length > best_length || (length == best_length && left < best_left)) {
      best_length = length;
      best_left = left;
      best_right = i;
    }
  }
  cout << best_length << ' ' << best_left << ' ' << best_right << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种二：统计所有有效括号子串

新定义：统计连续且格式正确的子串个数。对每个右括号找到与之匹配的左括号 `open`；以当前右括号结尾的有效子串数量等于 1 加上紧邻前一段结尾处的数量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  vector<int> length(s.size());
  vector<long long> count(s.size());
  long long answer = 0;
  for (int i = 1; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '(') {
      continue;
    }
    int open = i - length[i - 1] - 1;
    if (open >= 0 && s[open] == '(') {
      length[i] = length[i - 1] + 2;
      if (open > 0) {
        length[i] += length[open - 1];
        count[i] = count[open - 1];
      }
      ++count[i];
      answer += count[i];
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。`long long` 用于最多 $O(n^2)$ 个子串的计数。

## 变种三：支持三种括号

新定义：字符串可含 `()[]{}`，要求类型正确且嵌套合法，求最长连续合法子串。栈保存未匹配左括号；类型不匹配的右括号直接清空并更新失效边界。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool match(char left, char right) {
  return (left == '(' && right == ')') || (left == '[' && right == ']') ||
      (left == '{' && right == '}');
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  vector<int> stack;
  int boundary = -1;
  int answer = 0;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    if (s[i] == '(' || s[i] == '[' || s[i] == '{') {
      stack.push_back(i);
    } else if (!stack.empty() && match(s[stack.back()], s[i])) {
      stack.pop_back();
      int left_boundary = stack.empty() ? boundary : stack.back();
      answer = max(answer, i - left_boundary);
    } else {
      stack.clear();
      boundary = i;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。原题只看左右括号数量的双向计数法在多类型括号下会失效。

## 变种四：最少删除字符使整个字符串合法

新定义：可删除括号，求最少删除数，使剩余序列成为合法括号串。扫描时统计未匹配左括号；遇到多余右括号就计一次删除，最后再删除剩余左括号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int open = 0;
  int deletions = 0;
  for (char ch : s) {
    if (ch == '(') {
      ++open;
    } else if (open > 0) {
      --open;
    } else {
      ++deletions;
    }
  }
  cout << deletions + open << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。这已从“最长连续子串”改成“允许删除的全局序列修复”，原单调边界模型不再是目标。

## 可复现验证

- 三个官方样例、全左括号、全右括号、完全合法、嵌套与并列有效段均应覆盖。
- 短随机串可枚举所有连续子串并检查平衡，作为 DP、栈与计数变种的 oracle。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/longest-valid-parentheses/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/longest-valid-parentheses/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-49-lc45/">← [力扣 Top 49] LC 45 跳跃游戏 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-512-q1-lc4000/">[力扣竞赛] 第 512 场周赛 Q1 LC 4000 给定数位和的最大整数 简单 →</a>
</nav>
