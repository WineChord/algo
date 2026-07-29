---
title: "[力扣 Top 22] LC 206 反转链表 简单"
---

# [力扣 Top 22] LC 206 反转链表 简单

<p class="daily-archive-kicker">2026-07-28 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-28 题目列表</a> · <a href="../../data-structures/linked-lists.md">进入知识专题</a></p>

## 官方原始信息

- 难度：LeetCode 官方「简单」；非竞赛题，无官方分值与 ZeroTracer 竞赛分。
- 官方链接：https://leetcode.cn/problems/reverse-linked-list/
- slug：`reverse-linked-list`
- 函数签名：`ListNode* reverseList(ListNode* head)`
- 题意：反转单链表并返回新头节点。
- 示例：`[1,2,3,4,5] -> [5,4,3,2,1]`；`[1,2] -> [2,1]`；`[] -> []`。
- 官方示意图：https://assets.leetcode.com/uploads/2021/02/19/rev1ex1.jpg 与 https://assets.leetcode.com/uploads/2021/02/19/rev1ex2.jpg。
- 约束：节点数 $0\ldots5000$；$-5000\le\text{Node.val}\le5000$。
- 官方进阶：分别使用迭代与递归完成。

以下代码块都内置等价 `ListNode` 定义以便独立 C++23 编译。

## 约束、样例与边界

链表只能沿 `next` 单向访问，因此任何解都至少读取 $n$ 个节点。空链表、单节点、自带重复值都不改变指针逻辑。最关键的破坏性边界是：改写 `cur->next` 前若未保存原后继，剩余链表将永久丢失。递归深度最坏 5000，通常可通过，但迭代更稳。

## 暴力：收集节点后逆序重连

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* reverseList(ListNode* head) {
    vector<ListNode*> nodes;
    for (ListNode* p = head; p; p = p->next) nodes.push_back(p);
    for (int i = (int)nodes.size() - 1; i > 0; --i) nodes[i]->next = nodes[i - 1];
    if (!nodes.empty()) nodes[0]->next = nullptr;
    return nodes.empty() ? nullptr : nodes.back();
  }
};
```

时间 $O(n)$，空间 $O(n)$。它覆盖全部节点，但保存了本可由三个指针表达的完整序列。

## 最优：迭代反转每一条边

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
      ListNode* next = cur->next;
      cur->next = prev;
      prev = cur;
      cur = next;
    }
    return prev;
  }
};
```

循环不变量：`prev` 是已经反转且节点集合正确的前缀头，`cur` 是尚未处理后缀头，两部分不重不漏。保存 `next` 后反转当前边，再同时推进，保持不变量；结束时后缀为空，`prev` 即完整答案。时间 $O(n)$，空间 $O(1)$，达到最优。样例 `[1,2,3]` 的状态依次为 `prev=1,cur=2`、`prev=2->1,cur=3`、`prev=3->2->1,cur=null`。

面试优先记忆迭代三指针：常数小、无栈溢出风险，也最容易迁移到区间与分组反转。

## Follow-up 1：递归反转

递归先反转 `head->next` 的后缀，再让原后继指回 `head`。原算法仍成立，但隐式栈空间变为 $O(n)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* reverseList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* newHead = reverseList(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
  }
};
```

时间 $O(n)$，递归空间 $O(n)$。

## Follow-up 2：只反转区间 $[\mathtt{left},\mathtt{right}]$

区间前后必须保持连接。用哨兵找到区间前驱，再做头插法，每次把区间内下一个节点搬到区间头；对应 LC 92。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int i = 1; i < left; ++i) before = before->next;
    ListNode* first = before->next;
    for (int i = left; i < right; ++i) {
      ListNode* moved = first->next;
      first->next = moved->next;
      moved->next = before->next;
      before->next = moved;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 3：每 $k$ 个节点一组反转

不足 $k$ 个的末段保持原样。每轮先确认完整组，再复用局部三指针反转并连接；对应 LC 25。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    while (true) {
      ListNode* kth = groupPrev;
      for (int i = 0; i < k && kth; ++i) kth = kth->next;
      if (!kth) break;
      ListNode* groupNext = kth->next;
      ListNode* prev = groupNext;
      ListNode* cur = groupPrev->next;
      while (cur != groupNext) {
        ListNode* next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
      }
      ListNode* oldHead = groupPrev->next;
      groupPrev->next = kth;
      groupPrev = oldHead;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 4：不得修改原链表

破坏性重连失效；扫描原链表并把新节点头插到副本中。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
ListNode* reversedCopy(const ListNode* head) {
  ListNode* copy = nullptr;
  for (const ListNode* p = head; p; p = p->next) copy = new ListNode(p->val, copy);
  return copy;
}
```

时间 $O(n)$，新节点空间 $O(n)$。

## Follow-up 5：回文判断后恢复链表

找到中点，反转后半段并比较；为避免调用后改变输入，再反转一次恢复。对应 LC 234。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
  ListNode* reverse(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
      ListNode* next = head->next;
      head->next = prev;
      prev = head;
      head = next;
    }
    return prev;
  }
public:
  bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast->next && fast->next->next) {
      slow = slow->next;
      fast = fast->next->next;
    }
    ListNode* second = reverse(slow->next);
    bool ok = true;
    for (ListNode* a = head, *b = second; b; a = a->next, b = b->next) {
      if (a->val != b->val) ok = false;
    }
    slow->next = reverse(second);
    return ok;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。

## 易错点与验证

- 改边前保存原后继；最终旧头必须指向 `nullptr`。
- 递归基例同时覆盖空链与单节点。
- 区间和分组反转要保存组前驱、旧组头和组后继。
- 随机验证：生成长度 $0\ldots100$ 的链表，比较向量逆序结果与迭代反转；再反转一次应恢复原值序列和节点地址顺序。

## Reference

- [官方题目](https://leetcode.cn/problems/reverse-linked-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-21-lc20.md">← [力扣 Top 21] LC 20 有效的括号 简单</a>
<a class="daily-archive-pager__next" href="leetcode-top-23-lc21.md">[力扣 Top 23] LC 21 合并两个有序链表 简单 →</a>
</nav>
