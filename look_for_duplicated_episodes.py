#!/usr/bin/env python
# _*_ coding:utf-8 _*

"""
@author:  Rubén Hortas Astariz <http://rubenhortas.blogspot.com>
@contact: rubenhortas at gmail.com
@github:  http://github.com/rubenhortas
@license: CC BY-NC-SA 3.0 <http://creativecommons.org/licenses/by-nc-sa/3.0/>
@file:    look_for_duplicated_episodes.py
"""

import argparse
import os
import re

from presentation.Messages import exception_msg
from presentation.MessagesCheckForDuplicated import header, bestFile_msg, rm_msg, repeatedFile_msg
from utils.ClearScreen import clear_screen


EPISODE_PATTERN = re.compile("[0-9]{1,2}x[0-9]{1,2}")


def __get_best_quality(path, repeated_episodes):
    """
    __get_best_quality(path, episodes)
        Looking videos with best quality among the repeated videos.
    Arguments:
        - path: Current path for video files.
        - episodes: List of repeated episodes in the path.
    """

    path_files = []
    best_file = None

    for f in os.listdir(path):
        current_file = os.path.join(path, f)
        if os.path.isfile(current_file):
            path_files.append(current_file)

    if path_files != []:
        for episode in repeated_episodes:
            best_file, discarted_files = __get_best_file(episode, path_files)

            bestFile_msg(best_file)
            for f in discarted_files:
                rm_msg(f)
            if not debugging and not testing:
                try:
                    os.remove(f)
                except Exception as e:
                    exception_msg(e)


def __get_best_file(episode, path_files):
    """
    __get_best_file(episode, path_files)
        Gets the best file in the path.
        Returns best file and discarted files.
    Arguments:
        - episode: Current episode for search repeated files.
        - path_files: Files in the path.
    """

    repeated_files = []
    best_file = None
    ov_file = None

    for f in path_files:
        if episode in f:
            repeated_files.append(f)

    for f in repeated_files:
        # Compare size and OV
        if 'VO' in f:
            ov_file = f
        else:
            if ((best_file is None) or
                    (os.path.getsize(best_file) < os.path.getsize(f))):
                best_file = f

    if best_file is None:
        best_file = ov_file

    discarted_files = repeated_files[:]  # deep copy
    discarted_files.remove(best_file)

    return best_file, discarted_files


def __start_scan(episodes_path):

    for root, dirs, files in os.walk(path, topdown=True, onerror=None,
                                     followlinks=False):
        # Sort the dirs
        if len(dirs) > 0:
            dirs = dirs.sort()

        repeated_episodes = []

        if len(files) > 0:
            if len(dirs) == 0:
                episodes = []
                for f in files:
                    episode_match = EPISODE_PATTERN.search(f)
                    if episode_match:
                        current_episode = episode_match.group(0)
                        if current_episode not in episodes:
                            episodes.append(current_episode)
                        else:
                            if(current_episode not in repeated_episodes):
                                repeated_episodes.append(current_episode)
                                relative_episode_path = root.replace(episodes_path, "")
                                repeatedFile_msg(os.path.join(relative_episode_path, current_episode))
        if repeated_episodes != []:
            __get_best_quality(root, repeated_episodes)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Look for repeated chapters')
    parser.add_argument('path', metavar='path',
                        help="path where the files are being sought")
    parser.add_argument("-t", "--test", dest="test",
                        action="store_true",
                        help="Runs a single test showing the output.")

    parser.add_argument("-d", "--debug", dest="debug",
                        action="store_true",
                        help="Shows debug info")

    args = parser.parse_args()

    path = args.path
    testing = args.test
    debugging = args.debug

    clear_screen()

    header(path, debugging, testing)

    __start_scan(path)