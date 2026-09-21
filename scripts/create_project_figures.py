#!/usr/bin/env python3
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "03_figures"
OUT.mkdir(exist_ok=True)

FONT_CANDIDATES = [
    Path("/workspace/scratch/5dac3d6fdad8/NotoSansCJKsc-Regular.otf"),
    Path("/workspace/scratch/df6aee2eaf3c/NotoSansCJKsc-Regular.otf"),
]
for candidate in FONT_CANDIDATES:
    if candidate.exists():
        font_manager.fontManager.addfont(candidate)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=str(candidate)).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#1F4E79"
MID = "#5B9BD5"
LIGHT = "#D9EAF7"
PALE = "#EEF5FA"
ORANGE = "#ED7D31"
GREEN = "#70AD47"
GRAY = "#666666"
RED = "#C00000"


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white", transparent=False)
    plt.close(fig)
    # LibreOffice has rendering defects with some RGBA PNGs; flatten to opaque RGB.
    with Image.open(path) as im:
        im.convert("RGB").save(path, optimize=True)


def box(ax, xy, wh, text, fc=PALE, ec=BLUE, fontsize=10, lw=1.4):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
                           facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color="#202020")
    return patch


def arrow(ax, p1, p2, color=BLUE, lw=1.5):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", lw=lw, color=color))


