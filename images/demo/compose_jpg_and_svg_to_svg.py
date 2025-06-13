import svgutils.transform as sg
from PIL import Image

# ==== 输入路径 ====
# jpgs = [
#     "top.jpg",      # 顶部图像
#     "middle.jpg",   # 中部图像
#     "bottom.jpg"    # 底部图像
# ]

# svgs = [
#     "a.svg",  # Baseline
#     "b.svg",  # Previous Uncertainty
#     "c.svg",  # Covariance-based Uncertainty
#     "d.svg",  # Proprioceptive Classifier
#     "e.svg"   # Ours
# ]
jpgs = [
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/n015-2018-07-18-11-41-49+0800__CAM_FRONT_RIGHT__1531885798520339.jpg",      # 顶部图片
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/n015-2018-07-18-11-41-49+0800__CAM_FRONT__1531885798512465.jpg",   # 中间图片
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/n015-2018-07-18-11-41-49+0800__CAM_FRONT_LEFT__1531885798504844.jpg"    # 底部图片
]

svgs = [
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/7_13_base.svg",  # (a) Baseline
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/7_13_unc.svg",  # (b) Previous Uncertainty
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/7_13_cov.svg",  # (c) Covariance-based Uncertainty
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/7_13_sc.svg",  # (d) Proprioceptive Classifier
    "/Volumes/Insane/DingXianYou/ShenYou_Gu/Project/MapTR_Uncertainty/teaser/teaser1/7-13/7_13_cosc.svg",  # (e) Ours
]


labels = [
    "(a) Baseline",
    "(b) Previous Uncertainty",
    "(c) Covariance-based Uncertainty",
    "(d) Proprioceptive Classifier",
    "(e) Ours"
]

# ==== 布局参数 ====
margin = 20
gap = 10
label_fontsize = 10

# ==== 将 JPG 转为 SVG <image> ====
jpg_svgs = []
for i, jpg_path in enumerate(jpgs):
    img = Image.open(jpg_path)
    width, height = img.size
    svg_text = '<?xml version="1.0" standalone="no"?>\n'
    svg_text += f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
    svg_text += f'  <image href="{jpg_path}" width="{width}" height="{height}"/>\n'
    svg_text += '</svg>'
    temp_svg_path = f"temp_left_{i}.svg"
    with open(temp_svg_path, "w") as f:
        f.write(svg_text)
    jpg_svgs.append(temp_svg_path)

# ==== 获取右侧 SVG 尺寸 ====
first_right = sg.fromfile(svgs[0])
right_w, right_h = map(lambda x: int(x.replace("pt", "")), first_right.get_size())

left_w = right_w
left_h = right_h // 3

canvas_width = margin * 3 + left_w + len(svgs) * (right_w + gap) - gap
canvas_height = margin * 2 + right_h

fig = sg.SVGFigure(str(canvas_width), str(canvas_height))
elements = []

# ==== 左侧拼 JPG 转 SVG（竖排）====
for i, svg_path in enumerate(jpg_svgs):
    svg = sg.fromfile(svg_path)
    root = svg.getroot()
    root.moveto(margin, margin + i * left_h)
    elements.append(root)

# ==== 右侧拼 SVG（横排）====
for j, svg_path in enumerate(svgs):
    svg = sg.fromfile(svg_path)
    root = svg.getroot()
    x_offset = margin * 2 + left_w + j * (right_w + gap)
    root.moveto(x_offset, margin)
    elements.append(root)

    # 注解标签
    label = sg.TextElement(x_offset + 5, margin + right_h - 5, labels[j], size=label_fontsize, font="Arial")
    elements.append(label)

fig.append(elements)
fig.save("final_output.svg")
print("✅ 已保存：final_output.svg")
