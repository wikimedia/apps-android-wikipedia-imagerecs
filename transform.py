import sys

# Dmitry Brant, Apr 2021

arg_id = 1

while arg_id < len(sys.argv):
    if "prod-" not in sys.argv[arg_id]:
        continue

    in_file = open(sys.argv[arg_id], encoding="utf-8")

    wiki_name = sys.argv[arg_id].split("-")[1]
    out_file = open(wiki_name + "_image_candidates.tsv", mode="w", encoding="utf-8")
    arg_id = arg_id + 1

    # remove headers
    line = in_file.readline()
    prev_pageid = -1
    source_str = ""
    prev_image = ""
    line_out = ""

    while True:
        line = in_file.readline()
        if not line:
            break

        line_arr = line.replace("\n", "").replace("\r", "").split("\t")

        if prev_pageid != int(line_arr[0]):
            # write out the previous line
            if len(line_out) > 0:
                out_file.write(line_out + source_str + "\n")

            line_out = ""
            source_str = ""
            prev_pageid = int(line_arr[0])
            prev_image = line_arr[2]

        source = line_arr[4]

        if len(line_out) == 0:
            line_out = line_arr[0] + "\t" + line_arr[2] + "\t"

        # add on new sources?
        if prev_image.replace("_", " ") == line_arr[2].replace("_", " "):
            if len(source_str) > 0:
                source_str += ","
            if source == "wikidata":
                source_str += "wd"
            elif source == "commons":
                source_str += "com"
            elif source == "wikipedia":
                source_str += line_arr[8].replace("wiki", "").replace("_min_nan", "")
            else:
                print(">>>>> " + source)

    # write out the last line
    if len(line_out) > 0:
        out_file.write(line_out + source_str + "\n")

    in_file.close()
