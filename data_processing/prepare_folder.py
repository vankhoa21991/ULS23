import argparse
import os
import shutil
import glob
from tqdm import tqdm
import json

fully_supervised_archives = [
        ["NIH_LN/MED", -1],
        ["NIH_LN/ABD", -1],
        ["DeepLesion3D", 1],
        ["diag_boneCT", 1],
        ["LiTS", 2],
        ["diag_pancreasCT", 1],
        ["kits21-master", 2],
        ["LIDC-IDRI", 1],
        ["LNDb", 1],
        ["MDSC/Task06_Lung", 1],
        ["MDSC/Task07_Pancreas", 2],
        ["MDSC/Task10_Colon", 1],
    ]

partially_supervised_archives = [
        ["CCC18_preprocessed", archives_folder + "/CCC18/combined_anno_ccc18_with_z.csv"],
        ["DeepLesion_preprocessed", archives_folder + "/DeepLesion/DL_info.csv"],
    ]

def main(input_dir, output_dir, split_file):
    os.makedirs(output_dir, exist_ok=True)
    with open(split_file, "r") as f:
        split = json.load(f)
    print("Split file loaded")
    
    # processed
    image_files = glob.glob(input_dir + "/processed_data/*/*/images/*.nii.gz")
    print("Processing {} files".format(len(image_files)))

    # image_files2 = glob.glob(input_dir + "/novel_data/*/images/*.nii.gz")
    # print("Processing {} files".format(len(image_files2)))
    # image_files += image_files2

    # print("Processing {} files".format(len(image_files)))

    for archive in fully_supervised_archives:
        print("Processing archive: {}".format(archive[0]))
        archive_files = [f for f in image_files if archive[0] in f]
        for f in tqdm(archive_files):
            case = f.split("/")[-1].split(".")[0]
            if case in split["train"]:
                shutil.copy(f, output_dir + "/train/images")
            elif case in split["val"]:
                shutil.copy(f, output_dir + "/val/images")
            elif case in split["test"]:
                shutil.copy(f, output_dir + "/test/images")
            else:
                print("Case {} not found in split".format(case))

    return

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--image_folder", type=str, default="data/ULS23/ULS23")
    args.add_argument("--output_folder", type=str, default="data/ULS23/ULS23_processed")
    args.add_argument("--split_file", type=str, default="data/ULS23/ULS23_split.txt")
    args = args.parse_args()
    main(args.image_folder, args.output_folder, args.split_file)

