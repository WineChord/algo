---
title: "[力扣 Top 118] LC 91 解码方法 中等"
---

# [力扣 Top 118] LC 91 解码方法 中等

<p class="daily-archive-kicker">2026-08-06 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../dp/string-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4323ad3113451184033bbb9c0b79a355ba8f74ee0d803d00a32315ace308049a -->
## 官方原始信息

- Top 排名：118
- 题号：LC 91
- 官方中文标题：解码方法
- 官方难度：中等
- 官方链接：[解码方法](https://leetcode.cn/problems/decode-ways/)

### 原始题意、签名、样例与约束

数字串按 `1->A,...,26->Z` 解码，求完整解码方案数；带前导零的片段非法，可能无解。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int numDecodings(string s);
};
```

```text
"12" -> 2
"226" -> 3
"06" -> 0
```

- $1\le\lvert s\rvert\le100$，只含数字，可能以 0 开头。
- 答案保证在 32 位整数范围内。

## 约束推导与观察

以位置 `i` 结尾的最后一个编码只可能占 1 位或 2 位：单字符合法当且仅当非 `0`；双字符合法当且仅当数值在 10 到 26。暴力递归会对相同后缀重复计算，状态只需“已解码前缀长度”。

## 解法递进

### 解法一：递归枚举分组

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int dfs(const string& s, int index) {
    if (index == static_cast<int>(s.size())) {
      return 1;
    }
    if (s[index] == '0') {
      return 0;
    }
    int answer = dfs(s, index + 1);
    if (index + 1 < static_cast<int>(s.size()) && stoi(s.substr(index, 2)) <= 26) {
      answer += dfs(s, index + 2);
    }
    return answer;
  }
public:
  int numDecodings(string s) {
    return dfs(s, 0);
  }
};
```

时间最坏 $O(2^n)$，递归空间 $O(n)$，适合短串 oracle。

### 解法二：前缀动态规划

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n + 1);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
      if (s[i - 1] != '0') {
        dp[i] += dp[i - 1];
      }
      if (i >= 2) {
        int value = (s[i - 2] - '0') * 10 + s[i - 1] - '0';
        if (10 <= value && value <= 26) {
          dp[i] += dp[i - 2];
        }
      }
    }
    return dp[n];
  }
};
```

时间、空间均为 $O(n)$。

### 最佳实用解：滚动两个状态

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int numDecodings(string s) {
    int twoBack = 1;
    int oneBack = s[0] == '0' ? 0 : 1;
    for (int i = 1; i < static_cast<int>(s.size()); ++i) {
      int current = s[i] == '0' ? 0 : oneBack;
      int value = (s[i - 1] - '0') * 10 + s[i] - '0';
      if (10 <= value && value <= 26) {
        current += twoBack;
      }
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
};
```

时间 $O(n)$，空间 $O(1)$，是最佳实用解。表 DP 更方便恢复方案；只计数时优先记忆滚动状态。

## 正确性证明

令 `dp[i]` 为前 `i` 位的解码数。任一完整解码的最后一个字母要么由第 `i` 位单独形成，此时它非零，前部有 `dp[i-1]` 种；要么由最后两位形成，此时数值在 `[10,26]`，前部有 `dp[i-2]` 种。两类按最后编码长度互斥且覆盖全部方案，所以递推正确。初值 `dp[0]=1` 表示空前缀有一种完成方式，滚动变量逐项保持同一递推。

## 样例手推

`226`：`dp=[1,1,2,3]`，最后一位可单独接在 `22` 的两种解码后，也可把 `26` 接在 `2` 后，共 3。`06` 首位使 `dp[1]=0`，`06` 又不在合法两位范围，答案 0。`10` 只能整体解码，答案 1。

## 易错点与方案比较

- `0` 不能单独解码，只能属于 `10` 或 `20`。
- 两位值必须至少为 10，不能把 `06` 当 6。
- `dp[0]=1` 是组合计数的乘法单位，不表示空串是题目输入。
- 恢复方案用完整 DP；只计数用滚动数组。

## 变种一：含通配符 `*`

