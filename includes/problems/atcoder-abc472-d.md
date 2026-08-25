<div class="problem-anchor" id="problem-atcoder-abc472-d"></div>

??? problem "AtCoder ABC472 D: Bomber Mad"
    [打开原题 ↗](https://atcoder.jp/contests/abc472/tasks/abc472_d?lang=en){ .problem-source }

    **难度与分值**：官方分值 400；AtCoder 未给出单题官方难度；AtCoder Problems 社区估算难度 605（2026-08-26）

    **题意**：网格中的安全空格要求所在整行与整列都没有炸弹。统计能沿四方向空格、在至多 $K$ 步内到达任一安全空格的起点数。

    **思路**：先标记含炸弹的行列，从全部安全格同时做多源 BFS。每个空格第一次访问时的层数就是它到安全集合的障碍最短路；只扩展距离小于 $K$ 的节点。

    **复杂度**：时间 $O(HW)$，额外空间 $O(HW)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int h, w, k;
      cin >> h >> w >> k;
      vector<string> s(h);
      for (string& row : s)
        cin >> row;
      vector<int> rowBomb(h), colBomb(w);
      for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
          if (s[i][j] == '#') {
            rowBomb[i] = 1;
            colBomb[j] = 1;
          }
        }
      }
      vector<int> dist(h * w, -1);
      queue<int> q;
      long long answer = 0;
      for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
          int id = i * w + j;
          if (s[i][j] == '.' && !rowBomb[i] && !colBomb[j]) {
            dist[id] = 0;
            q.push(id);
            ++answer;
          }
        }
      }
      const int di[4] = {-1, 1, 0, 0};
      const int dj[4] = {0, 0, -1, 1};
      while (!q.empty()) {
        int id = q.front();
        q.pop();
        int i = id / w, j = id % w;
        if (dist[id] == k)
          continue;
        for (int z = 0; z < 4; ++z) {
          int ni = i + di[z], nj = j + dj[z];
          if (ni < 0 || ni >= h || nj < 0 || nj >= w)
            continue;
          int next = ni * w + nj;
          if (s[ni][nj] == '#' || dist[next] != -1)
            continue;
          dist[next] = dist[id] + 1;
          q.push(next);
          ++answer;
        }
      }
      cout << answer << '\n';
      return 0;
    }
    ```
