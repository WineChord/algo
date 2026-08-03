---
title: "[力扣 Top 99] LC 707 设计链表 中等"
---

# [力扣 Top 99] LC 707 设计链表 中等

<p class="daily-archive-kicker">2026-08-04 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-04 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=ebf43ff4c365931394875278b1e48831e808062f8d2c894827c21c4dc1e7607c -->
## 官方原始信息

- Top 排名：99
- 题号：LC 707
- 官方中文标题：设计链表
- 官方难度：中等
- 官方链接：[设计链表](https://leetcode.cn/problems/design-linked-list/)

### 原始题意

自行实现 `MyLinkedList`，支持按下标读取、头插、尾插、指定下标前插入和按下标删除。下标从 0 开始，不得使用内置链表库。

### 函数签名

<!-- compile:leetcode -->
```cpp
class MyLinkedList {
public:
  MyLinkedList();
  int get(int index);
  void addAtHead(int val);
  void addAtTail(int val);
  void addAtIndex(int index, int val);
  void deleteAtIndex(int index);
};
```

### 全部官方样例

```text
输入：
["MyLinkedList","addAtHead","addAtTail","addAtIndex","get","deleteAtIndex","get"]
[[],[1],[3],[1,2],[1],[1],[1]]
输出：[null,null,null,null,2,null,3]
解释：依次得到 1，1->3，1->2->3；读取下标 1 为 2；删除后为 1->3。
```

### 全部约束

- $0\le index,val\le1000$。
- 五类操作总调用次数不超过 2000。
- 不得使用内置 `LinkedList` 库。

## 约束推导与哨兵不变量

调用次数不大，数组模拟也能通过；但题目考查节点链接和边界统一。使用头尾哨兵的双向链表，可让真实节点始终处于两个已存在节点之间：插入和删除无需区分头、尾空表。维护 `size` 后先判下标，再从离目标更近的一端走，单次访问为 $O(\min(index,size-index))$。

## 解法递进

### 解法一：动态数组模拟接口

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MyLinkedList {
  vector<int> values;
public:
  MyLinkedList() = default;
  int get(int index) {
    return 0 <= index && index < static_cast<int>(values.size()) ? values[index] : -1;
  }
  void addAtHead(int val) {
    values.insert(values.begin(), val);
  }
  void addAtTail(int val) {
    values.push_back(val);
  }
  void addAtIndex(int index, int val) {
    if (0 <= index && index <= static_cast<int>(values.size())) {
      values.insert(values.begin() + index, val);
    }
  }
  void deleteAtIndex(int index) {
    if (0 <= index && index < static_cast<int>(values.size())) {
      values.erase(values.begin() + index);
    }
  }
};
```

读取 $O(1)$，中间插入删除 $O(n)$，空间 $O(n)$。它适合作为操作序列对拍 oracle，但没有练到链表结构。

### 最佳实用解：双向哨兵链表

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MyLinkedList {
  struct Node {
    int value;
    Node* previous;
    Node* next;
    explicit Node(int value = 0) : value(value), previous(nullptr), next(nullptr) {
    }
  };
  Node* head;
  Node* tail;
  int size;
  Node* nodeAt(int index) const {
    if (index < size / 2) {
      Node* node = head->next;
      while (index-- > 0) {
        node = node->next;
      }
      return node;
    }
    Node* node = tail;
    for (int steps = size - index; steps > 0; --steps) {
      node = node->previous;
    }
    return node;
  }
  void insertBefore(Node* next, int value) {
    Node* node = new Node(value);
    Node* previous = next->previous;
    node->previous = previous;
    node->next = next;
    previous->next = node;
    next->previous = node;
    ++size;
  }
public:
  MyLinkedList() : head(new Node()), tail(new Node()), size(0) {
    head->next = tail;
    tail->previous = head;
  }
  ~MyLinkedList() {
    Node* node = head;
    while (node != nullptr) {
      Node* next = node->next;
      delete node;
      node = next;
    }
  }
  int get(int index) {
    return 0 <= index && index < size ? nodeAt(index)->value : -1;
  }
  void addAtHead(int val) {
    insertBefore(head->next, val);
  }
  void addAtTail(int val) {
    insertBefore(tail, val);
  }
  void addAtIndex(int index, int val) {
    if (0 <= index && index <= size) {
      insertBefore(index == size ? tail : nodeAt(index), val);
    }
  }
  void deleteAtIndex(int index) {
    if (index < 0 || index >= size) {
      return;
    }
    Node* node = nodeAt(index);
    node->previous->next = node->next;
    node->next->previous = node->previous;
    delete node;
    --size;
  }
};
```

头尾插 $O(1)$，其余操作 $O(\min(index,n-index))$，空间 $O(n)$。哨兵让所有链接修改服从同一不变量，最适合作为链表模板。

## 正确性证明

始终维持：`head->next` 到 `tail->previous` 恰为按顺序的 `size` 个真实节点，且任意相邻节点互为 `next/previous`。构造时不变量对空表成立。`insertBefore` 只把新节点插入一条既有相邻边并把 `size` 加一，顺序和双向链接保持；删除把目标两邻居重新直连并减一，也保持不变量。`nodeAt` 从任一哨兵按准确步数到达第 `index` 个节点，因此所有公开接口符合定义。

## 样例手推、边界与易错点

空表哨兵相连；头插 1 后为 `head<->1<->tail`；尾插 3，再在下标 1 前插 2，得到 `1,2,3`；删除下标 1 后得到 `1,3`。空表读取、`index==size` 尾插、`index>size` 忽略、删除唯一节点均由哨兵统一处理。

- `get` 与 `delete` 的合法范围是 $[0,size)$，插入是 $[0,size]$。
- 修改链接时必须同时更新两个方向。
- 删除后先断链再 `delete`，并防止继续访问悬空指针。
- 自管内存的类应处理析构；若允许复制，还需遵守 Rule of Five，本题判题不会复制对象。

## 变种一：给定节点句柄时 $O(1)$ 删除

新定义：插入返回稳定句柄，之后可按句柄删除，不再按下标定位。双向链接的修改不变，省去遍历。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* previous;
  Node* next;
};
int main() {
  int queryCount;
  cin >> queryCount;
  Node head{0, nullptr, nullptr};
  Node tail{0, &head, nullptr};
  head.next = &tail;
  unordered_map<int, Node*> handles;
  int nextHandle = 1;
  while (queryCount--) {
    char type;
    cin >> type;
    if (type == '+') {
      int value;
      cin >> value;
      Node* node = new Node{value, tail.previous, &tail};
      tail.previous->next = node;
      tail.previous = node;
      handles[nextHandle] = node;
      cout << nextHandle++ << '\n';
    } else {
      int handle;
      cin >> handle;
      auto it = handles.find(handle);
      if (it != handles.end()) {
        Node* node = it->second;
        node->previous->next = node->next;
        node->next->previous = node->previous;
        delete node;
        handles.erase(it);
      }
    }
  }
  for (Node* node = head.next; node != &tail;) {
    Node* next = node->next;
    delete node;
    node = next;
  }
}
```

期望单次 $O(1)$，空间 $O(n)$。稳定句柄改变了定位模型。

## 变种二：循环双向链表

新定义：尾节点的后继是头节点，支持光标向前或向后循环移动。只用一个哨兵，空表时它自环。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* previous;
  Node* next;
};
int main() {
  int n, steps;
  cin >> n >> steps;
  Node sentinel{0, nullptr, nullptr};
  sentinel.previous = sentinel.next = &sentinel;
  for (int i = 0; i < n; ++i) {
    int value;
    cin >> value;
    Node* node = new Node{value, sentinel.previous, &sentinel};
    sentinel.previous->next = node;
    sentinel.previous = node;
  }
  Node* cursor = sentinel.next;
  while (steps-- > 0 && cursor != &sentinel) {
    cursor = cursor->next;
    if (cursor == &sentinel) {
      cursor = cursor->next;
    }
  }
  if (cursor != &sentinel) {
    cout << cursor->value << '\n';
  }
  while (sentinel.next != &sentinel) {
    Node* node = sentinel.next;
    sentinel.next = node->next;
    delete node;
  }
}
```

