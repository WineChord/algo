??? problem "洛谷 P3367 · 并查集"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P3367){ .problem-source }

    **题意**：维护若干集合，支持合并两个元素所在集合，以及查询两个元素是否属于同一集合。

    **思路**：并查集用代表元表示集合；路径压缩缩短查找链，按大小合并避免树过深。

    **复杂度**：\(m\) 次操作总时间 \(O(m\alpha(n))\)，额外空间 \(O(n)\)。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n, m;
        cin >> n >> m;
        vector<int> p(n + 1), sz(n + 1, 1);
        iota(p.begin(), p.end(), 0);
        function<int(int)> find = [&](int x) {
            return p[x] == x ? x : p[x] = find(p[x]);
        };
        while (m--) {
            int op, x, y;
            cin >> op >> x >> y;
            x = find(x);
            y = find(y);
            if (op == 2) cout << (x == y ? 'Y' : 'N') << '\n';
            else if (x != y) {
                if (sz[x] < sz[y]) swap(x, y);
                p[y] = x;
                sz[x] += sz[y];
            }
        }
    }
    ```