对应 [LC 639 解码方法 II](https://leetcode.cn/problems/decode-ways-ii/)。`*` 代表 1 到 9，分别计算单字符和双字符可选数并取模。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  static constexpr long long mod = 1000000007;
  long long single(char c) {
    if (c == '*') {
      return 9;
    }
    return c == '0' ? 0 : 1;
  }
  long long paired(char a, char b) {
    if (a == '*' && b == '*') {
      return 15;
    }
    if (a == '*') {
      return b <= '6' ? 2 : 1;
    }
    if (b == '*') {
      return a == '1' ? 9 : a == '2' ? 6 : 0;
    }
    int value = (a - '0') * 10 + b - '0';
    return 10 <= value && value <= 26;
  }
public:
  int numDecodings(string s) {
    long long twoBack = 1;
    long long oneBack = single(s[0]);
    for (int i = 1; i < static_cast<int>(s.size()); ++i) {
      long long current = single(s[i]) * oneBack;
      current += paired(s[i - 1], s[i]) * twoBack;
      current %= mod;
      twoBack = oneBack;
      oneBack = current;
    }
    return oneBack;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：恢复字典序最小的解码串

新定义：无解输出空串。先做后缀可行性 DP，再从左到右选择能完成且字母更小的编码。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string smallestDecoding(const string& s) {
  int n = s.size();
  vector<char> possible(n + 1);
  possible[n] = true;
  for (int i = n - 1; i >= 0; --i) {
    if (s[i] != '0' && possible[i + 1]) {
      possible[i] = true;
    }
    if (i + 1 < n) {
      int value = (s[i] - '0') * 10 + s[i + 1] - '0';
      possible[i] |= 10 <= value && value <= 26 && possible[i + 2];
    }
  }
  string answer;
  for (int i = 0; i < n;) {
    int one = s[i] - '0';
    if (one >= 1 && possible[i + 1]) {
      answer.push_back('A' + one - 1);
      ++i;
    } else {
      int two = one * 10 + s[i + 1] - '0';
      answer.push_back('A' + two - 1);
      i += 2;
    }
  }
  return possible[0] ? answer : "";
}
int main() {
  string s;
  cin >> s;
  cout << smallestDecoding(s) << '\n';
}
```

时间、空间均为 $O(n)$。

## 变种三：自定义数字码表

新定义：给定若干互异数字串作为合法代码，求解码数。用 Trie 从每个位置向后匹配所有码字。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  array<int, 10> next;
  bool terminal = false;
  Node() {
    next.fill(-1);
  }
};
int main() {
  int m;
  string s;
  cin >> s >> m;
  vector<Node> trie(1);
  while (m--) {
    string code;
    cin >> code;
    int node = 0;
    for (char c : code) {
      int digit = c - '0';
      if (trie[node].next[digit] == -1) {
        trie[node].next[digit] = trie.size();
        trie.emplace_back();
      }
      node = trie[node].next[digit];
    }
    trie[node].terminal = true;
  }
  vector<long long> dp(s.size() + 1);
  dp[0] = 1;
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    int node = 0;
    for (int j = i; j < static_cast<int>(s.size()); ++j) {
      node = trie[node].next[s[j] - '0'];
      if (node == -1) {
        break;
      }
      if (trie[node].terminal) {
        dp[j + 1] += dp[i];
      }
    }
  }
  cout << dp[s.size()] << '\n';
}
```

时间 $O(nL)$，其中 $L$ 为最长码字长度；空间为 Trie 与 $O(n)$。

## 变种四：在线追加数字并查询当前方案数

新定义：字符逐个到达，每次输出当前前缀解码数。原滚动递推只依赖前一字符和两个计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  string stream;
  cin >> stream;
  long long twoBack = 1;
  long long oneBack = 0;
  char previous = 0;
  for (int i = 0; i < static_cast<int>(stream.size()); ++i) {
    char currentDigit = stream[i];
    long long current = currentDigit == '0' ? 0 : (i == 0 ? 1 : oneBack);
    if (i > 0) {
      int value = (previous - '0') * 10 + currentDigit - '0';
      if (10 <= value && value <= 26) {
        current += twoBack;
      }
    }
    twoBack = i == 0 ? 1 : oneBack;
    oneBack = current;
    previous = currentDigit;
    cout << current << '\n';
  }
}
```

每个字符 $O(1)$ 时间，总额外空间 $O(1)$。

## 可复现验证

枚举长度不超过 16 的数字串，以递归分组为 oracle，对比表 DP 与滚动 DP；固定覆盖 `0`、`06`、`10`、`20`、`27`、连续零和全 1。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/decode-ways/)
- [对应知识专题](../../dp/string-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-117-lc78/">← [力扣 Top 117] LC 78 子集 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-119-lc73/">[力扣 Top 119] LC 73 矩阵置零 中等 →</a>
</nav>
