import os
import json

stories_m2 = r"c:\Coding_Notebook\Projects\school\room-math-story\stories\중2"
stories_m3 = r"c:\Coding_Notebook\Projects\school\room-math-story\stories\중3"

data = {}

for folder in [stories_m2, stories_m3]:
    if os.path.exists(folder):
        for f in sorted(os.listdir(folder)):
            if f.endswith(".txt"):
                with open(os.path.join(folder, f), 'r', encoding='utf-8') as file:
                    data[os.path.join(os.path.basename(folder), f)] = file.readline().strip()

with open(r"c:\Coding_Notebook\Projects\school\room-math-story\titles.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=4)
