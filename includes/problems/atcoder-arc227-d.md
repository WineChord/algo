<div class="problem-anchor" id="problem-atcoder-arc227-d"></div>

??? problem "AtCoder ARC227 D: Median of Binary Strings"
    [打开原题 ↗](https://atcoder.jp/contests/arc227/tasks/arc227_d?lang=en){ .problem-source }

    **难度与分值**：官方分值 700；AtCoder 未标注单题难度；AtCoder Problems 社区估算难度 2277（2026-08-20）

    **题意**：黑板上有若干等长二进制串；每次可选三个串（允许重复），加入它们逐位多数得到的新串。对每个查询串判断它是否能由这些操作产生。

    **思路**：目标可达当且仅当它在任意两坐标上的二比特模式都被某个初始串同时见证。预处理每个“坐标—比特”字面量的初始串位集；两个见证集合无交时，把对应字面量标为冲突。查询只需检查目标选择的字面量集合中是否出现冲突。

    **复杂度**：机器字时间约为 $O(NM+M^2\lceil N/64\rceil+QM\lceil2M/64\rceil)$，空间为 $O(MN+M^2)$ 位。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    constexpr int maxStrings = 500;
    constexpr int maxLength = 500;
    constexpr int maxLiterals = 1000;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, m, q;
      cin >> n >> m >> q;
      vector<array<bitset<maxStrings>, 2>> matches(m);
      for (int row = 0; row < n; ++row) {
        string source;
        cin >> source;
        for (int position = 0; position < m; ++position) {
          matches[position][source[position] - '0'].set(row);
        }
      }
      vector<array<bitset<maxLiterals>, 2>> conflicts(m);
      for (int i = 0; i < m; ++i) {
        for (int firstBit = 0; firstBit <= 1; ++firstBit) {
          for (int j = 0; j < m; ++j) {
            for (int secondBit = 0; secondBit <= 1; ++secondBit) {
              if ((matches[i][firstBit] & matches[j][secondBit]).none()) {
                conflicts[i][firstBit].set(2 * j + secondBit);
              }
            }
          }
        }
      }
      while (q--) {
        string target;
        cin >> target;
        bitset<maxLiterals> selected;
        for (int i = 0; i < m; ++i) selected.set(2 * i + target[i] - '0');
        bool possible = true;
        for (int i = 0; i < m && possible; ++i) {
          if ((conflicts[i][target[i] - '0'] & selected).any()) possible = false;
        }
        cout << (possible ? "Yes\n" : "No\n");
      }
      return 0;
    }
    ```
