---
title: "[力扣每日一题] 2026-08-26｜LC 2904 最短且字典序最小的美丽子字符串"
---

# [力扣每日一题] 2026-08-26｜LC 2904 最短且字典序最小的美丽子字符串

<p class="daily-archive-kicker">2026-08-26 · 第 5/5 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-26 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=90bc6ac06c7d762137b0bc1e225ba24f8612e1bd4a09e55db7ff77fc832f057a -->
[力扣 2904｜最短且字典序最小的美丽子字符串](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/)

## 官方原始信息

- 题号：LC 2904
- 官方中文标题：最短且字典序最小的美丽子字符串
- 难度：中等
- 历史竞赛信息：第 367 场周赛 Q2，官方分值 4
- ZeroTracer 社区估算竞赛分：1483.304（抓取于 2026-08-26；不是力扣官方分值）
- 北京时间每日题日期：2026-08-26
- 官方链接：[leetcode.cn 题目页](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/)
- 函数签名：`string shortestBeautifulSubstring(string s, int k)`

### 原始题意

给定二进制字符串 `s` 和正整数 `k`。若一个子字符串中 `1` 的个数恰好为 `k`，就称它为美丽子字符串。先最小化所选子字符串的长度，再在所有最短候选中返回字典序最小者；若不存在，返回空字符串。

### 全部官方样例

```text
示例 1
输入：s = "100011001", k = 3
输出："11001"
解释：共有 7 个含恰好 3 个 1 的子字符串；最短长度是 5，长度为 5 的候选中字典序最小的是 "11001"。

示例 2
输入：s = "1011", k = 2
输出："11"
解释：美丽子字符串有 "101"、"011"、"11"；最短且字典序最小的是 "11"。

示例 3
输入：s = "000", k = 1
输出：""
解释：不存在含 1 的子字符串。
```

### 全部约束

- $1\le |s|\le100$
- $1\le k\le |s|$
- `s` 是二进制字符串。

## 最优结论与推荐记忆方案

记录所有 `1` 的位置 $p_0,p_1,\ldots,p_{m-1}$。最短美丽子字符串一定以 `1` 开始、以 `1` 结束，因此它一定恰好是某 $k$ 个连续 `1` 从 $p_i$ 到 $p_{i+k-1}$ 的紧致区间。枚举这些窗口，先比较长度，再比较字符串字典序即可。

推荐记住：**当目标只约束某字符的出现次数时，最短合法区间不会保留首尾无贡献字符；把问题转到目标字符的位置数组上。**

时间复杂度为 $O(n^2)$：候选只有 $O(n)$ 个，但构造、比较长度为 $O(n)$ 的字符串。空间复杂度为 $O(n)$。在本题 $n\le100$ 下，这是最清晰、稳定的实用解。

## 约束推导、溢出与边界

- 枚举左右端点有 $O(n^2)$ 个区间；若再逐字符统计 `1`，总时间是 $O(n^3)$，在 $n=100$ 时仍可运行，但重复计数明显。
- 前缀和能把区间计数降到 $O(1)$，整体为 $O(n^2)$；不过仍枚举了大量首尾为 `0`、不可能最短的区间。
- 位置数组只枚举 $m-k+1\le n$ 个真正可能最短的紧致区间。
- 长度、下标和 `1` 的数量都不超过 $100$，`int` 完全足够，没有整数溢出风险。

必须覆盖的边界：

- 整个字符串中 `1` 少于 $k$ 个：返回空串。
- $k=1$ 且存在 `1`：答案一定是 `"1"`。
- 所有字符都是 `1`：答案是长度为 $k$ 的全 `1` 字符串。
- 多个候选长度相同：必须比较候选内容，不能只保留最左者。
- 前导或结尾的 `0` 不会属于最短候选，但候选内部的 `0` 可能无法删除。

## 官方样例手推

样例 1 的 `1` 位置为 $[0,4,5,8]$，$k=3$：

- 窗口 $(0,4,5)$ 给出区间 `s[0..5] = "100011"`，长度 $6$；
- 窗口 $(4,5,8)$ 给出区间 `s[4..8] = "11001"`，长度 $5$。

第二个候选更短，所以答案是 `"11001"`。这也说明只需要考察连续的 $k$ 个 `1`，不必枚举题面列出的所有更宽区间。

## 解法一：三重循环暴力

