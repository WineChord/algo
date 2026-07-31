---
title: "[力扣 Top 61] LC 41 缺失的第一个正数 困难"
---

# [力扣 Top 61] LC 41 缺失的第一个正数 困难

<p class="daily-archive-kicker">2026-08-01 · 第 2/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-01 题目列表</a> · <a href="../../../basics/sequence-invariants/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=cf179cb796ca9b1583d567b262af1b49b7a21a6a8d79c4b5840e79022ca1576d -->
## 官方原始信息

- Top 排名：61
- 题号：LC 41
- 官方中文标题：缺失的第一个正数
- 官方难度：困难
- 官方链接：[缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/)

### 原始题意

给定一个未排序整数数组 `nums`，返回其中没有出现的最小正整数。要求算法在线性时间内完成，并且只使用常数级额外空间。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  int firstMissingPositive(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [1,2,0]
输出：3
解释：1 和 2 都出现，首个缺失正数为 3。
```

```text
输入：nums = [3,4,-1,1]
输出：2
解释：1 出现而 2 没有出现。
```

```text
输入：nums = [7,8,9,11,12]
输出：1
解释：1 没有出现。
```

### 全部约束

- $1\le |nums|\le10^5$。
- $-2^{31}\le nums_i\le2^{31}-1$。
- 目标时间复杂度为 $O(n)$，目标额外空间复杂度为 $O(1)$。

## 约束推导与边界

长度为 $n$ 的数组即使包含 $1,2,\ldots,n$，答案也只会是 $n+1$；否则答案必在 $[1,n]$。因此，负数、零和大于 $n$ 的数都不可能直接成为答案，可以忽略。这个值域界限允许把数组下标当作哈希槽：值 $x$ 的唯一正确位置是下标 $x-1$。

重复值不能反复交换，否则会死循环；交换前必须检查目标槽中的值是否已经等于当前值。极端整数只参与范围判断，不做加减，因而没有溢出风险。

## 解法递进

### 解法一：排序后线性扫描

排序把相同值聚在一起。从候选答案 1 开始扫描：遇到相等值就把候选加一，遇到更大值即可停止。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int firstMissingPositive(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int missing = 1;
    for (int value : nums) {
      if (value == missing) {
        ++missing;
      } else if (value > missing) {
        break;
      }
    }
    return missing;
  }
};
```

时间复杂度 $O(n\log n)$，排序通常使用 $O(\log n)$ 栈空间。它正确但没有满足线性时间目标。

### 解法二：布尔标记消除排序

用长度 $n+1$ 的布尔数组记录 $[1,n]$ 中出现过的数，随后找首个未标记位置。时间降至 $O(n)$，代价是 $O(n)$ 额外空间。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int firstMissingPositive(vector<int>& nums) {
    int n = nums.size();
    vector<char> present(n + 1);
    for (int value : nums) {
      if (1 <= value && value <= n) {
        present[value] = true;
      }
    }
    for (int value = 1; value <= n; ++value) {
      if (!present[value]) {
        return value;
      }
    }
    return n + 1;
  }
};
```

### 最佳实用解：原地循环置换

扫描每个下标 `i`。只要当前值 $x$ 位于 $[1,n]$，且 `nums[x-1]` 不是 $x$，就把 $x$ 换到自己的槽位。置换完成后，第一个不满足 `nums[i]==i+1` 的下标对应答案；若全部满足则答案为 $n+1$。

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  int firstMissingPositive(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
      while (1 <= nums[i] && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
        swap(nums[i], nums[nums[i] - 1]);
      }
    }
    for (int i = 0; i < n; ++i) {
      if (nums[i] != i + 1) {
        return i + 1;
      }
    }
    return n + 1;
  }
};
```

时间复杂度 $O(n)$，额外空间复杂度 $O(1)$。虽然有嵌套 `while`，每次交换都会把至少一个合法值送入永久正确的槽位，总交换次数不超过 $n$。

## 正确性证明

对任意 $x\in[1,n]$，算法只有在槽位 $x-1$ 尚未存放 $x$ 时才把某个 $x$ 交换过去。一旦槽位 $x-1$ 得到 $x$，后续条件会阻止相同值把它换走。因此循环结束时，值 $x$ 在原数组中出现，当且仅当 `nums[x-1]==x`。

第二次扫描按 $1,2,\ldots,n$ 的顺序检查这些槽位。第一个失配位置 $i$ 表示 $i+1$ 未出现，而所有更小正数均出现，所以它正是最小缺失正数。若没有失配，$1$ 到 $n$ 全部出现，根据答案上界，最小缺失正数只能是 $n+1$。

## 样例手推

对 `[3,4,-1,1]`：

1. 下标 0 的 3 换到槽位 2，得到 `[-1,4,3,1]`；
2. 下标 1 的 4 换到槽位 3，得到 `[-1,1,3,4]`；
3. 下标 1 的 1 再换到槽位 0，得到 `[1,-1,3,4]`；
4. 扫描槽位时，位置 0 正确，位置 1 不是 2，返回 2。

最小规模 `[1]` 返回 2；全为非正数时返回 1；重复数组 `[1,1]` 不会死循环并返回 2；`[1,2,\ldots,n]` 返回 $n+1$。

## 易错点与方案比较

