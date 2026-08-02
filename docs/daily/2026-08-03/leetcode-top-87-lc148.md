---
title: "[力扣 Top 87] LC 148 排序链表 中等"
---

# [力扣 Top 87] LC 148 排序链表 中等

<p class="daily-archive-kicker">2026-08-03 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ef2f8c29563e1f99f21c77654ae16bb9dd5e4d9b73280bd3607ce804f61fcfce -->
## 官方原始信息

- Top 排名：87
- 题号：LC 148
- 官方中文标题：排序链表
- 官方难度：中等
- 官方链接：[排序链表](https://leetcode.cn/problems/sort-list/)

### 原始题意

给定单链表头节点 `head`，按升序返回排序后的链表。进阶要求时间 $O(n\log n)$、额外空间 $O(1)$。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* sortList(ListNode* head);
};
```

### 全部官方样例

```text
输入：head = [4,2,1,3]
输出：[1,2,3,4]
```

```text
输入：head = [-1,5,3,4,0]
输出：[-1,0,3,4,5]
```

```text
输入：head = []
输出：[]
```

### 全部约束

- 链表节点数在 $[0,5\times10^4]$。
- $-10^5\le Node.val\le10^5$。
- 进阶：$O(n\log n)$ 时间和 $O(1)$ 额外空间。

## 约束推导与结构选择

$n=5\times10^4$ 排除 $O(n^2)$ 插入排序。数组上的堆排和快排依赖随机访问，而单链表只能顺序走；归并排序的“切分”和“合并”都只改 `next` 指针，天然适配。

递归归并时间正确，但递归栈为 $O(\log n)$，严格说不满足进阶的 $O(1)$ 额外空间。自底向上按长度 1、2、4……合并相邻有序段，可以消除递归栈。合并时相等值优先取左段，保持节点的原相对顺序。

## 解法递进

### 解法一：收集节点值后排序

把值放入数组，排序，再顺序写回链表。它简单正确，但使用 $O(n)$ 空间，且没有真正重排节点。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* sortList(ListNode* head) {
    vector<int> values;
    for (ListNode* node = head; node; node = node->next) {
      values.push_back(node->val);
    }
    sort(values.begin(), values.end());
    int index = 0;
    for (ListNode* node = head; node; node = node->next) {
      node->val = values[index++];
    }
    return head;
  }
};
```

时间 $O(n\log n)$，额外空间 $O(n)$。

### 解法二：自顶向下归并排序

快慢指针找中点、断链，递归排序两半再稳定合并。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  ListNode* merge(ListNode* first, ListNode* second) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (first && second) {
      if (first->val <= second->val) {
        tail->next = first;
        first = first->next;
      } else {
        tail->next = second;
        second = second->next;
      }
      tail = tail->next;
    }
    tail->next = first ? first : second;
    return dummy.next;
  }
public:
  ListNode* sortList(ListNode* head) {
    if (!head || !head->next) {
      return head;
    }
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
      slow = slow->next;
      fast = fast->next->next;
    }
    ListNode* second = slow->next;
    slow->next = nullptr;
    return merge(sortList(head), sortList(second));
  }
};
```

时间 $O(n\log n)$，递归栈 $O(\log n)$。

### 最佳实用解：自底向上原地归并

每轮把链表切成相邻的长度 `width` 段，两两合并；用哑节点连接新链表。最后一段不足长度也能自然处理。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  ListNode* split(ListNode* head, int length) {
    while (--length && head) {
      head = head->next;
    }
    if (!head) {
      return nullptr;
    }
    ListNode* next = head->next;
    head->next = nullptr;
    return next;
  }
  pair<ListNode*, ListNode*> merge(ListNode* first, ListNode* second) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (first && second) {
      if (first->val <= second->val) {
        tail->next = first;
        first = first->next;
      } else {
        tail->next = second;
        second = second->next;
      }
      tail = tail->next;
    }
    tail->next = first ? first : second;
    while (tail->next) {
      tail = tail->next;
    }
    return {dummy.next, tail};
  }
public:
  ListNode* sortList(ListNode* head) {
    int length = 0;
    for (ListNode* node = head; node; node = node->next) {
      ++length;
    }
    ListNode dummy(0, head);
    for (int width = 1; width < length; width *= 2) {
      ListNode* previous = &dummy;
      ListNode* current = dummy.next;
      while (current) {
        ListNode* first = current;
        ListNode* second = split(first, width);
        current = split(second, width);
        auto [mergedHead, mergedTail] = merge(first, second);
        previous->next = mergedHead;
        mergedTail->next = current;
        previous = mergedTail;
      }
    }
    return dummy.next;
  }
};
```

时间 $O(n\log n)$，额外空间 $O(1)$，满足进阶要求。

## 正确性证明

第 `width` 轮开始时，链表可分成若干长度至多 `width` 的有序段；初始 `width=1` 显然成立。算法逐对切下相邻段并稳定合并，合并结果有序且长度至多 `2*width`，并按原覆盖顺序无遗漏地重新连接所有节点。因此下一轮不变量对 `2*width` 成立。宽度首次不小于链表长度时，整表已成为一个有序段。算法只重连既有节点，每个节点恰好出现一次，所以返回链表既完整又升序。

## 样例手推

