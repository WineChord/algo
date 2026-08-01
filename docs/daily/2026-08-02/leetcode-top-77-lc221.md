---
title: "[力扣 Top 77] LC 221 最大正方形 中等"
---

# [力扣 Top 77] LC 221 最大正方形 中等

<p class="daily-archive-kicker">2026-08-02 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-02 题目列表</a> · <a href="../../../dp/grid-dp/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=a07a52539268d948fca7f0ded5cbc5911525c9d162fe0748fe705753d4af674d -->
## 官方原始信息

- Top 排名：77
- 题号：LC 221
- 官方中文标题：最大正方形
- 官方难度：中等
- 官方链接：[最大正方形](https://leetcode.cn/problems/maximal-square/)

### 原始题意

在一个只含 `'0'` 与 `'1'` 的二维矩阵中，找出只包含 `'1'` 的最大轴对齐正方形，返回其面积。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int maximalSquare(vector<vector<char>>& matrix);
};
```

### 全部官方样例

```text
输入：matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
输出：4
```

```text
输入：matrix = [["0","1"],["1","0"]]
输出：1
```

```text
输入：matrix = [["0"]]
输出：0
```

### 全部约束

- $m=matrix.length$，$n=matrix[i].length$。
- $1\le m,n\le300$。
- 每个元素为字符 `'0'` 或 `'1'`。

## 约束推导与局部状态

枚举左上角与边长再逐格检查会达到高次复杂度。要用 $O(mn)$，状态必须让每个格子只处理常数次。定义 `dp[i][j]` 为以 `(i-1,j-1)` 作为右下角的全 1 正方形最大边长。若当前格为 0，答案是 0；若为 1，扩展边长受左、上、左上三个相邻正方形中最短者限制：

$$
dp[i][j]=1+\min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]).
$$

加一圈零哨兵可消除边界特判。边长最多 300，面积最多 90000，`int` 安全。压缩成一维时必须额外保存更新前的左上值。

## 解法递进

### 解法一：枚举每个候选正方形

枚举左上角、边长，并扫描候选内部所有格子。只要遇到 0 就否决。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximalSquare(vector<vector<char>>& matrix) {
    int rows = matrix.size();
    int columns = matrix[0].size();
    int best = 0;
    for (int top = 0; top < rows; ++top) {
      for (int left = 0; left < columns; ++left) {
        for (int size = 1; top + size <= rows && left + size <= columns; ++size) {
          bool valid = true;
          for (int row = top; row < top + size && valid; ++row) {
            for (int column = left; column < left + size; ++column) {
              if (matrix[row][column] == '0') {
                valid = false;
                break;
              }
            }
          }
          if (valid) {
            best = max(best, size);
          }
        }
      }
    }
    return best * best;
  }
};
```

最坏时间 $O(mn\min(m,n)^3)$，空间 $O(1)$；只适合小矩阵 oracle。

### 解法二：二维动态规划

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximalSquare(vector<vector<char>>& matrix) {
    int rows = matrix.size();
    int columns = matrix[0].size();
    vector<vector<int>> dp(rows + 1, vector<int>(columns + 1));
    int best = 0;
    for (int row = 1; row <= rows; ++row) {
      for (int column = 1; column <= columns; ++column) {
        if (matrix[row - 1][column - 1] == '1') {
          dp[row][column] =
              1 + min({dp[row - 1][column], dp[row][column - 1], dp[row - 1][column - 1]});
          best = max(best, dp[row][column]);
        }
      }
    }
    return best * best;
  }
};
```

时间 $O(mn)$，空间 $O(mn)$。

### 最佳实用解：一维滚动状态

`dp[column]` 更新前是上方状态，更新后的 `dp[column-1]` 是左方状态，变量 `diagonal` 保存更新前的左上状态。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int maximalSquare(vector<vector<char>>& matrix) {
    int rows = matrix.size();
    int columns = matrix[0].size();
    vector<int> dp(columns + 1);
    int best = 0;
    for (int row = 1; row <= rows; ++row) {
      int diagonal = 0;
      for (int column = 1; column <= columns; ++column) {
        int up = dp[column];
        if (matrix[row - 1][column - 1] == '1') {
          dp[column] = 1 + min({up, dp[column - 1], diagonal});
          best = max(best, dp[column]);
        } else {
          dp[column] = 0;
        }
        diagonal = up;
      }
    }
    return best * best;
  }
};
```

时间 $O(mn)$，空间 $O(n)$。只求面积时这是最简洁的最优方案。

## 正确性证明

若当前格为 0，不存在以它为右下角的全 1 正方形。若为 1，设左、上、左上的最大边长最小值为 $k$。三个区域共同保证当前格左上方存在一个 $k\times k$ 全 1 方块，同时当前格所在的新底边和右边分别由左、上状态覆盖，因此可构成边长 $k+1$ 的正方形。若试图构成更大正方形，则它的左、上、左上子方块都至少需要边长 $k+1$，与最小者只有 $k$ 矛盾。故递推精确。扫描所有右下角并取最大边长，必覆盖全局最优正方形。

## 样例手推

