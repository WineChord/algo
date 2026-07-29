---
title: "[力扣 Top 28] LC 25 K 个一组翻转链表 困难"
---

# [力扣 Top 28] LC 25 K 个一组翻转链表 困难

<p class="daily-archive-kicker">2026-07-28 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-28 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

## 官方原始信息

- 官方链接：[打开官方页面](https://leetcode.cn/problems/reverse-nodes-in-k-group/)
- slug：`reverse-nodes-in-k-group`
- 官方难度：困难；官方竞赛分未提供；ZeroTracer 数据集无记录。
- 函数签名：`ListNode* reverseKGroup(ListNode* head, int k)`
- 题意：从头开始，每 `k` 个节点为一组反转；末尾不足 `k` 个节点保持原顺序。必须重连节点，不能只交换节点值。
- 样例 1：`[1,2,3,4,5], k=2` 输出 `[2,1,4,3,5]`。
- 样例 2：`[1,2,3,4,5], k=3` 输出 `[3,2,1,4,5]`。
- 约束：$1\le k\le n\le5000$，$0\le Node.val\le1000$。

链表节点数不大，但进阶要求 $O(1)$ 额外空间。真正困难之处是同时保存当前组前驱、组尾之后入口及反转后的新头/新尾，避免断链。

## 解法一：收集节点再重连

先把节点指针存入数组。完整组按逆序接回，不足 `k` 的后缀按原序接回。这是正确基线，并未交换节点值。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseKGroup(ListNode* head, int k) {
    vector<ListNode*> nodes;
    for (ListNode* cur = head; cur; cur = cur->next) nodes.push_back(cur);
    ListNode dummy;
    ListNode* tail = &dummy;
    int n = nodes.size();
    for (int start = 0; start < n; start += k) {
      if (start + k <= n) {
        for (int i = start + k - 1; i >= start; --i) {
          tail->next = nodes[i];
          tail = tail->next;
        }
      } else {
        for (int i = start; i < n; ++i) {
          tail->next = nodes[i];
          tail = tail->next;
        }
      }
    }
    tail->next = nullptr;
    return dummy.next;
  }
};
```

时间 $O(n)$，额外空间 $O(n)$。

## 解法二：递归分组

先确认当前段至少有 `k` 个节点，再反转半开区间 `[head,nextGroup)`，递归处理后缀。代码短，但递归深度 $O(n/k)$，不满足严格 $O(1)$ 额外空间。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode* nextGroup = head;
    for (int i = 0; i < k; ++i) {
      if (!nextGroup) return head;
      nextGroup = nextGroup->next;
    }
    ListNode* prev = reverseKGroup(nextGroup, k);
    ListNode* cur = head;
    while (cur != nextGroup) {
      ListNode* next = cur->next;
      cur->next = prev;
      prev = cur;
      cur = next;
    }
    return prev;
  }
};
```

时间 $O(n)$，递归栈 $O(n/k)$。

## 最佳实用解：哨兵 + 原地分组反转

`groupPrev` 指向待处理组的前驱：

1. 从 `groupPrev` 向后走 `k` 步找到 `kth`；不存在则剩余不足一组，结束。
2. 保存 `groupNext=kth->next`。
3. 令 `prev=groupNext`，反转 `[groupPrev->next,groupNext)`；这样旧组头自然连接到下一组。
4. `groupPrev->next=kth` 接上新组头，再把 `groupPrev` 推进到旧组头（即新组尾）。