`[4,2,1,3]`：宽度 1 时合并为 `[2,4]` 与 `[1,3]`；宽度 2 时合并两段，依次取 1、2、3、4，得到 `[1,2,3,4]`。空链表长度为 0，不进入循环并直接返回空；单节点同理。

## 易错点与方案比较

- 快慢指针递归版必须断开 `slow->next`，否则形成重复递归。
- `split` 要在段尾置空，合并才不会越过边界。
- 每次合并后必须找到并保存合并段尾，再接回尚未处理部分。
- 相等时取左段的 `<=` 才能稳定；写 `<` 会让右段相等节点提前。
- 自顶向下更短，自底向上严格常数辅助空间；题目进阶优先后者。

## 变种一：按绝对值稳定排序

新定义：按 `abs(val)` 升序，相等时保持原节点顺序。只需把合并比较器改为绝对值的 `<=`，底层归并结构不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
Node* mergeLists(Node* first, Node* second) {
  Node dummy{};
  Node* tail = &dummy;
  while (first && second) {
    if (abs(first->value) <= abs(second->value)) {
      tail->next = first;
      first = first->next;
    } else {
      tail->next = second;
      second = second->next;
    }
    tail = tail->next;
  }
  tail->next = first ? first : second;
  return dummy.next;
}
Node* sortList(Node* head) {
  if (!head || !head->next)
    return head;
  Node* slow = head;
  Node* fast = head->next;
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
  }
  Node* second = slow->next;
  slow->next = nullptr;
  return mergeLists(sortList(head), sortList(second));
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  for (Node* node = sortList(n ? &nodes[0] : nullptr); node; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\log n)$，递归栈 $O(\log n)$。

## 变种二：排序双向链表

新定义：节点还有 `prev` 指针。归并连接 `next` 时同步维护新头的 `prev=nullptr` 与每条反向边。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* previous;
  Node* next;
};
Node* mergeLists(Node* first, Node* second) {
  Node dummy{};
  Node* tail = &dummy;
  while (first || second) {
    Node* chosen;
    if (!second || (first && first->value <= second->value)) {
      chosen = first;
      first = first->next;
    } else {
      chosen = second;
      second = second->next;
    }
    tail->next = chosen;
    chosen->previous = tail == &dummy ? nullptr : tail;
    tail = chosen;
  }
  tail->next = nullptr;
  return dummy.next;
}
Node* sortList(Node* head) {
  if (!head || !head->next)
    return head;
  Node* slow = head;
  Node* fast = head->next;
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
  }
  Node* second = slow->next;
  slow->next = nullptr;
  second->previous = nullptr;
  return mergeLists(sortList(head), sortList(second));
}
int main() {
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].previous = i ? &nodes[i - 1] : nullptr;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  for (Node* node = sortList(n ? &nodes[0] : nullptr); node; node = node->next) {
    cout << node->value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n\log n)$，递归栈 $O(\log n)$。

## 变种三：合并 $K$ 条已排序链表

新定义：输入已各自有序的 $K$ 条链表，输出全局有序链表。最小堆始终保存每条链表尚未取出的头节点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int listCount;
  cin >> listCount;
  vector<vector<Node>> storage(listCount);
  auto compare = [](Node* left, Node* right) { return left->value > right->value; };
  priority_queue<Node*, vector<Node*>, decltype(compare)> heap(compare);
  for (int i = 0; i < listCount; ++i) {
    int size;
    cin >> size;
    storage[i].resize(size);
    for (int j = 0; j < size; ++j) {
      cin >> storage[i][j].value;
      storage[i][j].next = j + 1 < size ? &storage[i][j + 1] : nullptr;
    }
    if (size)
      heap.push(&storage[i][0]);
  }
  Node dummy{};
  Node* tail = &dummy;
  while (!heap.empty()) {
    Node* node = heap.top();
    heap.pop();
    if (node->next)
      heap.push(node->next);
    tail->next = node;
    tail = node;
  }
  tail->next = nullptr;
  for (Node* node = dummy.next; node; node = node->next)
    cout << node->value << ' ';
  cout << '\n';
}
```

总节点数为 $N$ 时，时间 $O(N\log K)$，空间 $O(K)$。

## 变种四：链表几乎有序时使用插入排序

新定义：逆序很少，希望利用局部有序性。维护已排序前缀，把每个节点插入哑节点后的正确位置；最坏平方，但接近有序时移动较少。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next;
};
int main() {
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  Node dummy{INT_MIN, nullptr};
  Node* current = n ? &nodes[0] : nullptr;
  while (current) {
    Node* next = current->next;
    Node* position = &dummy;
    while (position->next && position->next->value <= current->value) {
      position = position->next;
    }
    current->next = position->next;
    position->next = current;
    current = next;
  }
  for (Node* node = dummy.next; node; node = node->next)
    cout << node->value << ' ';
  cout << '\n';
}
```

最坏时间 $O(n^2)$，空间 $O(1)$；一般规模仍应使用归并排序。

## 验证说明

本轮将七段代码按 C++23 编译；自底向上链表排序会与数组排序 oracle 在随机长度 0–50、含重复值的链表上逐节点对拍，并检查节点集合、无环、升序和稳定性。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/sort-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-86-lc136/">← [力扣 Top 86] LC 136 只出现一次的数字 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-88-lc10/">[力扣 Top 88] LC 10 正则表达式匹配 困难 →</a>
</nav>
