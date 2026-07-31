---
title: "[力扣 Top 66] LC 23 合并 K 个升序链表 困难"
---

# [力扣 Top 66] LC 23 合并 K 个升序链表 困难

<p class="daily-archive-kicker">2026-08-01 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../data-structures/linked-lists/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=68ca3d54c41f16df4766e6ef1e3cd7a12ea76219f8f02cfb1e93ce458c079215 -->
## 官方原始信息

- Top 排名：66
- 题号：LC 23
- 官方中文标题：合并 K 个升序链表
- 官方难度：困难
- 官方链接：[合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/)

### 原始题意

给定 $k$ 个分别按升序排列的单链表，合并为一个升序链表并返回头节点。

### 函数签名

<!-- compile:leetcode-list -->
```cpp
class Solution {
public:
  ListNode* mergeKLists(vector<ListNode*>& lists);
};
```

### 全部官方样例

```text
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
```

```text
输入：lists = []
输出：[]
```

```text
输入：lists = [[]]
输出：[]
```

### 全部约束

- $k=|lists|$，$0\le k\le10^4$。
- $0\le |lists_i|\le500$。
- 所有链表节点总数 $N\le10^4$。
- $-10^4\le value\le10^4$。
- 每个输入链表均按升序排列。

## 约束推导与边界

每次输出的下一个节点只能来自某条尚未耗尽链表的表头，因此候选最多 $k$ 个。线性扫描候选要 $O(k)$，最小堆可把选择降为 $O(\log k)$。弹出某节点后，仅需把它在原链表中的后继加入候选集，堆大小始终不超过非空链表数。

可以直接复用原节点，只改写 `next`，无需新建 $N$ 个节点。空列表数组、全部空链表和单条链表都由同一逻辑覆盖。节点值与比较均在 `int` 范围内。

## 解法递进

### 解法一：逐条合并

