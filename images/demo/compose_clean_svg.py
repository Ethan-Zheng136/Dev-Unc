import svgutils.transform as sg

# ===== 输入路径 =====
left_svgs = ["left_top.svg", "left_middle.svg", "left_bottom.svg"]
right_svgs = ["a.svg", "b.svg", "c.svg", "d.svg", "e.svg"]
labels = [
    "(a) Baseline",
    "(b) Previous Uncertainty",
    "(c) Covariance-based Uncertainty",
    "(d) Proprioceptive Classifier",
    "(e) Ours"
]

# ===== 布局参数（自动布局 + 间隔）=====
margin = 20
gap = 10

# 加载右侧 SVG 获取单图尺寸（取第一张）
first_right = sg.fromfile(right_svgs[0])
first_size = first_right.get_size()
right_w, right_h = int(first_size[0].replace("pt", "")), int(first_size[1].replace("pt", ""))

# 设置左图尺寸（等高竖排）
left_w = right_w
left_h = right_h // 3

# 整体图像大小
canvas_width = margin * 3 + left_w + len(right_svgs) * (right_w + gap) - gap
canvas_height = margin * 2 + right_h

# 创建 SVG 画布
fig = sg.SVGFigure(str(canvas_width), str(canvas_height))
elements = []

# 拼接左侧 3 张图（竖排）
for i, svg_path in enumerate(left_svgs):
    svg = sg.fromfile(svg_path)
    root = svg.getroot()
    root.moveto(margin, margin + i * left_h)
    elements.append(root)

# 拼接右侧 5 张图（横排）
for j, svg_path in enumerate(right_svgs):
    svg = sg.fromfile(svg_path)
    root = svg.getroot()
    x_offset = margin * 2 + left_w + j * (right_w + gap)
    root.moveto(x_offset, margin)
    elements.append(root)

    # 添加文字标签
    label = sg.TextElement(x_offset + 5, margin + right_h - 5, labels[j], size=10, font="Arial")
    elements.append(label)

# 合并所有元素
fig.append(elements)
fig.save("final_output.svg")
print("✅ 已生成：final_output.svg")
