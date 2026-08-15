<div class="problem-anchor" id="problem-atcoder-arc226-e"></div>

??? problem "AtCoder ARC226 E: Cellular Messenger"
    [打开原题 ↗](https://atcoder.jp/contests/arc226/tasks/arc226_e?lang=en){ .problem-source }

    **难度与分值**：官方分值 1000；AtCoder 未标注难度；AtCoder Problems 社区估算难度 3505（2026-08-16）

    **题意**：设计一个二值元胞自动机，把发送格每轮写入的任意比特流延迟固定轮数后，在远处接收格逐位恢复。

    **思路**：用两行恒 1 轨道让中间行的总邻居数规则等价于 Rule 90。长度 63 的路径邻接矩阵在二元域上满足 A^63=0；单脉冲恰在第 63 次更新到达接收格，随后清零，线性叠加保证连续输入互不干扰。

    **复杂度**：生成时间与额外空间均为 O(65)。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      cout << "000000010\n";
      cout << "011111010\n";
      cout << "3 65\n";
      cout << string(65, '1') << '\n';
      cout << string(65, '0') << '\n';
      cout << string(65, '1') << '\n';
      cout << "1 0 1 63 63\n";
    }
    ```
