<div class="problem-anchor" id="problem-atcoder-arc226-c"></div>

??? problem "AtCoder ARC226 C · Square Corner Packing"
    [打开原题 ↗](https://atcoder.jp/contests/arc226/tasks/arc226_c?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 700 分，官方未标注难度；AtCoder Problems 社区估算难度为 2070（核对于 2026-08-14）。

    **题意**：在 H×W 的白色网格中反复选择四角都仍为白色的轴对齐正方形，把四角涂黑；最大化操作数并输出一种最优方案。

    **思路**：每次操作在任意一行、任意一列都恰染 0 或 2 格，因此最终每行、每列的黑格数均为偶数，由奇数边长必须留下白格得到上界。偶边网格用单位正方形配对达到上界；奇×奇网格先铺边带，再递归填充更小奇数正方形，同样达到上界。

    **复杂度**：构造与输出时间 O(HW)，保存方案空间 O(HW)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    using Operation = array<int, 3>;
    void addOperation(vector<Operation>& operations, int r, int c, int side,
                      bool transpose) {
      if (transpose) swap(r, c);
      operations.push_back({r, c, side});
    }
    void buildOddSquare(int size, int row, int column,
                        vector<Operation>& operations, bool transpose) {
      if (size == 1) return;
      if (size == 3) {
        addOperation(operations, row, column, 1, transpose);
        return;
      }
      addOperation(operations, row, column, size - 1, transpose);
      for (int offset = 1; offset <= size - 4; offset += 2) {
        addOperation(operations, row, column + offset, 1, transpose);
        addOperation(operations, row + offset, column + size - 2, 1, transpose);
      }
      for (int offset = 2; offset <= size - 3; offset += 2) {
        addOperation(operations, row + size - 2, column + offset, 1, transpose);
        addOperation(operations, row + offset, column, 1, transpose);
      }
      buildOddSquare(size - 4, row + 2, column + 2, operations, transpose);
    }
    vector<Operation> solve(int height, int width) {
      vector<Operation> operations;
      if (height % 2 == 0 || width % 2 == 0) {
        for (int r = 1; r < height; r += 2) {
          for (int c = 1; c < width; c += 2) {
            operations.push_back({r, c, 1});
          }
        }
        return operations;
      }
      bool transpose = false;
      if (height > width) {
        swap(height, width);
        transpose = true;
      }
      buildOddSquare(height, 1, 1, operations, transpose);
      for (int c = height + 1; c <= width; c += 2) {
        for (int r = 1; r < height; r += 2) {
          addOperation(operations, r, c, 1, transpose);
        }
      }
      return operations;
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int height, width;
        cin >> height >> width;
        vector<Operation> operations = solve(height, width);
        cout << operations.size() << '\n';
        for (auto [r, c, side] : operations) {
          cout << r << ' ' << c << ' ' << side << '\n';
        }
      }
    }
    ```
