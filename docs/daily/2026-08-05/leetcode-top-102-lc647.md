---
title: "[力扣 Top 102] LC 647 回文子串 中等"
---

# [力扣 Top 102] LC 647 回文子串 中等

<p class="daily-archive-kicker">2026-08-05 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../strings/palindrome-centers/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=f2def2f7d7dfa8457c02fd9bcee328bf516881cc7ff4dc367b0046ee1909f34a -->
## 官方原始信息

- Top 排名：102
- 题号：LC 647
- 官方中文标题：回文子串
- 官方难度：中等
- 官方链接：[回文子串](https://leetcode.cn/problems/palindromic-substrings/)

### 原始题意

给定仅含小写英文字母的字符串 `s`，统计其中所有连续回文子串。相同文本出现在不同位置时要分别计数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int countSubstrings(string s);
};
```

### 全部官方样例

```text
输入：s = "abc"
输出：3
解释：三个回文子串为 "a"、"b"、"c"。
```

```text
输入：s = "aaa"
输出：6
解释：三个 "a"、两个 "aa" 和一个 "aaa" 都要计数。
```

### 全部约束

- $1\le |s|\le1000$。
- `s` 仅由小写英文字母组成。

## 约束推导与观察

子串由左右端点唯一确定，共有 $O(n^2)$ 个。若每个子串再线性检查回文性，总时间为 $O(n^3)$。回文具有两个可复用结构：删去相同首尾后仍是回文；或者每个回文都有唯一的奇数中心或偶数中心。后者允许从每个中心向外扩张，每成功扩张一次便恰好发现一个新子串。

最大答案为 $n(n+1)/2\le500500$，`int` 足够。

## 解法递进

### 解法一：枚举端点并逐字符检查

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool palindrome(const string& s, int left, int right) {
    while (left < right) {
      if (s[left++] != s[right--]) {
        return false;
      }
    }
    return true;
  }
public:
  int countSubstrings(string s) {
    int answer = 0;
    for (int left = 0; left < static_cast<int>(s.size()); ++left) {
      for (int right = left; right < static_cast<int>(s.size()); ++right) {
        answer += palindrome(s, left, right);
      }
    }
    return answer;
  }
};
```

时间 $O(n^3)$，递归外额外空间 $O(1)$。重复扫描相同内部区间是瓶颈。

### 解法二：区间动态规划

令 `dp[l][r]` 表示 `s[l..r]` 是否回文。首尾相同且区间长度不超过 2，或内部区间已知为回文时，当前区间成立。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countSubstrings(string s) {
    int n = s.size();
    vector<vector<char>> dp(n, vector<char>(n));
    int answer = 0;
    for (int left = n - 1; left >= 0; --left) {
      for (int right = left; right < n; ++right) {
        dp[left][right] = s[left] == s[right] && (right - left <= 1 || dp[left + 1][right - 1]);
        answer += dp[left][right];
      }
    }
    return answer;
  }
};
```

时间 $O(n^2)$，空间 $O(n^2)$。它适合后续需要任意区间回文查询的任务。

### 最佳实用解：枚举回文中心

共有 $2n-1$ 个奇偶中心。把中心编号写成 `center`，初始左右端点分别为 `center / 2` 与 `center / 2 + center % 2`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countSubstrings(string s) {
    int n = s.size();
    int answer = 0;
    for (int center = 0; center < 2 * n - 1; ++center) {
      int left = center / 2;
      int right = left + center % 2;
      while (left >= 0 && right < n && s[left] == s[right]) {
        ++answer;
        --left;
        ++right;
      }
    }
    return answer;
  }
};
```

时间 $O(n^2)$，额外空间 $O(1)$。在 $n\le1000$ 下，它比 DP 更省空间、实现更稳，是面试优先记忆的方案。

### 理论最优：Manacher 半径

分别维护奇回文半径 `odd` 与偶回文半径 `even`；每个半径值正好等于该中心贡献的回文子串数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int countSubstrings(string s) {
    int n = s.size();
    vector<int> odd(n), even(n);
    for (int i = 0, left = 0, right = -1; i < n; ++i) {
      int radius = i > right ? 1 : min(odd[left + right - i], right - i + 1);
      while (i - radius >= 0 && i + radius < n && s[i - radius] == s[i + radius]) {
        ++radius;
      }
      odd[i] = radius;
      if (i + radius - 1 > right) {
        left = i - radius + 1;
        right = i + radius - 1;
      }
    }
    for (int i = 0, left = 0, right = -1; i < n; ++i) {
      int radius = i > right ? 0 : min(even[left + right - i + 1], right - i + 1);
      while (i - radius - 1 >= 0 && i + radius < n && s[i - radius - 1] == s[i + radius]) {
        ++radius;
      }
      even[i] = radius;
      if (i + radius - 1 > right) {
        left = i - radius;
        right = i + radius - 1;
      }
    }
    return accumulate(odd.begin(), odd.end(), 0) + accumulate(even.begin(), even.end(), 0);
  }
};
```

时间 $O(n)$，空间 $O(n)$。它消除了不同中心之间的重复比较，但索引证明与实现负担更高；只有规模明显放大或还需要全部半径时优先。

## 正确性证明

任意回文子串 `[l,r]` 有唯一中心：若长度为奇数，中心是一个字符；若长度为偶数，中心是两个相邻字符之间。中心扩张从该中心的最短回文开始，每次两端字符相等才继续，因此计入的每个区间都是回文；它会依次经过 `[l,r]` 的所有内层半径，故必然计入该区间。唯一中心又保证同一位置区间不会被重复计数，所以最终计数恰为全部回文子串数。

## 样例手推

`aaa` 有三个奇中心：贡献 1、2、1；两个偶中心各贡献 1，总计 6。`abc` 的任意中心向外第一步都会遇到不同字符，因此只有三个单字符回文。最小输入长度为 1 时共有一个中心，答案为 1。

## 易错点与方案比较

- 回文“子串”必须连续，不能按子序列计数。
- 相同内容的不同位置要分别计数。
- 奇偶中心都要枚举；漏掉偶中心会漏掉 `aa`。
- DP 更利于回答后续任意区间查询；中心扩张空间最小；Manacher 渐进最优但不应为 $n=1000$ 增加无谓复杂度。

## 变种一：按长度统计回文子串数量

新定义：返回 `count[len]`。中心扩张仍成立，只需在每次成功扩张时记录当前长度。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string s;
  cin >> s;
  int n = s.size();
  vector<int> count(n + 1);
  for (int center = 0; center < 2 * n - 1; ++center) {
    int left = center / 2;
    int right = left + center % 2;
    while (left >= 0 && right < n && s[left] == s[right]) {
      ++count[right - left + 1];
      --left;
      ++right;
    }
  }
  for (int length = 1; length <= n; ++length) {
    cout << count[length] << (length == n ? '\n' : ' ');
  }
}
```