把当前结果与下一条链表用双指针合并。第 $i$ 次可能重新扫描前 $i$ 条链表的全部节点，极端不均衡时总成本为 $O(Nk)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
  ListNode() = default;
  explicit ListNode(int value) : val(value) {
  }
};
class Solution {
  ListNode* mergeTwo(ListNode* first, ListNode* second) {
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
  ListNode* mergeKLists(vector<ListNode*>& lists) {
    ListNode* answer = nullptr;
    for (ListNode* head : lists) {
      answer = mergeTwo(answer, head);
    }
    return answer;
  }
};
```

最坏时间 $O(Nk)$，合并过程额外空间 $O(1)$。

### 优化：分治两两合并

每轮把链表成对合并，链表总长度在每一层只被扫描一次，共有 $O(\log k)$ 层。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
  ListNode() = default;
  explicit ListNode(int value) : val(value) {
  }
};
class Solution {
  ListNode* mergeTwo(ListNode* first, ListNode* second) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (first && second) {
      ListNode*& chosen = first->val <= second->val ? first : second;
      tail->next = chosen;
      chosen = chosen->next;
      tail = tail->next;
    }
    tail->next = first ? first : second;
    return dummy.next;
  }
public:
  ListNode* mergeKLists(vector<ListNode*>& lists) {
    for (int interval = 1; interval < static_cast<int>(lists.size()); interval *= 2) {
      for (int i = 0; i + interval < static_cast<int>(lists.size()); i += 2 * interval) {
        lists[i] = mergeTwo(lists[i], lists[i + interval]);
      }
    }
    return lists.empty() ? nullptr : lists[0];
  }
};
```

时间 $O(N\log k)$，迭代实现额外空间 $O(1)$。

### 最佳实用解：最小堆维护当前表头

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct ListNode {
  int val = 0;
  ListNode* next = nullptr;
  ListNode() = default;
  explicit ListNode(int value) : val(value) {
  }
};
class Solution {
public:
  ListNode* mergeKLists(vector<ListNode*>& lists) {
    auto greaterNode = [](ListNode* left, ListNode* right) { return left->val > right->val; };
    priority_queue<ListNode*, vector<ListNode*>, decltype(greaterNode)> heap(greaterNode);
    for (ListNode* head : lists) {
      if (head) {
        heap.push(head);
      }
    }
    ListNode dummy;
    ListNode* tail = &dummy;
    while (!heap.empty()) {
      ListNode* node = heap.top();
      heap.pop();
      if (node->next) {
        heap.push(node->next);
      }
      tail->next = node;
      tail = node;
    }
    tail->next = nullptr;
    return dummy.next;
  }
};
```

时间 $O(N\log k)$，堆空间 $O(k)$。

## 正确性证明

堆始终恰好保存每条未耗尽链表的首个未输出节点。因为单条链表升序，其余节点都不小于该表头；所以所有未输出节点的全局最小值必在堆中，弹出的堆顶就是下一项。弹出后加入同链表后继，重新恢复不变量。

归纳每次选择，输出前缀始终是全部输入节点中最小的若干项并按非递减顺序排列。所有节点最终各入堆、出堆一次，结果既不遗漏也不重复。

## 样例手推

三个初始表头 1、1、2 入堆。依次弹出 1 后补入 4，弹出另一个 1 后补入 3，再弹出 2 后补入 6；之后候选为 3、4、6，最终得到 `1,1,2,3,4,4,5,6`。

$k=0$ 或所有表头为空时堆为空，返回空；$k=1$ 时节点按原顺序逐个弹出，链表内容不变。

## 易错点与方案比较

- `priority_queue` 默认是最大堆，比较器方向要反转。
- 只能把非空表头入堆。
- 复用节点时最后显式令尾节点 `next=nullptr`，避免将旧链意外保留。
- 分治与堆同为 $O(N\log k)$：分治额外空间更小、顺序访问缓存友好；堆适合链表长度高度不均、数据流式到达。面试优先记忆堆的不变量，同时知道分治是同阶备选。

## 变种一：合并 $k$ 个升序数组

数组不能通过指针后继推进，用 `(值,数组编号,下标)` 作为堆元素。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Entry {
  int value;
  int list;
  int index;
  bool operator>(const Entry& other) const {
    return tie(value, list, index) > tie(other.value, other.list, other.index);
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k;
  cin >> k;
  vector<vector<int>> lists(k);
  priority_queue<Entry, vector<Entry>, greater<Entry>> heap;
  for (int i = 0; i < k; ++i) {
    int length;
    cin >> length;
    lists[i].resize(length);
    for (int& value : lists[i]) {
      cin >> value;
    }
    if (length) {
      heap.push({lists[i][0], i, 0});
    }
  }
  vector<int> answer;
  while (!heap.empty()) {
    Entry current = heap.top();
    heap.pop();
    answer.push_back(current.value);
    if (++current.index < static_cast<int>(lists[current.list].size())) {
      current.value = lists[current.list][current.index];
      heap.push(current);
    }
  }
  for (int i = 0; i < static_cast<int>(answer.size()); ++i) {
    cout << answer[i] << (i + 1 == static_cast<int>(answer.size()) ? '\n' : ' ');
  }
}
```

时间 $O(N\log k)$，堆空间 $O(k)$，输出空间 $O(N)$。

## 变种二：只求全体节点中的第 $r$ 小值

无需构造完整链表；弹堆 $r$ 次后立即返回。若总节点不足 $r$，输出 `NONE`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using State = tuple<int, int, int>;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k, rank;
  cin >> k >> rank;
  vector<vector<int>> lists(k);
  priority_queue<State, vector<State>, greater<State>> heap;
  for (int i = 0; i < k; ++i) {
    int length;
    cin >> length;
    lists[i].resize(length);
    for (int& value : lists[i]) {
      cin >> value;
    }
    if (length) {
      heap.push({lists[i][0], i, 0});
    }
  }
  while (!heap.empty() && rank > 1) {
    auto [value, list, index] = heap.top();
    heap.pop();
    if (++index < static_cast<int>(lists[list].size())) {
      heap.push({lists[list][index], list, index});
    }
    --rank;
  }
  cout << (heap.empty() ? string("NONE") : to_string(get<0>(heap.top()))) << '\n';
}
```

时间 $O(r\log k)$，空间 $O(k)$。

## 变种三：按降序合并多条降序链

候选仍是每条链的表头，但现在每次取最大值，使用默认最大堆。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using State = tuple<int, int, int>;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k;
  cin >> k;
  vector<vector<int>> lists(k);
  priority_queue<State> heap;
  for (int i = 0; i < k; ++i) {
    int length;
    cin >> length;
    lists[i].resize(length);
    for (int& value : lists[i]) {
      cin >> value;
    }
    if (length) {
      heap.push({lists[i][0], i, 0});
    }
  }
  bool first = true;
  while (!heap.empty()) {
    auto [value, list, index] = heap.top();
    heap.pop();
    cout << (first ? "" : " ") << value;
    first = false;
    if (++index < static_cast<int>(lists[list].size())) {
      heap.push({lists[list][index], list, index});
    }
  }
  cout << '\n';
}
```

时间 $O(N\log k)$，空间 $O(k)$。

## 变种四：合并时输出游程频次

若下游只关心每个值出现次数，可在堆序列上在线聚合连续相等值，不保存长度为 $N$ 的结果。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
using State = tuple<int, int, int>;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int k;
  cin >> k;
  vector<vector<int>> lists(k);
  priority_queue<State, vector<State>, greater<State>> heap;
  for (int i = 0; i < k; ++i) {
    int length;
    cin >> length;
    lists[i].resize(length);
    for (int& value : lists[i]) {
      cin >> value;
    }
    if (length) {
      heap.push({lists[i][0], i, 0});
    }
  }
  bool has = false;
  int current = 0;
  long long count = 0;
  while (!heap.empty()) {
    auto [value, list, index] = heap.top();
    heap.pop();
    if (!has || value != current) {
      if (has) {
        cout << current << ' ' << count << '\n';
      }
      has = true;
      current = value;
      count = 0;
    }
    ++count;
    if (++index < static_cast<int>(lists[list].size())) {
      heap.push({lists[list][index], list, index});
    }
  }
  if (has) {
    cout << current << ' ' << count << '\n';
  }
}
```

时间 $O(N\log k)$，空间 $O(k)$，输出仅为不同值数量。

## 可复现验证

随机生成最多 12 条升序数组并转成链表，把逐条合并、分治和最小堆结果与“收集全部值后排序”比较；覆盖空列表、全部空链、重复值、负值和极不均衡长度。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/merge-k-sorted-lists/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/merge-k-sorted-lists/)
- [对应知识专题](../../data-structures/linked-lists.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-65-lc224/">← [力扣 Top 65] LC 224 基本计算器 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-67-lc234/">[力扣 Top 67] LC 234 回文链表 简单 →</a>
</nav>
