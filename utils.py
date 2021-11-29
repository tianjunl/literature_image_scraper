"""
This file includes structural funtions for the scraper project.
"""

import os
import pandas as pd


def SetupPath(proj_dir):
    """
    This function returns all paths that are used in this project
    and create new directories if they do not already exist.
    """
    data_dir = proj_dir + os.sep + "data" + os.sep
    pdf_path = data_dir + "pdf" + os.sep
    output_path = data_dir + "output" + os.sep
    all_image_path = output_path + "all_image" + os.sep
    detect_path = all_image_path + "detected" + os.sep
    list_path = output_path + "lists" + os.sep
    cache_path = output_path + "cache" + os.sep

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(all_image_path):
        os.mkdir(all_image_path)
    if not os.path.exists(detect_path):
        os.mkdir(detect_path)
    if not os.path.exists(list_path):
        os.mkdir(list_path)
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

    return (
        data_dir,
        pdf_path,
        output_path,
        all_image_path,
        detect_path,
        list_path,
        cache_path,
    )


def SetupLists(pdf_files, file_num_start):
    """
    This function initiates DataFrames for image information, 
    the skip list of scraping and the complete file list.
    """
    image_info = pd.DataFrame(
        {
            "image_name": [],
            "image_type": [],
            "image_bytes": [],
            "object_detected": [],
            "cercus": [],
            "cerci": [],
            "earwig": [],
            "file_number": [],
            "page_number": [],
            "page_total": [],
            "file_name": [],
        }
    )

    skip_list = pd.DataFrame({"file_number": [], "page_total": [], "file_name": [],})

    file_list = pd.DataFrame(
        {
            "number": range(file_num_start, len(pdf_files) + file_num_start),
            "file_name": pdf_files,
        }
    )

    return image_info, skip_list, file_list
