# 1 nm IPD量测机台——技术基线

> 当前版本：v0.4  
> 状态：方案设计与分析阶段  
> 原则：只记录当前有效口径；未验证能力不得写成实测结果。

## 1. 当前工作主线

### A. 机台子系统
负责运动平台、工作点计量、Z/调平、ESC、力框/计量框、隔振、控制与settling等。

### B. 整机主线
负责整机测量流程、1 nm指标分解、误差预算、25 Die抽检策略、节拍模型及各子系统之间的统一口径。

---

## 2. 当前整机测量流程

- 🟢 Wafer级调平只执行一次。
- 🟢 自动对焦采用Sony类狭缝式光学自动对焦方案。
- 🔴 原“暂定共聚焦自动对焦”口径废弃。
- 🟢 不采用XY长距离运动中的高速随动对焦。
- 🟡 保留Focus Ready / Measurement Ready两级settling策略：XY大运动结束并进入狭缝AF可捕获状态后启动Z对焦；对焦期间XY残余振动继续衰减，图像采集前再满足最终量测稳定条件。
- 🟢 工作点激光干涉计量在运动、停稳与图像采集全过程持续进行，不作为额外串行节拍步骤。
- 🟢 IPD为全局计算：25 Die抽检用于确定Wafer级低阶变形，单Die内部测量用于确定高阶局部变形。

当前流程：
Wafer上片 → ESC吸附 → 找正/建系 → Wafer级调平 → 25 Die依次寻址 → Focus Ready → Z狭缝AF对焦（同时XY继续残余settling） → Measurement Ready → 图像采集 → 下一Die → 25点完成 → 全局IPD解算 → 输出Wafer级低阶与Die内高阶结果。

---

## 3. 25 Die抽检几何

- 🟢 采样点总数：25。
- 🟢 中心点：1个。
- 🟢 8个方位角，每隔45°。
- 🟢 每个方位角3个径向采样点：
  - r1 = 50 mm
  - r2 = 100 mm
  - r3 = 140 mm
- 🟢 总计：1 + 8×3 = 25点。

---

## 4. 扫描路径规划

### 4.1 已定原则

🟢 **采用外围起始的非规则Z字蛇形扫描。**

路径不是沿半径方向由外向内扫描，也不是规则矩形网格的直线Z字；而是根据25个离散采样点在晶圆平面上的空间位置，保持整体由一侧向另一侧、再向下一扫描带切换并反向扫描的蛇形拓扑。

### 4.2 优化目标优先级

路径规划优先级确定为：

1. **保持Z字蛇形拓扑与空间连续访问；**
2. **抑制跨片大跨度跳跃；**
3. **降低总运动距离；**
4. **最终以运动时间与停稳时间之和作为真实优化目标，而非几何最短路。**

即：

```text
Z字拓扑优先 > 抑制大跳 > 总路径最短
```

### 4.3 热漂移考虑

扫描路径需同时兼顾热漂移：

- 采样时间应随晶圆空间位置连续展开；
- 避免长时间只测量晶圆单一区域；
- 避免过大的跨片跳跃引入额外运动和停稳时间；
- 每个采样点至少记录 (x, y, t)，后续如条件允许增加温度T，用于区分空间低阶IPD与随时间变化的热漂移。

### 4.4 当前工程表述

25个抽检点采用外围起始的非规则蛇形扫描策略。在保持空间连续访问和热漂移可辨识性的基础上，对跨片大跨度运动进行约束。路径规划不以几何最短路为唯一目标，而以各段运动时间与停稳时间之和最小为最终优化目标。

---

## 5. Settling与自动对焦

### 5.1 Focus Ready

🟡 XY大行程运动结束后，当平台残余位置、速度及振动进入狭缝AF的有效检测/捕获条件时，允许启动Z向自动对焦；此时不要求工作点达到最终IPD量测稳定状态。

Focus Ready最终由狭缝AF有效检测范围、信号线性区、XY残余速度/振动及Z执行机构闭环条件共同确定，具体数值待方案参数、供应商规格或样机测试确认。

### 5.2 Measurement Ready

🟡 图像采集仅在自动对焦完成，且工作点干涉计量确认Wafer相对于光学测量基准的稳定性满足IPD量测要求后启动。

