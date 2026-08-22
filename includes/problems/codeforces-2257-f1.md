<div class="problem-anchor" id="problem-codeforces-2257-f1"></div>

??? problem "Codeforces 2257F1: Beaver's Jumping Track (Easy Version)"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/F1){ .problem-source }

    **难度与分值**：Codeforces Round 1117 Div.2 F1；官方分值 2750；官方 rating 未给出；官方标签 `data structures`、`dp`、`matrices`（2026-08-23）

    **题意**：若一次向前跳跃的起点和终点同在平台 $i$，就付罚值 $s_i$，跨平台跳跃免费；最大跳长 $x\le5$。支持平台长度、罚值的点更新，并询问从平台 $l$ 首格到平台 $r$ 末格的最小罚值。

    **思路**：格子 DP 只依赖前 $x$ 格，把每个平台压成从左边界 $x$ 个状态到右边界 $x$ 个状态的 min-plus 矩阵。平台串联就是有序 min-plus 乘法；用线段树维护矩阵积，查询时从平台 $l$ 首格构造起始向量。

    **复杂度**：建树 $O(nx^3)$；单次更新或询问 $O(x^3\log n)$；空间 $O(nx^2)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using int64 = long long;
    constexpr int MAX_X = 5;
    constexpr int64 INF = 4000000000000000000LL;
    int jumpLimit;
    struct Matrix {
      array<int64, MAX_X * MAX_X> value;
      Matrix() {
        value.fill(INF);
      }
      int64& at(int row, int column) {
        return value[row * MAX_X + column];
      }
      int64 at(int row, int column) const {
        return value[row * MAX_X + column];
      }
    };
    Matrix identityMatrix() {
      Matrix answer;
      for (int i = 0; i < jumpLimit; ++i) answer.at(i, i) = 0;
      return answer;
    }
    Matrix multiply(const Matrix& left, const Matrix& right) {
      Matrix answer;
      for (int i = 0; i < jumpLimit; ++i) {
        for (int k = 0; k < jumpLimit; ++k) {
          int64 first = left.at(i, k);
          if (first == INF) continue;
          for (int j = 0; j < jumpLimit; ++j) {
            int64 second = right.at(k, j);
            if (second == INF) continue;
            answer.at(i, j) = min(answer.at(i, j), first + second);
          }
        }
      }
      return answer;
    }
    Matrix platformMatrix(int length, int64 penalty) {
      Matrix answer;
      for (int input = 0; input < jumpLimit; ++input) {
        int start = input - jumpLimit + 1;
        for (int output = 0; output < jumpLimit; ++output) {
          int target = length - jumpLimit + 1 + output;
          if (target <= 0) {
            if (target == start) answer.at(input, output) = 0;
          } else {
            int remaining = target - start - jumpLimit;
            int paidJumps = remaining <= 0 ? 0 : (remaining + jumpLimit - 1) / jumpLimit;
            answer.at(input, output) = 1LL * paidJumps * penalty;
          }
        }
      }
      return answer;
    }
    class SegmentTree {
    public:
      SegmentTree(const vector<int>& length, const vector<int64>& penalty) {
        size = 1;
        while (size < static_cast<int>(length.size())) size *= 2;
        tree.assign(size * 2, identityMatrix());
        for (int i = 0; i < static_cast<int>(length.size()); ++i) {
          tree[size + i] = platformMatrix(length[i], penalty[i]);
        }
        for (int node = size - 1; node > 0; --node) {
          tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
        }
      }
      void update(int index, int length, int64 penalty) {
        int node = size + index;
        tree[node] = platformMatrix(length, penalty);
        for (node /= 2; node > 0; node /= 2) {
          tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
        }
      }
      Matrix query(int left, int right) const {
        Matrix leftProduct = identityMatrix();
        Matrix rightProduct = identityMatrix();
        for (left += size, right += size; left < right; left /= 2, right /= 2) {
          if (left % 2 == 1) leftProduct = multiply(leftProduct, tree[left++]);
          if (right % 2 == 1) rightProduct = multiply(tree[--right], rightProduct);
        }
        return multiply(leftProduct, rightProduct);
      }
    private:
      int size;
      vector<Matrix> tree;
    };
    int64 answerQuery(
        int left, int right, const vector<int>& length, const vector<int64>& penalty,
        const SegmentTree& tree) {
      array<int64, MAX_X> state;
      state.fill(INF);
      for (int output = 0; output < jumpLimit; ++output) {
        int target = length[left] - jumpLimit + 1 + output;
        if (target < 1) continue;
        int paidJumps = (target - 1 + jumpLimit - 1) / jumpLimit;
        state[output] = 1LL * paidJumps * penalty[left];
      }
      Matrix product = tree.query(left + 1, right + 1);
      array<int64, MAX_X> result;
      result.fill(INF);
      for (int input = 0; input < jumpLimit; ++input) {
        if (state[input] == INF) continue;
        for (int output = 0; output < jumpLimit; ++output) {
          if (product.at(input, output) == INF) continue;
          result[output] = min(result[output], state[input] + product.at(input, output));
        }
      }
      return result[jumpLimit - 1];
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n;
      int q;
      cin >> n >> q >> jumpLimit;
      vector<int> length(n);
      vector<int64> penalty(n);
      for (int& value : length) cin >> value;
      for (int64& value : penalty) cin >> value;
      SegmentTree tree(length, penalty);
      while (q--) {
        char type;
        cin >> type;
        if (type == '1') {
          int index;
          int value;
          cin >> index >> value;
          --index;
          length[index] = value;
          tree.update(index, length[index], penalty[index]);
        } else if (type == '2') {
          int index;
          int64 value;
          cin >> index >> value;
          --index;
          penalty[index] = value;
          tree.update(index, length[index], penalty[index]);
        } else {
          int left;
          int right;
          cin >> left >> right;
          cout << answerQuery(left - 1, right - 1, length, penalty, tree) << '\n';
        }
      }
      return 0;
    }
    ```
