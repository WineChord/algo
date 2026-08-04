---
title: "[力扣 Top 105] LC 169 多数元素 简单"
---

# [力扣 Top 105] LC 169 多数元素 简单

<p class="daily-archive-kicker">2026-08-05 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=e1e105912bb5d11724846dc3989d2de53cf2e9d1b00cabe2999cddc8daeaaa17 -->
## 官方原始信息

- Top 排名：105
- 题号：LC 169
- 官方中文标题：多数元素
- 官方难度：简单
- 官方链接：[多数元素](https://leetcode.cn/problems/majority-element/)

### 原始题意

给定非空数组 `nums`，返回出现次数严格大于 $\lfloor n/2\rfloor$ 的元素。题目保证该元素存在。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int majorityElement(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [3,2,3]
输出：3
```

```text
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

### 全部约束

- $n=nums.length$。
- $1\le n\le5\times10^4$。
- $-10^9\le nums[i]\le10^9$。
- 输入保证多数元素存在。
- 进阶目标：时间 $O(n)$、额外空间 $O(1)$。

## 约束推导与观察

多数元素出现超过一半，因此把一个多数元素与任意一个非多数元素配对抵消后，多数元素仍至少剩一个。Boyer–Moore 投票正是在线执行这种抵消：计数归零意味着已扫描前缀可以完全配平，不会影响后缀中最终多数元素的身份。

元素值需 `int`，票数最大为 $n$，也可用 `int`；不涉及乘法溢出。

## 解法递进

### 解法一：哈希计数

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int majorityElement(vector<int>& nums) {
    unordered_map<int, int> count;
    for (int value : nums) {
      if (++count[value] > static_cast<int>(nums.size()) / 2) {
        return value;
      }
    }
    return 0;
  }
};
```

平均时间 $O(n)$，空间 $O(n)$。它直接但未达到常量空间进阶目标。

### 解法二：排序后取中位位置

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int majorityElement(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    return nums[nums.size() / 2];
  }
};
```

时间 $O(n\log n)$，排序栈空间依实现而定，并修改输入。多数元素连续块长度超过一半，必覆盖中间位置。

### 最佳实用解：Boyer–Moore 投票

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int majorityElement(vector<int>& nums) {
    int candidate = 0;
    int votes = 0;
    for (int value : nums) {
      if (votes == 0) {
        candidate = value;
      }
      votes += value == candidate ? 1 : -1;
    }
    return candidate;
  }
};
```

时间 $O(n)$，空间 $O(1)$，达到进阶目标。题目保证存在多数，因此无需第二遍验证。

## 正确性证明

把扫描过程中的一次 `+1` 与后续一次 `-1` 看作删除两个不同元素。删除一对不同元素不会改变原多数元素在剩余序列中仍比所有非多数元素总数更多这一事实。计数归零时，当前前缀已被不同值配对消去；重新选择候选不会丢失多数信息。全数组所有可能的异值对都抵消后，多数元素必有剩余，所以最终候选就是多数元素。

## 样例手推

`[2,2,1,1,1,2,2]`：候选 2 的票数依次为 1、2、1、0；第五个值把候选改为 1、票数 1；随后两个 2 抵消并在归零后重新成为候选，最终得到 2。单元素数组第一步即成为候选。

## 易错点与方案比较

- 多数定义是严格大于一半，不是大于等于。
- 若题目不保证多数存在，第一遍只产生候选，必须第二遍核验。
- 投票数不能解释为真实出现次数，它是尚未抵消的净票。
- 哈希最直观，排序会改输入；投票同时达到线性时间和常量空间，应优先记忆。

## 变种一：多数元素不保证存在

新定义：若没有出现次数超过一半的值，返回空。第一遍投票，第二遍精确计数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> values(n);
  int candidate = 0;
  int votes = 0;
  for (int& value : values) {
    cin >> value;
    if (votes == 0) {
      candidate = value;
    }
    votes += value == candidate ? 1 : -1;
  }
  int occurrences = count(values.begin(), values.end(), candidate);
  if (occurrences > n / 2) {
    cout << candidate << '\n';
  } else {
    cout << "NONE\n";
  }
}
```

时间 $O(n)$，空间 $O(n)$ 仅来自示例输入存储；若数据可重放则算法状态仍为 $O(1)$。

## 变种二：找出所有出现次数超过 $n/3$ 的元素

