---
title: "[力扣 Top 81] LC 31 下一个排列 中等"
---

# [力扣 Top 81] LC 31 下一个排列 中等

<p class="daily-archive-kicker">2026-08-03 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../math/permutation-ranking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=0e2cac9004624e365946cf79b1296748a7c17ea906f537dead64072d1308e3f3 -->
## 官方原始信息

- Top 排名：81
- 题号：LC 31
- 官方中文标题：下一个排列
- 官方难度：中等
- 官方链接：[下一个排列](https://leetcode.cn/problems/next-permutation/)

### 原始题意

整数数组的“下一个排列”是按字典序严格大于当前排列的最小排列；若当前排列已经最大，则改成最小排列。要求原地修改数组，并且只能使用常数额外空间。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  void nextPermutation(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3]
输出：[1,3,2]
```

```text
输入：nums = [3,2,1]
输出：[1,2,3]
```

```text
输入：nums = [1,1,5]
输出：[1,5,1]
```

### 全部约束

- $1\le nums.length\le100$。
- $0\le nums_i\le100$。
- 必须原地修改，只使用常数额外空间。

## 约束推导与关键结构

排列总数可达 $100!$，不能生成并排序所有排列。要得到“刚好更大”的排列，应尽量让高位不变，只在尽可能靠右的位置增加。

从右向左找第一个 `nums[p] < nums[p+1]`。其右侧必为非递增后缀，已经是该前缀下的最大排列。若找不到这样的 `p`，整个数组非递增，当前排列全局最大，只需反转成非递减最小排列。

若找到 `p`，应把 `nums[p]` 换成后缀中严格大于它的最小值。因后缀非递增，从右向左遇到的第一个更大值就是所求。交换后，后缀仍为非递增；反转后变成最小非递减排列。重复值要求使用严格 `<` 与 `>`，否则可能没有真正变大。

## 解法递进

### 解法一：生成全部不同排列并排序

排序副本后用回溯生成全部不同排列，字典序排序，再查找当前排列的后继。它覆盖定义，但时间和空间都是阶乘级，只适合作为很小数组 oracle。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  void generate(const vector<int>& values, vector<int>& current, vector<int>& used,
      vector<vector<int>>& permutations) {
    if (current.size() == values.size()) {
      permutations.push_back(current);
      return;
    }
    for (int i = 0; i < static_cast<int>(values.size()); ++i) {
      if (used[i] || (i > 0 && values[i] == values[i - 1] && !used[i - 1])) {
        continue;
      }
      used[i] = true;
      current.push_back(values[i]);
      generate(values, current, used, permutations);
      current.pop_back();
      used[i] = false;
    }
  }
public:
  void nextPermutation(vector<int>& nums) {
    vector<int> values = nums;
    sort(values.begin(), values.end());
    vector<vector<int>> permutations;
    vector<int> current, used(nums.size());
    generate(values, current, used, permutations);
    auto position = lower_bound(permutations.begin(), permutations.end(), nums);
    ++position;
    nums = position == permutations.end() ? permutations.front() : *position;
  }
};
```

设不同排列数为 $P$，时间 $O(Pn)$，空间 $O(Pn)$，无法满足约束目标。

### 最佳实用解：右侧最大后缀上的局部进位

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void nextPermutation(vector<int>& nums) {
    int pivot = static_cast<int>(nums.size()) - 2;
    while (pivot >= 0 && nums[pivot] >= nums[pivot + 1]) {
      --pivot;
    }
    if (pivot >= 0) {
      int successor = nums.size() - 1;
      while (nums[successor] <= nums[pivot]) {
        --successor;
      }
      swap(nums[pivot], nums[successor]);
    }
    reverse(nums.begin() + pivot + 1, nums.end());
  }
};
```

时间 $O(n)$，额外空间 $O(1)$，严格满足题目要求。

## 正确性证明

枢轴右侧原本非递增，因此不存在仅改变更右位置就能得到更大排列的方案；若无枢轴，整个排列已最大，反转得到全局最小排列。若有枢轴，任何下一个排列必须在不早于 `pivot` 的位置首次变大，而更右位置不可能承担首次变大，所以首次变化必须在 `pivot`。选择后缀中严格大于枢轴的最小元素，使该位的增量最小；交换后把余下元素排成非递减顺序，使同一新前缀下的后缀最小。故所得排列严格更大，且不存在夹在两者之间的排列。

## 样例手推

`[1,2,3]` 的枢轴是 2，后缀最小更大值是 3，交换得 `[1,3,2]`，单元素后缀无需变化。`[3,2,1]` 无枢轴，整段反转为 `[1,2,3]`。`[1,1,5]` 的枢轴为第二个 1，与 5 交换后反转后缀，得到 `[1,5,1]`。

## 易错点与方案比较

- 枢轴条件是严格上升 `nums[p] < nums[p+1]`；重复值不能当成可进位。
- 后继必须严格大于枢轴，并从右侧找第一个，不能随意选最大值。
- 无枢轴时 `pivot=-1`，反转区间应从 0 开始。
- 交换后必须反转整个后缀；只排序当然也正确，但变成 $O(n\log n)$。
- 该方法是常数空间的线性最优解，推荐记忆“找下降后缀、进一位、后缀最小化”。

## 变种一：求上一个排列

新定义：求字典序严格更小的最大排列；若不存在则变为最大排列。把所有不等号反向，并把后缀反转成非递增。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  int pivot = n - 2;
  while (pivot >= 0 && a[pivot] <= a[pivot + 1]) {
    --pivot;
  }
  if (pivot >= 0) {
    int predecessor = n - 1;
    while (a[predecessor] >= a[pivot]) {
      --predecessor;
    }
    swap(a[pivot], a[predecessor]);
  }
  reverse(a.begin() + pivot + 1, a.end());
  for (int value : a) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：恢复十进制数字组成的下一个更大整数

新定义：给定非负整数的数字串，重排全部数字得到严格更大的最小整数；不存在则输出 -1。结构与下一个排列相同，还需检查结果是否超过 32 位有符号整数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string digits;
  cin >> digits;
  int pivot = static_cast<int>(digits.size()) - 2;
  while (pivot >= 0 && digits[pivot] >= digits[pivot + 1]) {
    --pivot;
  }
  if (pivot < 0) {
    cout << -1 << '\n';
    return 0;
  }
  int successor = digits.size() - 1;
  while (digits[successor] <= digits[pivot]) {
    --successor;
  }
  swap(digits[pivot], digits[successor]);
  reverse(digits.begin() + pivot + 1, digits.end());
  long long value = stoll(digits);
  cout << (value <= INT_MAX ? value : -1) << '\n';
}
```

