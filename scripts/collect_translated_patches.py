import argparse
import json
import os
from os.path import join as pjoin
from tqdm import tqdm


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(script_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta", required=True, help="Path to the meta file.")
    args = parser.parse_args()
    meta_file = args.meta

    with open(meta_file, "r") as f:
        meta_data = json.load(f)

    for meta_entry in tqdm(meta_data):
        id = int(meta_entry["id"])
        if id in [9, 10]:  # two bugs that could not be reproduced
            continue
        bug_id = meta_entry["bug_id"]
        subject = meta_entry["subject"]
        
        bug_id_lower = bug_id.lower()
        subject_lower = subject.lower()
        container = f"vulnloc-fuzzrepairvalidate-{subject_lower}-{bug_id}-TP1-CP1-0"

        # get the container up
        os.system(f"docker start {container}")
        
        # copy patches out
        os.system(f"docker cp {container}:/data/validatation_dataset/patches/{bug_id}/unix_patches {root_dir}/patches/{bug_id}/unix_patches")

        os.system(f"docker stop {container}")

        # also remove the trialing part in fix file
        unix_patch_dir = pjoin(root_dir, "patches", bug_id, "unix_patches")
        for patch_file in os.listdir(unix_patch_dir):
            full_path = pjoin(unix_patch_dir, patch_file)
            with open(full_path, "r") as f:
                lines = f.readlines()
            lines[1] = lines[1].replace(".updated", "")
            with open(full_path, "w") as f:
                f.writelines(lines)


if __name__ == "__main__":
    main()
