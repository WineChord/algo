---
title: "[力扣 Top 4] LC 146 LRU 缓存 中等"
---

# [力扣 Top 4] LC 146 LRU 缓存 中等

<p class="daily-archive-kicker">2026-07-26 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-26 题目列表</a> · <a href="../../data-structures/hash-and-cache.md">进入知识专题</a></p>

## 官方原始信息

- 难度：中等
- 官方链接：https://leetcode.cn/problems/lru-cache/
- 类接口：`LRUCache(int capacity)`、`int get(int key)`、`void put(int key, int value)`

### 原始题意

设计固定容量的 LRU（最近最少使用）缓存。`get` 命中后返回值并把该键标记为最近使用；未命中返回 `-1`。`put` 更新已有键或插入新键，并把该键标记为最近使用；若超出容量，淘汰最久未使用的键。`get` 与 `put` 都要求平均 $O(1)$。

### 全部官方样例

容量为 $2$，依次执行：

`put(1,1), put(2,2), get(1), put(3,3), get(2), put(4,4), get(1), get(3), get(4)`

返回序列为：

`null, null, null, 1, null, -1, null, -1, 3, 4`

关键状态：`get(1)` 后键 $1$ 变为最近使用，因此插入键 $3$ 时淘汰键 $2$；访问键 $3$ 后再插入键 $4$，淘汰键 $1$。

### 全部约束

- $1\le capacity\le 3000$
- $0\le key\le 10000$
- $0\le value\le 10^5$
- `get` 与 `put` 总调用次数最多 $2\times 10^5$
- 两个操作必须达到平均 $O(1)$

## 最优结论

哈希表解决“按键找到节点”，双向链表解决“删除任意节点、移到最近端、淘汰最旧端”。链表头表示最近使用，尾表示最久未使用；哈希表保存 `key -> 链表迭代器`。两种结构共同维护后，`get`、`put` 都是平均 $O(1)$，空间 $O(capacity)$。面试中优先用 `std::list + unordered_map`，再能手写双向链表以解释底层不变量。

## 约束、边界与关键观察

- 只用哈希表无法知道谁最久未用；只用链表按键查找又是 $O(capacity)$。
- 单链表删除任意已知节点仍需要前驱；双向链表可在 $O(1)$ 删除。
- 更新已有键也算一次使用，必须移动到最近端。
- `get` 命中同样会改变淘汰顺序，不能是只读查询。
- 容量始终为正，但插入新键后仍应统一检查是否超限。
- 哈希表中的迭代器必须始终指向当前链表节点；删除节点前先移除映射。

## 样例状态演化

容量 $2$，链表按“最近 $\to$ 最旧”表示：

- `put(1,1)`：`[1]`
- `put(2,2)`：`[2,1]`
- `get(1)`：命中并移到头部，`[1,2]`
- `put(3,3)`：插入后淘汰尾部 $2$，`[3,1]`
- `get(2)`：未命中，顺序不变
- `put(4,4)`：淘汰尾部 $1$，`[4,3]`

## 解法一：顺序数组模拟

数组头部为最近使用。每次 `get` 或更新都线性寻找键并移动；插入超限时删除末尾。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LRUCache {
  int cap;
  vector<pair<int, int>> a;
  int findKey(int key) {
    for (int i = 0; i < (int)a.size(); ++i) {
      if (a[i].first == key) return i;
    }
    return -1;
  }
  void moveFront(int i) {
    auto item = a[i];
    a.erase(a.begin() + i);
    a.insert(a.begin(), item);
  }
public:
  LRUCache(int capacity) : cap(capacity) {}
  int get(int key) {
    int i = findKey(key);
    if (i == -1) return -1;
    int value = a[i].second;
    moveFront(i);
    return value;
  }
  void put(int key, int value) {
    int i = findKey(key);
    if (i != -1) {
      a[i].second = value;
      moveFront(i);
      return;
    }
    a.insert(a.begin(), {key, value});
    if ((int)a.size() > cap) a.pop_back();
  }
};
```

单次操作 $O(capacity)$，空间 $O(capacity)$。它是正确基准，但违反官方复杂度要求。

## 解法二：`list` 与哈希表（最佳实用解）

`list::splice` 能在 $O(1)$ 把已有节点移动到链表头，并保持迭代器有效。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LRUCache {
  int cap;
  list<pair<int, int>> order;
  unordered_map<int, list<pair<int, int>>::iterator> pos;
  void touch(list<pair<int, int>>::iterator it) {
    order.splice(order.begin(), order, it);
  }
public:
  LRUCache(int capacity) : cap(capacity) {}
  int get(int key) {
    auto it = pos.find(key);
    if (it == pos.end()) return -1;
    touch(it->second);
    return it->second->second;
  }
  void put(int key, int value) {
    auto it = pos.find(key);
    if (it != pos.end()) {
      it->second->second = value;
      touch(it->second);
      return;
    }
    order.push_front({key, value});
    pos[key] = order.begin();
    if ((int)order.size() > cap) {
      int oldKey = order.back().first;
      pos.erase(oldKey);
      order.pop_back();
    }
  }
};
```

