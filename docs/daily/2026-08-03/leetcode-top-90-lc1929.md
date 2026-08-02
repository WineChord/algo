---
title: "[力扣 Top 90] LC 1929 数组串联 简单"
---

# [力扣 Top 90] LC 1929 数组串联 简单

<p class="daily-archive-kicker">2026-08-03 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4eedfc7d44469357d87ef4172f02160d45b6bfcaef96524021bca1e8a6c1098c -->
## 官方原始信息

- Top 排名：90
- 题号：LC 1929
- 官方中文标题：数组串联
- 官方难度：简单
- 官方链接：[数组串联](https://leetcode.cn/problems/concatenation-of-array/)

### 原始题意

给定长度为 $n$ 的整数数组 `nums`，构造长度 $2n$ 的数组 `ans`，满足 `ans[i]=nums[i]` 且 `ans[i+n]=nums[i]`，返回 `ans`。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> getConcatenation(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,1]
输出：[1,2,1,1,2,1]
```

```text
输入：nums = [1,3,2,1]
输出：[1,3,2,1,1,3,2,1]
```

### 全部约束

- $1\le nums.length\le1000$。
- $1\le nums_i\le1000$。

## 约束推导与边界

输出本身含 $2n$ 个元素，任何显式返回数组的算法都需要 $\Omega(n)$ 时间与 $\Omega(n)$ 输出空间。题目给出的下标关系直接说明每个原元素要写到 `i` 与 `i+n` 两处；没有搜索、排序或数值运算。

$2n\le2000$，长度与元素均不会溢出 `int`。输入非空，但同一实现也自然支持空数组。应预先分配 `2*n` 或 `reserve(2*n)`，避免不必要的多次扩容。

## 解法递进

### 解法一：连续两次追加

按输入顺序循环两遍并 `push_back`。预留容量后总搬移为线性。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> getConcatenation(vector<int>& nums) {
    vector<int> answer;
    answer.reserve(nums.size() * 2);
    for (int repeat = 0; repeat < 2; ++repeat) {
      for (int value : nums) {
        answer.push_back(value);
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，输出空间 $O(n)$，额外工作空间 $O(1)$。

### 最佳实用解：一次循环写两个确定位置

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> getConcatenation(vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(2 * n);
    for (int i = 0; i < n; ++i) {
      answer[i] = nums[i];
      answer[i + n] = nums[i];
    }
    return answer;
  }
};
```

时间 $O(n)$，输出空间 $O(n)$，除返回值外额外空间 $O(1)$。它逐字对应题目下标公式，常数和证明最简。

## 正确性证明

循环遍历每个 $i\in[0,n)$，分别写入 `answer[i]=nums[i]` 和 `answer[i+n]=nums[i]`。前一组下标恰覆盖 `[0,n)`，后一组恰覆盖 `[n,2n)`，两组不重叠且并集为整个输出范围。因此每个输出位置恰被写一次，并满足题目两条定义，返回数组正确。

## 样例手推

对 `[1,2,1]`，`n=3`：位置 0 与 3 写 1，位置 1 与 4 写 2，位置 2 与 5 写 1，得到 `[1,2,1,1,2,1]`。单元素 `[7]` 会得到 `[7,7]`。

## 易错点与方案比较

- 第二份起点是 `i+n`，不是 `i+n-1`。
- 输出长度必须为 `2*n`；仅 `reserve` 不会改变可下标访问的 `size`。
- 若使用 `insert(answer.end(), nums.begin(), nums.end())` 两次同样正确，但下标公式写法更直接。
- 该题的线性复杂度已由输出规模决定，不需要寻求“常数时间”显式构造。

## 变种一：重复串联 $K$ 次

新定义：返回 `nums` 连续重复 $K$ 次的数组。输出位置 $i$ 对应 `nums[i mod n]`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, repeatCount;
  cin >> n >> repeatCount;
  vector<int> nums(n), answer(n * repeatCount);
  for (int& value : nums)
    cin >> value;
  for (int i = 0; i < n * repeatCount; ++i) {
    answer[i] = nums[i % n];
  }
  for (int value : answer)
    cout << value << ' ';
  cout << '\n';
}
```

时间与输出空间均为 $O(nK)$。构造前应在更大约束下检查 `n*K` 的长度溢出。

## 变种二：只回答虚拟串联数组的下标查询

新定义：重复次数很大，不实际构造；每次给出合法零基下标，返回对应值。周期性使答案为 `nums[index%n]`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, queryCount;
  long long repeatCount;
  cin >> n >> repeatCount >> queryCount;
  vector<int> nums(n);
  for (int& value : nums)
    cin >> value;
  while (queryCount--) {
    long long index;
    cin >> index;
    if (index < 0 || index >= repeatCount * n)
      cout << "OUT\n";
    else
      cout << nums[index % n] << '\n';
  }
}
```

预处理 $O(n)$，每次查询 $O(1)$，空间 $O(n)$；避免了 $O(nK)$ 实体数组。

## 变种三：循环左移后再重复两次

新定义：先把数组循环左移 $r$ 位，再串联两份。虚拟第 $i$ 位来自原下标 $(i+r)\bmod n$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long shift;
  cin >> n >> shift;
  vector<int> nums(n), answer(2 * n);
  for (int& value : nums)
    cin >> value;
  shift %= n;
  for (int i = 0; i < 2 * n; ++i) {
    answer[i] = nums[(i + shift) % n];
  }
  for (int value : answer)
    cout << value << ' ';
  cout << '\n';
}
```

时间 $O(n)$，输出空间 $O(n)$。

## 变种四：串联多组不同数组并支持随机访问

新定义：有 $K$ 个数组，不展平存储；回答全局下标属于哪一组以及其值。保存各组累计长度，用 `upper_bound` 定位。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int arrayCount, queryCount;
  cin >> arrayCount >> queryCount;
  vector<vector<int>> arrays(arrayCount);
  vector<long long> prefix(arrayCount + 1);
  for (int i = 0; i < arrayCount; ++i) {
    int size;
    cin >> size;
    arrays[i].resize(size);
    for (int& value : arrays[i])
      cin >> value;
    prefix[i + 1] = prefix[i] + size;
  }
  while (queryCount--) {
    long long index;
    cin >> index;
    if (index < 0 || index >= prefix.back()) {
      cout << "OUT\n";
      continue;
    }
    int group = upper_bound(prefix.begin(), prefix.end(), index) - prefix.begin() - 1;
    cout << group << ' ' << arrays[group][index - prefix[group]] << '\n';
  }
}
```

预处理 $O(K)$（不计读入），每次查询 $O(\log K)$，空间为原数组加 $O(K)$ 索引。

## 验证说明

本轮将六段代码按 C++23 编译；一次双写解会与两次追加法在随机数组上逐元素对拍，并复核两个官方样例、单元素、最大长度与重复值。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/concatenation-of-array/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-89-lc98/">← [力扣 Top 89] LC 98 验证二叉搜索树 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-513-q1-lc4010/">[力扣竞赛] 第 513 场周赛 Q1 LC 4010 数对的最大强度 简单 →</a>
</nav>
