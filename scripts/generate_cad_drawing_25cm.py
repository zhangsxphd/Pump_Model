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

def draw_cad_sheet_25cm():
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
    # VIEW 1: 正视图 (FRONT VIEW) - Center (230, 530)
    # Scale: 1mm = 1.3 units (compact 246mm chassis -> 319.8 units)
    # =========================================================================
    S = 1.30
    fx0, fy0 = 230, 530
    cw, ch = 246 * S, 176 * S  # 319.8, 228.8
    fl, fb = fx0 - cw/2, fy0 - ch/2

    ax.text(fx0, fy0 + ch/2 + 60, "正视图 (主视图 / FRONT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(fx0, fy0 + ch/2 + 46, "★ 极限尺寸约束: 246mm × 176mm (严格 ≤ 250×250mm / 25×25cm) ★", fontsize=8.5, ha='center', color='#DC2626', fontweight='bold')

    # Chassis Outer Box (R14)
    box = FancyBboxPatch((fl, fb), cw, ch, boxstyle=f"round,pad=0,rounding_size={14*S}",
                         facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(box)

    # 4 Foot pads at bottom (span 200 mm)
    for foot_x in [fx0 - 100*S, fx0 + 100*S]:
        ax.add_patch(Rectangle((foot_x - 10*S, fb - 6*S), 20*S, 6*S, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.2))

    # Front Panel (238 x 166 mm)
    pw, ph = 238 * S, 166 * S
    pl, pb = fx0 - pw/2, fy0 - ph/2
    panel_box = FancyBboxPatch((pl, pb), pw, ph, boxstyle=f"round,pad=0,rounding_size={10*S}",
                               facecolor='#FFFFFF', edgecolor='#475569', linewidth=1.2)
    ax.add_patch(panel_box)

    # 4 Corner panel mounting screws (M3 at +/- 108, +/- 72)
    for scx in [fx0 - 108*S, fx0 + 108*S]:
        for scy in [fy0 - 72*S, fy0 + 72*S]:
            ax.add_patch(Circle((scx, scy), 3.5*S/2, facecolor='#E2E8F0', edgecolor=C_OUTLINE, lw=0.9))
            ax.plot([scx - 3.5, scx + 3.5], [scy, scy], color='#64748B', lw=0.6)
            ax.plot([scx, scx], [scy - 3.5, scy + 3.5], color='#64748B', lw=0.6)

    # 8 Pumps (2 rows x 4 cols: pitch X = 58.0, pitch Y = 68.0)
    pump_xs_mm = [-87.0, -29.0, 29.0, 87.0]
    pump_ys_mm = [-34.0, 34.0]
    
    for row_idx, py_mm in enumerate(pump_ys_mm):
        for col_idx, px_mm in enumerate(pump_xs_mm):
            pcx = fx0 + px_mm * S
            pcy = fy0 + py_mm * S
            
            # Centerlines
            ax.plot([pcx - 26*S, pcx + 26*S], [pcy, pcy], color=C_CENTER, lw=0.5, linestyle='-.')
            ax.plot([pcx, pcx], [pcy - 22*S, pcy + 42*S], color=C_CENTER, lw=0.5, linestyle='-.')
            
            # Mounting ears (width 56.6, height 8.1, holes pitch 48.5)
            ear_w = 48.5 * S
            ear_h = 8.1 * S
            ax.add_patch(Rectangle((pcx - ear_w/2, pcy - ear_h/2), ear_w, ear_h, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.9))
            ax.add_patch(Circle((pcx - 24.25*S, pcy), 4.05*S, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.9))
            ax.add_patch(Circle((pcx + 24.25*S, pcy), 4.05*S, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.9))
            # Ear screw holes (Φ3.2)
            ax.add_patch(Circle((pcx - 24.25*S, pcy), 3.2*S/2, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=0.7))
            ax.add_patch(Circle((pcx + 24.25*S, pcy), 3.2*S/2, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=0.7))
            
            # Circular pump head body (Φ37.5)
            ax.add_patch(Circle((pcx, pcy), 37.5*S/2, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.1))
            ax.add_patch(Circle((pcx, pcy), 31.5*S/2, facecolor='#1E293B', edgecolor='#475569', lw=0.7))
            ax.text(pcx, pcy, "KEF", fontsize=5.5, color='#F8FAFC', ha='center', va='center', fontweight='bold')
            
            # Top manifold block
            ax.add_patch(Rectangle((pcx - 11*S, pcy + 10*S), 22*S, 11.85*S, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=0.9))
            
            # 2 Barbed Nozzles
            for nx_offset in [-6.5*S, 6.5*S]:
                nz_x = pcx + nx_offset
                nz_y = pcy + 21.85*S
                ax.add_patch(Rectangle((nz_x - 1.8*S, nz_y), 3.6*S, 20*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.7))
                for barb_dy in [5*S, 10*S]:
                    pts = np.array([
                        [nz_x - 1.8*S, nz_y + barb_dy],
                        [nz_x - 2.6*S, nz_y + barb_dy + 3.5*S],
                        [nz_x + 2.6*S, nz_y + barb_dy + 3.5*S],
                        [nz_x + 1.8*S, nz_y + barb_dy]
                    ])
                    ax.add_patch(Polygon(pts, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=0.6))

    # Front View Dimensions
    p1_x = fx0 + pump_xs_mm[0]*S
    p2_x = fx0 + pump_xs_mm[1]*S
    p3_x = fx0 + pump_xs_mm[2]*S
    p4_x = fx0 + pump_xs_mm[3]*S
    p_bot_y = fy0 + pump_ys_mm[0]*S
    p_top_y = fy0 + pump_ys_mm[1]*S

    draw_dim_h(fl, fl + cw, fb, -32, "外壳总宽 246.0 (≤250)")
    draw_dim_h(pl, pl + pw, fb, -18, "前面板宽 238.0")
    draw_dim_h(p1_x, p2_x, fy0 + pump_ys_mm[1]*S + 45*S, 14, "紧凑列距 58.0")
    draw_dim_h(p1_x, p4_x, fy0 + pump_ys_mm[1]*S + 45*S, 28, "4泵总跨距 174.0")

    draw_dim_v(fb, fb + ch, fl, -25, "外壳高 176.0 (≤250)")
    draw_dim_v(pb, pb + ph, fl, -12, "面板高 166.0")
    draw_dim_v(p_bot_y, p_top_y, p1_x - 28*S, -10, "排距 68.0")

    ax.annotate("泵耳间缝隙 1.4mm\n紧凑无干涉排布", xy=(p2_x + 28.3*S, p_bot_y), xytext=(p2_x + 35*S, p_bot_y - 25*S),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')
    ax.annotate("4× M3 螺丝固定面板\n(孔距 216×144)", xy=(fx0 - 108*S, fy0 + 72*S), xytext=(fx0 - 138*S, fy0 + 82*S),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')


    # =========================================================================
    # VIEW 2: 俯视图 (TOP VIEW) - Center (230, 230)
    # Depth = 126 mm (chassis), total = 151.5 mm
    # =========================================================================
    tx0, ty0 = fx0, 230
    cd = 126 * S  # 163.8
    tl, tb = tx0 - cw/2, ty0 - cd/2

    ax.text(tx0, ty0 + cd/2 + 45, "俯视图 (顶面投影 / TOP VIEW)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(tx0, ty0 + cd/2 + 34, "展示机箱深度 126mm、中隔板与后部电控仓布置", fontsize=8, ha='center', color='#64748B')

    top_box = FancyBboxPatch((tl, tb), cw, cd, boxstyle=f"round,pad=0,rounding_size={14*S}",
                            facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(top_box)

    # Front panel line
    ax.plot([tl + 4*S, tl + cw - 4*S], [tb + cd, tb + cd], color='#334155', lw=2.0)

    # 4 Pumps sticking out front
    pump_front_len = 25.5 * S
    motor_in_len = 52.5 * S
    
    for px_mm in pump_xs_mm:
        pcx = tx0 + px_mm * S
        ax.add_patch(Rectangle((pcx - 37.5*S/2, tb + cd), 37.5*S, pump_front_len,
                               facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.1))
        # Hidden motors inside
        ax.add_patch(Rectangle((pcx - 31.5*S/2, tb + cd - 11.5*S), 31.5*S, 11.5*S,
                               facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))
        ax.add_patch(Rectangle((pcx - 27.5*S/2, tb + cd - 52.5*S), 27.5*S, 41*S,
                               facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))
        ax.plot([pcx, pcx], [tb + cd + pump_front_len + 4, tb + cd - 58*S], color=C_CENTER, lw=0.5, linestyle='-.')

    # Middle partition wall at Z = -60 mm
    part_y = tb + cd - 60*S
    ax.plot([tl + 4*S, tl + cw - 4*S], [part_y, part_y], color='#94A3B8', lw=1.2, linestyle='--')
    ax.text(tx0 - 50*S, part_y - 8, "中隔板 Z=-60 (t=4)", fontsize=7, color='#64748B')

    # Rear bay: 8-ch relay board representation (136 x 52 mm)
    ax.add_patch(Rectangle((tx0 - 68*S, tb + 25*S), 136*S, 20*S, facecolor='#E2E8F0', edgecolor='#64748B', lw=0.8, linestyle=':'))
    ax.text(tx0, tb + 35*S, "后部电控区 (8路继电器 / 12V电源 / MCU)", fontsize=7.5, color='#475569', ha='center', va='center')

    # Dimensions
    draw_dim_v(tb, tb + cd, tl + cw, 12, "外壳深度 126.0")
    draw_dim_v(tb + cd, tb + cd + pump_front_len, tl + cw, 12, "外凸 25.5")
    draw_dim_v(tb, tb + cd + pump_front_len, tl + cw, 24, "总深度 151.5 (≤250)")
    draw_dim_v(tb + cd - motor_in_len, tb + cd, p1_x - 20*S, -14, "电机深入 52.5")


    # =========================================================================
    # VIEW 3: 右侧视图 (RIGHT SIDE VIEW) - Center (535, 530)
    # Width = 126 mm, Height = 176 mm
    # =========================================================================
    sx0, sy0 = 530, fy0
    sl, sb = sx0 - cd/2, sy0 - ch/2

    ax.text(sx0 + pump_front_len/2, sy0 + ch/2 + 60, "右侧视图 (侧面投影 / RIGHT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(sx0 + pump_front_len/2, sy0 + ch/2 + 46, "左右对称双侧通风散热格栅、后置DC供电口", fontsize=8, ha='center', color='#64748B')

    side_box = FancyBboxPatch((sl, sb), cd, ch, boxstyle=f"round,pad=0,rounding_size={14*S}",
                             facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(side_box)

    # Foot pads
    for foot_z in [sl + 25*S, sl + (126-25)*S]:
        ax.add_patch(Rectangle((foot_z - 10*S, sb - 6*S), 20*S, 6*S, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.2))

    # Side ventilation slots (4 vertical slots: 2 upper, 2 lower)
    for v_z in [sl + (126-55)*S, sl + (126-35)*S]:
        ax.add_patch(Rectangle((v_z - 2.5*S, sy0 + 35*S - 16*S), 5*S, 32*S, facecolor='#64748B', edgecolor=C_OUTLINE, lw=0.7))
        ax.add_patch(Rectangle((v_z - 2.5*S, sy0 - 35*S - 16*S), 5*S, 32*S, facecolor='#64748B', edgecolor=C_OUTLINE, lw=0.7))

    # DC 12V power jack
    ax.add_patch(Rectangle((sl - 2*S, sy0 - 60*S - 6*S), 4*S, 12*S, facecolor='#475569', edgecolor=C_OUTLINE, lw=0.9))
    ax.text(sl - 5, sy0 - 60*S, "DC 12V", fontsize=6.5, color='#475569', ha='right', va='center')

    # External Pumps on front
    for py_mm in pump_ys_mm:
        p_side_y = sy0 + py_mm * S
        ax.add_patch(Rectangle((sl + cd, p_side_y - 37.5*S/2), 4*S, 37.5*S, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.9))
        ax.add_patch(Rectangle((sl + cd + 4*S, p_side_y - 37.5*S/2), 24*S, 37.5*S, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.1))
        ax.add_patch(Rectangle((sl + cd + 21*S - 1.8*S, p_side_y + 18.75*S), 3.6*S, 22*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.7))
        ax.add_patch(Rectangle((sl + cd - 52.5*S, p_side_y - 27.5*S/2), 52.5*S, 27.5*S, facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))

    # Dimensions
    draw_dim_h(sl, sl + cd, sb, -20, "深度 126.0")
    draw_dim_h(sl + cd, sl + cd + pump_front_len, sb, -20, "外凸 25.5")
    draw_dim_v(sb, sb + ch, sl + cd + pump_front_len, 18, "高度 176.0")
    draw_dim_v(sb - 6*S, sb, sl, -16, "脚垫 6.0")


    # =========================================================================
    # VIEW 4: 3D 轴测图 (ISOMETRIC 3D RENDER) - Positioned at (900, 530)
    # =========================================================================
    ax.text(935, fy0 + ch/2 + 60, "三维轴测效果参考 (COMPACT 3D CAD)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(935, fy0 + ch/2 + 46, "Shapr3D 原生紧凑款实体模型立体渲染", fontsize=8, ha='center', color='#64748B')

    try:
        iso_img_path = '/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/compact_25cm_3d_preview.png'
        iso_img = Image.open(iso_img_path)
        ax.imshow(iso_img, extent=(730, 1150, fy0 - ch/2 - 10, fy0 + ch/2 + 35), zorder=10)
        ax.add_patch(Rectangle((730, fy0 - ch/2 - 10), 420, ch + 45, fill=False, edgecolor='#CBD5E1', lw=0.8))
    except Exception as e:
        print("Could not load iso image:", e)


    # =========================================================================
    # DESIGN FEATURES & PARAMETERS TABLE (Center Bottom)
    # =========================================================================
    ax.text(800, 310, "★ 25×25cm 极限包络尺寸验证与参数表 (DIMENSION VERIFICATION) ★", fontsize=10.5, fontweight='bold', ha='center', color='#DC2626')

    table_data = [
        ("尺寸项目 / 部件", "实测尺寸 (mm / cm)", "25×25cm 约束判定", "工程配合与结构说明"),
        ("整机外形总宽", "246.0 mm (24.60 cm)", "✔ 合格 (< 25.0 cm)", "4泵紧凑列距58mm，耳间隙1.4mm，四角R14圆角"),
        ("整机外形总高", "176.0 mm (17.60 cm)", "✔ 合格 (< 25.0 cm)", "含底脚垫总高 182.0 mm (18.2 cm)，远低于25cm"),
        ("整机外形总深", "151.5 mm (15.15 cm)", "✔ 合格 (< 25.0 cm)", "机箱厚度126mm + 泵头外凸25.5mm，远低于25cm"),
        ("前面板安装板", "238.0 × 166.0 × 4.0 mm", "✔ 合格 (平嵌内嵌)", "8×Φ33mm电机通孔 + 16×Φ3.2mm M3孔，刚性极佳"),
        ("面板固定方式", "4× M3 沉头螺丝", "四角孔距 216 × 144 mm", "紧固于机箱内壁 4 处加厚增强圆柱立柱"),
        ("前后双仓划分", "隔板厚 4.0mm (Z=-60mm)", "电机与电路物理隔离", "前仓56mm放8台电机；后仓62mm放电控模块"),
        ("后部电气配置", "横置8路继电器 + 12V电源", "仓内宽238×高166×深62", "继电器板横置固定，空间宽裕，走线顺畅"),
        ("双侧对流散热", "左右侧壁各 4× (5×32mm)", "烟囱自然对流风道", "双侧壁对称百叶槽，有效排出电源与继电器热量")
    ]

    row_y = 285
    col_x = [450, 610, 750, 1160]
    for row_idx, row in enumerate(table_data):
        is_header = (row_idx == 0)
        bg_col = '#E2E8F0' if is_header else ('#FEF2F2' if '✔' in row[2] and row_idx <= 3 else ('#F8FAFC' if row_idx % 2 == 1 else '#FFFFFF'))
        ax.add_patch(Rectangle((col_x[0], row_y - 15), col_x[3] - col_x[0], 15,
                               facecolor=bg_col, edgecolor='#CBD5E1', lw=0.6))
        for col_idx in range(4):
            cell_text = row[col_idx]
            font_w = 'bold' if is_header or col_idx in [1, 2] else 'normal'
            if col_idx == 2 and '✔' in cell_text:
                text_col = '#15803D'
            elif is_header:
                text_col = C_FRAME
            else:
                text_col = '#1E293B'
            ax.text(col_x[col_idx] + 5, row_y - 8, cell_text, fontsize=7.0, va='center',
                    fontweight=font_w, color=text_col)
        row_y -= 15

    # =========================================================================
    # MODIFICATION CONFIRMATION GUIDE (Bottom Left)
    # =========================================================================
    note_box_x, note_box_y = 25, 25
    ax.add_patch(Rectangle((note_box_x, note_box_y), 410, 95, fill=True, facecolor='#FEF2F2', edgecolor='#FCA5A5', lw=1.2))
    ax.text(note_box_x + 10, note_box_y + 82, "25cm 紧凑方案确认指引 (CONFIRMATION GUIDE):", fontsize=8.5, fontweight='bold', color='#DC2626')
    
    questions = [
        "1. 尺寸确认: 目前三向全尺寸 246 × 182 × 151.5 mm，均严格控制在 25×25cm 制造上限内。",
        "2. 紧凑列距: 水平列距 58mm (相邻耳缝隙 1.4mm)，紧密美观；若需更宽可缩为3泵或上下交错。",
        "3. 电控后置: 8路继电器板与电源移至中隔板后仓，正面紧凑无冗余宽度，布线整洁隔离。",
        "4. 面板固定: 4颗 M3 沉头螺丝固定，如需无螺丝卡扣或翻盖结构请随时提出。",
        "5. 制造工艺: 本尺寸可完美放入任意 256×256 或 250×250mm 标准 3D 打印热床一体成型打印！"
    ]
    for i, q in enumerate(questions):
        ax.text(note_box_x + 10, note_box_y + 68 - i * 13, q, fontsize=7.2, color='#7F1D1D')

    # =========================================================================
    # TITLE BLOCK (Bottom Right)
    # =========================================================================
    tb_x, tb_y, tb_w, tb_h = 820, 25, 355, 95
    ax.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=True, facecolor='#F1F5F9', edgecolor=C_FRAME, linewidth=1.5))
    ax.plot([tb_x, tb_x + tb_w], [tb_y + 60, tb_y + 60], color=C_FRAME, lw=1)
    ax.plot([tb_x, tb_x + tb_w], [tb_y + 35, tb_y + 35], color=C_FRAME, lw=1)
    ax.plot([tb_x + 180, tb_x + 180], [tb_y, tb_y + 60], color=C_FRAME, lw=1)
    ax.plot([tb_x + 270, tb_x + 270], [tb_y, tb_y + 35], color=C_FRAME, lw=1)

    ax.text(tb_x + tb_w / 2, tb_y + 78, "8路蠕动泵一体机 (≤25×25cm 紧凑外置方案)", fontsize=11.0, fontweight='bold', ha='center', va='center', color=C_FRAME)
    ax.text(tb_x + tb_w / 2, tb_y + 68, "工程三视图与极限包络尺寸草图 (CAD DRAFT V3.0)", fontsize=8, ha='center', va='center', color='#475569')
    
    ax.text(tb_x + 8, tb_y + 48, "图纸代号: KEF-8CH-25CM-01", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 48, "方案状态: 尺寸已达标 ≤25cm", fontsize=7.5, fontweight='bold', va='center', color='#15803D')
    ax.text(tb_x + 8, tb_y + 24, "比例: 1:2", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 24, "单位: mm", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 280, tb_y + 24, "投影: 第三视角", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 8, tb_y + 8, "设计建模: Shapr3D / B-Rep", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 8, "日期: 2026-10-04", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 280, tb_y + 8, "图幅: A3 标准图纸", fontsize=7.5, va='center', color=C_TEXT)

    out_path = "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/cad_blueprint_25cm_compact.png"
    plt.savefig(out_path, bbox_inches='tight', dpi=200, facecolor=C_BG)
    print("Compact 25cm CAD Blueprint generated at:", out_path)

if __name__ == '__main__':
    draw_cad_sheet_25cm()
