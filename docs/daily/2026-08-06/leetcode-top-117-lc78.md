---
title: "[力扣 Top 117] LC 78 子集 中等"
---

# [力扣 Top 117] LC 78 子集 中等

<p class="daily-archive-kicker">2026-08-06 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-06 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=451845af6c9c85b3f65287c1f71adc5264185a7e5d4f4c9e2958099956fabede -->
## 官方原始信息

- Top 排名：117
- 题号：LC 78
- 官方中文标题：子集
- 官方难度：中等
- 官方链接：[子集](https://leetcode.cn/problems/subsets/)

### 原始题意、签名、样例与约束

给定元素互不相同的数组，返回全部子集，顺序任意且不得重复。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<vector<int>> subsets(vector<int>& nums);
};
```

```text
[1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
[0] -> [[],[0]]
```

- $1\le n\le10$，$-10\le nums_i\le10$，元素两两不同。

## 约束推导与观察

每个元素只有选或不选两种独立决策，所以答案必有 $2^n$ 个子集；仅输出本身就需 $\Theta(n2^n)$ 个元素量，指数复杂度不可避免。关键是保证每条决策路径只对应一个子集。

## 解法递进

### 解法一：二进制掩码枚举

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<vector<int>> subsets(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> answer;
    for (int mask = 0; mask < (1 << n); ++mask) {
      vector<int> subset;
      for (int i = 0; i < n; ++i) {
        if (mask >> i & 1) {
          subset.push_back(nums[i]);
        }
      }
      answer.push_back(move(subset));
    }
    return answer;
  }
};
```

时间 $O(n2^n)$，输出外空间 $O(n)$。

### 最佳实用解：回溯决策树

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer;
  vector<int> path;
  void dfs(const vector<int>& nums, int index) {
    if (index == static_cast<int>(nums.size())) {
      answer.push_back(path);
      return;
    }
    dfs(nums, index + 1);
    path.push_back(nums[index]);
    dfs(nums, index + 1);
    path.pop_back();
  }
public:
  vector<vector<int>> subsets(vector<int>& nums) {
    dfs(nums, 0);
    return answer;
  }
};
```

时间 $O(n2^n)$，递归与路径空间 $O(n)$。掩码法常数小；回溯更容易加入剪枝、固定大小等限制，面试优先记忆回溯模型。

## 正确性证明

深度 `i` 决定是否选 `nums[i]`。任一叶子对应一个长度为 `n` 的布尔选择向量，从而唯一确定一个子集；反之任一子集按其是否包含每个互异元素，唯一确定一条根到叶路径。因此算法既不遗漏也不重复，叶子收集结果恰为幂集。

## 样例手推

对 `[1,2]`，决策依次生成 `[]`、`[2]`、`[1]`、`[1,2]`。空集来自全部不选，全集来自全部选。`n=10` 时恰产生 1024 个子集。

## 易错点与方案比较

- 入答案时必须复制 `path`，不能保存同一可变引用。
- 选择分支返回后必须 `pop_back` 恢复状态。
- `1<<n` 在本题安全；更大 `n` 应使用 `1ULL<<n`，但输出也会先爆炸。
- 输入互异，因此原题无需排序去重。

## 变种一：输入可能含重复元素

对应 [LC 90 子集 II](https://leetcode.cn/problems/subsets-ii/)。排序后，同层只选择每个值的第一次出现。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer;
  vector<int> path;
  void dfs(const vector<int>& nums, int start) {
    answer.push_back(path);
    for (int i = start; i < static_cast<int>(nums.size()); ++i) {
      if (i > start && nums[i] == nums[i - 1]) {
        continue;
      }
      path.push_back(nums[i]);
      dfs(nums, i + 1);
      path.pop_back();
    }
  }
public:
  vector<vector<int>> subsetsWithDup(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    dfs(nums, 0);
    return answer;
  }
};
```

时间 $O(n2^n)$ 上界，空间 $O(n)$。

## 变种二：只输出大小为 `k` 的子集

对应 [LC 77 组合](https://leetcode.cn/problems/combinations/)。剩余元素不足时剪枝。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  vector<vector<int>> answer;
  vector<int> path;
  void dfs(int n, int k, int start) {
    if (static_cast<int>(path.size()) == k) {
      answer.push_back(path);
      return;
    }
    int need = k - path.size();
    for (int value = start; value <= n - need + 1; ++value) {
      path.push_back(value);
      dfs(n, k, value + 1);
      path.pop_back();
    }
  }
public:
  vector<vector<int>> combine(int n, int k) {
    dfs(n, k, 1);
    return answer;
  }
};
```

时间与输出规模同阶 $O(k\binom nk)$，空间 $O(k)$。

## 变种三：统计和等于目标的子集数量

新定义：元素可为负，`n<=40`，只计数不恢复。拆成两半枚举子集和，再二分配对。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<long long> allSums(const vector<int>& a) {
  vector<long long> sums(1, 0);
  for (int value : a) {
    int size = sums.size();
    for (int i = 0; i < size; ++i) {
      sums.push_back(sums[i] + value);
    }
  }
  return sums;
}
int main() {
  int n;
  long long target;
  cin >> n >> target;
  vector<int> left(n / 2), right(n - n / 2);
  for (int& x : left) {
    cin >> x;
  }
  for (int& x : right) {
    cin >> x;
  }
  vector<long long> a = allSums(left);
  vector<long long> b = allSums(right);
  sort(b.begin(), b.end());
  long long answer = 0;
  for (long long sum : a) {
    auto range = equal_range(b.begin(), b.end(), target - sum);
    answer += range.second - range.first;
  }
  cout << answer << '\n';
}
```

时间 $O(2^{n/2}n)$，空间 $O(2^{n/2})$。

## 变种四：Gray Code 顺序遍历所有子集

新定义：相邻输出子集只改变一个元素。第 `i` 个 Gray 码为 `i^(i>>1)`。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int& x : a) {
    cin >> x;
  }
  int previous = 0;
  set<int> current;
  for (int i = 0; i < (1 << n); ++i) {
    int gray = i ^ (i >> 1);
    int changed = gray ^ previous;
    if (changed) {
      int bit = countr_zero(static_cast<unsigned>(changed));
      if (gray >> bit & 1) {
        current.insert(a[bit]);
      } else {
        current.erase(a[bit]);
      }
    }
    for (int value : current) {
      cout << value << ' ';
    }
    cout << '\n';
    previous = gray;
  }
}
```

状态更新 $O(\log n)$，总输出仍受 $\Theta(n2^n)$ 限制。

## 可复现验证

枚举 `n<=10` 的随机互异数组，分别把掩码法与回溯法结果中的每个子集排序，再把全集排序比较；检查结果数为 $2^n$ 且无重复。变种分别对照暴力计数。全部代码重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/subsets/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-116-lc203/">← [力扣 Top 116] LC 203 移除链表元素 简单</a>
<a class="daily-archive-pager__next" href="../leetcode-top-118-lc91/">[力扣 Top 118] LC 91 解码方法 中等 →</a>
</nav>
