---
title: "[力扣 Top 112] LC 155 最小栈 中等"
---

# [力扣 Top 112] LC 155 最小栈 中等

<p class="daily-archive-kicker">2026-08-06 · 第 3/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../data-structures/augmented-stacks/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=bed301087303b8b6e860c3e0177e262736e0940aa15766136592994350a36ada -->
## 官方原始信息

- Top 排名：112
- 题号：LC 155
- 官方中文标题：最小栈
- 官方难度：中等
- 官方链接：[最小栈](https://leetcode.cn/problems/min-stack/)

### 原始题意与函数签名

设计栈 `MinStack`，支持 `push`、`pop`、`top`，并在常数时间返回当前最小值。`pop`、`top`、`getMin` 只会在非空栈上调用。

<!-- compile:leetcode -->
```cpp
class MinStack {
public:
  MinStack();
  void push(int val);
  void pop();
  int top();
  int getMin();
};
```

### 全部官方样例

```text
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
输出：[null,null,null,null,-3,null,0,-2]
```

### 全部约束

- $-2^{31}\le val\le2^{31}-1$。
- 四类操作合计最多调用 $3\times10^4$ 次。
- `pop`、`top`、`getMin` 调用时栈非空。

## 约束推导与观察

若只存普通栈，`getMin` 每次扫描需要 $O(n)$。关键是让每一层同时保存“压入该元素以后前缀的最小值”；弹栈时历史最小值随该层一起恢复。值可能覆盖完整 32 位，存差值编码时要使用 64 位。

## 解法递进

### 解法一：查询时扫描

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MinStack {
  vector<int> values;
public:
  MinStack() = default;
  void push(int val) {
    values.push_back(val);
  }
  void pop() {
    values.pop_back();
  }
  int top() {
    return values.back();
  }
  int getMin() {
    return *min_element(values.begin(), values.end());
  }
};
```

`push/pop/top` 为 $O(1)$，`getMin` 为 $O(n)$，空间 $O(n)$。

### 最佳实用解：每层保存值与前缀最小值

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MinStack {
  vector<pair<int, int>> data;
public:
  MinStack() = default;
  void push(int val) {
    int minimum = data.empty() ? val : min(val, data.back().second);
    data.push_back({val, minimum});
  }
  void pop() {
    data.pop_back();
  }
  int top() {
    return data.back().first;
  }
  int getMin() {
    return data.back().second;
  }
};
```

所有操作 $O(1)$，空间 $O(n)$。双栈也同阶，但成对存储让层级天然同步，最不容易漏弹，优先记忆。

### 同阶方案：单栈差值编码

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MinStack {
  vector<long long> differences;
  long long minimum = 0;
public:
  MinStack() = default;
  void push(int val) {
    if (differences.empty()) {
      differences.push_back(0);
      minimum = val;
      return;
    }
    differences.push_back(static_cast<long long>(val) - minimum);
    minimum = min(minimum, static_cast<long long>(val));
  }
  void pop() {
    long long difference = differences.back();
    differences.pop_back();
    if (difference < 0) {
      minimum -= difference;
    }
  }
  int top() {
    long long difference = differences.back();
    return static_cast<int>(difference > 0 ? minimum + difference : minimum);
  }
  int getMin() {
    return static_cast<int>(minimum);
  }
};
```

仍为 $O(1)$ 操作和 $O(n)$ 空间，只把每层两整数压为一个 64 位整数；证明与溢出负担更高。

## 正确性证明

对子栈长度归纳。空栈后首次压入 `(val,val)`，第二字段显然是当前最小值。假设栈顶第二字段是旧栈最小值，压入 `val` 后存入两者较小值，正是新栈最小值。弹出顶层后，下面一层记录的仍是弹入该层时的完整前缀最小值，因此历史状态被正确恢复。`top` 取第一字段，四个接口都正确。

## 样例手推

依次压入 `-2,0,-3`，记录为 `(-2,-2),(0,-2),(-3,-3)`，首次 `getMin` 返回 `-3`。弹出最后一层后顶层恢复为 `(0,-2)`，所以 `top=0` 且 `getMin=-2`。重复最小值如 `2,1,1` 也分别保存 `2,1,1`，弹出一个 `1` 后最小值仍是 `1`。

## 易错点与方案比较

- 辅助最小栈若只在严格变小时压入，会在重复最小值弹出时失步；应使用 `<=` 或保存计数。
- 差值可能超出 32 位，必须用 `long long`。
- 不要在 `pop` 后访问空栈；本题只保证调用前非空。
- 成对栈占两个整数但最稳定；差值编码省字段，不是复杂度升级。

## 变种一：同时返回最小值出现次数

新定义：增加 `countMin()`。栈顶保存当前最小值和出现次数，压入时按大小更新。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class CountMinStack {
  struct State {
    int value;
    int minimum;
    int count;
  };
  vector<State> data;
public:
  void push(int value) {
    if (data.empty()) {
      data.push_back({value, value, 1});
    } else if (value < data.back().minimum) {
      data.push_back({value, value, 1});
    } else {
      int count = data.back().count + (value == data.back().minimum);
      data.push_back({value, data.back().minimum, count});
    }
  }
  void pop() {
    data.pop_back();
  }
  int getMin() const {
    return data.back().minimum;
  }
  int countMin() const {
    return data.back().count;
  }
};
int main() {
  CountMinStack st;
  int q;
  cin >> q;
  while (q--) {
    string op;
    cin >> op;
    if (op == "push") {
      int x;
      cin >> x;
      st.push(x);
    } else if (op == "pop") {
      st.pop();
    } else {
      cout << st.getMin() << ' ' << st.countMin() << '\n';
    }
  }
}
```

每次操作 $O(1)$，空间 $O(n)$。

## 变种二：支持常数时间最小值的队列

新定义：队列支持 `push`、`pop`、`getMin`。用两个最小栈组成队列；需要出队时把输入栈倒入输出栈。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MinQueue {
  vector<pair<int, int>> input;
  vector<pair<int, int>> output;
  void add(vector<pair<int, int>>& st, int value) {
    int minimum = st.empty() ? value : min(value, st.back().second);
    st.push_back({value, minimum});
  }
  void transfer() {
    if (!output.empty()) {
      return;
    }
    while (!input.empty()) {
      int value = input.back().first;
      input.pop_back();
      add(output, value);
    }
  }
public:
  void push(int value) {
    add(input, value);
  }
  void pop() {
    transfer();
    output.pop_back();
  }
  int getMin() const {
    int answer = INT_MAX;
    if (!input.empty()) {
      answer = min(answer, input.back().second);
    }
    if (!output.empty()) {
      answer = min(answer, output.back().second);
    }
    return answer;
  }
};
int main() {
  MinQueue queue;
  int q;
  cin >> q;
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int x;
      cin >> x;
      queue.push(x);
    } else if (type == 2) {
      queue.pop();
    } else {
      cout << queue.getMin() << '\n';
    }
  }
}
```

每个元素最多进出两个栈，均摊时间 $O(1)$，空间 $O(n)$。

## 变种三：持久化最小栈

新定义：每次压栈或弹栈产生一个新版本，旧版本仍可查询。每个节点记录值、前缀最小值和父节点。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
struct Node {
  int value;
  int minimum;
  int parent;
};
int main() {
  int q;
  cin >> q;
  vector<Node> nodes(1, {0, INT_MAX, 0});
  vector<int> version(q + 1);
  for (int i = 1; i <= q; ++i) {
    int base, type;
    cin >> base >> type;
    int top = version[base];
    if (type == 1) {
      int x;
      cin >> x;
      nodes.push_back({x, min(x, nodes[top].minimum), top});
      version[i] = nodes.size() - 1;
    } else if (type == 2) {
      version[i] = nodes[top].parent;
    } else {
      version[i] = top;
      cout << nodes[top].minimum << '\n';
    }
  }
}
```

