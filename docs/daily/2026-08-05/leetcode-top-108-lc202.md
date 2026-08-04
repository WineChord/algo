---
title: "[力扣 Top 108] LC 202 快乐数 简单"
---

# [力扣 Top 108] LC 202 快乐数 简单

<p class="daily-archive-kicker">2026-08-05 · 第 9/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../graph/functional-graphs/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=c292727a7579faa446b9b3e1ffeac788c0994a4c990e370d810124ae47cbc251 -->
## 官方原始信息

- Top 排名：108
- 题号：LC 202
- 官方中文标题：快乐数
- 官方难度：简单
- 官方链接：[快乐数](https://leetcode.cn/problems/happy-number/)

### 原始题意

对正整数反复执行“替换为各十进制数位平方和”。若最终到达 1，则为快乐数；若进入不含 1 的循环，则不是。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  bool isHappy(int n);
};
```

### 全部官方样例

```text
输入：n = 19
输出：true
解释：1^2+9^2=82，8^2+2^2=68，6^2+8^2=100，1^2+0^2+0^2=1。
```

```text
输入：n = 2
输出：false
```

### 全部约束

- $1\le n\le2^{31}-1$。

## 约束推导与观察

把变换记为 $f(n)$。十位 `int` 最多 10 个十进制数位，第一次变换后不超过 $10\times9^2=810$；此后状态落在有限小集合中，所以轨迹必到达 1 或重复某个状态。问题因此是函数图上的“目标点或环”判定，可用集合记录访问，也可用 Floyd 快慢指针把空间降为常量。

数位平方和最大很小，`int` 安全。

## 解法递进

### 解法一：哈希集合检测重复状态

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int nextValue(int value) {
    int sum = 0;
    while (value) {
      int digit = value % 10;
      sum += digit * digit;
      value /= 10;
    }
    return sum;
  }
public:
  bool isHappy(int n) {
    unordered_set<int> seen;
    while (n != 1 && seen.insert(n).second) {
      n = nextValue(n);
    }
    return n == 1;
  }
};
```

时间与轨迹长度乘数位数成正比，空间为访问状态数。它最直观，但存储并非必要。

### 最佳实用解：Floyd 判环

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int nextValue(int value) {
    int sum = 0;
    while (value) {
      int digit = value % 10;
      sum += digit * digit;
      value /= 10;
    }
    return sum;
  }
public:
  bool isHappy(int n) {
    int slow = n;
    int fast = nextValue(n);
    while (fast != 1 && slow != fast) {
      slow = nextValue(slow);
      fast = nextValue(nextValue(fast));
    }
    return fast == 1;
  }
};
```

时间 $O(\log n)$ 可理解为第一次压缩数位加有限状态轨迹，额外空间 $O(1)$。它与 LC 141、LC 287 共用函数图判环模型。

## 正确性证明

轨迹由确定函数 `nextValue` 唯一决定，且第一次后进入有限集合，因此只有两种终态：到达固定点 1，或进入不含 1 的环。快指针若先到 1，原轨迹必到 1；否则 Floyd 定理保证快慢指针在环内相遇。相遇且快指针不为 1 时，轨迹已进入非 1 环，永远无法到达 1。算法的返回值因而与快乐数定义完全一致。

## 样例手推

`19→82→68→100→1`，快指针最终先到 1。`2` 的轨迹会进入 `4→16→37→58→89→145→42→20→4` 的环，快慢指针在其中相遇，因此返回 false。

## 易错点与方案比较

- 判断的是状态值重复，不是某个十进制数位重复。
- 快指针每轮必须应用变换两次。
- `0` 不是合法输入；变换 100 时数位 0 自然贡献 0。
- 集合法便于恢复轨迹，Floyd 空间最优；只需布尔答案时推荐 Floyd。

## 变种一：返回完整终止轨迹或循环

新定义：输出首次重复前的状态序列，并报告是到达 1 还是环入口。需要哈希表保存首次位置，Floyd 不能直接恢复全部轨迹。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int nextValue(int value) {
  int sum = 0;
  while (value) {
    int digit = value % 10;
    sum += digit * digit;
    value /= 10;
  }
  return sum;
}
int main() {
  int n;
  cin >> n;
  unordered_map<int, int> first;
  vector<int> path;
  while (n != 1 && !first.contains(n)) {
    first[n] = path.size();
    path.push_back(n);
    n = nextValue(n);
  }
  path.push_back(n);
  for (int i = 0; i < static_cast<int>(path.size()); ++i) {
    cout << path[i] << (i + 1 == static_cast<int>(path.size()) ? '\n' : ' ');
  }
  cout << (n == 1 ? "HAPPY" : "CYCLE " + to_string(first[n])) << '\n';
}
```

