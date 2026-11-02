"""Build the final report .docx from report.md (a small Markdown subset).

Supported: '# ', '## ', '### ' headings; '- ' bullets; '1. ' numbered items; paragraphs;
**bold** and *italic* inline; tables (a caption line 'Table ...' followed by '|' rows, first row
is the header); figures '![Figure caption](path)'; '<<PAGEBREAK>>'; '<<TOC>>'; lines starting
with '%' before the first heading form the title page.
    python build_report.py report.md Final_Report.docx
"""

import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Calibri"
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*)")


def add_inline(par, text, size=None, bold=False):
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            run = par.add_run(piece[2:-2])
            run.bold = True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            run = par.add_run(piece[1:-1])
            run.italic = True
        else:
            run = par.add_run(piece)
        if bold:
            run.bold = True
        if size:
            run.font.size = Pt(size)


def add_field(par, instr):
    run = par.add_run()
    for tag, text in (("begin", None), (None, instr), ("separate", None), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def new_list_num(doc, style_par):
    """Create a fresh numbering instance (restarting at 1) based on the List Number style."""
    numbering = doc.part.numbering_part.numbering_definitions._numbering
    num_pr = style_par.style.element.pPr.numPr
    base_num_id = num_pr.numId.val
    abstract_id = None
    for num in numbering.findall(qn("w:num")):
        if num.get(qn("w:numId")) == str(base_num_id):
            abstract_id = num.find(qn("w:abstractNumId")).get(qn("w:val"))
    new_id = max(int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))) + 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(new_id))
    an = OxmlElement("w:abstractNumId")
    an.set(qn("w:val"), abstract_id)
    num.append(an)
    ov = OxmlElement("w:lvlOverride")
    ov.set(qn("w:ilvl"), "0")
    so = OxmlElement("w:startOverride")
    so.set(qn("w:val"), "1")
    ov.append(so)
    num.append(ov)
    numbering.append(num)
    return new_id


def set_num(par, num_id):
    p_pr = par._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    nid = OxmlElement("w:numId")
    nid.set(qn("w:val"), str(num_id))
    num_pr.append(ilvl)
    num_pr.append(nid)
    p_pr.append(num_pr)


def shade(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def setup_styles(doc):
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    pf = st.paragraph_format
    pf.space_after = Pt(6)
    pf.line_spacing = 1.15
    for name, size, color in (("Heading 1", 16, "1F3864"), ("Heading 2", 13, "2F5496"),
                              ("Heading 3", 11.5, "2F5496")):
        h = doc.styles[name]
        h.font.name = FONT
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = RGBColor.from_string(color)
        h.element.rPr.rFonts.set(qn("w:asciiTheme"), "") if False else None
        rfonts = h.element.rPr.find(qn("w:rFonts"))
        if rfonts is not None:
            for k in list(rfonts.attrib):
                del rfonts.attrib[k]
            rfonts.set(qn("w:ascii"), FONT)
            rfonts.set(qn("w:hAnsi"), FONT)
        h.paragraph_format.space_before = Pt(14 if name == "Heading 1" else 10)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
    cap = doc.styles["Caption"]
    cap.font.name = FONT
    cap.font.size = Pt(9.5)
    cap.font.italic = False
    cap.font.bold = False
    cap.font.color.rgb = RGBColor(0x40, 0x40, 0x40)


def add_table(doc, caption, rows):
    cp = doc.add_paragraph(style="Caption")
    add_inline(cp, caption)
    cp.paragraph_format.keep_with_next = True
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    ncol = len(cells[0])
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(cells):
        for j in range(ncol):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            add_inline(p, row[j] if j < len(row) else "", size=9.5, bold=(i == 0))
            if i == 0:
                shade(cell, "D9E2F3")
    # repeat header row
    tr_pr = t.rows[0]._tr.get_or_add_trPr()
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    tr_pr.append(hdr)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def main(src, dst):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Cm(2.3))
    sec.top_margin = sec.bottom_margin = Cm(2.2)
    setup_styles(doc)

    lines = open(src, encoding="utf-8").read().splitlines()
    i = 0
    # title page
    title_lines = []
    while i < len(lines) and not lines[i].startswith("# "):
        if lines[i].startswith("%"):
            title_lines.append(lines[i][1:].strip())
        i += 1
    if title_lines:
        for _ in range(5):
            doc.add_paragraph()
        for k, tl in enumerate(title_lines):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(p, tl, size=22 if k == 0 else 12, bold=(k == 0))
            if k == 0:
                p.paragraph_format.space_after = Pt(24)
        p = doc.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)

    # footer page numbers
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(fp, "PAGE")

    numbered_restart = True
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            numbered_restart = True
            i += 1
            continue
        if s == "<<PAGEBREAK>>":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif s == "<<TOC>>":
            h = doc.add_paragraph()
            add_inline(h, "Contents", size=16, bold=True)
            add_field(doc.add_paragraph(), 'TOC \\o "1-2" \\h \\z \\u')
        elif s.startswith("### "):
            doc.add_heading(s[4:], level=3)
        elif s.startswith("## "):
            doc.add_heading(s[3:], level=2)
        elif s.startswith("# "):
            doc.add_heading(s[2:], level=1)
        elif s.startswith("!["):
            m = re.match(r"!\[(.*)\]\((.*)\)", s)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            img = os.path.join(os.path.dirname(os.path.abspath(src)), m.group(2))
            if os.path.exists(img):
                p.add_run().add_picture(img, width=Cm(15.5))
            else:
                p.add_run("[Figure pending: %s]" % m.group(2)).italic = True
            cp = doc.add_paragraph(style="Caption")
            add_inline(cp, m.group(1))
        elif re.match(r"^Table [A-Z]?\d+\.", s) and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            rows = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            add_table(doc, s, rows)
            i = j
            continue
        elif s.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, s[2:])
            p.paragraph_format.space_after = Pt(3)
        elif re.match(r"^\d+\. ", s):
            p = doc.add_paragraph(style="List Number")
            add_inline(p, re.sub(r"^\d+\. ", "", s))
            p.paragraph_format.space_after = Pt(3)
            if s.startswith("1. "):
                current_num = new_list_num(doc, p)
            set_num(p, current_num)
        elif s.startswith("> "):
            # hanging-indent reference entry
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-1.0)
            add_inline(p, s[2:])
        else:
            p = doc.add_paragraph()
            add_inline(p, s)
        numbered_restart = False
        i += 1

    # ask Word to refresh fields (TOC) on open
    settings = doc.settings.element
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings.append(upd)
    doc.save(dst)
    print("Saved", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
