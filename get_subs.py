import argparse
import os
import signal

from application.get_subs import load_plugins
from application.get_subs_plugins.get_sub_plugin import execute_plugin
from application.utils.python_utils import exit_signal_handler
from application.utils.python_utils import get_interpreter_version
from config import SHOWS_PATHS
from crosscutting.condition_messages import print_error, print_info
from crosscutting.constants import REQUIRED_PYTHON_VERSION
from domain.utils.file_handler import is_video, get_videos


def _get_shows_paths_files():
    video_files = []

    for path in SHOWS_PATHS:
        if os.path.exists(path):
            videos = get_videos(path)
            # TODO: Test this
            video_files.append(list(videos))
        else:
            print_error("{0} does not exists".format(path))

    return video_files


def _get_video_files_from_args(files):
    video_files = []

    for f in files:
        if is_video(f):
            video_files.append(f)
        else:
            print_error("{0} is not a video".format(f))

    return video_files

if __name__ == "__main__":
    video_files = []

    signal.signal(signal.SIGINT, exit_signal_handler)

    interpreter = get_interpreter_version()

    if interpreter == REQUIRED_PYTHON_VERSION:
        parser = argparse.ArgumentParser(description='Download subtitles for shows')

        parser.add_argument('files', metavar='files', nargs='*', help='files to download subtitles')
        parser.add_argument('-l', '--lang', help='subtitles language')

        args = parser.parse_args()

        print_info("Getting subtitles")

        if args.files:
            video_files = _get_video_files_from_args(args.files)

        else:
            video_files = _get_shows_paths_files()

        if len(video_files) > 0:
                plugins_loaded = load_plugins()

                if plugins_loaded:
                    print_info("Downloading subtitles...")

                    for f in video_files:
                        subtitle_found = False

                        for plugin in plugins_loaded:
                            subtitle_found = execute_plugin(plugin, f)
                            if subtitle_found:
                                break

                        if not subtitle_found:
                            print_info("\tSubtitle not found")

        else:
            print_error("No files specified")
else:
    print_error("Requires Python {0}".format(REQUIRED_PYTHON_VERSION))
exit(0)
