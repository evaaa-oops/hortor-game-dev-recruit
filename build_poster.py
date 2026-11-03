try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'Pillow'])
    from PIL import Image, ImageDraw, ImageFont

import qrcode

# === Fonts ===
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
def fz(size):
    return ImageFont.truetype(FONT_PATH, size)

# === Colors ===
BG = (8, 8, 20)
WHITE = (255, 255, 255)
DIM_WHITE = (200, 200, 210)
GRAY = (120, 120, 135)
LIGHT_GRAY = (80, 80, 95)
CYAN = (0, 212, 255)
CYAN_DIM = (0, 160, 200)
CARD_BG = (18, 18, 38)
CARD_BORDER = (35, 35, 65)
DIVIDER = (30, 30, 55)
GREEN = (0, 200, 100)
RED_DIM = (180, 70, 70)

# === Canvas ===
W, H = 1080, 2350
img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# === Top gradient glow ===
for i in range(300):
    ratio = i / 300
    r = int(8 + 10 * (1 - ratio))
    g = int(8 + 30 * (1 - ratio))
    b = int(20 + 60 * (1 - ratio))
    draw.line([(0, i), (W, i)], fill=(r, g, b))

# === Decorative top line ===
draw.line([(340, 55), (740, 55)], fill=CYAN_DIM, width=2)

# === Title ===
y = 120
draw.text((W//2, y), "用 AI 做过游戏？", fill=WHITE, font=fz(56), anchor="mt")
y += 76
draw.text((W//2, y), "我们找的就是你！", fill=WHITE, font=fz(56), anchor="mt")

# === Subtitle ===
y += 90
draw.text((W//2, y), "有已上线作品？来主导新项目，我们兜底发行", fill=GRAY, font=fz(30), anchor="mt")

# === Badge ===
y += 72
badge_text = "推荐成功入职 · 推荐人得 ¥10,000"
bbox = draw.textbbox((0, 0), badge_text, font=fz(32))
bw = bbox[2] - bbox[0] + 80
bh = 60
bx = (W - bw) // 2
draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=30, fill=GREEN)
draw.text((W//2, y + bh//2 + 1), badge_text, fill=WHITE, font=fz(32), anchor="mm")

y += 78
draw.text((W//2, y), "入职当日发放 · 不拖不套路", fill=LIGHT_GRAY, font=fz(24), anchor="mt")

# === Divider ===
y += 65
draw.line([(100, y), (980, y)], fill=DIVIDER, width=1)

# === Section: 岗位核心亮点 ===
y += 55
draw.rounded_rectangle([(100, y+2), (104, y+36)], radius=2, fill=CYAN)
draw.text((120, y), "岗位核心亮点", fill=WHITE, font=fz(38))

y += 62

# Use simple text labels instead of emoji
highlights = [
    ("01", "用 AI 开发游戏，不是嘴上说说", "Cursor、Claude、各种 AI 全配\n迭代周期从「周」压到「小时」"),
    ("02", "方向你定，不层层审批", "游戏玩法、题材，完全自主决策\n给你资源和试错空间"),
    ("03", "发行通道现成", "买量+发行团队就位\n好 Demo 直接进通道，你只需专注创作"),
    ("04", "无上限奖金", "底薪 + 项目分红 + 升星激励\n游戏做成功，你就能分到"),
]

for num, title, desc in highlights:
    card_y = y
    card_h = 130
    draw.rounded_rectangle([(80, card_y), (1000, card_y + card_h)], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)
    
    # Number badge
    draw.rounded_rectangle([(108, card_y + 18), (148, card_y + 58)], radius=8, fill=CYAN_DIM)
    draw.text((128, card_y + 38), num, fill=WHITE, font=fz(22), anchor="mm")
    
    # Title
    draw.text((168, card_y + 16), title, fill=WHITE, font=fz(32))
    
    # Description lines
    desc_y = card_y + 56
    for line in desc.split('\n'):
        draw.text((168, desc_y), line, fill=GRAY, font=fz(24))
        desc_y += 30
    
    y = card_y + card_h + 14

# === Divider ===
y += 25
draw.line([(100, y), (980, y)], fill=DIVIDER, width=1)

# === Section: 我们希望你 ===
y += 55
draw.rounded_rectangle([(100, y+2), (104, y+36)], radius=2, fill=CYAN)
draw.text((120, y), "我们希望你", fill=WHITE, font=fz(38))

y += 65

requirements = [
    ("✓", "深度使用 AI", "策划、美术、程序、调优，AI 贯穿每一个环节"),
    ("✓", "有已上线作品", "Steam / TapTap / itch / 微信 / 抖音都行"),
    ("✗", "不需要赚到钱", "有上线作品就行，不要求爆款"),
    ("✗", "拒绝伪 AI 使用", "我们要的是把 AI 融入全流程的创作者"),
]

for icon, title, desc in requirements:
    icon_color = CYAN if icon == "✓" else RED_DIM
    # Icon circle
    draw.ellipse([(100, y+2), (128, y+30)], fill=icon_color)
    draw.text((114, y+16), icon, fill=WHITE, font=fz(18), anchor="mm")
    
    draw.text((148, y), title, fill=WHITE, font=fz(32))
    draw.text((148, y + 40), desc, fill=GRAY, font=fz(24))
    y += 88

# === Divider ===
y += 25
draw.line([(100, y), (980, y)], fill=DIVIDER, width=1)

# === QR Code Section ===
y += 65

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=8, border=2)
qr.add_data('https://evaaa-oops.github.io/hortor-game-dev-recruit/')
qr.make(fit=True)
qr_img = qr.make_image(fill_color='#080814', back_color='#ffffff')
qr_size = 260
qr_img = qr_img.resize((qr_size, qr_size))

# QR code - white rounded card
qr_x = (W - qr_size) // 2
qr_y = y
qr_pad = 18
draw.rounded_rectangle([(qr_x - qr_pad, qr_y - qr_pad), (qr_x + qr_size + qr_pad, qr_y + qr_size + qr_pad)], radius=18, fill=WHITE)
img.paste(qr_img, (qr_x, qr_y))

# Text below QR
y = qr_y + qr_size + 42
draw.text((W//2, y), "长按识别，直接投递", fill=WHITE, font=fz(34), anchor="mt")

y += 52
draw.text((W//2, y), "疯狂游戏（豪腾系）", fill=GRAY, font=fz(26), anchor="mt")

y += 36
draw.text((W//2, y), "HR 耿叶", fill=LIGHT_GRAY, font=fz(22), anchor="mt")
y += 32
draw.text((W//2, y), "gengye@hortorgames.com", fill=LIGHT_GRAY, font=fz(22), anchor="mt")

# === Bottom decorative line ===
draw.line([(340, H - 55), (740, H - 55)], fill=CYAN_DIM, width=2)

# === Save ===
output = "/Users/xiaogengdemac/WorkBuddy/2026-10-30-17-18-23/referral-page/poster.png"
img.save(output, "PNG", quality=95)
print(f"Poster saved: {output} ({W}x{H})")
