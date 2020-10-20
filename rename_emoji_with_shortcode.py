from nototools import unicode_data
import shutil
import pathlib

import re
import unidecode

em_version = re.compile(r"^(\(emoji\) *)?E\d+(\.\d+)?")


# this function is copied in generate_emoji_html
def shortcode(u_seq):
    n = unicode_data.get_emoji_sequence_name(u_seq)
    n = unidecode.unidecode(n)
    n = re.sub(em_version, "", n)
    n = n.replace("(emoji)", "")
    n = n.lower().strip()
    n = n.replace("*", "star")
    n = n.replace(r"\x{23}", "number_sign")
    n = n.replace("'", "")
    n = n.replace("(", "")
    n = n.replace(")", "_")
    n = n.replace(": ", "_")
    n = n.replace(" & ", "_")
    n = n.replace(" - ", "_")
    n = n.replace("-", "_")
    n = n.replace(", ", "_")
    n = n.replace(" ", "_")
    n = n.replace("__", "_")
    return n


source = pathlib.Path("./build/compressed_pngs/")
destination = pathlib.Path("./build/compressed_pngs-named/")


rename = set()

for f in source.iterdir():
    if f.suffix != ".png":
        continue
    n = f.stem
    n = n.split("_")[1:]
    n[0] = n[0][1:]
    n = tuple([int(i, base=16) for i in n])
    n = shortcode(n)

    rename.add((f, n))

destination.mkdir(exist_ok=True)
for source, dest_name in rename:
    dest = destination / dest_name
    dest = dest.with_suffix(".png")

    shutil.copy(source, dest)
