---
title: "[力扣 Top 57] LC 76 最小覆盖子串 困难"
---

# [力扣 Top 57] LC 76 最小覆盖子串 困难

<p class="daily-archive-kicker">2026-07-31 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../data-structures/hash-and-cache/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=b217ae95a6bdb13b1cb0a0ee34cda1958d0e58e754b9ec50ee7d06c43d21a208 -->
## 官方原始信息

- Top 排名：57
- 题号：LC 76
- 官方中文标题：最小覆盖子串
- 官方难度：困难
- 官方链接：[最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/)

### 原始题意

给定字符串 `s` 和 `t`，返回 `s` 中包含 `t` 全部字符及其重复次数的最短连续子串；不存在则返回空串。测试保证答案唯一。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string minWindow(string s, string t);
};
```

### 全部官方样例

```text
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最短覆盖子串是 "BANC"。
```

```text
输入：s = "a", t = "a"
输出："a"
```

```text
输入：s = "a", t = "aa"
输出：""
解释：覆盖必须满足重复次数，s 中只有一个 'a'。
```

### 全部约束

- $1\le |s|,|t|\le10^5$。
- `s` 和 `t` 只含大小写英文字母。
- 若存在答案，答案唯一。
- 进阶要求设计 $O(|s|+|t|)$ 算法。

## 约束推导与边界

枚举所有子串需要平方级候选，无法承受 $10^5$。当一个窗口已经覆盖 `t` 时，右端继续右移不会让窗口失去覆盖性；可以单调右移扩张、单调右移左端收缩。用 `need[c]` 表示窗口还缺多少个字符 `c`，再用 `missing` 记录总缺口，窗口合法判断即可从扫描整个字符集降为 $O(1)$。

## 解法递进

### 解法一：枚举左端并向右寻找首个合法窗口

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string minWindow(string s, string t) {
    array<int, 128> required{};
    for (unsigned char character : t) {
      ++required[character];
    }
    int bestStart = -1;
    int bestLength = numeric_limits<int>::max();
    for (int left = 0; left < static_cast<int>(s.size()); ++left) {
      array<int, 128> count{};
      int missing = t.size();
      for (int right = left; right < static_cast<int>(s.size()); ++right) {
        unsigned char character = s[right];
        if (count[character] < required[character]) {
          --missing;
        }
        ++count[character];
        if (missing == 0) {
          if (right - left + 1 < bestLength) {
            bestLength = right - left + 1;
            bestStart = left;
          }
          break;
        }
      }
    }
    return bestStart == -1 ? "" : s.substr(bestStart, bestLength);
  }
};
```

时间 $O(|s|^2+|t|)$，空间 $O(1)$。

### 最佳实用解：缺口计数滑动窗口

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string minWindow(string s, string t) {
    array<int, 128> need{};
    for (unsigned char character : t) {
      ++need[character];
    }
    int missing = t.size();
    int left = 0;
    int bestStart = 0;
    int bestLength = numeric_limits<int>::max();
    for (int right = 0; right < static_cast<int>(s.size()); ++right) {
      unsigned char added = s[right];
      if (need[added] > 0) {
        --missing;
      }
      --need[added];
      while (missing == 0) {
        if (right - left + 1 < bestLength) {
          bestLength = right - left + 1;
          bestStart = left;
        }
        unsigned char removed = s[left++];
        ++need[removed];
        if (need[removed] > 0) {
          ++missing;
        }
      }
    }
    return bestLength == numeric_limits<int>::max() ? "" : s.substr(bestStart, bestLength);
  }
};
```

时间 $O(|s|+|t|)$，空间 $O(1)$；字符集推广后空间为 $O(\Sigma)$。

## 正确性证明

`need[c]` 始终等于目标所需数量减去当前窗口中 `c` 的数量；正值表示缺口，非正值表示已满足或有富余。加入字符时，只有原本仍缺该字符才减少 `missing`；移出字符后，只有 `need` 变为正数才重新产生缺口，因此 `missing == 0` 当且仅当窗口覆盖 `t`。固定右端时，循环持续右移左端直到窗口首次失效，故期间记录了该右端对应的最短合法窗口。所有右端都被处理，取全局最短即为答案。

## 样例手推

扫描 `"ADOBEC"` 后首次覆盖 `"ABC"`，收缩得到 `"ADOBEC"`。继续到第二个 `A` 和后续字符，窗口依次缩短；右端到 `C` 时，左端可推进到 `B`，得到长度 4 的 `"BANC"`，再移除 `B` 就失效，因此它是该右端最短窗口。

## 易错点与方案比较

- 目标字符的重复次数必须逐个满足，不能只用集合。
- `need` 允许为负，代表窗口中该字符有富余。
- 更新答案必须发生在移出左端字符之前。
- 推荐缺口计数模板：只维护一个 `missing`，比每轮比较两个频次数组更稳定。

## 变种一：返回所有并列最短覆盖窗口

题目不再保证唯一答案。扫描时若发现更短窗口就清空结果，等长则追加起点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, t;
  cin >> s >> t;
  array<int, 128> need{};
  for (unsigned char character : t) {
    ++need[character];
  }
  int missing = t.size();
  int left = 0;
  int bestLength = numeric_limits<int>::max();
  vector<int> starts;
  for (int right = 0; right < static_cast<int>(s.size()); ++right) {
    unsigned char added = s[right];
    if (need[added] > 0) {
      --missing;
    }
    --need[added];
    while (missing == 0) {
      int length = right - left + 1;
      if (length < bestLength) {
        bestLength = length;
        starts.clear();
        starts.push_back(left);
      } else if (length == bestLength) {
        starts.push_back(left);
      }
      unsigned char removed = s[left++];
      ++need[removed];
      if (need[removed] > 0) {
        ++missing;
      }
    }
  }
  if (starts.empty()) {
    cout << -1 << '\n';
  } else {
    for (int start : starts) {
      cout << start << ' ' << s.substr(start, bestLength) << '\n';
    }
  }
}
```

