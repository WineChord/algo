---
title: "[力扣 Top 114] LC 142 环形链表 II 中等"
---

# [力扣 Top 114] LC 142 环形链表 II 中等

<p class="daily-archive-kicker">2026-08-06 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../graph/functional-graphs/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=cb3d958d645910459c16380f4b18d8f5a8f1bab53bbdaa69d7edfd9ae60e9d17 -->
## 官方原始信息

- Top 排名：114
- 题号：LC 142
- 官方中文标题：环形链表 II
- 官方难度：中等
- 官方链接：[环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/)

### 原始题意、函数签名、样例与约束

给定单链表头节点，返回入环的第一个节点；无环返回 `nullptr`，且不得修改链表。`pos` 只描述评测数据，不是函数参数。

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* detectCycle(ListNode* head);
};
```

```text
输入：head = [3,2,0,-4], pos = 1
输出：索引 1 的节点
输入：head = [1,2], pos = 0
输出：索引 0 的节点
输入：head = [1], pos = -1
输出：null
```

- 节点数在 $[0,10^4]$ 内。
- $-10^5\le Node.val\le10^5$。
- `pos=-1` 或为合法索引；进阶要求 $O(1)$ 空间。

## 约束推导与观察

哈希集合可记录首次重复节点，但占 $O(n)$ 空间。Floyd 快慢指针若相遇，则设入环前长度为 $\mu$、环长为 $\lambda$，相遇时快指针比慢指针多走整环；由同余关系，从头和相遇点各走一步会在入环点相遇。

## 解法递进

### 解法一：哈希记录访问顺序

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
  ListNode* detectCycle(ListNode* head) {
    unordered_set<ListNode*> seen;
    while (head) {
      if (!seen.insert(head).second) {
        return head;
      }
      head = head->next;
    }
    return nullptr;
  }
};
```

时间 $O(n)$，空间 $O(n)$。

### 最佳实用解：Floyd 两阶段

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
  ListNode* detectCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    do {
      if (!fast || !fast->next) {
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
};
```

时间 $O(n)$，空间 $O(1)$，优先记忆。哈希法更直观且能直接得到访问序号，但常数空间要求下 Floyd 最稳。

## 正确性证明

若无环，快指针最终到达空节点并返回空。若有环，慢指针入环后，快指针相对它每轮前进一步，至多 $\lambda$ 轮相遇。设相遇前慢指针走了 $\mu+x$ 步，则快指针走了 $2(\mu+x)$ 步，差值 $\mu+x$ 是环长倍数，所以 $\mu\equiv-x\pmod\lambda$。从相遇点再走 $\mu$ 步，恰从环内偏移 `x` 回到入环点；从头走 $\mu$ 步也到入环点，故第二阶段返回值正确。

## 样例手推

`3→2→0→-4→2` 中快慢指针会在环内相遇。把慢指针放回头后，两者同步前进，在值为 2 的索引 1 节点相遇。单节点自环第一阶段一次即相遇，第二阶段直接返回头；单节点无环则检测到 `fast->next` 为空。

## 易错点与方案比较

- 比较节点地址，不比较节点值。
- `pos` 不是参数，不能尝试读取。
- 快指针前进前必须检查 `fast` 与 `fast->next`。
- Floyd 第二阶段两指针都一次走一步，不能继续让一个指针走两步。

## 变种一：返回环长

相遇后让一个指针绕环一周，步数就是 $\lambda$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
int cycleLength(ListNode* head) {
  ListNode* slow = head;
  ListNode* fast = head;
  do {
    if (!fast || !fast->next) {
      return 0;
    }
    slow = slow->next;
    fast = fast->next->next;
  } while (slow != fast);
  int length = 1;
  for (fast = fast->next; fast != slow; fast = fast->next) {
    ++length;
  }
  return length;
}
int main() {
  cout << cycleLength(nullptr) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种二：安全地断开环

新定义：若有环，把环内指向入口的那条边改为空。先找入口，再绕环找其前驱。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
void removeCycle(ListNode* head) {
  ListNode* slow = head;
  ListNode* fast = head;
  do {
    if (!fast || !fast->next) {
      return;
    }
    slow = slow->next;
    fast = fast->next->next;
  } while (slow != fast);
  slow = head;
  while (slow != fast) {
    slow = slow->next;
    fast = fast->next;
  }
  ListNode* tail = slow;
  while (tail->next != slow) {
    tail = tail->next;
  }
  tail->next = nullptr;
}
int main() {
  removeCycle(nullptr);
}
```

时间 $O(n)$，空间 $O(1)$；此变种允许修改链表，原题不允许。

## 变种三：两个无环链表的第一个相交节点

对应 [LC 160 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/)。双指针各走 `A+B` 与 `B+A`，长度差被抵消。

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
  ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    ListNode* a = headA;
    ListNode* b = headB;
    while (a != b) {
      a = a ? a->next : headB;
      b = b ? b->next : headA;
    }
    return a;
  }
};
```

时间 $O(n+m)$，空间 $O(1)$。

## 变种四：函数迭代中首次重复状态

新定义：给定函数图 `next[0..n-1]` 和起点，返回尾长、环长与入口。链表 Floyd 原样迁移到整数状态。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, start;
  cin >> n >> start;
  vector<int> next(n);
  for (int& x : next) {
    cin >> x;
  }
  int slow = next[start];
  int fast = next[next[start]];
  while (slow != fast) {
    slow = next[slow];
    fast = next[next[fast]];
  }
  int entry = start;
  int tailLength = 0;
  while (entry != slow) {
    entry = next[entry];
    slow = next[slow];
    ++tailLength;
  }
  int cycleLength = 1;
  for (int x = next[entry]; x != entry; x = next[x]) {
    ++cycleLength;
  }
  cout << entry << ' ' << tailLength << ' ' << cycleLength << '\n';
}
```

时间 $O(\mu+\lambda)$，空间 $O(1)$。

## 可复现验证

随机生成长度不超过 100 的链表，枚举 `pos=-1..n-1` 建环，用地址哈希法作 oracle 对比 Floyd；固定覆盖空链表、单节点无环、自环、入口为头、长尾短环。所有代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/linked-list-cycle-ii/)
- [对应知识专题](../../graph/functional-graphs.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-113-lc122/">← [力扣 Top 113] LC 122 买卖股票的最佳时机 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-115-lc143/">[力扣 Top 115] LC 143 重排链表 中等 →</a>
</nav>
