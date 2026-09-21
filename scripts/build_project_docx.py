#!/usr/bin/env python3
from copy import deepcopy
from pathlib import Path
import re
import subprocess

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "01_project_book" / "1nm晶圆IPD量测设备_整机项目书.md"
OUT = ROOT / "01_project_book" / "1nm晶圆IPD量测设备_整机项目书_V2.0.docx"
BUILD = ROOT / ".docx_build"
REFERENCE = BUILD / "reference.docx"
TEMP = BUILD / "project_raw.docx"

BODY_FONT = "Noto Sans CJK SC"
LATIN_FONT = "Times New Roman"
BLUE = "1F4E79"
LIGHT_BLUE = "D9EAF7"
PALE_BLUE = "EEF5FA"
GRAY = "666666"

FIGURES = [
    (ROOT / "03_figures" / "fig01_scope.png", 15.2),
    (ROOT / "03_figures" / "fig02_coordinate_chain.png", 15.2),
    (ROOT / "03_figures" / "fig03_wafer_sampling.png", 11.2),
    (ROOT / "03_figures" / "fig04_system_architecture.png", 15.2),
    (ROOT / "03_figures" / "fig05_error_budget.png", 15.0),
    (ROOT / "03_figures" / "fig06_motion_metrology.png", 15.2),
    (ROOT / "03_figures" / "fig07_fit_residual.png", 15.0),
    (ROOT / "03_figures" / "fig08_timing.png", 15.0),
    (ROOT / "03_figures" / "fig09_validation_ladder.png", 14.8),
]

# Static page numbers make the directory useful in PDF/preview software that does
# not refresh Word fields. They are updated after the final pagination audit.
TOC_PAGES = {
    "项目摘要": "ii", "插图清单": "iv", "符号与缩略语": "v",
    "第一章  项目背景与应用需求": "1", "第二章  测量原理与性能定义": "4",
    "第三章  系统总体设计": "8", "第四章  整机误差预算": "11",
    "第五章  精密运动与位置计量": "14", "第六章  静电卡盘与面形补偿": "17",
    "第七章  隔振系统与结构稳定性": "18", "第八章  深紫外显微成像": "19",
    "第九章  狭缝式自动对焦": "21", "第十章  图形定位与IPD解算": "22",
    "第十一章  环境控制与漂移补偿": "24", "第十二章  测量节拍与数据处理": "25",
    "第十三章  系统标定与性能验证": "27", "结论与实施建议": "30",
    "参考文献": "31", "附录A  设计输入与冻结口径": "32",
    "附录B  顶层主张与证据闭环": "33", "附录C  数据记录最小集合": "34",
    "附录D  风险与阶段交付": "35",
}


def set_run_font(run, east=BODY_FONT, latin=LATIN_FONT, size=None, bold=None, color=None):
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), east)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_style_font(style, east=BODY_FONT, latin=LATIN_FONT, size=10.5, bold=False, color="000000"):
    style.font.name = latin
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = RGBColor.from_string(color)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), east)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = tcpr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcpr.append(shd)
    shd.set(qn("w:fill"), fill)


def cant_split(row):
    trpr = row._tr.get_or_add_trPr()
    trpr.append(OxmlElement("w:cantSplit"))


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    trpr.append(tbl_header)


def set_cell_margins(cell, top=70, start=90, bottom=70, end=90):
    tc = cell._tc
    tcpr = tc.get_or_add_tcPr()
    tc_mar = tcpr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tcpr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def add_page_field(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char1, instr, fld_char2])
    set_run_font(run, size=9, color=GRAY)


def toc_paragraph():
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    p.append(ppr)
    r = OxmlElement("w:r")
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "目录将在打开文档时更新"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r.extend([begin, instr, sep, text, end])
    p.append(r)
    return p


