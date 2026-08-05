---
title: "[力扣 Top 111] LC 189 轮转数组 中等"
---

# [力扣 Top 111] LC 189 轮转数组 中等

<p class="daily-archive-kicker">2026-08-06 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8f11518e67164382000f2b40459bc7ed7c434f03b45ac25042889e05c10fb846 -->
## 官方原始信息

- Top 排名：111
- 题号：LC 189
- 官方中文标题：轮转数组
- 官方难度：中等
- 官方链接：[轮转数组](https://leetcode.cn/problems/rotate-array/)

### 原始题意与函数签名

给定整数数组 `nums` 和非负整数 `k`，把每个元素向右轮转 `k` 个位置，原地写回数组。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  void rotate(vector<int>& nums, int k);
};
```

### 全部官方样例

```text
输入：nums = [1,2,3,4,5,6,7], k = 3
输出：[5,6,7,1,2,3,4]
解释：连续右移三次后得到目标数组。
```

```text
输入：nums = [-1,-100,3,99], k = 2
输出：[3,99,-1,-100]
```

### 全部约束

- $1\le n=\lvert nums\rvert\le10^5$。
- $-2^{31}\le nums_i\le2^{31}-1$。
- $0\le k\le10^5$。
- 进阶要求给出多种方法，并尝试 $O(1)$ 额外空间的原地算法。

## 约束推导与观察

位置 `i` 的元素最终去往 $(i+k)\bmod n$，所以先令 `k %= n`。逐次右移会重复搬运同一元素；一次性复制能把时间降到 $O(n)$。若还要常数空间，可以把目标排列拆成环，或利用“三次翻转”：整体翻转后，前 `k` 个与后 `n-k` 个分别翻转。

## 解法递进

### 解法一：模拟每一步右移

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<int>& nums, int k) {
    int n = nums.size();
    k %= n;
    while (k--) {
      int last = nums.back();
      for (int i = n - 1; i > 0; --i) {
        nums[i] = nums[i - 1];
      }
      nums[0] = last;
    }
  }
};
```

时间 $O(nk)$，空间 $O(1)$，适合作为小规模 oracle。

### 解法二：辅助数组直接落到目标位置

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<int>& nums, int k) {
    int n = nums.size();
    vector<int> copy(n);
    for (int i = 0; i < n; ++i) {
      copy[(i + k) % n] = nums[i];
    }
    nums.swap(copy);
  }
};
```

时间 $O(n)$，空间 $O(n)$，映射最直观。

### 最佳实用解：三次翻转

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  void rotate(vector<int>& nums, int k) {
    int n = nums.size();
    k %= n;
    reverse(nums.begin(), nums.end());
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
  }
};
```

时间 $O(n)$，空间 $O(1)$。环置换同阶且每个元素写入次数更少，但要处理最大公约数或访问计数；三次翻转的证明和实现更稳，优先记忆。

## 正确性证明

把原数组写成 `A B`，其中 `B` 是最后 `k` 个元素。目标是 `B A`。整体翻转得到 `reverse(B) reverse(A)`；再分别翻转两段，恰得到 `B A`。每次翻转只交换元素，不丢失也不重复元素，所以结果正是右轮转 `k` 位。

## 样例手推

`[1,2,3,4,5,6,7]`、`k=3` 时，`A=[1,2,3,4]`、`B=[5,6,7]`。整体翻转为 `[7,6,5,4,3,2,1]`，再翻前 3 个和后 4 个，得到 `[5,6,7,1,2,3,4]`。`k=0` 或 `k` 为 `n` 的倍数时，两次全段翻转相互抵消，仍正确。

## 易错点与方案比较

- 必须在取模前保证 `n>0`；本题约束已保证非空。
- 不要用 `k` 次 `insert/erase`，其最坏时间同样为 $O(nk)$。
- 三次翻转的切分点是 `begin()+k`，不是 `begin()+n-k`。
- 辅助数组最易解释；三次翻转在时间和空间上都最优；环置换适合需要减少写次数的场景。

## 变种一：向左轮转 `k` 位

新定义：把前 `k` 个元素移到末尾。将数组拆成 `A B`，目标为 `B A`，依次翻转 `A`、`B`、整体即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  k %= n;
  reverse(a.begin(), a.begin() + k);
  reverse(a.begin() + k, a.end());
  reverse(a.begin(), a.end());
  for (int i = 0; i < n; ++i) {
    cout << a[i] << " \n"[i + 1 == n];
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：只轮转闭区间 `[l,r]`

新定义：数组其余位置不变，子数组向右轮转 `k` 位。原证明直接作用于该迭代器区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, l, r, k;
  cin >> n >> l >> r >> k;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  int len = r - l + 1;
  k %= len;
  reverse(a.begin() + l, a.begin() + r + 1);
  reverse(a.begin() + l, a.begin() + l + k);
  reverse(a.begin() + l + k, a.begin() + r + 1);
  for (int i = 0; i < n; ++i) {
    cout << a[i] << " \n"[i + 1 == n];
  }
}
```

时间 $O(r-l+1)$，空间 $O(1)$。

## 变种三：多次询问轮转后的单点值

新定义：原数组不实际修改；每次给出累计右移量 `k` 和目标下标 `i`，返回当前位置的值。维护总偏移即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  long long shift = 0;
  while (q--) {
    int type;
    long long x;
    cin >> type >> x;
    if (type == 1) {
      shift = (shift + x) % n;
    } else {
      int index = (x - shift % n + n) % n;
      cout << a[index] << '\n';
    }
  }
}
```

每次操作 $O(1)$，空间 $O(n)$。

## 变种四：轮转链表

对应 [LC 61 旋转链表](https://leetcode.cn/problems/rotate-list/)。链表无法随机访问，先求长度并首尾成环，再在第 `n-k` 个节点后断开。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
class Solution {
public:
  ListNode* rotateRight(ListNode* head, int k) {
    if (!head || !head->next) {
      return head;
    }
    int n = 1;
    ListNode* tail = head;
    while (tail->next) {
      tail = tail->next;
      ++n;
    }
    k %= n;
    if (k == 0) {
      return head;
    }
    tail->next = head;
    int steps = n - k;
    while (steps--) {
      tail = tail->next;
    }
    ListNode* answer = tail->next;
    tail->next = nullptr;
    return answer;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

用模拟右移作为 oracle，枚举长度 $1\ldots8$、元素小值域及 `k=0..20`，与三次翻转逐项比较；另覆盖单元素、`k=0`、`k=n`、`k\gg n` 和含重复值数组。发布代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/rotate-array/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc469-e/">← [atcoder] ABC469 E Pro Exam Eligibility</a>
<a class="daily-archive-pager__next" href="../leetcode-top-112-lc155/">[力扣 Top 112] LC 155 最小栈 中等 →</a>
</nav>
