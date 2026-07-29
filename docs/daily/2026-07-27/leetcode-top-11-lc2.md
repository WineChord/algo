---
title: "[力扣 Top 11] LC 2 两数相加 中等"
---

# [力扣 Top 11] LC 2 两数相加 中等

<p class="daily-archive-kicker">2026-07-27 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-27 题目列表</a> · <a href="../../data-structures/index.md">进入知识专题</a></p>

官方题目：https://leetcode.cn/problems/add-two-numbers/

## 官方原始信息

- 题号：2
- 官方中文标题：两数相加
- 官方英文标题：Add Two Numbers
- slug：`add-two-numbers`
- 官方难度：中等
- 函数签名：`ListNode* addTwoNumbers(ListNode* l1, ListNode* l2)`
- 官方竞赛归属与分值：未发现官方竞赛归属，官方分值未知
- ZeroTracer 社区估算竞赛分：无。2026-07-27 检索公开 `data.json`，该 slug 不在数据集中

### 原始题意

两个非空单链表分别表示两个非负整数。链表按十进制低位到高位存储，每个节点是一位数字；除数字 0 本身外，表示中没有前导零。计算两数之和，并以相同的逆序链表形式返回。

### 全部官方样例

1. `l1 = [2,4,3], l2 = [5,6,4]`，输出 `[7,0,8]`，因为 $342+465=807$。
2. `l1 = [0], l2 = [0]`，输出 `[0]`。
3. `l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]`，输出 `[8,9,9,9,0,0,0,1]`。

### 全部官方约束

- 每个链表节点数在 $[1,100]$
- $0\le Node.val\le9$
- 输入表示的数字除 0 外不含前导零

## 约束推导、样例与边界

最多 100 位，远超内置整数类型；把整个链表转换成 `long long` 会溢出。逆序存储恰好让链表头对应手算加法的个位，可以从头同步扫描并维护一个进位。任何算法都至少要读取较长链表的每一位，时间下界为 $\Omega(m+n)$。

样例 3 前四列都是 $9+9+\text{carry}$，产生数字 8 后连续进位；短链表耗尽后，长链表剩余的 9 仍要与进位相加，最终还多出最高位 1。这说明循环条件必须包含 `carry`。

边界：

- `[0] + [0]` 不应生成额外节点。
- 两链长度不同，短链耗尽后缺失位按 0 处理。
- 最后一列仍有进位时必须追加节点。
- 值相同不意味着节点可以共用；默认解法创建独立结果链表，不修改输入。
- 输出长度至多 $\max(m,n)+1$。

## 解法一：复制数字到数组后逐位相加

先把链表数字复制到数组、补齐缺位，再执行小学加法。这是正确而直观的基线，但重复保存了输入。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
public:
  ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    vector<int> a, b;
    for (; l1; l1 = l1->next) a.push_back(l1->val);
    for (; l2; l2 = l2->next) b.push_back(l2->val);
    int n = max(a.size(), b.size()), carry = 0;
    ListNode dummy;
    ListNode* tail = &dummy;
    for (int i = 0; i < n || carry; ++i) {
      int sum = carry;
      if (i < static_cast<int>(a.size())) sum += a[i];
      if (i < static_cast<int>(b.size())) sum += b[i];
      tail->next = new ListNode(sum % 10);
      tail = tail->next;
      carry = sum / 10;
    }
    return dummy.next;
  }
};
```

时间 $O(m+n)$，除输出外额外空间 $O(m+n)$。瓶颈是数组并未提供随机访问收益，链表本身已按所需顺序排列。

## 解法二：链表同步扫描（最佳实用解）

每轮读取两个当前位（缺失视为 0）与旧进位，输出 `sum % 10`，新进位为 `sum / 10`。哑节点统一处理结果头。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
public:
  ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    ListNode dummy;
    ListNode* tail = &dummy;
    int carry = 0;
    while (l1 || l2 || carry) {
      int sum = carry;
      if (l1) {
        sum += l1->val;
        l1 = l1->next;
      }
      if (l2) {
        sum += l2->val;
        l2 = l2->next;
      }
      tail->next = new ListNode(sum % 10);
      tail = tail->next;
      carry = sum / 10;
    }
    return dummy.next;
  }
};
```

### 正确性证明

循环不变量：处理完前 $t$ 个节点后，结果链表的前 $t$ 位恰是两数之和的最低 $t$ 位，`carry` 等于向第 $t$ 位以上传递的进位。初始 $t=0$ 时结果为空、进位为 0，不变量成立。下一轮把两数第 $t$ 位与 `carry` 相加，模 10 得到和的第 $t$ 位，整除 10 得到唯一正确的新进位，因此不变量保持。循环在两输入均耗尽且进位为 0 时结束，此时所有有效位均已输出，所以结果正确。

时间复杂度 $O(\max(m,n))$，除结果链表外额外空间 $O(1)$。每列最大和 $9+9+1=19$，`int` 足够。推荐记忆“逐列状态只有进位 + 哑节点”的模型。

## 同阶方案比较与常见错误

- 迭代和递归都能线性完成。递归写法自然但调用栈 $O(\max(m,n))$，没有优势。
- 数组基线与同步扫描时间同阶；后者少复制、可流式生成答案。
- 若允许破坏输入，可复用较长链表节点，将结果新增节点降到最多 1 个；常规题解默认不修改输入，更安全。

常见错误：

