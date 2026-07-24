??? problem "洛谷 P1082 · 同余方程"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P1082){ .problem-source }

    **题意**：求同余方程 $ax\equiv1\pmod b$ 的最小正整数解。

    **思路**：扩展欧几里得算法求出 $ax+by=\gcd(a,b)$ 的一组系数。题目保证逆元存在，即最大公因数为 $1$；把得到的 $x$ 对 $b$ 规范到 $[0,b)$ 即可。

    **复杂度**：时间 $O(\log b)$，递归栈空间 $O(\log b)$。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    long long exgcd(long long a,long long b,long long& x,long long& y){
        if(!b){x=1;y=0;return a;}
        long long x1,y1,g=exgcd(b,a%b,x1,y1);
        x=y1;
        y=x1-a/b*y1;
        return g;
    }
    int main(){
        long long a,b,x,y;
        cin>>a>>b;
        exgcd(a,b,x,y);
        cout<<(x%b+b)%b<<'\n';
    }
    ```
