---
title: "[力扣 Top 47] LC 160 相交链表 简单"
---

# [力扣 Top 47] LC 160 相交链表 简单

<p class="daily-archive-kicker">2026-07-30 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ed972d532a92825b2ad9ccdc9dbe003bf82854026ff2200550c44c43c193fba5 -->
## 官方原始信息

- Top 排名：47
- 题号：LC 160
- 官方中文标题：相交链表
- 官方难度：简单
- 官方链接：[相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/)

### 原始题意

给定两个无环单链表的头节点，返回它们相交的第一个节点；不相交则返回空指针。相交按节点对象是否相同判断，不按节点值判断，且不能修改原链表。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* getIntersectionNode(ListNode* headA, ListNode* headB);
};
```

### 全部官方样例

```text
输入：intersectVal = 8
listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]
skipA = 2, skipB = 3
输出：Intersected at '8'
```

```text
输入：intersectVal = 2
listA = [1,9,1,2,4], listB = [3,2,4]
skipA = 3, skipB = 1
输出：Intersected at '2'
```

```text
输入：intersectVal = 0
listA = [2,6,4], listB = [1,5]
skipA = 3, skipB = 2
输出：No intersection
```

### 全部约束

- 两个链表长度分别为 $m,n$，且 $1\le m,n\le3\times10^4$。
- $1\le Node.val\le10^5$。
- 链式结构无环。
- 相交后两个链表共享完整后缀，不可能再次分开。
- 进阶要求 $O(m+n)$ 时间、$O(1)$ 额外空间。

## 约束推导与结构观察

若两个单链表共享某个节点，该节点的 `next` 也相同，所以从首个交点起共享整个后缀。困难只在两条独有前缀长度可能不同。让两个指针都走恰好 $m+n$ 步，分别经历 `A+B` 与 `B+A`，就能自动抵消长度差。

## 解法递进

### 解法一：枚举节点对

比较 A 中每个节点与 B 中每个节点的地址，时间 $O(mn)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    for (ListNode* a = headA; a != nullptr; a = a->next) {
      for (ListNode* b = headB; b != nullptr; b = b->next) {
        if (a == b) {
          return a;
        }
      }
    }
    return nullptr;
  }
};
```

### 解法二：哈希集合

记录 A 的所有节点，再扫描 B 找第一个命中。时间 $O(m+n)$，空间 $O(m)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    unordered_set<ListNode*> seen;
    for (ListNode* node = headA; node != nullptr; node = node->next) {
      seen.insert(node);
    }
    for (ListNode* node = headB; node != nullptr; node = node->next) {
      if (seen.contains(node)) {
        return node;
      }
    }
    return nullptr;
  }
};
```

### 最佳实用解：双指针交换起点

指针走到本链表末尾后切换到另一条链表头；二者要么在首个交点相遇，要么同时到达空指针。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    ListNode* a = headA;
    ListNode* b = headB;
    while (a != b) {
      a = a == nullptr ? headB : a->next;
      b = b == nullptr ? headA : b->next;
    }
    return a;
  }
};
```

时间复杂度 $O(m+n)$，额外空间 $O(1)$。

## 正确性证明

若两链表不相交，指针 `a` 依次走过 A 与 B，`b` 依次走过 B 与 A；总路程均为 $m+n$，最终同时成为空指针。

若独有前缀长度分别为 $x,y$，共享后缀长度为 $c$，则 `a` 在走过 $x+c+y$ 步后到达交点，`b` 在走过 $y+c+x$ 步后也到达同一节点。交换头节点使两者总路程相同，长度差被抵消。相交后后继完全相同，所以首次相遇就是首个交点。

## 样例手推

样例一中 A 独有前缀长 2，B 独有前缀长 3。A 指针先走完 A 后切到 B，B 指针先走完 B 后切到 A；两者各补走对方独有前缀后，在值为 8 的同一节点对象相遇。值为 1 的两个节点地址不同，不会误判。

## 易错点与方案比较

- 必须比较指针地址 `a == b`，不能比较 `val`。
- 循环条件允许两者在 `nullptr` 相遇，因此不需要额外“不相交”分支。
- 不能临时反转、断开或给链表打标记，因为题目要求结构保持不变。
- 双指针方案最短且满足进阶；哈希方案更易推广到有环或多链表但占额外空间。
- 该结论依赖无环；有环时指针可能永不进入相同的有限路程模型。

## 变种一：返回共享后缀长度