def heading_xml(text, level=1):
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    pstyle = OxmlElement("w:pStyle")
    pstyle.set(qn("w:val"), f"Heading{level}")
    ppr.append(pstyle)
    p.append(ppr)
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def configure_reference():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Mm(25)
    sec.bottom_margin = Mm(25)
    sec.left_margin = Mm(25)
    sec.right_margin = Mm(25)
    sec.header_distance = Mm(12)
    sec.footer_distance = Mm(12)
    sec.different_first_page_header_footer = True

    normal = doc.styles["Normal"]
    set_style_font(normal, size=10.5)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.first_line_indent = Pt(21)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    normal.paragraph_format.line_spacing = Pt(20)
    normal.paragraph_format.space_after = Pt(0)

    for name in ("Body Text", "First Paragraph"):
        if name in doc.styles:
            set_style_font(doc.styles[name], size=10.5)
            doc.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            doc.styles[name].paragraph_format.first_line_indent = Pt(21)
            doc.styles[name].paragraph_format.line_spacing = Pt(20)
            doc.styles[name].paragraph_format.space_after = Pt(0)

    title = doc.styles["Title"]
    set_style_font(title, size=26, bold=True, color="000000")
    title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(95)
    title.paragraph_format.space_after = Pt(18)

    subtitle = doc.styles["Subtitle"]
    set_style_font(subtitle, size=16, bold=False, color=BLUE)
    subtitle.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(42)

    for level, size, before, after in ((1,18,16,18),(2,15,16,8),(3,12,12,6)):
        st = doc.styles[f"Heading {level}"]
        set_style_font(st, size=size, bold=True, color="000000")
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.keep_together = True
        if level == 1:
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            st.paragraph_format.page_break_before = True
        else:
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for name in ("Author", "Date"):
        if name in doc.styles:
            set_style_font(doc.styles[name], size=11, color=GRAY)
            doc.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if "Caption" in doc.styles:
        cap = doc.styles["Caption"]
        set_style_font(cap, size=9, color="000000")
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.first_line_indent = Pt(0)
        cap.paragraph_format.space_before = Pt(4)
        cap.paragraph_format.space_after = Pt(8)

    for name in ("Table", "Table Caption"):
        if name in doc.styles:
            set_style_font(doc.styles[name], size=9)

    doc.add_paragraph("reference")
    doc.save(REFERENCE)


def insert_toc(doc):
    target = next((p for p in doc.paragraphs if p.text.strip() == "插图清单"), None)
    if target is None:
        raise RuntimeError("cannot locate 插图清单")
    entries = [
        "项目摘要", "插图清单", "符号与缩略语",
        "第一章  项目背景与应用需求", "第二章  测量原理与性能定义",
        "第三章  系统总体设计", "第四章  整机误差预算",
        "第五章  精密运动与位置计量", "第六章  静电卡盘与面形补偿",
        "第七章  隔振系统与结构稳定性", "第八章  深紫外显微成像",
        "第九章  狭缝式自动对焦", "第十章  图形定位与IPD解算",
        "第十一章  环境控制与漂移补偿", "第十二章  测量节拍与数据处理",
        "第十三章  系统标定与性能验证", "结论与实施建议", "参考文献",
        "附录A  设计输入与冻结口径", "附录B  顶层主张与证据闭环",
        "附录C  数据记录最小集合", "附录D  风险与阶段交付",
    ]
    # Insert the title first; subsequent insert-before operations keep it ahead
    # of all entries when the entries themselves are added in reverse order.
    target._p.addprevious(heading_xml("目录", 1))
    for text in entries:
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:after"), "80")
        ppr.append(spacing)
        tabs = OxmlElement("w:tabs")
        tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "right")
        tab.set(qn("w:leader"), "dot")
        tab.set(qn("w:pos"), "9000")
        tabs.append(tab)
        ppr.append(tabs)
        p.append(ppr)
        r = OxmlElement("w:r")
        t = OxmlElement("w:t")
        t.text = text
        tab_run = OxmlElement("w:tab")
        page = OxmlElement("w:t")
        page.text = TOC_PAGES[text]
        r.extend([t, tab_run, page])
        p.append(r)
        target._p.addprevious(p)


def add_front_section_break(doc):
    first_chapter = next((p for p in doc.paragraphs if p.text.strip() == "第一章 项目背景与应用需求"), None)
    if first_chapter is None:
        raise RuntimeError("cannot locate first chapter")
    body_sect = doc._element.body.sectPr
    sect_copy = deepcopy(body_sect)
    # A dedicated empty paragraph immediately before chapter 1 keeps the whole
    # symbols table in the Roman-numbered front matter. doc.paragraphs omits
    # table content, so attaching the break to the previous visible paragraph
    # would incorrectly start Arabic numbering inside that table.
    break_p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    ppr.append(sect_copy)
    break_p.append(ppr)
    first_chapter._p.addprevious(break_p)
    pgnum = sect_copy.find(qn("w:pgNumType"))
    if pgnum is None:
        pgnum = OxmlElement("w:pgNumType")
        sect_copy.append(pgnum)
    pgnum.set(qn("w:fmt"), "lowerRoman")
    pgnum.set(qn("w:start"), "1")
    body_pgnum = body_sect.find(qn("w:pgNumType"))
    if body_pgnum is None:
        body_pgnum = OxmlElement("w:pgNumType")
        body_sect.append(body_pgnum)
    body_pgnum.set(qn("w:fmt"), "decimal")
    body_pgnum.set(qn("w:start"), "1")
    # The section break already starts a new page; suppress the Heading 1
    # page-break override here so chapter 1 is body page 1, not body page 2.
    first_chapter.paragraph_format.page_break_before = False


