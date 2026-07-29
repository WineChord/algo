---
title: "[力扣 Top 32] LC 22 括号生成 中等"
---

# [力扣 Top 32] LC 22 括号生成 中等

<p class="daily-archive-kicker">2026-07-29 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../search/backtracking.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：32
- 题号：LC 22
- 官方中文标题：括号生成
- 官方难度：中等
- 官方链接：<https://leetcode.cn/problems/generate-parentheses/>

### 原始题意

给定括号对数 `n`，生成所有可能且有效的括号组合，答案顺序任意。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<string> generateParenthesis(int n);
};
```

### 全部官方样例

```text
输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
```

```text
输入：n = 1
输出：["()"]
```

### 全部约束

- $1\le n\le8$。
- 输出数量是第 $n$ 个 Catalan 数 $C_n=\frac{1}{n+1}\binom{2n}{n}$。
- 输出本身含 $\Theta(C_n n)$ 个字符，任何完整生成算法都至少需要该时间。

## 最优结论

回溯时只维护仍可能扩展成答案的前缀：

- 左括号已用数小于 `n` 时可以放 `(`；
- 右括号已用数小于左括号已用数时可以放 `)`。

当长度达到 `2n` 时得到一个且仅一个有效序列。时间 $O(C_n n)$，递归额外空间 $O(n)$，不计输出。

## 约束与观察

有效前缀的核心不变量是任意前缀中 `left >= right`。若某一前缀右括号更多，此后无论加入什么都无法修复它；剪掉这些前缀正是从暴力到最优的关键。

边界 `n=1` 只有 `()`。递归结束条件可写为长度 `2n`，此时在不变量下左右数量必均为 `n`。

## 解法递进

### 解法一：枚举全部二进制串再验证

把每个位置视为选左或右括号，枚举 $2^{2n}=4^n$ 个串，再扫描验证。时间 $O(4^n n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool valid(const string& value) {
    int balance = 0;
    for (char ch : value) {
      balance += ch == '(' ? 1 : -1;
      if (balance < 0) {
        return false;
      }
    }
    return balance == 0;
  }
public:
  vector<string> generateParenthesis(int n) {
    vector<string> answer;
    int length = 2 * n;
    for (int mask = 0; mask < (1 << length); ++mask) {
      string candidate(length, ')');
      for (int i = 0; i < length; ++i) {
        if ((mask >> i) & 1) {
          candidate[i] = '(';
        }
      }
      if (valid(candidate)) {
        answer.push_back(candidate);
      }
    }
    return answer;
  }
};
```

### 解法二：有效前缀回溯

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void search(int n, int left, int right, string& current, vector<string>& answer) {
    if (static_cast<int>(current.size()) == 2 * n) {
      answer.push_back(current);
      return;
    }
    if (left < n) {
      current.push_back('(');
      search(n, left + 1, right, current, answer);
      current.pop_back();
    }
    if (right < left) {
      current.push_back(')');
      search(n, left, right + 1, current, answer);
      current.pop_back();
    }
  }
public:
  vector<string> generateParenthesis(int n) {
    vector<string> answer;
    string current;
    current.reserve(2 * n);
    search(n, 0, 0, current, answer);
    return answer;
  }
};
```

### 同阶方案：按较小规模拼接

任一非空有效序列都可唯一写成 `"(" + A + ")" + B`，其中 `A`、`B` 分别使用 `i` 与 `n-1-i` 对括号。动态规划按对数拼接也为输出最优量级，但会复制更多中间字符串；面试更推荐回溯。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<string> generateParenthesis(int n) {
    vector<vector<string>> dp(n + 1);
    dp[0] = {""};
    for (int pairs = 1; pairs <= n; ++pairs) {
      for (int inside = 0; inside < pairs; ++inside) {
        for (const string& left : dp[inside]) {
          for (const string& right : dp[pairs - 1 - inside]) {
            dp[pairs].push_back("(" + left + ")" + right);
          }
        }
      }
    }
    return dp[n];
  }
};
```

## 正确性证明

不变量：每次递归进入时，当前前缀中左括号不少于右括号，且二者均不超过 `n`。两个分支条件保持该不变量。

完备性：任意有效序列的每个前缀都满足不变量。沿该序列逐字符选择时，对应分支永远不会被剪掉，因此最终一定生成。

唯一性：每条递归路径对应唯一字符序列；不同路径首个不同分支产生不同字符串，所以无重复。

终止时长度为 `2n`，不变量和数量上限迫使左右括号都恰为 `n`，因此所有输出有效。

## 样例手推

