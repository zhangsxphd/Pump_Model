# 8路蠕动泵一体机（9.5 cm 极限板宽 / 左右反向出管方案）CAD 设计与尺寸规范

## 一、方案核心要求变更与设计说明

根据最新确认要求：
1. **安装方向严格相反（左右背向出管）**：
   - **左侧 4 个泵**：喷嘴与出管方向朝向**左侧 / 前侧外部**（$\leftarrow$）。
   - **右侧 4 个泵**：喷嘴与出管方向朝向**右侧 / 后侧外部**（$\rightarrow$）。
   - **正面排布结构**：形成 `前侧出泵方向 ←【4 个泵】｜中间区域 (11.5mm)｜【4 个泵】→ 后侧出泵方向`。
   - **杜绝同向干涉**：软管分别从左右两侧边沿引出，彻底解决管路交叉打结和空间拥挤问题。
2. **面板极限宽度 9.5 厘米（95.0 mm）**：
   - 面板宽度严格定为 **95.0 mm（9.5 cm）**。
   - 8 台泵采用坚向 4+4 双列布置，两列中心距 49.0 mm，两列泵体间留有 11.5 mm 独立中央物理走线/隔断通道。
3. **整机极限尺寸严格 $\le 25 \times 25\text{ cm}$**：
   - 面板外形：$95.0\text{ mm} \times 240.0\text{ mm}$。
   - 整机全包络尺寸：$95.0\text{ mm (宽)} \times 240.0\text{ mm (高)} \times 101.5\text{ mm (深)}$，即使加上左右两侧外伸出水嘴（总跨距 136.2 mm），全轴向均严格控制在 25 cm 以内！

---

## 二、CAD 标准工程草图（三视图与尺寸标注）

![8路蠕动泵一体机 9.5cm板宽左右反向工程草图](/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/cad_blueprint_95mm_opposite.png)

---

## 三、三维轴测实体渲染效果（Shapr3D 原生模型）

![Shapr3D 三维实体装配渲染 (9.5cm左右反向出管)](/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/opposite_pumps_95mm_3d_preview.png)

---

## 四、外形包络尺寸达标判定表（9.5cm板宽 & ≤ 25×25 cm 验证）

| 检验项目 / 部件 | 设计实测尺寸 (mm) | 对应厘米 (cm) | 约束指标判定 | 结构裕量与工程配合说明 |
| :--- | :--- | :--- | :---: | :--- |
| **前面板宽度 (Panel W)** | **95.0 mm** | **9.50 cm** | <font color="#10B981">**✓ 严格达标**</font> | 完全吻合指定的 9.5 cm 板宽指标 |
| **整机外形总高 (Height)** | **240.0 mm** | **24.00 cm** | <font color="#10B981">**✓ 合格 (≤ 25 cm)**</font> | 坚向 4 泵紧凑列距 58.0 mm，距 25 cm 仍有 10 mm 裕量 |
| **整机底座深度 (Depth)** | **72.0 mm** *(含泵头101.5)* | **7.20 cm** *(10.15)* | <font color="#10B981">**✓ 合格 (≤ 25 cm)**</font> | 电机深 52.5 mm + 后腔预留 12.5 mm 接线电控裕量 |
| **左侧 4 泵出水方向** | **朝向左侧/前侧外部** | **←** | <font color="#10B981">**✓ 严格达标**</font> | 倒角防折弯，软管直接向左侧顺畅输出 |
| **右侧 4 泵出水方向** | **朝向右侧/后侧外部** | **→** | <font color="#10B981">**✓ 严格达标**</font> | 两组朝向完全相反（背向外凸），杜绝干涉 |
| **中部分隔通道间距** | **净空 11.5 mm** | **1.15 cm** | <font color="#10B981">**✓ 合格**</font> | 左右两排泵体间保留完整走线与绝缘安全通道 |
| **出水嘴最大横向总跨距** | **136.2 mm** | **13.62 cm** | <font color="#10B981">**✓ 合格 (≤ 25 cm)**</font> | 即使计入两侧突出宝塔水嘴，依然远低于 25 cm |

---

## 五、干涉检测与配合验证

- **干涉碰撞检测（Clash Detection）**：装配体 14 个独立实体，经 91 组几何碰撞核验，**0 干涉（Clashes: 0）**。
- **电机与仓壁配合**：
  - 左列电机中心位于 $X = -24.5\text{ mm}$，右列电机中心位于 $X = +24.5\text{ mm}$。
  - 两台 $\Phi 27.5\text{ mm}$ 电机之间的内部水平间隙为 **21.5 mm**，绝不相碰。
  - 电机到机箱内侧壁的避让距离为 **6.25 mm**，装配顺畅。

---

## 六、交付文件清单（位于 `~/Documents/Shapr3D_Models/`）

已生成全套 CAD 实体与 3D 打印切片文件，并已推送至 Shapr3D：

1. **整机装配体总成**：
   - CAD 实体：[`8_channel_opposite_pumps_95mm.step`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/8_channel_opposite_pumps_95mm.step)
   - 3D 打印格式：[`8_channel_opposite_pumps_95mm.stl`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/8_channel_opposite_pumps_95mm.stl)
2. **9.5cm 前面板（反向开孔）**：
   - CAD 实体：[`front_mounting_panel_95mm.step`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/front_mounting_panel_95mm.step)
   - 3D 打印格式：[`front_mounting_panel_95mm.stl`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/front_mounting_panel_95mm.stl) / [`front_mounting_panel_95mm.3mf`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/front_mounting_panel_95mm.3mf)
3. **9.5cm 机箱外壳**：
   - CAD 实体：[`chassis_enclosure_95mm.step`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/chassis_enclosure_95mm.step)
   - 3D 打印格式：[`chassis_enclosure_95mm.stl`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/chassis_enclosure_95mm.stl) / [`chassis_enclosure_95mm.3mf`](file:///Users/zhangshuxuan/Documents/Shapr3D_Models/chassis_enclosure_95mm.3mf)
