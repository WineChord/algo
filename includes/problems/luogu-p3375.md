??? problem "洛谷 P3375 · KMP 字符串匹配"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P3375){ .problem-source }

    **题意**：输出模式串在文本串中的全部出现位置，并输出模式串每个前缀对应的最长相等真前后缀长度。

    **思路**：先为模式串构造前缀函数 `pi`。匹配时发生失配，就沿 `pi` 链缩短已匹配前缀；完整匹配后输出位置，再回退到 `pi[m-1]`，从而保留可能重叠的匹配。

    **复杂度**：时间 $O(n+m)$，空间 $O(m)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        string s,p;
        cin>>s>>p;
        int m=p.size();
        vector<int> pi(m);
        for(int i=1,j=0;i<m;i++){
            while(j&&p[i]!=p[j]) j=pi[j-1];
            if(p[i]==p[j]) j++;
            pi[i]=j;
        }
        for(int i=0,j=0;i<(int)s.size();i++){
            while(j&&s[i]!=p[j]) j=pi[j-1];
            if(s[i]==p[j]) j++;
            if(j==m) cout<<i-m+2<<'\n',j=pi[j-1];
        }
        for(int x:pi) cout<<x<<' ';
        cout<<'\n';
    }
    ```