### 5.3 时间重叠

当前采用：

```text
XY Move
→ Focus Ready
→ [Z Autofocus || XY residual settling / fine-stage compensation]
→ Measurement Ready
→ Acquisition
```

即Z自动对焦可与XY最终残余settling部分重叠，而不是等待XY完全达到最终量测稳定状态后才开始对焦。

### 5.4 待验证

🔵 Patterned wafer可能使狭缝AF受到图形、膜层、反射率及局部台阶影响，后续需验证pattern-dependent focus bias、有效线性范围、捕获范围、Z闭环响应时间、重复性及标定策略。

---

## 6. 光学FOV与Die内扫描

### 6.1 有效量测FOV

🟡 **第一版整机节拍按 200 µm × 200 µm 的高精度有效IPD量测FOV进行设计。**

该数值为当前设计基线/目标值，不作为已验证性能。193 nm光学系统本身应保留更大的光学可用视场，最终高精度有效FOV需通过像差、畸变、场依赖误差、标定残差和IPD算法共同验证。

🔴 30 µm级FOV不作为当前整机节拍基线。

### 6.2 Die内测量方式

🟢 10 mm × 10 mm Die内部当前采用**高密度Step-and-Measure**，不采用连续扫描成像作为第一版方案。

原因：连续扫描对恒速误差、速度纹波、动态姿态、工作点动态误差、相机触发同步及干涉仪时间同步要求更高；第一版优先保证1 nm级IPD方案的可实现性和误差链可验证性。

🟢 Wafer级已经采用25 Die稀疏抽检；Die内暂不进一步大幅稀疏，以保证高阶局部IPD变形的可辨识性。Die内自适应降采样仅作为后续节拍优化方向。

### 6.3 视场数量

200 µm FOV、10 mm × 10 mm Die：

- 无overlap时约 50 × 50 = 2500 FOV/Die；
- 若采用约10% overlap、步距约180 µm，则约 56 × 56 = 3136 FOV/Die。

因此整机节拍的主导项预计由Die内大量micro-step的move/settle/acquisition决定，而不是25个Die之间的大步距寻址。

---

## 7. Die内micro-step与settling基线

### 7.1 主矛盾

🟢 对180–200 µm Die内小步距，纯运动时间预计不是主导项，**Measurement Ready settling是关键节拍KPI**。

当前目标是缩短：

```text
T_micro-step = T_move + T_controlled-settle
```

而不是单纯追求最大速度或最大加速度。

### 7.2 第一版时间目标

🟡 200 µm级micro-step的第一版设计目标：

- 纯move：约 10–20 ms 量级；
- controlled settling：约 20–30 ms 量级；
- **move-to-Measurement-Ready：约 40–50 ms/FOV**。

当前节拍baseline：

```text
50 ms / FOV
```

同时保留敏感性分析：

- 20 ms/FOV：挑战目标；
- 50 ms/FOV：第一版工程设计基线；
- 100 ms/FOV：保守档。

⚠️ 上述数值均为设计目标/节拍假设，并非已验证实测能力。

### 7.3 Measurement Ready判据

最终settling不能只以电机编码器/光栅位置误差作为判据，而应由工作点干涉计量确认Wafer相对于Lens/光学测量基准的相对稳定性。

Measurement Ready后续需明确：

- 工作点允许RMS/3σ窗口；
- 统计带宽；
- hold time；
- X/Y/Z及姿态方向要求；
- 稳定性如何映射到最终IPD误差预算。

### 7.4 Settling优化优先级

🟡 当前优化路径：

1. 轨迹整形 / S-curve / input shaping，减少对结构模态的激励；
2. 结构模态识别，获得ESC+wafer+精动台+计量框的FRF、主模态和阻尼；
3. notch / state damping等共振抑制；
4. 加速度/力前馈，减少反馈控制收尾时间；
5. 降低动件质量和重心、提高连接刚度和第一阶模态；
6. 控制jerk，避免以过大的结构激励换取很小的move时间收益；
7. 由工作点计量定义Measurement Ready，而不是要求所有内部环路误差都同时趋近于零。

核心优化目标：