期望时间：构造 $O(1)$，每次 `get`/`put` 为 $O(1)$；空间 $O(capacity)$。

### 正确性证明

维护两个不变量：链表从头到尾严格按最近使用时间由新到旧排列；哈希表恰好包含缓存内所有键并指向其唯一节点。命中的 `get` 和更新 `put` 把对应节点移到头部，恢复第一不变量而不改变集合；新插入键置于头部，若超限则删除尾节点，尾节点按不变量正是最久未使用者，同时删除其映射。由归纳，两条不变量始终成立，所有返回值和淘汰选择均正确。

## 解法三：手写双向链表

面试官要求不依赖 `std::list` 时，用哨兵节点消除头尾特判。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LRUCache {
  struct Node {
    int key, value;
    Node *prev, *next;
    Node(int k, int v) : key(k), value(v), prev(nullptr), next(nullptr) {}
  };
  int cap;
  Node *head, *tail;
  unordered_map<int, Node*> pos;
  void remove(Node* node) {
    node->prev->next = node->next;
    node->next->prev = node->prev;
  }
  void addFront(Node* node) {
    node->next = head->next;
    node->prev = head;
    head->next->prev = node;
    head->next = node;
  }
  void touch(Node* node) {
    remove(node);
    addFront(node);
  }
public:
  LRUCache(int capacity) : cap(capacity) {
    head = new Node(0, 0);
    tail = new Node(0, 0);
    head->next = tail;
    tail->prev = head;
  }
  int get(int key) {
    auto it = pos.find(key);
    if (it == pos.end()) return -1;
    touch(it->second);
    return it->second->value;
  }
  void put(int key, int value) {
    auto it = pos.find(key);
    if (it != pos.end()) {
      it->second->value = value;
      touch(it->second);
      return;
    }
    Node* node = new Node(key, value);
    pos[key] = node;
    addFront(node);
    if ((int)pos.size() > cap) {
      Node* old = tail->prev;
      remove(old);
      pos.erase(old->key);
      delete old;
    }
  }
  ~LRUCache() {
    Node* cur = head;
    while (cur) {
      Node* next = cur->next;
      delete cur;
      cur = next;
    }
  }
};
```

复杂度同样为平均 $O(1)$；手写版更容易出现指针和资源管理错误，所以工程与竞赛中优先 `std::list`。

## 常见错误

- `get` 命中后没有更新新旧顺序。
- 更新已有键时新建第二个节点，导致映射与链表分叉。
- 超限时先 `pop_back`，随后已经无法取得被淘汰键来删除哈希项。
- 保存 `vector` 迭代器；插入和删除会使其失效。
- 手写链表忘记同时维护四条相邻指针或释放被淘汰节点。
- 把哈希期望 $O(1)$ 误写成严格最坏 $O(1)$。

## Follow-up 1：LFU，频率相同时淘汰最旧者

对应 [LeetCode 460 · LFU 缓存](https://leetcode.cn/problems/lfu-cache/)。额外维护每个频率的一条 LRU 链表，以及当前最小频率。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LFUCache {
  struct Entry {
    int value, freq;
    list<int>::iterator it;
  };
  int cap, minFreq = 0;
  unordered_map<int, Entry> data;
  unordered_map<int, list<int>> buckets;
  void touch(int key) {
    auto& e = data[key];
    int f = e.freq;
    buckets[f].erase(e.it);
    if (f == minFreq && buckets[f].empty()) ++minFreq;
    ++e.freq;
    buckets[e.freq].push_front(key);
    e.it = buckets[e.freq].begin();
  }
public:
  LFUCache(int capacity) : cap(capacity) {}
  int get(int key) {
    if (!data.count(key)) return -1;
    int value = data[key].value;
    touch(key);
    return value;
  }
  void put(int key, int value) {
    if (cap == 0) return;
    if (data.count(key)) {
      data[key].value = value;
      touch(key);
      return;
    }
    if ((int)data.size() == cap) {
      int old = buckets[minFreq].back();
      buckets[minFreq].pop_back();
      data.erase(old);
    }
    minFreq = 1;
    buckets[1].push_front(key);
    data[key] = {value, 1, buckets[1].begin()};
  }
};
```

