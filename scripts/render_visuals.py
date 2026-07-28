#!/usr/bin/env python3
"""Render the repository's original explanatory SVG figures and provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "figures"

INK = "#172033"
MUTED = "#5f6b7a"
LINE = "#c8d1dc"
SOFT = "#f4f7fa"
BLUE = "#2563eb"
BLUE_SOFT = "#dbeafe"
TEAL = "#0f766e"
TEAL_SOFT = "#ccfbf1"
ORANGE = "#c2410c"
ORANGE_SOFT = "#ffedd5"
PURPLE = "#6d28d9"
PURPLE_SOFT = "#ede9fe"
RED = "#b42318"
RED_SOFT = "#fee4e2"
GREEN = "#15803d"
GREEN_SOFT = "#dcfce7"
WHITE = "#ffffff"


class Canvas:
    def __init__(self, width: int, height: int, title: str, desc: str) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.desc = desc
        self.items: list[str] = []

    def rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        fill: str = WHITE,
        stroke: str = LINE,
        radius: int = 12,
        stroke_width: int = 2,
    ) -> None:
        self.items.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}"/>'
        )

    def line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        *,
        stroke: str = LINE,
        width: int = 2,
        dash: str | None = None,
        arrow: bool = False,
    ) -> None:
        attrs = [
            f'x1="{x1}"',
            f'y1="{y1}"',
            f'x2="{x2}"',
            f'y2="{y2}"',
            f'stroke="{stroke}"',
            f'stroke-width="{width}"',
            'stroke-linecap="round"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if arrow:
            attrs.append('marker-end="url(#arrow)"')
        self.items.append("<line " + " ".join(attrs) + "/>")

    def path(
        self,
        d: str,
        *,
        fill: str = "none",
        stroke: str = LINE,
        width: int = 2,
        arrow: bool = False,
        dash: str | None = None,
    ) -> None:
        attrs = [
            f'd="{d}"',
            f'fill="{fill}"',
            f'stroke="{stroke}"',
            f'stroke-width="{width}"',
            'stroke-linecap="round"',
            'stroke-linejoin="round"',
        ]
        if arrow:
            attrs.append('marker-end="url(#arrow)"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        self.items.append("<path " + " ".join(attrs) + "/>")

    def circle(
        self,
        cx: int,
        cy: int,
        radius: int,
        *,
        fill: str = WHITE,
        stroke: str = LINE,
        stroke_width: int = 2,
    ) -> None:
        self.items.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def text(
        self,
        x: int,
        y: int,
        value: str,
        *,
        size: int = 18,
        fill: str = INK,
        weight: int = 400,
        anchor: str = "start",
        family: str = "sans",
    ) -> None:
        font = (
            '"SFMono-Regular",Consolas,"Liberation Mono",monospace'
            if family == "mono"
            else '"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif'
        )
        self.items.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f"font-family='{font}'>{escape(value)}</text>"
        )

    def pill(
        self,
        x: int,
        y: int,
        width: int,
        label: str,
        *,
        fill: str = BLUE_SOFT,
        color: str = BLUE,
    ) -> None:
        self.rect(x, y, width, 36, fill=fill, stroke=fill, radius=18, stroke_width=1)
        self.text(x + width // 2, y + 24, label, size=15, fill=color, weight=600, anchor="middle")

    def node(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        subtitle: str = "",
        *,
        fill: str = WHITE,
        stroke: str = LINE,
        accent: str | None = None,
    ) -> None:
        self.rect(x, y, width, height, fill=fill, stroke=stroke, radius=12)
        if accent:
            self.rect(x, y, 6, height, fill=accent, stroke=accent, radius=3, stroke_width=0)
        self.text(x + 20, y + 31, title, size=18, weight=650)
        if subtitle:
            self.text(x + 20, y + 57, subtitle, size=14, fill=MUTED)

    def render(self) -> str:
        title_id = "figure-title"
        desc_id = "figure-desc"
        body = "\n  ".join(self.items)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="{title_id} {desc_id}">
  <title id="{title_id}">{escape(self.title)}</title>
  <desc id="{desc_id}">{escape(self.desc)}</desc>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>
    </marker>
  </defs>
  <rect width="{self.width}" height="{self.height}" fill="{WHITE}"/>
  {body}
</svg>
"""


@dataclass(frozen=True)
class Figure:
    slug: str
    title: str
    description: str
    width: int
    height: int
    placements: tuple[str, ...]
    draw: Callable[[Canvas], None]


def learning_path(c: Canvas) -> None:
    c.text(54, 48, "学习不是直线，而是带依赖的循环", size=24, weight=650)
    stages = [
        (54, "0", "解题闭环", "读题 · 暴力 · 验证", BLUE, BLUE_SOFT),
        (230, "1", "基础工具箱", "扫描 · 排序 · 二分", TEAL, TEAL_SOFT),
        (406, "2", "结构与搜索", "栈队列 · 图遍历", PURPLE, PURPLE_SOFT),
        (582, "3", "模型与证明", "DP · 贪心 · 图论", ORANGE, ORANGE_SOFT),
        (758, "4", "专题与比赛", "迁移 · 复盘 · 组合", GREEN, GREEN_SOFT),
    ]
    for x, number, title, subtitle, color, fill in stages:
        c.circle(x + 65, 122, 32, fill=fill, stroke=color, stroke_width=3)
        c.text(x + 65, 130, number, size=22, fill=color, weight=700, anchor="middle")
        c.node(x, 178, 132, 84, title, subtitle, fill=WHITE, stroke=color)
    for x1, x2 in zip((151, 327, 503, 679), (230, 406, 582, 758)):
        c.line(x1, 122, x2 - 6, 122, stroke=MUTED, width=2, arrow=True)
    c.path("M 824 286 C 824 354, 118 354, 118 286", stroke=BLUE, width=3, arrow=True)
    c.rect(258, 374, 426, 42, fill=WHITE, stroke=WHITE, radius=4, stroke_width=0)
    c.text(471, 402, "比赛暴露薄弱环节，复盘把知识重新接回前置节点", size=17, fill=BLUE, weight=600, anchor="middle")


