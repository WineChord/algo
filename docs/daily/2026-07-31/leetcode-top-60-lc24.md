---
title: "[力扣 Top 60] LC 24 两两交换链表中的节点 中等"
---

# [力扣 Top 60] LC 24 两两交换链表中的节点 中等

<p class="daily-archive-kicker">2026-07-31 · 第 11/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=69602975fa6cf4a9be4fd3029ad27d1335e8d5f376a24fee806e4ea1479cc7eb -->
## 官方原始信息

- Top 排名：60
- 题号：LC 24
- 官方中文标题：两两交换链表中的节点
- 官方难度：中等
- 官方链接：[两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/)

### 原始题意

给定单链表，两两交换相邻节点并返回新头节点。必须交换节点本身，不能只修改节点中的值。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* swapPairs(ListNode* head);
};
```

### 全部官方样例

```text
输入：head = [1,2,3,4]
输出：[2,1,4,3]
```

```text
输入：head = []
输出：[]
```

```text
输入：head = [1]
输出：[1]
```

### 全部约束

- 链表节点数范围为 $[0,100]$。
- $0\le Node.val\le100$。
- 不得只修改节点内部的值。

## 约束推导与边界

链表长度很小，但题目考查的是指针重连。每次处理相邻的 `first` 与 `second`，还必须把前一组的尾部接到交换后的 `second`。虚拟头节点统一了“首对交换会改变头节点”和普通中间节点两种情况。空链表、单节点以及奇数长度的最后一个节点都应原样保留。

## 解法递进

### 解法一：收集节点指针后交换相邻项

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* nextNode = nullptr) : val(value), next(nextNode) {
  }
};
class Solution {
public:
  ListNode* swapPairs(ListNode* head) {
    vector<ListNode*> nodes;
    for (ListNode* current = head; current != nullptr; current = current->next) {
      nodes.push_back(current);
    }
    for (int i = 0; i + 1 < static_cast<int>(nodes.size()); i += 2) {
      swap(nodes[i], nodes[i + 1]);
    }
    for (int i = 0; i < static_cast<int>(nodes.size()); ++i) {
      nodes[i]->next = i + 1 < static_cast<int>(nodes.size()) ? nodes[i + 1] : nullptr;
    }
    return nodes.empty() ? nullptr : nodes[0];
  }
};
```

时间 $O(n)$，空间 $O(n)$。