def style_document(doc):
    normal = doc.styles["Normal"]
    set_style_font(normal, size=10.5)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.first_line_indent = Pt(21)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    normal.paragraph_format.line_spacing = Pt(20)
    normal.paragraph_format.space_after = Pt(0)
    for level, size, before, after in ((1,18,16,18),(2,15,16,8),(3,12,12,6)):
        st = next(s for s in doc.styles if s.style_id == f"Heading{level}")
        set_style_font(st, size=size, bold=True, color="000000")
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.keep_together = True
        if level == 1:
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            st.paragraph_format.page_break_before = True
        else:
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for name, size, color in (("Title",26,"000000"),("Subtitle",16,BLUE)):
        if name in doc.styles:
            set_style_font(doc.styles[name], size=size, bold=(name == "Title"), color=color)
            doc.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if "Title" in doc.styles:
        doc.styles["Title"].paragraph_format.space_before = Pt(95)
        doc.styles["Title"].paragraph_format.space_after = Pt(18)
    if "Subtitle" in doc.styles:
        doc.styles["Subtitle"].paragraph_format.space_after = Pt(42)
    if "Caption" in doc.styles:
        set_style_font(doc.styles["Caption"], size=9)
        doc.styles["Caption"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.styles["Caption"].paragraph_format.first_line_indent = Pt(0)
    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(25)
        section.bottom_margin = Mm(25)
        section.left_margin = Mm(25)
        section.right_margin = Mm(25)
        section.header_distance = Mm(12)
        section.footer_distance = Mm(12)

    # Cover is the first page of the front section.
    doc.sections[0].different_first_page_header_footer = True

    for section in doc.sections:
        header = section.header
        header.is_linked_to_previous = False
        hp = header.paragraphs[0]
        hp.text = "1 nm级晶圆图案位置与IPD量测设备项目书  |  V2.0"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for r in hp.runs:
            set_run_font(r, size=8.5, color=GRAY)
        footer = section.footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0]
        fp.clear()
        add_page_field(fp)

    for p in doc.paragraphs:
        if p.style and p.style.name in ("Normal", "Body Text", "First Paragraph"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Pt(21)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            p.paragraph_format.line_spacing = Pt(20)
            p.paragraph_format.space_after = Pt(0)
        if p.text.strip().startswith("关键词："):
            p.paragraph_format.first_line_indent = Pt(0)
        if p.text.strip() == "项目组" or re.fullmatch(r"2026年9月", p.text.strip()):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.text.strip().startswith("图") and re.match(r"图\d+-\d+", p.text.strip()):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Pt(0)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_run_font(r, size=9)
        if any(run._element.xpath('.//w:drawing') for run in p.runs):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Pt(0)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.line_spacing = 1
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True

        for r in p.runs:
            if not r._element.xpath('.//m:oMath'):
                set_run_font(r, size=r.font.size.pt if r.font.size else None)

    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        if table.rows:
            repeat_header(table.rows[0])
        for ri, row in enumerate(table.rows):
            cant_split(row)
            for cell in row.cells:
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                set_cell_margins(cell)
                if ri == 0:
                    shade(cell, BLUE)
                elif ri % 2 == 0:
                    shade(cell, PALE_BLUE)
                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent = Pt(0)
                    p.paragraph_format.line_spacing = Pt(14)
                    p.paragraph_format.space_after = Pt(0)
                    for r in p.runs:
                        set_run_font(r, size=8.5, bold=(ri == 0), color=("FFFFFF" if ri == 0 else "000000"))

    # Pandoc's percentage widths are not interpreted consistently by office
    # renderers. Lock every inline figure to a known physical width and retain
    # its source aspect ratio so diagrams cannot collapse into a thin strip.
    if len(doc.inline_shapes) != len(FIGURES):
        raise RuntimeError(
            f"expected {len(FIGURES)} inline figures, found {len(doc.inline_shapes)}"
        )
    for shape, (image_path, width_cm) in zip(doc.inline_shapes, FIGURES):
        with Image.open(image_path) as im:
            pixel_width, pixel_height = im.size
        shape.width = Cm(width_cm)
        shape.height = int(shape.width * pixel_height / pixel_width)

    # Ensure Word updates TOC and fields on open.
    settings = doc.settings._element
    update = settings.find(qn("w:updateFields"))
    if update is None:
        update = OxmlElement("w:updateFields")
        settings.append(update)
    update.set(qn("w:val"), "true")


def main():
    BUILD.mkdir(exist_ok=True)
    cmd = [
        "pandoc", str(SOURCE), "-o", str(TEMP),
        "--standalone",
        "--resource-path", str(ROOT),
        "--from", "markdown+tex_math_dollars+link_attributes+implicit_figures",
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    doc = Document(TEMP)
    insert_toc(doc)
    add_front_section_break(doc)
    doc.save(TEMP)
    doc = Document(TEMP)
    style_document(doc)
    doc.core_properties.title = "1 nm级晶圆图案位置与IPD量测设备项目书"
    doc.core_properties.subject = "整机方案论证、误差预算与验证基线"
    doc.core_properties.comments = "基于当前技术基线、写作基线和证据树生成；工程分配不等同实测结论。"
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
