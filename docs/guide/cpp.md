# 竞赛 C++

竞赛代码首先要在压力下稳定正确，其次才是短。理想风格是结构紧凑、边界明确、变量符合常见语义，同时避免宏技巧和过度压行制造额外认知成本。

## 最小可用模板

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    cin >> T;
    while (T--) {
    }
    return 0;
}
```

若题目没有多组测试，删除 `T` 和循环即可。不要默认输出精度、模数或文件重定向；只把当前题目确实需要的内容放进模板。

## 类型与整数范围

| 类型 | 常见范围 | 典型用途 |
| --- | --- | --- |
| `int` | 约 \([-2.1\times10^9,2.1\times10^9]\) | 下标、计数、较小权值 |
| `long long` | 约 \([-9.2\times10^{18},9.2\times10^{18}]\) | 前缀和、距离、乘积 |
| `__int128` | 约 \(\pm 1.7\times10^{38}\) | 可能超过 64 位的中间乘积 |
| `double` | 约 15–16 位十进制有效数字 | 浮点二分、几何 |

表达式会先按操作数类型计算，再赋值：

<!-- compile:skip -->
```cpp
long long area = 1LL * n * m;
```

如果写成 `long long area = n * m;` 且 `n,m` 都是 `int`，乘法可能在赋值前已经溢出。

## 常见容器选择

| 需求 | 首选 | 复杂度提示 |
| --- | --- | --- |
| 连续存储、随机访问 | `vector` | 访问 \(O(1)\)，尾插均摊 \(O(1)\) |
| 两端插入删除 | `deque` | 两端 \(O(1)\) |
| 后进先出 | `stack` 或 `vector` | 栈顶 \(O(1)\) |
| 先进先出 | `queue` | 队首、队尾 \(O(1)\) |
| 动态最值 | `priority_queue` | 插入、删除堆顶 \(O(\log n)\) |
| 有序集合 | `set` / `map` | 操作 \(O(\log n)\) |
| 哈希查找 | `unordered_set` / `unordered_map` | 期望 \(O(1)\)，最坏可退化 |

`map[key]` 在键不存在时会插入默认值。只想检查存在性时优先使用 `find` 或 `contains`。

## 排序与比较器

比较器必须满足严格弱序，尤其不能写 `a <= b`：

<!-- compile:skip -->
```cpp
sort(a.begin(), a.end(), [](const auto& x, const auto& y) {
    if (x.first != y.first) return x.first < y.first;
    return x.second > y.second;
});
```

若只需去重：

<!-- compile:skip -->
```cpp
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());
```

## Lambda 与递归

C++23 可以用显式对象参数写递归 Lambda：

<!-- compile:skip -->
```cpp
auto dfs = [&](this auto&& self, int u, int p) -> void {
    for (int v : g[u]) if (v != p) self(v, u);
};
```

在只支持 C++17/20 的平台，可传入自身：

<!-- compile:skip -->
```cpp
auto dfs = [&](auto&& self, int u, int p) -> void {
    for (int v : g[u]) if (v != p) self(self, v, u);
};
```

## 调试输出

本地调试信息应写到标准错误，避免污染答案：

```cpp
#ifdef LOCAL
#define debug(x) cerr << #x << " = " << (x) << '\n'
#else
#define debug(x) ((void)0)
#endif
```

编译时使用 `-DLOCAL` 开启。提交前仍应检查复杂度和边界，不能把“样例能过”当成完成。

## 编译建议

本地至少打开常用警告：

```bash
g++ -std=c++23 -O2 -Wall -Wextra -Wshadow -Wconversion solution.cpp
```

排查越界和未定义行为时，可临时关闭优化并使用 sanitizer：

```bash
g++ -std=c++23 -O0 -g -fsanitize=address,undefined solution.cpp
```

!!! note "可移植性"

    `#include <bits/stdc++.h>` 是 GNU 工具链的竞赛惯例，不是 ISO C++ 标准头文件。在线评测通常支持；面试环境或非 GNU 编译器中，应改为显式包含实际使用的标准头文件。

## 风格原则

- 缩进和大括号保持一致，不把整段逻辑压成一行。
- 常见下标可以用 `i,j,l,r`，图节点可用 `u,v`；核心状态应有可辨认的名字。
- 把重复且独立的逻辑提成函数，但不为一次调用制造多层抽象。
- C++ 代码块内部保持连续，不插入空行；结构分隔通过函数、缩进和简短命名表达。
- 优先写自己能证明且能在比赛中稳定复现的版本。
