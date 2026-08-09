---
title: "[力扣 Top 124] LC 61 旋转链表 中等"
---

# [力扣 Top 124] LC 61 旋转链表 中等

<p class="daily-archive-kicker">2026-08-09 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=367b158d8e0e2cacb681d1a80ea7e894691f39bfd7b4b7ad1f4b3e1c22a9e391 -->
## 官方原始信息

- Top 排名：124
- 题号：LC 61
- 官方中文标题：旋转链表
- 官方难度：中等
- 官方链接：[旋转链表](https://leetcode.cn/problems/rotate-list/)

### 原始题意与函数签名

给定单链表头节点 `head` 和非负整数 `k`，把每个节点向右移动 `k` 个位置，返回旋转后的头节点。

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* rotateRight(ListNode* head, int k);
};
```

### 全部官方样例

```text
输入：head = [1,2,3,4,5], k = 2
输出：[4,5,1,2,3]
```

```text
输入：head = [0,1,2], k = 4
输出：[2,0,1]
```

### 全部约束

- 链表节点数 $n$ 在 $[0,500]$ 内。
- $-100\le Node.val\le100$。
- $0\le k\le2\times10^9$。

## 约束推导与观察

`k` 远大于链表长度，必须先取 $k\bmod n$。右移 `r` 位等价于在原链表第 $n-r$ 个节点后切开，把后段接到前面。单链表不能随机访问，所以先扫一遍得到长度与尾节点，再走到新尾节点即可。

## 解法递进

### 解法一：重复执行一次右移

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
class Solution {
public:
  ListNode* rotateRight(ListNode* head, int k) {
    if (!head) {
      return nullptr;
    }
    for (int step = 0; step < k; ++step) {
      if (!head->next) {
        break;
      }
      ListNode* previous = nullptr;
      ListNode* tail = head;
      while (tail->next) {
        previous = tail;
        tail = tail->next;
      }
      previous->next = nullptr;
      tail->next = head;
      head = tail;
    }
    return head;
  }
};
int main() {
}
```

每次移动都找尾节点，时间 $O(nk)$，空间 $O(1)$。当 `k` 达到 $2\times10^9$ 时不可行。

### 解法二：保存所有节点地址

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
class Solution {
public:
  ListNode* rotateRight(ListNode* head, int k) {
    if (!head) {
      return nullptr;
    }
    vector<ListNode*> nodes;
    for (ListNode* p = head; p; p = p->next) {
      nodes.push_back(p);
    }
    int n = nodes.size();
    int shift = k % n;
    if (shift == 0) {
      return head;
    }
    nodes[n - shift - 1]->next = nullptr;
    nodes.back()->next = head;
    return nodes[n - shift];
  }
};
int main() {
}
```

时间 $O(n)$、空间 $O(n)$，逻辑直观，但辅助数组并非必需。

### 最佳实用解：首尾成环后在切点断开

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
class Solution {
public:
  ListNode* rotateRight(ListNode* head, int k) {
    if (!head || !head->next || k == 0) {
      return head;
    }
    int n = 1;
    ListNode* tail = head;
    while (tail->next) {
      tail = tail->next;
      ++n;
    }
    int shift = k % n;
    if (shift == 0) {
      return head;
    }
    tail->next = head;
    int stepsToNewTail = n - shift - 1;
    ListNode* newTail = head;
    while (stepsToNewTail--) {
      newTail = newTail->next;
    }
    ListNode* newHead = newTail->next;
    newTail->next = nullptr;
    return newHead;
  }
};
int main() {
}
```

时间 $O(n)$、空间 $O(1)$。成环把“尾接头”统一完成，只需在唯一新尾处断开，是优先记忆方案。

## 正确性证明

设有效右移量为 $r=k\bmod n$。若 $r=0$，每个节点回到原位置。否则旋转后原下标 $n-r$ 的节点成为新头，原下标 $n-r-1$ 的节点成为新尾。算法先把原尾连接原头形成保持原相对顺序的环，再从原头走 $n-r-1$ 步定位新尾，令其后继为新头并断开。所得线性次序正是原后 $r$ 个节点接原前 $n-r$ 个节点，因此正确。

## 样例手推

`[1,2,3,4,5]` 中 $n=5,r=2$。新尾是原下标 2 的节点 3，新头是节点 4；断开后得到 `[4,5,1,2,3]`。样例 2 中 $4\bmod3=1$，新头为 2，得到 `[2,0,1]`。

## 易错点与方案比较

