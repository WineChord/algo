---
title: "[力扣竞赛] 第 511 场周赛 Q4 LC 3999 字符串变换后的最少分组数 困难"
---

# [力扣竞赛] 第 511 场周赛 Q4 LC 3999 字符串变换后的最少分组数 困难

<p class="daily-archive-kicker">2026-07-29 · 第 12/14 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-29 题目列表</a> · <a href="../../../strings/cyclic-normalization/">进入知识专题</a></p>

## 官方原始信息

- 来源：力扣中国
- 比赛：第 511 场周赛
- 题号：Q4 / LC 3999
- 官方中文标题：字符串变换后的最少分组数
- 官方难度：困难
- ZeroTracer 社区估算竞赛分：2162（抓取于 2026-07-29；不是力扣官方难度）
- 官方链接：[打开官方页面](https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/)

### 原始题意

给定字符串数组 `words`。对字符串 `s`，分别取出偶数下标字符序列 `E` 与奇数下标字符序列 `O`；`E` 和 `O` 可以各自向右循环移动任意次，再放回各自的奇偶下标。若一个字符串可经一次这样的变换得到另一个字符串，则二者等价。

把所有字符串划分为尽量少的组，使每个字符串恰属一组，且同组任意两个字符串等价。返回最少组数。


### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minGroups(vector<string>& words);
};
```

### 全部官方样例

样例 1：

```text
输入：words = ["ntgwz","zwntg"]
输出：1
```

`ntgwz` 的偶位序列为 `ngz`，奇位序列为 `tw`；分别循环右移后可得到 `zwntg`。

样例 2：

```text
输入：words = ["abc","cab","bac","acb","bca","cba"]
输出：3
```

可分为 `["abc","cba"]`、`["cab","bac"]`、`["acb","bca"]`。

样例 3：

```text
输入：words = ["leet","abb","bab","deed","edde","code","bba"]
输出：5
```

可分为 `["abb","bba"]`、`["deed","edde"]`、`["leet"]`、`["bab"]`、`["code"]`。

### 全部约束

- $1\le |words|\le 10^5$。
- $1\le |words_i|\le 5\cdot 10^5$。
- 所有字符串长度之和不超过 $5\cdot 10^5$。
- 字符串仅含小写英文字母。

## 最优结论

一个字符串的等价类完全由两个循环字符串类决定：

1. 偶数下标序列在循环旋转意义下的等价类；
2. 奇数下标序列在循环旋转意义下的等价类。

用 Booth 算法在线性时间求每个序列的字典序最小循环表示，把“长度 + 偶位最小表示 + 奇位最小表示”作为唯一签名。最少组数就是不同签名的数量。

- 时间复杂度：$O(\sum |words_i|)$。
- 空间复杂度：$O(\sum |words_i|)$。
- 推荐记忆：独立循环移位对应两个 necklace canonical form；Booth 算法把每个 necklace 归一化。

## 约束与观察

总长度达到 $5\cdot10^5$，不能枚举每个字符串的全部旋转并逐个排序。若一个长度为 `m` 的序列直接生成 `m` 个旋转，每个旋转复制 $O(m)$ 个字符，单串就会达到 $O(m^2)$。

循环旋转是等价关系。两个字符串等价，当且仅当：

- 原串长度相同；
- 它们的偶位序列互为循环旋转；
- 它们的奇位序列互为循环旋转。

因为两个序列的旋转次数彼此独立，不能把整串直接做最小旋转。

## 解法递进

### 解法一：两两比较并枚举旋转

把每个新字符串与已有组代表逐一比较，并枚举偶位、奇位序列所有旋转。最坏可达 $O(W^2L^3)$，只适合极小数据。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  bool isRotation(const string& a, const string& b) {
    return a.size() == b.size() && (a + a).find(b) != string::npos;
  }
  pair<string, string> split(const string& word) {
    string even;
    string odd;
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      (i % 2 == 0 ? even : odd).push_back(word[i]);
    }
    return {even, odd};
  }
  bool equivalent(const string& a, const string& b) {
    if (a.size() != b.size()) {
      return false;
    }
    auto [ae, ao] = split(a);
    auto [be, bo] = split(b);
    return isRotation(ae, be) && isRotation(ao, bo);
  }
public:
  int minGroups(vector<string>& words) {
    vector<string> representatives;
    for (const string& word : words) {
      bool found = false;
      for (const string& representative : representatives) {
        if (equivalent(word, representative)) {
          found = true;
          break;
        }
      }
      if (!found) {
        representatives.push_back(word);
      }
    }
    return static_cast<int>(representatives.size());
  }
};
```

### 解法二：枚举全部旋转求规范表示

每个序列取所有旋转中字典序最小者，再用哈希集合去重。它消除了组间两两比较，但复制所有旋转仍为 $O(\sum |word_i|^2)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string minimumRotation(const string& value) {
    if (value.empty()) {
      return "";
    }
    string best = value;
    for (int shift = 1; shift < static_cast<int>(value.size()); ++shift) {
      string rotated = value.substr(shift) + value.substr(0, shift);
      best = min(best, rotated);
    }
    return best;
  }
  string signature(const string& word) {
    string even;
    string odd;
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      (i % 2 == 0 ? even : odd).push_back(word[i]);
    }
    return to_string(word.size()) + "#" + minimumRotation(even) + "#" + minimumRotation(odd);
  }
