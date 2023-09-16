import argparse
import json
import os
from os.path import join as pjoin
from tqdm import tqdm


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(script_dir)


def collect_unix_patches_helper(container, bug_id, patch_dir_name):
    local_dst_dir = f"{root_dir}/patches/{bug_id}/{patch_dir_name}"
    if os.path.exists(local_dst_dir):
        return

    # get the container up
    os.system(f"docker start {container}")
    # copy patches out
    os.system(f"docker cp {container}:/data/validatation_dataset/patches/{bug_id}/{patch_dir_name} {local_dst_dir}")
    # stop the container
    os.system(f"docker stop {container}")

    # also remove the trialing part in fix file
    unix_patch_dir = pjoin(root_dir, "patches", bug_id, patch_dir_name)
    for patch_file in os.listdir(unix_patch_dir):
        full_path = pjoin(unix_patch_dir, patch_file)
        with open(full_path, "r") as f:
            lines = f.readlines()
        lines[1] = lines[1].replace(".updated", "")
        with open(full_path, "w") as f:
            f.writelines(lines)

def collect_unix_patches(container, bug_id):
    patch_dir_name = "unix_patches"
    collect_unix_patches_helper(container, bug_id, patch_dir_name)


def collect_unix_patches_w_context(container, bug_id):
    patch_dir_name = "unix_patches_w_context"
    collect_unix_patches_helper(container, bug_id, patch_dir_name)
    

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
        
        subject_lower = subject.lower()
        container = f"vulnloc-fuzzrepairvalidate-{subject_lower}-{bug_id}-TP1-CP1-0"

        collect_unix_patches(container, bug_id)
        collect_unix_patches_w_context(container, bug_id)

if __name__ == "__main__":
    main()
