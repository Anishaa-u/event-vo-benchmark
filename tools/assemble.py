"""Join the report parts, fill {{PLACEHOLDERS}} from fill.json, report the word count of the body
(excluding title page, references and appendices, as the brief requires), and build the .docx.
    python assemble.py            -> report.md, Final_Report_Anisha_Uddin.docx
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ["part1_front.md", "part2_method.md", "part3_findings.md", "part3b_discussion.md", "part4_end.md"]


def main():
    text = "\n\n".join(open(os.path.join(HERE, p), encoding="utf-8").read() for p in PARTS)
    fill_path = os.path.join(HERE, "fill.json")
    fill = json.load(open(fill_path, encoding="utf-8")) if os.path.exists(fill_path) else {}
    for k, v in fill.items():
        text = text.replace("{{" + k + "}}", v)
    left = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
    text = re.sub(r"\{\{([A-Z0-9_]+)\}\}", r"[PENDING: \1]", text)
    open(os.path.join(HERE, "report.md"), "w", encoding="utf-8").write(text)

    body = text.split("# Abstract", 1)[1].split("# References", 1)[0]
    body = re.sub(r"<<[A-Z]+>>|!\[.*?\]\(.*?\)", "", body)
    body_words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.,'%()/-]*", body))
    print(f"Body words (abstract to conclusion and Section 7, excl. references/appendices): {body_words}")
    if left:
        print("Unfilled placeholders:", ", ".join(left))
    out = os.path.join(HERE, "Final_Report_Anisha_Uddin.docx")
    subprocess.run([sys.executable, os.path.join(HERE, "build_report.py"), os.path.join(HERE, "report.md"), out],
                   check=True)


if __name__ == "__main__":
    main()
