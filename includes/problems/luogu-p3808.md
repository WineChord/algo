??? problem "洛谷 P3808 · AC 自动机（简单版）"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P3808){ .problem-source }

    **题意**：给定多个小写模式串和一篇文本，求有多少个模式串曾在文本中出现；重复输入的模式串分别计数。

    **思路**：先把模式串插入 Trie，再用 BFS 构造失配指针和缺省转移，得到 AC 自动机。扫描文本时沿当前节点的失配链收集结尾计数；一个结尾首次计入后标记，保证同一模式串无论出现多少次都只统计一次。

    **复杂度**：构建和匹配近似 \(O(\sum |p_i|+|s|+\text{命中链})\)，空间 \(O(\sum |p_i|)\)。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    struct Node{int ch[26]{},fail,cnt;};
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n;
        cin>>n;
        vector<Node> t(1);
        while(n--){
            string s;
            cin>>s;
            int u=0;
            for(char c:s){
                int x=c-'a';
                if(!t[u].ch[x]) t[u].ch[x]=t.size(),t.push_back({});
                u=t[u].ch[x];
            }
            t[u].cnt++;
        }
        queue<int> q;
        for(int c=0;c<26;c++) if(t[0].ch[c]) q.push(t[0].ch[c]);
        while(!q.empty()){
            int u=q.front();
            q.pop();
            for(int c=0;c<26;c++){
                int v=t[u].ch[c];
                if(v) t[v].fail=t[t[u].fail].ch[c],q.push(v);
                else t[u].ch[c]=t[t[u].fail].ch[c];
            }
        }
        string s;
        cin>>s;
        int u=0,ans=0;
        for(char c:s){
            u=t[u].ch[c-'a'];
            for(int v=u;v&&t[v].cnt!=-1;v=t[v].fail) ans+=t[v].cnt,t[v].cnt=-1;
        }
        cout<<ans<<'\n';
    }
    ```
