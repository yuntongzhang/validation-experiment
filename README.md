Dataset used for patch validation speed experiment.

Scripts:
- prepare_dataset.py: Collect inputs and patches in raw (fuzzrepair) format.
- collect_translated_patches: After translating raw patches in individual containers, this script
    collects them and store them here.

How to use:
- python3 scripts/prepare_dataset.py --meta scripts/meta-data.json --patch-dst patches --input-dst inputs --src /home/yuntong/fuzzrepair-results-sep-05-original-repetition/
- Now run special mode in the validation run.py script (from other repo) 
- Do not delete the containers containing translated patches.
- python3 scripts/collect_translated_patches.py --meta scripts/meta-data.json
