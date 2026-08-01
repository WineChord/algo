---
title: "[力扣 Top 76] LC 19 删除链表的倒数第 N 个结点 中等"
---

# [力扣 Top 76] LC 19 删除链表的倒数第 N 个结点 中等

<p class="daily-archive-kicker">2026-08-02 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d3fe0ecb4738ca3560c88938b0839983ad3127fd3db13da3eec5ad259437231d -->
## 官方原始信息

- Top 排名：76
- 题号：LC 19
- 官方中文标题：删除链表的倒数第 N 个结点
- 官方难度：中等
- 官方链接：[删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)

### 原始题意

给定单链表头结点 `head` 与整数 `n`，删除倒数第 `n` 个结点并返回新头结点。进阶要求一趟扫描完成。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* removeNthFromEnd(ListNode* head, int n);
};
```

### 全部官方样例

```text
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

```text
输入：head = [1], n = 1
输出：[]
```

```text
输入：head = [1,2], n = 1
输出：[1]
```

### 全部约束

- 链表结点数为 `sz`，$1\le sz\le30$。
- $0\le Node.val\le100$。
- $1\le n\le sz$。
- 进阶：尝试一趟扫描。

## 约束推导与接线目标

倒数第 $n$ 个结点等价于正数第 $sz-n+1$ 个。两趟法先求长度再定位；一趟法则让快指针先领先慢指针 $n$ 个结点。当快指针抵达末尾时，慢指针恰位于待删结点的前驱。

删除头结点没有天然前驱，使用哨兵 `dummy -> head` 把它统一成普通接线：令 `slow->next = slow->next->next`。官方保证 `n` 合法，不必处理越界。结点值不参与运算，无溢出风险。

## 解法递进

### 解法一：两趟扫描计算长度

第一趟求长度，第二趟从哨兵走 `length-n` 步到前驱。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* removeNthFromEnd(ListNode* head, int n) {
    int length = 0;
    for (ListNode* node = head; node != nullptr; node = node->next) {
      ++length;
    }
    ListNode dummy(0, head);
    ListNode* previous = &dummy;
    for (int step = 0; step < length - n; ++step) {
      previous = previous->next;
    }
    previous->next = previous->next->next;
    return dummy.next;
  }
};
```

时间 $O(sz)$，空间 $O(1)$，但读取链表两趟。

### 解法二：保存全部结点指针

把哨兵和每个结点指针压栈，下标直接定位前驱。它把“倒数”转成随机访问。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0, head);
    vector<ListNode*> nodes;
    for (ListNode* node = &dummy; node != nullptr; node = node->next) {
      nodes.push_back(node);
    }
    ListNode* previous = nodes[nodes.size() - n - 1];
    previous->next = previous->next->next;
    return dummy.next;
  }
};
```

时间 $O(sz)$，空间 $O(sz)$；它直观但没有满足进阶的一趟常数空间目标。

### 最佳实用解：固定间距双指针

