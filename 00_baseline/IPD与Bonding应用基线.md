# IPD量测与Fusion Bonding应用基线

> 状态：当前有效讨论口径
> 更新日期：2026-09-16
> 适用范围：1 nm IPD量测设备的应用定义、测量对象、Bonding Overlay关联与下一次Bonding前馈

## 1. 项目应用定位

本项目不再仅定义为“背面光刻前的IPD/CPE量测设备”。当前更完整的应用闭环为：

```text
Pre-bond同面位置场量测
        ↓
Fusion Bonding
        ↓
Post-bond同面位置场复测
        ↓
同一组计量特征坐标差分
        ↓
IPD Map / IPD fingerprint
        ├──→ 关联并推测 Bonding Overlay / Bonding distortion
        ├──→ 评价当前 Bonding 几何质量与稳定性
        ├──→ 结合独立真值推测界面质量风险
        ├──→ 更新 Bonding 工艺模型
        ├──→ 为下一次 Bonding 的 wafer 配对、预对准、压力/间隙/键合波等参数提供前馈
        └──→ 后续 Backside Lithography / CPE（适用时）
```

因此，IPD应被定义为Fusion Bonding过程的一个**空间响应量**，而不是仅作为光刻补偿参数。

## 2. 当前主应用场景

### 2.1 顶层晶圆同一可访问表面的Pre/Post差分

当前主路线为：在Fusion Bonding前后，量测顶层晶圆同一物理表面上的同一组可追踪计量特征。两次量测均采用一致的特征定义、坐标方向和定位算法，不再采用“键合前测正面、键合后测背面”，也不引入front-to-back transfer calibration。

```text
顶层晶圆同一可访问表面
        ↓
Pre-bond位置场测量
        ↓
Fusion Bonding
        ↓
Post-bond复测同一表面、同一组计量特征
        ↓
统一晶圆坐标系下差分获得IPD
```

计量特征可包括专用十字、box、grating、周期性阵列、dummy结构或其他具有稳定几何中心的标记。原始表面无可定位图形时，需要在工艺设计阶段增加专用metrology mark；仅对无图形硅面成像，不能形成1 nm级可追溯二维位置坐标。

## 3. 同面差分的关键边界

设同一计量表面为\(S\)，第\(i\)个计量特征经统一坐标转换后的Pre/Post位置分别为\(\mathbf r_{i,S}^{pre}\)和\(\mathbf r_{i,S}^{post}\)，则：

\[
\boxed{
\mathbf{IPD}_{i,S}
=
\mathbf r_{i,S}^{post}
-
\mathbf r_{i,S}^{pre}
}
\]

当前定义同时要求：

1. 两次量测针对同一物理表面，不是两个表面之间的坐标转移；
2. 两次量测针对同一组具有唯一身份的计量特征；
3. 两次量测之间的工艺不能移除、覆盖或重构该表面及计量特征；
4. 两次量测统一晶圆中心、notch方向、坐标尺度及允许扣除项。

主流程建议将Post-bond同面量测布置在会破坏计量表面和标记的减薄、刻蚀或再成膜之前。若在减薄后量测新显露结构，该结果属于后续工艺状态位置场，不再纳入本基线的严格同面差分，需另建工艺贡献和坐标传递模型。

坐标配准只消除两次上片造成的整体位姿差异，不能使用无约束高阶拟合把真实Bonding畸变一并扣除。应同时保留原始位置场、刚性配准后位置场、低阶模型和高阶残差。

## 4. 当前IPD的工艺定义

当前主IPD表示Fusion Bonding前后同一表面的位置变化：

\[
\mathbf D_{meas}
=
\mathbf D_{bond}
+
\Delta\mathbf E_{chuck}
+
\Delta\mathbf E_{temp}
+
\Delta\mathbf E_{metrology}.
\]

其中，\(\mathbf D_{bond}\)为Bonding引起的真实面内位置变化；其余项分别表示两次夹持状态差异、温度状态差异和量测链差异。项目目标是通过一致的夹持、温控、工作点计量、设备标定和重复性试验约束这些附加项，并给出差分结果的不确定度。

该定义优先服务Bonding几何质量评价。若需要进一步推测空洞、局部黏附不足或结合强度等界面质量，必须引入SAM、红外、强度或电学结果作为独立真值进行标定；IPD仅作为关联特征，不能单独给出唯一结论。

