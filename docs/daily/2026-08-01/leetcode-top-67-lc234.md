---
title: "[力扣 Top 67] LC 234 回文链表 简单"
---

# [力扣 Top 67] LC 234 回文链表 简单

<p class="daily-archive-kicker">2026-08-01 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c32e4f0254aa84bd86033aad166fa33c3f19bd9e114f1fd0d3b7024e74dab0bf -->
## 官方原始信息

- Top 排名：67
- 题号：LC 234
- 官方中文标题：回文链表
- 官方难度：简单
- 官方链接：[回文链表](https://leetcode.cn/problems/palindrome-linked-list/)

### 原始题意

给定单链表头节点 `head`，判断从头到尾的节点值序列是否为回文。进阶要求 $O(n)$ 时间与 $O(1)$ 额外空间。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  bool isPalindrome(ListNode* head);
};
```

### 全部官方样例

```text
输入：head = [1,2,2,1]
输出：true
```

```text
输入：head = [1,2]
输出：false
```

### 全部约束

- 节点数 $1\le n\le10^5$。
- $0\le Node.val\le9$。

## 约束推导与边界

单链表不能从尾向前访问，直接双端比较需要把值复制到数组，额外空间 $O(n)$。若要常数空间，可以用快慢指针找到后半段起点，把后半段原地反转后与前半段逐项比较，最后再反转一次恢复输入结构。

奇数长度的中间节点无需比较；让 `fast` 每次走两步、`slow` 每次一步，循环结束时 `slow` 正好指向后半段起点：偶数长度为右半首项，奇数长度为中点后的首项。

## 解法递进

### 解法一：复制值到数组

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
};
class Solution {
public:
  bool isPalindrome(ListNode* head) {
    vector<int> values;
    for (ListNode* node = head; node; node = node->next) {
      values.push_back(node->val);
    }
    return equal(values.begin(), values.begin() + values.size() / 2, values.rbegin());
  }
};
```

时间 $O(n)$，空间 $O(n)$。它最简单且不会修改链表。

### 最佳实用解：反转后半段、比较并恢复

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
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
  bool isPalindrome(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast->next && fast->next->next) {
      slow = slow->next;
      fast = fast->next->next;
    }
    ListNode* reversed = reverseList(slow->next);
    ListNode* first = head;
    ListNode* second = reversed;
    bool answer = true;
    while (second) {
      if (first->val != second->val) {
        answer = false;
        break;
      }
      first = first->next;
      second = second->next;
    }
    slow->next = reverseList(reversed);
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$，并在返回前恢复原链表。

### 同阶时间方案：递归回程比较

