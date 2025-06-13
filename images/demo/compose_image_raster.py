from PIL import Image, ImageDraw, ImageFont
import cairosvg
import os


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


# final_width = 1079     # 最终图像宽度
# final_height = 421     # 最终图像高度

# left_width = 280       # 左边区域宽度（三张 JPG 共用）
# left_height = 140      # 每张 JPG 的高度

# right_width = 160      # 每张 SVG 图像的宽度
# right_height = 140     # 每张 SVG 图像的高度

# label_y_offset = 130   # 文字标签的纵坐标

canvas = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))

for i, jpg in enumerate(jpgs):
    if not os.path.exists(jpg):
        raise FileNotFoundError(f"找不到文件：{jpg}")
    img = Image.open(jpg).resize((left_width, left_height))
    canvas.paste(img, (0, i * left_height))

for j, svg in enumerate(svgs):
    if not os.path.exists(svg):
        raise FileNotFoundError(f"找不到文件：{svg}")

    png_path = f"temp_svg_{j}.png"
    cairosvg.svg2png(url=svg, write_to=png_path, output_width=right_width, output_height=right_height)
    svg_img = Image.open(png_path)
    canvas.paste(svg_img, (left_width + j * right_width, 0))

    draw = ImageDraw.Draw(canvas)
    draw.text((left_width + j * right_width + 5, label_y_offset), labels[j], fill=(0, 0, 0))

canvas.save("final_output.png")
print("已保存:final_output.png")
