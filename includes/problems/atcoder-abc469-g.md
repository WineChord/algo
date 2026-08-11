<div class="problem-anchor" id="problem-atcoder-abc469-g"></div>

??? problem "AtCoder ABC469 G · K-nacci Operations"
    [打开原题 ↗](https://atcoder.jp/contests/abc469/tasks/abc469_g?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 575 分，比赛 Rated Range 为 0–1999；[AtCoder Problems](https://kenkoooo.com/atcoder/#/table/) 社区模型估算难度为 2804（非官方，检索于 2026-08-11）。

    **题意**：前 $K$ 个 `a`/`b` 操作串已知，之后按新到旧拼接前 $K$ 串；在 $N$ 可达 $10^{18}$ 时求轮转与反转作用后的文本。

    **思路**：把轮转与反转压成二面体群元素；群递推右消元后，方向以 $K+1$ 为周期，偏移成为周期系数线性递推，再用一个周期矩阵快速幂。

    **复杂度**：令 $P=K+1$，时间 $O(\sum|S_i|+P^3\log N+|T|)$，空间 $O(P^2+|T|)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Transform {
      int direction;
      int offset;
    };
    using Matrix = vector<vector<int>>;
    Transform concatenate(const Transform& first, const Transform& second, int length) {
      return {first.direction * second.direction,
          (first.offset + first.direction * second.offset % length + length) % length};
    }
    Transform parseTransform(const string& operations, int length) {
      Transform result{1, 0};
      for (char operation : operations) {
        Transform current;
        if (operation == 'a') {
          current = {1, 1 % length};
        } else {
          current = {-1, (length - 1) % length};
        }
        result = concatenate(result, current, length);
      }
      return result;
    }
    Matrix multiply(const Matrix& left, const Matrix& right, int modulus) {
      int size = left.size();
      Matrix product(size, vector<int>(size));
      for (int row = 0; row < size; ++row) {
        for (int column = 0; column < size; ++column) {
          long long sum = 0;
          for (int middle = 0; middle < size; ++middle) {
            sum += 1LL * left[row][middle] * right[middle][column];
          }
          product[row][column] = sum % modulus;
        }
      }
      return product;
    }
    vector<int> multiply(const Matrix& matrix, const vector<int>& values, int modulus) {
      int size = matrix.size();
      vector<int> product(size);
      for (int row = 0; row < size; ++row) {
        long long sum = 0;
        for (int column = 0; column < size; ++column) {
          sum += 1LL * matrix[row][column] * values[column];
        }
        product[row] = sum % modulus;
      }
      return product;
    }
    vector<int> advanceOne(
        const vector<int>& state,
        int previousDirection,
        int nextDirection,
        int modulus) {
      int size = state.size();
      vector<int> next(size);
      long long leading = 1LL * (1 + previousDirection) * state[0]
                        - 1LL * nextDirection * state.back();
      leading %= modulus;
      if (leading < 0) leading += modulus;
      next[0] = leading;
      for (int index = 1; index < size; ++index) next[index] = state[index - 1];
      return next;
    }
    string solve(const vector<string>& initial, unsigned long long target, const string& text) {
      int count = initial.size();
      int period = count + 1;
      int length = text.size();
      vector<Transform> transform(period + 1);
      for (int index = 1; index <= count; ++index) {
        transform[index] = parseTransform(initial[index - 1], length);
      }
      Transform combined{1, 0};
      for (int index = count; index >= 1; --index) {
        combined = concatenate(combined, transform[index], length);
      }
      transform[period] = combined;
      Transform answerTransform;
      if (target <= static_cast<unsigned long long>(period)) {
        answerTransform = transform[target];
      } else {
        vector<int> state(period);
        for (int index = 0; index < period; ++index) state[index] = transform[period - index].offset;
        Matrix block(period, vector<int>(period));
        for (int index = 0; index < period; ++index) block[index][index] = 1 % length;
        for (int step = 1; step <= period; ++step) {
          int previous = step == 1 ? period : step - 1;
          Matrix next(period, vector<int>(period));
          for (int column = 0; column < period; ++column) {
            long long value = 1LL * (1 + transform[previous].direction) * block[0][column]
                            - 1LL * transform[step].direction * block[period - 1][column];
            value %= length;
            if (value < 0) value += length;
            next[0][column] = value;
          }
          for (int row = 1; row < period; ++row) next[row] = block[row - 1];
          block.swap(next);
        }
        unsigned long long remaining = target - period;
        unsigned long long fullBlocks = remaining / period;
        int extra = remaining % period;
        while (fullBlocks > 0) {
          if (fullBlocks & 1ULL) state = multiply(block, state, length);
          fullBlocks >>= 1ULL;
          if (fullBlocks > 0) block = multiply(block, block, length);
        }
        for (int step = 1; step <= extra; ++step) {
          int previous = step == 1 ? period : step - 1;
          state = advanceOne(state, transform[previous].direction, transform[step].direction, length);
        }
        int residue = (target - 1) % period + 1;
        answerTransform = {transform[residue].direction, state[0]};
      }
      string answer(length, '?');
      for (int index = 0; index < length; ++index) {
        int source = (answerTransform.direction * index + answerTransform.offset) % length;
        if (source < 0) source += length;
        answer[index] = text[source];
      }
      return answer;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int count;
      cin >> count;
      vector<string> initial(count);
      for (string& operations : initial) cin >> operations;
      unsigned long long target;
      string text;
      cin >> target >> text;
      cout << solve(initial, target, text) << '\n';
    }
    ```
