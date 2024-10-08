"# WikiDataProcessing" 

1. Firstly a raw dataset should be prepared:
```comandline
python prepare_raw_dataset.py
```
2. Then, WikiData JSON lines file should be indexes:
```comandline
indexing "latest-all.json" "latest-all.bin"
```
3. Then, Qid2Line dictionary should be created:
```comandline
create_qid2line "latest-all.json" "qid2line.json"
```
4. Finally, qid are collected with "collect_qids.py".