枚举每个非空子字符串，再逐字符数 `1`。若数量恰为 $k$，按“长度更短，或同长但字典序更小”更新答案。它直接覆盖全部候选，因此正确。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string shortestBeautifulSubstring(string s, int k) {
    string ans;
    int n = static_cast<int>(s.size());
    for (int l = 0; l < n; ++l) {
      for (int r = l; r < n; ++r) {
        int ones = 0;
        for (int i = l; i <= r; ++i) ones += s[i] == '1';
        if (ones != k) continue;
        string cur = s.substr(l, r - l + 1);
        if (ans.empty() || cur.size() < ans.size() ||
            (cur.size() == ans.size() && cur < ans)) {
          ans = cur;
        }
      }
    }
    return ans;
  }
};
```

时间复杂度 $O(n^3)$，空间复杂度 $O(n)$。瓶颈是重叠区间反复统计同一批字符。

## 解法二：前缀和消除重复计数

令 $pre[i]$ 表示 `s[0..i-1]` 中 `1` 的个数，则区间 $[l,r]$ 的 `1` 数量是 $pre[r+1]-pre[l]$。枚举区间不变，但每次计数降为 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string shortestBeautifulSubstring(string s, int k) {
    int n = static_cast<int>(s.size());
    vector<int> pre(n + 1);
    for (int i = 0; i < n; ++i) pre[i + 1] = pre[i] + (s[i] == '1');
    string ans;
    for (int l = 0; l < n; ++l) {
      for (int r = l; r < n; ++r) {
        if (pre[r + 1] - pre[l] != k) continue;
        string cur = s.substr(l, r - l + 1);
        if (ans.empty() || cur.size() < ans.size() ||
            (cur.size() == ans.size() && cur < ans)) {
          ans = cur;
        }
      }
    }
    return ans;
  }
};
```

时间复杂度 $O(n^2)$，空间复杂度 $O(n)$。它消除了计数重复，但仍访问了 $O(n^2)$ 个区间。

## 最佳实用解：枚举连续的 k 个 1

### 算法

1. 扫描 `s`，把所有 `1` 的下标加入 `pos`。
2. 若 `pos.size() < k`，返回空串。
3. 对每个 $0\le i\le m-k$，取紧致区间 $[pos[i],pos[i+k-1]]$。
4. 用长度优先、字典序次优的规则更新答案。

### 正确性证明

**引理 1**：任意最短美丽子字符串都以 `1` 开始并以 `1` 结束。

若首字符是 `0`，删除它后 `1` 的数量不变而长度更短，与最短性矛盾；尾字符同理。

**引理 2**：任意最短美丽子字符串中的 $k$ 个 `1`，在全局 `1` 位置数组中必为连续的 $k$ 项。

子字符串覆盖的是原串的连续区间。若它包含 $p_i$ 和 $p_j$，就必然包含二者之间的全部 `1`；因此其中的 $k$ 个位置在 `pos` 中连续。

**引理 3**：对每组连续的 $k$ 个 `1`，其唯一可能成为全局最短候选的区间是从第一个 `1` 到最后一个 `1` 的紧致区间。

任何更宽区间只能在两端额外加入 `0`，不会改变 `1` 的数量，只会增加长度。

**定理**：算法返回最短且字典序最小的美丽子字符串。

由引理 1–3，所有可能的最短答案都在算法枚举的紧致区间中。算法先取最短长度，再在同长候选中取字典序最小者，故结论成立。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string shortestBeautifulSubstring(string s, int k) {
    vector<int> pos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') pos.push_back(i);
    }
    if (static_cast<int>(pos.size()) < k) return "";
    string ans;
    for (int i = 0; i + k <= static_cast<int>(pos.size()); ++i) {
      string cur = s.substr(pos[i], pos[i + k - 1] - pos[i] + 1);
      if (ans.empty() || cur.size() < ans.size() ||
          (cur.size() == ans.size() && cur < ans)) {
        ans = cur;
      }
    }
    return ans;
  }
};
```

时间复杂度 $O(n^2)$，空间复杂度 $O(n)$。若只计算候选端点而不复制、比较字符串，位置窗口扫描本身是 $O(n)$。

## 易错点

- 目标是“恰好 $k$ 个 `1`”，不是至少 $k$ 个。
- 优先级是先最短、再字典序；不能把全局字典序最小放在长度之前。
- 同长度候选不能默认最左者字典序最小。
- 候选必须使用连续的 $k$ 个 `1`；跳过中间 `1` 会使区间实际包含超过 $k$ 个。
- 没有候选时返回 `""`，不要返回原串或哨兵字符串。

## Follow-up 1：返回全部最优起点

新要求是返回所有“长度最短且内容等于字典序最小答案”的子字符串起点。先求出最佳字符串，再二次枚举位置窗口并比较内容；重复出现的相同字符串会保留全部下标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> allBestStarts(string s, int k) {
    vector<int> pos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') pos.push_back(i);
    }
    string best;
    vector<pair<int, string>> candidates;
    for (int i = 0; i + k <= static_cast<int>(pos.size()); ++i) {
      string cur = s.substr(pos[i], pos[i + k - 1] - pos[i] + 1);
      candidates.push_back({pos[i], cur});
      if (best.empty() || cur.size() < best.size() ||
          (cur.size() == best.size() && cur < best)) {
        best = cur;
      }
    }
    vector<int> ans;
    for (const auto &[start, cur] : candidates) {
      if (cur == best) ans.push_back(start);
    }
    return ans;
  }
};
```

时间、空间均为 $O(n^2)$，因为保存了所有候选字符串；只保存端点并二次截取可把额外空间降为 $O(n)$。

## Follow-up 2：固定字符串，多组 k 询问

