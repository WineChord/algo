<div class="problem-anchor" id="problem-codeforces-2247-d2"></div>

??? problem "CF Round 1111 · Div.2 D2 · XOR Sorting (Hard Version) (2247D2)"
    [打开原题 ↗](https://codeforces.com/contest/2247/problem/D2){ .problem-source }

    **难度与分值**：Codeforces 官方 1250 分；官方 API 暂未给出 problem rating，标签为 `bitmasks`、`data structures`、`greedy`。

    **题意**：允许交换满足 $(i\mathbin{\mathrm{XOR}}j)\le k$ 的下标元素；初始状态及每次点赋值后，求把数组排成非降序所需的最小 $k$。

    **思路**：答案是 0 或二的幂。线段树每个对齐二进制块维护最小值、最大值与内部答案；若左半最大值大于右半最小值，当前块边界产生逆序，答案提升到半块长度。

    **复杂度**：建树 $O(n)$，每次点赋值 $O(\log n)$，额外空间 $O(n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Node {
      int minimum;
      int maximum;
      int need;
    };
    Node mergeNode(const Node& left, const Node& right, int half) {
      return {min(left.minimum, right.minimum), max(left.maximum, right.maximum),
          max({left.need, right.need, left.maximum > right.minimum ? half : 0})};
    }
    void solve() {
      int n, q;
      cin >> n >> q;
      int size = 1;
      while (size < n) {
        size <<= 1;
      }
      const int INF = 1'000'000'001;
      vector<Node> tree(2 * size, {INF, INF, 0});
      for (int i = 0; i < n; ++i) {
        cin >> tree[size + i].minimum;
        tree[size + i].maximum = tree[size + i].minimum;
      }
      int half = 1;
      for (int first = size; first > 1; first >>= 1, half <<= 1) {
        for (int node = first >> 1; node < first; ++node) {
          tree[node] = mergeNode(tree[node << 1], tree[node << 1 | 1], half);
        }
      }
      cout << tree[1].need << '\n';
      while (q--) {
        int index, value;
        cin >> index >> value;
        int node = size + index;
        tree[node] = {value, value, 0};
        half = 1;
        for (node >>= 1; node > 0; node >>= 1, half <<= 1) {
          tree[node] = mergeNode(tree[node << 1], tree[node << 1 | 1], half);
        }
        cout << tree[1].need << '\n';
      }
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        solve();
      }
    }
    ```