递归先走到尾部，回程时用一个前向指针从头移动。代码短，但调用栈为 $O(n)$，在 $10^5$ 节点时有栈溢出风险。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
};
class Solution {
  ListNode* front;
  bool compare(ListNode* node) {
    if (!node) {
      return true;
    }
    if (!compare(node->next) || front->val != node->val) {
      return false;
    }
    front = front->next;
    return true;
  }
public:
  bool isPalindrome(ListNode* head) {
    front = head;
    return compare(head);
  }
};
```

## 正确性证明

快慢指针结束后，`slow->next` 开始的节点数等于需要与前半段比较的节点数。反转该后半段后，其遍历顺序等于原链表从尾向中间的顺序。于是同步前进 `first` 与 `second`，比较的正是第 1 个与倒数第 1 个、第 2 个与倒数第 2 个，直至全部成对位置。

全部相等当且仅当原值序列为回文。最后再次反转同一段并接回 `slow`，反转是自身的逆操作，因此链表结构完全恢复，不影响结论。

## 样例手推

`1→2→2→1` 中，快慢指针令 `slow` 停在第一个 2；后半段 `2→1` 反转为 `1→2`。与头部依次比较得到 `1=1`、`2=2`，返回真，再把后半段恢复。奇数链 `1→2→1` 中 `slow` 停在中间 2，只反转最后一个节点，中点自然跳过。

## 易错点与方案比较

- 快指针循环条件要先检查 `fast->next` 再检查 `fast->next->next`。
- 比较长度以后半段为准，奇数长度无需比较中点。
- 若接口调用者可能复用输入链表，应在返回前恢复；不能因提前发现不等就漏掉恢复。
- 数组法最稳且适合只读输入；进阶条件下推荐“找中点—反转后半—比较—恢复”四步模板。

## 变种一：输入链表严格只读

不能改 `next`，使用显式值数组完成双端比较。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  vector<int> values;
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  for (const Node* node = n ? &nodes[0] : nullptr; node; node = node->next) {
    values.push_back(node->value);
  }
  bool answer = equal(values.begin(), values.begin() + values.size() / 2, values.rbegin());
  cout << (answer ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种二：双向链表

若节点同时有 `prev` 与 `next`，可从两端向中间比较，不需要复制或反转。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* previous = nullptr;
  Node* next = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].previous = i ? &nodes[i - 1] : nullptr;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  Node* left = n ? &nodes[0] : nullptr;
  Node* right = n ? &nodes[n - 1] : nullptr;
  bool answer = true;
  while (left && right && left != right && left->previous != right) {
    if (left->value != right->value) {
      answer = false;
      break;
    }
    left = left->next;
    right = right->previous;
  }
  cout << (answer ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，额外空间 $O(1)$。

## 变种三：允许删除至多一个节点后成为回文

单链表上分叉尝试很难恢复状态；先转数组，在首次不等时分别跳过左端或右端之一。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
bool palindrome(const vector<int>& values, int left, int right) {
  while (left < right) {
    if (values[left++] != values[right--]) {
      return false;
    }
  }
  return true;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> values(n);
  for (int& value : values) {
    cin >> value;
  }
  int left = 0;
  int right = n - 1;
  while (left < right && values[left] == values[right]) {
    ++left;
    --right;
  }
  bool answer =
      left >= right || palindrome(values, left + 1, right) || palindrome(values, left, right - 1);
  cout << (answer ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。若输入本来就是数组，额外空间为 $O(1)$。

## 变种四：链表可能含环

回文要求有限序列；先用 Floyd 算法检测环，有环则报告 `CYCLE`，无环再正常判断。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  Node* next = nullptr;
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, cycleEntry;
  cin >> n >> cycleEntry;
  vector<Node> nodes(n);
  for (int i = 0; i < n; ++i) {
    cin >> nodes[i].value;
    nodes[i].next = i + 1 < n ? &nodes[i + 1] : nullptr;
  }
  if (n && cycleEntry >= 0) {
    nodes.back().next = &nodes[cycleEntry];
  }
  Node* head = n ? &nodes[0] : nullptr;
  Node* slow = head;
  Node* fast = head;
  do {
    slow = slow ? slow->next : nullptr;
    fast = fast && fast->next ? fast->next->next : nullptr;
  } while (slow && fast && slow != fast);
  if (slow && fast) {
    cout << "CYCLE\n";
    return 0;
  }
  vector<int> values;
  for (Node* node = head; node; node = node->next) {
    values.push_back(node->value);
  }
  bool answer = equal(values.begin(), values.begin() + values.size() / 2, values.rbegin());
  cout << (answer ? "YES" : "NO") << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；环检测本身只用 $O(1)$ 空间。

## 可复现验证

随机生成长度 1 到 200 的值序列并转成链表，把原地方案与数组双端比较对拍；调用前后重新遍历节点地址与 `next`，确认结构逐项恢复。覆盖奇偶长度、单节点、全相同与首尾附近失配。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/palindrome-linked-list/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/palindrome-linked-list/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-66-lc23/">← [力扣 Top 66] LC 23 合并 K 个升序链表 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-68-lc994/">[力扣 Top 68] LC 994 腐烂的橘子 中等 →</a>
</nav>