def solving_loop(c: Canvas) -> None:
    c.text(52, 48, "从可解释的暴力，到可验证的最优", size=24, weight=650)
    labels = [
        ("题目契约", "输入 · 输出 · 约束", BLUE, BLUE_SOFT),
        ("朴素解", "完整覆盖选择空间", TEAL, TEAL_SOFT),
        ("定位瓶颈", "重复计算 · 无序候选 · 冗余状态", PURPLE, PURPLE_SOFT),
        ("建立不变量", "只保留仍会影响未来的信息", ORANGE, ORANGE_SOFT),
        ("证明与实现", "边界语义与转移保持一致", GREEN, GREEN_SOFT),
        ("测试与复盘", "极值 · 对拍 · 约束迁移", RED, RED_SOFT),
    ]
    positions = [(54, 92), (360, 92), (666, 92), (666, 236), (360, 236), (54, 236)]
    for (x, y), (title, subtitle, color, fill) in zip(positions, labels):
        c.node(x, y, 240, 84, title, subtitle, fill=fill, stroke=color)
    c.line(294, 134, 348, 134, stroke=MUTED, width=2, arrow=True)
    c.line(600, 134, 654, 134, stroke=MUTED, width=2, arrow=True)
    c.line(786, 176, 786, 224, stroke=MUTED, width=2, arrow=True)
    c.line(666, 278, 612, 278, stroke=MUTED, width=2, arrow=True)
    c.line(360, 278, 306, 278, stroke=MUTED, width=2, arrow=True)
    c.path("M 174 326 C 174 392, 30 392, 30 134 C 30 82, 54 78, 78 78", stroke=BLUE, width=3, arrow=True)
    c.text(480, 372, "反例或性能不达标时，回到最早失效的假设", size=17, fill=BLUE, weight=600, anchor="middle")
    c.pill(323, 400, 150, "正确性")
    c.pill(486, 400, 150, "复杂度", fill=TEAL_SOFT, color=TEAL)
    c.text(480, 458, "每次优化都应同时回答：为什么更快？为什么仍然正确？", size=17, fill=MUTED, anchor="middle")


def growth_rates(c: Canvas) -> None:
    c.text(52, 46, "输入规模增加时，不同增长率迅速分离", size=24, weight=650)
    c.line(94, 390, 874, 390, stroke=INK, width=2, arrow=True)
    c.line(94, 390, 94, 88, stroke=INK, width=2, arrow=True)
    c.text(878, 414, "n", size=18, weight=600)
    c.text(54, 80, "工作量", size=16, weight=600)
    for x, label in ((220, "小"), (450, "中"), (680, "大")):
        c.line(x, 390, x, 398, stroke=MUTED)
        c.text(x, 422, label, size=14, fill=MUTED, anchor="middle")
    c.path("M 102 367 C 300 362, 600 350, 852 332", stroke=TEAL, width=4)
    c.text(835, 322, "n", size=17, fill=TEAL, weight=700)
    c.path("M 102 370 C 290 365, 560 330, 852 260", stroke=BLUE, width=4)
    c.text(840, 250, "n log n", size=17, fill=BLUE, weight=700, anchor="end")
    c.path("M 102 374 C 360 368, 655 300, 852 135", stroke=ORANGE, width=4)
    c.text(845, 126, "n²", size=17, fill=ORANGE, weight=700, anchor="end")
    c.path("M 102 376 C 450 374, 700 324, 812 92", stroke=RED, width=4)
    c.text(800, 84, "2ⁿ", size=17, fill=RED, weight=700, anchor="end")
    c.line(724, 104, 724, 390, stroke=LINE, dash="7 7")
    c.text(712, 116, "同一时间预算", size=14, fill=MUTED, anchor="end")
    c.text(94, 457, "示意图只比较增长趋势；实际边界还取决于常数、语言、内存与测试组数。", size=15, fill=MUTED)


def binary_boundary(c: Canvas) -> None:
    c.text(52, 46, "半开区间始终包住第一个 true", size=24, weight=650)
    x0, y, w = 92, 140, 86
    values = ["false", "false", "false", "false", "true", "true", "true", "true", "true"]
    for i, value in enumerate(values):
        color, fill = (MUTED, SOFT) if value == "false" else (BLUE, BLUE_SOFT)
        c.rect(x0 + i * w, y, w - 4, 66, fill=fill, stroke=color, radius=6)
        c.text(x0 + i * w + 41, y + 40, value, size=15, fill=color, weight=650, anchor="middle", family="mono")
        c.text(x0 + i * w + 41, y + 90, str(i), size=14, fill=MUTED, anchor="middle", family="mono")
    c.line(x0 - 8, 116, x0 + 4 * w - 2, 116, stroke=ORANGE, width=4)
    c.line(x0 + 4 * w - 2, 116, x0 + 9 * w - 4, 116, stroke=BLUE, width=4)
    c.text(x0 + 2 * w, 101, "已知不满足", size=15, fill=ORANGE, weight=600, anchor="middle")
    c.text(x0 + 6.5 * w, 101, "答案候选区", size=15, fill=BLUE, weight=600, anchor="middle")
    for x, label, color in ((x0, "l", ORANGE), (x0 + 4 * w, "mid", PURPLE), (x0 + 9 * w - 4, "r", BLUE)):
        c.line(x, 226, x, 270, stroke=color, width=3)
        c.text(x, 298, label, size=19, fill=color, weight=700, anchor="middle", family="mono")
    c.node(216, 334, 240, 72, "check(mid) = false", "令 l = mid + 1", fill=ORANGE_SOFT, stroke=ORANGE)
    c.node(504, 334, 240, 72, "check(mid) = true", "令 r = mid", fill=BLUE_SOFT, stroke=BLUE)


def sequence_pointers(c: Canvas) -> None:
    c.text(48, 44, "指针的移动方向来自“被跨过部分已经定稿”", size=23, weight=650)
    rows = [
        ("滑动窗口", "l", "r", "窗口内状态合法；右扩、左缩", TEAL, TEAL_SOFT),
        ("相向双指针", "l →", "← r", "移动受限的一侧，一次排除一批组合", BLUE, BLUE_SOFT),
        ("读写压缩", "write", "read →", "写指针之前是稳定答案前缀", PURPLE, PURPLE_SOFT),
    ]
    for row, (name, left, right, note, color, fill) in enumerate(rows):
        y = 92 + row * 118
        c.text(48, y + 23, name, size=18, weight=650)
        for i in range(9):
            c.rect(210 + i * 58, y, 52, 48, fill=fill if 2 <= i <= 6 else SOFT, stroke=color if 2 <= i <= 6 else LINE, radius=5)
            c.text(236 + i * 58, y + 31, str(i), size=14, fill=MUTED, anchor="middle", family="mono")
        c.text(210 + 2 * 58, y - 10, left, size=15, fill=color, weight=700, anchor="middle", family="mono")
        c.text(210 + 6 * 58 + 52, y - 10, right, size=15, fill=color, weight=700, anchor="middle", family="mono")
        c.text(210, y + 76, note, size=15, fill=MUTED)


