---
title: "[力扣 Top 56] LC 17 电话号码的字母组合 中等"
---

# [力扣 Top 56] LC 17 电话号码的字母组合 中等

<p class="daily-archive-kicker">2026-07-31 · 第 7/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-07-31 题目列表</a> · <a href="../../../search/backtracking/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=2a3fcb52558eb08b0196395663dd8b58ad1e8ea02bba7a40b73adcb543823ec6 -->
## 官方原始信息

- Top 排名：56
- 题号：LC 17
- 官方中文标题：电话号码的字母组合
- 官方难度：中等
- 官方链接：[电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

### 原始题意

给定只含数字 2 到 9 的字符串 `digits`，按照传统电话键盘映射，返回所有可能的字母组合，顺序不限。数字不映射到自身。

### 函数签名

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  vector<string> letterCombinations(string digits);
};
```

### 全部官方样例

```text
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

```text
输入：digits = "2"
输出：["a","b","c"]
```

### 全部约束

- $1\le |digits|\le4$。
- `digits[i]` 取自字符 `'2'` 到 `'9'`。

## 约束推导与边界

每一位独立选择对应按键上的一个字母，答案是若干集合的笛卡尔积。最大输出数为 $4^4=256$，因此回溯可以直接生成全部答案。复杂度下界就是输出字符总数；优化目标是只走合法分支，而不是枚举 26 个字母再过滤。

## 解法递进

### 解法一：枚举所有小写字符串后过滤

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  vector<string> letterCombinations(string digits) {
    const vector<string> letters = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> answer;
    long long total = 1;
    for (int i = 0; i < static_cast<int>(digits.size()); ++i) {
      total *= 26;
    }
    for (long long mask = 0; mask < total; ++mask) {
      long long value = mask;
      string candidate(digits.size(), 'a');
      for (int i = static_cast<int>(digits.size()) - 1; i >= 0; --i) {
        candidate[i] = static_cast<char>('a' + value % 26);
        value /= 26;
      }
      bool valid = true;
      for (int i = 0; i < static_cast<int>(digits.size()); ++i) {
        if (letters[digits[i] - '0'].find(candidate[i]) == string::npos) {
          valid = false;
        }
      }
      if (valid) {
        answer.push_back(candidate);
      }
    }
    return answer;
  }
};
```

时间 $O(n26^n)$，空间不计输出为 $O(n)$。

### 最佳实用解：按位回溯生成笛卡尔积

<!-- compile:leetcode -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
  const vector<string> letters = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
  vector<string> answer;
  string current;
  void search(const string& digits, int index) {
    if (index == static_cast<int>(digits.size())) {
      answer.push_back(current);
      return;
    }
    for (char letter : letters[digits[index] - '0']) {
      current.push_back(letter);
      search(digits, index + 1);
      current.pop_back();
    }
  }
public:
  vector<string> letterCombinations(string digits) {
    search(digits, 0);
    return answer;
  }
};
```

若答案数为 $P$，时间 $O(nP)$，递归空间 $O(n)$，输出空间 $O(nP)$。

## 正确性证明

递归第 `index` 层只从 `digits[index]` 对应字母集合中选一个字符，因此叶子字符串每一位都合法。反过来，任意合法组合在每一层都有唯一对应的字符选择，递归会沿这条唯一路径到达叶子，所以没有遗漏或重复。到达深度 `n` 时恰好选了每一位的一个字母，收集结果正确。

## 样例手推

`"23"` 的第一层选择 `a、b、c`；每个分支的第二层再选择 `d、e、f`。深度优先遍历依次得到 `ad、ae、af、bd、be、bf、cd、ce、cf`。

## 易错点与方案比较

- 数字字符转下标要用 `digits[i] - '0'`。
- 按键 7 和 9 各有 4 个字母，不能假设每层固定 3 个分支。
- 官方约束保证输入非空；若复用到允许空串的接口，应先约定返回空数组还是含空串的数组。
- 回溯复杂度与输出下界同阶，是应优先记忆的写法。

## 变种一：键盘映射由输入给定

读入 10 个映射串；任一数字映射为空时结果为空。算法仍是笛卡尔积回溯。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
vector<string> mapping(10);
vector<string> answer;
string current;
void search(const string& digits, int index) {
  if (index == static_cast<int>(digits.size())) {
    answer.push_back(current);
    return;
  }
  for (char letter : mapping[digits[index] - '0']) {
    current.push_back(letter);
    search(digits, index + 1);
    current.pop_back();
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  for (string& letters : mapping) {
    cin >> letters;
    if (letters == "-") {
      letters.clear();
    }
  }
  string digits;
  cin >> digits;
  search(digits, 0);
  for (const string& value : answer) {
    cout << value << '\n';
  }
}
```

时间与输出字符总数同阶，递归空间 $O(n)$。

## 变种二：只求组合数量

不生成字符串，直接把每个按键的字母数相乘；使用大整数题可再换成任意精度类型。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const vector<int> count = {0, 0, 3, 3, 3, 3, 3, 4, 3, 4};
  string digits;
  cin >> digits;
  unsigned long long answer = 1;
  for (char digit : digits) {
    answer *= count[digit - '0'];
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(1)$。

## 变种三：返回字典序第 k 个组合

各映射串已按字母升序排列。用后缀组合数把一基的 `k` 转成混合进制下标，无需枚举前面的答案。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const vector<string> letters = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
  string digits;
  unsigned long long k;
  cin >> digits >> k;
  int n = digits.size();
  vector<unsigned long long> suffix(n + 1, 1);
  for (int i = n - 1; i >= 0; --i) {
    suffix[i] = suffix[i + 1] * letters[digits[i] - '0'].size();
  }
  if (k < 1 || k > suffix[0]) {
    cout << -1 << '\n';
    return 0;
  }
  --k;
  string answer;
  for (int i = 0; i < n; ++i) {
    unsigned long long index = k / suffix[i + 1];
    answer.push_back(letters[digits[i] - '0'][index]);
    k %= suffix[i + 1];
  }
  cout << answer << '\n';
}
```

时间 $O(n)$，空间 $O(n)$。

## 变种四：T9 字典筛选

只返回词典中与数字串完全匹配的单词。此时遍历词典比生成所有组合后查词典更直接。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  const string keyOf = "22233344455566677778889999";
  string digits;
  int dictionarySize;
  cin >> digits >> dictionarySize;
  while (dictionarySize--) {
    string word;
    cin >> word;
    bool matches = word.size() == digits.size();
    for (int i = 0; matches && i < static_cast<int>(word.size()); ++i) {
      matches = keyOf[word[i] - 'a'] == digits[i];
    }
    if (matches) {
      cout << word << '\n';
    }
  }
}
```

时间为词典总字符数，额外空间 $O(1)$。

## 可复现验证

枚举所有长度 1 到 4 的数字串，把回溯结果与迭代笛卡尔积结果排序后比较，并检查结果数量等于各按键字母数之积。另对第 k 个组合逐项与完整排序结果核对。

## 来源

- [力扣中国官方题面](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)
- [对应知识专题](../../search/backtracking.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-55-lc131/">← [力扣 Top 55] LC 131 分割回文串 中等</a>
<a class="daily-archive-pager__next" href="../leetcode-top-57-lc76/">[力扣 Top 57] LC 76 最小覆盖子串 困难 →</a>
</nav>