- 空链表不能取模；先处理 `head == nullptr`。
- 新尾需要走 $n-r-1$ 步，不是 $n-r$ 步。
- 成环后必须断开，否则返回循环链表。
- `k` 很大但 `int` 足够；关键是先对长度取模，避免重复移动。

## 变种一：向左旋转 `k` 位

新定义：把每个节点向左移动。左移 $k$ 等价于右移 $n-(k\bmod n)$，也可直接在第 `k mod n` 个节点前切开。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
ListNode* rotateLeft(ListNode* head, int k) {
  if (!head || !head->next) {
    return head;
  }
  int n = 1;
  ListNode* tail = head;
  while (tail->next) {
    tail = tail->next;
    ++n;
  }
  int shift = k % n;
  if (shift == 0) {
    return head;
  }
  ListNode* newTail = head;
  for (int i = 1; i < shift; ++i) {
    newTail = newTail->next;
  }
  ListNode* newHead = newTail->next;
  newTail->next = nullptr;
  tail->next = head;
  return newHead;
}
int main() {
}
```

时间 $O(n)$、空间 $O(1)$。

## 变种二：只旋转下标区间 `[left,right]`

新定义：仅把单链表的一段向右旋转 `k` 位，其余节点位置不变。先用哨兵找到段前驱和段尾，再在该段内部成环、切开、接回。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
ListNode* rotateRange(ListNode* head, int left, int right, int k) {
  if (!head || left == right) {
    return head;
  }
  ListNode dummy(0, head);
  ListNode* before = &dummy;
  for (int pos = 1; pos < left; ++pos) {
    before = before->next;
  }
  int len = right - left + 1;
  int shift = k % len;
  if (shift == 0) {
    return dummy.next;
  }
  ListNode* oldHead = before->next;
  ListNode* oldTail = oldHead;
  for (int i = 1; i < len; ++i) {
    oldTail = oldTail->next;
  }
  ListNode* after = oldTail->next;
  oldTail->next = oldHead;
  ListNode* newTail = oldHead;
  for (int i = 0; i < len - shift - 1; ++i) {
    newTail = newTail->next;
  }
  before->next = newTail->next;
  newTail->next = after;
  return dummy.next;
}
int main() {
}
```

时间 $O(n)$、空间 $O(1)$。

## 变种三：输入链表不可修改

新定义：必须保留原链表结构，返回旋转后的深拷贝。先收集值，按新下标顺序创建新节点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  explicit ListNode(int x = 0, ListNode* p = nullptr) : val(x), next(p) {
  }
};
ListNode* rotatedCopy(const ListNode* head, int k) {
  vector<int> values;
  for (const ListNode* p = head; p; p = p->next) {
    values.push_back(p->val);
  }
  if (values.empty()) {
    return nullptr;
  }
  int n = values.size();
  int shift = k % n;
  ListNode dummy;
  ListNode* tail = &dummy;
  for (int i = 0; i < n; ++i) {
    int source = (i - shift + n) % n;
    tail->next = new ListNode(values[source]);
    tail = tail->next;
  }
  return dummy.next;
}
int main() {
}
```

时间 $O(n)$、额外空间 $O(n)$，代价换来原结构完全不变。

## 变种四：静态数组上的大量旋转与访问

新定义：底层序列不变，支持多次左右旋转和按当前逻辑下标读取。无需每次搬动元素，只维护逻辑头偏移。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class RotatedView {
  vector<int> data;
  int head = 0;
public:
  explicit RotatedView(vector<int> values) : data(move(values)) {
  }
  void rotateRight(long long k) {
    int n = data.size();
    head = (head - static_cast<int>(k % n) + n) % n;
  }
  void rotateLeft(long long k) {
    int n = data.size();
    head = (head + static_cast<int>(k % n)) % n;
  }
  int at(int index) const {
    return data[(head + index) % data.size()];
  }
};
int main() {
  RotatedView view({1, 2, 3, 4});
  view.rotateRight(1);
  cout << view.at(0) << '\n';
}
```

每次旋转与访问均为 $O(1)$，空间 $O(n)$。链表若也需要大量随机访问，原结构不再合适，应换成数组式表示。

## 可复现验证

枚举长度 $0..12$、全部 $0\le k\le30$，把链表结果转成数组，与数组下标公式 `(i-k mod n+n) mod n` 对照；并检查节点数量不变、无环且原节点恰出现一次。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/rotate-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-123-lc39/">← [力扣 Top 123] LC 39 组合总和 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-125-lc746/">[力扣 Top 125] LC 746 使用最小花费爬楼梯 简单 →</a>
</nav>