public:
  int minGroups(vector<string>& words) {
    unordered_set<string> groups;
    for (const string& word : words) {
      groups.insert(signature(word));
    }
    return static_cast<int>(groups.size());
  }
};
```

### 解法三：Booth 最小表示

Booth 算法在双倍串上同时维护两个候选起点 `i`、`j`。比较到首个不同字符时，字典序较大候选以及此前等价的起点都不可能最优，可整段跳过。每个下标只被常数次访问。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string minimumRotation(const string& value) {
    int n = static_cast<int>(value.size());
    if (n == 0) {
      return "";
    }
    string doubled = value + value;
    int first = 0;
    int second = 1;
    int offset = 0;
    while (first < n && second < n && offset < n) {
      char a = doubled[first + offset];
      char b = doubled[second + offset];
      if (a == b) {
        ++offset;
        continue;
      }
      if (a > b) {
        first += offset + 1;
        if (first == second) {
          ++first;
        }
      } else {
        second += offset + 1;
        if (first == second) {
          ++second;
        }
      }
      offset = 0;
    }
    int start = min(first, second);
    return doubled.substr(start, n);
  }
  string signature(const string& word) {
    string even;
    string odd;
    even.reserve((word.size() + 1) / 2);
    odd.reserve(word.size() / 2);
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      (i % 2 == 0 ? even : odd).push_back(word[i]);
    }
    return to_string(word.size()) + "|" + minimumRotation(even) + "|" + minimumRotation(odd);
  }
public:
  int minGroups(vector<string>& words) {
    unordered_set<string> groups;
    groups.reserve(words.size() * 2);
    for (const string& word : words) {
      groups.insert(signature(word));
    }
    return static_cast<int>(groups.size());
  }
};
```

## 正确性证明

引理 1：一次变换不改变偶位序列和奇位序列各自的循环旋转等价类。

证明：变换对两个序列分别只做循环右移，字符集合与环上相对次序均不变。

引理 2：若两个等长字符串的偶位序列互为循环旋转，且奇位序列也互为循环旋转，则两字符串等价。

证明：分别选择把第一个字符串的两个序列转到第二个字符串对应序列所需的旋转次数；两个次数允许独立选择，放回后恰得到第二个字符串。

引理 3：两个非空字符串互为循环旋转，当且仅当它们的字典序最小循环表示相同。

证明：同一旋转轨道拥有完全相同的旋转集合，因而最小元素相同；反之，最小表示相同意味着两者都能旋转到该字符串，故互为旋转。

定理：不同签名的数量等于最少分组数。

证明：由引理 1–3，签名相同与题目定义的等价完全等价。每个等价类必须单独成组，而同类所有字符串可放在一组，所以组数正是签名数。

## 样例手推

对 `ntgwz`：

- 偶位序列 `ngz` 的最小循环表示为 `gnz`；
- 奇位序列 `tw` 的最小循环表示为 `tw`。

对 `zwntg`：

- 偶位序列 `zng` 的最小循环表示也是 `gnz`；
- 奇位序列 `wt` 的最小循环表示也是 `tw`。

长度与两个规范表示均相同，因此二者只占一个组。

## 边界与易错点

- 长度为 1 时，奇位序列为空；空串需要稳定的规范表示。
- 字符串长度必须进入签名，避免不同拆分长度产生歧义。
- 两个子序列的旋转是独立的，不能对整串做 Booth。
- `word.size()` 总和是线性复杂度证明中的规模参数。
- 分隔符不在小写字母表中，可安全避免拼接歧义。

## 验证说明

对长度 1–9、字母表 `{a,b,c}` 的随机字符串，Booth 签名与“生成全部旋转后取最小值”的独立实现逐一比较；再用两两等价 oracle 核对最终组数。

## Follow-up 与变种

### 变种一：统计等价字符串对数

每个新字符串与此前同签名的每个字符串形成一对。维护签名出现次数，加入前把旧次数累加到答案。时间仍为 $O(\sum |word_i|)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string minimumRotation(const string& s) {
    if (s.empty()) {
      return "";
    }
    string d = s + s;
    int n = static_cast<int>(s.size());
    int i = 0;
    int j = 1;
    int k = 0;
    while (i < n && j < n && k < n) {
      if (d[i + k] == d[j + k]) {
        ++k;
      } else {
        int& loser = d[i + k] > d[j + k] ? i : j;
        loser += k + 1;
        if (i == j) {
          ++j;
        }
        k = 0;
      }
    }
    int start = min(i, j);
    return d.substr(start, n);
  }
  string key(const string& word) {
    string even;
    string odd;
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      (i & 1 ? odd : even).push_back(word[i]);
    }
    return minimumRotation(even) + "#" + minimumRotation(odd);
  }
