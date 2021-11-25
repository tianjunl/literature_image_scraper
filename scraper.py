"""
This file is the main script of this project. 
"""

import os
import io
import argparse
import shutil
import pandas as pd
import fitz
from PIL import Image
from object_detection import CountObjects, DetectObjects
from utils import SetupPath, SetupLists


# read and store user input
parser = argparse.ArgumentParser(description="Literature Image Scraper -v1.0.0")
parser.add_argument(
    "--max_page",
    help="<int> maximal page number (default: 20). "
    + "Files with more pages will not be scraped but documented. ",
    type=int,
    nargs="?",
    default=20,
)
parser.add_argument(
    "--file_start",
    help="<int> starting number for PDF files (default: 1). "
    + "If you want to scrape PDF files in batches and concatenate the results later, "
    + "or to avoid overwriting the previous outputs, please give a integer here "
    + "that is larger than the maximum file number of the previous execution.",
    type=int,
    nargs="?",
    default=1,
)
args = parser.parse_args()


# set up directories
proj_dir = os.getcwd()
(
    data_dir,
    pdf_path,
    output_path,
    all_image_path,
    detect_path,
    list_path,
    cache_path,
) = SetupPath(proj_dir)


# set up CSV lists for output
pdf_files = sorted(os.listdir(pdf_path), key=str.lower)
image_info, skip_list, file_list = SetupLists(pdf_files, args.file_start)
file_list.to_csv(list_path + "file_list.csv")


# scrape through each PDF for images
for file_index, file in enumerate(pdf_files):

    pdf_file = fitz.open(pdf_path + file)
    print(f"[+] Scraping file {file}")

    # to skip scraping the files with more pages than user requested
    if len(pdf_file) > args.max_page:
        new_skip = pd.DataFrame(
            {
                "file_number": [file_index + args.file_start],
                "page_total": [len(pdf_file)],
                "file_name": [file],
            }
        )
        skip_list = skip_list.append(new_skip, ignore_index=True)

    else:
        # scrape through each page
        for page_index in range(len(pdf_file)):

            page = pdf_file[page_index]
            image_list = page.get_images()

            for image_index, img in enumerate(page.get_images()):

                # to exclude images which are page slices (size ratio threshold: 1:4 or 4:1)
                if (img[2] >= 4 * img[3]) or (img[3] >= 4 * img[2]):
                    pass
                else:
                    # extract image and its information
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # record image information and save the image
                    with Image.open(io.BytesIO(image_bytes)) as image_file:
                        image_name = (
                            "file_"
                            + str(file_index + args.file_start)
                            + "_page_"
                            + str(page_index + 1)
                            + "_"
                            + str(image_index + 1)
                        )
                        new_record = pd.DataFrame(
                            {
                                "image_name": [image_name],
                                "image_type": [image_ext],
                                "image_bytes": [len(image_bytes)],
                                "object_detected": [False],
                                "cercus": [0],
                                "cerci": [0],
                                "earwig": [0],
                                "file_number": [file_index + args.file_start],
                                "page_number": [page_index + 1],
                                "page_total": [len(pdf_file)],
                                "file_name": [file],
                            }
                        )
                        image_file.save(all_image_path + image_name + "." + image_ext)

                    # detect objects with a pre-trained model and save detection results
                    detections = DetectObjects(
                        image_name,
                        image_ext,
                        source_path=all_image_path,
                        cache_path=cache_path,
                    )
                    if detections:
                        cercus, cerci, earwig = CountObjects(detections)
                        new_record.iloc[0, 3:7] = [True, cercus, cerci, earwig]

                        # move these target images to another directory
                        shutil.move(
                            all_image_path + image_name + "." + image_ext,
                            detect_path + image_name + "." + image_ext,
                        )
                    else:
                        pass

                    image_info = image_info.append(new_record, ignore_index=True)


# export image information and skip list in CSV format
image_info.to_csv(list_path + "image_info.csv")
skip_list.to_csv(list_path + "skip_list.csv")
