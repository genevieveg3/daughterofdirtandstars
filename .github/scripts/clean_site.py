import json, os, re, shutil, subprocess, sys

SRC = "mirror/daughterofdirtandstars.com"
OUT = "site"
SITE = "https://daughterofdirtandstars.com"

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(SRC, OUT)

# id -> path for ?p= shortlinks
idmap = {}
for f in ("pg.json", "ps.json"):
    for item in json.load(open(f)):
        idmap[str(item["id"])] = item["link"].replace(SITE, "") or "/"

# 1. rename versioned asset files (styles.css@ver=1.7.css -> styles.css)
for root, _, files in os.walk(OUT):
    for name in files:
        if "@ver=" in name:
            new = name.split("@ver=")[0]
            os.rename(os.path.join(root, name), os.path.join(root, new))
extra = os.path.join(OUT, "contact", "index.html@reason=speaking.html")
if os.path.exists(extra):
    os.remove(extra)

REMOVE_TAGS = [
    r'<link rel="alternate" title="oEmbed[^>]*>\s*',
    r'<link rel="https://api\.w\.org/"[^>]*>\s*',
    r'<link rel="alternate" title="JSON"[^>]*>\s*',
    r'<link rel="EditURI"[^>]*>\s*',
    r'<meta name="generator"[^>]*>\s*',
    r"<link rel='shortlink'[^>]*>\s*",
    r'<script[^>]*id="wp-emoji-settings"[^>]*>.*?</script>\s*',
    r'<script[^>]*>[^<]*wp-emoji[^<]*</script>\s*',
    r'<script type="module">[^<]*wp-emoji[^<]*</script>\s*',
    r"<style id='wp-emoji-styles-inline-css'>.*?</style>\s*",
]

missing_remote = set()

def fix_url(u, depth):
    # absolute site URL -> root-relative
    if u.startswith(SITE):
        u = u[len(SITE):] or "/"
        if u.startswith(("/wp-content/", "/wp-includes/")):
            path = u.split("?")[0]
            missing_remote.add(path)
            u = path
    u = re.sub(r"index\.html@p=(\d+)\.html", lambda m: idmap.get(m.group(1), "/"), u)
    u = u.replace("index.html@reason=speaking.html", "?reason=speaking")
    u = re.sub(r"(\.(?:css|js|png|jpe?g|webp|svg|woff2?))@ver=[^\"'\s,]*?(?:\.css)?$", r"\1", u)
    u = re.sub(r"@ver=[^\"'\s,]*$", "", u)
    return u

def fix_attr(m):
    attr, q, val = m.group(1), m.group(2), m.group(3)
    if attr == "srcset":
        parts = []
        for p in val.split(","):
            bits = p.strip().split(" ", 1)
            bits[0] = fix_url(bits[0], 0)
            parts.append(" ".join(bits))
        val = ", ".join(parts)
    else:
        val = fix_url(val, 0)
    return f"{attr}={q}{val}{q}"

for root, _, files in os.walk(OUT):
    for name in files:
        if not name.endswith(".html"):
            continue
        p = os.path.join(root, name)
        rel = os.path.relpath(p, OUT)
        page_path = "/" + (os.path.dirname(rel) + "/" if os.path.dirname(rel) else "")
        h = open(p, encoding="utf-8").read()
        for pat in REMOVE_TAGS:
            h = re.sub(pat, "", h, flags=re.S)
        h = re.sub(r'<link rel="canonical" href="[^"]*" />',
                   f'<link rel="canonical" href="{SITE}{page_path}" />', h)
        h = re.sub(r'\b(href|src|srcset|action)=(["\'])(.*?)\2', fix_attr, h)
        open(p, "w", encoding="utf-8").write(h)

# fetch any assets still only referenced remotely
for path in sorted(missing_remote):
    dest = OUT + path
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        r = subprocess.run(["curl", "-sSf", "-o", dest, SITE + path])
        print("fetched" if r.returncode == 0 else "FAILED", path)

open(os.path.join(OUT, "CNAME"), "w").write("daughterofdirtandstars.com\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")

# second-pass cleanup
for root, _, files in os.walk(OUT):
    for name in files:
        if not name.endswith(".html"):
            continue
        p = os.path.join(root, name)
        h = open(p, encoding="utf-8").read()
        h = re.sub(r'<style id="wp-emoji-styles-inline-css">.*?</style>\s*', '', h, flags=re.S)
        h = re.sub(r'<script type="module">(?:(?!</script>).)*wp-emoji(?:(?!</script>).)*</script>\s*', '', h, flags=re.S)
        h = re.sub(r'<link rel="alternate" type="application/rss\+xml"[^>]*>\s*', '', h)
        open(p, "w", encoding="utf-8").write(h)
print("cleanup done")

