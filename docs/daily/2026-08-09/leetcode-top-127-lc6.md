---
title: "[力扣 Top 127] LC 6 Z 字形变换 中等"
---

# [力扣 Top 127] LC 6 Z 字形变换 中等

<p class="daily-archive-kicker">2026-08-09 · 第 8/14 题 · 力扣 Top</p>

<p class="daily-archive-utility"><a href="../">返回 2026-08-09 题目列表</a> · <a href="../../../strings/">进入知识专题</a></p>

<!-- DAILY_CANONICAL_BODY_START sha256=8442da6e4ac75383f13386dca665e4db9a8b7be7cf78c19b1adbdb0bd8e12e13 -->
## 官方原始信息

- Top 排名：127
- 题号：LC 6
- 官方中文标题：Z 字形变换
- 官方难度：中等
- 官方链接：[Z 字形变换](https://leetcode.cn/problems/zigzag-conversion/)

### 原始题意与函数签名

把字符串 `s` 按给定行数从上到下、再斜向上循环排列，最后逐行读取并返回结果。

<!-- compile:leetcode -->
```cpp
class Solution {
public:
  string convert(string s, int numRows);
};
```

### 全部官方样例

```text
输入：s = "PAYPALISHIRING", numRows = 3
输出："PAHNAPLSIIGYIR"
排列：
P   A   H   N
A P L S I I G
Y   I   R
```

```text
输入：s = "PAYPALISHIRING", numRows = 4
输出："PINALSIGYAHRPI"
排列：
P     I     N
A   L S   I G
Y A   H R
P     I
```

```text
输入：s = "A", numRows = 1
输出："A"
```

### 全部约束

- $1\le |s|\le1000$。
- `s` 由英文字母、逗号和句点组成。
- $1\le numRows\le1000$。

## 约束推导与观察

当行数为 $r>1$ 时，行号按 `0,1,...,r-1,r-2,...,1` 周期变化，周期长度为 $p=2r-2$。问题不要求还原二维空格，只要把每个字符送入对应行，再按行拼接。`r=1` 时周期为 0，必须单独返回。

## 解法递进

### 解法一：显式模拟二维画布

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string convert(string s, int numRows) {
    if (numRows == 1 || numRows >= static_cast<int>(s.size())) {
      return s;
    }
    int n = s.size();
    vector<vector<char>> canvas(numRows, vector<char>(n, '\0'));
    int row = 0;
    int column = 0;
    int direction = 1;
    for (char ch : s) {
      canvas[row][column] = ch;
      if (row == 0) {
        direction = 1;
      } else if (row == numRows - 1) {
        direction = -1;
      }
      if (direction == 1) {
        ++row;
      } else {
        --row;
        ++column;
      }
    }
    string answer;
    for (const auto& line : canvas) {
      for (char ch : line) {
        if (ch != '\0') {
          answer.push_back(ch);
        }
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(rn)$（扫描画布）、空间 $O(rn)$，直观但存了大量空格。

### 解法二：只保存实际行字符串

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string convert(string s, int numRows) {
    if (numRows == 1 || numRows >= static_cast<int>(s.size())) {
      return s;
    }
    vector<string> rows(numRows);
    int row = 0;
    int direction = 1;
    for (char ch : s) {
      rows[row].push_back(ch);
      if (row == 0) {
        direction = 1;
      } else if (row == numRows - 1) {
        direction = -1;
      }
      row += direction;
    }
    string answer;
    for (const string& line : rows) {
      answer += line;
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n)$、空间 $O(n)$。状态机写法最易理解。

### 最佳实用解：按周期直接枚举原下标

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
  string convert(string s, int numRows) {
    if (numRows == 1 || numRows >= static_cast<int>(s.size())) {
      return s;
    }
    int period = 2 * numRows - 2;
    string answer;
    answer.reserve(s.size());
    for (int row = 0; row < numRows; ++row) {
      for (int base = row; base < static_cast<int>(s.size()); base += period) {
        answer.push_back(s[base]);
        int diagonal = base + period - 2 * row;
        if (row != 0 && row != numRows - 1 && diagonal < static_cast<int>(s.size())) {
          answer.push_back(s[diagonal]);
        }
      }
    }
    return answer;
  }
};
int main() {
}
```

时间 $O(n)$、输出外空间 $O(1)$。它直接按照最终输出顺序访问原串，常数和额外空间最小；状态机版更直观，公式版更适合追求空间。

## 正确性证明

周期 `period=2r-2` 内，字符下标 `q` 的行号为 `min(q,period-q)`。对固定行 `row`，竖直字符下标是 `row+t*period`；非首尾行还有同周期的斜线字符 `t*period+period-row`，即代码中的 `base+period-2*row`。算法按行从上到下、每行按原出现顺序枚举这两类下标，恰等于逐行读取 Z 字形，且每个原下标在唯一一行出现一次。

## 样例手推

三行时周期为 4。第 0 行取下标 `0,4,8,12` 得到 `PAHN`；第 1 行交替取 `1,3,5,7,9,11,13` 得到 `APLSIIG`；第 2 行取 `2,6,10` 得到 `YIR`，拼接即官方答案。

## 易错点与方案比较

- `numRows=1` 时周期为 0，必须提前返回。
- 首行和末行没有斜线字符，不能重复加入。
- 当 `numRows>=|s|` 时每个字符独占一行，结果就是原串。
- 公式中的斜线下标是 `base+period-2*row`，且需要边界判断。

## 变种一：反向还原原字符串

新定义：给定变换结果、原行数，恢复变换前字符串。先计算每个原位置所属行的长度，再把结果切给各行并按原行号轨迹取回。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string inverseZigzag(const string& encoded, int rows) {
  int n = encoded.size();
  if (rows == 1 || rows >= n) {
    return encoded;
  }
  int period = 2 * rows - 2;
  vector<int> rowOf(n), count(rows);
  for (int i = 0; i < n; ++i) {
    int q = i % period;
    rowOf[i] = min(q, period - q);
    ++count[rowOf[i]];
  }
  vector<string> buckets(rows);
  int offset = 0;
  for (int row = 0; row < rows; ++row) {
    buckets[row] = encoded.substr(offset, count[row]);
    offset += count[row];
  }
  vector<int> used(rows);
  string original;
  for (int row : rowOf) {
    original.push_back(buckets[row][used[row]++]);
  }
  return original;
}
int main() {
  cout << inverseZigzag("PAHNAPLSIIGYIR", 3) << '\n';
}
```

时间 $O(n)$、空间 $O(n)$。

## 变种二：只查询输出位置 `k` 的字符

新定义：不构造完整输出，只求逐行结果的第 `k` 个字符。逐行计数并枚举该行下标，空间降为常数。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
char zigzagAt(const string& s, int rows, int k) {
  if (rows == 1 || rows >= static_cast<int>(s.size())) {
    return s.at(k);
  }
  int period = 2 * rows - 2;
  for (int row = 0; row < rows; ++row) {
    for (int base = row; base < static_cast<int>(s.size()); base += period) {
      if (k-- == 0) {
        return s[base];
      }
      int diagonal = base + period - 2 * row;
      if (row != 0 && row != rows - 1 && diagonal < static_cast<int>(s.size())) {
        if (k-- == 0) {
          return s[diagonal];
        }
      }
    }
  }
  throw out_of_range("k");
}
int main() {
  cout << zigzagAt("PAYPALISHIRING", 3, 0) << '\n';
}
```

单次查询最坏 $O(n)$、空间 $O(1)$；大量查询应预处理下标映射。

## 变种三：按 Unicode 码点而非 UTF-8 字节变换

新定义：输入已解码为 `u32string`，每个 Unicode 码点视作一个字符，避免把多字节 UTF-8 编码拆开。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
u32string convertCodePoints(const u32string& s, int rows) {
  if (rows == 1 || rows >= static_cast<int>(s.size())) {
    return s;
  }
  vector<u32string> lines(rows);
  int row = 0;
  int direction = 1;
  for (char32_t codePoint : s) {
    lines[row].push_back(codePoint);
    if (row == 0) {
      direction = 1;
    } else if (row == rows - 1) {
      direction = -1;
    }
    row += direction;
  }
  u32string result;
  for (const auto& line : lines) {
    result += line;
  }
  return result;
}
int main() {
  cout << convertCodePoints(U"算法竞赛", 2).size() << '\n';
}
```

时间 $O(n)$、空间 $O(n)$；UTF-8 与 UTF-32 的编解码属于接口层，应在调用前后完成。

## 变种四：行数随周期使用自定义轨迹

新定义：给定一个合法行号周期 `pattern`，字符依次落入这些行。经典 Z 字形只是 `0,1,...,r-1,...,1` 的特例。

<!-- compile:standalone -->
```cpp
#include <bits/stdc++.h>
using namespace std;
string convertByPattern(const string& s, int rows, const vector<int>& pattern) {
  if (pattern.empty()) {
    return s;
  }
  vector<string> buckets(rows);
  for (int i = 0; i < static_cast<int>(s.size()); ++i) {
    int row = pattern[i % pattern.size()];
    if (row < 0 || row >= rows) {
      throw invalid_argument("row");
    }
    buckets[row].push_back(s[i]);
  }
  string answer;
  for (const string& row : buckets) {
    answer += row;
  }
  return answer;
}
int main() {
  cout << convertByPattern("abcdef", 3, {0, 2, 1, 2}) << '\n';
}
```

时间 $O(n)$、空间 $O(n)$；直接下标公式通常不再有简单闭式，行桶模拟更稳健。

## 可复现验证

枚举字符串长度 $1..80$ 与行数 $1..90$，以二维画布为 oracle，对比行桶和周期公式；并验证 `inverseZigzag(convert(s,r),r)==s`。所有代码块重新通过 GNU++23 编译。
<!-- DAILY_CANONICAL_BODY_END -->

## Reference

- [官方题目](https://leetcode.cn/problems/zigzag-conversion/)
- [对应知识专题](../../strings/index.md)

<nav class="daily-archive-pager" aria-label="当日题目导航">
<a class="daily-archive-pager__previous" href="../leetcode-top-126-lc295/">← [力扣 Top 126] LC 295 数据流的中位数 困难</a>
<a class="daily-archive-pager__next" href="../leetcode-top-128-lc93/">[力扣 Top 128] LC 93 复原 IP 地址 中等 →</a>
</nav>