public:
  long long countEquivalentPairs(vector<string>& words) {
    unordered_map<string, long long> frequency;
    long long answer = 0;
    for (const string& word : words) {
      string signature = key(word);
      answer += frequency[signature];
      ++frequency[signature];
    }
    return answer;
  }
};
```

### 变种二：每个奇偶序列还允许反转

旋转加反转形成二面体等价。一个序列的规范表示取“原串最小旋转”和“反串最小旋转”的较小者；其余框架不变。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string minimumRotation(const string& s) {
    if (s.empty()) {
      return "";
    }
    string d = s + s;
    int n = static_cast<int>(s.size());
    int i = 0;
    int j = 1;
    int k = 0;
    while (i < n && j < n && k < n) {
      if (d[i + k] == d[j + k]) {
        ++k;
        continue;
      }
      if (d[i + k] > d[j + k]) {
        i += k + 1;
        if (i == j) {
          ++i;
        }
      } else {
        j += k + 1;
        if (i == j) {
          ++j;
        }
      }
      k = 0;
    }
    int start = min(i, j);
    return d.substr(start, n);
  }
  string dihedral(const string& value) {
    string reversed = value;
    reverse(reversed.begin(), reversed.end());
    return min(minimumRotation(value), minimumRotation(reversed));
  }
public:
  int minGroups(vector<string>& words) {
    unordered_set<string> groups;
    for (const string& word : words) {
      string even;
      string odd;
      for (int i = 0; i < static_cast<int>(word.size()); ++i) {
        (i & 1 ? odd : even).push_back(word[i]);
      }
      groups.insert(to_string(word.size()) + "#" + dihedral(even) + "#" + dihedral(odd));
    }
    return static_cast<int>(groups.size());
  }
};
```

### 变种三：只有偶数下标序列允许旋转

奇位序列必须逐字符相同，因此签名改为“偶位最小旋转 + 原始奇位序列”。时间复杂度保持线性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  string minimumRotation(const string& s) {
    if (s.empty()) {
      return "";
    }
    string d = s + s;
    int n = static_cast<int>(s.size());
    int i = 0;
    int j = 1;
    int k = 0;
    while (i < n && j < n && k < n) {
      if (d[i + k] == d[j + k]) {
        ++k;
      } else {
        if (d[i + k] > d[j + k]) {
          i += k + 1;
          if (i == j) {
            ++i;
          }
        } else {
          j += k + 1;
          if (i == j) {
            ++j;
          }
        }
        k = 0;
      }
    }
    int start = min(i, j);
    return d.substr(start, n);
  }
public:
  int minGroups(vector<string>& words) {
    unordered_set<string> groups;
    for (const string& word : words) {
      string even;
      string odd;
      for (int i = 0; i < static_cast<int>(word.size()); ++i) {
        (i & 1 ? odd : even).push_back(word[i]);
      }
      groups.insert(to_string(word.size()) + "#" + minimumRotation(even) + "#" + odd);
    }
    return static_cast<int>(groups.size());
  }
};
```

### 变种四：在线加入字符串并查询当前组数

每次插入仍只需计算一个规范签名。若签名首次出现，组数加一；单次时间与字符串长度线性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OnlineGroups {
  unordered_set<string> signatures;
  string minimumRotation(const string& s) {
    if (s.empty()) {
      return "";
    }
    string d = s + s;
    int n = static_cast<int>(s.size());
    int i = 0;
    int j = 1;
    int k = 0;
    while (i < n && j < n && k < n) {
      if (d[i + k] == d[j + k]) {
        ++k;
        continue;
      }
      if (d[i + k] > d[j + k]) {
        i += k + 1;
        if (i == j) {
          ++i;
        }
      } else {
        j += k + 1;
        if (i == j) {
          ++j;
        }
      }
      k = 0;
    }
    int start = min(i, j);
    return d.substr(start, n);
  }
  string key(const string& word) {
    string even;
    string odd;
    for (int i = 0; i < static_cast<int>(word.size()); ++i) {
      (i & 1 ? odd : even).push_back(word[i]);
    }
    return to_string(word.size()) + "#" + minimumRotation(even) + "#" + minimumRotation(odd);
  }
public:
  int add(const string& word) {
    signatures.insert(key(word));
    return static_cast<int>(signatures.size());
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  OnlineGroups groups;
  while (q--) {
    string word;
    cin >> word;
    cout << groups.add(word) << '\n';
  }
  return 0;
}
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/)
- [第 511 场周赛官方页面](https://leetcode.cn/contest/weekly-contest-511/)
- [ZeroTracer 社区估算竞赛分](https://zerotrac.github.io/leetcode_problem_rating/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/minimum-number-of-string-groups-through-transformations/)
- [对应知识专题](../../strings/cyclic-normalization.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-40-lc236/">← [力扣 Top 40] LC 236 二叉树的最近公共祖先 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2247-d1/">[codeforces] CF Round 1111 Div.2 D1 XOR Sorting (Easy Version) →</a>
</nav>