时间 $O(|s|+|t|)$，结果空间与并列窗口数成正比。

## 变种二：字符是任意整数 token

固定 128 大小数组失效，改用哈希表；滑动窗口不变量不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<long long> source(n);
  unordered_map<long long, int> need;
  for (long long& value : source) {
    cin >> value;
  }
  for (int i = 0; i < m; ++i) {
    long long value;
    cin >> value;
    ++need[value];
  }
  int missing = m;
  int left = 0;
  int bestStart = -1;
  int bestLength = numeric_limits<int>::max();
  for (int right = 0; right < n; ++right) {
    if (need[source[right]] > 0) {
      --missing;
    }
    --need[source[right]];
    while (missing == 0) {
      if (right - left + 1 < bestLength) {
        bestLength = right - left + 1;
        bestStart = left;
      }
      ++need[source[left]];
      if (need[source[left]] > 0) {
        ++missing;
      }
      ++left;
    }
  }
  cout << bestStart << ' ' << (bestStart == -1 ? 0 : bestLength) << '\n';
}
```

期望时间 $O(n+m)$，空间 $O(\Sigma)$。

## 变种三：求至多含 k 种不同字符的最长子串

目标从“满足下界”变为“不同字符数不超过上界”，窗口在违规时收缩。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  int k;
  cin >> s >> k;
  array<int, 128> count{};
  int distinct = 0;
  int left = 0;
  int answer = 0;
  for (int right = 0; right < static_cast<int>(s.size()); ++right) {
    unsigned char added = s[right];
    if (count[added]++ == 0) {
      ++distinct;
    }
    while (distinct > k) {
      unsigned char removed = s[left++];
      if (--count[removed] == 0) {
        --distinct;
      }
    }
    answer = max(answer, right - left + 1);
  }
  cout << answer << '\n';
}
```

时间 $O(|s|)$，空间 $O(1)$。

## 变种四：最小覆盖子序列

要求窗口中按顺序包含 `t`，而非只满足频次。`start[j]` 记录当前扫描位置前，匹配到 `t[j]` 的子序列最晚起点；最晚起点给当前右端的最短窗口。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s, t;
  cin >> s >> t;
  vector<int> start(t.size(), -1);
  int bestStart = -1;
  int bestLength = numeric_limits<int>::max();
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    for (int j = static_cast<int>(t.size()) - 1; j >= 1; --j) {
      if (s[i] == t[j] && start[j - 1] != -1) {
        start[j] = start[j - 1];
      }
    }
    if (s[i] == t[0]) {
      start[0] = i;
    }
    if (start.back() != -1 && i - start.back() + 1 < bestLength) {
      bestLength = i - start.back() + 1;
      bestStart = start.back();
    }
  }
  cout << (bestStart == -1 ? "" : s.substr(bestStart, bestLength)) << '\n';
}
```

时间 $O(|s||t|)$，空间 $O(|t|)$。

## 可复现验证

在小字母表上随机生成长度不超过 12 的 `s` 与长度不超过 5 的 `t`，把线性窗口与平方枚举逐例比较；另外验证返回串的频次覆盖、最短性以及无解时为空。子序列变种与枚举所有窗口检查子序列交叉核对。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/minimum-window-substring/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-window-substring/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-56-lc17/">← [力扣 Top 56] LC 17 电话号码的字母组合 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-58-lc51/">[力扣 Top 58] LC 51 N 皇后 困难 →</a>
</nav>
