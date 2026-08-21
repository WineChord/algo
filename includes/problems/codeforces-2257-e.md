<div class="problem-anchor" id="problem-codeforces-2257-e"></div>

??? problem "Codeforces 2257E: Busy Beaver"
    [打开原题 ↗](https://codeforces.com/contest/2257/problem/E){ .problem-source }

    **难度与分值**：官方分值 2250；官方 rating 未给出；官方标签 `brute force`、`data structures`、`divide and conquer`、`dp`、`greedy`、`implementation`、`sortings`（2026-08-22）

    **题意**：多个楼宇项目各有必须按序施工的楼层；每层先支付成本、再获得奖励，项目之间可任意交错。给定初始资本，求能造出的最高单栋楼层数，平局取最小项目编号。

    **思路**：把每个项目切成最短的非负净收益段，并计算完整执行一段所需的最低准入资本。用小根堆维护各项目下一段；只要堆顶可负担，就执行并暴露后继。资本无法再增长后，对每个项目独立试算剩余负尾部，选最高者。

    **复杂度**：时间 $O(M\log n)$，空间 $O(M+n)$，其中 $M=\sum m_i$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Segment {
      long long need;
      long long gain;
      int end;
    };
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int tests;
      cin >> tests;
      while (tests--) {
        int n;
        long long capital;
        cin >> n >> capital;
        vector<vector<long long>> cost(n), reward(n);
        vector<vector<Segment>> segments(n);
        for (int i = 0; i < n; ++i) {
          int m;
          cin >> m;
          cost[i].resize(m);
          reward[i].resize(m);
          for (long long& value : cost[i]) cin >> value;
          for (long long& value : reward[i]) cin >> value;
          long long balance = 0;
          long long need = 0;
          for (int floor = 0; floor < m; ++floor) {
            need = max(need, cost[i][floor] - balance);
            balance += reward[i][floor] - cost[i][floor];
            if (balance >= 0) {
              segments[i].push_back({need, balance, floor + 1});
              balance = 0;
              need = 0;
            }
          }
        }
        using Entry = pair<long long, int>;
        priority_queue<Entry, vector<Entry>, greater<Entry>> available;
        vector<int> nextSegment(n);
        vector<int> built(n);
        for (int i = 0; i < n; ++i) {
          if (!segments[i].empty()) available.push({segments[i][0].need, i});
        }
        while (!available.empty() && available.top().first <= capital) {
          int project = available.top().second;
          available.pop();
          const Segment& segment = segments[project][nextSegment[project]];
          capital += segment.gain;
          built[project] = segment.end;
          ++nextSegment[project];
          if (nextSegment[project] < static_cast<int>(segments[project].size())) {
            available.push({segments[project][nextSegment[project]].need, project});
          }
        }
        int bestHeight = -1;
        int bestProject = -1;
        for (int i = 0; i < n; ++i) {
          long long current = capital;
          int height = built[i];
          while (height < static_cast<int>(cost[i].size()) &&
              current >= cost[i][height]) {
            current += reward[i][height] - cost[i][height];
            ++height;
          }
          if (height > bestHeight) {
            bestHeight = height;
            bestProject = i;
          }
        }
        cout << bestHeight << ' ' << bestProject + 1 << '\n';
      }
      return 0;
    }
    ```
