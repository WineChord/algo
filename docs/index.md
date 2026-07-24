---
hide:
  - navigation
  - toc
---

<div class="scholar-home scholar-home--algo">
<header class="scholar-masthead">
<div class="scholar-running-head">
<span>Wine &amp; Chord · Algorithm Studies</span>
<span>Continuously revised</span>
</div>
<div class="scholar-hero-grid">
<div class="scholar-hero-copy">
<p class="scholar-overline">算法研究札记 · 第一卷</p>
<h1>算法，作为一种推理语言</h1>
<p class="scholar-deck">从约束、模型与不变量出发，沿着可验证的朴素解走向最优复杂度。这里整理的不只是答案，更是一套能迁移到陌生问题的思考方法。</p>
<nav class="scholar-actions" aria-label="首页入口">
<a href="guide/roadmap/">进入学习路径 <span aria-hidden="true">→</span></a>
<a href="problems/">查阅题解索引 <span aria-hidden="true">→</span></a>
</nav>
</div>
<aside class="scholar-abstract">
<p class="scholar-label">Abstract / 摘要</p>
<p>每个主题都从直觉开始，经过形式化、复杂度与正确性证明，最终落到可以稳定实现的竞赛代码，并继续追问条件变化后的算法边界。</p>
<dl class="scholar-facts">
<div><dt>核心语言</dt><dd>C++</dd></div>
<div><dt>推理主线</dt><dd>Brute Force → Optimal</dd></div>
<div><dt>组织方式</dt><dd>概念 · 模板 · 题解 · 变种</dd></div>
</dl>
</aside>
</div>
<div class="scholar-meta">
<span><b>范围</b> 算法竞赛与面试题</span>
<span><b>重点</b> 建模、证明与复杂度</span>
<span><b>语言</b> 中文为主，术语双语</span>
<span><b>版本</b> 持续修订</span>
</div>
</header>
<section class="scholar-section">
<header class="scholar-section-head">
<span class="scholar-section-number">01</span>
<div>
<h2>知识目录</h2>
<p>从通用解题方法进入，再按技巧、结构与数学模型建立可交叉检索的知识网络。</p>
</div>
</header>
<nav class="scholar-catalog" aria-label="算法知识目录">
<a class="scholar-entry" href="guide/problem-solving/">
<span class="scholar-entry-no">01</span>
<span class="scholar-entry-title"><strong>解题方法</strong><small>Problem Solving</small></span>
<span class="scholar-entry-desc">读约束、建模、构造暴力、定位瓶颈、证明并测试。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="basics/">
<span class="scholar-entry-no">02</span>
<span class="scholar-entry-title"><strong>基础技巧</strong><small>Techniques</small></span>
<span class="scholar-entry-desc">排序、二分、双指针、前缀和、差分与位运算。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="data-structures/">
<span class="scholar-entry-no">03</span>
<span class="scholar-entry-title"><strong>数据结构</strong><small>Data Structures</small></span>
<span class="scholar-entry-desc">从栈、堆与并查集，到树状数组、线段树和平衡树。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="graph/">
<span class="scholar-entry-no">04</span>
<span class="scholar-entry-title"><strong>图论</strong><small>Graph Theory</small></span>
<span class="scholar-entry-desc">遍历、最短路、拓扑序、生成树、连通性与网络流。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="dp/">
<span class="scholar-entry-no">05</span>
<span class="scholar-entry-title"><strong>动态规划</strong><small>Dynamic Programming</small></span>
<span class="scholar-entry-desc">状态设计、转移依赖、无后效性、空间优化与常见模型。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="math/">
<span class="scholar-entry-no">06</span>
<span class="scholar-entry-title"><strong>数学</strong><small>Mathematics</small></span>
<span class="scholar-entry-desc">数论、组合计数、概率、矩阵与多项式方法。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="strings/">
<span class="scholar-entry-no">07</span>
<span class="scholar-entry-title"><strong>字符串</strong><small>String Algorithms</small></span>
<span class="scholar-entry-desc">KMP、Trie、字符串哈希、AC 自动机与后缀结构。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
<a class="scholar-entry" href="problems/">
<span class="scholar-entry-no">08</span>
<span class="scholar-entry-title"><strong>题解索引</strong><small>Problem Archive</small></span>
<span class="scholar-entry-desc">按平台、难度、核心技巧与变种关系组织完整题解。</span>
<span class="scholar-entry-arrow" aria-hidden="true">↗</span>
</a>
</nav>
</section>
<section class="scholar-section scholar-methods">
<div class="scholar-methods-copy">
<span class="scholar-section-number">02</span>
<h2>从题面到定理</h2>
<p>一份可靠题解，应当让读者看见算法是如何被推导出来的，而不只是最后那段代码。</p>
<p class="scholar-reading-note"><span>推荐起点</span><a href="guide/problem-solving/">解题方法</a>建立统一流程，<a href="basics/binary-search/">二分查找</a>展示如何把不变量写进模板。</p>
</div>
<ol class="scholar-method-list">
<li><span>01</span><strong>约束与模型</strong><p>把数据范围翻译成时间预算，去掉故事外壳，辨认真正的状态与关系。</p></li>
<li><span>02</span><strong>朴素解</strong><p>先建立最直接的正确算法，明确它重复计算了什么，也为对拍准备基准。</p></li>
<li><span>03</span><strong>优化与证明</strong><p>用预处理、单调性、状态压缩或数据结构消除瓶颈，并给出完整正确性论证。</p></li>
<li><span>04</span><strong>实现与迁移</strong><p>检查边界、整数范围和常数；改变条件，验证结论还能否成立。</p></li>
</ol>
</section>
<footer class="scholar-colophon">
<p>“模板应当压缩已经理解的推理，而不是替代理解。”</p>
<span>Algorithm Studies · Wine &amp; Chord</span>
</footer>
</div>
