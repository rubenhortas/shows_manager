#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
@author:  Rubén Hortas Astariz <http://rubenhortas.blogspot.com>
@contact: rubenhortas at gmail.com
@github:  http://github.com/rubenhortas
@license: CC BY-NC-SA 3.0 <http://creativecommons.org/licenses/by-nc-sa/3.0/>
@file:    Video.py
"""

import os
import re

from crosscutting import Messages

from .Episode import Episode
from .File import File


EXPANDED_NAMES = {
    # American Horror Story
    "americanhstory": "American Horror Story",
    "ahs":            "American Horror Story",
    "americanstory":  "American Horror Story",

    # Arrow
    "arr": "Arrow",

    # Bates Motel
    "bmotel":        "Bates Motel",
    "bamotel":       "Bates Motel",
    "batesmotel":    "Bates Motel",

    # Boardwalk Empire
    "booardempire":       "Boardwalk Empire",
    "boardwalkempire":   "Boardwalk Empire",
    "boarempire":        "Boardwalk Empire",

    # Bob"s Burgers
    "bobs burgers":  "Bob\"s Burgers",

    # Castle
    "cas": "Castle",

    # Doctor Who
    "doctorwho":     "Doctor Who",

    # Érase una vez
    "erasevez":      "Érase una vez (Once upon a time)",
    "erase una vez": "Érase una vez (Once upon a time)",

    # El mentalista
    "ementalista":   "El mentalista",
    "mentalista":    "El mentalista",

    # Elementary
    "ele":      "Elementary",
    "elem":     "Elementary",
    "eleme":    "Elementary",
    "elmntry":  "Elementary",

    # Marvel"s Agents of SHIELD
    "marvel\"s agents of s h i e l d":   "Marvel\"s Agents of S.H.I.E.L.D.",
    "marvels agents":                    "Marvel\"s Agents of S.H.I.E.L.D.",


    # Ray Donovan
    "rdonovan": "Ray Donovan",

    # South Park
    "sp":        "South Park",
    "spark":     "South Park",
    "southpark": "South Park",

    # The Big Bang Theory
    "tbbtheory":     "The Big Bang Theory",
    "tbibatheory":   "The Big Bang Theory",

    # The Middle
    "tmidd":        "The Middle",
    "tmid":         "The Middle",
    # The Walking Dead
    "twalkdead":     "The Walking Dead",
    "twalkingdead":  "The Walking Dead",

    # True Detective
    "tdetective":    "True detective",
    "trdetective":   "True detective",
}

EPISODE_TITLE_PATTERN = re.compile("[\w ]*", re.UNICODE)
YEAR_PATTERN = re.compile(" \d{4}")
QUALITIES = ["720p", "1080p"]


class Video(File):
    """
    Class Video
        Stores the data and operations relatives to the video files.
        Child class of cFile.
    """

    episode_in_name = None
    episode_title = None
    original_version = False

    def __init__(self, files_path, file_name, testing):
        super(Video, self).__init__(files_path, file_name, testing)

        if not self.is_well_formated():
            self.__remove_quality()
#             self.__get_episode()
#             if self.__is_serie():
#                 self.__set_ov()
#                 self.__get_show_name()
#                 self.__wrap_year()
#                 self.__expand_show_name()
#                 self.__get_episode_title()
#                 self.__set_show_name()
#                 self._File__translate()
#                 self.f_abs_new_path = os.path.join(self.files_path,
#                                                    self.file_name_new)
#                 self._File__rename()

    def __remove_quality(self):
        """
        __remove_quality(self)
            Removes video quality from file name.
        """

        for quality in QUALITIES:
            if quality in self.file_name:
                self.file_name = self.file_name.replace(quality, "")

        self.file_name = self.file_name.replace("..", ".")
        self.file_name = self.file_name.strip()

#     def __get_episode(self):
#         """
#         __get_episode(self)
#             Retrieves and stores the data relative to the season and
#             episode.
#         """
#         this_episode = Episode(self.file_name)
#
#         # If is a serie (movies doesn"t have episodes)
#         if this_episode.episode_in_name:
#             self.episode_in_name = this_episode.episode_in_name
#             self.episode = this_episode.episode
#             self.new_file_name = self.file_name.replace(self.episode_in_name,
#                                                         self.episode)
#
#     def __is_serie(self):
#         """
#         __is_serie(self)
#             Returns if the video file is a serie.
#         """
#
#         if self.episode_in_name:
#             return True
#         else:
#             return False
#
#     def __get_show_name(self):
#         """
#         __get_show_name(self)
#             Gets the show name and if it's in original version.
#         """
#
#         self.extension = os.path.splitext(self.file_name)[1]
#         file_name = os.path.splitext(self.file_name)[0]
#
#         list_file_name = file_name.split(self.episode_in_name)
#
#         show_name = list_file_name[0]
#         show_name = show_name.replace(".", " ")
#         show_name = show_name.strip()
#
#         self.show_name = show_name
#
#     def __expand_show_name(self):
#         """
#         __expand_show_name(self)
#             Expands some serie titles.
#         """
#
#         if self.show_name.lower() in EXPANDED_NAMES:
#             self.show_name = EXPANDED_NAMES.get(self.show_name.lower())
#
#     def __get_episode_title(self):
#
#         file_name = os.path.splitext(self.file_name)[0]
#
#         list_file_name = file_name.split(self.episode_in_name)
#
#         show_name = list_file_name[1]
#
#         if show_name:
#             title_match = EPISODE_TITLE_PATTERN.search(show_name)
#
#             if title_match:
#                 episode_title = title_match.group(0).strip()
#
#                 if episode_title != "":
#                     self.episode_title = episode_title
#
#     def __set_ov(self):
#         """
#         __set_ov(self)
#             Sets if the file is in Original Version.
#         """
#
#         # Get and set if the file is in original version
#         if "newpct" not in self.file_name:
#             self.original_version = True
#
#     def __wrap_year(self):
#         """
#         __wrap_year(self)
#             Wraps the year (if exists) into parentheses.
#         """
#
#         year_match = YEAR_PATTERN.search(self.show_name)
#
#         if year_match:
#             year_in_show_name = year_match.group(0).lstrip()
#             new_year = "({0})".format(year_in_show_name)
#             self.show_name = self.show_name.replace(
#                 year_in_show_name, new_year)
#
#     def __set_show_name(self):
#         """
#         __set_show_name(self)
#             Sets the output title.
#         """
#
#         # Do not change if the year is in the title
#         if self.episode_in_name not in self.show_name:
#
#             new_file_name = "{0} {1}".format(self.show_name, self.episode)
#
#             if self.episode_title:
#                 new_file_name = "{0} - {1}".format(
#                     new_file_name, self.episode_title)
#
#             if self.original_version:
#                 new_file_name = "{0} (VO)".format(new_file_name)
#
#             self.file_name_new = "{0}{1}".format(new_file_name, self.extension)
#
#         else:
#             self.file_name_new = self.file_name
