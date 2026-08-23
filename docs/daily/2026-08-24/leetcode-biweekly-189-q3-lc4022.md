---
title: "[力扣竞赛] 第 189 场双周赛 Q3 LC 4022 无限字符串里第 K 个数字 中等"
---

# [力扣竞赛] 第 189 场双周赛 Q3 LC 4022 无限字符串里第 K 个数字 中等

<p class="daily-archive-kicker">2026-08-24 · 第 3/5 题 · 力扣竞赛</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-24 题目列表</a> · <a href="../../../math/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=f16fcced41fe5de0dfecb102aeaa975af5b25f8a5047632a037bdcb95ae234dc -->
[力扣官方题目：4022. 无限字符串里第 K 个数字](https://leetcode.cn/problems/k-th-digit-in-infinite-string/)

## 官方原始信息

- 比赛：第 189 场双周赛；题目：Q3，LC 4022。
- 官方中文标题：无限字符串里第 K 个数字；官方难度：中等；官方竞赛分值：5 分。
- ZeroTracer 社区估算竞赛分：1914.972，抓取于 2026-08-24；这不是力扣官方难度或分值。
- 官方链接：[https://leetcode.cn/problems/k-th-digit-in-infinite-string/](https://leetcode.cn/problems/k-th-digit-in-infinite-string/)
- 函数签名：`int kthDigit(long long k)`。
- 官方标签：数学、二分查找。

### 原始题意

把所有正整数的十进制表示无分隔地拼接。对每个非负整数 $b$，块 $b$ 包含区间
$[10b,10b+9]$ 内的正整数：$b$ 为偶数时按递增顺序拼接，$b$ 为奇数时按递减顺序拼接。
因此开头依次是 1–9、19–10、20–29、39–30……返回整个无限字符串中从 1 开始计数的第
$k$ 位数字。

### 全部官方样例

```text
示例 1
输入：k = 4
输出：4
解释：开头为 "123456789.."，第 4 位是 4。

示例 2
输入：k = 15
输出：7
解释：开头为 "123456789191817.."，第 15 位是 7。

示例 3
输入：k = 11
输出：9
解释：开头为 "12345678919.."，第 11 位是 9。
```

### 全部约束

- $1\le k\le10^{15}$。

## 最优结论摘要

块内倒序只改变同一组 10 个整数的排列，不改变这一块的总位数。先按十进制位数跳过完整
数段，定位到某个 $d$ 位整数；再用“第几个十数块、块内第几个整数”恢复真实整数，最后取其
第几位。时间复杂度 $O(\log k)$，额外空间 $O(\log k)$（仅用于十进制字符串；也可纯算术
做到 $O(1)$）。

## 约束推导、溢出与边界

- $k$ 达到 $10^{15}$，逐字符生成字符串完全不可行，必须整段跳过。
- 一位正整数只有 1–9，共 9 位；块 0 中的 0 不属于正整数，不能写进字符串。
- 对 $d\ge2$，全部 $d$ 位整数从 $10^{d-1}$ 开始，恰好落在一个十数块边界；每块 10 个
  整数且位数相同。
- $d$ 位整数一共有 $9\times10^{d-1}$ 个，共贡献 $9\times10^{d-1}\times d$ 位。
- 分段总位数的中间乘积使用 `__int128`，避免扩大约束或接近边界时乘法溢出。
- 所有位置先转成 0-based 再做除法和取模，可统一处理“整数下标”和“整数内数字下标”。
- 块号本身可能很大，但在当前约束下仍安全落在 `long long`。

## 官方样例手推

对 $k=15$，先跳过一位数的 9 位，块内剩余位置为 6。二位数段中，0-based 整数下标为
$(6-1)/2=2$，数字内下标为 $(6-1)\bmod2=1$。它位于块 $b=1$，该块按 19、18、17……
倒序，所以对应整数是 17；下标 1 的数字是 7。

## 解法一：直接生成足够长的前缀

从块 0 开始，按奇偶方向把每个正整数转成字符串并追加，直到长度至少为 $k$。它完全按定义
模拟，所以正确；但时间与空间都是 $\Theta(k)$，只能用于极小数据和随机对拍 oracle。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int kthDigit(long long k) {
    string sequence;
    for (long long block = 0; static_cast<long long>(sequence.size()) < k; ++block) {
      long long first = max(1LL, block * 10);
      long long last = block * 10 + 9;
      if (block % 2 == 0) {
        for (long long value = first; value <= last; ++value) {
          sequence += to_string(value);
        }
      } else {
        for (long long value = last; value >= first; --value) {
          sequence += to_string(value);
        }
      }
    }
    return sequence[k - 1] - '0';
  }
};
```

## 从逐字符生成到按位数整段跳过

若忽略每个十数块内部的顺序，把所有 $d$ 位正整数写一遍，字符总数并不会改变。因此先判断
$k$ 落在哪个十进制位数段，无需知道经过了哪些具体块。进入该段后：

$$
\text{numberIndex}=\left\lfloor\frac{k-1}{d}\right\rfloor,
\qquad
\text{digitIndex}=(k-1)\bmod d.
$$

其中此处的 $k$ 已减去更短整数的全部位数。`numberIndex / 10` 给出相对块号，
`numberIndex % 10` 给出块内序号；再根据实际块号奇偶决定顺序。

## 最佳实用解：位数分段加块内直接映射

### 正确性证明

**引理一**：按位数跳段不会受块内升降序影响。每个块仍恰好包含原区间内每个正整数一次，
排列不改变数字字符总数；同一 $d$ 位段的总位数仍是 $9\times10^{d-1}d$。

**引理二**：进入 $d$ 位段后，算法恢复的整数就是包含目标位的整数。整除 $d$ 得到此前
完整经过的整数数量，取模得到目标在当前整数内的位置。每 10 个连续下标对应一个十数块；
块号为偶数时偏移 `offset` 对应 `start + offset`，为奇数时对应
`start + 9 - offset`，恰与题目顺序相同。

根据引理一，算法删去的都是目标之前的完整字符段；根据引理二，剩余位置被映射到唯一正确
整数及其唯一正确数字位置，因此返回值正确。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int kthDigit(long long k) {
    if (k <= 9) return static_cast<int>(k);
    k -= 9;
    long long power = 10;
    int digits = 2;
    while (true) {
      __int128 segment = static_cast<__int128>(9) * power * digits;
      if (segment >= k) break;
      k -= static_cast<long long>(segment);
      power *= 10;
      ++digits;
    }
    long long numberIndex = (k - 1) / digits;
    int digitIndex = static_cast<int>((k - 1) % digits);
    long long blockStart = power + numberIndex / 10 * 10;
    long long block = blockStart / 10;
    long long offset = numberIndex % 10;
    long long value = block % 2 == 0 ? blockStart + offset : blockStart + 9 - offset;
    return to_string(value)[digitIndex] - '0';
  }
};
```

时间复杂度 $O(\log k)$，额外空间 $O(\log k)$；循环实际至多经过约 15 个位数层级。

## 同阶方案比较与易错点

也可以二分第一个累计位数不少于 $k$ 的块，再在该块内定位。二分需要实现“写出 1 到某数
共多少位”的计数函数，复杂度同为 $O(\log k\log k)$ 或经常数位数优化后近似 $O(\log k)$。
直接按位数分段状态更少、边界更易证明，竞赛中更推荐。

- 把块 0 写成 0–9，导致从第一位起全部错位。
- 用块号相对奇偶代替实际 $b$ 的奇偶；从三位数开始的首块 $b=10$ 是偶数。
- 忘记把 $k$ 转成 0-based，恰在整数或块边界时产生 off-by-one。
- 认为倒序会改变整个位数段的长度，从而做不必要的逐块扣减。
- 用 `long long` 直接计算 `9 * power * digits`，不给更大约束留溢出余量。
- 从题面中保留与函数接口、输入输出和判题无关的无意义局部变量要求。

## 可复现验证

两份原题函数均以 C++23 编译并通过全部三个官方样例、$k=1,9,10,11$、十数块边界、
99/100 位数边界及 $k=10^{15}$。随机生成小位置，以直接构造字符串为 oracle 对拍最优解。

## Follow-up 与约束变种

### 变种一：批量回答很多个位置

新定义：给出 $Q\le2\times10^5$ 个 $k$。预先保存每个位数段的起点、整数个数与字符数，
每次二分所属位数段，再复用原映射。预处理 $O(18)$，每问 $O(\log18)$，空间 $O(18)$。

<!-- compile:program -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Segment {
  long long start;
  long long cumulative;
  int digits;
};
int answer(long long k, const vector<Segment>& segments) {
  int position = lower_bound(
      segments.begin(), segments.end(), k,
      [](const Segment& segment, long long value) {
        return segment.cumulative < value;
      }) - segments.begin();
  long long before = position == 0 ? 0 : segments[position - 1].cumulative;
  long long offsetInSegment = k - before - 1;
  int digits = segments[position].digits;
  long long numberIndex = offsetInSegment / digits;
  int digitIndex = offsetInSegment % digits;
  if (digits == 1) return static_cast<int>(numberIndex + 1);
  long long blockStart = segments[position].start + numberIndex / 10 * 10;
  long long block = blockStart / 10;
  long long offset = numberIndex % 10;
  long long value = block % 2 == 0 ? blockStart + offset : blockStart + 9 - offset;
  return to_string(value)[digitIndex] - '0';
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  vector<Segment> segments;
  long long power = 1;
  __int128 cumulative = 0;
  for (int digits = 1; digits <= 15; ++digits) {
    cumulative += static_cast<__int128>(9) * power * digits;
    long long end = static_cast<long long>(
        min<__int128>(cumulative, 1000000000000000LL));
    segments.push_back({power, end, digits});
    if (cumulative >= 1000000000000000LL) break;
    power *= 10;
  }
  int q;
  cin >> q;
  while (q--) {
    long long k;
    cin >> k;
    cout << answer(k, segments) << '\n';
  }
  return 0;
}
```

### 变种二：同时返回所属整数与数字位置

新定义：返回三元组 `(value, position, digit)`，其中 `value` 是包含目标位的整数，
`position` 是该数字在整数中的 1-based 位置。原算法没有失效，只需保留中间量。时间
$O(\log k)$，额外空间 $O(\log k)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Location {
  long long value;
  int position;
  int digit;
};
class Solution {
public:
  Location locate(long long k) {
    if (k <= 9) return {k, 1, static_cast<int>(k)};
    k -= 9;
    long long power = 10;
    int digits = 2;
    while (static_cast<__int128>(9) * power * digits < k) {
      k -= 9 * power * digits;
      power *= 10;
      ++digits;
    }
    long long numberIndex = (k - 1) / digits;
    int digitIndex = (k - 1) % digits;
    long long blockStart = power + numberIndex / 10 * 10;
    long long block = blockStart / 10;
    long long offset = numberIndex % 10;
    long long value = block % 2 == 0 ? blockStart + offset : blockStart + 9 - offset;
    return {value, digitIndex + 1, to_string(value)[digitIndex] - '0'};
  }
};
```

### 变种三：推广到任意进制

新定义：$2\le B\le10$，块 $b$ 包含 $Bb$ 到 $Bb+B-1$ 的正整数；偶数块递增、奇数块
递减，所有整数用 $B$ 进制无分隔拼接。返回第 $k$ 个数位的数值。把 10 全部替换为 $B$，
一位正整数数量改为 $B-1$；对 $d\ge2$，$B^{d-1}$ 仍与块边界对齐。时间
$O(\log_B k)$，空间 $O(1)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int kthDigitInBase(long long k, int base) {
    if (k <= base - 1) return static_cast<int>(k);
    k -= base - 1;
    long long power = base;
    int digits = 2;
    while (static_cast<__int128>(base - 1) * power * digits < k) {
      k -= static_cast<long long>(static_cast<__int128>(base - 1) * power * digits);
      power *= base;
      ++digits;
    }
    long long numberIndex = (k - 1) / digits;
    int digitIndex = (k - 1) % digits;
    long long blockStart = power + numberIndex / base * base;
    long long block = blockStart / base;
    long long offset = numberIndex % base;
    long long value = block % 2 == 0
        ? blockStart + offset : blockStart + base - 1 - offset;
    long long divisor = 1;
    for (int i = digitIndex + 1; i < digits; ++i) divisor *= base;
    return static_cast<int>(value / divisor % base);
  }
};
```

### 变种四：块方向由周期模式决定

新定义：给定仅含 `A` 与 `D` 的非空模式串 `pattern`；块 $b$ 的方向由
`pattern[b % pattern.size()]` 决定，`A` 表示递增，`D` 表示递减。位数计数仍完全不受方向
影响，只有恢复整数时改查模式。时间 $O(\log k)$，空间 $O(\log k)$。

<!-- compile:function -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int kthDigitWithPattern(long long k, const string& pattern) {
    if (k <= 9) return static_cast<int>(k);
    k -= 9;
    long long power = 10;
    int digits = 2;
    while (static_cast<__int128>(9) * power * digits < k) {
      k -= 9 * power * digits;
      power *= 10;
      ++digits;
    }
    long long numberIndex = (k - 1) / digits;
    int digitIndex = (k - 1) % digits;
    long long blockStart = power + numberIndex / 10 * 10;
    long long block = blockStart / 10;
    long long offset = numberIndex % 10;
    bool ascending = pattern[block % pattern.size()] == 'A';
    long long value = ascending ? blockStart + offset : blockStart + 9 - offset;
    return to_string(value)[digitIndex] - '0';
  }
};
```

## 推荐记忆

本题最重要的拆分是“计数不看块内顺序，定位才看块内顺序”。先按位数跳过完整字符段，再用
整除定位整数、取模定位数字，最后只在恢复整数时处理块的升降序。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/k-th-digit-in-infinite-string/)
- [对应知识专题](../../math/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-141-lc62/">← [力扣 Top 141] LC 62 不同路径 中等</a>
<a class="daily-archive-pager__next" href="../codeforces-2257-f2/">[codeforces] CF Round 1117 Div.2 F2 Beaver&#x27;s Jumping Track (Hard Version) →</a>
</nav>
