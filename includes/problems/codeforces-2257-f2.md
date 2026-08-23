<div class="problem-anchor" id="problem-codeforces-2257-f2"></div>

??? problem "Codeforces 2257F2: Beaver's Jumping Track (Hard Version)"
    [打开原题 ↗](https://codeforces.com/problemset/problem/2257/F2){ .problem-source }

    **难度与分值**：Codeforces Round 1117 Div.2 F2；官方分值 1000；官方 rating 未给出；官方标签 `data structures`、`dp`、`matrices`（2026-08-24）

    **题意**：平台串成一条轨道，最大跳长 $x\le10$；同平台跳跃付该平台罚值，跨平台跳跃免费。支持平台长度、罚值的点更新，并询问从平台 $l$ 首格到平台 $r$ 末格的最小罚值；$n\le10^6$。

    **思路**：用最近 $x$ 个格子的 DP 值作为边界状态，平台对应 $x\times x$ min-plus 转移。单平台转移每列只有两档代价，可用前后缀最小值在 $O(x^2)$ 右乘；再按 16 个平台一块，只在线段树中保存块矩阵，避免为百万个平台各存一份矩阵。

    **复杂度**：建树 $O(nx^2+(n/B)x^3)$；更新 $O(Bx^2+x^3\log(n/B))$；询问 $O(Bx+x^2\log(n/B))$；空间 $O(n+(n/B)x^2)$，其中 $B=16$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using int64 = long long;
    constexpr int MAX_X = 10;
    constexpr int BLOCK_SIZE = 16;
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
    Matrix appendPlatform(const Matrix& left, int length, int64 penalty) {
      Matrix answer;
      for (int row = 0; row < jumpLimit; ++row) {
        array<int64, MAX_X + 1> prefix;
        array<int64, MAX_X + 1> suffix;
        prefix[0] = INF;
        for (int k = 0; k < jumpLimit; ++k) {
          prefix[k + 1] = min(prefix[k], left.at(row, k));
        }
        suffix[jumpLimit] = INF;
        for (int k = jumpLimit - 1; k >= 0; --k) {
          suffix[k] = min(suffix[k + 1], left.at(row, k));
        }
        for (int column = 0; column < jumpLimit; ++column) {
          int target = length - jumpLimit + 1 + column;
          if (target <= 0) {
            int input = target + jumpLimit - 1;
            answer.at(row, column) = left.at(row, input);
            continue;
          }
          int shifted = length + column - jumpLimit;
          int quotient = shifted / jumpLimit;
          int remainder = shifted % jumpLimit;
          if (remainder > 0 && prefix[remainder] != INF) {
            answer.at(row, column) =
                prefix[remainder] + 1LL * (quotient + 1) * penalty;
          }
          if (suffix[remainder] != INF) {
            answer.at(row, column) = min(
                answer.at(row, column),
                suffix[remainder] + 1LL * quotient * penalty);
          }
        }
      }
      return answer;
    }
    array<int64, MAX_X> applyPlatform(
        const array<int64, MAX_X>& state, int length, int64 penalty) {
      array<int64, MAX_X + 1> prefix;
      array<int64, MAX_X + 1> suffix;
      prefix[0] = INF;
      for (int k = 0; k < jumpLimit; ++k) {
        prefix[k + 1] = min(prefix[k], state[k]);
      }
      suffix[jumpLimit] = INF;
      for (int k = jumpLimit - 1; k >= 0; --k) {
        suffix[k] = min(suffix[k + 1], state[k]);
      }
      array<int64, MAX_X> answer;
      answer.fill(INF);
      for (int column = 0; column < jumpLimit; ++column) {
        int target = length - jumpLimit + 1 + column;
        if (target <= 0) {
          answer[column] = state[target + jumpLimit - 1];
          continue;
        }
        int shifted = length + column - jumpLimit;
        int quotient = shifted / jumpLimit;
        int remainder = shifted % jumpLimit;
        if (remainder > 0 && prefix[remainder] != INF) {
          answer[column] = prefix[remainder] + 1LL * (quotient + 1) * penalty;
        }
        if (suffix[remainder] != INF) {
          answer[column] = min(
              answer[column], suffix[remainder] + 1LL * quotient * penalty);
        }
      }
      return answer;
    }
    array<int64, MAX_X> applyMatrix(
        const array<int64, MAX_X>& state, const Matrix& matrix) {
      array<int64, MAX_X> answer;
      answer.fill(INF);
      for (int i = 0; i < jumpLimit; ++i) {
        if (state[i] == INF) continue;
        for (int j = 0; j < jumpLimit; ++j) {
          if (matrix.at(i, j) == INF) continue;
          answer[j] = min(answer[j], state[i] + matrix.at(i, j));
        }
      }
      return answer;
    }
    class BlockTree {
    public:
      BlockTree(vector<int>& length, vector<int64>& penalty)
          : length(length), penalty(penalty) {
        blockCount =
            (static_cast<int>(length.size()) + BLOCK_SIZE - 1) / BLOCK_SIZE;
        size = 1;
        while (size < blockCount) size *= 2;
        tree.assign(size * 2, identityMatrix());
        for (int block = 0; block < blockCount; ++block) rebuildLeaf(block);
        for (int node = size - 1; node > 0; --node) {
          tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
        }
      }
      void update(int index) {
        int block = index / BLOCK_SIZE;
        rebuildLeaf(block);
        for (int node = (size + block) / 2; node > 0; node /= 2) {
          tree[node] = multiply(tree[node * 2], tree[node * 2 + 1]);
        }
      }
      array<int64, MAX_X> apply(
          array<int64, MAX_X> state, int left, int right) const {
        vector<int> leftNodes;
        vector<int> rightNodes;
        for (left += size, right += size; left < right; left /= 2, right /= 2) {
          if (left % 2 == 1) leftNodes.push_back(left++);
          if (right % 2 == 1) rightNodes.push_back(--right);
        }
        for (int node : leftNodes) state = applyMatrix(state, tree[node]);
        for (auto iterator = rightNodes.rbegin();
             iterator != rightNodes.rend(); ++iterator) {
          state = applyMatrix(state, tree[*iterator]);
        }
        return state;
      }
    private:
      void rebuildLeaf(int block) {
        Matrix product = identityMatrix();
        int begin = block * BLOCK_SIZE;
        int end = min(static_cast<int>(length.size()), begin + BLOCK_SIZE);
        for (int i = begin; i < end; ++i) {
          product = appendPlatform(product, length[i], penalty[i]);
        }
        tree[size + block] = product;
      }
      vector<int>& length;
      vector<int64>& penalty;
      int blockCount;
      int size;
      vector<Matrix> tree;
    };
    int64 answerQuery(
        int left, int right, const vector<int>& length,
        const vector<int64>& penalty, const BlockTree& tree) {
      array<int64, MAX_X> state;
      state.fill(INF);
      for (int column = 0; column < jumpLimit; ++column) {
        int target = length[left] - jumpLimit + 1 + column;
        if (target < 1) continue;
        int paidJumps = (target - 1 + jumpLimit - 1) / jumpLimit;
        state[column] = 1LL * paidJumps * penalty[left];
      }
      int position = left + 1;
      while (position <= right && position % BLOCK_SIZE != 0) {
        state = applyPlatform(state, length[position], penalty[position]);
        ++position;
      }
      int firstBlock = position / BLOCK_SIZE;
      int lastBlock = (right + 1) / BLOCK_SIZE;
      if (firstBlock < lastBlock) {
        state = tree.apply(state, firstBlock, lastBlock);
        position = lastBlock * BLOCK_SIZE;
      }
      while (position <= right) {
        state = applyPlatform(state, length[position], penalty[position]);
        ++position;
      }
      return state[jumpLimit - 1];
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
      BlockTree tree(length, penalty);
      while (q--) {
        char type;
        cin >> type;
        if (type == '1') {
          int index;
          int value;
          cin >> index >> value;
          --index;
          length[index] = value;
          tree.update(index);
        } else if (type == '2') {
          int index;
          int64 value;
          cin >> index >> value;
          --index;
          penalty[index] = value;
          tree.update(index);
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
