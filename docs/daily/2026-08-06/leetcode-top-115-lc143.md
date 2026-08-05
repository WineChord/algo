---
title: "[力扣 Top 115] LC 143 重排链表 中等"
---

# [力扣 Top 115] LC 143 重排链表 中等

<p class="daily-archive-kicker">2026-08-06 · 第 6/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a572633b49d052c5a1ee42c392ba77b8f1a2c30672e4a7d9b26bdb75c6067894 -->
## 官方原始信息

- Top 排名：115
- 题号：LC 143
- 官方中文标题：重排链表
- 官方难度：中等
- 官方链接：[重排链表](https://leetcode.cn/problems/reorder-list/)

### 原始题意、签名、样例与约束

把 $L_0\to L_1\to\cdots\to L_n$ 原地重排为 $L_0\to L_n\to L_1\to L_{n-1}\to\cdots$，必须改变节点连接，不能只交换值。

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  void reorderList(ListNode* head);
};
```

```text
输入：[1,2,3,4]  输出：[1,4,2,3]
输入：[1,2,3,4,5]  输出：[1,5,2,4,3]
```

- $1\le$ 链表长度 $\le5\times10^4$。
- $1\le Node.val\le1000$。

## 约束推导与观察

目标顺序交替取原链表左端和右端。数组保存所有节点可直接双指针重连，但需 $O(n)$ 空间。常数空间方案分三步：快慢指针切成两半、反转后半段、交替合并。每一步都只改 `next`。

## 解法递进

### 解法一：节点数组

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
  void reorderList(ListNode* head) {
    vector<ListNode*> nodes;
    for (ListNode* p = head; p; p = p->next) {
      nodes.push_back(p);
    }
    int left = 0;
    int right = nodes.size() - 1;
    while (left < right) {
      nodes[left++]->next = nodes[right];
      if (left == right) {
        break;
      }
      nodes[right--]->next = nodes[left];
    }
    nodes[left]->next = nullptr;
  }
};
```

时间 $O(n)$，空间 $O(n)$，最适合作为结构 oracle。

### 最佳实用解：切分、反转、拉链合并

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
class Solution {
  ListNode* reverseList(ListNode* head) {
    ListNode* previous = nullptr;
    while (head) {
      ListNode* next = head->next;
      head->next = previous;
      previous = head;
      head = next;
    }
    return previous;
  }
public:
  void reorderList(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast->next && fast->next->next) {
      slow = slow->next;
      fast = fast->next->next;
    }
    ListNode* second = reverseList(slow->next);
    slow->next = nullptr;
    ListNode* first = head;
    while (second) {
      ListNode* nextFirst = first->next;
      ListNode* nextSecond = second->next;
      first->next = second;
      second->next = nextFirst;
      first = nextFirst;
      second = nextSecond;
    }
  }
};
```

时间 $O(n)$，空间 $O(1)$，是面试优先记忆方案。

## 正确性证明

切分后第一段依次为 $L_0,L_1,\ldots$，后半段反转后依次为 $L_n,L_{n-1},\ldots$。合并循环每轮从两段各取一个头节点，按“前段一个、后段一个”追加，恰生成目标前缀；两段内部相对顺序保持不变。后半段长度不超过前半段，循环结束后剩余至多一个前段节点，且切分时已保证尾指针为空，因此结果完整且无环。

## 样例手推

`1→2→3→4→5` 切为 `1→2→3` 和 `4→5`，反转后段得 `5→4`，交替合并得到 `1→5→2→4→3`。长度 1、2 时后半段为空或只有一个节点，同一代码自然成立。

## 易错点与方案比较

- 必须先令 `slow->next=nullptr`，否则合并后可能成环。
- 合并前要保存两条旧 `next`，不能改完再取。
- 中点选择应让第一段长度不小于第二段。
- 数组法最直观；三阶段链表法空间最优且每层不递归。

## 变种一：返回新数组而不修改链表

新定义：链表只读，返回目标值序列。双端读取节点值即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
vector<int> reorderedValues(ListNode* head) {
  vector<int> values;
  for (; head; head = head->next) {
    values.push_back(head->val);
  }
  vector<int> answer;
  int left = 0;
  int right = values.size() - 1;
  while (left <= right) {
    answer.push_back(values[left++]);
    if (left <= right) {
      answer.push_back(values[right--]);
    }
  }
  return answer;
}
int main() {
  cout << reorderedValues(nullptr).size() << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种二：按 `L0,Ln,Ln-1,L1,...` 的四步模式重排

新定义：按给定索引模式输出节点值。索引访问不再对应简单拉链，数组模型更合适。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  vector<int> answer;
  int left = 0;
  int right = n - 1;
  while (left <= right) {
    answer.push_back(a[left++]);
    if (left <= right) {
      answer.push_back(a[right--]);
    }
    if (left <= right) {
      answer.push_back(a[right--]);
    }
    if (left <= right) {
      answer.push_back(a[left++]);
    }
  }
  for (int i = 0; i < n; ++i) {
    cout << answer[i] << " \n"[i + 1 == n];
  }
}
```

时间、空间均为 $O(n)$。

## 变种三：双向链表原地交替取首尾

双向链表能直接找到尾部；每次摘下尾节点插到当前左节点之后。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int val;
  Node* prev;
  Node* next;
};
void reorder(Node* head) {
  if (!head) {
    return;
  }
  Node* tail = head;
  while (tail->next) {
    tail = tail->next;
  }
  Node* left = head;
  while (left != tail && left->next != tail) {
    Node* nextLeft = left->next;
    Node* oldTail = tail;
    tail = tail->prev;
    tail->next = nullptr;
    oldTail->prev = left;
    oldTail->next = nextLeft;
    left->next = oldTail;
    nextLeft->prev = oldTail;
    left = nextLeft;
  }
}
int main() {
  reorder(nullptr);
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种四：恢复原顺序

新定义：已知链表正是本题重排结果，恢复原链表。把奇数位和偶数位拆成两链，再反转偶数位并接回。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
};
ListNode* reverseList(ListNode* head) {
  ListNode* previous = nullptr;
  while (head) {
    ListNode* next = head->next;
    head->next = previous;
    previous = head;
    head = next;
  }
  return previous;
}
void restore(ListNode* head) {
  if (!head || !head->next) {
    return;
  }
  ListNode* first = head;
  ListNode* secondHead = head->next;
  ListNode* second = secondHead;
  while (second && second->next) {
    first->next = second->next;
    first = first->next;
    second->next = first->next;
    second = second->next;
  }
  first->next = reverseList(secondHead);
}
int main() {
  restore(nullptr);
}
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

枚举长度 `1..100` 的随机值链表，以节点数组构造的目标地址序列为 oracle；检查最优解地址顺序、节点数守恒、尾指针为空且无环，再执行恢复变种核对原地址序列。所有代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/reorder-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-114-lc142/">← [力扣 Top 114] LC 142 环形链表 II 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-116-lc203/">[力扣 Top 116] LC 203 移除链表元素 简单 →</a>
</nav>
