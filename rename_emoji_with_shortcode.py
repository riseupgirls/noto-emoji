from nototools import unicode_data
import shutil
import pathlib
import os

import re
import unidecode

em_version = re.compile(r"^(\(emoji\) *)?E\d+(\.\d+)?")

new_to_old = {}

# this function is copied in generate_emoji_html
def shortcode(u_seq):
    n = unicode_data.get_emoji_sequence_name(u_seq)
    old = n
    n = unidecode.unidecode(n)
    n = re.sub(em_version, "", n)
    n = n.replace("(emoji)", "")
    n = n.lower().strip()
    n = n.replace("*", "star")
    n = n.replace(r"\x{23}", "number_sign")
    n = n.replace("'", "")
    n = n.replace("\"", "")
    n = n.replace(".", "_")
    n = n.replace("(", "")
    n = n.replace(")", "_")
    n = n.replace(": ", "_")
    n = n.replace(" & ", "_")
    n = n.replace(" - ", "_")
    n = n.replace("-", "_")
    n = n.replace(", ", "_")
    n = n.replace(" ", "_")
    n = n.replace("__", "_")
    if n in new_to_old:
        raise Exception("We already have a file named: {}, it points on: {}".format(n, new_to_old[n]))
    new_to_old[n] =old
    return n


source = pathlib.Path("./build/compressed_pngs/").absolute()
destination = pathlib.Path("./build/release/emoji").absolute()

rename = set()

for f in source.iterdir():
    if f.suffix != ".png":
        continue
    n = f.stem
    n = n.split("_")[1:]
    n[0] = n[0][1:]
    n = tuple([int(i, base=16) for i in n])
    n = shortcode(n)

    rename.add((f.absolute(), pathlib.Path(n)))

destination.mkdir(parents=True, exist_ok=True)
os.chdir(destination)

for source, dest_name in rename:
    dest = destination / dest_name
    dest = dest.with_suffix(".png")
    shutil.copy(source, destination)
    os.symlink(source.name, dest.name)
