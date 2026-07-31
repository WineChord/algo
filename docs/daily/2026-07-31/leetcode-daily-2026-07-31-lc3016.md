---
title: "[力扣每日一题] 2026-07-31｜LC 3016 输入单词需要的最少按键次数 II"
---

# [力扣每日一题] 2026-07-31｜LC 3016 输入单词需要的最少按键次数 II

<p class="daily-archive-kicker">2026-07-31 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a43107ba30b50850072e4bb2a2b7799fb2bde88baf6662aa582ec067acaf0154 -->
## 官方原始信息

- 日期：2026-07-31（Asia/Shanghai）
- 题号：LC 3016
- 官方中文标题：输入单词需要的最少按键次数 II
- 官方难度：中等
- 官方链接：[输入单词需要的最少按键次数 II](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/?envType=daily-question&envId=2026-07-31)

### 原始题意

字符串 `word` 只含小写英文字母。电话按键 2 到 9 共 8 个按键可重新映射字母：每个按键可映射任意多个不同字母，每个小写字母必须恰好属于一个按键。在某个按键上排第 1 个字母按 1 次，排第 2 个字母按 2 次，依此类推。求输入整个 `word` 的最少按键总次数。按键 0、1、`*` 与 `#` 不映射字母；并非每个可用按键都必须实际承载 `word` 中出现的字母。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int minimumPushes(string word);
};
```

### 全部官方样例

```text
输入：word = "abcde"
输出：5
解释：把五个字母分别放在五个按键的第一位置，每个字符只需按一次。
```

```text
输入：word = "xyzxyzxyzxyz"
输出：12
解释：x、y、z 各出现 4 次，分别放在三个按键的第一位置，总成本为 4+4+4=12。
```

```text
输入：word = "aabbccddeeffgghhiiiiii"
输出：24
解释：出现频率最高的 i 放在第一层；八个最常用字母占据 8 个成本为 1 的槽位，剩余字母进入下一层，最小总成本为 24。
```

### 全部约束

- $1\le |word|\le10^5$。
- `word` 只含小写英文字母。

## 约束推导与核心模型

映射的具体按键编号不重要，重要的是 26 个可用槽位的按压成本：8 个成本 1、8 个成本 2、8 个成本 3、2 个成本 4。若字母 `c` 出现 `freq[c]` 次并被放入成本 `cost[c]` 的槽位，它对总答案贡献 `freq[c] × cost[c]`。因此问题化为：把 26 个频率与已排序的 26 个槽位成本配对，使加权和最小。

## 解法递进

### 解法一：穷举出现字母到成本槽位的分配

下面的回溯对每个出现过的字母尝试所有尚未使用的槽位，正确但规模稍大就不可行，只用于理解和小规模 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<int> frequency;
  vector<int> cost;
  vector<char> used;
  long long best;
  void search(int index, long long total) {
    if (total >= best) {
      return;
    }
    if (index == static_cast<int>(frequency.size())) {
      best = total;
      return;
    }
    for (int slot = 0; slot < 26; ++slot) {
      if (!used[slot]) {
        used[slot] = true;
        search(index + 1, total + 1LL * frequency[index] * cost[slot]);
        used[slot] = false;
      }
    }
  }
public:
  int minimumPushes(string word) {
    array<int, 26> count{};
    for (char character : word) {
      ++count[character - 'a'];
    }
    for (int value : count) {
      if (value > 0) {
        frequency.push_back(value);
      }
    }
    for (int slot = 0; slot < 26; ++slot) {
      cost.push_back(slot / 8 + 1);
    }
    used.assign(26, false);
    best = numeric_limits<long long>::max();
    search(0, 0);
    return best;
  }
};
```

若有 $d$ 个不同字母，时间为 $O(P(26,d))$，空间 $O(d+26)$；只适合很小的 $d$。

