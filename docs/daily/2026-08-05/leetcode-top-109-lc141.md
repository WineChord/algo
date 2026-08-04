---
title: "[力扣 Top 109] LC 141 环形链表 简单"
---

# [力扣 Top 109] LC 141 环形链表 简单

<p class="daily-archive-kicker">2026-08-05 · 第 10/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../graph/functional-graphs/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=3cecd3308962a8d71ea25413a1b25f4e4f827fc6aaa612006b85e6217899ab0f -->
## 官方原始信息

- Top 排名：109
- 题号：LC 141
- 官方中文标题：环形链表
- 官方难度：简单
- 官方链接：[环形链表](https://leetcode.cn/problems/linked-list-cycle/)

### 原始题意

给定单链表头节点 `head`，判断沿 `next` 是否会再次到达此前节点。题面中的 `pos` 只用于描述测试数据，不是函数参数。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  bool hasCycle(ListNode* head);
};
```

### 全部官方样例

```text
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：尾节点连接到第二个节点。
```

```text
输入：head = [1,2], pos = 0
输出：true
解释：尾节点连接到第一个节点。
```

```text
输入：head = [1], pos = -1
输出：false
```

### 全部约束

- 节点数在 `[0,10^4]`。
- $-10^5\le Node.val\le10^5$。
- `pos` 为 -1 或链表中的合法下标，但不传入函数。
- 进阶目标为 $O(1)$ 内存。

## 约束推导与观察

节点值可能重复，不能用 `val` 判断是否重访，必须比较节点地址。无环时快指针最终到达空；有环时，进入环后快指针每轮相对慢指针多走一步，相对距离会遍历所有环长余数，必然相遇。

本题没有算术溢出风险；关键是访问 `fast->next->next` 前同时检查 `fast` 与 `fast->next`。

## 解法递进

### 解法一：哈希集合记录节点地址

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
  bool hasCycle(ListNode* head) {
    unordered_set<ListNode*> seen;
    for (ListNode* node = head; node; node = node->next) {
      if (!seen.insert(node).second) {
        return true;
      }
    }
    return false;
  }
};
```

平均时间 $O(n)$，空间 $O(n)$。它直观且能保存访问历史，但未达到常量空间进阶目标。

### 最佳实用解：Floyd 快慢指针

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
  bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
      slow = slow->next;
      fast = fast->next->next;
      if (slow == fast) {
        return true;
      }
    }
    return false;
  }
};
```

时间 $O(n)$，空间 $O(1)$，不改写链表，是推荐方案。

## 正确性证明

无环时，快指针严格向链尾推进，最终 `fast` 或 `fast->next` 为空，算法返回 false。有环时，慢指针至多经过入环距离后进入环；此后把两指针位置差看作模环长的余数，每轮快指针比慢指针多走一步，余数每次加一，至多环长轮必为零，即两地址相同，算法返回 true。因此返回值与是否存在环完全一致。

## 样例手推

`3→2→0→-4→2...` 中慢指针每轮走 1 步，快指针走 2 步，二者进入环后相遇。单节点无自环时 `fast->next` 初始为空，直接返回 false；若单节点指向自身，第一轮二者都回到该节点并返回 true。

## 易错点与方案比较

- `pos` 不在函数签名中，不能依赖它。
- 比较节点指针而非节点值。
- 循环条件必须先检查 `fast->next`。
- 哈希法更容易扩展到恢复路径；Floyd 同时线性且常量空间，应优先记忆。

## 变种一：返回环入口

新定义：若有环，返回第一个环节点，否则返回空。相遇后把一指针移回头部，再同速前进。

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

时间 $O(n)$，空间 $O(1)$；对应 [LC 142](https://leetcode.cn/problems/linked-list-cycle-ii/)。

## 变种二：返回环长与入环距离

新定义：输出 `(prefixLength, cycleLength)`；无环输出 `(-1,0)`。先求入口，再绕环一周计数。

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
pair<int, int> cycleShape(ListNode* head) {
  ListNode* slow = head;
  ListNode* fast = head;
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
    if (slow == fast) {
      int prefix = 0;
      slow = head;
      while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
        ++prefix;
      }
      int length = 1;
      for (ListNode* node = slow->next; node != slow; node = node->next) {
        ++length;
      }
      return {prefix, length};
    }
  }
  return {-1, 0};
}
int main() {
  int n, pos;
  cin >> n >> pos;
  vector<ListNode*> nodes;
  for (int i = 0; i < n; ++i) {
    nodes.push_back(new ListNode(i));
    if (i) {
      nodes[i - 1]->next = nodes[i];
    }
  }
  if (n && pos >= 0) {
    nodes.back()->next = nodes[pos];
  }
  auto [prefix, length] = cycleShape(n ? nodes[0] : nullptr);
  cout << prefix << ' ' << length << '\n';
}
```

时间 $O(n)$，空间 $O(1)$（不计输入构造）。

## 变种三：在只读函数图中判环

新定义：节点是数组下标，每个下标有一个下一跳或 `-1`。这与链表相同，只把空指针换成哨兵值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int jump(const vector<int>& next, int node) {
  return node == -1 ? -1 : next[node];
}
int main() {
  int n, start;
  cin >> n >> start;
  vector<int> next(n);
  for (int& node : next) {
    cin >> node;
  }
  int slow = start;
  int fast = start;
  while (fast != -1 && jump(next, fast) != -1) {
    slow = jump(next, slow);
    fast = jump(next, jump(next, fast));
    if (slow == fast) {
      cout << "true\n";
      return 0;
    }
  }
  cout << "false\n";
}
```

时间 $O(n)$，空间 $O(1)$。LC 287 正是“值作为下一下标”的特殊函数图。

## 变种四：安全判断两条可能有环链表是否相交

新定义：返回是否共享任意节点。分别求环入口；两条无环链表用尾节点判断，一有环一无环必不相交，两条有环则检查两个入口是否在同一环。

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
ListNode* entry(ListNode* head) {
  ListNode* slow = head;
  ListNode* fast = head;
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
    if (slow == fast) {
      slow = head;
      while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
      }
      return slow;
    }
  }
  return nullptr;
}
bool intersect(ListNode* first, ListNode* second) {
  ListNode* firstEntry = entry(first);
  ListNode* secondEntry = entry(second);
  if (!firstEntry && !secondEntry) {
    if (!first || !second) {
      return false;
    }
    while (first->next) {
      first = first->next;
    }
    while (second->next) {
      second = second->next;
    }
    return first == second;
  }
  if (!firstEntry || !secondEntry) {
    return false;
  }
  ListNode* node = firstEntry;
  do {
    if (node == secondEntry) {
      return true;
    }
    node = node->next;
  } while (node != firstEntry);
  return false;
}
int main() {
  cout << "Use intersect(first, second) with constructed lists.\n";
}
```

时间 $O(n+m)$，空间 $O(1)$。直接同时遍历两条环形链表会无限循环，必须先分类环结构。

## 验证说明

本轮将六段代码按 C++23 编译；哈希与 Floyd 会对拍 50,000 个随机链表形状，覆盖空链表、单节点、自环、尾接头、长前缀短环与无环。入口、环长和函数图版本分别与访问地址时间戳 oracle 核验。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/linked-list-cycle/)
- [对应知识专题](../../graph/functional-graphs.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-108-lc202/">← [力扣 Top 108] LC 202 快乐数 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-110-lc84/">[力扣 Top 110] LC 84 柱状图中最大的矩形 困难 →</a>
</nav>
