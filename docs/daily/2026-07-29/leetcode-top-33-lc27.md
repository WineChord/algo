---
title: "[力扣 Top 33] LC 27 移除元素 简单"
---

# [力扣 Top 33] LC 27 移除元素 简单

<p class="daily-archive-kicker">2026-07-29 · 第 4/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="index.md">返回 2026-07-29 题目列表</a> · <a href="../../basics/index.md">进入知识专题</a></p>

## 官方原始信息

- Top 排名：33
- 题号：LC 27
- 官方中文标题：移除元素
- 官方难度：简单
- 官方链接：<https://leetcode.cn/problems/remove-element/>

### 原始题意

给定数组 `nums` 和值 `val`，原地移除所有等于 `val` 的元素，返回剩余元素数量 `k`。只要求 `nums[0..k)` 包含所有保留元素；顺序可以改变，后缀内容和数组物理长度不参与评测。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int removeElement(vector<int>& nums, int val);
};
```

### 全部官方样例

```text
输入：nums = [3,2,2,3], val = 3
输出：2，前两个元素为 [2,2]
```

```text
输入：nums = [0,1,2,2,3,0,4,2], val = 2
输出：5，前五个元素可为 [0,1,4,0,3]
```

### 全部约束

- $0\le |nums|\le100$。
- $0\le nums_i\le50$。
- $0\le val\le100$。

## 最优结论

若希望保持相对顺序，用写指针维护已确认保留区间 `[0,write)`；扫描到不等于 `val` 的元素就写到 `nums[write]` 并递增。时间 $O(n)$、额外空间 $O(1)$，且每个元素只读一次。

题目允许改变顺序时，若 `val` 很少，还可以用右端元素覆盖待删除位置，减少写入次数；两者同阶，面试默认推荐稳定写指针，因为不变量最清楚。

## 约束与观察

原地要求排除额外结果数组，但不要求真正缩短 `vector`。返回值定义了有效前缀边界。空数组应直接返回 0；`val` 不出现时返回原长度；全部匹配时返回 0。

## 解法递进

### 解法一：额外数组收集

逻辑直接但使用 $O(n)$ 额外空间，不满足原地目标。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeElement(vector<int>& nums, int val) {
    vector<int> kept;
    for (int value : nums) {
      if (value != val) {
        kept.push_back(value);
      }
    }
    copy(kept.begin(), kept.end(), nums.begin());
    return static_cast<int>(kept.size());
  }
};
```

### 解法二：稳定写指针

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeElement(vector<int>& nums, int val) {
    int write = 0;
    for (int value : nums) {
      if (value != val) {
        nums[write++] = value;
      }
    }
    return write;
  }
};
```

### 同阶方案：与未处理尾部交换

当当前位置等于 `val` 时，用尾部尚未判断的元素覆盖它，并缩短有效右边界；覆盖后当前位置必须再次检查。写次数约等于被删除元素数，但顺序改变。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeElement(vector<int>& nums, int val) {
    int index = 0;
    int size = static_cast<int>(nums.size());
    while (index < size) {
      if (nums[index] == val) {
        nums[index] = nums[size - 1];
        --size;
      } else {
        ++index;
      }
    }
    return size;
  }
};
```

## 正确性证明

稳定方案循环不变量：扫描每个元素前，`nums[0..write)` 恰好是已扫描前缀中所有不等于 `val` 的元素，并保持原相对顺序。

若当前值等于 `val`，不写入，不变量继续成立；否则把它写到有效前缀末尾并增加 `write`，新前缀恰好多包含该保留值。扫描结束后，所有元素均已处理，因此有效前缀恰为全部保留元素，`write` 即所求 `k`。

## 样例手推

`[0,1,2,2,3,0,4,2]`、`val=2`：

- 读到 `0,1` 后 `write=2`；
- 两个 `2` 被跳过；
- `3,0,4` 依次写到下标 2、3、4；
- 最终 `write=5`，有效前缀为 `[0,1,3,0,4]`。

## 易错点

- 不要调用 `erase` 循环删除；连续移动会退化为 $O(n^2)$。
- 尾部覆盖方案覆盖后不能立刻递增左指针。
- 只保证前 `k` 个位置，后缀无需清零。
- 若业务要求稳定性，应明确选择写指针方案。

## 验证说明

随机生成长度 0–100 的数组，以标准库过滤结果为 oracle；验证返回长度、有效前缀多重集合，以及稳定方案的相对顺序。

## Follow-up 与变种

### 变种一：一次移除多个值

把待删除值放入哈希集合，写指针框架不变。时间期望 $O(n+m)$，空间 $O(m)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int removeValues(vector<int>& nums, const vector<int>& removed) {
    unordered_set<int> banned(removed.begin(), removed.end());
    int write = 0;
    for (int value : nums) {
      if (!banned.contains(value)) {
        nums[write++] = value;
      }
    }
    return write;
  }
};
```

### 变种二：按任意谓词过滤

把“等于 `val`”抽象成调用方提供的谓词。以下保留所有非负数。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int keepNonNegative(vector<int>& nums) {
    int write = 0;
    for (int value : nums) {
      if (value >= 0) {
        nums[write++] = value;
      }
    }
    return write;
  }
};
```

### 变种三：有序数组中每个值最多保留 `k` 次

写入前查看写指针前第 `k` 个元素。时间 $O(n)$、空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int keepAtMost(vector<int>& nums, int k) {
    if (k == 0) {
      return 0;
    }
    int write = 0;
    for (int value : nums) {
      if (write < k || nums[write - k] != value) {
        nums[write++] = value;
      }
    }
    return write;
  }
};
```

### 变种四：同时返回被移除的原下标

扫描时收集匹配位置，并继续稳定压缩。时间 $O(n)$；除输出外额外空间 $O(1)$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  pair<int, vector<int>> removeAndReport(vector<int>& nums, int val) {
    vector<int> removedIndices;
    int write = 0;
    for (int read = 0; read < static_cast<int>(nums.size()); ++read) {
      if (nums[read] == val) {
        removedIndices.push_back(read);
      } else {
        nums[write++] = nums[read];
      }
    }
    return {write, removedIndices};
  }
};
```

## Reference

- [力扣中国官方题面](https://leetcode.cn/problems/remove-element/)

### 延伸阅读

- [官方题目](https://leetcode.cn/problems/remove-element/)
- [对应知识专题](../../basics/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="leetcode-top-32-lc22.md">← [力扣 Top 32] LC 22 括号生成 中等</a>
<a class="daily-archive-pager__next" href="leetcode-top-34-lc9.md">[力扣 Top 34] LC 9 回文数 简单 →</a>
</nav>