```text
min [ T_move + T_MeasurementReady ]
```

而不是单独最小化T_move。

---

## 8. 节拍模型

### 8.1 Die间寻址

单个抽检Die的大步距寻址阶段：

```text
T_die-entry ≈ T_move + T_focus-ready + max(T_focus, T_residual-settle-after-focus-ready)
```

### 8.2 Die内高密度Step-and-Measure

Die内节拍当前按：

```text
T_Die ≈ N_FOV × (T_micro-move + T_micro-settle + T_acq) + N_AF × T_AF-extra
```

其中：

- N_FOV ≈ 2500（无overlap）或约3136（10% overlap）；
- AF不默认每个FOV执行一次完整重新对焦；
- 后续优先考虑局部焦面模型 + Z前馈 + 周期性focus check，以避免AF成为新的节拍瓶颈。

### 8.3 整片Wafer

```text
T_wafer =
T_load
+ T_align
+ T_level
+ Σ[T_die-entry + T_Die]
+ T_global_IPD
+ T_unload
```

其中工作点干涉计量为持续并行计量，不单独增加节拍项。

---

## 9. 当前高优先级待确认项

### P0

- 🔵 1 nm IPD的正式误差预算与Measurement Ready稳定窗口；
- 🔵 193 nm光学系统最终可实现的高精度有效FOV；
- 🔵 200 µm micro-step后50 ms move-to-ready目标的工程可实现性；
- 🔵 单FOV曝光、相机读出和数据传输时间；
- 🔵 Die内AF频率与局部焦面建模策略。

### P1

- 🔵 精动平台行程、带宽、负载和主模态；
- 🔵 input shaping / notch / feedforward参数；
- 🔵 计量框、力框、花岗岩和隔振系统对micro-settle的传递函数；
- 🔵 patterned wafer对Sony类狭缝AF的系统偏差。

---

## 10. Baseline Change Log

### v0.4 — 2026-09-14
- 复核并确认当前整机与机台子系统两条主线保持不变。
- 维持Sony类狭缝AF、Focus Ready / Measurement Ready两级settling、工作点干涉仪持续计量等当前口径。
- 维持25 Die抽检几何：中心点 + 8方位 × r=50/100/140 mm。
- 维持外围起始的非规则Z字蛇形扫描，并继续以抑制跨片大跳和最小化move+settle为路径优化目标。
- 维持193 nm成像方案下200 µm × 200 µm高精度有效FOV为第一版节拍设计基线；30 µm级FOV不作为当前基线。
- 维持10 mm × 10 mm Die内高密度Step-and-Measure方案，确认Die内micro-step而非Die间大步距是当前节拍主矛盾。
- 维持200 µm级micro-step的move-to-Measurement-Ready按50 ms/FOV做第一版节拍设计，20 ms挑战、100 ms保守。
- 未将当前尚未完成公开资料/样机验证的FOV、settling、AF动态指标写成已验证能力。

### v0.3 — 2026-09-13
- 将高精度有效IPD量测FOV第一版设计基线设为200 µm × 200 µm。
- 明确Die内采用高密度Step-and-Measure，不采用连续扫描作为第一版方案。
- 明确Wafer级25 Die已完成稀疏抽检，Die内暂不进一步大幅稀疏。
- 将Die内180–200 µm micro-step后的Measurement Ready settling识别为关键节拍KPI。
- 第一版move-to-ready按50 ms/FOV做节拍设计；20 ms为挑战目标，100 ms为保守档。
- Settling优化优先级更新为轨迹整形、模态识别、共振抑制、前馈、结构优化、jerk约束和工作点判据。
- 节拍模型增加Die内高密度FOV扫描项。

### v0.2 — 2026-09-11
- 自动对焦由暂定共聚焦修改为Sony类狭缝式自动对焦。
- 保留并细化Focus Ready / Measurement Ready两级settling策略。
- 明确Z自动对焦可与XY residual settling部分时间重叠。
- 节拍模型更新为考虑两级settling与对焦重叠的模型。
- 新增patterned wafer对狭缝AF影响的待验证项。

### v0.1 — 2026-09-11
- 建立25 Die抽检几何、非规则Z字蛇形扫描与基础节拍模型。