从哨兵出发，让 `fast` 先走 $n+1$ 步，使两指针间隔包含待删结点；随后同步前进，`fast` 为空时 `slow` 正好是前驱。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0, head);
    ListNode* fast = &dummy;
    ListNode* slow = &dummy;
    for (int step = 0; step <= n; ++step) {
      fast = fast->next;
    }
    while (fast != nullptr) {
      fast = fast->next;
      slow = slow->next;
    }
    slow->next = slow->next->next;
    return dummy.next;
  }
};
```

时间 $O(sz)$，额外空间 $O(1)$，只扫描一趟。也可让快指针从 `head` 先走 $n$ 步，再让慢指针从哨兵同步走；关键是明确间距不变量。

## 正确性证明

快指针先从哨兵前进 $n+1$ 条边，所以之后两指针之间始终相隔 $n+1$ 条边。同步移动保持该间距。当 `fast` 走到空指针时，从 `slow` 的下一结点到链表末尾恰有 $n$ 个真实结点，因此 `slow->next` 正是倒数第 $n$ 个结点。接线跳过它后，其余结点顺序不变；哨兵保证删除头结点时同样成立。

## 样例手推

`[1,2,3,4,5],n=2` 中，快指针先从哨兵走 3 步到结点 3。同步移动到 `fast=null` 时，慢指针位于结点 3；跳过其后结点 4 得 `[1,2,3,5]`。单结点时快指针走到空，慢指针仍为哨兵，接线后返回空链表。

## 易错点与方案比较

- 删除的是倒数第 `n` 个，不是值为 `n` 的结点。
- 无哨兵时删除头结点需要特判；哨兵能统一接线。
- 快指针的初始步数必须与慢指针起点一起推导，不能混用不同模板。
- 若语言要求手动释放内存，可保存待删指针后 `delete`；力扣接口只要求返回正确链表。
- 两趟法最容易证明，一趟双指针满足进阶且同为常数空间，推荐记忆“领先距离编码倒数位置”。

## 变种一：删除正数第 $k$ 个结点

新定义：位置从头开始计数。直接走到第 $k$ 个结点的前驱，不需要快慢间距。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value, Node* next = nullptr) : value(value), next(next) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int size, k;
  cin >> size >> k;
  Node dummy(0);
  Node* tail = &dummy;
  for (int i = 0; i < size; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  Node* previous = &dummy;
  for (int step = 1; step < k; ++step) {
    previous = previous->next;
  }
  previous->next = previous->next->next;
  for (Node* node = dummy.next; node != nullptr; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(k)$，空间 $O(1)$（不计输入链表）。

## 变种二：一次删除多个倒数位置

新定义：给出互异的多个倒数位置，同时基于原链表删除。先求长度，把它们转为正向下标，再一趟接线；不能逐次删除后重新解释位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value, Node* next = nullptr) : value(value), next(next) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int size, count;
  cin >> size >> count;
  Node dummy(0);
  Node* tail = &dummy;
  for (int i = 0; i < size; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  vector<char> removed(size);
  while (count--) {
    int fromEnd;
    cin >> fromEnd;
    removed[size - fromEnd] = true;
  }
  Node* previous = &dummy;
  Node* current = dummy.next;
  for (int index = 0; current != nullptr; ++index) {
    if (removed[index]) {
      previous->next = current->next;
    } else {
      previous = current;
    }
    current = current->next;
  }
  for (Node* node = dummy.next; node != nullptr; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(sz+q)$，额外空间 $O(sz)$。

## 变种三：输入链表不可修改

新定义：原结点必须保持原样，返回一条删除目标后的新链表。先求长度，再复制所有非目标结点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value, Node* next = nullptr) : value(value), next(next) {
  }
};
Node* copyWithout(Node* head, int fromEnd) {
  int length = 0;
  for (Node* node = head; node != nullptr; node = node->next) {
    ++length;
  }
  int skipped = length - fromEnd;
  Node dummy(0);
  Node* tail = &dummy;
  int index = 0;
  for (Node* node = head; node != nullptr; node = node->next, ++index) {
    if (index != skipped) {
      tail->next = new Node(node->value);
      tail = tail->next;
    }
  }
  return dummy.next;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int size, fromEnd;
  cin >> size >> fromEnd;
  Node dummy(0);
  Node* tail = &dummy;
  for (int i = 0; i < size; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  for (Node* node = copyWithout(dummy.next, fromEnd); node != nullptr; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(sz)$，新链表空间 $O(sz)$；只读要求使原地 $O(1)$ 接线不再适用。

## 变种四：删除倒数第 $l$ 到第 $r$ 个结点

新定义：从尾部计数的闭区间全部删除。先求长度，换算成从头的闭区间 `[length-r,length-l]`，一次接线跳过整段。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
  Node(int value, Node* next = nullptr) : value(value), next(next) {
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int size, leftFromEnd, rightFromEnd;
  cin >> size >> leftFromEnd >> rightFromEnd;
  Node dummy(0);
  Node* tail = &dummy;
  for (int i = 0; i < size; ++i) {
    int value;
    cin >> value;
    tail->next = new Node(value);
    tail = tail->next;
  }
  int first = size - rightFromEnd;
  int last = size - leftFromEnd;
  Node* previous = &dummy;
  for (int i = 0; i < first; ++i) {
    previous = previous->next;
  }
  Node* after = previous->next;
  for (int i = first; i <= last; ++i) {
    after = after->next;
  }
  previous->next = after;
  for (Node* node = dummy.next; node != nullptr; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(sz)$，额外空间 $O(1)$。

## 验证说明

一趟解与长度法对 8000 条随机链表、全部合法 `n` 对拍，覆盖删头、删尾、单结点与重复值；七段 C++23 代码均通过编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-75-lc394/">← [力扣 Top 75] LC 394 字符串解码 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-77-lc221/">[力扣 Top 77] LC 221 最大正方形 中等 →</a>
</nav>