时间 $O(n^2)$，空间 $O(n)$。

## 变种二：返回最长回文子串

新定义：不计数，而是恢复最长区间。每次扩张后比较长度并保存左右端点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string longestPalindrome(string s) {
    int bestLeft = 0;
    int bestLength = 1;
    int n = s.size();
    for (int center = 0; center < 2 * n - 1; ++center) {
      int left = center / 2;
      int right = left + center % 2;
      while (left >= 0 && right < n && s[left] == s[right]) {
        if (right - left + 1 > bestLength) {
          bestLeft = left;
          bestLength = right - left + 1;
        }
        --left;
        ++right;
      }
    }
    return s.substr(bestLeft, bestLength);
  }
};
```

时间 $O(n^2)$，空间 $O(1)$；对应 [LC 5](https://leetcode.cn/problems/longest-palindromic-substring/)。

## 变种三：字符流逐个追加并报告累计数量

新定义：每追加一个字符，立即输出当前字符串的回文子串总数。中心扩张会重复工作，回文树把不同回文作为节点；新字符产生的新增出现数等于当前最长回文后缀沿失配链接的节点数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int length = 0;
  int link = 0;
  int suffixCount = 0;
  array<int, 26> next{};
};
int main() {
  string input;
  cin >> input;
  vector<Node> tree(2);
  tree[0].length = -1;
  tree[0].link = 0;
  tree[1].length = 0;
  tree[1].link = 0;
  string built;
  int last = 1;
  long long total = 0;
  for (char ch : input) {
    built.push_back(ch);
    int position = static_cast<int>(built.size()) - 1;
    int current = last;
    while (position - 1 - tree[current].length < 0 ||
        built[position - 1 - tree[current].length] != ch) {
      current = tree[current].link;
    }
    int edge = ch - 'a';
    if (!tree[current].next[edge]) {
      Node node;
      node.length = tree[current].length + 2;
      int link = tree[current].link;
      if (node.length == 1) {
        node.link = 1;
      } else {
        while (
            position - 1 - tree[link].length < 0 || built[position - 1 - tree[link].length] != ch) {
          link = tree[link].link;
        }
        node.link = tree[link].next[edge];
      }
      node.suffixCount = 1 + tree[node.link].suffixCount;
      tree.push_back(node);
      tree[current].next[edge] = static_cast<int>(tree.size()) - 1;
    }
    last = tree[current].next[edge];
    total += tree[last].suffixCount;
    cout << total << '\n';
  }
}
```

总时间 $O(n\lvert\Sigma\rvert)$ 的朴素上界、对固定小写字母表可视为 $O(n)$，空间 $O(n\lvert\Sigma\rvert)$；原中心法不适合每次追加后从头重算。

## 变种四：问号可匹配任意字符

新定义：字符串还可含 `?`，若能为每个位置独立选择字母使某子串成为回文，就计入。两端相同或任一端为 `?` 即兼容，中心扩张仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool compatible(char a, char b) {
  return a == b || a == '?' || b == '?';
}
int main() {
  string s;
  cin >> s;
  int n = s.size();
  long long answer = 0;
  for (int center = 0; center < 2 * n - 1; ++center) {
    int left = center / 2;
    int right = left + center % 2;
    while (left >= 0 && right < n && compatible(s[left], s[right])) {
      ++answer;
      --left;
      ++right;
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n^2)$，空间 $O(1)$。若同一个 `?` 必须在全串保持同一替换值，局部兼容不再充分，需要全局约束模型。

## 验证说明

本轮将九段代码按 C++23 编译；主解、DP、Manacher 与三次暴力会对拍所有长度不超过 9 的三进制字母串，并随机核验长度 1000 的重复字符、交替字符和一般字符串。流式版本逐前缀与中心扩张结果比较。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/palindromic-substrings/)
- [对应知识专题](../../strings/palindrome-centers.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-101-lc69/">← [力扣 Top 101] LC 69 x 的平方根 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-103-lc92/">[力扣 Top 103] LC 92 反转链表 II 中等 →</a>
</nav>
