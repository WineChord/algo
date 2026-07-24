??? problem "洛谷 P5318 · 查找文献"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P5318){ .problem-source }

    **题意**：从编号 $1$ 的文献出发，在有向图中分别按深度优先和广度优先访问可达节点；有多个选择时优先访问编号小的节点。

    **思路**：先把每个节点的出边按终点升序排序。DFS 用显式栈帧记录每个节点下一条待看的边，既与递归访问次序一致，也避免深链递归爆栈；BFS 则按升序邻接表正常扩展。

    **复杂度**：排序总计 $O(m\log m)$ 上界，遍历 $O(n+m)$，空间 $O(n+m)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n,m;
        cin>>n>>m;
        vector<vector<int>> g(n+1);
        while(m--){int u,v;cin>>u>>v;g[u].push_back(v);}
        for(auto& e:g) sort(e.begin(),e.end());
        vector<int> vis(n+1),it(n+1),a;
        stack<int> st;
        st.push(1);
        vis[1]=1;
        a.push_back(1);
        while(!st.empty()){
            int u=st.top();
            while(it[u]<(int)g[u].size()&&vis[g[u][it[u]]]) it[u]++;
            if(it[u]==(int)g[u].size()){st.pop();continue;}
            int v=g[u][it[u]++];
            vis[v]=1;
            a.push_back(v);
            st.push(v);
        }
        for(int x:a) cout<<x<<' ';
        cout<<'\n';
        fill(vis.begin(),vis.end(),0);
        queue<int> q;
        q.push(1);
        vis[1]=1;
        while(!q.empty()){
            int u=q.front();
            q.pop();
            cout<<u<<' ';
            for(int v:g[u]) if(!vis[v]) vis[v]=1,q.push(v);
        }
        cout<<'\n';
    }
    ```
