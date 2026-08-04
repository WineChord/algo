---
title: "[力扣 Top 103] LC 92 反转链表 II 中等"
---

# [力扣 Top 103] LC 92 反转链表 II 中等

<p class="daily-archive-kicker">2026-08-05 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=4947024dadad486aa7e5a374d862df6226d536becd1792e2a5df478188ef2c34 -->
## 官方原始信息

- Top 排名：103
- 题号：LC 92
- 官方中文标题：反转链表 II
- 官方难度：中等
- 官方链接：[反转链表 II](https://leetcode.cn/problems/reverse-linked-list-ii/)

### 原始题意

给定单链表头节点 `head` 和两个一基位置 `left`、`right`，原地反转从第 `left` 个到第 `right` 个节点组成的连续区间，返回反转后的头节点。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right);
};
```

### 全部官方样例

```text
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]
```

```text
输入：head = [5], left = 1, right = 1
输出：[5]
```

### 全部约束

- 链表节点数为 $n$。
- $1\le n\le500$。
- $-500\le Node.val\le500$。
- $1\le\mathtt{left}\le\mathtt{right}\le n$。
- 进阶要求一趟扫描完成。

## 约束推导与观察

链表不支持随机访问，真正困难的不是反转本身，而是保存三处连接：区间前驱、区间反转后的头和尾、区间后继。若 `left = 1`，真实头节点会改变；哨兵节点能把“反转从头开始”统一为普通区间。

节点值范围与算法无关，不能通过数值排序。只需改写 `next`，不会产生算术溢出。

## 解法递进

### 解法一：保存区间值再写回

它不改变节点拓扑，而是用数组反转值。若题目或调用方关注节点身份，这种方案不满足真正的链表区间反转语义，因此只作为对照基准。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right) {
    vector<int> values;
    ListNode* node = head;
    for (int position = 1; position <= right; ++position, node = node->next) {
      if (position >= left) {
        values.push_back(node->val);
      }
    }
    reverse(values.begin(), values.end());
    node = head;
    int index = 0;
    for (int position = 1; position <= right; ++position, node = node->next) {
      if (position >= left) {
        node->val = values[index++];
      }
    }
    return head;
  }
};
```

时间 $O(n)$，额外空间 $O(n)$，并且节点值被修改。

### 最佳实用解：哨兵加区间头插

先令 `before` 指向区间前驱。每轮摘下 `tail->next`，把它插到 `before` 之后；`tail` 始终是已反转区间的尾。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int position = 1; position < left; ++position) {
      before = before->next;
    }
    ListNode* tail = before->next;
    for (int step = 0; step < right - left; ++step) {
      ListNode* moved = tail->next;
      tail->next = moved->next;
      moved->next = before->next;
      before->next = moved;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$，只扫描到 `right`。它统一处理 `left = 1`，是推荐记忆的实现。

### 同阶方案：先标准反转，再接回三段

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int position = 1; position < left; ++position) {
      before = before->next;
    }
    ListNode* first = before->next;
    ListNode* current = first;
    ListNode* previous = nullptr;
    for (int position = left; position <= right; ++position) {
      ListNode* following = current->next;
      current->next = previous;
      previous = current;
      current = following;
    }
    before->next = previous;
    first->next = current;
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。它复用了整链表反转模板，但临时断开方向时需要更仔细保存边界；头插法更不易接错。

## 正确性证明

头插循环开始时，`before->next` 是当前已反转部分的头，`tail` 是其尾，`tail->next` 是尚未搬入的第一个节点。一次操作摘下该节点并插到 `before` 后方，因此已反转部分长度增加 1、节点顺序恰好继续逆转；`tail->next` 又自动指向下一个未处理节点，区间外两段仍连通。执行 `right-left` 次后，原区间全部节点逆序且前后连接完整。哨兵保证 `left=1` 时同一证明仍成立。

## 样例手推

对 `1→2→3→4→5`、区间 `[2,4]`，`before=1`、`tail=2`。先把 3 插到 1 后得到 `1→3→2→4→5`；再把 4 插入得到 `1→4→3→2→5`。`left=right` 时循环零次，链表保持不变。

## 易错点与方案比较

- `left`、`right` 是一基位置。
- 不能丢失 `tail->next`，否则区间后缀断链。
- 反转节点与交换节点值不是同一契约。
- 返回 `dummy.next`，不要固定返回原 `head`。
- 头插与标准反转同为 $O(n)$/$O(1)$；头插的连接不变量更局部，面试中更稳。

