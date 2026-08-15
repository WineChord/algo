---
title: "[力扣 Top 136] LC 118 杨辉三角 简单"
---

# [力扣 Top 136] LC 118 杨辉三角 简单

<p class="daily-archive-kicker">2026-08-16 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-16 题目列表</a> · <a href="../../../math/combinatorial-counting/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=184f023b6dba5cfd97d8e1b0d91b50c15710e6bf44fb4f5e76765a79a3f1baa4 -->
[力扣 118：杨辉三角](https://leetcode.cn/problems/pascals-triangle/)

## 官方原始信息

- 题号：118。
- 官方中文标题：杨辉三角。
- 官方难度：简单。
- 函数签名：`vector<vector<int>> generate(int numRows)`。
- 题意：给定正整数 `numRows`，生成杨辉三角的前 `numRows` 行。第 `r` 行第
  `c` 个数等于它左上方与右上方两个数之和；两侧边界恒为 1。

### 全部官方样例

样例 1：

```text
输入：numRows = 5
输出：[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
```

样例 2：

```text
输入：numRows = 1
输出：[[1]]
```

### 全部官方约束

- `1 <= numRows <= 30`。

官方页面还给出了杨辉三角的逐行生长示意图；本题的递推、边界与样例已经完整确定算法语义。

## 约束、输出下界与整数范围

第 `r` 行有 `r + 1` 个数，前 `n` 行一共输出

$$
1+2+\cdots+n=\frac{n(n+1)}2=\Theta(n^2)
$$

个整数。因此任何完整返回答案的算法，时间和返回值本身占用的空间都至少是
$\Omega(n^2)$；目标不是追求虚假的线性时间，而是让每个输出位置只计算一次。

第 `r` 行第 `c` 项是组合数 $\binom rc$。约束下最大值为
$\binom{29}{14}=77558760$，小于 `int` 上限；相邻两项相加也不会溢出 32 位有符号整数。
若把行数放大，组合数会快速超过 64 位，届时需要取模或大整数。

## 样例手推与边界

从 `[1]` 开始：

- 新行两端先放 1；
- 第 3 行内部是 `1 + 1 = 2`，得到 `[1,2,1]`；
- 第 4 行内部是 `1 + 2 = 3` 与 `2 + 1 = 3`；
- 第 5 行内部是 `1 + 3 = 4`、`3 + 3 = 6`、`3 + 1 = 4`。

于是得到官方样例 1。`numRows = 1` 时没有内部位置，直接返回 `[[1]]`。
重复值是杨辉三角的正常结构，不需要去重；题目保证至少一行，不存在空输入。

## 解法一：按定义递归计算每个位置

最直接的暴力做法是把每个位置都当作一个独立问题：边界返回 1，内部递归求两个父节点。
它覆盖全部位置，因而正确；但同一个上层组合数会被许多下层位置反复计算。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  int value(int row, int column) {
    if (column == 0 || column == row) return 1;
    return value(row - 1, column - 1) + value(row - 1, column);
  }
public:
  vector<vector<int>> generate(int numRows) {
    vector<vector<int>> triangle(numRows);
    for (int row = 0; row < numRows; ++row) {
      triangle[row].resize(row + 1);
      for (int column = 0; column <= row; ++column) {
        triangle[row][column] = value(row, column);
      }
    }
    return triangle;
  }
};
```

递归树的重复子问题使总时间达到 $O(n2^n)$，递归栈为 $O(n)$，返回值为
$O(n^2)$。它只适合作为小规模正确性 oracle。

## 从暴力到最优：保存上一行

暴力的瓶颈不是递推式，而是没有复用已经算出的父节点。按行生成时，第 `row` 行只依赖
第 `row - 1` 行：

$$
a_{row,0}=a_{row,row}=1,
\qquad
a_{row,column}=a_{row-1,column-1}+a_{row-1,column}.
$$

答案本身就保存了上一行，因此不需要额外哈希表或递归记忆化。每个内部位置做一次加法，
正好达到输出规模下界。

## 最佳实用解：逐行动态规划

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> generate(int numRows) {
    vector<vector<int>> triangle;
    triangle.reserve(numRows);
    for (int row = 0; row < numRows; ++row) {
      vector<int> current(row + 1, 1);
      for (int column = 1; column < row; ++column) {
        current[column] = triangle[row - 1][column - 1] +
            triangle[row - 1][column];
      }
      triangle.push_back(move(current));
    }
    return triangle;
  }
};
```