平均每次操作 $O(1)$，空间 $O(capacity)$。

## Follow-up 2：按条目权重限制总容量

容量不再是条目个数，而是所有权重之和。插入或更新后，从 LRU 尾部持续淘汰到总权重不超限。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class WeightedLRU {
  struct Item {
    int key, value, weight;
  };
  int cap, used = 0;
  list<Item> order;
  unordered_map<int, list<Item>::iterator> pos;
public:
  WeightedLRU(int capacity) : cap(capacity) {}
  int get(int key) {
    auto it = pos.find(key);
    if (it == pos.end()) return -1;
    order.splice(order.begin(), order, it->second);
    return it->second->value;
  }
  void put(int key, int value, int weight) {
    auto it = pos.find(key);
    if (it != pos.end()) {
      used -= it->second->weight;
      it->second->value = value;
      it->second->weight = weight;
      used += weight;
      order.splice(order.begin(), order, it->second);
    } else {
      order.push_front({key, value, weight});
      pos[key] = order.begin();
      used += weight;
    }
    while (used > cap && !order.empty()) {
      used -= order.back().weight;
      pos.erase(order.back().key);
      order.pop_back();
    }
  }
};
```

每个条目只会被淘汰一次，连续操作的淘汰成本可做均摊分析；查找和移动仍是期望 $O(1)$。

## Follow-up 3：加入过期时间 TTL

接口显式接收当前时间。最小堆按过期时间清理，版本号使旧堆记录惰性失效；LRU 链表仍负责容量淘汰。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class LRUCacheTTL {
  struct Item {
    int key, value, expire, version;
  };
  int cap, nextVersion = 0;
  list<Item> order;
  unordered_map<int, list<Item>::iterator> pos;
  using Event = tuple<int, int, int>;
  priority_queue<Event, vector<Event>, greater<Event>> events;
  void erase(list<Item>::iterator it) {
    pos.erase(it->key);
    order.erase(it);
  }
  void purge(int now) {
    while (!events.empty() && get<0>(events.top()) <= now) {
      auto [expire, key, version] = events.top();
      events.pop();
      auto it = pos.find(key);
      if (it != pos.end() && it->second->version == version) erase(it->second);
    }
  }
public:
  LRUCacheTTL(int capacity) : cap(capacity) {}
  int get(int key, int now) {
    purge(now);
    auto it = pos.find(key);
    if (it == pos.end()) return -1;
    order.splice(order.begin(), order, it->second);
    return it->second->value;
  }
  void put(int key, int value, int ttl, int now) {
    purge(now);
    auto it = pos.find(key);
    if (it != pos.end()) erase(it->second);
    int version = ++nextVersion;
    order.push_front({key, value, now + ttl, version});
    pos[key] = order.begin();
    events.emplace(now + ttl, key, version);
    if ((int)order.size() > cap) erase(prev(order.end()));
  }
};
```

堆使单次操作为 $O(\log capacity)$；空间还包含尚未弹出的惰性事件。

## Follow-up 4：多线程访问

最小正确改造是用同一把互斥锁保护哈希表与链表组成的复合不变量；读命中也会改顺序，因此 `get` 不能使用共享读锁。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class ThreadSafeLRU {
  int cap;
  list<pair<int, int>> order;
  unordered_map<int, list<pair<int, int>>::iterator> pos;
  mutex mu;
public:
  ThreadSafeLRU(int capacity) : cap(capacity) {}
  int get(int key) {
    lock_guard<mutex> lock(mu);
    auto it = pos.find(key);
    if (it == pos.end()) return -1;
    order.splice(order.begin(), order, it->second);
    return it->second->second;
  }
  void put(int key, int value) {
    lock_guard<mutex> lock(mu);
    auto it = pos.find(key);
    if (it != pos.end()) {
      it->second->second = value;
      order.splice(order.begin(), order, it->second);
      return;
    }
    order.push_front({key, value});
    pos[key] = order.begin();
    if ((int)order.size() > cap) {
      pos.erase(order.back().first);
      order.pop_back();
    }
  }
};
```

锁内算法复杂度不变，但高并发下吞吐会受串行化影响；分片缓存需要重新定义跨分片的淘汰语义。

## Reference

- 官方题面与接口：https://leetcode.cn/problems/lru-cache/

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/lru-cache/)
- [对应知识专题](../../data-structures/hash-and-cache.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-3-lc3.md">← [力扣 Top 3] LC 3 无重复字符的最长子串 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-5-lc42.md">[力扣 Top 5] LC 42 接雨水 困难 →</a>
</nav>