时间与轨迹长度成正比，空间同样为 $O(轨迹长度)$。

## 变种二：任意进制下的数位平方和

新定义：使用 $2\le B\le36$ 进制的数位，但输入仍以十进制整数给出。取模和除数改为 `base`，函数图方法不变。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long nextValue(long long value, int base) {
  long long sum = 0;
  while (value) {
    long long digit = value % base;
    sum += digit * digit;
    value /= base;
  }
  return sum;
}
int main() {
  long long n;
  int base;
  cin >> n >> base;
  long long slow = n;
  long long fast = nextValue(n, base);
  while (fast != 1 && slow != fast) {
    slow = nextValue(slow, base);
    fast = nextValue(nextValue(fast, base), base);
  }
  cout << (fast == 1 ? "true" : "false") << '\n';
}
```

空间 $O(1)$；一次变换为 $O(\log_B n)$。不同进制的环结构不同，不能复用十进制已知环表。

## 变种三：数位的 $p$ 次幂和

新定义：$1\le p\le9$。使用安全乘法计算单个数位幂，仍以访问集合判定终态是否为 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long digitPowerSum(long long value, int power) {
  long long sum = 0;
  while (value) {
    int digit = value % 10;
    long long term = 1;
    for (int exponent = 0; exponent < power; ++exponent) {
      term *= digit;
    }
    sum += term;
    value /= 10;
  }
  return sum;
}
int main() {
  long long n;
  int power;
  cin >> n >> power;
  unordered_set<long long> seen;
  while (n != 1 && seen.insert(n).second) {
    n = digitPowerSum(n, power);
  }
  cout << (n == 1 ? "true" : "false") << '\n';
}
```

时间取决于轨迹长度与 $p\log n$，空间为状态数。幂次放大后有限状态上界改变，不能沿用平方和的 810 上界。

## 变种四：批量询问并跨询问记忆结果

新定义：大量十进制询问。对每条新轨迹暂存路径，一旦碰到已知状态即可把整条路径标为快乐或不快乐。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int nextValue(int value) {
  int sum = 0;
  while (value) {
    int digit = value % 10;
    sum += digit * digit;
    value /= 10;
  }
  return sum;
}
int main() {
  int q;
  cin >> q;
  unordered_map<int, bool> known{{1, true}};
  while (q--) {
    int n;
    cin >> n;
    vector<int> path;
    unordered_map<int, int> local;
    int current = n;
    while (!known.contains(current) && !local.contains(current)) {
      local[current] = path.size();
      path.push_back(current);
      current = nextValue(current);
    }
    bool happy = known.contains(current) && known[current];
    for (int value : path) {
      known[value] = happy;
    }
    cout << (happy ? "true" : "false") << '\n';
  }
}
```

摊还时间优于逐问独立遍历，空间为所有被记忆的状态。若输入范围无限且幂次变化，应限制缓存或只缓存压缩后的小状态。

## 验证说明

本轮将六段代码按 C++23 编译；Floyd 与集合法会对拍全部 $1\le n\le10^6$，并覆盖 1、19、2、最大 32 位正整数及已知非快乐环。进制、幂次和批量版本分别与独立访问集合 oracle 核验。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/happy-number/)
- [对应知识专题](../../graph/functional-graphs.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-107-lc179/">← [力扣 Top 107] LC 179 最大数 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-109-lc141/">[力扣 Top 109] LC 141 环形链表 简单 →</a>
</nav>