每次更新与查询 $O(1)$，总空间 $O(q)$。

## 变种四：同时维护最小值与最大值

新定义：增加 `getMax()`。每层同时记录前缀最小值和最大值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class MinMaxStack {
  struct State {
    int value;
    int minimum;
    int maximum;
  };
  vector<State> data;
public:
  void push(int value) {
    if (data.empty()) {
      data.push_back({value, value, value});
    } else {
      data.push_back({value, min(value, data.back().minimum), max(value, data.back().maximum)});
    }
  }
  void pop() {
    data.pop_back();
  }
  int top() const {
    return data.back().value;
  }
  int getMin() const {
    return data.back().minimum;
  }
  int getMax() const {
    return data.back().maximum;
  }
};
int main() {
  MinMaxStack st;
  st.push(3);
  st.push(1);
  st.push(5);
  cout << st.getMin() << ' ' << st.getMax() << '\n';
}
```

所有操作 $O(1)$，空间 $O(n)$。

## 可复现验证

随机生成合法操作序列，以 `vector<int>` 扫描最小值作为 oracle，对比所有 `top/getMin` 结果；固定覆盖重复最小值、完整 32 位端点、连续弹栈和交替压弹。所有完整代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/min-stack/)
- [对应知识专题](../../data-structures/augmented-stacks.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-111-lc189/">← [力扣 Top 111] LC 189 轮转数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-113-lc122/">[力扣 Top 113] LC 122 买卖股票的最佳时机 II 中等 →</a>
</nav>
