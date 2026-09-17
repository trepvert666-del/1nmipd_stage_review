# IPD量测与Fusion Bonding应用基线

> 状态：当前有效讨论口径
> 更新日期：2026-09-17
> 适用范围：1 nm IPD量测设备的应用定义、测量对象、Bonding Overlay关联与下一次Bonding前馈

## 1. 项目应用定位

本项目不再仅定义为“背面光刻前的IPD/CPE量测设备”。项目名称中的“1 nm”统一指设备对有效图案或计量标记X、Y位置的量测能力，以及由该位置相对规定参考形成IPD的能力；不指后续光刻CPE残差、曝光后Overlay或Bonding Overlay达到1 nm。

当前更完整的应用闭环为：

```text
最终工艺状态位置场量测
        +
设计 / 理想 / Golden wafer / 批次参考网格
        ↓
最终状态 IPD Map / IPD fingerprint
        ├──→ 评价最终几何质量与批次稳定性
        ├──→ 关联并推测 Bonding Overlay / Bonding distortion
        ├──→ 为后续 Backside Lithography / CPE提供输入
        ├──→ 结合独立真值推测界面质量风险
        └──→ 更新 Bonding 工艺模型及下一片/下一批Recipe
       
可选增强：Pre/Post对应位置场差分
        └──→ 分离Bonding或指定工艺区间新增的IPD
```

因此，IPD应被定义为Fusion Bonding过程的一个**空间响应量**，而不是仅作为光刻补偿参数。

## 2. 当前测量模式

### 2.1 最终状态单次量测：生产主模式

当前主模式不要求必须进行Pre/Post差分。晶圆完成Bonding及规定的后续工艺后，在需要评价或曝光的最终状态下量测可见计量特征，并与设计网格、理想网格、Golden wafer或经确认的批次参考网格比较，得到最终状态IPD。

该模式用于：

- 评价最终晶圆位置场、低阶/高阶畸变和局部热点；
- 形成Bonding质量风险及工艺稳定性特征；
- 为后续Backside Lithography / CPE提供尽可能接近曝光状态的输入；
- 与历史Recipe、过程Trace及独立质量真值关联，更新Bonding模型。

最终状态量测不要求键合前已经测过同一片晶圆，也不要求两次测量面相同，因此不需要建立正反面坐标转移关系。

### 2.2 Pre/Post差分：可选诊断模式

若需要回答“Bonding或指定工艺区间新增了多少变形”，可增加Pre-bond位置场量测，并在Post-bond对应状态复测同一组可追踪特征。差分模式用于机理研究、DOE和Recipe优化，不作为生产模式获得IPD的必要条件。

## 3. 最终状态IPD与参考网格

设第\(i\)个计量特征的最终晶圆坐标为\(\mathbf r_i^{final}\)，参考位置为\(\mathbf r_i^{ref}\)，则：

\[
\boxed{
\mathbf{IPD}_i^{final}
=
\mathbf r_i^{final}
-
\mathbf r_i^{ref}
}
\]

参考网格可以来自版图设计坐标、规定的理想晶圆网格、Golden wafer或经统计确认的批次基准。不同参考定义对应不同物理含义，必须随结果记录：

- 以设计/理想网格为参考时，结果包含初始制造偏差和全部前序工艺累积变形；
- 以Golden wafer或批次模型为参考时，结果表示相对于过程基准的偏离；
- 用于CPE时，应采用与曝光坐标系统一、且尽可能接近曝光工艺状态的最终位置场。

坐标建系可扣除规定的晶圆中心、notch方向、整体平移和旋转，但不能使用无约束高阶拟合把真实工艺畸变一并吸收。应保留原始位置场、建系后位置场、低阶模型和高阶残差。

## 4. 可选差分IPD及工艺解释边界

若执行Pre/Post对应特征量测，则：

\[
\boxed{
\Delta\mathbf{IPD}_i
=
\mathbf r_i^{post}
-
\mathbf r_i^{pre}
}
\]

