---
title: "[力扣 Top 55] LC 131 分割回文串 中等"
---

# [力扣 Top 55] LC 131 分割回文串 中等

<p class="daily-archive-kicker">2026-07-31 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4cdebd8adcdd7d2d55b61d30151debac41c779fca89cf7521d6b6019310369d6 -->
## 官方原始信息

- Top 排名：55
- 题号：LC 131
- 官方中文标题：分割回文串
- 官方难度：中等
- 官方链接：[分割回文串](https://leetcode.cn/problems/palindrome-partitioning/)

### 原始题意

把字符串 `s` 切成若干非空连续子串，要求每一段都是回文串，返回所有可能的分割方案。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<string>> partition(string s);
};
```

### 全部官方样例

```text
输入：s = "aab"
输出：[["a","a","b"],["aa","b"]]
```

```text
输入：s = "a"
输出：[["a"]]
```

### 全部约束

- $1\le |s|\le16$。
- `s` 只含小写英文字母。

## 约束推导与边界

长度 16 明确允许指数级枚举。两个相邻字符之间各有“切”或“不切”两种选择，因此候选切法最多 $2^{n-1}$ 种；输出本身也可能达到指数级。优化重点不是消灭枚举，而是避免对相同子串反复判回文。单字符天然是回文，整串回文和每字符单独成段都由同一递归覆盖。

## 解法递进

### 解法一：回溯时逐段检查回文

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<string>> answer;
  vector<string> path;
  bool isPalindrome(const string& s, int left, int right) {
    while (left < right) {
      if (s[left++] != s[right--]) {
        return false;
      }
    }
    return true;
  }
  void search(const string& s, int start) {
    if (start == static_cast<int>(s.size())) {
      answer.push_back(path);
      return;
    }
    for (int end = start; end < static_cast<int>(s.size()); ++end) {
      if (!isPalindrome(s, start, end)) {
        continue;
      }
      path.push_back(s.substr(start, end - start + 1));
      search(s, end + 1);
      path.pop_back();
    }
  }
public:
  vector<vector<string>> partition(string s) {
    search(s, 0);
    return answer;
  }
};
```

最坏时间 $O(n^2 2^n)$：约 $O(n2^n)$ 个候选段，每次判回文再花 $O(n)$；递归空间 $O(n)$，不计输出。

### 最佳实用解：预处理回文区间后回溯

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<string>> answer;
  vector<string> path;
  vector<vector<char>> palindrome;
  void search(const string& s, int start) {
    if (start == static_cast<int>(s.size())) {
      answer.push_back(path);
      return;
    }
    for (int end = start; end < static_cast<int>(s.size()); ++end) {
      if (!palindrome[start][end]) {
        continue;
      }
      path.push_back(s.substr(start, end - start + 1));
      search(s, end + 1);
      path.pop_back();
    }
  }
public:
  vector<vector<string>> partition(string s) {
    int n = s.size();
    palindrome.assign(n, vector<char>(n));
    for (int left = n - 1; left >= 0; --left) {
      for (int right = left; right < n; ++right) {
        palindrome[left][right] =
            s[left] == s[right] && (right - left <= 2 || palindrome[left + 1][right - 1]);
      }
    }
    search(s, 0);
    return answer;
  }
};
```

预处理 $O(n^2)$；枚举与复制输出最坏 $O(n2^n)$；辅助空间 $O(n^2)$。

## 正确性证明

动态规划式 `palindrome[l][r]` 为真，当且仅当两端字符相等，且内部长度不超过 1 或内部区间也是回文；按 `left` 递减计算时内部状态已经得到，因此表准确。回溯在位置 `start` 枚举所有可能的段尾，只沿回文段递归，所以产生的每个方案都合法。任一合法分割的第一段必对应某个枚举到的 `end`，随后其余段由归纳假设完整枚举，因此没有遗漏；不同端点序列唯一确定分割，不会重复。

## 样例手推

`"aab"` 从位置 0 可选 `"a"` 或 `"aa"`。选择 `"a"` 后只能再选 `"a"`、`"b"`，得到 `["a","a","b"]`；选择 `"aa"` 后接 `"b"`，得到 `["aa","b"]`。`"aab"` 本身不是回文，不会形成第三条分支。

## 易错点与方案比较

- 回溯状态是“下一段起点”，到达 `n` 时才收集答案。
- 选择后必须 `pop_back` 恢复现场。
- `right - left <= 2` 同时覆盖长度 1、2、3，避免访问越界。
- 两种解法枚举树相同；预处理版把重复回文判断降为 $O(1)$，推荐作为默认实现。

## 变种一：求最少切割次数

输出所有方案不再必要。令 `cuts[i]` 表示前缀 `s[0..i)` 的最少段数，最后减 1 得切割次数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  int n = s.size();
  vector<vector<char>> palindrome(n, vector<char>(n));
  for (int left = n - 1; left >= 0; --left) {
    for (int right = left; right < n; ++right) {
      palindrome[left][right] =
          s[left] == s[right] && (right - left <= 2 || palindrome[left + 1][right - 1]);
    }
  }
  vector<int> pieces(n + 1, n + 1);
  pieces[0] = 0;
  for (int end = 1; end <= n; ++end) {
    for (int start = 0; start < end; ++start) {
      if (palindrome[start][end - 1]) {
        pieces[end] = min(pieces[end], pieces[start] + 1);
      }
    }
  }
  cout << pieces[n] - 1 << '\n';
}
```