样例 1 的第二、三行右侧形成连续 1。处理 `(2,3)`（零基）时，左、上、左上状态的最小值为 1，当前边长变为 2，面积为 4；没有位置能得到 3。单个 `0` 状态始终为 0，返回 0；任一单个 `1` 得边长 1。

## 易错点与方案比较

- 返回面积，不是边长。
- 矩阵元素是字符，比较 `'1'` 而非整数 1。
- 一维压缩中 `diagonal` 必须在覆盖 `dp[column]` 前保存。
- 状态锚定右下角；若改成左上角，依赖方向也要一起改变。
- 二维版更适合恢复坐标，一维版空间更小；只求面积时推荐一维版。

## 变种一：统计所有全 1 正方形数量

新定义：不只求最大值，统计所有边长的全 1 正方形。以某格为右下角且最大边长为 $k$ 时，它贡献 $k$ 个不同边长正方形，因此累加全部 `dp`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<int> dp(columns + 1);
  long long answer = 0;
  for (int row = 1; row <= rows; ++row) {
    int diagonal = 0;
    for (int column = 1; column <= columns; ++column) {
      char cell;
      cin >> cell;
      int up = dp[column];
      dp[column] = cell == '1' ? 1 + min({up, dp[column - 1], diagonal}) : 0;
      diagonal = up;
      answer += dp[column];
    }
  }
  cout << answer << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$。

## 变种二：返回最大正方形坐标

新定义：输出最大面积以及左上、右下坐标。每次刷新最大边长时记录右下角，再由边长反推左上角。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<string> matrix(rows);
  for (string& row : matrix) {
    cin >> row;
  }
  vector<int> dp(columns + 1);
  int best = 0;
  int bottom = -1;
  int right = -1;
  for (int row = 1; row <= rows; ++row) {
    int diagonal = 0;
    for (int column = 1; column <= columns; ++column) {
      int up = dp[column];
      dp[column] = matrix[row - 1][column - 1] == '1' ? 1 + min({up, dp[column - 1], diagonal}) : 0;
      diagonal = up;
      if (dp[column] > best) {
        best = dp[column];
        bottom = row - 1;
        right = column - 1;
      }
    }
  }
  cout << best * best << '\n';
  if (best > 0) {
    cout << bottom - best + 1 << ' ' << right - best + 1 << ' ' << bottom << ' ' << right << '\n';
  }
}
```

时间 $O(mn)$，空间 $O(n)$。

## 变种三：改求最大全 1 矩形

新定义：形状不再要求正方形。逐行维护连续高度，每行把问题转为柱状图最大矩形，用单调栈求解。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns;
  cin >> rows >> columns;
  vector<int> height(columns + 1);
  int answer = 0;
  for (int row = 0; row < rows; ++row) {
    string line;
    cin >> line;
    for (int column = 0; column < columns; ++column) {
      height[column] = line[column] == '1' ? height[column] + 1 : 0;
    }
    vector<int> stack;
    for (int column = 0; column <= columns; ++column) {
      while (!stack.empty() && height[stack.back()] > height[column]) {
        int h = height[stack.back()];
        stack.pop_back();
        int left = stack.empty() ? 0 : stack.back() + 1;
        answer = max(answer, h * (column - left));
      }
      stack.push_back(column);
    }
  }
  cout << answer << '\n';
}
```

时间 $O(mn)$，空间 $O(n)$；矩形需要同时优化高和宽，原三邻居递推不再成立。

## 变种四：正方形内允许至多 $k$ 个 0

新定义：允许噪声后，局部最短边状态失效。用二维前缀和 $O(1)$ 统计任意正方形零数，并二分最大可行边长。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, columns, allowed;
  cin >> rows >> columns >> allowed;
  vector<vector<int>> prefix(rows + 1, vector<int>(columns + 1));
  for (int i = 1; i <= rows; ++i) {
    string line;
    cin >> line;
    for (int j = 1; j <= columns; ++j) {
      int zero = line[j - 1] == '0';
      prefix[i][j] = prefix[i - 1][j] + prefix[i][j - 1] - prefix[i - 1][j - 1] + zero;
    }
  }
  auto feasible = [&](int size) {
    for (int bottom = size; bottom <= rows; ++bottom) {
      for (int right = size; right <= columns; ++right) {
        int zeros = prefix[bottom][right] - prefix[bottom - size][right] -
            prefix[bottom][right - size] + prefix[bottom - size][right - size];
        if (zeros <= allowed) {
          return true;
        }
      }
    }
    return false;
  };
  int low = 0;
  int high = min(rows, columns) + 1;
  while (low + 1 < high) {
    int middle = (low + high) / 2;
    if (feasible(middle)) {
      low = middle;
    } else {
      high = middle;
    }
  }
  cout << low * low << '\n';
}
```

时间 $O(mn\log\min(m,n))$，空间 $O(mn)$。

## 验证说明

滚动 DP 与候选枚举对 5000 个随机小矩阵对拍，覆盖全 0、全 1、单行、单列和棋盘格；七段 C++23 代码全部编译通过。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/maximal-square/)
- [对应知识专题](../../dp/grid-dp.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-76-lc19/">← [力扣 Top 76] LC 19 删除链表的倒数第 N 个结点 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-78-lc1768/">[力扣 Top 78] LC 1768 交替合并字符串 简单 →</a>
</nav>