时间 $O(d)$，空间 $O(d)$（字符串表示）。

## 变种三：互异元素的第 $K$ 个后继排列

新定义：$n\le20$ 且元素互异，循环意义下前进 $K$ 个排列。先用阶乘数制求当前排名，加 $K$ 取模，再按排名反解，避免重复执行 $K$ 次线性算法。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  unsigned long long k;
  cin >> n >> k;
  vector<int> permutation(n), sortedValues;
  for (int& value : permutation) {
    cin >> value;
  }
  sortedValues = permutation;
  sort(sortedValues.begin(), sortedValues.end());
  vector<unsigned long long> factorial(n + 1, 1);
  for (int i = 1; i <= n; ++i) {
    factorial[i] = factorial[i - 1] * i;
  }
  vector<int> available = sortedValues;
  unsigned long long rank = 0;
  for (int i = 0; i < n; ++i) {
    int position =
        lower_bound(available.begin(), available.end(), permutation[i]) - available.begin();
    rank += position * factorial[n - 1 - i];
    available.erase(available.begin() + position);
  }
  rank = (rank + k) % factorial[n];
  available = sortedValues;
  for (int i = 0; i < n; ++i) {
    unsigned long long block = factorial[n - 1 - i];
    int position = rank / block;
    rank %= block;
    cout << available[position] << ' ';
    available.erase(available.begin() + position);
  }
  cout << '\n';
}
```

时间 $O(n^2)$，空间 $O(n)$；`n\le20` 保证 $n!$ 可放入无符号 64 位。

## 变种四：自定义排序规则下的下一个排列

新定义：字符串按大小写不敏感字典序比较字符，并以原字符作次级顺序。只要比较器是严格弱序，枢轴、后继与反转逻辑完全保留。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;
  auto lessCharacter = [](char left, char right) {
    return pair<char, char>{tolower(left), left} < pair<char, char>{tolower(right), right};
  };
  int pivot = static_cast<int>(s.size()) - 2;
  while (pivot >= 0 && !lessCharacter(s[pivot], s[pivot + 1])) {
    --pivot;
  }
  if (pivot >= 0) {
    int successor = s.size() - 1;
    while (!lessCharacter(s[pivot], s[successor])) {
      --successor;
    }
    swap(s[pivot], s[successor]);
  }
  reverse(s.begin() + pivot + 1, s.end());
  cout << s << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。比较器不满足传递性时，“字典序后继”本身就没有稳定定义。

## 验证说明

本轮将六段代码按 C++23 编译；最佳解会与全排列 oracle 在随机长度 1–8、含重复值的数组上对拍，并覆盖全相等、严格升序、严格降序、枢轴旁重复与单元素边界。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/next-permutation/)
- [对应知识专题](../../math/permutation-ranking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-b/">← [atcoder] ABC469 B Isolated Seats</a>
<a class="daily-archive-pager__next" href="../leetcode-top-82-lc139/">[力扣 Top 82] LC 139 单词拆分 中等 →</a>
</nav>