`n=3` 时，从空串先选 `(`。前缀 `((` 可继续选 `(` 得 `((()))`，也可选 `)` 得 `(()...)`。前缀 `())` 会在尝试第二个右括号前被 `right < left` 条件剪掉，因此不会产生无效结果。

## 易错点

- 允许放右括号的条件是 `right < left`，不是 `right < n`。
- 回溯后必须 `pop_back` 恢复现场。
- 不要用集合去重掩盖递归状态设计错误。
- 输出顺序不影响判题。

## 验证说明

对 `n=1..8`，检查输出数量等于 Catalan 数；每个串再以栈平衡验证，排序后与暴力枚举结果比较。

## Follow-up 与变种

### 变种一：只求方案数

状态 `dp[left][right]` 统计有效前缀完成方式。复杂度 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  long long countParentheses(int n) {
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    dp[0][0] = 1;
    for (int left = 0; left <= n; ++left) {
      for (int right = 0; right <= left; ++right) {
        if (left < n) {
          dp[left + 1][right] += dp[left][right];
        }
        if (right < left) {
          dp[left][right + 1] += dp[left][right];
        }
      }
    }
    return dp[n][n];
  }
};
```

### 变种二：返回字典序第 `k` 个序列

先记忆化统计每个状态的完成数；`(` 比 `)` 小，若以 `(` 开头的块不足 `k`，整块跳过。复杂度 $O(n^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int n = 0;
  long long cap = 0;
  vector<vector<long long>> memo;
  long long count(int left, int right) {
    if (left == n && right == n) {
      return 1;
    }
    long long& result = memo[left][right];
    if (result != -1) {
      return result;
    }
    result = 0;
    if (left < n) {
      result = min(cap, result + count(left + 1, right));
    }
    if (right < left) {
      result = min(cap, result + count(left, right + 1));
    }
    return result;
  }
public:
  string kthParenthesis(int pairs, long long k) {
    n = pairs;
    cap = k;
    memo.assign(n + 1, vector<long long>(n + 1, -1));
    if (count(0, 0) < k) {
      return "";
    }
    string answer;
    int left = 0;
    int right = 0;
    while (left < n || right < n) {
      long long firstBlock = left < n ? count(left + 1, right) : 0;
      if (left < n && k <= firstBlock) {
        answer.push_back('(');
        ++left;
      } else {
        k -= firstBlock;
        answer.push_back(')');
        ++right;
      }
    }
    return answer;
  }
};
```

### 变种三：限制最大嵌套深度

当前深度是 `left-right`。只有深度小于上限时才能继续放左括号。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void dfs(int n, int limit, int left, int right, string& current, vector<string>& answer) {
    if (left == n && right == n) {
      answer.push_back(current);
      return;
    }
    if (left < n && left - right < limit) {
      current.push_back('(');
      dfs(n, limit, left + 1, right, current, answer);
      current.pop_back();
    }
    if (right < left) {
      current.push_back(')');
      dfs(n, limit, left, right + 1, current, answer);
      current.pop_back();
    }
  }
public:
  vector<string> generateWithMaxDepth(int n, int limit) {
    vector<string> answer;
    string current;
    dfs(n, limit, 0, 0, current, answer);
    return answer;
  }
};
```

### 变种四：每一对可选择多种括号类型

打开括号时选择一种类型并压栈；关闭时只能使用栈顶对应类型。以下生成 `()` 与 `[]` 两种类型，时间与输出规模成正比。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  const string opens = "([";
  const string closes = ")]";
  void dfs(int n, int opened, int closed, string& stack, string& current, vector<string>& answer) {
    if (closed == n) {
      answer.push_back(current);
      return;
    }
    if (opened < n) {
      for (int type = 0; type < 2; ++type) {
        stack.push_back(static_cast<char>('0' + type));
        current.push_back(opens[type]);
        dfs(n, opened + 1, closed, stack, current, answer);
        current.pop_back();
        stack.pop_back();
      }
    }
    if (!stack.empty()) {
      int type = stack.back() - '0';
      stack.pop_back();
      current.push_back(closes[type]);
      dfs(n, opened, closed + 1, stack, current, answer);
      current.pop_back();
      stack.push_back(static_cast<char>('0' + type));
    }
  }
public:
  vector<string> generateTwoTypes(int n) {
    vector<string> answer;
    string stack;
    string current;
    dfs(n, 0, 0, stack, current, answer);
    return answer;
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/generate-parentheses/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/generate-parentheses/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-31-lc279.md">← [力扣 Top 31] LC 279 完全平方数 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-33-lc27.md">[力扣 Top 33] LC 27 移除元素 简单 →</a>
</nav>
