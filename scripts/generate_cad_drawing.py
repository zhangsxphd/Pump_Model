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

C_BG = '#FBFDFF'        # Off-white technical drawing background
C_FRAME = '#1E3A8A'     # Engineering blue frame
C_OUTLINE = '#0F172A'   # Main object outline
C_HIDDEN = '#64748B'    # Hidden lines
C_CENTER = '#DC2626'    # Centerlines
C_DIM = '#1D4ED8'       # Technical dimension blue
C_TEXT = '#0F172A'      # Annotation text
C_PUMP_EDGE = '#1E293B' # Pump edge

def draw_cad_sheet():
    # A3 Aspect Ratio (420 x 297 mm -> 3360 x 2376 px at 200 DPI)
    fig = plt.figure(figsize=(24, 16), dpi=160)
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 800)
    ax.axis('off')

    # 1. Standard Technical Drawing Border
    ax.add_patch(Rectangle((15, 15), 1170, 770, fill=False, edgecolor=C_FRAME, linewidth=2.5))
    ax.add_patch(Rectangle((25, 25), 1150, 750, fill=False, edgecolor=C_FRAME, linewidth=1.2))

    # Grid reference marks
    for i, x in enumerate(range(120, 1150, 190), start=1):
        ax.text(x, 20, str(i), fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
        ax.text(x, 770, str(i), fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
    for i, y in enumerate(range(100, 750, 140), start=1):
        c = chr(64 + i)
        ax.text(20, y, c, fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')
        ax.text(1170, y, c, fontsize=8.5, ha='center', va='center', color=C_FRAME, fontweight='bold')

    # Helper: Dimension line with arrows and background box for text
    def draw_dim_h(x1, x2, y_ref, offset, text, text_pos='above'):
        y_dim = y_ref + offset
        # Extension lines
        ax.plot([x1, x1], [y_ref, y_dim + (3 if offset>0 else -3)], color=C_DIM, lw=0.7)
        ax.plot([x2, x2], [y_ref, y_dim + (3 if offset>0 else -3)], color=C_DIM, lw=0.7)
        # Dimension line
        ax.annotate('', xy=(x1, y_dim), xytext=(x2, y_dim),
                    arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=0.9, shrinkA=0, shrinkB=0))
        # Text with light background to prevent line overlap
        ty = y_dim + (4 if offset > 0 else -5)
        ax.text((x1 + x2)/2, ty, text, fontsize=7.5, ha='center',
                va='bottom' if offset>0 else 'top', color=C_DIM, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.15', facecolor=C_BG, edgecolor='none'))

    def draw_dim_v(y1, y2, x_ref, offset, text, text_pos='right'):
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
    # VIEW 1: 正视图 (FRONT VIEW) - Positioned at (270, 520)
    # Scale: 1mm = 1.15 units
    # =========================================================================
    S = 1.15
    fx0, fy0 = 265, 530
    cw, ch = 352 * S, 176 * S  # 404.8, 202.4
    fl, fb = fx0 - cw/2, fy0 - ch/2

    ax.text(fx0, fy0 + ch/2 + 58, "正视图 (主视图 / FRONT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(fx0, fy0 + ch/2 + 45, "外壳总宽 352mm × 高 176mm | 8路KEF蠕动泵外置直通安装", fontsize=8, ha='center', color='#64748B')

    # Chassis Outer Box with rounded corners
    box = FancyBboxPatch((fl, fb), cw, ch, boxstyle=f"round,pad=0,rounding_size={14*S}",
                         facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(box)

    # 4 Foot pads at bottom
    for foot_x in [fl + 28*S, fl + (352-28)*S]:
        ax.add_patch(Rectangle((foot_x - 10*S, fb - 6*S), 20*S, 6*S, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.2))

    # Front Panel (338 x 162 mm)
    pw, ph = 338 * S, 162 * S
    pl, pb = fx0 - pw/2, fy0 - ph/2
    panel_box = FancyBboxPatch((pl, pb), pw, ph, boxstyle=f"round,pad=0,rounding_size={10*S}",
                               facecolor='#FFFFFF', edgecolor='#475569', linewidth=1.2)
    ax.add_patch(panel_box)

    # 4 Corner panel mounting screws (M3)
    for scx in [fx0 - 158*S, fx0 + 158*S]:
        for scy in [fy0 - 70*S, fy0 + 70*S]:
            ax.add_patch(Circle((scx, scy), 3.5*S/2, facecolor='#E2E8F0', edgecolor=C_OUTLINE, lw=0.9))
            ax.plot([scx - 3.5, scx + 3.5], [scy, scy], color='#64748B', lw=0.6)
            ax.plot([scx, scx], [scy - 3.5, scy + 3.5], color='#64748B', lw=0.6)

    # Internal Partition Wall indication (dashed)
    part_x = fx0 + (100 * S)
    ax.plot([part_x, part_x], [pb + 4*S, pb + ph - 4*S], color='#94A3B8', lw=1.0, linestyle='--')
    ax.text(part_x + 3, fy0 + 55*S, "隔离中隔板 X=+100", fontsize=7, color='#64748B', rotation=90)

    # 8 Pumps
    pump_xs_mm = [-128.0, -64.0, 0.0, 64.0]
    pump_ys_mm = [-30.0, 38.0]
    
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

    # Right Electronics Bay annotation
    elec_x0 = fx0 + 100*S + 4*S
    elec_w = (176 - 100)*S - 8*S
    ax.add_patch(Rectangle((elec_x0, fy0 - ch/2 + 8*S), elec_w, ch - 16*S, facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=0.7, linestyle=':'))
    ax.text(elec_x0 + elec_w/2, fy0 + 35, "内部电控仓", fontsize=8, color='#475569', ha='center', fontweight='bold')
    ax.text(elec_x0 + elec_w/2, fy0 + 22, "(8路继电器板", fontsize=7, color='#64748B', ha='center')
    ax.text(elec_x0 + elec_w/2, fy0 + 11, "MCU / 12V电源)", fontsize=7, color='#64748B', ha='center')

    # Front View Dimensions:
    p1_x = fx0 + pump_xs_mm[0]*S
    p2_x = fx0 + pump_xs_mm[1]*S
    p3_x = fx0 + pump_xs_mm[2]*S
    p4_x = fx0 + pump_xs_mm[3]*S
    p_bot_y = fy0 + pump_ys_mm[0]*S
    p_top_y = fy0 + pump_ys_mm[1]*S

    # Width dimensions (bottom)
    draw_dim_h(fl, fl + cw, fb, -32, "外壳总宽 352.0")
    draw_dim_h(pl, pl + pw, fb, -18, "前面板宽 338.0")
    # Horizontal pitch dimensions (top)
    draw_dim_h(p1_x, p2_x, fy0 + pump_ys_mm[1]*S + 45*S, 14, "列距 64.0")
    draw_dim_h(p1_x, p4_x, fy0 + pump_ys_mm[1]*S + 45*S, 28, "4泵总跨距 192.0")

    # Height dimensions (left)
    draw_dim_v(fb, fb + ch, fl, -22, "外壳总高 176.0")
    draw_dim_v(pb, pb + ph, fl, -10, "前面板高 162.0")
    draw_dim_v(p_bot_y, p_top_y, p1_x - 28*S, -10, "排距 68.0")

    # Pump callouts (leaders)
    ax.annotate("4× 面板安装螺钉\n(M3沉头孔距 316×140)", xy=(fx0 - 158*S, fy0 + 70*S), xytext=(fx0 - 158*S - 35, fy0 + 70*S + 18),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')
    ax.annotate("泵安装耳距 48.5\n(2×Φ3.2 M3螺丝孔)", xy=(p4_x - 24.25*S, p_top_y), xytext=(p4_x + 18*S, p_top_y - 20*S),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')
    ax.annotate("双宝塔嘴管距 13.0\n出液嘴高 22.0", xy=(p3_x + 6.5*S, p_top_y + 36*S), xytext=(p3_x + 18*S, p_top_y + 44*S),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')


    # =========================================================================
    # VIEW 2: 俯视图 (TOP VIEW) - Positioned at (265, 235)
    # Depth = 120 mm
    # =========================================================================
    tx0, ty0 = fx0, 230
    cd = 120 * S  # 138
    tl, tb = tx0 - cw/2, ty0 - cd/2

    ax.text(tx0, ty0 + cd/2 + 45, "俯视图 (顶面投影 / TOP VIEW)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(tx0, ty0 + cd/2 + 34, "展示机箱深度 120mm、泵头外凸 25.5mm 与电机深入内部结构", fontsize=8, ha='center', color='#64748B')

    # Chassis top outline
    top_box = FancyBboxPatch((tl, tb), cw, cd, boxstyle=f"round,pad=0,rounding_size={14*S}",
                            facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(top_box)

    # Front panel line at front surface (Z = 0)
    ax.plot([tl + 7*S, tl + cw - 7*S], [tb + cd, tb + cd], color='#334155', lw=2.0)

    # 4 Pumps sticking out from front face (Z > 0)
    pump_front_len = 25.5 * S
    motor_in_len = 52.5 * S
    
    for px_mm in pump_xs_mm:
        pcx = tx0 + px_mm * S
        # External pump head
        ax.add_patch(Rectangle((pcx - 37.5*S/2, tb + cd), 37.5*S, pump_front_len,
                               facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.1))
        # Nozzle tips
        ax.add_patch(Rectangle((pcx - 6.5*S - 1.8*S, tb + cd + 17*S), 3.6*S, 4*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.6))
        ax.add_patch(Rectangle((pcx + 6.5*S - 1.8*S, tb + cd + 17*S), 3.6*S, 4*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.6))
        
        # Internal motor & collar (hidden lines)
        ax.add_patch(Rectangle((pcx - 31.5*S/2, tb + cd - 11.5*S), 31.5*S, 11.5*S,
                               facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))
        ax.add_patch(Rectangle((pcx - 27.5*S/2, tb + cd - 52.5*S), 27.5*S, 41*S,
                               facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))
        # Centerlines
        ax.plot([pcx, pcx], [tb + cd + pump_front_len + 5, tb + cd - 58*S], color=C_CENTER, lw=0.5, linestyle='-.')

    # Internal partition wall at X = +100
    p_wall_x = tx0 + 100*S
    ax.plot([p_wall_x, p_wall_x], [tb + 4*S, tb + cd - 4*S], color='#94A3B8', lw=1.0, linestyle='--')
    ax.text(p_wall_x + 3, ty0 - 15, "隔板 X=+100", fontsize=7, color='#64748B', rotation=90)

    # Foot pads position indication (circles)
    for fx in [tl + 28*S, tl + (352-28)*S]:
        for fz in [tb + 25*S, tb + (120-25)*S]:
            ax.add_patch(Circle((fx, fz), 10*S, facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle=':'))

    # Top View Dimensions (Between Top View and Table)
    draw_dim_v(tb, tb + cd, tl + cw, 12, "外壳深度 120.0")
    draw_dim_v(tb + cd, tb + cd + pump_front_len, tl + cw, 12, "外凸 25.5")
    draw_dim_v(tb, tb + cd + pump_front_len, tl + cw, 24, "总深度 145.5")
    # Motor depth into box
    draw_dim_v(tb + cd - motor_in_len, tb + cd, p1_x - 20*S, -14, "电机深入 52.5")


    # =========================================================================
    # VIEW 3: 右侧视图 (RIGHT SIDE VIEW) - Positioned at (640, 530)
    # Width = 120 mm (depth of chassis), Height = 176 mm
    # =========================================================================
    sx0, sy0 = 640, fy0
    sl, sb = sx0 - cd/2, sy0 - ch/2

    ax.text(sx0 + pump_front_len/2, sy0 + ch/2 + 58, "右侧视图 (侧面投影 / RIGHT ELEVATION)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(sx0 + pump_front_len/2, sy0 + ch/2 + 45, "展示侧面通风散热孔、机箱深度与外凸泵头侧面轮廓", fontsize=8, ha='center', color='#64748B')

    # Side outer box
    side_box = FancyBboxPatch((sl, sb), cd, ch, boxstyle=f"round,pad=0,rounding_size={14*S}",
                             facecolor='#F8FAFC', edgecolor=C_OUTLINE, linewidth=2.0)
    ax.add_patch(side_box)

    # Foot pads at bottom
    for foot_z in [sl + 25*S, sl + (120-25)*S]:
        ax.add_patch(Rectangle((foot_z - 10*S, sb - 6*S), 20*S, 6*S, facecolor='#CBD5E1', edgecolor=C_OUTLINE, lw=1.2))

    # Right side ventilation slots (4 vertical slots: 2 upper, 2 lower)
    for v_z in [sl + (120-45)*S, sl + (120-28)*S]:
        ax.add_patch(Rectangle((v_z - 2.5*S, sy0 + 35*S - 16*S), 5*S, 32*S, facecolor='#64748B', edgecolor=C_OUTLINE, lw=0.7))
    for v_z in [sl + (120-45)*S, sl + (120-28)*S]:
        ax.add_patch(Rectangle((v_z - 2.5*S, sy0 - 35*S - 16*S), 5*S, 32*S, facecolor='#64748B', edgecolor=C_OUTLINE, lw=0.7))

    # DC 12V power jack on rear wall
    ax.add_patch(Rectangle((sl - 2*S, sy0 - 55*S - 6*S), 4*S, 12*S, facecolor='#475569', edgecolor=C_OUTLINE, lw=0.9))
    ax.text(sl - 5, sy0 - 55*S, "DC 12V", fontsize=6.5, color='#475569', ha='right', va='center')

    # External Pumps on front (sl + cd)
    for py_mm in pump_ys_mm:
        p_side_y = sy0 + py_mm * S
        # Flange
        ax.add_patch(Rectangle((sl + cd, p_side_y - 37.5*S/2), 4*S, 37.5*S, facecolor='#E2E8F0', edgecolor=C_PUMP_EDGE, lw=0.9))
        # Pump head
        ax.add_patch(Rectangle((sl + cd + 4*S, p_side_y - 37.5*S/2), 24*S, 37.5*S, facecolor='#334155', edgecolor=C_PUMP_EDGE, lw=1.1))
        # Top nozzle (upward)
        ax.add_patch(Rectangle((sl + cd + 21*S - 1.8*S, p_side_y + 18.75*S), 3.6*S, 22*S, facecolor='#94A3B8', edgecolor=C_OUTLINE, lw=0.7))
        # Motor hidden line inside
        ax.add_patch(Rectangle((sl + cd - 52.5*S, p_side_y - 27.5*S/2), 52.5*S, 27.5*S, facecolor='none', edgecolor=C_HIDDEN, lw=0.7, linestyle='--'))

    # Side View Dimensions:
    draw_dim_h(sl, sl + cd, sb, -20, "深度 120.0")
    draw_dim_h(sl + cd, sl + cd + pump_front_len, sb, -20, "外凸 25.5")
    draw_dim_v(sb, sb + ch, sl + cd + pump_front_len, 18, "高度 176.0")
    draw_dim_v(sb - 6*S, sb, sl, -16, "脚垫 6.0")

    ax.annotate("散热孔 4× (5×32mm)\n垂直对流通风", xy=(sl + (120-28)*S, sy0 + 35*S), xytext=(sl + 15*S, sy0 + 68*S),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.7), fontsize=7, color=C_DIM, fontweight='bold')


    # =========================================================================
    # VIEW 4: 3D 轴测透视图 (ISOMETRIC 3D RENDER) - Positioned at (970, 530)
    # Embed the actual rendered 3D CAD isometric preview image
    # =========================================================================
    ax.text(990, fy0 + ch/2 + 58, "三维轴测效果参考 (ISOMETRIC 3D CAD)", fontsize=11, fontweight='bold', ha='center', color=C_FRAME)
    ax.text(990, fy0 + ch/2 + 45, "Shapr3D 原生实体模型三维立体透视图", fontsize=8, ha='center', color='#64748B')

    try:
        iso_img_path = '/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/assembly_external_preview.png'
        iso_img = Image.open(iso_img_path)
        # Crop white margins if any
        # Place into axes at [820, fy0 - ch/2 - 10, 340, 240]
        ax.imshow(iso_img, extent=(820, 1160, fy0 - ch/2 - 10, fy0 + ch/2 + 35), zorder=10)
        ax.add_patch(Rectangle((820, fy0 - ch/2 - 10), 340, ch + 45, fill=False, edgecolor='#CBD5E1', lw=0.8))
    except Exception as e:
        print("Could not load iso image:", e)

    # =========================================================================
    # DESIGN FEATURES & PARAMETERS TABLE (Bottom Center & Right)
    # =========================================================================
    card_x, card_y = 500, 290
    ax.text(670, 310, "核心设计特征与参数核对表 (DESIGN PARAMETERS & BOM)", fontsize=10.5, fontweight='bold', ha='center', color=C_FRAME)

    table_data = [
        ("部件 / 特征名称", "设计尺寸 (mm)", "结构说明与配合关系"),
        ("整机外形尺寸", "352.0 × 176.0 × 120.0", "长×高×深，壁厚 4.0mm，四角 R14 大圆角过渡，美观抗压"),
        ("8路蠕动泵排布", "两排 4+4 外置安装", "水平列距 64.0mm，垂直排距 68.0mm，耳部间隙 7.4mm，防碰干涉"),
        ("前面板安装板", "338.0 × 162.0 × 4.0", "平嵌于外壳前端；8×Φ33.0mm电机通孔 + 16×Φ3.2mm M3螺丝孔"),
        ("面板固定方式", "4× M3 沉头螺丝", "四角孔距 316.0 × 140.0mm，连接外壳 4 处角部增强圆柱螺丝柱"),
        ("机箱内部划分", "双仓隔离设计", "左侧 272mm 泵驱动电机仓；右侧 72mm 纯电控仓 (隔离隔板厚 4mm)"),
        ("后部电气配置", "竖置继电器 + 12V电源", "8路继电器板竖直布置；底部集成 12V 电源模块与主控 MCU"),
        ("通风散热通道", "4× (5.0 × 32.0mm) 竖槽", "右侧壁上下对流百叶槽，形成烟囱自对流散热，后壁留 Φ12mm DC孔"),
        ("底部防滑脚垫", "4× (Φ20.0 × 6.0mm)", "前后跨距 70.0mm，左右跨距 296.0mm，提供稳固台面支撑与防震")
    ]

    row_y = 285
    col_x = [490, 630, 800, 1160]
    for row_idx, row in enumerate(table_data):
        is_header = (row_idx == 0)
        bg_col = '#E2E8F0' if is_header else ('#F8FAFC' if row_idx % 2 == 1 else '#FFFFFF')
        ax.add_patch(Rectangle((col_x[0], row_y - 15), col_x[3] - col_x[0], 15,
                               facecolor=bg_col, edgecolor='#CBD5E1', lw=0.6))
        for col_idx in range(3):
            cell_text = row[col_idx]
            font_w = 'bold' if is_header else ('bold' if col_idx < 2 else 'normal')
            text_col = C_FRAME if is_header else ('#1E293B' if col_idx < 2 else '#475569')
            ax.text(col_x[col_idx] + 6, row_y - 8, cell_text, fontsize=7.2, va='center',
                    fontweight=font_w, color=text_col)
        row_y -= 15

    # =========================================================================
    # USER MODIFICATION CONFIRMATION GUIDE (Bottom Left)
    # =========================================================================
    note_box_x, note_box_y = 25, 25
    ax.add_patch(Rectangle((note_box_x, note_box_y), 450, 95, fill=True, facecolor='#FEF2F2', edgecolor='#FCA5A5', lw=1.2))
    ax.text(note_box_x + 10, note_box_y + 82, "请确认以下 5 个关键修改点 (CONFIRMATION CHECKLIST):", fontsize=8.5, fontweight='bold', color='#DC2626')
    
    questions = [
        "1. 泵列距 (目前 64mm，泵耳留隙 7.4mm): 是否需要调宽 (如 68~70mm，机箱会宽 15~20mm)？",
        "2. 外壳深度 (目前 120mm，电机后电控空间留 60mm): 电源/主板是否需要更薄/更深空间？",
        "3. 前面板固定: 目前为 4 颗角部螺丝固定，是否需要保留螺丝或改为卡扣/内嵌式？",
        "4. 右侧电控仓宽度 (目前 72mm): 现有 8路继电器板及 WiFi/MCU 是否足够容纳？",
        "5. 外露出液管线: 泵头外露直接插拔软管，是否需要在机箱前面板加装管卡或外接快速接头？"
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

    ax.text(tb_x + tb_w / 2, tb_y + 78, "8路蠕动泵一体机 (两排4+4外置安装方案)", fontsize=11.5, fontweight='bold', ha='center', va='center', color=C_FRAME)
    ax.text(tb_x + tb_w / 2, tb_y + 68, "总成工程设计草稿图 / 尺寸标注图 (CAD DRAFT)", fontsize=8, ha='center', va='center', color='#475569')
    
    ax.text(tb_x + 8, tb_y + 48, "图纸代号: KEF-8CH-CAD-01", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 48, "方案状态: 待用户确认修改", fontsize=7.5, fontweight='bold', va='center', color='#DC2626')
    ax.text(tb_x + 8, tb_y + 24, "比例: 1:2 (图示准比)", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 24, "单位: mm", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 280, tb_y + 24, "投影: 第三视角", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 8, tb_y + 8, "设计建模: Shapr3D / B-Rep", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 190, tb_y + 8, "日期: 2026-10-04", fontsize=7.5, va='center', color=C_TEXT)
    ax.text(tb_x + 280, tb_y + 8, "图幅: A3 标准图纸", fontsize=7.5, va='center', color=C_TEXT)

    out_path = "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/cad_blueprint_8ch_pump.png"
    plt.savefig(out_path, bbox_inches='tight', dpi=200, facecolor=C_BG)
    print("Perfect CAD Blueprint generated at:", out_path)

if __name__ == '__main__':
    draw_cad_sheet()
