from typing import *
import spacy
import json
from multiprocessing import Queue, Process
from threading import Thread
from tqdm import tqdm


def get_article(filepath: str, batch_size: int = 8):
    batch = []
    with open(filepath, "rt", encoding="utf8") as file:
        for line in file:
            article = json.loads(line)
            batch.append(article)
            
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

def process_section(section: Dict[str, Union[str, List[int]]], page_id2item_id: Dict):
    tokens = NLP(section["text"])
    token_offsets = [(token.idx, token.idx + len(token)) for token in tokens]
    tokens = [token.text for token in tokens]

    output = {"tokenized_text": tokens, "ner": [], "qids": {}}

    for offset, length, target_page_id in zip(section["link_offsets"], section["link_lengths"], section["target_page_ids"]):
        item_id = page_id2item_id.get(str(target_page_id), None)
        if item_id:
            char_start = offset
            char_end = offset + length

            token_start = None
            token_end = None
            for i, (token_start_idx, token_end_idx) in enumerate(token_offsets):
                if token_start is None and token_start_idx >= char_start:
                    token_start = i
                if token_end_idx > char_end:
                    token_end = i
                    break
            if token_start is not None and token_end is not None:
                output["ner"].append((token_start, token_end, item_id))
                if not output["qids"].get(item_id, None):
                    output["qids"][item_id] = True
                # print(f"({output['tokenized_text'][token_start:token_end]}, {item_id})")

    return output


def process_article(article: Dict, queue: Queue, page_id2item_id: Dict):
    for section in article["sections"]:
        queue.put(process_section(section, page_id2item_id=page_id2item_id))


def paralelize(articles: List[Dict], page_id2item_id: Dict):
    queue = Queue()
    threads = [Thread(target=process_article, args=(article, queue, page_id2item_id)) for article in articles]

    for thread in threads:
        thread.daemon = True
        thread.start()

    [thread.join() for thread in threads]

    results = []

    while not queue.empty():
        results.append(queue.get())

    return results

def write_line(line: str, filepath: str):
    with open(filepath, "a", encoding="utf8") as file:
        file.write(line + "\n")


if __name__ == "__main__":
    NLP = spacy.blank("en")

    base_path = r"E:\Knowledgator\text-classification-datasets\wiki_ner\raw"
    page_id2item_id = json.load(open(base_path + r"\page_id2item_id.json"))
    out_path = "dataset_5m.jsonl"
    batch_size = 8

    cur = 0
    total = int(5e6)  

    with tqdm(total=total, desc="Processing Sections", unit="section") as pbar:
        for batch in get_article(base_path + r"\link_annotated_text.jsonl", batch_size=batch_size):
            results = paralelize(batch, page_id2item_id=page_id2item_id)
            
            for res in results:
                write_line(json.dumps(res, ensure_ascii=False), out_path)

            pbar.update(len(results))  
            
            cur += len(results)
            if cur >= total:
                break

    print(f"Processed {cur} sections and saved to {out_path}")
