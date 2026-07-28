# 字符串算法知识地图

字符串问题常把“字符相等比较”扩展为前缀、模式、字典和周期结构。先区分任务是单模式匹配、多模式匹配、字典查询、子串比较，还是全局后缀关系。

## 总览

| 任务 | 常用算法 | 典型复杂度 |
| --- | --- | --- |
| 单模式匹配 | KMP、Z 函数 | $O(n+m)$ |
| 多模式匹配 | Trie、AC 自动机 | 与文本长度和匹配数相关 |
| 子串相等判断 | 字符串哈希 | 预处理 $O(n)$，查询 $O(1)$ 期望 |
| 回文半径 | Manacher | $O(n)$ |
| 全部后缀排序 | 后缀数组 | 常见 $O(n\log n)$ |
| 后缀集合与在线扩展 | 后缀自动机 | $O(n)$ 状态量级 |

## KMP：在失配时复用已知前缀

朴素匹配在失配后把模式串整体右移，并重复比较已经知道相等的字符。KMP 用前缀函数 `pi[i]` 记录：

> `s[0..i]` 的最长真前缀长度，且这个前缀也是后缀。

失配时跳到更短的可行 border，而不是让文本指针回退。

下面返回模式串在文本中的所有起始位置：

```cpp
#include <bits/stdc++.h>
using namespace std;
vector<int> kmp(string_view text, string_view pat) {
    if (pat.empty()) return {};
    int m = pat.size();
    vector<int> pi(m), ans;
    for (int i = 1, j = 0; i < m; ++i) {
        while (j && pat[i] != pat[j]) j = pi[j - 1];
        if (pat[i] == pat[j]) ++j;
        pi[i] = j;
    }
    for (int i = 0, j = 0; i < (int)text.size(); ++i) {
        while (j && text[i] != pat[j]) j = pi[j - 1];
        if (text[i] == pat[j]) ++j;
        if (j == m) ans.push_back(i - m + 1), j = pi[j - 1];
    }
    return ans;
}
int main() {
    string text, pattern;
    cin >> text >> pattern;
    for (int p : kmp(text, pattern)) cout << p << ' ';
    cout << '\n';
}
```

每次回退虽然可能跳多步，但指针总增量和总回退量都是线性，时间 $O(n+m)$，空间 $O(m)$。

代表题目：

--8<-- "includes/problems/lc-28.md"

--8<-- "includes/problems/lc-459.md"

--8<-- "includes/problems/luogu-p3375.md"

## Trie

Trie 把公共前缀合并成路径，适合：

- 插入和查询字典单词；
- 前缀计数；
- 最大异或配对的 01-Trie；
- 作为 AC 自动机的字典结构。

若字符集固定且较小，可以用数组存儿子，速度快但空间大；字符集稀疏时可使用映射。必须区分“路径存在”和“某个单词在此结束”。

--8<-- "includes/problems/lc-208.md"

--8<-- "includes/problems/lc-421.md"

## 公共前缀

最长公共前缀可以逐列验证：一旦某个字符串结束或字符不同，任何更长前缀都不可能成立。检查工作不会超过实际访问过的字符总数。

--8<-- "includes/problems/lc-14.md"

## 字符串哈希

多项式滚动哈希把字符串映射为整数，可在 $O(1)$ 时间比较子串哈希。它简单高效，但哈希碰撞意味着通常是概率正确。

提高可靠性的方式：

- 双模哈希；
- 64 位自然溢出配合随机基数；
- 哈希筛选后，在必要时做字符级确认。

安全性要求高或存在对抗输入时，优先考虑确定性算法，不能把“碰撞概率低”写成“绝不碰撞”。

## AC 自动机

AC 自动机把多个模式串插入 Trie，再建立类似 KMP 的失配指针。扫描文本时同时推进所有可能模式，适合敏感词匹配、字典模式计数等多模式任务。

复杂度通常写作

$$
O\!\left(\sum |\mathrm{pattern}|+|\mathrm{text}|+\mathrm{matches}\right),
$$

具体还取决于字符集和如何统计输出。

--8<-- "includes/problems/luogu-p3808.md"

## 回文与后缀结构

- 回文判断少量询问可用双指针；
- 大量静态回文查询可用哈希；
- 所有中心的最长回文半径用 Manacher；
- 给定字符多重集合构造最小回文时，先把完整答案降维到左半边；
- 需要比较后缀、统计不同子串或求最长重复子串时，考虑后缀数组或后缀自动机。

最长回文子串从三次暴力、区间 DP、中心扩展到 Manacher 的推导与约束变种，见[回文：区间状态、中心与线性半径](palindrome-centers.md)。

字符频次、字典序最小构造、多重集合第 $k$ 个答案与相邻交换成本，见[回文重排：把完整字符串降维到左半边](palindrome-rearrangements.md)。

代表题目：

--8<-- "includes/problems/lc-5.md"

--8<-- "includes/problems/lc-214.md"

--8<-- "includes/problems/lc-1044.md"

--8<-- "includes/problems/lc-3517.md"

## 易错检查

- 处理的是字节、ASCII 字符还是 Unicode 码点；
- 空模式串语义是否明确；
- `pi`、下标和答案位置是 0-based 还是 1-based；
- Trie 节点是否标记单词结束；
- 哈希减法是否规范成非负；
- 多模式统计是否会沿失配树重复或遗漏；
- 总字符串长度限制是否比单个字符串限制更关键。
