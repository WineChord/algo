---
title: "[力扣 Top 69] LC 138 随机链表的复制 中等"
---

# [力扣 Top 69] LC 138 随机链表的复制 中等

<p class="daily-archive-kicker">2026-08-01 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a93426bb0e02f95f5453c8c7022c225f6b6c6976e2ab5dff99b399d729bbbfb2 -->
## 官方原始信息

- Top 排名：69
- 题号：LC 138
- 官方中文标题：随机链表的复制
- 官方难度：中等
- 官方链接：[随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/)

### 原始题意

单链表每个节点除 `next` 外还有 `random`，它可指向链内任意节点或空。构造由全新节点组成的深拷贝，使两类指针在复制节点之间保持相同关系，且复制链表中的指针不能指回原节点。

### 函数签名

<!-- compile:leetcode-random-list -->
```cpp
class Solution {
public:
  Node* copyRandomList(Node* head);
};
```

### 全部官方样例

```text
输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

```text
输入：head = [[1,1],[2,1]]
输出：[[1,1],[2,1]]
```

```text
输入：head = [[3,null],[3,0],[3,null]]
输出：[[3,null],[3,0],[3,null]]
```

### 全部约束

- $0\le n\le1000$。
- $-10^4\le Node.val\le10^4$。
- `random` 为空或指向链表中的某个节点。

## 约束推导与边界

复制值与 `next` 容易，难点是遇到 `random` 时目标副本可能尚未创建。通用解用映射 `original -> clone` 建立身份对应；若要常数额外空间，可利用 `next` 链暂时把每个副本插到原节点后面。此时原节点 `x` 的副本恒为 `x->next`，所以 `x->random` 的副本就是 `x->random->next`。

最后必须把交织链拆成原链和复制链，同时恢复原链。空链直接返回空。值是否重复无关，映射与交织都按节点地址而不是值识别身份。

## 解法递进

### 解法一：哈希表两遍复制

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Node {
public:
  int val;
  Node* next;
  Node* random;
  explicit Node(int value) : val(value), next(nullptr), random(nullptr) {
  }
};
class Solution {
public:
  Node* copyRandomList(Node* head) {
    unordered_map<Node*, Node*> clone;
    clone[nullptr] = nullptr;
    for (Node* node = head; node; node = node->next) {
      clone[node] = new Node(node->val);
    }
    for (Node* node = head; node; node = node->next) {
      clone[node]->next = clone[node->next];
      clone[node]->random = clone[node->random];
    }
    return clone[head];
  }
};
```

期望时间 $O(n)$，额外空间 $O(n)$。它最通用、证明最直接。

### 最佳实用解：交织节点实现常数辅助空间

第一遍在每个原节点后插入副本；第二遍连接副本的 `random`；第三遍拆链并恢复原链。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Node {
public:
  int val;
  Node* next;
  Node* random;
  explicit Node(int value) : val(value), next(nullptr), random(nullptr) {
  }
};
class Solution {
public:
  Node* copyRandomList(Node* head) {
    if (!head) {
      return nullptr;
    }
    for (Node* node = head; node;) {
      Node* next = node->next;
      node->next = new Node(node->val);
      node->next->next = next;
      node = next;
    }
    for (Node* node = head; node; node = node->next->next) {
      node->next->random = node->random ? node->random->next : nullptr;
    }
    Node* copiedHead = head->next;
    for (Node* node = head; node;) {
      Node* copy = node->next;
      Node* next = copy->next;
      node->next = next;
      copy->next = next ? next->next : nullptr;
      node = next;
    }
    return copiedHead;
  }
};
```

时间 $O(n)$，除返回的新节点外额外空间 $O(1)$。

## 正确性证明

交织第一遍后，对每个原节点 $x$，紧随它的 `x->next` 是值相同且唯一对应的副本。若 `x->random=y`，则 `y->next` 正是 $y$ 的副本，因此第二遍赋值使副本随机边保持完全相同的对应关系；空指针也保持为空。

第三遍对每对相邻的原／副本节点，把原节点重新连到下一个原节点，把副本连到下一个副本。于是原链恢复，副本链的 `next` 与 `random` 都只指向副本，并且节点值与所有边一一对应，满足深拷贝定义。

## 样例手推

原链 `7→13→11` 交织为 `7→7'→13→13'→11→11'`。若原 13 的 `random` 指向 7，则 `13'->random=13->random->next=7'`。拆链后原链回到 `7→13→11`，复制链为 `7'→13'→11'`，随机关系未指回原节点。

空链返回空；单节点随机指向自身时，交织后 `copy->random=original->random->next=copy`，自环正确保留。

## 易错点与方案比较

- 不能用节点值做键，值允许重复。
- 设置 `random` 前必须保证所有副本已经插入。
- 第二遍原节点每次跨两步；第三遍要先保存下一个原节点再改指针。
- 深拷贝不仅要求值相等，还要求复制图中的任何指针都不落到原图。
- 哈希表法适用于任意图结构并最易维护；交织法利用了 `next` 是一条完整线性链，空间最优但会暂时修改输入。进阶题优先记忆交织三遍法。

## 变种一：复制任意有向图

若每个节点有任意邻接表，无法交织到单一 `next` 链。用 BFS 加地址映射，在发现新节点时创建副本。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  vector<Node*> neighbors;
  explicit Node(int value) : value(value) {
  }
};
Node* cloneGraph(Node* start) {
  if (!start) {
    return nullptr;
  }
  unordered_map<Node*, Node*> clone{{start, new Node(start->value)}};
  queue<Node*> queue;
  queue.push(start);
  while (!queue.empty()) {
    Node* node = queue.front();
    queue.pop();
    for (Node* neighbor : node->neighbors) {
      if (!clone.contains(neighbor)) {
        clone[neighbor] = new Node(neighbor->value);
        queue.push(neighbor);
      }
      clone[node]->neighbors.push_back(clone[neighbor]);
    }
  }
  return clone[start];
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<Node*> nodes;
  for (int i = 0; i < n; ++i) {
    nodes.push_back(new Node(i));
  }
  while (m--) {
    int from, to;
    cin >> from >> to;
    nodes[from]->neighbors.push_back(nodes[to]);
  }
  Node* copy = cloneGraph(n ? nodes[0] : nullptr);
  cout << (copy ? copy->value : -1) << '\n';
}
```