时间 $O(n^2)$，空间 $O(n^2)$。

## 变种二：只统计回文分割方案数

令 `ways[i]` 为前缀 `s[0..i)` 的合法分割数，不保存具体路径。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  string s;
  cin >> s;
  int n = s.size();
  vector<vector<char>> palindrome(n, vector<char>(n));
  for (int left = n - 1; left >= 0; --left) {
    for (int right = left; right < n; ++right) {
      palindrome[left][right] =
          s[left] == s[right] && (right - left <= 2 || palindrome[left + 1][right - 1]);
    }
  }
  vector<long long> ways(n + 1);
  ways[0] = 1;
  for (int end = 1; end <= n; ++end) {
    for (int start = 0; start < end; ++start) {
      if (palindrome[start][end - 1]) {
        ways[end] = (ways[end] + ways[start]) % mod;
      }
    }
  }
  cout << ways[n] << '\n';
}
```

时间 $O(n^2)$，空间 $O(n^2)$。

## 变种三：统计恰好分成 k 段的方案数

增加“已经使用多少段”这一维，原回溯的可行性判断仍可复用。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const long long mod = 1000000007;
  string s;
  int k;
  cin >> s >> k;
  int n = s.size();
  vector<vector<char>> palindrome(n, vector<char>(n));
  for (int left = n - 1; left >= 0; --left) {
    for (int right = left; right < n; ++right) {
      palindrome[left][right] =
          s[left] == s[right] && (right - left <= 2 || palindrome[left + 1][right - 1]);
    }
  }
  vector<vector<long long>> ways(n + 1, vector<long long>(k + 1));
  ways[0][0] = 1;
  for (int end = 1; end <= n; ++end) {
    for (int start = 0; start < end; ++start) {
      if (!palindrome[start][end - 1]) {
        continue;
      }
      for (int pieces = 1; pieces <= k; ++pieces) {
        ways[end][pieces] = (ways[end][pieces] + ways[start][pieces - 1]) % mod;
      }
    }
  }
  cout << ways[n][k] << '\n';
}
```

时间 $O(n^2k)$，空间 $O(nk+n^2)$。

## 变种四：返回字典序第 k 个分割

在原约束 $n\le16$ 下可枚举全部方案，按字符串向量的字典序排序后选择；超出范围则输出 -1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<string>> answer;
vector<string> path;
vector<vector<char>> palindrome;
void search(const string& s, int start) {
  if (start == static_cast<int>(s.size())) {
    answer.push_back(path);
    return;
  }
  for (int end = start; end < static_cast<int>(s.size()); ++end) {
    if (palindrome[start][end]) {
      path.push_back(s.substr(start, end - start + 1));
      search(s, end + 1);
      path.pop_back();
    }
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  long long k;
  cin >> s >> k;
  int n = s.size();
  palindrome.assign(n, vector<char>(n));
  for (int left = n - 1; left >= 0; --left) {
    for (int right = left; right < n; ++right) {
      palindrome[left][right] =
          s[left] == s[right] && (right - left <= 2 || palindrome[left + 1][right - 1]);
    }
  }
  search(s, 0);
  sort(answer.begin(), answer.end());
  if (k < 1 || k > static_cast<long long>(answer.size())) {
    cout << -1 << '\n';
    return 0;
  }
  for (const string& part : answer[k - 1]) {
    cout << part << ' ';
  }
  cout << '\n';
}
```

时间由输出规模主导，最坏 $O(n2^n\log 2^n)$，辅助空间 $O(n^2)$ 加结果。

## 可复现验证

对长度不超过 10 的随机二元字符串，把预处理版与逐段检查版的方案排序后逐项比较，并验证每个输出段确为回文、拼接后等于原串。最少切割和计数变种与完整方案枚举统计交叉核对。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/palindrome-partitioning/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/palindrome-partitioning/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-54-lc240/">← [力扣 Top 54] LC 240 搜索二维矩阵 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-56-lc17/">[力扣 Top 56] LC 17 电话号码的字母组合 中等 →</a>
</nav>