差分结果更接近指定工艺区间新增的位置变化，但仍包含两次夹持、温度、建系和量测链差异：

\[
\Delta\mathbf D_{meas}
=
\Delta\mathbf D_{process}
+
\Delta\mathbf E_{chuck}
+
\Delta\mathbf E_{temp}
+
\Delta\mathbf E_{metrology}.
\]

两次独立量测且单次标准差相同时，差分随机误差近似满足\(\sigma_{\Delta d}\approx\sqrt{2}\sigma_m\)。因此，差分有利于分离工艺增量，但量测链和不确定度也更长。

只测最终状态同样可以建立IPD fingerprint并评价几何质量，但不能把最终IPD全部归因于Bonding。若要由最终IPD推测Bonding状态，需要同时引入来片形貌、Recipe、过程Trace和历史标定数据。对空洞、局部黏附不足或结合强度等界面质量，还必须用SAM、红外、强度或电学结果作为独立真值；IPD只能作为关联特征。

## 5. Top-wafer IPD与Bonding Overlay的物理关系

### 5.1 基本关系

Bonding Overlay描述上下两片晶圆之间的相对位置误差；Top IPD描述顶层晶圆最终grid相对设计/参考网格的偏离，或在可选差分模式下描述规定工艺区间的增量位移。二者有关，但不是同一个量。

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
第n片/批：最终状态 IPD_n
        +
Bonding recipe_n / 过程Trace / 独立质量真值
        +
可选：Pre-bond shape/grid及Pre/Post差分
        ↓
更新 θ → IPD → Quality / Overlay 模型
        ↓
第n+1片：来片信息与目标工艺窗口
        ↓
预测风险与畸变
        ↓
Recipe_(n+1) / wafer pairing / alignment / pressure / gap / timing前馈
```

因此，本设备后续可提供三层输出：

1. **Measure**：高精度IPD Map；
2. **Diagnose/Predict**：Bonding fingerprint、Bonding Overlay关联/预测；
3. **Control input**：为下一次Bonding提供前馈参数和工艺窗口依据。

Backside Lithography/CPE保留为另一个下游出口，但不再是唯一应用终点。上述Bonding质量识别率、Bonding Overlay预测误差、CPE拟合残差和曝光后Overlay均作为应用效果单独验证，不继承本机图案位置量测的1 nm指标。

## 9. 当前项目书建议表述

推荐在项目背景中使用：

> 本项目面向Fusion Bonding及其后续工艺形成的晶圆面内位置变化开展1 nm级图案位置量测。设备以最终状态单次位置场量测为生产主模式，将图像局部定位与曝光工作点坐标融合为统一晶圆坐标，并通过最终实测坐标相对设计或参考网格的偏差获得IPD fingerprint，用于评价几何质量、关联Bonding Overlay并形成后续光刻CPE输入；在研发和异常分析阶段，可增加Pre/Post对应位置场差分，以分离Bonding或指定工艺区间新增的变形。结合来片形貌、Bonding recipe、过程Trace及独立质量真值，可进一步建立IPD与Bonding状态之间的关联模型，并为后续Recipe优化提供反馈信息。这里的1 nm只约束图案位置/IPD量测能力，不构成CPE、曝光后Overlay或Bonding Overlay的1 nm承诺。

避免使用以下过强表述：

- “Top IPD就是Bonding Overlay”；
- “测一片Top wafer即可唯一反演所有Bonding参数”；
- “Bonding Overlay = 2 × Top IPD”；
- “最终状态IPD全部由Bonding产生”；
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
3. 最终状态参考网格的来源、定义、坐标追溯和不确定度；
4. 最终状态计量标记的可见性、设计坐标和长期几何稳定性；
5. 差分模式下Bonding、夹持差异、温度差异及其他工艺步骤贡献的实验分离方案；
6. Incoming wafer shape是否应作为设备必测输入或外部接口输入；
7. Bonding Overlay真值如何获得并作为模型训练/验证基准；
8. IPD fingerprint到Bonding recipe前馈的参数接口与验收方式。
