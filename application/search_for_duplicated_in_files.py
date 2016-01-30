#!/usr/bin/env python
# _*_ coding:utf-8 _*

"""
@author:      Rubén Hortas Astariz <http://rubenhortas.blogspot.com>
@contact:     rubenhortas at gmail.com
@github:      http://github.com/rubenhortas
@license:     CC BY-NC-SA 3.0 <http://creativecommons.org/licenses/by-nc-sa/3.0/>
@file:        search_for_duplicated_in_files.py
@interpreter: python3
"""

import difflib
import re
import string

from application.utils.dictionary_utils import increment
from crosscutting.messages_search_for_duplicated_in_files import print_duplicated_msg
from domain.duplicated_item import DuplicatedItem


MATCH_THRESHOLD = 0.90


def search_in_files(in_file, from_file):
    """
    search_in_files(in_file, from_file)
        Searches for coincidences between two files.
        Searches in file 'in_file' coincidences from file 'from_file'.
    Arguments:
        - in_file: (string) File [path and] name.
        - from_file: (string) File [path and] name.
    """

    in_file_content = __get_file_content(in_file)
    from_file_content = __get_file_content(from_file)

    __compare_lists_items(
        from_file_content, in_file_content, from_file, in_file)


def search_in_file(in_file):
    """
    search_in_file(in_file)
        Searches for coincidences inside a file.
    Arguments:
        - in_file: (string) File [path and] name.
    """

    in_file_content = __get_file_content(in_file)

    in_file_content_tmp = in_file_content[:]  # Deep copy

    __compare_lists_items(in_file_content, in_file_content_tmp, in_file, None)


def __get_file_content(file_name):
    """
    __get_file_content(file_name)
        Gets file content as a sorted list. One list item per line.
    Arguments:
        - file_name: (string) File [path and] name.
    """

    file_content = []

    f = open(file_name, encoding="UTF-8", errors="ignore")

    for line in f:
        file_content.append(line.strip())

    f.close()

    return sorted(file_content)


def __compare_lists_items(list1, list2, in_file, from_file):
    """
    __compare_lists_items(list1, list2, from_file)
        Searches if exists every element of list1 in list2
    Arguments:
        - list1: (list) List one.
        - list2: (list) List two.
        - from_file: (string) File containing list2 items.
    """
    duplicated = {}

    for item_list1 in list1:
        matches = 0
        for item_list2 in list2:
            match_ratio = __get_match_ratio(item_list1, item_list2)
            if match_ratio > MATCH_THRESHOLD:
                matches = matches + 1
                if from_file or (matches > 1):
                    duplicated_item = DuplicatedItem(item_list2, match_ratio)
                    increment(duplicated, duplicated_item)
                    # list2.remove(item_list2)

    __print_duplicated_items(
        duplicated, item_list1.strip(), in_file, from_file)


def __get_match_ratio(item1, item2):
    """
    __get_match_ratio(str1, str2)
        Compares two lines.
    Arguments:
        - item1: (line) item one.
        - item2: (line) item two.
    """

    str1 = item1.lower().strip()
    str2 = item2.lower().strip()

    for p in string.punctuation:
        str1.replace(p, '')
        str2.replace(p, '')

    # Replace multiple spaces for one space
    str1 = re.sub('\s+', str1, ' ')
    str2 = re.sub('\s+', str2, ' ')

    match_ratio = difflib.SequenceMatcher(None, str1, str2).ratio()

    return match_ratio


def __print_duplicated_items(duplicated_items, item1, in_file, from_file):
    for duplicated_item in duplicated_items:
        print_duplicated_msg(
            item1, duplicated_item.name, in_file, from_file, duplicated_item.match_ratio, duplicated_items[duplicated_item])
