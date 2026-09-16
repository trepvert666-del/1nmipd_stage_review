# IPD量测与Fusion Bonding应用基线

> 状态：当前有效讨论口径
> 更新日期：2026-09-16
> 适用范围：1 nm IPD量测设备的应用定义、测量对象、Bonding Overlay关联与下一次Bonding前馈

## 1. 项目应用定位

本项目不再仅定义为“背面光刻前的IPD/CPE量测设备”。当前更完整的应用闭环为：

```text
Pre-bond metrology
        ↓
Fusion Bonding
        ↓
Post-bond / post-thinning metrology
        ↓
IPD Map / IPD fingerprint
        ├──→ 关联并推测 Bonding Overlay / Bonding distortion
        ├──→ 评价当前 Bonding 过程质量与稳定性
        ├──→ 更新 Bonding 工艺模型
        ├──→ 为下一次 Bonding 的 wafer 配对、预对准、压力/间隙/键合波等参数提供前馈
        └──→ 后续 Backside Lithography / CPE（适用时）
```

因此，IPD应被定义为Fusion Bonding过程的一个**空间响应量**，而不是仅作为光刻补偿参数。

## 2. 当前主应用场景

### 2.1 Via-first / Via-middle及可显露计量结构

当前优先考虑的工艺场景为：

```text
顶层晶圆完成器件 / via-first TSV / 专用计量结构
        ↓
Pre-bond位置场测量
        ↓
Fusion Bonding
        ↓
顶层晶圆背面减薄
        ↓
TSV / dummy via / metrology via / reveal mark显露
        ↓
Post-bond背面位置场测量
        ↓
差分获得IPD
```

设备第一阶段以**表面光学计量**为主，不以through-Si IR作为主技术路线。

适用结构不限定为功能TSV，可包括：

- functional TSV；
- dummy TSV；
- metrology via；
- 周期性via array；
- 专用十字、box、grating或其他reveal mark；
- 其他经减薄后可在背面直接观察、并可与键合前建立坐标关系的结构。

## 3. Pre/Post测量面的关键边界

第二次测量位于Bonding + thinning/reveal之后的顶层晶圆背面。

从严格物理定义看，若希望得到真正的backside IPD，第一次测量也应对应最终背面材料坐标：

\[
IPD_{BS}=P^{post}_{BS}-P^{pre}_{BS}.
\]

但在via-first等工艺中，Pre-bond时最终背面特征仍埋在厚Si内部，纯表面光学无法直接观测。因此当前必须显式区分“测量面一致”和“可实现性”。

### 3.1 不直接采用“正面TSV端 → 背面TSV端”无条件做差

若第一次测TSV正面端、第二次测reveal后的TSV背面端，则：

\[
\Delta P_{meas}
=IPD_{BS}+\Delta P_{front-back}^{TSV}+E_{reveal}+E_{metrology}.
\]

其中，\(\Delta P_{front-back}^{TSV}\)包含TSV轴线倾斜、DRIE垂直度、锥度等造成的两端固有XY差异，因此不能在1 nm目标下无条件忽略。

例如TSV有效深度50 µm、轴线倾斜100 µrad时，两端横向偏移已约为5 nm。

### 3.2 当前推荐路线

对于纯表面光学设备，当前更合理的工程路线为：

\[
\hat P^{pre}_{BS}=P^{pre}_{FS}+C_{FB},
\]

其中：

- \(P^{pre}_{FS}\)：键合前可从表面测得的位置；
- \(C_{FB}\)：front-to-back transfer calibration，由专用结构、test wafer和工艺标定获得；
- \(\hat P^{pre}_{BS}\)：对键合前最终backside reference position的估计。

最终：

\[
IPD_{BS}=P^{post}_{BS}-\hat P^{pre}_{BS}.
\]

专用metrology via / reveal mark应优先于“单根功能TSV圆心”作为1 nm级计量基准。

## 4. 当前IPD的工艺定义

第二次测量发生在Bonding + thinning/reveal之后，因此实际测量结果不仅包含纯Bonding变形，还可能包含减薄和reveal造成的附加位置变化：

\[
D_{meas}=D_{bond}+D_{thin}+D_{reveal}.
\]

因此：

- 若目标是研究纯Bonding机制，需要通过独立试验/模型分离\(D_{thin}\)和\(D_{reveal}\)；
- 若目标是评价进入下一工序前的实际晶圆状态，则\(D_{meas}\)本身就是有价值的过程IPD；
- 若用于后续背面光刻/CPE，则应使用工艺后实际状态，而不是强行删除真实存在的thinning/reveal影响。

当前项目书中优先使用“工艺状态IPD / process IPD”这一更严谨概念，避免把Bonding+Thinning后的差分结果全部称为“纯Bonding IPD”。

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
3. Front-to-back transfer calibration \(C_{FB}\)的结构设计和长期稳定性；
4. 功能TSV与专用metrology via在1 nm级定位稳定性上的差异；
5. Bonding、thinning、reveal三部分IPD贡献的实验分离方案；
6. Incoming wafer shape是否应作为设备必测输入或外部接口输入；
7. Bonding Overlay真值如何获得并作为模型训练/验证基准；
8. IPD fingerprint到Bonding recipe前馈的参数接口与验收方式。
