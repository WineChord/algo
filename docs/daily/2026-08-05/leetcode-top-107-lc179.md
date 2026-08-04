---
title: "[力扣 Top 107] LC 179 最大数 中等"
---

# [力扣 Top 107] LC 179 最大数 中等

<p class="daily-archive-kicker">2026-08-05 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-05 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=87377ab796d880889280467cb52467919baef13f1ea384e38b3f67fe3ab96883 -->
## 官方原始信息

- Top 排名：107
- 题号：LC 179
- 官方中文标题：最大数
- 官方难度：中等
- 官方链接：[最大数](https://leetcode.cn/problems/largest-number/)

### 原始题意

给定一组非负整数，重新排列所有整数的顺序并直接拼接，使所得整数最大。由于结果可能很长，返回字符串。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string largestNumber(vector<int>& nums);
};
```

### 全部官方样例

```text
输入：nums = [10,2]
输出："210"
```

```text
输入：nums = [3,30,34,5,9]
输出："9534330"
```

### 全部约束

- $1\le nums.length\le100$。
- $0\le nums[i]\le10^9$。

## 约束推导与观察

把元素转成字符串后，两个块 `a`、`b` 的相对顺序只可能形成 `a+b` 或 `b+a`。若前者字典序更大，就必须把 `a` 放前；十进制串等长比较与数值比较一致。这个局部比较恰能定义全局排序，而按整数值或首字符排序都会在 `3` 与 `30` 等情况失效。

结果长度最多约 1000，必须直接拼接字符串。若最大块为 `"0"`，所有块都是零，应统一返回一个 `"0"`。

## 解法递进

### 解法一：枚举全部排列

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string largestNumber(vector<int>& nums) {
    vector<string> values;
    for (int value : nums) {
      values.push_back(to_string(value));
    }
    sort(values.begin(), values.end());
    string answer;
    do {
      string candidate;
      for (const string& value : values) {
        candidate += value;
      }
      answer = max(answer, candidate);
    } while (next_permutation(values.begin(), values.end()));
    size_t first = answer.find_first_not_of('0');
    return first == string::npos ? "0" : answer.substr(first);
  }
};
```

时间 $O(n!\cdot nL)$，空间 $O(nL)$，只适合极小输入。重复枚举的根因是没有利用两块交换的局部结构。

### 最佳实用解：按 `a+b > b+a` 排序

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string largestNumber(vector<int>& nums) {
    vector<string> values;
    values.reserve(nums.size());
    for (int value : nums) {
      values.push_back(to_string(value));
    }
    sort(values.begin(), values.end(),
        [](const string& a, const string& b) { return a + b > b + a; });
    if (values[0] == "0") {
      return "0";
    }
    string answer;
    for (const string& value : values) {
      answer += value;
    }
    return answer;
  }
};
```

设总数字字符数为 $L$、单块最大长度为 $w$，时间 $O(n\log n\cdot w+L)$，空间 $O(L)$。在本题约束下 $w\le10$。

## 正确性证明

若某排列中相邻块为 `a,b` 且 `b+a > a+b`，交换它们后，结果在此前公共前缀不变，并在这两块覆盖的第一处差异变大，因此原排列不可能最优。排序后的序列不存在这样的逆序相邻对，所以任何相邻交换都不能改善它。另一方面，比较 `a+b` 与 `b+a` 等价于比较两个无限周期串 `aaaa...` 与 `bbbb...` 的前 $|a|+|b|$ 个字符，因而关系具有传递性，能形成合法严格弱序。故排序结果为全局最大拼接。

## 样例手推

`3` 与 `30` 比较 `330 > 303`，所以 3 在前；`34` 与 3 比较 `343 > 334`，所以 34 在前。继续比较得到 `9,5,34,3,30`，拼接为 `9534330`。`[0,0]` 排序后首项为 0，返回单个 `0`。

## 易错点与方案比较

- 不能按整数大小、字符串长度或首字符单独排序。
- 比较器必须用严格 `>`，不能用 `>=`，否则违反排序器契约。
- 不要把超长结果转换回整数。
- 全零时需规范化；其他情况不能随意删除内部零。

## 变种一：拼接得到最小非负整数

新定义：目标改为最小拼接，比较器反向；若允许前导零，直接拼接即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<string> values(n);
  for (string& value : values) {
    cin >> value;
  }
  sort(
      values.begin(), values.end(), [](const string& a, const string& b) { return a + b < b + a; });
  for (const string& value : values) {
    cout << value;
  }
  cout << '\n';
}
```

