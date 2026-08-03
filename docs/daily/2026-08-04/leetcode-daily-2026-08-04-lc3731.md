---
title: "[力扣每日一题] 2026-08-04｜LC 3731 找出缺失的元素"
---

# [力扣每日一题] 2026-08-04｜LC 3731 找出缺失的元素

<p class="daily-archive-kicker">2026-08-04 · 第 14/14 题 · 力扣每日一题</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=652e61356a29fb45e354a502c55052de3a5e2c188b6e29c1e729a719b73ebc5c -->
## 官方原始信息

- 日期：2026-08-04（Asia/Shanghai）
- 题号：LC 3731
- 官方中文标题：找出缺失的元素
- 官方难度：简单
- 官方链接：[找出缺失的元素](https://leetcode.cn/problems/find-missing-elements/)

### 原始题意

给定由互不相同整数组成的数组。它原本包含最小值到最大值之间的所有整数，现在可能缺少一部分；最小值和最大值保证仍在数组中。按递增顺序返回范围内所有缺失整数，没有缺失则返回空列表。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> findMissingElements(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,4,2,5]
输出：[3]
解释：完整范围是 [1,2,3,4,5]，只缺少 3。
```

```text
输入：nums = [7,8,6,9]
输出：[]
解释：范围 [6,9] 内没有缺失整数。
```

```text
输入：nums = [5,1]
输出：[2,3,4]
解释：范围 [1,5] 内缺少 2、3、4。
```

### 全部约束

- $2\le nums.length\le100$。
- $1\le nums[i]\le100$。
- 数组元素互不相同。
- 最小值与最大值仍然存在。

## 约束推导与输出下界

值域只有 1 到 100，可以用定长存在表。先求最小、最大值，再标记输入值，最后顺序扫描闭区间；扫描顺序天然满足输出有序。若完整范围长度为 $R=max-min+1$，输出最多 $R-n$ 个值，任何算法至少需要 $\Omega(n+R)$ 的读写工作。所有值和下标均可由 `int` 安全表示。

## 解法递进

### 解法一：排序后逐个补相邻缺口

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findMissingElements(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<int> answer;
    for (int index = 1; index < static_cast<int>(nums.size()); ++index) {
      for (int value = nums[index - 1] + 1; value < nums[index]; ++value) {
        answer.push_back(value);
      }
    }
    return answer;
  }
};
```

时间 $O(n\log n+R)$，排序栈空间通常 $O(\log n)$。它适用于值域不小但数组可排序的情形，代价是修改输入顺序。

### 最佳实用解：存在表加范围扫描

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findMissingElements(vector<int>& nums) {
    int minimum = *min_element(nums.begin(), nums.end());
    int maximum = *max_element(nums.begin(), nums.end());
    array<bool, 101> present{};
    for (int value : nums) {
      present[value] = true;
    }
    vector<int> answer;
    for (int value = minimum; value <= maximum; ++value) {
      if (!present[value]) {
        answer.push_back(value);
      }
    }
    return answer;
  }
};
```

时间 $O(n+R)$，存在表为固定 $O(1)$ 空间，输出空间 $O(R-n)$。当前值域下它最直接、常数最低，是推荐答案。

### 同阶替代：哈希集合

若值域不再固定为 100，可把存在表改成 `unordered_set<int>`，然后扫描 `[min,max]`。期望时间 $O(n+R)$，空间 $O(n)$；但当范围极大时，即使缺失输出本身也很大，逐值扫描仍不可避免，除非接口改为区间压缩输出。

## 正确性证明

存在表在标记后满足：对任意输入范围内的整数 $v$，`present[v]` 为真当且仅当 $v$ 出现在 `nums`。算法恰扫描官方定义的完整范围 `[minimum,maximum]`，仅把不存在的值加入答案，因此没有遗漏或误收。扫描变量严格递增，故答案天然有序。

## 样例手推、边界与易错点

对 `[1,4,2,5]`，最小值 1、最大值 5；标记 1、2、4、5 后顺序扫描，仅 3 未标记。对 `[7,8,6,9]` 每个范围值都存在，返回空列表。`[5,1]` 会依次输出 2、3、4。

- 扫描边界必须包含最小值和最大值；虽然二者保证存在，闭区间写法最不易错。
- 不能假定 `nums[0]`、`nums.back()` 是最小和最大，输入无序。
- 题目保证元素互异；若有重复，缺失数量不能用 `R-n` 直接推导。
- 排序解会修改输入，若调用方要求保留顺序应复制或用存在表。

## 变种一：只返回缺失元素数量

新定义：不枚举具体值，只求数量。互异且两端存在时，完整范围大小减现有元素数即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  int minimum = INT_MAX;
  int maximum = INT_MIN;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    minimum = min(minimum, value);
    maximum = max(maximum, value);
  }
  cout << maximum - minimum + 1 - n << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。输出目标改变后无需扫描整个范围。

## 变种二：范围内恰缺一个数

新定义：给定范围两端 `low,high`，其中恰少一个整数，输入无重复。用异或消去所有已出现值，无需担心加法溢出。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int low, high, n;
  cin >> low >> high >> n;
  int answer = 0;
  for (int value = low; value <= high; ++value) {
    answer ^= value;
  }
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    answer ^= value;
  }
  cout << answer << '\n';
}
```

时间 $O(high-low+n)$，空间 $O(1)$。若范围是连续的 0 到 $m$，可用四周期异或公式把范围部分降到 $O(1)$。

## 变种三：输入允许重复值

新定义：重复不影响“是否存在”，先放入集合，再从最小值扫到最大值；不能再用数组长度推断缺失数量。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  set<int> present;
  int minimum = INT_MAX;
  int maximum = INT_MIN;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    present.insert(value);
    minimum = min(minimum, value);
    maximum = max(maximum, value);
  }
  for (int value = minimum; value <= maximum; ++value) {
    if (!present.contains(value)) {
      cout << value << ' ';
    }
  }
  cout << '\n';
}
```

时间 $O(n\log n+R\log n)$，空间 $O(n)$；用哈希集合可得到期望 $O(n+R)$。

## 变种四：值域巨大，输出缺失区间而非逐个整数

新定义：值可到 $10^{18}$，要求输出极大缺口的闭区间。排序后只检查相邻不同值，输出 `[previous+1,current-1]`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<long long> numbers(n);
  for (long long& value : numbers) {
    cin >> value;
  }
  sort(numbers.begin(), numbers.end());
  numbers.erase(unique(numbers.begin(), numbers.end()), numbers.end());
  for (int i = 1; i < static_cast<int>(numbers.size()); ++i) {
    if (numbers[i - 1] + 1 < numbers[i]) {
      cout << numbers[i - 1] + 1 << ' ' << numbers[i] - 1 << '\n';
    }
  }
}
```

时间 $O(n\log n)$，空间 $O(n)$。区间压缩使运行时间依赖输入和缺口段数，而不是缺失整数总数。

## 可复现验证

全部代码块按 GNU++23 编译。最佳解与排序解在随机互异数组上对拍，并覆盖完整连续范围、只保留两端、范围宽度 2、值域边界 1 和 100。官方三组样例逐项通过。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-missing-elements/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../codeforces-2248-c/">← [codeforces] CF Round 1113 Div.2 C Maximize the Score</a>
<span class="daily-archive-pager__empty"></span>
</nav>