给定同一个 `s`，每次询问不同的 $k$。`1` 的位置只预处理一次；每个询问独立扫描长度为 $k$ 的位置窗口。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<string> shortestForQueries(string s, const vector<int> &queries) {
    vector<int> pos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') pos.push_back(i);
    }
    vector<string> out;
    for (int k : queries) {
      string best;
      for (int i = 0; i + k <= static_cast<int>(pos.size()); ++i) {
        string cur = s.substr(pos[i], pos[i + k - 1] - pos[i] + 1);
        if (best.empty() || cur.size() < best.size() ||
            (cur.size() == best.size() && cur < best)) {
          best = cur;
        }
      }
      out.push_back(best);
    }
    return out;
  }
};
```

预处理 $O(n)$；每问最多构造 $O(n)$ 个长度 $O(n)$ 的候选，最坏 $O(n^2)$，总时间 $O(n+Qn^2)$，额外空间 $O(n+Qn)$。

## Follow-up 3：字符在线追加

固定 $k$，字符串从空串开始逐字符追加；每次追加后返回当前答案。每出现一个新的 `1`，只会新增一个以它为第 $k$ 个 `1` 的紧致窗口，比较这一项即可；追加 `0` 不会产生新的最短候选。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class OnlineBeautiful {
  int k;
  string s;
  vector<int> pos;
  string best;
public:
  explicit OnlineBeautiful(int target) : k(target) {}
  string append(char ch) {
    s.push_back(ch);
    if (ch == '0') return best;
    pos.push_back(static_cast<int>(s.size()) - 1);
    if (static_cast<int>(pos.size()) < k) return best;
    int left = pos[pos.size() - k];
    string cur = s.substr(left, pos.back() - left + 1);
    if (best.empty() || cur.size() < best.size() ||
        (cur.size() == best.size() && cur < best)) {
      best = cur;
    }
    return best;
  }
};
int main() {
  int k;
  string stream;
  cin >> k >> stream;
  OnlineBeautiful solver(k);
  for (char ch : stream) cout << solver.append(ch) << '\n';
}
```

每次新增的窗口只有一个；字符串比较使单次最坏 $O(n)$、总时间 $O(n^2)$，空间 $O(n)$。

## Follow-up 4：规模放大到 2×10^5

当 $n\le2\times10^5$ 时，候选仍只有 $O(n)$ 个，但逐个比较长字符串可能退化到 $O(n^2)$。先构建后缀数组；对于同一最短长度的两个候选，比较其起点后缀的排名即可决定字典序（若候选内容完全相同，任选其一）。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> suffixRanks(const string &s) {
    int n = static_cast<int>(s.size());
    vector<int> sa(n), rank(n), next_rank(n);
    iota(sa.begin(), sa.end(), 0);
    for (int i = 0; i < n; ++i) rank[i] = s[i];
    for (int len = 1; len < n; len *= 2) {
      sort(sa.begin(), sa.end(), [&](int i, int j) {
        if (rank[i] != rank[j]) return rank[i] < rank[j];
        int ri = i + len < n ? rank[i + len] : -1;
        int rj = j + len < n ? rank[j + len] : -1;
        return ri < rj;
      });
      next_rank[sa[0]] = 0;
      for (int p = 1; p < n; ++p) {
        int i = sa[p - 1], j = sa[p];
        pair<int, int> left = {rank[i], i + len < n ? rank[i + len] : -1};
        pair<int, int> right = {rank[j], j + len < n ? rank[j + len] : -1};
        next_rank[j] = next_rank[i] + (left != right);
      }
      rank.swap(next_rank);
      if (rank[sa.back()] == n - 1) break;
    }
    return rank;
  }
public:
  string shortestBeautifulSubstring(string s, int k) {
    vector<int> pos;
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
      if (s[i] == '1') pos.push_back(i);
    }
    if (static_cast<int>(pos.size()) < k) return "";
    vector<int> rank = suffixRanks(s);
    int best_left = -1, best_len = numeric_limits<int>::max();
    for (int i = 0; i + k <= static_cast<int>(pos.size()); ++i) {
      int left = pos[i], len = pos[i + k - 1] - left + 1;
      if (len < best_len ||
          (len == best_len && rank[left] < rank[best_left])) {
        best_left = left;
        best_len = len;
      }
    }
    return s.substr(best_left, best_len);
  }
};
```

该实现用比较排序构建后缀数组，时间复杂度 $O(n\log^2 n)$、空间复杂度 $O(n)$；用基数排序可进一步做到 $O(n\log n)$。位置窗口扫描仍为 $O(n)$。

## 可复现验证说明

- 三个官方样例分别得到 `"11001"`、`"11"`、`""`。
- 最优实现重新以 C++23 编译。
- 以三重循环暴力为 oracle，穷举所有长度 $1$ 到 $12$ 的二进制字符串及所有合法 $k$，逐项比较最优实现；共 $90,114$ 组，全部一致。

## 来源与 Algo 状态

- [力扣中国官方题目页](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/)
- [力扣中国每日一题入口](https://leetcode.cn/problemset/)

Algo 发布状态在本轮网站门禁和线上核验完成后更新。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2253-b/">← [codeforces] CF Educational Round 193 Div.2 B Hypercarp and the Control Panel</a>
<span class="daily-archive-pager__empty"></span>
</nav>
