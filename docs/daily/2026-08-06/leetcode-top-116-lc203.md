---
title: "[力扣 Top 116] LC 203 移除链表元素 简单"
---

# [力扣 Top 116] LC 203 移除链表元素 简单

<p class="daily-archive-kicker">2026-08-06 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=aa3072be3ececbec9d3716f47e358c34773c3c8acc15f18cb9bd464e6b71aab0 -->
## 官方原始信息

- Top 排名：116
- 题号：LC 203
- 官方中文标题：移除链表元素
- 官方难度：简单
- 官方链接：[移除链表元素](https://leetcode.cn/problems/remove-linked-list-elements/)

### 原始题意、签名、样例与约束

删除单链表中所有值等于 `val` 的节点，返回新头节点。

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* removeElements(ListNode* head, int val);
};
```

```text
[1,2,6,3,4,5,6], val=6 -> [1,2,3,4,5]
[], val=1 -> []
[7,7,7,7], val=7 -> []
```

- 节点数在 $[0,10^4]$ 内。
- $1\le Node.val\le50$，$0\le val\le50$。

## 约束推导与观察

删除头节点会改变返回值。若分别特判连续头部和中间节点，分支容易遗漏；虚拟头节点把“删除原头”统一成“修改前驱的 `next`”。每个节点只需访问一次。

## 解法递进

### 解法一：复制保留节点

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
  ListNode* removeElements(ListNode* head, int val) {
    ListNode dummy;
    ListNode* tail = &dummy;
    for (; head; head = head->next) {
      if (head->val != val) {
        tail->next = new ListNode(head->val);
        tail = tail->next;
      }
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，额外空间 $O(n)$，且不复用原节点。

### 最佳实用解：虚拟头节点原地跳过

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* removeElements(ListNode* head, int val) {
    ListNode dummy{0, head};
    ListNode* previous = &dummy;
    while (previous->next) {
      if (previous->next->val == val) {
        previous->next = previous->next->next;
      } else {
        previous = previous->next;
      }
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$，优先记忆。

### 同阶方案：递归后序过滤

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* removeElements(ListNode* head, int val) {
    if (!head) {
      return nullptr;
    }
    head->next = removeElements(head->next, val);
    return head->val == val ? head->next : head;
  }
};
```

时间 $O(n)$，递归栈 $O(n)$；更短但长链表有栈深风险。

## 正确性证明

循环不变量：`dummy` 到 `previous` 的链表只含已扫描且应保留的节点，`previous->next` 是首个未决定节点。若其值等于目标，跳过它不改变已保留前缀；否则把 `previous` 前移，将该节点加入保留前缀。每轮至少排除一个未决定节点，终止时所有节点均处理，返回的 `dummy.next` 恰含全部且仅含非目标节点，并保持原相对顺序。

## 样例手推

对 `[1,2,6,3,4,5,6]`，前驱依次越过 1、2；遇 6 时保持前驱不动并把 `next` 指向 3，最后一个 6 同理被跳过。全为 7 时前驱始终是虚拟头，最终返回空。

## 易错点与方案比较

- 删除节点后不要立刻前移前驱，否则连续目标值会漏删。
- 本题平台负责节点生命周期；若业务代码要求释放内存，应先保存被删指针再 `delete`。
- 不能只修改节点值来“覆盖”删除。
- 递归简洁；虚拟头迭代在空间和稳定性上更优。

## 变种一：按任意谓词删除

新定义：删除所有不在闭区间 `[low,high]` 的节点，虚拟头结构不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
ListNode* keepRange(ListNode* head, int low, int high) {
  ListNode dummy{0, head};
  ListNode* previous = &dummy;
  while (previous->next) {
    int value = previous->next->val;
    if (value < low || value > high) {
      previous->next = previous->next->next;
    } else {
      previous = previous->next;
    }
  }
  return dummy.next;
}
int main() {
  cout << (keepRange(nullptr, 0, 1) == nullptr) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：删除排序链表中所有重复值

对应 [LC 82 删除排序链表中的重复元素 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/)。发现重复段后整体跳过。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
public:
  ListNode* deleteDuplicates(ListNode* head) {
    ListNode dummy{0, head};
    ListNode* previous = &dummy;
    while (previous->next) {
      ListNode* first = previous->next;
      ListNode* after = first->next;
      while (after && after->val == first->val) {
        after = after->next;
      }
      if (first->next != after) {
        previous->next = after;
      } else {
        previous = first;
      }
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：不可变链表的结构共享过滤

新定义：原链表不可修改；从尾到头递归，若当前节点保留则新建节点，否则共享已过滤后缀。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int val;
  shared_ptr<const Node> next;
};
shared_ptr<const Node> removeValue(shared_ptr<const Node> head, int value) {
  if (!head) {
    return nullptr;
  }
  auto suffix = removeValue(head->next, value);
  if (head->val == value) {
    return suffix;
  }
  if (suffix == head->next) {
    return head;
  }
  return make_shared<Node>(Node{head->val, suffix});
}
int main() {
  cout << (removeValue(nullptr, 1) == nullptr) << '\n';
}
```

时间 $O(n)$，新节点最多 $O(n)$，未变化后缀可共享。

## 变种四：双向链表删除目标值并维护尾指针

新定义：返回新的头尾指针。删除时同时修复前驱与后继。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int val;
  Node* prev;
  Node* next;
};
pair<Node*, Node*> removeValue(Node* head, Node* tail, int value) {
  for (Node* p = head; p;) {
    Node* next = p->next;
    if (p->val == value) {
      if (p->prev) {
        p->prev->next = p->next;
      } else {
        head = p->next;
      }
      if (p->next) {
        p->next->prev = p->prev;
      } else {
        tail = p->prev;
      }
    }
    p = next;
  }
  return {head, tail};
}
int main() {
  auto [head, tail] = removeValue(nullptr, nullptr, 1);
  cout << (head == tail) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

随机生成长度 `0..100`、值域 `0..8` 的链表，以数组过滤为 oracle，比对输出值序列、保留节点相对顺序、尾指针为空和无环；覆盖空链表、目标只在头尾、连续目标、全删与完全不删。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/remove-linked-list-elements/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-115-lc143/">← [力扣 Top 115] LC 143 重排链表 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-117-lc78/">[力扣 Top 117] LC 78 子集 中等 →</a>
</nav>
