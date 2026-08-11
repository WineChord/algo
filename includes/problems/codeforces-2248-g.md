<div class="problem-anchor" id="problem-codeforces-2248-g"></div>

??? problem "CF Round 1113 · Div.2 G · No Balance Left (2248G)"
    [打开原题 ↗](https://codeforces.com/contest/2248/problem/G){ .problem-source }

    **难度与分值**：Codeforces 官方 3500 分、rating 3000，官方 tags 为 bitmasks、dp、math、number theory（核对时间为 2026-08-11）。

    **题意**：商品可无限购买，每笔按总价触发一个最大返利；对每个初始余额判断能否经有限次购买恰好归零。

    **思路**：bitset 无界背包求可支付总价；首个净增益交易以下做带负担门槛的净损失 DAG，以上利用可重复增资和全部净变化的 gcd 判定同余可达。

    **复杂度**：令 $V=\max(s,a_m)$，时间 $O(V^2/64+n+m+V\log V)$，空间 $O(V)$。

    **C++ 实现**

    <!-- compile:standalone -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    constexpr int LIMIT = 125001;
    int main() {
      ios::sync_with_stdio(false);
      cin.tie(nullptr);
      int n, m, s;
      cin >> n >> m >> s;
      vector<int> price(n);
      for (int& value : price) {
        cin >> value;
      }
      vector<int> threshold(m + 1), rebate(m + 1);
      for (int i = 1; i <= m; ++i) {
        cin >> threshold[i] >> rebate[i];
      }
      int bound = max(s, threshold[m]);
      bitset<LIMIT> spendable;
      spendable.set(0);
      for (int value : price) {
        spendable.set(value);
      }
      for (int total = 1; total <= bound; ++total) {
        if (spendable[total]) {
          spendable |= spendable << total;
        }
      }
      vector<int> need(bound + 1, bound + 1);
      vector<int> increases, decreases;
      int firstIncrease = s + 1;
      int activity = 0;
      for (int total = 1; total <= bound; ++total) {
        if (!spendable[total]) {
          continue;
        }
        while (activity < m && threshold[activity + 1] <= total) {
          ++activity;
        }
        int net = rebate[activity] - total;
        if (net > 0) {
          increases.push_back(net);
          firstIncrease = min(firstIncrease, total);
        } else {
          int decrease = -net;
          need[decrease] = min(need[decrease], total);
          decreases.push_back(decrease);
        }
      }
      vector<pair<int, int>> losses;
      for (int decrease = 1; decrease <= bound; ++decrease) {
        if (need[decrease] <= bound) {
          losses.push_back({need[decrease], decrease});
        }
      }
      sort(losses.begin(), losses.end());
      bitset<LIMIT> reachable, activeLosses;
      reachable.set(0);
      size_t nextLoss = 0;
      int lowEnd = min(s, firstIncrease - 1);
      for (int balance = 1; balance <= lowEnd; ++balance) {
        while (nextLoss < losses.size() && losses[nextLoss].first <= balance) {
          activeLosses.set(LIMIT - 1 - losses[nextLoss].second);
          ++nextLoss;
        }
        reachable[balance] =
            (reachable & (activeLosses >> (LIMIT - 1 - balance))).any();
      }
      int invariant = 0;
      for (int value : increases) {
        invariant = gcd(invariant, value);
      }
      for (int value : decreases) {
        invariant = gcd(invariant, value);
      }
      for (int value : price) {
        invariant = gcd(invariant, value);
      }
      invariant = gcd(invariant, rebate[m]);
      int cheapest = *min_element(price.begin(), price.end());
      for (int balance = 1; balance <= s; ++balance) {
        bool answer = balance < firstIncrease
                          ? reachable[balance]
                          : cheapest < threshold[1] && balance % invariant == 0;
        cout << (answer ? "YES" : "NO") << '\n';
      }
    }
    ```
