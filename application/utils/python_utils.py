from sys import version_info


def get_interpreter_version():
    """
    get_interpreter_version()
        Gets the current version of the python interpreter.
    """

    major, minor, micro, release, serial = version_info
    return major


# noinspection PyUnusedLocal
def exit_signal_handler(signal, frame):
    """"
    exit_signal_handler(signal, frame)
        Handles an exit signal.
    Arguments:
        signal: (int) number of signal.
        frame: (string) name of the signal handler.
    """

    exit(0)