- 把逆序链表再次反转，做了无谓工作。
- 循环只写 `while (l1 || l2)`，漏掉最终进位。
- 短链耗尽后直接挂接长链剩余部分，却忘记进位仍可能持续传播。
- 尝试把 100 位数字转换为整数。
- 返回哑节点而不是 `dummy.next`。

## Follow-up 1：数字改为正序存储（LC 445）

### 新定义与变化

最高位在链表头，且不允许修改输入。直接从头相加无法提前知道低位进位；用两个栈把访问顺序反转，再把新节点插到结果头部。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
public:
  ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    vector<int> a, b;
    for (; l1; l1 = l1->next) a.push_back(l1->val);
    for (; l2; l2 = l2->next) b.push_back(l2->val);
    int i = a.size() - 1, j = b.size() - 1, carry = 0;
    ListNode* head = nullptr;
    while (i >= 0 || j >= 0 || carry) {
      int sum = carry;
      if (i >= 0) sum += a[i--];
      if (j >= 0) sum += b[j--];
      head = new ListNode(sum % 10, head);
      carry = sum / 10;
    }
    return head;
  }
};
```

时间 $O(m+n)$，额外空间 $O(m+n)$。对应官方题：[LC 445 两数相加 II](https://leetcode.cn/problems/add-two-numbers-ii/)。

## Follow-up 2：允许原地复用输入节点

### 新定义与变化

调用者明确允许破坏输入，目标是除必要的最终进位外不新建结果节点。先选择较长链表作为承载体，再原地写回各列。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
  int length(ListNode* p) {
    int n = 0;
    for (; p; p = p->next) ++n;
    return n;
  }
public:
  ListNode* addTwoNumbersInPlace(ListNode* l1, ListNode* l2) {
    if (length(l1) < length(l2)) swap(l1, l2);
    ListNode* head = l1;
    ListNode* prev = nullptr;
    int carry = 0;
    while (l1) {
      int sum = l1->val + carry + (l2 ? l2->val : 0);
      l1->val = sum % 10;
      carry = sum / 10;
      prev = l1;
      l1 = l1->next;
      if (l2) l2 = l2->next;
    }
    if (carry) prev->next = new ListNode(carry);
    return head;
  }
};
```

时间 $O(m+n)$，额外空间 $O(1)$，新节点最多一个。代价是输入对象失去原值；共享节点或不可变数据环境中不可使用。

## Follow-up 3：改为任意进制 $B$

### 新定义与变化

节点值范围为 $[0,B-1]$，仍按低位在前存储。原算法完全保留，只把 `% 10`、`/ 10` 改为 `% base`、`/ base`。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
public:
  ListNode* addInBase(ListNode* a, ListNode* b, int base) {
    ListNode dummy;
    ListNode* tail = &dummy;
    long long carry = 0;
    while (a || b || carry) {
      long long sum = carry;
      if (a) {
        sum += a->val;
        a = a->next;
      }
      if (b) {
        sum += b->val;
        b = b->next;
      }
      tail->next = new ListNode(sum % base);
      tail = tail->next;
      carry = sum / base;
    }
    return dummy.next;
  }
};
```

时间 $O(m+n)$，除输出外空间 $O(1)$。新约束必须保证 `base` 合法，并用足够宽的类型容纳单列和。

## Follow-up 4：同时相加 $k$ 个逆序链表

### 新定义与变化

每列汇总所有尚有节点的链表，再传播可能大于 1 的进位。设总节点数为 $S$，逐列访问每条链表会花 $O(kL)$，其中 $L$ 为最长长度；用活动索引列表可避免反复扫描已结束链表，但朴素写法更稳定。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {}
};
class Solution {
public:
  ListNode* addKNumbers(vector<ListNode*> lists) {
    ListNode dummy;
    ListNode* tail = &dummy;
    long long carry = 0;
    while (carry || any_of(lists.begin(), lists.end(), [](ListNode* p) { return p != nullptr; })) {
      long long sum = carry;
      for (ListNode*& p : lists) {
        if (!p) continue;
        sum += p->val;
        p = p->next;
      }
      tail->next = new ListNode(sum % 10);
      tail = tail->next;
      carry = sum / 10;
    }
    return dummy.next;
  }
};
```

若最长长度为 $L$，时间 $O(kL)$，输入指针副本占 $O(k)$，输出另计。若链表长度高度不均衡，可维护活动列表，使时间接近 $O(S+k)$。

## 可复现验证

- 官方元数据、三组样例与全部约束通过力扣中国 GraphQL `question(titleSlug: "add-two-numbers")` 于 2026-07-27 核对。
- ZeroTracer `data.json` 同日检索无此 slug。
- 基础同步扫描以随机十进制数字串构造链表，并与字符串逐位加法 oracle 对拍；覆盖不同长度、全 9、零和最终进位。
- 所有代码块应以 C++23 独立编译。

## Reference

- [力扣中国 LC 2 官方题面](https://leetcode.cn/problems/add-two-numbers/)
- [力扣中国 LC 445 官方题面](https://leetcode.cn/problems/add-two-numbers-ii/)
- [ZeroTracer 社区竞赛分数据](https://zerotrac.github.io/leetcode_problem_rating/data.json)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/add-two-numbers/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="atcoder-abc468-b.md">← [atcoder] ABC468 B Corridor Watch</a>
<a class="daily-archive-pager__next" href="leetcode-top-12-lc560.md">[力扣 Top 12] LC 560 和为 K 的子数组 中等 →</a>
</nav>