循环不变量：`dummy.next` 到 `groupPrev` 的前缀已经按规则完成且连接正确；`groupPrev->next` 是尚未处理后缀。每轮只改当前完整组内部指针和两条边界连接，因此已完成前缀与未处理后缀均不丢失。终止时后缀少于 `k`，按题意保持原样。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    while (true) {
      ListNode* kth = groupPrev;
      for (int i = 0; i < k && kth; ++i) kth = kth->next;
      if (!kth) break;
      ListNode* groupNext = kth->next;
      ListNode* prev = groupNext;
      ListNode* cur = groupPrev->next;
      while (cur != groupNext) {
        ListNode* next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
      }
      ListNode* oldHead = groupPrev->next;
      groupPrev->next = kth;
      groupPrev = oldHead;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。优先记忆此解：边界清楚、无栈风险，并可直接迁移到任意分组重排。

样例 `k=2`：哨兵后的首组 `[1,2]` 变成 `[2,1]`，`groupPrev` 移到节点 `1`；第二组 `[3,4]` 变成 `[4,3]`；剩余节点 `5` 不足一组而停止。

边界：`k=1` 指针会原样重连；`k=n` 全链反转；`n%k!=0` 的尾段不动。常见错误：未先保存 `groupNext`；反转循环写成 `cur!=kth` 而漏掉 `kth`；推进到新组头造成重复处理；把“不改节点值”误解成不能改 `next`；遗漏哨兵导致首组难接。

## Follow-up 1：只反转位置 `[left,right]`

新定义：仅反转一个连续区间。仍用哨兵定位区间前驱，再做头插法；分组检查不再需要。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int i = 1; i < left; ++i) before = before->next;
    ListNode* tail = before->next;
    for (int i = left; i < right; ++i) {
      ListNode* moved = tail->next;
      tail->next = moved->next;
      moved->next = before->next;
      before->next = moved;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 2：组大小由数组给出

新定义：依次按 `groups[i]` 个节点分组；完整组反转，不完整的最后请求及剩余链表保持原序。固定 `k` 的推进逻辑仍成立，只需每轮读取不同长度。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseVariableGroups(ListNode* head, vector<int>& groups) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    for (int length : groups) {
      ListNode* last = groupPrev;
      for (int i = 0; i < length && last; ++i) last = last->next;
      if (!last) break;
      ListNode* groupNext = last->next;
      ListNode* prev = groupNext;
      ListNode* cur = groupPrev->next;
      while (cur != groupNext) {
        ListNode* next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
      }
      ListNode* oldHead = groupPrev->next;
      groupPrev->next = last;
      groupPrev = oldHead;
    }
    return dummy.next;
  }
};
```

设实际处理节点总数为 $m$，时间 $O(m)$，空间 $O(1)$。

## Follow-up 3：只反转第 1、3、5… 个完整 `k` 组

新定义：奇数组反转、偶数组保持原样；不足 `k` 的尾段保持原样。偶数组只推进指针，奇数组复用原地反转。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseAlternatingGroups(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    bool reverse = true;
    while (true) {
      ListNode* last = before;
      for (int i = 0; i < k && last; ++i) last = last->next;
      if (!last) break;
      if (!reverse) {
        before = last;
      } else {
        ListNode* after = last->next;
        ListNode* prev = after;
        ListNode* cur = before->next;
        while (cur != after) {
          ListNode* next = cur->next;
          cur->next = prev;
          prev = cur;
          cur = next;
        }
        ListNode* oldHead = before->next;
        before->next = last;
        before = oldHead;
      }
      reverse = !reverse;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## Follow-up 4：组长依次为 1,2,3,…，只反转实际长度为偶数的组

新定义对应 LC 2074。末组可以不足计划长度，但按其实际长度奇偶决定。必须先数出实际组长，再决定是否反转。

<!-- compile:leetcode-list -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  ListNode* reverseEvenLengthGroups(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int expected = 1; before->next; ++expected) {
      ListNode* last = before;
      int actual = 0;
      while (actual < expected && last->next) {
        last = last->next;
        ++actual;
      }
      if (actual % 2 == 1) {
        before = last;
        continue;
      }
      ListNode* after = last->next;
      ListNode* prev = after;
      ListNode* cur = before->next;
      while (cur != after) {
        ListNode* next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
      }
      ListNode* oldHead = before->next;
      before->next = last;
      before = oldHead;
    }
    return dummy.next;
  }
};
```

时间 $O(n)$，空间 $O(1)$。

## 可复现验证

用数组构造链表，将最优解输出与“数组按完整 `k` 块反转”的 oracle 在随机 `n<=50`、`1<=k<=n` 上逐项比较；同时检查节点地址集合不变、无环、节点数不变。编译与对拍结果见 `validation-report.json`。

## Reference

- [官方题目](https://leetcode.cn/problems/reverse-nodes-in-k-group/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-27-lc121/">← [力扣 Top 27] LC 121 买卖股票的最佳时机 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-29-lc704/">[力扣 Top 29] LC 704 二分查找 简单 →</a>
</nav>