- 合法范围是闭区间 $[1,n]$，值 $n+1$ 不需要放入数组。
- 目标下标是 `nums[i]-1`，先做范围判断后才能访问。
- 必须检查 `nums[nums[i]-1] != nums[i]`，否则重复值会无限交换。
- 排序法最易讲，布尔标记法最易写；题目硬性要求同时达到 $O(n)$ 与 $O(1)$ 时，推荐记忆“值域受长度约束时，把数组本身当哈希表”的循环置换。

## 变种一：不允许修改输入数组

新定义：输入只读，仍求首个缺失正数。原地槽位失效，必须显式保存出现性；位图是稳定选择。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<char> present(n + 1);
  for (int i = 0; i < n; ++i) {
    long long value;
    cin >> value;
    if (1 <= value && value <= n) {
      present[value] = true;
    }
  }
  for (int value = 1; value <= n; ++value) {
    if (!present[value]) {
      cout << value << '\n';
      return 0;
    }
  }
  cout << n + 1 << '\n';
}
```

时间 $O(n)$，空间 $O(n)$；只读与常数空间无法同时由这个值域哈希思路满足。

## 变种二：输出前 $k$ 个缺失正数

新定义：除最小值外，还要按升序输出前 $k$ 个缺失正数。先完成循环置换，再收集失配槽位；若不足，则从 $n+1$ 向上补齐。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int& value : a) {
    cin >> value;
  }
  for (int i = 0; i < n; ++i) {
    while (1 <= a[i] && a[i] <= n && a[a[i] - 1] != a[i]) {
      swap(a[i], a[a[i] - 1]);
    }
  }
  vector<int> answer;
  unordered_set<int> large;
  for (int i = 0; i < n; ++i) {
    if (a[i] != i + 1) {
      answer.push_back(i + 1);
    }
    if (a[i] > n) {
      large.insert(a[i]);
    }
  }
  for (int value = n + 1; static_cast<int>(answer.size()) < k; ++value) {
    if (!large.contains(value)) {
      answer.push_back(value);
    }
  }
  for (int i = 0; i < k; ++i) {
    cout << answer[i] << (i + 1 == k ? '\n' : ' ');
  }
}
```

期望时间 $O(n+k)$，额外空间 $O(n)$；保存大于 $n$ 的原数组值是为了避免错误补出已经出现的数。

## 变种三：数据流持续追加并随时查询

新定义：每次加入一个整数后，输出当前最小缺失正数。数组槽位无法预先固定，用哈希集合保存尚未越过的正数，并让指针单调前进。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  unordered_set<long long> seen;
  long long missing = 1;
  while (q--) {
    long long value;
    cin >> value;
    if (value >= missing) {
      seen.insert(value);
    }
    while (seen.erase(missing)) {
      ++missing;
    }
    cout << missing << '\n';
  }
}
```

每个值至多插入、删除一次，期望总时间 $O(q)$，空间 $O(q)$。若需要抵抗哈希退化，可改用有序集合，复杂度为 $O(q\log q)$。

## 变种四：固定值域上的点更新与查询

新定义：数组元素会被修改，值域限定为 $[1,V]$，每次更新后求最小未出现值。原地置换不再稳定；维护每个值的频次，并用线段树寻找首个频次为零的位置。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q, valueLimit;
  cin >> n >> q >> valueLimit;
  vector<int> a(n), frequency(valueLimit + 2);
  int size = 1;
  while (size < valueLimit + 1) {
    size <<= 1;
  }
  vector<int> tree(2 * size);
  auto setLeaf = [&](int value) {
    int at = size + value - 1;
    tree[at] = frequency[value] == 0;
    for (at >>= 1; at > 0; at >>= 1) {
      tree[at] = tree[at << 1] + tree[at << 1 | 1];
    }
  };
  for (int value = 1; value <= valueLimit + 1; ++value) {
    tree[size + value - 1] = 1;
  }
  for (int at = size - 1; at > 0; --at) {
    tree[at] = tree[at << 1] + tree[at << 1 | 1];
  }
  for (int& value : a) {
    cin >> value;
    if (1 <= value && value <= valueLimit + 1) {
      ++frequency[value];
    }
  }
  for (int value = 1; value <= valueLimit + 1; ++value) {
    setLeaf(value);
  }
  while (q--) {
    int index, value;
    cin >> index >> value;
    --index;
    if (1 <= a[index] && a[index] <= valueLimit + 1) {
      --frequency[a[index]];
      setLeaf(a[index]);
    }
    a[index] = value;
    if (1 <= value && value <= valueLimit + 1) {
      ++frequency[value];
      setLeaf(value);
    }
    int at = 1;
    while (at < size) {
      at = tree[at << 1] ? at << 1 : at << 1 | 1;
    }
    cout << at - size + 1 << '\n';
  }
}
```

建树 $O(n+V\log V)$，每次更新与查询 $O(\log V)$，空间 $O(V)$。实际可批量建叶以把初始化降为 $O(n+V)$。

## 可复现验证

对长度不超过 8、元素取自 $[-3,10]$ 的随机数组，把循环置换结果与排序扫描、布尔标记逐项比较；另外覆盖全为负数、全为重复值、完整排列和含 `INT_MIN`／`INT_MAX` 的边界。所有代码按 C++23 编译。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/first-missing-positive/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/first-missing-positive/)
- [对应知识专题](../../basics/sequence-invariants.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../atcoder-abc468-g/">← [atcoder] ABC468 G Restricted Permutation</a>
<a class="daily-archive-pager__next" href="../leetcode-top-62-lc105/">[力扣 Top 62] LC 105 从前序与中序遍历序列构造二叉树 中等 →</a>
</nav>