时间复杂度为 $O(n^2)$，返回值空间为 $O(n^2)$，除返回值外当前行只占 $O(n)$。
这是面试和竞赛中应优先记忆的写法：递推关系直接、没有除法、证明短，而且已经达到输出下界。

## 同阶方案：逐行使用组合数乘法公式

同一行相邻组合数满足

$$
\binom r c=\binom r{c-1}\frac{r-c+1}{c}.
$$

它不读取上一行，也能在 $O(n^2)$ 时间生成答案。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> generate(int numRows) {
    vector<vector<int>> triangle;
    for (int row = 0; row < numRows; ++row) {
      vector<int> current(row + 1, 1);
      long long value = 1;
      for (int column = 1; column <= row; ++column) {
        value = value * (row - column + 1) / column;
        current[column] = static_cast<int>(value);
      }
      triangle.push_back(move(current));
    }
    return triangle;
  }
};
```

这也是 $O(n^2)$ 时间与 $O(n^2)$ 返回空间，常数相近。它依赖“乘积必可整除”的组合数事实，
放大约束时中间乘法更容易溢出；动态规划只有加法，证明和实现更稳定，所以仍推荐前一种。

## 正确性证明

对行号做数学归纳。

基例：第 0 行被构造为 `[1]`，与杨辉三角定义一致。

归纳假设：前 `row` 行均已正确。构造第 `row` 行时，两端被设为 1；每个内部位置
`column` 被设为上一行 `column - 1` 与 `column` 两个位置之和，恰是题目定义。
因此第 `row` 行正确。由归纳法，返回的全部 `numRows` 行都正确。

## 易错点

- 行、列使用 0 下标时，第 `row` 行长度是 `row + 1`。
- 内层循环只能遍历 `1 <= column < row`，两端不能读取不存在的父节点。
- 若原地更新一行，必须从右向左；从左向右会读到本轮刚改写的值。
- 完整三角形的空间不能声称为 $O(n)$；只能说辅助空间为 $O(n)$。
- 乘法公式必须先乘后除并使用更宽类型，不能先做整数除法。

## 验证说明

对 `numRows = 1..30`，分别运行递归、逐行动态规划和组合数乘法三种实现，逐项比较所有行；
同时核对每行长度、两端为 1、左右对称以及内部递推式。发布代码另以 C++23 语法编译。

## 变种一：只返回第 `rowIndex` 行

新定义与 [力扣 119：杨辉三角 II](https://leetcode.cn/problems/pascals-triangle-ii/) 一致。
完整三角形不再需要保留；一维数组从右向左更新，避免覆盖仍要使用的旧值。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> getRow(int rowIndex) {
    vector<int> row(rowIndex + 1, 0);
    row[0] = 1;
    for (int current = 1; current <= rowIndex; ++current) {
      for (int column = current; column >= 1; --column) {
        row[column] += row[column - 1];
      }
    }
    return row;
  }
};
```

时间 $O(rowIndex^2)$，空间 $O(rowIndex)$。原递推仍成立，改变的只是无需保留历史行。

## 变种二：对任意模数生成前 `n` 行

