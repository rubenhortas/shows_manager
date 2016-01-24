#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
@author:  Rubén Hortas Astariz <http://rubenhortas.blogspot.com>
@contact: rubenhortas at gmail.com
@github:  http://github.com/rubenhortas
@license: CC BY-NC-SA 3.0 <http://creativecommons.org/licenses/by-nc-sa/3.0/>
@file:    video.py
"""

import os
import re

from crosscutting.constants import EXPANDED_NAMES
from crosscutting.constants import OV_TRACKERS
from crosscutting.constants import QUALITIES

from .episode import Episode
from .file import File


EPISODE_TITLE_PATTERN = re.compile("[\w ]*", re.UNICODE)


class Video(File):

    episode_in_file_name = None
    episode_title = None
    original_version = False

    def __init__(self, files_path, file_name, testing):
        super(Video, self).__init__(files_path, file_name, testing)

        if not self.is_well_formatted():
            self.__remove_quality()
            self.__get_episode()
            if self.__is_serie():
                self.__set_ov()
                self.__get_show_name()
                self.show_name = self._wrap_year(self.show_name)
                self.__expand_show_name()
                self.__get_episode_title()
                self.__get_new_file_name()
                self._translate()
                self.new_path = os.path.join(self.path, self.new_file_name)
                self._rename(testing)

    def __remove_quality(self):
        """
        __remove_quality(self)
            Removes video quality from file name.
        """

        for quality in QUALITIES:
            if quality in self.file_name:
                self.file_name = self.file_name.replace(quality, "")

        if ".." in self.file_name:
            self.file_name = self.file_name.replace("..", ".")

        self.file_name = self.file_name.strip()

    def __get_episode(self):
        """
        __get_episode(self)
            Retrieves and stores the data relative to the season and
            episode.
        """

        episode = Episode(self.file_name)

        if episode.episode_in_file_name:
            self.episode_in_file_name = episode.episode_in_file_name
            self.episode = episode.episode_formatted
            self.new_file_name = self.file_name.replace(self.episode_in_file_name,
                                                        self.episode)

    def __is_serie(self):
        """
        __is_serie(self)
            Returns if the video file is a serie.
        """

        if self.episode_in_file_name:
            return True
        else:
            return False

    def __set_ov(self):
        """
        __set_ov(self)
            Sets if the file is in Original Version.
        """

        for tracker_name in OV_TRACKERS:
            if tracker_name in self.file_name:
                self.original_version = True
                break

    def __get_show_name(self):
        """
        __get_show_name(self)
            Gets the show name and if it's in original version.
        """

        splitted_file_name = os.path.splitext(self.file_name)

        file_name = splitted_file_name[0]
        self.extension = splitted_file_name[1]

        show_name = file_name.split(self.episode_in_file_name)[0]
        show_name = show_name.replace(".", " ")
        show_name = show_name.strip()

        self.show_name = show_name

    def __expand_show_name(self):
        """
        __expand_show_name(self)
            Expands some serie titles.
        """

        show_name_lower = self.show_name.lower()

        if show_name_lower in EXPANDED_NAMES:
            self.show_name = EXPANDED_NAMES.get(show_name_lower)

    def __get_episode_title(self):

        file_name = os.path.splitext(self.file_name)[0]

        file_name_splitted = file_name.split(self.episode_in_file_name)

        if file_name_splitted[1]:
            match = EPISODE_TITLE_PATTERN.search(file_name_splitted[1])

            if match:
                episode_title = match.group(0).strip()

                if episode_title != "":
                    self.episode_title = episode_title

    def __get_new_file_name(self):
        """
        __set_show_name(self)
            Sets the output title.
        """

        new_file_name = "{0} {1}".format(self.show_name, self.episode)

        if self.episode_title:
            new_file_name = "{0} {1}".format(new_file_name, self.episode_title)

        if self.original_version:
            new_file_name = "{0} {1}".format(
                new_file_name, self.original_version)

        self.new_file_name = "{0}{1}".format(new_file_name, self.extension)
