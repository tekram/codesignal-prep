import markdown
from weasyprint import HTML

with open("CHEATSHEET.md", "r") as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: 'DejaVu Sans', Arial, sans-serif;
    font-size: 11px;
    line-height: 1.5;
    margin: 15mm 15mm 15mm 15mm;
    color: #111;
  }}
  h1 {{ font-size: 18px; border-bottom: 2px solid #333; padding-bottom: 4px; margin-top: 0; }}
  h2 {{ font-size: 14px; border-bottom: 1px solid #aaa; padding-bottom: 2px; margin-top: 18px; color: #222; }}
  h3 {{ font-size: 12px; margin-top: 12px; }}
  code {{
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 10px;
    background: #f4f4f4;
    padding: 1px 4px;
    border-radius: 3px;
  }}
  pre {{
    background: #f4f4f4;
    border-left: 3px solid #555;
    padding: 8px 10px;
    overflow-x: auto;
    margin: 6px 0;
  }}
  pre code {{
    background: none;
    padding: 0;
    font-size: 10px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0;
    font-size: 10px;
  }}
  th, td {{
    border: 1px solid #ccc;
    padding: 4px 8px;
    text-align: left;
  }}
  th {{ background: #eee; font-weight: bold; }}
  ul, ol {{ margin: 4px 0; padding-left: 20px; }}
  li {{ margin: 2px 0; }}
  hr {{ border: none; border-top: 1px solid #ccc; margin: 10px 0; }}
  p {{ margin: 4px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html).write_pdf("CHEATSHEET.pdf")
print("Done: CHEATSHEET.pdf")
