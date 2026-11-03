try:
    import openpyxl
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openpyxl>=3.1.0"])
    import openpyxl

from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def xl_color(css_hex):
    value = css_hex.removeprefix("#").upper()
    return "FF" + value

XL_HEADER_BG = xl_color("#4472C4")
XL_HEADER_FONT = xl_color("#FFFFFF")
XL_LIGHT_BG = xl_color("#D9E2F3")
XL_BORDER = xl_color("#BFBFBF")
XL_ACCENT = xl_color("#2F5597")

thin = Side(style="thin", color=XL_BORDER)
border_all = Border(top=thin, bottom=thin, left=thin, right=thin)

wb = openpyxl.Workbook()
wb.properties.title = "游戏制作人招聘 - 投递记录"

ws = wb.active
ws.title = "投递记录"

# Column headers
headers = [
    "序号", "提交时间", "类型", "推荐人姓名", "推荐人手机号",
    "候选人姓名", "候选人手机号", "作品链接", "推荐理由",
    "简历文件", "处理状态", "备注"
]

header_font = Font(name="PingFang SC", size=11, bold=True, color=XL_HEADER_FONT)
header_fill = PatternFill(start_color=XL_HEADER_BG, end_color=XL_HEADER_BG, fill_type="solid")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
    cell.border = border_all

# Column widths
widths = [6, 20, 10, 14, 16, 14, 16, 30, 30, 20, 12, 30]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Data validation for 类型 and 处理状态
from openpyxl.worksheet.datavalidation import DataValidation

type_dv = DataValidation(type="list", formula1='"推荐朋友,自荐"', allow_blank=True)
type_dv.error = "请选择有效类型"
type_dv.errorTitle = "输入错误"
ws.add_data_validation(type_dv)
type_dv.add(f"C2:C1000")

status_dv = DataValidation(type="list", formula1='"待处理,已联系,面试中,已录用,未通过"', allow_blank=True)
status_dv.error = "请选择有效状态"
ws.add_data_validation(status_dv)
status_dv.add(f"K2:K1000")

# Freeze header row
ws.freeze_panes = "A2"

# Auto filter
ws.auto_filter.ref = f"A1:L1"

# Add 5 empty rows with formatting
data_font = Font(name="PingFang SC", size=10)
data_align = Alignment(vertical="center", wrap_text=True)
light_fill = PatternFill(start_color=XL_LIGHT_BG, end_color=XL_LIGHT_BG, fill_type="solid")

for row in range(2, 7):
    for col in range(1, 13):
        cell = ws.cell(row=row, column=col)
        cell.font = data_font
        cell.alignment = data_align
        cell.border = border_all
    # Alternate row color
    if row % 2 == 0:
        for col in range(1, 13):
            ws.cell(row=row, column=col).fill = light_fill

# Row height for header
ws.row_dimensions[1].height = 30

# Second sheet: 说明
ws2 = wb.create_sheet("说明")
ws2["A1"] = "游戏制作人（AI 方向）招聘 - 投递记录表"
ws2["A1"].font = Font(name="PingFang SC", size=14, bold=True)
ws2["A3"] = "字段说明："
ws2["A3"].font = Font(name="PingFang SC", size=11, bold=True)

instructions = [
    ["序号", "自动编号"],
    ["提交时间", "候选人提交表单的时间"],
    ["类型", "推荐朋友 / 自荐"],
    ["推荐人姓名", "填写表单的人的姓名"],
    ["推荐人手机号", "填写表单的人的手机号（用于发放推荐奖励）"],
    ["候选人姓名", "被推荐人的姓名（自荐时填自己）"],
    ["候选人手机号", "被推荐人的手机号"],
    ["作品链接", "候选人最满意的作品链接"],
    ["推荐理由", "推荐人填写的一句话推荐理由"],
    ["简历文件", "候选人上传的简历文件名"],
    ["处理状态", "待处理 / 已联系 / 面试中 / 已录用 / 未通过"],
    ["备注", "HR 内部备注"],
]

for i, (field, desc) in enumerate(instructions, 4):
    ws2.cell(row=i, column=1, value=field).font = Font(name="PingFang SC", size=10, bold=True)
    ws2.cell(row=i, column=2, value=desc).font = Font(name="PingFang SC", size=10)

ws2.column_dimensions["A"].width = 16
ws2.column_dimensions["B"].width = 50

output_path = "/Users/xiaogengdemac/WorkBuddy/2026-10-30-17-18-23/referral-page/投递记录表.xlsx"
wb.save(output_path)
print(f"Saved to {output_path}")