若Pre/Post之间除Bonding外还包含退火或其他不会破坏计量表面的步骤，测得结果是这些步骤共同形成的工艺状态IPD。需要研究纯Bonding贡献时，应通过短流程对照试验或模型分离附加工艺影响。

## 5. Top-wafer IPD与Bonding Overlay的物理关系

### 5.1 基本关系

Bonding Overlay描述上下两片晶圆之间的相对位置误差；Top IPD描述顶层晶圆自身grid在工艺前后的位移。二者有关，但不是同一个量。

定义顶层和底层晶圆的面内位移分别为：

\[
\mathbf u_t(x,y),\qquad \mathbf u_b(x,y).
\]

则Bonding Overlay可概念性写为：

\[
\boxed{
\mathbf O(x,y)
=
\mathbf O_0(x,y)
+
\mathbf u_t(x,y)
-
\mathbf u_b(x,y)
}
\]

其中\(\mathbf O_0\)表示Bonding前的初始对准误差。

因此：

\[
\boxed{
O \neq IPD_{top}
}
\]

更完整地：

\[
\boxed{
O
=
IPD_{top}
-
IPD_{bottom}
+
O_{align}
}
\]

Top IPD可以作为Bonding Overlay的重要观测量，但不能直接等同于Bonding Overlay。

### 5.2 对称双晶圆的简化理解

若上下两片晶圆材料、厚度、结构和边界条件近似对称，局部错配量\(\mathbf m\)会由两片晶圆按等效面内刚度分担。

简化表示：

\[
\mathbf u_t=\alpha\mathbf m,
\]

\[
\mathbf u_b=-(1-\alpha)\mathbf m,
\]

\[
\alpha\approx\frac{K_b}{K_t+K_b}.
\]

当\(K_t\approx K_b\)时，可近似理解为上下晶圆共同分担错配。

但“Bonding Overlay = 2 × Top IPD”只在非常理想的对称、小变形条件下才可能近似成立，不能作为当前项目的默认公式。

## 6. Bonding变形如何形成Top IPD

当前物理链条定义为：

```text
Incoming wafer shape / bow / saddle / nanotopography
        +
Bonding gap / initial alignment / chuck flatness
        +
Bond initiation force / pressure / release strategy
        +
Bond-wave velocity与传播非均匀性
        +
Temperature / surface activation / interface condition
        ↓
界面局部接触与牵引 / 应力重分布
        ↓
上下晶圆弹性协调变形
        ↓
Top wafer in-plane strain/displacement field
        ↓
Post-bond Top IPD fingerprint
```

因此Top IPD不是随机结果，而是Bonding力学过程的空间响应。

## 7. 用Top IPD推测Bonding状态与Overlay的方法

### 7.1 前向模型

把Bonding状态参数写为：

\[
\boldsymbol\theta=
[g,F,v_b,P(x,y),Shape_t,Shape_b,Chuck,T,Surface,\ldots].
\]

建立：

\[
\mathbf D_{top}=\mathcal F(\boldsymbol\theta).
\]

其中可采用有限元、薄板模型、流固耦合或数据驱动代理模型。

### 7.2 Overlay预测

在有历史Bonding Overlay标定数据后，建立：

\[
\boxed{
\hat{\mathbf O}
=G(IPD_{top},Shape_t,Shape_b,Recipe,Alignment)
}
\]

输出应定义为“Bonding Overlay预测/关联结果”，而不是把Top IPD直接称为Bonding Overlay。

### 7.3 反问题 / Bonding fingerprint识别

测得\(\mathbf D_{top}^{meas}\)后，可通过：

\[
\hat{\boldsymbol\theta}
=
\arg\min_{\boldsymbol\theta}
\left\|
\mathcal F(\boldsymbol\theta)-\mathbf D_{top}^{meas}
\right\|^2
+
\lambda R(\boldsymbol\theta)
\]

识别最可能的Bonding状态。

工程上第一阶段不建议直接反演全部物理参数，而应先建立IPD fingerprint与工艺异常的统计/物理关联，例如：

| IPD空间特征 | 优先调查的Bonding因素 |
|---|---|
| 全片近似isotropic scaling | 热状态、整体应力、chuck bow |
| 中心径向扩张/收缩 | bond initiation / center force / pressure |
| 环状畸变 | bonding-wave速度突变、传播停顿或局部状态变化 |
| 单边高阶畸变 | incoming shape不对称、gap不均、chuck不对称 |
| 四叶/鞍形 | saddle shape、chuck deformation、边界约束 |
| 局部热点 | particle、局部接触异常、表面缺陷 |