时间与空间均为 $O(V+E)$。

## 变种二：序列化为 `[value, random_index]`

新定义：不克隆对象，只输出平台所用的索引表示。先给 `next` 链节点编号，再把随机指针映射为下标。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next = nullptr;
  Node* random = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  vector<int> randomIndex(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value >> randomIndex[i];
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  for (int i = 0; i < n; ++i) {
    nodes[i].random = randomIndex[i] < 0 ? nullptr : &nodes[randomIndex[i]];
  }
  unordered_map<Node*, int> index;
  for (int i = 0; i < n; ++i) {
    index[&nodes[i]] = i;
  }
  for (Node* node = n ? &nodes[0] : nullptr; node; node = node->next) {
    cout << node->value << ' ' << (node->random ? index[node->random] : -1) << '\n';
  }
}
```

时间 $O(n)$，映射空间 $O(n)$。

## 变种三：每个节点有两条随机指针

交织身份技巧仍成立；第二遍同时映射 `randomA` 与 `randomB`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next = nullptr;
  Node* randomA = nullptr;
  Node* randomB = nullptr;
  explicit Node(int value) : value(value) {
  }
};
Node* cloneList(Node* head) {
  if (!head) {
    return nullptr;
  }
  for (Node* node = head; node; node = node->next->next) {
    Node* copy = new Node(node->value);
    copy->next = node->next;
    node->next = copy;
  }
  for (Node* node = head; node; node = node->next->next) {
    node->next->randomA = node->randomA ? node->randomA->next : nullptr;
    node->next->randomB = node->randomB ? node->randomB->next : nullptr;
  }
  Node* answer = head->next;
  for (Node* node = head; node;) {
    Node* copy = node->next;
    Node* next = copy->next;
    node->next = next;
    copy->next = next ? next->next : nullptr;
    node = next;
  }
  return answer;
}
int main() {
  Node* node = new Node(1);
  node->randomA = node;
  cout << cloneList(node)->value << '\n';
}
```

时间 $O(n)$，辅助空间 $O(1)$。随机边条数固定为常数时，交织法可直接扩展。

## 变种四：`next` 与 `random` 都可能走出主链形成一般可达图

原题保证所有随机目标在 `next` 主链上；取消该保证后，交织法无法为链外节点建立身份。把两种指针都视为图边并做 BFS 克隆。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next = nullptr;
  Node* random = nullptr;
  explicit Node(int value) : value(value) {
  }
};
Node* cloneReachable(Node* start) {
  if (!start) {
    return nullptr;
  }
  unordered_map<Node*, Node*> clone{{start, new Node(start->value)}};
  queue<Node*> queue;
  queue.push(start);
  while (!queue.empty()) {
    Node* node = queue.front();
    queue.pop();
    for (Node* target : {node->next, node->random}) {
      if (target && !clone.contains(target)) {
        clone[target] = new Node(target->value);
        queue.push(target);
      }
    }
    clone[node]->next = node->next ? clone[node->next] : nullptr;
    clone[node]->random = node->random ? clone[node->random] : nullptr;
  }
  return clone[start];
}
int main() {
  Node* first = new Node(1);
  Node* second = new Node(2);
  first->random = second;
  second->next = first;
  cout << cloneReachable(first)->random->value << '\n';
}
```

时间与空间均为 $O(V+E)$，并能处理环。

## 可复现验证

随机生成长度 0 到 200 的链和随机下标，分别用哈希法与交织法复制；按原节点索引检查值、`next`、`random` 关系，同时断言两组节点地址集合不相交，并确认原链拆分后逐指针恢复。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/copy-list-with-random-pointer/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/copy-list-with-random-pointer/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-68-lc994/">← [力扣 Top 68] LC 994 腐烂的橘子 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-70-lc102/">[力扣 Top 70] LC 102 二叉树的层序遍历 中等 →</a>
</nav>