当 `n` 较大而只关心模 `mod` 的结果时，每次加法立即取模。因为只使用加法，`mod`
不必是质数；这比带除法的组合数公式更稳健。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<vector<long long>> pascalModulo(int n, long long mod) {
  vector<vector<long long>> answer(n);
  for (int row = 0; row < n; ++row) {
    answer[row].assign(row + 1, 1 % mod);
    for (int column = 1; column < row; ++column) {
      answer[row][column] = (answer[row - 1][column - 1] +
          answer[row - 1][column]) % mod;
    }
  }
  return answer;
}
int main() {
  int n;
  long long mod;
  cin >> n >> mod;
  auto triangle = pascalModulo(n, mod);
  for (const auto& row : triangle) {
    for (int i = 0; i < static_cast<int>(row.size()); ++i) {
      if (i) cout << ' ';
      cout << row[i];
    }
    cout << '\n';
  }
}
```

时间和输出空间仍为 $O(n^2)$；要求 `mod >= 1`。

## 变种三：大量组合数询问

若只询问若干个 $\binom nk\bmod p$，其中 `p` 为质数且所有 `n < p`，不应生成整张三角形。
预处理阶乘和逆阶乘，单次询问 $O(1)$。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long power(long long value, long long exponent, long long mod) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * value % mod;
    value = value * value % mod;
    exponent >>= 1;
  }
  return result;
}
int main() {
  int maximum, queries;
  long long prime;
  cin >> maximum >> queries >> prime;
  vector<long long> factorial(maximum + 1, 1);
  vector<long long> inverse(maximum + 1, 1);
  for (int i = 1; i <= maximum; ++i) {
    factorial[i] = factorial[i - 1] * i % prime;
  }
  inverse[maximum] = power(factorial[maximum], prime - 2, prime);
  for (int i = maximum; i > 0; --i) {
    inverse[i - 1] = inverse[i] * i % prime;
  }
  while (queries--) {
    int n, k;
    cin >> n >> k;
    if (k < 0 || k > n) cout << 0 << '\n';
    else cout << factorial[n] * inverse[k] % prime *
        inverse[n - k] % prime << '\n';
  }
}
```

预处理 $O(N)$，每次询问 $O(1)$，空间 $O(N)$。若 `n >= p`，需要 Lucas 定理等新工具。

## 变种四：带障碍的网格路径计数

$\binom rc$ 也等于从 `(0,0)` 只向下或向右走到 `(r-c,c)` 的路径数。加入障碍后闭式失效，
但“来自上方与左方之和”的同一递推仍成立。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
long long countPaths(const vector<string>& grid) {
  int rows = static_cast<int>(grid.size());
  int columns = static_cast<int>(grid[0].size());
  vector<long long> paths(columns, 0);
  paths[0] = grid[0][0] == '.';
  for (int row = 0; row < rows; ++row) {
    for (int column = 0; column < columns; ++column) {
      if (grid[row][column] == '#') paths[column] = 0;
      else if (column > 0) paths[column] += paths[column - 1];
    }
  }
  return paths.back();
}
int main() {
  int rows, columns;
  cin >> rows >> columns;
  vector<string> grid(rows);
  for (string& row : grid) cin >> row;
  cout << countPaths(grid) << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$。障碍把纯组合数问题变为局部状态动态规划。

## 变种五：流式输出而不保存整张三角形

若接口改为“依次打印每一行”，返回值不再要求随机访问历史行，只需保存当前一行并从右向左更新。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int rows;
  cin >> rows;
  vector<unsigned long long> current(rows, 0);
  current[0] = 1;
  for (int row = 0; row < rows; ++row) {
    if (row > 0) {
      for (int column = row; column >= 1; --column) {
        current[column] += current[column - 1];
      }
    }
    for (int column = 0; column <= row; ++column) {
      if (column) cout << ' ';
      cout << current[column];
    }
    cout << '\n';
  }
}
```

时间仍为 $O(n^2)$，但辅助空间降为 $O(n)$；这是输出接口改变后才能实现的空间优化。

## 来源

- [力扣 118 官方题面](https://leetcode.cn/problems/pascals-triangle/)
- [力扣 119 官方题面](https://leetcode.cn/problems/pascals-triangle-ii/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/pascals-triangle/)
- [对应知识专题](../../math/combinatorial-counting.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc226-e/">← [atcoder] ARC226 E Cellular Messenger</a>
<a class="daily-archive-pager__next" href="../leetcode-weekly-514-q3-lc4016/">[力扣竞赛] 第 514 场周赛 Q3 LC 4016 两个不重叠子正方形的最大面积 中等 →</a>
</nav>