### 最佳实用解：频率降序匹配成本升序

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int minimumPushes(string word) {
    array<int, 26> frequency{};
    for (char character : word) {
      ++frequency[character - 'a'];
    }
    sort(frequency.begin(), frequency.end(), greater<int>());
    int answer = 0;
    for (int index = 0; index < 26; ++index) {
      answer += frequency[index] * (index / 8 + 1);
    }
    return answer;
  }
};
```

统计时间 $O(|word|)$，对固定 26 项排序可视为 $O(1)$；空间 $O(1)$。答案最多为 $4\times10^5$，`int` 足够。

## 正确性证明

考虑任意两个字母，频率分别为 $f_a\ge f_b$，所占槽位成本为 $c_a>c_b$。交换它们前后的成本差为

$$
(f_ac_a+f_bc_b)-(f_ac_b+f_bc_a)=(f_a-f_b)(c_a-c_b)\ge0.
$$

因此让高频字母占更高成本槽位永远不会更优；任何存在这种逆序的方案都可交换而不增成本。不断消除逆序后，必得到“频率降序、成本升序”的配对，故该方案全局最优。代码恰按此顺序计算。

## 样例手推

第三个样例中 `i` 出现 6 次，`a` 到 `h` 各出现 2 次。最高频的 `i` 和另外 7 个字母占 8 个成本为 1 的槽位，剩下一个频率 2 的字母占成本 2 的槽位，总成本为 $6+7\times2+2\times2=24$。

## 易错点与方案比较

- 共有 8 个按键，所以每一层恰有 8 个槽位，而不是传统映射中每键最多 3 或 4 个字母。
- 必须统计出现次数；只按不同字母数计算会忽略高频字母的收益。
- 没出现的字母频率为 0，排在末尾即可，仍能补全“每个字母恰好映射一次”的要求。
- 推荐记忆“频率降序 × 槽位成本升序”的交换论证；具体按键编号只在需要恢复映射时再构造。

## 变种一：可用按键数改为 b

若有 `b` 个可重新映射的按键，第 `index` 个升序槽位成本为 `index / b + 1`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int keys;
  string word;
  cin >> keys >> word;
  array<int, 26> frequency{};
  for (char character : word) {
    ++frequency[character - 'a'];
  }
  sort(frequency.begin(), frequency.end(), greater<int>());
  long long answer = 0;
  for (int index = 0; index < 26; ++index) {
    answer += 1LL * frequency[index] * (index / keys + 1);
  }
  cout << answer << '\n';
}
```

时间 $O(|word|+26\log26)$，空间 $O(1)$。

## 变种二：恢复一份最优按键映射

频率相同的字母按字母序打破平局。第 `i` 个字母放到按键 `2+i%8` 的第 `i/8+1` 个位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string word;
  cin >> word;
  array<int, 26> count{};
  for (char character : word) {
    ++count[character - 'a'];
  }
  vector<pair<int, char>> letters;
  for (int i = 0; i < 26; ++i) {
    letters.push_back({-count[i], static_cast<char>('a' + i)});
  }
  sort(letters.begin(), letters.end());
  array<vector<char>, 8> mapping;
  long long cost = 0;
  for (int i = 0; i < 26; ++i) {
    mapping[i % 8].push_back(letters[i].second);
    cost += 1LL * (-letters[i].first) * (i / 8 + 1);
  }
  cout << cost << '\n';
  for (int key = 0; key < 8; ++key) {
    cout << key + 2 << ':';
    for (char character : mapping[key]) {
      cout << ' ' << character;
    }
    cout << '\n';
  }
}
```

时间 $O(|word|+26\log26)$，空间 $O(26)$。

## 变种三：每个槽位有任意给定成本

输入至少 26 个可用槽位成本。重排不等式仍成立：频率降序与成本升序配对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string word;
  int slots;
  cin >> word >> slots;
  vector<long long> costs(slots);
  for (long long& cost : costs) {
    cin >> cost;
  }
  if (slots < 26) {
    cout << -1 << '\n';
    return 0;
  }
  array<long long, 26> frequency{};
  for (char character : word) {
    ++frequency[character - 'a'];
  }
  sort(frequency.begin(), frequency.end(), greater<long long>());
  sort(costs.begin(), costs.end());
  long long answer = 0;
  for (int i = 0; i < 26; ++i) {
    answer += frequency[i] * costs[i];
  }
  cout << answer << '\n';
}
```

时间 $O(|word|+slots\log slots)$，空间 $O(slots)$。

## 变种四：在线增删字符并查询最小成本

字母表只有 26 个字符，每次查询重新排序频率即可，代码简单且每次仅 $O(26\log26)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long minimumCost(array<long long, 26> frequency) {
  sort(frequency.begin(), frequency.end(), greater<long long>());
  long long answer = 0;
  for (int index = 0; index < 26; ++index) {
    answer += frequency[index] * (index / 8 + 1);
  }
  return answer;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  array<long long, 26> frequency{};
  while (q--) {
    char operation;
    cin >> operation;
    if (operation == '?') {
      cout << minimumCost(frequency) << '\n';
    } else {
      char character;
      cin >> character;
      if (operation == '+') {
        ++frequency[character - 'a'];
      } else if (frequency[character - 'a'] > 0) {
        --frequency[character - 'a'];
      }
    }
  }
}
```

更新 $O(1)$，查询 $O(26\log26)$，空间 $O(1)$。

## 可复现验证

对不同字母数不超过 8 的随机短串，把排序贪心与穷举槽位分配逐例比较；对一般随机串再与直接按频率分组计算的独立实现比较。覆盖单一字母、恰好 8/9/16/17/24/25/26 种字母和长度 $10^5$。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/)
- [力扣中国每日一题入口](https://leetcode.cn/problemset/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/?envType=daily-question&envId=2026-07-31)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2247-e/">← [codeforces] CF Round 1111 Div.2 E Build a Tree</a>
<span class="daily-archive-pager__empty"></span>
</nav>