def canvas(size=(11, 5.5)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def fig_scope():
    fig, ax = canvas((11, 5.1))
    levels = [
        (0.06, "直接量测", "图像中心 + 曝光工作点\n→ 晶圆坐标与IPD", GREEN),
        (0.39, "模型解算", "低阶矩阵 + 高阶残差\n→ 空间指纹与不确定度", MID),
        (0.72, "应用验证", "Bonding风险 / Overlay预测\nAlignment与CPE输入", ORANGE),
    ]
    for x, title, body, c in levels:
        box(ax, (x, 0.35), (0.23, 0.34), f"{title}\n\n{body}", fc="#FFFFFF", ec=c, fontsize=11, lw=2)
    arrow(ax, (0.29, 0.52), (0.39, 0.52))
    arrow(ax, (0.62, 0.52), (0.72, 0.52))
    ax.text(0.175, 0.18, "1 nm主验收终点", color=RED, weight="bold", ha="center", fontsize=11)
    ax.plot([0.06, 0.29], [0.25, 0.25], color=RED, lw=2.5)
    ax.text(0.835, 0.18, "需独立工艺/Overlay真值", color=GRAY, ha="center", fontsize=10)
    ax.set_title("量测对象、模型结果与下游应用必须分层", fontsize=15, weight="bold", color=BLUE)
    save(fig, "fig01_scope.png")


def fig_coordinate_chain():
    fig, ax = canvas((12, 5.2))
    items = [
        (0.02, "原始图像\n像素中心 p"),
        (0.22, "尺度 / 方向 /\n畸变Map C"),
        (0.42, "曝光门内\n干涉坐标 r̄exp"),
        (0.62, "计量→晶圆\n变换 T"),
        (0.82, "晶圆坐标 rW\n与IPD"),
    ]
    for i, (x, label) in enumerate(items):
        color = GREEN if i == 4 else BLUE
        box(ax, (x, 0.38), (0.16, 0.28), label, fc="white", ec=color, fontsize=11, lw=2)
        if i < len(items)-1:
            arrow(ax, (x+0.16, 0.52), (items[i+1][0], 0.52))
    ax.text(0.50, 0.20, "统一时间戳 · 坐标系 · 标定版本 · 有效性", ha="center", fontsize=11, color=GRAY)
    ax.set_title("每次曝光的图像点与机械坐标形成可追溯闭环", fontsize=15, weight="bold", color=BLUE)
    save(fig, "fig02_coordinate_chain.png")


def fig_wafer_sampling():
    fig, ax = plt.subplots(figsize=(7.3, 7.3))
    wafer = Circle((0, 0), 150, facecolor="#FAFAFA", edgecolor=BLUE, lw=2)
    ax.add_patch(wafer)
    pts = [(0, 0)]
    for r in (50, 100, 140):
        for a in np.deg2rad(np.arange(0, 360, 45)):
            pts.append((r*np.cos(a), r*np.sin(a)))
    outer = sorted(pts[1:], key=lambda p: (-p[1], p[0] if int((150-p[1])//40)%2==0 else -p[0]))
    route = [pts[0]] + outer
    xs, ys = zip(*route)
    ax.plot(xs, ys, color=MID, lw=1.2, alpha=.7, zorder=1)
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=70, c=ORANGE, edgecolors="white", zorder=2)
    for idx, (x, y) in enumerate(route, 1):
        ax.text(x+4, y+4, str(idx), fontsize=7, color=GRAY)
    ax.plot([0, 0], [145, 151], color=BLUE, lw=3)
    ax.set_aspect("equal")
    ax.set_xlim(-165, 165); ax.set_ylim(-165, 165)
    ax.set_xlabel("晶圆X / mm"); ax.set_ylabel("晶圆Y / mm")
    ax.grid(alpha=.18)
    ax.set_title("中心 + 8方位×3半径的25 Die抽检几何", fontsize=14, weight="bold", color=BLUE)
    save(fig, "fig03_wafer_sampling.png")


def fig_system_architecture():
    fig, ax = canvas((12, 7.0))
    box(ax, (0.05, 0.66), (0.25, 0.19), "DUV显微成像\n图像 / 像素中心 / 质量", fc=LIGHT)
    box(ax, (0.375, 0.66), (0.25, 0.19), "运动 + 四通道干涉\n工作点 / 姿态 / 曝光门", fc=LIGHT)
    box(ax, (0.70, 0.66), (0.25, 0.19), "AF + ESC + 环境\n焦位 / 面形 / 温湿压", fc=LIGHT)
    box(ax, (0.17, 0.34), (0.66, 0.17), "统一坐标、统一时基与标定版本\n像素物方映射 + 曝光坐标 + 晶圆坐标变换", fc="white", ec=BLUE, fontsize=12, lw=2)
    box(ax, (0.17, 0.08), (0.66, 0.15), "IPD数据产品\n原始场 · 四/六参数矩阵 · 低阶重建 · 高阶残差 · 不确定度", fc="#E2F0D9", ec=GREEN, fontsize=12, lw=2)
    for x in (0.175, 0.50, 0.825):
        arrow(ax, (x, 0.66), (0.39 + (x-0.5)*0.25, 0.51))
    arrow(ax, (0.50, 0.34), (0.50, 0.23))
    ax.set_title("整机物理链与数据链在图案坐标处汇合", fontsize=15, weight="bold", color=BLUE)
    save(fig, "fig04_system_architecture.png")


def fig_error_budget():
    labels = ["图像/中心", "运动/计量", "光学映射", "ESC/面形", "温度", "全局坐标", "Z/AF"]
    vals = [0.55, 0.55, 0.35, 0.35, 0.25, 0.25, 0.15]
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    bars = ax.bar(labels, vals, color=[BLUE, MID, GREEN, GREEN, ORANGE, MID, "#A5A5A5"])
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+.02, f"{v:.2f}", ha="center", fontsize=10)
    ax.axhline(1.0, color=RED, linestyle="--", lw=1.4, label="系统目标 1.00 nm")
    ax.text(6.45, .96, "RSS = 0.999 nm", ha="right", va="top", color=RED, weight="bold")
    ax.set_ylabel("二维综合3σ工程分配 / nm")
    ax.set_ylim(0, 1.12)
    ax.grid(axis="y", alpha=.2)
    ax.set_title("V0.1一级预算：分项是补偿后残差，不是原始误差", fontsize=14, weight="bold", color=BLUE)
    save(fig, "fig05_error_budget.png")


def fig_motion_metrology():
    fig, ax = canvas((12, 5.4))
    items = [
        (0.03, "宏动平台\n大行程寻址", ORANGE),
        (0.23, "局部微动\n残余补偿", GREEN),
        (0.43, "ESC / 晶圆\n实际工作点", BLUE),
        (0.65, "四通道干涉\n平移 + Rz", MID),
        (0.83, "曝光加权坐标\n进入图像融合", GREEN),
    ]
    for i, (x, t, c) in enumerate(items):
        box(ax, (x, .40), (.15, .25), t, fc="white", ec=c, fontsize=10.5, lw=2)
        if i < len(items)-1:
            arrow(ax, (x+.15, .525), (items[i+1][0], .525))
    ax.annotate("反馈 / 前馈", xy=(.30,.69), xytext=(.71,.78), ha="center", color=BLUE,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.25", color=BLUE, lw=1.5))
    ax.text(.50,.20,"环外参考验证镜头—参考端与晶圆—平面镜未观测差模",ha="center",fontsize=10.5,color=GRAY)
    ax.set_title("控制目标是曝光期间Wafer—Lens真实相对运动", fontsize=15, weight="bold", color=BLUE)
    save(fig, "fig06_motion_metrology.png")


def fig_fit_residual():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    x, y = np.meshgrid(np.linspace(-1,1,9), np.linspace(-1,1,9))
    u_low = .09*x + .035*y
    v_low = -.03*x + .07*y
    u_high = .018*np.sin(3*np.pi*x)*np.cos(2*np.pi*y)
    v_high = .018*np.cos(2*np.pi*x)*np.sin(3*np.pi*y)
    datasets = [(u_low+u_high,v_low+v_high,"原始IPD场"),(u_low,v_low,"矩阵重建低阶"),(u_high,v_high,"Die内高阶残差")]
    for ax,(u,v,title) in zip(axes,datasets):
        ax.quiver(x,y,u,v,angles="xy",scale_units="xy",scale=.35,color=BLUE,width=.006)
        ax.set_aspect("equal"); ax.set_xlim(-1.15,1.15); ax.set_ylim(-1.15,1.15)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title,fontsize=12,weight="bold")
        for s in ax.spines.values(): s.set_color("#BBBBBB")
    fig.suptitle("完整畸变 = 低阶矩阵重建场 + 局部残差", fontsize=15, weight="bold", color=BLUE)
    save(fig, "fig07_fit_residual.png")


def fig_timing():
    fig, ax = plt.subplots(figsize=(11, 3.8))
    starts = [0, 150, 250]
    widths = [150, 100, 30]
    labels = ["XY稳定 150 ms", "AF 100 ms", "曝光/采集 30 ms"]
    colors = [BLUE, MID, GREEN]
    for s,w,l,c in zip(starts,widths,labels,colors):
        ax.barh([0], [w], left=[s], height=.42, color=c, edgecolor="white")
        ax.text(s+w/2,0,l,ha="center",va="center",color="white",fontsize=11,weight="bold")
    ax.barh([-.65],[70],left=[280],height=.25,color="#D9D9D9",edgecolor=GRAY,hatch="//")
    ax.text(315,-.65,"移动/恢复/读出/握手另计",ha="center",va="center",fontsize=9.5,color=GRAY)
    ax.axvline(280,color=RED,ls="--")
    ax.text(280,.38,"已知串行下限 280 ms",ha="right",color=RED,fontsize=10,weight="bold")
    ax.set_xlim(0,370); ax.set_ylim(-1, .7); ax.set_yticks([]); ax.set_xlabel("时间 / ms")
    ax.grid(axis="x",alpha=.18)
    ax.set_title("当前基线不是“150 ms/帧”",fontsize=14,weight="bold",color=BLUE)
    save(fig, "fig08_timing.png")


def fig_validation_ladder():
    fig, ax = canvas((10.5, 5.8))
    labels = [
        ("M0", "需求/目标"), ("M1", "机理与计算"), ("M2", "公开证据\n本机换算"),
        ("M3", "子系统试验\n原始数据 + U"), ("M4", "标准样件\n端到端盲测"), ("M5", "冻结流程\n整机复现")
    ]
    for i,(m,t) in enumerate(labels):
        x=.06+i*.15; y=.12+i*.105
        fc = LIGHT if i <= 2 else "white"
        ec = BLUE if i <= 2 else GRAY
        box(ax,(x,y),(.13,.20),f"{m}\n{t}",fc=fc,ec=ec,fontsize=9.5,lw=2)
        if i < len(labels)-1: arrow(ax,(x+.13,y+.10),(x+.15,y+.205))
    ax.text(.29,.86,"当前：M1为主、部分M2",color=RED,fontsize=12,weight="bold",ha="center")
    ax.text(.76,.18,"达到M4/M5后才能对外形成\n“已验证1 nm”结论",color=GRAY,fontsize=10.5,ha="center")
    ax.set_title("证据成熟度必须随试验逐级升级",fontsize=15,weight="bold",color=BLUE)
    save(fig, "fig09_validation_ladder.png")


if __name__ == "__main__":
    fig_scope()
    fig_coordinate_chain()
    fig_wafer_sampling()
    fig_system_architecture()
    fig_error_budget()
    fig_motion_metrology()
    fig_fit_residual()
    fig_timing()
    fig_validation_ladder()
    print(f"created 9 figures in {OUT}")
