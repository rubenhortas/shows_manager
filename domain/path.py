import os
import re

from config import SEASON_PATH_NAME
from crosscutting.condition_messages import print_exception

# noinspection PyBroadException
try:
    # python 3.5 re. Crashes on minor versions
    FILE_WELL_FORMATTED_PATTERN = re.compile(
        "(?P<season>[\d]{1,2})x(?P<episode>[\d]{1,2})(?P<episode_title>.*)?\.(?P<extension>[\w]{3})", re.UNICODE)
except:
    # python 3 re
    FILE_WELL_FORMATTED_PATTERN = re.compile(
        "(?P<season>[\d]{1,2})x(?P<episode>[\d]{1,2})(?P<episode_title>[\w \-()])?\.(?P<extension>[\w]{3})",
        re.UNICODE)


class Path:
    """
    Path
        Stores the information relative to a file and it's destination path.
    """

    show_name = None
    season = None
    season_path = None
    episode = None
    episode_title = None
    extension = None
    final_destination = None

    def __init__(self, file_name, dest, testing):

        match = FILE_WELL_FORMATTED_PATTERN.search(file_name)
        try:
            if match:
                self.season = match.group("season")
                self.episode = match.group("episode")
                self.episode_title = match.group("episode_title")
                self.extension = match.group("extension")
                self.show_name = file_name.split(self.season)[0].strip()

                name_tmp = "{0}x{1}".format(self.season, self.episode)

                if self.episode_title and (self.episode_title != ""):
                    name_tmp = "{0} - {1}".format(name_tmp, self.episode_title)

                file_final_name = "{0}.{1}".format(name_tmp, self.extension)

                if self.__path_exists(dest):
                    self.season_path = "{0} {1}".format(SEASON_PATH_NAME, self.season)
                    if not self.__season_exists(dest):
                        self.__create_season_dir(dest, testing)

                    self.final_destination = os.path.join(dest, self.show_name, self.season_path, file_final_name)
        except Exception as e:
            print_exception(e)

    def __path_exists(self, path):
        """
        __path_exists(self, path)
            Checks if the path for the show already exists in the destination
            directory.
        Arguments:
            - path: (string) Current destination path for the files.
        """

        destination = os.path.join(path, self.show_name)
        return os.path.isdir(destination)

    def __season_exists(self, path):
        """
        __season_exists(self, path)
            Checks if already exists the path for the season in the
            destiny directory.
        Arguments:
            - path: (string) Current destiny path for the files.
        """

        season_path = os.path.join(path, self.show_name, self.season_path)
        return os.path.isdir(season_path)

    def __create_season_dir(self, path, testing):
        """
        __create_season_dir(self, path)
            Creates the season path for the file in the destination path.
        Arguments:
            - path: (string) Current destiny path for the files.
        """

        season_path = os.path.join(path, self.show_name, self.season_path)

        if not testing:
            os.mkdir(season_path)
