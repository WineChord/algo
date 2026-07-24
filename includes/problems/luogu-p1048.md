??? problem "洛谷 P1048 · 采药"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P1048){ .problem-source }

    **题意**：在总时间不超过 $T$ 的前提下，每株草药至多采一次，求能够取得的最大总价值。

    **思路**：标准 0/1 背包。`dp[j]` 表示容量为 `j` 时的最大价值；每件物品的容量倒序枚举，确保它只被选择一次。

    **复杂度**：时间 $O(MT)$，空间 $O(T)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int T,M;
        cin>>T>>M;
        vector<int> dp(T+1);
        while(M--){
            int t,v;
            cin>>t>>v;
            for(int j=T;j>=t;j--) dp[j]=max(dp[j],dp[j-t]+v);
        }
        cout<<dp[T]<<'\n';
    }
    ```
