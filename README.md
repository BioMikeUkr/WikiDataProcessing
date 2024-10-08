## WikiData downloading:
```commandline
wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.gz
```
or
```commandline
aria2c --max-connection-per-server 16 https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.gz
```
## Processing
1. Firstly a raw dataset should be prepared:
```commandline
python prepare_raw_dataset.py
```
2. Then, WikiData JSON lines file should be indexed:
```commandline
./indexing "latest-all.json" "latest-all.bin"
```
3. Then, Qid2Line dictionary should be created:
```commandline
./create_qid2line "latest-all.json" "qid2line.json"
```
4. Finally, qids are collected with "collect_qids.py".
