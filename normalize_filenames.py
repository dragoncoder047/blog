import glob
import datetime
import html
import os
import string
import re

os.chdir("markdown/")

files = glob.glob("*.md")

dates = {}
draft_dates = {}


def slugify(s: str):
    return re.sub(fr"[\s{re.escape(string.punctuation)}]+", "_",
                  html.unescape(s).lower()).strip("_")


for file in files:
    date = None
    is_draft = False
    title = ""
    with open(file) as f:
        for line in f:
            lLine = line.lower().strip()
            if lLine.startswith("date:"):
                date = datetime.date.fromisoformat(
                    lLine.removeprefix("date:").strip())
            if lLine == "status: draft":
                is_draft = True
            if lLine.startswith("title:"):
                title = line[6:].strip()
    if not date:
        continue
    if is_draft:
        draft_dates[file] = (date, slugify(title))
    else:
        dates[file] = (date, slugify(title))

old2new = {n: f"{i+1:04d}_{t}.md" for i, (n, (d, t)) in
           enumerate(sorted(dates.items(),
                            key=lambda file: dates[file[0]][0]))}
old2new_drafts = {n: f"draft_{i+1:04d}_{t}.md" for i, (n, (d, t)) in
                  enumerate(sorted(draft_dates.items(),
                                   key=lambda file: draft_dates[file[0]][0]))}

for a, b in sorted((old2new | old2new_drafts).items()):
    os.rename(a, b)
