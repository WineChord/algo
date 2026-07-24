??? problem "洛谷 P3383 · 线性筛素数"
    [打开原题 ↗](https://www.luogu.com.cn/problem/P3383){ .problem-source }

    **题意**：筛出不超过 \(n\) 的所有质数，并回答若干次“第 \(k\) 个质数是多少”。

    **思路**：欧拉筛让每个合数只被它的最小质因子筛掉。枚举当前数 \(i\) 与已有质数 \(p\) 的乘积；当 \(p\mid i\) 时停止，因为继续枚举会让同一合数被重复标记。

    **复杂度**：预处理时间 \(O(n)\)，空间 \(O(n)\)，每次查询 \(O(1)\)。

    **C++ 实现**

    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    int main(){
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n,q;
        cin>>n>>q;
        vector<bool> comp(n+1);
        vector<int> primes;
        for(int i=2;i<=n;i++){
            if(!comp[i]) primes.push_back(i);
            for(int p:primes){
                if(1LL*i*p>n) break;
                comp[i*p]=1;
                if(i%p==0) break;
            }
        }
        while(q--){int k;cin>>k;cout<<primes[k-1]<<'\n';}
    }
    ```