def prefix_difference(c: Canvas) -> None:
    c.text(48, 44, "区间信息可以留在两个边界，再由前缀扫描恢复", size=23, weight=650)
    x0, y, w = 72, 104, 92
    for i, value in enumerate((2, 1, 0, 3, 0, 2, 1, 0, 0)):
        c.rect(x0 + i * w, y, w - 6, 58, fill=SOFT, stroke=LINE, radius=5)
        c.text(x0 + i * w + 43, y + 36, str(value), size=17, anchor="middle", family="mono")
        c.text(x0 + i * w + 43, y + 82, str(i), size=13, fill=MUTED, anchor="middle", family="mono")
    l, r = x0 + 2 * w, x0 + 6 * w + w - 6
    c.line(l, 194, r, 194, stroke=BLUE, width=5)
    c.text((l + r) // 2, 222, "给区间 [l, r] 整体加 v", size=16, fill=BLUE, weight=650, anchor="middle")
    c.line(l, 244, l, 288, stroke=TEAL, width=3, arrow=True)
    c.line(r, 244, r, 288, stroke=ORANGE, width=3, arrow=True)
    c.node(l - 72, 304, 180, 70, "diff[l] += v", "贡献从这里开始", fill=TEAL_SOFT, stroke=TEAL)
    c.node(r - 108, 304, 198, 70, "diff[r + 1] -= v", "贡献从这里撤销", fill=ORANGE_SOFT, stroke=ORANGE)
    c.path("M 300 402 C 410 446, 560 446, 670 402", stroke=PURPLE, width=3, arrow=True)
    c.rect(330, 442, 308, 30, fill=WHITE, stroke=WHITE, radius=3, stroke_width=0)
    c.text(484, 465, "一次前缀和恢复每个位置的净增量", size=16, fill=PURPLE, weight=650, anchor="middle")


def top_k_filter(c: Canvas) -> None:
    c.text(48, 44, "只保留仍可能进入最终答案的候选", size=23, weight=650)
    stream = [4, 1, 9, 3, 8, 2, 7]
    for i, value in enumerate(stream):
        x = 58 + i * 70
        c.circle(x, 124, 25, fill=SOFT, stroke=LINE)
        c.text(x, 131, str(value), size=18, anchor="middle", family="mono")
    c.text(58, 82, "输入流", size=16, fill=MUTED, weight=600)
    c.line(556, 124, 642, 124, stroke=BLUE, width=3, arrow=True)
    c.node(652, 86, 250, 78, "大小为 k 的候选集", "队首是最容易被淘汰者", fill=BLUE_SOFT, stroke=BLUE)
    c.text(74, 248, "读到新值 x", size=18, weight=650)
    c.node(228, 210, 206, 76, "候选未满", "直接加入 x", fill=TEAL_SOFT, stroke=TEAL)
    c.node(520, 210, 206, 76, "x > 当前最小", "淘汰最小，再加入 x", fill=ORANGE_SOFT, stroke=ORANGE)
    c.node(374, 332, 206, 76, "x ≤ 当前最小", "永久丢弃 x", fill=SOFT, stroke=MUTED)
    c.path("M 176 252 C 194 252, 200 248, 218 248", stroke=MUTED, arrow=True)
    c.path("M 176 260 C 340 302, 430 302, 510 260", stroke=MUTED, arrow=True)
    c.path("M 622 294 C 622 326, 590 348, 590 348", stroke=MUTED, arrow=True)
    c.text(480, 452, "被第 k 大阈值压住的历史元素，以后不会因只插入而重新成为候选。", size=16, fill=MUTED, anchor="middle")


def pair_extrema(c: Canvas) -> None:
    c.text(48, 44, "从完整顺序中，只抽取答案真正需要的两项信息", size=23, weight=650)
    values = [3, 5, 2, 8, 6, 9]
    for i, value in enumerate(values):
        x = 62 + i * 73
        c.rect(x, 90, 58, 58, fill=SOFT, stroke=LINE, radius=6)
        c.text(x + 29, 126, str(value), size=18, anchor="middle", family="mono")
    c.line(520, 119, 600, 119, stroke=MUTED, width=3, arrow=True)
    c.node(616, 82, 264, 76, "扫描状态", "max₁ = 9, max₂ = 8", fill=BLUE_SOFT, stroke=BLUE)
    c.node(72, 230, 224, 92, "枚举所有数对", "O(n²) · 信息最完整", fill=SOFT, stroke=MUTED)
    c.node(368, 230, 224, 92, "排序全部元素", "O(n log n) · 顺序过剩", fill=ORANGE_SOFT, stroke=ORANGE)
    c.node(664, 230, 224, 92, "维护前二", "O(n) · 恰好充分", fill=TEAL_SOFT, stroke=TEAL)
    c.line(296, 276, 356, 276, stroke=MUTED, arrow=True)
    c.line(592, 276, 652, 276, stroke=MUTED, arrow=True)
    c.text(480, 390, "目标对两个非负因子都单调，因此任何非前二元素都可被更大的候选替换。", size=16, fill=MUTED, anchor="middle")


def signed_extrema(c: Canvas) -> None:
    c.text(48, 44, "负号使最大乘积同时依赖数轴两端", size=23, weight=650)
    c.line(82, 190, 876, 190, stroke=INK, width=2, arrow=True)
    points = [(-10, 116), (-10, 178), (1, 574), (2, 664), (3, 754)]
    for value, x in points:
        color = ORANGE if value < 0 else BLUE
        fill = ORANGE_SOFT if value < 0 else BLUE_SOFT
        c.circle(x, 190, 22, fill=fill, stroke=color, stroke_width=3)
        c.text(x, 197, str(value), size=16, fill=color, weight=700, anchor="middle", family="mono")
    c.path("M 574 146 C 630 92, 704 92, 754 146", stroke=BLUE, width=4)
    c.text(666, 82, "h₃ · h₂ · h₁ = 6", size=17, fill=BLUE, weight=650, anchor="middle")
    c.path("M 116 236 C 252 332, 610 332, 754 236", stroke=ORANGE, width=4)
    c.text(432, 350, "l₁ · l₂ · h₁ = 300", size=17, fill=ORANGE, weight=650, anchor="middle")
    c.node(158, 390, 252, 70, "三个最大值", "覆盖三个非负或全负候选", fill=BLUE_SOFT, stroke=BLUE)
    c.node(550, 390, 252, 70, "两个最小值 + 最大值", "覆盖一正两负候选", fill=ORANGE_SOFT, stroke=ORANGE)


def linked_list_rewire(c: Canvas) -> None:
    c.text(48, 44, "改写 next 之前，先保存尚未处理后缀的入口", size=23, weight=650)
    xs = [124, 280, 436, 592, 748]
    for i, x in enumerate(xs, 1):
        c.rect(x, 114, 78, 52, fill=SOFT, stroke=LINE, radius=8)
        c.text(x + 39, 147, str(i), size=18, anchor="middle", family="mono")
        if i < 5:
            c.line(x + 80, 140, xs[i] - 6, 140, stroke=MUTED, arrow=True)
    c.text(124, 94, "prev", size=15, fill=BLUE, weight=700, anchor="middle", family="mono")
    c.text(280, 94, "current", size=15, fill=ORANGE, weight=700, anchor="middle", family="mono")
    c.text(436, 94, "next", size=15, fill=TEAL, weight=700, anchor="middle", family="mono")
    c.path("M 318 190 C 290 252, 222 252, 202 190", stroke=ORANGE, width=3, arrow=True)
    c.text(260, 280, "current->next = prev", size=16, fill=ORANGE, weight=650, anchor="middle", family="mono")
    c.line(436, 214, 590, 214, stroke=TEAL, width=4)
    c.text(513, 246, "未处理后缀仍可达", size=15, fill=TEAL, weight=650, anchor="middle")
    c.node(90, 330, 226, 78, "已反转前缀", "由 prev 指向", fill=BLUE_SOFT, stroke=BLUE)
    c.node(367, 330, 226, 78, "当前局部接线", "只修改一条边", fill=ORANGE_SOFT, stroke=ORANGE)
    c.node(644, 330, 226, 78, "未处理后缀", "由 next 保留入口", fill=TEAL_SOFT, stroke=TEAL)


def monotonic_queue(c: Canvas) -> None:
    c.text(48, 44, "队列只保留尚未过期、也尚未被支配的下标", size=23, weight=650)
    values = [1, 3, -1, -3, 5, 3, 6, 7]
    x0, base = 74, 246
    scale = 16
    for i, value in enumerate(values):
        h = (value + 4) * scale
        fill = BLUE_SOFT if i in (4, 6, 7) else SOFT
        stroke = BLUE if i in (4, 6, 7) else LINE
        c.rect(x0 + i * 88, base - h, 54, h, fill=fill, stroke=stroke, radius=4)
        c.text(x0 + i * 88 + 27, base + 26, str(value), size=15, anchor="middle", family="mono")
        c.text(x0 + i * 88 + 27, base + 48, f"i={i}", size=12, fill=MUTED, anchor="middle", family="mono")
    c.line(54, base, 890, base, stroke=INK)
    c.node(78, 326, 242, 78, "队首淘汰：过期", "下标已经离开窗口", fill=ORANGE_SOFT, stroke=ORANGE)
    c.node(359, 326, 242, 78, "队尾淘汰：被支配", "更晚的新值还不小", fill=RED_SOFT, stroke=RED)
    c.node(640, 326, 242, 78, "保留：仍可能成为最大值", "下标递增，值严格递减", fill=BLUE_SOFT, stroke=BLUE)
    c.text(480, 454, "每个下标只入队一次、出队一次，因此总弹出次数是 O(n)。", size=16, fill=MUTED, anchor="middle")


def lru_composition(c: Canvas) -> None:
    c.text(48, 44, "定位与顺序是两种不同的信息，需要两种结构协作", size=23, weight=650)
    c.node(58, 102, 238, 80, "哈希表", "key → 稳定节点引用", fill=BLUE_SOFT, stroke=BLUE)
    keys = [("A", 220), ("B", 282), ("C", 344)]
    for key, y in keys:
        c.rect(82, y, 80, 48, fill=SOFT, stroke=LINE, radius=7)
        c.text(122, y + 31, key, size=17, anchor="middle", family="mono")
    c.text(82, 292, "O(1) 定位", size=16, fill=BLUE, weight=650)
    nodes = [("MRU", "C", 376, TEAL), ("", "A", 520, BLUE), ("LRU", "B", 664, ORANGE)]
    for label, key, x, color in nodes:
        c.rect(x, 188, 112, 64, fill=WHITE, stroke=color, radius=8, stroke_width=3)
        c.text(x + 56, 228, key, size=20, fill=color, weight=700, anchor="middle", family="mono")
        if label:
            c.text(x + 56, 172, label, size=14, fill=color, weight=700, anchor="middle", family="mono")
    c.line(488, 220, 514, 220, stroke=MUTED, arrow=True)
    c.line(632, 220, 658, 220, stroke=MUTED, arrow=True)
    c.line(658, 240, 632, 240, stroke=MUTED, arrow=True)
    c.line(514, 240, 488, 240, stroke=MUTED, arrow=True)
    c.text(538, 292, "双向链表维护从新到旧的顺序", size=16, fill=MUTED, anchor="middle")
    for y, target_x in ((220, 720), (282, 576), (344, 432)):
        c.path(f"M 164 {y + 24} C 260 {y + 24}, 260 220, {target_x - 8} 220", stroke=BLUE, width=2, arrow=True)
    c.node(382, 370, 394, 72, "一次命中", "哈希定位节点 → 从原位置摘除 → 移到 MRU", fill=TEAL_SOFT, stroke=TEAL)


def graph_selector(c: Canvas) -> None:
    c.text(48, 44, "先识别边的语义，再选择遍历或最短路工具", size=23, weight=650)
    c.node(62, 92, 228, 76, "只问可达 / 连通？", "DFS 或 BFS", fill=BLUE_SOFT, stroke=BLUE)
    c.node(366, 92, 228, 76, "边权全部相同？", "BFS 按层得到最短步数", fill=TEAL_SOFT, stroke=TEAL)
    c.node(670, 92, 228, 76, "边权需要累计？", "进入最短路分支", fill=ORANGE_SOFT, stroke=ORANGE)
    c.line(290, 130, 354, 130, stroke=MUTED, arrow=True)
    c.line(594, 130, 658, 130, stroke=MUTED, arrow=True)
    c.node(90, 254, 218, 78, "权值只有 0 / 1", "0-1 BFS · deque", fill=PURPLE_SOFT, stroke=PURPLE)
    c.node(371, 254, 218, 78, "权值非负", "Dijkstra · heap", fill=BLUE_SOFT, stroke=BLUE)
    c.node(652, 254, 218, 78, "存在负边", "Bellman–Ford / DAG", fill=RED_SOFT, stroke=RED)
    c.path("M 784 172 C 784 212, 760 222, 760 244", stroke=ORANGE, width=3, arrow=True)
    c.path("M 784 172 C 700 212, 500 212, 500 244", stroke=ORANGE, width=3, arrow=True)
    c.path("M 784 172 C 620 204, 202 204, 202 244", stroke=ORANGE, width=3, arrow=True)
    c.text(480, 418, "若目标、边权或状态含义改变，算法选择也必须重新证明。", size=17, fill=MUTED, anchor="middle")


def parity_state(c: Canvas) -> None:
    c.text(48, 44, "把“到达点 u 时的奇偶”提升为显式状态", size=23, weight=650)
    base_nodes = [(114, 140, "s"), (280, 90, "a"), (280, 190, "b"), (446, 140, "t")]
    for x, y, label in base_nodes:
        c.circle(x, y, 25, fill=SOFT, stroke=LINE)
        c.text(x, y + 7, label, size=18, anchor="middle", family="mono")
    for x1, y1, x2, y2, w in ((139, 132, 254, 98, 0), (139, 148, 254, 182, 1), (305, 98, 421, 132, 1), (305, 182, 421, 148, 0)):
        c.line(x1, y1, x2, y2, stroke=BLUE if w == 0 else ORANGE, width=3, arrow=True)
        c.text((x1 + x2) // 2, (y1 + y2) // 2 - 8, str(w), size=14, fill=BLUE if w == 0 else ORANGE, weight=700, anchor="middle", family="mono")
    c.text(270, 252, "原图：边权决定是否翻转奇偶", size=15, fill=MUTED, anchor="middle")
    c.line(500, 70, 500, 302, stroke=LINE, dash="7 7")
    for row, parity in enumerate(("even", "odd")):
        y = 112 + row * 126
        c.text(548, y + 7, parity, size=15, fill=TEAL if row == 0 else PURPLE, weight=700, family="mono")
        for col, label in enumerate(("s", "a", "b", "t")):
            x = 650 + col * 78
            color = TEAL if row == 0 else PURPLE
            fill = TEAL_SOFT if row == 0 else PURPLE_SOFT
            c.circle(x, y, 22, fill=fill, stroke=color)
            c.text(x, y + 6, label, size=14, fill=color, weight=700, anchor="middle", family="mono")
    c.line(672, 112, 706, 112, stroke=TEAL, arrow=True)
    c.line(750, 112, 784, 238, stroke=ORANGE, arrow=True)
    c.line(672, 238, 706, 112, stroke=ORANGE, arrow=True)
    c.line(750, 238, 784, 238, stroke=PURPLE, arrow=True)
    c.text(724, 292, "乘积图：(u, parity)", size=15, fill=MUTED, anchor="middle", family="mono")
    c.node(198, 350, 564, 72, "统一转移", "沿权值 w 的边：(u, p) → (v, p xor w)", fill=BLUE_SOFT, stroke=BLUE)


def tree_postorder(c: Canvas) -> None:
    c.text(48, 44, "父节点只需要子树摘要，不需要反复扫描整棵子树", size=23, weight=650)
    nodes = [(480, 92, "u", BLUE), (286, 194, "a", TEAL), (674, 194, "b", TEAL), (204, 316, "c", PURPLE), (368, 316, "d", PURPLE), (592, 316, "e", PURPLE), (756, 316, "f", PURPLE)]
    for x1, y1, x2, y2 in ((464, 114, 302, 172), (496, 114, 658, 172), (274, 216, 218, 294), (298, 216, 354, 294), (662, 216, 606, 294), (686, 216, 742, 294)):
        c.line(x1, y1, x2, y2, stroke=LINE, width=3)
    for x, y, label, color in nodes:
        fill = BLUE_SOFT if color == BLUE else TEAL_SOFT if color == TEAL else PURPLE_SOFT
        c.circle(x, y, 25, fill=fill, stroke=color, stroke_width=3)
        c.text(x, y + 7, label, size=18, fill=color, weight=700, anchor="middle", family="mono")
    for x1, y1, x2, y2 in ((220, 290, 272, 218), (352, 290, 300, 218), (608, 290, 660, 218), (740, 290, 688, 218), (306, 180, 458, 116), (654, 180, 502, 116)):
        c.line(x1, y1, x2, y2, stroke=ORANGE, width=3, arrow=True)
    c.text(480, 374, "叶 → 子树根 → 父节点", size=17, fill=ORANGE, weight=650, anchor="middle")
    c.text(480, 418, "返回值必须恰好包含父节点合并所需的信息。", size=16, fill=MUTED, anchor="middle")


def dp_dag(c: Canvas) -> None:
    c.text(48, 44, "转移式定义依赖边，循环顺序就是 DAG 的拓扑序", size=23, weight=650)
    positions = [(116, 232, "dp[0]"), (294, 134, "dp[1]"), (294, 330, "dp[2]"), (494, 134, "dp[3]"), (494, 330, "dp[4]"), (704, 232, "dp[5]")]
    edges = [(154, 220, 250, 154), (154, 244, 250, 310), (338, 134, 450, 134), (338, 330, 450, 330), (338, 150, 462, 306), (338, 314, 462, 158), (538, 134, 660, 216), (538, 330, 660, 248)]
    for x1, y1, x2, y2 in edges:
        c.line(x1, y1, x2, y2, stroke=MUTED, width=2, arrow=True)
    for i, (x, y, label) in enumerate(positions):
        color = BLUE if i in (0, 5) else TEAL if i in (1, 2) else PURPLE
        fill = BLUE_SOFT if color == BLUE else TEAL_SOFT if color == TEAL else PURPLE_SOFT
        c.rect(x, y - 30, 88, 60, fill=fill, stroke=color, radius=9)
        c.text(x + 44, y + 6, label, size=15, fill=color, weight=700, anchor="middle", family="mono")
    c.pill(174, 416, 164, "状态：保留什么")
    c.pill(398, 416, 164, "转移：最后一步", fill=TEAL_SOFT, color=TEAL)
    c.pill(622, 416, 164, "顺序：依赖先算", fill=PURPLE_SOFT, color=PURPLE)


def recurrence_collapse(c: Canvas) -> None:
    c.text(48, 44, "优化存储之前，先看清状态依赖", size=23, weight=650)
    c.node(54, 92, 214, 78, "递归树", "重复展开相同子问题", fill=RED_SOFT, stroke=RED)
    c.node(374, 92, 214, 78, "记忆 / 递推表", "每个状态只计算一次", fill=BLUE_SOFT, stroke=BLUE)
    c.node(694, 92, 214, 78, "滚动状态", "只保留下一步仍依赖的值", fill=TEAL_SOFT, stroke=TEAL)
    c.line(268, 131, 362, 131, stroke=MUTED, arrow=True)
    c.line(588, 131, 682, 131, stroke=MUTED, arrow=True)
    c.circle(160, 240, 24, fill=RED_SOFT, stroke=RED)
    c.text(160, 247, "f₅", size=16, anchor="middle", family="mono")
    for x, label in ((104, "f₄"), (216, "f₃")):
        c.circle(x, 308, 22, fill=SOFT, stroke=LINE)
        c.text(x, 315, label, size=14, anchor="middle", family="mono")
        c.line(148 if x == 104 else 172, 260, x, 286, stroke=MUTED)
    c.circle(160, 372, 20, fill=ORANGE_SOFT, stroke=ORANGE)
    c.text(160, 378, "f₃", size=13, anchor="middle", family="mono")
    c.line(116, 326, 148, 354, stroke=MUTED)
    for i in range(6):
        color = BLUE if i >= 3 else LINE
        c.rect(360 + i * 44, 270, 40, 44, fill=BLUE_SOFT if i >= 3 else SOFT, stroke=color, radius=5)
        c.text(380 + i * 44, 298, f"f{i}", size=12, anchor="middle", family="mono")
    c.text(486, 344, "按依赖方向填表", size=15, fill=BLUE, weight=650, anchor="middle")
    c.rect(728, 254, 68, 68, fill=TEAL_SOFT, stroke=TEAL, radius=9)
    c.rect(814, 254, 68, 68, fill=TEAL_SOFT, stroke=TEAL, radius=9)
    c.text(762, 295, "a", size=22, fill=TEAL, weight=700, anchor="middle", family="mono")
    c.text(848, 295, "b", size=22, fill=TEAL, weight=700, anchor="middle", family="mono")
    c.line(798, 288, 808, 288, stroke=TEAL, arrow=True)
    c.text(805, 354, "新值只依赖最近状态", size=15, fill=TEAL, weight=650, anchor="middle")
    c.text(480, 442, "空间压缩改变存储，不改变状态定义、转移和正确性。", size=16, fill=MUTED, anchor="middle")


def edit_distance_grid(c: Canvas) -> None:
    c.text(48, 44, "编辑距离：每个格子枚举最后一次操作", size=23, weight=650)
    x0, y0, cell = 210, 102, 58
    rows, cols = "horse", "ros"
    c.text(x0 - 68, y0 - 12, "source", size=14, fill=MUTED, family="mono")
    c.text(x0 + 110, y0 - 30, "target", size=14, fill=MUTED, family="mono")
    for j, ch in enumerate(" " + cols):
        c.text(x0 + j * cell + cell // 2, y0 - 12, ch if ch != " " else "∅", size=16, fill=BLUE, weight=650, anchor="middle", family="mono")
    for i, ch in enumerate(" " + rows):
        c.text(x0 - 20, y0 + i * cell + 35, ch if ch != " " else "∅", size=16, fill=TEAL, weight=650, anchor="middle", family="mono")
        for j in range(len(cols) + 1):
            fill = BLUE_SOFT if (i, j) in ((0, 0), (1, 1), (2, 1), (3, 2), (4, 2), (5, 3)) else SOFT
            stroke = BLUE if fill == BLUE_SOFT else LINE
            c.rect(x0 + j * cell, y0 + i * cell, cell - 4, cell - 4, fill=fill, stroke=stroke, radius=4)
            if i == 0:
                value = j
            elif j == 0:
                value = i
            else:
                value = ""
            if value != "":
                c.text(x0 + j * cell + 27, y0 + i * cell + 34, str(value), size=14, anchor="middle", family="mono")
    tx, ty = x0 + 3 * cell, y0 + 5 * cell
    c.line(tx - cell + 26, ty - cell + 26, tx + 10, ty + 10, stroke=PURPLE, width=3, arrow=True)
    c.line(tx - cell + 26, ty + 26, tx + 10, ty + 26, stroke=ORANGE, width=3, arrow=True)
    c.line(tx + 26, ty - cell + 26, tx + 26, ty + 10, stroke=TEAL, width=3, arrow=True)
    c.node(560, 136, 292, 68, "替换 / 匹配", "dp[i - 1][j - 1]", fill=PURPLE_SOFT, stroke=PURPLE)
    c.node(560, 234, 292, 68, "删除", "dp[i - 1][j]", fill=TEAL_SOFT, stroke=TEAL)
    c.node(560, 332, 292, 68, "插入", "dp[i][j - 1]", fill=ORANGE_SOFT, stroke=ORANGE)


def residue_cycle(c: Canvas) -> None:
    c.text(48, 44, "让前缀余数恰好每隔 k 步再次相遇", size=23, weight=650)
    cx, cy, radius = 278, 246, 142
    positions = [(278, 104), (413, 202), (362, 356), (194, 356), (143, 202)]
    for i, (x, y) in enumerate(positions):
        c.circle(x, y, 25, fill=BLUE_SOFT, stroke=BLUE, stroke_width=3)
        c.text(x, y + 7, str(i), size=17, fill=BLUE, weight=700, anchor="middle", family="mono")
    for (x1, y1), (x2, y2) in zip(positions, positions[1:] + positions[:1]):
        c.line(x1, y1, x2, y2, stroke=TEAL, width=3, arrow=True)
    c.text(cx, cy - 6, "Rᵢ = i mod k", size=19, fill=TEAL, weight=700, anchor="middle", family="mono")
    c.text(cx, cy + 26, "示例 k = 5", size=15, fill=MUTED, anchor="middle")
    c.node(532, 108, 322, 76, "距离 < k", "窗口内余数互异，没有过短碰撞", fill=TEAL_SOFT, stroke=TEAL)
    c.node(532, 220, 322, 76, "距离 = k", "相同余数首次重现，目标区间出现", fill=BLUE_SOFT, stroke=BLUE)
    c.node(532, 332, 322, 76, "可实现性", "相邻余数差映射为 [1, m] 内正数", fill=ORANGE_SOFT, stroke=ORANGE)


def factorial_blocks(c: Canvas) -> None:
    c.text(48, 44, "固定前缀后，全部后缀排列形成连续字典序块", size=23, weight=650)
    colors = [(BLUE, BLUE_SOFT), (TEAL, TEAL_SOFT), (ORANGE, ORANGE_SOFT), (PURPLE, PURPLE_SOFT)]
    x = 66
    widths = [196, 196, 196, 196]
    for i, (width, (color, fill)) in enumerate(zip(widths, colors), 1):
        c.rect(x, 100, width, 116, fill=fill, stroke=color, radius=8, stroke_width=3)
        c.text(x + width // 2, 142, f"首位选 {i}", size=18, fill=color, weight=700, anchor="middle")
        c.text(x + width // 2, 178, "后缀共有 3! 种", size=16, fill=MUTED, anchor="middle")
        c.text(x + width // 2, 202, f"排名区间 [{(i - 1) * 6}, {i * 6 - 1}]", size=14, fill=color, anchor="middle", family="mono")
        x += width + 14
    c.text(68, 278, "目标排列 3 1 4 2", size=19, weight=650, family="mono")
    digits = [("c₀ = 2", "跳过首位 1、2 的两个 3! 块"), ("c₁ = 0", "剩余值中没有比 1 更小者"), ("c₂ = 1", "跳过一个 1! 块")]
    for i, (digit, note) in enumerate(digits):
        y = 316 + i * 54
        c.pill(68, y, 124, digit, fill=BLUE_SOFT if i == 0 else SOFT, color=BLUE if i == 0 else INK)
        c.text(216, y + 24, note, size=15, fill=MUTED)
    c.node(624, 310, 264, 112, "Lehmer 码", "rank = Σ cᵢ · (n-i-1)!", fill=PURPLE_SOFT, stroke=PURPLE)


def palindrome_radius(c: Canvas) -> None:
    c.text(48, 44, "中心与半径统一描述连续回文", size=23, weight=650)
    chars = list("# a # b # a # c # a # b # a #".split())
    x0, y, step = 76, 144, 50
    for i, ch in enumerate(chars):
        fill = BLUE_SOFT if 4 <= i <= 10 else SOFT
        stroke = BLUE if 4 <= i <= 10 else LINE
        c.circle(x0 + i * step, y, 20, fill=fill, stroke=stroke)
        c.text(x0 + i * step, y + 6, ch, size=15, fill=INK, anchor="middle", family="mono")
    center = x0 + 7 * step
    c.line(center, 84, center, 196, stroke=PURPLE, width=3, dash="6 6")
    c.text(center, 74, "center", size=15, fill=PURPLE, weight=700, anchor="middle", family="mono")
    c.path(f"M {x0 + 4 * step} 216 C {center - 100} 276, {center + 100} 276, {x0 + 10 * step} 216", stroke=BLUE, width=4)
    c.text(center, 286, "radius = 3", size=16, fill=BLUE, weight=700, anchor="middle", family="mono")
    c.node(84, 340, 238, 76, "中心扩展", "每个中心独立向两侧比较", fill=TEAL_SOFT, stroke=TEAL)
    c.node(361, 340, 238, 76, "Manacher 复用", "区间内先取镜像半径下界", fill=PURPLE_SOFT, stroke=PURPLE)
    c.node(638, 340, 238, 76, "继续扩张", "只有最右边界会贡献新比较", fill=BLUE_SOFT, stroke=BLUE)


def palindrome_half(c: Canvas) -> None:
    c.text(48, 44, "回文重排只需决定左半边", size=23, weight=650)
    c.node(54, 96, 252, 82, "字符频次", "a: 4 · b: 2 · c: 1", fill=SOFT, stroke=LINE)
    c.line(306, 137, 362, 137, stroke=MUTED, arrow=True)
    c.node(374, 96, 212, 82, "左半边", "a a b", fill=BLUE_SOFT, stroke=BLUE)
    c.line(586, 137, 642, 137, stroke=MUTED, arrow=True)
    c.node(654, 96, 252, 82, "完整回文", "a a b | c | b a a", fill=TEAL_SOFT, stroke=TEAL)
    chars = list("aabcbaa")
    for i, ch in enumerate(chars):
        x = 190 + i * 84
        color = BLUE if i < 3 else ORANGE if i == 3 else TEAL
        fill = BLUE_SOFT if i < 3 else ORANGE_SOFT if i == 3 else TEAL_SOFT
        c.rect(x, 252, 62, 62, fill=fill, stroke=color, radius=7)
        c.text(x + 31, 291, ch, size=22, fill=color, weight=700, anchor="middle", family="mono")
    c.line(190, 334, 420, 334, stroke=BLUE, width=4)
    c.line(526, 334, 756, 334, stroke=TEAL, width=4)
    c.text(305, 362, "按字典序优化", size=15, fill=BLUE, weight=650, anchor="middle")
    c.text(641, 362, "左半边镜像", size=15, fill=TEAL, weight=650, anchor="middle")
    c.text(473, 362, "奇频中心", size=15, fill=ORANGE, weight=650, anchor="middle")
    c.text(480, 424, "每个合法答案与一个左半边排列一一对应。", size=17, fill=MUTED, anchor="middle")


FIGURES = (
    Figure("learning-path", "算法学习路径", "从解题闭环到专题训练，并通过比赛复盘回到薄弱前置知识。", 960, 470, ("docs/guide/roadmap.md",), learning_path),
    Figure("solving-loop", "算法解题闭环", "从题目契约、朴素解和瓶颈分析走向不变量、证明、实现与测试。", 960, 470, ("docs/guide/problem-solving.md",), solving_loop),
    Figure("growth-rates", "常见复杂度增长趋势", "线性、线性对数、平方和指数增长率随输入规模增加而分离。", 960, 480, ("docs/guide/complexity.md",), growth_rates),
    Figure("binary-search-boundary", "二分查找边界不变量", "半开搜索区间包围单调布尔序列中第一个为真的位置。", 960, 450, ("docs/basics/binary-search.md",), binary_boundary),
    Figure("sequence-pointer-invariants", "序列扫描的指针不变量", "滑动窗口、相向双指针和读写压缩对应不同的定稿语义。", 960, 450, ("docs/basics/sequence-invariants.md",), sequence_pointers),
    Figure("prefix-difference-boundaries", "差分的区间边界事件", "区间加法在左边界开始、右边界之后撤销，再由前缀和恢复。", 960, 480, ("docs/basics/prefix-sums-and-difference.md",), prefix_difference),
    Figure("top-k-candidate-filter", "Top-K 候选过滤", "输入流经过大小为 k 的候选集，永久淘汰不可能进入答案的元素。", 960, 480, ("docs/basics/top-k-extrema.md",), top_k_filter),
    Figure("pair-product-information", "非负两数乘积的信息压缩", "枚举、排序和前二扫描逐步减少不必要信息。", 960, 440, ("docs/basics/pair-product-extrema.md",), pair_extrema),
    Figure("signed-product-extrema", "有符号三数乘积的双端候选", "最大乘积只需比较三个最大值与两个最小值加最大值。", 960, 480, ("docs/basics/signed-product-extrema.md",), signed_extrema),
    Figure("linked-list-rewire", "单链表局部接线", "反转当前边之前保存后继，从而不丢失尚未处理后缀。", 960, 460, ("docs/data-structures/linked-lists.md",), linked_list_rewire),
    Figure("monotonic-queue-elimination", "单调队列的两类淘汰", "队首按窗口过期，队尾按值支配淘汰，剩余候选保持单调。", 960, 480, ("docs/data-structures/monotonic-queues.md",), monotonic_queue),
    Figure("lru-composition", "LRU 的哈希表与双向链表", "哈希表负责按键定位，双向链表负责维护最近使用顺序。", 960, 470, ("docs/data-structures/hash-and-cache.md",), lru_composition),
    Figure("graph-algorithm-selector", "图算法选择路径", "按可达性、边权与负边条件选择 DFS、BFS、0-1 BFS、Dijkstra 或其他工具。", 960, 450, ("docs/graph/index.md",), graph_selector),
    Figure("parity-product-state", "奇偶乘积状态图", "将原图节点与路径奇偶组合为显式状态，并按边权翻转奇偶。", 960, 460, ("docs/graph/weighted-parity-states.md",), parity_state),
    Figure("tree-postorder-aggregation", "树上后序聚合", "叶和子树的摘要沿后序向父节点汇合。", 960, 450, ("docs/graph/tree-aggregation.md",), tree_postorder),
    Figure("dp-state-dag", "动态规划状态依赖 DAG", "状态转移形成有向无环依赖，递推顺序必须先计算前驱。", 960, 470, ("docs/dp/index.md",), dp_dag),
    Figure("recurrence-state-collapse", "线性递推的状态压缩", "递归树先去重成递推表，再按依赖窗口压缩为滚动状态。", 960, 470, ("docs/dp/linear-recurrences.md",), recurrence_collapse),
    Figure("edit-distance-grid", "编辑距离状态网格", "每个双序列前缀状态从替换、删除和插入三个前驱转移。", 960, 480, ("docs/dp/sequence-dp.md",), edit_distance_grid),
    Figure("residue-cycle", "前缀余数周期构造", "余数状态在距离 k 处首次重复，从而排除更短的整除子数组。", 960, 460, ("docs/math/modular-constructions.md",), residue_cycle),
    Figure("factorial-blocks", "排列字典序的阶乘块", "固定前缀后每个候选值对应一个连续的后缀排列块。", 960, 490, ("docs/math/permutation-ranking.md",), factorial_blocks),
    Figure("palindrome-radius", "回文中心与半径", "插入分隔符后奇偶回文统一为中心和半径，并可复用镜像半径。", 960, 460, ("docs/strings/palindrome-centers.md",), palindrome_radius),
    Figure("palindrome-half", "回文重排的左半边降维", "频次决定左半边和中心，右半边由镜像唯一确定。", 960, 450, ("docs/strings/palindrome-rearrangements.md",), palindrome_half),
)


def render_all(output: Path) -> int:
    output.mkdir(parents=True, exist_ok=True)
    expected = {f"{figure.slug}.svg" for figure in FIGURES}
    for stale in output.glob("*.svg"):
        if stale.name not in expected:
            stale.unlink()
    assets = []
    for figure in FIGURES:
        canvas = Canvas(figure.width, figure.height, figure.title, figure.description)
        figure.draw(canvas)
        path = output / f"{figure.slug}.svg"
        payload = canvas.render()
        path.write_text(payload, encoding="utf-8")
        assets.append(
            {
                "file": f"docs/assets/figures/{path.name}",
                "title": figure.title,
                "description": figure.description,
                "kind": "original-svg",
                "width": figure.width,
                "height": figure.height,
                "license": "MIT",
                "source": "Repository-authored explanatory diagram",
                "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                "placements": [
                    {"page": page, "id": f"figure-{figure.slug}"}
                    for page in figure.placements
                ],
            }
        )
    manifest = {
        "schema_version": 1,
        "generated_by": "scripts/render_visuals.py",
        "assets": assets,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return len(FIGURES)


def check_generated() -> None:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="algo-visual-check-") as directory:
        temporary = Path(directory)
        render_all(temporary)
        expected = {path.name for path in temporary.iterdir() if path.is_file()}
        actual = {
            path.name
            for path in OUT.iterdir()
            if path.is_file() and path.suffix in (".svg", ".json")
        }
        for name in sorted(expected | actual):
            wanted = temporary / name
            committed = OUT / name
            if not wanted.is_file():
                errors.append(f"unexpected generated asset: {committed.relative_to(ROOT)}")
            elif not committed.is_file():
                errors.append(f"missing generated asset: {committed.relative_to(ROOT)}")
            elif wanted.read_bytes() != committed.read_bytes():
                errors.append(f"stale generated asset: {committed.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Generated visual check passed: {len(FIGURES)} figures and manifest")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="render to a temporary directory and compare with committed assets",
    )
    args = parser.parse_args()
    if args.check:
        check_generated()
        return
    count = render_all(OUT)
    print(f"Rendered {count} figures and manifest")


if __name__ == "__main__":
    main()