新定义：答案最多两个。维护两个候选与票数，抵消三个互异元素，再二次验证。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> majorityElement(vector<int>& nums) {
    int first = 0;
    int second = 1;
    int firstVotes = 0;
    int secondVotes = 0;
    for (int value : nums) {
      if (value == first) {
        ++firstVotes;
      } else if (value == second) {
        ++secondVotes;
      } else if (firstVotes == 0) {
        first = value;
        firstVotes = 1;
      } else if (secondVotes == 0) {
        second = value;
        secondVotes = 1;
      } else {
        --firstVotes;
        --secondVotes;
      }
    }
    vector<int> answer;
    for (int candidate : {first, second}) {
      if (count(nums.begin(), nums.end(), candidate) > static_cast<int>(nums.size()) / 3 &&
          find(answer.begin(), answer.end(), candidate) == answer.end()) {
        answer.push_back(candidate);
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(1)$；对应 [LC 229](https://leetcode.cn/problems/majority-element-ii/)。

## 变种三：带正权重的多数元素

新定义：每个记录 `(value, weight)` 权重为正，目标值权重和超过总权重一半。把票数增减从 1 改为权重；若反方权重更大，候选切换并保留差额。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  long long balance = 0;
  int candidate = 0;
  vector<pair<int, long long>> records(n);
  for (auto& [value, weight] : records) {
    cin >> value >> weight;
    if (balance == 0) {
      candidate = value;
      balance = weight;
    } else if (value == candidate) {
      balance += weight;
    } else if (balance > weight) {
      balance -= weight;
    } else {
      candidate = value;
      balance = weight - balance;
    }
  }
  long long total = 0;
  long long chosen = 0;
  for (auto [value, weight] : records) {
    total += weight;
    if (value == candidate) {
      chosen += weight;
    }
  }
  cout << (chosen > total - chosen ? to_string(candidate) : "NONE") << '\n';
}
```

时间 $O(n)$，空间 $O(n)$ 用于验证；权重和使用 64 位。无权投票的逐项抵消不足以处理大权重记录。

## 变种四：静态区间多数查询

新定义：多次询问 `[l,r]`，若区间有严格多数则输出，否则 `NONE`。线段树合并 Boyer–Moore 候选，再用每个值的有序位置表二分验证。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Vote {
  int candidate = 0;
  int balance = 0;
};
Vote mergeVote(Vote left, Vote right) {
  if (!left.balance) {
    return right;
  }
  if (!right.balance) {
    return left;
  }
  if (left.candidate == right.candidate) {
    return {left.candidate, left.balance + right.balance};
  }
  return left.balance > right.balance ? Vote{left.candidate, left.balance - right.balance}
                                      : Vote{right.candidate, right.balance - left.balance};
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  int size = 1;
  while (size < n) {
    size *= 2;
  }
  vector<Vote> tree(2 * size);
  unordered_map<int, vector<int>> positions;
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    tree[size + i] = {value, 1};
    positions[value].push_back(i);
  }
  for (int node = size - 1; node; --node) {
    tree[node] = mergeVote(tree[node * 2], tree[node * 2 + 1]);
  }
  while (q--) {
    int left, right;
    cin >> left >> right;
    --left;
    int originalLeft = left;
    int originalRight = right;
    Vote fromLeft, fromRight;
    for (left += size, right += size; left < right; left /= 2, right /= 2) {
      if (left & 1) {
        fromLeft = mergeVote(fromLeft, tree[left++]);
      }
      if (right & 1) {
        fromRight = mergeVote(tree[--right], fromRight);
      }
    }
    int candidate = mergeVote(fromLeft, fromRight).candidate;
    const vector<int>& list = positions[candidate];
    int occurrences = lower_bound(list.begin(), list.end(), originalRight) -
        lower_bound(list.begin(), list.end(), originalLeft);
    string answer = occurrences * 2 > originalRight - originalLeft ? to_string(candidate) : "NONE";
    cout << answer << '\n';
  }
}
```

预处理 $O(n)$，每问 $O(\log n)$，空间 $O(n)$。单次全数组投票无法直接证明任意子区间候选。

## 验证说明

本轮将七段代码按 C++23 编译；哈希、排序、投票与朴素计数会对拍 30,000 个保证存在多数的随机数组，并覆盖单元素、负数和刚超过一半。无保证、$n/3$、加权与区间版本分别用精确计数 oracle 核验。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/majority-element/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-104-lc347/">← [力扣 Top 104] LC 347 前 K 个高频元素 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-106-lc287/">[力扣 Top 106] LC 287 寻找重复数 中等 →</a>
</nav>
