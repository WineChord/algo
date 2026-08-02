---
title: "[力扣 Top 85] LC 152 乘积最大子数组 中等"
---

# [力扣 Top 85] LC 152 乘积最大子数组 中等

<p class="daily-archive-kicker">2026-08-03 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3fa2da32a5d00a585512c52ef54f8cd12ab28220783af2f1b32d0ddee0b0ce3b -->
## 官方原始信息

- Top 排名：85
- 题号：LC 152
- 官方中文标题：乘积最大子数组
- 官方难度：中等
- 官方链接：[乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/)

### 原始题意

给定整数数组 `nums`，找出乘积最大的非空连续子数组并返回乘积。官方保证任意前缀或后缀的乘积以及答案都在 32 位整数范围内。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maxProduct(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [2,3,-2,4]
输出：6
解释：子数组 [2,3] 的乘积为 6。
```

```text
输入：nums = [-2,0,-1]
输出：0
解释：不能跨过 0 选择 [-2,-1]。
```

### 全部约束

- $1\le nums.length\le2\times10^4$。
- $-10\le nums_i\le10$。
- 任意前缀或后缀乘积以及答案保证在 32 位有符号整数范围内。

## 约束推导与状态

连续子数组有 $O(n^2)$ 个。和问题只需维护最大前缀，但乘以负数会让最大与最小交换角色：很负的积再乘负数可能成为最大值。因此同时维护以当前位置结尾的最大积 `maximum` 与最小积 `minimum`。

对新值 $x$，以当前位置结尾的子数组只有三类：单独取 $x$、把上一最大积乘 $x$、把上一最小积乘 $x$。新最大值取三者最大，新最小值取三者最小。零会自然让状态在 0 与重新从后续元素开始之间选择，无需分段特判。

## 解法递进

### 解法一：枚举所有连续子数组

固定左端点，向右累乘并更新答案。它覆盖全部候选，可作为随机对拍 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    int answer = nums[0];
    for (int left = 0; left < static_cast<int>(nums.size()); ++left) {
      int product = 1;
      for (int right = left; right < static_cast<int>(nums.size()); ++right) {
        product *= nums[right];
        answer = max(answer, product);
      }
    }
    return answer;
  }
};
```

时间 $O(n^2)$，空间 $O(1)$，上限会超时。

### 最佳实用解：同步维护最大与最小结尾积

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maxProduct(vector<int>& nums) {
    int maximum = nums[0];
    int minimum = nums[0];
    int answer = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
      int previousMaximum = maximum;
      int previousMinimum = minimum;
      maximum = max({nums[i], previousMaximum * nums[i], previousMinimum * nums[i]});
      minimum = min({nums[i], previousMaximum * nums[i], previousMinimum * nums[i]});
      answer = max(answer, maximum);
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$，是约束下的最优解。

## 正确性证明

归纳假设 `maximum/minimum` 分别是以上一位置结尾的所有非空子数组乘积极值。任何以当前位置结尾的非空子数组要么只含当前元素，要么由某个以上一位置结尾的子数组追加当前值。乘以正数时极值来自原最大/最小，乘以负数时二者交换，乘以零时都归零；统一取三候选最大和最小覆盖所有情况。故新状态正确。所有连续子数组都有唯一右端点，逐位置取 `maximum` 的全局最大值便是答案。

## 样例手推

`[2,3,-2,4]`：起始 `(max,min)=(2,2)`；读 3 得 `(6,3)`，答案 6；读 -2 得 `(-2,-12)`；读 4 得 `(4,-48)`，答案仍 6。`[-2,0,-1]` 在 0 处状态变为 `(0,0)`，之后 -1 的最大结尾积为 0，但单独 -1 更小，最终答案 0，不能跨零组合首尾。

## 易错点与方案比较

- 必须同时保存上一轮最大与最小；先更新 `maximum` 再用它算 `minimum` 会污染状态。
- 答案初始化为首元素而非 0，否则全负且无零数组会出错。
- 连续性意味着零会切断子数组，不能跳过零。
- 官方保证中间相关乘积不溢出 `int`；若去掉该保证，应改用更宽或任意精度类型。
- 前后缀扫描也能以 $O(n)$ 求解，但最大/最小 DP 更容易扩展到恢复区间与删除变种，优先推荐。

## 变种一：恢复最优子数组区间

新定义：返回最大乘积及字典序最小的一基区间。给最大、最小状态同步记录起点，比较三候选并在全局更新时保存区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long& value : a)
    cin >> value;
  long long maximum = a[0], minimum = a[0], answer = a[0];
  int maximumStart = 0, minimumStart = 0, answerLeft = 0, answerRight = 0;
  for (int i = 1; i < n; ++i) {
    vector<pair<long long, int>> candidates{
        {a[i], i}, {maximum * a[i], maximumStart}, {minimum * a[i], minimumStart}};
    auto largest = max_element(candidates.begin(), candidates.end(), [](auto x, auto y) {
      return x.first != y.first ? x.first < y.first : x.second > y.second;
    });
    auto smallest = min_element(candidates.begin(), candidates.end(), [](auto x, auto y) {
      return x.first != y.first ? x.first < y.first : x.second < y.second;
    });
    maximum = largest->first;
    maximumStart = largest->second;
    minimum = smallest->first;
    minimumStart = smallest->second;
    if (maximum > answer ||
        (maximum == answer &&
            pair<int, int>{maximumStart, i} < pair<int, int>{answerLeft, answerRight})) {
      answer = maximum;
      answerLeft = maximumStart;
      answerRight = i;
    }
  }
  cout << answer << '\n' << answerLeft + 1 << ' ' << answerRight + 1 << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：允许删除子数组内至多一个元素

新定义：选择一个连续区间，可不删除或删除其中一个元素，剩余元素顺序拼接后求最大乘积。状态增加 `deletedMaximum/deletedMinimum`；它们来自此前已删除状态继续乘，或删除当前元素而继承未删除状态。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long& value : a)
    cin >> value;
  long long keepMaximum = a[0], keepMinimum = a[0], answer = a[0];
  long long dropMaximum = a[0], dropMinimum = a[0];
  for (int i = 1; i < n; ++i) {
    long long oldMaximum = keepMaximum, oldMinimum = keepMinimum;
    long long oldDropMaximum = dropMaximum, oldDropMinimum = dropMinimum;
    keepMaximum = max({a[i], oldMaximum * a[i], oldMinimum * a[i]});
    keepMinimum = min({a[i], oldMaximum * a[i], oldMinimum * a[i]});
    dropMaximum = max({a[i], oldMaximum, oldDropMaximum * a[i], oldDropMinimum * a[i]});
    dropMinimum = min({a[i], oldMinimum, oldDropMaximum * a[i], oldDropMinimum * a[i]});
    answer = max({answer, keepMaximum, dropMaximum});
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。区间最终必须至少保留一个元素，初始化禁止在首位形成空结果。

## 变种三：数组首尾相接

新定义：允许连续子数组跨越末尾与开头，但每个元素最多使用一次。对小规模版本枚举起点并最多扩展 $n$ 个位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long& value : a)
    cin >> value;
  long long answer = a[0];
  for (int start = 0; start < n; ++start) {
    long long product = 1;
    for (int length = 1; length <= n; ++length) {
      product *= a[(start + length - 1) % n];
      answer = max(answer, product);
    }
  }
  cout << answer << '\n';
}
```

时间 $O(n^2)$，空间 $O(1)$。原线性状态失效，因为跨边界区间同时依赖前缀与后缀。

## 变种四：答案扩展到 128 位

新定义：去掉 32 位保证，但承诺所有转移结果可放入有符号 128 位整数。状态改用 `__int128`，输出时自行转换十进制，避免任何 64 位中间溢出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string toString(__int128 value) {
  if (value == 0)
    return "0";
  bool negative = value < 0;
  if (negative)
    value = -value;
  string result;
  while (value > 0) {
    result.push_back('0' + value % 10);
    value /= 10;
  }
  if (negative)
    result.push_back('-');
  reverse(result.begin(), result.end());
  return result;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<__int128> a(n);
  for (__int128& value : a) {
    long long input;
    cin >> input;
    value = input;
  }
  __int128 maximum = a[0], minimum = a[0], answer = a[0];
  for (int i = 1; i < n; ++i) {
    __int128 oldMaximum = maximum, oldMinimum = minimum;
    maximum = max(a[i], max(oldMaximum * a[i], oldMinimum * a[i]));
    minimum = min(a[i], min(oldMaximum * a[i], oldMinimum * a[i]));
    answer = max(answer, maximum);
  }
  cout << toString(answer) << '\n';
}
```

时间 $O(n)$，额外空间 $O(n)$ 用于输入；若继续放大到超过 128 位，才需要真正的任意精度整数。

## 验证说明

本轮将六段代码按 C++23 编译；线性 DP 会与 $O(n^2)$ 枚举在随机长度 1–12、值域 $[-5,5]$ 上对拍，并复核两个官方样例、单元素、全负、含零、奇偶个负数与多段零分隔。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximum-product-subarray/)
- [对应知识专题](../../dp/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-84-lc135/">← [力扣 Top 84] LC 135 分发糖果 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-86-lc136/">[力扣 Top 86] LC 136 只出现一次的数字 简单 →</a>
</nav>
