??? problem "洛谷 P1177 · 排序"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P1177){ .problem-source }

    **题意**：读入 $n$ 个整数，将它们按从小到大的顺序输出。

    **思路**：直接使用 `std::sort`，其比较排序复杂度满足本题 $n\le 10^5$ 的范围。

    **复杂度**：时间 $O(n\log n)$，排序栈空间通常为 $O(\log n)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main() {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n;
        cin >> n;
        vector<int> a(n);
        for (int& x : a) cin >> x;
        sort(a.begin(), a.end());
        for (int i = 0; i < n; ++i) cout << a[i] << " \n"[i + 1 == n];
    }
    ```
