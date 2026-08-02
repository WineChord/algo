---
title: "[力扣 Top 84] LC 135 分发糖果 困难"
---

# [力扣 Top 84] LC 135 分发糖果 困难

<p class="daily-archive-kicker">2026-08-03 · 第 5/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-03 题目列表</a> · <a href="../../../basics/greedy-exchange/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=2341757358dc94ee862ec9a9a2f791df90ce2d8674a7e3a7b5bdfcde3a5bce0f -->
## 官方原始信息

- Top 排名：84
- 题号：LC 135
- 官方中文标题：分发糖果
- 官方难度：困难
- 官方链接：[分发糖果](https://leetcode.cn/problems/candy/)

### 原始题意

$n$ 个孩子站成一排，每人至少一颗糖；若某个孩子评分严格高于相邻孩子，他获得的糖也必须严格更多。求满足条件的最少糖果总数。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int candy(vector<int>& ratings);
};
```

### 全部官方样例

```text
输入：ratings = [1,0,2]
输出：5
解释：可分配 [2,1,2]。
```

```text
输入：ratings = [1,2,2]
输出：4
解释：可分配 [1,2,1]；相等评分不要求糖数关系。
```

### 全部约束

- $1\le n\le2\times10^4$。
- $0\le ratings_i\le2\times10^4$。

## 约束推导与不变量

约束只沿相邻边传播。每个孩子至少 1 颗；若只考虑左邻，则从左到右在上升边上递增即可得到逐点最小值 `L[i]`；只考虑右邻，对称地从右到左得到 `R[i]`。同时满足两侧约束的逐点最小糖数是

$$
candy_i=\max(L_i,R_i).
$$

总数最大约为 $1+2+\cdots+n\le2.0001\times10^8$，`int` 安全。评分相等不产生边，必须重置为 1，不能使用非严格比较。

## 解法递进

### 解法一：反复松弛所有相邻约束

从全 1 开始，反复扫描；若高评分孩子糖不更多，就把它提升到低评分邻居加 1。直到无变化。该方法能收敛到最小固定点，但长单调序列会传播很多轮。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int candy(vector<int>& ratings) {
    int n = ratings.size();
    vector<int> candies(n, 1);
    bool changed = true;
    while (changed) {
      changed = false;
      for (int i = 0; i + 1 < n; ++i) {
        if (ratings[i] > ratings[i + 1] && candies[i] <= candies[i + 1]) {
          candies[i] = candies[i + 1] + 1;
          changed = true;
        }
        if (ratings[i] < ratings[i + 1] && candies[i] >= candies[i + 1]) {
          candies[i + 1] = candies[i] + 1;
          changed = true;
        }
      }
    }
    return accumulate(candies.begin(), candies.end(), 0);
  }
};
```

最坏时间 $O(n^2)$，空间 $O(n)$，适合小规模 oracle。