新定义：除交点外，还返回从交点到尾部的节点数。不改变找交点的方法，命中后再扫描一次共享后缀。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
pair<Node*, int> intersection(Node* head_a, Node* head_b) {
  Node* a = head_a;
  Node* b = head_b;
  while (a != b) {
    a = a == nullptr ? head_b : a->next;
    b = b == nullptr ? head_a : b->next;
  }
  int length = 0;
  for (Node* node = a; node != nullptr; node = node->next) {
    ++length;
  }
  return {a, length};
}
int main() {
  return 0;
}
```

时间 $O(m+n)$，空间 $O(1)$。

## 变种二：求 $k$ 条无环链表的公共起始节点

新定义：返回所有 $k$ 条链表共同拥有的最早节点。两两求交：先求前两条的交点，把该节点当作一条共享后缀的头，再与下一条求交。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
Node* intersect_two(Node* a_head, Node* b_head) {
  Node* a = a_head;
  Node* b = b_head;
  while (a != b) {
    a = a == nullptr ? b_head : a->next;
    b = b == nullptr ? a_head : b->next;
  }
  return a;
}
Node* intersect_all(const vector<Node*>& heads) {
  if (heads.empty()) {
    return nullptr;
  }
  Node* common = heads[0];
  for (int i = 1; i < static_cast<int>(heads.size()) && common != nullptr; ++i) {
    common = intersect_two(common, heads[i]);
  }
  return common;
}
int main() {
  return 0;
}
```

若各链表长度至多 $L$，时间 $O(kL)$ 的量级，空间 $O(1)$（不计输入头数组）。因为任意公共部分仍是某条共享后缀，逐步求交不会丢失可能答案。

## 变种三：链表可能有环

新定义：两个单链表各自可能含环，求任意共同节点。先用 Floyd 找环入口。若都无环，退化为原题；若只有一个有环则不可能相交；若都有环，先检查两个环是否为同一个环，再判断入环前是否相交。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
Node* cycle_entry(Node* head) {
  Node* slow = head;
  Node* fast = head;
  do {
    if (fast == nullptr || fast->next == nullptr) {
      return nullptr;
    }
    slow = slow->next;
    fast = fast->next->next;
  } while (slow != fast);
  slow = head;
  while (slow != fast) {
    slow = slow->next;
    fast = fast->next;
  }
  return slow;
}
int distance_to(Node* head, Node* stop) {
  int distance = 0;
  while (head != stop) {
    head = head->next;
    ++distance;
  }
  return distance;
}
Node* intersection_with_cycles(Node* a, Node* b) {
  Node* entry_a = cycle_entry(a);
  Node* entry_b = cycle_entry(b);
  if ((entry_a == nullptr) != (entry_b == nullptr)) {
    return nullptr;
  }
  if (entry_a == nullptr) {
    Node* x = a;
    Node* y = b;
    while (x != y) {
      x = x == nullptr ? b : x->next;
      y = y == nullptr ? a : y->next;
    }
    return x;
  }
  Node* cursor = entry_a;
  do {
    if (cursor == entry_b) {
      break;
    }
    cursor = cursor->next;
  } while (cursor != entry_a);
  if (cursor != entry_b) {
    return nullptr;
  }
  int len_a = distance_to(a, entry_a);
  int len_b = distance_to(b, entry_b);
  Node* x = a;
  Node* y = b;
  while (len_a > len_b) {
    x = x->next;
    --len_a;
  }
  while (len_b > len_a) {
    y = y->next;
    --len_b;
  }
  while (x != y && x != entry_a && y != entry_b) {
    x = x->next;
    y = y->next;
  }
  return x == y ? x : entry_a;
}
int main() {
  return 0;
}
```

时间 $O(m+n)$，空间 $O(1)$。若两入口不同但属于同一环，环上没有由两条头路径共同定义的唯一“第一个”节点，因此这里返回 A 的环入口作为任意共同节点。

## 变种四：只允许读取节点编号，不能比较指针

新定义：每个节点有全局唯一不可变 `id`，跨链表共享节点表现为同一 `id`，但接口不暴露地址。用哈希集合记录第一条链表的编号。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  long long id;
  Node* next;
};
long long intersection_id(Node* a, Node* b) {
  unordered_set<long long> seen;
  for (Node* node = a; node != nullptr; node = node->next) {
    seen.insert(node->id);
  }
  for (Node* node = b; node != nullptr; node = node->next) {
    if (seen.contains(node->id)) {
      return node->id;
    }
  }
  return -1;
}
int main() {
  return 0;
}
```

时间 $O(m+n)$，空间 $O(m)$。若编号不保证全局唯一，无法仅凭值恢复“同一节点”语义，必须改变接口或保留对象身份。

## 可复现验证

- 三个官方样例、头节点即相交、只共享尾节点、完全不交、相同值但不同节点均应覆盖。
- 随机构造两条独有前缀加共享后缀，可把哈希解作为 oracle 与双指针解对拍。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/intersection-of-two-linked-lists/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/intersection-of-two-linked-lists/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-46-lc739/">← [力扣 Top 46] LC 739 每日温度 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-48-lc1143/">[力扣 Top 48] LC 1143 最长公共子序列 中等 →</a>
</nav>
