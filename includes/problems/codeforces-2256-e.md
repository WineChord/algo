<div class="problem-anchor" id="problem-codeforces-2256-e"></div>

??? problem "Codeforces 2256E / 2255C: Even If the World Turns"
    [打开原题 ↗](https://codeforces.com/contest/2256/problem/E){ .problem-source }

    **难度与分值**：官方 rating 2100；Div.1 C / Div.2 E 官方分值 1750 / 2750

    **题意**：双运行通信题：第一次只能交换两个黑白格来编码目标；图片随后可环移、旋转、镜像或反色，第二次仅凭结果图恢复目标。

    **思路**：在模 n 的二维环上用黑格坐标和乘黑格数逆元作为重心。一次黑白交换可把重心调到目标；仿射几何变换让重心等变，补集同时把数量与坐标和取负，故反色不改变重心。

    **复杂度**：每个测试时间 O(n^2)，空间 O(n^2)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    long long extendedGcd(long long a, long long b, long long& x, long long& y) {
      if (b == 0) {
        x = 1;
        y = 0;
        return a;
      }
      long long nextX, nextY;
      long long divisor = extendedGcd(b, a % b, nextX, nextY);
      x = nextY;
      y = nextX - a / b * nextY;
      return divisor;
    }
    int normalize(long long value, int mod) {
      value %= mod;
      if (value < 0) value += mod;
      return static_cast<int>(value);
    }
    int inverseModulo(int value, int mod) {
      long long x, y;
      extendedGcd(value, mod, x, y);
      return normalize(x, mod);
    }
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      string mode;
      cin >> mode;
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        cin >> n;
        vector<string> picture(n);
        for (string& row : picture) cin >> row;
        int blackCount = 0;
        int sumRow = 0;
        int sumColumn = 0;
        for (int row = 0; row < n; ++row) {
          for (int column = 0; column < n; ++column) {
            if (picture[row][column] == '#') {
              ++blackCount;
              sumRow = (sumRow + row) % n;
              sumColumn = (sumColumn + column) % n;
            }
          }
        }
        if (mode == "first") {
          int targetRow, targetColumn;
          cin >> targetRow >> targetColumn;
          --targetRow;
          --targetColumn;
          int deltaRow = normalize(1LL * blackCount * targetRow - sumRow, n);
          int deltaColumn = normalize(1LL * blackCount * targetColumn - sumColumn, n);
          if (deltaRow == 0 && deltaColumn == 0) {
            cout << "1 1 1 1\n";
            continue;
          }
          bool found = false;
          for (int row = 0; row < n && !found; ++row) {
            for (int column = 0; column < n && !found; ++column) {
              if (picture[row][column] != '#') continue;
              int nextRow = (row + deltaRow) % n;
              int nextColumn = (column + deltaColumn) % n;
              if (picture[nextRow][nextColumn] == '.') {
                cout << row + 1 << ' ' << column + 1 << ' ';
                cout << nextRow + 1 << ' ' << nextColumn + 1 << '\n';
                found = true;
              }
            }
          }
        } else {
          int inverse = inverseModulo(blackCount % n, n);
          int targetRow = normalize(1LL * sumRow * inverse, n);
          int targetColumn = normalize(1LL * sumColumn * inverse, n);
          cout << targetRow + 1 << ' ' << targetColumn + 1 << '\n';
        }
      }
    }
    ```
