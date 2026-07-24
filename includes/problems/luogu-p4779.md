??? problem "洛谷 P4779 · 单源最短路径（标准版）"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P4779){ .problem-source }

    **题意**：给定带非负权的有向图和源点，输出源点到每个节点的最短距离。

    **思路**：使用邻接表和小根堆优化 Dijkstra。若堆顶距离不等于当前记录值，说明它是一次旧更新，直接跳过；否则用它松弛所有出边。

    **复杂度**：时间 \(O((n+m)\log n)\)，空间 \(O(n+m)\)。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n,m,s;
        cin>>n>>m>>s;
        vector<vector<pair<int,int>>> g(n+1);
        while(m--){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});}
        const long long inf=4e18;
        vector<long long> d(n+1,inf);
        priority_queue<pair<long long,int>,vector<pair<long long,int>>,greater<>> q;
        d[s]=0;
        q.push({0,s});
        while(!q.empty()){
            auto [du,u]=q.top();
            q.pop();
            if(du!=d[u]) continue;
            for(auto [v,w]:g[u]) if(d[v]>du+w) d[v]=du+w,q.push({d[v],v});
        }
        for(int i=1;i<=n;i++) cout<<(d[i]==inf?2147483647:d[i])<<' ';
        cout<<'\n';
    }
    ```
