#!/usr/bin/env python3
"""
Generate Standard CAD Engineering Blueprint for:
8-Channel Peristaltic Pump Station (9.5cm Width / Opposite Mounting Design)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
from PIL import Image
import numpy as np

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Hiragino Sans GB', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

C_BG = '#FBFDFF'        # Blueprint off-white
C_FRAME = '#1E3A8A'     # Engineering blue
C_OUTLINE = '#0F172A'   # Main object outline
C_HIDDEN = '#64748B'    # Hidden lines
C_CENTER = '#DC2626'    # Centerlines
C_DIM = '#1D4ED8'       # Dimension lines & text
C_TEXT = '#0F172A'      # Annotation text
C_PUMP_EDGE = '#1E293B' # Pump edge

def draw_cad_sheet_95mm():
    fig = plt.figure(figsize=(24, 16), dpi=160)
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 800)
    ax.axis('off')

    # 1. Border
    ax.add_patch(Rectangle((15, 15), 1170, 770, fill=False, edgecolor=C_FRAME, linewidth=2.5))
    ax.add_patch(Rectangle((25, 25), 1150, 750, fill=False, edgecolor=C_FRAME, linewidth=1.2))

    # Grid marks
    for i, x in enumerate(range(120, 1150, 190), start=1):
        ax.text(x, 20, str(i), fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
        ax.text(x, 770, str(i), fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
    for i, y in enumerate(range(100, 750, 140), start=1):
        c = chr(64 + i)
        ax.text(20, y, c, fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
        ax.text(1170, y, c, fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')

    def draw_dim_h(x1, x2, y_ref, offset, text):
        y_dim = y_ref + offset
        ax.plot([x1, x1], [y_ref, y_dim + (3 if offset>0 else -3)], color=C_DIM, lw=0.7)
        ax.plot([x2, x2], [y_ref, y_dim + (3 if offset>0 else -3)], color=C_DIM, lw=0.7)
        ax.annotate('', xy=(x1, y_dim), xytext=(x2, y_dim),
                    arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=0.9, shrinkA=0, shrinkB=0))
        ty = y_dim + (4 if offset > 0 else -5)
        ax.text((x1 + x2)/2, ty, text, fontsize=7.5, ha='center',
                va='bottom' if offset>0 else 'top', color=C_DIM, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.15', facecolor=C_BG, edgecolor='none'))

    def draw_dim_v(y1, y2, x_ref, offset, text):
        x_dim = x_ref + offset
        ax.plot([x_ref, x_dim + (3 if offset>0 else -3)], [y1, y1], color=C_DIM, lw=0.7)
        ax.plot([x_ref, x_dim + (3 if offset>0 else -3)], [y2, y2], color=C_DIM, lw=0.7)
        ax.annotate('', xy=(x_dim, y1), xytext=(x_dim, y2),
                    arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=0.9, shrinkA=0, shrinkB=0))
        tx = x_dim + (4 if offset > 0 else -4)
        ax.text(tx, (y1 + y2)/2, text, fontsize=7.5, ha='left' if offset>0 else 'right',
                va='center', color=C_DIM, fontweight='bold', rotation=90,
                bbox=dict(boxstyle='square,pad=0.15', facecolor=C_BG, edgecolor='none'))

    # =========================================================================
    # VIEW 1: 主视图 (FRONT VIEW) - Center (200, 480)
    # Scale: 1mm = 1.3 units. Panel W=95mm -> 123.5u, H=240mm -> 312u
    # =========================================================================
    S = 1.25
    fx0, fy0 = 200, 480
    pw, ph = 95.0 * S, 240.0 * S # 118.75, 300.0
    pl, pb = fx0 - pw/2, fy0 - ph/2

    ax.text(fx0, fy0 + ph/2 + 55, "正视图 (主视图 / FRONT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(fx0, fy0 + ph/2 + 40, "★ 板宽约束: 95.0 mm (9.5 cm) | 整机极限 ≤ 250×250 mm ★", fontsize=8.5, ha='center', color='#DC2626', fontweight='bold')

    # Panel Body (R6)
    panel_box = FancyBboxPatch((pl, pb), pw, ph, boxstyle=f"round,pad=0,rounding_size={6*S}",
                               facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=1.8)
    ax.add_patch(panel_box)

    # Center dividing zone guide lines
    mid_gap = 11.5 * S
    ax.plot([fx0 - mid_gap/2, fx0 - mid_gap/2], [pb + 10, pb + ph - 10], color='#94A3B8', lw=0.8, ls='--')
    ax.plot([fx0 + mid_gap/2, fx0 + mid_gap/2], [pb + 10, pb + ph - 10], color='#94A3B8', lw=0.8, ls='--')
    ax.text(fx0, fy0, "中间区域\n(11.5mm)", fontsize=6.8, ha='center', va='center', color='#64748B', fontweight='bold')

    # 4 Corner Mounting Screws
    cx_off, cy_off = 38.0 * S, 110.0 * S
    for cx in [fx0 - cx_off, fx0 + cx_off]:
        for cy in [fy0 - cy_off, fy0 + cy_off]:
            ax.add_patch(Circle((cx, cy), 1.7 * S, facecolor='white', edgecolor=C_OUTLINE, lw=0.8))
            ax.plot([cx - 2.5*S, cx + 2.5*S], [cy, cy], color=C_CENTER, lw=0.5)
            ax.plot([cx, cx], [cy - 2.5*S, cy + 2.5*S], color=C_CENTER, lw=0.5)

    # 8 Pumps: 4 on Left (pointing Left <-), 4 on Right (pointing Right ->)
    pump_ys = [-87.0, -29.0, 29.0, 87.0]
    xl = fx0 - 24.5 * S
    xr = fx0 + 24.5 * S
    r_body = 18.75 * S
    r_ear = 4.0 * S

    for py_val in pump_ys:
        py = fy0 + py_val * S

        # LEFT PUMP: Center at (xl, py), Nozzles point Left (<-)
        # 1. Ears along Y at py +- 24.25*S
        ax.add_patch(Circle((xl, py + 24.25*S), r_ear, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.8))
        ax.add_patch(Circle((xl, py - 24.25*S), r_ear, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.8))
        ax.add_patch(Rectangle((xl - r_ear, py - 24.25*S), 2*r_ear, 48.5*S, facecolor='#E2E8F0', edgecolor='none'))
        ax.add_patch(Circle((xl, py + 24.25*S), 1.6*S, facecolor='white', edgecolor=C_PUMP_EDGE, lw=0.6))
        ax.add_patch(Circle((xl, py - 24.25*S), 1.6*S, facecolor='white', edgecolor=C_PUMP_EDGE, lw=0.6))
        # 2. Main Body
        ax.add_patch(Circle((xl, py), r_body, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.2))
        ax.add_patch(Circle((xl, py), 15.5*S, facecolor='#1E293B', edgecolor='#0F172A', lw=0.8))
        ax.text(xl, py, "KEF", color='#94A3B8', fontsize=5.5, ha='center', va='center', fontweight='bold')
        # 3. Barbed Nozzles pointing LEFT (<-)
        for ny_off in [-6.5*S, 6.5*S]:
            ny = py + ny_off
            ax.add_patch(Rectangle((xl - 40*S, ny - 2.0*S), 22*S, 4.0*S, facecolor='#94A3B8', edgecolor=C_PUMP_EDGE, lw=0.7))
            # Barbs
            ax.add_patch(Polygon([[xl - 28*S, ny + 2.8*S], [xl - 31*S, ny + 2.8*S], [xl - 33*S, ny + 2.0*S],
                                  [xl - 33*S, ny - 2.0*S], [xl - 31*S, ny - 2.8*S], [xl - 28*S, ny - 2.8*S]],
                                 closed=True, facecolor='#64748B', edgecolor=C_PUMP_EDGE, lw=0.6))
            ax.add_patch(Polygon([[xl - 34*S, ny + 2.8*S], [xl - 37*S, ny + 2.8*S], [xl - 39*S, ny + 2.0*S],
                                  [xl - 39*S, ny - 2.0*S], [xl - 37*S, ny - 2.8*S], [xl - 34*S, ny - 2.8*S]],
                                 closed=True, facecolor='#64748B', edgecolor=C_PUMP_EDGE, lw=0.6))

        # RIGHT PUMP: Center at (xr, py), Nozzles point Right (->)
        # 1. Ears along Y at py +- 24.25*S
        ax.add_patch(Circle((xr, py + 24.25*S), r_ear, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.8))
        ax.add_patch(Circle((xr, py - 24.25*S), r_ear, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.8))
        ax.add_patch(Rectangle((xr - r_ear, py - 24.25*S), 2*r_ear, 48.5*S, facecolor='#E2E8F0', edgecolor='none'))
        ax.add_patch(Circle((xr, py + 24.25*S), 1.6*S, facecolor='white', edgecolor=C_PUMP_EDGE, lw=0.6))
        ax.add_patch(Circle((xr, py - 24.25*S), 1.6*S, facecolor='white', edgecolor=C_PUMP_EDGE, lw=0.6))
        # 2. Main Body
        ax.add_patch(Circle((xr, py), r_body, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.2))
        ax.add_patch(Circle((xr, py), 15.5*S, facecolor='#1E293B', edgecolor='#0F172A', lw=0.8))
        ax.text(xr, py, "KEF", color='#94A3B8', fontsize=5.5, ha='center', va='center', fontweight='bold')
        # 3. Barbed Nozzles pointing RIGHT (->)
        for ny_off in [-6.5*S, 6.5*S]:
            ny = py + ny_off
            ax.add_patch(Rectangle((xr + 18*S, ny - 2.0*S), 22*S, 4.0*S, facecolor='#94A3B8', edgecolor=C_PUMP_EDGE, lw=0.7))
            # Barbs
            ax.add_patch(Polygon([[xr + 28*S, ny + 2.8*S], [xr + 31*S, ny + 2.8*S], [xr + 33*S, ny + 2.0*S],
                                  [xr + 33*S, ny - 2.0*S], [xr + 31*S, ny - 2.8*S], [xr + 28*S, ny - 2.8*S]],
                                 closed=True, facecolor='#64748B', edgecolor=C_PUMP_EDGE, lw=0.6))
            ax.add_patch(Polygon([[xr + 34*S, ny + 2.8*S], [xr + 37*S, ny + 2.8*S], [xr + 39*S, ny + 2.0*S],
                                  [xr + 39*S, ny - 2.0*S], [xr + 37*S, ny - 2.8*S], [xr + 34*S, ny - 2.8*S]],
                                 closed=True, facecolor='#64748B', edgecolor=C_PUMP_EDGE, lw=0.6))

    # Flow direction callout banners
    ax.annotate('前侧出泵方向 (← 4个泵)', xy=(xl - 42*S, fy0), xytext=(xl - 65*S, fy0),
                arrowprops=dict(facecolor='#2563EB', edgecolor='none', width=2.5, headwidth=7),
                fontsize=8.5, fontweight='bold', color='#1E40AF', ha='right', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.0))
    ax.annotate('后侧出泵方向 (4个泵 →)', xy=(xr + 42*S, fy0), xytext=(xr + 65*S, fy0),
                arrowprops=dict(facecolor='#2563EB', edgecolor='none', width=2.5, headwidth=7),
                fontsize=8.5, fontweight='bold', color='#1E40AF', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.0))

    # Front View Dimensions
    draw_dim_h(pl, pl + pw, pb + ph, 20, "板宽 95.0 mm (9.5 cm)")
    draw_dim_h(xl, xr, pb + ph, 8, "两列中心距 49.0")
    draw_dim_h(xl - 43.6*S, xr + 43.6*S, pb, -22, "出水嘴总跨距 136.2 mm")
    draw_dim_v(pb, pb + ph, pl, -22, "板长/总高 240.0 mm (24.0 cm ≤25cm)")
    draw_dim_v(fy0 + pump_ys[0]*S, fy0 + pump_ys[1]*S, pl + pw, 18, "坚向排距 58.0")
    draw_dim_v(fy0 + pump_ys[0]*S, fy0 + pump_ys[3]*S, pl + pw, 32, "4泵总跨距 174.0")

    # =========================================================================
    # VIEW 2: 俯视图 (TOP VIEW / 顶面投影) - Center (200, 160)
    # Scale: S = 1.25. W=95mm, Depth=72mm (with pump head protrude 29.5mm)
    # =========================================================================
    tx0, ty0 = 200, 170
    cd = 72.0 * S
    p_head = 29.5 * S

    ax.text(tx0, ty0 + cd/2 + 35, "俯视图 (顶面投影 / TOP VIEW)", fontsize=10.5, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(tx0, ty0 + cd/2 + 23, "展示95mm机身、左右对称反向出水嘴与后部电控仓", fontsize=7.5, ha='center', color='#475569')

    # Chassis Box Outline
    ax.add_patch(Rectangle((tx0 - pw/2, ty0 - cd/2), pw, cd, facecolor='#F8FAFC', edgecolor=C_OUTLINE, lw=1.5))
    # Panel Front Surface (at bottom Y = ty0 - cd/2)
    ax.add_patch(Rectangle((tx0 - pw/2, ty0 - cd/2), pw, 4*S, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.0))

    # Top pumps protruding forward
    # Left pump: body at (tx0 - 24.5*S), nozzle pointing LEFT (<-)
    ax.add_patch(Rectangle((tx0 - 24.5*S - r_body, ty0 - cd/2 - p_head), 2*r_body, p_head, facecolor='#334155', edgecolor=C_OUTLINE, lw=1.0))
    ax.add_patch(Rectangle((tx0 - 24.5*S - 40*S, ty0 - cd/2 - p_head + 8*S), 25*S, 4*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.7))
    # Right pump: body at (tx0 + 24.5*S), nozzle pointing RIGHT (->)
    ax.add_patch(Rectangle((tx0 + 24.5*S - r_body, ty0 - cd/2 - p_head), 2*r_body, p_head, facecolor='#334155', edgecolor=C_OUTLINE, lw=1.0))
    ax.add_patch(Rectangle((tx0 + 24.5*S + 15*S, ty0 - cd/2 - p_head + 8*S), 25*S, 4*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.7))

    # Internal motors hidden outlines (dashed)
    ax.add_patch(Rectangle((tx0 - 24.5*S - 13.75*S, ty0 - cd/2 + 4*S), 27.5*S, 52.5*S, fill=False, edgecolor=C_HIDDEN, lw=0.8, ls='--'))
    ax.add_patch(Rectangle((tx0 + 24.5*S - 13.75*S, ty0 - cd/2 + 4*S), 27.5*S, 52.5*S, fill=False, edgecolor=C_HIDDEN, lw=0.8, ls='--'))
    ax.text(tx0 - 24.5*S, ty0, "左列电机\n(Φ27.5)", fontsize=6.0, ha='center', va='center', color=C_HIDDEN)
    ax.text(tx0 + 24.5*S, ty0, "右列电机\n(Φ27.5)", fontsize=6.0, ha='center', va='center', color=C_HIDDEN)

    draw_dim_h(tx0 - pw/2, tx0 + pw/2, ty0 + cd/2, 12, "机壳宽度 95.0 mm")
    draw_dim_v(ty0 - cd/2, ty0 + cd/2, tx0 + pw/2, 14, "底座深度 72.0")
    draw_dim_v(ty0 - cd/2 - p_head, ty0 + cd/2, tx0 + pw/2, 30, "整机总深 101.5 mm")

    # =========================================================================
    # VIEW 3: 右侧视图 (RIGHT ELEVATION) - Center (490, 480)
    # =========================================================================
    sx0, sy0 = 490, 480
    ax.text(sx0, sy0 + ph/2 + 55, "右侧视图 (侧面投影 / RIGHT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(sx0, sy0 + ph/2 + 40, "左右对称通风百叶、外露凸出泵头与底部支撑脚", fontsize=7.5, ha='center', color='#475569')

    # Chassis Side Box
    ax.add_patch(Rectangle((sx0 - cd/2, sy0 - ph/2), cd, ph, facecolor='#F8FAFC', edgecolor=C_OUTLINE, lw=1.8))
    # Front panel plate (left edge of side view)
    ax.add_patch(Rectangle((sx0 - cd/2 - 4*S, sy0 - ph/2), 4*S, ph, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.0))

    # 4 Pump heads sticking out to the left
    for py_val in pump_ys:
        py = sy0 + py_val * S
        # Pump body side
        ax.add_patch(Rectangle((sx0 - cd/2 - 4*S - 25.5*S, py - r_body), 25.5*S, 2*r_body, facecolor='#334155', edgecolor=C_OUTLINE, lw=1.0))
        # Nozzle pointing toward viewer / side
        ax.add_patch(Rectangle((sx0 - cd/2 - 4*S - 18*S, py - 4*S), 6*S, 8*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.8))

    # Ventilation slots on side
    for vy_val in [-60.0, -20.0, 20.0, 60.0]:
        vy = sy0 + vy_val * S
        ax.add_patch(Rectangle((sx0 - 10*S, vy - 2*S), 20*S, 4*S, facecolor='#64748B', edgecolor=C_OUTLINE, lw=0.6))

    # Bottom foot pads (on the back wall / right edge)
    ax.add_patch(Rectangle((sx0 + cd/2, sy0 - cy_off - 5*S), 5*S, 10*S, facecolor='#475569', edgecolor=C_OUTLINE, lw=0.8))
    ax.add_patch(Rectangle((sx0 + cd/2, sy0 + cy_off - 5*S), 5*S, 10*S, facecolor='#475569', edgecolor=C_OUTLINE, lw=0.8))

    draw_dim_h(sx0 - cd/2, sx0 + cd/2, sy0 + ph/2, 12, "底座深 72.0")
    draw_dim_h(sx0 - cd/2 - 29.5*S, sx0 + cd/2, sy0 - ph/2, -18, "含泵头总深 101.5 mm")
    draw_dim_v(sy0 - ph/2, sy0 + ph/2, sx0 + cd/2, 18, "高度 240.0 mm (24.0 cm)")

    # =========================================================================
    # VIEW 4: 三维轴测效果参考 (3D ISOMETRIC CAD EMBED) - Center (850, 560)
    # =========================================================================
    ax.text(850, 755, "三维真实装配实体渲染 (3D ISOMETRIC PREVIEW)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(850, 740, "Shapr3D 原生实体模型 / 左右反向出水嘴 / 9.5cm极限板宽", fontsize=8.0, ha='center', color='#475569')

    # Load 3D preview render image
    preview_img_path = '/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/opposite_pumps_95mm_3d_preview.png'
    try:
        img = Image.open(preview_img_path)
        # Position image in [620, 390, 460, 340]
        ax.imshow(img, extent=[630, 1070, 400, 730], aspect='auto', zorder=5)
        ax.add_patch(Rectangle((630, 400), 440, 330, fill=False, edgecolor='#CBD5E1', lw=1.2, zorder=6))
    except Exception as e:
        ax.text(850, 560, f"3D 预览图载入: {e}", ha='center', va='center')

    # =========================================================================
    # SECTION 5: 尺寸参数核验与方案判定表 - Box (630, 170) to (1140, 370)
    # =========================================================================
    ax.text(885, 375, "★ 9.5cm 板宽与 ≤25×25cm 极限制约核验表 ★", fontsize=10.5, fontweight='bold', ha='center', color='#DC2626')

    # Table layout
    cols = [630, 750, 855, 960, 1140]
    headers = ["部件 / 检验项目", "设计实测尺寸 (mm)", "约束指标判定", "工程配合与结构说明"]
    rows = [
        ["前面板宽度 (Panel W)", "95.0 mm (9.50 cm)", "✓ 严格达标 (9.5cm)", "完全吻合用户指定 9.5cm 板宽要求"],
        ["整机外形总高 (Height)", "240.0 mm (24.00 cm)", "✓ 合格 (≤ 25.0 cm)", "坚向 4 泵紧凑列距 58mm，富余 10mm"],
        ["整机机箱深度 (Depth)", "72.0 mm (含泵头 101.5)", "✓ 合格 (≤ 25.0 cm)", "电机深52.5mm + 后腔布线裕量12.5mm"],
        ["左侧4泵出水方向", "朝向左侧/前侧外部 (←)", "✓ 严格达标", "倒角防折弯出管，外凸直接对接软管"],
        ["右侧4泵出水方向", "朝向右侧/后侧外部 (→)", "✓ 严格达标", "两组出水方向完全相反，杜绝干涉"],
        ["中部分隔通道间距", "净空宽 11.5 mm", "✓ 合格 (独立隔断)", "左右两排泵体间完整物理间隙与走线道"],
        ["出水嘴最大横向跨距", "136.2 mm (13.62 cm)", "✓ 合格 (≤ 25.0 cm)", "即使计入两侧出水嘴，依然远低于25cm"]
    ]

    # Draw Table Header
    y_t = 350
    ax.add_patch(Rectangle((cols[0], y_t - 22), cols[-1] - cols[0], 22, facecolor='#1E3A8A', edgecolor='none'))
    for ci, h in enumerate(headers):
        ax.text((cols[ci] + cols[ci+1])/2, y_t - 11, h, color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')

    # Draw Table Rows
    y_r = y_t - 22
    for ri, r in enumerate(rows):
        bg = '#F8FAFC' if ri % 2 == 0 else '#FFFFFF'
        ax.add_patch(Rectangle((cols[0], y_r - 18), cols[-1] - cols[0], 18, facecolor=bg, edgecolor='#E2E8F0', lw=0.6))
        for ci, val in enumerate(r):
            tc = '#16A34A' if '✓' in val else C_TEXT
            fw = 'bold' if '✓' in val or ci==0 else 'normal'
            ax.text((cols[ci] + cols[ci+1])/2, y_r - 9, val, color=tc, fontsize=6.8, fontweight=fw, ha='center', va='center')
        y_r -= 18

    # =========================================================================
    # SECTION 6: 制造与装配技术指引 (CONFIRMATION NOTES)
    # =========================================================================
    ax.add_patch(Rectangle((40, 40), 570, 85, facecolor='#FEF2F2', edgecolor='#F87171', lw=1.0))
    ax.text(50, 112, "【9.5cm 反向出管设计核心特征 (DESIGN NOTES)】", fontsize=8.5, fontweight='bold', color='#991B1B')
    notes = [
        "1. 左右反向出管：左4泵喷嘴朝左 (←)，右4泵喷嘴朝右 (→)，形成背向外凸，流体管路左右各自出线，零交叉零打结。",
        "2. 极致板宽 9.5cm：精准将 8 个泵收容在 95mm 宽度的长条形面板内，中间保留 11.5mm 走线隔断，电机仓内间隙达 21.5mm。",
        "3. 全向极限制约 ≤ 25cm：全机尺寸 95 × 240 × 101.5 mm，即使加上出水嘴总宽仅 136.2mm，任意 3D 打印热床均可直接整机打印！",
        "4. 双重放置姿态：本结构既可垂直立式摆放（塔式），也可水平平卧摆放（控制台式），前后侧出管逻辑完全一致。"
    ]
    for ni, note in enumerate(notes):
        ax.text(50, 95 - ni * 16, note, fontsize=6.8, color='#7F1D1D')

    # =========================================================================
    # TITLE BLOCK (工程图签) - Bottom Right [630, 40, 510, 90]
    # =========================================================================
    tb_x, tb_y = 630, 40
    tb_w, tb_h = 510, 90
    ax.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, facecolor='#FFFFFF', edgecolor=C_FRAME, lw=1.5))
    ax.plot([tb_x, tb_x + tb_w], [tb_y + 45, tb_y + 45], color=C_FRAME, lw=1.0)
    ax.plot([tb_x + 320, tb_x + 320], [tb_y, tb_y + tb_h], color=C_FRAME, lw=1.0)
    ax.plot([tb_x + 415, tb_x + 415], [tb_y, tb_y + 45], color=C_FRAME, lw=1.0)

    # Title & Subtitle
    ax.text(tb_x + 160, tb_y + 68, "8路蠕动泵一体机 (9.5cm 极限板宽 / 左右反向方案)", fontsize=10.5, fontweight='bold', color=C_FRAME, ha='center', va='center')
    ax.text(tb_x + 160, tb_y + 54, "工程三视图与极限包络尺寸草图 (CAD DRAFT V4.0)", fontsize=7.5, color='#475569', ha='center', va='center')

    # Details
    ax.text(tb_x + 15, tb_y + 30, "图纸代号: KEF-8CH-95MM-OPP", fontsize=7.2, color=C_TEXT)
    ax.text(tb_x + 15, tb_y + 12, "设计建模: Shapr3D / build123d", fontsize=7.2, color=C_TEXT)
    ax.text(tb_x + 180, tb_y + 30, "设计状态: 9.5cm 板宽已达标", fontsize=7.2, fontweight='bold', color='#16A34A')
    ax.text(tb_x + 180, tb_y + 12, "约束判定: 严格 ≤ 25×25 cm", fontsize=7.2, color=C_TEXT)

    ax.text(tb_x + 367, tb_y + 30, "比例: 1:1.25", fontsize=7.2, color=C_TEXT, ha='center')
    ax.text(tb_x + 367, tb_y + 12, "单位: mm", fontsize=7.2, color=C_TEXT, ha='center')
    ax.text(tb_x + 462, tb_y + 30, "日期: 2026-10-04", fontsize=7.2, color=C_TEXT, ha='center')
    ax.text(tb_x + 462, tb_y + 12, "图幅: A3 标准", fontsize=7.2, color=C_TEXT, ha='center')

    # Save
    out_path = '/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/cad_blueprint_95mm_opposite.png'
    plt.savefig(out_path, dpi=160, bbox_inches='tight', facecolor=C_BG)
    plt.close()
    print("9.5cm CAD Blueprint generated successfully at:", out_path)

if __name__ == '__main__':
    draw_cad_sheet_95mm()