构造 $O(n)$，移动 $O(steps)$，空间 $O(n)$。

## 变种三：持久化头插链表

新定义：每次头插产生新版本，旧版本仍可访问。节点不可变且版本只保存头指针，结构共享即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  shared_ptr<const Node> next;
};
int main() {
  int queryCount;
  cin >> queryCount;
  vector<shared_ptr<const Node>> versions(1, nullptr);
  while (queryCount--) {
    char type;
    int version;
    cin >> type >> version;
    if (type == '+') {
      int value;
      cin >> value;
      versions.push_back(make_shared<Node>(Node{value, versions[version]}));
    } else {
      int index;
      cin >> index;
      auto node = versions[version];
      while (node != nullptr && index-- > 0) {
        node = node->next;
      }
      cout << (node == nullptr ? -1 : node->value) << '\n';
    }
  }
}
```

每次头插 $O(1)$，查询 $O(index)$，新增版本只增加一个节点。

## 变种四：大规模下标操作改用隐式 Treap

新定义：操作次数放大到 $2\times10^5$，仍按下标插入、删除、读取。普通链表定位为线性，隐式 Treap 以子树大小支持期望 $O(\log n)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  unsigned priority;
  int size;
  Node* left;
  Node* right;
  explicit Node(int value, unsigned priority)
      : value(value), priority(priority), size(1), left(nullptr), right(nullptr) {
  }
};
int sizeOf(Node* node) {
  return node == nullptr ? 0 : node->size;
}
void pull(Node* node) {
  if (node != nullptr) {
    node->size = 1 + sizeOf(node->left) + sizeOf(node->right);
  }
}
void split(Node* node, int count, Node*& left, Node*& right) {
  if (node == nullptr) {
    left = right = nullptr;
  } else if (sizeOf(node->left) >= count) {
    split(node->left, count, left, node->left);
    right = node;
    pull(right);
  } else {
    split(node->right, count - sizeOf(node->left) - 1, node->right, right);
    left = node;
    pull(left);
  }
}
Node* merge(Node* left, Node* right) {
  if (left == nullptr || right == nullptr) {
    return left == nullptr ? right : left;
  }
  if (left->priority > right->priority) {
    left->right = merge(left->right, right);
    pull(left);
    return left;
  }
  right->left = merge(left, right->left);
  pull(right);
  return right;
}
int get(Node* node, int index) {
  int leftSize = sizeOf(node->left);
  if (index == leftSize) {
    return node->value;
  }
  return index < leftSize ? get(node->left, index) : get(node->right, index - leftSize - 1);
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  mt19937 random(1234567);
  int queryCount;
  cin >> queryCount;
  Node* root = nullptr;
  while (queryCount--) {
    char type;
    int index;
    cin >> type >> index;
    if (type == '+') {
      int value;
      cin >> value;
      Node *left, *right;
      split(root, index, left, right);
      root = merge(merge(left, new Node(value, random())), right);
    } else if (type == '-') {
      Node *left, *middle, *right;
      split(root, index, left, right);
      split(right, 1, middle, right);
      delete middle;
      root = merge(left, right);
    } else {
      cout << get(root, index) << '\n';
    }
  }
}
```

每次操作期望 $O(\log n)$，空间 $O(n)$；代价是实现与证明复杂度显著上升。

## 可复现验证

所有代码块按 GNU++23 编译。双向链表与动态数组 oracle 在随机合法/非法操作序列上逐次比较返回值及完整序列，并覆盖空表、唯一节点和两端操作。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/design-linked-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-98-lc543/">← [力扣 Top 98] LC 543 二叉树的直径 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-100-lc67/">[力扣 Top 100] LC 67 二进制求和 简单 →</a>
</nav>
