---
title: "[力扣 Top 23] LC 21 合并两个有序链表 简单"
---

# [力扣 Top 23] LC 21 合并两个有序链表 简单

<p class="daily-archive-kicker">2026-07-28 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

## 官方原始信息

- 难度：LeetCode 官方「简单」；非竞赛题，无官方分值与 ZeroTracer 竞赛分。
- 官方链接：[打开官方页面](https://leetcode.cn/problems/merge-two-sorted-lists/)
- slug：`merge-two-sorted-lists`
- 函数签名：`ListNode* mergeTwoLists(ListNode* list1, ListNode* list2)`
- 题意：复用两条非递减单链表的全部节点，拼接为一条非递减链表。
- 示例：`[1,2,4] + [1,3,4] -> [1,1,2,3,4,4]`；`[] + [] -> []`；`[] + [0] -> [0]`。
- 官方示意图：[打开来源页面](https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg)。
- 约束：每条链节点数 $0\ldots50$；$-100\le\text{Node.val}\le100$；两链均非递减。

## 约束、样例与边界

答案必须包含 $m+n$ 个节点，所以时间下界为 $\Omega(m+n)$。空链可直接返回另一链；相等值必须保留两次。选择 `<=` 时优先取 `list1` 可提供稳定的来源顺序。输入题面默认两链不共享节点；若可能共享后缀，需要额外防重。

## 暴力：复制数值、排序并新建链表

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* mergeTwoLists(ListNode* a, ListNode* b) {
    vector<int> values;
    for (; a; a = a->next) values.push_back(a->val);
    for (; b; b = b->next) values.push_back(b->val);
    sort(values.begin(), values.end());
    ListNode dummy;
    ListNode* tail = &dummy;
    for (int x : values) {
      tail->next = new ListNode(x);
      tail = tail->next;
    }
    return dummy.next;
  }
};
```

时间 $O((m+n)\log(m+n))$，新节点与数组空间 $O(m+n)$。它没有利用输入已有序，也违背“可直接复用原节点”的资源优势。

## 最优：双指针与哨兵尾指针

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (list1 && list2) {
      if (list1->val <= list2->val) {
        tail->next = list1;
        list1 = list1->next;
      } else {
        tail->next = list2;
        list2 = list2->next;
      }
      tail = tail->next;
    }
    tail->next = list1 ? list1 : list2;
    return dummy.next;
  }
};
```

循环不变量：`dummy.next...tail` 是两条已消费前缀中全部节点组成的非递减答案，且 `list1`、`list2` 指向各自未消费后缀。两头较小值是全体未处理节点中的最小值，接入后不可能破坏顺序。任一链耗尽时，另一有序后缀可整体连接。时间 $O(m+n)$，空间 $O(1)$。

样例前四次选择依次为 `1(list1),1(list2),2,3`，随后接上 `[4,4]`。优先记忆哨兵迭代版：没有单独处理答案头的分支，空间也优于递归。

## Follow-up 1：递归合并

较小头节点的后继应是两个剩余后缀的递归合并结果。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* mergeTwoLists(ListNode* a, ListNode* b) {
    if (!a) return b;
    if (!b) return a;
    if (a->val <= b->val) {
      a->next = mergeTwoLists(a->next, b);
      return a;
    }
    b->next = mergeTwoLists(a, b->next);
    return b;
  }
};
```

时间 $O(m+n)$，递归空间 $O(m+n)$。

## Follow-up 2：合并 $k$ 条有序链表

两个头的比较扩展为从 $k$ 个当前头中取最小值；小根堆避免每轮扫描全部链。对应 LC 23。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
class Solution {
public:
  ListNode* mergeKLists(vector<ListNode*>& lists) {
    auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> q(cmp);
    for (ListNode* head : lists) if (head) q.push(head);
    ListNode dummy;
    ListNode* tail = &dummy;
    while (!q.empty()) {
      ListNode* node = q.top();
      q.pop();
      if (node->next) q.push(node->next);
      tail->next = node;
      tail = node;
    }
    return dummy.next;
  }
};
```

设总节点数为 $N$，时间 $O(N\log k)$，堆空间 $O(k)$。

## Follow-up 3：禁止修改输入链表

原地接节点失效；比较逻辑不变，但每次复制较小值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
ListNode* mergedCopy(const ListNode* a, const ListNode* b) {
  ListNode dummy;
  ListNode* tail = &dummy;
  while (a || b) {
    if (!b || (a && a->val <= b->val)) {
      tail->next = new ListNode(a->val);
      a = a->next;
    } else {
      tail->next = new ListNode(b->val);
      b = b->next;
    }
    tail = tail->next;
  }
  return dummy.next;
}
```

时间 $O(m+n)$，新节点空间 $O(m+n)$。

## Follow-up 4：合并后每个数值只保留一次

新目标不再保留重复出现；接入节点前比较答案尾值，并删除被跳过节点。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
ListNode* mergeUnique(ListNode* a, ListNode* b) {
  ListNode dummy;
  ListNode* tail = &dummy;
  while (a || b) {
    ListNode*& source = (!b || (a && a->val <= b->val)) ? a : b;
    ListNode* node = source;
    source = source->next;
    if (tail != &dummy && tail->val == node->val) {
      delete node;
    } else {
      tail->next = node;
      tail = node;
    }
  }
  tail->next = nullptr;
  return dummy.next;
}
```

时间 $O(m+n)$，空间 $O(1)$；该版本取得输入节点所有权。

## Follow-up 5：两条输入可能共享物理后缀

普通算法会把同一节点接入两次并可能成环。先找交点；只合并交点之前的两个前缀，最后把公共后缀接一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};
ListNode* mergeWithSharedSuffix(ListNode* a, ListNode* b) {
  unordered_set<ListNode*> seen;
  for (ListNode* p = a; p; p = p->next) seen.insert(p);
  ListNode* common = b;
  while (common && !seen.count(common)) common = common->next;
  ListNode dummy;
  ListNode* tail = &dummy;
  while (a != common || b != common) {
    if (b == common || (a != common && a->val <= b->val)) {
      tail->next = a;
      a = a->next;
    } else {
      tail->next = b;
      b = b->next;
    }
    tail = tail->next;
  }
  tail->next = common;
  return dummy.next;
}
```

时间 $O(m+n)$，用于识别共享节点的额外空间 $O(m)$；若先用双指针求交点，可把空间降为 $O(1)$。

## 易错点与验证

- 接入节点后先推进来源指针，再推进 `tail`。
- 剩余后缀可整体接上，不必逐个复制。
- 相等值不能误去重；稳定需求决定使用 `<` 还是 `<=`。
- 随机验证：生成两组有序数组转链表，合并后与拼接排序的向量 oracle 比较；同时检查输出节点数、非递减性和节点地址不重不漏。

## Reference

- [官方题目](https://leetcode.cn/problems/merge-two-sorted-lists/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-22-lc206/">← [力扣 Top 22] LC 206 反转链表 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-24-lc283/">[力扣 Top 24] LC 283 移动零 简单 →</a>
</nav>