### 最佳实用解：左右两遍取逐点最大值

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int candy(vector<int>& ratings) {
    int n = ratings.size();
    vector<int> candies(n, 1);
    for (int i = 1; i < n; ++i) {
      if (ratings[i] > ratings[i - 1]) {
        candies[i] = candies[i - 1] + 1;
      }
    }
    int answer = candies[n - 1];
    int fromRight = 1;
    for (int i = n - 2; i >= 0; --i) {
      fromRight = ratings[i] > ratings[i + 1] ? fromRight + 1 : 1;
      answer += max(candies[i], fromRight);
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(n)$。只存左约束，右约束用一个变量滚动，代码短且易证明，是最佳实用解。

### 同阶常数空间方案：统计上坡与下坡

一段严格上坡需要糖数 $1,2,\ldots$；下坡对称。峰顶同时属于两段，只需取两侧高度最大值一次。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int candy(vector<int>& ratings) {
    int answer = 1;
    int up = 0;
    int down = 0;
    int peak = 0;
    for (int i = 1; i < static_cast<int>(ratings.size()); ++i) {
      if (ratings[i] > ratings[i - 1]) {
        up += 1;
        peak = up;
        down = 0;
        answer += up + 1;
      } else if (ratings[i] == ratings[i - 1]) {
        up = down = peak = 0;
        answer += 1;
      } else {
        up = 0;
        down += 1;
        answer += down + 1;
        if (peak >= down) {
          answer -= 1;
        }
      }
    }
    return answer;
  }
};
```

时间 $O(n)$，额外空间 $O(1)$。它空间更优，但峰顶去重细节更难审查；面试中优先写两遍法，内存极严时再写坡度法。

## 正确性证明

左扫得到的 `left[i]` 是仅考虑左邻约束时的最小可行糖数：非上升边取 1，上升边必须且只需比左邻多 1。右扫同理得到仅考虑右邻的最小值 `right[i]`。任何全局可行方案都必须逐点不少于二者，所以不少于 `max(left[i],right[i])`；该最大值又同时满足左、右两类约束，因为对应严格边至少由一侧下界保证。因此它是逐点且总和意义下的最小可行方案，算法求和正确。

## 样例手推

`[1,0,2]` 左扫为 `[1,1,2]`，右侧下界为 `[2,1,1]`，逐点最大得 `[2,1,2]`，总数 5。`[1,2,2]` 左扫 `[1,2,1]`，右侧没有下降约束，答案 4；相等的最后两人无需相同或递增糖数。

## 易错点与方案比较

- 评分相等时没有大小约束，必须把单侧连续量重置为 1。
- 只左扫会漏掉长下降坡，只右扫会漏掉上升坡。
- 两侧结果要取最大值而不是相加，峰顶只属于一个孩子。
- 坡度法在下坡长度不超过此前上坡高度时要减去重复峰顶贡献。
- 两遍法空间 $O(n)$ 但证明和实现最稳定；坡度法 $O(1)$ 空间、状态更微妙。

## 变种一：返回一组最优分配

新定义：输出最少总数及每个孩子的糖数。保留完整左右数组并逐点取最大值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> rating(n), left(n, 1), right(n, 1);
  for (int& value : rating) {
    cin >> value;
  }
  for (int i = 1; i < n; ++i) {
    if (rating[i] > rating[i - 1])
      left[i] = left[i - 1] + 1;
  }
  for (int i = n - 2; i >= 0; --i) {
    if (rating[i] > rating[i + 1])
      right[i] = right[i + 1] + 1;
  }
  long long total = 0;
  for (int i = 0; i < n; ++i) {
    left[i] = max(left[i], right[i]);
    total += left[i];
  }
  cout << total << '\n';
  for (int value : left)
    cout << value << ' ';
  cout << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种二：孩子围成圆环

新定义：首尾也相邻。线性左右扫描失效；按评分从小到大处理，某孩子的糖数等于所有更低评分邻居糖数最大值加 1。相等评分之间没有边。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> rating(n), order(n), candy(n, 1);
  for (int& value : rating)
    cin >> value;
  iota(order.begin(), order.end(), 0);
  sort(order.begin(), order.end(), [&](int a, int b) { return rating[a] < rating[b]; });
  for (int index : order) {
    for (int neighbor : {(index - 1 + n) % n, (index + 1) % n}) {
      if (rating[index] > rating[neighbor]) {
        candy[index] = max(candy[index], candy[neighbor] + 1);
      }
    }
  }
  cout << accumulate(candy.begin(), candy.end(), 0LL) << '\n';
}
```

时间 $O(n\log n)$，空间 $O(n)$。按评分排序给出了有向约束图的拓扑顺序。

## 变种三：高评分者至少多 $D$ 颗

新定义：严格高评分的相邻孩子糖数至少相差 $D\ge1$。两遍转移中的 `+1` 改为 `+D`，基础仍为 1。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, difference;
  cin >> n >> difference;
  vector<int> rating(n);
  vector<long long> candy(n, 1), right(n, 1);
  for (int& value : rating)
    cin >> value;
  for (int i = 1; i < n; ++i) {
    if (rating[i] > rating[i - 1])
      candy[i] = candy[i - 1] + difference;
  }
  for (int i = n - 2; i >= 0; --i) {
    if (rating[i] > rating[i + 1])
      right[i] = right[i + 1] + difference;
  }
  long long answer = 0;
  for (int i = 0; i < n; ++i)
    answer += max(candy[i], right[i]);
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；总数可能随 $D$ 增大，使用 `long long`。

## 变种四：任意无向关系图上的评分约束

新定义：孩子由图连接；沿任意边，高评分端必须糖更多。把每条不等评分边从低评分指向高评分，按评分升序做最长路 DP。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, edgeCount;
  cin >> n >> edgeCount;
  vector<int> rating(n), order(n), candy(n, 1);
  vector<vector<int>> graph(n);
  for (int& value : rating)
    cin >> value;
  while (edgeCount--) {
    int first, second;
    cin >> first >> second;
    --first;
    --second;
    graph[first].push_back(second);
    graph[second].push_back(first);
  }
  iota(order.begin(), order.end(), 0);
  sort(order.begin(), order.end(), [&](int a, int b) { return rating[a] < rating[b]; });
  for (int node : order) {
    for (int neighbor : graph[node]) {
      if (rating[node] > rating[neighbor]) {
        candy[node] = max(candy[node], candy[neighbor] + 1);
      }
    }
  }
  cout << accumulate(candy.begin(), candy.end(), 0LL) << '\n';
}
```

时间 $O((n+E)\log n)$，空间 $O(n+E)$。线性两遍是路径图这一特殊结构上的更快实现。

## 验证说明

本轮将七段代码按 C++23 编译；两遍法与常数空间坡度法会同时对照反复松弛 oracle，在随机长度 1–10、含相等评分的数组上对拍，并复核两个官方样例、全相等、单调、锯齿与长谷底。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/candy/)
- [对应知识专题](../../basics/greedy-exchange.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-83-lc13/">← [力扣 Top 83] LC 13 罗马数字转整数 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-85-lc152/">[力扣 Top 85] LC 152 乘积最大子数组 中等 →</a>
</nav>
