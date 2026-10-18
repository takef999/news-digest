#!/usr/bin/env python3
"""Turn a routine email body (cid: images) into a public web page in the news-digest site.
usage: make_page.py YYYY-MM-DD /path/to/body.html /path/to/img_dir
- copies imgN.jpg -> img/YYYY-MM-DD/imgN.jpg
- rewrites src="cid:imgN.jpg" -> src="img/YYYY-MM-DD/imgN.jpg"
- adds <title>, lazy loading, back link to index
- regenerates index.html (newest first)
"""
import sys, os, re, shutil, glob, datetime
site = os.path.dirname(os.path.abspath(__file__))
date, body, imgdir = sys.argv[1], sys.argv[2], sys.argv[3]
d = datetime.date.fromisoformat(date)
wd = "月火水木金土日"[d.weekday()]
label = f"{d.year}年{d.month}月{d.day}日（{wd}）"
out_img = os.path.join(site, "img", date); os.makedirs(out_img, exist_ok=True)
h = open(body, encoding="utf-8").read()
for f in glob.glob(os.path.join(imgdir, "*.jpg")):
    shutil.copy(f, out_img)
h = re.sub(r'src="cid:([^"]+)"', lambda m: f'src="img/{date}/{m.group(1)}" loading="lazy"', h)
head = (f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>朝のニュースまとめ {label}</title><meta name="robots" content="noindex">')
h = re.sub(r'<head>.*?</head>', f'<head>{head}</head>', h, count=1, flags=re.S)
nav = '<div style="max-width:640px;margin:0 auto;padding:10px 16px;font-size:13px;font-family:sans-serif;"><a href="./" style="color:#1a4fa0;">← 過去のまとめ一覧</a></div>'
h = h.replace('</body>', nav + '</body>', 1)
open(os.path.join(site, f"{date}.html"), "w", encoding="utf-8").write(h)
# index
pages = sorted((os.path.basename(p)[:-5] for p in glob.glob(os.path.join(site, "20??-??-??.html"))), reverse=True)
items = []
for p in pages:
    pd = datetime.date.fromisoformat(p)
    items.append(f'<li style="padding:12px 0;border-bottom:1px solid #e5e7eb;"><a href="{p}.html" style="color:#1a4fa0;text-decoration:none;font-size:17px;">{pd.year}年{pd.month}月{pd.day}日（{"月火水木金土日"[pd.weekday()]}）</a></li>')
idx = ('<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>朝のニュースまとめ</title><meta name="robots" content="noindex"></head>'
       '<body style="margin:0;background:#f2f3f5;font-family:-apple-system,BlinkMacSystemFont,\'Hiragino Sans\',\'Noto Sans JP\',sans-serif;">'
       '<div style="max-width:640px;margin:0 auto;background:#fff;min-height:100vh;">'
       '<div style="background:#1a2b4c;color:#fff;padding:20px 16px;font-size:22px;font-weight:bold;">朝のニュースまとめ</div>'
       '<ul style="list-style:none;margin:0;padding:0 16px;">' + "".join(items) + '</ul></div></body></html>')
open(os.path.join(site, "index.html"), "w", encoding="utf-8").write(idx)
open(os.path.join(site, ".nojekyll"), "w").close()
print("wrote", f"{date}.html", "and index.html;", len(pages), "pages")