以上为需要通过试验和模型验证的诊断假设，不作为单一因果判据。

## 8. 下一次Bonding前馈闭环

当前设备的高层价值闭环定义为：

\[
\boxed{
Measure\rightarrow Understand\rightarrow Predict\rightarrow Control
}
\]

具体为：

```text
第n片/批：Pre-bond shape + Pre-bond grid
        ↓
Bonding recipe_n
        ↓
Post-bond IPD_n + 实际Bonding Overlay_n
        ↓
更新 θ → IPD → Overlay 模型
        ↓
第n+1片：Pre-bond shape/grid
        ↓
预测风险与畸变
        ↓
Recipe_(n+1) / wafer pairing / alignment / pressure / gap / timing前馈
```

因此，本设备后续可提供三层输出：

1. **Measure**：高精度IPD Map；
2. **Diagnose/Predict**：Bonding fingerprint、Bonding Overlay关联/预测；
3. **Control input**：为下一次Bonding提供前馈参数和工艺窗口依据。

Backside Lithography/CPE保留为另一个下游出口，但不再是唯一应用终点。

## 9. 当前项目书建议表述

推荐在项目背景中使用：

> 本项目面向Fusion Bonding过程中晶圆面内位置变化的高精度量测。通过建立同片晶圆工艺前后的高密度位置场，获得IPD fingerprint，并结合上下晶圆初始形貌、对准状态及Bonding recipe，建立IPD与Bonding Overlay及键合工艺状态之间的关联模型。一方面用于评价当前Bonding质量、识别高阶和局部畸变，另一方面为后续晶圆配对、预对准和键合参数优化提供前馈信息；在存在背面光刻的工艺中，IPD结果还可进一步转换为CPE输入。

避免使用以下过强表述：

- “Top IPD就是Bonding Overlay”；
- “测一片Top wafer即可唯一反演所有Bonding参数”；
- “Bonding Overlay = 2 × Top IPD”；
- “Bonding+Thinning后测得的差分就是纯Bonding IPD”。

## 10. 公开资料基线

以下资料用于支撑当前理论链条，具体工况、数值和适用边界需在正式项目书中逐条核对：

1. **Low Distortion Fusion Bonding using Pneumatically Warped Wafers**, 2026. 研究Bonding方式、wafer shape、bond-front与post-bond grid distortion/CPE之间关系。  
   https://arxiv.org/abs/2606.04625

2. **Investigation of direct wafer bonding dynamics and in-plane distortion**, 2026. 建立direct bonding dynamics与IPD之间的流固耦合/力学联系。  
   https://www.sciencedirect.com/science/article/pii/S0026271426002684

3. **Investigation of Distortion in Wafer-to-wafer Bonding with Highly Bowed Wafers**, imec等。关注top/bottom wafer grid及最终overlay residual之间关系。  
   https://imec-publications.be/entities/publication/e345bb71-a947-4336-95e7-117630277baf/full

4. **ECTC 2025相关imec工作**：将incoming wafer shape、bonding recipe、bonding gap与nonlinear bonding-overlay residual联系。  
   https://imec-publications.be/entities/publication/082235d5-cb65-46a7-8e29-f20af1c129b1

5. **Yu & Suo, A model of wafer bonding by elastic accommodation**, Journal of the Mechanics and Physics of Solids, 1998. 经典晶圆键合弹性协调模型。  
   https://www.sciencedirect.com/science/article/pii/S0022509697001002

6. **Tokyo Electron, WO2025019059A1, Integrated metrology for process controls in wafer bonding system**. 将pre/post bonding metrology、wafer shape、IPD、stress/force等用于Bonding模型和下一片recipe控制。  
   https://patents.google.com/patent/WO2025019059A1/en

## 11. 后续待验证问题

1. Top IPD对Bottom IPD及Bonding Overlay的可辨识程度；
2. 是否增加Bottom wafer测量通道/流程以降低模型欠定性；
3. 同面metrology mark的结构设计、可见性和长期几何稳定性；
4. 计量标记在Bonding前后是否保持同一身份，且不被覆盖、移除或重构；
5. Bonding、夹持差异、温度差异及其他保留工艺步骤对IPD贡献的实验分离方案；
6. Incoming wafer shape是否应作为设备必测输入或外部接口输入；
7. Bonding Overlay真值如何获得并作为模型训练/验证基准；
8. IPD fingerprint到Bonding recipe前馈的参数接口与验收方式。
