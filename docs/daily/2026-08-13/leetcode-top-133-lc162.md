---
title: "[力扣 Top 133] LC 162 寻找峰值 中等"
---

# [力扣 Top 133] LC 162 寻找峰值 中等

<p class="daily-archive-kicker">2026-08-13 · 第 2/5 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-13 题目列表</a> · <a href="../../../basics/binary-search/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=d9a6cef3c2cdaee317098a5c147bc1b040a6b517cad53faa155b3ef93cf1880f -->
[官方题目：LC 162 寻找峰值](https://leetcode.cn/problems/find-peak-element/)

## 官方原始信息

- 题号：162。
- 标题：寻找峰值。
- 难度：中等。
- 官方链接：[力扣中国](https://leetcode.cn/problems/find-peak-element/)。
- 题库顺序：Top 133；权威表格原行标题与当前官方标题一致。
- 标签：数组、二分查找。

给定整数数组 `nums`，峰值元素严格大于左右相邻元素。数组边界外视为负无穷；返回任意一个峰值下标。必须设计 $O(\log n)$ 算法。

函数签名：

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int findPeakElement(vector<int>& nums);
};
```

### 官方样例

样例 1：

```text
输入：nums = [1,2,3,1]
输出：2
解释：3 是峰值，返回下标 2。
```

样例 2：

```text
输入：nums = [1,2,1,3,5,6,4]
输出：1 或 5
解释：2 与 6 都是峰值，返回任意一个均可。
```

### 全部约束

- $1\le n\le1000$。
- $-2^{31}\le nums[i]\le2^{31}-1$。
- 对每个相邻位置都有 $nums[i]\ne nums[i+1]$。
- 边界外的 `nums[-1]` 与 `nums[n]` 视为 $-\infty$。

## 约束推导与关键观察

线性扫描显然能找到峰值，却不满足题目明确要求的 $O(\log n)$。相邻元素不相等，意味着任意相邻边只有严格上升或严格下降两种状态。

查看中点 `mid` 与右邻点：

- 若 `nums[mid] < nums[mid + 1]`，沿右侧上坡走。有限数组最终要么继续到右边界，要么首次转为下降；两种情形都保证 `[mid+1,right]` 中存在峰值。
- 否则中点处在下降坡或已经是峰值；`[left,mid]` 中必有峰值。

我们不要求函数值整体单调，只利用“坡向能保留至少一个解”的存在性不变量。

## 解法递进

### 解法一：逐点检查

从左到右找第一个严格大于两侧的位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findPeakElement(vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    for (int i = 0; i < n; ++i) {
      bool largerLeft = i == 0 || nums[i] > nums[i - 1];
      bool largerRight = i + 1 == n || nums[i] > nums[i + 1];
      if (largerLeft && largerRight) return i;
    }
    return -1;
  }
};
int main() {
  vector<int> nums{1, 2, 3, 1};
  cout << Solution().findPeakElement(nums) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。它正确且适合作为 oracle，但没有利用题目要求。

### 解法二：边界哨兵的开区间二分

也可把答案区间写成开区间，通过判断上坡逐步收缩；但边界和循环条件更容易写错。更稳健的实用形式是闭区间 `[left,right]`，且只在 `left < right` 时访问 `mid+1`。

### 最佳实用解：沿坡保留峰值

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int findPeakElement(vector<int>& nums) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] < nums[middle + 1]) left = middle + 1;
      else right = middle;
    }
    return left;
  }
};
int main() {
  vector<int> nums{1, 2, 1, 3, 5, 6, 4};
  cout << Solution().findPeakElement(nums) << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。

## 正确性证明

循环不变量：闭区间 `[left,right]` 内至少有一个峰值。

初始时整个数组必有峰值：从任意位置沿严格上升方向前进，有限步后必到边界或转为下降。若 `nums[mid] < nums[mid+1]`，从 `mid+1` 向右沿上坡即可在右半找到峰值，所以删除左半安全；否则从 `mid` 向左对应地保证左半存在峰值，所以令 `right=mid` 安全。每轮区间严格缩小，终止时 `left==right`；不变量保证该唯一位置就是峰值。

## 样例手推与边界

对 `[1,2,3,1]`：初始 `[0,3]`，`mid=1` 且 $2<3$，保留 `[2,3]`；随后 `mid=2` 且 $3>1$，保留 `[2,2]`，返回 2。

- 单元素数组直接返回 0。
- 严格递增数组返回末尾；严格递减数组返回开头。
- 多峰时返回哪一个取决于二分路径，题目允许任意峰值。
- 不需真的构造负无穷，因算法只比较数组内相邻元素。

## 方案比较与推荐

线性扫描证明最简单，却违反指定复杂度；二分只做一次相邻比较，常数、额外空间和实现稳定性都很好。面试中优先记“看 `mid` 到 `mid+1` 的坡向并保留峰值存在的一侧”，不要误记成对数值做普通单调查找。

## 易错点

- 循环必须是 `left < right`，这样 `mid+1` 才始终合法。
- 上坡时要丢掉 `mid`，即 `left=mid+1`；下降时 `mid` 可能就是峰值，必须保留。
- 相邻不等是严格坡向证明的关键；若允许平台，相等分支需要重新定义目标。
- 不要用 `INT_MIN` 模拟边界并参与潜在算术运算。

## 可复现验证

两种完整代码均以 C++23 严格编译。官方样例分别得到合法下标 2 与 5。本轮固定种子随机生成 100,000 个长度 1 至 100、相邻元素不同的数组，逐次验证二分返回位置严格大于实际存在的左右邻点，零失败。

## 变种一：返回所有峰值

输出规模可达 $\Theta(n)$，必须线性扫描；原二分只保证找到一个，无法越过输出下界。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> allPeaks(vector<int>& nums) {
    vector<int> answer;
    int n = static_cast<int>(nums.size());
    for (int i = 0; i < n; ++i) {
      if ((i == 0 || nums[i] > nums[i - 1]) &&
          (i + 1 == n || nums[i] > nums[i + 1])) answer.push_back(i);
    }
    return answer;
  }
};
int main() {
  vector<int> nums{1, 3, 2, 4, 1};
  for (int x : Solution().allPeaks(nums)) cout << x << ' ';
}
```

时间 $O(n)$，输出外空间 $O(1)$。

## 变种二：返回最高峰

若“峰值”改成全局最大值下标，局部坡向不再能丢弃另一侧更高的峰，只能扫描全体。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int highestPeak(vector<int>& nums) {
    return static_cast<int>(max_element(nums.begin(), nums.end()) - nums.begin());
  }
};
int main() {
  vector<int> nums{5, 1, 4, 3};
  cout << Solution().highestPeak(nums) << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：允许相邻相等并返回平台峰左端

平台可能横跨中点，仅看一个坡向不再可靠。先把相邻相等值压缩成段，再在段值上寻找严格峰并返回原段左端。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int plateauPeak(vector<int>& nums) {
    vector<int> value;
    vector<int> first;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
      if (value.empty() || value.back() != nums[i]) {
        value.push_back(nums[i]);
        first.push_back(i);
      }
    }
    int left = 0;
    int right = static_cast<int>(value.size()) - 1;
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (value[middle] < value[middle + 1]) left = middle + 1;
      else right = middle;
    }
    return first[left];
  }
};
int main() {
  vector<int> nums{1, 3, 3, 3, 2};
  cout << Solution().plateauPeak(nums) << '\n';
}
```

预处理 $O(n)$，二分 $O(\log n)$，空间 $O(n)$。

## 变种四：二维矩阵峰值

每轮取中间列的列最大值；若它小于左或右邻点，就向更高的一侧移动，否则它是二维峰值。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<int> findPeakGrid(vector<vector<int>>& mat) {
    int rows = static_cast<int>(mat.size());
    int left = 0;
    int right = static_cast<int>(mat[0].size()) - 1;
    while (left <= right) {
      int column = left + (right - left) / 2;
      int row = 0;
      for (int r = 1; r < rows; ++r) {
        if (mat[r][column] > mat[row][column]) row = r;
      }
      int before = column == 0 ? INT_MIN : mat[row][column - 1];
      int after = column == static_cast<int>(mat[0].size()) - 1 ? INT_MIN : mat[row][column + 1];
      if (mat[row][column] > before && mat[row][column] > after) return {row, column};
      if (before > mat[row][column]) right = column - 1;
      else left = column + 1;
    }
    return {-1, -1};
  }
};
int main() {
  vector<vector<int>> mat{{1, 4}, {3, 2}};
  auto answer = Solution().findPeakGrid(mat);
  cout << answer[0] << ' ' << answer[1] << '\n';
}
```

对 $m\times n$ 矩阵，时间 $O(m\log n)$，空间 $O(1)$。

## 变种五：单峰数组中找最大值

若数组保证先严格升后严格降，峰唯一；同一二分直接返回全局最大值，证明更强。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int mountainTop(vector<int>& nums) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;
    while (left < right) {
      int middle = left + (right - left) / 2;
      if (nums[middle] < nums[middle + 1]) left = middle + 1;
      else right = middle;
    }
    return left;
  }
};
int main() {
  vector<int> nums{0, 2, 5, 3, 1};
  cout << Solution().mountainTop(nums) << '\n';
}
```

时间 $O(\log n)$，空间 $O(1)$。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/find-peak-element/)
- [对应知识专题](../../basics/binary-search.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-arc226-b/">← [atcoder] ARC226 B Bin-ary Packing</a>
<a class="daily-archive-pager__next" href="../leetcode-biweekly-188-q4-lc4009/">[力扣竞赛] 第 188 场双周赛 Q4 LC 4009 最小化最大可能等待时间 困难 →</a>
</nav>