时间 $O(n\log n\cdot w)$，空间 $O(L)$。若禁止前导零，必须先选择第一个非零块，原比较器不能直接覆盖该额外约束。

## 变种二：在任意进制下拼接最大数字

新定义：输入已是合法的 $2\le B\le36$ 进制大写数字串。数位字符顺序固定为 `0-9A-Z`，同样比较两种拼接即可。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int base, n;
  cin >> base >> n;
  static_cast<void>(base);
  vector<string> values(n);
  for (string& value : values) {
    cin >> value;
  }
  sort(
      values.begin(), values.end(), [](const string& a, const string& b) { return a + b > b + a; });
  if (values[0] == "0") {
    cout << "0\n";
    return 0;
  }
  for (const string& value : values) {
    cout << value;
  }
  cout << '\n';
}
```

时间与十进制相同。关键是字符编码必须与数位大小顺序一致；小写或自定义字母表需显式映射。

## 变种三：返回原下标的确定性顺序

新定义：若 `a+b == b+a`，按原下标小者优先，并返回下标排列。次级规则不改变拼接值，但让结果可复现。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  vector<pair<string, int>> values;
  for (int index = 0, value; index < n; ++index) {
    cin >> value;
    values.push_back({to_string(value), index});
  }
  sort(values.begin(), values.end(), [](const auto& a, const auto& b) {
    string ab = a.first + b.first;
    string ba = b.first + a.first;
    return ab != ba ? ab > ba : a.second < b.second;
  });
  for (int i = 0; i < n; ++i) {
    cout << values[i].second << (i + 1 == n ? '\n' : ' ');
  }
}
```

时间 $O(n\log n\cdot w)$，空间 $O(L+n)$。原题只要求字符串，不需要这个稳定身份契约。

## 变种四：求字典序第 `k` 大的拼接排列

新定义：$n\le9$，元素按下标视为不同，求全部排列中第 `k` 大拼接。局部贪心只给最大值，不再给完整排名；在小规模下枚举每个下标排列，生成拼接串后统一排序。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  unsigned long long k;
  cin >> n >> k;
  vector<string> value(n);
  for (string& item : value) {
    cin >> item;
  }
  vector<int> order(n);
  iota(order.begin(), order.end(), 0);
  vector<string> arrangements;
  do {
    string joined;
    for (int index : order) {
      joined += value[index];
    }
    arrangements.push_back(joined);
  } while (next_permutation(order.begin(), order.end()));
  sort(arrangements.begin(), arrangements.end(), greater<>());
  if (k == 0 || k > arrangements.size()) {
    cout << "INVALID\n";
  } else {
    cout << arrangements[k - 1] << '\n';
  }
}
```

若拼接串长为 $L$，时间 $O(n!\cdot(L+\log(n!)\cdot L))$，空间 $O(n!\cdot L)$。重复数字仍按原下标区分，因此相同字符串可以占据多个名次；`k` 必须满足 $1\le k\le n!$。

## 验证说明

本轮将六段代码按 C++23 编译；排序解会与全排列 oracle 对拍 20,000 个 $n\le8$ 的随机数组，并重点覆盖 `3/30/34`、重复块、不同长度、全零与 `121/12`。比较器额外检查反对称性和传递性。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/largest-number/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-106-lc287/">← [力扣 Top 106] LC 287 寻找重复数 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-108-lc202/">[力扣 Top 108] LC 202 快乐数 简单 →</a>
</nav>
