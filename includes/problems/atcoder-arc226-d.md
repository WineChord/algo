<div class="problem-anchor" id="problem-atcoder-arc226-d"></div>

??? problem "AtCoder ARC226 D · Penta-Queue"
    [打开原题 ↗](https://atcoder.jp/contests/arc226/tasks/arc226_d?lang=en){ .problem-source }

    **难度与分值**：AtCoder 官方 800 分，比赛 rated 范围为 1200–2799；AtCoder Problems 社区估算难度为 2642（核对于 2026-08-15）。

    **题意**：交互过程中，新值总是进入队列 1；可以把任意非空队列的队首移到任意队尾。面对全局删除最小值请求，需在总移动次数不超过 100000 的前提下回答正确队列。

    **思路**：把元素按规模 1、9、81、729 分层归并，并保留第五个队列作为最高层。每层始终是一条升序队列；九个同级块触发一次稳定归并，元素每升一层只被移动常数次，因此移动总数受几何级数控制。

    **复杂度**：最多 5000 次插入与 5000 次删除；本策略总移动次数不超过预算，每次删除只比较五个队首。

    **C++ 实现**

    <!-- compile:interactive -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int queryCount;
      if (!(cin >> queryCount)) return 0;
      array<deque<int>, 5> queues;
      const array<int, 4> limit = {1, 9, 81, 729};
      auto moveValue = [&](int from, int to,
          vector<pair<int, int>>& operations) {
        int value = queues[from].front();
        queues[from].pop_front();
        queues[to].push_back(value);
        operations.push_back({from + 1, to + 1});
      };
      auto mergeQueues = [&](int from, int to,
          vector<pair<int, int>>& operations) {
        int rotations = static_cast<int>(queues[to].size());
        for (int step = 0; step < rotations; ++step) {
          while (!queues[from].empty() &&
              queues[from].front() < queues[to].front()) {
            moveValue(from, to, operations);
          }
          moveValue(to, to, operations);
        }
        while (!queues[from].empty()) moveValue(from, to, operations);
      };
      for (int round = 0; round < 2 * queryCount; ++round) {
        int type;
        if (!(cin >> type) || type == -1) return 0;
        if (type == 1) {
          int value;
          cin >> value;
          queues[0].push_back(value);
          vector<pair<int, int>> operations;
          for (int level = 0; level < 4; ++level) {
            if (static_cast<int>(queues[level].size()) >= limit[level]) {
              mergeQueues(level, level + 1, operations);
            }
          }
          cout << operations.size() << '\n';
          for (auto [from, to] : operations) {
            cout << from << ' ' << to << '\n';
          }
        } else {
          int chosen = -1;
          for (int i = 0; i < 5; ++i) {
            if (queues[i].empty()) continue;
            if (chosen == -1 || queues[i].front() < queues[chosen].front()) {
              chosen = i;
            }
          }
          cout << chosen + 1 << '\n';
          queues[chosen].pop_front();
        }
        cout.flush();
      }
    }
    ```