## 变种一：反转整个链表

新定义：区间固定为 `[1,n]`，不再需要前后拼接，只保留标准三指针反转。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
class Solution {
public:
  ListNode* reverseList(ListNode* head) {
    ListNode* previous = nullptr;
    ListNode* current = head;
    while (current) {
      ListNode* following = current->next;
      current->next = previous;
      previous = current;
      current = following;
    }
    return previous;
  }
};
```

时间 $O(n)$，空间 $O(1)$；对应 [LC 206](https://leetcode.cn/problems/reverse-linked-list/)。

## 变种二：每 $k$ 个节点一组反转

新定义：只反转完整的长度 $k$ 分组，末尾不足 $k$ 个保持原序。每组先确认右边界存在，再复用局部头插。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
class Solution {
public:
  ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    while (true) {
      ListNode* end = before;
      for (int i = 0; i < k && end; ++i) {
        end = end->next;
      }
      if (!end) {
        break;
      }
      ListNode* tail = before->next;
      for (int step = 1; step < k; ++step) {
        ListNode* moved = tail->next;
        tail->next = moved->next;
        moved->next = before->next;
        before->next = moved;
      }
      before = tail;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$；对应 [LC 25](https://leetcode.cn/problems/reverse-nodes-in-k-group/)。

## 变种三：原链表只读，返回持久化副本

新定义：不得改写任何原节点。先复制全部值，在副本数组中反转目标区间，再建立新链表。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
ListNode* persistentReverse(ListNode* head, int left, int right) {
  vector<int> values;
  for (ListNode* node = head; node; node = node->next) {
    values.push_back(node->val);
  }
  reverse(values.begin() + left - 1, values.begin() + right);
  ListNode dummy;
  ListNode* tail = &dummy;
  for (int value : values) {
    tail->next = new ListNode(value);
    tail = tail->next;
  }
  return dummy.next;
}
int main() {
  int n, left, right;
  cin >> n >> left >> right;
  ListNode dummy;
  ListNode* tail = &dummy;
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    tail->next = new ListNode(value);
    tail = tail->next;
  }
  for (ListNode* node = persistentReverse(dummy.next, left, right); node; node = node->next) {
    cout << node->val << (node->next ? ' ' : '\n');
  }
}
```

时间 $O(n)$，新版本空间 $O(n)$。原地算法在只读或版本化场景中失效。

## 变种四：反转多个互不相交且按位置递增的区间

新定义：给定若干 `[l,r]`，保证递增且不重叠。让扫描指针只向前移动，每个节点最多参与一次反转。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int value = 0, ListNode* following = nullptr) : val(value), next(following) {
  }
};
ListNode* reverseRanges(ListNode* head, const vector<pair<int, int>>& ranges) {
  ListNode dummy(0, head);
  ListNode* before = &dummy;
  int beforePosition = 0;
  for (auto [left, right] : ranges) {
    while (beforePosition + 1 < left) {
      before = before->next;
      ++beforePosition;
    }
    ListNode* tail = before->next;
    for (int step = 0; step < right - left; ++step) {
      ListNode* moved = tail->next;
      tail->next = moved->next;
      moved->next = before->next;
      before->next = moved;
    }
    before = tail;
    beforePosition = right;
  }
  return dummy.next;
}
int main() {
  int n, q;
  cin >> n >> q;
  ListNode dummy;
  ListNode* tail = &dummy;
  for (int i = 0, value; i < n; ++i) {
    cin >> value;
    tail->next = new ListNode(value);
    tail = tail->next;
  }
  vector<pair<int, int>> ranges(q);
  for (auto& [left, right] : ranges) {
    cin >> left >> right;
  }
  for (ListNode* node = reverseRanges(dummy.next, ranges); node; node = node->next) {
    cout << node->val << (node->next ? ' ' : '\n');
  }
}
```

时间 $O(n+\sum(r_i-l_i))=O(n)$，额外空间 $O(1)$（不计输入区间）。若区间重叠，顺序会影响结果，必须重新定义契约。

## 验证说明

本轮将八段代码按 C++23 编译；三种主方案会与数组区间反转 oracle 对拍 20,000 个随机链表及全部合法区间，并检查节点地址集合不变、无断链、无环。变种覆盖 $k=1$、不足一组、首尾区间和多个相邻区间。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/reverse-linked-list-ii/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-102-lc647/">← [力扣 Top 102] LC 647 回文子串 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-104-lc347/">[力扣 Top 104] LC 347 前 K 个高频元素 中等 →</a>
</nav>
