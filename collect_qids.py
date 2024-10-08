import struct
import os
import json
from tqdm import tqdm

def get_line(filepath: str):
    with open(filepath, "rt", encoding="utf8") as file:
        for line in file:
            article = json.loads(line)
            yield list(article["qids"].keys())
              
def read_offsets(filename):
    offset_size = struct.calcsize('q')
    file_size = os.path.getsize(filename)

    if file_size % offset_size != 0:
        raise ValueError("Invalid file format, size is not a multiple of offset size")

    offsets = []

    with open(filename, 'rb') as f:
        while True:
            data = f.read(offset_size)
            if not data:
                break
            (offset,) = struct.unpack('q', data)
            offsets.append(offset)
    return offsets

def get_line_at_offset(text_file, offset):
    with open(text_file, 'rb') as f:
        f.seek(offset)
        line_bytes = b''
        while True:
            c = f.read(1)
            if not c or c == b'\n':
                break
            line_bytes += c
        line = line_bytes.decode('utf-8')
    return line

offsets = read_offsets('latest-all.bin')

print("Total ids: ", len(offsets))
qids_dict = {}
qid2line = json.load(open("qid2line.json", "rt", encoding="utf8"))

#qids_dict = json.load(open("target_ontology_100k.json", "rt", encoding="utf8"))

i = 0
for qids in tqdm(get_line("dataset_1m.jsonl"), total=1000000):
    i += 1
    if i ==1000999:
       break
    for qid in qids:
        if qids_dict.get(qid, None):
            continue
        try:
            index = qid2line.get(f"Q{qid}")
            offset = offsets[index]
            line = json.loads(get_line_at_offset('latest-all.json', offset)[:-1])
            qids_dict[f"{qid}"] = {"label": line["labels"]["en"]["value"], "desc": line["descriptions"]["en"]["value"]}
        except Exception:
            qids_dict[f"{qid}"] = None

with open("target_ontology_1m.json", "wt", encoding="utf8") as file:
        json.dump(qids_dict, file, indent=4)