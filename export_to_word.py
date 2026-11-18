# -*- coding: utf-8 -*-
"""
Exporter script: Converts PROJECT_REPORT_60_PAGES.md to a beautifully styled
Microsoft Word document (CampusGrid_MCA_Practical_Report.docx).
Includes official university logo, cover page, certificate, declaration,
tables, styled code blocks, and academic typography.
"""
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, "PROJECT_REPORT_60_PAGES.md")
LOGO_FILE = os.path.join(BASE_DIR, "university_logo.jpeg")
OUTPUT_DOCX = os.path.join(BASE_DIR, "CampusGrid_MCA_Practical_Report.docx")
OUTPUT_DOCX_ALT = os.path.join(BASE_DIR, "PROJECT_REPORT_60_PAGES.docx")

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding for a table cell in twips."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    """Applies clean borders to a table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def add_page_number_to_section(section):
    """Adds page numbering to footer."""
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("CampusGrid Practical Report | Page ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.font.italic = True
    run.font.color.rgb = RGBColor(120, 120, 120)

    # XML for dynamic Page field
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    p._p.append(fldSimple)

def build_docx():
    print(f">> Reading markdown from: {MD_FILE}")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()

    # Configure Margins (1 inch everywhere)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        add_page_number_to_section(section)

    # Normal Style configuration
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # 1. BUILD COVER PAGE
    # -------------------------------------------------------------
    print(">> Generating Cover Page...")
    if os.path.exists(LOGO_FILE):
        logo_p = doc.add_paragraph()
        logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        logo_p.paragraph_format.space_before = Pt(0)
        logo_p.paragraph_format.space_after = Pt(12)
        logo_p.add_run().add_picture(LOGO_FILE, width=Inches(5.0))
    else:
        p_univ = doc.add_paragraph()
        p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_univ.add_run("KRISTU JAYANTI (DEEMED TO BE UNIVERSITY)\nBENGALURU, INDIA\n")
        r.bold = True
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(12, 35, 64)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(18)
    p_proj.paragraph_format.space_after = Pt(8)
    r_sub = p_proj.add_run("Project-based Practical Report on\n")
    r_sub.font.size = Pt(14)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(70, 70, 70)

    r_title = p_proj.add_run("“CAMPUSGRID: INTELLIGENT CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM”\n")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(12, 35, 64)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(12)
    p_req.paragraph_format.space_after = Pt(12)
    r_req = p_req.add_run(
        "Submitted in partial fulfilment of the requirements for\n"
        "“Data Structures and Algorithms Lab” for the 1st Semester\n"
        "Master of Computer Applications (MCA)\n"
    )
    r_req.font.size = Pt(13)
    r_req.font.color.rgb = RGBColor(40, 40, 40)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(24)
    p_subm.paragraph_format.space_after = Pt(6)
    r_subm = p_subm.add_run("Submitted by\n")
    r_subm.font.size = Pt(13)
    r_subm.font.bold = True

    # Candidate table for clean alignment
    cand_tbl = doc.add_table(rows=1, cols=2)
    cand_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cand_tbl.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cand_tbl.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = cand_tbl.rows[0].cells[0].paragraphs[0].add_run("<Candidate Name>")
    r_c1.bold = True
    r_c1.font.size = Pt(13)
    r_c2 = cand_tbl.rows[0].cells[1].paragraphs[0].add_run("<Candidate Reg. no.>")
    r_c2.bold = True
    r_c2.font.size = Pt(13)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(28)
    p_guide.paragraph_format.space_after = Pt(4)
    r_gu = p_guide.add_run("Under the guidance of\n")
    r_gu.font.size = Pt(13)
    r_gu.font.italic = True

    p_gname = doc.add_paragraph()
    p_gname.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gname.paragraph_format.space_before = Pt(2)
    p_gname.paragraph_format.space_after = Pt(24)
    r_gn = p_gname.add_run("<Guide Name>\n")
    r_gn.bold = True
    r_gn.font.size = Pt(14)
    r_gn.font.color.rgb = RGBColor(12, 35, 64)
    r_gd = p_gname.add_run("Department of Computer Applications\nKristu Jayanti (Deemed to be University), Bengaluru")
    r_gd.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PARSE AND RENDER MARKDOWN BODY
    # -------------------------------------------------------------
    print(">> Parsing Markdown document...")
    lines = md_text.splitlines()

    # Skip initial front matter from markdown since we custom generated the cover
    start_idx = 0
    for idx, line in enumerate(lines):
        if "## CERTIFICATE OF ORIGINALITY & APPROVAL" in line:
            start_idx = idx
            break

    in_code_block = False
    code_lines = []
    code_lang = ""

    in_table = False
    table_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            return
        
        # Parse table rows
        rows_data = []
        for tline in table_lines:
            clean = tline.strip()
            if not clean.startswith("|") or "---" in clean:
                continue
            cols = [c.strip() for c in clean.split("|")[1:-1]]
            if cols:
                rows_data.append(cols)

        if rows_data:
            num_rows = len(rows_data)
            num_cols = max(len(r) for r in rows_data)
            tbl = doc.add_table(rows=num_rows, cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(tbl)

            for r_idx, row in enumerate(rows_data):
                is_header = (r_idx == 0)
                for c_idx in range(num_cols):
                    cell = tbl.rows[r_idx].cells[c_idx]
                    cell_text = row[c_idx] if c_idx < len(row) else ""
                    # strip markdown bold or formatting inside cell
                    cell_text = cell_text.replace("**", "").replace("`", "")
                    cell.paragraphs[0].text = cell_text
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
                    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

                    run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run()
                    run.font.name = "Times New Roman"
                    if is_header:
                        set_cell_background(cell, "0C2340")
                        run.font.bold = True
                        run.font.size = Pt(10.5)
                        run.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        run.font.size = Pt(10)
                        if r_idx % 2 == 1:
                            set_cell_background(cell, "F8F9FA")
                        else:
                            set_cell_background(cell, "FFFFFF")

            # Space after table
            sp_p = doc.add_paragraph()
            sp_p.paragraph_format.space_before = Pt(0)
            sp_p.paragraph_format.space_after = Pt(8)

        in_table = False
        table_lines = []

    def flush_code_block():
        nonlocal in_code_block, code_lines, code_lang
        if not code_lines:
            in_code_block = False
            return
        
        full_code = "\n".join(code_lines)
        code_tbl = doc.add_table(rows=1, cols=1)
        code_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = code_tbl.rows[0].cells[0]
        set_cell_background(cell, "F4F5F7")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        # Border
        set_table_borders(code_tbl, color="D0D5DD", sz="6", val="single")

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(0)
        cp.paragraph_format.line_spacing = 1.05
        
        run = cp.add_run(full_code)
        run.font.name = "Consolas"
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(33, 37, 41)

        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(6)

        in_code_block = False
        code_lines = []
        code_lang = ""

    i = start_idx
    total_lines = len(lines)
    while i < total_lines:
        line = lines[i]
        stripped = line.strip()

        # Handle fenced code block
        if stripped.startswith("```"):
            if in_code_block:
                flush_code_block()
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Handle Markdown Table
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            i += 1
            continue
        elif in_table:
            flush_table()

        # Handle page breaks
        if stripped in ["---", "<br>", "<br><br>", "<br><br><br>"]:
            # If line is --- preceded or followed by major section, we can ignore or add subtle space
            i += 1
            continue

        # Headings
        if stripped.startswith("# "):
            heading_text = stripped[2:].strip()
            # If major chapter heading, add page break
            if any(heading_text.startswith(x) for x in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "CERTIFICATE", "DECLARATION", "ACKNOWLEDGMENTS", "TABLE OF CONTENTS"]):
                doc.add_page_break()

            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(16)
            h.paragraph_format.space_after = Pt(8)
            h.paragraph_format.keep_with_next = True
            run = h.add_run(heading_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(16.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(12, 35, 64)
            i += 1
            continue

        if stripped.startswith("## "):
            heading_text = stripped[3:].strip()
            if any(heading_text.startswith(x) for x in ["CERTIFICATE", "DECLARATION", "ACKNOWLEDGMENTS", "TABLE OF CONTENTS"]):
                doc.add_page_break()

            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(6)
            h.paragraph_format.keep_with_next = True
            run = h.add_run(heading_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 78, 121)
            i += 1
            continue

        if stripped.startswith("### "):
            heading_text = stripped[4:].strip()
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
            h.paragraph_format.keep_with_next = True
            run = h.add_run(heading_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(46, 91, 130)
            i += 1
            continue

        if stripped.startswith("#### "):
            heading_text = stripped[5:].strip()
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(3)
            h.paragraph_format.keep_with_next = True
            run = h.add_run(heading_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.italic = True
            run.font.color.rgb = RGBColor(60, 60, 60)
            i += 1
            continue

        # Bullet lists
        if stripped.startswith("- ") or stripped.startswith("* "):
            item_text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            _format_inline_markdown(p, item_text)
            i += 1
            continue

        # Numbered lists (e.g. "1. ")
        num_match = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if num_match:
            item_text = num_match.group(2)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            _format_inline_markdown(p, item_text)
            i += 1
            continue

        # Normal Paragraph
        if stripped:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.2
            _format_inline_markdown(p, stripped)

        i += 1

    if in_table:
        flush_table()
    if in_code_block:
        flush_code_block()

    print(f">> Saving Word Document to: {OUTPUT_DOCX}")
    doc.save(OUTPUT_DOCX)
    print(f">> Saving copy to: {OUTPUT_DOCX_ALT}")
    doc.save(OUTPUT_DOCX_ALT)
    print(">> EXPORT TO WORD FILE COMPLETE!")

def _format_inline_markdown(paragraph, text):
    """Parses bold, italic, inline code, and math tokens into runs."""
    # Split by bold (**text**)
    parts = re.split(r'(\*\*.*?\*\*|\`.*?\`|\$.*?\$)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(180, 40, 40)
        elif part.startswith("$") and part.endswith("$"):
            # Math notation
            clean_math = part[1:-1].replace(r"\le", "≤").replace(r"\ge", "≥").replace(r"\neq", "≠").replace(r"\forall", "∀").replace(r"\in", "∈").replace(r"\times", "×").replace(r"\approx", "≈").replace(r"\cdot", "·").replace(r"\land", "∧").replace(r"\lor", "∨")
            run = paragraph.add_run(clean_math)
            run.font.name = "Cambria Math"
            run.font.size = Pt(11.5)
            run.font.italic = True
        else:
            run = paragraph.add_run(part)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

if __name__ == "__main__":
    build_docx()

