---
title: "[力扣 Top 46] LC 739 每日温度 中等"
---

# [力扣 Top 46] LC 739 每日温度 中等

<p class="daily-archive-kicker">2026-07-30 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-30 题目列表</a> · <a href="../../../data-structures/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=de80dcbd9e6753a80e2923ab186b89a464775e7c60609abbaaf42316dfaeeae4 -->
## 官方原始信息

- Top 排名：46
- 题号：LC 739
- 官方中文标题：每日温度
- 官方难度：中等
- 官方链接：[每日温度](https://leetcode.cn/problems/daily-temperatures/)

### 原始题意

给定每天的温度数组 `temperatures`。对每一天，返回还需等待多少天才会遇到严格更高的温度；之后不存在更高温度则返回 0。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<int> dailyTemperatures(vector<int>& temperatures);
};
```

### 全部官方样例

```text
输入：temperatures = [73,74,75,71,69,72,76,73]
输出：[1,1,4,2,1,1,0,0]
```

```text
输入：temperatures = [30,40,50,60]
输出：[1,1,1,0]
```

```text
输入：temperatures = [30,60,90]
输出：[1,1,0]
```

### 全部约束

- $1\le n\le10^5$。
- $30\le temperatures_i\le100$。
- “更高”是严格大于，相等温度不能结算答案。

## 约束推导与结构观察

对每个位置向右扫描会达到 $O(n^2)$。如果某一天还没遇到更高温度，它只需等待；当新温度到达时，可以一次结算所有比它低、且仍未结算的最近下标。未结算下标的温度必须保持单调不增，否则较低温度早应被当前较高温度弹出。

## 解法递进

### 解法一：逐日起向右寻找

每个位置检查第一个严格更高值，时间 $O(n^2)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> dailyTemperatures(vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> answer(n);
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        if (temperatures[j] > temperatures[i]) {
          answer[i] = j - i;
          break;
        }
      }
    }
    return answer;
  }
};
```

### 最佳实用解：单调栈

栈中保存仍未找到答案的下标，按温度从栈底到栈顶单调不增。处理第 `i` 天时，只要新温度严格更高，就不断弹出并令答案为下标差。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> dailyTemperatures(vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> answer(n);
    vector<int> stack;
    for (int i = 0; i < n; ++i) {
      while (!stack.empty() && temperatures[stack.back()] < temperatures[i]) {
        int previous = stack.back();
        stack.pop_back();
        answer[previous] = i - previous;
      }
      stack.push_back(i);
    }
    return answer;
  }
};
```

时间复杂度 $O(n)$，空间复杂度 $O(n)$。

## 正确性证明

不变量：处理完前 `i-1` 天后，栈中恰是尚未遇到更高温度的下标，且对应温度单调不增。

当 `temperatures[i]` 大于栈顶温度时，对该栈顶而言，`i` 是第一个更高温度：若中间已有更高值，它早已在当时被弹出。于是答案可安全写成 `i-top`。反复弹出后，剩余栈顶温度不低于当前值，把 `i` 入栈仍维持单调不增。扫描结束后留在栈内的位置右侧没有更高温度，默认答案 0 正确。

## 样例手推

对前六天 `73,74,75,71,69,72`：

```text
74 到来：弹出 73，等待 1 天
75 到来：弹出 74，等待 1 天
71、69 依次入栈
72 到来：弹出 69（1 天）、71（2 天）
```

随后 76 会弹出 72 与 75，分别得到 1 天和 4 天。

## 易错点与方案比较

- 相等温度不能弹出，因此比较符号是 `<`，不是 `<=`。
- 栈必须存下标，才能计算距离；温度通过原数组读取。
- 每个下标至多入栈、出栈一次，嵌套 `while` 仍是线性复杂度。
- 从右向左也能维护温度下标栈；从左向右更符合“新元素结算旧请求”的在线模型。
- 推荐把本题作为“下一个严格更大元素”的标准单调栈模板。

## 变种一：下一个大于等于当前温度的日期

新定义：相等温度也算满足条件。只需把弹栈条件从 `<` 改成 `<=`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> temperature(n), answer(n), stack;
  for (int& value : temperature) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    while (!stack.empty() && temperature[stack.back()] <= temperature[i]) {
      int previous = stack.back();
      stack.pop_back();
      answer[previous] = i - previous;
    }
    stack.push_back(i);
  }
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。这个一字符差异改变了栈的严格性，必须从新定义重新确认。

## 变种二：温度按圆环重复一轮

新定义：最后一天之后回到第一天，每个位置最多向后查看 $n-1$ 天。遍历两遍下标，但只有第一遍入栈；第二遍只负责结算。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> temperature(n), answer(n), stack;
  for (int& value : temperature) {
    cin >> value;
  }
  for (int step = 0; step < 2 * n; ++step) {
    int i = step % n;
    while (!stack.empty() && temperature[stack.back()] < temperature[i]) {
      int previous = stack.back();
      stack.pop_back();
      answer[previous] = (i - previous + n) % n;
    }
    if (step < n) {
      stack.push_back(i);
    }
  }
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。未被弹出的全局最高温位置保持 0。

## 变种三：流式到达并即时输出已结算请求

新定义：每天温度在线到达；无法提前输出所有答案，但新温度到来时立刻输出所有刚刚确定的 `(旧下标, 等待天数)`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<pair<int, int>> stack;
  for (int day = 0; day < q; ++day) {
    int temperature;
    cin >> temperature;
    while (!stack.empty() && stack.back().second < temperature) {
      auto [previous_day, previous_temperature] = stack.back();
      stack.pop_back();
      cout << previous_day << ' ' << day - previous_day << '\n';
      static_cast<void>(previous_temperature);
    }
    stack.push_back({day, temperature});
  }
  while (!stack.empty()) {
    cout << stack.back().first << " 0\n";
    stack.pop_back();
  }
}
```

每次到达摊还 $O(1)$，未完成请求占 $O(n)$ 空间。最后输出 0 的顺序若有要求，应另存答案数组再统一输出。

## 变种四：利用温度值域只有 71 种

新定义不变。从右向左维护每个精确温度最近出现的下标；对当前温度枚举所有更高温度的最近位置并取最小。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> temperature(n), answer(n);
  for (int& value : temperature) {
    cin >> value;
  }
  const int INF = numeric_limits<int>::max();
  array<int, 101> nearest;
  nearest.fill(INF);
  for (int i = n - 1; i >= 0; --i) {
    int next = INF;
    for (int value = temperature[i] + 1; value <= 100; ++value) {
      next = min(next, nearest[value]);
    }
    if (next != INF) {
      answer[i] = next - i;
    }
    nearest[temperature[i]] = i;
  }
  for (int value : answer) {
    cout << value << ' ';
  }
  cout << '\n';
}
```

时间 $O(71n)=O(n)$，空间 $O(71)$。常数比单调栈更大，但展示了“小值域替代通用数据结构”的方法。

## 可复现验证

- 三个官方样例、全相等、严格下降、严格上升和末尾无答案应全部覆盖。
- 小规模随机温度序列可用 $O(n^2)$ 解作为 oracle，与单调栈和小值域解对拍。
- 所有完整代码按 C++23 编译。

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/daily-temperatures/)
<!-- DAILY_CANONICAL_BODY_END -->

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/daily-temperatures/)
- [对应知识专题](../../data-structures/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-45-lc209/">← [力扣 Top 45] LC 209 长度最小的子数组 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-47-lc160/">[力扣 Top 47] LC 160 相交链表 简单 →</a>
</nav>