### 最佳实用解：虚拟头节点原地重连

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* nextNode = nullptr) : val(value), next(nextNode) {
  }
};
class Solution {
public:
  ListNode* swapPairs(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* previous = &dummy;
    while (previous->next != nullptr && previous->next->next != nullptr) {
      ListNode* first = previous->next;
      ListNode* second = first->next;
      first->next = second->next;
      second->next = first;
      previous->next = second;
      previous = first;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 正确性证明

每轮开始时，`previous` 指向已经处理完的前缀最后一个节点，`previous->next` 是下一对的第一个节点。三次赋值把 `previous -> first -> second -> suffix` 精确改成 `previous -> second -> first -> suffix`，没有丢失后缀；随后 `previous=first`，不变量对下一组继续成立。循环只在至少还有两个节点时执行，所以剩余 0 或 1 个节点自然保留。结束时虚拟头的后继就是交换后的完整链表。

## 样例手推

`dummy -> 1 -> 2 -> 3 -> 4` 首轮变为 `dummy -> 2 -> 1 -> 3 -> 4`，`previous` 移到 1；第二轮把 `1 -> 3 -> 4` 改成 `1 -> 4 -> 3`，得到 `2 -> 1 -> 4 -> 3`。

## 易错点与方案比较

- 必须先保存 `first` 和 `second`，按固定顺序重连，避免丢失后缀。
- 每轮结束后 `previous` 应指向交换后靠后的 `first`。
- 不能通过交换 `val` 规避节点重连。
- 递归写法同样简洁但使用 $O(n)$ 调用栈；虚拟头迭代版常数空间，推荐默认使用。

## 变种一：每 k 个节点一组翻转

不足 `k` 个的尾段保持原序。每组先确认长度足够，再翻转半开区间。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value) : value(value), next(nullptr) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  Node dummy(0);
  Node* tail = &dummy;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  Node* groupPrevious = &dummy;
  while (true) {
    Node* kth = groupPrevious;
    for (int i = 0; i < k && kth != nullptr; ++i) {
      kth = kth->next;
    }
    if (kth == nullptr) {
      break;
    }
    Node* groupNext = kth->next;
    Node* previous = groupNext;
    Node* current = groupPrevious->next;
    while (current != groupNext) {
      Node* next = current->next;
      current->next = previous;
      previous = current;
      current = next;
    }
    Node* oldFirst = groupPrevious->next;
    groupPrevious->next = kth;
    groupPrevious = oldFirst;
  }
  for (Node* current = dummy.next; current != nullptr; current = current->next) {
    cout << current->value << " \n"[current->next == nullptr];
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：交换第 i 与第 j 个节点

节点按一基编号。保存两个节点及其前驱，再分相邻与不相邻情况重连。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value = 0) : value(value), next(nullptr) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, firstIndex, secondIndex;
  cin >> n >> firstIndex >> secondIndex;
  Node dummy;
  Node* tail = &dummy;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  if (firstIndex > secondIndex) {
    swap(firstIndex, secondIndex);
  }
  if (firstIndex != secondIndex) {
    Node* beforeFirst = &dummy;
    for (int i = 1; i < firstIndex; ++i) {
      beforeFirst = beforeFirst->next;
    }
    Node* beforeSecond = &dummy;
    for (int i = 1; i < secondIndex; ++i) {
      beforeSecond = beforeSecond->next;
    }
    Node* first = beforeFirst->next;
    Node* second = beforeSecond->next;
    if (first->next == second) {
      first->next = second->next;
      second->next = first;
      beforeFirst->next = second;
    } else {
      swap(first->next, second->next);
      beforeFirst->next = second;
      beforeSecond->next = first;
    }
  }
  for (Node* current = dummy.next; current != nullptr; current = current->next) {
    cout << current->value << " \n"[current->next == nullptr];
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：仅交换逆序的相邻节点

每一对中只有前值大于后值时才交换节点；这相当于对不重叠的相邻对各做一次局部排序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value = 0) : value(value), next(nullptr) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  Node dummy;
  Node* tail = &dummy;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  Node* previous = &dummy;
  while (previous->next != nullptr && previous->next->next != nullptr) {
    Node* first = previous->next;
    Node* second = first->next;
    if (first->value > second->value) {
      first->next = second->next;
      second->next = first;
      previous->next = second;
      previous = first;
    } else {
      previous = second;
    }
  }
  for (Node* current = dummy.next; current != nullptr; current = current->next) {
    cout << current->value << " \n"[current->next == nullptr];
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种四：双向链表两两交换

除 `next` 外还要同步维护 `previous`，并最终检查两种方向遍历一致。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* previous;
  Node* next;
  Node(int value = 0) : value(value), previous(nullptr), next(nullptr) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  Node dummy;
  Node* tail = &dummy;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    Node* node = new Node(value);
    tail->next = node;
    node->previous = tail;
    tail = node;
  }
  Node* before = &dummy;
  while (before->next != nullptr && before->next->next != nullptr) {
    Node* first = before->next;
    Node* second = first->next;
    Node* after = second->next;
    before->next = second;
    second->previous = before;
    second->next = first;
    first->previous = second;
    first->next = after;
    if (after != nullptr) {
      after->previous = first;
    }
    before = first;
  }
  Node* current = dummy.next;
  if (current != nullptr) {
    current->previous = nullptr;
  }
  while (current != nullptr) {
    cout << current->value << " \n"[current->next == nullptr];
    current = current->next;
  }
}
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

对长度 0 到 30 的随机链表，把原地版本输出节点地址序列与“收集指针后交换”的 oracle 比较；同时验证每个原节点恰出现一次、没有环、值未修改。覆盖空表、单节点、奇数和偶数长度。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/swap-nodes-in-pairs/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/swap-nodes-in-pairs/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-59-lc35/">← [力扣 Top 59] LC 35 搜索插入位置 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-512-q2-lc4001/">[力扣竞赛] 第 512 场周赛 Q2 LC 4001 聚合两个时间序列 中等 →</a>
</nav>
